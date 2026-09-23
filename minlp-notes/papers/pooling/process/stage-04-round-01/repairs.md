# Stage 4, round 1: implemented minor repairs

A separate repair agent implemented only m1–m3 accepted in `adjudication.md`, after reading that adjudication, reviewers04 and14, and the relevant manuscript context. The edits are ready for root inspection. This record does not close stage4 or begin stage5.

## Exact manuscript changes

- **m1, `s1:model`:** added initial preprocessing that intersects each arc-flow and node-total flow-bound interval with `[0,infinity)` and rejects an empty intersection. This applies only to nonnegative flow quantities, not quality intervals; homogeneous zero-delivery quality semantics remain unchanged. The unusable-pool sentence now checks that zero belongs to the pool-throughput interval and every incident-arc interval, while retaining external-node contracts. Saved the exact pre-edit Section 1 source as `process/snapshots/stage-01-before-stage04-minor.tex`.
- **m1, proofs of `s4:fixed-inputs` and `s4:bounded-attachments`:** replaced lower-bound-only checks before pool deletion with zero-membership checks in the full pool-throughput and incident-arc intervals. Adjacent external-node requirements remain in place. These checks reject the reviewer's pool interval `[-2,-1]` counterexample; normalization also rejects that interval immediately.
- **m2, comparison after the two basic pooling consequences:** stated that both the Boland et al. and Haugland–Hendrix fixed-input predecessor models omit bypasses, and that the latter explicitly discusses the convention. Citations and bibliography metadata are unchanged.
- **m3, `s4:path-projection` statement:** specified polynomially many arithmetic operations and comparisons for lifting abstract feasible real endpoints. For endpoints in a represented common real-algebraic field of polynomial degree and encoding length, the statement now explicitly gives polynomial bit time including input and output encoding, while retaining the same-field and polynomial-total-encoding guarantees. Its constructive proof is unchanged.

All other theorem statements and proofs are preserved. Sections 2–3 and `bibliography.bib` retain their pre-repair hashes. The frozen stage4 review input remains unchanged.

## Verification

- Inspected the exact diffs against both pre-edit snapshots; changes are confined to the three accepted corrections and adjacent line wrapping.
- Ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from `papers/pooling`. Exit status 0; `main.pdf` contains 54 pages (661499 bytes).
- Inspected the final `main.log`: no LaTeX/package warnings, overfull or underfull boxes, undefined references or citations, multiply defined labels, or rerun requests. Matches for warning/rerun package names and informational metadata are not diagnostics.
- No unrelated tests or review reruns were performed. Root's final diff/dependency check and stage closure remain pending.

## SHA-256 hashes

| File | SHA-256 |
|---|---|
| Pre-edit Section 1 snapshot `process/snapshots/stage-01-before-stage04-minor.tex` | `be6256a4ad55a371cc280523072277ac682518ab3527cc82f496e78d17ea97bf` |
| Repaired `sections/01-foundations.tex` | `e023daa9d8ceb445d931e193dce9d47ae1934e17ac13b54d4591710e3f8f76ae` |
| Frozen stage4 input `process/snapshots/stage-04-round-01.tex` | `1ac2f2edead7ed519c97dec65e299412b7c10eb6709e1978ebdf2d2611c6bbe7` |
| Repaired `sections/04-structural-algorithms.tex` | `88b1c181cde7f72b48535054de702a2ff4688a470633eb56e528c519974189de` |
| Unchanged `sections/02-algebraic-complexity.tex` | `8abd1d862cc58d23ee4671f2610c02ca04c27390353ba023b442325565514e67` |
| Unchanged `sections/03-restricted-hardness.tex` | `b8201a4bc6a61d4304f888649afe97bfc4aeefd9234d314a8cae3b805b3fad40` |
| Unchanged `bibliography.bib` | `b775778a852b7ed9255dcb25f6a953848c310681b6be21450f8b8ec3b2f3edea` |
