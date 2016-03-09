FROM alpine:3.3

RUN apk add --update-cache curl python3 openssl ca-certificates \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && curl -sSL https://bootstrap.pypa.io/get-pip.py | python - \
    && pip install --disable-pip-version-check --no-cache-dir boto3==1.2.3 boto==2.38.0 docker-py==1.7.0 \
    && apk del --purge curl \
    && rm -rf /var/cache/apk/*

COPY . /

ENTRYPOINT ["python", "/deploy.py"]
