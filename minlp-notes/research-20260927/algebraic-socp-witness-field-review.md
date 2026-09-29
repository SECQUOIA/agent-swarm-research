# One common field for a minimum-norm SOCP witness

Date: 2026-09-28. Status: proof extension and independent review completed;
no unresolved gap was found in the stated encoding bounds.
This note checks the common-field and coefficient bounds needed to recover
an exact witness for second-order cone systems whose coefficients lie in
one explicitly represented real number field. It is a supporting extension
of the existing perturbation and height arguments, not a novelty claim.

## 1. Statement and representation

Let \(K=\mathbb Q(\alpha)\) be given by an explicit primitive irreducible
polynomial \(p\in\mathbb Z[T]\), a rational isolating interval selecting
one real root \(\alpha\), and power-basis representations of every
coefficient. Write \(D=[K:\mathbb Q]\). The total binary input length
\(N\ge2\) includes the dense polynomial and all coefficient vectors,
so \(D\le N\). No succinct representation of an exponentially large
degree is allowed.

Consider a nonempty set

\[
 C=\{x:Ax\le b,\ Ex=e,\
              \|A_ix+b_i\|_2\le c_i^Tx+d_i\ (1\le i\le m)\},
                                                               \tag{1}
\]

with coefficients in \(K\), using its selected real embedding. A supplied
rational box, if present, is included among the original affine rows.
Set

\[
 q_i(x)=\|A_ix+b_i\|^2-(c_i^Tx+d_i)^2,\qquad
 h=\dim_K\operatorname{span}_K\{\nabla^2q_i\}.        \tag{2}
\]

The squared polynomials can be indefinite. Their description always retains
the affine signs \(c_i^Tx+d_i\ge0\). The number \(h\) is the
matrix-span dimension over \(K\), not the common range dimension or the
rational span dimension of the algebraic matrices.

Since \(C\) is nonempty, closed, and convex, it has a unique point
\(x^*\) of minimum Euclidean norm. There are effective absolute constants
in the following bounds:

\[
 [K(x^*):K]\le N^{O(h+1)},\qquad
 [\mathbb Q(\alpha,x^*):\mathbb Q]\le D N^{O(h+1)},      \tag{3}
\]

and every coordinate has an absolute integer minimal polynomial with degree
and coefficient bit length at most \(N^{O(h+1)}\). The tuple
\((\alpha,x^*)\) has a rational univariate representation of total
length \(N^{O(h+1)}\). In particular, an effectively computable rational
box of radius with bit length \(N^{O(h+1)}\) contains \(x^*\).

The degree in (3) is a **joint** degree bound. Multiplying the individual
coordinate degree bounds would instead introduce the ambient number of
variables into the exponent and would not prove the statement.

These are existence and encoding bounds. The recovery algorithm must still
approximate one fixed point and recognize its coordinates or a primitive
generator. This note does not infer a sharper running-time exponent from
the output bound.

## 2. One perturbation and an unknown auxiliary box

Choose a Hessian basis \(B_1,\ldots,B_h\) over \(K\), and introduce
the quadratic lift

\[
 w=(x,y)\in P,\qquad
 F_j(w)=\tfrac12x^TB_jx-y_j=0\quad(1\le j\le h).       \tag{4}
\]

Here \(P\) is a polyhedron over \(K\) encoding all original quadratic
inequalities through the \(y\) coordinates, together with every affine
row and cone sign. The lift is exact and unique at each feasible \(x\).
In particular \(x^*\) has one lift \(w^*\).

Choose an unknown finite integer \(R\) such that \(w^*\) lies strictly
inside \([-R,R]^{n+h}\). Neither a numerical value nor an encoding bound
for \(R\) is needed. On the compact set
\(P\cap[-R,R]^{n+h}\), consider

\[
\begin{split}
 \min_w\quad&\|x\|^2+\varepsilon P_0(w),\\
 |F_j(w)+\varepsilon^2P_j(w)|&\le\varepsilon
                                    \quad(1\le j\le h),
\end{split}                                                   \tag{5}
\]

where the \(P_j\) are fixed generic integer quadratic polynomials with
polynomial coefficient bit lengths.

