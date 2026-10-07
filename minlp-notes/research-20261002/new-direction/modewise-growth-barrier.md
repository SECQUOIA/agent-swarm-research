# Mode-wise growth does not remove discrete arithmetic difficulty

Date: 2026-10-02. Status: an elementary reduction and a routine forest-oracle
corollary, with [independent mathematical review](../reviews/modewise-growth-barrier-review.md).
The review's minor zero-objective inequality correction has been applied.
No novelty claim or literature comparison is made here.

## Claim and scope

Uniform quadratic growth within every discrete mode does not suffice for
polynomial-time exact optimization of bounded-treewidth mixed box QP.
This remains true when the continuous relaxation is convex, all variables
lie in the unit interval, the full Hessian norm is bounded by an absolute
constant, and the interaction graph has treewidth two.

The reduction is from ordinary SUBSET SUM, a weakly NP-complete problem.
It also rules out a certified additive-approximation algorithm polynomial
in input length and `log(1/epsilon)` under these assumptions, unless
`P=NP`. It does not rule out pseudo-polynomial algorithms, approximation
polynomial in `1/epsilon`, or algorithms with additional discrete
arithmetic or geometric parameters.

## Reduction

Start with positive integers `a_1,...,a_n,B`, where `B>0`. Discard every
`a_i>B`, since it cannot belong to a subset summing to `B`. Instances with
no remaining item are trivial. Thus assume `n>=1` and `1<=a_i<=B`.

Introduce binary `z_i`, continuous `s_i in [0,1]`, and fixed `s_0=0`.
Set

```
b_i = 2^(-i) a_i/B,       tau = 2^(-n),
F(s,z) = sum_(i=1)^n (s_i - s_(i-1)/2 - b_i z_i)^2
         + (s_n-tau)^2.
```

The coefficients are rational and have polynomial encoding length.
Each `b_i` has a numerator of at most `O(log B)` bits and a denominator
of at most `O(log B+i)` bits. The full representation has
`O(n log(B+1)+n^2)` bits, apart from ordinary indexing overhead, and hence
polynomial size in the SUBSET SUM input length. Expanding the squares
also preserves polynomial encoding length.

Each recurrence factor has scope `{s_(i-1),s_i,z_i}`; the initial fixed
coordinate is omitted. These bags form a path with one-state separators.
The interaction graph therefore has treewidth at most two, and exactly
two when `n>=2`: every later recurrence factor contains a triangle with
nonzero coefficients. Every state occurs in at most two recurrence bags;
every binary variable occurs in one.

Since the objective is a sum of squares, `F>=0`. It equals zero precisely
when every recurrence and the terminal equation hold. Iterating the
recurrence then gives

```
s_n = sum_(i=1)^n 2^(-(n-i)) b_i z_i
    = 2^(-n) (sum_i a_i z_i)/B.
```

Thus `min F=0` if and only if a subset sums to `B`. Conversely, the
trajectory from any binary assignment satisfies the box bounds: starting
from zero, `0<=s_i<=s_(i-1)/2+1/2<=1`. In particular, a successful subset
always gives a feasible zero-objective point.

## An explicit objective gap

For any feasible point, put

```
r_i = s_i-s_(i-1)/2-b_i z_i,       r_T = s_n-tau,
delta(z) = 2^(-n) ((sum_i a_i z_i)/B-1).
```

Telescoping gives

```
delta(z) = r_T - sum_(i=1)^n 2^(-(n-i)) r_i.
```

Cauchy--Schwarz therefore yields

```
delta(z)^2 <= (1 + sum_(k=0)^(n-1) 4^(-k)) F(s,z)
           <= (7/3) F(s,z).
```

On a NO instance, integer subset sums imply
`|delta(z)|>=2^(-n)/B` for every mode. Consequently

```
min F >= Delta,       Delta = (3/7) 4^(-n) / B^2.
```

The number `Delta` has polynomial bit length, and
`log(1/Delta)=O(n+log B)`. An additive approximation with error less than
`Delta/2` distinguishes YES from NO, whether it returns a guaranteed
additive value estimate or a certified interval of that width. For a
feasible near-optimal objective, YES gives a value below `Delta/2`, while
NO gives a value at least `Delta`. Hence polynomial dependence on
`log(1/epsilon)` would solve SUBSET SUM in polynomial time.

## Uniform curvature and growth within each mode

Write `D=I-S/2`, where `S` is the backward shift on `R^n`, and write
`C=diag(b_1,...,b_n)`. The residual vector is `Ds-Cz`. Since `||S||<=1`,

```
(1/2)||v|| <= ||Dv|| <= (3/2)||v||.
```

For every fixed binary mode, the state Hessian is the same matrix

