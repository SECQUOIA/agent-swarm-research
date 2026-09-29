# Exact comparison for certified strongly convex quartics is PosSLP-complete

Date: 2026-09-28. The component upper and lower proofs have passed
independent adversarial review. A separate
[composition and scope review](exact-convex-quartic-complexity-review.md)
also passed. Publication priority remains unestablished.

Exact minimum-threshold comparison for an unconstrained rational
quartic is PosSLP-complete when the input supplies a positive definite
rational Gram matrix proving global SOS-convexity. The same holds
for order comparisons of its unique minimizer's coordinates. Thus
even a verifiable strict curvature certificate leaves the full
arithmetic-circuit sign problem in an exact continuous node bound.
This is a classification of exact arithmetic, not a demonstrated
running-time improvement or a proof of NP-hardness.

## Input and output conventions

The input explicitly gives a rational polynomial \(f\) of degree
at most four in \(n\ge1\) variables and a rational symmetric matrix
\(M\succ0\) satisfying
\[
 v^{\mathsf T}\nabla^2 f(X)v
   =(v,X\otimes v)^{\mathsf T}M(v,X\otimes v).                 \tag{1}
\]
All coefficients and matrix entries use ordinary binary rational
encoding. Polynomial coefficient comparison and rational symmetric
elimination verify this format in polynomial time. Invalid inputs
can be rejected. A determinant and trace bound supplies a positive
rational \(\mu\) of polynomial bit length with \(M\succeq\mu I\),
and hence \(\nabla^2f\succeq\mu I\). Thus \(f\) has a unique attained
minimum at a point \(p\).

PosSLP asks whether an integer arithmetic circuit, starting from
zero and one and using addition, subtraction, and multiplication,
has positive output. Completeness below means polynomial-time
many-one equivalence with that problem. It does not assert that
PosSLP is outside P or is NP-hard. The threshold \(r\) is rational
and explicitly encoded.

| Decision problem under (1) | Established complexity |
| --- | --- |
| \(f(p)<r\), \(f(p)\le r\), \(f(p)>r\), or \(f(p)\ge r\) | Each is PosSLP-complete. |
| \(p_j<r\), \(p_j\le r\), \(p_j>r\), or \(p_j\ge r\) | Each is PosSLP-complete. |
| \(f(p)=r\) or \(p_j=r\) | Each reduces to one PosSLP instance; no matching equality lower bound is claimed. |
| Global nonnegativity or real polynomial SOS membership | Each is PosSLP-complete. |
| Existence of a rational positive definite Gram on all monomials of degree at most two | PosSLP-complete. |
| Rational polynomial SOS membership, allowing singular Grams | PosSLP-hard; the present arguments do not give a general matching upper bound. |

The positive definite matrix in (1) is a **Hessian Gram**. It is
different from a polynomial Gram \(Q\) satisfying
\(f=m_2^{\mathsf T}Qm_2\), where \(m_2\) lists all monomials
of degree at most two. Keeping these two certificates distinct is
essential to the last three rows.

## Why the classification holds

The [general upper bound](strong-convex-quartic-posslp-upper.md)
needs only an explicitly supplied global strong-convexity bound,
so it applies beyond the certificate class (1). A polynomial-bit
rational approximation reaches a controlled Newton neighborhood.
Polynomially many exact Newton steps then give doubly exponential
accuracy when stored as a shared rational arithmetic circuit.
Real quantifier elimination supplies a separation bound for nonzero
values of the relevant algebraic observable at \(p\). Shifted
comparisons distinguish signs and equality; division elimination
produces one PosSLP instance. The reduction never expands the very
large intermediate numerators and denominators.

The [lower bound](unconstrained-quartic-posslp-reduction.md) first
simulates integer arithmetic by bounded cubic-root circuits, using
the [reviewed simulation](posslp-certified-cubic-root-reduction.md).
A quartic realization gives those roots as its unique zero and
supplies a strict rational Hessian Gram. A small cubic perturbation
turns a designated signal's sign into the minimum's sign while
preserving a full Hessian Gram at least the identity. Every output
minimum is nonzero. Replacing an integer output \(V\) by \(1-V\)
reverses positivity, so both directions of strict and weak order
comparison are covered. The unperturbed realization similarly
gives the coordinate-comparison lower bounds.

For completeness, the SOS consequences use two separate facts.
SOS-convexity and the stationary minimizer imply
\(f-f(p)\) is real SOS, by Taylor integration of the Hessian
certificate. Consequently real SOS and nonnegativity are equivalent
in this class. This Taylor principle is established prior theory;
it is not a new SOS theorem.

