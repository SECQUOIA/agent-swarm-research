# Review of the unbounded nonconvex finite-infimum extension

Date: 2026-09-27. Status: independent proof review completed, including a
full reading of the saved [author manuscript](nonconvex-finite-infimum.md).
No mathematical gap was found. One incorrect literature title was reported
for correction. The author supplied the proof route,
but this reviewer did not develop the underlying feasibility theorem.
A separately assigned reviewer checked the double-limit algebra. This is
evidence of correctness, not a formal verification or a novelty claim.

The proposed theorem says that a finite infimum of a rational quadratic
objective over a nonempty set defined by weak rational quadratic and affine
constraints has an integer annihilator of degree and coefficient bit length
\(N^{O(h+1)}\), where \(h\) is the span dimension of the constraint Hessian
matrices. Convexity, boundedness, and attainment are not assumed. The
objective Hessian is excluded from \(h\).

This review read the complete
[nonconvex certificate proof](nonconvex-hessian-span-frontier.md) and
the [finite-quotient elimination lemma](explicit-span-separation.md),
then checked the additional parameter and limiting steps below. It does
not replace the earlier reviews of those two prerequisites.

## 1. Expanding boxes preserve the intended infimum

The lift by a rational Hessian basis gives \(h\) quadratic equations
\(F_j(w)=0\), together with a rational polyhedron \(P\). Intersecting all
lifted coordinates with \([-R,R]\) gives compact sets whose union, as
\(R\to\infty\), is the entire lifted feasible set. These sets are nonempty
for all sufficiently large \(R\). Their minimum values \(v(R)\) decrease
to the original finite infimum \(\theta\). The lift does not require the
original feasible set or any minimizing sequence to be bounded.

For each fixed such \(R\), replace the equations by
\[
 |F_j(w)+\varepsilon^2P_j(w)|\le\varepsilon
\]
and replace the objective by \(q_0(w)+\varepsilon P_0(w)\). An original
boxed minimizer is feasible in these bands for every sufficiently small
positive \(\varepsilon\). Compactness of the fixed box and uniform
convergence of its perturbed objective show that the perturbed values
converge to \(v(R)\). The permissible tail of \(\varepsilon\) can depend
on \(R\). Nothing in the proof needs a uniform tail or convergence of
minimizers as \(R\to\infty\).

## 2. Affine charts and one uniform perturbation

After choosing a subset of active affine rows, including box rows, its
coefficient matrix is independent of \(R\), and its right-hand side is
affine in \(R\). A row-independent subsystem therefore has a chart
\[
 w=a+bR+Vu
\]
whose rational coefficients and constant denominators have polynomial bit
length. Remaining consistency conditions are affine equations in \(R\).
They hold identically, or they can hold at at most one radius. Thus all
charts relevant outside a finite exceptional set have this uniform form.
Keeping \(R\) symbolic is essential to the claimed coefficient bound.

For each chart and oriented subset of the \(h\) bands, take the bad
coefficient polynomial supplied by the genericity lemma in the certificate
proof. Its substitution is nonzero in
\((R,\varepsilon,\operatorname{coeff}(P_0,\ldots,P_h))\): at any one
fixed radius and nonzero \(\varepsilon\), restriction of arbitrary
quadratics in \(w\) onto the chart is surjective onto quadratics in \(u\).

Choose a nonzero coefficient in its expansion in **both** \(R\) and
\(\varepsilon\), and use the integer-grid argument on the product over
the finitely many chart and support choices. Its degree is at most
\(2^{\operatorname{poly}(N)}\). This yields one tuple of integer
perturbation coefficients with polynomial bit length. It works
simultaneously for every radius outside a finite set: after choosing the
tuple, a nonzero polynomial in \((R,\varepsilon)\) can vanish identically
in \(\varepsilon\) at only finitely many \(R\).

This argument needs no coefficient-height estimate for the bad polynomial.
Its degree controls the grid size. It also needs no efficient construction
of the successful perturbation, because the theorem bounds the encoding of
an existing algebraic value.

## 3. Select supports in the nested order

Fix a sequence of nonexceptional radii \(R_j\to\infty\). For each radius,
there are finitely many affine charts and active oriented band subsets.
Choose one occurring along infinitely many \(\varepsilon\downarrow0\).
At such a minimizer, inactive affine rows can be omitted locally. The
genericity conditions give ordinary KKT multipliers, an invertible
multiplier Hessian, and an invertible bordered KKT matrix. The reconstructed
active system has a nonsingular root in at most \(h\) multiplier variables.

