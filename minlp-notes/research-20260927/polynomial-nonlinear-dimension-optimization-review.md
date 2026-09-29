# Adversarial review of full convex polynomial optimization

Date: 2026-09-28. This is a fresh review of the complete
[optimization manuscript](polynomial-nonlinear-dimension-optimization.md),
including its final degree refinement. I also read the separate
[witness bounds audit](polynomial-nonlinear-dimension-witness-review.md),
the [optimization prior audit](polynomial-nonlinear-dimension-optimization-prior.md),
and the relevant statements and proofs in the value, feasibility,
affine-fiber recovery, and common-field recovery dependencies. A separate
fresh reviewer checked the status and complexity composition in Sections
3--4 and 8 and inspected the primary algebraic-recognition theorem.

**Finding.** I found no remaining mathematical or bit-complexity gap in
the assembled theorem, conditional on its separately reviewed exact
feasibility and general convex semialgebraic value theorems. The claimed
algorithm has cost and output length \(f(k,r,d)N^C\), with absolute
\(C\). The common field degree can be bounded by \(g(r,d)\),
independently of the integer dimension, row count, and linear continuous
dimension. This review does not establish novelty, prove the imported
theorems again, or establish practical solver performance.

## Attainment and the value oracle

I independently checked the standing model and definitions in the
[Bank--Mandel primary preview](https://api.pageplace.de/preview/DT0400.9783112720936_A50662169/preview-9783112720936_A50662169.pdf):
printed pages 18 and 20 define globally quasiconvex polynomial rows and
the integer-generated and mixed-integer-generated recession conditions.
Theorem 3(iii), page 24, supplies the integer-generated condition for
rational coefficients. The stable subsystem on page 34 retains a
subfamily of those same polynomials, so that conclusion also applies to
its recession cone. It implies the hypothesis of Theorem 7(ii), which
makes the mixed-integer feasible right-hand-side domain closed.

In the manuscript's model, each full row \(C_iv+p_i(z,u)\), including
the objective, is a rational globally convex polynomial in all real
variables. Appending the objective as a row and taking the limit of
feasible objective thresholds proves finite attainment. The argument
requires neither a Slater point nor the compact-plus-cone hypothesis
used for a different model in Bank--Mandel. The preview contains the
published statements but omits the proof of Theorem 7; this review checks
the statement's application, not that omitted proof.

The Farkas multiplier matrix includes the objective's row \(C_0\).
It remains constant and rational. Normalization by the sum of the
nonnegative multipliers gives a compact polytope, and its vertices
describe precisely the projected weak system. Rational minor bounds
control each vertex separately. A positive denominator is cleared within
each projected polynomial; no denominator product over the exponential
family is used. Convexity of every projected polynomial follows from its
nonnegative multiplier coefficients.

Consequently the epigraph in \((z,t)\) is convex and upward closed.
After a successful feasibility query, it has a mixed-integer point.
These are exactly the geometric premises of the imported general value
theorem. Quantifier elimination removes only the \(r\) nonlinear
continuous coordinates. I inspected the full displayed statement of
Basu's [survey, Theorem 2.27](https://arxiv.org/abs/1409.1534), including
its integer coefficient bound: individual output degrees and coefficient
bits have the required bounds independently of predicate count. The
formula length and computation time do depend on that count. The proof
uses only the former bounds and does not execute quantifier elimination
on the exponential family.

The unboundedness test has the correct direction and uses the original
unboxed model. If every finite value has minimal-polynomial coefficient
bits at most \(L\), one can take \(M=2^{L+2}\). A feasible point
with objective at most \(-M-1\) excludes a finite infimum. Failure of
that query bounds the already nonempty model below. No continuous
relaxation value or optimizer box is substituted for this argument.

Rational threshold bisection gives certified approximations to the finite
value. The focused reviewer independently opened
[Kannan--Lenstra--Lovasz, Theorem 1.19](https://www.math.cmu.edu/~af1p/Teaching/AdditiveCombinatorics/LLLL.pdf),
printed page 241. A degree bound \(A\) and coefficient-bit bound
\(L\) require only \(O(A^2+A\log A+AL)\) approximation bits and
polynomial bit complexity, including values outside the unit interval.
Thus the scalar recognition interface is sufficient; it is not an
uncertified integer-relation step.

## Degree, selected points, and a uniform box

The improved degree bound follows by a separate argument from the height
bound. Fix an attained optimal integer assignment. Its fiber epigraph,
after Farkas elimination, has degree at most \(\max(2,d)\) in
\((u,t)\). Integer substitution changes coefficient heights but not
degrees. Eliminating \(u\) gives a one-dimensional description whose
individual degrees depend only on \((r,d)\). The finite endpoint
\(\theta\) must be a root of a nonzero output polynomial: otherwise
all signs would be locally constant and could not define that boundary.
Hence \(\deg\theta\le g(r,d)\). The generic value theorem still
supplies the uniform height and small optimal-integer-assignment bounds.
For \(r=0\), an optimal integer fiber is a rational linear program,
so its finite attained value is rational.

For each optimal integer assignment in the supplied integer box, the
projected optimal set \(U_\theta\) is closed for a specific reason:
Farkas elimination of a constant matrix gives a finite family of weak
polynomial inequalities. The proof does not use the false assertion that
arbitrary projections of closed convex sets are closed. Convexity and
nonemptiness then give a unique minimum-norm point \(u^*\).

The singleton formula in (14) selects the intended real root of the value
polynomial, imposes projected feasibility, and compares the norm with
every feasible projected point. Its quantified block sizes depend only on
\(r\). It therefore bounds the individual degrees of \(u_i^*\) by
\(g(r,d)\), and their coefficient bits by \(f(k,r,d)N^C\).
If no nonzero output atom vanished at the selected coordinate, the output
formula would hold throughout a neighborhood; that contradicts the
singleton property. Passing to the minimal-polynomial factor preserves
the bound.

The field is explicitly
\(K=\mathbb Q(\theta,u_1^*,\ldots,u_r^*)\). Multiplying at most
\(r+1\) individual degree bounds still gives \([K:\mathbb Q]\le
g(r,d)\). The proof never multiplies degrees over the unrestricted
number of linear continuous coordinates.

At \(u^*\), the remaining fiber has rational matrix \(A\) and
right-hand side in \(K\). The minimum-norm point \(v^*\) lies in
the span of a linearly independent subset of its active normals. Solving
those active equalities gives

\[
 v^*=A_I^T(A_IA_I^T)^{-1}b_I^*.
\]

This holds with dependent active rows and zero multipliers elsewhere; it
does not require nondegeneracy. If \(v^*=0\), use the empty subset.
Thus every coordinate remains in \(K\). Rational minor bounds, a
common integral multiple of \(\theta,u^*\), degree-\(d\)
denominator clearing, and bounds on all conjugates give the claimed
coordinate heights. The revised text explicitly clears the polynomial
coefficient denominators as well as those of the rational matrix.

These estimates are uniform over every optimal integer assignment of the
given bit length. This is essential: integer bisection may select a
different assignment from the one whose existence first supplied the
integer radius. The proof gives a single computable continuous box
containing the canonical pair for every such assignment.

## Recovery and complexity

Every optimal-face query retains the same compact box. The original
optimum is a lower bound on every restricted objective. A nonempty
restricted model has minimum equal to \(\theta\) exactly when it
contains an original optimizer, because continuity and compactness give
attainment. Empty restrictions are handled separately. Thus value
comparison is a valid optimal-face feasibility test using rational input
only. Integer interval bisection uses complementary integer endpoints,
so it always retains an optimizer and never enumerates the box.

For the selected integer assignment, the fixed box contains the unboxed
canonical pair. The minimum-norm projected point of the boxed optimal
set therefore equals the point whose arithmetic bounds were proved.
Norm bisection and the projection inequality force every retained point
near that same \(u^*\). Coordinate bisection may retain nearby points
without retaining \(u^*\) itself, so restarting from the original box
for each new accuracy request is necessary and is included.

The outward right-hand-side approximation contains the true affine fiber
and is nonempty. Its minimum-norm rational QP solution has norm at most
\(\|v^*\|\). The rational-matrix Hoffman estimate repairs it to the
true fiber within \(\zeta=2H_A\delta\). Combining this repair with
the projection inequality proves (24). The stated precision constant is
safe: if \(0<\eta\le1\) and
\(\zeta\le\eta^2/[16(V+1)]\), the right side of (24) is at most
\((1+\sqrt{33})\eta/16<\eta\). Polynomial evaluation on the known
box needs only a degree factor times coefficient, radius, and requested
accuracy bits. The QP introduces no additional nonlinear core into the
feasibility oracle; it is solved by the separate rational QP algorithm.

The resulting approximation oracle consistently approximates one tuple,
not arbitrary conjugates or arbitrary optimizers. It meets the hypotheses
of the reviewed common-field recovery theorem, which I read. Including
the value ensures that the affine fiber's right-hand side is in the
declared field. Exact substitution checks the returned original rows and
objective; global optimality also relies on the exact value algorithm.

All rational oracle queries preserve degree at most \(\max(2,d)\)
and the supplied nonlinear core. A linear number of box coefficients of
\(p\) bits has length \(O(Np)\), absorbed by an absolute power of
\(N+p+1\). Only current intervals are retained. Most importantly,
the nesting depth is fixed: common-field recognition calls approximation,
approximation calls boxed value recovery, and value recovery calls
feasibility and scalar recognition. Value recovery never calls optimizer
recovery. The number of integer bisections changes the number of calls,
not their nesting depth. This preserves an absolute input exponent.

## Scope, prior work, and verification

The contribution must remain a candidate structural exact-complexity and
output theorem. Attainment, fixed-dimensional integer optimization,
implicit separation, real algebraic sampling, and algebraic recognition
all have substantial precedents. The prior audit additionally records a
published folklore statement about mixed-integer convex FPT extensions.
Neither that statement nor an unsuccessful search resolves priority for
the precise large-linear-extension result. I found no basis for claiming
a new attainment theorem, a first mixed-integer convex FPT algorithm, or
practical speedup.

The scope still requires rational native globally convex polynomials,
explicit monomials, bounded degree as a parameter, and constant
coefficients on eliminated coordinates. The revised discussion correctly
leaves quasiconvex extension to a separately verified separation argument.
It does not claim that a generic counterexample to quasiconvex sums settles
that more structured extension.

I read the new exact quartic example and its checker; the identity proves
global optimality because \(z(z-1)\ge0\) for every integer \(z\),
not merely the finitely many integers sampled by the script. Its cubic
coordinate relations and inverse maps agree with the stated common field.
I also independently checked the repeated-squaring family in (27)--(28).
Every coordinate after the first square is nonnegative, so its fixed-first-
coordinate fiber minimum is indeed \(a^{2^r}\). The derivative of
the reduced objective is \(2^r(a^{2^r-1}-2)\), which changes sign
once and gives the unique optimizer. Each row's Hessian acts on one of
the \(r\) nonlinear coordinates, so the stated intrinsic dimension is
exact. Eisenstein's criterion gives degree \(2^r-1\) for the first
coordinate and its nonzero rational multiple \(\theta\). This proves
the exponential lower boundary for all \(r\), including degree one
when \(r=1\); the script checks only eight finite instances.
I read the extended checker and did not rerun it after the author's
passing run.
No new numerical test would establish the general arithmetic or
complexity assertions; those were checked as mathematical arguments and
against the primary statements identified above.

Targeted document verification checked this review's local links, final
newline, control characters, and trailing whitespace. No project-wide
verification, CI inspection, or Lean formalization was performed. A
positive review records the scrutiny described here, not a guarantee of
correctness.
