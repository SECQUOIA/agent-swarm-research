# Review of expected exact work under rational linear perturbations

Date: 2026-10-02. Verdict: no blocking mathematical or bit-complexity
issue found in the completed [expected-work note](../new-direction/expected-smoothed-qp.md).
One wording clarification and the verification record are noted below.

This review covers the full-coordinate perturbation theorem for bounded
continuous rational polytopes with at most two negative Hessian directions.
The [negative-inertia theorem](../new-direction/negative-inertia-qp.md),
its exact convex-QP oracle, and the separately reviewed spectral
normalization are inputs. The finite-grid theorem in Section 8 of the
[proximal-tail note](../new-direction/proximal-growth-tail.md) was checked
for the uniformity and constants used here. This review does not extend
the result to mixed-integer polytopes, fewer perturbed coordinates, or
three or more negative directions.

The grid has the stated uniform tail. With `F_face=2^m` and
`D=8(F_face+1)^2`, the residual is `beta=2nD/M`, independently of the
growth threshold. The condition `M>=2nDB` therefore gives `beta B<=1`
on one fixed sampling grid, including draws with ties. Because `B`
depends only on the number of supplied inequalities, the grid can be
chosen before sampling. Its logarithmic size is
`O(m+log(n+1))`, and each perturbed coefficient has polynomial encoding
length. There is no dependence on an arithmetic bound that itself
depends on `M`.

The fallback is exact even when the ambient Hessian is singular or the
optimizer set contains a continuum. Choose an optimizer whose minimal
face has the least possible dimension. Tangent stationarity and local
minimality make the restricted Hessian positive semidefinite. A tangent
null direction would preserve the objective until it reached the boundary,
producing an optimizer on a smaller face. Hence the restricted Hessian
is positive definite, unless the face is a vertex. An independent basis
of active input rows defines its affine hull, including when the polytope
has lower dimension. The corresponding KKT matrix is nonsingular, so
enumeration includes this optimizer.

Every retained candidate is feasible. Thus additional stationary points
with indefinite tangent Hessians or multipliers of either sign cannot
lower the candidate minimum below the true minimum. Singular systems may
be skipped, and equal objective values may use any deterministic tie rule.
There are at most `2^m` subsets. Each KKT system has order at most `2n`,
and rational linear algebra, feasibility checks, and objective comparisons
take polynomial bit work. Determinant bounds also give polynomial-length
witnesses and values. These facts justify `B P(L)` without assuming growth.

The fast algorithm has the precise conditioning exponent needed by the
expectation calculation. For `k` equal to one or two, spectral normalization
gives `kappa<2+4nu/g_*`; the number of cells and corner queries per level
is `O((1+sqrt(kappa))^k)`. Refinement depth is
`poly(L)+O(log kappa)`. Per-level arithmetic and exact reconstruction add
fixed powers of the bit length and depth, giving

\[
 T_{\rm fast}\le P(L)Z^{k/2}(1+\log Z)^d,
 \qquad Z=\max\{1,\nu/g_*\}.
\]

The polynomial can be enlarged uniformly over `k<=2`. No additional
inverse power of growth is needed. Correctness of the fast algorithm's
lower bounds and acceptance tests does not use growth; only termination
depends on it. The fallback therefore also covers `g_*=0`.

Interleaving elementary bit operations of the two fixed algorithms gives
the minimum of their work bounds up to a fixed factor. The note correctly
requires interruptible arithmetic and convex-QP computations. It does not
treat an uninterruptible exact oracle call as one unit of work. For
`p=k/2>0`, the pointwise bound

\[
 \min\{B,Z^p(1+\log Z)^d\}
 \le(1+p^{-1}\log B)^d\min\{B,Z^p\}
\]

is valid both below and above the threshold `Z^p=B`, and by continuity
at `Z=infinity`. This controls all additional logarithms of conditioning.
A separate universal rational lower bound on positive growth is unnecessary.
Any absolute scale contribution to the recovery depth, such as the
difference between `log(1/g_*)` and `log Z`, is bounded by ordinary input
bits through the rational spectral bounds and is included in `P(L)`.

For `r=nu S/sigma` and `t>=1`, the uniform grid tail gives
`Pr{Z>t}<=r/t+beta`. Integrating the capped nonnegative variable yields

\[
 \mathbb E\min\{B,Z^p\}
 \le1+r\int_1^B t^{-1/p}\,dt+\beta(B-1).
\]

Thus the displayed bounds `2+r` for `k=1` and `2+r log B` for `k=2`
are correct. They include all draws, rather than conditioning on a
successful-growth event. Since `log B=O(m+1)` and sampled encoding lengths
are uniformly polynomial in the base input length, all remaining factors
fit into `(I+1)^K(1+nu S/sigma)`. The separate `k=0` convex branch and the
singleton case are consistent with this bound. A numerical polynomial
bound on `nu S/sigma` remains necessary for the stated polynomial-time
consequence.

The reviewed draft's phrase "least original objective value" was clarified
to "least perturbed objective value `F_xi(x)`". The optimizer throughout
is for the one sampled objective. This is a wording clarification, not
a change to the argument. The small fallback check below belongs in the
note's final verification record.

The initial targeted command `python - <<'PY'` implemented rational
Gaussian elimination and active-subset enumeration with `fractions.Fraction`.
It passed the following five fixtures. Their expected optima were derived
directly, independently of enumeration:

| Fixture | Objective and feasible set | Exact optimum |
| --- | --- | --- |
| Zero objective with a continuum | `0` on `[0,1]^2` | `0` |
| Singular ambient Hessian with an optimal edge | `x_1^2-x_1` on `[0,1]^2` | `-1/4` |
| Lower-dimensional segment | `x_1^2-x_1-x_2^2`, `0<=x_1<=1`, `x_2=0` | `-1/4` |
| Concave endpoint tie | `-x^2` on `[-1,1]` | `-1` |
| Redundant equalities | `x_1`, `x_1=1/3`, `0<=x_2<=1`, with redundant row `2x_1<=2/3` | `1/3` |

The reusable [fallback checker](../new-direction/check_expected_smoothed_qp.py)
preserves those fixtures and reuses the existing diagnostic `FaceQP`
enumerator. The targeted command

```text
python research-20261002/new-direction/check_expected_smoothed_qp.py
```

passed all five fixtures after converting every fixture coefficient to
`Fraction`. The first saved-checker run exposed that the reused diagnostic
oracle expects rational inputs: plain integer rows introduced floating-point
division and failed the redundant-equality case. Explicit conversion now
preserves exact arithmetic, and the checker asserts rational output types.
The checker exercises only exact active-subset
fallback behavior. It does not implement the perturbation tail, spectral
normalization, the production convex-QP algorithm, interleaving, or an
expected-runtime benchmark. The expected-work conclusion is established
by the mathematical argument above. No project-wide verification, CI
inspection, or literature search was performed for this review.

A separate delegated reader checked the complete expected-work note and
found no blocker; its own narrow independent check also approved the cap,
moment calculation, and sampling argument. A targeted inline Python check
passed whitespace, paired math delimiters, and local link targets in this
review and its checker.
