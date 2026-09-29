# A residual obstruction to degree 23 in five variables

Date: 2026-09-28. Status: the conditional proof passed an
[independent proof audit](degree23-residual-obstruction-review.md) and
an additional [independent root review](five-variable-degree-root-review.md).
The latter review did
not rerun the checker. This note concerns a **proper quadratic complete
intersection**. The separate
[positive-base argument](five-variable-positive-base-bound.md) now
removes that hypothesis for the five-variable convex-quartic
application and proves the sharp degree bound 21. No priority claim
is made.

The proposed residual consisting of eight quadratic-complete-intersection
points and one external rational point leaves an unwanted real
projective quadratic zero. More generally, the same obstruction holds for every
residual scheme of odd length at most nine, including nonreduced schemes.
Consequently, under the proper-complete-intersection hypothesis, the
five-variable degree bound improves from the classical conditional bound
23 to 21. The [cyclic family](cyclic-quartic-exponential-degree.md)
attains 21 in five variables.

## 1. Precise statement

Let \(Z\subset\mathbb P^5_{\mathbb Q}\) be a zero-dimensional complete
intersection of five quadrics, of length 32. Suppose

\[
 Z=\Gamma\sqcup R,
 \qquad \Gamma\text{ reduced},\qquad
 \operatorname{length}(R)\in\{1,3,5,7,9\}.
 \tag{1}
\]

Both subschemes are defined over \(\mathbb Q\). Then the common zero set
of all rational quadrics containing \(\Gamma\) contains a real point
of \(R\).

The disjoint decomposition in (1) holds when \(\Gamma\) is a union of
simple points of \(Z\), including a simple Galois orbit. There is no
assumption that \(R\) is reduced.

For the convex rational-SOS quartic application, assume that the quartic
leading form is positive at every nonzero real vector. The homogenized
quadratic factors then have no real common zero at infinity, and their
only real affine common zero is the prescribed minimizer. If five
rational linear combinations of these factors define a proper complete
intersection and are nonsingular at the minimizer, (1) rules out all
odd orbit degrees \(23,25,27,29,31\). Thus the orbit degree is at most
21 under these assumptions. Directions where the quartic leading form
vanishes require the separate reduction in
[the degree-bound note](quartic-zero-degree-adversarial.md).

## 2. The finite-algebra pairing

Choose a rational linear form \(L\) nonzero at every geometric point
of \(Z\), and use the affine chart \(L=1\). Such an \(L\) exists
because there are only finitely many points. Let \(A\) be the
32-dimensional coordinate algebra, filtered by images \(F_iA\) of
polynomials of degree at most \(i\).

The associated graded algebra is the Artinian reduction of the
homogeneous complete-intersection ring by \(L\). It is a complete
intersection of five quadrics in five variables, with Hilbert series
\((1+t)^5\). Its socle is one-dimensional in degree five, and its
products in complementary degrees give perfect pairings.

It follows that there is a rational functional \(\lambda:A\to\mathbb Q\)
such that

\[
 \lambda(F_4A)=0,
 \qquad (a,b)\longmapsto\lambda(ab)
 \text{ is nondegenerate}.
 \tag{2}
\]

Here is the filtered argument for the second assertion. Choose any
nonzero functional on \(A/F_4A\), a one-dimensional vector space.
If \(a\ne0\) has leading filtration degree \(i\), choose an element
in graded degree \(5-i\) pairing nontrivially with its leading class.
Any lift \(b\in F_{5-i}A\) then has \(\lambda(ab)\ne0\).

The decomposition in (1) gives \(A=A_\Gamma\times A_R\). The restriction
\(\lambda_R\) of \(\lambda\) to the second direct factor is also a
Frobenius functional: its multiplication pairing is nondegenerate.

Let \(q\) be a rational quadric vanishing on \(\Gamma\), dehomogenized
in this chart. Set

\[
 B=A_R/\operatorname{Ann}_{A_R}(q),
 \quad \ell=\dim_{\mathbb Q} B,
 \quad \beta(a,b)=\lambda_R(qab).
 \tag{3}
\]

For \(q\ne0\) on \(R\), \(B\) is a nonzero finite algebra and
\(\beta\) is well defined and nondegenerate. Indeed, an element pairs
to zero with every other element exactly when its product with \(q\)
is zero, by nondegeneracy of the original pairing.

Let \(V\subset B\) be the image of affine linear polynomials and put
\(v=\dim V\). Since \(q\) vanishes on the entire direct factor
\(A_\Gamma\), for \(a,b\in V\) we have

\[
 \beta(a,b)=\lambda(qab)=0;
\]

the polynomial \(qab\) has degree at most four. Thus \(V\) is totally
isotropic for a nondegenerate bilinear form on \(B\), and

\[
 2v\leq\ell.
 \tag{4}
\]

This argument uses an ordinary nondegenerate symmetric bilinear form,
not a positive definite form. It applies over \(\mathbb Q\), and
continues to hold after extension to \(\mathbb R\) or \(\mathbb C\).

## 3. The quadratic base gives the other inequality

