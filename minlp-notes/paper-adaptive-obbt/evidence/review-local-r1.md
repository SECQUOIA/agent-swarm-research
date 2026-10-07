# Independent review of the local-rate development

Status: the 1,097-line first draft of `sections/local-rates.tex` and the
400-line first draft of `appendices/local-proofs.tex` have been reviewed.
Awaiting the revisions before issuing the final manuscript verdict.

## Scope

This is a read-only mathematical review of the local contraction, stalling,
composite expansion, and boundary arguments. Only this evidence file is owned
by this reviewer. No manuscript text, archived evidence, experiment, solver
output, global verification, or CI state has been changed or regenerated.

The review has read `AGENTS.md`, `evidence/BRIEF.md`,
`evidence/INTEGRATION-NOTES.md`, `evidence/audit-rates.md`, the substantive
mathematical sections of September `theory.md`, the complete analytic parts of
`proofs-12-11.md`, and the corresponding proof discussion in
`review-theory.md`. The current foundations and preamble were read for the
assumptions and notation inherited by the local-rate section.

## Analytic checks completed before manuscript review

1. Independently derived the complete-graph cube support minimum
   `t^2+a(n-1)t-a n(n-1)/2` for `n>=3`. The bound on the sum of absolute
   values is valid for both signs of the sum of the other coordinates and is
   attained with those coordinates zero. The audit's root and exact stall
   threshold follow.
2. Checked the two-variable cube and rectangle support minimizations. The
   interior-box sandwich gives a two-sided geometric bound and a kth-root
   rate. It does not alone imply convergence of successive ratios.
3. Checked the composite recursion for lower and upper gaps, including signs
   of nonzero factor values, zero factors, median selection at a critical
   point, zero first-order intervals, and degenerate shapes. The simultaneous
   proof of the interval-violation estimate is essential for the univariate
   step. The finite Lipschitz bounds and finite factor sequence preserve
   uniformity through clipping. Under locally Lipschitz scalar second
   derivatives, the full objective also has a locally Lipschitz Hessian, so
   its Taylor remainder has the stated cubic order.
4. Checked the repaired boundary induction. Its start requires `N>1`; the
   terminal active estimate at `k=N>1` needs no upper cutoff restriction.
   At `N=1`, only the initial coarse estimate is justified. Bounds in the
   prescribed free enclosing scale do not give a recurrence for the actual
   free gauge.

## Nonsmooth-factor distinction to check in the draft

The local smoothness hypothesis concerns each scalar factor near its actual
argument value. Thus `abs` at a nonzero argument is covered by the smooth
theorem. At a zero argument it is not covered, but a first-order relaxation
error is not inevitable: the convex relaxation of the direct objective
`abs(x)` is exact.

A smooth final objective can nevertheless lose first-order exactness through
a nonsmooth factor at zero. On `[-t,t]`, represent
`f(x)=abs(x)-abs(x)+x^2=x^2` by composite rules with the convex square kept
exact. The first `abs` factor has convex relaxation `abs(x)` and concave
envelope `t`. Signed scaling and summation give
`phi_B(x)=x^2+abs(x)-t`, so the objective relaxation gap at zero is exactly
`t`. Clipping does not remove that error. Consequently smoothness of the final
objective alone cannot replace the scalar-factor hypothesis.

## Required corrections in the first main-section draft

Line references below refer to the 1,097-line draft read on this review pass;
labels identify the statements if later edits move the lines.

### 1. Boundary initialization must forbid negative active extents

`thm:boundary`, lines 940–943, does not explicitly require `d^0 in S` or
`B_0' subset B_0`. The proof requires the active lower endpoints to equal
`x_i*`; otherwise the active linear term need not be nonnegative, and the
active width is not the upper extent from `x_i*`.

