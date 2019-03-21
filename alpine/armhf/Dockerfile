ARG BUILD_VERSION
FROM arm32v6/alpine:$BUILD_VERSION

# QEMU for crossbuilds
COPY qemu-arm-static /usr/bin/qemu-arm-static

# Default ENV
ENV LANG C.UTF-8

# Base system
ARG BASHIO_VERSION=0.1.0
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
