FROM alpine:3.3

RUN apk add --update-cache curl python-dev openssl-dev ca-certificates libffi-dev gcc musl-dev \
    && curl -sSL https://bootstrap.pypa.io/get-pip.py | python - pip==8.1.1 \
    && pip install --disable-pip-version-check --no-cache-dir boto3==1.2.6 gcloud==0.11.0 azure-storage==0.30.0 docker-py==1.7.2 \
    && apk del --purge curl \
    && rm -rf /var/cache/apk/*

COPY . /

ENTRYPOINT ["python", "/deploy.py"]
