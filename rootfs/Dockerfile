FROM quay.io/deis/base:0.2.0

RUN apt-get update \
	&& apt-get install -y \
		gcc \
		libffi6 \
		libffi-dev \
		libssl1.0.0 \
		libssl-dev \
		musl \
		musl-dev \
		python \
		python-dev \
		--no-install-recommends \
	&& curl -sSL https://bootstrap.pypa.io/get-pip.py | python - pip==8.1.1 \
	&& pip install --disable-pip-version-check --no-cache-dir docker-py==1.9.0 \
	&& apt-get remove -y --auto-remove --purge \
		gcc \
		libffi-dev \
		libssl-dev \
		musl-dev \
		python-dev \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man /usr/share/doc

ADD https://storage.googleapis.com/object-storage-cli/bb8e054/objstorage-bb8e054-linux-amd64 /bin/objstorage
RUN chmod +x /bin/objstorage

COPY . /

CMD ["python", "/deploy.py"]
