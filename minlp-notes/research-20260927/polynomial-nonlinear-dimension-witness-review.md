# Bounds audit for polynomial optimizer witnesses

Date: 2026-09-28. Scope: the arithmetic and recovery argument for the
optimization extension of
[polynomial feasibility with few nonlinear coordinates](polynomial-nonlinear-dimension-frontier.md).
The complete draft of
[the optimization theorem](polynomial-nonlinear-dimension-optimization.md)
was read, with detailed checks of Sections 3--8. This audit assumes the
separately reviewed generic convex epigraph value bound, the exact
polynomial feasibility oracle, and the classical finite-attainment result.
It checks their arithmetic interfaces, the selected-point formula, degree
and height accounting, and conversion to a full continuous optimizer.

**Finding.** The assembled argument gives \(f(k,r,d)N^C\) encoding and
recovery bounds, with an absolute input exponent, provided the full tuple
includes the optimal value and optimal-face feasibility queries use one
fixed compact box. The box is essential to the query equivalence; equality
of an unboxed infimum with the target value need not imply intersection
with the optimal set without a separate attainment theorem. The completed
draft includes these conditions and proves a uniform box for every optimal
integer assignment within its integer search box. No gap was found in the
reviewed arithmetic and recovery steps.

## 1. Conditional setup

Fix a rationally encoded integer assignment whose bit length is already
bounded by \(f(k,r,d)N^C\). Write the continuous fiber as

\[
 Cv+p(u)\le0,\qquad
 q_0(u,v)=C_0v+p_0(u),                              \tag{1}
\]

where all matrices are rational and constant and all polynomials have
degree at most \(d\). The objective and constraint polynomials are convex
in the original formulation. The objective's nonlinear variables are
included in the same \(r\)-dimensional core \(u\). Assume the finite
optimal value \(\theta\) is attained in this fiber and has a supplied
integer minimal polynomial and rational isolating interval, with degree
\(f(k,r,d)\) and coefficient/endpoint bits \(f(k,r,d)N^C\).

The optimum set is convex: it equals the original feasible set intersected
with the convex sublevel \(q_0\le\theta\). Its projection onto \(u\)
is also closed. Indeed, append just the objective upper row

\[
                         C_0v+p_0(u)\le a,
\]

and eliminate \(v\) by Farkas' lemma. This gives a finite, potentially
exponential, basic closed description

\[
                     P_j(u,a)\le0\quad(1\le j\le S). \tag{2}
\]

Its degree is at most \(\max(d,1)\), and individual coefficient bits
have the stated FPT bound. The matrix eliminated by Farkas remains
rational and constant. At \(a=\theta\), the original rows and objective
upper bound describe exactly the optimum set. Adding both signs of the
objective equality would also be valid for the arithmetic argument, but
is unnecessary here.

Consequently that projection has a unique minimum-norm point \(u^*\).
The same reasoning applies if rational coordinate boxes have already been
appended. All choices of a box must be fixed before defining the selected
point.

## 2. Quantifier elimination supplies the needed coordinate bounds

Let \(M_\theta(a)=0\), \(\ell<a<h\), select \(a=\theta\).
For a free scalar \(t\), a formula selecting coordinate \(u_i^*\) is

\[
 \begin{split}
 \exists a\,\exists u\;[&M_\theta(a)=0\ \wedge\ \ell<a<h
       \ \wedge\ t=u_i\ \wedge\ \bigwedge_jP_j(u,a)\le0\\
 &\wedge\ \forall w\bigl(
       (\bigwedge_jP_j(w,a)\le0)
             \Longrightarrow \|u\|^2\le\|w\|^2\bigr)]. \tag{3}
 \end{split}
\]

The existential block has \(r+1\) variables and the universal block has
\(r\). There is only one free scalar. The maximum degree is
\(D=\max\{d,\deg M_\theta,2\}=f(k,r,d)\), and maximum coefficient
bits are \(\tau=f(k,r,d)N^C\).

