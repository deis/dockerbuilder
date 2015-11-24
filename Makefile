# Short name: Short name, following [a-zA-Z_], used all over the place.
# Some uses for short name:
# - Docker image name
# - Kubernetes service, rc, pod, secret, volume names
SHORT_NAME := dockerbuilder

# Enable vendor/ directory support.
export GO15VENDOREXPERIMENT=1

# SemVer with build information is defined in the SemVer 2 spec, but Docker
# doesn't allow +, so we use -.
VERSION := 0.0.1-$(shell date "+%Y%m%d%H%M%S")

# Common flags passed into Go's linker.
LDFLAGS := "-s -X main.version=${VERSION}"

# Docker Root FS
BINDIR := ./rootfs

# Legacy support for DEV_REGISTRY, plus new support for DEIS_REGISTRY.
DEV_REGISTRY ?= $(eval docker-machine ip deis):5000
DEIS_REGISTY ?= ${DEV_REGISTRY}

# Kubernetes-specific information for RC, Service, and Image.
RC := manifests/deis-${SHORT_NAME}-rc.yaml
SVC := manifests/deis-${SHORT_NAME}-service.yaml
IMAGE := deis/${SHORT_NAME}:${VERSION}

all:
	@echo "Use a Makefile to control top-level building of the project."

# This illustrates a two-stage Docker build. docker-compile runs inside of
# the Docker environment. Other alternatives are cross-compiling, doing
# the build as a `docker build`.
#
# Aaron (11/24/2015): doesn't work because it can't resolve external Go dependencies. Use build-alpine instead
build:
	mkdir -p ${BINDIR}/bin
	docker run --rm -v ${PWD}:/app -w /app golang:1.5.1 make docker-compile

build-alpine:
	docker run --rm -it -e GO15VENDOREXPERIMENT=1 -v $$GOPATH:/gopath -e GOPATH=/gopath -e CGO_ENABLED=0 -w /gopath/src/github.com/deis/dockerbuilder golang:1.5.1 go build -o /gopath/src/github.com/deis/dockerbuilder/dockerbuilder -a -installsuffix cgo -ldflags ${LDFLAGS}

# For cases where build is run inside of a container.
docker-compile:
	go build -o ${BINDIR}/bin/boot -a -installsuffix cgo -ldflags ${LDFLAGS} boot.go

# For cases where we're building from local
# We also alter the RC file to set the image name.
docker-build: build-alpine
	docker build --rm -t ${IMAGE} .

# Push to a registry that Kubernetes can access.
docker-push:
	docker push ${IMAGE}

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

# builds a mc client (https://github.com/minio/mc) for use in an alpine:3.1 docker image.
# assumes that $GOPATH/src/github.com/minio/mc exists. to get it, run go get github.com/minio/mc
build-mc-alpine:
	docker run --rm -it -e GO15VENDOREXPERIMENT=1 -v $$GOPATH:/gopath -e GOPATH=/gopath -e CGO_ENABLED=0 -w /gopath/src/github.com/minio/mc golang:1.5.1 go build -o /gopath/src/github.com/minio/mc/mc
	cp $$GOPATH/src/github.com/minio/mc/mc ./rootfs/bin/mc
	rm $$GOPATH/src/github.com/minio/mc/mc

.PHONY: all build docker-compile kube-up kube-down deploy
