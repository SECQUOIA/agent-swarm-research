# Prior results for quasiconvex mixed-integer values

Date: 2026-09-28. Status: focused primary-source audit, with
[independent review](quasiconvex-mixed-value-prior-review.md). This supplements
[the convex value audit](generic-convex-mixed-value-prior.md); it does not
establish novelty or replace the proposed theorem's proof.

The question is whether an existing theorem bounds the algebraic degree
and coefficient bit length of a finite, possibly unattained value

\[
\theta=\inf\{t:(z,t)\in E,\ z\in\mathbb Z^k\},
\]

when the rational semialgebraic set \(E\) is upward closed in \(t\)
and every strict projected sublevel
\(C_\tau=\{z:\exists t<\tau,\ (z,t)\in E\}\) is convex.
Joint convexity of \(E\) is not assumed. The proposed bounds depend on
fixed dimensions, individual atom degree and coefficient bit length,
but not atom count. Bounded blocks of quantified real variables are
also allowed. This audit did not verify a prior theorem with all these
properties. That is a statement about the sources checked below, not a
claim that no such theorem exists.

## 1. Heinz and Hildebrand--Köppe: exact, but pure integer objectives

The strongest directly inspected statement in this line is
Hildebrand--Köppe, *A new Lenstra-type Algorithm for Quasiconvex Polynomial
Integer Minimization with Complexity* \(2^{O(n\log n)}\),
[author preprint](https://arxiv.org/pdf/1006.4661).
Equation (1), p. 1, minimizes an integer-coefficient quasiconvex polynomial
\(\widehat F(x)\) under integer-coefficient quasiconvex polynomial
constraints, with **every coordinate of \(x\) integral**.

Theorem 1.1, p. 2, gives an exact algorithm returning a minimum point or
confirming that none exists. For degree bound \(d\ge2\), individual
coefficient bit bound \(l\), and \(s\) constraints, its general-case
output bound is \(l d^{O(n)}\), independent of \(s\); its running time
depends on \(s\). The proof on p. 25 uses a bounded-size ball containing
some minimizer, if one exists, and bounds the integer objective value.
It identifies its reasoning with Heinz's Theorem 5.1.

These are significant quasiconvex predecessors, but integer-valued
objectives cannot have a finite unattained infimum over a nonempty
feasible set. The stated theorem therefore does not give the proposed
free-real value bound. Replacing the objective by an integral threshold
coordinate only supplies a rounding of that value.

Heinz (2005), *Complexity of integer quasiconvex polynomial optimization*,
J. Complexity 21, 543--556, was checked through its
[publisher abstract](https://www.sciencedirect.com/science/article/pii/S0885064X05000348)
and [author poster](https://www.damtp.cam.ac.uk/user/na/FoCM/FoCM05/Posters/heinz.pdf),
which give the same pure-integer formulation. The original full theorem
was not independently inspected in this focused audit; the precise
theorem comparison above uses Hildebrand--Köppe's full text.

## 2. Espinoza--Fukasawa--Goycoolea: a genuine unattained-value predecessor

Espinoza--Fukasawa--Goycoolea (2010), *Lifting, tilting and fractional
programming revisited: a study on mixed integer linear sets*, Operations
Research Letters 38, 559--563,
[author PDF](https://mgoycool.github.io/papers/10espinoza_orl.pdf),
studies

\[
M=\{x\in\mathbb R^n:Ax\ge h,\ x_i\in\mathbb Z\ (i\in I)\},
\qquad
\inf_{x\in M}\frac{a^Tx-b}{c^Tx-d},
\]

with rational data, nonempty, possibly unbounded \(M\), and denominator
nonzero on \(M\). Section 2 assumes \(c^Tx-d\ge0\); Section 5
separates denominator signs.

Theorem 2.3(5), manuscript p. 2, identifies the finite value upon
termination as either a feasible-point ratio or a recession-direction
ratio \(a^Tr/c^Tr\). Section 5, pp. 5--6, explicitly constructs
asymptotically optimal sequences and treats nonattainment. The p. 3
convergence paragraph gives finite termination when the MIP oracle
returns only finitely many possible solutions.

No atom-independent degree/height theorem is stated. Rationality follows
using rational mixed-integer hulls. A binary-size bound needs a further
hull-size argument, which should be checked before claiming a new
linear-fractional value-size result. Arbitrary semialgebraic or conic
regions are outside the stated theorem.

Restricting the continuous domain to \(c^Tx-d>0\), strict ratio
sublevels are affine cuts of that convex domain. Thus the comparison
is substantive; nonlinear constraints and algebraic values are the
additional fractional-MISOCP scope.

## 3. Mixed-integer pseudoconvex algorithms with bounded domains

Westerlund--Pörn (2002), *Solving Pseudo-Convex Mixed Integer Optimization
Problems by Cutting Plane Techniques*, Optimization and Engineering 3,
253--280, is a genuine mixed-integer predecessor:
[author PDF](https://users.abo.fi/twesterl/some-selected-papers/40.%20OPTE-TW-RP-2002.pdf).
Printed pp. 255--256 assume differentiable pseudoconvex objective and
constraint functions, a compact continuous domain \(X\), a finite
integer domain \(Y\) defined by variable bounds, and a nonempty feasible
region. The convergence paragraph on p. 258 explicitly uses compactness
of \(X\) and finiteness of \(Y\). This establishes earlier algorithmic
work beyond jointly convex objectives, but does not supply the proposed
unbounded, possibly unattained algebraic-value theorem.

Zhong--You (2014), *Globally convergent exact and inexact parametric
algorithms for solving large-scale mixed-integer fractional programs and
applications in process systems engineering*, remains an access-limited
lead: [publisher page](https://www.sciencedirect.com/science/article/abs/pii/S0098135413003396).
The full article was not obtained. [Author slides](https://cache.org/sites/default/files/winter15-You.pdf),
slide 13, describe exact/inexact Newton iterations and accuracy of MIP
subproblem solutions. They do not verify the article's complete
hypotheses or a symbolic algebraic-value output theorem. No stronger
claim is based on this source.

## 4. An older fractional source requires caution

Abbas--Moulai (1999), *An Algorithm for Mixed Integer Linear Fractional
Programming Problems*, Belgian Journal of Operations Research,
Statistics and Computer Science 39(1), 21--30,
[primary PDF](https://www.orbel.be/jorbel/index.php/jorbel/article/download/295/256),
has a broad abstract, but Theorem 2's proof on printed p. 27 incorrectly
asserts that an unbounded feasible set prevents attainment. A constant
ratio on an unbounded set already disproves that assertion.
Algorithm Step 1, p. 26, also returns an unattained continuous supremum
before checking integer feasibility. For example, impose
\(x=1/2\), \(y\ge0\), require \(x\) integral, and maximize
\(y/(1+y)\). The continuous supremum is 1, while the mixed-integer
set is empty. The stronger, carefully delimited Espinoza et al. result
is preferable to treating this older paper's general statement as
verified prior art for arbitrary unbounded mixed-integer domains.

## 5. Strict-sublevel convexity does not control attainment

For any rational semialgebraic \(S\subseteq\mathbb R^k\), let

\[
E=(\mathbb R^k\times(0,\infty))\cup(S\times\{0\}).
\]

This set is upward closed. Its strict projected sublevels are empty
for \(\tau\le0\) and all of \(\mathbb R^k\) for \(\tau>0\), so
all are convex. The mixed-integer infimum is always 0, but it is
attained exactly when \(S\cap\mathbb Z^k\ne\varnothing\).
Consequently, strict-sublevel convexity alone leaves the exact boundary
arbitrary. This example does not refute the proposed value bound. It
does prevent an automatic transfer of small optimal-witness or
attainment-algorithm conclusions from the jointly convex setting.
Those conclusions need additional boundary hypotheses, such as convex
weak level sets \(\{z:(z,t)\in E\}\), together with an appropriate proof.
Positive-denominator linear-fractional models on convex continuous
domains have convex weak as well as strict levels.
An explicit fixed-dimensional Pell example in
[the proposed theorem's Section 7](quasiconvex-mixed-value-frontier.md#7-why-strict-sublevels-do-not-control-optimal-witness-size)
shows exponential optimal-witness bit length under these strict-level
hypotheses while the optimal value remains zero.

Verification: inspected the full Hildebrand--Köppe, Espinoza et al.,
Westerlund--Pörn, and Abbas--Moulai primary PDFs at the pages cited above;
used only the stated abstract/poster/slides access for Heinz and
Zhong--You. The independent review found no substantive error in its
stated scope; its denominator-domain clarification was applied.
`git diff --check -- research-20260927/quasiconvex-mixed-value-prior.md`
passed, and a targeted Python `Path.is_file()` check confirmed the local
comparison and frontier links. Source inspection used `pdftotext -layout`,
targeted `rg -n` searches, and `sed -n` excerpts. No project-wide checks
or CI inspection were performed.
