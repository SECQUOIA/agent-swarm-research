# Weighted reconstruction cannot repair a drifting fan certificate

Date: 2026-10-02. Status: an explicit obstruction for the existing
closed-intersection shell certificate, with a fixed canonical coefficient
allocation. This is not an optimization lower bound, and it does not rule
out different partitions, slopes, decompositions, or refactorizations.
No external search or knowledge-base material was used.

## Main conclusion

The current regridded certificate can have a lower bound at most `-1/64`
even when its center is the exact optimizer, the optimum is zero, the
interaction graph is a fan of treewidth two, the global Hessian norm is at
most `3/2`, and global quadratic growth holds with `g=1/4`.
This persists at arbitrarily fine base mesh sizes when the grading ratio
is fixed and the fan is sufficiently long.

Consequently, changing only the representative of the coordinate copies,
or their weights in an error estimate, cannot remove the occurrence
dependence of this certificate. The lower bound itself is wrong by a
constant amount; its soundness as a lower bound is unaffected.

The obstruction uses the existing rule that cells meeting only at a
boundary are eligible. A valid strengthened implementation can omit those
pairs, as the original certificate note explicitly observes. The example
below does not establish the same obstruction for that implementation.

## 1. A rational nonconvex family with fixed global conditioning

Let

```
n = 4^r,        beta = 1/4,       a = beta/sqrt(n) = 2^(-r-2),
b = 1/8,       A = 3/8,
X = [0,1] x [-1,1]^n.
```

Write the first coordinate as `u` and the other coordinates as
`v_1,...,v_n`. Define

```
F(u,v) = A u + (1/2) sum_i v_i^2
                 + a u sum_i v_i - b sum_(i=1)^(n-1) v_i v_(i+1).       (1)
```

All data are rational, and the binary input length is polynomial in `n`.
Every displayed edge coefficient is nonzero. The interaction graph is the
fan consisting of a path on the `v_i` and the common hub `u`.

The Hessian is the sum of the leaf identity, a hub-arrow matrix of norm
`beta`, and a path-adjacency matrix of norm at most `2b`. Therefore

```
||H||_2 <= 1 + beta + 2b = 3/2.                                      (2)
```

The Hessian is indefinite: its principal submatrix on `u,v_i` has
determinant `-a^2`. Nevertheless, the boundary linear term gives uniform
global quadratic growth. Put `s=||v||_2`. Since

```
|sum_i v_i| <= sqrt(n) s,
sum_(i=1)^(n-1) |v_i v_(i+1)| <= s^2,
beta u s <= 2 beta^2 u^2 + s^2/8,
```

we have, for `0<=u<=1`,

```
F(u,v) >= A u - 2 beta^2 u^2 + (1/2-b-1/8)s^2
       >= (A-2 beta^2)u^2 + s^2/4
        = (u^2+s^2)/4.                                               (3)
```

Thus the unique optimizer is `c=x*=0`, the optimum is zero, and `g=1/4`
works globally. The ratio `||H||_2/g` is at most six.

## 2. Fixed path decomposition and canonical allocation

Use the `N=n-1` bags

```
V_t = {u,v_t,v_(t+1)},       t=1,...,N,
```

in path order, rooted at bag 1. Bag size is three. The separator of bag
`t>=2` is `{u,v_t}`. Assign `A u` to the root. Assign each `v_i^2/2`
and `a u v_i` to bag `i` when `i<n`, and assign the two terms for `v_n`
to the last bag. Assign `-b v_i v_(i+1)` to bag `i`.

Every coefficient is assigned exactly once. At the center zero, every
nonroot subtree gradient is zero, so every prescribed separator slope is
zero. In particular, the large enough linear term that proves (3) is
paid only by the root hub copy.

Consider a configuration in which every leaf-coordinate copy is `-a`.
Let `u_t` be the hub copy in bag `t`, and require `u_1=0`. The sum of the
unrelaxed local objective values is exactly

```
Psi = beta^2/2 - a^2 [sum_(t=1)^N u_t + u_N] - b(n-1)a^2.             (4)
```

Any valid local lower models satisfy `ell_(t,B_t)(z^t)<=a_t(z^t)`.
Since the slopes vanish, the configuration value `Phi` therefore
satisfies `Phi<=Psi`. This conclusion includes the affine Taylor models
used by the rational box-QP theorem; it does not depend on their error
constants.

## 3. Exact dyadic shell compatibility

Use the shell partitions from Lemma 3.1 of the
[original certificate note](../../research-20260929/theory-decomposition/decomposition-certificates.md).
Let `theta=2^(-mu)`, with `mu>=1`, and let `h=2^(1-j)<=a/2`.
These are exactly the stage mesh sizes for a box with largest side two.

A shell of inner radius `R` and outer radius `2R` has grid spacing
`g_R=theta R`. Its grid lines are integer multiples of `g_R`, because
the center is zero and `2R/g_R` is an integer. Keep grid cells outside
the inner cube, as in that lemma.

We explicitly construct a chain of separator cells along

```
(u,v) = (u,-a),       0<=u<=1.
```

The initial shell has `R=a/2` and spacing `g_R=theta a/2`. Take
`J=[-a,-a+g_R]`. The `2/theta` cells

```
D = I x J,       I=[l g_R,(l+1)g_R],       0<=l<2/theta,
```

cover the portion `0<=u<=a`. They are genuine retained shell cells:
their `J` coordinate lies outside the inner cube. Each lifts to the
genuine bag cell `B=I x J x J`, which contains `(u,-a,-a)` along its
hub interval.

For each later band `[R,2R]`, with

```
R = a, 2a, ..., 1/2,
```

