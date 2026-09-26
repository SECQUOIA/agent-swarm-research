# Anonymous submission files

The current deliverables are `submission.pdf`, `latex-source.zip`, and
`computational-supplement.zip`. Author and affiliation fields are intentionally
empty. These files have not been submitted externally. Internal revision status
is recorded in `../revision-20260909/STATUS.md`; package creation is not acceptance.
These files and `manifest.json` contain the September 9 revision (commit
`876ca480`). The manuscript sources were revised afterwards (see
[../README.md](../README.md)), and these files were not refreshed.

Each archive has its own top-level directory, concise README, and SHA-256 payload
manifest. `manifest.json` records the input hashes, archive payload hashes, and
hashes and sizes of the three deliverables. The LaTeX source archive contains all
manuscript inputs. The separate supplement contains the runnable implementations,
tests, independent checks, canonical measurements, and table generator.

Rebuild the deliverables from the repository root:

```sh
python paper-network-simplex/delivery/build-packages.py
```

To test a rebuild without replacing these files:

```sh
python paper-network-simplex/delivery/build-packages.py --output /tmp/network-simplex-rebuild
```

The builder uses an explicit file selection, sorted archive members, fixed ZIP
timestamps and permissions, and a fixed PDF build time with variable PDF metadata
suppressed. It compiles in a temporary directory outside the repository and
rejects LaTeX warnings and box diagnostics. Rebuilds are byte-identical with the
same inputs and toolchain; cross-version TeX or compression output can differ.
No private build logs, reviews, research archives, or external literature PDFs
are included in either archive.

`README-source.md`, `README-supplement.md`, `API.md`, and `requirements.txt` are
the package documentation templates. `checks/` contains independent finite checks
selected during the mathematical audit. Their package names and imports avoid
dependence on internal review directories. Production code and canonical raw
data are copied unchanged.
