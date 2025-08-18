# Home Assistant Base Images

These base images are designed as Docker base images for use with building Home Assistant containers and add-ons.
It is recommended to use these as a base for your own Home Assistant Add-ons.

Using these images as a base for other Docker projects is, however, not recommended.

The image include [S6-Overlay](https://github.com/just-containers/s6-overlay), [Bashio](https://github.com/hassio-addons/bashio) and [TempIO](https://github.com/home-assistant/tempio).

## Base images

We support version that are not EOL: https://alpinelinux.org/releases/

| Image | OS | Tags | latest |
|-------|----|------|--------|
| armhf-base | Alpine | 3.19, 3.20, 3.21, 3.22 | 3.22 |
| armv7-base | Alpine | 3.19, 3.20, 3.21, 3.22 | 3.22 |
| aarch64-base | Alpine | 3.19, 3.20, 3.21, 3.22 | 3.22 |
| amd64-base | Alpine | 3.19, 3.20, 3.21, 3.22 | 3.22 |
| i386-base | Alpine | 3.19, 3.20, 3.21, 3.22 | 3.22 |

### jemalloc

We support on our platforms jemalloc. On the application which you want to enable it, set as environment `LD_PRELOAD="/usr/local/lib/libjemalloc.so.2"` on your Dockerfile or before you start the application.

### Python images

We support the latest 3 release with the latest 3 Alpine version.

| Image | OS | Python versions | Tags | latest |
|-------|----|-----------------|------|--------|
| armhf-base-python | Alpine | 3.11, 3.12, 3.13 | 3.11-alpine3.20, 3.11-alpine3.21, 3.11-alpine3.22, 3.12-alpine3.20, 3.12-alpine3.21, 3.12-alpine3.22, 3.13-alpine3.20, 3.13-alpine3.21, 3.13-alpine3.22 | 3.13-alpine3.22 |
| armv7-base-python | Alpine | 3.11, 3.12, 3.13 | 3.11-alpine3.20, 3.11-alpine3.21, 3.11-alpine3.22, 3.12-alpine3.20, 3.12-alpine3.21, 3.12-alpine3.22, 3.13-alpine3.20, 3.13-alpine3.21, 3.13-alpine3.22 | 3.13-alpine3.22 |
| aarch64-base-python | Alpine | 3.11, 3.12, 3.13 | 3.11-alpine3.20, 3.11-alpine3.21, 3.11-alpine3.22, 3.12-alpine3.20, 3.12-alpine3.21, 3.12-alpine3.22, 3.13-alpine3.20, 3.13-alpine3.21, 3.13-alpine3.22 | 3.13-alpine3.22 |
| amd64-base-python | Alpine | 3.11, 3.12, 3.13 | 3.11-alpine3.20, 3.11-alpine3.21, 3.11-alpine3.22, 3.12-alpine3.20, 3.12-alpine3.21, 3.12-alpine3.22, 3.13-alpine3.20, 3.13-alpine3.21, 3.13-alpine3.22 | 3.13-alpine3.22 |
| i386-base-python | Alpine | 3.11, 3.12, 3.13 | 3.11-alpine3.20, 3.11-alpine3.21, 3.11-alpine3.22, 3.12-alpine3.20, 3.12-alpine3.21, 3.12-alpine3.22, 3.13-alpine3.20, 3.13-alpine3.21, 3.13-alpine3.22 | 3.13-alpine3.22 |

## Others

### Debian images

**Note**: We prefer the Alpine based version because it's more IoT friendly. In some case, you need a glibc system like this.

| Image | OS | Tags | latest |
|-------|----|------|--------|
| armv7-base-debian | Debian | bookworm, trixie | trixie |
| armhf-base-debian | Debian | bookworm, trixie | trixie |
| aarch64-base-debian | Debian | bookworm, trixie | trixie |
| amd64-base-debian | Debian | bookworm, trixie | trixie |
| i386-base-debian | Debian | bookworm, trixie | trixie |

### Ubuntu images

**Note**: We prefer the alpine based version because it's more IoT friendly. In some case, you need a glibc system like this.

| Image | OS | Tags | latest |
|-------|----|------|--------|
| armv7-base-ubuntu | Ubuntu | 14.04, 16.04, 18.04 20.04 | 20.04 |
| aarch64-base-ubuntu | Ubuntu | 14.04, 16.04, 18.04 20.04 | 20.04 |
| amd64-base-ubuntu | Ubuntu | 14.04, 16.04, 18.04 20.04 | 20.04 |
| i386-base-ubuntu | Ubuntu | 14.04, 16.04, 18.04 | |

### Raspbian images

| Image | OS | Tags | latest |
|-------|----|------|--------|
| armhf-base-raspbian | Raspbian | bookworm, trixie | trixie |
