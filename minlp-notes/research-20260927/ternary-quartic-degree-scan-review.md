# Independent review of the finite ternary power-embedding scan

Date: 2026-09-28. Status: the stated finite exclusion passes independent
proof and code review. It does not establish a general degree bound.

I read [the scan note](ternary-quartic-degree-scan.md), inspected the
complete [script](scan_ternary_quartic_degree.py), and ran its retained
exact verifier:

```text
python research-20260927/scan_ternary_quartic_degree.py --verify
```

It passed all 196 cases: 186 forced missing pure-quartic coefficients,
two forced zeros at the origin, and eight positive definite rational
dual annihilators. The verifier recomputes the rational kernels and
checks the exact identities and factorization signs; it does not rerun
the numerical solver.

The first-jet coefficient map has the correct powers and factors. For
a monomial with exponent vector \(b\), evaluation has exponent
\(b\cdot e\), and its \(i\)-th derivative has coefficient
\(b_i\) and exponent \(b\cdot e-e_i\). Reduction by
\(\alpha^d=2\) is exact. Eisenstein irreducibility makes the rational
coefficient equations equivalent to first-order vanishing at the selected
point, rather than merely formal quotient equations. Extending their
rational kernel to a real span in the subsequent Gram feasibility test
only relaxes the necessary conditions and cannot invalidate an exclusion
for rational polynomials.

The missing-coefficient obstruction is correct because the coefficient
of \(x_i^2v_i^2\) in the Hessian biform is twelve times the coefficient
of \(x_i^4\), and only the square of the corresponding Hessian-basis
monomial produces that term. A positive definite Gram requires its
diagonal entry to be positive. The origin obstruction uses all its
hypotheses: the point is nonzero, its gradient vanishes, and strict
Hessian positivity would make it the unique minimizer.

The Hessian coefficient map correctly doubles off-diagonal directional
terms. The Gram coefficient map uses all ordered pairs of basis entries,
so its adjoint has entries equal to the multiplier on the corresponding
product monomial. Consequently a rational multiplier annihilating the
entire Hessian coefficient space satisfies

\[
 \lambda^{\mathsf T}\Gamma(M)=\operatorname{tr}(ZM)=0.
\]

The exact verifier checks that \(Z\) is symmetric positive definite.
For nonzero \(M\succeq0\), the trace is strictly positive, yielding
the claimed contradiction. No numerical infeasibility result is used as
a proof. The saved numerical margins and projection procedure explain
discovery only.

The code verifies that the record list equals the full intended set of
196 distinct exponent triples. Reducing integer exponents modulo \(d\)
and applying nonzero rational coordinate scalings correctly extends the
conclusion to distinct nonzero residues, including negative exponents.
It does not cover other number fields, arbitrary power combinations, or
all three-variable quartics.

The conclusion is therefore a verified negative result for this finite
family. It does not conflict with the degree-five
[ternary counterexample](ternary-rational-sos-convex-counterexample.md).
No project-wide verification, numerical optimization rerun, Lean proof,
or CI inspection was performed for this review.
