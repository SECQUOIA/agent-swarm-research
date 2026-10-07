# Closing record: separation limits and the choice of quadratic cuts

Date: 2026-10-04. This closes the [October 1 program](PROGRAM.md), begun
2026-10-01. All eleven streams are finished. “Reviewed” means checked by
another research agent, not journal peer review. A final correction checked
by the coordinating agent is distinguished below from an independent
review of that correction. This closing record was reviewed once by an
independent critic ([CLOSEOUT-review.md](CLOSEOUT-review.md)); fixes are
applied, and it has not been re-reviewed. It records existing proofs, certificates,
experiments and reviews; no new research computations were run to write it.

The program substantially answers its original question, but does not
identify a generally best solver cut. Exact separation remains hard even
for binary points satisfying strong standard relaxations. Optimizing a
single intersection cut can improve its corner bound without improving an
LP cutting trajectory or a full solve. The bilinear Lorentz-orbit family
and its maximal completions have both single-cut and closure limitations;
scaled vertex depth gives a useful quantitative account of their worst
single-cut loss. Implied minors have analogous tangent obstructions, with
an exact example showing a larger gap, but no uniform ordering of bilinear
and minor gaps. The three-variable family adds something beyond existing
named relaxations and performs well on constructed triple-gap instances;
edge-sharing constructions show little gain. Its
completeness remains conjectural. Four positive variables already preclude
any finite SDP lift of the full quadratic hull. The practical evidence
supports careful separation, normalization and validation, rather than a
claim that a stronger local criterion makes quadratic cuts worth enabling
in SCIP.

## Main answers and scope

- **Separation limits.** The binary stream proves strong NP-completeness
  for several cut classes, including hypermetric, rounded psd and gap-1
  separation. These results strengthen the starting integer-QP theorem.
  Fixed rank and a fixed positive normalized-violation threshold offer
  tractable regimes, but numerical rank does not supply exact rational
  input. The hard constructed violations can be polynomially small;
  hardness does not imply that practical relaxation optima are difficult.
- **Best intersection cut.** For positive objective weights, the unrestricted
  supremum equals the corner-hull bound in the starting theorem. Attainment
  is a separate question, and several sufficiency statements have close
  classical precedents. Restricted orbit families can lose arbitrarily much.
  Bounded scaled depth supplies a uniform lower ratio bound; an angle
  condition alone does not. Taking every cut from the restricted family does
  not generally recover the full corner-hull dominant.
- **Best cut in a solver.** Corner-bound maximization frequently has no
  discriminating power in the SCIP corner experiments. Where it does, maximizing
  it does not establish better root or tree performance. The multiround
  experiment finds a small later-round loss outside SCIP. The SCIP experiment
  withdraws its stock-solver timing comparison because batches were not
  comparable. Neither supplies a general prescription to enable these cuts.
  Ray scaling can remove many first-piece rejection conditions while
  preserving the mathematical cut; a validated implementation is still needed.
- **Small quadratic hulls.** The selective family can replace the exact
  three-variable lift to solver accuracy in the constructed tests, often
  with fewer or smaller blocks. Natural-instance evidence is mostly negative.
  Three-variable completeness is open; the nonexistence of a finite SDP lift
  from four positive variables is proved using external representability
  results, not inferred from the numerical searches.

Labels below have specific meanings. **Proved** refers to a mathematical
argument in the notes, sometimes using stated external theorems; it does
not mean proof-assistant formalization. **Computer-assisted** refers to an
exact-arithmetic certificate or finite symbolic check with a retained
verifier. **Numerical** refers to floating-point solver output and sampled
comparisons. **Heuristic** includes restricted searches, capped searches
without a completion certificate, and proposed solver policies.
**Literature** refers to inspected sources and the documented limits of the
audit. None of these labels establishes publication novelty.

## Results and final reviews by stream

### scip-rule-fidelity

**Question.** Does the earlier Python model reproduce SCIP's actual sets,
ray intersections and cuts, and is the corner-bound criterion meaningful
on real solver corners?

**Results.** **Numerical/source audit:** 610,193 ray comparisons from 7,945
attempts gave 1,211 discrepancies, about 0.2%, all assigned to the documented
cutoff, infinity, bisection or rounding cases. The old Case 4 transformation
was wrong when `κ ≠ 0`; the earlier bilinear experiments had `κ = 0` and
were unaffected by that transcription error. **Computer-assisted:** ten
stored LP-corner bounds in the starting note were infeasible underestimates;
exact rational brackets establish the corrections. **Numerical:** 3,347 of
4,578 sampled MINLPLib attempts, 73.1%, have a zero-cost face meeting the
quadratic feasible set, so their corner bound is zero. Apparent exceptional
zero-cost recession gaps in four records of `waterund32` (k=651, 715, 1138,
1292) arise from the approximately 10⁻¹⁴ dumped LP value of the bilinear
partner of `t_x612`. The drift is present in the dumped LP values; whether
it exists at the true LP corner is undetermined. These are not established
geometric gaps. The corner oracle is exact up to floating point for `ρ ≤ 2`
and uses generic three-ray KKT enumeration for `ρ = 3`, which can miss
degenerate minimizers. Only `ρ ≥ 4` uses solver estimates (232 records);
these are not global certificates.

At positive-`z_K` MINLPLib corners, SCIP's set/corner-bound ratio has median
0.923 per corner and 0.818 with instance weighting; about a third of corners
are below 0.5. Generator medians are 0.976 and 0.992. In 183 of 371
low-ratio records, SCIP's set exits a zero-rate ray that never reaches `S`.
Across all MINLPLib attempts, 37.7% generate a cut, 49.5% abort on dynamism
and 12.7% on zero basis status. The source audit also finds that
`ignorebadrayrestriction` and `ignorenhighre` do the opposite of their
descriptions; the per-expression limit counts generated cuts and resets
at restarts.

**Proved/source audit plus numerical diagnostic:** rescaling a ray rescales
its intersection parameter inversely and leaves its mathematical cut
coefficient unchanged. In the first tested restriction-polynomial piece,
scaling can turn a dynamism abort into a pass: 1,728/1,799, or 96.1%, in the
sample, and 31,926/34,834, or 91.7%, in the full diagnostic set. These are
passes of that piece, not counts of valid cuts rescued in a full solver.
They do not show that a new S-free set is needed. SCIP does not normalize
these rays in the inspected implementation.

**Solver relevance.** Correct the corner oracle before optimizing against it.
Validate any scaling change through all restriction pieces and numerical
safeguards. The recorded LP-seen rates are lower bounds on observed use,
not proof that the remaining cuts never enter an LP.

**Review.** Two rounds. Round 1's verdict was “Minor fixes”, with one
major-rated issue M1: the numerical-failure interpretation. Round 2 required
minor fixes. The last
revision's fixes were checked by the coordinating agent against the
numbers log and SCIP source for the ray-scaling claim. Not refereed.

**Key files:** [note, including corrections in §7](scip-rule-fidelity/note.md),
[r1](scip-rule-fidelity/reviews/review-r1.md),
[r2](scip-rule-fidelity/reviews/review-r2.md),
[code](scip-rule-fidelity/code/), [logs](scip-rule-fidelity/logs/).

### scip-set-selection

**Question.** Does choosing a different quadratic-free set inside SCIP make
intersection cuts pay off at roots or in full solves?

**Results.** **Proved, within the stated nondegeneracy conditions:** the
implemented candidate sets are S-free. **Heuristic:** the search samples
24 half-circle directions and refines locally when `dim λ = 2`; higher
dimensions use projected subgradient ascent. It is not a global search
over the full orbit. **Numerical:** across the three root seeds, enabling
SCIP's point-rule cuts improves the root-gap fraction by 0.114, 0.104 and
0.106, with a root CPU cost. Relative to that rule, the corner criterion
changes it by −0.008, −0.007 and −0.010; efficacy gives +0.001, +0.003 and
−0.004. These do not establish a useful replacement. The floored corner
criterion `min_j w̃_j α_j` is attained at a zero-cost ray at 81.6% of
109,389 corners in a full scan of 305 root instances. It is a positive
floored surrogate even though the true single-cut bound is zero, so it
does not measure a positive corner gain. The observed acceptance-threshold
fallback concerns fully degenerate corners (9% of the scan).

The original full-solve row capture changes tree search. Round 1 therefore
led to 120 stock-SCIP reruns, with 77 optimal solves and 43 limits. Round 2
found that cross-batch CPU timing still could not support the claimed
stock comparison. It also withdrew the attribution of the patched/stock
CPU gap to “instrumentation distortion”: batch speed explains that gap,
while row capture changes some paths. **Withdrawn:** the conclusion that enabling stock
intersection cuts improves full-solve time. Same-path comparisons do not
repair a cross-batch timing design. The original patched solved counts and
tree observations remain records of that instrumented experiment, not a
stock-SCIP performance result. Seed-0 debug-solution runs are not ordinary
seed-0 full-solve benchmarks; their audit also has unresolved warnings and
reference-value issues.

**Solver relevance.** This is a no-go result for the proposed criterion on
these samples, not a theorem that every set-selection rule fails, and not
an answer to whether stock SCIP should enable these cuts by default.

**Review.** Three rounds: r1 had one major issue, row capture changing tree
search, addressed by the stock rerun; r2 had a new major issue, cross-batch
timing, addressed by withdrawing the claims. The coordinating agent checked
that fix. Independent [round 3](scip-set-selection/reviews/review-r3.md)
verified the r2 revision (N1 and N2). Its optional O1–O3 wording fixes are
now applied; those later edits have not been re-reviewed. Not refereed.

**Key files:** [note, especially §§7.4, 9 and the r2 revision](scip-set-selection/note.md),
[r1](scip-set-selection/reviews/review-r1.md),
[r2](scip-set-selection/reviews/review-r2.md),
[r3](scip-set-selection/reviews/review-r3.md),
[code](scip-set-selection/code/), [logs](scip-set-selection/logs/).

### multiround

