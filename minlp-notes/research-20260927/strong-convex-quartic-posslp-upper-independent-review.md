# Independent review of the unconstrained strongly convex quartic upper bound

Date: 2026-09-28. Status: the frozen upper-bound proof passes independent
adversarial review. No substantive mathematical defect was found.
Four known LaTeX corrections and minor scope clarifications do not
change the argument.

The reviewed [main note](strong-convex-quartic-posslp-upper.md) has
SHA256
f397f336b607017a5c035354bbb3d81609cc6e73f1fb06e8b70be04b03b4a7b2.
This reviewer did not develop the construction. The review reconstructs
the quantitative proof, checks both primary source dependencies, and
distinguishes the upper bound from the separately reviewed lower bounds.
No priority claim follows from this audit.

## Input scope and curvature certificate

The domain is all of \(\mathbb R^n\). A supplied positive rational
\(\mu\) guarantees \(\nabla^2f\succeq\mu I\) globally. It follows
that \(f\) is coercive and has a unique minimizer \(p\), with
\(\nabla f(p)=0\). This is stronger than strict convexity or
convexity only on a bounded domain; those weaker hypotheses are not
silently used.

For the verifiable format, let \(M\succ0\) be a rational Hessian Gram
on the full basis \((v,X\otimes v)\). If its eigenvalues are positive,

\[
 \lambda_{\min}(M)
 =\frac{\det M}{\prod_{\lambda\ne\lambda_{\min}}\lambda}
 \ge\frac{\det M}{(\operatorname{tr}M)^{h-1}}=\mu.
\]

The basis vector has squared norm
\((1+\|X\|^2)\|v\|^2\ge\|v\|^2\). Hence this \(\mu\)
is a valid curvature lower bound. Exact polynomial coefficient
comparison checks the identity, and rational \(LDL^{\mathsf T}\)
checks positive definiteness. Determinants, traces, and the displayed
integer power have polynomial bit complexity and output size in the
explicit matrix input. The resulting enlarged length \(L\) is
polynomial in the original certificate length.

As usual, take \(n\ge1\). If zero-dimensional constant objectives are
allowed as an input convention, they can be handled directly by rational
comparison, avoiding the empty-matrix trace expression.

## Radius, derivatives, and the initial neighborhood

Writing \(C=\sum_\alpha|f_\alpha|\le2^{2L}\), the gradient at zero
has norm at most \(C\): its entries are the linear coefficients, whose
Euclidean norm is at most their absolute sum. Strong monotonicity gives
\(\mu\|p\|\le\|\nabla f(0)\|\), including the trivial case \(p=0\).
Thus \(\|p\|\le2^{3L}\).

For \(R=2^{4L}\), a partial derivative of order \(k\le3\) is
bounded on the ball by its falling-factorial coefficient bound times
\(C(1+R)^{4-k}\). The factors four, twelve, and twenty-four
are valid for orders one, two, and three. Passing to Euclidean gradient,
matrix operator, and trilinear operator norms costs at most
\(\sqrt n,n,n^{3/2}\), respectively. The manuscript's resulting
exponent bounds

\[
 18L+4,\quad15L+5,\quad11L+6,\quad8L+6
\]

are conservative and at most \(20L\) for \(L\ge2\).
Integrating the third derivative along a segment in the convex ball
gives the claimed Hessian Lipschitz bound \(B=2^{20L}\).

With \(\rho=\mu/(4B)\), strong convexity implies

\[
 f(x_0)-f(p)\le\mu\rho^2/2
 \quad\Longrightarrow\quad \|x_0-p\|\le\rho.
\]

Both \(\rho\) and the requested objective error
\(\varepsilon_0=\mu^3/(32B^2)\) have polynomial bit length.
Also \(\rho<1\), and \(\|p\|+\rho<R\), so this entire
neighborhood lies inside the derivative-bound ball.

## Primary source for the rational initial point

