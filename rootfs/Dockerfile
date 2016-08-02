FROM quay.io/deis/base:0.3.0

RUN apt-get update \
	&& apt-get install -y \
		gcc \
		git \
		libffi6 \
		libffi-dev \
		libssl1.0.0 \
		libssl-dev \
		musl \
		musl-dev \
		python \
		python-dev \
		--no-install-recommends \
	&& curl -sSL https://bootstrap.pypa.io/get-pip.py | python - pip==8.1.2 \
	&& pip install --disable-pip-version-check --no-cache-dir git+https://github.com/docker/docker-py.git@9b63bed6a0b5185b043e85df8c49d86d2c048aa1 \
	&& apt-get remove -y --auto-remove --purge \
		gcc \
		libffi-dev \
		libssl-dev \
		musl-dev \
		python-dev \
		git \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man /usr/share/doc

ADD https://storage.googleapis.com/object-storage-cli/bb8e054/objstorage-bb8e054-linux-amd64 /bin/objstorage
RUN chmod +x /bin/objstorage

COPY . /

CMD ["python", "/deploy.py"]
