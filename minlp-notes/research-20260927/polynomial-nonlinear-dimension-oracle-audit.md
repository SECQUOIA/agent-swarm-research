# Oracle audit for convex polynomial systems with few nonlinear coordinates

Date: 2026-09-28. Scope: the mixed-integer oracle step in the developing
convex-polynomial extension. This note audits the interface; the required
integer radius, continuous fiber radius, positive residual gap, and mesh
size are separate inputs. The author coordinated with the main proof and
prior-audit authors, then independently inspected the primary algorithmic
sources and reconstructed the needed oracle. An
[independent adversarial review](polynomial-nonlinear-dimension-oracle-review.md)
checked the complete adaptation and its substantive correction below.

**Finding.** A deterministic FPT integer-feasibility step is justified for
the strictly relaxed construction below. It follows by adapting the
Hildebrand--Koppe shallow-cut and lattice recursion proof to an oracle
returning a violated convex polynomial. Their explicit-row theorem alone
does not state this extension. The strict inequalities, uniformly bounded
row coefficients, and closure under integer affine substitutions supply
the additional information used in the adaptation.

## 1. Precise input to this part of the argument

Write the original native rows as

\[
 C_i v+p_i(z,u)\le0,
 \qquad z\in\mathbb Z^k,\quad u\in\mathbb R^r.       \tag{1}
\]

The matrix \(C\) is constant and rational. Every \(p_i\) is a rational
polynomial of degree at most \(d\), convex jointly in \((z,u)\).
Affine rows and equations represented by opposite inequalities are
allowed. This is convexity of the native polynomial functions, a stronger
assumption than convexity of their common feasible set.

Assume the preceding radius and gap arguments have supplied rational
numbers of bit length \(f(k,r,d)N^C\) with these properties:

- If an integer-feasible point exists, one exists with
  \(\|z\|_\infty\le B\) and \(\|(u,v)\|_\infty\le R\).
- For every integer \(z\) in the wider integer box, the minimum of the
  maximum positive original residual over
  \(\|(u,v)\|_\infty\le2R\) is zero or at least \(\Delta>0\).
- A rational mesh \(\delta>0\) is small enough that rounding the
  \(u\) coordinates of the bounded feasible point to
  \(u=\delta a\), \(a\in\mathbb Z^r\), changes each original residual
  by less than \(\varepsilon/2\), where
  \(0<\varepsilon<\Delta\). The rounded point remains inside the wider
  continuous box.

Now require the **strict** inequalities

\[
 C_i v+p_i(z,\delta a)<\varepsilon,
 \quad |z_j|<B+1,
 \quad |\delta a_j|<2R,
 \quad |v_j|<2R.                                    \tag{2}
\]

Use a wider integer box when the supplied integer-radius convention needs
one. All coordinates whose bounds are retained are included in the strict
system. The integer tuple is \(y=(z,a)\in\mathbb Z^m\),
\(m=k+r\). If \(m=0\), ordinary strict linear feasibility in \(v\)
handles this step.

The rounded feasible anchor makes every row in (2) strict. Conversely,
an integer \(y\) satisfying (2) has original residual below
\(\varepsilon<\Delta\) at the same integer \(z\), so that original
fiber is feasible by the supplied gap. This proves the needed equivalence
of integer feasibility. It does not assert that the returned rounded
continuous point satisfies the original rows exactly.

Original affine equations and lower-dimensional feasible sets cause no
problem: their two opposite rows are relaxed before the strict system is
formed. No Slater assumption on (1) is being imposed.

## 2. An exact oracle for the strict projected set

Absorb the mesh, relaxation, and strict boxes into the notation

\[
                  C v+b(y)<0.                       \tag{3}
\]

The entries of \(b\) remain globally convex polynomials of degree at
most \(d\). Define

\[
 \Lambda=\{\lambda\ge0:C^T\lambda=0,
                              \mathbf1^T\lambda=1\}.
\]

For each extreme point \(\lambda\) of this rational polytope, let
\(P_\lambda(y)=\lambda^Tb(y)\). Strict linear alternatives give

\[
 Y:=\{y:\exists v,\ Cv+b(y)<0\}
   =\{y:P_\lambda(y)<0\text{ for every extreme }\lambda\}. \tag{4}
\]

Here is a direct algorithmic proof, including equality at the boundary.
At a rational query \(y\), solve the rational linear program

