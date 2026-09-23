# Deterministic potential-flow certificates: independent review

Three independent reviewers examined the package on 2026-09-20, one per group of
obligations, and a fourth later reviewed CC40, which none of those three groups
covered. None of them wrote the proofs they reviewed. Each was asked to find
defects rather than to confirm success, was allowed to build scratch files
outside the repository, and was forbidden to modify any file under review.

Reviews are internal research-agent checks. They are not journal peer review.

| Group | Obligations | Modules | Outcome |
|---|---|---|---|
| Certificate soundness | CC01-CC13, CC22-CC24, CC39 | `Bregman`, `Bisection`, `Scenario`, `Curvature`, `DyadicRoot` | No blocking or significant defect; all obligations judged discharged |
| Duality and Laplacian | CC14-CC21, CC25-CC30 | `Support`, `SupportComplete`, `Laplacian`, `FieldDuality` | No blocking or significant defect; all obligations judged discharged |
| Worked example | CC31-CC38 | `TwoPath`, `TwoPathComparison` | No blocking or significant defect; all obligations judged discharged |
| Rational construction support | CC40 | `CertResults` | Reviewed later than the other three groups, which had left it uncovered. No mathematical gap; obligation judged discharged. Three prose defects found and corrected; see below |

## Checks the reviewers performed themselves

The reviews did not rest on reading statements. Each reviewer built scratch
instantiations to test non-vacuity and boundary behaviour:

- **The example network was re-derived from raw incidence.** The example
  reviewer enumerated every edge's tail and head for `L = 1, 2, 3, 4` and ran an
  automated structural audit for `L = 1, 2, 3, 5, 8`: two internally disjoint
  source-sink paths of exactly `L` edges, every edge oriented toward the sink,
  in-degree and out-degree one at every internal node, no shared internal node,
  no self-loops, and the nominations `2`, `-2`, `0`. Conservation was also
  checked directly from `Network.incidence` at every node for `L = 3`, without
  using the module's own conservation lemmas. A mis-encoded graph would have made
  every downstream theorem true but meaningless; it is not mis-encoded.
- **The completeness statement was attacked on a concrete instance.** The duality
  reviewer built a two-edge rational network, confirmed the acceptance predicate
  *accepts* the optimal certificate and *rejects* both undersized roots and
  `lambda = 0` by kernel evaluation, checked that the accepted bound equals the
  attained support maximum, and separately brute-forced 2,073,600 rational dual
  data in Python: no point undercut the support maximum, and the minimum
  achievable bound was exactly the support value.
- **The scenario hypothesis bundle was instantiated non-degenerately**, including
  a case where the physical flow has a negative coordinate while the trial flow is
  nonnegative there, so the selection rule picks the opposite branch and the
  residual bound is active rather than vacuous. `Compatible` was shown to be a
  real restriction by exhibiting an instance where it fails.
- **The example's attaining dual was recomputed independently** for `L = 2` and
  `L = 3`, including the residual on both paths, the root test holding with
  equality, and the three pieces of the bound summing to exactly `1 + eps`. The
  reviewer additionally proved that the multiplier `1/(4 L eps)` is the *unique*
  scalar satisfying the potential-consistency identity.
- **Boundary cases were instantiated**, including self-loop and disconnected
  networks for CC09, straddling and negative curvature intervals for CC22, a
  zero-curvature edge and the `C_* = 0` branch for CC30, and `a = 0`, `q = 0`,
  and 60-bit precision for CC39.
- **The bisection was evaluated in the kernel** on brackets with negative trial
  values and brackets straddling zero, and its output independently checked to
  bracket a sign change of the divergence test.

## Findings and their resolution

No finding was blocking or significant. All were resolved.

| Finding | Resolution |
|---|---|
| `COVERAGE.md` cited `Network.sum_goal_eq_sum_residual` for CC23, which does not exist under that name | Citation corrected to `sum_goal_eq_sum_residual_of_feasible`. The name had been changed during integration to resolve a genuine clash (below). |
| `Network.exists_zeroAdmissible_iff` (CC25) carried a hypothesis `0 <= h` that the source's Fredholm criterion does not need | Hypothesis removed; the criterion is now proved directly from the ordered-field range lemma. |
| The correspondence between the matrix-free KKT condition and the source's `eq:a-cert-kkt` was recorded as prose only | The Schur-complement system is now stated in Lean and its equivalence proved in both directions, so the correspondence is machine-checked rather than hand-checked. |
| `C_*` was identified only through an `OptimalFactor` hypothesis, not as an infimum | `isLeast_factor` added, identifying the optimal factor as the least element of the admissible factor set. |
| CC36's asymptotics were literally about the auxiliary cubic `bregShape`, with no stated bridge to `edgeBregman` for the example | Bridge lemmas added, so the boundary displacements are proved to solve the actual divergence equation. |
| CC36's negative-side uniqueness was proved only inside a window, which is genuinely necessary for `bregShape` but not for the divergence | Global uniqueness for `edgeBregman` on each side of the trial value added. The reviewer's justification for the window — that `bregShape c a = c a^2 + 2 a^3 / 3` vanishes again at `a = -3 c / 2`, below `-c` — is correct arithmetic but **is not proved by any declaration in the package**. It appears in the docstring of `existsUnique_edgeBregman_le` and in [COVERAGE.md](COVERAGE.md) as reviewer reasoning about why the window is needed, not as verified content. |
| CC37's limit was stated with the factor `1 / sum h` without a theorem connecting it to the optimal factor | `hEdge_pos` and the instantiation of `optimalFactor_sel` at those curvatures added. |
| CC31 did not aggregate the per-edge drops into the example's "path drops are both `L`" | Path-drop lemma added. |
| CC06's boundary theorems exhibited a sublevel boundary point without claiming uniqueness | Uniqueness corollaries added under coefficient positivity. |
| `README.md` linked review and verification records that did not yet exist | This file and `VERIFICATION.md` now exist. |

