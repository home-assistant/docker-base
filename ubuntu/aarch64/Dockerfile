ARG BUILD_VERSION
FROM arm64v8/ubuntu:$BUILD_VERSION

COPY qemu-aarch64-static /usr/bin/qemu-aarch64-static
RUN apt-get update && apt-get install -y \
        bash \
        jq \
        tzdata \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*
