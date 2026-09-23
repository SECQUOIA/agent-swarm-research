# Stage 3, round 1, independent review 2

Verdict: **pass; no major or minor correction requested**.

Reviewed all stage 3 manuscript additions, the exact-check script, author
report and snapshot, bibliography and literature additions, coverage plan,
and the coordinator's closure audit. I did not read another current review
or edit manuscript source. The later frontier development and contributed
formal-consequence section were not treated as accepted mathematics.

## Mathematical findings

### Hypotheses and examples

- The restriction formula in Proposition `prop:stable` is correct, including
  the factor in the symmetric cross term. Convergence for each fixed normal
  to the stably convex tuple supplies all sufficiently large good levels.
  The two-form result holds in every positive dimension. For three forms,
  the `n>=3` and signed positive-definite-combination conditions are exactly
  those needed by the cited classical result; persistence of definiteness
  under arbitrary sufficiently small tuple perturbations is valid.
- The comparison of PDLC for the `A_i` and `Q_i` retains its essential
  strict-feasibility and nonzero trivial-multiplier qualification. Dividing
  that aggregate by its negative constant legitimately gives the last
  coordinate rank-one matrix in the **real** span. The Schur-complement
  threshold is correct. The discussion does not promote this into a new
  unresolved three-form theorem.
- Example `ex:ahc-not-hhc` correctly has `A_1=I`, strict feasibility, stable
  parts and AHC. Restriction to `x_3=t` cancels all three constant terms and
  produces the stated nonconvex binary-square image. Thus it proves strict
  weakening, and the stable-parts-to-HHC nonimplication.
- Example `ex:hhc-not-stable` has convex hyperplane images because all three
  components coincide. Its perturbations converge to the original tuple;
  the proposed midpoint forces two squared coordinates to equal `1/2`
  while their product vanishes, an impossibility. This proves the other
  nonimplication without incorrectly using a diagonal separable tuple.
- The four-row ordinary-hidden-convexity example has a proper cylindrical
  hull bound, only trivial convex certificates, a convex full image and
  convex `t=0` image. The injective three-parameter representation transfers
  the midpoint contradiction on every nonzero sweep level. The three-row
  reduction retains injectivity and the certificate obstruction; its
  `|x_1+x_2|<3` argument and unbounded feasible line are valid.
- The closed-system example has proper full-dimensional hull, HHC through
  two independent forms, and only trivial convex certificates. For a good
  closed multiplier, strict containment of the origin forces a negative
  constant. The traceless two-by-two block then contributes one negative
  eigenvalue and the constant another. This proves the good-multiplier
  family is empty and verifies the claimed necessity of the omitted BDS
  qualification, not merely failure of the main strict theorem.
- The strip example has precisely `-2<x_1<-1`; all strict globally convex
  aggregates admit zero. Its explicit Shor lift satisfies both rows with
  residual `-1/2`, while the first row keeps the relaxation proper.

### Consequences and SDP statements

- The closed-system equivalence follows by inclusions and the proper closed
  convex aggregate sublevel. It does not require or claim equality of the
  two hulls. The three-regime result keeps the separate `n>=2` emptiness
  and `n>=3` full-description restrictions and proves the homogenized
  strict-feasibility equivalence, including perturbing a `t=0` point.
- The compact multiplier slice gives attained objectives when nonempty.
  Zero PSD trace detects zero quadratic part, and both signs of each
  linear coordinate detect its vanishing. The `2n+1` count, empty-slice
  branch, and exact-versus-floating-point distinction are all correct.
- The cone used for the Shor projection is not incorrectly assumed closed.
  Its dual is exactly the nonnegative PSD-multiplier cone. The interior
  addition argument and quadratic mixing identity have the correct signs.
  Mixing with a strict point proves closure equality; extrapolating to
  `2x-x_0` and taking the midpoint proves actual full-space membership,
  a stronger conclusion than density alone. The nontrivial-certificate
  converse and main-theorem corollary follow.
- Both nonclosed-projection examples have the claimed endpoint behavior.
  At an endpoint, zero first covariance diagonal forces zero covariance
  cross entry. At interior first coordinates, the displayed rank-one
  covariance can accommodate arbitrary second coordinate. The compact
  variant's actual feasible set is bounded because its first coordinate
  is at least `1/4`. Its aggregation intersection and Shor projection
  remain distinct, so the historical comparison respects compactness.

### Application and reproducibility

The positive affine box margin proves local infeasibility. PSD aggregation
makes every tangent globally valid, and the additional first-order condition
at a box minimizer is sufficient to exclude the whole box with one tangent.
The absolute-value and affine-minimum LP lifts are exact for the stated
diagonal-dominance restriction. The rational sum-of-squares identity is
correct. Signed affine equality weights share the normalization, and logical
activation conditions remain attached to conditional rows.

The example's estimator factorizations, root termwise witness, aggregate
matrix and determinant, tangent, feasible activation witnesses, DD interval,
two margin pieces, breakpoint, and optimum `1/35` check out. The normalized
and unnormalized margins are distinguished. The purely bilinear obstruction
and implication from a common Shor lift correctly delimit the application.
The script supplements these proofs rather than pretending that its finite
witness checks prove the geometric assertions.

## Literature and checks performed

- Re-read the BDS v2 proof of its two-/three-form corollary and exact
  Theorem 2.24 / Remark 2.25 statement. The cited dimension, good-multiplier
  definition, and nonzero homogeneous-aggregate qualification agree.
- Read the stable-convexity passage in `/tmp/sherraw.txt`; it matches the
  neighborhood definition used here. No unverified roundness theorem is
  imported.
- Read Fujie–Kojima Conditions 1.2 and 1.4 and Theorem 2.1 in `/tmp/fk.txt`.
  Strict original feasibility supplies its SDP Slater condition, and its
  assertion is the closure relation used by the manuscript.
- Inspected the local Berthold–Witzig discussion of local linearizations
  and nonlinear aggregation. Opened Dong's primary author manuscript at
  <https://optimization-online.org/wp-content/uploads/2014/03/4274.pdf>
  and its publisher record
  <https://epubs.siam.org/doi/10.1137/140960657>. The application makes
  restrained established-method attributions, without a novelty or
  performance claim.
- Independently opened Song–Xia's primary manuscript,
  <https://arxiv.org/html/2108.08517v1>, whose Theorem 2.1 explicitly
  reproduces and locates Polyak 1998 Theorem 2.1 with `n>=3`, three real
  forms, and a signed positive-definite combination. This corroborates
  the exact implication and locator used; I did not newly inspect the
  original Polyak PDF.
- Ran `python3 paper-quadratic-aggregation/supplement/check_examples.py`:
  passed. Independently read its coefficient-dictionary checks and
  re-derived the universal sign and cone arguments.
- Compared the author snapshot hashes of `main.tex`, the bibliography,
  both added sections, application appendix, and exact-check script: all
  match the reviewed snapshot. Scanned the dedicated stage 3 final LaTeX
  log for warnings, undefined references, and overfull/underfull boxes:
  no matches. No build rerun, Lean execution, project-wide verification,
  or CI inspection was performed.

This accepts stage 3 within its stated scope. It does not certify the later
frontier mathematics, newly contributed formal consequences, or the final
submission package.
