# Adversarial review of min-marginal grid pruning

Date: 2026-10-02. Scope: mathematical and bit-complexity review of the proposed
pruned shared-grid algorithm. No external literature search was performed.
This review does not establish originality.

## Verdict

The proposed pruning step is sound and removes the accuracy-dependent power
in the coordinate-state count. I found no mathematical obstruction to the
resulting fixed-parameter bound in bag size and the upper-curvature/growth
ratio. Three details are necessary:

1. Keep a monotone feasible incumbent and a record of the pruning steps.
2. Abort an unknown-conditioning trial before a coordinate grid exceeds a
   computable state cap. Without this cap, unsuccessful trials can retain the
   old accuracy-dependent power.
3. Include an additive unit length when localizing retained integer intervals.
   Ignoring unit intervals in the correction does not make their geometric
   length vanish.

The argument uses the assumptions and notation of
[the shared-grid theorem](../geometric-dp/theorem.md). In particular, the
domain is a product of continuous or integer intervals, a valid global upper
coordinate-curvature bound `L>0` is known, and

```
F(x)-f* >= g ||x-x*||^2
```

holds on the actual mixed domain. Let `kappa=max(1,L/g)`. The proofs below
allow continuous and integer coordinates together. They do not extend the
method to arbitrary coupled constraints.

## 1. Conditional lower bounds and safe deletion

At a stage, let `B` be the current mixed box, containing every original
global optimizer. Build the usual shared coordinate grids and corrections,
and write

```
G(y) = F(y)-D(y),
M_i(v) = min { G(y) : y_i=v, y lies on the product grid }.
```

For an adjacent coordinate interval `I=[a,b]`, the number

```
lambda_i(I) = min(M_i(a),M_i(b))
```

is a lower bound for `F(x)` over all feasible `x` in `B` with `x_i in I`.
Indeed, independently round all coordinates to their adjacent grid endpoints
with mean equal to `x`. Coordinate `i` then takes only the values `a,b`.
The existing rounding lemma gives `E G(Y)<=F(x)`, while every rounded point
has `G(Y)>=lambda_i(I)`. At a grid endpoint, keep that coordinate fixed.
For integer unit intervals, no feasible point is strictly between the
endpoints, which is exactly why their correction may be zero.

Let `U` be the best feasible value obtained so far, updated by taking a
minimum. Delete an interval only if `lambda_i(I)>U`. Taking, in each
coordinate, the hull of all surviving intervals preserves all global
optimizers. Taking a hull may reintroduce intervals that individually passed
the deletion test; that only weakens pruning. Endpoints remain feasible, and
integer-coordinate endpoints remain integers.

A corrected-grid minimizer `y` is a valid next center even if `F(y)>U`.
Every adjacent interval containing `y_i` survives, since

```
M_i(y_i)=G(y)=LB<=f*<=U.
```

Thus `y` belongs to the next retained box. Any already fixed coordinate can
simply remain fixed.

## 2. Localization of every surviving interval

Use `0<theta<=1/4` and `theta^2<=1/(8 kappa)`. Let the current scale be `h`,
the incoming center be `z`, and the corrected-grid minimizer be `y`. The
existing contraction theorem applies unchanged to the current restricted
box: it still contains `x*`, and the same global curvature and growth bounds
hold there. With its constant `B0=max(1,4L/(11g))<=kappa`, it gives

```
||z-x*||^2 <= 4 kappa n h^2,
||y-x*||^2 <= kappa n h^2.
```

The first inequality also holds at stage zero because the initial scale is
the maximum original side length. Using the mesh estimate directly gives

```
D(y) <= (L/4)[1+10 theta^2 kappa] n h^2
     <= (9L/16) n h^2.
```

Therefore `U-f*<=9Ln h^2/16`. If an interval survives, one of its endpoints
`v` satisfies `M_i(v)<=U`. A minimizing grid assignment `w` for that
min-marginal exists and satisfies `G(w)<=U`. Hence

```
g ||w-x*||^2 <= D(w)+U-f*.
D(w) <= Ln h^2/4
        +(L theta^2/2)(||w-x*||^2+||z-x*||^2).
```

Combining these inequalities yields

```
(g-L theta^2/2)||w-x*||^2 <= (17L/16)n h^2,
||w-x*||^2 <= (17L/(15g))n h^2
            <= (17 kappa/15)n h^2.
```

Every point of the surviving interval is at distance at most

```
5 sqrt(n kappa) h
```

from `y_i` for a continuous coordinate. For an integer coordinate, the
valid bound is `1+5 sqrt(n kappa)h`. To check these constants, the selected
endpoint has distance at most
`(sqrt(17/15)+1)sqrt(n kappa)h` from `y_i`; the adjacent interval length is
at most `h+theta(sqrt(17/15)+2)sqrt(n kappa)h`, except that an integer unit
interval may instead have length one. These bounds are strictly below the
displayed constants.

