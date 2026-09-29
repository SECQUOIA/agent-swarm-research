# Independent review of stationary quartics at the quintic tower

Date: 2026-09-28. Status: passed; no substantive mathematical correction
needed. Reviewer: lattice_height_check, who did not contribute to the
stationary-space theorem before this review.

I read the frozen [candidate proof](tower-quartic-stationary-space.md)
and reconstructed its induction. The conclusions
\[
 J_{3,k}=0,\qquad
 J_{4,k}=\{q^{\mathsf T}Aq:A\in\operatorname{Sym}_{5k}(\mathbb Q)\}
\]
hold for every \(k\geq1\), with a unique representing matrix. Here
stationarity means both zero value and zero full ambient gradient at
the supplied point. The proof does not require nonnegativity or
convexity. I used the complete quadratic basis and product independence
from the [reviewed companion theorem](tower-quadratic-vanishing-space-review.md)
as dependencies.

The local interpolation step has the correct field and dimension.
With \(L=\mathbb Q(a_{k-1})\) and \(K=\mathbb Q(a_k)\), inclusion
follows from \(a_{k-1}=a_k^5\). Eisenstein irreducibility of
\(T^{5^j}-2\) gives \([K:L]=5\). Thus the twenty local monomials
of degree at most three map to a twenty-dimensional \(L\)-space of
values and three derivatives. For the first gate, \(L=\mathbb Q\)
and the radicand is two.

The residue decomposition must use different field-coordinate rows
for different derivatives. A monomial of weight \(r\) modulo five
contributes to value residue \(r\), to the \(x\)-derivative residue
\(r-1\), to the \(y\)-derivative residue \(r-2\), and to the
\(z\)-derivative residue \(r-3\). These twenty rows are disjoint
across the five blocks and exhaust the codomain. With these shifted
rows, the five displayed matrices and their nonzero determinants are
correct. No claim about interpolation at generic points is needed.

The passage from local interpolation to coefficient vanishing is
legitimate. Every earlier tower coordinate lies in \(L\), so
specializing the earlier variables puts all coefficients in that
field. The local lemma uses only the value and the three last-gate
partial derivatives. Its conclusion is that the specialized polynomial
is identically zero in the last three independent variables, not just
that it vanishes at their supplied values.

The cubic induction then closes with the stated total-degree bounds.
Coefficients of last-gate monomials of degree two or three have degree
at most one in the earlier variables. They vanish identically by
rational affine independence. The remainder is
\[
 h_0(U)+x_kh_1(U)+y_kh_2(U)+z_kh_3(U),
 \qquad \deg h_0\leq3,\quad \deg h_j\leq2\ (j>0).
\]
All four coefficient values vanish at the earlier point. For each
earlier ambient coordinate, the corresponding derivative of this
remainder is a relation over \(L\) among
\(1,a_k,a_k^2,a_k^3\). Their independence makes every coefficient
derivative vanish separately. The earlier quadratic stationary space
is zero because its derivatives are rational affine polynomials
vanishing at the tower point. The cubic induction therefore kills
all four coefficients. At the first gate, local interpolation gives
the result directly; no undefined zero-gate field is used.

The quartic proof uses two different degree notions correctly. The
part of degree four in the last triple has constant rational
coefficients because the total degree is at most four. The fifteen
products of the last gate's five leading quadratics span all ternary
homogeneous quartics. Subtracting the corresponding relation products
therefore removes precisely this part. Each subtracted product has
zero value and full gradient at the tower point, including derivatives
in earlier variables. This follows from the product rule and the
vanishing of both factors; it does not treat the predecessor variable
in a last-gate relation as globally constant.

After this subtraction, local cubic interpolation kills every
specialized coefficient. Last-gate degree-three coefficients are
affine in the earlier variables and hence are zero polynomials.
The six quadratic coefficients have degree at most two and belong
to the earlier rational quadratic vanishing space.

The crucial compatibility condition for those six coefficients is
also an identity of polynomials. Among last-gate monomials of degree
at most two, only \(y_k^2\) and \(x_kz_k\) evaluate to the field
basis element \(a_k^4\). The other possible wraps are
\(y_kz_k=a_{k-1}\) and \(z_k^2=a_{k-1}a_k\), which contribute
to basis residues zero and one. Differentiate the remainder in any
earlier ambient variable before evaluating it. Its zero value then
forces the corresponding derivative of
\(c_{y^2}+c_{xz}\) to vanish. The sum itself already vanishes at
the earlier point. It is a rational polynomial of degree at most two,
so the established zero quadratic stationary space gives
\[
                         c_{y^2}+c_{xz}=0
\]
identically. An assertion only about its value at the tower point
would not suffice here; the full-gradient hypothesis supplies exactly
the missing information.

