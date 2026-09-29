# Penalty encoding and the dimension of nonlinear dependence

Date: 2026-09-27. Status: research continuation. The rank theorem below has
a complete proof and independent adversarial reviews of its main steps.
It is a structural refinement of the existing penalty manuscript, not yet
a claim of a substantial standalone advance or settled priority.

## 1. Question and result

The manuscript in `paper-exact-penalties` proves that exact norm penalties
can need exponentially many bits in the continuous dimension. It also
proves polynomial encoding when either continuous dimension or the number
of nonlinear native inequalities is fixed. A different situation occurs
when many constraints depend quadratically on the same few linear
features of the continuous variables.

Consider the manuscript's model: rational expanded polynomials of total
degree at most two, finite rational boxes, continuous variables `x`, boxed
integer variables `z`, convex native quadratic inequalities
`g_i(x,z) <= 0`, and a separate affine
linking equality `Ax+Bz=b`. Assume feasibility and refined Slater on every
equality-feasible slice: all native inequalities nonlinear in `x` are
simultaneously strict at some point satisfying the native affine constraints
and the linking equality. Let `N` be the explicit binary input length,
including the objective data when stating an objective-dependent bound.

Write `Q_i` for the positive semidefinite continuous Hessians of the native
inequalities, excluding the objective, and define

```
V = intersection_i ker Q_i,
r = codim V = rank(sum_i Q_i).
```

The equality follows from positive semidefiniteness. The integer variables
cannot affect these Hessians because the total degree is at most two.

Let `X` be the native set and `F={(x,z) in X:Ax+Bz=b}`.

**Theorem 1 (joint native Hessian rank).** There is a finite constant
`C >= 1` such that

```
dist_2((x,z), F) <= C ||Ax+Bz-b||_infinity  for every (x,z) in X,
log_2 C <= N^{O(1)} 2^{O(r)}.
```

Consequently, for any rational quadratic objective, including an
indefinite one, there is an integer coefficient `rho >= 1` satisfying

```
bit(rho) <= N^{O(1)} 2^{O(r)}
```

for which the minimizers of

```
f(x,z) + rho ||Ax+Bz-b||_infinity
```

over the native set are exactly the original optimal feasible points.
The same coefficient works for the one-norm. All constants are absolute.
More generally, an objective with supplied Lipschitz constant `L` on the
input box admits every coefficient `rho>L C`. The extra bits depend on
the supplied encoding of `L`. The quadratic case automatically supplies
an `L` of polynomial bit length.

Thus fixed `r` permits polynomial-time output of a conservative sufficient
integer coefficient on the promised input class, without enumeration of
integer slices. This is an output guarantee, not a polynomial-time solution
method or useful numerical calibration rule.

The parameter has an intrinsic linear-algebraic meaning for the supplied
quadratic functions: it is the smallest number of linear features needed
to express all their quadratic parts. It is invariant under invertible
affine changes of continuous coordinates. It is **not** an invariant of
the feasible set under arbitrary alternative descriptions. Redundant
quadratic inequalities can increase it.

**Affine-restriction variant.** If supplied native affine equalities are
`Ex+Dz=e`, use rational elimination to choose a basis matrix `W` of
`ker E` whose free-coordinate rows form the identity.
The same result holds with

```
r_E = rank(sum_i W^T Q_i W)
```

in place of `r`, provided refined Slater is imposed only on rows that
remain nonlinear after this restriction. Slice-wise inconsistent affine
equalities discard that slice. Otherwise rational elimination writes
`x=x_0(z)+W u` with uniform polynomial-bit data; the free coordinates
`u` are selected among the original coordinates and retain rational
box bounds. The rank `r_E` is independent of this basis choice.
Apply the proof below in these coordinates. When translating a repair
within a feasible fiber back to `x`, multiply its distance bound by
`||W||_2<=2^{N^{O(1)}}`, which preserves the displayed asymptotic bound.
Infeasible fibers still use the original full box diameter. This reduction
uses native equalities, not the linking equalities being penalized.

## 2. Eliminating the common linear directions

The following elementary projection fact supplies the reduction. It is a
coefficient-sensitive application of Farkas' lemma, not a new projection
theorem.

