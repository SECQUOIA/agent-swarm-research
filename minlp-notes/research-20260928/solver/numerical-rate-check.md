# Targeted numerical checks of the two sparse rate examples

Date: 2026-09-28. These calculations check definitions, signs, degree
conventions, and the observed size of the gaps in
[quadratic sharpness](quadratic-sharpness.md) and
[the affine recourse boundary](affine-recourse-rate-boundary.md).
They provide numerical evidence, not additional rate theorems, certified
SDP bounds, or solver speedup claims.

Both dense order-two SDPs return values close to the proved optimum zero.
The sparse SDPs return negative values. The quadratic example is numerically
consistent with its inverse-square gap; the affine example has the much
slower inverse-order pattern. Ordinary quadratic modules and full
preorderings give nearly identical values in many tested cases. That
observation does not extend the proved preordering rate theorems to
ordinary modules.

## Formulation and independent assembly

The reproducible implementation is
[check_numerical_rates.py](check_numerical_rates.py). Main results are in
[numerical-rate-results.json](numerical-rate-results.json); an order-two
check with a second SDP solver is in
[numerical-rate-scs-crosscheck.json](numerical-rate-scs-crosscheck.json).
The implementation was assembled separately from the proof-check scripts.

For the quadratic example, substitute `x=(u+1)/2`, `z=(v+1)/2` into

\[
f=x^2-2xy+y^2+z^2+2yz.
\]

The bags are `(u,y)` and `(y,v)`, each on `[-1,1]^2`. Their objective
polynomials are, respectively,

\[
\tfrac14u^2+\tfrac12u+\tfrac14-uy-y,
\qquad
y^2+\tfrac14v^2+\tfrac12v+\tfrac14+yv+y.
\]

Each bag uses its two quadratic box generators. For the affine example,
the bags are `(x,y)` and `(y,v)`, with `z=(v+1)/2`, objective `-xy+z`,
and generator lists

\[
 (1-x^2,1-y^2),\qquad
 (1-y^2,\tfrac{1+v}{2},\tfrac{1-v}{2},
                  \tfrac{1+v}{2}-y,\tfrac{1+v}{2}+y).
\]

These are exactly the affine changes of the generator lists in the
theoretical notes. An independent review caught an earlier use of
`1-v^2` in place of the two linear endpoint generators for the affine
example. Although the feasible set is unchanged, the truncated cones can
change. The implementation was corrected, independently rechecked, and
the reported results rerun with the displayed lists.

An order-`r` local moment vector contains all monomials of total degree
at most `2r`. For a generator product `g`, its localizing matrix uses
monomials of total degree at most `floor((2r-deg(g))/2)`. The ordinary
quadratic module includes `g=1` and each individual generator. The full
preordering includes every squarefree generator product whose degree is
at most `2r`. Each local law has mass one; shared moments of `y` agree
through degree `2r`. Dense models use one moment vector and the union of
the generator lists. All SDP matrices use a monomial basis.

Exact rational checks verify the transformed objective polynomials,
the dense certificate identities, normalization and separator rows, and
7,831 entries of localizing maps evaluated at rational Dirac moments.
These checks cover orders two and three for both examples, both local
cone choices, and sparse and dense assembly. They validate those finite
instances of the implementation, not an all-order theorem.

The [independent review](numerical-rate-review.md) rechecked the assembly
and dual diagnostic signs. It also independently compared a finite-grid
measure LP with the approximation LP, confirming the factor two to
floating-point accuracy.

## SDP and approximation results

The tables report **gap estimates**, the negative of the returned sparse
primal objective. The exact minimum is zero. `Grid ideal` is twice the
best approximation error returned by a finite-grid LP of degree `2r`.
The proved inequalities apply to the exact mathematical relaxations;
they are not inferred from solver values.

For the quadratic example, the separator target is `h(y)=(max(y,0))^2`.
The rigorous lower bound is

\[
 -\rho_r\ge \frac{2}{27\pi(2r+2)^2}.
\]

| Order `r` | Preordering gap estimate | Module gap estimate | Grid ideal `2E_{2r}(h)` estimate | Proved lower bound, rounded |
|---:|---:|---:|---:|---:|
| 2 | 0.027634589 | 0.027634589 | 0.027634558 | 0.000654959 |
| 3 | 0.010635448 | 0.010635450 | 0.010635465 | 0.000368414 |
| 4 | 0.005549265 | 0.005549379 | 0.005549375 | 0.000235785 |
| 5 | 0.003390347 | 0.003390518 | 0.003390731 | 0.000163740 |
| 6 | 0.002281468 | 0.002281712 | 0.002281799 | 0.000120299 |