For an explicit failure under a literal reading, take `f(x,y)=x+y^2` on
the original box `[0,1] x [-1,1]`, with the exact objective relaxation
defined on all boxes of `R^2`. The original minimizer is zero, `g_A=1`, and
the boundary model on `S` is `Q=xi_y^2`, so `G_M=0` and the free contraction
premises hold for `delta=1/4`, `lambda=3/4`. The proposed initial box
`B_0'=[-t_0,t_0]^2` satisfies the displayed initialization unless admissibility
is imposed. At cutoff zero its first active width is `t_0`, whereas the
claimed initial upper bound is `delta*t_0^2/4`.

**Repair:** state `d^0 in S` and `B_0' subset B_0`, with `0<t_0<=bar t`.
Alternatively explicitly require the active lower endpoints of the start
and every comparison box to equal `x_i*` and explain any larger allowed
domain.

### 2. Indefinite curvature requires restrictions on feasible directions

Lines 455–457 after `eq:quadratic-Q` say that indefinite `H` requires
constraints that are *inactive* near `x*`. This reverses the implication.
Inactive constraints leave a neighborhood feasible and cannot remove a
negative-curvature direction.

**Repair:** write that indefinite `H` requires constraints that exclude its
negative-curvature directions from the local feasible set. Retained affine
equations are one example.

### 3. The auxiliary-only reduction must specify the square relaxation

Lines 858–861 say that quadratic auxiliaries occurring only in the objective
give `eq:quadratic-Q` exactly. That is false for the endpoint-tangent square
auxiliaries of `ex:finite-square`, which also occur only in the objective.
Their projection is `sum_i(2h_i abs(x_i)-h_i^2)`, rather than the exact
diagonal squares in `eq:quadratic-Q`.

**Repair:** say that minimizing objective-only auxiliaries decouples the
terms, and yields `eq:quadratic-Q` when convex squares are kept exact and
distinct-variable bilinear terms use the stated envelopes. With finite square
tangents it instead yields `ex:finite-square`'s model.

### 4. The new row test needs its zero-diagonal case

Lines 592–593 define the explicit value of `c_kj` by
`-H_kj^2/(2H_jj)` when `abs(H_kj)<=H_jj`. With the permitted case
`H_jj=H_kj=0`, this is `0/0`. Degenerate rectangular scaling necessarily
creates this case.

**Repair:** use that quotient only when `H_jj>0` and
`abs(H_kj)<=H_jj`; use `H_jj/2-abs(H_kj)` otherwise. This gives zero when
both entries vanish and `-abs(H_kj)` when only the diagonal vanishes.
The variational definition at line 588 is already robust.

The rectangular clause of `prop:quadratic-rows`, lines 604–605, should state
the contraction test only for positive half-widths or remove fixed
coordinates first. Testing the strict inequality on an artificial coordinate
with zero half-width can never succeed: its scaled row is zero and the
right side is nonnegative. This does not falsify the sufficient implication,
but prevents the advertised test from certifying contraction of the remaining
coordinates.

### 5. The asymmetric eigenbox proof contains a false strict inequality

`prop:asymmetric-eigenboxes`, lines 524–525, asserts
`q(y)>q_2(y)>=0` for every `y` when the unique minimizer of `q_2` is not
usable by the full envelope. In the second-plane region `q=q_2`, so the
strict first inequality is false. The required conclusion remains correct.

**Repair:** at `t=rho*b`, `q_2(y)>0` except at its unique minimum. At that
minimum either the point is outside the box, or the other plane is strictly
larger and hence `q>q_2=0`. Thus `q>0` on the whole cross-section `x=rho*b`. Compactness
then makes the support strictly smaller than `rho*b`.

### 6. Face tests are sufficient tests, not a general dichotomy

`cor:face-test`, lines 383–384, says that `2n` programs decide between the
two cases. Zero face values or mixed signs can satisfy neither hypothesis.
Lines 396–399 also describe a round moving and retaining endpoints without
specifying the cutoff or whether the round is the tangent round.

