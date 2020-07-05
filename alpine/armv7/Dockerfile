ARG BUILD_VERSION
FROM arm32v7/alpine:$BUILD_VERSION

# QEMU for crossbuilds
COPY qemu-arm-static /usr/bin/qemu-arm-static

# Default ENV
ENV \
    LANG="C.UTF-8" \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_CMD_WAIT_FOR_SERVICES=1

# Set shell
SHELL ["/bin/ash", "-o", "pipefail", "-c"]

# Version
ARG BASHIO_VERSION=0.9.0
ARG S6_OVERLAY_VERSION=2.0.0.1
ARG JEMALLOC_VERSION=5.2.1

# Base system
WORKDIR /usr/src
RUN apk add --no-cache \
        bash \
        jq \
        tzdata \
        ca-certificates \
        curl \
        bind-tools \
    \
    && apk add --no-cache --virtual .build-deps \
        build-base \
    \
    && curl -L -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-arm.tar.gz" \
        | tar zxvf - -C / \
    && mkdir -p /etc/fix-attrs.d \
    && mkdir -p /etc/services.d \
    \
    && curl -L -s "https://github.com/jemalloc/jemalloc/releases/download/${JEMALLOC_VERSION}/jemalloc-${JEMALLOC_VERSION}.tar.bz2" \
        | tar -xjf - -C /usr/src \
    && cd /usr/src/jemalloc-${JEMALLOC_VERSION} \
    && ./configure \
    && make \
    && make install \
    \
    && mkdir -p /usr/src/bashio \
    && curl -L -s "https://github.com/hassio-addons/bashio/archive/v${BASHIO_VERSION}.tar.gz" \
        | tar -xzf - --strip 1 -C /usr/src/bashio \
    && mv /usr/src/bashio/lib /usr/lib/bashio \
    && ln -s /usr/lib/bashio/bashio /usr/bin/bashio \
    \
    && apk del .build-deps \
    && rm -rf /usr/src/*

# S6-Overlay
WORKDIR /
ENTRYPOINT ["/init"]
