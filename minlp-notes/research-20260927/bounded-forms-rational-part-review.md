# Rational-part bit bounds for a semialgebraic linear subspace

Independent review of one lemma in the bounded-forms argument, 2026-09-28.
The conclusion below is an existential encoding bound. It is not an algorithm
whose running time is independent of the length of the Boolean formula.

## Verdict and height convention

Let a real linear subspace \(A\subseteq\mathbb R^k\) be defined by a finite
Boolean combination of sign conditions on integer polynomials of degree at
most \(D\) and coefficient magnitude at most \(2^\tau\). Assume
\(k,D,\tau\ge1\). Then \(A\cap\mathbb Q^k\) has a rational vector-space basis
whose coordinate numerator and denominator **bit lengths** are bounded by

\[
 (\tau+1)(2D+1)^{O(k)}.
\tag{1}
\]

This bound does not depend on the number of atoms or Boolean operations. It
also applies when \(A\) itself is not a rational subspace. An empty basis is
allowed when its rational part is zero.

If “height” means absolute numerator or denominator magnitude, a bound of the
form \((DH)^{O(k)}\), with input coefficient magnitudes at most \(H\), is
false. For \(D\ge2\), the line

\[
 A_D=\{(2^Dt,t,2t):t\in\mathbb R\}
\]

has the formula

\[
 [y\ne0\ \wedge\ z-2y=0\ \wedge\ xy^{D-1}-z^D=0]
 \quad\vee\quad [x=y=z=0].
\]

The dimension is three, the degree is \(D\), and every coefficient has
magnitude at most two. If all numerators and denominators of a nonzero
rational vector on this line had magnitude at most \(M\), then
\(|x/y|\le M^2\). Hence \(M\ge2^{D/2}\). There is no conflict with (1).

## 1. An algebraic basis with bounded absolute logarithmic heights

Write \(d=\dim A\). The cases \(d=0\) and \(d=k\) are immediate, so suppose
\(0<d<k\). Choose a coordinate set \(I\subseteq\{1,\ldots,k\}\) of size
\(d\) such that the coordinate projection \(\pi_I:A\to\mathbb R^d\) is an
isomorphism. For each standard basis vector \(e_j\in\mathbb R^d\), let
\(a_j\) be the unique point of

\[
 \{x\in A:x_I=e_j\}.
\tag{2}
\]

The vectors \(a_1,\ldots,a_d\) form a basis of \(A\). The formulas (2) add
only degree-one polynomials with coefficients in \(\{-1,0,1\}\).

Fix one such point \(a_j\). Among all polynomials appearing in its singleton
formula, retain those that vanish at \(a_j\). Every other polynomial has a
fixed, nonzero sign throughout some neighborhood of \(a_j\), because the
list is finite. Any common zero of the retained polynomials in that
neighborhood has exactly the same full sign pattern as \(a_j\), so it
satisfies the singleton formula. Thus \(a_j\) is an isolated **real** common
zero of the retained polynomials. Complex isolation is unnecessary.

Select a basis of their coefficient vectors over \(\mathbb Q\), using a
subset of the retained polynomials themselves. There are at most

\[
 M=\binom{k+D}{k}
\]

members in this subset. It has exactly the same common zero set. No new
polynomial coefficients are formed, so its degrees and coefficient magnitudes
retain the original bounds. This is the step that removes the atom count.

Hansen, Koucký, Lauritzen, Miltersen, and Tsigaridas, *Exact Algorithms for
Solving Stochastic Games*, February 20, 2012 version, Theorem 23, gives explicit
coordinate bounds for isolated real zeros of an integer polynomial system.
Applied to this subset, each coordinate of \(a_j\) is a root of a nonzero
integer polynomial with degree at most

\[
 \delta=(2D+1)^k
\]

and coefficient magnitudes at most \(2^L\), where a valid uniform choice is

\[
 L=2k\bigl(\tau+4k\log_2(DM)\bigr)(2D+1)^{k-1}.
\tag{3}
\]

