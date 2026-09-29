# Prior comparison for rational minimizers with long denominators

Date: 2026-09-28. Status: scoped primary-source reading; publication
priority is unestablished.

The target result is the
[unit-circle quartic construction](rational-convex-quartic-minimizer-height.md):
a polynomial-size rational quartic with a unique rational minimizer in
\([-1,1]^N\), whose terminal coordinate denominators require
\(2^{\Omega(N)}\) bits. The construction supplies short rational
square factors and a short positive definite rational full Hessian
Gram. The main distinctions are rationality of the actual minimizer,
bounded coordinates, unconstrained optimization, and a single globally
strongly SOS-convex quartic.

## Convex polynomial approximation does not bound denominators

[Slot, Steurer, and Wiedmer, *Hesse's Redemption: Efficient Convex
Polynomial Programming*, arXiv:2511.03440v1](https://arxiv.org/html/2511.03440v1),
Theorem 1.1 and Corollary 1.2, give polynomial bounds on logarithmic
minimizer norm and polynomial-time additive approximation over rational
polyhedra. The norm bound does not bound rational denominators. Their
Section 1.3 distinguishes approximate witnesses from compact rational
witnesses for an exact threshold. Appendix C gives irrational optimizer
examples and a univariate degree-four rationality statement when the
minimum value is rational; it does not supply a height bound for rational
multivariate minimizers.

The circle family is consistent with the approximation theorem:
its minimizer has bounded norm and is easy to approximate, but its exact
fraction representation is long. This comparison concerns the inspected
v1 preprint. No claim is made about an uninspected proceedings version.

## Exact optimization with rational minimizers assumes their height

[Jiang, *Minimizing Convex Functions with Rational Minimizers*,
arXiv:2007.01445v5](https://arxiv.org/pdf/2007.01445v5), Theorem 1.6,
treats separation-oracle optimization when the minimizer set is a
bounded rational polyhedron with bounded LCM vertex complexity.
Definition 2.6 measures the logarithm of a common denominator of a
vertex. This parameter is an assumption in the oracle complexity bound,
not a consequence of a small polynomial description of the objective.

For the circle family, the minimizer set is a rational singleton in the
unit box. Its least common denominator is exactly \(5^{2^k}\), so
its LCM vertex complexity is
\(\lceil2^k\log_2 5\rceil\). Thus a polynomial bound on that
parameter cannot be inferred from bounded coordinates and a short
strongly SOS-convex quartic description. This does not contradict
Jiang's theorem or the earlier Grötschel--Lovász--Schrijver methods
that it improves.

## Large convex witnesses are established prior

[Pataki and Touzov, *How Do Exponential Size Solutions Arise in
Semidefinite Programming?*, arXiv:2103.00041v2](https://arxiv.org/pdf/2103.00041v2),
pages 2--3, recalls Khachiyan's convex quadratic system
\(u_i\geq u_{i+1}^2\), \(u_m\geq2\). Every feasible point
has \(u_1\geq2^{2^{m-1}}\), forcing exponential bit length.
Each quadratic row has a two-by-two semidefinite representation.
That example is unbounded and forces large coordinate magnitudes.
It is not an unconstrained strongly convex quartic with a bounded
rational unique minimizer.

The general phenomenon of exponential rational output length is
therefore not new. The unit-circle construction addresses the stated
more restrictive setting. Merely replacing large variables by their
reciprocals would not preserve convexity of an arbitrary system and
would not prove the asserted quartic result.

## Exponentially long rational local minimizers are also known

[Zhang, *Complexity Aspects of Fundamental Questions in Polynomial
Optimization*, Example 2.5.3, printed pages 49--50](https://optimization-online.org/wp-content/uploads/2020/08/7992.pdf),
constructs cubic polynomials \(y^{\mathsf T}A_n(x)y\) whose local
minimizers require exponential bit length. Their local-minimizer set
is \(\{x:A_n(x)\succ0\}\times\{0\}\); the block structure
forces \(x_1\geq4,x_2\geq16,\ldots,x_n\geq2^{2^n}\).
Rational local minimizers exist. The polynomial is nonconvex, the
local-minimizer set is unbounded, and the large representation comes
from coordinate magnitudes.

This is a direct optimizer-height predecessor. It does not already
give a bounded unique rational global minimizer for a strongly convex
quartic. The fresh reviewer located this source; the author separately
opened and read the example and its surrounding discussion.

## General upper bounds permit exponential rational height

[Safey El Din and Zhi, *Computing Rational Points in Convex
Semialgebraic Sets and SOS Decompositions*, arXiv:0910.2973v1](https://arxiv.org/pdf/0910.2973v1),
Theorem 1.1, decides rational feasibility of a convex semialgebraic
set defined by a quantifier-free formula with \(s\) integer
polynomials of degree at most \(D\) and coefficient bit length
\(\sigma\). If a rational point exists, their algorithm returns
one with coordinate bit length at most \(\sigma D^{O(N^3)}\).
The assumptions include lower-dimensional convex sets and therefore
rational singletons.

After clearing denominators, the circle family is one such set,
\(\{F_k\leq0\}\), with degree four and polynomial coefficient
bit length. Its exponential lower bound is compatible with that upper
bound. The result does not match the upper bound's dependence on
\(N\), and no such matching claim is made.

## Search record and limitations

The searches used combinations of `convex polynomial`, `rational
minimizer`, `bit length`, `height`, `denominator`, `convex quartic`,
`SOS-convex`, `exponential`, and `unit circle`. Primary texts were
opened and read for the five comparisons above, including Jiang's
Theorem 1.6 and Definition 2.6 and Safey El Din--Zhi's Theorem 1.1.
The local text copy of *Hesse's Redemption* was also read in Sections
1.1--1.3 and Appendix C. The detailed algorithms in these papers have
not been independently rederived in this audit.

No inspected source supplies all the restrictions of the target
construction. That finding does not establish novelty. In particular,
equivalent examples may occur under exact optimization, rational
reconstruction, arithmetic dynamics, or semidefinite representations.
The elementary fact that powering a rational point of the unit circle
increases its denominator is not claimed to be new. The proposed
contribution is its realization as the rational optimizer of a short,
globally strongly SOS-convex quartic with short rational certificates.

## Targeted documentation checks

The author ran an inline `python -` check on the six authored notes
for optimizer height, prior comparison, optimal Gram height, local
conditioning, quaternion sign compilation, and their coordinate-comparison
composition. It passed final-newline, whitespace, control-character,
math-delimiter, and eighteen local-link checks. A targeted
`git diff --check --` on the optimizer-height notes, their two initial
reviews, and the independent checker also passed. Mathematical checker
commands and their limits are recorded in the respective result notes.
No project-wide verification or CI inspection was used.
