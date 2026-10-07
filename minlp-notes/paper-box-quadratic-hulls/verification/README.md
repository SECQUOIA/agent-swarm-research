# Targeted manuscript verification

The verification is limited to this manuscript and its companion. No
project-wide verification, CI status inspection, or CI log inspection was
performed. Existing optimization campaigns were not rerun.

## Mathematical review

Independent reviews reconstructed the three-variable proofs, the finite-lift
obstruction and graph formulations, the new edge-contact classification, and
the separation and comparison tools. No substantive error remained after
revision. The reports are in
[`evidence/reviews`](../evidence/reviews).

The proof arithmetic was checked with new focused exact calculations, without
an optimization solver:

- The twenty rational moments give all 27 positive definite localizing
  matrices, the stated minimum leading determinants, all 24 and 48 switched
  SOC slacks, and the separating value `-1/40`.
- The parameterized validity identity, family edge restrictions, and
  27-block order-unit identity expand exactly.
- The 25 Horn-form terms have the same exponent after evaluation at the
  stated infinitesimal point.
- An independent enumeration of all 4,096 cube-edge subsets confirms the
  exhaustive contact-graph cases. This checks a finite combinatorial step;
  the manuscript proves the classification analytically.

The final classification requires only positive square coefficients and
positive values at all cube vertices. The source gate for Hildebrand's
rank-one subtraction criterion was resolved against arXiv version 4;
[`hildebrand-source-receipt.md`](../evidence/hildebrand-source-receipt.md)
records the exact statement and published metadata.

The reports distinguish these new proof checks from archived optimization
experiments. The single shared GPT Luna lead, with max reasoning, checked the
external source contracts and completed the literature audit through the
serialized `$lit` workflow. The source contracts are in
[`literature-audit.md`](../evidence/literature-audit.md), and the final batches
and receipt are in
[`literature/runs/2026-10-06-box-hulls-literature-luna`](../../literature/runs/2026-10-06-box-hulls-literature-luna/run.md).
Its final check exited 0 with `KB_CHECK=ok`, `UNREAD=200`, and
`READ_UNCITED=776`. These counts cover the whole knowledge base. The three
reported preview warnings predate this intake and concern unrelated works.
The shared lead performed the final KB maintenance; this manuscript session
remained read-only during that handoff.

Diananda's full text and Shor's full text remain unavailable; Shor is used
only for bibliographic attribution. Maxfield–Minc's original PDF independently
supports the needed order-four cone identity. The official Clarabel and SCS
release pages were inspected, although their KB packages remain unread after
HTML ingestion failed. No theorem depends on an unread source. The audit
records these access limits and confines the novelty claims to the results
and prior works actually compared.

## Build and record checks

Commands run from the manuscript directory include:

```sh
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=verification main.tex
make
python3 companion/inspect_records.py
python3 verification/check_package.py
pdftotext -layout main.pdf verification/main.txt
pdfinfo main.pdf
```

The preliminary direct TeX pass succeeded. `make` then ran BibTeX and all
necessary TeX passes. The final anonymous PDF has 55 pages. The local build,
freshly extracted source build, and freshly extracted companion check all
exited 0. The source archive contains 23 files and the companion contains
378 files. Results are recorded in [`final-checks.json`](final-checks.json);
the final TeX log is `main.log`.

There are no unresolved TeX diagnostics or overfull/underfull boxes. Both
BibTeX runs report the one expected warning
`Warning--empty year in BurerBoxQPInstances2019`: the official benchmark
repository has no publication date, so its year is omitted. The checker
allows only that exact diagnostic and records it separately; it rejects
every other bibliography or TeX warning. The `2019` suffix is an internal
citation key, not a publication year.

The companion inspector passed: 371 copied-source SHA256 hashes, 334
constructed-method table rows, 109 hard-objective closure comparisons, and
the strict-audit sensitivity calculations. It uses only the Python standard
library, imports no optimization implementation, generates no instance, and
solves no model. Checksums establish provenance; they do not certify a solver
result.

The final PDF was inspected using `pdftotext`, `pdfinfo`, and page renders
made with `pdftoppm -f N -l N -scale-to 1400 -singlefile -png main.pdf
verification/previews/final-page-N` for pages 1, 7, 11, 29, 33, 36, 53,
and 55. These cover the title and abstract, contact diagram, family formulation
proof, numerical table, bibliography, exact matrix certificate, facet-minimum
curvature table, and completed final proof. The layout is readable, with no
clipped displays or tables. Text extraction contains no unresolved `??`
references; the source scan found no draft placeholders.

The two archives are generated by:

```sh
python3 verification/package.py
```

Their byte counts and SHA256 hashes, together with the PDF hash, are stored
in `artifact-manifest.json`. A fresh temporary extraction of the submission
archive is compiled with `latexmk -pdf -interaction=nonstopmode
-halt-on-error main.tex`. The companion inspector is also run from a fresh
temporary extraction. These checks ensure that the distributed packages do
not depend on the surrounding repository.