There are only finitely many chart and support labels independent of the
radius. One label therefore occurs on an unbounded subsequence of the
\(R_j\). This establishes one polynomial KKT family while preserving the
inner limits to \(v(R_j)\). Multipliers need not remain bounded in either
limit.

Zero-dimensional charts require a separate elementary branch. Their
point is \(w=a+bR\), so their limiting boxed value is the rational
polynomial \(q_0(a+bR)\). If it has a finite limit on an unbounded sequence,
its positive-degree coefficients vanish and the limit is its rational
constant term. The same coefficient-size bound follows.

## 4. The two-parameter elimination is valid

For a positive-dimensional chart, all reconstructed polynomials belong to
\(\mathbb Z[R,\varepsilon,\lambda]\) after clearing constant rational
denominators. Their degrees in each parameter and in the multipliers are
polynomial in \(N\), and the logarithms of their full coefficient
\(\ell_1\)-norms are polynomial in \(N\). No specialized radius is encoded
as an input coefficient.

Run the finite-quotient proof over
\(\mathbb Q(R,\varepsilon,\delta)\). Globally extract the lowest nonzero
coefficients in \(\zeta\), then \(\delta\), then \(\varepsilon\), in that
order. The result is a nonzero polynomial \(P(R,t)\) satisfying
\[
 P(R_j,v(R_j))=0
\]
on the selected sequence. Specialization can increase a vanishing order
or make this identity vacuous at one radius; it cannot invalidate it. A
nonzero polynomial \(P\) has only finitely many radii at which
\(P(R,\cdot)\) is identically zero.

Write
\[
 P(R,t)=R^m p_m(t)+\sum_{i<m}R^i p_i(t),\qquad p_m\ne0.
\]
Divide by \(R_j^m\) and let \(j\to\infty\). Since
\(v(R_j)\to\theta\) is finite, the lower-order terms tend to zero, giving
\(p_m(\theta)=0\). Coefficient extraction preserves the value degree
bound and cannot increase coefficient norm.

More explicitly, with the notation of the finite-quotient lemma,
\[
 L=(a+1)^s,\quad T=a(s+1),\quad
 K=L[\tau(T+1)+2+\lceil\log_2 L\rceil],
\]
where \(\tau\) bounds the logarithm of the coefficient norm in all of
\((R,\varepsilon,\lambda)\), the final polynomial has degree at most
\(L\) and coefficient norm at most \(2^K\). This is
\(N^{O(h+1)}\) in the claimed parameters. The separately assigned
algebra reviewer independently obtained these same bounds and found no
specialization obstruction.

The order of limits is material. On \(xy\ge1\), \(x,y\ge0\), with
\(x,y\le R\) and \(R\ge1\), the minimum of
\(x-\varepsilon y^2\), for \(\varepsilon\ge0\), is
\[
 v_\varepsilon(R)=R^{-1}-\varepsilon R^2.
\]
Its equation is \(Rt+\varepsilon R^3-1=0\). Taking the lowest
\(\varepsilon\) coefficient first and then the highest \(R\) coefficient
gives \(t\), which annihilates the true infimum zero. Reversing these
operations gives a constant after stripping \(\varepsilon\). Taking
\(\varepsilon=1/R\) also produces a divergent value. The proposed proof
uses the correct nested order throughout.

## 5. The complexity consequences have the stated scope

A computable degree and height bound yields a uniform rational integer
\(M\) with polynomial bit length for fixed \(h\), strictly larger than
the absolute value of every finite infimum for an input of the given size.
For a nonempty instance,
\[
 \inf q_0=-\infty
 \quad\Longleftrightarrow\quad
 \exists x\in S:\ q_0(x)\le-M-1.
\]
The forward implication is the definition of an infimum of \(-\infty\).
The reverse implication follows from the strict universal bound in the
finite case. Adding this threshold row increases the Hessian span by at
most one. Thus the existing fixed-span feasibility certificate puts this
unboundedness test in NP.

For a finite infimum, threshold-feasibility bisection approximates it even
when it is not attained. At the exact infimum the oracle may answer either
way according to attainment, but either update retains the infimum in the
closed bracket. Polynomially many precision bits suffice for exact
algebraic reconstruction from the proved degree and height bounds. This
supports an \(\mathrm{FP}^{\mathrm{NP}}\) computation of the finite value
for fixed \(h\), together with classification of empty and unbounded
instances. It does not return a minimizer when none exists, provide a
polynomial-time algorithm without an NP oracle, or supply short certificates
of global optimality.

## 6. The coefficient-sensitive refinement is valid

