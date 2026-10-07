# Prior-art comparison: PosSLP through convex point output

Date: 2026-10-02. This is a focused comparison of the proposed
[PosSLP-to-convex-point reduction](../new-direction/posslp-convex-point-extraction.md)
with primary sources. The saved reduction now has degree four and arbitrary
primal interaction graph. Its actual-file mathematical review passed; see the
[independent review](../reviews/posslp-convex-point-review.md). This is not
publication-priority clearance.

## Strong approximation of actual solutions is established

Etessami and Yannakakis already reduce PosSLP, by a polynomial-time
many-one reduction, to strong approximation of an actual solution coordinate
in a Nash equilibrium. Their Theorem 4(1) gives a promised-gap decision
problem for four-player Nash: the game has a unique equilibrium and a
designated strategy probability is either exactly zero or exactly one.
Theorem 4(2) gives the three-player variant: for every fixed positive
`epsilon`, distinguish probability zero from probability greater than
`1-epsilon`, still with a unique equilibrium. The paper also allows
`epsilon=2^{-poly}` in this second result. These are gap/point-output claims
about a genuine solution; they are not weak-equilibrium residual guarantees.
See “On the Complexity of Nash Equilibria and Other Fixed Points,”
[DOI 10.1137/080720826](https://doi.org/10.1137/080720826), Theorem 4,
printed pp. 21–22; the full theorem and PosSLP proof are in the local primary
text `literature/papers/etessami2010-on-the-complexity-of-nash/fulltext.md`
(pp. 21–31).

This is the strongest direct precedent for the *complexity and output
pattern*. It means the proposed result is not the first constant-accuracy
hardness transfer to an actual solution or a unique solution. The proposed
transfer is into a different problem class: minimizers of an explicitly
given rational quartic that is jointly convex on its rational feasible box,
with a designated coordinate separated by one for its unique optimizer. The
candidate does not claim whole-space convexity or bounded interaction width.
Nash equilibrium conditions are nonlinear fixed-point or
complementarity conditions, not global minimization of an explicit convex
objective. The relevant contribution is this transfer of PosSLP to
constant-accuracy point output for this box-convex polynomial optimization
class.

## Exact convex-feasibility precedent

Tarasov and Vyalyi give a close convex-programming comparison. The read
primary text defines exact semidefinite feasibility (SDFP) as deciding
whether a rational affine subspace of symmetric matrices intersects the
positive-semidefinite cone. Theorem 4 reduces arithmetic-circuit comparison
to SDFP; Theorem 3 supplies the basis reductions, including to
division-free circuits. The direction is from arithmetic sign decisions to
exact convex semidefinite feasibility. It does not give the proposed output
guarantee: SDFP asks only whether a feasible matrix exists and does not
approximate any point of a polynomial minimizer set. The SDFP model is a
rational affine matrix pencil intersected with the PSD cone, not polynomial
minimization over a compact box. The candidate instead asks for a point near
the unique optimizer of a polynomial convex on its box, with a constant
coordinate gap. See “Semidefinite Programming and Arithmetic Circuit
Evaluation,” [arXiv:cs/0512035v1](https://arxiv.org/abs/cs/0512035v1),
Theorem 3 p. 5, SDFP definition pp. 7–8, and Theorem 4 pp. 8–9. The local
read primary text is [fulltext.md](../../literature/papers/tarasov2005-semidefinite-programming-and-arithmetic-circuit/fulltext.md).
The separate 2008 journal version, DOI
[10.1016/j.dam.2007.04.023](https://doi.org/10.1016/j.dam.2007.04.023), is
metadata-only/unread because its publisher text was not retrieved; the
comparison here is specifically the arXiv v1 statement.

## Arithmetic-complexity context

Allender, Bürgisser, Kjeldgaard-Pedersen, and Miltersen show that PosSLP is
in the counting hierarchy (Theorem 1.4) and that Square Root Sum reduces to
PosSLP (Section 1.4; Corollary 1.5 places SRS in the counting hierarchy as
well). This supports treating PosSLP as an established arithmetic
comparison benchmark. It gives only the reduction direction `SRS <= PosSLP`;
these sources do not establish that PosSLP is strictly harder than SRS or
vice versa. See “On the Complexity of Numerical Analysis,” [DOI
10.1137/070697926](https://doi.org/10.1137/070697926), Theorem 1.4 and
Section 1.4; the read primary text is
`literature/papers/allender2009-on-the-complexity-of-numerical/fulltext.md`.

## Scoped conclusion

The primary literature establishes both (i) PosSLP-hard constant-gap
approximation of a coordinate of a unique actual solution, and (ii) a
polynomial reduction of arithmetic-circuit sign comparison to exact convex
semidefinite feasibility. Those precedents prevent a broad novelty claim
about strong point approximation or about exact convex-feasibility
consequences of arithmetic circuits. They do not by themselves supply the
combination claimed by this candidate: a rational polynomial convex on a
box whose constant-accuracy optimizer point reveals the circuit sign.

The PosSLP reduction has a unique optimizer whose designated coordinate is
exactly one when the circuit output is positive and zero otherwise. A point
within `1/4` in either maximum or Euclidean norm reveals the answer. The
quartic can be scaled to bounded coefficient magnitudes, then affinely
mapped to a unit box; no treewidth bound is claimed. Its Hessian is positive
definite at the optimizer, but the curvature in the designated coordinate
depends on a positive sign-test amplitude with no polynomial lower bound.
Thus the construction does not supply a uniform growth modulus that turns
value accuracy into point accuracy. The proof review and targeted diagnostics
are recorded in the [review report](../reviews/posslp-convex-point-review.md).

This remains a conditional implication about point output; it is not an
NP-hardness result or a separation of complexity classes. Objective-value
approximation and an unevaluated implicit optimizer description are
different outputs; for a broader weak-value versus point-output comparison,
see [`convex-point-radical-prior.md`](convex-point-radical-prior.md). The
candidate also gives a one-dimensional core-only
noise extension: each noise draw leaves the PosSLP-encoding residual and
decision coordinate unchanged, so an always-correct expected-polynomial
full-point algorithm would yield a Las Vegas expected-polynomial PosSLP
algorithm. This does not imply deterministic polynomial time.