The projective scheme \(T=\operatorname{Spec}B\), considered inside
the chart, is a closed subscheme of \(R\) and hence of \(Z\). Its
linear span has dimension \(v-1\). The five quadrics defining \(Z\)
restrict to quadrics in this span with a zero-dimensional common zero
set. Choose \(v-1\) generic linear combinations forming a proper
intersection in the span. Scheme-theoretic inclusion and Bézout give

\[
 \ell\leq 2^{v-1}.
 \tag{5}
\]

The case \(v=1\) means \(T\subset\mathbb P^0\), which has length
at most one, so (5) also holds in that case. Neither (4) nor (5)
discards nilpotents or intersection multiplicity.

If \(1\leq\ell\leq9\), the integer inequalities

\[
 2v\leq\ell\leq2^{v-1}
 \tag{6}
\]

force \(v=4\) and \(\ell=8\). For \(v\leq3\), the lower bound
exceeds the upper bound; for \(v\geq5\), the lower bound exceeds nine.
In the surviving case, \(T\) is a complete intersection of three
quadrics in its span \(\mathbb P^3\): it is contained in such a
complete intersection and has the same length eight.

This is a statement about the support algebra of a quadratic
functional as in (3). It does **not** assert that every length-nine
scheme with dependent quadratic evaluations is a complete intersection
or has length eight.

The same proof directly recovers the classical lower bound for an
arbitrary finite scheme \(R_0\) with finite quadratic base. A failure
of independent quadratic conditions gives a nonzero functional
\(\psi:A_{R_0}\to\mathbb Q\) annihilating the images of polynomials
of degree at most two. Define

\[
 J_\psi=\{a:\psi(ab)=0\text{ for all }b\in A_{R_0}\}.
\]

This is an ideal, and the induced multiplication pairing on
\(A_{R_0}/J_\psi\) is nondegenerate by construction. Equations
(4)–(6) apply without requiring \(R_0\) itself to be Gorenstein.
Consequently every scheme of length at most seven with finite
quadratic base imposes independent conditions on quadrics. A scheme
of length nine can impose dependent conditions, as (8) does, but
every nonzero quadratic dependency then has a support quotient of
length eight. This proves the requested small-length distinction
including nonreduced schemes; it is a classical special case, not a
new general Cayley–Bacharach result.

## 4. Real parity finishes the proof

Suppose, contrary to the statement in Section 1, that the quadrics
through \(\Gamma\) have no common real zero on \(R\). There are
only finitely many real geometric points of \(R\). A rational linear
combination \(q\) of a rational basis of these quadrics can be chosen
nonzero at all of them: the excluded choices form finitely many proper
real linear subspaces, whose union cannot contain all rational vectors.

In the real algebra \(A_R\otimes\mathbb R\), each local factor has
residue field \(\mathbb R\) or \(\mathbb C\). At every factor with
real residue field, \(q\) is a unit, so passage to (3) leaves that
factor unchanged. Factors with residue field \(\mathbb C\) have even
real dimension, and so do all their quotients. Therefore

\[
 \ell\equiv\operatorname{length}(R)\pmod 2.
 \tag{7}
\]

By (1), \(\ell\) is odd and at most nine. The residual scheme has a
real geometric point because its length is odd, so \(q\) is nonzero
and \(\ell\geq1\). This contradicts Section 3, which forces
\(\ell=8\). The argument includes arbitrarily nonreduced local
factors, provided they are residual components of the stated complete
intersection.

## 5. The proposed nine-point residual

Use coordinates \(x_0,\ldots,x_5\) on \(\mathbb P^5\). Let

\[
 R_8=\{[1:\pm1:\pm1:\pm1:0:0]\},
 \qquad b=[0:0:0:0:1:0],
 \qquad R=R_8\sqcup\{b\}.
 \tag{8}
\]

The eight points form a \((2,2,2)\) complete intersection in the
subspace \(x_4=x_5=0\). Their Hilbert function is
\(1,4,7,8,8,\ldots\). Adding the external point increases every
positive-degree value by one, so

\[
 H_R=(1,5,8,9,9,\ldots),\qquad h_R=(1,4,3,1).
 \tag{9}
\]

If \(\Gamma\) is linked to \(R\) in a proper \((2,2,2,2,2)\)
complete intersection, the usual complete-intersection linkage formula
gives

\[
 h_\Gamma(t)=h_Z(t)-t^5h_R(t^{-1})
 =1+5t+9t^2+7t^3+t^4.
 \tag{10}
\]

Its coefficients sum to 23, as proposed. Formula (10) is correct,
but it gives no guarantee that the common quadratic base of
\(\Gamma\) excludes \(b\).

In fact every quadric through \(\Gamma\) vanishes at \(b\).
If \(q\) is such a quadric, \(qx_4^2\) is a quartic vanishing on
\(\Gamma\cup R_8\). The Cayley–Bacharach degree of the five-quadric
complete intersection is four, so it also vanishes at the remaining
point \(b\). Since \(x_4(b)=1\), we obtain \(q(b)=0\).
This conclusion also follows from the residue pairing in Section 2.