Also, under (1),
\[
 \min f>0
 \quad\Longleftrightarrow\quad
 f\text{ has a positive definite rational polynomial Gram}.     \tag{2}
\]
For the forward direction, replace \((f,M)\) by
\((f/\mu,M/\mu)\), so the Hessian Gram is at least the identity,
and choose a rational Taylor center close enough to \(p\).
Completing the linear term leaves a positive rational
constant. The Taylor squares span the homogeneous quadratics; the
completed norm and positive constant span the affine terms. This
gives a positive definite rational Gram for \(f/\mu\); multiplying
that Gram by \(\mu\) gives one for \(f\), as proved in
[the lower-bound note, Section 5](unconstrained-quartic-posslp-reduction.md).
For the reverse direction, \(m_2(X)\) includes the constant one,
so \(m_2(X)^{\mathsf T}Qm_2(X)\ge\lambda_{\min}(Q)>0\).
This proves the positive definite Gram row using exact strict
minimum comparison.

At minimum zero, rational SOS is a different question. The
[reviewed ternary example](ternary-rational-sos-convex-counterexample.md)
satisfies (1), has minimum zero, and is real SOS but has no rational
polynomial SOS. Therefore the nonnegativity upper bound cannot be
used to fill the last row of the table. The hardness construction
has strictly positive yes instances with rational positive definite
Grams and strictly negative no instances, so it does establish that
row's lower bound.

The quartic degree is the first possible one for this classification.
A globally convex polynomial of degree at most three is quadratic:
its Hessian's linear part must vanish, since its scalar quadratic
forms remain nonnegative along both directions of every affine line.
A strongly convex rational quadratic has a rational minimizer and
minimum computable by rational linear algebra. This is an elementary
degree observation, not a separate hardness result.

## Exact witnesses can be short or long depending on their representation

For every strictly feasible unconstrained instance \(\min f<0\)
with a supplied strong-convexity bound, the upper-bound construction
prints a rational feasible point as a polynomial-size shared
arithmetic circuit. Its final Newton point is already more accurate
than the nonzero minimum's separation gap. This is a constructive
statement: no exact sign oracle is needed to build that point,
although exact validation of the printed circuit is not asserted
to be polynomial-time ordinary binary arithmetic.

In contrast, the [rational-witness lower bound](strict-convex-quartic-rational-witness-lower-bound.md)
constructs a polynomial-size family in \(n=2k\) variables satisfying
(1), with \(\nabla^2 f\succeq I\), whose zero sublevel set is
compact, has nonempty interior, and lies in \((-1,5)^n\). Every
rational feasible point has a first-coordinate denominator requiring
\(\Omega(n2^{n/2})\) bits. The universal circuit-witness upper
therefore coexists with superpolynomial expanded rational output.
Neither statement decides membership in NP using ordinary verifiers.

There is also a quantitative distinction between interior and boundary
SOS certificates. A reviewed [upper bound](interior-gram-single-exponential-upper.md)
gives a rational positive definite polynomial Gram of total size
\(\operatorname{poly}(L)2^{O(n)}\) for every strictly positive input
in (1), counting its supplied Hessian Gram in \(L\). A reviewed
[lower family](interior-gram-bit-lower-bound.md) requires
\(\Omega(n2^{n/2})\) denominator bits in every such positive
definite Gram, while retaining a short singular rational Gram and
short rational SOS. The exponential dimension dependence is therefore
qualitatively necessary for interior Grams. This is not a lower bound
for arbitrary rational SOS certificates.

## What the result adds and what remains

Exact SDP and SOCP already encode arithmetic-circuit comparison.
The [lower-bound primary audit](posslp-convex-quartic-prior.md)
checks Tarasov--Vyalyi and the SOCP deduction. The restriction to
one unconstrained globally strongly SOS-convex quartic with a
supplied strict rational Hessian certificate is the added lower-bound
claim. It cannot be replaced by existing hardness of recognizing
quartic convexity, because recognition is already certified here.

The [upper-bound primary audit](strong-convex-quartic-posslp-upper-prior.md)
credits Etessami--Stewart--Yannakakis, Appendix C, Corollary C.8:
Newton iteration, algebraic separation, shared arithmetic, and a
single PosSLP comparison already give completeness for probabilistic
polynomial-system thresholds. The upper bound adapts that established
architecture to supplied global curvature. The complete restricted
classification is the main combined claim. No literature search
establishes publication priority.

For MINLP, the classification identifies an exact arithmetic task
that can remain inside an otherwise well-behaved continuous
relaxation. It could guide interfaces that retain compressed exact
quantities and distinguish a certified sign from a numerical
approximation. Practical value still requires suitable implementations,
manageable circuit growth, and useful instances; none is demonstrated
by the reduction. Constrained optimization, missing curvature bounds,
and the cost of explicit algebraic output require separate arguments.

The [upper review](strong-convex-quartic-posslp-upper-independent-review.md),
[lower review](posslp-unconstrained-quartic-adversarial-review.md),
and [witness review](strict-quartic-rational-witness-independent-review.md)
record independent proof reconstruction and targeted exact checks.
The root read those proofs and reviews and rechecked their composition.
The checks do not implement the full reductions, formalize them in
Lean, or establish novelty. No project-wide verification or CI
inspection is part of this synthesis.
