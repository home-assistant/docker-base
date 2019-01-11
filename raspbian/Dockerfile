ARG BUILD_FROM
FROM raspbian/$BUILD_FROM

COPY qemu-arm-static /usr/bin/qemu-arm-static
RUN apt-get update && apt-get install -y \
        bash \
        jq \
        tzdata \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*