take its `1/theta` hub intervals of length `theta R`, and take any grid
interval `J` containing `-a`. The cells `I x J` and `I x J x J` are
retained shell cells because their hub coordinate lies outside the inner
cube. All boxes have positive side lengths after clipping to the domain.

There are `r+2` later bands. The chain therefore has exactly

```
K = (r+4)/theta                                                     (5)
```

cells. Write their consecutive hub intervals as
`[q_0,q_1],...,[q_(K-1),q_K]`, where `q_0=0` and `q_K=1`.
Two consecutive cells both contain `(q_t,-a)`, even when their `J`
intervals or shell levels differ.

For bags `t<=K`, select the lifted `t`th cell and set `u_t=q_(t-1)`.
For all later bags, select the final cell and set `u_t=1`.
Select the corresponding separator cell at each nonroot bag.
The selected point belongs to both its own bag and separator cells.
Its separator cell meets the preceding bag projection at the shared
chain endpoint. Hence this is a legal configuration under Lemma 1.5.

This proves compatibility using actual grid cells and exact dyadic
alignment. A bound on successive point distances alone would not prove
that compatibility.

## 4. A fixed certificate gap at every finer base mesh

Assume `n>=4K`. All hub copies after bag `K` equal one, and all earlier
copies are nonnegative. The extra `u_N` term in (4) gives

```
sum_(t=1)^N u_t + u_N >= n-K.
```

Substitute this into (4), and drop its nonpositive path-edge term:

```
LB <= Phi <= Psi
   <= beta^2/2 - beta^2(1-K/n)
   <= -beta^2/4 = -1/64.                                            (6)
```

The condition is

```
n theta >= 4(r+4),       r=(1/2)log_2 n.                             (7)
```

It is satisfied by arbitrarily large rational instances for every fixed
positive dyadic `theta`. Once `h<=a/2`, the construction and its count
do not depend on `h`. Thus every finer certificate at center zero still
has the gap in (6). With the exact optimum as incumbent, no tolerance
smaller than `1/64` can be certified by these fixed-center solves.
This does not prove nontermination of the actual regridding iteration:
that iteration can replace zero by a different reconstructed center,
which changes the separator slopes and the subsequent configurations.

Conversely, uniform success on this family with the specified partitions
and slopes requires escaping at least the regime (7). In particular,
the grading ratio must become smaller than a constant times
`log(n)/n`, or the certificate construction must change. This is a
necessary condition established by this example, not a sufficient mesh
bound.

For any reconstruction rule, including a coefficient-weighted average
of hub copies, the reconstructed feasible point has objective at least
zero by (3). Its gap above this lower bound is therefore at least
`1/64`. Choosing a different representative cannot cure (6). A weighted
copy-energy inequality that would imply a vanishing gap for these same
certificates must fail on this configuration.

## 5. What the obstruction does and does not exclude

The essential conclusion concerns the existing closed-intersection
certificate on the specified path decomposition. It is stronger than
showing that an unweighted Poincare estimate is loose: an actual legal
configuration forces the computed lower bound below the true optimum.

There is a strongly convex version as well. Replace `A u` by `u^2/2`,
keep the root assignment, and keep the other terms. The global Hessian
then lies between `(1/2)I` and `(3/2)I`, and the same configuration still
satisfies (4)--(6). This version specifically defeats assigning the hub
diagonal to one bag. Distributing that diagonal can change the result.
For example, with `d=1-2b`, its objective has the decomposition

```
sum_i [u^2/(2n) + (d/2)v_i^2 + a u v_i]
  + (b/2)sum_(i=1)^(n-1)(v_i-v_(i+1))^2
  + (b/2)(v_1^2+v_n^2).                                             (8)
```

Every term is positive semidefinite, since `d>beta^2`. Keeping these
convex terms exact eliminates negative configuration values at zero.
This does not prove that the particular affine Taylor models have the
same property. The nonconvex family (1) has no hub diagonal available
to distribute; its boundary linear term is lost away from the root
copy in the fixed-slope relaxation.

Two limitations are material:

- The original note permits strengthening the valid DP by omitting
  intersections that only touch in both its local-consistency and
  child-minorant constraints. The chain above uses those pairs.
  Omitting them in both places blocks this chain. Omitting only the
  parent-bag/child-separator pairs does not: choose each child separator
  to be the preceding bag's projection and move the boundary-only
  intersection to the child's own bag/separator pair. Whether all
  remaining copy drift can be controlled requires a separate proof;
  this example does not answer it.
- Choosing different affine slopes, anisotropic or coordinated
  partitions, another decomposition, or adding cancelling bag terms
  changes the relaxation. No impossibility claim for those choices,
  or for an occurrence-free optimization algorithm, follows here.

## Verification record

The algebra and shell-cell construction were checked directly against
the displayed definitions in the local certificate notes. An independent
math exploration obtained the same fan construction, verified (3), and
derived the PSD decomposition (8). A separate geometric reviewer read
the original definitions and verified the exact cell chain and count.
That review also identified the distinction between omitting touching
pairs in one constraint and in both constraints, stated above. Neither
review found a mathematical defect in the scoped obstruction.

The targeted command actually run was `python3 - <<'PY'`, with an inline
`fractions.Fraction` check of the displayed construction. It passed
105 shell cases, containing 11,718 exact cells, at seven fan sizes, five
dyadic grading ratios, and three finer base meshes. The checks verified
grid alignment, shell membership, domain clipping, successive closed
intersections, the exact count (5), and 69 negative-gap instances meeting
(7). Exact identities for the growth constants and the note's local
Markdown link also passed. No full dynamic program was implemented or
run; (6) follows from its configuration characterization.

No project-wide verification, CI inspection, external search, or
knowledge-base access was performed.
