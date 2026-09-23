# Stage 7 author report

Status: authored and frozen for five independent reviewers. Stages 1–6b
remain accepted. Stage 7 and the separate whole-manuscript stage 8 have not
yet completed their required review cycles.

## Scientific synthesis

The title, abstract, introduction, and discussion now present one coherent
paper on certificate existence, exact description size, and approximation.
The introduction maps BDS Conjectures 3.3, 3.1, and 3.2 to the affirmative,
affirmative, and negative answers, respectively. It states the strict PDLC
transfer as the contribution relative to the known four-bound and credited
sharpness example, and retains the dissertation priority qualification.
It distinguishes classical fidelity/QMP/duality/approximation inputs from
new statements with their exact scopes.

Section 7 now has a self-contained proof of the exact strict hull for every
r≥2. Let a=sqrt(p), b=sqrt(q), choose a unit e perpendicular to b*u-a*v,
and put gamma=(u·e)/a=(v·e)/b. Choosing
max(0,(1/2-h)/(ab))<k<1 gives opposite-sign roots
-gamma±sqrt(gamma²+k). At either root, the two squared norms increase by
p*k and q*k and the inner product increases by a*b*k. Both resulting
points are strictly feasible; their positive root-derived weights recover
the original point. Necessity follows from the good coordinate rays and
(q,p,2sqrt(pq)). Thus the general BDS hull theorem is no longer needed as
an input for this example. The all-good intersection is derived after the
hull formula. This replaces the older dimension-three midpoint-only remark.
The construction was independently checked against the actual formal
HullCore source and root lemma, not inferred solely from its documentation.

All formal contributions are integrated in a concise main scope table and
a detailed 15-page standalone formal supplement. The main paper is 42 pages.
The main table explicitly excludes the arbitrary-quadratic obstruction,
general sharp Gram theorem, strict PDLC four-bound, many-row/application
appendices, objective-specific duality, countable dense weak sufficiency,
and literature priority from formal coverage. It distinguishes the smaller
2n+1 SDP test and stronger sqrt(2)/2000 lower constant from the exact
formal interfaces. All five original wrappers remain buildable.

## Portable proof and submission sources

The supplied Lean project contains exactly 64 owned modules and 5 recursively
identified local support modules, copied byte-for-byte from the repository.
Its pinned toolchain, lakefile and dependency manifest are included, together
with five audit partitions, claims and declaration maps. The standalone
runner checks fingerprints, warning-free 64-target compilation, exact owned
declaration counts, transitive allowed axioms and all 64 kernel replays.
The counts are 178+158+248+93+232=909. The allowed axioms are only propext,
Classical.choice and Quot.sound. Imported support/dependency scope is explicit.

The coordinator independently ran the portable runner while author prose
work continued. Its success manifest and logs are included as fresh portable
verification evidence. The author did not duplicate that expensive run.
Only a local cache symlink was used by the coordinator; `.lake` is excluded
from the archive. The project has independent dependency-fetch instructions.

`package_submission.py` creates a deterministic source ZIP with 208
SHA256-tracked source/evidence files plus its manifest. It includes generated
bibliographies and all required figure/source assets, and excludes caches,
process/review history, root-run logs, and third-party literature PDFs.
`paper.pdf`, `formal-supplement.pdf`, and the ZIP are available at the paper
root / `dist/`. Authorship and funding were not supplied, so no metadata was
invented; the README identifies those author-provided submission fields.

## Checks actually run

- `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/final main.tex`
  and the same command for `formal-supplement.tex`: PASS, 42 and 15 pages.
- The same latexmk options with `-outdir=build/stage07` for each of the five
  individual formal wrappers: PASS.
- All seven final logs: no warnings, undefined references, or overfull/
  underfull boxes. Added xurl to support readable portable paths.
- `python3 supplement/check_examples.py`, `check_infinite_aggregation.py`,
  `check_approximation.py`, `check_four_aggregation.py`, and
  `check_three_dimensional_span.py`: all PASS. Full outputs are in
  `build/stage07/exact-checks.log`. These were run once; plotting inputs and
  figure were unchanged, so no redundant figure regeneration was performed.
- Bib/cross-reference/path checks: all 26 bibliography entries used, no
  missing citation keys, and no absolute workspace or surrounding-repository
  inputs in LaTeX.
- `python3 package_submission.py`: PASS. ZIP SHA256 integrity checks all pass.
- Extracted the ZIP into `/tmp/quadratic-submission-check-h5sfb2q4/` and built
  both the main manuscript and detailed supplement there with latexmk: PASS.
  These builds do not use the surrounding repository. See
  `build/stage07/document-checks.txt` and `archive-*.log`.
- Rendered and inspected the title/abstract, new two-point proof page, and
  main formal scope table (main pages 1, 19, 32–33); no clipping or layout
  defect found. Main and supplement text were extracted for inspection.

No project-wide tests, CI status or logs, or unrelated topic changes were
performed. All authored changes are confined to the paper folder. Historical
coverage is preserved, while PROCESS and the current coverage table now give
one noncontradictory status. Source fingerprints are frozen in the stage 7
snapshot for the required review.
