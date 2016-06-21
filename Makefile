# Short name: Short name, following [a-zA-Z_], used all over the place.
# Some uses for short name:
# - Docker image name
# - Kubernetes service, rc, pod, secret, volume names
SHORT_NAME := dockerbuilder

# Enable vendor/ directory support.
export GO15VENDOREXPERIMENT=1

# Common flags passed into Go's linker.
LDFLAGS := "-s -X main.version=${VERSION}"

# Docker Root FS
BINDIR := ./rootfs

# Legacy support for DEV_REGISTRY, plus new support for DEIS_REGISTRY.
DEV_REGISTRY ?= $(eval docker-machine ip deis):5000
DEIS_REGISTY ?= ${DEV_REGISTRY}/
IMAGE_PREFIX ?= deis

include versioning.mk

all:
	@echo "Use a Makefile to control top-level building of the project."

# For cases where we're building from local
docker-build:
	docker build --rm -t ${IMAGE} rootfs
	docker tag ${IMAGE} ${MUTABLE_IMAGE}

# Deploy is a Kubernetes-oriented target
deploy: kube-service kube-rc

# Some things, like services, have to be deployed before pods. This is an
# example target. Others could perhaps include kube-secret, kube-volume, etc.
kube-service:
	kubectl create -f ${SVC}

# When possible, we deploy with RCs.
kube-rc:
	kubectl create -f ${RC}

kube-clean:
	kubectl delete rc deis-example

bootstrap:
	@echo Nothing to do.

test:
	@echo "Implement functional tests in _tests directory"

.PHONY: all build docker-compile kube-up kube-down deploy
