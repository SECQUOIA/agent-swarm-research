# Independent adversarial review of the nonlinear-dynamics extension

Date: 2026-10-02. Verdict: no mathematical blocker found in the complete
[nonlinear-dynamics note](../new-direction/nonlinear-dynamics.md).
This review covers the proof and its stated oracle scope. It makes no
literature or novelty assessment.

The extension works because every repair displacement changes only
`s_1,...,s_T`, and the frozen adjoints make the global adjusted gradient
zero on exactly those coordinates. This is an exact cancellation for
arbitrary repair displacements, rather than a tangent approximation.
Neither interiority nor stationarity of the feasible center is needed.

I independently derived the following steps before reading the complete
draft, then checked their constants and signs against that draft:

- A midpoint Taylor strip of half-thickness `H width(B)^2/4` contains
  every true graph point in its leaf. Every strip point has true equality
  residual at most `(H/2) width(B)^2`. The local domain is a compact
  polytope, so the original convex objective lower model still gives a
  convex local optimization problem.
- The forward recursion gives
  `||R(x)-x||_2<=||q(x)||_2/(1-a)`. Combining copy mismatch and strip
  residual gives the stated `rho` and `D`. The `K s0` term is essential
  even when there is no copy mismatch.
- The backward adjoint signs are correct for `q_t=s_(t+1)-phi_t`.
  The bound `U=G/(1-a)` is uniform in the horizon. Multipliers are frozen
  while differentiating the adjusted bag functions.
- The configuration identity includes the necessary term
  `-sum_t mu_t q_t(z^t)`. Its absolute contribution is at most `UK Q`.
  The adjusted gradient bound `Mbar=M+UH`, the resulting `B0`, the three
  restrictions on `theta`, and the displayed contraction and stopping
  constants follow with the stated signs and coefficients.
- Leaf-dependent strips and infeasibility flags preserve the true
  feasible configurations, including the optimizer. Therefore `LB<=f*`
  remains valid. A finite local state need only satisfy the strip; the
  forward repair supplies exact global feasibility.
- Strips do not change the shell incidence count. The displayed box and
  convex-oracle counts inherit the original count without additional
  nonlinear optimization calls.

For the final example `phi(s,u)=s/4+u/2+s^2/8`, direct calculation gives
the exact image `[-5/8,7/8]`, `a=b=1/2`, `H=1/4`, `U=4`, `Mbar=3`,
`Lq=sqrt(3/2)`, and `rho=13/2`. The objective has feasible quadratic
growth with `g=3/4`, and its reduced final-control second derivative at
`15/16` is `-35/256`. Thus the example has nonlinear equalities and a
nonconvex reduced objective with constants independent of the horizon.

The theorem's limits are material and correctly stated. Strip validity
requires a supplied valid curvature bound or certified enclosure. The
multiplier bound introduces a first-derivative parameter. Whole-box
invariance is a promise, additional terminal or state constraints are
outside the theorem, and controls are continuous. The exact-real model
does not establish polynomial bit complexity: the note's example
`s_t=2^(-(3*2^t-2))` correctly exhibits exponential explicit denominator
length despite stable dynamics.

The targeted command actually run for the final example was:

```text
python3 research-20261002/new-direction/check_nonlinear_dynamics.py
```

It passed 200 exact-rational configurations at horizons `1,2,3,4,6`.
The checks cover leaf and strip membership, quadratic graph residuals,
sampled repair box preservation, adjoint bounds and state cancellation,
the exact adjusted telescoping identity, and the stable repair bound.
There were 632 nonzero local graph residuals and 439 nonzero separator
copy mismatches; every telescoping residual was exactly zero. The
saved report is
[`check_nonlinear_dynamics.json`](../new-direction/check_nonlinear_dynamics.json).

Before the final example was selected, an inline `python3 - <<'PY'`
check passed another 200 exact-rational configurations at the same
horizons for the different variant `phi(s,u)=s/4+u/4+s^2/8`. It checked
the strip residual, repair box preservation, adjoints, exact telescoping
identity, and repair residual bound. That earlier run does not verify
the final example's `u/2` coefficient; the saved targeted script above
does.

These configuration checks support the algebra. They do not execute the
full dynamic program or replace the analytic proof. No project-wide
verification, CI inspection, or literature search was performed.
