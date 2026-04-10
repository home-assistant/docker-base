ARG BASE_IMAGE=alpine
ARG ALPINE_VERSION=3.23
ARG BUILD_FROM=${BASE_IMAGE}:${ALPINE_VERSION}

################
# Build jemalloc
################

FROM ${BUILD_FROM} AS jemalloc-build

ENV LANG="C.UTF-8"

SHELL ["/bin/ash", "-o", "pipefail", "-x", "-c"]

ARG JEMALLOC_VERSION=5.3.0

WORKDIR /usr/src/jemalloc

ADD "https://github.com/jemalloc/jemalloc.git#${JEMALLOC_VERSION}" /usr/src/jemalloc

RUN \
    --mount=type=cache,target=/var/cache/apk,sharing=locked \
    apk add --update-cache --virtual .build-deps \
        build-base \
        autoconf \
        git \
    && ./autogen.sh \
        --with-lg-page=16 \
    && make -j "$(nproc)" \
    && make install_lib_shared install_bin \
    && apk del .build-deps \
    && rm -rf /usr/src/*

############################
# Intermediary merge image #
############################

FROM ${BUILD_FROM} AS merge

ENV LANG="C.UTF-8"

SHELL ["/bin/ash", "-o", "pipefail", "-x", "-c"]

ARG S6_OVERLAY_VERSION=3.2.2.0
ARG BASHIO_VERSION=0.17.5
ARG TEMPIO_VERSION=2024.11.2

# Sanity check for later steps
ARG TARGETARCH
RUN \
    if [ -z "${TARGETARCH}" ]; then \
        echo "TARGETARCH is not set, please use Docker BuildKit for the build." && exit 1; \
    fi

# Content created in the build stage
COPY --link --from=jemalloc-build / /

# Base system packages
RUN \
    --mount=type=cache,target=/var/cache/apk,sharing=locked \
    apk add --update-cache \
        bash \
        bind-tools \
        ca-certificates \
        curl \
        jq \
        libstdc++ \
        tzdata \
        xz

# S6-Overlay
ADD --unpack=true "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz" /
ADD --unpack=true "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-arch.tar.xz" /
ADD --unpack=true "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-noarch.tar.xz" /

# bashio
ADD --unpack=true "https://github.com/hassio-addons/bashio/archive/v${BASHIO_VERSION}.tar.gz" /usr/src/bashio

WORKDIR /usr/src/bashio

# Install bashio
RUN \
    mv /usr/src/bashio/bashio-*/lib /usr/lib/bashio \
    && ln -s /usr/lib/bashio/bashio /usr/bin/bashio

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
    && rm -rf /usr/src/bashio

# Root filesystem
COPY rootfs /

#########################
# Final flattened image #
#########################

# Inherit config from the original base image
FROM ${BUILD_FROM}

# Copy everything from the merged build
COPY --from=merge / /

# S6-Overlay entrypoint
ENTRYPOINT ["/init"]

# Set shell
SHELL ["/bin/ash", "-o", "pipefail", "-c"]

# Default env for S6 and Python/uv
ENV \
    LANG="C.UTF-8" \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_CMD_WAIT_FOR_SERVICES=1 \
    S6_SERVICES_READYTIME=50 \
    UV_EXTRA_INDEX_URL="https://wheels.home-assistant.io/musllinux-index/"

LABEL \
    io.hass.type="base" \
    io.hass.base.name="alpine"
