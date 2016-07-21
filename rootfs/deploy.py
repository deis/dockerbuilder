import docker
import os
import tarfile
import time
import requests
import subprocess

DEBUG = os.environ.get('DEIS_DEBUG') in ('true', '1')
regsitryLocation = os.getenv('DEIS_REGISTRY_LOCATION', 'on-cluster')


def log_output(stream, decode):
    error = False
    for chunk in stream:
        if 'error' in chunk:
            error = True
            if isinstance(chunk, basestring):  # Change "basestring" to "str" for Python3
                print(chunk.decode('utf-8'))
            else:
                print(chunk['error'].decode('utf-8'))
        elif decode:
            stream_chunk = chunk.get('stream')
            if stream_chunk:
                stream_chunk = stream_chunk.encode('utf-8').strip()
                print(stream_chunk.replace('\n', ''))
        elif DEBUG:
            print(chunk.decode('utf-8'))
    if error:
        # HACK: delay so stderr is logged before this dockerbuilder pod exits.
        time.sleep(3)
        exit(1)


def log(msg):
    if DEBUG:
        print(msg)


def get_registry_name():
    hostname = os.getenv('DEIS_REGISTRY_HOSTNAME', "").replace("https://", "").replace("http://", "")
    if regsitryLocation == "off-cluster":
        organization = os.getenv('DEIS_REGISTRY_ORGANIZATION')
        regName = ""
        # empty hostname means dockerhub and hence no need to prefix the image
        if hostname != "":
            regName = hostname + "/"
        # Registries may have organizations/namespaces under them which needs to
        # be prefixed to the image
        if organization != "":
            regName = regName + organization
        return regName
    elif regsitryLocation == "ecr":
        return hostname
    elif regsitryLocation == "gcr":
        return hostname+"/"+os.getenv('DEIS_REGISTRY_GCS_PROJ_ID')
    else:
        return os.getenv("DEIS_REGISTRY_SERVICE_HOST") + ":" + os.getenv("DEIS_REGISTRY_SERVICE_PORT")


def docker_push(client, repo, tag):
    if regsitryLocation != "on-cluster":
        hostname = os.getenv('DEIS_REGISTRY_HOSTNAME', 'https://index.docker.io/v1/')
        auth_config = {
            'username': os.getenv('DEIS_REGISTRY_USERNAME'),
            'password': os.getenv('DEIS_REGISTRY_PASSWORD'),
            'serveraddress': hostname,
        }
        return client.push(repo, tag=tag, stream=True, auth_config=auth_config)
    else:
        return client.push(repo, tag=tag, stream=True)


def download_file(tar_path):
    os.putenv('BUCKET_FILE', "/var/run/secrets/deis/objectstore/creds/builder-bucket")
    if os.getenv('BUILDER_STORAGE') == "minio":
        os.makedirs("/tmp/objectstore/minio")
        bucketFile = open('/tmp/objectstore/minio/builder-bucket', 'w')
        bucketFile.write('git')
        bucketFile.close()
        os.putenv('BUCKET_FILE', "/tmp/objectstore/minio/builder-bucket")
    elif os.getenv('BUILDER_STORAGE') in ["azure", "swift"]:
        os.putenv('CONTAINER_FILE', "/var/run/secrets/deis/objectstore/creds/builder-container")
    command = ["objstorage", "--storage-type="+os.getenv('BUILDER_STORAGE'), "download", tar_path, "apptar"]
    subprocess.check_call(command)

tar_path = os.getenv('TAR_PATH')
if tar_path:
    if os.path.exists("/var/run/secrets/deis/objectstore/creds/"):
        download_file(tar_path)
    else:
        r = requests.get(tar_path)
        with open("apptar", "wb") as app:
            app.write(r.content)

log("download tar file complete")
with tarfile.open("apptar", "r:gz") as tar:
    tar.extractall("/app/")
log("extracting tar file complete")
client = docker.Client(version='auto')
registry = get_registry_name()
imageName, imageTag = os.getenv('IMG_NAME').split(":", 1)
repo = registry + "/" + os.getenv('IMG_NAME')
stream = client.build(tag=repo, stream=True, decode=True, rm=True, path='/app')
log_output(stream, True)
print("Pushing to registry")
stream = docker_push(client, registry+'/'+imageName, imageTag)
log_output(stream, False)