```
H_s = 2(D^T D + e_n e_n^T),
(1/2)I <= H_s <= (13/2)I.
```

Each mode therefore has a unique box-constrained state minimizer `s*(z)`.
Strong convexity and the first-order inequality at that constrained
minimizer give, including boundary minima,

```
F(s,z)-min_u F(u,z) >= (1/4)||s-s*(z)||^2.
```

The entire continuous relaxation in `(s,z)` is convex. Its Hessian is

```
H = 2([D,-C]^T [D,-C] + e_(s_n)e_(s_n)^T).
```

Here `||C||<=1/2`, so

```
0 <= H,       ||H|| <= 2((3/2)^2+(1/2)^2+1) = 7.
```

The largest diagonal curvature is at most four. These bounds are
independent of `n`, `B`, and the item values. The continuous-state slice
condition number is at most thirteen. Thus the hardness does not come
from badly conditioned continuous optimization within a fixed mode.

## Why this does not contradict the conditioned algorithms

The existing [finite-state extension](../geometric-dp/extensions.md)
requires growth relative to a common optimal exposed vector, or the
[anchor theorem](projection-anchors.md) requires growth toward the
projected global optimal set. Neither assumes only growth around each
mode's own minimizer. The mode-wise estimate above provides no useful
uniform constant for those stronger conditions.

A two-item family makes the distinction explicit. Take `n=2`, `B>=3`,
`a_1=B`, and `a_2=B-1`. The unique globally optimal mode is `(1,0)`, with
state vector `(1/2,1/4)` and value zero. The other mode `(0,1)` has the
feasible recurrence trajectory `(0,(B-1)/(4B))`, whose objective is
`1/(16B^2)` and whose squared distance from the optimal state vector is
`1/4+1/(16B^2)`. Therefore any projected global growth constant satisfies

```
g <= 1/(4B^2+1),
```

even though every mode retains growth constant `1/4` and the uniform
curvature bounds above. With binary-encoded `B`, this upper bound can be
exponentially small in the input length.

The missing information concerns how different mode minima compete and
where their continuous centers lie. Enumerating the finite states inside
a sparse DP does not by itself control that information.

## Width one: a routine corollary of the forest oracle

For comparison, arbitrary rational binary--continuous box QP is exactly
polynomial-time solvable when its full interaction graph is a forest,
using the existing continuous forest box-QP oracle cited in
[the feedback-vertex note](fan-exploration.md). This observation does not
require growth or convexity and is not claimed as a new forest algorithm.

Write the original objective with squared coefficient `q_i` on each
binary variable `z_i`. Relax `z_i` to `[0,1]` and add

```
M_i z_i(1-z_i),       M_i=max(0,q_i)+1.
```

For fixed values of the other variables, the new objective is a strictly
concave quadratic in `z_i`. Its minimum over that interval occurs at an
endpoint. Sequentially replacing the binary coordinates of a continuous
optimum by minimizing endpoints never increases the objective, and
produces a binary optimum. At every binary point the added terms vanish,
so the relaxed penalized optimum equals the original mixed optimum.
The additions are unary, preserve the forest graph, and have polynomial
encoding length. Applying the rational continuous forest oracle and then
endpoint rounding proves the claim.

This gives a narrow structural contrast: the known forest oracle handles
width one, while the width-two reduction blocks the proposed extension
based only on mode-wise conditioning. It does not classify other
restrictions on width-two models.

## Verification and attribution limits

The derivation above is algebraic. The targeted command
`python3 - <<'PY' ... PY`, using only `fractions.Fraction` and
`itertools.product`, passed the following exact checks: 140 SUBSET SUM
instances with `1<=n<=3`, `1<=B<=4`, and every item tuple in
`{1,...,B}^n`; all 940 binary-assignment trajectories; and 22,740
telescoping-identity and gap checks over state vectors in `{0,1/2,1}^n`.
It also checked the displayed growth ratio for `3<=B<=100` and 539
endpoint-concavification cases with squared and linear coefficients in
`{-3,...,3}` and interval points `k/10`, `0<=k<=10`. All checks passed.
These finite checks do not establish the reduction for arbitrary inputs.
No project-wide checks or CI inspection were run. The
[independent review](../reviews/modewise-growth-barrier-review.md) checked
the reduction, gap, bit lengths, curvature, constrained mode growth,
global-growth example, and forest corollary. Its only requested correction
was replacing the final strict Cauchy--Schwarz comparison by a non-strict
one, so the display also holds at zero-objective points; this is applied
above. The review records additional exact active-face, boundary-growth,
Hessian, and graph checks. External source comparison remains separate. SUBSET SUM
hardness and the continuous forest oracle are existing results; this note
makes no priority claim for their combination or this reduction.
