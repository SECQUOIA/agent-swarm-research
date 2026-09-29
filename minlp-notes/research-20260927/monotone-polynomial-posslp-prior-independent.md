# Independent prior-work audit: exact strongly convex polynomial comparison

Date: 2026-09-28. This is a literature-scope audit, not a proof review.
It supplements [the main prior-work audit](strong-convex-quartic-posslp-upper-prior.md)
and [the source supplement](strong-monotone-exact-prior-supplement.md).

The target is exact rational-threshold comparison of the minimum or a
minimizer coordinate of an explicitly encoded rational quartic, with a
supplied rational \(\mu>0\) satisfying
\(\nabla^2 f(x)\succeq\mu I\) for every \(x\in\mathbb R^n\).
The proposed upper bound is a polynomial-time **many-one** reduction to
PosSLP, including equality at the threshold. The narrower certified input
class also has a proposed matching lower bound. Those proofs are recorded
separately in [the main result](strong-convex-quartic-posslp-upper.md).

None of the additional primary statements inspected below gives this
classification. Several establish exact optimizer representations or
finite convergence and must be acknowledged. This source check narrows
the risk of an overlooked equivalent theorem; it does not establish
priority or novelty.

## 1. Convex optimization gates already give fixed-point representations

Filos-Ratsikas, Hansen, Høgh, and Hollender,
[*FIXP-membership via Convex Optimization: Games, Cakes, and Markets*](https://arxiv.org/pdf/2111.06878v3),
arXiv v3, 25 April 2023, Theorem 3.2, printed page 19, constructs an
algebraic circuit in polynomial time for a bounded convex program with
linear equalities, convex inequalities, and subgradient pseudogates.
Under their explicit Slater condition, its auxiliary fixed points project
to optimal solutions. Definition 3.4 requires a point strictly inside the
box and all inequalities, together with linearly independent equality
rows. Definition 3.2 makes the representation precise: the correct output
is obtained at a fixed point of the auxiliary coordinates. The published
article has [DOI 10.1137/22M1472656](https://doi.org/10.1137/22M1472656);
the inspected theorem text is from arXiv v3.

For the present target, a box containing the minimizer and polynomial
gradient circuits fit this framework. This is an application of an
existing optimizer representation. It does **not** provide an ordinary
finite arithmetic circuit evaluating the optimizer, or an algorithm
deciding the sign of an optimizer coordinate in PosSLP. The auxiliary
fixed-point problem still has to be solved.

## 2. Contraction results concern approximation

Etessami and Yannakakis,
[*On the Complexity of Nash Equilibria and Other Fixed Points*](https://homepages.inf.ed.ac.uk/kousha/nash_focs07_full_j_spec_issue_sub.pdf),
SIAM Journal on Computing 39(6), 2010, Proposition 2, author-manuscript
page 16, reduces strong approximation to weak approximation for their
polynomially contracting maps. With polynomial computability, strong
approximation belongs to PPAD. The contraction definition on page 13
allows a factor below \(1-2^{-q(|I|)}\), for a polynomial \(q\).
This statement concerns proximity to a fixed point, rather than exact
rational-threshold comparison. In particular, it does not resolve
equality or supply the proposed many-one PosSLP upper bound.

Terminology matters. For a gradient, strong monotonicity means
\[
 (\nabla f(x)-\nabla f(y))^T(x-y)\geq\mu\|x-y\|^2.
\]
This differs from the coordinatewise order preservation of nonnegative
polynomial systems. A supplied binary rational \(\mu\) also does not imply
an inverse-polynomial condition number. Describing the target merely as
"well conditioned" would conceal a material part of its input model.

## 3. Finite SOS convergence is not an exact bit-complexity classification

De Klerk and Laurent,
[*On the Lasserre hierarchy of semidefinite programming relaxations of convex polynomial optimization problems*](https://ir.cwi.nl/pub/18610/18610D.pdf),
SIAM Journal on Optimization 21(3), 2011, Corollary 3.3, proves finite
convergence under convexity, Slater's condition, an Archimedean quadratic
module, and positive definite objective Hessian at the minimizer. It
does not give the target exact-decision bound. Theorem 4.2 rules out a
uniform relaxation-order bound depending only on the listed dimensions,
degrees, and support sizes. Those parameters omit coefficient bit lengths
and a supplied curvature bound; the theorem does not rule out a bound
using these additional parameters. The final CWI version is used because
earlier versions have different numbering.

The newer source must be compared in its current form. Đurašinović and
Lasserre,
[*Finite convergence of the Moment–SOS hierarchy under hidden convexity*](https://arxiv.org/pdf/2603.00284v2),
arXiv v2, 5 August 2026, Assumption 3.1 and Theorem 3.4, assumes a compact
set with a redundant unit-ball inequality, SOS-concave defining
inequalities, and a Hessian representation
\[
 \nabla^2 f=\sum_{j=0}^{m+1}L_jL_j^Tg_j,\qquad g_0=1.
\]
Writing \(a_j\) for the maximum degree of an entry of \(L_j\) and
\(d_j=\lceil\deg(g_j)/2\rceil\), it proves exactness and minimizer
recovery from first moments at relaxation orders satisfying
\[
 N\geq N_{\min},\qquad
 N\geq1+\max\{a_0,\max_{j\geq1}(a_j+d_j)\}.
\]
Here \(N_{\min}\) is the minimum order needed to represent the objective
and constraints. Strong convexity on the set guarantees existence of the
Hessian representation through a matrix Positivstellensatz. The stated
order depends on certificate degrees, rather than a proved polynomial
bound in rational input length and supplied curvature. The representation
need not be known to construct the hierarchy. The paper does not give an
exact bit-cost or PosSLP classification.

Even when a small exact SDP representation is available, exact threshold
decision for that representation is an additional issue. Finite
mathematical exactness alone cannot replace the arithmetic-circuit
construction required by the present upper bound.

## 4. Other inspected results and the contribution that remains to distinguish

The [source supplement](strong-monotone-exact-prior-supplement.md) checks
Nie–Sun–Tang–Zhang's polynomial variational inequality method and
Cucker–Krick–Malajovich–Wschebor's condition-dependent real-zero counting.
The first proves finite convergence with polynomial optimization
subproblems under its finiteness and genericity assumptions. The second
has an arithmetic bound exponential in dimension. Neither inspected
theorem gives polynomial-time exact comparison for the target.

The strongest relevant arithmetic precedent remains the PPS threshold
classification and compressed Newton method of Etessami, Stewart, and
Yannakakis, already checked in
[the main audit](strong-convex-quartic-posslp-upper-prior.md). Likewise,
the Allender–Bürgisser–Kjeldgaard-Pedersen–Miltersen bridge from real
computation to \(\mathrm P^{\mathrm{PosSLP}}\) must not be relabeled a
many-one PosSLP theorem, and fixed algebraic machine constants must not
be relabeled an arbitrary input family of polynomial roots.

The defensible contribution, if the separate proofs withstand review,
is the exact complexity theorem for this explicitly encoded global
gradient class, including its supplied-curvature promise and equality
cases. It is not the first use of Newton iteration in compressed
arithmetic, the first fixed-point representation of convex optimization,
or the first finite SOS representation of strongly convex minima.

## Verification record

The theorem statements and definitions above were read in the linked
primary versions. A separate agent checked the de Klerk–Laurent,
polynomial-VI, and zero-counting source scopes in the supplement. The
additional OPT-gate and 2026 Moment–SOS interpretations passed a fresh
independent source check. That check also confirmed that the 2026 order
is sufficient, not asserted to be the smallest exact order. No
mathematical proof in the result files was changed or verified by this
literature task.

Targeted verification: a Python check passed for final newline,
whitespace, control characters, paired math delimiters, and five local
Markdown links. The command
`git diff --check -- research-20260927/monotone-polynomial-posslp-prior-independent.md`
passed. No project-wide verification or CI inspection was run.