## Notes recorded rather than changed

- The `Scenario` bundle does not require the trial flow to be conserved, although
  the source's `y` satisfies `Ay = b`. This weakens the hypotheses, so the proved
  statements are strictly stronger than the source's. A reader matching
  hypotheses one-for-one against `prop:a-cert-signs` should expect this.
- CC09 is proved in the coordinate-free form that `CLAIMS.md` requires. Its
  identification with the literal componentwise zero-sum condition would need a
  notion of connected component, which the network model does not carry.
- CC28's Lean system is the un-eliminated block form; the Schur-complement form
  and its equivalence are now both stated, and neither is inverted anywhere, so
  singular gauges and redundant conservation rows remain permitted.

## Defect found during integration

Separately from the reviews, integration found a real defect: `Curvature.lean`
and `Laplacian.lean` both declared `PotentialFlow.Network.sum_goal_eq_sum_residual`
with different statements, so the two modules could not be imported together.
This had not surfaced because no module imported both. The curvature lemma was
renamed to `sum_goal_eq_sum_residual_of_feasible`, the example module now imports
`Curvature` and uses the real `curvatureFloor` rather than the local copy the
clash had forced on it, and all twelve modules are now confirmed to import
together.

## Follow-up: rational witnesses for CC35

A later review found a formal coverage gap: the two-path dual witnesses and
attainment theorems were stated over `ℝ`, with their rationality for rational
`eps` left as an informal consequence of the formulas. This did not invalidate
the real bounds, but left part of CC35 outside Lean.

`TwoPath.exists_rat_dualPotential` now constructs rational node potentials, and
`TwoPath.exists_rational_dual_data` proves that the multiplier, both potential
vectors and both root vectors used by the existing theorems are casts of rational
data. The targeted checks for this correction are recorded in
[VERIFICATION.md](VERIFICATION.md).

The same gap was then checked for across the rest of the package, and one further
instance was found and closed. The distinction that governs it: where the source's
rational object is an **input**, it is universally quantified, so proving the
statement over the reals is strictly stronger (CC03's interval endpoints, CC15's
multiplier, potentials and roots); where it is a **witness**, it is existentially
quantified, and a real-valued construction is strictly weaker. CC35 and CC33 are
the two witness cases in the example. CC33 is now closed by
`TwoPath.exists_integral_dual_witnesses` and `TwoPath.exists_integral_dualLower`,
which exhibit the example's potentials as integer data and its conjugate roots as
rational data, and show that those exact witnesses pass the root test and produce
the dual value `2 L / 3`. The obligations whose rational typing was specified from
the start -- CC06, CC19, CC29, CC39 and CC40 -- were already stated over `ℚ`.

## A hole in this file's own review coverage, since closed

The three groups above cover CC01-CC39 across **eleven** modules. CC40 and
`CertResults.lean` fell outside every group, so the package's claim of complete
independent review was unearned until the fourth review. The discrepancy was
visible in the records themselves: [VERIFICATION.md](VERIFICATION.md) says the
package has twelve proof modules, while the table above lists eleven.

CC40 has now been independently reviewed, and **is discharged**. The reviewer
recomputed the worked two-edge instance in exact rationals and reproduced every
figure — gap `1/2`, curvature floors `(3/2, 0)`, residuals `(1, 0)`,
`ratFactor = 2/3`, final check `2/3 <= 25/36` — and confirmed that the
zero-curvature branch is genuinely exercised and decision-relevant: replacing the
goal with `![1, 1]` is rejected even at radius `100`, so the guard fires rather
than being vacuously satisfied. The axiom check is clean, and the absence of
`Lean.ofReduceBool` from the dependency cone is machine-checkable evidence that
`native_decide` is used nowhere in it.

Three prose defects in the CC40 row of [COVERAGE.md](COVERAGE.md) were found and
are corrected there:

- **The blanket sentence "No optimizer output, pre-existing physical solution or
  numerical tolerance appears as a hypothesis" was false** for two declarations
  the row listed under soundness. `intervalAccepted_mem` and
  `intervalAccepted_drop_enclosure` take feasibility and minimality of `x` as
  hypotheses. The sentence is now scoped to the four headline soundness theorems,
  which produce the physical flow existentially. The first three require only
  acceptance; `gap_zero_sound` additionally requires `C.gap = 0`, an exact
  condition on the certificate data.
