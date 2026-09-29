# Rational denominators repair the convex quartic SOS obstruction

Date: 2026-09-28. Status: explicit exact certificate and minimum
denominator degree passed fresh independent review. The general
existence statements below are consequences of prior work, not novelty
claims.

The three-variable rational SOS-convex counterexample has a small exact
rational-function SOS certificate. Its failure of rational polynomial
SOS does not persist when an everywhere-positive quadratic denominator
is allowed. The minimum possible degree of a common polynomial
denominator is exactly two.

This makes the certificate limitation precise. Rational polynomial
squares cannot certify the attained optimum of this example, while
rational-function squares with no real poles can. The result is a
supporting example and a boundary on the earlier obstruction; it is not
a complexity lower bound or a solver speedup. A
[further scaling theorem](rational-radial-exponent-obstruction.md)
shows that fixed radial multipliers can require unbounded order within
this strict convex class, while short adaptive quadratic denominators
continue to suffice.

## 1. The polynomial and an exact quadratic multiplier

Use
\[
\begin{aligned}
r_0&=2-2xy,&r_1&=2x^2-2yz,&r_2&=2y^2-4z,\\
r_3&=2z^2-x,&r_4&=2xz-y,
\end{aligned}
\]
and put
\[
A=4r_0+5r_1+3r_2+9r_3,\qquad
F=A^2+\sum_{i=0}^3r_i^2-r_4^2.
\]
The [independent review of the original construction](ternary-rational-sos-convex-counterexample-review.md)
establishes that \(F\) has a rational positive definite Hessian Gram
certificate, \(\nabla^2F\succeq I\), and minimum zero at
\[
p=(a^{-1},a,a^{-3}),\qquad a=\sqrt[5]{2}>0.
\]
It also proves that \(F\) is not a sum of rational polynomial squares.
Here we retain that polynomial exactly.

Set
\[
R=1+x^2+y^2+z^2.
\]
The [exact certificate checker](check_ternary_rational_sos_quadratic_multiplier.py)
contains an integer symmetric matrix \(N\) of size fifteen and the
following rational vector \(b\):
\[
\begin{aligned}
b=(&z^2-x/2,\ y^2-2z,\ xz-y/2,\ xy-1,\ x^2-yz,\\
&z^3-y/4,\ yz^2-1/2,\ y^2z-x,\ y^3-2yz,\\
&xz^2-yz/2,\ xyz-z,\ xy^2-y,\ x^2z-1/2,\ x^2y-x,\ x^3-z)^{\mathsf T}.
\end{aligned}
\]
It verifies the identities and strict inequality
\[
\boxed{\quad b^{\mathsf T}Nb=8RF,\qquad N-8I_{15}\succ0.\quad}       \tag{1}
\]
The entries satisfy \(|N_{ij}|\le4240\). The checker gives all
entries explicitly, so (1) is a finite exact certificate, not an
existence assertion based on a numerical SDP.

The components of \(b\) form the complete rational vector space of
polynomials of degree at most three vanishing at \(p\). Indeed, there
are twenty cubic monomials, their evaluations span the degree-five
field \(\mathbb Q(a)\), and the displayed fifteen independent
polynomials vanish at \(p\). Completeness of this basis motivated the
search. The identity and positive definiteness in (1) suffice to verify
the multiplier certificate even without that completeness argument.

Rational \(LDL^{\mathsf T}\) factorization of \(N/8\) expresses
\(RF\) as fifteen positively weighted rational cubic squares.
Every positive rational weight is a sum of four rational constant
squares. Therefore
\[
RF=\sum_j q_j^2,\qquad q_j\in\mathbb Q[x,y,z],\quad \deg q_j\le3.     \tag{2}
\]
No extension of the coefficient field is used.

## 2. A common denominator of minimum degree

A multiplier certificate and a common denominator are different
objects. From (2),
\[
R^2F
=\sum_j q_j^2+\sum_j(xq_j)^2+\sum_j(yq_j)^2+\sum_j(zq_j)^2.
\]
Consequently
\[
F=\sum_j(q_j/R)^2+
  \sum_j(xq_j/R)^2+
  \sum_j(yq_j/R)^2+
  \sum_j(zq_j/R)^2.                                      \tag{3}
\]
The common denominator \(R\) has degree two and is at least one
everywhere. The rational numerators in (3) have degree at most four.
The cleared identity uses \(R^2F\), of degree eight, rather than
mistaking the degree-six multiplier identity for a squared-denominator
identity.

**Cancellation lemma.** If a rational polynomial \(P\) is not rational
SOS, no rational-function SOS representation of \(P\) has a common
polynomial denominator of degree at most one.

