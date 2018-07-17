ARG BUILD_VERSION
FROM arm32v6/alpine:$BUILD_VERSION

COPY qemu-arm-static /usr/bin/qemu-arm-static
RUN apk upgrade --no-cache \
    && apk add --no-cache bash jq tzdata ca-certificates