Thus the Hilbert vector in (10) can describe a degree-23 linked scheme,
but this particular scheme cannot be the sole real quadratic zero
needed by the rational-SOS quartic construction with positive quartic
leading form. In the original chart \(x_5=1\), \(b\) is at infinity:
it contradicts positivity of that leading form, without by itself
exhibiting a second affine zero. In a chart where \(b\) is affine it
instead gives an unwanted affine zero. Thus changing charts does not
remove the real projective obstruction under the stated hypotheses.

An [explicit exact linkage example](degree23-linkage-negative-example.md)
now realizes this Hilbert-vector calculation with an irreducible
degree-23 affine coordinate field. Its common quadratic base retains
\(b\), and the field has three real embeddings; thus it does not
provide the required unique-real-zero construction.

## 6. Literature boundary and limitations

Eisenbud, Green, and Harris,
[*Higher Castelnuovo theory* (1993)](https://eisenbud.github.io/papers/pdfs/1993-002.pdf), printed
pp. 195–199, state the modern Cayley–Bacharach identity for arbitrary
mutually residual closed subschemes and prove the following low-degree
case: a subscheme of a zero-dimensional quadratic complete intersection
which imposes dependent conditions on quadrics has length at least
eight. The boundary case is a three-quadric complete intersection in
\(\mathbb P^3\). Their Theorem 2 includes nonreduced schemes; no
reduced-point interpretation is needed. The local
[PDF](quartic-degree-sources/eisenbud-green-harris-1993.pdf) and
[OCR transcript](quartic-degree-sources/eisenbud-green-harris-1993.txt)
were examined. The OCR loses some weak inequality signs, so exact
endpoint claims should be checked against the PDF.

Their generalized Cayley–Bacharach theorem already gives the
conditional bound 23 for the five-variable application. The argument
above uses classical complete-intersection Gorenstein duality,
elementary isotropic dimension, and real parity to exclude the next
odd case as well. We have not established whether this combination,
or an equivalent real-scheme statement, has appeared previously.

An especially close antecedent for the pairing is Eisenbud and
Popescu,
[*The Projective Geometry of the Gale Transform* (2000)](https://eisenbud.github.io/papers/pdfs/2000-003.pdf), Theorem 7.1,
printed p. 154. For finite Gorenstein schemes of length \(2r+2\) in
\(\mathbb P^r\), they characterize self-association by a generating
dual functional that vanishes on products of linear forms. This is
exactly the pairing structure at the equality \(\ell=2v\) used
above. Their [author preprint](https://arxiv.org/pdf/math/9807127),
Theorem 7.1 and its proof, were examined directly. The pairing
construction and its nonreduced interpretation therefore have clear
classical antecedents; the real-parity consequence is the part whose
precise prior status remains unchecked.

The 1996
[Cayley–Bacharach survey](https://www.ams.org/bull/1996-33-03/S0273-0979-96-00666-0/S0273-0979-96-00666-0.pdf)
states the independent-condition assertion as Conjecture CB11 in
general degrees. Search excerpts were available, but the direct PDF
request returned 403. It was used only to locate terminology, not
as the proof source. Searches for length-nine quadratic
Cayley–Bacharach schemes and totally isotropic evaluation pairings did
not establish priority. Related quadratic Artinian Gorenstein
classification searches were not used: no quadratic Gorenstein
generation conjecture or general Eisenbud–Green–Harris conjecture is
assumed here.

The finite-algebra argument alone does not handle a positive-dimensional
common complex base with no real points: five combinations may fail
to give a proper complete intersection. This was the remaining
obstruction when this note was written. The subsequently verified
[positive-base argument](five-variable-positive-base-bound.md) excludes
that case at degree at least 23 in five variables. Together the two
notes prove the unconditional sharp bound 21 for the stated rational
SOS convex class. The proper-intersection hypothesis remains part of
this note's abstract residual theorem; it has not been removed from
an arbitrary higher-dimensional analogue.

## 7. Targeted verification

The retained exact checker
[check_degree23_residual_obstruction.py](check_degree23_residual_obstruction.py)
checks the ranks, Hilbert differences, and quadratic dependence
support for (8), the linkage arithmetic in (10), and the finite list
of pairs in (6). It also checks a nonreduced sharp example of the
pairing: \(\mathbb Q[t_1,\ldots,t_5]/(t_i^2)\), with the coefficient
of \(t_1\cdots t_5\) as residue functional and \(q=t_1t_2\).
The quotient in (3) has length eight, its linear image has dimension
four, and its multiplication pairing is nondegenerate while that
linear image is totally isotropic.

These calculations do not prove scheme-theoretic Bézout or
complete-intersection duality. The proof above supplies the symbolic
argument conditional on those classical facts. The independent audit
linked at the opening reconstructed those steps and reran the checker;
the root agent supplied a further independent proof read. These reviews
do not establish priority or remove the proper-intersection hypothesis.

Commands run for this note:

- `python research-20260927/check_degree23_residual_obstruction.py`:
  passed all exact assertions.
- A local Python check of this Markdown file: paired display delimiters,
  control characters, and trailing whitespace passed.

No project-wide verification or CI inspection was performed.
