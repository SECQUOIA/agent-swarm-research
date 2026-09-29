# Targeted verification of affine-recourse kernel rounding

Date: 2026-09-28. This record concerns
[affine-recourse-kernel-upper.md](affine-recourse-kernel-upper.md).

## Exact local feasibility and repair check

Command actually run:

```text
python research-20260928/solver/check_affine_recourse_upper.py
```

Result: all assertions passed. The exact SymPy fixture has one shared
variable, two private variables, order `r=2`, and complete recourse fibers
`P(u)={y in [-1,1]^2:y1+y2=1+u}`. Its source shared moments are evaluation
at zero, its private mean is `(1/2,1/2)`, and its private second-moment
matrix is the identity. The joint private moment matrix is positive
semidefinite.

The script checks every local moment and localizing constraint at that
order. Nevertheless `L((y1+y2-1-u)^2)=1`, so the moment functional has no
representing probability law on the feasible set. The fixture therefore
tests a case beyond averaging genuine feasible-point distributions.

For `m=2`, the conditional source mean stays zero while the output is `v`.
The private mean satisfies the source fiber but violates the output fiber
unless `v=0`. Its exact projection is `((1+v)/2,(1+v)/2)` and its squared
movement is `v^2/2`. The integrated source displacement is exactly `5/12`,
the stated sharp intermediate transport constant `V_2`.

With objective `f(u,y)=u(y1+y2)`, the matrix surrogate and original moment
objective both integrate to zero. The repaired objective integrates to
`5/12`. This checks a genuinely positive repair cost. It is not a lower
bound on the relaxation gap: this particular feasible moment objective
need not be optimal.

The script also verifies that the two-node quadrature fails for the
degree-four transport expression while the three-node quadrature is exact.
This independently challenges the need for `N>=m+1` in the finite-grid
theorem. A separate feasible source atom verifies that the full conditional
matrix vanishes at a zero-density endpoint.

## Independent proof audit

A separate agent derived the argument before reading the finished draft,
then read the full draft line by line. Its
[review](affine-recourse-upper-review.md) checks the degree reserve,
repeated shared generators, source-box feasibility, zero-density matrix,
uniform Hoffman repair, continuity of projection, objective inequality,
SDP dimensions, and grid quadrature.

The audit independently sharpened the displacement constant to
`V_m=3(4m-3)/(2m(2m^2+1))` and confirmed its attainment at source zero.
It suggested making zero-density source means explicit and using
`m=ceil(r/s)` for the simpler coarse bound in `r`. Both changes were
checked directly and incorporated.

Its targeted command was:

```text
python research-20260928/solver/check_affine_recourse_transport_review.py
```

The reviewer and the theorem's author both ran the command; all assertions
passed. It checks exact triangular-convolution
identities for `m=2,...,60` and independently expanded monomial/arcsine
integration for `m=2,...,10`. The script is retained in the repository.

## What this verification establishes

The computations establish exact finite-instance constraint feasibility,
algebraic identities, a positive repair cost, and the quadrature boundary.
They do not establish the general theorem, literature priority, numerical
stability, bit complexity, or a matching lower rate for the SDP gap.

The independent review checks the written general argument and finds no
substantive gap. That is evidence, not a formal correctness guarantee.
No Lean formalization, project-wide verification, or CI status/log
inspection was performed for this topic.
