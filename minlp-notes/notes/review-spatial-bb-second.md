# Second independent review: spatial branch-and-bound lower bound

Date: 2026-09-05. Reviewed `results/spatial-bb-exponential-lower-bound.md`
after corrections from the first review. Verdict: **core results pass; two
minor scope/formulation corrections required and applied in this review.**

## Checked mathematical claims

- Lemma 1 is correct for every integer `1<=k<=n-1`. The slice is nonempty,
  and every vertex has exactly one fractional coordinate, equal to `1/2`.
- The chord formula, domination of every univariate convex underestimator,
  McCormick substitution, and minimal-alpha alphaBB identity are correct.
- Theorem 1's partition witnesses are distinct, feasible, and all covered by
  leaves. Endpoint restrictions `Z intersect A=empty` and
  `H intersect D=empty` are valid. The chord bound at a witness forces
  `|M intersect R|>m(1/2-2epsilon)`. Uniform-subset avoidance and the final
  union bound give the stated **minimum**, including the degenerate `z=0`
  case. No disjointness or tree structure is used.
- The specialization `n=3t`, `k=m=z=t`, and `epsilon=1/8` gives
  `(3/2)^(n/24)`. Exponential growth for any family with both `k` and `n-k`
  linear follows by choosing `m,z` each proportional to `n-k`.
- Proposition 2 is valid. All chords are nonnegative; the middle interval
  contributes the target exactly; the final corner boxes contribute at least
  `(1-alpha)/2`. The exact node count is `2^(n+2)-3`. Strict fathoming is
  handled by an arbitrarily small positive target margin.
- The fixed-`k` half-interval certificate is correct. Its exact leaf count is
  `C(n+1,k+1)` (Pascal recurrence with boundary counts one), hence the stated
  polynomial bound is valid, though not optimally expressed near `k=n-1`.
- Remark 3's corrected sufficient condition for the root SDP point is valid.
  In fact its McCormick condition fails exactly at `k=n-1`; the text safely
  makes a narrower sufficient claim. The covariance spectrum is correct.
- A relative-gap rule specifically of the form `LB >= (1-r)UB`, `0<=r<1`,
  implies the absolute threshold `LB>=1/4-r/4`; other denominator conventions
  need their own translation. Equality tolerance `delta` gives feasible
  objective at least `max(0,1/4-delta^2)` and the stated weakening is safe
  whenever its resulting target remains positive.

## Corrections

### 1. Objective tightening needs an augmented cover

The old Remark 2 said both feasibility-based and objective-based tightening
never remove points of `F`, and that the final leaves cover `F`. Objective
cutoffs can discard feasible points with high objective values. The cover
must include the discarded certified slabs as well as the final leaves.
Feasibility-based tightening alone preserves all points of `F`.

The numerical `(q+1)N` bound remains correct when there are at most `q`
certified slab deletions per processed node. It does not grant unrestricted
use of stronger relaxations or uncharged non-box deletions. The revised
wording states this explicitly. A closure issue for open slabs is avoided
by stating the result for discarded slabs whose **closed box** is certified
at the target. This is the precise sufficient hypothesis needed for the
cover proof.

### 2. Arbitrary convex underestimators may have unattained infima

A real convex function on a closed interval need not be lower semicontinuous
at its endpoints. For example `g(0)=0` and `g(x)=x-1` for `0<x<=1` is convex
and lies below `x(1-x)`, but its infimum is `-1` and is not attained.
Thus the definition of `LB_g` should use `inf`, or add a closedness
assumption on every `g_i`. Replacing `min` by `inf` keeps the intended class
as broad as possible and leaves every inequality in the proof unchanged.
The chord LP itself remains a minimum because its objective is continuous.

## Verification performed

Ran `python code/spatial_bb_lower_bound/check_lower_bound.py` successfully:
all vertex, envelope, explicit-tree and random witness checks passed;
246 pruned random boxes were encountered. The additional exact-rational
Remark 3 checks and Remark 7 leaf LP checks also passed.

The existing script has two `if __name__ == '__main__'` blocks; both run
under direct execution, so none of the appended checks are skipped. Its
opening summary still says the root SDP claim holds for `n>=2k`; this is a
stale comment, not a failing mathematical check. It is corrected here to
match the actual condition.

The proof is independent of these numerical checks. I did not find a
counterexample or missing hypothesis in the corrected theorem, its
matching exponential upper bound, or its fixed-`k` certificate.

## Follow-on finding

The original note leaves the behavior of SDP plus RLT under spatial
branching open. A stronger cover lower bound is now proved in
`notes/spatial-bb-strengthening-investigation.md`, with the same exponent in
the balanced family. Its key construction uses deterministic witness
coordinates on restricted intervals and exchangeable second moments on
coordinates whose interval is still `[0,1]`. This is a new candidate result
requiring its own independent audit and literature assessment.
