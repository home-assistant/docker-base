ARG BASE_IMAGE=ubuntu
ARG UBUNTU_VERSION=24.04
ARG BUILD_FROM=${BASE_IMAGE}:${UBUNTU_VERSION}
FROM ${BUILD_FROM}

# Default ENV
ENV \
    LANG="C.UTF-8" \
    DEBIAN_FRONTEND="noninteractive" \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_CMD_WAIT_FOR_SERVICES=1 \
    S6_SERVICES_READYTIME=50

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Base system
WORKDIR /usr/src

ARG TARGETARCH
ARG BASHIO_VERSION=0.17.5
ARG TEMPIO_VERSION=2024.11.2
ARG S6_OVERLAY_VERSION=3.2.2.0

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
    && apt-get update && apt-get install -y --no-install-recommends \
        bash \
        jq \
        tzdata \
        curl \
        ca-certificates \
        xz-utils \
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
    && curl -L -f -s -o /usr/bin/tempio \
        "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${TEMPIO_ARCH}" \
    && chmod a+x /usr/bin/tempio \
    \
    && mkdir -p /usr/src/bashio \
    && curl -L -f -s "https://github.com/hassio-addons/bashio/archive/v${BASHIO_VERSION}.tar.gz" \
        | tar -xzf - --strip 1 -C /usr/src/bashio \
    && mv /usr/src/bashio/lib /usr/lib/bashio \
    && ln -s /usr/lib/bashio/bashio /usr/bin/bashio \
    \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/src/*

# S6-Overlay
WORKDIR /
ENTRYPOINT ["/init"]

LABEL \
    io.hass.type="base" \
    io.hass.base.name="ubuntu"