**Lemma 2.** Suppose a system has the form

```
C v + q(u,t) <= 0,
```

with at most `M` rows, rational `C`, and convex quadratic row functions
`q_i` in `u`, affine in the scalar `t`. If all initial dimensions, row
counts and coefficient bit lengths are polynomial in `N`, then its
projection onto `(u,t)` has a description by at most `2^M` convex quadratic
weak inequalities, each with coefficient bit length polynomial in `N`.
The projected rows remain affine in `t`.

**Proof.** Let `K={y >= 0:C^T y=0}`. Farkas' lemma says that the fiber in
`v` is nonempty exactly when `y^T q(u,t) <= 0` for every `y in K`.
The cone `K` is pointed and is generated by its extreme rays; if it is
zero, no inequalities are required. Every extreme ray has support at most
`rank(C)+1`, and a support determines at most one ray. To see the support
bound, let `S` be a ray's positive support. If the nullspace of `C_S^T`
had dimension greater than one, a sufficiently small perturbation in
both signs along an independent null vector would stay positive on `S`,
contradicting extremality. Thus `|S|-rank(C_S^T)=1`.

A generator follows from minors after fixing one nonzero coordinate, so
rational determinant bounds give polynomial coefficient bit length.
There are at most `2^M` supports. Each row `y^T q` sums at most `M`
polynomial-bit rational multiples of polynomial-bit quadratic coefficients;
its coefficient bit length remains polynomial. Nonnegative weights
preserve convexity. Denominators can be cleared separately in each output
row; no common denominator over exponentially many rows is needed.
Farkas' lemma establishes equality of the projection
and the weak-inequality description directly; no assertion that arbitrary
closed convex projections are closed is used. ∎

For every integer slice, choose a rational basis `T_0` of `V` and a
rational complement `T_1`. Rational elimination supplies such matrices
and the inverse of `T=[T_1 T_0]` with polynomial coefficient bit length.
Write

```
x = T_1 u + T_0 v,       u in R^r.
```

Every native row is quadratic only in `u` and affine in `v`, since
`Q_i T_0=0`. Affine residual rows, box rows and additional scalar bounds
retain this form. Substitution of any boxed integer assignment and the
coordinate change preserve polynomial bit length uniformly in the slice.
Consequently Lemma 2 applies to all auxiliary systems below.

There is no requirement to construct this exponentially long projection.
Its role is to establish quantitative bounds. The logarithm of its row
count is polynomial, which is what the next argument needs.

## 3. Two small-dimensional reciprocal constructions

We use the following consequence of [Basu and Roy's final author
manuscript, Theorems 3 and 4](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf).
For degree-two integer polynomial systems in `d` variables, coefficient
bit size `tau`, and `S` rows, a radius `R` can be chosen with

```
log_2 R <= (tau + log(S+1) + 1) 2^{O(d)}.
```

Such a ball contains every bounded component and meets every nonempty
component of a basic closed system. We only use weak inequalities and
equations. The exponential row count from Lemma 2 therefore contributes
polynomially to `log R`. The inspected final source, unlike an earlier
online draft, explicitly states the required weak-sign scope.

**Infeasible slices.** Fix a nonempty native slice that cannot meet the
linking equality. Its compactness gives

```
delta_z = min_Xz ||Ax+Bz-b||_infinity > 0.
```

Choose a positive rational `R_0` of polynomial bit length that bounds the
residual norm throughout the input box. Add the affine inequalities

```
-t <= (Ax+Bz-b)_j <= t,       0 <= t <= R_0.
```

Project the common-kernel variables `v`. The resulting set `P_z` in
`(u,t)` is compact, being the projection of a compact original system,
and all its points have `t >= delta_z`. Consider

```
H_z = {(u,t,w):(u,t) in P_z, w >= 0, t w = 1}.
```

This is a nonempty bounded basic closed set in `r+2` variables; every
polynomial still has degree at most two. Its largest `w` is exactly
`1/delta_z`. The containing-radius bound gives

```
delta_z^{-1} <= 2^{N^{O(1)} 2^{O(r)}}.                 (1)
```

**Positive Slater margins.** On an equality-feasible slice with nonlinear
native rows, let `P_z^aff` consist of its affine native constraints and
the linking equality. Consider

