ARG BUILD_VERSION
FROM i386/alpine:$BUILD_VERSION

RUN apk upgrade --no-cache \
    && apk add --no-cache bash jq tzdata ca-certificates

