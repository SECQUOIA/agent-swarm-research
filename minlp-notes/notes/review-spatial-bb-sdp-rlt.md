# Independent review of the SDP–RLT spatial branch-and-bound lower bound

Date: 2026-09-05. Reviewer: independent `spatial_sdp_review` agent.
Reviewed: `notes/spatial-bb-strengthening-investigation.md`, together with
`results/spatial-bb-exponential-lower-bound.md`.

**Verdict: the candidate lower-bound theorem is mathematically correct, with
the explicit convention that every node box is contained in `[0,1]^n`.**
The affine-product closure claim also holds. The counting statement for
objective-based bound tightening needs the augmented cover stated in the
candidate; final leaves alone do not generally cover the original feasible
set. This review establishes correctness within the stated relaxation and
branching model, not novelty.

## Independent checks of the construction

Write `r=|R|`, `s=|U|`, and let `H_U,M_U,Z_U` denote the cardinalities of
the witness classes in `U`. The hypothesis `r<min(k,z)` gives
`H_U>=1` and `Z_U>=1`. Hence

```
1 <= t=H_U+p M_U <= H_U+M_U <= s-1.
```

In particular the denominator `s(s-1)` is nonzero. This is the substantive
reason that the restriction on `|R|` suffices: after arbitrary restricted
coordinates have been fixed to their witness values, the remaining fractional
cardinality stays away from both endpoints.

For the unrestricted block,

```
c=t/s,
d=t(t-1)/(s(s-1)),
c-d=t(s-t)/(s(s-1)),
d-c^2=-(c-d)/s.
```

Thus its covariance is exactly

```
(c-d) (I - J/s),
```

a nonnegative multiple of an orthogonal projection. The deterministic
restricted rows have zero covariance. By the Schur complement of the
constant entry `1`, the whole augmented moment matrix is positive
semidefinite. This argument includes the endpoint cases `t=1` and `t=s-1`.

The four off-diagonal unrestricted RLT expressions are

```
d,
c-d,
c-d,
(s-t)(s-t-1)/(s(s-1)).
```

Their signs follow from `1<=t<=s-1`. For a repeated coordinate the products
have expectations `c`, `0`, and `1-c`; including repeated indices therefore
introduces no omitted condition. If either coordinate is restricted, its
bound slack is deterministic, including when its interval is degenerate.
The corresponding lifted product equals that deterministic nonnegative
slack times the other slack's nonnegative first moment. This verifies all
box RLT products, not merely off-diagonal McCormick inequalities.

For an unrestricted row,

```
c+(s-1)d = t c,
sum_j X_ij = t c + c sum_{j in R} w_j = K c.
```

For a restricted row, the equality follows from `X_ij=w_i x_j` and
`sum_j x_j=K`. Therefore the equality products really hold on every row.
The unrestricted diagonal has `X_ii=x_i`; the objective is precisely
`|M intersect R|p(1-p)`, as claimed.

These are direct algebraic verifications independent of the author's
numerical checks. The companion script
`code/spatial_bb_lower_bound/check_sdp_rlt_strengthening.py` was also inspected:
its four rational RLT expressions agree with these formulas, and it includes
degenerate restricted intervals. Its numerical PSD check is supplementary;
the projection formula above supplies exact PSD certification.

## Counting and pruning

Put `h=m(1/2-2epsilon)` and `q=min(k,z,h)`. For `r<q`,

```
SDP(B) <= |M intersect R|p(1-p)
       <= r p(1-p)
       < h/(2m)
        = 1/4-epsilon.
```

All inequalities remain valid for `m=1`. Consequently a pruned box
containing a witness has `r>=q`, and either `|A|>=q/2` or `|D|>=q/2`.
There is no rounding issue: `r,|A|,|D|` are integers while these comparisons
are valid real inequalities.

A fixed box containing a witness excludes every zero witness coordinate
from `A` and every unit witness coordinate from `D`. The marginal
hypergeometric avoidance estimates do not require independence of those two
events. Taking the smaller of the two marginal upper bounds is valid.
Since at least one exponent is at least `q/2`, taking the larger of the two
bases raised to `q/2` gives a uniform upper bound on witness coverage. Its
reciprocal is the **minimum**, as stated, of the two exponential expressions.
The union bound proves the cover result without any disjointness assumption.

