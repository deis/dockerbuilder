SHORT_NAME := dockerbuilder
DEIS_REGISTY ?= quay.io/
IMAGE_PREFIX ?= deis

include versioning.mk

# For cases where we're building from local
docker-build:
	docker build --rm -t ${IMAGE} rootfs
	docker tag ${IMAGE} ${MUTABLE_IMAGE}

setup-venv:
	@if [ ! -d venv ]; then pyvenv venv && source venv/bin/activate; fi
	pip install --disable-pip-version-check -q -r rootfs/dev_requirements.txt

test: test-style test-functional

test-style:
	cd rootfs && flake8 --show-source --config=setup.cfg .

test-functional:
	@echo "Implement functional tests in _tests directory"

.PHONY: all build docker-compile kube-up kube-down deploy
