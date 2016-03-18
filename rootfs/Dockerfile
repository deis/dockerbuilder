FROM alpine:3.3

RUN apk add --update-cache curl python-dev openssl-dev ca-certificates libffi-dev gcc musl-dev\
    && curl -sSL https://raw.githubusercontent.com/pypa/pip/7.1.2/contrib/get-pip.py | python - \
    && pip install --disable-pip-version-check --no-cache-dir boto3==1.2.6 gcloud==0.11.0 azure-storage==0.30.0 docker-py==1.7.0 \
    && apk del --purge curl \
    && rm -rf /var/cache/apk/*

COPY . /

ENTRYPOINT ["python", "/deploy.py"]
