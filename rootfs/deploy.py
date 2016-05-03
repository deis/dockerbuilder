import docker
import os
import sys
import tarfile
import requests

import boto3
import botocore
import json
from botocore.utils import fix_s3_host
from botocore.client import Config
from oauth2client.service_account import ServiceAccountCredentials
from gcloud.storage.client import Client
from azure.storage.blob import BlockBlobService


DEBUG = os.environ.get('DEIS_DEBUG') in ('true', '1')


def log_output(stream, decode):
    for chunk in stream:
        if decode:
            stream_chunk = chunk.get('stream')
            if stream_chunk:
                print(stream_chunk.replace('\n', ''))
        else:
            print(chunk.decode('utf-8'))

def download_file(tar_path):
    if os.getenv('BUILDER_STORAGE') == "s3":
        with open('/var/run/secrets/deis/objectstore/creds/accesskey', 'r') as access_file:
            AWS_ACCESS_KEY_ID = access_file.read()
        with open('/var/run/secrets/deis/objectstore/creds/secretkey', 'r') as secret_file:
            AWS_SECRET_ACCESS_KEY = secret_file.read()
        with open('/var/run/secrets/deis/objectstore/creds/region', 'r') as region_file:
            AWS_DEFAULT_REGION = region_file.read()

        bucket_name = ""
        with open('/var/run/secrets/deis/objectstore/creds/builder-bucket', 'r') as bucket_file:
            bucket_name = bucket_file.read()

        conn = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_DEFAULT_REGION)
        conn.Bucket(bucket_name).Object(tar_path).download_file('apptar')

    elif os.getenv('BUILDER_STORAGE') == "gcs":
        bucket_name = ""
        with open('/var/run/secrets/deis/objectstore/creds/builder-bucket', 'r') as bucket_file:
            bucket_name = bucket_file.read()
        scopes = ['https://www.googleapis.com/auth/devstorage.full_control']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('/var/run/secrets/deis/objectstore/creds/key.json', scopes=scopes)
        with open('/var/run/secrets/deis/objectstore/creds/key.json') as data_file:
            data = json.load(data_file)
        client = Client(credentials=credentials, project=data['project_id'])
        client.get_bucket(bucket_name).get_blob(tar_path).download_to_filename("apptar")

    elif os.getenv('BUILDER_STORAGE') == "azure":
      with open('/var/run/secrets/deis/objectstore/creds/accountname', 'r') as account_file:
          accountname = account_file.read()
      with open('/var/run/secrets/deis/objectstore/creds/accountkey', 'r') as key_file:
          accountkey = key_file.read()
      with open('/var/run/secrets/deis/objectstore/creds/builder-container', 'r') as container_file:
          container_name = container_file.read()
      block_blob_service = BlockBlobService(account_name=accountname, account_key=accountkey)
      block_blob_service.get_blob_to_path(container_name, tar_path, 'apptar')

    else :
      with open('/var/run/secrets/deis/objectstore/creds/accesskey', 'r') as access_file:
          AWS_ACCESS_KEY_ID = access_file.read()
      with open('/var/run/secrets/deis/objectstore/creds/secretkey', 'r') as secret_file:
          AWS_SECRET_ACCESS_KEY = secret_file.read()

      AWS_DEFAULT_REGION = "us-east-1"
      bucket_name = "git"
      mHost = os.getenv('DEIS_MINIO_SERVICE_HOST')
      mPort = os.getenv('DEIS_MINIO_SERVICE_PORT')
      if mPort == "80" :
      	# If you add port 80 to the end of the endpoint_url, boto3 freaks out.
      	S3_URL = "http://"+mHost
      else :
      	S3_URL="http://"+mHost+":"+mPort

      conn = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_DEFAULT_REGION, endpoint_url=S3_URL, config=Config(signature_version='s3v4'))
      # stop boto3 from automatically changing the endpoint
      conn.meta.client.meta.events.unregister('before-sign.s3', fix_s3_host)

      conn.Bucket(bucket_name).Object(tar_path).download_file('apptar')

tar_path = os.getenv('TAR_PATH')
if tar_path:
    if os.path.exists("/var/run/secrets/deis/objectstore/creds/"):
        download_file(tar_path)
    else:
        r = requests.get(tar_path)
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
if DEBUG:
    log_output(stream, False)
