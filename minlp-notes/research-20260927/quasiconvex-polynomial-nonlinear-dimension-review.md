# Full adversarial review of the quasiconvex polynomial extension

Date: 2026-09-28. Scope: the complete
[quasiconvex polynomial optimization note](quasiconvex-polynomial-nonlinear-dimension-frontier.md),
including its implicit projection, feasibility, exact value, full optimizer,
and intrinsic-direction claims. This reviewer did not develop the main
argument. The review read the convex feasibility and optimization proofs,
their oracle and arithmetic audits, the reviewed quasiconvex mixed-value
theorem, and the new projection, oracle, and prior audits.

**Finding.** No substantive gap was found in the extension, conditional on
the explicitly imported theorems and reviewed dependencies. The exact
bound remains \(f(k,r,d)N^C\), with an absolute input exponent. The
common-field degree can use the stronger bound \(g(r,d)\) from the
convex optimization note. The constant-coefficient lemma and the use of
continuous Hessian blocks are also valid under global quasiconvexity;
they do not need a positive-semidefinite Hessian argument.

This is a conditional mathematical audit, not formal verification or a
novelty certificate. Qualitative attainment and quasiconvex integer
separation are established results. The contribution should remain a
structural exact-complexity and output theorem, with priority unconfirmed.

## 1. Projection preserves the required row class

For a native row \(c^Tv+p(y)\), \(c\ne0\), choose \(a\) with
\(c^Ta=1\). The zero sublevel restricted to \(v=ta\) is the
hypograph of \(-p\). Convexity of that sublevel implies convexity of
\(p\). Thus every row involving the eliminated block is convex as a
function, even when the native assumption is only global quasiconvexity.
Merely quasiconvex rows must have zero eliminated-variable coefficients.

The normalized Farkas set is a compact rational polytope. If its vertex
\(\lambda\) gives a zero matrix row positive weight less than one,
subtracting that weight times the corresponding unit vector leaves a
second normalized feasible multiplier. This contradicts extremality.
Every vertex therefore gives either one zero-matrix native row or a
nonnegative combination of convex rows. Each projected polynomial is
globally quasiconvex. This is a special property of the constant-matrix
model; arbitrary sums of quasiconvex polynomials would not suffice.

The finite weak Farkas description proves that the projected set is
closed. Its convexity also follows directly by projection of an
intersection of convex sublevels. No general assertion that a closed
convex set has closed projections is being used.

For strict relaxed rows, phase I is a rational LP at each fixed query.
Its finite optimum, ensured by opposite box rows, is negative exactly
when the projected strict system is feasible. An optimal dual vertex
returns a violated member of the same fixed family otherwise, including
at equality. Vertex denominators depend on the constant matrix, not the
query coordinates. Clearing each returned polynomial separately by a
positive multiplier preserves its strict sublevel and coefficient bound.

The phase-I scalar must not be treated as another native variable subject
to a global quasiconvexity promise: \(p(y)-s\) need not be jointly
quasiconvex. The proposed proof does not do this. When the eliminated block
is empty, native rows can be tested directly. If the normalized Farkas
polytope is empty before boxes are added, the weak and strict alternatives
are interpreted vacuously rather than as infeasibility.

## 2. The rational quasiconvex shallow cuts are valid

I independently checked the argument in Section 3 against the
[separate oracle review](quasiconvex-polynomial-oracle-review.md).

The constant-line implication uses both global quasiconvexity and
polynomiality. A closed convex sublevel containing a complete line and
one point contains the parallel line through that point. Therefore a
restriction parallel to a constant line is bounded above on the whole
real line. A nonconstant univariate quasiconvex polynomial cannot have
this property: its odd-degree or positive even-degree tail is unbounded
above, whereas a negative even-degree leading term violates quasiconvexity
between two distant endpoints. Invariance along every vector of a basis
then implies global constancy.

