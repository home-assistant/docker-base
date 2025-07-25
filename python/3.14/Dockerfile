ARG BUILD_FROM
FROM $BUILD_FROM

ARG \
    PYTHON_VERSION \
    PIP_VERSION \
    CERT_IDENTITY \
    CERT_OIDC_ISSUER \
    QEMU_CPU

# ensure local python is preferred over distribution python
ENV PATH=/usr/local/bin:$PATH

# Set shell
SHELL ["/bin/ash", "-o", "pipefail", "-c"]

COPY *.patch /usr/src/
RUN set -ex \
    && export PYTHON_VERSION=${PYTHON_VERSION} \
    && apk add --no-cache --virtual .fetch-deps \
        openssl \
        tar \
        xz \
    && apk add --no-cache --virtual .cosign cosign \
        --repository="https://dl-cdn.alpinelinux.org/alpine/v3.21/community" \
    \
    && curl -L -o python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
    && curl -L -o python.tar.xz.sigstore "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.sigstore" \
    && cosign verify-blob \
        --new-bundle-format \
        --certificate-identity "${CERT_IDENTITY}" \
        --certificate-oidc-issuer "${CERT_OIDC_ISSUER}" \
        --bundle python.tar.xz.sigstore \
        python.tar.xz \
    && mkdir -p /usr/src/python \
    && tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
    && rm python.tar.xz \
    \
    && apk add --no-cache --virtual .build-deps  \
        patch \
        bzip2-dev \
        coreutils \
        dpkg-dev dpkg \
        expat-dev \
        findutils \
        build-base \
        gdbm-dev \
        libc-dev \
        libffi-dev \
        libnsl-dev \
        openssl \
        openssl-dev \
        libtirpc-dev \
        linux-headers \
        make \
        mpdecimal-dev \
        ncurses-dev \
        pax-utils \
        readline-dev \
        sqlite-dev \
        tcl-dev \
        tk \
        tk-dev \
        xz-dev \
        zlib-dev \
        bluez-dev \
    # add build deps before removing fetch deps in case there's overlap
    && apk del .fetch-deps .cosign \
    \
    && for i in /usr/src/*.patch; do \
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
# set thread stack size to 1MB so we don't segfault before we hit sys.getrecursionlimit()
# https://github.com/alpinelinux/aports/commit/2026e1259422d4e0cf92391ca2d3844356c649d0
        EXTRA_CFLAGS="-DTHREAD_STACK_SIZE=0x100000" \
    && make install \
    \
	&& find /usr/local -type f -executable -not \( -name '*tkinter*' \) -exec scanelf --needed --nobanner --format '%n#p' '{}' ';' \
		| tr ',' '\n' \
		| sort -u \
		| awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
		| xargs -rt apk add --no-cache --virtual .python-rundeps \
	&& apk del .build-deps \
	\
    && find /usr/local -depth \
        \( \
            -type d -a \( -name test -o -name tests \) \
        \) -exec rm -rf '{}' + \
    && rm -rf /usr/src/python \
    && rm -f /usr/src/*.patch

# make some useful symlinks that are expected to exist
RUN cd /usr/local/bin \
    && ln -s idle3 idle \
    && ln -s pydoc3 pydoc \
    && ln -s python3 python \
    && ln -s python3-config python-config

RUN set -ex; \
    \
    apk add --no-cache --virtual .fetch-deps openssl; \
    \
    curl -L -o get-pip.py 'https://bootstrap.pypa.io/get-pip.py'; \
    \
    apk del .fetch-deps; \
    \
    python get-pip.py \
        --disable-pip-version-check \
        --no-cache-dir \
        pip==${PIP_VERSION} \
    ; \
    pip --version; \
    \
    find /usr/local -depth \
        \( \
            -type d -a \( -name test -o -name tests \) \
        \) -exec rm -rf '{}' +; \
    rm -f get-pip.py
