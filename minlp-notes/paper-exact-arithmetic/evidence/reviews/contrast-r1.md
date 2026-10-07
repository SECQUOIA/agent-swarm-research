# Independent review of the quadratic contrasts and boundaries

Date: 2026-10-05. This is an internal proof review of the actual completed
Appendices J and K, refreshed after the contrast author's completion notice
and checked against `evidence/authoring/contrast.md`. It covers Q1–Q12,
including the newly requested feasible-point output consequence, and K's
degeneracy, nullvector, uncertainty and penalty boundaries. Q13–Q14 remain
outside this arithmetic comparison scope under DECISIONS D3.

The local arguments are sound after the repairs below. One theorem statement
is false as currently quantified. Its later uses already satisfy the missing
condition, so the output lower bounds do not need to be removed. Imported
contracts remain a separate source gate: this report does not accept them
merely because their internal applications are consistent.

## Findings that require repair

**Medium — arbitrary weights in `thm:qc-blocks`(d), J:1519–1534 and
1571–1578.** Part (b) allows arbitrary positive rational weights, while (d)
assumes only \(\omega_k\ge1\). Its proof uses both
\(\omega_i\ge1\) and \(\omega_i\le\omega_k\). The preservation claim is
false without these conditions. Take two valid blocks, put \(\omega_2=1\),
and choose a positive rational \(\omega_1\) large enough that
\(\eta\omega_1\lambda_1>\lambda_2\). The prescribed
\(\eta=1/(4\bar\gamma)\) is independent of \(\omega_1\). At the old
optimizer both new rows are active, and stationarity uniquely requires

\[
 \begin{pmatrix}1&\eta\\\eta&1\end{pmatrix}
 \begin{pmatrix}\mu_1\\\mu_2\end{pmatrix}
 =\begin{pmatrix}\omega_1\lambda_1\\\lambda_2\end{pmatrix},
 \qquad
 \mu_2=\frac{\lambda_2-\eta\omega_1\lambda_1}{1-\eta^2}<0.
\]

The two active gradients are independent because the block optimizers are
nonzero and the displayed matrix is invertible. The new system has Slater's
point zero. Convex KKT necessity therefore excludes the old optimizer.
Minimal repair: begin (d) with “With the weights of (c), let …”, or require
\(1\le\omega_i\le\omega_k\) for every \(i\). All later constructions
already use (c).

**Low — rational approximation parameters and empty rows in
`thm:qc-number-field-qp`, J:2548–2555, 2593–2598 and 2604–2607.** Choose
positive rational upper bounds of polynomial length for the Hoffman
constants, \(U\), and the Lipschitz bound before forming the rational
\(\delta,\varepsilon\). In the final precision formula replace
\(\max_\iota\|C_\iota\|_1\) by
\(K_C=\max(\{1\}\cup\{\|C_\iota\|_1\})\). The present denominator is
zero or undefined for all-zero or empty \(C\); those cases are allowed by
the theorem. The chart, norm-penalty and active-set arguments otherwise
reconstruct correctly.

**Medium — the eliminated object in K:483–485.** A fractional penalty
\(\mathcal R^{2^{-\mathfrak p(L)}}\) is not a polynomial. Eliminating
intermediate chain variables while retaining \(s_0\) produces the polynomial
inequalities \(H_Vs_0^{2^{\mathfrak p(L)}}\ge\pm r_i(x)\), one for each
signed residual. Eliminating \(s_0\) gives the fractional objective. Replace
“the eliminated penalty is a polynomial” with the high-degree-constraint
statement already used at K:449. The explicit lift has degree two and is
nonconvex.

**Medium source-contract correction — missing degree floor in K:363–374.**
The printed coefficient bound cannot hold literally at
\(\mathfrak d=1\). Quantify
\(z_1=2x,\ z_i=2z_{i-1},\ z_k\ge1\). The projected set is
\(x\ge2^{-k}\); its boundary requires a linear integer polynomial divisible
by \(2^kx-1\), despite constant input coefficient heights. Specify
\(\mathfrak d\ge2\), or use \(\max\{2,\mathfrak d\}\), according to
the vetted source. The root-penalty application uses degree two already.