\[
 \max_{v,\sigma}\ \sigma
 \quad\text{subject to}\quad Cv+b(y)+\sigma\mathbf1\le0. \tag{5}
\]

It is feasible: set \(v=0\) and take \(\sigma\) sufficiently negative.
The opposite strict box rows bound \(\sigma\) from above, so the optimum
is finite and attained. Its dual is

\[
                  \min_{\lambda\in\Lambda}-\lambda^Tb(y). \tag{6}
\]

If the optimum is positive, its primal point proves strict membership.
If the optimum is nonpositive, choose an optimal extreme point in (6).
It gives \(P_\lambda(y)\ge0\), a violated strict polynomial row.
The equality case must be reported as nonmembership. A bounded rational
LP admits an optimal extreme point, computable with polynomial overhead;
the output must be such a vertex, rather than an arbitrary dual solution
whose encoding could inherit unnecessary query-dependent data.

In the more general formulation without box rows, \(\Lambda\) may be
empty. Then strict linear alternatives give \(Y=\mathbb R^m\), and
(5) is unbounded above. The actual bounded construction avoids this case,
but it must not be mistaken for infeasibility if boxes are omitted.

Every extreme \(\lambda\) has support at most
\(\operatorname{rank}C+1\). Its coordinates are determined by minors
of \(\binom{C^T}{\mathbf1^T}\), independently of \(y\). Hence their
bit lengths have a uniform bound polynomial in the encoding of \(C\).
After separately clearing positive denominators in each
\(P_\lambda\), (4) is a finite family

\[
 Y=\{y:F_j(y)<0\ \forall j\},\qquad
 F_j\in\mathbb Z[y],                               \tag{7}
\]

of globally convex polynomials. Its degree is at most \(d\), the
maximum coefficient bit length is bounded by
\(\ell=f(k,r,d)N^C\), and each row has at most
\(M=\binom{m+d}{d}\) monomials. There may be exponentially many rows.

The LP oracle evaluates the explicit original polynomials at a rational
query, finds one such multiplier, and forms only its selected polynomial.
Its time and output length are polynomial in the explicit input length,
query bit length, and the stated parameter-dependent bounds. Gradients
are those of this **fixed returned polynomial**. Re-optimizing the
multiplier while taking a derivative would instead attempt to
differentiate a nonsmooth maximum and is not this oracle.

## 3. The precise implicit-row consequence of the lattice algorithm

The following is the interface needed here.

**Implicit convex-polynomial integer-feasibility lemma.** Let a bounded
open convex set \(Y\subseteq\mathbb R^m\) have a finite representation
(7). Suppose degree, coefficient-bit, and monomial-count bounds
\(d,\ell,M\) are supplied, together with a rational outer radius.
Suppose a rational-query algorithm either confirms membership in (7) or
returns one violated polynomial, with the stated degree and coefficient
bounds. Then integer feasibility is decidable deterministically in
\(f(m,d)\operatorname{poly}(\ell,\log R_0)\) oracle bit operations.
If each oracle call has polynomial bit cost in its explicit input and
query, the complete algorithm has the corresponding FPT bit bound.

This is a proof-level consequence of the classical lattice algorithm,
not a separately located published theorem with precisely this wording.
The following checks explain why the number of implicit rows drops out.

### 3.1 Every feasible lattice point has uniformly positive volume nearby

Append an integer quadratic row
\(\|y\|_2^2-K<0\), with \(K\) large enough that it is strictly
satisfied throughout the given outer box. This ensures an explicitly
encoded strict bounding row. Increase \(d\) to at least two.

If \(\widehat y\in Y\cap\mathbb Z^m\), then
\(F_j(\widehat y)\le-1\) for every row, by integrality. On an outer
box enlarged by one, a common bound for every row's gradient is, for
example,

\[
 L=\max\{1,\sqrt m\,M d\,2^\ell(R_0+1)^d\}.       \tag{8}
\]

Replace it by a larger rational number if necessary. Every point within
\(\rho=1/(2L)\) of \(\widehat y\) still satisfies all the rows
strictly. Thus \(\operatorname{vol}(Y)\) exceeds the volume of a
rational cube of side \(\rho/m\). The logarithm of its reciprocal is
at most

\[
                  f(m,d)(\ell+\log(R_0+1)+1).        \tag{9}
\]