**Proof.** A nonzero constant denominator would give rational
polynomial SOS directly. Otherwise the denominator is a nonconstant
rational affine polynomial \(\ell\). Clearing it gives
\[
\ell^2P=\sum_j u_j^2,\qquad u_j\in\mathbb Q[x].
\]
Every \(u_j\) vanishes on the real affine hyperplane \(\ell=0\),
because a sum of real squares is zero there. Make a rational invertible
affine change of variables sending \(\ell\) to a nonzero rational
multiple of the first coordinate. Polynomial division by that
coordinate shows that \(\ell\) divides every \(u_j\) over
\(\mathbb Q\). Cancelling \(\ell^2\) gives a rational polynomial
SOS for \(P\), a contradiction. \(\square\)

Apply the lemma to \(F\) and combine it with (3). Its minimum common
polynomial denominator degree is exactly two. This does not minimize
the number of squares or claim that the particular denominator \(R\)
is unique.

## 3. The general regular-denominator existence result is prior theory

The following useful statement is a consequence of the general-ring
results of Burgdorf, Scheiderer, and Schweighofer.

**Corollary of prior results.** Let \(f\in\mathbb Q[x_1,\ldots,x_n]\)
be nonnegative on \(\mathbb R^n\), of even degree \(2d\). Suppose
its leading homogeneous form is positive definite, its real zero set
is finite, and its Hessian is positive definite at every real zero.
Then, for some integer \(N\ge0\),
\[
(1+\|x\|^2)^Nf\in\Sigma\mathbb Q[x]^2.                       \tag{4}
\]
The empty zero set is allowed. Increasing \(N\) by one preserves the
property, so \(N\) can be made even to obtain a rational-function SOS
with a common denominator having no real zeros.

