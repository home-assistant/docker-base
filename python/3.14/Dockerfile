ARG BASE_IMAGE=ghcr.io/home-assistant/base
ARG BASE_VERSION=3.23
ARG BUILD_FROM=${BASE_IMAGE}:${BASE_VERSION}

####################
# Get Python sources
####################

FROM ${BUILD_FROM} AS python-source

ARG PYTHON_VERSION=3.14.4
ARG CERT_IDENTITY=hugo@python.org
ARG CERT_OIDC_ISSUER=https://github.com/login/oauth

SHELL ["/bin/ash", "-o", "pipefail", "-x", "-c"]

WORKDIR /tmp/python-fetch

# Fetch Python source and signatures
ADD "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz" /tmp/python-fetch/python.tar.xz
ADD "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz.sigstore" /tmp/python-fetch/python.tar.xz.sigstore

# Verify Python sources
RUN \
    --mount=type=cache,target=/var/cache/apk,sharing=locked \
    apk add --update-cache --virtual .fetch-deps \
        cosign \
        openssl \
        tar \
        xz \
    && cosign verify-blob \
        --new-bundle-format \
        --certificate-identity "${CERT_IDENTITY}" \
        --certificate-oidc-issuer "${CERT_OIDC_ISSUER}" \
        --bundle python.tar.xz.sigstore \
        python.tar.xz \
    && mkdir -p /usr/src/python \
    && tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
    && apk del .fetch-deps \
    && rm -rf /tmp/python-fetch

##############
# Python build
##############

FROM ${BUILD_FROM} AS build

# Ensure local python is preferred over distribution python
ENV PATH=/usr/local/bin:$PATH

SHELL ["/bin/ash", "-o", "pipefail", "-x", "-c"]

# Install build dependencies
RUN \
    --mount=type=cache,target=/var/cache/apk,sharing=locked \
    apk add --update-cache --virtual .build-deps \
        bluez-dev \
        build-base \
        bzip2-dev \
        coreutils \
        dpkg-dev dpkg \
        expat-dev \
        findutils \
        gdbm-dev \
        libc-dev \
        libffi-dev \
        libtirpc-dev \
        libnsl-dev \
        linux-headers \
        make \
        mpdecimal-dev \
        ncurses-dev \
        openssl \
        openssl-dev \
        patch \
        pax-utils \
        readline-dev \
        sqlite-dev \
        tcl-dev \
        tk \
        tk-dev \
        xz-dev \
        zlib-dev

# Copy with link, so installing deps can run in parallel while downloading sources
COPY --link --from=python-source /usr/src/python /usr/src/python

# Build and install patched Python
RUN \
    --mount=type=bind,source=./patches,target=/usr/src/patches \
    for i in /usr/src/patches/*.patch; do \
        patch -d /usr/src/python -p 1 < "${i}"; done \
    && cd /usr/src/python \
    && gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
    && ./configure \
        --build="$gnuArch" \
        --enable-loadable-sqlite-extensions \
        --enable-optimizations \
        --enable-option-checking=fatal \
        --enable-shared \
        --with-lto \
        --with-system-libmpdec \
        --with-system-expat \
        --without-ensurepip \
        --without-static-libpython \
    && make -j "$(nproc)" \
        LDFLAGS="-Wl,--strip-all" \
        CFLAGS="-fno-semantic-interposition -fno-builtin-malloc -fno-builtin-calloc -fno-builtin-realloc -fno-builtin-free" \
# set thread stack size to 2MB so we don't segfault before we hit sys.getrecursionlimit()
# https://github.com/alpinelinux/aports/commit/2026e1259422d4e0cf92391ca2d3844356c649d0
# https://github.com/alpinelinux/aports/commit/675f1babb7ac89068d32b8f4b4e8bbfbb04c96ac
        EXTRA_CFLAGS="-DTHREAD_STACK_SIZE=0x200000" \
    && make install \
    && apk del .build-deps \
    && rm -rf /usr/src/python

# Search and install runtime dependencies (except tkinter)
RUN \
    --mount=type=cache,target=/var/cache/apk,sharing=locked \
    find /usr/local -type f -executable -not \( -name '*tkinter*' \) -exec scanelf --needed --nobanner --format '%n#p' '{}' ';' \
        | tr ',' '\n' \
        | sort -u \
        | awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
        | xargs -rt apk add --update-cache --virtual .python-rundeps \
    && find /usr/local -depth \
        \( \
            -type d -a \( -name test -o -name tests \) \
        \) -exec rm -rf '{}' +

# Make some useful symlinks that are expected to exist
RUN \
    cd /usr/local/bin \
    && ln -s idle3 idle \
    && ln -s pydoc3 pydoc \
    && ln -s python3 python \
    && ln -s python3-config python-config

# Install pip
ARG PIP_VERSION=26.0.1

RUN \
    --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    set -ex; \
    python -m ensurepip --upgrade --default-pip; \
    pip3 install --upgrade pip=="${PIP_VERSION}"; \
    pip --version

#########################
# Final flattened image #
#########################

# Inherit config from the original base image
FROM ${BUILD_FROM}

# Copy everything from the build
COPY --from=build / /

# Ensure local python is preferred over distribution python
ENV PATH=/usr/local/bin:$PATH

LABEL \
    io.hass.type="base" \
    io.hass.base.name="python"