Section 8 of the saved manuscript separates structural size \(S_0\) from
the largest input numerator or denominator bit length \(\tau_0\). I
checked its stronger bound
\[
 \deg P\le S_0^{O(h+1)},\qquad
 \log_2\|P\|_1\le(\tau_0+1)S_0^{O(h+1)}.
\]
The argument preserves linear dependence on \(\tau_0+1\):

- Hessian-basis extraction and affine charts use rational determinants
  of structurally bounded order. Their coefficient heights are
  \((\tau_0+1)S_0^{O(1)}\).
- The degree of the genericity obstruction and the number of chart and
  support choices depend on structural size. Their coefficients may depend
  on \(\tau_0\), but the grid argument only uses degree. Thus the chosen
  integer perturbations need only \(S_0^{O(1)}\) bits.
- Before determinant expansion, one can clear denominators in the
  structurally many restricted quadratic coefficients. Every later
  expression has denominator dividing a structurally bounded power of
  that common denominator. It is unnecessary to multiply separately over
  the potentially numerous expanded monomial coefficients. Adjugates,
  substitution, and coefficient norms therefore preserve the claimed
  linear dependence on \(\tau_0+1\).
- The multiplication-determinant bound is linear in the logarithmic
  coefficient norm. Passing to polynomial factors adds only a degree
  term. The common-field primitive-element and trace-matrix construction
  in the feasibility proof multiplies heights by polynomials in the field
  degree, preserving the same form. Root-isolation bounds do so as well.

Appending an explicit radius of logarithmic size
\((\tau_0+1)S_0^{O(h+1)}\) adds only linearly many affine rows. Applying
the bound again therefore multiplies two factors of form
\(S_0^{O(h+1)}\); it does not compose the exponent with itself. This
justifies the stated removal of an artificial quadratic exponent in
\(h\) from this particular encoding argument. It does not by itself bound
the runtime of an algorithm whose other steps might have worse dependence.

## 7. Bounded integer variables do not invalidate the extension

Section 10 assumes explicitly bounded integer coordinates and a fixed span
of the continuous Hessian blocks. Each integer assignment then has
polynomial bit length, and substitution changes the continuous linear and
constant coefficients by only a uniform polynomial factor in bit length.
The continuous Hessian blocks themselves do not change. A rational
objective threshold adds at most one Hessian direction.

There are finitely many integer assignments. If one feasible slice is
unbounded below, the full problem is unbounded below. Otherwise the finite
global infimum is the minimum of the finitely many feasible slice infima,
so it equals one of them and inherits the uniform degree and height bound.
This argument does not require any slice infimum to be attained. The NP
threshold query can guess the bounded integer assignment and its continuous
algebraic certificate. The classification and exact-value argument then
applies as written. I found no gap in this extension.

## 8. Prior-art boundary checked during this review

[El Hilany and Tsigaridas, *Bounds on the infimum of polynomials over a
generic semi-algebraic set using asymptotic critical values*, arXiv
2407.17093v1](https://arxiv.org/html/2407.17093v1), Introduction and
Theorem 1, already give degree and size bounds for unattained infima. Their
constrained theorem assumes a closed, connected set whose constraint-subset
varieties are smooth complete intersections. Its bounds are exponential
in ambient dimension. The proposed extension instead treats quadratic
data with arbitrary degeneracy and arbitrary affine rows, and bounds value
encoding polynomially when the Hessian span is fixed. These are distinct
assumptions and conclusions; the comparison does not establish priority.

The primary arXiv abstract and full text were both inspected. The saved
draft initially used a different title for this source; the exact title
above and the closed-and-connected part of its definition of completeness
were sent to the author for correction. The source's single listed version
is v1, dated 24 July 2024.

The prior generic QCQP algebraic-degree result of Nie and Ranestad, and
the finite-quotient deformation literature cited in the prerequisite
notes, remain relevant. An unattained-infimum theorem should not be
presented using only attained generic KKT results as its comparison.

## 9. Verification limits

The proof audit is symbolic and independent of numerical optimization.
The exact example above checks why the parameter order matters; it cannot
validate the universal theorem. A targeted inline `python -` command checked
this document's local links, trailing whitespace, control characters, and
final newline; SymPy in the same command checked the example's polynomial
identity, both coefficient-extraction orders, and its nested and diagonal
limits. All assertions passed. The scoped command
`git diff --check -- research-20260927/nonconvex-finite-infimum-review.md`
also returned successfully; the Python text checks apply independently of
Git tracking status. No Lean formalization, project-wide
verification, or CI inspection was performed. After the author manuscript
was saved, I read it in full and checked that its parameter selection and
limit ordering agree with the reviewed proof. I separately checked its new
coefficient-sensitive refinement and bounded-integer extension, as recorded
above. The requested literature-title correction does not change any proof.
