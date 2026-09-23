# Stage 4, round 1: independent review 1

**Findings: 0 major issues; 0 minor issues.** No repair is required by this
review. This is a framing, integration, figure, and reproducibility review;
it does not replace the planned fresh full-proof review.

I inspected the abstract, introduction, conclusion, reproducibility appendix,
overview script and figure, packaging script, README, Makefile, macros,
bibliography, final source ledger, and Stage 4 author audit. I did not read
peer reviews or modify manuscript sources or generated submission artifacts.

## Headline accuracy and exposition

The abstract and introduction agree with the reviewed mathematical results.
They state the fixed positive relative-error contract, the first-admissible
threshold index, equality at the cheaper tier, and the distinction between
the positive-width and singleton high bands. The even plateau and concrete
`5/6` versus `1/2` comparison are correctly restricted to a single
definite-parity transform. The odd logarithmic factor is retained. The
degree-six witness is explicitly only an upper bound for `F_3`.

The joint high-accuracy overview states positive `K` and fixed positive
`beta`. The intermediate-regime discussion retains the margin factor near
the upper tier boundary and only claims the quadratic multiplicative gap
away from that boundary. The conclusion preserves these unresolved questions
instead of implying a uniform optimal multiplicative law.

The introduction explicitly says that queries are paid when applying the
conversion circuit and paid again on reuse. It separates coherent conversion
from learning an instance and preparing a state. The LP overview specifies
the dual Newton state, counted RHS access for that task, matrix-only access
for the compiler, the zero-query coarse exception, the public primal
predictor, and the digital-value bypass. It does not advertise the example
as an end-to-end LP or QIPM lower bound.

The problem definition and roadmap make the paper independently readable
without the research notes. The source ledger accurately records the
corrections and strengthenings checked in the earlier reviews, including
the high-band endpoint, rounded index asymptotics, even plateau, odd
logarithm, uniform growing-order constants, and LP coarse exception.

## Literature and novelty scope

The introduction attributes synthesis, generic amplification, polynomial
query representations, classical approximation tools, factor benefits, and
amplitude estimation to prior work. Its priority claim is qualified and
specific to the stated shift problem and theorem combination.

I independently checked the recent comparison descriptions and metadata
against primary pages for [Dong–Larsen–Lin–Sarkar](https://arxiv.org/abs/2608.30937),
[Laneve](https://quantum-journal.org/papers/q-2026-03-13-2025/),
[Somma–de Wolf](https://arxiv.org/abs/2608.24493), and
[King et al.](https://journals.aps.org/prl/abstract/10.1103/m3fj-m4rm).
The summarized minimax/retraction, adversary/state-conversion, guided-state,
and sum-of-squares topics match those sources. The separate dimension and
guide-overlap hypotheses are not transferred to this paper's task.
[Sarkar–Yoder's abstract](https://arxiv.org/abs/2111.07182) supports the stated
exterior-constraint and endpoint-matching comparison. Orsucci–Dunjko and the
implementation references were checked in my earlier-stage reviews. These
checks support the scoped related-work statements; they are not a guarantee
of universal priority over all approximation literature.

## Figure and scripts

The overview is readable and accurately displays threshold membership using
filled and open markers. Its left panel plots the proved unrestricted
exponents; exponent zero is correctly qualified in the caption by the coarse
logarithmic cost when `c<1`. The right panel uses only the range
`1/32 <= K <= 1/12`, where the witness and plateau prove the displayed even
orders. The odd logarithmic factor is visible. No unknown value of `F_3` is
plotted as a transition.

The overview shares the stationary-equation solver with the reviewed
diagnostic script and checks the inequalities needed by the plot. Floating
point diagnostics are consistently distinguished from continuous-domain
proofs. The scripts require no external data or network.

## Independent package validation

I verified the archive CRC and all 18 entries against the frozen workspace
files byte for byte. The archive includes all required sources, the figure,
the generated bibliography, and the scripts; it excludes audits and local
literature.

I extracted it to `/tmp/stage4-review1-mk1y2khe` and used the qipm environment
to run `make`, `make figures`, and `make` again. All passed. The resulting
31-page PDF has no final LaTeX warnings, undefined references, or overfull or
underfull boxes. Its extracted text matches the frozen PDF exactly. There
are 100 distinct labels and no missing referenced label. The regenerated
overview CSV matches the frozen CSV exactly, and both figure scripts
reproduce their reported checks. README instructions and Makefile behavior
are consistent: the ordinary build needs TeX but not Python, while figure
regeneration and packaging use Python.
