ARG BUILD_VERSION
FROM alpine:$BUILD_VERSION

# Default ENV
ENV \
    LANG="C.UTF-8" \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_CMD_WAIT_FOR_SERVICES=1

# Set shell
SHELL ["/bin/ash", "-o", "pipefail", "-c"]

# Base system
ARG BASHIO_VERSION=0.9.0
ARG S6_OVERLAY_VERSION=2.0.0.1
RUN apk add --no-cache \
        bash \
        jq \
        tzdata \
        ca-certificates \
        curl \
        bind-tools \
    \
    && curl -L -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-amd64.tar.gz" \
        | tar zxvf - -C / \
    && mkdir -p /etc/fix-attrs.d \
    && mkdir -p /etc/services.d \
    \
    && mkdir -p /tmp/bashio \
    && curl -L -s https://github.com/hassio-addons/bashio/archive/v${BASHIO_VERSION}.tar.gz | tar -xzf - --strip 1 -C /tmp/bashio \
    && mv /tmp/bashio/lib /usr/lib/bashio \
    && ln -s /usr/lib/bashio/bashio /usr/bin/bashio \
    && rm -rf /tmp/bashio

# S6-Overlay
ENTRYPOINT ["/init"]
