FROM alpine:3.3

RUN apk add --update-cache curl bash openssl sudo python3 && rm -rf /var/cache/apk/*
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN curl -sSL https://raw.githubusercontent.com/pypa/pip/7.1.2/contrib/get-pip.py | python -
RUN pip install --disable-pip-version-check --no-cache-dir docker-py==1.7.0
RUN pip install boto3==1.2.3

COPY . /

ENTRYPOINT ["python", "/deploy.py"]
