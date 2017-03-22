SHORT_NAME := dockerbuilder
DEIS_REGISTRY ?= quay.io/
IMAGE_PREFIX ?= deis

include versioning.mk

DEV_ENV_IMAGE := quay.io/deis/python-dev:v0.1.0
DEV_ENV_WORK_DIR := /app
DEV_ENV_PREFIX := docker run --rm -v ${CURDIR}/rootfs:${DEV_ENV_WORK_DIR} -w ${DEV_ENV_WORK_DIR}
DEV_ENV_CMD := ${DEV_ENV_PREFIX} ${DEV_ENV_IMAGE}

# For cases where we're building from local
docker-build:
	docker build ${DOCKER_BUILD_FLAGS} -t ${IMAGE} rootfs
	docker tag ${IMAGE} ${MUTABLE_IMAGE}

test: test-style test-functional

test-style:
	${DEV_ENV_CMD} flake8 --show-source --config=setup.cfg .

test-functional:
	@echo "Implement functional tests in _tests directory"

.PHONY: all docker-build test test-style test-functional
