FROM alpine:3.1

ENV VERSION 0.0.1
ENV GO15VENDOREXPERIMENT 1
ENV CGO_ENABLED 0
ENV LDFLAGS "-s -X main.version=$VERSION"
ENV BINDIR rootfs/bin

WORKDIR /app
ADD dockerbuilder dockerbuilder
CMD /app/dockerbuilder