**Low — uncertainty and regularization scope, K:14–16, 28–29 and
161–164.** Singular equalities can prevent accurate objective upper bounds
from uncertain data; the examples do not preclude every form of
certification. They explicitly allow robust root existence. Replace bare
“minimized approximately” with the vetted objective-gap/value approximation
contract. The regularization paragraph should refer to nonzero optimal
comparison gaps and say that choosing \(\varepsilon\) from the uniform
separation bound can require exponentially many printed bits, rather than
asserting this necessity for every instance or arbitrary function values.

**Low — literal small cases in K.** At K:320–321, give the bag
\(\{x,y_1\}\) for \(k=1\). State positive chain length in the penalty
limits, choose an integer-valued \(\mathfrak p(L)\ge1\), and replace
rational bounds on integer coordinates by their inward integral ceiling and
floor before binary expansion at K:397–400. These are short qualifications;
they do not change the intended results.

## Encoding and integration checks

J:96–98 explicitly defines native dense matrix input. Under that contract,
the printed lengths for the block and singleton constructions are correct.
For the global polynomial format with full \(n\)-component exponent vectors,
the new feasible-point construction has the safe bound

\[
 L_{\rm exp}=O\!\left(k^3d^2[\log(kd\varpi_k)+kd]\right).
\]

For fixed \(k\), this is \(O_k(d^3+d^2\log d)\), and choosing
\(k>3C\) gives the same obstruction to \(\phi(3k)L^C\) output time.
Similarly the optimization-block proof can use a polynomially larger input
bound and a correspondingly larger fixed \(k\). State explicitly which
encoding supplies the sharper printed lengths; the conclusion is robust in
both formats.

J:131–143 and 1705–1717 now correctly separate scalar degree from joint
field degree, coordinatewise output from common-field output, minimal
polynomial support from other equations, and rational circuits from circuits
with root-selection gates. The interface in Section 06:116–118 still calls
an irrational coordinate's alternative a “shared arithmetic circuit” without
that qualification; the root has commissioned its wording repair. Numerical
distance outputs and rational rectangular certificates remain different
formats under Sections 01 and 02. No large-degree or long-coefficient
argument here proves a decision or approximation lower bound.

## Reconstructed proof coverage

