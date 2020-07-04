ARG BUILD_FROM
FROM $BUILD_FROM

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# Set shell
SHELL ["/bin/ash", "-o", "pipefail", "-c"]

# install ca-certificates so that HTTPS works consistently
# the other runtime dependencies for Python are installed later
RUN apk add --no-cache ca-certificates

ENV GPG_KEY 0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D
ENV PYTHON_VERSION 3.6.11

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
        gcc \
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
        --with-system-expat \
        --with-system-ffi \
        --without-ensurepip \
    && make -j "$(nproc)" \
# set thread stack size to 1MB so we don't segfault before we hit sys.getrecursionlimit()
# https://github.com/alpinelinux/aports/commit/2026e1259422d4e0cf92391ca2d3844356c649d0
        EXTRA_CFLAGS="-DTHREAD_STACK_SIZE=0x100000" \
# setting PROFILE_TASK makes "--enable-optimizations" reasonable: https://bugs.python.org/issue36044
        PROFILE_TASK='-m test.regrtest --pgo \
            test_asyncio \
            test_asyncore \
            test_array \
            test_base64 \
            test_binascii \
            test_binop \
            test_bisect \
            test_bytes \
            test_cmath \
            test_codecs \
            test_collections \
            test_complex \
            test_dataclasses \
            test_datetime \
            test_decimal \
            test_difflib \
            test_embed \
            test_float \
            test_fstring \
            test_functools \
            test_generators \
            test_hashlib \
            test_heapq \
            test_int \
            test_itertools \
            test_json \
            test_long \
            test_math \
            test_memoryview \
            test_operator \
            test_ordered_dict \
            test_pickle \
            test_pprint \
            test_re \
            test_set \
            test_sqlite \
            test_statistics \
            test_struct \
            test_tabnanny \
            test_time \
            test_unicode \
            test_xml_etree \
            test_xml_etree_c \
		' \
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
ENV PYTHON_PIP_VERSION 20.1.1

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

# Setup jemalloc
ARG JEMALLOC_VERSION=5.2.1

RUN apk add --no-cache --virtual .build-deps \
        build-base \
    && curl -L -s https://github.com/jemalloc/jemalloc/releases/download/${JEMALLOC_VERSION}/jemalloc-${JEMALLOC_VERSION}.tar.bz2 | tar -xjf - -C /usr/src \
    && cd /usr/src/jemalloc-${JEMALLOC_VERSION} \
    && ./configure \
    && make \
    && make install \
    && apk del .build-deps \
    && rm -rf /usr/src/jemalloc-${JEMALLOC_VERSION}
