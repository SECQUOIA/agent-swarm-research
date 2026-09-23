# Bundled stage 1 reference certificates

The two Python scripts in this directory are byte-for-byte copies of the
repository scripts identified in `origin-manifest.json`. The manifest records
the SHA-256 digest of each original and its repository-relative source path.
Those paths record provenance; execution does not read the original files.
Both scripts use only the Python standard library.

Run the commands in the manuscript README from the manuscript directory (or
from the root of a frozen snapshot). `stage01/check_boundaries.py` imports this
bundled `one_switch_certificate.py` relative to its own location, so no mutable
repository code is needed.
