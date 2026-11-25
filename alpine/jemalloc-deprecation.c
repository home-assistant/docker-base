/*
 * Appended to jemalloc's src/jemalloc.c at build time.
 *
 * jemalloc is deprecated in the Home Assistant base images. Print a warning
 * when the library gets loaded (e.g. through LD_PRELOAD), once per process
 * tree: the marker environment variable is inherited by child processes.
 */
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor))
static void
ha_jemalloc_deprecation_warning(void) {
	static const char msg[] =
	    "WARNING: jemalloc is deprecated in the Home Assistant base images "
	    "and will be removed in the next release. Stop loading "
	    "/usr/local/lib/libjemalloc.so.2 (e.g. through LD_PRELOAD), or add "
	    "jemalloc to your own image (e.g. apk add jemalloc) to keep using "
	    "it.\n";
	static char marker[] = "HA_JEMALLOC_DEPRECATION_WARNED=1";

	if (getenv("HA_JEMALLOC_DEPRECATION_WARNED") != NULL) {
		return;
	}
	putenv(marker);
	if (write(STDERR_FILENO, msg, sizeof(msg) - 1) < 0) {
		/* Nothing useful can be done if stderr is not writable. */
	}
}