The genericity argument from the
[nonconvex certificate proof](nonconvex-hessian-span-frontier.md#4-a-quantitative-genericity-lemma)
works on every active affine chart of the **original** polyhedron \(P\),
over \(K\). Restrictions of arbitrary quadratic perturbations are still
surjective onto chart quadratics. Each bad-coefficient polynomial is nonzero
over \(K\); a nonzero polynomial over any characteristic-zero field cannot
vanish on a full integer grid larger than its degree. The degree and number
of bad loci depend on dimensions and polynomial degrees, not on coefficient
rationality. The resulting integer perturbation coefficients therefore have
polynomial bit lengths. This is an existence argument and does not enumerate
the charts or construct the grid.

For sufficiently small positive \(\varepsilon\), the exact lift \(w^*\)
satisfies the perturbed bands, so (5) has minimizers. Every cluster point of
these minimizers as \(\varepsilon\downarrow0\) satisfies (4), by
compactness. Uniform objective convergence and comparison with \(w^*\)
show that its \(x\)-coordinates minimize the original squared norm.
Uniqueness gives \(x=x^*\), and uniqueness of the lift gives \(w=w^*\).

Consequently all minimizers of (5) are strictly inside the auxiliary box for
every sufficiently small positive \(\varepsilon\). Otherwise a sequence
of boundary minimizers would have a boundary cluster point, contradicting
that \(w^*\) is strictly interior. Thus **all auxiliary box rows become
inactive**. They enter none of the active charts, KKT equations, or
coefficient estimates below.

This argument directly controls the global minimum-norm point on an
unbounded set. It avoids first computing a feasible-point radius and then
feeding its bit length into a second bound. If a rational box was originally
supplied, its rows remain in \(P\); only the additional unknown box is
discarded.

## 3. One chart and one support for all outputs

Choose \(\varepsilon_\nu\downarrow0\), avoiding the finite exceptional
values of the genericity conditions. By the finite pigeonhole principle,
retain one active affine chart

\[
                    w=a+Vu,\qquad a,V\text{ over }K,
                                                               \tag{6}
\]

and one oriented active-band subset, of size \(s\le h\), for all
retained minimizers. Every retained point converges to the same \(w^*\).
The coefficients of (6) have polynomial encoding length and polynomial
Weil height, by rational-minor bounds over the represented field. For
example, multiplication by a field element is a rational \(D\)-by-\(D\)
matrix, and an invertible field linear system can be solved as an expanded
rational system of polynomial dimension. No normal closure is needed.

If the chart has dimension zero, \(w^*=a\in K^{n+h}\), and the
claims follow directly. Otherwise let its dimension be \(d>0\). The
genericity conditions give independent active band gradients, an invertible
multiplier Hessian \(M\), and an invertible full bordered KKT matrix.
These are separate conditions; gradient independence and invertibility of
an indefinite \(M\) alone would be insufficient.

Stationarity gives \(u=p/\Delta\), where \(\Delta=\det M\) and
\(p\) is its adjugate numerator. Substitution into the selected band
equations gives

\[
 G_i(\varepsilon,\lambda)=0\quad(1\le i\le s).        \tag{7}
\]

At the selected roots the multiplier Jacobian is nonsingular, by the Schur
complement of the bordered KKT matrix. Every coordinate of \(w\), and
every fixed \(K\)-linear or affine combination of these coordinates,
is a rational output \(B/A\) of (7), with nonzero denominator.
All these outputs use the **same roots, chart, support, and point limit**.

The multiplier degrees are bounded by \(a_0=N^{O(1)}\), uniformly for
all these linear forms. Their coefficient heights can depend on the chosen
linear form; their multiplier degrees do not. One may use \(a_0=2d\)
for the usual common denominator \(\Delta^2\). Thus

\[
                  L=(a_0+1)^s\le N^{O(h+1)}.          \tag{8}
\]

## 4. Local heights and absolute coordinate polynomials

The [finite-quotient lemma over a number field](algebraic-coefficient-span-precision.md#3-the-finite-quotient-lemma-over-k)
is purely algebraic and requires no convexity at other embeddings. Its
nonsingular-root and finite-limit hypotheses were established above at the
selected real embedding. The extension of the nonconvex scalar bounds to
this field, including affine charts and generic perturbations, is also
checked in [the algebraic-threshold note, Section 2](algebraic-threshold-misocp.md#2-the-algebraic-radius-and-gap-inputs-extend-to-this-field).

Let \(E\) be the averaged logarithmic joint local coefficient norm of
the reduced equations and one coordinate output: use coefficient
\(\ell_1\)-norms at archimedean places and maximum coefficient norms at
finite places. Every explicitly represented input field element has Weil
height \(N^{O(1)}\). Affine elimination, determinants, adjugates, and
quadratic substitution preserve

\[
                            E\le N^{O(1)}.           \tag{9}
\]

This estimate bounds the determinant norm before expansion; it does not sum
the heights of exponentially many determinant terms. Generic perturbations
and the rational squared-norm objective obey the same estimate. The formal
parameter \(\varepsilon\) is part of the coefficient norm, so its
numerical size does not enter (9). The unknown radius does not appear at
all.

The field lemma gives a nonzero polynomial \(P\in K[t]\) for each
coordinate \(\xi\), with

\[
\begin{split}
 \deg P&\le L,\\
 H_{\rm aff}(\operatorname{coeff}P)&\le
 W:=L(a_0(s+1)+1)E+\log(L!)+L\log3.
\end{split}                                                   \tag{10}
\]

The selected finite limit is obtained by extracting the lowest nonzero
\(\varepsilon\)-coefficient. Extraction cannot increase any local norm.
Consequently \(W\le N^{O(h+1)}\).

The product formula and local Cauchy bounds imply

\[
 [K(\xi):K]\le L,\qquad h_{\rm W}(\xi)\le W+\log2.   \tag{11}
\]

Its primitive integer minimal polynomial has degree at most \(DL\),
and logarithmic coefficient norm at most

\[
                         DL(W+2\log2).              \tag{12}
\]

All quantities in (11)--(12) are polynomial in \(N\) for fixed \(h\),
even though \(D\) grows with the input. Equivalently, a field norm of
\(P\) supplies a nonzero rational annihilator, but taking a normal closure
or assigning optimization meaning to conjugate systems is unnecessary.
The local-height calculation supplies the coefficient control that a bare
field-norm statement would leave unproved.

## 5. Joint degree: do not multiply coordinate degrees

The coordinates are algebraic over \(K\) by (11), so they generate a
finite separable extension \(E_*=K(x^*)\). The same fixed-support proof
applies to **every** \(K\)-linear form \(\sum_jc_jx_j^*\), with the
same degree bound \(L\). Only the coefficient height changes with
\(c_j\). The primitive element theorem supplies one such linear form
that generates \(E_*\) over \(K\). Therefore

\[
                      [E_*:K]\le L,\qquad
                      [E_*:\mathbb Q]\le DL.         \tag{13}
\]

This argument would fail if separate coordinate minimizers or subsequences
were used and did not describe one common point. Here the one fixed tuple
\(w^*\) and common root sequence precede every choice of output.

For verification against the input, the useful absolute field is
\(E_* = \mathbb Q(\alpha,x^*)\). A representation of
\(\mathbb Q(x^*)\) alone might omit the field generator needed to
evaluate the input coefficients. Formula (13) controls the enlarged field
directly.

## 6. One short absolute representation, including the input generator

Put \(J=DL\), an upper bound on the absolute joint degree. Among the
\(\mathbb Q\)-embeddings of \(E_*\), each distinct pair differs on
at least one coordinate of the generating tuple \((\alpha,x^*)\).
The equal-image condition on an integer linear form in that tuple is one
proper coefficient hyperplane. There are at most \(J(J-1)/2\) pairs.
The integer-grid argument therefore gives coefficients

\[
 0\le c_j\le J(J-1)/2,\qquad
 \gamma=c_0\alpha+\sum_{j=1}^n c_jx_j^*,\qquad
                         E_*=\mathbb Q(\gamma).       \tag{14}
\]

The rational-degree-one case is immediate, including an all-zero primitive
combination when \(E_*=\mathbb Q\). The height inequalities for sums
and products, (11), and the input bound on \(\alpha\) give
\(h_{\rm W}(\gamma)\le N^{O(h+1)}\). Its integer minimal polynomial
therefore has the same coefficient-bit bound. One can also apply the field
finite-quotient lemma directly to the affine output in (14); the extra term
\(c_0\alpha\in K\) changes no multiplier degree.

For completeness, the conversion to coordinate polynomials has polynomial
overhead in the joint degree and these heights. Multiply \(\gamma\)
by the leading coefficient of its integer minimal polynomial to obtain an
algebraic integer primitive generator \(\beta\). Similarly, multiply
each coordinate of \((\alpha,x^*)\) by its own minimal-polynomial
leading coefficient to obtain an algebraic integer. In the basis
\(1,\beta,\ldots,\beta^{e-1}\), where \(e=[E_*:\mathbb Q]\),
the trace-pairing matrix

\[
                     (\operatorname{Tr}_{E_*/\mathbb Q}
                                        \beta^{i+j})_{0\le i,j<e}
                                                               \tag{15}
\]

is an integer matrix of nonzero determinant, by separability. Its entries
and the trace right-hand sides have polynomial bit lengths in
\(n,J,W\) and the input height bound: conjugate Cauchy bounds control
every term in each trace. Cramer's rule gives rational coordinate
polynomials of the same polynomial bit size. Divide the coordinate scales
back out. Integer minimal-polynomial root separation gives a rational
isolating interval selecting the intended real \(\beta\), also with
polynomially many bits. The resulting total length is \(N^{O(h+1)}\),
and includes a polynomial representing the original \(\alpha\).

Finally, (12) and Cauchy's root bound give one effectively computable
\(B=N^{C(h+1)}\) such that

\[
                      |x_j^*|<2^{B+2}\quad(1\le j\le n).
                                                               \tag{16}
\]

The box in (16) contains the canonical point itself. It is not merely a box
meeting the feasible set.

## 7. Consequences, limitations, and prior machinery

The rational-coordinate approximation argument in
[the rational SOCP recovery note](socp-exact-witness-recovery.md) uses only
convexity, exact feasibility decisions, and rational norm thresholds.
It therefore targets this same point when the original coefficients belong
to \(K\), using the common-field feasibility theorem. The added norm
cone has rational squared Hessian \(8I\), so it increases the span over
\(K\) by at most one. Appending \(\alpha\), whose exact isolating
description is already supplied, to the approximation tuple allows ordinary
absolute common-field recovery and verification. Those algorithmic steps
are separate from the existence proof above.

If the printed box or recognition precision has \(N^{O(h+1)}\) bits,
feeding it into a feasibility runtime expressed in total input length can
increase the exponent further. The safe algorithmic conclusion is polynomial
time for each fixed \(h\), with an exponent depending on \(h\).
An \(N^{O(h+1)}\) output bound alone does not establish that same sharp
running-time exponent. No fixed-parameter bound \(f(h)N^C\) is claimed.

The proof uses established primitive-element, trace-pairing, height, and
finite-quotient machinery. The reviewed
[number-field height note](algebraic-coefficient-span-precision.md#7-sources-and-verification-limits)
records the primary sources for heights and local arithmetic. The present
extension combines that machinery with the nonconvex generic-band proof;
it does not apply a native-PSD theorem directly to indefinite squared SOC
Hessians. Convexity is used for the unique selected point at the real
embedding, not for the algebraic elimination or the conjugate systems.

## 8. Verification and a nontrivial field-extension example

The [independent field review](algebraic-socp-witness-field-independent.md)
checks the unknown-box argument, fixed common tuple for all linear outputs,
relative and absolute joint degree, coefficient heights, primitive-element
selection, trace conversion, and isolating intervals. A separate subreview
checked the primitive-element and finite-grid reasoning. The review also
records an exact quartic field-conversion calculation. These reviews rely
on the previously reviewed genericity and finite-quotient lemmas.

As a direct SOCP check, put \(K=\mathbb Q(\alpha)\),
\(\alpha=\sqrt2\), and \(s=3+\alpha\). The system

\[
 \|(1+\alpha/2,1,\alpha/2)\|\le x,\qquad
 \|(2x,s-1)\|\le s+1                                  \tag{17}
\]

has the unique feasible point \(x=\sqrt{3+\sqrt2}\). The first
squared residual is \(s-x^2\), with its sign requiring \(x\ge0\);
the second is \(4x^2-4s\), and \(s+1>0\). Thus equality is forced.
The two squared Hessians are \(-2\) and \(8\), so \(h=1\).
The witness has relative degree two over \(K\) and absolute degree four,
with minimal polynomial

\[
                          X^4-6X^2+7.
\]

The input generator is recovered by \(\alpha=x^2-3\). A targeted inline
SymPy command checked the norm and residual identities modulo
\(\alpha^2-2\), both Hessians, irreducibility of this quartic, and the
generator identity modulo it. All assertions passed. This finite example
checks representation and sign details; it does not prove the universal
degree or height bounds.

No Lean formalization, project-wide verification, or CI inspection was run.
A targeted inline Python check passed for this note's final newline,
trailing whitespace, control characters, paired math delimiters, and all six
local links. These checks concern document integrity, not the theorem.
