ARG BUILD_VERSION
FROM arm32v7/ubuntu:$BUILD_VERSION

COPY qemu-arm-static /usr/bin/qemu-arm-static
RUN apt-get update && apt-get install -y \
        bash \
        jq \
        tzdata \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