The rational LDL directions have ellipsoidal lengths between one half
and one. The proposed \(2s\) test points form a cross-polytope
containing the claimed inner ellipsoid with
\(\beta=4s(s+1)\). If all test points are strictly feasible, their
entire convex hull lies in the strict set. Thus the closed inner ellipsoid
is contained in the strict set itself, not merely its closure.

For a rejected polynomial \(F\), the two nearby-gradient searches are
correct. If \(F(c)<0\), every continuation beyond the rejected test
point on the same ray remains outside the strict sublevel. Among \(D\)
distinct samples, its nonzero derivative of degree at most \(D-1\)
cannot vanish everywhere. If \(F(c)\ge0\), negative samples on
both sides of any basis line would put \(c\) in the strict sublevel.
One whole sample side is therefore nonnegative; a nonconstant restriction
again has a nonzero derivative at one of its \(D\) samples. Both
constructions stay strictly inside ellipsoidal radius \(1/(s+1)\).

Differentiating the segment from the selected violation \(w\) toward
a strictly feasible point gives the weak supporting inequality
\(\nabla F(w)^T(x-w)\le0\). This yields the required shallow cut.
The normal and the stronger offset \(\nabla F(w)^Tw\) are rational.
The square root in the displayed shallow-cut guarantee need not be encoded.
The rejected-zero-gradient shortcut is correctly absent; \(F(x)=x^3\)
at zero would refute it.

I reread Hildebrand--Koppe's primary text, Sections 5.2--5.3, especially
Lemmas 5.2 and 5.4, Corollary 5.3, and Theorem 5.7. These supply the
existing quasiconvex geometric machinery. The note reconstructs it with
rational sampling and an implicit-row interface; it should not claim a
new separation principle.

## 3. Feasibility and the absolute exponent

Basu--Roy's meeting radius bounds apply to the projected semialgebraic
fiber regardless of convexity of its row polynomials. The rational-matrix
minimum-norm formula then bounds a linear lift. Convexity of the original
sublevel intersection, and hence of its integer-coordinate projection,
supplies the hypothesis of the integer witness bound.

The residual epigraph in the positive-gap argument may be nonconvex. This
causes no failure: it is the image of a compact truncated epigraph, and
its finite Farkas description has the same degree and individual height
bounds. When its positive minimum is \(\alpha\), the reciprocal
graph \(ty=1\), \(y\ge0\), is compact and has largest last
coordinate \(1/\alpha\). The containing radius theorem applies to
all its bounded components. No convex separation is performed on this
residual epigraph.

The gradient estimate used to select the rational grid is a coefficient
estimate on a known box, not a convexity estimate. Relaxing each native
right-hand side preserves global quasiconvexity. A rounded feasible anchor
satisfies every enlarged-box row strictly. Conversely, a strict relaxed
integer point has residual below the uniform gap and therefore certifies
exact feasibility in the same original integer fiber. The grid is never
enumerated; it adds precisely \(r\) integer variables.

For \(k=0\), the same grid argument applies with \(r\) integer
grid coordinates. If \(k+r=0\), the remaining strict system is an
LP. The convex note's separate direct continuous gradient test is not
needed and must not be imported with its zero-gradient shortcut.

For the integer recursion, rational LDL, line substitution, evaluations,
and gradients have length at most
\(f(s,D)(H+H_E+1)\), linear in the changing input and ellipsoid
lengths. The fixed family can remain implicit. The strict integral margin
at a feasible lattice point supplies a uniform volume threshold using
only coefficient and derivative bounds; no row-count factor is needed.
Affine integer substitutions preserve quasiconvexity and degree.

I read the existing recursion proof, including its repair of the short-map
argument. Rational quadratic lattice subroutines supply a primitive
shortest direction; eigenvalue and determinant bounds control its bits.
The section map must satisfy \(a^TU=e_s^T\), and fresh bounding
balls handle translations. The changed rounding ratio affects only
dimension factors. Controlled rational ellipsoid rounding and these maps
retain the recurrence \(L_{j+1}\le f(s,D)(L_j+1)\). Its depth is
parameter-bounded, so this step does not produce \(N^{f(k,r,d)}\).
The existing lattice and ellipsoid theorems remain imports; the present
review checks their changed interface, not a new proof of those theorems.

