# Independent review of the implicit convex-polynomial integer oracle

Date: 2026-09-28. Scope: the deterministic oracle transfer in
[the oracle audit](polynomial-nonlinear-dimension-oracle-audit.md).
This reviewer did not develop that argument. The review read the audit,
the corresponding sections of the main theorem, and the local primary
Hildebrand--Koppe text. The radius, gap, and grid bounds supplied to this
interface are assumed here; this is not a review of their proofs.

**Finding.** No substantive gap remains after the corrections below were
incorporated and independently rechecked. The strict projection oracle,
volume bound, and explicit shallow-cut construction are valid. The
recursive bit argument needed a direct bound on lattice coordinate maps:
Hildebrand--Koppe Remark 5.5 assumes such a bound and does not itself prove
it. The repair below supplies that bound. Rational convex integer QP also
provides a precise deterministic lattice subroutine without encoding an
irrational square-root matrix as a rational lattice basis. The revised
adaptation gives the claimed FPT bound, subject to its stated radius,
gap, and standard controlled ellipsoid-rounding inputs.

## 1. What the primary theorem does and does not supply

The primary source is
[Hildebrand--Koppe, *A new Lenstra-type Algorithm for Quasiconvex Polynomial
Integer Minimization*](https://arxiv.org/pdf/1006.4661), inspected locally as
`common-range-prior-sources/hildebrand-koppe.txt`.
Its Section 4 leaves shallow-cut and membership costs as oracle costs.
Theorem 5.7 supplies a shallow-cut algorithm for an explicit polynomial
list, with output bits linear in the polynomial and ellipsoid coefficient
bits. Corollary 5.8 gives rounding output bits linear in polynomial height
and volume-threshold bits. Remark 5.5 bounds substituted polynomial
coefficients **assuming** a coordinate map of the stated bit length;
Remark 5.6 handles composed evaluation. Lemma 6.1 supplies the strict
integer-margin volume bound. Theorem 6.3 treats an explicit list of strict
integer-polynomial inequalities.

These are the relevant interfaces. The source does not directly state
the implicit-row theorem. Its exact wording cannot replace the additional
checks below. In particular, iterating a merely polynomial output-size
bound across dimension reductions would not establish an absolute
input-size exponent.

## 2. Strict projection, including boundary points

Write the relaxed boxed system as

\[
                         Cv+b(y)<0,
 \qquad y\in\mathbb R^m.
\]

For a rational query \(y\), the maximum uniform slack LP is feasible:
set \(v=0\) and choose a sufficiently negative slack. Its optimum is
finite because of the opposite strict box rows, and a finite rational LP
optimum is attained. The normalized dual feasible set

\[
 \Lambda=\{\lambda\ge0:C^T\lambda=0,
                              \mathbf1^T\lambda=1\}
\]

is a compact rational polytope. Strong duality gives

\[
 \exists v:Cv+b(y)<0
 \quad\Longleftrightarrow\quad
 \lambda^Tb(y)<0\quad\text{for every vertex of }\Lambda.
                                                               \tag{1}
\]

A zero optimum means nonmembership in this strict set. It must not be
accepted merely because the associated weak system is feasible. If boxes
are omitted and \(\Lambda\) is empty, the slack problem is unbounded
above, and the projected set is the whole space; the audit states this
boundary case correctly.

When the slack optimum is nonpositive, a dual optimal vertex supplies a
violated polynomial. A vertex of an optimal face is a vertex of
\(\Lambda\). Its support has size at most \(\operatorname{rank}C+1\),
and its coordinates have rational minor bounds depending on \(C\),
not on the queried point. Thus choosing a vertex is material: an arbitrary
point in the optimal dual face need not have a query-independent encoding
bound. Exact LP and rational postprocessing can select such a vertex.

Every returned polynomial is a nonnegative combination of the globally
convex native polynomials. Clearing denominators by a positive integer
preserves convexity and strict signs. The normalization can be chosen
from the polynomial coefficients alone, so each returned row belongs to
one fixed finite family. Its coefficient bits and monomial count are
uniformly bounded. The family can be exponentially long without being
constructed.

The main theorem relaxes both signs of every affine equality before
forming (1). Its rounded feasible anchor lies strictly inside the wider
boxes. Conversely, the strict original-row residual lies below the supplied
positive gap at the same original integer assignment. These observations
justify using a full-dimensional strict set even when the original model
has no interior. They do not justify replacing a weak implicit family by
strict inequalities without that relaxation.

## 3. The shallow-cut construction works with exact rational data

Let \(E(A,a)\) contain the projected set, with rational \(A\succ0\).
For a rational LDL factorization \(A=LDL^T\), choose dyadic \(t_i\)
satisfying \(\sqrt{D_{ii}}/2\le t_i\le\sqrt{D_{ii}}\). Exact
rational comparisons find such numbers with bit length linear, up to a
dimension factor, in the input bit bound. No square root needs to be
encoded exactly.

In the coordinates \(LD^{1/2}\), the points

\[
                        a\pm\frac{t_iLe_i}{m+1}
\]

have axis distances between \(1/[2(m+1)]\) and \(1/(m+1)\).
Their convex hull contains a Euclidean ball of radius
\(1/[2(m+1)\sqrt m]\). Consequently the conservative rational ratio
\(\beta=2m(m+1)\) is valid. If all these finitely many points satisfy
the strict family, their entire convex hull does too, including its
boundary. The resulting inner ellipsoid is contained in the strict set.

Otherwise a returned convex polynomial \(F\) satisfies \(F(y)\ge0\)
at a test point. If \(\nabla F(y)=0\), convexity makes \(y\) a global
minimizer of \(F\), so the strict row, and hence the whole family, is
empty. For \(c=\nabla F(y)\ne0\), convexity gives

\[
 c^Tx<c^Ty
 \le c^Ta+\frac{\sqrt{c^TAc}}{m+1}
 \quad\text{for every strictly feasible }x.          \tag{2}
\]

This is the correct shallow-cut geometry for the convention
\(E(A,a)=\{x:(x-a)^TA^{-1}(x-a)\le1\}\). The normal is rational;
the square-root offset is an ellipsoid-method expression, not a required
rational input number. The audit correctly uses \(A\), rather than
\(A^{-1}\), in (2).

The usual closed-set rounding method can be run on the closure of the
strict set: every returned weak cut contains that closure, while every
inner-ellipsoid certificate is stronger, lying in the strict set itself.
This distinction prevents an integer point on a deleted boundary from
being accepted. Zero-dimensional sections must use the actual strict
membership oracle.

## 4. Integer margins control volume without counting rows

After positive denominator clearing, let all strict polynomials have
integer coefficients of at most \(\ell\) bits and at most \(M\)
monomials, with degree at most \(d\). At an integer feasible point,
every row has value at most \(-1\). On a bounding box enlarged by one,
the common coefficient and degree bounds give one uniform gradient bound
\(L\). A ball of radius at most \(1/(2L)\) about that point remains
strictly feasible for **all** rows simultaneously. No union bound or
row-count multiplier is needed.

This gives a conditional positive volume threshold whose reciprocal
logarithm is at most

\[
 f(m,d)(\ell+\log(R+1)+1).
\]

The same argument applies after an integer affine substitution, because
restricted rows still have integer coefficients. It does not require a
known feasible center or a supplied inscribed ball. Shrinking an outer
ellipsoid below this volume correctly rules out strict integer feasibility.

## 5. The missing direct bound on recursive lattice maps

Suppose all entries of \(A\) and \(a\) have at most \(H\) bits.
Clear the at most \(m^2\) denominators of \(A\) by a positive integer
\(D_A\). Then \(D_AA\) is positive definite and integral, so its
determinant is a positive integer. A matrix-norm bound and the product
of eigenvalues give

\[
 \lambda_{\min}(A)
       \ge2^{-O(m^3)(H+\log(m+1))}.                 \tag{3}
\]

Let \(h\ne0\) minimize \(h^TAh\) over integer vectors. Comparing
with a coordinate unit vector gives \(h^TAh\le2^H\). Equation (3)
therefore gives a coordinate-bit bound

\[
       \operatorname{bits}(h)
           \le O(m^3)(H+\log(m+1)).                \tag{4}
\]

The vector \(h\) is primitive, since dividing a nontrivial common
integer factor would strictly decrease its positive quadratic value.

Use extended-gcd column operations to construct a unimodular integer
matrix \(U\) with

\[
                          h^TU=e_m^T.
\]

At most \(m-1\) two-coordinate gcd steps suffice. Each elementary
matrix has entries bounded in bits by a constant times the bound in (4).
Multiplying these matrices, and applying the cofactor formula to their
unimodular product, bounds the bits of \(U\) and \(U^{-1}\) by
\(\operatorname{poly}(m)(H+1)\). This is linear in \(H\).
The correct parameterization of the level \(h^Ty=t\) is

\[
                             y=U(w,t).
\]

Merely completing \(h\) itself to a lattice basis would not establish
this identity; the row-normal condition on \(U\) is required.

If the inner ellipsoid has no integer point, its flatness bound gives
\(\sqrt{h^TAh}\le m\beta/2\). It is enough to consider

\[
 t=\lfloor h^Ta\rfloor+j,
 \qquad |j|\le\lceil m\beta/2\rceil+2.
\]

There are only dimension-dependent many levels. Every level has bits
\(\operatorname{poly}(m)(H+1)\); no irrational endpoint comparison is
needed for this conservative list.

If the old set lies in a ball of radius \(R\) about zero, the new
coordinates satisfy \(\|w\|\le\|U^{-1}\|R\). Append a fresh strict
origin-centered ball with an integer radius enlarged by one. Its radius
bits are bounded by
\(\log(R+1)+\operatorname{poly}(m)(H+1)\). This handles translated
affine sections without claiming that an old origin-centered bounding
quadratic retains that form. Old bounding rows may have linear terms;
they remain valid convex polynomials.

Finally, a degree-\(d\) polynomial of coefficient bits \(\ell\),
substituted at \(U(w,t)\), has coefficient bits at most

\[
 \ell+d\,\operatorname{bits}(U,t)
       +O(d\log(m+1))+\log\binom{m+d}{d},            \tag{5}
\]

after harmless parameter-dependent enlargement of the constants.
Thus the transformed height is linear in \(\ell+H+1\), times a
function of \(m,d\). This supplies the hypothesis that Remark 5.5
requires, rather than attributing its proof to that remark.

## 6. Exact lattice subroutines with rational quadratic forms

An exact square root of a rational positive-definite matrix need not be
rational. Thus a rational-basis Euclidean lattice theorem should not be
applied to \(A^{1/2}\) without explaining the representation.
A separate, already established import avoids that issue:
[Del Pia, version 2, Theorem 3](https://arxiv.org/pdf/2311.00099v2)
gives deterministic FPT exact optimization of a rational PSD quadratic
objective over the integer points of a rational polyhedron.

To find the shortest direction, minimize \(h^TAh\) over each of the
\(2m\) polyhedra \(h_i\ge1\) and \(h_i\le-1\), and retain the
best result. Their union contains precisely the nonzero integer vectors.
To test the inner ellipsoid, minimize
\((x-a)^TA^{-1}(x-a)\) over \(x\in\mathbb Z^m\), and compare the
result with \(1/\beta^2\). Both objectives are rational and positive
definite; both minima are attained. These calls have cost
\(f(m)\operatorname{poly}(H)\), without using the new polynomial
feasibility theorem. If the inner test succeeds, its returned point lies
in the strict set. If it fails, the flatness argument in Section 5 applies.

## 7. Why the recursion retains an absolute input exponent

The shallow-cut oracle has output bits
\(f(m,d)(\ell+H+1)\). Controlled rational rounding of ellipsoid data,
as in the source's Corollary 5.8, is necessary. Unrounded rational updates
would not supply a bit bound. The resulting ellipsoid output has bits
linear in the current height, outer-radius bits, and volume-threshold
bits, times a dimension and degree factor.

Combined with Sections 4--5, one recursive level replaces the bound
\(\ell+\log(R+1)+1\) by at most a parameter-dependent multiple
of that bound. There are at most \(m\) levels. Their product is a
function of \(m,d\), not a power of input length depending on \(m\).
There are only parameter-dependent many branch nodes. At every node,
exact LP queries, polynomial evaluation, and rational convex integer QP
have absolute polynomial exponents. This gives the claimed deterministic
FPT bit bound.

The transfer of the ellipsoid output guarantee uses the same interface
as the explicit-list proof: a shallow-cut or rounding answer and a
linear-in-height bound on its output. The explicit row scan has been
replaced by the LP oracle, while the remaining geometric steps and their
precision requirements are unchanged. The source's Corollary 5.8 refers
to Heinz for its rounding proof; this review does not claim to have
retrieved Heinz's complete article independently.

## 8. Scope and verification record

This review establishes no priority claim. It assumes the main theorem's
effective radius, residual gap, and rounding mesh. It requires globally
convex native polynomials, a constant eliminated-variable matrix, a finite
uniformly bounded implicit integer-polynomial family, and exact rational
membership with a violated row. Merely knowing that a projected feasible
set is convex would not satisfy these requirements.

The proof was checked by reconstruction and primary-source comparison.
The review prompted the explicit branch-map argument and the rational-QP
lattice import, so those repairs are overlapping contributions, not an
independent second derivation of the original proof. The revised Section
3.3 was read in full and independently rechecked: the rational-form QP
calls, shortest-direction bound, correct unimodular section, fresh
bounding ball, and linear height recurrence now appear explicitly.

A targeted inline `python -` check verified this review's final newline,
whitespace, control characters, balanced math delimiters, and local links.
It passed. The author's separate exact-example tests are recorded in the
audit; this review did not rerun those unchanged checks. No project-wide
verification, CI inspection, or Lean formalization was performed.
