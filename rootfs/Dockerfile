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
	&& pip install --disable-pip-version-check --no-cache-dir boto3==1.2.6 gcloud==0.11.0 azure-storage==0.30.0 docker-py==1.7.2 \
	&& apt-get remove -y --auto-remove --purge \
		gcc \
		libffi-dev \
		libssl-dev \
		musl-dev \
		python-dev \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man /usr/share/doc

COPY . /

CMD ["python", "/deploy.py"]

ENV WORKFLOW_RELEASE 2.0.0