**Repair:** say that the programs evaluate the two sufficient tests; they
may leave the question unresolved. In the mixed-sign paragraph, refer to the
zero-cutoff tangent round. For a finite relaxation with a nonzero remainder,
strictly positive/negative signs give the analogous conclusion on sufficiently
small boxes at zero cutoff. An arbitrary positive cutoff can retain the
positive-value face. In part (a), explicitly require `0<delta<min face value`.

The root's generic borderline example supplies a useful stronger explanation
that the strict contraction and strict stall hypotheses do not exhaust the
possibilities; its insertion is not needed for the validity of either theorem.

### 7. Boundary rates must remain upper enclosures

`thm:boundary`(c), lines 955–957, says that the free gauge decreases
geometrically with factor `lambda`. To avoid asserting the unsupported actual
one-round recurrence, replace this by the explicit result
`g_{u_F}((B_k)_F)<=t_k`, or by `free widths are O(lambda^k)`.
The current part (a) proves precisely this enclosure.

The first-order-condition description at lines 874–875 must be qualified as
the first-order conditions for a problem with only bounds. With other
constraints, general KKT conditions need not give `g_i=0` on the box-free
coordinates. The finite projected boundary expansion, including retained
constraints, remains a separate assumption.

The zero-gradient active-coordinate sentence at lines 970–973 also needs
the contraction condition on the enlarged one-sided free cone; merely moving
a coordinate into the free set does not establish it. Remove fixed
coordinates before defining this split, and state that the free boundary
theorem concerns nonempty `A` and `F`; the all-active case is treated
separately. At lines 974–975, quadratic convergence in the all-active case is
the zero-cutoff conclusion. At positive cutoff only the forced recurrence
and an `O(epsilon)` upper enclosure are proved.

### 8. Generic positive-cutoff floors have only upper bounds

Lines 1082–1083 call the generic fixed limit's width "of order
`sqrt(epsilon)`". The generic theorem proves `O(sqrt(epsilon))`, not a matching
lower bound. The extra feasible-neighborhood and local objective upper-growth
premises in `cor:tangent-rate` are what prove `Theta(sqrt(epsilon))`.
The boundary interpretation at lines 964–966 and the gap interpretation at
lines 1043–1047 should likewise describe upper bounds unless the extra
premises or the exact example are invoked.

The optional positive constant `M` in `cor:tangent-rate`, lines 284–285,
should be declared `M>0` before taking its reciprocal. `rho=0` in
`prop:tangent-eigenrate` should be separated as one-round collapse, rather
than writing a geometric `Theta(0^k)` rate.

### 9. Improving a cutoff can help outside a protected fixed box

Lines 362–364 and 1063–1064 say that improving the incumbent cannot help
under `thm:local-stall`. The theorem proves that the protected box cannot
be removed. It does not forbid useful tightening outside that box.

For an analytic counterexample, let `f(x)=x^2` and use the valid, monotone,
convex family `phi_[l,u](x)=x^2-(u-l)^2/2`. Its tangent model is
`Q(d,xi)=xi^2-(d^-+d^+)^2/2`. Every centered shape `v=(1,1)` has strictly
negative face values `-1`, so `thm:local-stall` applies at every scale.
On `B_0=[-1,10]`, however, cutoff `U=40` retains every point, whereas cutoff
zero reduces the upper endpoint to `sqrt(121/2)<10` in the first round.
The centered protected boxes still persist.

**Repair:** improving the incumbent cannot remove this fixed-box
obstruction or force singleton collapse; it may still tighten the enclosing
box outside it.

### 10. A single minimizer does not supply the local hypotheses

The final sentence, lines 1095–1097, says that at nodes containing a single
minimizer the local theory applies. The strong-convexity stall examples in
this same section have a unique minimizer even on arbitrarily small centered
boxes. A single minimizer removes the multiple-minimizer hull obstruction
but does not give a contraction shape or local entry.