[Slot, Steurer and Wiedmer, Corollary 1.2](https://arxiv.org/html/2511.03440v1#S1.SS2)
was read directly, together with the encoding convention and its
algorithmic proof. It explicitly outputs a point in the given
nonempty rational polyhedron, with additive objective error and runtime
polynomial in the encoding lengths and logarithm of the inverse error.
The source treats the bit model and allows \(P=\mathbb R^n\).
The algorithm is deterministic; no randomized identity-test step is
required to find the approximate point. Its use of a small Hessian
evaluation point elsewhere establishes a size bound, rather than
requiring an unproved deterministic search in the reduction here.

Applying the corollary with \(\varepsilon_0\) gives an actual rational
point of polynomial bit length. Strong convexity excludes unboundedness.
The source's Proposition 3.2 omits convexity in its displayed statement,
but its proof uses convex gradient separation. The manuscript correctly
uses the explicitly convex corollary and does not import that omitted
hypothesis as a nonconvex result.

The source is sufficient, although its general solution-radius theorem
is more than is needed here: the supplied \(\mu\) already gives an
explicit polynomial-bit radius. A classical bounded convex
weak-optimization implementation could provide this initial point.
Thus the upper bound should not be presented as requiring a newly
available solution bound for this strongly convex subclass.

## Exact Newton refinement

The fundamental-theorem-of-calculus identity

\[
 \nabla f(x)=\int_0^1
 \nabla^2 f(p+t(x-p))(x-p)\,dt
\]

gives the displayed Newton error identity after subtracting it from
\(\nabla^2 f(x)(x-p)\). All segments lie inside the established ball.
The inverse Hessian norm is at most \(1/\mu\), and integration of
\(B(1-t)\|x-p\|\) yields

\[
 e_{k+1}\le\frac{B}{2\mu}e_k^2.
\]

For \(q_k=Be_k/(2\mu)\), the initial bound is \(q_0\le1/8\);
therefore \(q_k\le2^{-3\cdot2^k}\). The iterates remain in the
neighborhood: in fact \(e_{k+1}\le e_k/8\) whenever
\(e_k\le\rho\). This justifies the derivative bounds at all steps.

The Hessian at each rational iterate is symmetric positive definite.
Rational \(LDL^{\mathsf T}\) elimination has positive pivots and
needs neither square roots nor branch decisions. Each step evaluates
fixed-degree polynomials and performs polynomially many rational
operations. Retaining the complete directed acyclic computation graph
keeps a polynomial number of steps polynomial in circuit size.
The proof never claims that the expanded rational iterates have
polynomial bit length.

## Quantifier elimination and separation

[Basu's survey, Theorem 2.16, printed page 12](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf)
was read in the primary PDF, including a rendered image of the theorem.
For one quantified block of \(n\) variables and one free variable,
the output degree bound specializes to \(d^{O(n)}\).
The theorem also bounds coefficient bit lengths by
\(\tau d^{O(n)}\), with an absolute effective constant.
The latter clause is essential and is explicitly present in the source.

After clearing rational denominators, the gradient equations and
\(z=h(X)\) have degree at most four and polynomial coefficient bit
length. Their real projection is precisely \(\{h(p)\}\), because
the globally strongly convex function has exactly one real critical
point. Hence the theorem gives a quantifier-free description with
degree and coefficient-bit bounds at most \(2^{a(L)}\) for a fixed
effective polynomial majorant \(a\).

Some nonzero output polynomial must vanish at \(h(p)\). Otherwise
all finitely many nonzero polynomial signs would be constant in an
open interval around that point, and the formula would define an
interval there. Identically zero polynomials do not affect this
argument because their signs are constant.

Let \(\alpha=h(p)\ne0\), and remove all powers of \(z\) from a
nonzero integer annihilator \(P\). Its remaining constant term has
magnitude at least one. If \(|\alpha|<1\), the other terms have
total magnitude at most
\(\deg(P)\max|P_i|\,|\alpha|\).
Thus

\[
 |\alpha|\ge
 2^{-a(L)-2^{a(L)}}\ge2^{-2^{a(L)+1}}=g.
\]

The case \(|\alpha|\ge1\) satisfies the same lower bound.
This does not exclude \(\alpha=0\); zero is separated at the final
comparison step.

No finite-complex-critical-locus assumption is used. That omission
would have been unsafe: radial strongly convex quartics can have
positive-dimensional complex critical components. For example,
\(f(X)=(\sum X_i^2)^2+\sum X_i^2\) has real Hessian at least
\(2I\), but every complex point satisfying \(\sum X_i^2=-1/2\)
is critical. For \(n\ge2\) this is a positive-dimensional component.
The real singleton and real quantifier elimination suffice.

The reduction does not execute quantifier elimination or construct
the annihilator. The effective majorant is fixed once for the algorithm;
its coefficients do not depend on the instance. Constructing \(g\)
therefore takes polynomially many squarings, without printing its
expanded denominator.

## Final comparisons and arithmetic-circuit conversion

For \(k=a(L)+2\), the value or coordinate error is bounded by

\[
 2^{21L+1-12\cdot2^{a(L)}}\le g/8.
\]

The required exponent comparison is exactly
\(21L+4\le10\cdot2^{a(L)}\), which follows from the chosen
lower bound on \(a(L)\). The objective error uses the gradient
bound along the segment between \(x_k\) and \(p\); the coordinate
error is smaller.

The four shifted sign expressions distinguish the corresponding
strict or weak comparisons, including zero. For equality,
\(g^2/4-\widehat\alpha^2\) is at least \(15g^2/64>0\)
when \(\alpha=0\), and at most \(-33g^2/64<0\) otherwise.
No final expression is zero on a promised input.

The fraction rule

\[
 \frac{N_a/D_a}{N_b/D_b}
 =\frac{N_aD_bN_b}{D_aN_b^2}
\]

preserves positive denominators for every nonzero divisor, regardless
of its sign. The Newton and positive-pivot arguments prove all needed
divisors are nonzero. Constantly many integer arithmetic gates replace
each rational gate, with sharing retained. The final numerator is
therefore one PosSLP instance, and the construction uses no PosSLP
oracle while producing it.

For strictly feasible objective instances, \(\min f<0\), the same
separation and approximation imply \(f(x_k)\le-7g/8<0\).
This proves the stated short shared rational-circuit witness. It
does not imply a short expanded binary witness, nor a rational point
in a zero-minimum singleton.

## Related Newton reductions and scope

The directly inspected
[Etessami–Stewart–Yannakakis Appendix C](https://arxiv.org/pdf/1201.2374v2)
provides a close methodological precedent. Theorem C.4 supplies
doubly exponential Newton accuracy after polynomially many steps;
Lemma C.5 supplies algebraic separation; Corollary C.8 gives
many-one reductions of strict rational-threshold comparisons for
probabilistic polynomial system least fixed-point coordinates to
PosSLP. Its proof uses polynomial-size matrix inversion circuits and
repeated squaring. The current upper bound should credit this explicit
precedent in addition to the broader numerical-analysis references.
The domains and hypotheses differ: that result concerns probabilistic
fixed points, while this note concerns unconstrained minimizers with
global curvature certification.

The verified contribution of this note is an upper bound for the
stated class, using classical approximation, real algebraic bounds,
and Newton circuits. Its combination with a matching lower bound can
yield a completeness theorem. This review independently checked the
root-coordinate lower reduction earlier, but does not replace the
separate audit of the unconstrained minimum-value lower reduction.
No claim about arbitrary constrained quartics, NP-hardness of PosSLP,
or polynomial-time exact optimization follows.

## Targeted checks and remaining limits

The command

~~~text
python research-20260927/check_strong_convex_quartic_upper_review.py
~~~

passed. Exact symbolic calculations check a coupled quartic's Newton
integral identity and the two-dimensional rational \(LDL^{\mathsf T}\)
solve. Exact rational calculations check all five comparison formulas
at the worst nearest-gap and zero endpoints. Integer calculations check
the derivative and final-precision exponent margins for \(2\le L\le64\).
These finite checks supplement the universal proof; they do not prove
the cited source theorems or all-dimensional convergence.

For source inspection, the Basu PDF was downloaded to a temporary
file and its printed page 12 rendered with
\( \texttt{pdftoppm -f 12 -l 12} \); the coefficient-bit clause was
visually confirmed. The Slot–Steurer–Wiedmer and
Etessami–Stewart–Yannakakis statements were read directly online.
No Lean formalization, project-wide verification, or CI inspection was
performed.

The known missing backslashes in three occurrences of “qquad” and
the one “:quad” occurrence should be fixed. Apart from those presentation
repairs, the original upper-bound proof needs no mathematical correction.

## Observable extension and amended-source reconciliation

The amended source has SHA256
df5791fec9197b2c2fd699a19f2a38653de050ef6ffcc38d6c7c3e9f6d3e7bb3.
Its extension to a supplied rational polynomial \(h\) of degree at
most four passes independent review. The encoding of \(h\) is included
in \(L\), and its coefficient sum obeys the same bound as \(f\).
The derivative estimates use only coefficient magnitudes and degree,
so they bound \(\|\nabla h\|\) on the same ball even when \(h\)
is nonconvex.

Only \(f\) is minimized to find the initial point and only \(f\)
is used in Newton's method. The real formula
\(\exists X:\nabla f(X)=0,\ z=h(X)\) still defines exactly
\(\{h(p)\}\), with unchanged degree and height parameters.
The segment estimate

\[
 |h(x_k)-h(p)|\le B\|x_k-p\|
\]

therefore proves the same \(g/8\) error bound. All five comparison
circuits remain valid. The claim means one PosSLP instance for each
specified order or equality predicate; a single binary answer is not
claimed to return all three possible signs simultaneously.

For two objectives on disjoint blocks, the sum
\(F(X,Y)=f_1(X)+f_2(Y)\) has curvature at least
\(\min(\mu_1,\mu_2)\), and its unique minimizer is the pair of
minimizers. The observable \(h(X,Y)=f_1(X)-f_2(Y)\) thus compares
their exact minimum values, including equality, with one PosSLP
instance for a chosen predicate. The input size remains polynomial.

The amended note correctly uses the supplied-curvature theorem here.
A nontrivial separable sum generally cannot possess a positive
definite Hessian Gram on the full joint basis: such a Gram would
imply a lower Hessian bound growing as \(1+\|(X,Y)\|^2\) in
every direction, whereas a direction in the \(X\) block has curvature
independent of \(Y\). Separate certificates nevertheless give the
required rational \(\min(\mu_1,\mu_2)\).

The added lower-degree observation is also correct. If a globally
convex polynomial has degree at most three, its Hessian has the form
\(H_0+\sum_i X_i H_i\). For every vector \(v\), the scalar
\(v^{\mathsf T}(H_0+tH_i)v\) is nonnegative for both signs of
arbitrarily large \(t\); hence \(v^{\mathsf T}H_iv=0\).
Symmetry implies \(H_i=0\), so the polynomial has degree at most two.
With the supplied positive curvature, rational linear algebra computes
its rational minimizer and value in polynomial bit time.
This does not assert a separation of P from PosSLP.

The source amendments correctly credit the directly inspected
Etessami–Stewart–Yannakakis precedent and explain that the supplied
radius makes the general 2025 radius theorem unnecessary here.
The LaTeX fixes, zero-dimensional direct case, and distinct notation
for the Gram dimension are correct. The restriction of the combined
completeness statement to order relations avoids asserting an unproved
equality lower bound.

The extension changes no Newton or separation constants. Its additional
arguments were checked analytically; no further computation was needed.

The final status-and-wording version has SHA256
5363549e10f4b6d517257b3a16b397d40e2783e1c2d394930cd9f657a25e8003.
It explicitly states one instance per chosen binary predicate and says
“degree at most two” in the lower-degree observation. Its reviewed
status and verification disclosure match the completed audits above.
This final reconciliation passes; no mathematical construction changed.