There is no row-count factor. No feasible center or interior ball is
supplied to the algorithm: (9) is a conditional volume threshold. If
ellipsoid shrinking puts \(Y\) in a smaller-volume ellipsoid, then
\(Y\) contains no lattice point.

### 3.2 A direct rational shallow-cut oracle

Write a rational outer ellipsoid as

\[
 E(A,a)=\{a+x:x^TA^{-1}x\le1\},\qquad A\succ0.
\]

A rational LDL factorization gives \(A=L D L^T\). For each diagonal
entry \(d_i>0\), choose a dyadic rational \(t_i\) with
\(\sqrt{d_i}/2\le t_i\le\sqrt{d_i}\). Its bit length is polynomial
in that of \(d_i\); no irrational square root is part of the output.
Put \(v_i=L e_i t_i\), and query the \(2m\) points

\[
                      y_i^\pm=a\pm v_i/(m+1).       \tag{10}
\]

Every point in (10) lies within ellipsoidal radius \(1/(m+1)\). Their
convex hull contains
\(E(A/[4m(m+1)^2],a)\). To check this, use coordinates
\(L D^{1/2}\): the axis lengths of the resulting cross-polytope lie
between \(1/[2(m+1)]\) and \(1/(m+1)\), and
\(\|x\|_1\le\sqrt m\|x\|_2\).

If all query points belong to \(Y\), convexity shows that this inner
ellipsoid belongs to \(Y\). Thus we have a rounding certificate with
the conservative rational ratio \(\beta=2m(m+1)\).

Otherwise let a query point \(y\) return a violated convex polynomial
\(F\), so \(F(y)\ge0\). If \(\nabla F(y)=0\), convexity gives
\(F(x)\ge F(y)\ge0\) for every \(x\); the strict family is empty.
If \(c=\nabla F(y)\ne0\), convexity gives

\[
 Y\subseteq\{x:c^Tx<c^Ty\}
 \subseteq
 \{x:c^Tx\le c^Ta+\sqrt{c^TAc}/(m+1)\}.           \tag{11}
\]

This is the required rational-normal shallow cut. Polynomial evaluation,
differentiation, and all query coordinates have controlled bit lengths.
The construction uses only membership and one returned polynomial at a
time. It does not search through the defining family.

More precisely, if the current ellipsoid has coefficient bit bound \(H\),
rational minor bounds for LDL give query points of bit length
\(f(m)(H+1)\). Evaluating the returned polynomial's gradient therefore
uses coefficients of bit length at most
\(f(m,d)(\ell+H+1)\). This is linear in the varying bit bounds, as
required by the rational shallow-cut method's precision analysis. One
must use that method with its controlled rounding of ellipsoid data;
unrounded rational updates alone would not prove the stated bit bound.

Although \(Y\) is open, outer cuts remain valid for its closure, while
the inner ellipsoid is contained in \(Y\) itself: it lies in the convex
hull of finitely many strictly feasible points. This distinction preserves
exact feasibility when the inner ellipsoid supplies a lattice point.

### 3.3 Recursion and the absolute input exponent

Apply the rational shallow-cut ellipsoid method with the volume threshold
(9). Its controlled bit implementation, used in Hildebrand--Koppe
Corollary 5.8, returns ellipsoid coefficients with bit lengths at most
\(f(m,d)(\ell+\log R_0+1)\). The per-call bound established above
has the same linear dependence on the varying coefficient and ellipsoid
bit bounds. Changing the rounding ratio to \(\beta=2m(m+1)\) changes
only dimension factors.