**Repair:** say that the contraction conclusions can apply at such nodes
when the expansion, monotonicity, contraction, and local-entry premises have
been verified.

## Nonblocking manuscript improvements

The paragraph at lines 752–755 should give the concrete domain and regularity
premises for clipped monotonicity: every natural interval of a univariate
argument lies inside that scalar function's domain, and the scalar functions
are Lipschitz on the relevant intervals. Local `C^2` supplies these properties
on sufficiently small comparison boxes. Referencing "their assumptions"
alone leaves the reader unable to check when the example following
`thm:composite-expansion` establishes monotonicity.

The round-count paragraph at lines 1050–1056 should give an *upper bound*,
such as the ceiling of the displayed logarithm, for reaching the prescribed
enclosing scale. An upper contraction factor does not prove that roughly
that many rounds are needed. Exact rates on eigenboxes support equality-type
round-count statements separately.

The nonsmooth distinction above is absent from the first main-section draft.
A short insertion after `thm:composite-expansion` would read:

> The smoothness hypothesis is local in each scalar factor. For example,
> `abs` at a nonzero argument is covered, while at zero the theorem does not
> apply. A direct convex relaxation of `abs(x)` is exact. Conversely, smoothness
> of the final objective is insufficient: the representation
> `abs(x)-abs(x)+x^2=x^2` on `[-t,t]`, with the square kept exact, has composite
> lower relaxation `x^2+abs(x)-t`, including after clipping. Its relaxation
> gap at zero is `t`.

## Main-section developments independently accepted

The positive-cutoff result in `prop:two-variable-cutoff-floor`(c) is a useful
and sound completion beyond the audit's symmetric-start statement. A bounded
start containing the prescribed limiting cube is squeezed between that
protected cube and the iterates of a larger centered cube, so it has exactly
the same limit. The containing-cube premise is essential and is present.

The new sufficient row-contraction bound is sound once its explicit
zero-diagonal convention is repaired. The signed stall example attains this
lower bound on every face. The complete-graph proof by convex symmetrization
is also sound: for `s<0` the one-sided slopes are bounded above by
`(n-1)(2s-a(n-3))<0`, and for `s>0` they are positive. The support minimum is
therefore at `s=0`, giving the audit's exact root and threshold.

The two-variable rate remains stated as `Theta(rho^k)` on arbitrary interior
boxes, with exact multiplication on eigenboxes. The section explicitly
declines a successive-ratio convergence claim for arbitrary boxes. The repaired
boundary theorem excludes the refined active bound at `N=1` and gives the
correct analytic terminal-case counterexample.

## Appendix findings

### 11. Handle the empty lower-bound witness interval

At appendix lines 323–331, the proof of `lem:boundary-step`(iv) chooses the
largest `s` satisfying a condition that has no `s>=0` solution when
`epsilon+(G^F(d_F)-delta/2)t^2<0`. The theorem's displayed lower bound is
then negative and hence automatically true, but this case must be stated
before constructing a witness.

**Repair:** when that numerator is negative, the asserted bound follows
from the retained origin and the nonnegativity of the width. Otherwise
take the largest permitted `s`. Using a positive part in the lemma, as in
the audit, gives a cleaner automatic zero lower bound without changing
any later result.

### 12. Complete the unconditional sign-selection proof

`lem:sign-selection`, appendix lines 110–124, gives an unconditional
`C C' t^3` bound but proves only the case `s*=0` and the case of small
`t` with `s*!=0`. The statement is correct; its omitted case takes one
sentence.

**Repair:** if `s_t` and nonzero `s*` have the same sign, the selection
error is zero regardless of the size of `t`. If they have opposite signs,
`abs(s_t)<=abs(s_t-s*)<=C t`, so multiplying by the relaxation gap
`C' t^2` gives the asserted bound. At `s_t=0` the error is zero.

### 13. Match the boundary proof's notation and limiting qualifier

