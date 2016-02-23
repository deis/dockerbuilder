import docker
import os
import tarfile
import os.path
import boto3
import requests

from botocore.client import Config
from urllib.parse import urlparse


def log_output(stream, decode):
    for chunk in stream:
        if decode:
            stream_chunk = chunk.get('stream')
            if stream_chunk:
                print(stream_chunk.replace('\n', ''))
        else:
            print(chunk.decode('utf-8'))


tar_url = os.getenv('TAR_URL')
if tar_url:
    if os.path.exists("/var/run/secrets/object/store/access-key-id"):
        with open("/var/run/secrets/object/store/access-key-id", encoding='utf-8') as the_file:
            secretId = the_file.read().strip()
        with open("/var/run/secrets/object/store/access-secret-key", encoding='utf-8') as the_file:
            secretKey = the_file.read().strip()
        url = urlparse(tar_url)
        hosturl = url.scheme + "://" + url.netloc
        s3 = boto3.client('s3', config=Config(signature_version='s3v4'),
                          endpoint_url=hosturl,
                          aws_access_key_id=secretId,
                          aws_secret_access_key=secretKey,
                          region_name=os.environ.get('REGION', 'us-east-1'))
        bucket = url.path.split('/')[1]
        key = ('/').join(url.path.split('/')[2:])
        s3.download_file(bucket, key, 'apptar')
    else:
        r = requests.get(tar_url)
        with open("apptar", "wb") as app:
            app.write(r.content)

print("download tar file complete")
with tarfile.open("apptar", "r:gz") as tar:
    tar.extractall("/app/")
print("extracting tar file complete")
client = docker.Client(version='auto')
registry = os.getenv("DEIS_REGISTRY_SERVICE_HOST") + ":" + os.getenv("DEIS_REGISTRY_SERVICE_PORT")
imageName, imageTag = os.getenv('IMG_NAME').split(":", 1)
repo = registry + "/" + os.getenv('IMG_NAME')
stream = client.build(tag=repo, stream=True, decode=True, rm=True, path='/app')
log_output(stream, True)
print("pushing to registry")
stream = client.push(registry+'/'+imageName, tag=imageTag, stream=True, insecure_registry=True)
log_output(stream, False)
