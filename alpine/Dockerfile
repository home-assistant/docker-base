ARG BASE_IMAGE=alpine
ARG ALPINE_VERSION=3.23
ARG BUILD_FROM=${BASE_IMAGE}:${ALPINE_VERSION}
FROM ${BUILD_FROM}

# Default ENV
ENV \
    LANG="C.UTF-8" \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_CMD_WAIT_FOR_SERVICES=1 \
    S6_SERVICES_READYTIME=50 \
    UV_EXTRA_INDEX_URL="https://wheels.home-assistant.io/musllinux-index/"

# Set shell
SHELL ["/bin/ash", "-o", "pipefail", "-c"]

# Base system
WORKDIR /usr/src

ARG TARGETARCH
ARG BASHIO_VERSION=0.17.5
ARG TEMPIO_VERSION=2024.11.2
ARG S6_OVERLAY_VERSION=3.2.2.0
ARG JEMALLOC_VERSION=5.3.0

RUN \
    set -x \
    && if [ -z "${TARGETARCH}" ]; then \
            case "$(uname -m)" in \
                x86_64) TARGETARCH="amd64" ;; \
                aarch64|arm64) TARGETARCH="arm64" ;; \
                *) echo "Unsupported architecture: $(uname -m)" && exit 1 ;; \
            esac; \
        fi \
    && case "${TARGETARCH}" in \
            amd64) TEMPIO_ARCH="amd64"; S6_ARCH="x86_64" ;; \
            arm64) TEMPIO_ARCH="aarch64"; S6_ARCH="aarch64" ;; \
            *) echo "Unsupported TARGETARCH: ${TARGETARCH}" && exit 1 ;; \
        esac \
    && apk add --no-cache \
        bash \
        bind-tools \
        ca-certificates \
        curl \
        jq \
        libstdc++ \
        tzdata \
        xz \
    \
    && apk add --no-cache --virtual .build-deps \
        build-base \
        autoconf \
        git \
    \
    && curl -L -f -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${S6_ARCH}.tar.xz" \
        | tar Jxvf - -C / \
    && curl -L -f -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz" \
        | tar Jxvf - -C / \
    && curl -L -f -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-arch.tar.xz" \
        | tar Jxvf - -C / \
    && curl -L -f -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-noarch.tar.xz" \
        | tar Jxvf - -C / \
    && mkdir -p /etc/fix-attrs.d \
    && mkdir -p /etc/services.d \
    \
    && git clone "https://github.com/jemalloc/jemalloc" /usr/src/jemalloc \
    && cd /usr/src/jemalloc \
    && git checkout ${JEMALLOC_VERSION} \
    && ./autogen.sh \
        --with-lg-page=16 \
    && make -j "$(nproc)" \
    && make install_lib_shared install_bin \
    \
    && mkdir -p /usr/src/bashio \
    && curl -L -f -s "https://github.com/hassio-addons/bashio/archive/v${BASHIO_VERSION}.tar.gz" \
        | tar -xzf - --strip 1 -C /usr/src/bashio \
    && mv /usr/src/bashio/lib /usr/lib/bashio \
    && ln -s /usr/lib/bashio/bashio /usr/bin/bashio \
    \
    && curl -L -f -s -o /usr/bin/tempio \
        "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${TEMPIO_ARCH}" \
    && chmod a+x /usr/bin/tempio \
    \
    && apk del .build-deps \
    && rm -rf /usr/src/*

# Root filesystem
COPY rootfs /

# S6-Overlay
WORKDIR /
ENTRYPOINT ["/init"]

LABEL \
    io.hass.type="base" \
    io.hass.base.name="alpine"
