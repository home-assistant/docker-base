ARG BUILD_VERSION
FROM arm32v6/alpine:$BUILD_VERSION

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
ARG TEMPIO_VERSION=2020.10.2
ARG S6_OVERLAY_VERSION=2.1.0.2
ARG JEMALLOC_VERSION=5.2.1

# Base system
WORKDIR /usr/src
ARG BUILD_ARCH

# hadolint ignore=SC2086
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
        patch \
        pkgconf \
    \
    && mkdir -p /usr/src/tzdata \
    && curl -L -f -s "https://www.iana.org/time-zones/repository/releases/tzcode2020c.tar.gz" \
        | tar -xzf - -C /usr/src/tzdata \
    && curl -L -f -s "https://www.iana.org/time-zones/repository/releases/tzdata2020c.tar.gz" \
        | tar -xzf - -C /usr/src/tzdata \
    && cd /usr/src/tzdata \
    && make CFLAGS="-DHAVE_STDINT_H=1" TZDIR="/usr/share/zoneinfo" \
    && _timezones="africa antarctica asia australasia europe northamerica southamerica etcetera backward factory" \
    && ./zic -b fat -y ./yearistype -d /usr/share/zoneinfo $_timezones \
    && ./zic -b fat -y ./yearistype -d /usr/share/zoneinfo/right -L leapseconds $_timezones \
    && ./zic -b fat -y ./yearistype -d /usr/share/zoneinfo -p America/New_York \
    && install -m444 -t /usr/share/zoneinfo iso3166.tab zone1970.tab zone.tab \
    && install -m755 zic zdump /usr/sbin \
    && rm -f /usr/share/zoneinfo/localtime \
    \
    && mkdir -p /usr/src/posixtz \
    && cd /usr/src/posixtz \
    && curl -J -L -o posixtz.xz "https://dev.alpinelinux.org/archive/posixtz/posixtz-0.5.tar.xz" \
    && tar xvf posixtz.xz --strip 1 \
    && curl -J -L --retry 5 -o 0001.patch \
        "https://git.alpinelinux.org/aports/plain/main/tzdata/0001-posixtz-ensure-the-file-offset-we-pass-to-lseek-is-o.patch" \
    && curl -J -L --retry 5 -o 0002.patch \
        "https://git.alpinelinux.org/aports/plain/main/tzdata/0002-fix-implicit-declaration-warnings-by-including-strin.patch" \
    && patch -p 2 < 0001.patch \
    && patch -p 2 < 0002.patch \
    && make posixtz \
    && install -Dm755 posixtz /usr/bin/posixtz \
    \
    && curl -L -f -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-armhf.tar.gz" \
        | tar zxvf - -C / \
    && mkdir -p /etc/fix-attrs.d \
    && mkdir -p /etc/services.d \
    \
    && curl -L -f -s "https://github.com/jemalloc/jemalloc/releases/download/${JEMALLOC_VERSION}/jemalloc-${JEMALLOC_VERSION}.tar.bz2" \
        | tar -xjf - -C /usr/src \
    && cd /usr/src/jemalloc-${JEMALLOC_VERSION} \
    && ./configure \
    && make \
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