**Question.** Why can the best single-cut orbit rule lose over several
rounds, can a different policy repair the loss, and when does the loop converge?

**Results.** **Numerical:** in 220 paired random McCormick instances outside
SCIP, the corrected orbit rule ties the first round on average, with pooled
difference −0.001 and interval [−0.016, +0.014], but loses after rounds 10
and 20 by −0.012 [−0.017, −0.006]. The old antiparallel-ray bug matters in
the first round; its measured later-round effect is −0.001 [−0.003, +0.002].
The claim that it explains about 40% (0.017 of 0.044) of the reversal is
withdrawn. Early policy
choices lead to harder subsequent states. Bound attainment and ties do not
explain the loss by themselves: nonattaining policies also lose. Shorter
steps on many rays are a plausible common factor, with limited intervention
evidence. Neither the within-rule correlations nor the underpowered
`maj2` versus `rnd0.33` intervention test confirms causality.

**Numerical, exploratory:** one orbit round at the root followed by SCIP
rounds already carries about half the pooled loss (`o1s`: −0.006
[−0.011, −0.002] after round 10). A post hoc efficacy rule has a pooled
advantage of +0.004 in AUC over rounds 1–10, with Holm-adjusted `p = 0.025`
in its stated 14-test family; after round 10 alone Holm `p = 0.33`.
It needs fresh data.
For continued-orbit recovery, pooled `o3s` has paired-t raw `p = 0.00369`
and 12-test Holm `p = 0.0443`. The wider 36-test tally gives 0.133; removing
its three duplicate tests gives a 33-test adjustment of 0.122. Test choice
also matters: the 12-test Wilcoxon adjustment is 0.056 for pooled `o3s`,
while the 10×20 `o3s` adjustment is 0.035. This is evidence of some recovery,
not an established general repair or a gain over the SCIP baseline.

**Proved:** uniform cut depth gives convergence (Theorem 2). Uniform
pointedness supplies that depth through Corollary 3 and Lemma 4; it is not
a hypothesis of Theorem 2 itself. These results concern a loop cutting every
violated term, or a one-cut loop selecting a most-violated term (Remark 3a).
Bound-optimal choices need not be uniformly deep (Proposition 5); no failing
natural bound-optimal rule is proved. The observed cones become flat
(pointedness about 0.001), so Corollary 3 does not apply to the experiments,
and no uniform depth bound establishes Theorem 2's hypothesis there.
Even a chosen sequence of maximal SCIP-derived cuts can remain suboptimal
on uniformly pointed cones. The latter is an adversarial sequence, not a
failure theorem for SCIP's natural rule.

**Solver relevance.** The local corner bound does not control a trajectory.
The recommendation to keep SCIP's set is a comparison within this external
root-loop experiment, not a full-SCIP recommendation or a timing claim.

**Review.** Four rounds. r1 corrected major causal and experimental claims;
r2 and r3 required minor fixes. r4 confirmed the r3 fixes: verified. Its
optional duplicate-test, Wilcoxon-sensitivity and indentation remarks have
been applied. Not refereed.

**Key files:** [note, especially §§3.5, 5 and 6](multiround/note.md),
[r1](multiround/reviews/review-r1.md), [r2](multiround/reviews/review-r2.md),
[r3](multiround/reviews/review-r3.md), [r4](multiround/reviews/review-r4.md),
[code](multiround/code/), [logs](multiround/logs/).

### minor-sets

**Question.** Do tangent obstructions and restricted-family losses persist
for SCIP's implied 2×2 minors, of signature `(2,2)`?

**Results.** **Proved/source audit:** for four distinct row/column indices,
SCIP's polar-factor minor set is an orbit member; BCM's rotation family is
a subfamily. A corner minimizer with independent projected support exists; it uses at
most three rays, with a specific apex-in-span requirement for support
three. For generic data, such a minimizer uses at most two rays. Tangent edges obstruct exact orbit
attainment. **Computer-assisted:** example A has best-orbit ratio in
[0.4495347, 0.4495363], below 0.45; SCIP's numerical ratio is lower still,
0.1358003. Example S1 gives a transverse, support-one obstruction with orbit
ratio in [0.7780998, 0.7781193]. Example B has ratio in
[0.9219403, 0.9219593]. **B alone proves exactly that minor gaps are not
uniformly larger than the compared bilinear gaps.** The 24 rounded corners
provide one-sided exact upper certificates with numerical lower values;
they are not 24 two-sided exact comparisons.

**Numerical:** 258 applied cuts match the reconstructed minor formula to
4.5·10⁻¹⁵. On 157 LP corners, maximizing the local margin can worsen the
LP objective relative to SCIP's choice. Some nearest-SCIP choices look
better, but the evidence does not establish their mean advantage. These
are LP re-solves, not a replacement inside SCIP's tree. **Proved:** an
adversarial scaling makes both SCIP's value `2√δ` and the BCM family's upper
bound `11.1√δ` vanish, while the point-rule and orbit families attain
`z_K = 1` (Proposition 11, §6).

**Solver relevance.** The signature change does not remove the obstruction.
The Ipopt availability guard and off-by-default separator matter to actual
integration. For principal minors with `det M̄ > 0`, §8 proves that the PSD
cone is the unique maximal set on the positive-trace component (the NSD
cone on the negative-trace component), and SCIP's cut attains `z_K`.
Principal minors with `det M̄ < 0`, bound strengthening and branch-and-bound
were not studied experimentally here.

**Review.** Four rounds. r2 repaired an omitted bilinear comparison; r3
added the exact B comparison; r4 confirmed the r3 fixes: verified. Its
optional request to distinguish B's exact conclusion from the rounded
corners' one-sided certificates has been applied. Not refereed.

**Key files:** [note, especially §§6, 7 and 9](minor-sets/note.md),
[r1](minor-sets/reviews/review-r1.md), [r2](minor-sets/reviews/review-r2.md),
[r3](minor-sets/reviews/review-r3.md), [r4](minor-sets/reviews/review-r4.md),
[code](minor-sets/code/), [logs](minor-sets/logs/).

### ratio-bound

**Question.** Which nondegeneracy condition prevents the best bilinear
orbit cut from losing an arbitrarily large fraction of the corner bound?

**Results.** **Proved:** scaled depth `D` yields `z_A/z_K ≥ f(D)`, where
`f(D) = 1/(1 + 2D²)` for `D ≤ 1` and
`f(D) = 1/((1 + √2)D)` for `D ≥ 1`; maximal completions satisfy `z_B ≥ z_A`.
Thus bounded depth gives a uniform guarantee. Unbounded depth permits bad
families; it does not make every deep corner bad. The worst-case order
`1/D` is sharp. The depth is invariant under the specified bilinear affine
symmetries, not arbitrary coordinate transformations.

**Proved/computer-assisted:** both A and B can lose arbitrarily much even
with fixed relative-discriminant margins; these are not angle conditions.
Theorem A analytically proves the lower asymptotic constant `1/(1 + √2)`;
the upper constant 1.54 is computer-assisted (Theorem B3(4)). The old
near-boundary value 0.0280 is replaced by [0.03052, 0.03056], exact for the
binary-float data model. **Proved:** in the specified unit `w − xy` model,
SCIP's point rule has worst behavior of order `min(1, 1/(κD))`; this is not
an assertion for every quadratic representation. Support-one exactness
has the interval criterion of §5: an interior overlap gives attainment,
disjoint closed intervals give a strict gap, and the boundary case remains
open for family (A). Whether the lowered-interval test extends to (B) is
also open. The cylinder criterion `H_cyl > 1` is sufficient for attainment
in both families, with sharp threshold 1 (Theorem C(4), Proposition C3).
An angle-only criterion is impossible (Proposition C2).

**Solver relevance.** Depth measures when restricted-family optimization
has a provable guarantee. It does not predict full-LP or tree performance.
Representation scaling changes the point-rule choice, whereas consistent
ray scaling preserves a given cut.

**Review.** Two rounds: r1 required three minor fixes: the wrong explanation
for three failed box searches, numerical values presented as exact, and
unstated SCIP scope. Round 2 verified the fixes.
Optional fixes were then applied and checked by the coordinating agent.
Not refereed.

**Key files:** [note](ratio-bound/note.md), [r1](ratio-bound/reviews/review-r1.md),
[r2](ratio-bound/reviews/review-r2.md), [code](ratio-bound/code/),
[logs and certificates](ratio-bound/logs/).

### orbit-closure

**Question.** Does combining every cut from the bilinear orbit A, its
maximal completions B, or the transformed point-rule family BP eliminate
the single-cut loss?

**Results.** **Proved:** on a smooth face with `|J^c| ≤ 1`, closure exactness
holds if and only if best-single-cut exactness holds (Corollary 4). This
includes support-two directions with three rays and transfers the starting
tangent obstruction to closures. It does not assert equality of the two
bounds: the closure can improve the bound, numerically by up to 0.084 of
`z_K` for (B). Proposition 5 gives `z_1 ≥ z_cl/N`, so the closure gain over
the best single cut is at most a factor `N`. **Computer-assisted:** Theorem 9
certifies explicit closure points excluding exactness for A, B and BP at
the starting Theorem 14 corner. For A and B the closure upper bound is
49/50 = 0.98, above the certified single-cut lower value 0.97538. Equality
of closure and single-cut values there is numerical, not proved.
At the starting Proposition 16 support-one corner, A has single-cut value
at most 0.9839 and closure at least 0.9953611, but closure at most 0.999.
The B value about 0.9953622 is numerical; its separate proposed certificate
remains incomplete.

**Proved:** at the W-corner, BP has
`inf(a_1 + a_2) = (√2 − 1)/2`; Theorem 11(c) characterizes the relevant
closure points analytically and resolves the stopped experiment's intended
claim. Family (B) is exact at that W-corner (Theorem 11(d)); BP already
has infinite factor at the Theorem 14 corner (Theorem 11(a)). Here the
factor is `ρ = sup_w z_K(w)/z_cl(w)`, not closure/single-cut improvement.
No uniform factor exists across corners for A, B or BP. The A/B qualitative
unboundedness follows from the proved ratio family;
the stated quantitative certificate has the narrower computer-assisted
basis. Locally, the certified A/B factor is at least 1.1166, while local
finiteness of `ρ_A` and `ρ_B` at the Theorem 14 corner remains open.
**Numerical:** rebasing reaches the original
corner bound on five of six examples; this is not finite convergence in
general.

**Solver relevance.** More cuts can help in support-one cases but cannot
repair every tangent loss. The W-corner is removed by ordinary bound
propagation, so it proves a geometric possibility rather than a likely
solver pathology.

**Review.** Two rounds with minor fixes. r2 required explicit verifier checks
on `λ̂` and a corrected Theorem 11(c) display. They were fixed; the
coordinating agent reran all certificates, verifiers, tests and the r2
reviewer's probes. Not refereed. The mathematical stream is finished despite
two historically incomplete searches described below.

**Key files:** [note](orbit-closure/note.md), [r1](orbit-closure/reviews/review-r1.md),
[r2](orbit-closure/reviews/review-r2.md),
[original stopped-job record](orbit-closure/CLOSEOUT.md),
[code](orbit-closure/code/), [logs and certificates](orbit-closure/logs/).
Local result numbers now are Lemma 12, Proposition 13 and Corollary 14;
these must not be confused with the starting note's Theorem 14 or
Proposition 16.

### intersection-literature

**Question.** What is already known, what survives as a plausible contribution,
and what do the accessible SCIP studies establish?

**Results.** **Literature/proved comparison:** much of the starting Theorem
1 is classical cut-generating-function sufficiency or dominance. The
transversality criterion is a modest general sufficient condition; its
examples have close precedents, and Proposition 2(b) is exactly
Kılınç-Karzan–Yang Example 4.3 after swapping coordinates, with a quadratic
sublevel set in place of their discrete sequence. Their printed
Corollary 3.12 needs an additional ray-avoidance condition; the corrected
form Corollary 3.12′ is proved given KY Proposition 3.11; not every step
of that proposition's proof was checked, and KY is an unrefereed draft.
Kılınç-Karzan–Steffy Corollary 2, for relaxed cut-generating functions,
has no cone hypothesis. Eckstein–Nediak's deepest-cut generation over S-free
sets is a major missing precedent. The Lorentz parametrization uses known
automorphism geometry; it extends BCM's known rotation subfamily to three
parameters rather than introducing set search as an idea.

**Proved:** containment of the feasible displacement set in the ray cone
is sufficient for attainment with nonnegative weights. **Numerical:** none
of the 120 sampled McCormick LP corners has a full projected ray cone at
the stated tolerance; the full-cone sufficient condition does not explain
those attainments. For bilinear `S`, containment holds if and only if the
projected cone is full, so neither part of Proposition A applies to any
of those 120 corners. **Literature:** the accessible development-SCIP study
is a root-gap comparison; density and lack of a rule predicting benefit
explain the default-off choice. The audit did not access the journal
version's full computations or the monoidal paper's computations, and
therefore does not exclude a published branch-and-bound comparison there.

**Solver relevance.** Reframe the contribution around specific geometric
limits and quantitative guarantees. Do not present standard dominance,
inertia arguments, or a failed search as novelty.

**Review.** Three rounds. r1 found major missed-source and argument issues;
r2 required minor fixes; r3 verified the revision. Not refereed.

**Key files:** [note, especially §§7–10](intersection-literature/note.md),
[r1](intersection-literature/reviews/review-r1.md),
[r2](intersection-literature/reviews/review-r2.md),
[r3](intersection-literature/reviews/review-r3.md),
[source manifest](intersection-literature/sources/MANIFEST.md).

### split-practice

**Question.** Are fixed-rank exact separation and general split searches
useful at actual SDP optima, and what objective should a separator optimize?

**Results.** **Numerical:** the tested root optima have numerical rank 1–5;
after the implemented families, 171 of 187 points have rank 1, four closed
or nearly closed points have ranks 2–12, and the 12 selected residual-gap
points have rank 9–39. Eleven of the latter have established numerical
gaps; the linear DM60 case has an unresolved optimum and an upper-bound
gap. Exact rational grid-neighbor enumeration corrects the original root
implementation's coefficient blow-up. All nine fractional rank-one roots
have short exact raw maximizers of their neighbors. In contrast, all 13
returned non-root vectors have maximum coefficient 30–69618975: eight
are unviolated at the stored point and five have normalized violation at
most 8.2·10⁻⁶. At four completed nearly closed neighbors, all exact
maximizers are long; the returned vectors are within 1.5% of shortest.
Rank truncation and the raw objective can therefore genuinely cause poor
non-root choices.

**Proved:** normalized violation is at most `1/(4‖w‖²)` at psd input
(notation of Lemma A); primitive directions suffice. Raw violation is at
most 1/4 for every psd `Y` with `Y₀₀ = 1` (Proposition C(a)); rational input
has the stated attainment criterion. Restricted 0/1 separation is
NP-complete in the ordinary sense even
at rank one, while unrestricted separation has the fixed-rank tractability
of the starting theorem. A fixed positive normalized threshold gives a
polynomial search. The signed extension of the restricted-hardness claim
is not proved here. **Numerical/capped:** 103 completed searches plus 17
adaptive norm-bound post-checks give 120 of 123 finished or numerically
certified normalized searches. Three capped results remain uncertified;
two are dense and were shown to be cap-sensitive.
These post-checks use floating-point bounds, not exact certificates.

**Numerical/heuristic:** the support-at-most-three extension closes six of
the 12 selected residual instances; general splits close four more. The
extension also changes supports one/two and right-hand-side selection, so
the gain is not attributable solely to ternary cuts. Dense exceptional
rounds cost about 2400 seconds for 0.003784 and 0.002216 percentage points
of additional improvement. The proposed policy—small-support splits first,
budgeted normalized search later—is supported by these root experiments,
not validated by tree performance.

**Solver relevance.** Validate a rational-neighbor candidate at the original
point, retain completion flags, account for discarded eigenvalues, and
avoid using raw violation as a proxy for useful progress. Numerical low
rank does not invalidate or directly instantiate an exact-rational theorem.

**Review.** Two rounds. r1 required major implementation and interpretation
fixes; r2 required minor non-root reporting fixes, now applied. The
coordinating agent reran `check_nonroot_r2.py` and
`summarize_revision_r2.py`. Not refereed.

**Key files:** [note](split-practice/note.md), [r1](split-practice/reviews/review-r1.md),
[r2](split-practice/reviews/review-r2.md), [code](split-practice/code/),
[logs](split-practice/logs/), [source manifest](split-practice/sources/MANIFEST.md).

### binary-separation

**Question.** Can the starting integer-QP hardness be extended to the binary
rounded-psd/hypermetric analogue, including points in familiar relaxations?

**Results.** **Proved:** an exact-cover Gram construction gives strong
NP-completeness of hypermetric, Boros–Hammer binary split, rounded psd and
gap-1 separation, as well as unrestricted k-gonal and the other named
classes specified in the note. Hypermetric membership is strongly coNP-complete. The scaled
construction uses `N = 8n + 2p + 1` and a polynomially bounded scale, repairing
the first version's bit-complexity gap. Hardness persists at positive
definite points passing the metric/Boolean-quadric triangle constraints,
including the facet-qualified variants proved in the note. Fixing support,
gonality or rank gives the specified polynomial or parameterized searches;
these do not contradict unrestricted hardness.

**Proved/computer-assisted checks:** for the stated scaled instances the
maximum Boros–Hammer violation is `1/(2N)` and the Padberg clique maximum
is `1/(4N)`. In Corollary 10, the pure odd-clique and inequality-(18)
maxima are `(q + 3)/(4qN)` at `εd̃` and `(q + 2)/(4qN)` at the switched
point `d″`, respectively. The first is the maximum over both pure
hypermetric and odd clique families; (18) uses Letchford's 2022 numbering.
Here `q` is the construction's
parameter, not the quadratic function. Gap-0 separation is NP-complete for
general matrices, with strong NP-completeness not shown. Its psd case is
easy; general-gap separation on psd
input remains open.

**Literature.** The latest inspected statement of the hypermetric separation
question being open is Letchford (2022). The reduction is a plausible
resolution of that question, subject to a full prior-art check. Several
classic sources were available only through citations or extracts. Unread
sources include Deza–Laurent Chapter 28 in full, Laurent–Poljak (1996),
Boros–Hammer (1993) and Erdahl (1992). The short proof uses standard parts
and may already be known to specialists; the checked sources and failed
searches do not establish priority.

**Solver relevance.** The result strengthens the worst-case barrier even
inside standard relaxations. It does not measure separator speed or rule
out finding useful cuts above a fixed practical threshold. The construction
does not establish constant conditioning or hardness of constant normalized
violation.

**Review.** Three rounds. r1 found a major strong-hardness encoding issue
and proposed the fix; the first author revision applied it.
r2 repaired a new major clique-class issue and strengthened the result;
r3 required minor fixes. Those fixes, including the new maximizer proof
step for `(q + 3)/(4qN)`, were checked by the coordinating agent: the step
was re-derived and `code/check_r3_violation_maxima.py` was rerun, with values
matching the formulas. Not refereed.

**Key files:** [note](binary-separation/note.md),
[r1](binary-separation/reviews/review-r1.md),
[r2](binary-separation/reviews/review-r2.md),
[r3](binary-separation/reviews/review-r3.md),
[code](binary-separation/code/), [logs](binary-separation/logs/).

### three-var-computation

**Question.** Does selective enforcement of the three-positive family improve
on Shor/RLT/triangles, Khajavirad and Anstreicher–Puges, at less cost than
an exact three-variable lift?

**Results.** **Proved:** separation of the family reduces to 15 bordered
systems; exact triple-hull depth and a triple-level gain bound provide
comparison tools. The gain lemma does not cover shared auxiliary moments
across triples. “Safe” dual bounds in the experiments are floating-point
calculations, not interval certificates. **Numerical:** Shor/RLT/triangles
is already tight to relative 10⁻⁶ on 82/99 `spar` instances and on all
18,000 small dense `spar`-style instances. In the AP variant, one of 12,000
instances has relative gap 3.6·10⁻⁶, closed by `KA`; the family adds nothing
there. These generators do not reproduce AP's published gap distribution.
Three random-sparse instances have unresolved `U − B` of 0.13–0.39, which
may reflect a true gap or heuristic error. Stored gain terms are 5.97%,
2.82% and 19.88% of those gaps, subject to numerical feasibility and depth
accuracy; no violated family orientation was found.

Only `spar090-075-1` received the strict complete residual-triangle re-audit:
117,480 triples give computed minimum depth −8.10·10⁻⁹. The gain term at
computed depths is 0.045% of the safe-bound gap, or 0.54% including the
primal-to-safe margin. A triangle residual forces exact minimum depth at
most −1.4164750622436273·10⁻⁸, hence a gain term at least about 0.079%,
or 0.58% including margin. **This is a lower bound on the upper-bound
expression, not a lower bound on attainable improvement.** Conditional
upper limits are about 0.56%/1.05% if exact minimum depth is at least −10⁻⁷,
or 0.60%/1.10% if each computed depth overestimates exact depth by at most
10⁻⁷. Neither premise is certified. The old 70.01% estimate reflected an
unenforced base triangle, not a demonstrated triple-family opportunity.

**Numerical:** on 109 hard three-variable objectives, `K` closes about
91% of the gap, `A` about 58%, `KA = K`, and the family 100%. All 256,556
sampled points satisfying the base relaxation and all family orientations
lie in the triple hull within accuracy; this is evidence for Conjecture 1,
not proof. On constructed chains and cacti, through 9000 variables, family
blocks reach the exact-lift bound to solver accuracy, while `KA` misses
0.31–3.73 percentage points of gap closure. Loaded-machine time factors
1.1–14 favor the family against the original exact-lift comparison, but
selection changes block counts, and other chain runs reverse the timing
order when the exact lift uses family selection. On cacti, `XF/F` is
2.1–5.7 within the same run: block type accounts for most of the advantage
there, though successive iterates select slightly different triple sets.
When hard triangles share edges (`ht`), tested methods close at most 0.514%
of the gap. No quiet-machine timing
or branch-and-bound conclusion follows.

**Solver relevance.** The family is a useful compact option on genuine
triple-gap structures. Most natural tested gaps leave little for any
triple-local constraint to improve. The observed average 1.02 orientations
per violated triple is an empirical cost observation, not a worst-case bound.

**Review.** Two rounds with minor fixes. Round 1's main finding was the
70.01% triangle artefact, with a strict re-audit by the reviewer; it also
raised AP-generator mismatch and timing. Its verdict required issue 1 to
be fixed before verification. Round 2 raised exact-depth headline precision
(the 0.079% lower gain-term bound and conditional 0.56%/0.60% upper limits),
cost interpretation and review-state reporting. The author corrected the
review's `ε = 10⁻⁷` sensitivity premise: an error bound of 10⁻⁷ alone also
requires the negative stored minimum, giving the 0.60% alternative.
The coordinating agent checked the last revision's
bound arithmetic and closeout checks. Not refereed.

**Key files:** [note](three-var-computation/note.md),
[r1](three-var-computation/reviews/review-r1.md),
[r2](three-var-computation/reviews/review-r2.md),
[code](three-var-computation/code/), [logs](three-var-computation/logs/),
[data](three-var-computation/data/).

### three-var-completeness

**Question.** Do the symmetry copies of the three-variable family complete
the hull, and does a finite SDP description remain possible with four
positive variables?

**Results.** **Proved:** diagonal caps `Y_ii ≤ x_i` are necessary for the
literal full moment hull; rounding identities connect the capped moment
relaxation to the positive-loop hull `H_3^+`. For nonnegative square
coefficients, the disjoint system
is exact when the product of the three cross coefficients is nonpositive,
using the stated BNW external theorem. Coordinate complementation reduces
the remaining strict sign patterns to supermodularity. Only six copies matter within each such sign pattern.
Five boundary strata yield extreme rays, with exact symbolic checks;
exposedness is not proved for them. **Open:** Conjecture 2.11 is the
three-positive completeness assertion for the positive-loop hull `H_n^+`
(here `n = 3`), equivalent to equality of the capped moment relaxation
with `QPB3`. The computational stream's Conjecture 1 is
stronger; the formulations should not be identified without the caps and
stated equivalence.

**Numerical:** 36,398 valid rays, including 1,371 outside the disjoint cone,
produce no missing ray at tolerance 10⁻⁶. Contact enumeration covers only
specified isolated point-contact configurations, not every boundary stratum.
Of 265 exact-contact attempts, 241 failed; failure is not infeasibility.
The successful and direct-retest searches supply evidence only.

**Proved:** Theorem 4.2 excludes a finite SDP lift for the full box quadratic
hull and positive-loop hull `H_n^+` when `n ≥ 4`, with the classical
three-variable lift making the dimension threshold sharp. Theorem 4.4
extends the obstruction to the stated polytopes of dimension at least four
with a simple vertex and pointed polyhedral cones of dimension at least five with
a simple extreme ray. Theorem 4.6 lowers the positive-induced graph
obstruction from a `K_5` minor to a `K_4` minor. These arguments use the full
Bodirsky–Kummer–Thom machinery; they are not merely applications of the
older `CP_5` corollary. Minor closure is proved. Paths and stars on four
positive vertices, and the remaining series-parallel classification, stay open.

**Solver relevance.** For a three-variable box QP already using the disjoint
system, family blocks are needed only when the cross coefficients have
positive product (Theorem 2.5). In larger or constrained models, the relevant
quadratic on a triple is a dual aggregate of objective and constraints;
objective signs alone do not justify omitting blocks. If Conjecture 2.11
holds, `R` plus caps is exact, but uses 27 localizing and 24 five-by-five
blocks, more than the six four-by-four DNN blocks of the Anstreicher–Burer
lift. Completeness is not needed for validity of the existing cuts.
The four-variable theorem rules out every finite SDP lift of the full
object, not good relaxations or useful special graph classes.

**Review.** Two rounds with minor fixes. r2 corrected failure reporting and
presentation; fixes were checked by the coordinating agent against the
logs. The S1 symbolic rerun was performed by the author during the r2
revision, recorded in `logs/check_boundary_rank_symbolic_r2_revision.txt`.
Not refereed. BNW is a recent preprint whose proof was read but not verified
line by line in this stream.

**Key files:** [note](three-var-completeness/note.md),
[r1](three-var-completeness/reviews/review-r1.md),
[r2](three-var-completeness/reviews/review-r2.md),
[code](three-var-completeness/code/), [logs](three-var-completeness/logs/),
[source manifest](three-var-completeness/sources/MANIFEST.md).

## What changed relative to the starting results

The [starting intersection-cut note](../research-20260928b/sfree/optimal-intersection-cuts.md)
and its [first review](../research-20260928b/reviews/sfree-review.md) and
[recheck](../research-20260928b/reviews/sfree-recheck.md) supplied the
unrestricted best-cut theorem, a bilinear restricted-family obstruction
and initial LP experiments. This program adds quantitative depth guarantees,
closure counterexamples and improvement factors, signature-`(2,2)` minor
obstructions, convergence conditions and counterexamples, and a much more
careful source audit. It also finds exact numerical errata and replaces the
initial favorable single-cut narrative with conditional solver evidence.
Some apparent “new” pieces of the starting theory are classical or close
consequences of known results.

The [starting split-separation note](../research-20260928b/side-results/split-separation-np-complete.md)
proved strong hardness for integer-QP split separation and fixed-rank
tractability. The binary Gram reduction is a substantive extension to
classes whose separation remained open in the inspected literature; its
positive-definite and triangle-feasible variants sharpen the statement.
The practical stream adds normalization bounds, a fixed-threshold search,
validated lattice-neighbor experiments and a clear distinction between
numerical and exact rank.

The [starting three-variable family](../research-20260925/three-positive-family-sdp.md)
and [publication assessment](../research-20260925/publication-quadratic-assessment.md)
supplied validity, a compact lift, separation from named relaxations and a
`K_5`-minor obstruction. This program supplies the requested comparisons,
a triple-gain bound, rounding and sign-class reductions, boundary extreme
rays, a precise capped completeness conjecture, the sharp four-variable
nonrepresentability threshold and the stronger `K_4`-minor obstruction.
It does not prove family completeness or general practical superiority.

## Errata and updates to apply to older notes

The files below were **not edited**. This list collects the streams'
corrections, attribution fixes and material qualifications. Some entries
supersede an accurately dated open question rather than correct a false
original theorem. Corrections confined to interrupted drafts of the current
streams remain in their own revision histories.

### Intersection-cut theory and literature

1. [Optimal intersection cuts](../research-20260928b/sfree/optimal-intersection-cuts.md),
   §2, Theorem 1 Remark (ii), and §10.2: replace the generic sufficiency
   attribution with CWY Theorem 1.1, CCDLM Theorem 6.3 and
   Kılınç-Karzan–Steffy Proposition 5 under their distinct cone hypotheses;
   their Corollary 2 concerns relaxed cut-generating functions and has no
   cone hypothesis. Use the corrected form of Kılınç-Karzan–Yang
   Corollary 3.12, including the extra ray-avoidance condition, proved given
   KY Proposition 3.11. Not every step of that proof was checked, and KY is
   an unrefereed draft. Qualify Theorem 1(4) as a
   general sufficient transversality condition, with known illustrative
   examples. Attribute Proposition 2(a)'s mechanism to CCDLM Example 6.1's
   variant and KY Example 4.5; Proposition 2(b) is KY Example 4.3 with
   coordinates swapped and a quadratic sublevel set replacing their discrete
   sequence. See [literature §8](intersection-literature/note.md#8-corrections-to-earlier-notes).
2. The same older file, §10.2, deeper-cuts paragraph: add Eckstein–Nediak,
   *Annals of Operations Research* 139 (2005), deepest-cut search over
   S-free sets, and Glover (1973)/Konno (1976) for the coefficient-wise order.
   Clarify that Balas–Margot, *Mathematical Programming* 137 (2013), 19–35,
   online 2011, fixes the S-free set and tightens the relaxation through
   point-ray collections: a complementary operation.
3. The same file, §§8 and 10.2: BCM's (14a) is exactly the rotation subfamily
   of the orbit, and SCIP's minor choice is the polar-factor member. BCM v7,
   p. 24, already warns that a violation-maximizing parameter need not give
   the deepest cut. Describe the three-parameter extension of a known
   one-parameter family. The precision is also recorded in
   [minor §9](minor-sets/note.md#9-relation-to-earlier-notes-and-prior-work).
4. The same file, §10.1, and
   [s-free scouting report](../research-20260928b/scouting/s-free-intersection-cuts.md),
   §1.3: Porembski (2004) is *Operations Research* 52(6), 942–953;
   cone adaptation is the separate *JOGO* 24 (2002), 89–107 paper.
   The 2001 *JOGO* 20(2) page discrepancy remains unresolved: Crossref
   109–132 versus zbMATH 113–136. Do not silently select one.
5. The scouting report, §1.1, BCM entries: replace local-KB Theorems
   4.3/4.7/4.10/4.15 by v7 Theorem 15/Corollary 16, Theorem 19,
   Corollary 25 and Theorem 27, respectively.
6. The optimal-intersection file, §10.1: retain September search counts as
   dated history, but add the October audit's 17 Semantic Scholar entries
   and recovered Chmiela citations. Counts and a failed search do not
   establish priority. The audit found no set-selection result among those
   inspected citations.
7. The optimal-intersection file, §§5 and 9.4: default-off is correct;
   the published rationale is density and lack of a criterion for benefit.
   State that no branch-and-bound comparison was found in accessible sources,
   with the journal and monoidal computations explicitly unread.
8. The optimal-intersection file, Summary “Open” and §10.2, and the
   scouting report, §2 OQ1(a): orbit/completion/point-rule closure
   exactness is now false in general. Distinguish a best single cut from
   the intersection of all cuts. The support-two directional equivalence
   is proved under the stated smoothness hypotheses, not for every direction;
   support one supplies a strict improvement example. The untraced §3.4
   reference has been dropped. See
   [orbit §§4–8, 11](orbit-closure/note.md).
9. The optimal-intersection file, §8.5, Theorem 14 and its second rational
   instance, and §8.6, Proposition 16: supplement numerical values 0.97539,
   0.83477 and 0.98385 with the exact A brackets
   [0.9753853, 0.9753864], [0.8347663, 0.8347772] and
   [0.9838465, 0.9838468]. The second bracket fixes four decimals, not all
   five quoted digits. See [minor §9](minor-sets/note.md#9-relation-to-earlier-notes-and-prior-work).
10. The optimal-intersection file, §8.6, near-boundary `_8` restart 3,
    and Summary “Adversarial search” and “Open” (`0.028 near ∂S`):
    withdraw 0.0280 and the infeasibility claim from 0.029 onward. The exact
    bracket is [763/25000, 191/6250] = [0.03052, 0.03056] for the code's
    exact binary-float instance and scaled rays; floating `z_K` is
    `1 + 6.7·10⁻¹⁶`. The orbit stream's early 0.0268 is also unreliable,
    not an alternative answer. Other archived restart changes are
    `_7` restart 0: 0.375→0.404; `_7` restart 3: 0.500→0.509;
    `_8` restart 2: 0.9375→0.9985. The quoted 0.6106, 0.6224 and 0.4526
    are reproduced numerically. The Summary's “97%” gap remains roughly
    correct with a ratio about 0.0305. See [ratio §6.1](ratio-bound/note.md#61-corrections-and-additions-to-the-sfree-note).
11. The same older file, §8.6 and §11's code description of B searches:
    `interior_shift` searches completions only after making the base orbit
    contain the apex. Values are valid lower bounds, not unrestricted
    B optima. On the specific proved bad family, certified 136.7 versus
    137 bounds limit this restriction's loss to below 0.22%; this does not
    certify every old B search.
12. The same file, Summary “Open” worst-case question (including
    `0.028 near ∂S`, corrected in item 10) and the final angle/margin
    discussion in §8.6: scaled depth gives the sharp worst-case order `1/D`;
    bounded depth gives a uniform lower guarantee. No angle-only threshold
    works, replacing the tentative cosine-about-0.16 statement. A fixed 1%
    margin does not prevent ratios tending to zero; it changes the constant.

### Corner-oracle and multiround numbers

13. [Optimal intersection cuts](../research-20260928b/sfree/optimal-intersection-cuts.md),
    §§9.1–9.2 and 11, and its `sfree/code/core.py`, `two_ray`/
    `corner_bound`: reject infeasible candidates from antiparallel projected
    rays and degenerate polynomial evaluation. The exact ten affected
    stored corners are seed 11 trials 3, 110, 122 and seed 12 trials
    14, 28, 71, 115, 140, 142, 174. The 77-random-corner validation did
    not cover the problematic LP pattern and was not rerun by the fidelity
    stream. Fidelity calls it “probably not affected”; the firmer claim
    that it lacked such corners is multiround's. Other uses of
    `core.corner_bound` on validation, adversarial and random corners were
    not rechecked by fidelity. The multiround sample finds 55/420 affected
    corners, 13%.
    See [fidelity §7.1](scip-rule-fidelity/note.md#71-ten-stored-corner-bounds-in-section-92-were-wrong-coretwo_ray)
    and [multiround §6](multiround/note.md#6-corrections-to-earlier-notes).
14. The same older file, §9.2: apply the following corrections. The two
    samples have 47 and 73 corners; parentheses contain medians.

    | Quantity | Old, 47 / 73 | Corrected, 47 / 73 |
    | --- | --- | --- |
    | SCIP corner increment | 0.700 (0.839) / 0.591 (0.634) | 0.724 (0.864) / 0.616 (0.647) |
    | Orbit corner increment | 0.755 (1.000) / 0.648 (0.795) | 0.783 (1.000) / 0.675 (0.800) |
    | SCIP LP re-solve | 0.895 (0.957) / 0.870 (0.934) | unchanged |
    | Orbit LP re-solve | 0.929 (1.000) / 0.907 (0.999) | 0.931 (1.000) / 0.910 (1.000) |
    | Corner-optimal-cut LP re-solve | 0.755 (1.000) / 0.648 (0.795) | 0.783 (1.000) / 0.675 (0.800) |

    SCIP below 0.9 of the corner bound changes from 26/120 to 27/120;
    below 0.5 remains 3/120. Attainment in all 120 sampled corners survives
    the corrected oracle within the reported numerical accuracy. In §9.2's
    LP comparison, orbit better by more than 0.01 changes 60→62 of 120;
    orbit worse by more than 0.01 changes 26→22. These counts were checked
    by substituting the ten saved corrections into the original 120 records.
15. The same older file, §9.3: in the fidelity rerun, 4×4 orbit round 1
    changes 0.863→0.891; the later quoted 0.967/0.998/1.000 are unchanged.
    The 6×8 orbit sequence at rounds 1/2/3/10 changes
    0.701/0.796/0.832/0.887→0.701/0.799/0.828/0.901;
    completion B ends at 0.904 instead of 0.881. Completion B's 4×4 round 1
    also changes 0.863→0.891; its 6×8 rounds 2/3 change
    0.796/0.832→0.799/0.828. The 4×4 comparison “8 of 12 better, 1 worse”
    becomes “9 of 12 better, none worse”, at threshold 0.01.
    The corner-optimal rule's
    4×4 sequence changes 0.722/0.796/0.796/0.796→
    0.781/0.854/0.854/0.854; its 6×8 constant changes 0.584→0.613.
    The later multiround implementation obtains orbit 0.904 instead of
    0.887 at round 10, rather than the fidelity implementation's 0.901;
    preserve this implementation distinction. SCIP's quoted sequences are
    unchanged. Qualify §9.3's “wins the first round on average”: the larger
    corrected sample ties on average (−0.001 [−0.016, +0.014]). The withdrawn
    claim attributed about 40% (0.017 of 0.044) of the later reversal to the
    bug; the larger sample does not support it.
16. The same file, §9.4: qualify single-cut strict improvement as a
    same-corner comparison. It does not imply a better multiround trajectory;
    on the larger corrected sample the first-round mean ties and later rounds
    lose. Do not replace this with a universal causal claim about degeneracy.
17. The same file, §11, `sfree/code/scout_sfree.py`, `ms_set`, Case 4:
    correct the transformation for `κ ≠ 0`; the ZIB source formula is
    correct. The old bilinear experiments used `κ = 0`, so this is not
    their numerical erratum. See [fidelity §7.2](scip-rule-fidelity/note.md#72-case-4-of-the-earlier-model-scout_sfreems_set-is-wrong-for-κ--0).
18. The same file, §3, Theorem 4(3)'s `core.two_ray` closed-form claim:
    also validate candidates in `core.corner_bound` with
    very small weights or constant restricted quadratics. The selection
    stream found nine infeasible outputs in 408 tested cases; discarding
    them avoids a false bound but does not prove the remaining search finds
    the true optimum. See [selection §4.2](scip-set-selection/note.md#42-a-robustness-problem-in-the-sfree-code-correction-to-earlier-code).

### Integer and binary split separation

19. [Split-separation note](../research-20260928b/side-results/split-separation-np-complete.md),
    Summary novelty caveat, §6 “The binary analogue is open”, and §8 final
    Limits bullet: retain the original statement as dated history, then add
    the binary stream's strong-hardness resolution and its psd/triangle
    variants. Also update §8's Limits bullet “The hard points need not
    satisfy binary structure”: binary Corollary 6 supplies hardness with
    `diag(X) = x`. The same update applies to
    [split review](../research-20260928b/reviews/split-separation-review.md),
    the status table's “still open”, the contribution list's “open binary
    analogue” and the requested §2.1 caution, as well as §8.3. The historical quotation in
    [split final review](../research-20260928b/reviews/split-final-review.md),
    table row “§6 binary analogue”, remains a correct quotation.
20. The split note, §6 attribution: Galli–Kaparis–Letchford did not originate
    rounded psd inequalities. Their §2 lists earlier references; the name
    occurs in Letchford–Sørensen (2012), (10). In Boolean-quadric form these
    are Boros–Hammer inequalities, with the stated 1993 antecedent.
21. The split note, §6 reduction: rounded-psd separation to hypermetric
    separation is Letchford–Sørensen (2012), Proposition 19; GKL reproduce
    it as Theorem 3. Cite the published GKL, *Operations Research Letters*
    40 (2012), §4, p. 151, alongside the 2011 preprint when quoting openness.
22. Citation caution when updating the split note's §6 bibliography:
    the split note does not cite Laurent–Poljak, but GKL 2012's reference
    list confuses two papers. *Gap inequalities for the cut polytope* is *European Journal
    of Combinatorics* 17 (1996), 233–254, DOI 10.1006/eujc.1996.0020.
    *On the facial structure of the set of correlation matrices* is *SIAM
    Journal on Matrix Analysis and Applications* 17 (1996), 530–547,
    DOI 10.1137/0617031.
23. The split note, §6 “does not settle the binary case”: true of its old
    construction, but the Delaunay obstruction is not intrinsic; the new
    exact-cover construction meets it. §§6–7's “post-2012 literature not
    searched” is superseded by the documented search, whose latest inspected
    openness statement is from 2022. Do not convert this into a verified
    absence of later work. See [binary §8](binary-separation/note.md#8-corrected-status-for-a-paper-and-corrections-to-earlier-notes).
24. The split note, §8 fixed-rank tractability and practical-rank discussion:
    specify exact rational psd input. Numerical rank/truncation changes the
    input and needs validation at the stored point. Root coefficient blow-up
    in the old practical implementation is corrected by exact reduction;
    long non-root maximizers can remain intrinsic to the raw objective on
    the chosen neighbor. Add the tested rank distribution, without treating
    it as a distribution-free claim. See [split-practice §11](split-practice/note.md#11-reuse-of-the-first-agents-work-corrections).

### Three-positive quadratics

25. [Three-positive exploration](../research-20260925/three-positive-exploration.md),
    §4 Theorem 3 and its scope paragraph, and §7's unresolved-target
    paragraph: strengthen `K_5` to `K_4` using
    the new Theorem 4.6. Four-positive components containing a `K_4` minor are
    covered; series-parallel components remain outside the obstruction.
    In [publication assessment](../research-20260925/publication-quadratic-assessment.md),
    the “Sparse obstruction to every finite SDP lift” row and “Remaining
    questions” section need the same update and the sharp full-four-cube
    theorem. State the stronger dependence on full BKT machinery rather
    than only Corollary 3.18.
26. [Three-positive counterexample](../research-20260925/three-positive-disjoint-counterexample.md),
    the exposed-extreme-ray statement in its open five-contact region:
    retain that scope. Boundary strata S1–S5 are now proved extreme, not
    proved exposed. See [completeness §6](three-var-completeness/note.md#6-corrections-to-earlier-notes-and-to-the-interrupted-draft).
27. [Family note](../research-20260925/three-positive-family-sdp.md), §3:
    the disclaimer that all symmetry copies are not proved complete remains
    correct. For the literal full hull add `Y_ii ≤ x_i`; six copies suffice
    within each strict supermodular sign pattern. Cite the current
    Conjecture 2.11, with its capped equivalence. In the exploration's
    random-search discussion, §6, the 21,000 tested instances already had
    strictly positive diagonals and positive cross coefficients, hence were
    in the supermodular class. The sign-class reduction confines the missing
    case to that class; their lack of gaps reflects the small gap region,
    not sampling the wrong sign class, and is still not completeness.
28. The family note, §5, and publication assessment, cost comparison
    and remaining experiments: the classical six-tetrahedron lift is valid,
    but an exact five-tetrahedron comparator is also known and is used here.
    The experiment request is now partly answered on constructed instances;
    no tree comparison is supplied. The observed 1.02 orientations per
    violated triple does not invalidate the earlier worst-case allowance
    for 24 copies or prove a universal cost advantage. See
    [computation §§5 and 6.2](three-var-computation/note.md).

### Extracted SCIP cuts

29. The optimal-intersection file, §11's code-description paragraph:
    retain that its original “SCIP's set” was a reimplementation, then add
    that [fidelity §8](scip-rule-fidelity/note.md) now checks cuts extracted
    from SCIP and finds the sets and steps match within the stated numerical
    and root-finder qualifications.

## Connections and tensions

The fidelity and set-selection streams diagnose different sources of a
zero criterion. Fidelity's 73.1% is a zero-cost face meeting the quadratic
feasible set in 4,578 MINLPLib attempts. Selection's 81.6%, often rounded
to 82%, is a floored criterion `min_j w̃_j α_j` attained at a zero-cost ray
in a full scan of 109,389 corners on 305 root instances. The surrogate can
be positive while the true single-cut bound is zero. Only the fully
degenerate cases (9%) exhibit the observed acceptance-threshold fallback.
They use different tests, populations and
instrumentation; the percentages are not competing estimates of one rate.
Both warn that a local bound criterion often supplies little discrimination.

Multiround's “keep SCIP's set” conclusion concerns an external LP loop
compared with its tested alternatives. Selection's no-go conclusion concerns
the implemented candidate search inside SCIP and cannot determine the
stock off-versus-on full-solve question after timing withdrawal. These
results agree on the limits of corner-bound maximization but do not jointly
establish a default parameter policy. Minor LP re-solves independently show
that the best local margin can produce a worse full LP objective.

Ray scaling and set selection also answer different questions. Ray scaling
can preserve an existing mathematical cut while repairing a first-piece
numerical rejection condition. Changing the quadratic representation can
change SCIP's selected set and its quality, as in the ratio stream. Neither
finding permits silently exchanging representations or skipping numerical
validity checks. Fixing numerical generation may be cheaper than choosing
a more complicated set, but its actual benefit is unmeasured.

Ratio bounds describe a best *single* restricted cut. Orbit closure shows
when combining cuts improves that bound and when it cannot make it exact.
On a smooth face with `|J^c| ≤ 1`, combining cuts can improve the bound,
but cannot make it exact unless the best-single-cut bound already is exact.
This transfers support-two tangent obstructions directly; support-one
examples permit strict closure gains. Minor geometry broadens the obstruction
to signature `(2,2)`. B's exact comparison prevents the unsupported stronger
claim that these higher-signature gaps are always larger.

Binary hardness and split-practice tractability are compatible. The hard
points need not have the low exact rank seen at many roots, and the
constructed violations shrink with size. Fixed-threshold normalized search
can be polynomial even when exact all-cut separation is hard. Numerical
rank rises after easy gaps close; exact enumeration at a rank-truncated
neighbor can return cuts that are useless at the original point. Thus neither
hardness nor low-rank root success predicts a useful full separator alone.

The computational family conjecture and completeness conjecture are linked
through rounding and caps, but have different scope. Numerical agreement
with the exact triple lift on constructed chains is not proof of the full
three-variable description. Conversely, four-variable nonrepresentability
does not prevent useful triple-local relaxations. The gain lemma explains
why even a complete triple hull might add little on many natural instances;
its scope excludes methods coupling auxiliary moments across triples.

## Work not run, and its priority

No experiments in this section were run for this closing record. “Recommended”
means needed for the indicated stronger claim or proposed paper; “optional”
means the current stated result does not depend on it.

| Work | State and reason | Priority |
| --- | --- | --- |
| Quiet-machine, interleaved stock SCIP off versus stock point-rule cuts | The 120 stock reruns came from a different batch; timing claims were withdrawn. Instrumented capture also changes trees. | Recommended before any full-solve benefit or default-setting claim. Use the same batch, load control, seeds, limits and capture-free binaries. |
| Ordinary seed-0 full solves, followed by a broader seed comparison | Seed-0 short debug runs are not full-solve performance measurements. The existing full comparison uses seeds 1 and 2 and cannot repair timing by itself. | Recommended for a solver-performance paper; include the new stock baselines and report path variability. |
| Complete debug/reference-value audit | Saved runs include unresolved warning and reference-value cases; zero final reported violations does not settle them. | Recommended before asserting numerical validity of the modified solver across that test set. |
| Implement and validate ray normalization | Present evidence covers first restriction-piece abort conditions, not actual cuts through every piece and safeguard. | Recommended before claiming rescued cuts or benchmarking a scaling change; use high-precision checks on difficult cases. |
| Strict residual-triangle audits on the other 16 `spar` instances | Two size-100 retries failed the residual target, one size-125 attempt stopped for cost, and 13 were not attempted. Only one complete strict audit exists. | Recommended before a uniform benchmark conclusion. Exact or interval bounds would be needed for certified gain limits. |
| Quiet timing for selective family versus exact lift, with matching triple selection | Shared-machine timing and different block selection confound the observed advantage. | Recommended for a computational-method paper; separate selection cost, block cost and iterations. Natural instances and node gaps are also needed for a solver claim. |
| Fresh multiround holdout with a fixed criterion and test family | Efficacy and recovery choices followed observed data; multiplicity and test choice change conclusions. | Recommended for a positive policy claim. Existing negative comparisons can be reported with their limitations. |
| Proposition 16 B closure certificate | Separate bounded search stopped after 676 seconds, with a retained checkpoint but no complete certificate. The B value is numerical. | Optional. Improve bounds/checkpointed search before another bounded attempt; the completed nonexactness and factor results do not require it. |
| Original W-corner BP certificate run | Stopped at the user's request; witnesses and queue were lost. Theorem 11(c) later proves its intended claim analytically. | No unchanged rerun recommended. Its partial log must not be promoted to a certificate. |
| Minor-set replacement inside SCIP | Only formula checks and external LP re-solves were done; the default and Ipopt guard complicate integration. | Optional for the geometry paper; recommended if claiming practical separator improvement. Negative-determinant principal minors and bound strengthening need separate scope. |
| Explicit-minor constraint in `nlhdlr_quadratic` | The claim that it produces `C_U` cuts for `x_1x_4 − x_2x_3 = 0` rests on source reading; no run tested it (minor OQ6). | Optional source-fidelity check before relying on that implementation claim. |
| Split policy in a branch-and-bound solver | Current gains are root-bound experiments, and the support-three extension also changes smaller supports/RHS choices. | Recommended for a practical separator paper, with an isolated support-three control and validation at original SDP points. |
| Larger dense hard-separation benchmarks | General searches can be capped and practical-threshold cuts differ from tiny exact violators. | Optional; unlikely to support an exact-separation performance claim without a clear practical target. |
| A 10,000-triangle chain and the killed `chain_m300_e0.3_s1` Gurobi solve | The first poses dense-memory costs; the second ended without a final status and its last incumbent was worse than the heuristic. | Optional; neither is needed for the reported family comparison. |
| More contact searches or random rays for completeness | Failed exact-contact searches and unclassified higher-dimensional contact strata remain. | Optional as exploration. A proof or an exact missing ray, rather than more negative sampling, is recommended for a completeness claim. |

Further literature work is also recommended before submission: obtain the
unread journal/monoidal intersection-cut computations and closest Porembski
texts; inspect the classic hypermetric, Boros–Hammer, Padberg, Dash and
Deza–Laurent sources directly; and verify the exact BNW/BKT dependencies
and overlapping nonrepresentability work. This is a publication condition,
not a claim that another search would itself prove novelty.

## Consolidated open questions

1. **Restricted quadratic-free families.** Determine the sharp asymptotic
   constant in the depth bound, exactness conditions beyond the established
   support-one interval and tangent criteria, and whether analogous depth
   guarantees hold for homogeneous minors. Settle Theorem C(3)'s boundary
   case for (A), and whether its lowered-interval test extends to (B);
   Proposition C2 rules out an angle-only criterion. Determine the depth
   constant's dependence on the relative-discriminant margin `μ` (ratio OQ2).
2. **Closures and rebasing.** Determine finiteness of
   `ρ_A = sup_w z_K/z_cl,A` and `ρ_B = sup_w z_K/z_cl,B` at the Theorem 14
   corner, exact values in the remaining support-one examples,
   and conditions for finite or convergent rebasing. Prove convergence or
   find counterexamples for natural policies when the uniform pointedness
   assumption fails; a uniform depth bound would suffice without it, and
   the adversarial sequence is not a counterexample for those natural rules.
   Is any natural bound-optimal rule provably failing? Can an A/B closure
   be exact in a support-one direction while no single cut is? Why do P/BP
   closures equal the best single cut in almost every tested direction?
   Is the orbit closure exact for minors (minor OQ4)?
3. **Useful solver choices.** Find a cheap criterion that predicts LP or
   tree progress when the local corner criterion is zero. Test whether
   validated ray scaling or a recession-aware/efficacy rule is useful enough
   to offset cut density and selection cost. Establish numerical validity
   and a robust corner oracle independently of performance measurement.
   Explain why most checkable cuts are never observed in an LP and whether
   the per-expression limit between restarts is intended (fidelity OQ4).
   Verify whether the full-space formulation improves the `ρ ≥ 4` brackets
   (fidelity OQ6), and whether `nlhdlr_quadratic` produces the expected `C_U`
   cuts for an explicit minor (minor OQ6). Test switching schedules inside
   SCIP (multiround OQ3), measure shorter steps for the unmeasured losing
   rules, and test causality with a better-powered `maj2` versus `rnd0.33`
   comparison and a tie-free bound-optimal choice (multiround OQ4).
   Can a cheap change to SCIP's `+1` constant remove its `κD` loss, and
   do grazing or conditioning bounds control Case 2 (ratio OQ3 and OQ6)?
4. **Separation complexity.** Settle general-gap separation on psd input,
   and approximation or constant-normalized-violation hardness under stronger
   conditioning/interiority restrictions. Is gap-0 separation strongly
   NP-hard? Keep the proved gap-0 distinction
   and fixed-support/rank/threshold algorithms separate from these questions.
5. **Practical split separation.** Control backward error under rationalization
   and rank truncation, and determine when a normalized general separator
   adds enough beyond cheap families at non-root nodes. Isolate the effect
   of ternary support from changed right-hand sides and smaller supports.
6. **Three-variable completeness.** Prove Conjecture 2.11 or exhibit an exact
   missing ray; determine whether the stronger computational Conjecture 1
   holds. Extend active-set/rounding analysis to strict supermodularity and
   unclassified contact strata. Decide exposedness of S1–S5.
7. **Finite SDP lifts on positive graphs and other domains.** Determine
   representability for `P_4`, `K_{1,3}`, the fan cone `COP(F_5)` and the
   remaining series-parallel graphs. Determine whether four-variable
   submodular quadratics admit a finite lift, and whether the obstruction
   extends to polytopes without simple vertices or cones outside the stated
   simple-ray hypotheses.
8. **Where triple-local cuts matter.** Identify natural root/node distributions
   with material triple gaps, compare selective blocks with equally selected
   exact lifts, and determine when coupled auxiliary moments improve beyond
   the local gain bound's scope. Find cheaper selection rules for `K`, `A`
   and `X`, and decide when triple-level separation is worth its cost
   (computation OQ4).
9. **Attainment and literature dependencies.** Characterize equality-case
   attainment beyond the existing sufficient conditions, and investigate
   the Eckstein–Nediak route to maximal sets attaining `z_K`
   (intersection-literature §15). Obtain any later KY version and verify
   Proposition 3.11 in full before relying on the corrected corollary.

## Publication recommendation

Use the program as a common technical report and artifact collection, not
one journal article covering every stream. The separation classes, local
intersection geometry and SDP representability questions have different
readers and proof machinery. The evidence supports three primary packages,
with a possible split of the third and a conditional computational paper.

1. **Binary separation complexity.** Build a focused paper from the starting
   integer result and the binary stream, centered on the binary Gram
   construction, polynomial encoding, positive-definite/triangle-feasible
   hardness and named-class consequences. The main audience is polyhedral
   combinatorics and discrete or mathematical optimization; a theory journal
   is a better fit than a solver-performance venue. This is the strongest
   plausible new complexity contribution: it addresses an explicitly open
   question in the inspected 2022 source. Before submission, polish the
   bit-complexity and membership proofs for publication (they are already
   given and reviewed), check the exact
   dictionaries and facet qualifications against original sources, include
   the repaired maximizer argument, and audit later literature with specialists.
   The practical split stream is useful motivation or a short appendix;
   its full benchmark narrative would distract from the theorem. “No later
   resolution found” is not a priority certificate.
2. **Limits and guarantees for quadratic intersection cuts.** Combine the
   corrected starting theory with ratio bounds, closures, bilinear/minor
   tangent obstructions and the relevant convergence results. The organizing
   question is how much a restricted family or a locally best cut can lose,
   and which geometric conditions give guarantees. Target continuous/nonconvex
   optimization and cutting-plane theory readers. Distinguish classical
   dominance and parametrization facts from the specific new obstructions,
   sharp-order bounds and closure statements. Formalize the hypotheses and
   support arguments, give the exact-certificate method and verifiers as an
   appendix/artifact, and obtain the closest unread sources. The two-sided
   and one-sided certificates must stay distinct. Multiround negative results
   can illustrate the local/global distinction, with causal claims and post
   hoc positive policies kept modest. Do not advertise a better SCIP solver.
3. **Three-positive quadratic hulls and the SDP boundary.** Combine the
   established family and counterexample with capped rounding/sign-class
   reductions, boundary rays and the dimension-four/K4 representability
   results. The audience is semidefinite and polynomial optimization. There
   are real proved contributions, but full family completeness is still a
   conjecture and nonrepresentability substantially uses known BKT machinery.
   Theorems 4.2 and 2.5 are short consequences of BKT and BNW, respectively,
   and may already be known to specialists. BNW is a recent preprint whose
   proof was read but not verified line by line here.
   Prepare self-contained transfer proofs, verify external BNW/BKT assumptions
   and real-closed-field steps, and compare closely with related cone
   nonrepresentability work. Present the triple computations as calibration
   and limited evidence, not completeness or a universal cost claim. If the
   representability proof and the constructive family make the manuscript too
   broad, separate a short obstruction paper from the family paper. The
   latter already has validity and separation results and need not wait for
   a completeness proof; proving completeness would materially strengthen it.

A **solver diagnostics or computational-method paper** is conditional. It
could join numerical fidelity, zero-cost criteria, ray-scaling rejection,
validated normalized split separation and selected family experiments only
if there is a clear method and a controlled evaluation. The current
negative/withdrawn results support a useful reproducibility report, but
not a strong claim of a faster general QP solver. Choose a computational
optimization or solver/software venue only after capture-free interleaved
stock comparisons, validity audits and quiet timing. If those experiments
remain negative, a focused diagnostic paper or public technical report is
more honest than forcing all streams into an algorithm paper.

The strongest evidence is the exact reductions, analytic bounds and retained
certificates. The weakest publication claims would be a new general idea of
“best S-free cut”, practical default-setting superiority, a proved complete
three-variable family, or uniform benchmark gains. The literature review
explicitly reduces the first claim; the experiments and open questions
exclude the others at present.

## Revision after critic review

The independent [critic review](CLOSEOUT-review.md) found five major local
errors and minor omissions. Each finding was checked against the cited
note passage before editing. All requested items are handled below; these
fixes have not been independently re-reviewed.

| Major item | Handling |
| --- | --- |
| 1. Three-variable solver relevance | Replaced the compact-exact-replacement claim with the actual block counts and Theorem 2.5's sign test, including the dual-aggregate caveat. |
| 2. Multiround Proposition 5 | States failure of uniform depth, not failure of a bound-optimal loop. |
| 3. Orbit Corollary 4 | States equivalence of exactness, not equality of bounds, in the summary and connections. |
| 4. Minor Proposition 11 | Cites §6: SCIP and BCM vanish; the point-rule and orbit families attain `z_K`. |
| 5. Orbit ratios | Defines `ρ = sup_w z_K/z_cl`, adds the factor-`N` single-cut bound, and corrects the local finiteness question. |

Minor summary and publication items:

- **Fidelity:** identifies the four `waterund32` records and dumped partner
  drift; distinguishes the `ρ ≤ 2`, `ρ = 3` and `ρ ≥ 4` methods; adds gap
  medians, zero-rate mechanism, failure rates and source-audit findings;
  records r1's minor-fixes verdict with major-rated M1.
- **Set selection:** describes the floored surrogate, full 305-instance
  scan and fully degenerate acceptance fallback; limits the angle grid to
  dimension two; records withdrawal of the instrumentation attribution
  and round 3's verified verdict.
- **Multiround:** corrects the withdrawn 40% attribution, root-orbit cost,
  AUC versus round-10 significance, convergence hypotheses and loop scope;
  states flat experimental cones and the unconfirmed, underpowered causal tests.
- **Minors:** changes “although” to the lower-SCIP comparison; adds the
  positive-determinant principal-minor result. Following the note, this is
  PSD for positive trace and NSD for negative trace; negative determinant
  was not studied experimentally.
- **Ratio bound:** separates the analytic lower constant from the
  computer-assisted 1.54 upper constant; uses relative discriminants;
  adds the sharp cylinder threshold and the actual three r1 issues.
- **Orbit closure:** adds the factor-`N` result, B's exact W-corner cut
  and BP's infinite Theorem 14 factor.
- **Literature:** includes the quadratic-sublevel/discrete-sequence
  distinction, bilinear containment equivalence, inapplicability of
  Proposition A to all 120 corners, conditional KY proof and unread proof
  steps, draft status, and Steffy Corollary 2's absence of a cone hypothesis.
- **Split practice:** accounts for the four intermediate-rank points;
  uses `w`, extends the 1/4 bound to all psd input, says ordinary
  NP-completeness, and distinguishes three uncertified capped searches
  from the two dense cap-sensitive cases.
- **Binary separation:** gives each maximum's family and point, identifies
  Letchford's (18) numbering, qualifies gap-0 hardness, corrects who found
  and applied the encoding fix, says to polish existing reviewed proofs,
  and names unread sources and the folklore caveat.
- **Three-variable computation:** corrects both review rounds and the
  author's sensitivity-premise correction; adds cactus cost, edge-sharing
  `ht` limits and the three unresolved sparse gaps with their gain terms.
- **Three-variable completeness:** uses the positive-loop hull name,
  pointed-cone scope and author S1-rerun attribution; adds the BKT/BNW
  novelty qualifications and BNW's recent, incompletely verified status
  to the publication recommendation.

Errata items 1 and 8 now qualify the literature comparison and drop the
untraced scouting §3.4 reference. Items 10/12 include the Summary's `0.028`
quote and retain its roughly correct 97% gap. Item 13 names unrechecked
oracle uses and separates fidelity's tentative claim from multiround's
firmer one. Item 14 adds 62/22 LP comparisons; item 15 adds completion-B
values, 9-of-12 comparison and first-round qualification; item 18 points
to §3. Item 19 adds the binary-structure Limits bullet and all three old
review-status locations; item 22 is a GKL citation caution. Item 25 adds
exploration §7 and `K_4`-minor wording; item 27 notes the already-positive
21,000-instance sample; item 28 cites family §5 only. New item 29 updates
the old reimplementation-only statement. Older files remain unedited.

The open-question list now includes gap-0 strong hardness; literature §15's
attainment and Eckstein–Nediak questions and the KY dependency;
fidelity OQ4/OQ6; multiround OQ3/OQ4 and natural-rule failure;
orbit OQ1/OQ2/OQ3; minor OQ4/OQ6; ratio OQ2/OQ3/OQ4/OQ6;
and computation OQ4. Minor OQ6 also has a work-not-run row.

The authorized note nits were applied: tracked fidelity dumps; multiround
13–34% ties and depth hypotheses; computation's conjecture caps and scoped
Clarabel tolerances; completeness's revision date and S1 attribution;
binary proof locations; minor r4 status and §10.4; ratio r2 date; and
selection's three status locations plus O1–O3. Both Clarabel values are
correct: `conic.py` and the strict log use 10⁻⁸ for main relaxations,
while `hullsep.py` uses 10⁻⁹ for depths. The note now distinguishes them
and the floating-point simplex calculation of family values.
`PROGRAM.md` now records selection's verified round 3.

## Process and verification record

Work began on 2026-10-01, continued through 2026-10-03 and the final stock
rerun/revision work, and closes on 2026-10-04. Account usage-limit
interruptions affected multiple author runs and some review attempts.
The stream notes distinguish retained logs from reconstructed history.
In particular, the first computation author stopped around 04:30 UTC on
October 2 with sections 4–8 unwritten; its background jobs completed by
08:47 EDT. Replacement authors checked existing outputs before using them.
The completeness interrupted draft was not preserved, so its historical
counts cannot be independently reconstructed. An interrupted binary fix
attempt made no edits, and an incomplete review attempt is not treated as
a completed verification. The completed reviews listed above are the basis
for the final status, together with the coordinating agent's specified checks.

The original orbit BP producer was stopped at the user's request. Its exit
was confirmed by 2026-10-02 18:39:50 UTC, after an earlier stop had missed
the separate background job. The retained log has 25,362 lines, including
430 accepted-triangle messages and 24,931 local-budget-exhaustion messages;
it has no completed certificate. These are messages, not verified coverage.
The process had local inner budgets but no useful overall runtime budget,
and no resumable checkpoint; termination lost witnesses and queue. Its
[stopped-job record](orbit-closure/CLOSEOUT.md) remains intact. The later
analytic theorem resolves the intended claim without resuming that run.
The separate bounded Proposition 16 B search retained a checkpoint and
remains optional and incomplete, not a completed certificate or an
unfinished obligation of this program.

Program files were included in repository commits made outside this program
(e.g. `d91d8d98b`, `f785387a8`, `b59ed1b83`); the program itself makes no
commits. This was checked with
`git log --oneline -- research-20261001 | head`. The closeout changes only
this record, `PROGRAM.md` and the authorized note headers/status and
cross-references, plus the note nits and optional selection r3 and minor
r4 remarks listed above. Review files,
code, logs, older research files and git state were left unchanged. Old
wording quoted as revision history was retained as history.

Only targeted checks were used; project-wide verification and CI status/logs
were not consulted. Historical solver and certificate commands are recorded
in each stream's “Checks actually run” section; they were not rerun for this
closing record. The final correction checks stated above are the coordinating
agent's reported checks, not new computations by the closeout author.
Verification reported by the original closeout author, before the critic review:

- `git log --oneline -- research-20261001 | head`: verified the named outside-program commits.
- `git diff --check -- research-20261001`: passed (exit 0).
- `git diff --no-index --check -- /dev/null research-20261001/CLOSEOUT.md`: no whitespace diagnostics; exit 1 reflects the new file differing from the empty input.
- Targeted `rg` audits: checked commit wording, final statuses, old result numbers and the numerical passages cited here. Revision-table quotations and references to results in other sources were distinguished from stale current claims.
- Inline Python document checks: all eleven final-status headers present; all local closeout targets and heading links valid. Session-start versus final text differences were inspected for every existing authorized file.
- Inline Python preservation check: all 11,455 protected program-file size/mtime records match the session-start digest; HEAD and the index digest are unchanged. Pre-existing modified and untracked files were preserved.

The closing record's quoted numbers were checked against their contextual
passages in the notes and final reviews, with an additional decimal-token
audit. Unresolved numerical premises and withdrawn timing claims remain
explicit. These document checks do not add research evidence or amount to
independent verification of the proofs.

Targeted checks run for this critic revision:

- Inline Python substitution of the ten saved corrections into the original
  120 LP records: 62 orbit improvements and 22 losses at threshold 0.01;
  no solver or certificate computation was run.
- Read-only `git ls-files` inventory and targeted `git log` check: 113
  tracked MINLPLib dumps, 2,202,572,656 bytes, included in `c3514f03e`.
- Targeted `rg`/`sed` reads and session-start text comparisons: checked
  every critic item, the allowed note edits and the distinct Clarabel settings.
  The final inline Python item/status checklist passed; its first run
  expected the separate literal `ratio OQ6`, and was corrected to match
  the combined `ratio OQ3 and OQ6` reference. No document change was needed
  for that assertion.
- Inline Python link checks: all 453 relative links and 13 Markdown
  fragments in `PROGRAM.md`, this record and the eleven current notes
  resolve. The broader scan of all 77 program Markdown files found 517
  relative-link occurrences, with 17 pre-existing failures in protected
  files: 16 in `three-var-computation/logs/note_first_draft_2026-10-02.md`,
  whose paths still assume the stream root, and a quoted citation to
  Proposition 5(b) in `intersection-literature/reviews/review-r1.md`,
  rendered as a link to `b`. Those files were not edited under the user's
  explicit no-log/no-review-edit rule.
- `git diff --check -- research-20261001`: passed. The separate
  `git diff --no-index --check -- /dev/null research-20261001/CLOSEOUT.md`
  check had no whitespace diagnostics.
- Inline Python SHA-256 preservation check: all 11,459 protected program
  files are unchanged from this revision's start; HEAD and the index digest
  are unchanged. No project-wide verification or CI status/log check was run.
