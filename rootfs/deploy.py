import docker
import os
import tarfile
import time
import requests
import subprocess


DEBUG = os.environ.get('DEIS_DEBUG') in ('true', '1')


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
registry = os.getenv("DEIS_REGISTRY_SERVICE_HOST") + ":" + os.getenv("DEIS_REGISTRY_SERVICE_PORT")
imageName, imageTag = os.getenv('IMG_NAME').split(":", 1)
repo = registry + "/" + os.getenv('IMG_NAME')
stream = client.build(tag=repo, stream=True, decode=True, rm=True, path='/app')
log_output(stream, True)
print("Pushing to registry")
stream = client.push(registry+'/'+imageName, tag=imageTag, stream=True, insecure_registry=True)
log_output(stream, False)
