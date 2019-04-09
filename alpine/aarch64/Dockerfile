ARG BUILD_VERSION
FROM arm64v8/alpine:$BUILD_VERSION

# QEMU for crossbuilds
COPY qemu-aarch64-static /usr/bin/qemu-aarch64-static

# Default ENV
ENV LANG C.UTF-8

# Base system
ARG BASHIO_VERSION=0.2.0
RUN apk upgrade --no-cache \
    && apk add --no-cache \
        bash \
        jq \
        tzdata \
        ca-certificates \
        curl \
    \
    && mkdir -p /tmp/bashio \
    && curl -L -s https://github.com/hassio-addons/bashio/archive/v${BASHIO_VERSION}.tar.gz | tar -xzf - --strip 1 -C /tmp/bashio \
    && mv /tmp/bashio/lib /usr/lib/bashio \
    && ln -s /usr/lib/bashio/bashio /usr/bin/bashio \
    && rm -rf /tmp/bashio