For `n=3t`, `k=m=z=t`, one has `q=h<t`, so the advertised exponent
`t(1/4-epsilon)` follows. The chord upper-bound certificate remains valid
because the diagonal mixed RLT inequality implies

```
X_ii <= (a_i+b_i)x_i-a_i b_i,
x_i-X_ii >= a_i b_i+(1-a_i-b_i)x_i.
```

Thus the SDP–RLT bound dominates the original chord LP bound.

## Products of all valid affine inequalities

This closure statement is correct on every nonempty `P=B intersect F`.
Affine Farkas duality gives, for every affine function `ell` nonnegative on
`P`, a representation

```
ell(x) = alpha_0
       + sum_i alpha_i (x_i-a_i)
       + sum_i beta_i (b_i-x_i)
       + lambda (sum_i x_i-K),
```

where `alpha_0,alpha_i,beta_i>=0` and `lambda` is unrestricted. The
nonnegative constant is necessary in this formulation. Degenerate boxes
are allowed; no strict-feasibility assumption is needed for the linear
programming duality assertion.

Let `L` be the degree-two linear functional defined by `L(1)=1`,
`L(x_i)=x_i`, and `L(x_i x_j)=X_ij`, and let `e=sum_i x_i-K`. Existing
constraints give

```
L(e)=0,
L(e x_i)=0 for every i,
therefore L(e v)=0 for every affine v.
```

Expand the product of two such Farkas representations. Terms involving
`e` vanish, including `L(e^2)`. Every remaining term is a nonnegative
coefficient times `1`, a box slack expectation, or a pair of box slack
expectations represented by an existing RLT inequality. Hence
`L(ell_1 ell_2)>=0`. Arbitrary valid affine inequalities and their pairwise
products cannot strengthen the relaxation. This does not establish closure
under arbitrary valid quadratic inequalities or objective-cutoff-dependent
affine inequalities.

## Precise bound-tightening scope

Feasibility-based coordinate tightening preserves every point of `F` in a
node, so it does not affect the witness cover proof.

For objective-based coordinate tightening, an augmented cover must also
include removed portions containing feasible points. The candidate's
assumption that those portions are certified above the target is sufficient.
For usual relaxation-based bound tightening with cutoff `T=1/4-epsilon`,
there is a useful boundary detail: a removed slab is open in its tightened
coordinate, while theorem boxes are closed. The following argument justifies
passing to its closure whenever the removed slab contains a true feasible
point.

Suppose a parent relaxation certifies that no point with objective `<T`
has `x_i<theta`, and let `S` be the closed parent slab `x_i<=theta`. Suppose
also that the open slab contains a true feasible point `v`. If the nodewise
SDP–RLT relaxation on `S` had a feasible point `y` of objective `<T`, then
`y` is feasible for the parent relaxation, because tightening a box only
strengthens its box RLT constraints. The exact lift of `v` is parent-feasible
and has `v_i<theta`. A sufficiently small positive mixture of that lift with
`y` would remain parent-feasible, have objective `<T`, and have coordinate
strictly below `theta`, contradicting the certificate. Thus `S` is pruned.
If the open slab contains no point of `F`, it needs no covering box.

Box-monotonicity used here follows directly by writing each parent bound
slack as its child bound slack plus a nonnegative constant and expanding
its products. PSD and equality products are unchanged. The same reasoning
applies to upper-bound reductions.

With at most `r` certified slab deletions per processed node and `N`
processed nodes, there are at most `rN` covering slabs and at most `N`
terminal boxes, giving `(r+1)N` cover members. This count does not establish
an exponential processed-node bound if one permits exponentially many
uncharged bound reductions at a node. Nor does it cover arbitrary nonlinear
feasible-region deductions from the objective cutoff.

## Required clarification and significance

The candidate should say explicitly `0<=a_i<=b_i<=1`. This makes its claim
that an unrestricted interval equals `[0,1]` exact. The author was notified.
The original separable note's statement that final leaves still cover `F`
after objective-based tightening should be corrected; the author was also
notified.

The extension is substantive within its stated model: a nonseparable
second-moment relaxation, equality coupling, and all affine-product cuts
still cannot overcome the witness-cover obstruction under arbitrary real
coordinate splits at fixed objective tolerance. The proof itself is an
elementary combination of the existing cover argument and exchangeable
fractional-cardinality moments. Whether that combination is novel or
publishable requires the separate comparison with prior SDP branch-and-bound
and knapsack proof-complexity results. This review makes no priority claim.
