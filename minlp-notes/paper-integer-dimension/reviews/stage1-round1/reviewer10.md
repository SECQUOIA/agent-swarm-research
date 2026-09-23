# Stage 1, round 1 — reviewer 10

Reviewed the complete `sections/01-foundations.tex` (lines 1–1206), with additional scrutiny of graph containment, actual linear encodings, endpoint coverage, error allocation, formulation size, and rational coefficients. I read `PROCESS.md`, `reviews/PROTOCOL.md`, `reviews/STAGE1-TASK.md`, `reviews/STAGE1-LENSES.md`, the snapshot, and `coverage.md`; I also inspected `main.tex`, `macros.tex`, and `references.bib`.

The stage's proof chain appears sound within the verification limits below. I found no false main theorem or material unproved construction step. The lower bounds correctly apply to unrestricted integer ranges through compact parity contacts. The binary constructions retain continuous residuals, preserve graph points, and allocate their errors correctly. The rational construction is explicitly a preview whose detailed proof belongs to stage 2.

Major findings: 0

Minor findings: 2

1. **MINOR — malformed multiplication in the smooth error budget.** In `sections/01-foundations.tex`, lines 974, 977, and 992, `C_0,2^{-T}` and `2C_0,2^{-T}` contain literal commas. These are not LaTeX spacing commands and render as punctuation inside the numerical estimate. The intended product is clear from the preceding Taylor argument, so this is a notation defect rather than a failed estimate. Replace the commas with `\,` or `\cdot`. At the same place, an explicit choice `T=max{0,log_2(2C_0/eps)}` for positive `C_0` would make the depth and error allocation directly reproducible.

2. **MINOR — make the polynomial construction's domain and enlarged derivative bound explicit.** In the polynomial part of Theorem `thm:smooth-ranks`, lines 984–993, the construction moves from the transformed original domain to an enclosing normalized box. The prefix point `A` need not lie in the original transformed domain. The zero Hessian blocks extend identically because the outputs are polynomials, but the numerical derivative bound must also be taken on the whole enclosing box. In addition, the displayed prefix construction alone permits all inputs of that enclosing box, whereas Definition `def:dimension` requires the projected input domain to remain the original box. Both repairs are elementary and already explicit in the corresponding original proof (`results/smooth-map-local-rank-integer-complexity.md`, “A compact upper formulation for polynomial maps”): say to retain the original affine domain constraints and coordinate identities, and to enlarge `C_0` using derivative bounds on the enclosing box before selecting `T`. I regard this as a local specification omission, not a substantive proof gap: both operations preserve the stated binary coefficient and size bound.

Verification details and limits:

- Independently checked the finite disjunction at zero weights and unused binary codes, exact binary products, empty prefixes and the endpoint 1, square and product residual bounds, signed coefficient summation, unequal-edge demand rounding, and the boundedness of the banded polyhedra used in disjunctions.
- Reconstructed the indefinite determinant estimate, covariance expansion, capacity-to-volume constant, principal compression, real descent and symmetric shrinking argument. Checked the one-sided sign conventions and unbounded output coverage, the oscillatory proof and its contact-volume application, the partial Legendre fiber/tube construction, and both directions of positive perspective transfer. The perspective rows need no bounds on the original continuous auxiliaries, because they homogenize those variables instead of linearizing products with them.
- Compared the relevant proofs in all nine stage-1 canonical result files, with focused reading of the upper constructions. Also read the rational nc-rank construction result, the supporting parity/epigraph/width note, and the perspective and constant-rank audits. Prior audit verdicts were not used as proofs.
- Checked primary-source statements in the cached GGOW text (Theorems 1.4, 1.17, and 2.18), Wolff's Theorem A on printed pages 50–51, and Nicola's Definition 1.1 and following paragraph. Checked the rational algorithm and extension invariance directly in [Ivanyos–Qiao–Subrahmanyam, 2018 version, Theorem 1.5 and Lemma 5.3](https://arxiv.org/html/1512.03531v5). Their hypotheses support the stage's stated rational scope. This was a targeted source check, not a complete bibliography-metadata or publication-priority audit. I did not independently reprove the imported free-field/operator-scaling theorems.
- Executed an independent inline Python checker: 837 exact rational square-prefix/envelope cases at depths 0–4, including the endpoint identity; 1,296 exact rational residual-product cases at pairs of depths 0–3; and 390 SciPy/HiGHS LP checks of the continuous folding formulation at depths 1–6 and 65 inputs per depth. All passed. The LP optimum agreed with the exact folding sequence to `1e-9`; the rational checks used exact fractions. These are regression checks of the displayed gadgets, not substitutes for their proofs.
- No manuscript edits, subagents, whole-paper compilation, or audit of the unwritten later-stage proofs was performed. No checker file was added.

All five frozen file hashes were recomputed with Python SHA-256 and matched `reviews/stage1-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |
