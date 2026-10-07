# Independent manuscript review: certificates, cutoffs, and residuals

Date: 2026-10-05. Reviewer scope: `sections/certificates.tex`,
`sections/cutoff.tex`, and `sections/residual.tex`. Only this review file is
owned by the reviewer. No manuscript, source report, or implementation was
edited. The first complete drafts of all three sections and the integrated
certificate revision have been reviewed. The findings below distinguish
revisions already present from corrections still needed in the reviewed
versions. The core results are sound; the important remaining scope and
integration issues are incumbent containment at a node and stale references
to the deleted duplicate limit theorem.

## Inputs and review standard

I read the repository `AGENTS.md`, `evidence/BRIEF.md`,
`evidence/audit-certificates.md`, `evidence/INTEGRATION-NOTES.md`, the October
study's `document/certificates.tex`, `document/foundations.tex`,
`document/frontier.tex`, and `theory/remaining-benefit.md`. I inspected the
reference model and row-checking interface in `theory/certificates.py` and
the relevant statements in the October `reviews/theory-review.md`.

The October review's warning against subtracting an upper residual is
superseded by the corrected proof in `audit-certificates.md`: if
`d <= r` and `r + M e <= e`, the exact tail after the first completed Jacobi
round is at most `M e <= e-r`. The subtraction is valid because of the
increment recurrence and the checked supersolution, not because an upper
bound can ordinarily be subtracted from another upper bound.

No literature search, numerical experiment, archived LP fixture,
project-wide verification, or CI inspection was performed.

## Certificate findings

1. **Resolved in the current draft: the current-round pool must be finite.**
   The initial `prop:current-round` required only a nonempty subset `W` but
   used minima and maxima over it. For example, `W=(0,1)` in `K=[0,1]`
   has neither endpoint extremum. The current statement explicitly says
   “nonempty finite subset”, which matches the intended finite-witness
   contract and fixes both the statement and proof.

2. **Resolved by integration: the projected objective range and the lifted
   polyhedron discussion disagreed.** The initial draft declared
   `phi_B:B -> R union {+infinity}`, then included a paragraph treating a
   lifted fiber with objective infimum `-infinity`. Within the declared
   range that case cannot occur. The simplest correction is to say that
   every nonempty relevant polyhedral fiber has a finite minimum, and
   omit the `-infinity` case. Alternatively, broaden the range explicitly
   and check all subsequent uses of `L`, witness thresholds, and differences
   of objective values. The compact lifted framework of the manuscript
   needs no such broader range. The integrated certificate section removes
   the duplicated setup and uses the foundations' compact lifted family,
   so the inconsistent `-infinity` passage no longer appears.

3. **Resolved: specify the objective in `ex:lambda`.** The initial example
   proved that its projection onto `(x,s)` is
   the nested square relaxation and that its auxiliary weights do not
   nest. To conclude monotonicity of `phi_B`, it must also specify a common
   objective on that projection, most naturally `v=s`. An objective
   involving the box-dependent weights need not have the claimed order.
   The integrated revision explicitly supplies objective `v=s`, explains
   that it depends only on `s`, and concludes the intended distinction.

4. **Resolved substantive correction: common fixed lifted rows preserve
   order under lifted nesting.** The initial cuts paragraph claimed that
   adding the same lifted row at every box preserves monotonicity. That
   does not follow from projected monotonicity. The current revision
   explicitly assumes lifted nesting, which is sufficient: intersection
   of nested lifted sets with the same halfspace preserves inclusion.

   The following exact counterexample explains the necessary distinction.
   Set

   ```text
   R(B) = {(x,t,s): x in B, 0<=t<=1, s=w(B)(1-t)},  v=t,
   f(x)=1,  exact original lift=(x,1,0).
   ```

   Before the new row, `phi_B=0` for every box, so the family is valid and
   projected-monotone. Add the globally valid fixed row `s<=1`; all exact
   original lifts satisfy it. The resulting value is
   `phi'_B=max(0,1-1/w(B))` for positive width. For `P=[0,1/2]` it is
   zero, while for `B=[0,2]` it is `1/2`. All face witnesses
   `(x,0,1/2)` on `P` satisfy the new row, but projected order fails on the
   larger box. Thus witness satisfaction alone does not repair the missing
   order premise. The final wording correctly excludes this construction.

5. **Resolved wording improvements, not proof defects.** In the initial
   certificate-cost discussion, “There is no general shortcut” stated an unsupported
   impossibility conclusion. The proved point is that checking a proposed
   box is cheap in arithmetic-operation count while finding a useful box
   can require endpoint solves and may fail for particular proposals.
   Also, “Only pools of original feasible points survive every valid
   reduction” should be phrased as a guarantee for original pools, not a
   converse classification. A changed relaxation can preserve additional
   pools; the manuscript proves that original feasible pools are always
   retained when the cutoff retains their original points. When merging
   certificates, “no larger ceilings, and often smaller ones” is more
   precise than strictly smaller ceilings in every direction. The
   integrated revision makes all three changes.

6. **Open finite-pool premise in `prop:round-check`.** This proposition
   declares `W` only as a subset of `K_U(B)` and concludes that it is a
   witness pool, whose definition requires a finite set. Require a finite
   subset here too. The actual pool of one endpoint solution per direction
   is finite. Without that premise an infinite `W=K_U(B)=[0,1]` in a
   constant-objective exact relaxation passes the stated hypotheses but
   is not a finite witness pool; choosing a finite face subpool repairs
   that conclusion.

## Certificate results checked and accepted

The current-round inequalities have the correct directions and concern
benefit rather than valid new bounds. The frozen-witness halving example
has the correct tangent violation and exact total displacement.

The `relaxation-sound step` definition and protection induction are sound
for exact Jacobi rounds, frozen selective endpoint updates, rebuilding
between sequential updates, and conservative inward updates. Protection
requires feasibility on the inner box itself. Projected order suffices
for box and objective-value ceilings; literal reuse of auxiliary
coordinates requires lifted nesting with the same objective.

The finite-completeness proposition is correct for a prescribed nonempty
compact fixed box. Coordinate supports give at most `2n` face points;
coincident faces can share a point. With rational polyhedral rows, rational
cutoff, and rational faces, each nonempty face polyhedron contains a
rational point. This is completeness of the supplied-certificate contract,
not completeness of floating proposal discovery or finite termination.

The join of two projected pools is protected on the coordinate hull of
their two boxes; lifted pools can be concatenated under lifted nesting.
The initial draft's `(L1),(L2)` limit proof is complete: compactness yields convergent
subsequences of face support points, fixed-box lower semicontinuity puts
their limits in every older cutoff set, and `(L2)` puts them in the limit
cutoff set. The reference-family proof of both premises handles infeasible
fibers and degenerate boxes. The complete sequential-round sandwich then
gives the same limit. The integrated certificate revision removes that
duplicate theorem and uses the foundations' `eq:closed-family` and
`prop:fixed-limit`, which give the needed limit conclusion and finite face
pool. An arbitrary fixed box need not contain the original sublevel hull;
their independent persistence gives `H_U subseteq B_infinity` and
`P subseteq B_infinity`, without implying `H_U subseteq P`.

Objective ceilings use a lower bound on this relaxation's current value,
not an arbitrary lower bound on the original optimum or a stronger native
relaxation. The three-variable stall correctly has original optimum zero,
all six protected faces at objective zero, and relaxed minimum `-3`.
The points also satisfy exact square epigraphs, so negative square lifts
are not the source of that gap.

The original-pool corollary, integral-face rounding condition, fractional
face counterexample, and child-box failure example are sound. On the new
child `[0,1] x [-1,1]^2`, its displayed face objective lower bound is
at least `1/2`, and the given lift at `(0,1,-1/2)` attains it.
The completed-round check can fail at a genuinely fixed output box because
the selected auxiliary coordinates fail rebuilding. A subsequent exact
round starting at the fixed box necessarily succeeds; this does not make
the arbitrary proposal routine complete.

## Cutoff findings

1. **Open empty-set correction in the interpretation of `prop:box-threshold`.**
   The theorem and proof correctly allow `K_U(P)` to be empty. The prose
   afterwards nevertheless says that `U<tau(P)` makes the next exact round
   move at least one endpoint strictly. If the cutoff is below `L(P)`, the
   round returns the empty set, whose endpoints are undefined. Replace that
   statement by: “the next exact round either detects an empty cutoff set
   or, if the cutoff set is nonempty, moves at least one endpoint strictly.”
   Compactness proves strictness only in the nonempty case.

2. **Open small empty-pool correction.** The frontier and response formulas
   use `min_j q_j` without explicitly requiring `k>=1`. The initial
   definition permits any finite set of lifted points. State that the pool
   for `prop:frontier` and `prop:cutoff-response` is nonempty; an empty
   cache supplies no witnesses. The reference frontier routine already
   returns an empty result for an empty cache, which is appropriate.

3. **Precision improvements.** Computing `tau_Z(P)` uses stored face
   membership and objective values, but still requires comparisons. Say
   “uses only the stored coordinates and objective values, without an
   optimization solve”, rather than “costs nothing beyond stored values”.
   The last row of the reuse table should not demand a new residual after
   every nominal change of region: a smaller region inside the region on
   which the same uniform bound was proved needs no new proof of that
   bound. The meaningful invalidation is leaving the verified invariant
   region or changing the map without a verified comparison. The cutoff
   perturbation result can also authorize transfer under stronger premises.

4. **Notation integration.** Using projected `W` and lifted `Z` is
   mathematically coherent and avoids conflating `max phi_P` with
   `max v_P`. The brief requests `W` for a finite pool. If the root applies
   that convention, `widehat W` for complete lifted points can retain the
   distinction without changing any formula.

## Cutoff results checked and accepted

The pool-face threshold is sharp, including equality at the threshold,
coincident faces, and redundant high-objective points. Convex mixing cannot
lower the threshold for protection of the same prescribed box: a convex
average on a face uses only points on that face. The full-relaxation face
threshold is exact under compact lifted attainment, with `+infinity` for
empty face fibers. Neither threshold characterizes existence of a different
protected box.

The mixing formula handles a cutoff-equality anchor (`theta=0`) and uses
one common convex relaxation and affine objective. Its rebuilding example
has the correct new secant violation. The coefficient-polytope proof of the
full frontier handles repeated points, equal values, strict straddling,
cutoff equality, and affine dependence without relying on image vertices
being vertices of the original pool's convex hull. Its quadratic candidate
count is valid. Filtering after a box change computes the exact frontier
of the filtered pool, not the old hull intersected with all new rows.

The new cutoff-response result is sound. Mixing optimal coefficient vectors
proves concavity of the pooled maximum. Between consecutive distinct pool
values the eligible originals and straddling pairs are fixed, so the same
function is the maximum of finitely many affine functions and is convex
there; hence it is affine there. The endpoint continuity proof bounds the
mass on more expensive points using the positive gap to the next pool value.
Negating the coordinate proves the minimum counterpart. Continuity and
monotonicity give a closed screening-cutoff interval when it is nonempty.

The worked three-point response and its cutoff `5/2` at tolerance `1/4`
are exact. The continuing-versus-restarting proof also checks out: order
gives the outer inclusion, and the new-cutoff greatest fixed box is retained
by the old relaxation-sound steps, giving the inner inclusion and equal
limits under `(L1),(L2)`.

## Residual findings

1. **Open important domain qualification: an incumbent must lie in the
   current box to supply the stated interval.** The invariant-interval
   lemma correctly assumes `p_P<=p_0`. The prose following it says that an
   incumbent singleton supplies the region whenever an incumbent defines
   the cutoff, and the cutoff-decrease subsection repeats that assertion.
   At a branch-and-bound node, a global incumbent can lie outside the node
   box. The interval then has reversed components or consists of no valid
   containing boxes, and the lemma cannot apply. Add `hat x in B(p_0)` in
   the first passage and “if it lies in the current box” in the second.
   If it lies outside, the residual corollary remains valid when another
   invariant region is independently supplied; the incumbent alone does
   not produce one.

2. **Open arithmetic-premise correction.** The least-majorant proposition
   is stated for real nonnegative `M` and `r`, correctly. The prose then
   says the least majorant is computed exactly by a rational linear solve
   whenever `rho(M)<1`. Add “when `M` and `bar d` are rational”. Spectral
   contraction ensures invertibility, but does not make irrational input
   rational.

3. **Open small family-domain correction in `ex:inactive`.** The example
   defines its projected family only on boxes containing zero, whereas the
   common framework requires all subboxes of the root box. Define the same
   indicator `phi_[ell,u](x)=0` iff `x<=u/2` on every subbox of `[-1,1]`.
   It remains valid for `X={0}`, projected-monotone because `u/2` is
   nondecreasing in `u`, and lower semicontinuous. Then state the formula
   `K_0([ell,u])=[ell,u/2]` only for `ell<=0<=u`. The matrix example and
   its invariant region are unchanged.

4. **Open boundary-index correction in `prop:history`.** The theorem
   permits `N=1`, but its expanded interpolation list includes
   `(s_(N-2),s_(N-1))`, which then has an undefined negative index. State
   the construction without an expanded list: both graphs contain
   `(s_k,s_(k+1))` for `0<=k<N`; add `(0,0)` and `(s_N,s_N)` for `G_1`,
   and `(0,0)` and `(s_N,s_N/2)` for `G_2`. This is the same construction
   and makes the `N=1` case explicit.

5. **Open useful proof completion in `ex:heron`.** The displayed support
   calculation is complete, but the claims of convergence to `r` and
   quadratic convergence should include their immediate error identity:

   ```text
   G(u)-r = (u-r)^2/(2u),  u>=r>0.
   ```

   Thus nonnegative errors decrease to zero (unless already zero), and
   their ratio to the preceding squared error tends to `1/(2r)`. This
   proves both claims, including the terminal case `u_0=r`, and requires
   no external reference or experiment.

6. **Precision improvements.** The history subsection says that neither
   an upper residual nor a comparison matrix can be inferred from history.
   An exact observed Jacobi displacement is itself valid residual
   information, as the preceding subsection correctly states. Restrict the
   impossibility claim to a uniform comparison bound or a nontrivial tail
   obtained solely from a finite strictly decreasing trajectory. Likewise,
   an old residual certificate does not *automatically* transfer after a
   cutoff decrease; the fixed-point comparison below can supply additional
   information under its separate hypotheses. The fixed-point comparison
   imposes a spectral condition, but the paper need not claim that every
   possible restricted comparison necessarily requires global spectral
   contraction.

## Residual results checked and accepted

The new ordered-pair hypothesis is sufficient and weaker than the previous
two-sided estimate. Consecutive iterates are ordered, so it gives
`Delta_(k+1)<=M Delta_k`; nonnegativity propagates the upper residual.
The finite supersolution bounds every partial matrix series, bounds the
decreasing trajectory below, and gives `p_m-p_infinity<=M^m e`. No convexity
or spectral-radius premise is needed for this trajectory estimate. If the
limit belongs to the region, ordered comparison and order preservation
prove that it is fixed. Closedness is a sufficient way to ensure that
membership. Empty cutoff sets are correctly excluded by the definition of
an invariant region on which `F` is defined.

The corrected after-first-round arithmetic is fully justified for an upper
residual: `p_1-p_infinity<=Me<=e-bar d`. It applies to the exact Jacobi
state `p_1`, including when `bar d` came from witnesses before any support
solve. It need not apply to an unprocessed or partly updated current box.
The source's original restriction against this subtraction was erroneous.

The least-majorant proof covers zero residual, singular `I-M`, and
noncontracting inactive directions. Nonnegative bounded partial sums
converge componentwise in finite dimension; passing through the finite
matrix gives `s=r+Ms`, and each supersolution bounds `s`. The inverse
formula is confined to `rho(M)<1`. The weighted-norm certificate uses
`w>0` and `0<=q<1`, so no coordinate is divided by zero and the explicit
majorant has the correct factor `1/(1-q)`.

An exact complete sequential round supplies an upper bound on the Jacobi
residual, because its output box is contained in the Jacobi output. That
does not identify its state with the exact first Jacobi state for the
after-round formula. Selective, interrupted, and conservative numeric
movements need not be upper residuals. With `(L1),(L2)`, the complete
sequential sandwich nevertheless transfers the Jacobi tail ceiling after
the same number of rounds by comparing their common limit.

The square example has the correct endpoint map, feasible support lift,
invariant interval, derivative bound, residual `3/4`, total majorant `6/5`,
after-round majorant `9/20`, and exact remaining motion `1/4`. Its first
three upper endpoints are correctly `5/4`, `41/40`, and `3281/3280`.

The cutoff-decrease corollary correctly requires a region invariant for
the **new** map, a uniform comparison for that map, and an upper residual
for that map at the actual current box. It does not infer these premises
from an incumbent value alone.

The new fixed-point shift proposition is sound and usefully weakens the
old uniform-cutoff premise. It compares existing ordered fixed points
`p_V<=p_U`; `F_V` is defined at both points and has the ordered-pair
estimate on their region; the cutoff estimate is needed only at `p_U`.
Substitution gives `x<=Mx+h(U-V)`, and `rho(M)<1` makes the remainder
`M^N x` vanish. Neither common invariance nor a whole cutoff interval is
needed for this comparison of existing points, and it makes no fixed-point
existence claim. The inactive-direction example correctly shows why a
finite trajectory supersolution cannot replace the spectral premise in
that general fixed-point comparison.

Apart from the expanded-index issue, the finite-history construction is
complete and satisfies the whole projected framework. Continuity and
monotonicity of its scalar map give `(L1),(L2)` even on boxes whose cutoff
sets are empty. The two maps share every prescribed positive strictly
decreasing finite history but have tails zero and `s_N`, respectively.
Its conclusion is confined to those histories and the stated broad
family; an exact no-movement round still certifies a fixed point, and the
construction makes no claim about McCormick-specific impossibility.

## Integration findings after the certificate revision

The certificate author has removed the duplicate `thm:limit-protected`
and its local `(L1),(L2)` conditions in favor of the foundations'
`eq:closed-family`, `prop:fixed-limit`, and `lem:sequential`. Those are
appropriate shared statements, but the cutoff and residual sections still
contain references to the deleted theorem and the now undefined condition
names. Replace them with the shared foundations results; in the history
theorem, verify the shared closedness condition directly by continuity of
its scalar `G` (if `u_k` decreases to `u` and `x_k<=G(u_k)` tends to `x`,
then `x<=G(u)`).

There is one scope detail to retain when making that replacement.
`prop:continue` currently permits any new cutoff for which every cutoff
set along the root trajectory is nonempty. The foundations'
`prop:fixed-limit` is stated under `U>=f*`. Its proof of a greatest fixed
limit also works with the more general nonempty-trajectory premise, without
an original feasible point. State that extension explicitly if retaining
`prop:continue` at the broader cutoff scope. The nested nonempty compact
boxes have a nonempty intersection, and their attained face supports pass
to the limit through `eq:closed-family`; the same persistence proof then
gives the greatest fixed box. No new analytic difficulty is involved.

## Verification actually run

One targeted command was run from the repository root:
`python3 -B -`, with an in-memory exact rational script. It imported only
the existing `Box`, `Model`, and `Row` classes and called their finite row
checks. It did not call an LP solver or change implementation files.

The script checked the child example's complete lifted point, its exact
objective `1/2`, the parent's zero-objective face witness, and the latter
witness's failure on the child. It also checked the rational objective
values and exact-original-lift validity in the common-row counterexample.

Output:

```text
PASS: new child example exact lifted rows; common-row projected-order counterexample
```

