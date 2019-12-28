[![Build Status](https://dev.azure.com/home-assistant/Hass.io/_apis/build/status/base?branchName=master)](https://dev.azure.com/home-assistant/Hass.io/_build/latest?definitionId=3&branchName=master)

# Hass.io Base Images

These base images are designed as Docker base images for use with building Hass.io containers and add-ons.
It is recommended to use these as a base for your own Hass.io add-ons. 

Using these images as a base for other Docker projects is, however, not recommended.

## Base images

| Image | OS | Tags | latest |
|-------|----|------|--------|
| armhf-base | Alpine | 3.6, 3.7, 3.8, 3.9, 3.10, 3.11 | 3.11 |
| armv7-base | Alpine | 3.9, 3.10, 3.11 | 3.11 |
| aarch64-base | Alpine | 3.6, 3.7, 3.8, 3.9, 3.10, 3.11 | 3.11 |
| amd64-base | Alpine | 3.6, 3.7, 3.8, 3.9, 3.10, 3.11 | 3.11 |
| i386-base | Alpine | 3.6, 3.7, 3.8, 3.9, 3.10, 3.11 | 3.11 |

## Python images

| Image | OS | Tags | latest |
|-------|----|------|--------|
| armhf-base-python | Alpine | 3.6, 3.7, 3.8, 3.6-alpine3.9, 3.6-alpine3.10, 3.6-alpine3.11, 3.7-alpine3.9, 3.7-alpine.3.10, 3.7-alpine.3.11, 3.8-alpine3.9, 3.8-alpine3.10, 3.8-alpine3.11 | 3.8-alpine.3.11 |
| aarch64-base-python | Alpine | 3.6, 3.7, 3.8, 3.6-alpine3.9, 3.6-alpine3.10, 3.6-alpine3.11, 3.7-alpine3.9, 3.7-alpine.3.10, 3.7-alpine.3.11, 3.8-alpine3.9, 3.8-alpine3.10, 3.8-alpine3.11 | 3.8-alpine.3.11 |
| amd64-base-python | Alpine | 3.6, 3.7, 3.8, 3.6-alpine3.9, 3.6-alpine3.10, 3.6-alpine3.11, 3.7-alpine3.9, 3.7-alpine.3.10, 3.7-alpine.3.11, 3.8-alpine3.9, 3.8-alpine3.10, 3.8-alpine3.11 | 3.8-alpine.3.11 |
| i386-base-python | Alpine | 3.6, 3.7, 3.8, 3.6-alpine3.9, 3.6-alpine3.10, 3.6-alpine3.11, 3.7-alpine3.9, 3.7-alpine.3.10, 3.7-alpine.3.11, 3.8-alpine3.9, 3.8-alpine3.10, 3.8-alpine3.11 | 3.8-alpine.3.11 |

## Ubuntu images

**Note**: We prefer the alpine based version because it's more IoT friendly. In some case, you need a glibc system like this.

| Image | OS | Tags | latest |
|-------|----|------|--------|
| armv7-base-ubuntu | Ubuntu | 14.04, 16.04, 18.04 | 18.04 |
| aarch64-base-ubuntu | Ubuntu | 14.04, 16.04, 18.04 | 18.04 |
| amd64-base-ubuntu | Ubuntu | 14.04, 16.04, 18.04 | 18.04 |
| i386-base-ubuntu | Ubuntu | 14.04, 16.04, 18.04 | 18.04 |

# Debian images

**Note**: We prefer the alpine based version because it's more IoT friendly. In some case, you need a glibc system like this.

| Image | OS | Tags | latest |
|-------|----|------|--------|
| armv7-base-debian | Debian | stretch buster | buster |
| armhf-base-debian | Debian | stretch buster | buster |
| aarch64-base-debian | Debain | stretch buster | buster |
| amd64-base-debian | Debain | stretch buster | buster |
| i386-base-debian | Debain | stretch buster | buster |

## Raspbian images

| Image | OS | Tags | latest |
|-------|----|------|--------|
| armhf-base-raspbian | Raspbian | jessie, stretch, buster | buster |

## Thanks

We use https://github.com/multiarch/qemu-user-static to provide a multiarch image.
