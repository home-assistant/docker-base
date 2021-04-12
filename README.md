# Home Assistant Base Images

These base images are designed as Docker base images for use with building Hass.io containers and add-ons.
It is recommended to use these as a base for your own Home Assistant Add-ons. 

Using these images as a base for other Docker projects is, however, not recommended.

The image include [S6-Overlay](https://github.com/just-containers/s6-overlay), [Bashio](https://github.com/hassio-addons/bashio) and [TempIO](https://github.com/home-assistant/tempio).

## Base images

We support version that are not EOL: https://alpinelinux.org/releases/

| Image | OS | Tags | latest |
|-------|----|------|--------|
| armhf-base | Alpine | 3.10, 3.11 3.12 3.13 | 3.13 |
| armv7-base | Alpine | 3.10, 3.11 3.12 3.13 | 3.13 |
| aarch64-base | Alpine | 3.10, 3.11 3.12 3.13 | 3.13 |
| amd64-base | Alpine | 3.10, 3.11 3.12 3.13 | 3.13 |
| i386-base | Alpine | 3.10, 3.11 3.12 3.13 | 3.13 |

### Jemalloc

We support on our platforms jemalloc. On application which you want enable it, set as envoriement `LD_PRELOAD="/usr/lib/libmimalloc.so"` on your Dockerfile or before you start the application.

### Python images

We support the latest 3 release with the latest 2 Alpine version.

| Image | OS | Tags | latest |
|-------|----|------|--------|
| armhf-base-python | Alpine | 3.7, 3.8, 3.9, 3.7-alpine.3.12, 3.7-alpine.3.13, 3.8-alpine3.12, 3.8-alpine3.13, 3.9-alpine3.12, 3.9-alpine3.13 | 3.9-alpine.3.13 |
| armv7-base-python | Alpine | 3.7, 3.8, 3.9, 3.7-alpine.3.12, 3.7-alpine.3.13, 3.8-alpine3.12, 3.8-alpine3.13, 3.9-alpine3.12, 3.9-alpine3.13 | 3.9-alpine.3.13 |
| aarch64-base-python | Alpine | 3.7, 3.8, 3.9, 3.7-alpine.3.12, 3.7-alpine.3.13, 3.8-alpine3.12, 3.8-alpine3.13, 3.9-alpine3.12, 3.9-alpine3.13 | 3.9-alpine.3.13 |
| amd64-base-python | Alpine | 3.7, 3.8, 3.9, 3.7-alpine.3.12, 3.7-alpine.3.13, 3.8-alpine3.12, 3.8-alpine3.13, 3.9-alpine3.12, 3.9-alpine3.13 | 3.9-alpine.3.13 |
| i386-base-python | Alpine | 3.7, 3.8, 3.9, 3.7-alpine.3.12, 3.7-alpine.3.13, 3.8-alpine3.12, 3.8-alpine3.13, 3.9-alpine3.12, 3.9-alpine3.13 | 3.9-alpine.3.13 |

## Others

### Debian images

**Note**: We prefer the alpine based version because it's more IoT friendly. In some case, you need a glibc system like this.

| Image | OS | Tags | latest |
|-------|----|------|--------|
| armv7-base-debian | Debian | stretch buster bullseye | buster |
| armhf-base-debian | Debian | stretch buster bullseye | buster |
| aarch64-base-debian | Debain | stretch buster bullseye | buster |
| amd64-base-debian | Debain | stretch buster bullseye | buster |
| i386-base-debian | Debain | stretch buster bullseye | buster |

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
| armhf-base-raspbian | Raspbian | stretch, buster, bullseye | buster |

## Thanks

We use https://github.com/multiarch/qemu-user-static to provide a multiarch image. 
