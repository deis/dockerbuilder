FROM alpine:3.1

ENV VERSION 0.0.1
ENV GO15VENDOREXPERIMENT 1
ENV CGO_ENABLED 0
ENV LDFLAGS "-s -X main.version=$VERSION"
ENV BINDIR rootfs/bin

RUN apk add --update curl bash && rm -rf /var/cache/apk/* && curl -L https://get.docker.com/builds/Linux/x86_64/docker-latest > /usr/bin/docker && chmod +x /usr/bin/docker

WORKDIR /app
ADD dockerbuilder dockerbuilder
CMD /app/dockerbuilder
