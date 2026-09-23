# Bundled reference certificates and checks

The Python scripts and JSON data in this directory are byte-for-byte copies of
the repository artifacts identified in `origin-manifest.json`. The manifest records
the SHA-256 digest of each original and its repository-relative source path.
Those paths record provenance; execution does not read the original files.
All scripts use only the Python standard library.

Run the commands in the manuscript README from the manuscript directory (or
from the root of a frozen snapshot). `stage01/check_boundaries.py` imports this
bundled `one_switch_certificate.py` relative to its own location, so no mutable
repository code is needed.

Stage 2 adds the all-dimension four-block verifier and its complete finite and
polynomial certificates. These are the computational premise of the manuscript's
weighted pair inequality. The n=4 three-block and n=5 four-block certificates are
optional independent special-case checks, explicitly subsumed by the manuscript's
stronger theorems. The n=3 counterexample verifier checks the original distinct-word
failure; `../stage02/check_new_results.py` independently strengthens that conclusion
to all words, allowing repetitions. The heavy-mode construction imports the bundled
`adjacent_pair_flow.py`; the separate DP audit imports no project code.

Run `python verification/stage02/run_checks.py` from the manuscript directory to
verify the manifest and run every stage 2 checker with local bundled dependencies.
Do not pass `-O` to Python because assertions perform exact certificate checks.
