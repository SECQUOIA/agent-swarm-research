# Root-graph MILP–MISOCP separation: bounded source assessment

Date: 2026-09-05. Candidate:
[small-exponent SOC formulation separation](small-exponent-soc-formulation-separation.md).
This is a source assessment; two independent full mathematical audits were
requested separately.

No exact prior statement of the candidate's fixed-error root-graph
separation was located. Its useful claim is specific: four binary variables
and polynomial rational MISOCP encoding suffice for a vertical outer
approximation of `x^(1/2^B)` on `[0,1]`, whereas every rational MILP satisfying
the same graph-coverage and accuracy requirements needs `Omega(2^B)` total
encoding. Neither short conic descriptions of numerically complicated
solutions nor repeated-squaring lifts are new. The homogeneous optimal-value
construction should be presented as an application of classical conic
duality, not as a new duality principle.

## Strongest relevant antecedents

**Large bit requirements in small conic systems.** Ryan O'Donnell, *SOS Is
Not Obviously Automatizable, Even Approximately* (ITCS 2017), DOI
10.4230/LIPIcs.ITCS.2017.59, explicitly recalls the classical existence of
small SDPs whose feasible solutions require exponential bit complexity,
attributing the phenomenon to Ramana/Khachiyan. Section 2 uses repeated
squaring in an example requiring large SOS certificate coefficients even at
fixed approximation error. Theorem 1 states that conclusion. These portions
were read in the author manuscript, PDF pages 3–6; its draft pagination and
conference placeholder differ from the published record.
[Primary manuscript](https://www.cs.cmu.edu/~odonnell/papers/sos-automatizability.pdf),
[published record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2017.59).

Our comparison: this is a clear predecessor to the numerical-encoding
phenomenon behind the candidate. It is not a theorem about all rational MILP
outer approximations of a root graph. Still, the broad slogan “small conic
systems can encode exponentially long numbers” cannot be claimed as new.
The original Ramana and Khachiyan texts cited there were not read in this
bounded pass; attribution to them is through the explicit discussion in
O'Donnell's paper.

**Compact power lifts.** Jie Wang, *Weighted Geometric Mean, Minimum Mediated
Set, and Optimal Simple Second-Order Cone Representation* (2024), DOI
10.1137/22M1531257, gives optimal simple SOC representations for bivariate
weighted geometric means. Algorithm 4.1, Remark 4.3, and Corollary 4.5,
printed p.1498 (PDF p.9), relate their size to the logarithm of the integer
exponent denominator. The restriction to a “simple” SOC representation is
part of that result. These statements and their surrounding proof were
checked, extending the abstract-only check in the earlier MILP note.
[Author-hosted paper](https://wangjie212.github.io/jiewang/research/wgm.pdf).

Qing Ye and Weijun Xie, *Second-Order Conic and Polyhedral Approximations of
the Exponential Cone: Application to Mixed-Integer Exponential Conic
Programs*, arXiv:2106.09123, Proposition 1, printed p.13 (PDF p.13), gives a
tower of SOC constraints for the epigraph of
`(1+2^(-N)x)^(2^N)` and credits earlier conic approximation work for the
tower representation. Its approximation target is an exponential-cone
model, not the candidate's full root graph.
[Primary preprint](https://arxiv.org/pdf/2106.09123).

Our comparison: repeated squaring and logarithmic-size power-inequality
representations are directly established ingredients. An epigraph or
hypograph lift alone does not supply the narrow full graph tube. The
candidate additionally encodes selected fixed optimal values as linear
coefficients through primal-dual feasibility and equality of values.

**Small polyhedral approximations of SOC constraints.** Aharon Ben-Tal and
Arkadi Nemirovski, *On Polyhedral Approximations of the Second-Order Cone*
(2001), DOI 10.1287/moor.26.2.193.10561, establishes lifted LP approximations
whose numbers of variables and constraints grow logarithmically with the
inverse cone tolerance. The publisher's detailed abstract specifies exact
coverage of the conic set and a multiplicative relaxation of each norm
inequality for the reverse containment. The abstract and opening statement
were checked; the full construction and coefficient rationalization were
not audited here.
[Primary publisher statement](https://pubsonline.informs.org/doi/10.1287/moor.26.2.193.10561).

Our comparison: this is the apparent contrary result that a presentation
should address. A bound on individual conic residuals does not, without an
additional conditioning argument, bound vertical error in the projected
root graph. The candidate imposes an exact primal-dual optimality equality
to encode extremely small slopes. Replacing its cones by approximate cones
does not automatically preserve those slopes with the accuracy required by
the root graph. Thus the quoted LP approximation guarantee does not
contradict the proposed total rational encoding lower bound. This audit
does not derive a quantitative tolerance threshold for that replacement.

## Optimal-value coefficient gadget

The proposed equations homogenize a fixed primal-dual optimality system.
For positive homogenizing weight, division recovers primal and dual
feasibility; equality of objective values then determines the fixed optimal
value. At weight zero, feasibility of the original primal and dual excludes
a nonzero common recession value. This is standard weak/strong duality
reasoning combined with homogenization.

Searches for conic representations of optimal-value graphs and homogenized
optimality systems did not locate this exact coefficient-gadget statement.
That absence does not justify a novelty claim for the gadget: the deduction
is immediate from established tools. Its role here is an explicit reusable
construction avoiding the expansion of a long rational coefficient.

## Recommended positioning and limits

Call this an elementary **total-encoding separation for fixed-accuracy graph
formulations**, assembled from classical ingredients. The quantifiers are
valuable: the lower bound allows arbitrary integer dimension and unbounded
integer auxiliaries, while the conic construction uses four binaries. The
result separates encoding size, not binary-variable count or exact solving
time.

The conic formulation has polynomial size under explicit sparse rational
encoding; any `O(B)` claim should retain its structured cone-list convention
and acknowledge index overhead under ordinary matrix encoding. The conic
feasible set may involve values with exponentially long explicit rational
representations. A short formulation is not a polynomial-time exact-output
algorithm. No real-coefficient MILP lower bound is asserted.

Recommended wording: “Combining classical conic optimality systems and
repeated-squaring lifts with a rational-LP denominator bound gives an
exponential total-encoding separation between rational MILP and rational
MISOCP outer approximations of reciprocal-power graphs at fixed vertical
accuracy. No matching graph-formulation statement was located in the
primary sources checked.” This wording remains conditional on the full
mathematical audits.

The bounded search covered MILP–MISOCP exponential formulation gaps,
optimal-value graphs and homogenization, rational power lifts, SOC-to-LP
approximation, and exponential solution/certificate bit complexity. It did
not establish exhaustive priority. The earlier
[MILP denominator assessment](small-exponent-rational-formulation-barrier-novelty.md)
contains the primary LP source and qualitative MILP-representability
comparison; those established ingredients retain their prior attribution.
