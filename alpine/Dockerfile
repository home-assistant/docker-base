ARG BUILD_FROM
# amd64: alpine:${VERSION}
# aarch64: arm64v8/alpine:${VERSION}

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

# Build Args
ARG \
    BASHIO_VERSION \
    TEMPIO_VERSION \
    S6_OVERLAY_VERSION \
    JEMALLOC_VERSION

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
        libstdc++ \
        tzdata \
        xz \
    \
    && apk add --no-cache --virtual .build-deps \
        build-base \
        autoconf \
        git \
    \
    && if [ "${BUILD_ARCH}" = "amd64" ]; then \
            export S6_ARCH="x86_64"; \
        else \
            export S6_ARCH="${BUILD_ARCH}"; \
        fi \
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
        "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}" \
    && chmod a+x /usr/bin/tempio \
    \
    && apk del .build-deps \
    && rm -rf /usr/src/*

# Root filesystem
COPY rootfs /

# S6-Overlay
WORKDIR /
ENTRYPOINT ["/init"]
