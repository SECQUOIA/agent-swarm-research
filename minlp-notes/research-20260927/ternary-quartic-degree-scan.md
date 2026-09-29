# A finite exclusion for three-variable quartic zero embeddings

Date: 2026-09-28. Status: exact finite certificates and the finite
exclusion passed independent proof and code review. This is an exploratory negative result,
not the principal rational SOS descent contribution.

For \(d\in\{7,9,11\}\), let \(\alpha\) be the real root of
\(T^d-2\). For every choice

\[
 1\leq e_1<e_2<e_3\leq d-1,
 \qquad p=(\alpha^{e_1},\alpha^{e_2},\alpha^{e_3}),
                                                               \tag{1}
\]

there is no rational quartic \(F\) satisfying
\(F(p)=0\), \(\nabla F(p)=0\), and having a positive definite
Hessian Gram matrix on the full basis \((v,x\otimes v)\).
Here \(x,v\in\mathbb R^3\), so that basis has twelve entries.
The Gram matrix could have real coefficients; the exclusion does not
assume it is rational.

The scan covers exactly 196 embeddings. There were no positive results.
Numerical optimization located eight separating certificates; all eight
were converted to exact rational certificates and checked. The other
188 exclusions follow directly from the rational first-derivative
equations.

## Why this search was useful

The existing rational SOS convex quartic degree bound in three variables
is five; see [the degree audit](quartic-zero-degree-adversarial.md).
Thus a rational SOS-convex quartic singleton of degree at least seven
would both break the rational SOS restriction and extend the known
zero-degree frontier. The simple power embeddings (1) were a small,
structured family in which to seek such a result.

Failure in this family does not establish a general degree bound for
SOS-convex quartics. The defining polynomial and the embedding are
substantial restrictions. Rational linear combinations of powers,
other irreducible polynomials, and higher-degree examples remain outside
the scan. This finite negative result should not be read as a novelty
claim or a complexity result.

## Exact equations before numerical optimization

Write \(F\) in the 35 monomials of total degree at most four. Reduce
the evaluations of each monomial and each of its three first derivatives
modulo \(T^d-2\). This gives a rational matrix \(J\) with \(4d\)
rows and 35 columns. Eisenstein's criterion at two proves irreducibility,
so

\[
 F(p)=0,\ \nabla F(p)=0
 \quad\Longleftrightarrow\quad
 \operatorname{coeff}(F)\in\ker_{\mathbb Q}J.
\]

The right-to-left implication is direct substitution. The reverse uses
linear independence of \(1,\alpha,\ldots,\alpha^{d-1}\) over the
rationals. An exact rational basis \(K\) of this kernel was computed
for every embedding.

Two immediate exclusions were applied:

- If every kernel member has coefficient zero on some \(x_i^4\),
  no full positive definite Hessian Gram matrix exists. Its diagonal
  entry corresponding to the monomial \(x_iv_i\) would have to equal
  twelve times that coefficient, hence would be zero.
- If every kernel member has constant coefficient zero, then
  \(F(0)=F(p)=0\). A full positive definite Hessian Gram matrix implies
  global strong convexity. Together with \(\nabla F(p)=0\), this
  implies \(F(0)>F(p)\), since \(p\ne0\), a contradiction.

The first exclusion accounted for 186 embeddings; the second for two.

## Exact certificates for the remaining eight cases

Let \(H\) map quartic coefficients to the 60 coefficients of
\(v^{\mathsf T}\nabla^2F(x)v\). There are ten monomials of degree
at most two in \(x\) and six monomials of degree two in \(v\).
Let \(\Gamma(M)\) be the coefficient vector of

\[
 (v,x\otimes v)^{\mathsf T}M(v,x\otimes v).
\]

A prospective Hessian Gram matrix must satisfy
\(\Gamma(M)=HKc\) for some real coefficient vector \(c\).

For each of the eight remaining cases, the recorded certificate is a
rational vector \(\lambda\in\mathbb Q^{60}\) satisfying

\[
 (HK)^{\mathsf T}\lambda=0,
 \qquad Z=\Gamma^*(\lambda)\succ0.                 \tag{2}
\]

The second condition was checked by an exact rational
\(LDL^{\mathsf T}\) factorization with twelve positive diagonal
pivots. If a nonzero positive semidefinite \(M\) were feasible, then

\[
 0=\lambda^{\mathsf T}HKc
   =\lambda^{\mathsf T}\Gamma(M)
   =\operatorname{tr}(ZM)>0,
\]

a contradiction. These eight certificates therefore exclude every
nonzero positive semidefinite Hessian Gram matrix, a stronger conclusion
than needed for the search.

Numerical discovery used CLARABEL to maximize a margin \(\delta\)
subject to \(M\succeq\delta I\), \(\operatorname{tr}M=1\), and
the coefficient equations. All eight margins were negative, between
approximately \(-0.0250\) and \(-0.0142\). Those numerical values
alone establish no exclusion. To obtain (2), the numerical dual vector
was rounded to rationals and orthogonally projected onto the exact
rational nullspace of \((HK)^{\mathsf T}\). Exact factorization then
verified positivity of its Gram adjoint.

| Degree | Forced zero pure quartic coefficient | Forced zero at origin | Exact positive definite dual |
|---|---:|---:|---:|
| 7 | 12 | 0 | 8 |
| 9 | 54 | 2 | 0 |
| 11 | 120 | 0 | 0 |

The eight dual-certified exponent triples are
\((1,2,4),(1,2,5),(1,3,6),(1,4,6),(2,3,4),(2,5,6),
(3,4,5),(3,5,6)\), all with degree seven. The two origin exclusions
are \((1,4,7)\) and \((2,5,8)\), both with degree nine.

## Scope and verification

An exponent may be reduced modulo \(d\), since
\(\alpha^{qd+r}=2^q\alpha^r\). Multiplication of each coordinate
by a nonzero rational number, and permutation of coordinates, preserve
the target properties by an invertible rational change of variables.
Consequently the result also covers integer exponent triples whose
residues modulo \(d\) are pairwise distinct and nonzero. This includes
negative exponents. No assertion about repeated or zero residues is
needed for the stated finite result.

The [scan and verifier](scan_ternary_quartic_degree.py) and
[all exact certificate data](ternary-quartic-degree-scan-results.json)
are saved. The following targeted commands passed:

```bash
python research-20260927/scan_ternary_quartic_degree.py
python research-20260927/scan_ternary_quartic_degree.py --verify
```

The second command recomputes the exact first-derivative kernels and
verifies every saved exclusion without solving a numerical optimization
problem. It checks that the 196 cases are exactly the intended set.
Separate targeted `python - <<'PY'` checks compared all 35 columns of
the Hessian coefficient map with direct symbolic differentiation and all
144 columns of the Gram coefficient map with direct monomial products.
Those checks, local Markdown checks, and a scoped `git diff --check`
also passed.
The first command used CVXPY 1.9.3 and CLARABEL. Exact computations used
SymPy. No project-wide checks, Lean verification, or CI inspection were
performed. A later [independent review](ternary-quartic-degree-scan-review.md)
checked the proofs and code and reran the exact verifier successfully.