For completeness, the lattice subroutines can be implemented entirely
with rational quadratic forms. Use the established deterministic FPT
algorithm for convex integer quadratic optimization over a rational
polyhedron, [Del Pia, Theorem 3](https://arxiv.org/pdf/2311.00099v2),
to minimize \((z-a)^TA^{-1}(z-a)\) over \(z\in\mathbb Z^m\).
An optimal value at most \(1/\beta^2\) returns a point in the inner
ellipsoid. Otherwise that ellipsoid is lattice free. Next minimize
\(d^TAd\) over nonzero integer \(d\), by solving the \(2m\)
subproblems \(\pm d_j\ge1\) and taking their smallest value.
This uses no rational encoding of an irrational square-root lattice
basis. These are applications of an existing quadratic theorem, not of
the polynomial theorem being developed.

The ellipsoidal flatness bound in Hildebrand--Koppe Corollary 3.6 shows
that the outer ellipsoid has width at most \(m\beta\) in the returned
direction. Thus it suffices to branch on the \(O(m\beta+1)\) integer
values \(t\) within \(m\beta/2\) of \(d^Ta\). The center is rational,
so this enumeration does not require an algebraic square root.

Here are the needed bounds on these branch maps; they do not follow just
from saying that a lattice subroutine is polynomial time. If the entries
of \(A,a\) have bit bound \(H\), rational determinant estimates give
\(\lambda_{\min}(A)\ge2^{-\operatorname{poly}(m)(H+1)}\).
Since a shortest \(d\) satisfies
\(d^TAd\le e_i^TAe_i\le2^H\), its coordinates have bit lengths
\(\operatorname{poly}(m)(H+1)\). It is primitive: dividing a
nonprimitive vector by its gcd would decrease its quadratic value.
The enumerated \(t\) have the same type of bit bound.

Extended gcd or Hermite normal form constructs an integer unimodular
matrix \(U\) satisfying
\(d^TU=e_m^T\), with entries and inverse entries of bit length
\(f(m)(H+1)\). A correct parameterization of the lattice hyperplane
is therefore

\[
                         y=U(w,t),\qquad w\in\mathbb Z^{m-1}. \tag{12}
\]

Merely completing \(d\) itself as the last *column* of an integer
basis does not give (12); orthogonality to the first columns is required.
This avoids a notational shortcut in the source's displayed section map.

Query the original oracle at \(U(w,t)\). A returned row becomes
\(F(U(w,t))\), remains convex, has integer coefficients, and retains
degree at most \(d\). It can be expanded in at most
\(\binom{m+d}{d}\) monomials, or evaluated by composition and the chain
rule. Expanding a degree-\(d\) monomial under this affine map adds at
most \(d\) times the map's coefficient bits, plus a dimension and
degree term. Thus the new row coefficient bits are bounded **linearly**
in the old row and map bit bounds, times \(f(m,d)\).

A translated section of the original bounding quadratic may have a
linear term. Retain that valid convex row, and append a fresh
origin-centered strict ball that contains the entire section. Indeed,
\(\|w\|\le\|U^{-1}\|R_0\) for every point in it. A slightly larger
integer-radius ball therefore has coefficient bits \(f(m)(H+\log R_0+1)\)
and changes no feasible points. This supplies the same bounding-row
convention at every recursive level without asserting that translated
sections preserve an origin-centered ellipsoid.

Together with (9), the ellipsoid and branch estimates give a recurrence
\(L_{j+1}\le f(m,d)(L_j+1)\) for all changing coefficient, radius,
and coordinate bit bounds. There are at most \(m\) levels. Thus the
final bound is \(f(m,d)(\ell+\log(R_0+1)+1)\), with an absolute
input-size exponent. This agrees with the substitution accounting in
Hildebrand--Koppe Remarks 5.5--5.6, while separately justifying their
hypothesis on the coordinate-map size. Iterating an unspecified
polynomial bound would not suffice.

The source algorithm's row scans are replaced by the oracle of Section 2;
the volume estimate and row transformation bounds are uniform over all
rows. This completes the implicit-row lemma with an absolute input-size
exponent. Substituting \(m=k+r\) and the supplied encoding bounds proves
the intended \(f(k,r,d)N^C\) mixed-integer feasibility step.

## 4. Primary comparisons and the scope of this import

[Hildebrand--Koppe, *A new Lenstra-type Algorithm for Quasiconvex
Polynomial Integer Minimization*](https://arxiv.org/pdf/1006.4661),
Theorem 1.1, treats an explicit polynomial list. Section 4 isolates the
costs of feasibility and shallow-cut oracles. Definition 2.1, Theorem 2.2,
Theorem 5.7, Remarks 5.5--5.6, and Lemma 6.1 provide the relevant rounding,
recursion, and volume machinery. Their hypotheses use strict integer
polynomial inequalities. These statements and proofs were read directly.
The simpler construction (10)--(11) uses global convexity; their more
general quasiconvex construction handles zero gradients differently.
No claim is made that their main theorem already states the oracle lemma
above.

[Dadush, *Integer Programming, Lattice Algorithms, and Deterministic
Volume Estimation*](https://ir.cwi.nl/pub/25614/Thesis_DDadush.pdf),
Theorem 7.5.1 and Algorithm 7.4, allow a circumscribed convex set with a
separation oracle and a convex objective with a subgradient oracle, but
their bound is in expectation. The earlier
[Dadush--Peikert--Vempala Theorem 4.7](https://arxiv.org/pdf/1011.5666)
also gives expected-time convex integer feasibility through a strong
separation oracle. The thesis definitions require controlled oracle-output
lengths. The inspected sources are alternatives for randomized bounds;
they are not the deterministic import used above.

[Dadush--Eisenbrand--Rothvoss, *From approximate to exact integer programming*](https://arxiv.org/pdf/2211.03859),
Theorems 16--17, give a newer randomized oracle route. The paper's
introduction specifies the relevant geometric and oracle guarantees.
This audit did not use it to remove or replace any of those guarantees.

[Del Pia, *Convex quadratic sets and the complexity of mixed integer
convex quadratic programming*](https://arxiv.org/pdf/2311.00099v2),
Section 5, warns that a polynomial evaluation oracle for a partially
minimized objective does not automatically yield a deterministic FPT
theorem: extension, subgradient, and expected-time assumptions matter.
That warning applies to a casual oracle citation. Here the proof supplies
a different concrete interface: globally convex returned polynomials,
strict integer margins, a deterministic shallow-cut construction, and
controlled integer affine recursion.

Heinz's full article was not independently retrieved in this audit.
Its pertinent lemmas were inspected as stated and used in the
Hildebrand--Koppe primary paper. No stronger theorem is attributed to it.

## 5. Failure modes that the interface excludes

Weak membership in the unrelaxed family is not enough to run the strict
algorithm. For example, replacing \(x^2\le0\) by \(x^2<0\) deletes
its feasible integer point. Replacing it by \(x^2-1<0\) preserves its
integer points, but changes membership at rational queries such as
\(x=1/2\). An oracle for the original family cannot be silently reused
for that transformed family. In an implicit description, separately
clearing denominators makes such per-row shifts particularly easy to
mismatch. The uniform native strict relaxation and LP (5) avoid this issue.

Likewise, a nonnegative combination of polynomials defining a convex set
need not be a convex polynomial unless the native polynomials themselves
are convex. For squared SOCP rows this premise generally fails. The
present gradient-cut argument does not extend the polynomial theorem to
arbitrary indefinite squared-cone representations.

The proof does not require an algorithm enumerating Farkas rows or
recognizing convexity of the input polynomials. Convexity is an assumption
of the problem class. It also does not prove the radius, gap, or rounding
claims listed in Section 1; those remain obligations of the main theorem.
The resulting algorithm may have an impractical parameter factor and
precision requirement.

## 6. Source and verification record

The Hildebrand--Koppe PDF and text were already available in
`common-range-prior-sources/`. The inspected Dadush thesis was saved there
as `dadush-thesis-2012.pdf` and `dadush-thesis-2012.txt`. The Del Pia text
was inspected in `sources-hessian-span-prior/delpia-2025.txt`, whose
filename refers to an earlier local catalog convention; the linked version
is the 2024 v2 paper. The other linked primary papers were opened directly.

The audit consists of primary-source inspection and the reconstructed
oracle proof above. It is not a general novelty determination. Targeted
command

```text
python research-20260927/check_polynomial_oracle_interface.py
```

passed 25 exact strict-projection queries, 144 exact gradient-cut checks,
30 rational ellipsoid test points, and four unimodular lattice section
maps. It also checks a strict boundary,
zero-gradient emptiness, the failure of a naive weak-oracle substitution,
an integer affine polynomial substitution, and the failure of a basis
that merely contains the flatness direction as its last column. These
checks test the displayed identities and edge cases. They do not implement the full
ellipsoid/lattice recursion or prove its bit complexity.

The independent reviewer identified an incomplete initial justification:
the cited coordinate-substitution remark assumes short lattice maps.
Section 3.3 now proves their size using the shortest-direction eigenvalue
bound and extended gcd, specifies the correct row-normal parameterization,
and appends fresh bounding balls. Both the author and reviewer rechecked
these corrections. The review found no remaining substantive gap in this
interface, conditional on the radius, gap, and mesh assumptions of
Section 1 and the stated controlled rational ellipsoid algorithm.

A targeted inline `python -` check passed for the audit's local links,
paired math delimiters, whitespace, control characters, final newline,
and the saved primary source files. No project-wide verification or CI
inspection was performed. Neither document checks nor the symbolic
examples establish the universal bit-complexity result.
