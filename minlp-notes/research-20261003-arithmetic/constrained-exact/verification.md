# Verification of constrained exact-arithmetic extensions

Date: 2026-10-03. This records topic-specific proof review and commands.
No project-wide verification or CI inspection was performed.

## Results and review scope

- [theorem.md](theorem.md): ordinary deterministic fixed-parameter exact
  comparison in nonlinear dimension, arbitrary rational linear constraints,
  full active-set recovery, and the mixed-integer consequence. The separate
  [independent review](independent-review.md) reconstructs the elimination,
  coefficient bounds, separation, approximation, and parameter composition.
- [structural-newton.md](structural-newton.md): conditional transfer from
  exact arithmetic QP subroutines and its box specializations for forest or
  Stieltjes Hessians. The [independent review](review-structural-newton.md)
  checks the source algorithm and circuit interface, as well as mathematical
  convergence and exact signs.
- [network-flow.md](network-flow.md): the separable capacitated-flow
  specialization using Végh's exact quadratic-flow algorithm. Its
  [independent review](network-flow-review.md) checks the arithmetic model,
  graph transformations, and nonlinear composition.
- [general-boundary.md](general-boundary.md): what remains unresolved for
  arbitrary polyhedra and unrestricted Hessians. This is an open boundary,
  not a negative complexity theorem.

The proof reviews are independent internal reconstructions. They are not
external peer review, formal verification, or a publication-priority audit.

## Targeted commands

The lead author ran:

```text
python research-20261003-arithmetic/constrained-exact/check_nonlinear_dimension.py
```

Result: passed eight exact polynomial/translation cases and 40 affine-face
cases, including 18 losses of nonlinear rank and elimination of 30 quadratic
directions. Fifteen exact sign/equality threshold checks also passed. The
checker tests symbolic identities over the rationals, rank extraction,
translations, degenerate face dimensions, and the final threshold logic.
It does not implement the general FPT optimizer or prove its asymptotic bit
complexity.

The flow author ran, and the independent flow reviewer reran:

```text
python3 research-20261003-arithmetic/constrained-exact/check_network_flow.py
```

Result: six cases and 42 exact rational Newton steps passed. These include
zero-multiplier boundary optima and a tiny positive inactive slack. This is
a diagnostic for the nonlinear-to-quadratic interface and the error bound;
it does not implement the general quadratic-flow algorithm.

The box reviewer ran:

```text
python3 research-20261003-arithmetic/constrained-exact/check_structural_newton_review.py
```

Result: 90 bounded-QP KKT checks and 714 principal-submatrix
admissible-vector checks passed, with every observed pivot count at most
twice the dimension. Four exact quartic Newton steps also passed; their
optimizer is an active bound with zero multiplier while the iterates stay
interior. The exact-arithmetic diagnostic is documented in
[its review](review-structural-newton.md). Its finite examples support the
claimed source interface, but the operation bound rests on the source
theorem and proof reconstruction.

## Primary dependencies

The single-block quantifier-elimination coefficient clause was checked
in Basu's survey, Theorem 2.16, printed page 12. Its coefficient bit bound
is linear in the input coefficient bit bound, with parameter-only
multipliers after reducing the number of algebraic variables.

The globally convex approximation guarantee was checked in
Slot--Steurer--Wiedmer, Corollary 1.2 and its proof. It outputs an actually
feasible rational point on a rational polyhedron; the iteration and output
bounds are polynomial in requested accuracy bits. The nonlinear-dimension
algorithm uses FPT-many printed bits. The Newton algorithms use polynomial
printed bits only for initialization and then shared circuits.

The exact box-QP and flow-QP source interfaces are recorded separately in
[primary-sources.md](primary-sources.md), [network-flow.md](network-flow.md),
and the corresponding independent reviews. None of those source results
is represented as a new algorithm developed here.

The lead author also ran a scoped inline Python document check over this
subdirectory: nine Markdown files and 29 local links passed final-newline,
trailing-whitespace, fenced-block, and link-existence checks. The command
`git diff --check -- research-20261003-arithmetic/constrained-exact` returned
success. These are local document checks, not CI results.
