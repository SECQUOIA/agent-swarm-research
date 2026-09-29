# Prior comparison for the proposed five-variable degree bound

Date: 2026-09-28. Status: bounded primary-source search. No equivalent
theorem was located in the inspected sources; this does not establish
novelty. This is a literature comparison, not an independent proof audit
of the [new geometric draft](five-variable-positive-base-bound.md).

## The exact candidate

The proposed arithmetic conclusion is
$[\mathbb Q(p):\mathbb Q]\leq21$ for a globally convex polynomial
$F=\sum_jq_j^2$ in five affine variables, with rational quadratic
$q_j$, a unique real zero $p$, and positive definite Hessian at $p$.
The existing cyclic construction attains 21 in the stronger globally
strongly convex class.

The additional geometric statement is about an arbitrary real linear
system of quadrics in $\mathbb P^5$. If its full base has at least 23
distinct points where the quadratic Jacobian has projective rank five,
and every positive-dimensional component has no real point, then the
full base is finite. The counted points may be nonreal. This matters
when comparing it with bounds on the number of real zeros.

## Closest prior and the remaining difference

Eisenbud, Green, and Harris,
[*Higher Castelnuovo Theory*](https://eisenbud.github.io/papers/pdfs/1993-002.pdf)
(1993), Section 3, printed pp. 195–199, states the modern
Cayley–Bacharach identity for mutually residual subschemes of a
zero-dimensional complete intersection. Theorem 2 proves the
low-degree dependent-condition bounds, including the length-eight
quadratic boundary case. Its assumptions permit nonreduced schemes.
The inspected argument requires containment in a finite quadratic
complete intersection. It does not automatically provide such an
intersection when all quadrics through a set have a positive-dimensional
base. Section 1 expressly frames its cardinality questions with a
zero-dimensional quadratic intersection hypothesis.

For the present application, this classical result and odd field degree
give the earlier conditional bound 23. The
[finite residual note](degree23-residual-obstruction.md) adds a
real-parity argument excluding odd residual lengths at most nine.
The new geometric draft supplies the separate positive-base argument.
The comparison concerns those two combinations of known tools;
neither complete-intersection duality nor a new general
Cayley–Bacharach theorem should be claimed as the contribution.

Fulton–Lazarsfeld positivity, Eklund–Jost–Peterson generic residual
degrees, and the minimal-degree classification are the closest
geometric ingredients. Their exact statements and assumptions are
recorded in the separate
[primary-source audit](small-residual-and-excess-prior.md).
They supply the weighted degree reduction, residual formula, and
low-degree models. That audit did not locate a packaged theorem with
the candidate's real-base and 23-point hypotheses. The threshold
argument is assembled from these classical results and the real
low-degree case analysis.

Nie and Ranestad,
[*Algebraic Degree of Polynomial Optimization*](https://arxiv.org/pdf/0802.1233),
Section 3.1 and Theorem 2.2, give the generic unconstrained critical
degree $(d-1)^n$ and its corresponding bound under finiteness hypotheses.
For quartics this is $3^n$. This is established prior for high
arithmetic complexity in polynomial optimization, but it neither
fixes the minimum at a rational value nor imposes rational quadratic
squares and a unique real zero. The generic critical-point count is
therefore not an equivalent sharp bound for this special zero fiber.

Slot, Steurer, and Wiedmer,
[*Hesse's Redemption*](https://arxiv.org/html/2511.03440v1),
Appendix C, Lemma C.3, proves that a rational univariate convex quartic
with rational minimum has rational minimizer. The appendix gives
irrational minimizers and a degree-six rational-zero example, and
discusses exact witness issues. The inspected version does not state
the five-variable extremum. Its algorithmic results concern approximate
optimization and should not be represented as contradicted by an
exact arithmetic bound.

Scheiderer,
[*Sums of squares of polynomials with rational coefficients*](https://ems.press/content/serial-article-files/32129)
(2016), Section 4, Theorem 4.1 and paragraph 4.14, treats rational
SOS descent for ternary quartic forms. Paragraph 4.14 explicitly gives
a rational sum of three quadratic squares with one real cubic node
and two nonreal conjugate nodes. This is strong prior for an irrational
unique real zero of a rational SOS quartic. Its dimension is two after
dehomogenization, and it does not assert the present convex
five-variable upper bound. The published Section 4 was rechecked in
the saved local text; the example is absent from the earlier arXiv
version.

Hassett, Kollár, and Tschinkel,
[*Rationality of even-dimensional intersections of two real quadrics*](https://ems.press/content/serial-article-files/43557)
(2022), Theorem 1.1 and Section 3, concerns smooth intersections of two
quadrics, rationality, and odd-degree subvarieties. Proposition 3.2
extracts a rational point from an odd-degree subvariety. These are
related real-algebraic parity and quadratic-intersection statements,
but their smooth complete-intersection and rationality conclusions
do not supply the asserted isolated-point threshold for a general
quadratic linear system in $\mathbb P^5$.

## Search scope and interpretation

Searches combined convex quartic, rational minimum, unique zero,
algebraic degree, degree 21, five variables, real quadratic complete
intersection, Cayley–Bacharach, 23 points, 22 points, isolated points,
positive-dimensional base, and excess intersection. Searches also
used the words twenty-two and five quadrics. Primary-source follow-up
covered the works listed above and the earlier excess audit.

The searches produced several unrelated uses of the same words:
convex regions bounded by determinantal quartics, counts of real
nodes, topology of smooth intersections of two quadrics, and generic
critical-point counts. None was treated as an equivalent statement
about the coordinate-field degree of one unique real zero. Search
snippets and repository reviews were leads, not substitutes for the
primary statements identified above.

The candidate's defensible significance, conditional on proof
verification and broader priority review, is a sharp arithmetic
extremum for a regular rational-SOS convex class. It strengthens the
elementary degree-31 bound in this dimension and identifies the
attainable endpoint 21. It does not presently improve a solver,
establish an exact complexity lower bound, or cover arbitrary rational
convex quartics without a rational SOS decomposition. A compact
classical proof can still yield a useful sharp result; the absence of
a located equivalent theorem is only evidence from this scoped search.

## Verification record

The candidate draft, finite residual note, existing quartic prior
audits, and the listed primary sections were examined. The EGH scan
was compared with its saved OCR transcript; endpoint details already
have a separate source audit, since the OCR loses weak inequalities.
Fresh delegation of this narrow search was attempted but rejected by
the agent thread limit. The present author contributed earlier
geometric source leads and does not claim full independence from the
new theorem's development.

Only this Markdown file received a targeted structural check. No
mathematical checker, project-wide tests, or CI inspection was run for
this literature audit.