```
x in P_z^aff,
g_i(x,z) + t <= 0 for each nonlinear native row i,
0 <= t <= 1.
```

Refined Slater makes a point with `t>0` exist. The original box rows are
among the native affine constraints. After the same projection, append
`w>=0` and `tw=1`. This basic closed set in `r+2` variables is nonempty.
It need not be bounded: values `t` approaching zero can make `w` diverge.
Use the **meeting-radius** bound here. It supplies one point with
`w <= 2^{N^{O(1)}2^{O(r)}}`, and therefore an original feasible point
whose common nonlinear slack is at least

```
sigma_z >= 2^{-N^{O(1)} 2^{O(r)}}.                   (2)
```

Projection equality ensures a corresponding original `x` exists. Neither
that point nor its coordinates have to be rational. This use of meeting
versus containing radii is essential.

## 4. A global error bound and arbitrary quadratic objectives

We first prove a coefficient bound for affine repair. Let `P` be a
rational polyhedron with polynomial-bit normals and let
`E=P intersect {Ax=d}` be nonempty. For every `x in P`, there exists
`y in E` with

```
||y-x||_2 <= H ||Ax-d||_infinity,       H <= 2^{N^{O(1)}}.       (3)
```

Indeed, take the Euclidean projection `y` of `x` onto `E`. The polyhedral
normal-cone formula gives

```
x-y = sum_i mu_i a_i + A^T lambda,
```

where `a_i` are normals of native affine rows active at `y` and `mu_i>=0`.
Conic elimination selects linearly independent generators among the
`a_i` and the signed equality normals. A nonsingular minor and rational
determinant bounds give a representation with
`||lambda||_1 <= H ||x-y||_2`, for uniform `H<=2^{N^{O(1)}}`.
Since `x in P` and `a_i` is active at `y`, `a_i^T(x-y)<=0`. Therefore

```
||x-y||_2^2 <= lambda^T A(x-y)
             <= H ||x-y||_2 ||Ax-d||_infinity.
```

Cancel the nonzero distance; the zero-distance case is immediate. This
is the standard polyhedral error-bound argument with its rational
coefficient estimate included. It neither uses Slater nor requires
independent original rows.

Now fix a feasible integer slice and `x in X_z`. Let `P` contain its
native affine constraints, including the input box, and set
`E=P intersect {Ax+Bz=b}`. Write
`e=||Ax+Bz-b||_infinity`. Apply (3) to obtain `y in E` with
`||y-x||_2<=H e`. Let `G` be a uniform Euclidean gradient bound for the
native quadratic functions on the continuous input box, and let `D`
bound the box diameter. Both have polynomial-bit rational upper bounds.
For every nonlinear row,

```
g_i(y,z) <= G H e = eta,
```

because `g_i(x,z)<=0` and the segment from `x` to `y` stays in the box.
Take a Slater point `xbar in E` with `g_i(xbar,z)<=-sigma_z` and define

```
alpha = eta/(sigma_z+eta),
w = (1-alpha)y + alpha xbar.
```

Then `w in E`. Convexity gives
`g_i(w,z)<=(1-alpha)eta-alpha sigma_z=0`, so `w in F_z`.
Furthermore,

```
||w-x||_2 <= H e + alpha D
            <= H(1+GD/sigma_z) e.                              (4)
```

When there are no nonlinear rows, take `w=y` and use (3). Notice that
the point being projected already satisfies every native affine row;
this is why only the linking residual appears in (3).

For a point on an equality-infeasible integer slice, select any fixed
point of the nonempty global feasible set. Its distance from the
original point is at most the diameter `D_all` of the full `(x,z)` input
box. Equation (1) then gives

```
dist_2((x,z),F) <= (D_all/delta_z) e.                           (5)
```

Combining (1), (2), (4), and (5) proves the first assertion of Theorem 1.
All bounds are uniform in boxed integer assignments, so the number of
slices does not enter the result.

For any objective with Lipschitz constant `L` on the full input box,
compactness supplies a nearest feasible point `a*` to each `a in X`.
Hence

```
f(a) >= f(a*)-L dist_2(a,F) >= v-L C ||r(a)||_infinity.
```