The theorem and its proof are in Section 5, printed pages 19–23 of the
[author-hosted manuscript](https://www.cs.au.dk/~arnsfelt/Papers/exactstochastic.pdf).
The source was inspected directly. Its bound applies to isolated real zeros,
including zeros lying on a positive-dimensional complex variety.

Let \(h_2(\alpha)\) denote absolute logarithmic Weil height, with logarithms
in base two. If an algebraic number is a root of an integer polynomial of
degree at most \(\delta\) and coefficient magnitudes at most \(2^L\), then

\[
 h_2(\alpha)\le B:=L+\tfrac12\log_2(\delta+1).
\tag{4}
\]

Indeed, the primitive minimal polynomial divides the given polynomial over
\(\mathbb Z\). Mahler measure is multiplicative and is at least one for a
nonzero integer polynomial. Its measure is therefore at most the Euclidean
coefficient norm of the given polynomial. Dividing its logarithmic measure
by the algebraic degree only improves the stated bound. In particular every
entry of the normalized basis has height at most \(B\), and the same is true
of every algebraic conjugate of every entry.

## 2. Taking the rational part without a compositum-degree loss

Let \(\overline{\mathbb Q}\subset\mathbb C\) be fixed and put

\[
 L_A=\operatorname{span}_{\overline{\mathbb Q}}
       \{a_1,\ldots,a_d\},\qquad
 W=\bigcap_{\sigma\in\operatorname{Gal}(\overline{\mathbb Q}/\mathbb Q)}
          \sigma L_A.
\]

The use of all algebraic conjugates, including nonreal ones, is deliberate.
A rational vector lies in \(L_A\) if and only if it lies in every conjugate
\(\sigma L_A\). Also, a rational vector in \(L_A\) belongs to the original
real space \(A\), because its coefficients in the normalized basis are its
real coordinates indexed by \(I\). Consequently

\[
 W\cap\mathbb Q^k=A\cap\mathbb Q^k.
\tag{5}
\]

An annihilating system for \(L_A\) is

\[
 x_\ell-\sum_{j=1}^d(a_j)_\ell x_{I_j}=0,
 \qquad \ell\notin I.
\]

Every coefficient in every conjugate of this system has height at most
\(B\). From all the conjugated rows, select at most \(k\) linearly
independent rows spanning their joint row space. This is possible by ordinary
finite-dimensional linear algebra, even though the displayed family is
indexed by all automorphisms. Let \(C\) be the resulting \(r\times k\)
matrix, of rank \(r\le k\). Then \(W=\ker C\).

The space \(W\), and hence its annihilator, is invariant under every such
automorphism. The unique reduced row-echelon matrix of the annihilator is
therefore fixed entrywise by every automorphism. Its entries lie in
\(\mathbb Q\). This proves rational descent without computing a number
field, a normal closure, or a compositum.

Choose an invertible \(r\times r\) column minor \(C_J\). A normalized basis
of \(\ker C\) is obtained by setting each free coordinate in turn to one,
the others to zero, and solving for the pivot coordinates. Each nontrivial
coordinate is a ratio of two determinants of \(r\times r\) matrices with
entry heights at most \(B\). For any such matrix \(E\), the local triangle
inequality at archimedean places and the ultrametric inequality at finite
places give

\[
 h_2(\det E)\le\sum_{i,j}h_2(E_{ij})+\log_2(r!)
             \le r^2B+\log_2(r!).
\]

The product formula then gives, for every resulting coordinate \(q\),

\[
 h_2(q)\le 2k^2B+2\log_2(k!).
\tag{6}
\]

These coordinates are rational by the descent argument. For a reduced
rational number \(q=u/v\), with \(v>0\), its height is exactly
\(h_2(q)=\log_2\max\{|u|,v\}\). Thus (6), with one extra bit for the usual
integer bit-length convention, is the required rational basis bound.
Equations (3)–(6) imply (1).

## Scope of the conclusion

- The bound concerns a basis over \(\mathbb Q\) of \(A\cap\mathbb Q^k\).
  It does not say that \(A\) has a rational basis, or that rational vectors
  are dense in \(A\).
- The selected coordinate chart, vanishing atoms, and conjugated rows are
  existential choices. The argument does not by itself compute them within
  the bit bound, or avoid reading a long explicit input formula.
- An attempted proof that encodes all basis points in one primitive field
  can incur an unnecessary product of extension degrees. Absolute heights
  and Galois-invariant row spaces avoid that loss.
- Rational input polynomials can first be cleared of denominators. The
  parameter \(\tau\) in this statement is the coefficient bit bound after
  that operation; a bound on individual rational coefficient numerator and
  denominator bits acquires at most the number of monomials as a factor.
- This is a consequence of established isolated-real-root bounds and
  elementary descent and height estimates. No novelty is claimed for the
  lemma. The contribution of this review is to validate its precise use and
  rule out an incorrect absolute-height interpretation.

## Verification record

The isolated-zero reduction, the Galois descent, and the determinant-height
argument were checked independently of the parent manuscript. No numerical
test can establish these universal claims, so no computational experiment
was substituted for the proof. Only the new Markdown file received local
formatting checks; no project-wide checks or CI inspection were performed.
