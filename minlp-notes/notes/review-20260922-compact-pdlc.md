# Adversarial review of compact inward perturbation for strict PDLC hulls

Date: 2026-09-22. Reviewer: `review_compact_pdlc`.

## Verdict

The simplified proof is correct, conditional on Blekherman–Dunbar's
four-aggregation theorem. I independently rebuilt its compactness,
regular-level, strictification, and multiplier-limit steps. I found no
counterexample or missing hypothesis in those steps. The proof applies to
independent triples in every dimension `n>=1`, not only `n>=3`.

There is also a direct way to cover dependent triples in every dimension:
replace the common perturbation `epsilon I` by three fixed positive
definite perturbation matrices. This removes both the separate dependent
case and its dependence on a two-quadratic aggregation theorem. The full
argument appears below. This extension is independently derived here;
the author and root researcher should recheck it before incorporating it.

This review establishes neither priority nor an efficient algorithm for
finding the four multipliers. It does not independently reconstruct the
topological proof of the external four-bound.

## Source and dimension check

I inspected the primary-source [BD arXiv v1 full
text](https://arxiv.org/html/2405.18282v1), especially Theorem 1.4,
the definitions of permissible and good aggregation, and Section 8.
Theorem 1.4 assumes PDLC, nonempty interior, closure of the interior, and
no points at infinity. Its conclusion uses at most four good aggregations.
It has no restriction `n>=3`. Section 8 explicitly treats `n=1` and `n=2`
in Proposition 8.7; these dimensions are not being inferred from the absence
of a restriction in the theorem statement alone. Section 8 explicitly does
not assume a smooth spectral curve. The proof of the four-bound combines
Propositions 8.6, 8.7, and 8.10.

An attempted opening of the [published eprint](https://epubs.siam.org/eprint/VRNXYR5GPAAPTF5RJHV3/full)
failed in this review's web tool. Accordingly, my personal source check is
of the arXiv text, not an independently successful download of the journal
version. Other reviewers' published-source checks remain separate evidence.

The new limit proof resembles the eigenvector argument used in BD's proof
of Proposition 3.15 in Section 8 to show that good aggregations form a
closed set. Its extra content is that the strictly feasible sets vary and
exhaust the original strict feasible set. This resemblance should be
acknowledged when explaining what is new: the contribution is the complete
compact inward transfer, not the invention of an eigenvector orientation
argument.

## Rebuilt proof, including dependent triples

Let `Qi` be three symmetric `d`-square matrices, `d=n+1>=2`, let
`fi(x)=(x,1)^T Qi(x,1)`, and let

```
S={x:fi(x)<0 for i=1,2,3}.
```

Assume `S` is nonempty, `conv(S)` is proper, and a signed combination of
the `Qi` is positive definite. No independence is assumed.

### 1. Properness rules out a common strictly negative direction

Write `Ai` for the leading block of `Qi`. If `d0!=0` satisfies
`d0^T Ai d0<0` for all three indices, then for every fixed `x` the leading
term of each univariate polynomial `fi(x+t d0)` is strictly negative.
Thus both `x+t d0` and `x-t d0` lie in `S` for all sufficiently large
positive `t`. Their midpoint is `x`, contradicting properness.

This step does not use PDLC. It does not assert the converse: absence of
a common negative direction need not characterize a proper hull.

### 2. Positive definite perturbations can enforce independence

Choose three linearly independent positive definite `d`-square matrices
`R1,R2,R3`. Such a choice exists already for `d=2`; for example,

```
R1=I,
R2=I+e1 e1^T,
R3=I+(e1 e2^T+e2 e1^T)/2.
```

The last matrix has eigenvalues `1/2,3/2` on the first two coordinates
and `1` on the remaining coordinates. Linear independence follows first
from the off-diagonal coordinate, then from the second diagonal coordinate,
and then from the first diagonal coordinate.

Put `Qi(epsilon)=Qi+epsilon Ri`. Select three coordinates of the space of
symmetric matrices for which the coordinate matrix of the `Ri` has a
nonzero determinant. The corresponding determinant for `Qi(epsilon)` is
a degree-three polynomial with nonzero leading coefficient. It has only
finitely many roots. Therefore the perturbed triple is independent for
every sufficiently small positive epsilon.

The signed PDLC certificate persists by continuity of the smallest
eigenvalue. Fixing `x0 in S` proves strict feasibility for all sufficiently
small epsilon. Writing `gi(x)=(x,1)^T Ri(x,1)>0`, the perturbed strict sets
satisfy

```
S_epsilon={x:fi(x)+epsilon gi(x)<0 for all i} subset S.
```

Every fixed finite subset of `S` belongs to `S_epsilon` for every
sufficiently small epsilon. These facts do not require uniform slack over
all of `S`.

### 3. Every positive perturbation has no points at infinity

Each leading block `Bi` of `Ri` is positive definite. A nonzero `d0`
satisfying `d0^T(Ai+epsilon Bi)d0<=0` for every index would satisfy
`d0^T Ai d0<0` for every index, contradicting step 1.

If the corresponding nonstrict set `C_epsilon` were unbounded, choose
`xk in C_epsilon` with norms tending to infinity. A convergent subsequence
of `xk/||xk||` would yield a unit vector satisfying all these nonpositive
leading inequalities. Thus `C_epsilon` is bounded. It is also closed.

### 4. Countably many exceptional levels suffice

For any continuous real function `h` on a space with a countable base,
if a point of `{h<=c}` is not in `cl{h<c}`, that point has value `c`
and has a basic neighborhood `B` on which `h>=c`. Therefore
`c=inf_B h`. There are at most countably many such values.

Apply this fact on `R^n` to

```
h(x)=max_i fi(x)/gi(x).
```

The positive denominators make this a continuous function. Its strict and
nonstrict sublevels at `-epsilon` are exactly `S_epsilon` and
`C_epsilon`. Choose a decreasing positive sequence tending to zero outside
the exceptional levels and small enough for step 2. Then

```
C_epsilon=cl(S_epsilon)=cl(int C_epsilon).
```

The second equality follows by sandwiching `S_epsilon` inside the interior
and using closedness. Nonempty strict feasibility makes the interior
nonempty. Thus every hypothesis of BD's four-bound holds.

### 5. Strictification needs the redundant-inequality deletion

BD gives at most four permissible good aggregated nonstrict inequalities
for `cl(conv C_epsilon)=cl(conv S_epsilon)`. Delete every aggregate
polynomial that is globally nonpositive. At least one remains because this
closed hull is bounded and nonempty.

If a quadratic `p` is not globally nonpositive, it cannot vanish at an
interior point of `{p<=0}`: vanishing there is a local maximum at zero;
the gradient is zero and the Hessian is negative semidefinite, making it
a global maximum. Consequently the retained strict inequalities describe
the interior of their nonstrict intersection. Since `conv S_epsilon` is
nonempty, open, and convex, it equals the interior of its closure. This
proves the required strict description. Each retained aggregate has exactly
one negative eigenvalue, since it has at most one and is negative at `x0`.

The deletion is substantive. A globally nonpositive quadratic can vanish
on an affine hyperplane and its strict sublevel would then remove points
from the interior of the closed hull.

### 6. The fixed-cardinality limit preserves strict goodness

Duplicate multipliers to have four and normalize each to the nonnegative
simplex. Pass to a common subsequence of their quadruples. Denote their
limits by `lambda_j`. The perturbed aggregate matrices satisfy

```
M_kj = sum_i lambda_kji Qi + epsilon_k sum_i lambda_kji Ri
      -> M_j = sum_i lambda_ji Qi.
```

Each limit has at most one negative eigenvalue by eigenvalue continuity
and at least one because its value at `(x0,1)` is strictly negative.
Choose unit eigenvectors for the unique negative eigenvalue, oriented
towards `(x0,1)`, and take another common subsequence. The limiting
eigenvector corresponds to the strictly negative eigenvalue of `M_j`.

For any fixed `x in S`, eventually both `x` and `x0` belong to
`S_epsilon_k`. The kth aggregate is strict-good, so their lifts belong
to the same convex component of its homogeneous negative sublevel. The
oriented eigenvector therefore has positive scalar product with each lift.
Its limiting scalar product with `(x,1)` is nonnegative. It cannot be zero:
`(x,1)^T M_j(x,1)<0`, whereas `M_j` is positive semidefinite on the
orthogonal complement of its negative eigenvector.

All lifts of `S` therefore lie in one component of the negative sublevel
of `M_j`. That component is convex even if `M_j` is singular: in an
eigenbasis it is a strict Lorentz cone times a nullspace. It contains every
lifted convex combination of points of `S`. Thus every limiting aggregate
is strictly negative on `conv(S)`.

Conversely, a point satisfying all four limiting inequalities strictly
satisfies all four perturbed inequalities for sufficiently large `k`.
It belongs to `conv(S_epsilon_k)`, hence to `conv(S)`. This proves exact
equality. Strict feasibility prevents a zero limiting matrix; simplex
normalization prevents a zero limiting multiplier.

## Other claims checked

The four oriented SOC constraints for the closed hull follow correctly
from the strict representation. Convex mixing with a single strictly
feasible point proves that their closed intersection is the closure of the
strict intersection. The orientation cannot be omitted in general.

The claimed sharpness for `n>=3` is consistent with the witness argument:
a negative coefficient of `rho` gives at least `n-1>=2` negative
eigenvalues, forcing every good multiplier into the stated four-ray cone.
This eigenvalue argument does not prove sharpness when `n=1` or `n=2`;
the upper bound extension should preserve that distinction.

No symbolic, numerical, Lean, project-wide, or CI verification was run by
this reviewer. The checks here were mathematical derivations and targeted
primary-source inspection. The main residual dependencies are correctness
of the external BD theorem and the separate priority investigation.
