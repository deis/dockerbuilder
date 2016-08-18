SHORT_NAME := dockerbuilder
DEIS_REGISTY ?= quay.io/
IMAGE_PREFIX ?= deis

include versioning.mk

# For cases where we're building from local
docker-build:
	docker build --rm -t ${IMAGE} rootfs
	docker tag ${IMAGE} ${MUTABLE_IMAGE}

test:
	@echo "Implement functional tests in _tests directory"

.PHONY: all build docker-compile kube-up kube-down deploy
