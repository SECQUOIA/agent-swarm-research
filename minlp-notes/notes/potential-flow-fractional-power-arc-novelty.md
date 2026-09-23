# Source audit: fractional-power exact arc-capacity comparison

Date: 2026-09-05. Status: bounded primary-literature audit, not a proof audit.

The candidate in [the fractional-power arc-barrier note](potential-flow-fractional-power-arc-barrier.md) reduces Square-Root-Sum to one exact arc-flow threshold on a passive simple cycle with fixed rational nominations and resistances, using the common law `phi(x)=sign(x)|x|^(3/2)`.

No inspected primary source states this precise reduction or this exact restricted hardness result. The general arithmetic difficulty of potential-based flows, including fractional powers of rational data, is already explicit in the literature. The defensible contribution is therefore the concrete single-cycle threshold obstruction and its contrast with the repository's polynomial-law exact theorem. This bounded search does not establish first priority or standalone publishability.

## The closest flow sources

### General homogeneous potential laws and the computational model

[Groß, Pfetsch, Schewe, Schmidt, and Skutella, *Algorithmic Results for Potential-Based Flows: Easy and Hard Cases*](https://optimization-online.org/wp-content/uploads/2017/08/6185.pdf), inspected preprint dated May 31, 2018, Section 2.1, PDF pp.2–3, already defines a common continuous, strictly increasing, odd law and its homogeneous specialization `alpha sign(x)|x|^r` for any `r>0`. PDF p.3 discusses efficient function evaluation, the Turing model, possible other real-arithmetic models, and root approximation. PDF p.5 gives the water-network exponent 1.852.

Theorem 3.2 and the energy formulation on PDF pp.6–7 establish the familiar uniqueness and strictly convex optimization mechanism. Theorem 3.7, PDF p.9, treats homogeneous single-source/single-sink scaling from a reference physical flow. It is not an explicit exact binary algorithm for the candidate's growing collection of nonzero node nominations. These results neither supply the proposed SRS reduction nor justify extending a polynomial-law exact comparison theorem to arbitrary fractional powers. The general model and uniqueness argument should not be presented as new.

### An explicit recent warning about irrational input transformations

Klimm, Pfetsch, Skutella, and Strubberg, *Approximating the Network Design Problem for Potential-Based Flows* (2026), Remark 8, notes that transformed path lengths `c_a^(r/(r+1))` can be irrational even for integral costs. To justify its exact shortest-path special case, the paper assumes those transformed lengths themselves are supplied as rational numbers. It treats later approximation algorithms using bounded precision. [[klimm2026-approximating-the-network-design-problem]] p.11-12

This is close motivation for the candidate's arithmetic distinction. It studies conductance design and path costs, rather than fixed-scenario arc-capacity comparison. The inspected remark does not prove SRS-hardness. Accordingly, avoid claiming that the present candidate is the first recognition that fractional powers can obstruct an exact bit-complexity argument.

### Convex-cost flow algorithms do not remove the issue

[Végh, *A Strongly Polynomial Algorithm for a Class of Minimum-Cost Flow Problems with Separable Convex Objectives*](https://arxiv.org/pdf/1110.4882), inspected arXiv text, PDF p.2, distinguishes exact rational output from irrational optima and discusses an earlier strong-polynomial impossibility result. The latter concerns a restricted arithmetic model and approximation, rather than the candidate's binary decision reduction.

Oracle 1, PDF p.8, requires either the cost derivative or its exponential to return rational values at rational arguments. Theorem 4.5, PDF p.15, additionally assumes exact trial and error subroutines. These hypotheses matter. For the candidate's energy cost `(2/5) beta |x|^(5/2)`, the derivative is `beta sign(x)|x|^(3/2)`, which need not be rational at rational arguments. Thus the theorem is not a blanket exact algorithm contradicting the candidate. The paper proves its oracle implementations for quadratic costs and the specified market applications; it does not provide the proposed fractional-power single-cycle hardness classification.

## What the source complexity problem establishes

[Eisenbrand, Haeberle, and Singer, *An Improved Bound on Sums of Square Roots via the Subspace Theorem*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol293-socg2024/LIPIcs.SoCG.2024.54/LIPIcs.SoCG.2024.54.pdf), SoCG 2024, PDF pp.1–2, studies exact sign decisions for integer combinations of square roots. It identifies polynomial-time decidability as open and improves separation dependence when radicands are fixed, with a constant depending on those radicands. That result does not give the uniform polynomial separation bound needed to settle arbitrary binary instances.

Consequently, SRS-hardness is a conditional arithmetic barrier: a polynomial-time exact solver for the stated flow predicate would decide the source problem in polynomial time. It is not an unconditional proof that no such flow algorithm exists, and it does not by itself establish NP-hardness. The candidate currently claims hardness only; this audit supplies no converse reduction or completeness result.

## Positioning against the polynomial-law theorem

The repository's [exact arc-capacity result](../results/potential-flow-exact-arc-capacity.md) depends on a polynomial representation after fixing the bounded circulation dimension. The new candidate is relevant because its graph still has only one circulation variable, but evaluating the cycle equation at a rational threshold aggregates independently varying radicals.

The law remains algebraic and smooth enough for the stated monotonicity argument. Calling it algebraic does not give a polynomial-size univariate polynomial representation of the entire aggregate automatically. Likewise, representing each radical with an auxiliary variable increases the real dimension with the number of arcs. These are explanations of why the existing proof does not transfer, not independent hardness arguments.

Suggested qualified wording after independent proof acceptance:

> Exact one-arc comparison for the fixed law `sign(x)|x|^(3/2)` is Square-Root-Sum-hard already on a simple cycle with fixed data. This gives a concrete arithmetic obstruction to extending the polynomial-law theorem to general algebraic power laws. We did not locate this restricted reduction in the inspected open literature.

Retain the separate scopes of exact comparison, additive approximation, and robust optimization. A singleton-scenario corollary transfers the reduction to a robust formulation that permits degenerate uncertainty boxes, but does not add an uncertain-load optimization mechanism. The example exponent 3/2 is inside the established mathematical power-law model; no source inspected here identifies it as the standard Hazen–Williams water law or the standard Weymouth gas law.

## Search scope and limitations

Queries combined potential-based flows, hydraulic and gas networks, nonlinear resistor networks, cyclic pipes, power laws, rational exponents, exact arithmetic, irrational solutions, Square-Root-Sum, SQRT-SUM, and sums of radicals. The inspected primary evidence covers the main general potential-flow framework, a recent network-design arithmetic caveat, separable convex-flow oracle assumptions, and recent radical separation work. Search hits on stochastic business-process “flows,” seismic root-sum-square formulas, and power-law degree distributions address different subjects and were excluded.

The search found no direct predecessor; it is not an exhaustive review of older hydraulic-network, nonlinear-circuit, or computational real-analysis literature. The elementary nature of the reduction warrants restrained novelty language even if independent verification accepts it.
