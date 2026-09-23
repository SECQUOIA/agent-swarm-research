# Portable Lean proof sources

This directory is an independent Lake project. It contains the paper's 64
proof modules and five local support modules, copied without mathematical
changes. `source-manifest.json` records every source SHA256. The five audit
partitions contain 178, 158, 248, 93, and 232 owned declarations: 909 total.
Their `CLAIMS.md` and `COVERAGE.md` files give the precise mathematical scope.
Links to local Lean sources were adapted for this package; references to
repository-only historical review records are retained as text.

Install Elan and Python 3, then run from this directory:

```sh
lake exe cache get
python3 verify.py
```

Elan selects Lean 4.33.1 from `lean-toolchain`. Lake resolves dependencies
from the included `lake-manifest.json`; do not replace that manifest with
new revisions. The first command downloads the pinned Mathlib build cache
and can require substantial disk space. Internet access is needed for the
initial toolchain/dependency/cache downloads. No surrounding repository is
required. A fresh dependency build is also possible when a cache is unavailable.

`verify.py` builds only the 64 explicitly named modules with `--wfail`, runs
all five audits, and invokes `lake env leanchecker MODULE` on each owned
module. Every audit traverses the axioms of every declaration owned by its
listed modules and fails unless all are among `propext`, `Classical.choice`,
and `Quot.sound`. The runner also checks the expected declaration counts and
unchanged hashes of all supplied proof sources, audit files, and build inputs.
Logs and a fresh machine-readable manifest are written to `verification/`.

The five imported local support modules and imported Mathlib dependencies
are used by the replay, not individually replayed by this script. The axiom
checks are transitive through their declarations. This uses Lean's own kernel,
not an independent proof-assistant implementation. See `../../FORMAL-VERIFICATION.md`
and the detailed PDF supplement for mathematical coverage and exclusions.
There is no numerical SDP solver verification or claim that Lean checks the
entire manuscript. The supplied project contains no downloaded dependencies,
build cache, or copyrighted literature PDFs.
