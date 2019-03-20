ARG BUILD_VERSION
FROM arm64v8/ubuntu:$BUILD_VERSION

# QEMU for crossbuilds
COPY qemu-aarch64-static /usr/bin/qemu-aarch64-static

# Default ENV
ENV LANG C.UTF-8

# Base system
ARG BASHIO_VERSION=0.1.0
RUN apt-get update && apt-get install -y \
        bash \
        jq \
        tzdata \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    \
    && mkdir -p /tmp/bashio \
    && curl -L -s https://github.com/hassio-addons/bashio/archive/v${BASHIO_VERSION}.tar.gz | tar -xzf - --strip 1 -C /tmp/bashio \
    && mv /tmp/bashio/lib /usr/lib/bashio \
    && ln -s /usr/lib/bashio/bashio /usr/bin/bashio \
    && rm -rf /tmp/bashio
