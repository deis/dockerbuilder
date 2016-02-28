FROM alpine:3.3

RUN apk add --update-cache curl python3 openssl \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && curl -sSL https://bootstrap.pypa.io/get-pip.py | python - \
    && pip install --disable-pip-version-check --no-cache-dir boto3==1.2.3 docker-py==1.7.2 \
    && apk del --purge curl \
    && rm -rf /var/cache/apk/*

COPY . /

ENTRYPOINT ["python", "/deploy.py"]