Dense order two returns `7.42e-11`. Its exactness is established by
the explicit polynomial certificate, not by this near-zero value.
Both sparse cones track the ideal local-measure gap closely. Exact
equality with `-2E_{2r}(h)` would be a stronger finite-order statement;
these computations do not establish it. In particular, approximate
SDP infeasibility and LP grid error can reverse the theoretical ordering
between an SDP value and the exact local-measure value.

For the affine example, the separator target is `|y|`. The rigorous
preordering gap lower bound is

\[
 -\rho_r\ge \frac{1}{9\pi(r+1)}.
\]

| Order `r` | Preordering gap estimate | Module gap estimate | Grid ideal `2E_{2r}(|y|)` estimate | Proved lower bound, rounded |
|---:|---:|---:|---:|---:|
| 2 | 0.135241798 | 0.139467359 | 0.135241758 | 0.011789255 |
| 3 | 0.091858110 | 0.091858122 | 0.091857969 | 0.008841941 |
| 4 | 0.069379400 | 0.069379491 | 0.069379273 | 0.007073553 |
| 5 | 0.055690342 | 0.055692747 | 0.055690143 | 0.005894628 |
| 6 | 0.046499698 | 0.046517571 | 0.046494624 | 0.005052538 |

Dense order two returns `4.27e-9`. At sparse order two the ordinary
module is visibly weaker than the preordering. SCS independently returns
gap estimates `0.139467359` and `0.135241803`, respectively. The larger
order differences are much smaller and affected by conditioning; no
claim about their exact size is made.

## What the approximation LP establishes

For each target and degree `n`, the LP minimizes `e` subject to
`-e <= target(y_i)-p(y_i) <= e` on 4,001 cosine-spaced nodes. The
polynomial uses a Chebyshev basis. Its returned coefficients are saved
and evaluated on 40,001 nodes for a separate diagnostic. Even an exact
solution of the fitting LP would give only a lower bound on the true
uniform approximation error. The actual solve uses floating-point
arithmetic, so the returned number is not a certified lower bound.
Likewise, the validation grid does not bound an error peak between its
nodes and does not certify an upper bound.

The following scaled values come only from the grid LPs, with `r=n/2`.
They show the distinct observed exponents more clearly than the raw
values do.

| Degree `n` | Quadratic target: `r^2 (2E_n)` estimate | Affine target: `r (2E_n)` estimate |
|---:|---:|---:|
| 4 | 0.110538233 | 0.270483516 |
| 8 | 0.088789993 | 0.277517093 |
| 12 | 0.082144781 | 0.278967742 |
| 16 | 0.078931501 | 0.279483702 |
| 24 | 0.075797412 | 0.279861705 |
| 32 | 0.074255542 | 0.279994839 |

These finite data neither prove the limiting constants nor independently
prove either asymptotic rate. The theoretical notes establish the rates.

## Accuracy limits and verification record

CLARABEL was asked for absolute gap, relative gap, and feasibility
tolerances `1e-9`. Every quadratic solve of order three or greater was
reported `optimal_inaccurate`. For the affine example, all preordering
solves, including the dense solve, and ordinary-module solves of order
four or greater had that status. There were no solver exceptions. The
status and diagnostics for every solve are retained in the JSON.

The largest absolute dual stationarity residuals were about `3.0e-7`
for the quadratic example and `1.2e-6` for the affine example. Localizing
matrices had minimum eigenvalues as low as `-8.2e-8` and `-1.9e-7`,
respectively. Some returned primal objectives were smaller than returned
dual objectives, including the affine module at orders five and six.
These are numerical feasibility failures, not violations of mathematical
weak duality. A small reported primal-dual gap alone cannot certify
either objective. No rounding or interval procedure converted these
outputs to exact feasible primal or dual points.

The SCS order-two check corroborates the signs and the substantial
affine cone difference. It is a second floating-point solve of the
same assembled SDP, not an independent proof of the formulation or its
optimal value. No higher-order reruns were pursued because the intended
sanity checks and conditioning limits were already clear.

Targeted commands run for the final formulation:

```sh
python -B research-20260928/solver/check_numerical_rates.py --check-only
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research-20260928/solver/check_numerical_rates.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research-20260928/solver/check_numerical_rates.py --orders 2 --solver SCS --lp-degrees 4 --output research-20260928/solver/numerical-rate-scs-crosscheck.json
```

The exact checks passed. Both numerical experiment commands completed.
The environment used Python 3.13.11, NumPy 2.5.1, SciPy 1.18.0, CVXPY
1.9.3, and SymPy 1.14.0; solver timings in the JSON are incidental and
are not benchmark claims. Only installed packages were used. No
project-wide verification, CI inspection, or Lean formalization was
performed for this numerical assessment.
