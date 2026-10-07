# Independent review of circuit representations of interior Grams

Date: 2026-10-03. **Result: passed.**

I read [the complete corollary](circuit-interior-gram.md), reconstructed
the Taylor Gram formula, and checked its use of the separately reviewed
[general-degree upper bound](strong-convex-polynomial-posslp-upper.md).
No mathematical correction is required. Publication priority is not
established by this review.

The degree-six observable
\(h=f-\|\nabla f\|^2/(2\mu)\) has polynomial explicit encoding
length: differentiating the quartic and multiplying its explicitly listed
terms require only polynomially many rational operations and monomials.
The derived rational \(\mu\) also has polynomial bit length. These data
therefore satisfy the upper theorem's charged input convention. Its shared
Newton circuit gives an exact rational vector \(q\), even when the expanded
fractions are very long. At the minimizer, \(h(p)=f(p)\); separation and
the \(g/8\) approximation error imply \(h(q)>0\) whenever \(f(p)>0\).
Constructing the Newton circuit does not query that sign.

The certificate \(A\succeq\mu I\) gives
\(\bar A\succeq\mu\operatorname{diag}(0,I)\). For every rational
\(q\), Taylor integration with
\((d,(q+td)\otimes d)=U+tV\) has coefficients
\(1/2\), \(1/3\), and \(1/12\) on its constant, cross, and
quadratic terms. These agree with the displayed two-square decomposition.
Completing the linear gradient term contributes exactly
\(\mu\|d+b/\mu\|^2/2+c\). Thus the polynomial identity is exact
on every valid input, independently of the sign of \(c\).

All Newton divisors are nonzero because the Hessians remain positive
definite. After Newton, only the positive rational \(\mu\) and fixed
nonzero rational constants are used as divisors. A zero or negative
minimum therefore does not invalidate circuit construction.

When \(c>0\), the Gram dominates positive multiples of the coefficient
outer products of every \(d_id_j\), every \(d_i+b_i/\mu\), and the
constant polynomial. Their coefficient rows span the entire space of
quadratics, including lower-degree terms. This proves positive definiteness
of the ordinary Gram. This step uses the **full strict quartic Hessian
basis** and does not extend automatically to arbitrary listed Hessian
monomials. Conversely, when \(\min f\le0\), a positive definite ordinary
Gram would give a positive value at every point because its monomial
vector contains one. The attained minimum contradicts this. The claimed
behavior on all valid inputs is therefore correct.

The coefficient matrices and their products have polynomial dimensions.
Keeping shared references to the circuit for \(q\) makes their total
construction size polynomial. This proves a compact representation result;
it does not prove efficient expansion, ordinary-bit exact validation, or
a short unweighted rational SOS circuit. The source correctly keeps these
claims separate.

I also ran a targeted inline Python/SymPy exact check for
\(f=(x^2+y^2)^2+x^2+y^2+C\), with \(C=-1,0,1\), two rational centers,
and a full rational strict Hessian Gram. All six translated identities
passed, the displayed factors had full coefficient rank, the positive
\(c\) case gave a positive definite matrix, and the zero/negative-minimum
cases had the required obstruction in the constant diagonal entry. These
finite checks support the formulas; the arguments above cover all inputs.
No project-wide verification or CI inspection was performed.
