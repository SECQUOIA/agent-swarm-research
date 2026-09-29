# An alternate perturbation proof of low-dimensional algebraic bounds

Date: 2026-09-28. This supporting proof was developed before checking the
shorter direct quantifier-elimination consequence in
[the optimizer witness note](common-range-optimizer-witness.md). Classical
quantifier elimination already proves the claimed encoding bounds, including
finite unattained infima. This alternate proof is preserved as a verification
resource, not as an independent novelty claim.

The use of an unknown box whose boundary is inactive also has a direct
precedent in [Jeronimo, Perrucci and Tsigaridas, Theorem 14](https://arxiv.org/abs/1112.0544).
Their proof uses a box around a compact minimizer set without allowing its
radius to enter the coefficient bound. The ordered regularization below
applies that principle to each positive regularization parameter.

## Low-dimensional polynomial bound

We use the following elementary consequence of generic perturbation and
finite-dimensional elimination.

**Lemma.** Let \(D\subseteq\mathbb R^d\) be nonempty and defined by
\(s\) weak rational polynomial inequalities of degree at most four, and
let \(g\) have degree at most four. Suppose every coefficient has
numerator and denominator bit length at most \(\tau\). If \(g\)
has finite infimum \(\gamma\) on \(D\), then \(\gamma\) has an
integer annihilator of degree at most \(F(d)\) and coefficient bit
length at most

\[
 F(d)(\tau+\log(s+1)+1).                              \tag{6}
\]

If the infimum is attained, some minimum-norm optimizer has coordinate
annihilators and a common rational univariate representation satisfying
the same type of bounds. Increasing the effective function \(F\) is
allowed. A constant number of additional polynomial outputs of bounded
degree can be included. The zero-dimensional case is immediate.

Here and below each polynomial is cleared of denominators separately.
There are only \(\binom{d+4}{4}\) monomials, so this changes \(\tau\)
by a factor depending on \(d\), not on \(s\).

### 1. Regularize and remove unknown box boundaries

Write \(D=\{u:p_i(u)\le0\}\). For \(\varepsilon>0\), minimize

\[
 g(u)+\varepsilon\|u\|^2\quad\hbox{on }D.             \tag{7}
\]

The objective is coercive on \(D\), because \(g\ge\gamma\)
there. It attains a minimum \(\gamma_\varepsilon\), and
\(\gamma_\varepsilon\to\gamma\) as \(\varepsilon\downarrow0\).
For each fixed \(\varepsilon\), all minimizers lie in a finite box:
comparison with any fixed feasible point bounds their norms. Choose an
unknown integer radius \(R_\varepsilon\) that contains all these
minimizers strictly. This radius is used only in a compactness argument and
never enters the polynomial coefficients.

Choose integer polynomials \(P_0,\ldots,P_s\) of degree at most four.
On this box, perturb (7) to

\[
 \begin{split}
 \min\quad&g(u)+\varepsilon\|u\|^2+\eta P_0(u),\\
 p_i(u)-\eta+\eta^2P_i(u)&\le0\quad(1\le i\le s).
 \end{split}                                                   \tag{8}
\]

Every fixed original feasible point satisfies the perturbed rows for small
enough positive \(\eta\). In particular an exact minimizer of (7)
does. Compactness and uniform convergence on the fixed box imply that all
clusters of perturbed minimizers, as \(\eta\downarrow0\), are exact
global minimizers of (7). Every such cluster is box-interior by its choice.
If arbitrarily small \(\eta\) admitted a boundary minimizer, a bounded
subsequence would give a boundary cluster, a contradiction. Hence all box
rows are inactive eventually, at this fixed \(\varepsilon\).

### 2. Genericity with logarithmic dependence on the row count

For each selected subset of at most \(d\) constraint polynomials, generic
degree-four coefficients make their active gradients independent and their
objective KKT system have only nonsingular roots. Generic \(d+1\)
polynomials have no common zero. These statements can be seen directly
from the coefficient incidence spaces: solve constraint constants for the
active equations and objective linear coefficients for stationarity. The
KKT incidence space is irreducible of the same dimension as coefficient
space. Taking selected constraints to be distinct coordinate functions and
the objective to be \(\sum_j u_j^2\) gives a nonsingular bordered
Jacobian. Its projection is dominant and generically finite; in characteristic
zero it is generically etale. The gradient-dependence incidence gives the
constraint discriminant in the same way.

The number of variables and degrees needed for each such incidence and its
bad-set projection depend only on \(d\). Standard elimination bounds
therefore give a nonzero bad-set polynomial of degree at most an effectively
computable function of \(d\). No particular single-exponential estimate
is needed here. There are at most \((s+1)^{d+1}\) relevant subsets.

For each fixed \(\varepsilon\) and \(\eta\ne0\), the coefficients
of \(P_i\) map invertibly onto arbitrary perturbed constraint coefficients,
and those of \(P_0\) onto arbitrary objective coefficients. Thus each
bad-set polynomial remains nonzero in the perturbation coefficients and
formal parameters \((\varepsilon,\eta)\). Choose one nonzero parameter
coefficient from each and avoid their product on an integer grid. This gives
one tuple with coefficient bit lengths at most

\[
 F(d)+O(d\log(s+1)).                                  \tag{9}
\]

After fixing the tuple, exclude the finitely many \(\varepsilon\) that
make a bad polynomial identically zero in \(\eta\), and then the
finitely many bad \(\eta\) for each remaining \(\varepsilon\).
At the resulting minimizers there are at most \(d\) active constraints,
their gradients are independent, and the full bordered KKT Jacobian is
nonsingular. Invertibility of the objective or multiplier Hessian alone is
neither assumed nor needed.

### 3. Eliminate a small full KKT system and take ordered limits

For each admissible \(\varepsilon\), retain a sequence
\(\eta\downarrow0\) with the same active subset; then retain a sequence
\(\varepsilon\downarrow0\) with that same subset. For \(j\le d\)
active rows, the complete KKT system has \(d+j\le2d\) variables
\((u,\lambda)\) and polynomial degree at most four in those variables.
Its coefficients are polynomials in the two formal parameters, with
coefficient norm logarithm bounded by (6). The selected root is nonsingular.

Apply the [finite-quotient elimination lemma](explicit-span-separation.md)
with degree four and at most \(2d\) variables. Its proof is unchanged with
two formal parameters: deform each equation by an auxiliary fifth power,
use the \(5^{d+j}\)-dimensional monomial quotient, form the multiplication
determinant of the desired polynomial output, and extract the lowest
auxiliary-parameter coefficient. The resulting nonzero output relation has
degree at most \(5^{2d}\) and coefficient bits of the form (6).

For the perturbed objective output, first extract the lowest nonzero
\(\eta\)-coefficient and take its finite inner limit
\(\gamma_\varepsilon\). Then extract the lowest nonzero
\(\varepsilon\)-coefficient and use
\(\gamma_\varepsilon\to\gamma\). Coefficient extraction increases
neither degree nor coefficient norm. This proves the finite-infimum part.
It does not require any bounded sequence of primal minimizers as
\(\varepsilon\downarrow0\).

If the original infimum is attained, comparison with a minimum-norm optimizer
\(u^*\) gives \(\|u_\varepsilon\|\le\|u^*\|\) for every exact
regularized minimizer. Extract a common convergent outer subsequence and
apply the same elimination to every coordinate on that subsequence. Its
limit is an optimizer of minimum norm. Each coordinate has degree bounded
by \(5^{2d}\), so the common field degree is at most
\(5^{2d^2}\), a function of \(d\). Elementary primitive-element and
rational-univariate-representation bounds preserve (6) after increasing
\(F\): bounded integer linear combinations separate the finitely many
embeddings, and trace linear algebra expresses every coordinate in the
resulting power basis. Only \(d\) coordinates enter this product bound.
This proves the lemma.
