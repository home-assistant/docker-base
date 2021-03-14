ARG BUILD_FROM
FROM $BUILD_FROM

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# Set shell
SHELL ["/bin/ash", "-o", "pipefail", "-c"]

# install ca-certificates so that HTTPS works consistently
# the other runtime dependencies for Python are installed later
RUN apk add --no-cache ca-certificates

ENV GPG_KEY E3FF2839C048B25C084DEBE9B26995E310250568
ENV PYTHON_VERSION 3.8.8

COPY *.patch /usr/src/
RUN set -ex \
    && apk add --no-cache --virtual .fetch-deps \
        gnupg \
        openssl \
        tar \
        xz \
    \
    && curl -L -o python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
    && curl -L -o python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" \
    && export GNUPGHOME="$(mktemp -d)" \
    && echo "disable-ipv6" >> "$GNUPGHOME/dirmngr.conf" \
    && gpg --batch --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEY" \
    && gpg --batch --verify python.tar.xz.asc python.tar.xz \
    && { command -v gpgconf > /dev/null && gpgconf --kill all || :; } \
    && rm -rf "$GNUPGHOME" python.tar.xz.asc \
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
    && apk del .fetch-deps \
    \
    && for i in /usr/src/*.patch; do \
        patch -d /usr/src/python -p 1 < "${i}"; done \
    && cd /usr/src/python \
    && gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
    && ./configure \
        --build="$gnuArch" \
        --enable-loadable-sqlite-extensions \
        --enable-optimizations \
        --enable-shared \
        --with-lto \
        --with-system-expat \
        --with-system-ffi \
        --without-ensurepip \
    && make -j "$(nproc)" \
        LDFLAGS="-Wl,--strip-all" \
        CFLAGS="-fno-semantic-interposition -fno-builtin-malloc -fno-builtin-calloc -fno-builtin-realloc -fno-builtin-free -ljemalloc" \
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

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 20.2.4

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
        "pip==$PYTHON_PIP_VERSION" \
    ; \
    pip --version; \
    \
    find /usr/local -depth \
        \( \
            -type d -a \( -name test -o -name tests \) \
        \) -exec rm -rf '{}' +; \
    rm -f get-pip.py
