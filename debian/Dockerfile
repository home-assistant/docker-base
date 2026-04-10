ARG BASE_IMAGE=debian
ARG DEBIAN_VERSION=trixie
ARG BUILD_FROM=${BASE_IMAGE}:${DEBIAN_VERSION}-slim
FROM ${BUILD_FROM} AS merge

# Default ENV
ENV \
    LANG="C.UTF-8" \
    DEBIAN_FRONTEND="noninteractive" \
    CURL_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt" \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_CMD_WAIT_FOR_SERVICES=1 \
    S6_SERVICES_READYTIME=50

SHELL ["/bin/bash", "-o", "pipefail", "-x", "-c"]

ARG BASHIO_VERSION=0.17.5
ARG TEMPIO_VERSION=2024.11.2
ARG S6_OVERLAY_VERSION=3.2.2.0

# Sanity check for later steps
ARG TARGETARCH
RUN \
    if [ -z "${TARGETARCH}" ]; then \
        echo "TARGETARCH is not set, please use Docker BuildKit for the build." && exit 1; \
    fi

# Enable APT cache reuse with BuildKit
RUN \
    rm -f /etc/apt/apt.conf.d/docker-clean

# Base system packages
RUN \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
        bash \
        jq \
        tzdata \
        curl \
        ca-certificates \
        xz-utils \
    && mkdir -p /usr/share/man/man1

# S6-Overlay
ADD --unpack=true "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz" /
ADD --unpack=true "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-arch.tar.xz" /
ADD --unpack=true "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-noarch.tar.xz" /

# bashio
ADD --unpack=true "https://github.com/hassio-addons/bashio/archive/v${BASHIO_VERSION}.tar.gz" /usr/src/bashio

WORKDIR /usr/src/bashio

RUN \
    mv /usr/src/bashio/bashio-*/lib /usr/lib/bashio \
    && ln -s /usr/lib/bashio/bashio /usr/bin/bashio \
    && rm -rf /usr/src/bashio

# Arch-specific downloads (tempio and s6-overlay)
RUN \
    case "${TARGETARCH}" in \
        amd64) TEMPIO_ARCH="amd64"; S6_ARCH="x86_64" ;; \
        arm64) TEMPIO_ARCH="aarch64"; S6_ARCH="aarch64" ;; \
        *) echo "Unsupported TARGETARCH: ${TARGETARCH}" && exit 1 ;; \
    esac \
    && curl -L -f -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${S6_ARCH}.tar.xz" \
        | tar Jxvf - -C / \
    && curl -L -f -s -o /usr/bin/tempio \
        "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${TEMPIO_ARCH}" \
    && chmod a+x /usr/bin/tempio

# Touch-ups and cleanup
RUN \
    mkdir -p /etc/fix-attrs.d \
    && mkdir -p /etc/services.d \
    && rm -rf /var/lib/apt/lists/*

#########################
# Final flattened image #
#########################

# Inherit config from the original base image
FROM ${BUILD_FROM}

# Copy everything from the merged build
COPY --from=merge / /

# S6-Overlay
ENTRYPOINT ["/init"]

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Default ENV
ENV \
    LANG="C.UTF-8" \
    DEBIAN_FRONTEND="noninteractive" \
    CURL_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt" \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_CMD_WAIT_FOR_SERVICES=1 \
    S6_SERVICES_READYTIME=50

LABEL \
    io.hass.type="base" \
    io.hass.base.name="debian"
