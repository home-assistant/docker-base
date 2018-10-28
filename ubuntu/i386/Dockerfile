ARG BUILD_VERSION
FROM i386/ubuntu:$BUILD_VERSION

RUN apt-get update && apt-get install -y \
        bash \
        jq \
        tzdata \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*