## 4. Values, attainment, and complete recovery

Fixed rational objective thresholds preserve the native row promise.
Allowing the threshold to vary need not give a quasiconvex polynomial or
a convex joint epigraph. The proof correctly uses the
[quasiconvex mixed-value theorem](quasiconvex-mixed-value-frontier.md).
Every weak slice of the projected epigraph is convex by sublevel
intersection and projection. Its strict slice is a nested union of such
weak slices and is convex. Thus both the finite-value theorem and its
separate optimal-integer corollary apply.

Farkas elimination with the appended objective row still has a constant
matrix. Quantifier elimination needs only the \(r\) nonlinear
continuous coordinates. Its individual degree and coefficient bounds
are unaffected by the lack of joint epigraph convexity. The exponential
description is used for effective bounds, not constructed by the algorithm.

I independently inspected the native quasiconvex-row definition,
Theorem 3(iii), the stable-subsystem definition, and Theorem 7(ii) in
Bank--Mandel's [1987 primary preview](https://api.pageplace.de/preview/DT0400.9783112720936_A50662169/preview-9783112720936_A50662169.pdf),
printed pages 18, 24, and 34. Rational coefficients give integer-generated
recession for the stable subfamily, hence its required mixed-integer
generation. The right-hand-side feasibility domain is closed. Appending
the native rational quasiconvex objective proves finite attainment.
Theorem 7 does not impose the compact-plus-cone assumption from other
parts of the chapter. Its proof is omitted from the preview; this review
checks the published statement and its application.

The root-bound unboundedness query uses the original unboxed model. Scalar
bisection and certified recognition then recover the finite value using
only rational feasibility queries. Fixing any attained optimal integer
assignment leaves a threshold description obtained by eliminating only
\(r\) variables. Its finite endpoint has degree \(g(r,d)\),
independently of the assignment's size or the number of integer variables.
The general value theorem remains necessary for the uniform height and
integer-witness bounds.

At a fixed optimal integer assignment, the projected optimal set is
nonempty, closed by finite weak Farkas inequalities, and convex. Its
minimum-norm point is unique. The reviewed singleton formula consequently
gives the same degree and height bounds as in the convex case. Include
the value in \(K=\mathbb Q(\theta,u^*)\). The minimum-norm
linear lift has the active-row rational-matrix formula, so every eliminated
coordinate remains in \(K\). Rational minors, denominator clearing,
and conjugate bounds give the uniform optimizer box; they do not multiply
field degrees over the unrestricted linear dimension.

This box contains the canonical pair for every optimal integer assignment
inside the bounded integer search region. Retaining it in every query
makes equality of the boxed minimum to \(\theta\) an exact test
for intersection with the original optimal set. Norm and coordinate
bisection approximate the same minimum-norm projected point, restarting
coordinate intervals for each requested precision. Convexity of that
optimal set is sufficient for the projection inequality; convexity of
the objective function is unnecessary.

The outward right-hand-side approximation and the rational minimum-norm
QP recover the same canonical linear lift through the reviewed Hoffman
estimate. These steps use a constant rational fiber matrix and polynomial
evaluation; quasiconvexity introduces no change. The joint approximation
oracle meets the imported common-field recovery hypotheses. Exact
substitution checks the final point against every native row. Value
recovery does not call optimizer recovery, so the subroutine nesting
depth remains fixed and the absolute exponent is preserved.

## 5. The intrinsic continuous-block strengthening is valid

The [projection audit](quasiconvex-polynomial-projection-review.md)
proves that a globally quasiconvex polynomial affine in one variable has
constant coefficient on that variable. I checked its reciprocal-coefficient
proof and requested a fresh
[independent affine-direction review](quasiconvex-affine-direction-independent-review.md),
which proves the result through Jensen equality and tests weakened
hypotheses.