- **`intervalAccepted_singleton` and `intervalAccepted_bracketInterval` were
  grouped under "soundness"** although they run in the acceptance direction.
  They are now labelled as non-vacuity results.
- **The row was silent about what CC40 does and does not assemble.** A scope
  sentence and the cross-reference to `RationalNetwork.RatSupportAccepted` under
  CC19 are now there.

## Documentation defects found after the reviews, and corrected here

Separately from the CC40 review above, an audit of this package's own prose found
scope wording that needed correction or clarification, two structural defects
in [COVERAGE.md](COVERAGE.md), and wrong or unlabelled numeric records in
[VERIFICATION.md](VERIFICATION.md). No Lean statement or proof changed. The
entries below distinguish inaccurate claims from true explanations whose relation
to the exported theorem needed to be clearer.

- **CC36's inherited example assumptions are now explicit.**
  `TwoPath.edgeBregman_one_shift` states the expansion at `cp = cm = 1`,
  `0 < y`, and `0 < y + a`. The surrounding two-path example in `CLAIMS.md`
  and the source already has unit coefficients and positive trial values
  `1 ± eps`. At `y = -1`, `a = 2`, the two sides are `2` and `4/3`, but that
  counterexample is outside the example's scope. It rules out an unrestricted
  generalization; it does not show that CC36 or its proof is wrong in context.
- **The `bregShape` second root is reviewer reasoning.** See the CC36 row
  above: the arithmetic is correct, but no separately stated Lean declaration
  proves it. This distinction clarifies the evidence rather than identifying a
  missing part of CC36.
- **CC30 said `Network.exists_isLeast_factor` holds "under the CC25 condition
  alone".** It also requires `∀ e, 0 ≤ h e`. Read next to the CC25 row, which
  stresses that the CC25 criterion carries no hypothesis on the curvatures, the
  phrase claimed a freedom this statement does not have.
- **CC26's proof witness has curvature energy exactly zero.** The earlier
  sentence was true, and that property is checked inside the proof. The coverage
  note now distinguishes it from the exported conclusion of
  `Network.exists_unbounded_of_not_zeroGoalCompatible`, which states only
  `(1/2) sum_e h e * d e ^ 2 ≤ delta`.
- **The namespace convention in [COVERAGE.md](COVERAGE.md) was incomplete**, not
  reaching `PotentialFlow.TwoPath`, `PotentialFlow.RationalNetwork`,
  `PotentialFlow.Scenario` or `PotentialFlow.CertExample`, so several citations
  could not be resolved under the rule as stated.
- **CC20 was listed twice**, in two sections with different declaration lists, and
  the first list omitted `RationalNetwork.ratSupportBound_exact_of_drops`. The map
  therefore had 41 rows for 40 obligations.
- **[VERIFICATION.md](VERIFICATION.md) carried wrong numbers.** The "Original
  package checks" table cited 962 audited declarations, which is the later
  CC33+CC35 re-run rather than the original 949, so it contradicted the log it
  points to; and two rows of the module line-count table, `TwoPath.lean` and
  `TwoPathComparison.lean`, did not match the commit the table says it describes.
  Two further figures were stale-but-true and were not marked as such where they
  appear. The corrections and the evidence are in that file.

A separate slip that could not be corrected in place: the checked-in
[verification/run.log](verification/run.log) describes "the 30 `#print axioms`
lines" and then reports "31 declarations". The log is a retained record of an
executed run and is not rewritten; the reconciliation is recorded in
[VERIFICATION.md](VERIFICATION.md).

One item the audit raised was **verified as accurate and left alone**: the
CC36–CC37 follow-up hedge below, that the conditional limits "include rational
rounding but do not construct a rounding procedure or certify arbitrary
perturbations". A stronger caveat is in fact warranted, and is recorded in the
CC37 row of [COVERAGE.md](COVERAGE.md): the two Laplacian rounding theorems
constrain only the lower endpoint.

## Follow-up: rounded asymptotics for CC36–CC37

A source review found that the manuscript extends the exact width limits to
rational outer endpoints and roots with errors `o(eps)`, while the mapped Lean
statements covered only exact endpoints and roots.

`TwoPath.tendsto_bregmanWidth_of_endpoint_errors` now proves stability of the
separate-edge width against errors measured from the actual endpoints.
`TwoPath.tendsto_curvatureFloor_of_endpoint_error` recomputes curvature from
perturbed endpoints, and `TwoPath.tendsto_laplacianWidth_of_endpoint_root_errors`
proves stability with root error measured against that new curvature sum.
An independent source review found no remaining correspondence or vacuity issue.
These conditional limits include rational rounding but do not construct a
rounding procedure or certify arbitrary perturbations. Targeted execution results
are recorded in [VERIFICATION.md](VERIFICATION.md).
