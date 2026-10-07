# Prior-art audit: precision of rectangular interval certificates

Date: 2026-10-02. This is a focused audit of the weak-active-sign example in
[`implicit-optimum-precision-obstruction.md`](../new-direction/implicit-optimum-precision-obstruction.md).
The proof review passed in
[`implicit-optimum-precision-review.md`](../reviews/implicit-optimum-precision-review.md).
The companion positive strategy that avoids a whole-box gradient-sign test is
compared in [`implicit-convex-patch-prior.md`](implicit-convex-patch-prior.md).
No priority claim is made.

The specific claim concerns one certificate format. An explicit degree-four
rational polynomial on a product box has a unique optimizer, global strong
convexity, graph width two, and fixed coordinate-curvature/growth ratio
\(112/27\). If a rational axis-aligned box contains the optimizer and must
certify \(\partial_y\widetilde F(x,0)\geq0\) for every point of that box,
then its terminal lower endpoint has denominator at least
\(2^{4\cdot2^n-2}\). This remains true if the certificate computes the exact
range of the derivative. The bound is on the ordinary binary encoding of that
endpoint. It does not rule out a compact recurrence, a root enclosure that
allows zero as its endpoint, a correlated proof at the implicit root, or other
certificate formats.

## Established interval methods

**Active-gradient signs and monotonicity tests are standard.** Neumaier’s
complete-search survey gives the first-order boundary sign conditions for box
constraints (§5, printed pp. 14–15), interval Newton/Krawczyk operators for
enclosing or excluding roots (§11, pp. 31–32), and box branch-and-bound (§12,
pp. 33–35). It also describes interval derivatives as optimality constraints
for constraint propagation and verification (§22, pp. 62–63). In the standard
monotonicity test, a derivative enclosure with a fixed sign excludes an
interior minimizer and can reduce a boundary box to a face. This is the
closest methodological comparator: the proposed certificate applies the
lower-bound KKT sign test uniformly over an enclosing free-coordinate box.
Neumaier’s treatment is about sound pruning and convergence at prescribed
tolerances; it does not bound the binary encoding length of rational boxes in
terms of input length and conditioning. He notes that rigorous methods can
exceed requested tolerances near degeneracy (§1), and that objective accuracy
alone may localize a minimizer only to order \(\sqrt{\epsilon}\), or worse for
a singular Hessian (§15, pp. 43–45). See [Neumaier (2004),
§§1, 5, 11–12, 15, 20, 22](https://doi.org/10.1017/S0962492904000194),
especially pp. 4–6, 14–15, 31–35, 43–45, 63–65.

Araya, Trombettoni, and Neveu give an adaptive interval-constraint
propagator that combines monotonicity-based image evaluation and interval
Newton narrowing. Their monotonicity-based extension is sharp when variables
repeated in an expression are monotone; the narrowing loop has logarithmic
dependence on a user-set relative interval precision (Propositions 1–4 and
Lemma 1, pp. 2–5). For the candidate, however, \(\log_2(1/a_n)=\Theta(2^n)\),
so a logarithmic dependence on requested coordinate precision can still be
exponential in the succinct input length. This is relevant because it removes ordinary interval
dependency overestimation in the monotone case. The current example survives
that improvement: \(\partial_y\widetilde F(x,0)=(x_n-x_{n-1}^2/8)/4\) is
increasing in \(x_n\) and decreasing in the nonnegative coordinate
\(x_{n-1}\), so the required corner is also the exact range minimum. The
required positive lower endpoint follows from the range itself, not from a
loose natural interval extension. The active derivative at the optimizer is
also only \(a_n/8\), so a numerical sign test using absolute error tolerance
must resolve a margin whose binary precision is \(\Theta(2^n)\). See [Araya et al. (2010),
“Exploiting Monotonicity in Interval Constraint Propagation”](https://doi.org/10.1609/aaai.v24i1.7541).

Adjiman, Dallwig, Floudas, and Neumaier use interval Hessian enclosures to
construct rigorous convex underestimators in \(\alpha\)BB. They show that
natural interval extensions can substantially overestimate curvature and
that algebraic reformulation or tighter enclosures can improve the bound
(Theorems 2.1 and 3.1 and the two-variable example, pp. 3–8). That is a
different issue from the present lower bound: the proposed derivative range
is exact, and no improvement in interval arithmetic can remove the forced
endpoint magnitude. See [Adjiman et al. (1998), Part I](https://doi.org/10.1016/S0098-1354(98)00027-1).

The classical interval literature therefore supplies the certificate
operation and its proof logic. The current obstruction identifies a specific
output-size limitation when that operation is required to establish the weak
active sign on every point of one independent-coordinate rectangle. It is not
a lower bound for interval branch-and-bound as a whole: subdivision may retain
many boxes, a different test may preserve cross-coordinate relations, and an
implicit root certificate can use the short residual recurrence directly.

## Repeated squaring and output length

Repeated squaring is a standard way to encode very small or very large
quantities with a short chain of bounded-degree equations. Deligkas, Fearnley,
Melissourgos, and Spirakis use a repeated-squaring chain in their proof that
approximate ETR remains ETR-hard: a polynomial-size formula forces a value
of doubly-exponential magnitude (Theorem 2 and §2.1, pp. 4–6). This supports
the general warning that numerical magnitude and representation length can
diverge sharply in succinct polynomial systems. Their result concerns
approximate feasibility and unbounded variables, not strongly convex
optimization on a bounded box or the size of an interval certificate. See
[Deligkas et al. (2022)](https://doi.org/10.1016/j.jcss.2021.11.002) and the
[open arXiv text](https://arxiv.org/abs/1810.01393).

O’Donnell gives a related bit-complexity example for degree-two
sum-of-squares proofs. Even with variables explicitly bounded, every degree-2
SOS proof for the constructed claim has \(\Theta(2^n)\) bit complexity
(Theorem 1, p. 6), due to repeated-squaring coefficient growth. This is a
proof-size obstruction for one SDP/SOS representation, not a rational-root
or interval-box lower bound. See [O’Donnell (2017)](https://doi.org/10.4230/LIPIcs.ITCS.2017.59).

These sources establish that succinct recurrences can force exponentially
long expanded numerical objects in neighboring settings. They do not give
the current combination of a unique rational optimizer, fixed graph width,
uniform strong convexity and quadratic growth, and a lower bound for a
whole-box active-gradient certificate. The proposed result should be stated
as that precise certificate-format obstruction, without claiming that
interval methods or exact certification generally require exponential
precision.

## Comparison boundary

The established ingredients are box subdivision, monotonicity/active-gradient
tests, interval Newton and Krawczyk verification, and repeated-squaring
constructions. The candidate’s contribution, if retained, is the explicit
strongly convex width-two instance showing that uniform growth and curvature
do not bound the endpoint bits needed by a *single rational rectangle* whose
whole free-coordinate range must satisfy the weak active KKT sign. Exact
range evaluation is already covered, so this is not merely an interval
dependency example. The short residual recurrence and the candidate’s
correlated sign proof demonstrate why the conclusion must remain limited to
that rectangle test. No claim is made about all global-optimization
certificates or all exact algorithms.

No new literature item was required for this audit; all cited full texts are
already in the local literature collection. No literature-KB files were
edited. Targeted source review only; no project-wide checks or CI inspection
were run.