| Coverage | Independent local assessment |
| --- | --- |
| Q1 | Reduced-numerator tangency proof, common-kernel branch, rational face restriction, two-ray epigraph lift, rational density/hull and constructive fixed-margin bisection check. The objective Hessian is omitted from the constraint parameter and explicitly included in the rational-optimal-face corollary. Span three and the three full ellipsoids check. |
| Q2, Q11 | Active affine differences compress the polynomial span. Minimal KKT support has at most \(\min(k,d)\) independent gradients. One parameter identity applies at exceptional regular roots; the two ordered limits preserve it. The common support supports the joint-field conclusion. Multihomogeneous count, local-norm deformation and height/separation calculations check, conditional on their stated external tools. Sharpness uses the generic count and Hilbert irreducibility as separate source contracts. |
| Q3 | Block Eisenstein valuation, larger-prime splitting, compositum degree, primitive weighted value, actual-coordinate shear and coefficient-support translation check. The weight-scope defect above is local. Common field and actual-coordinate lower bounds are distinguished. |
| Q3 feasible parallel | Prime-degree Kummer rotations and the norm argument prove degree \(d^k\) and primitive nonzero rational weighted sums. No unramified-extension Eisenstein argument is needed. The projected binomial form has logarithmic coefficient bits, three independent Hessians, and positive definite restrictions at the triangle vertices. Positive row mixing gives full-dimensional ellipsoids of span exactly \(3k\). The shear puts the primitive sum in an actual input coordinate; the positive-half-plane translation proves every minimal-polynomial coefficient is nonzero. |
| Q4 | One quartic row has the stated unique minimizer, strict feasible point, curvature and degree \(3^n\). Its row/Hessian-field parameter is distinguished from coefficient-matrix span and the quadratic lift. |
| Q5 | Tangent rows, complementarity, exposing identities and final quadratic identity preserve every feasible point and certify global optimality. Each curved restriction drops the restricted Hessian span. Minimal-support multipliers lie in \(\Q(p)\); height then power-basis encoding has the claimed size. The verifier does not certify canonical selection. No rational unweighted-SOS claim is made. |
| Q6, Q8 | Common-kernel removal makes the scalar determinant nonzero with only real roots. Singleton isolation forces the square of the minimal polynomial to divide it, giving minimum size \(2d\). The trace-form construction forces the entire feasible set to be the singleton. For corank one, normalized kernel coordinates generate the field; every real embedding fixes them using the original PSD matrix. The planar converse proves whole-set uniqueness. |
| Q7 | Pell divisibility and growth prove the stated classical expanded integer-output boundary. The proof distinguishes coefficient length, circuit representation, nonconvexity and feasibility decision. |
| Q9 | Rational charts and pseudoinverses put the selected optimizer in the input field. Supplied dense degree and power-basis heights control field separation. Hoffman estimates, outward rounding, norm selection, phase-I feasibility, boundedness classification and active-row reconstruction check after the small parameter/empty-row repairs above. |
| Q10 | Epigraph attainment is an external gate. Given it, a sparse algebraic aggregate and rounding inside the exact rational kernel-orthogonality equations retain a positive margin and give a rational certificate. The three support/margin/weight lower examples check and remain format-specific. |
| Q12 | Recognition candidates separate embeddings. Norm polynomials, rather than sample minimal polynomials, interpolate correctly when a sample is nonprimitive. Differentiation recovers coordinate maps. The minimum-norm feasible-point approximation oracle uses one fixed tuple and does not assume an exact oracle for every nonzero objective. |
| K | Fully zero Hessian gives precisely the rational affine system \(D^3f(x)=0\). The Newton discontinuity, extrapolated leading term \(5t/8\), irrational-kernel Schur bound, selected/common/maximal-rank kernel distinction, fixed-gap uncertainty and robust-root degree/precision argument check. Conditional on the effective source contracts, the algebraic-value-free interval construction, root exponent, interpolation bound and exact nonconvex quadratic lift check. |

## Source gate and readiness

The author's report lists Appendix J/K contracts as unverified by Luna.
This review requested exact checks through the root; it did not browse or
research sources. Before accepting the appendix, obtain the vetted contracts
for multihomogeneous isolated-root counting with extra components; the
Nie–Ranestad generic quadratic count; Hilbert irreducibility in density
form; convex KKT with affine rows and strict nonlinear rows; exact rational
QP/LP; Frank–Wolfe and Luo–Zhang attainment; the exact KLL recognition
threshold; univariate exact arithmetic; real-algebraic transfer;
prime-distribution, Eisenstein/ramification/Hensel facts; Weil-height
conventions; Brouwer degree; and the two Basu–Mohammad-Nezhad effective
bounds. In the latter, confirm the degree floor, coefficient assumptions,
formula-size dependence and graph-variable accounting. K's Slot–Steurer–
Wiedmer comparison must retain the already vetted objective-gap contract.
Attribution-only references are also subject to the separate literature audit.

Readiness is conditional: repair the false weight quantifier and the listed
local model/wording issues, then close the source gate. No unresolved internal
main proof gap was found. This is not a result-acceptance verdict.

Verification was analytical and document-scoped. Targeted reads used `cat`,
`rg`, `nl` and `sed` on J/K, their author report, BRIEF/DECISIONS, the prewrite
reviews, literature report, and Sections 01/02/03/06/07. Independent delegated
reviews checked K, the singleton constructions, and blocks/QP/Pell. No
mathematical scripts, experiments, historical checks, compilation,
project-wide verification or CI inspection were run by this review. The only
post-write command was a text-format check of this owned Markdown review,
recorded below.

```text
python - <<'PY'
from pathlib import Path
p = Path('paper-exact-arithmetic/evidence/reviews/contrast-r1.md')
s = p.read_text()
assert s.endswith('\n')
assert all(line == line.rstrip() for line in s.splitlines())
assert all(ord(c) >= 32 or c in '\n\t' for c in s)
print('contrast-r1.md: newline, whitespace and control-character checks passed')
PY
```