The coefficient-sensitive quantifier-elimination theorem in
[Basu's survey, Theorem 2.27](https://arxiv.org/abs/1409.1534)
gives output degrees depending only on \(D\) and block sizes, and
individual output coefficient bits bounded by \(\tau\) times such a
factor. These particular bounds do not depend on the number of predicates;
the output count and computation time do. The full displayed theorem,
including its integer coefficient bound, was inspected in the local author
survey. The original
[Basu--Pollack--Roy paper](https://doi.org/10.1145/235809.235813),
Theorem 1.3.1 on pages 1004--1005 together with the preceding definition
of a well-behaved algorithm, was also inspected. That definition bounds
intermediate and output integer bit sizes by input bit size times the
algebraic part of the complexity, separately from the predicate-count
factor.

The formula (3) defines a singleton. Therefore at least one nonzero
univariate polynomial in an equivalent quantifier-free formula vanishes
at \(u_i^*\). If none did, every nonconstant sign atom would be locally
constant near that coordinate, and the formula would hold on an interval,
contradicting uniqueness. Identically zero polynomials do not change this
argument. It follows that \(u_i^*\) has an integer annihilator of degree
\(f(k,r,d)\) and coefficient bits \(f(k,r,d)N^C\). Passing to its
minimal-polynomial factor preserves that form.

No algorithm constructs the exponential family or performs this quantifier
elimination. Only its effective degree and coefficient bounds are used.

Include the value in the field:

\[
                    K=\mathbb Q(\theta,u_1^*,\ldots,u_r^*).
\]

Multiplying the \(r+1\) individual degree bounds still gives
\([K:\mathbb Q]\le f(k,r,d)\), because \(r\) is a parameter.
This is sufficient for a general FPT statement. It does not give the
sharper singly exponential degree constant obtained by the quadratic
critical-point proof. Multiplying degrees of all eliminated coordinates
would be different: their number is part of the ordinary input size and
must not appear in such an exponent.

### 2.1 The degree bound does not require the integer dimension

The completed draft subsequently sharpened the algebraic degree to
\(g(r,d)\), independently of \(k\). This refinement is valid. Fix
any attained optimal integer assignment. Its epigraph in the single real
threshold coordinate is obtained by eliminating just \(r\) variables
from the constant-matrix Farkas family, whose degree is at most
\(\max(d,1)\). The finite endpoint \(\theta\) therefore has an
annihilator of degree \(g(r,d)\). The assignment's coordinates may
affect coefficient heights, but cannot affect this degree bound.

Using this bound for \(M_\theta\), the degree and variable counts in
(3) depend only on \(r,d\). Each selected \(u_i^*\), and hence
the field \(K\), has degree bounded by another function \(g(r,d)\).
The affine coordinates stay in this field by Section 3. The integer
dimension still enters the height and runtime bounds through the bounded
optimal integer assignment and the generic epigraph value theorem. This
sharpening does not remove either of those inputs.

## 3. The affine optimal fiber preserves the field

At \(u=u^*\), append the rational-normal objective upper row

\[
                   C_0v\le\theta-p_0(u^*).          \tag{4}
\]

Together with the original rows, this is a nonempty polyhedron
\(Av\le b^*\), with rational matrix \(A\) and right-hand side in
\(K\). Its unique minimum-norm point has the active-row formula

\[
                  v^*=A_I^T(A_IA_I^T)^{-1}b_I^*.    \tag{5}
\]

The rational matrix in (5) has coefficient bits polynomial in the input
matrix bits and dimensions. Every coordinate of \(v^*\) lies in \(K\);
no additional field extension is needed. The empty active set gives zero,
and a zero-dimensional affine fiber has no coordinates to recover.

For an explicit height check, let \(D_0\) be a common integer multiple
making \(\theta\) and every \(u_i^*\) integral after multiplication.
The product of their minimal polynomials' leading coefficients suffices,
so \(\log D_0\le(r+1)f(k,r,d)N^C\). Polynomial evaluation of degree
at most \(d\) uses \(D_0^d\), rather than the square used in the
quadratic proof. Clear the remaining rational denominators in (5).
These include both the polynomial coefficients in the right-hand side and
the active-matrix coefficients.
All conjugates are bounded by the coordinate root bounds and direct
degree-\(d\) polynomial evaluation. A field norm of degree
\([K:\mathbb Q]\le f(k,r,d)\) then gives an integer annihilator for
each \(v_j^*\), with coefficient bits \(f(k,r,d)N^C\).

This argument tolerates a polynomial number of matrix entries and output
coordinates. Their denominators and coefficient sums introduce fixed
polynomial factors in \(N\); they do not introduce a power of \(N\)
depending on \(k,r,d\).

## 4. The necessary approximation oracle

Fix a rational compact box containing an optimizer and work on the
corresponding boxed optimum set. For any extra rational weak constraint
family \(G\),

\[
 \text{the boxed optimum set meets }G
 \quad\Longleftrightarrow\quad
 \min\{q_0:(u,v)\text{ satisfies the box, original rows, and }G\}
                         =\theta,                   \tag{6}
\]

provided the right side treats an empty feasible set separately. Compactness
and continuity make every nonempty minimum attained. Without the box,
equality of infima would not justify (6).

Exact boxed value recovery from rational threshold feasibility gives an
oracle for (6), assuming the separately proved uniform algebraic value
bounds. Its queries keep rational data. To approximate the canonical
\(u^*\), use \(G\) consisting of rational bounds on \(\|u\|^2\)
and current coordinate intervals. The norm row has degree two and uses
only the existing \(u\) coordinates. The projection inequality places
all points in a sufficiently tight norm sublevel near \(u^*\), and
coordinate bisection then gives an approximation to that same tuple at
every requested precision. The fixed-box restart convention from
[common-range witness recovery](common-range-witness-recovery.md) applies.

Approximate \(\theta\) from its selected univariate representation.
Together with the \(u^*\) oracle, this approximates \(b^*\) in (4)--(5).
Degree-\(d\) polynomial evaluation on a known coordinate box needs only
\(f(r,d)\) times the input, radius, and requested accuracy bits. Apply
the rational outward-right-hand-side QP construction and Hoffman estimate
from Section 5 of the linked witness note. The matrix is rational and
unchanged, so its uniform Hoffman bound remains valid. That procedure
approximates the particular \(v^*\) in (5).

The full tuple \((\theta,u^*,v^*)\) now has degree and height bounds
\(f(k,r,d)\) and \(f(k,r,d)N^C\), and a certified approximation
oracle with corresponding FPT cost. The reviewed common-field recognition
algorithm has polynomial overhead in these quantities. Hence full exact
optimizer output has the desired FPT form, conditional on the boxed value
oracle and existence of the uniform optimizer box. Those two conditions
are separate parts of the optimization theorem, not consequences of this
coordinate argument alone.

## 5. Direct comparison with the complete optimization draft

The following interfaces were checked directly against Sections 3--8 of
the complete optimization draft.

1. Farkas elimination of the constant matrix on \(v\) produces
   individual polynomial coefficient bounds; it does not take a product
   of denominators over the exponential row collection. Quantifying only
   the \(r\) nonlinear continuous coordinates gives the degree and height
   form required by the general convex epigraph value theorem.
2. The value and optimal-integer-vector bounds are effective before their
   corresponding objects are known. The root bound therefore supplies
   the unboundedness threshold used on the original unboxed model. Value
   bisection and scalar recognition use rational feasibility queries and
   do not call continuous optimizer recovery.
3. Section 5 proves the canonical-point bounds uniformly for every
   optimal integer vector within its bounded integer box. This is stronger
   than existence of one small optimizer. It ensures that the integer
   vector later selected by coordinate bisection has its own canonical
   pair inside the same continuous box. There is no enumeration of the
   integer box in this argument.
4. Both components of the unboxed canonical pair lie in the fixed box:
   the minimum-norm projected point \(u^*\) and its minimum-norm affine
   lift \(v^*\). Consequently the boxed optimal projection contains
   \(u^*\) and is a subset of the unboxed projection. Its minimum-norm
   point is therefore precisely the same \(u^*\). The approximation
   oracle consistently selects the tuple whose arithmetic bounds were
   proved. Restarting coordinate intervals for every new accuracy request
   preserves this property.
5. At \(p\)-bit requested accuracy, norm and coordinate bisection require
   only polynomially many bits in \(p\) and the known box length.
   Polynomial evaluation changes this by a factor depending on the degree
   and nonlinear dimension. The outward-right-hand-side QP remains a
   rational problem; its rational normal matrix is unchanged by algebraic
   value and coordinate evaluations.
6. The nesting depth is fixed: tuple recognition calls an approximation
   oracle, that oracle calls boxed value recovery, and value recovery calls
   rational feasibility and scalar recognition. It does not recursively
   call tuple recovery. Each stage has an absolute polynomial exponent in
   its input length. The number of integer coordinates changes the number
   of bisection queries, not this nesting depth. Substituting
   \(p\le f(k,r,d)N^C\) into this fixed composition preserves an absolute
   exponent of \(N\).

The cases \(r=0\) and \(n=0\) remove the corresponding recovery stages;
they do not require a different field argument. The final exact substitution
check certifies the returned point's feasibility and objective value. Its
global optimality additionally relies on the separately established value
algorithm.

## 6. Verification scope

This audit rederived the singleton-polynomial argument, joint-degree
accounting, field preservation, denominator exponent, and compactness
requirement in (6). It read the coefficient-sensitive quantifier-elimination
statement directly. It then checked the complete draft's use of these
bounds, its uniform optimizer box, and its coefficient-sensitive recovery
composition. The underlying general convex epigraph theorem, exact
feasibility theorem, and Bank--Mandel finite-attainment theorem were not
re-proved here. This focused audit is not a substitute for an independent
review of the full theorem and its prior comparison.

No additional numerical tests are needed for these formula and parameter
checks. The exact QP/Hoffman recovery component already has independent
proof reviews and targeted symbolic tests. A targeted `python -` document
check passed for this file: final newline, trailing whitespace, control
characters, paired mathematical delimiters, and its three local links.
No project-wide verification, CI inspection, or formalization is claimed.