Consequently the next side length is at most
`10sqrt(n kappa)h` continuously, or `2+10sqrt(n kappa)h` for integer
coordinates. With next scale `h'=h/2` and `H'=max(h',1)`, the integer grid
count depends on

```
theta side_length/H' <= 2theta+20theta sqrt(n kappa)
                     < 1/2+8sqrt(n).
```

The continuous count has the same bound without the additive term. Thus
the number of coordinate states is `O(theta^-1 log(n+2))`, independently of
the accuracy stage. The logarithm of the conditioning ratio is unnecessary
in this count.

## 3. Unknown growth and the state cap

Naively running the old unknown-growth schedule is insufficient for the
new FPT claim: a failed trial need not prune, and can spend a number of table
operations proportional to `(accuracy bits)^p` before the successful trial.

A direct repair is to try `theta_m=2^(-m-2)` and impose the integer cap

```
Q_m = 100 theta_m^-1 ceil(log2(n+2)).
```

Generate each coordinate grid only until it finishes or has `Q_m+1` nodes.
In the latter case abandon the trial before allocating its product tables.
The initial stage and every later stage of the first admissible trial fit
below this cap by the preceding bounds and the existing geometric-grid
count. Every earlier trial has the same per-stage cap, whether or not its
growth estimate was valid.

Use the old finite stage budget for each trial, including its exact-QP
reconstruction target when exact rational output is required. Those targets
and budgets are monotone in `m`. Summing the work of earlier trials is then
a geometric sum in `theta_m^-p`, times polynomial factors. The factor
`log(n+2)^p` can be absorbed into `f(p)` times a fixed power of `n`:
maximizing `t^p exp(-t)` gives the usual bound. Thus the exponent of input
length and requested accuracy does not grow with `p`.

The cap changes no correctness condition: every deletion and returned lower
bound is valid for every positive trial parameter. Growth is used only to
show that an admissible trial completes within the cap and stage budget.

## 4. Min-marginals and rational arithmetic

All coordinate min-marginals can be computed by two-way min-sum message
passing on the supplied tree decomposition. After both message directions
are available, a bag belief is the exact optimum conditional on that bag
assignment. Minimize one such belief over all but a chosen coordinate.
Choose any containing bag for each coordinate. This costs
`O(p(N+number_of_factors)Q_m^p)` table work, up to routine indexing costs.
Arbitrary tree branching does not require a product of child state spaces.
The box-only setting has finite factor values and finite messages; outgoing
messages can be formed from accumulated neighboring messages without
quadratic overhead in bag degree.

For rational QP data there is a useful common-denominator invariant. Let `D`
be a common denominator of all input coefficients and endpoints. Write
`theta=2^-k`, `h_j=s2^-j`. An outward geometric offset after `t` steps is

```
h_j ((1+theta)^t-1)/theta.
```

Its denominator divides `D 2^(j+k max(t-1,0))`. All original endpoints lie
on the lattice `D^-1 Z`. Adding an old center takes the maximum dyadic
exponent, and clipping at an old endpoint preserves the same invariant.
Thus through stage `J`, every continuous coordinate lies in

```
(D 2^T)^-1 Z,       T<=J+k Q_m.
```

Integer coordinates are integral. Quadratic values and curvature
corrections share a denominator dividing `8D^3 2^(2T)`. Dynamic programming
uses sums, differences, comparisons, and selections, so it does not create
a product of table-entry denominators. Input box bounds and the number of
factors bound the numerators. The resulting bit lengths are polynomial in
the input length, `J`, and `kQ_m`. A separate reviewer independently
confirmed both this invariant and the state-cap repair.

## 5. Certificate history is required

The final restricted-grid DP alone is not a certificate over the original
box. Include the pruning history, or let a checker recompute that history.
At each stage the checker verifies the grids, correction values,
min-marginals, feasible incumbent, and retained coordinate hulls.

Every point lost from a retained box lies in at least one deleted coordinate
interval, whose conditional lower bound exceeds that stage's incumbent.
Monotonicity gives

```
deleted_region_lower_bound > U_old >= U_final >= LB_final.
```

Therefore the final lower bound applies on all discarded regions as well
as on the final retained box. Recording the successful trial suffices;
abandoned trials are not needed for the certificate. The total record has
the same FPT bound as the computation. No supplied or guessed growth
constant is needed by the checker.

For exact rational QP output, the height bound and rational reconstruction
in [the exact-QP note](../geometric-dp/exact-box-qp.md) apply unchanged once
this genuinely global lower bound is available. Feasibility, integrality,
and exact objective equality still require the stated final checks.

## Verification record

This review checked the conditional rounding argument, endpoint coverage,
center retention, localization inequalities, integer unit intervals,
failed-trial costs, message-passing work, common denominators, and certificate
coverage. It used only targeted reads of the two cited mathematical notes
and local instructions. No numerical test, project-wide verification, CI
inspection, or external search is claimed.
