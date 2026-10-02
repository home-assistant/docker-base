"""Normalize toolchain references in the installed Python's sysconfig.

CPython records the build-time compiler and linker in _sysconfigdata,
the installed Makefile and python3.x-config. pip/setuptools default to
these values when compiling extension modules from source, but images
downstream only ship the GNU toolchain (apk add build-base). The
interpreter is built with clang/lld purely for performance; extensions
built with gcc against it are ABI compatible, so rewrite the recorded
toolchain back to the GNU defaults.

Modeled after python-build-standalone's hack_sysconfig.py:
https://github.com/astral-sh/python-build-standalone/blob/main/cpython-unix/build-cpython.sh
"""

import importlib
import json
import os
import re
import sys
import sysconfig

REPLACEMENTS = [
    (re.compile(r"-fuse-ld=lld\s*"), ""),
    (re.compile(r"\bclang\+\+"), "g++"),
    (re.compile(r"\bclang\b"), "gcc"),
    (re.compile(r"\bllvm-ar\b"), "ar"),
    (re.compile(r"\bllvm-ranlib\b"), "ranlib"),
]


def normalize(text):
    for pattern, replacement in REPLACEMENTS:
        text = pattern.sub(replacement, text)
    return text


def normalize_file(path):
    with open(path, encoding="utf-8") as fh:
        data = fh.read()

    normalized = normalize(data)
    if normalized != data:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(normalized)
        print(f"normalized {path}")
    else:
        print(f"no changes needed in {path}")


def normalize_sysconfigdata():
    module = importlib.import_module(sysconfig._get_sysconfigdata_name())
    path = module.__file__
    build_time_vars = {
        key: normalize(value) if isinstance(value, str) else value
        for key, value in module.build_time_vars.items()
    }

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("# system configuration generated and used by the sysconfig module\n")
        fh.write(f"build_time_vars = {json.dumps(build_time_vars, indent=4, sort_keys=True)}\n")
    print(f"normalized {path}")

    return build_time_vars


def main():
    build_time_vars = normalize_sysconfigdata()
    normalize_file(sysconfig.get_makefile_filename())
    normalize_file(
        os.path.join(
            sysconfig.get_config_var("BINDIR"),
            f"python{sysconfig.get_config_var('VERSION')}-config",
        )
    )

    # keys used by sysconfig.customize_compiler() and python3.x-config, i.e.
    # everything downstream extension builds inherit (*_NODIST vars and the
    # LLVM_PROF_* PGO leftovers are never used by extension builds)
    toolchain_keys = (
        "CC", "CXX", "CFLAGS", "CPPFLAGS", "CCSHARED", "LDSHARED",
        "LDCXXSHARED", "BLDSHARED", "LINKCC", "LDFLAGS", "AR", "ARFLAGS",
        "RANLIB", "READELF",
    )
    for key in toolchain_keys:
        print(f"{key}={build_time_vars.get(key)}")
    leaked = {
        key: value
        for key in toolchain_keys
        if isinstance(value := build_time_vars.get(key), str)
        and ("clang" in value or "lld" in value or "llvm" in value)
    }
    if leaked:
        print(f"toolchain still leaks into sysconfig: {leaked}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