The proof of `thm:boundary` at appendix lines 349–350 uses `B_0` for the
initial box where the statement uses `B_0'`. Use the same symbol in the
proof and statement; the original domain remains `B_0`.

Main line 954 and appendix lines 381–382 write `eta_k->0` as `k->infinity`,
although the estimates stop at the finite `N` when the cutoff is positive.
Write `eta_k->0 whenever t_k->0`, including across local runs, or restrict
the `k->infinity` wording to `epsilon=0`. The established bounds
`sigma_1<=C t_0`, `sigma_k<=C t_{k-1}` for `2<=k<=N`, and the continuity
and remainder moduli prove the first version uniformly; no new assumption
is needed.

## Additional integration findings

The local section repeats the archived sequential factor near `0.705`
at lines 327–330. The foundations reviewer found, and a targeted read of
`code/review_checks/exp_gauss_seidel.py` independently confirms, that this
result comes from a variable-block update: both signed endpoints of one
variable are computed on the same relaxation, and the relaxation is rebuilt
before processing the next variable. The foundations define rebuilding after
each signed direction instead. Remove the numerical comparison or identify
its scheme and numerical scope explicitly. No experiment needs to be rerun.
The exact abstract comparison in `review-foundations-r1.md` supplies an
analytic replacement if wanted.

The construction before `thm:composite-expansion` gives the full lower
product rule but only says "its concave counterpart" at main line 744.
Since later factors use both inputs, explicitly defining the upper product
rule would make the theorem fully self-contained. With
`t_c(a)=max(c cv_a,c cc_a)`, that rule is
`cc_ab=min{t_{b^L}(a)+t_{a^U}(b)-a^U b^L,
t_{b^U}(a)+t_{a^L}(b)-a^L b^U}`. This is the rule proved by the appendix's
two crossed-product identities and used by its concave-gap recursion.

At main line 533, replace the rounded interval presented as an exact
inequality by `r/(1+r)<=c<=1/(1+r)`, followed by the approximate decimal
interval. The exact result is already proved in the preceding proposition.

## Appendix results independently accepted

All three induction properties in `thm:composite-expansion` are proved
together. The selected inputs used in a product are consistent at nonzero
factor values; zero values cost only cubic error. The natural-interval
dominance property puts the selected pair within `o(t^2)` of its rectangle.
The scalar-envelope comparison to the quadratic Taylor model avoids any
unstated fixed-curvature sign premise. The median rule at a nonzero scalar
derivative uses the proved dominance property, and a zero scalar derivative
removes the propagated quadratic term. These checks include every zero-width
and degenerate-shape case; no proof divides by an interval width.

The repaired boundary induction starts the small-active-shape regime only
for `N>=2`, obtains the terminal active estimate without the cutoff-size
restriction, and uses the coarse first-round estimate at `N=1`. Both limit
cases give the claimed constants. The proof evaluates only admissible
comparison boxes and uses the whole-family monotonicity for their transfer.
The main theorem must state the admissibility premise identified in finding 1.

No false second-order coefficient or hidden degeneracy exception was found
in the full composite proof. No new analytic flaw was found in the repaired
boundary induction beyond the statement and elementary proof omissions above.

## Current revision checklist

The main section is changing during integration. The following update refers
to the 1,221-line main file observed after the first correction batch, with
SHA-256 `bad865ea4d1b335bf79a040ba4acc8b91e84e97e7fbe2c53a68086501b9bd2e4`.
The appendix still has its first reviewed hash and 400 lines. These are
intermediate snapshots, not a final verdict.

The following findings have been corrected in the currently observed main
text: admissible boundary initialization; exclusion of negative-curvature
feasible directions; the specified square relaxation for objective-only
auxiliaries; zero diagonals and fixed coordinates in the row test; the
asymmetric strict-inequality argument; sufficient rather than exhaustive
face tests; the boundary upper enclosure rather than an actual gauge
recurrence; the box-only first-order condition; the one-sided cone's
contraction premise; zero-cutoff scope of all-active quadratic convergence;
generic upper floors; protected-box scope of incumbent improvements; the
single-minimizer node's missing hypotheses; `M>0`; `rho=0` collapse;
monotonicity domain/Lipschitz premises; and the nonsmooth cancellation example.
The critical `r*=1` example and centered rectangular map have also been
added and check analytically.