There is a stronger continuous version, also independently checked here.
Let a continuous globally quasiconvex function on the whole real vector
space have the form \(q(y,t)=a(y)t+b(y)\). If \(a(y_0)=0\),
a sufficiently high closed sublevel contains the complete vertical line
over \(y_0\). If any other slope were nonzero, the same sublevel
would contain a point above that base, hence the complete parallel line
through that point, a contradiction. Thus either all slopes vanish or
none do. In the latter case continuity gives a fixed sign. After reversing
\(t\), assume it is positive. Every
\((\alpha-b(y))/a(y)\) is concave. Jensen's inequality for all real
\(\alpha\) forces \(1/a\) to be globally affine; its global
positivity makes it constant. Hence \(a\) is constant.

If a fixed continuous direction \(h\) is in the polynomial kernel of
\(\nabla^2_{xx}g\), use coordinates with last direction \(h\).
The identity \(g_{tt}=0\) makes the transformed polynomial affine
in that coordinate. The coefficient lemma makes its directional derivative
constant in every remaining variable, including the variables later
restricted to integers. Therefore the full Hessian annihilates \((0,h)\).
The reverse implication is immediate by taking the continuous block.
The two kernel definitions agree, without a positive-semidefinite Hessian.
Indeed, the weaker identity \(h^T\nabla^2_{xx}g\,h\equiv0\)
already suffices.

Global joint quasiconvexity is essential. Convexity of one sublevel, or
quasiconvexity only within each fixed integer fiber, does not establish
constant coefficients. The separate review gives explicit counterexamples.
Recognition of the global promise is not part of the algorithm.

## 6. Prior comparison, significance, and verification limits

The [prior audit](quasiconvex-polynomial-nonlinear-dimension-prior.md)
is appropriately cautious. Hildebrand--Koppe's Theorem 1.1 already gives
FPT exact pure-integer quasiconvex polynomial optimization, and its proof
already supplies the geometric search used here. The candidate combines
that machinery with controlled implicit projection and exact algebraic
continuous output; neither ingredient should be described as a first
quasiconvex integer method.

I independently inspected the published
[Gavenčiak--Koutecký--Knop survey](https://iuuk.mff.cuni.cz/~koucky/EPAC/papers/disopt.pdf),
Appendix A.1. It explicitly calls the mixed-integer FPT extension folklore,
immediately after discussing many continuous variables in mixed linear
programming. It does not specify the precise nonlinear dimension or
algebraic output convention here. This is material priority pressure,
not evidence that the present exact statement is new or already proved.

I also checked Proposition 4.6 and Theorem 4.11 in
[Ahmadi--Olshevsky--Parrilo--Tsitsiklis](https://www.mit.edu/~jnt/Papers/J143-13-convex-poly-complexity.pdf).
Odd-degree globally quasiconvex polynomials are monotone univariate
polynomials of affine forms, and even homogeneous quasiconvex polynomials
are convex. Thus the nonconvex row enlargement has substantial structural
restrictions. A strict function-class inclusion does not by itself
demonstrate new geometric modeling power. Presenting the result as a
corollary or extension is more credible than treating this step as a
separate major advance. Practical parameter sizes, useful application
families, and numerical performance remain open.

A targeted inline `python -` command using exact fractions checked a
nonconvex compact residual epigraph: \(p(x)=x^3+1\) on
\([-1/2,0]\) has positive minimum \(7/8\), midpoint value
\(63/64>15/16\), and reciprocal maximum \(8/7\).
It also checked the zero-row Farkas decomposition for the matrix with
rows \(0,1,-1\). These checks challenge two transfer points; they
do not replace their general proofs. I read the separate oracle review's
six exact test cases and did not duplicate its unchanged test run.

Targeted document checks for this review cover local links, mathematical
delimiters, final newline, trailing whitespace, and control characters.
No project-wide verification, CI inspection, or Lean formalization was
performed. The elementary new lemmas and transfer proofs were checked
mathematically; the major imported quantitative algorithms retain their
separate sources and reviews. A positive review records this scrutiny,
not a guarantee of correctness or priority.