Every `rho>L C` makes every infeasible point strictly worse than `v`,
while original feasible minimizers attain `v`. A rational quadratic
objective, of arbitrary Hessian sign and rank, has a polynomial-bit
Lipschitz bound on the rational input box. This proves the penalty
conclusion. The one-norm conclusion follows by domination. ∎

For fixed `r`, a universal conservative rule can print `2^B` with
`B=N^C 2^{C(r+1)}` for a sufficiently large absolute constant `C`.
This does not require computing the projected rows or the slice margins.
The asymptotic constants have not been evaluated for numerical use.

## 5. What this adds, and what it does not

The theorem adds a parameter not covered by either existing positive
bound. Arbitrarily many constraints can use the same one-dimensional
quadratic feature while both the total continuous dimension and the
nonlinear row count grow. For example, rows

```
(a^T x)^2 + c_i^T x + d_i <= 0
```

all have common rank one even when the affine parts span many directions.
No sign or rank restriction on the quadratic objective Hessian is needed.
The error bound also supplies objective-independent feasibility repair
control, although the proof is not an efficient repair algorithm.
Such models can arise
when constraints use a small set of aggregate nonlinear quantities, but
no concrete solver improvement is established here.

The dependence on `r` cannot be replaced by a polynomial uniformly. In
the manuscript's chain of length `n`, the native quadratic Hessians have
joint rank `n-1`. The proved optimized-dual threshold is
`2^{2^n-1}`, whose ordinary binary representation has `2^n` bits. Thus
the rank dependence in Theorem 1 has the correct exponential order,
up to unspecified absolute constants and polynomial input factors.

Individual Hessian rank is a different parameter. Every nonlinear row
in the chain has rank one. Sparse interactions and small individual rank
therefore cannot replace joint rank.

The strict convexity and numerical conditioning of the *objective* also
do not control the native geometry. Conversely, Theorem 1 does not claim
anything without the stated Slater assumption on feasible slices.

### A limitation of facial-reduction depth

The chain also separates arithmetic conditioning from qualitative conic
regularity. Write `s_i=2^{-2^i}` and use the semidefinite form

```
X_i(a) = [[a_{i+1}, a_i], [a_i, 1]] >= 0,
a_1-s_1 >= 0.
```

The native system has a strict conic point, so its singularity degree is
zero. After adjoining the optimal-value equality `a_n=s_n`, exactly one
facial-reduction step suffices, independently of `n`. To check this, set

```
lambda_{n-1}=1,
lambda_{i-1}=2 s_i lambda_i,
lambda_0=2 s_1 lambda_1,
S_i=lambda_i [[1,-s_i],[-s_i,s_i^2]].
```

For `n>=2`, all these coefficients are positive, every `S_i` is positive
semidefinite of rank one, and direct telescoping gives

```
a_n-s_n = lambda_0(a_1-s_1) + sum_i trace(S_i X_i(a)).
```

At `a_n=s_n`, every nonnegative term on the right vanishes. The exposing
matrix `S_i` leaves precisely the ray generated by `X_i(s)`, and the seed
slack becomes zero. The point `a=s` lies in the relative interior of this
product face, with all box slacks positive. Thus there is no further
facial reduction to perform. The original conic system is not strictly
feasible after the equality is added, so its singularity degree is one.

Nevertheless `lambda_0=2^{n+1-2^n}` already has an exponentially long
ordinary denominator. A one-step exposing certificate can therefore
carry the same arithmetic difficulty as the exact penalty. Native
singularity degree or optimal-face singularity degree alone does not
bound penalty encoding. This is an elementary consequence of the
existing chain, not a claimed new general result on facial reduction.

The same chain has rank-one individual Hessians, diagonal commuting
Hessians, and a path as its quadratic variable-incidence graph. These
parameters likewise fail to exclude exponential penalty bit length.

## 6. Sources examined and priority assessment

- Existing local manuscript: `paper-exact-penalties/sections/02-geometry.tex`,
  `04-general-upper.tex`, `05-fixed-count.tex`, and `07-perturbations.tex`.
  Its proof already supplies the slice decomposition, margins, and
  rational affine-normal coefficient argument. The error-bound proof
  above removes its convex-objective restriction.
