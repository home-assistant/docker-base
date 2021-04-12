ARG BUILD_FROM
# amd64: alpine:${VERSION}
# i386: i386/alpine:${VERSION}
# aarch64: arm64v8/alpine:${VERSION}
# armv7: arm32v7/alpine:${VERSION}
# armhf: arm32v6/alpine:${VERSION}

FROM ${BUILD_FROM}

# Default ENV
ENV \
    LANG="C.UTF-8" \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_CMD_WAIT_FOR_SERVICES=1

# Set shell
SHELL ["/bin/ash", "-o", "pipefail", "-c"]

# Version
ARG \
    BASHIO_VERSION \
    TEMPIO_VERSION \
    S6_OVERLAY_VERSION \
    MIMALLOC_VERSION

# Base system
WORKDIR /usr/src
ARG BUILD_ARCH

RUN \
    set -x \
    && apk add --no-cache \
        bash \
        bind-tools \
        ca-certificates \
        curl \
        jq \
        tzdata \
    \
    && apk add --no-cache --virtual .build-deps \
        build-base \
        cmake \
        git \
    \
    && if [ "${BUILD_ARCH}" = "armv7" ]; then \
            export S6_ARCH="arm"; \
        elif [ "${BUILD_ARCH}" = "i386" ]; then \
            export S6_ARCH="x86"; \
        else \
            export S6_ARCH="${BUILD_ARCH}"; \
        fi \
    \
    && curl -L -f -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${S6_ARCH}.tar.gz" \
        | tar zxvf - -C / \
    && mkdir -p /etc/fix-attrs.d \
    && mkdir -p /etc/services.d \
    \
    && git clone --depth 1 -b v${MIMALLOC_VERSION} "https://github.com/microsoft/mimalloc" /usr/src/mimalloc \
    && mkdir -p /usr/src/mimalloc/build \
    && cd /usr/src/mimalloc/build \
    && cmake .. \
    && make -j "$(nproc)" \
    && make install \
    \
    && mkdir -p /usr/src/bashio \
    && curl -L -f -s "https://github.com/hassio-addons/bashio/archive/v${BASHIO_VERSION}.tar.gz" \
        | tar -xzf - --strip 1 -C /usr/src/bashio \
    && mv /usr/src/bashio/lib /usr/lib/bashio \
    && ln -s /usr/lib/bashio/bashio /usr/bin/bashio \
    \
    && curl -L -f -s -o /usr/bin/tempio \
        "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}" \
    && chmod a+x /usr/bin/tempio \
    \
    && apk del .build-deps \
    && rm -rf /usr/src/*

# S6-Overlay
WORKDIR /
ENTRYPOINT ["/init"]