The proof below spells out the rational coefficient issue. The relevant
prior tools are the pure-state membership criterion, its dichotomy for
ideals, and existence of order units in ideal squares: Theorem 2.5,
Corollary 4.12, Proposition 5.3(a), and Remark 5.5(1) of
[Burgdorf–Scheiderer–Schweighofer (2012)](https://ems.press/content/serial-article-files/43280).
Their geometric Hessian theorem is stated over \(\mathbb R\);
merely quoting that theorem and rounding a boundary Gram matrix would
not settle (4) over \(\mathbb Q\).

**Deduction.** Homogenize \(f\) to \(H(y_0,\ldots,y_n)\), put
\[
q=\sum_{i=0}^n y_i^2,\qquad
\mathcal A=\mathbb Q[y_0,\ldots,y_n]/(q-1),\qquad
M=\Sigma\mathcal A^2.
\]
The sphere relation bounds all coordinate functions in the SOS order,
so \(M\) is archimedean. Positive definiteness of the leading form
excludes zeros on the sphere with \(y_0=0\). All remaining zeros
come from the finite affine zero set. They are algebraic, and their
tangent Hessians on the sphere are positive definite: near such a
point, \(H=y_0^{2d}f(y/y_0)\), and the zero value and vanishing
gradient remove the derivatives of the prefactor.

Let \(J\) be the rational vanishing ideal of these sphere zeros.
It is an intersection of finitely many distinct maximal ideals of
\(\mathcal A\), with number fields as residue fields. The fields
need not be totally real. Each has a real embedding coming from a
zero. Vanishing of \(H\) and its tangent differential at that
embedding is injective on the residue field, hence holds over it.
Smoothness of the sphere and separability of the residue extension
then give membership in the square of each maximal ideal.
Comaximality gives \(H\in J^2\).

Choose generators \(b_i\) of \(J\) and put \(u=\sum_i b_i^2\).
The cited ideal-square result makes \(u\) an order unit on
\((J^2,M\cap J^2)\). The pure-state dichotomy has two cases.
Away from the zeros, a normalized pure state is a positive multiple
of evaluation, and therefore takes a positive value on \(H\).
At a zero \(z\), it factors through
\[
(J^2/\mathfrak mJ^2)\otimes_{\mathcal A/\mathfrak m,z}\mathbb R
\cong\operatorname{Sym}^2(T_z^*S^n).
\]
Positivity on squares makes its matrix positive semidefinite.
Normalization at \(u\) makes that matrix nonzero. Its pairing with
the positive definite tangent quadratic term of \(H\) is strictly
positive. The pure-state criterion gives \(rH\in M\) for an integer
\(r>0\); a positive rational scalar is a sum of rational squares,
so \(H\in M\). If there are no zeros, the usual strictly positive
archimedean representation result supplies the same conclusion.

Write \(H=\sum_i p_i^2\) in \(\mathcal A\).
Antipodal averaging separates each \(p_i\) into its even and odd
parts. Choose a sufficiently large even integer \(D\ge d\).
Using powers of \(q\), homogenize the even parts to forms \(E_i\)
of degree \(D\), and the odd parts to forms \(O_i\) of degree
\(D-1\). On the sphere the identity remains unchanged, and homogeneity
then gives the polynomial identity
\[
q^{D-d}H=\sum_iE_i^2+\sum_{i,j}(y_jO_i)^2.
\]
Setting \(y_0=1\) proves (4). All algebra and coefficient choices
remain over \(\mathbb Q\). \(\square\)

Both the three- and four-variable examples meet these hypotheses.
Their strict full Hessian Gram certificates imply positive definite
leading quartic forms as well as positive definite Hessians at their
unique zeros. Thus some regular rational denominator is guaranteed by
prior theory. Certificate (1) supplies a small exponent and exact data
for the three-variable example.

## 4. What the prior results do and do not bound

The sources examined on 2026-09-28 distinguish several questions.

- Artin's theorem already gives rational-function SOS for a rational
  nonnegative polynomial. Kaltofen, Li, Yang, and Zhi develop exact
  rational certificates through numerical discovery and exact recovery.
  The present small certificate uses that established type of workflow.
  [Primary algorithm paper](https://www.sciencedirect.com/science/article/pii/S0747717111001143).
- Lombardi, Perrucci, and Roy give general elementary recursive degree
  bounds in the number of variables and degree, with a tower of five
  exponentials. Their Theorem 1.4.4 permits a denominator that vanishes
  only where the polynomial vanishes. Over \(\mathbb Q\), its positive
  weights can be expanded into rational squares. It does not by itself
  ensure a denominator nonzero at the minimum.
  [Primary manuscript, Theorem 1.4.4](https://arxiv.org/pdf/1404.2338).
- Reznick's usual radial multiplier bound assumes a positive definite
  homogeneous form. The homogenizations here have zeros, so its
  minimum-to-maximum ratio is zero and that estimate does not apply.
  His absence-of-uniform-denominators theorem also rules out a single
  multiplier or finite menu for all nonnegative forms outside Hilbert's
  SOS cases. [Primary paper, Sections 2–3](https://arxiv.org/pdf/math/0306163).
- Scheiderer's local-ring Corollary 2.7 provides a second route to a
  denominator nonzero at an isolated nondegenerate real zero. It
  requires checking the zero-dimensional real-zero condition before
  passing from the completion to the local ring.
  [Primary local-ring paper](https://www.math.uni-bielefeld.de/lag/man/057.pdf).
- Benoist shows that formal power-series SOS alone can fail to descend
  to a local ring. His Theorems 0.3–0.4 rule out using that shortcut
  without its missing hypotheses. The real-closed-field theorem that
  ternary quartics have no bad points is also insufficient on its own
  for rational coefficient descent.
  [Primary paper, introduction and Remark 2.7](https://www.math.ens.psl.eu/~benoist/articles/badpoints.pdf).

There is no conflict between general bounds on the degree of an
adaptively chosen denominator and the absence of a fixed universal
denominator. For the broad class in (4), allowing empty zero sets,
there is no bound on its radial exponent depending only on dimension
and degree outside Hilbert's cases. Otherwise rational positive definite
forms, which are dense among nonnegative forms, and closedness of a
fixed-degree real SOS cone would give the universal radial multiplier
excluded by Reznick.

This last argument does not establish any lower bound for the narrower
class of rational strongly SOS-convex quartics. A
[separate argument using rational vanishing spaces](rational-radial-exponent-obstruction.md)
does prove unbounded fixed-radial order in that class, even with
three variables and an unchanged Hessian at the minimizer.
The proof of (4) supplies no useful exponent or coefficient-height
estimate. Input-sensitive bounds and the selection of short adaptive
denominators remain questions; a dimension-and-degree-only fixed-radial
bound is ruled out by the scaling theorem.

## 5. Verification and scope

Discovery used a fifteen-by-fifteen numerical SDP on the rational cubic
vanishing space. Integer rounding of free Gram entries followed by
exact coefficient projection produced \(N/8\). The saved checker
uses no numerical optimizer. The author ran:

~~~text
python research-20260927/check_ternary_rational_sos_quadratic_multiplier.py
~~~

It passed exact coefficient equality, positive rational LDL pivots for
\(N-8I\), and the cubic vanishing-space checks. The
[fresh reviewer](rational-denominator-certificate-fresh-review.md)
independently reconstructed the polynomials with sparse Fraction
arithmetic and checked all fifteen positive leading principal
determinants by the Bareiss algorithm. The reviewer also checked the
vanishing-space ranks, the original non-SOS coefficient obstruction,
the rational-function conversion, and the minimum-denominator proof.
Numerical eigenvalues were used only in discovery.

The general sphere deduction was checked by a primary-literature
reader and a separate reader, and reconstructed by this note's author.
It is presented as an application of established theorems, without
claiming a new general existence result. No Lean proof, project-wide
test, or CI inspection was performed.

A targeted inline Python document check, run as
\(\texttt{python3 -}\), passed for this note, the radial-exponent
note, and their two fresh reviews. It checked math-delimiter balance,
trailing whitespace, control characters, final newlines, and all
fourteen local file links. These are document checks, separate from
the exact mathematical checks above.