- [Basu and Roy (2010), final author
  manuscript](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf),
  Theorems 3 and 4; local copy
  `research-20260925/publication-sources/basu-roy-2010-final.txt`.
  The dependence on `log S`, degree two, and `r+2` variables supports
  the displayed bounds. Their real-algebraic estimates are prior work.
- [Grigoriev and Pasechnik (2005)](https://arxiv.org/abs/cs/0403008v3)
  and [Kamminga and Rudolph's full
  version](https://arxiv.org/abs/2411.03096v2), already compared in the
  local fixed-count manuscript. Their few-quadratic methods motivate a
  different parameter and are not claimed to be superseded here.
- [Ferrez, Fukuda and Liebling, fixed-rank convex quadratic maximization
  over binary variables](https://www.cs.mcgill.ca/~fukuda/download/paper/qpzono040429.pdf).
  The inspected abstract concerns a fixed-rank objective and zonotope
  enumeration. Its setting and algorithmic conclusion differ from the
  native-Hessian penalty bound above. Low-rank reductions themselves
  are plainly established tools.
- [Andersen, On formulating quadratic functions in optimization models,
  revised 2023](https://docs.mosek.com/whitepapers/qmodel.pdf), Sections
  2–3, uses low-rank factors to reduce nonlinear storage and computation.
  It does not state the quantitative error bound above.
- [Pirani, Effective curvature dimension in smooth DC optimization,
  September 23, 2026](https://arxiv.org/html/2609.28319v1), Introduction
  and displayed definition (1), uses the span of Hessian ranges as a
  curvature parameter. Its stated conclusions concern DC decompositions
  and counts of lower-model subproblems, rather than mixed-integer
  feasibility repair or exact-penalty coefficient encoding. This very
  recent source rules out treating the general curvature-subspace idea
  as new.
- [Zhao and Fan, On subspace properties of the quadratically constrained
  quadratic program](https://www.aimsciences.org/article/doi/10.3934/jimo.2017010),
  abstract inspected. It studies solution-containing subspaces. Its full
  assumptions and conclusions still require inspection before a complete
  priority assessment; an abstract alone does not exclude overlap.

Web searches on 2026-09-27 included “convex quadratic programming fixed
rank quadratic constraints bit complexity,” “quadratic common kernel
complexity optimization,” and “exact penalty rank quadratic constraints.”
They did not identify a matching exact-penalty theorem. This limited
search is not evidence of novelty. The candidate contribution is the
rank-sensitive *penalty encoding conclusion*, not Farkas projection,
low-rank coordinate reduction, or effective real-algebraic bounds.

## 7. Verification and next questions

The proof has been independently challenged on projection closedness,
ray coefficient sizes, the unrestricted objective Hessian, and boundedness
of the reciprocal constructions. The review agreed with the argument and
emphasized that the Slater reciprocal system needs a meeting-radius
bound. An alternative reviewed proof eliminates `t` by substitution,
producing degree-three rows in `r+1` variables; the degree-two version
above avoids that substitution.

The stronger error-bound proof was rechecked by a fresh independent
reviewer after its discovery. In particular, the normal-cone sign in (3),
the convex interpolation, and strict penalty inequality were checked.
The separate review is recorded in `penalty-rank-review.md`.

Targeted command actually run:

```
python3 research-20260927/check_penalty_frontier.py
```

Result: `PASS: 289 exact projection fibers; 197 exact repairs; 9 chain
rank/bit identities; 7 exposing identities`. These rational-arithmetic
examples check the projection signs, repair formula, rank indexing, and
the facial-exposure coefficients. They do not prove
the quantified theorem or validate the external algebraic-radius theorem.
No project-wide verification or CI inspection was performed. No Lean
claim is made.

The rank parameter is useful but likely not the strongest next direction.
The dimension of the *linear span* of the native Hessians can be much
smaller than their joint rank. The ongoing derivation in
`hessian-span-reduction.md` targets this stronger parameter and exact
convex-quadratic feasibility. It includes many full-rank constraints
sharing a small quadratic basis, which the joint-rank theorem does not
cover. Its current review status should be read separately.