The remaining current items are:

| Location in current snapshot | Remaining action |
| --- | --- |
| Main, paragraph after `prop:tangent-eigenrate`, around lines 330–340 | Remove the `0.7053` directional-rate attribution unless a matching archived operator or an analytic proof is supplied. The source read by this review uses variable-block updates. |
| Main, `thm:boundary`(b), around line 1057; appendix 381–382 | Qualify `eta_k->0` by `t_k->0`, or restrict `k->infinity` to the zero-cutoff case. |
| Appendix, proof of `lem:boundary-step`(iv), lines 323–331 | Handle the negative numerator before choosing the largest permitted nonnegative witness coordinate. |
| Appendix, proof of `lem:sign-selection`, lines 119–124 | Add the nonzero coefficient/opposite-sign case needed for the unconditional cubic bound. |
| Main, product construction before `thm:composite-expansion`, around line 830 | Give the upper product rule explicitly for a fully specified construction. |
| Main, paragraph after `prop:asymmetric-eigenboxes`, around lines 613–614 | State the exact interval using `r/(1+r)` and `1/(1+r)`; label the decimals approximate. |
| Main, asymmetric eigenbox proof, around line 604 | The set `x=rho*b` is an interior slice of the box, rather than a box face. My first proposed repair used the wrong word here; use "slice" or "cross-section." The strict support argument is valid. |
| Main, boundary gauge counterexample, around lines 1072–1075 | Specify `0<t_0<1` and `h<1`, or write the general map as `h'=min(h,h^2)`; containment forbids the unqualified map `h'=h^2` for `h>1`. |
| Main, new round-count bound, around lines 1162–1170 | Require `epsilon>0` and use `max(0,ceil(log(t_0/sqrt(2epsilon/delta))/log(1/lambda)))`, or state the logarithmic bound only for starts above the threshold. The current bare ceiling can be negative when the start is already inside the threshold. |

Two small edge conventions also make the proofs literal: treat `g_u(B)=0`
directly as the retained singleton before dividing by a scale in
`thm:tangent-contraction`, and retain the `tau=0` convention when restating
the sharp-growth entry threshold in `cor:local-gap`. The theorem conclusions
in these cases are valid.

The nonsmooth paragraph correctly separates a factor kink from smoothness of
the final objective. An optional explicit sentence that `abs` at a nonzero
argument is locally linear would complete the requested contrast in one
line.

The root's exact scalar comparison between Jacobi and directional rounds is
preferable to the numerical attribution. Its matrix eigenvalue is an analytic
operator result and requires no new experiment.

## Verification record

Targeted commands used so far were `pwd`, `rg --files`, `rg -n`, `cat`, and
`sed -n` reads of the files identified above and the current manuscript file
list. All mathematical checks listed above were analytic. No numerical
experiment, solver loop, random-instance check, project-wide verification,
CI-status inspection, CI-log inspection, or literature search was run.

The main-section and appendix review used targeted numbered `sed -n` reads,
`rg -n` searches, and `sha256sum` of those two files. The first reviewed hashes
were `8681302ee89ee1049a82ed4091f6ccb80a18ed3b297c67da90e564e8671c0327`
for `sections/local-rates.tex` and
`6dde4c7e8c0ff5f2b750ac1474a6c046a0ac12ee5a4f43c4002f73662a6d5755`
for `appendices/local-proofs.tex`. A targeted read of the archived
`exp_gauss_seidel.py` confirmed the numerical comparison's update scheme;
its code was not executed. The final manuscript verdict will be added after
reading both files as revised.
