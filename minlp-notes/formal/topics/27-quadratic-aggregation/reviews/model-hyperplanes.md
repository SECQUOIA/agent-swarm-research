# Model and hyperplane review

Date: 2026-09-22. Reviewer: the agent that implemented `EasyDirection.lean`;
the four modules reviewed here were implemented by other agents.

No correctness or source-fidelity issue was found in `Model.lean`,
`DefinitionsSequence.lean`, `Recession.lean`, or `Hyperplanes.lean`.
The review compared their definitions and conclusions with Sections 1–3 of
`results/quadratic-aggregation-trivial-hull-certificate.md` and the setting in
`paper-quadratic-aggregation/sections/01-setting.tex`. It does not constitute
an independent literature or novelty review.

## Definition fidelity

- `System` uses arbitrary real symmetric matrices, real linear coefficients,
  and real constants. `eval` and `homEval` retain the factor of two on the
  linear term and the square on the homogenizing coordinate. `feasible`
  requires strict negativity of every constraint. No definiteness or
  feasibility assumption is built into the data.
- `HHC` requires convexity of the homogeneous image of the kernel of every
  nonzero real linear functional. In finite-dimensional real vector spaces,
  those kernels are exactly the linear hyperplanes of codimension one.
  This includes the hyperplane at infinity and all sweeping hyperplanes;
  it does not replace HHC by convexity of the full homogeneous image.
  This identification with codimension-one subspaces is a mathematical
  interpretation of the definition, not an additional named Lean theorem.
- `AsymptoticHC` uses arbitrarily large real levels for each nonzero normal.
  `asymptoticHC_iff_sequence` proves equivalence to the source's strictly
  increasing sequence of good levels tending to positive infinity. The
  construction forces the kth level to exceed k, so strict increase alone
  is not mistaken for divergence. Normals and their sequences have the
  same quantifier order as the source.
- `Certificate` requires nonnegative nonzero weights, positive semidefinite
  aggregate quadratic part, and a nonzero aggregate quadratic or linear
  part. A negative constant aggregate alone is not a certificate.

## Geometric reductions

The recession lemma proves that a common strictly negative leading direction
forces the full convex hull. It uses continuity of all finitely many
homogeneous constraints, dehomogenizes two points, and verifies that their
midpoint is an arbitrary target. It does not assume HHC or strict feasibility.

The support lemma separates a point outside the open convex hull. Strict
feasibility is used to prove that the supporting normal is nonzero. The
hyperplane exclusion lemma treats the zero homogenizing coordinate by the
recession result and treats either sign of a nonzero coordinate by the
square-factor dehomogenization identity.

The orthant separation lemma proves both nonnegativity and nonzeroness of the
weights before normalizing their sum to one. Its conclusion is global
nonnegativity of the weighted image on the hyperplane, not merely a bound
at selected points. Substitution of `(x, α·x/s)` produces exactly the
restricted quadratic inequality used later. `exists_unbounded_certificates`
chooses levels above the requested threshold, the support threshold, and
zero; its denominator and positive-level requirements are justified.

All reviewed statements quantify over arbitrary natural `n` and `m`.
No unnecessary `n ≥ 1`, `m ≥ 1`, or `n ≥ 3` restriction was added. At `m = 0`,
strict feasibility is the whole ambient space and the separator hypotheses
cannot hold. At `n = 0`, a nonempty feasible set cannot have a proper convex
hull. These degenerate cases are handled by the stated hypotheses rather
than excluded silently.

## Targeted verification

The following commands passed locally:

```text
lake build Formal.QuadraticAggregation.Model Formal.QuadraticAggregation.DefinitionsSequence Formal.QuadraticAggregation.Recession Formal.QuadraticAggregation.Hyperplanes
lake env lean topics/27-quadratic-aggregation/verification/ReviewModelHyperplanes.lean
```

The second command checks representative theorem applications with unrestricted
natural dimensions and prints the axioms of all eight principal geometric
and definition-equivalence results. Its captured output is
`verification/review-model-hyperplanes.log`; the only reported axioms are
`propext`, `Classical.choice`, and `Quot.sound`.

No project-wide verification was run, and no CI status or logs were inspected.
This review covers the model, recession argument, and hyperplane reductions;
it does not review the coefficient-cone compactness or limiting contradiction.