A second targeted `python3 -B -` in-memory rational command checked the
new three-point cutoff-response example at cutoffs `0`, `1/2`, `1`, `2`,
`5/2`, `3`, and `4`; its four stated candidates at cutoff `2`; and its
screening threshold at tolerance `1/4`. It also confirmed that the existing
routine returns an empty frontier for an empty pool. No LP was solved.

Output:

```text
PASS: new cutoff-response example and screening threshold in exact rational arithmetic
```

A third targeted `python3 -B -` in-memory rational command checked
majorants with `M=diag(1,1/2)` and `M=diag(2,1/2)` and residual `(0,1/2)`;
the identity matrix with zero residual and zero majorant; a strict upper
residual in the scalar halving example and its exact-state limitation;
the three Heron values and error identity; and the corrected history
interpolation construction for `N=1` and `N=3`. It imported only the
finite `check_tail_majorant` routine and performed no optimization solve.

Output:

```text
PASS: singular and zero-residual majorants; strict upper-residual state; Heron values; N=1 and N=3 history construction
```

These are mathematical row and contract checks, not performance evidence
or CI results.

## Addendum: the introduction's link between rates and certificates

I independently reviewed the paragraph beginning “The rate theory and the
certificates” in `sections/introduction.tex` (initial lines 106–120).
The root's three concerns are correct.

- Positive width is not required for a finite certificate. For a concrete
  zero-slack example, take `f(x)=x^2`, `B_0=[-1,1]`, and the exact compact
  convex lift `R(B)={(x,s):x in B, x^2<=s<=1}` with affine objective `v=s`.
  At cutoff zero one Jacobi round returns `{0}`, and the single witness
  `(0,0)` certifies that singleton. It attains both coincident faces.
- A protected inner box and a certificate of no further motion serve
  different purposes. If `P` is the current box, the pool proves an exact
  stall. If `P` is strictly inside the current box, it gives ceilings on
  future motion, which can justify stopping for a specified tolerance.
  Singleton pools can do either. In the existing halving example, the
  singleton `{0}` supplies the exact total-motion ceilings even though
  no finite number of outer Jacobi rounds reaches it. Thus zero cutoff
  slack does not make finite pools inapplicable, nor does it make residual
  certificates the sole route to a stopping bound.
- A local width estimate does not by itself establish that the limit is
  fixed. For the general family, the introduction should invoke
  `eq:closed-family` when it claims that the limit admits a face pool.
  This property is verified for the reference McCormick family. In the
  special zero-slack contracting case the limit is the original minimizer
  singleton, which is fixed directly by validity; the broader
  positive-slack fixed-limit claim needs the stated closedness premise.

Replace the paragraph by the following text (labels match the integrated
certificate section):

```tex
The rate theory and the certificates answer different questions. The local
rate theory describes contraction and the scale of the limit using minimizer
and tangent data that are generally unavailable during search. A finite
pool covering all faces of a box and feasible on its rebuilt relaxation
certifies that box, including a singleton. If it is the current box, the
witnesses prove an exact stall; if it is an inner box,
they bound all later endpoint motion and can support stopping at a prescribed
tolerance. Under the decreasing-family closedness condition
\eqref{eq:closed-family}, the limit is fixed and admits at most $2n$
witnesses. In the local contracting regime its width is
$O(\sqrt\epsilon)$; at $\epsilon=0$ the limit is $\{x^*\}$, which may be
reached in finitely many rounds or approached only asymptotically. A
singleton certificate remains valid in either case. A verified residual
estimate provides another bound on remaining motion. In the contracting
regime, the dependence of the limiting width and relaxation gap on the cutoff motivates reconsidering
OBBT after an incumbent improvement, while the certificate's cutoff
threshold states exactly when its stored witnesses cease to cover the
protected faces.
```

The final sentence uses the sharp retained-pool face threshold. It does
not imply that a different protected box is unavailable after that
threshold is crossed. No new computation, literature search, or manuscript
edit was performed for this addendum.