Consequently the quadratic last-gate part is
\(\sum_{j=1}^5L_j(V)P_j(U)\), with every \(P_j\) in the earlier
quadratic vanishing space. Subtracting
\(\sum_jq_{k,j}(U,V)P_j(U)\) is allowed by the companion basis
theorem. These are cross-gate products of vanishing quadratics, so
they preserve full stationarity and total degree at most four.
In particular the term \(-x_{k-1}x_k\) in \(q_{k,5}\) has
last-gate degree one and total degree two. Multiplying it by a
quadratic \(P_5(U)\) leaves a last-linear coefficient of degree
at most three, as required; it does not invalidate the filtration.

The final remainder is last-linear, with constant coefficient of
degree at most four and other coefficients of degree at most three.
Power-basis independence gives zero value and zero earlier gradient
for each coefficient. The previously proved cubic result kills the
three nonconstant coefficients; quartic induction expresses the
constant coefficient in earlier relation products. For one gate,
subtracting the fifteen local products leaves a local stationary
cubic, which is zero. This proves the reverse inclusion for every
\(k\). Product independence from the companion theorem proves
uniqueness and dimension \(\binom{5k+1}{2}\).

The computational consequence stays within the stated scope.
There are \(\binom{3k+4}{4}=O(k^4)\) coefficient positions and
\(\binom{5k+1}{2}=O(k^2)\) relation products, all with bounded
integer coefficient entries. Rational linear algebra therefore
recovers the unique matrix in polynomial bit time when the input
is in the stationary space. Testing its positive semidefiniteness
and producing rational squares use the reviewed companion algorithm.
Membership in the stationary space can itself be checked by the
same product-span computation, or by exact sparse value and gradient
evaluation. In the latter method, each degree-at-most-four monomial
evaluates to \(2^t a_k^e\) with \(0\leq e<5^k\). Its raw exponent
is at most \(12\cdot5^{k-1}\), so \(t\leq2\), and every exponent
integer has \(O(k)\) bits. Grouping equal residues for each
derivative avoids a dense exponential-degree field representation.

The runtime is polynomial in \(k\) and the explicit rational input
length, not merely in the bit length of a succinctly supplied \(k\).
The result recognizes rational polynomial SOS in this supplied-point
class. It does not find an unknown tower point, decide real SOS or
nonnegativity in general, or infer ambient stationarity at a
constrained optimum. Rational coefficients are essential: over the
reals, squares of nonzero affine polynomials vanishing at the point
already give nonzero stationary quadratics.

The opening observation about an indefinite rational matrix for a
strongly convex real-SOS quartic is supported by the existing
[least-field construction](exponential-least-sos-field.md), together
with this theorem and the companion recognition result. It is not
a positivity consequence of the stationary-space proof alone. I
suggested adding that direct dependency link; this is an exposition
improvement, not a mathematical repair.

An independent nested reviewer, field_height_probe, rederived the
local interpolation matrix and computational scope without importing
the author's checker. The retained
[local checker](check_tower_quartic_first_jet_review.py) verifies all
twenty cubic monomials, computes their formal derivatives, substitutes
\((t,t^2,t^3)\), and reduces modulo \(t^5-b\). It checks that all
entries outside the shifted-residue blocks vanish and reproduces the
five displayed blocks. The targeted command is:

    python3 research-20260927/check_tower_quartic_first_jet_review.py

It passes with block determinants \(5,5b,-5b,-5b,-5b\), and grouped
full determinant \(-3125b^4\). I reran that command and checked that
all four local document links resolve. I also read the author's checker and
its stated finite kernel ranks; I did not rerun or extend those
overlapping global cases. These exact checks supplement the uniform
proof. No numerical roots, Lean proof, project-wide checks, or CI
inspection were used.

This review establishes no publication-priority claim. It audits the
specific uniform tower identity, using the reviewed companion
results. It does not assert an extension to general root circuits.
