# Novelty audit: additive optimization of quadratic cactus MPD

Date: 2026-09-05. This is an independent source audit of [the approximation investigation](potential-flow-cactus-approximation-investigation.md), separate from its mathematical review and the earlier [exact-arithmetic audit](potential-flow-cactus-arithmetic-novelty.md).

**Assessment:** no open source located in this search proves polynomial-bit-time additive optimization of maximum potential difference over arbitrary balanced interval nominations on quadratic passive cacti. The candidate appears to extend the known single-cycle theory in a substantial way. Its most distinctive ingredient is the polynomial family of nomination faces: after aggregation to the terminal block path, one optimizer has all nonsaturated loads in a single block, with at most two on a cycle. The inverse-Laplacian sensitivity identity and fixed-dimensional algebraic optimization are established tools and require explicit attribution. This assessment is conditional on the separate proof review and remains a bounded-search novelty assessment.

## Exact scope to preserve

The candidate considers positive rational resistances and the law

\[
\pi_u-\pi_v=\beta_e x_e|x_e|.
\]

Each signed nomination lies in a finite rational interval, and all nominations balance. The objective is the potential difference between two arbitrary specified nodes. Flow directions are unrestricted. The MPD subproblem has no additional arc capacities, potential bounds, compressors, valves, or integer design variables. The claim is a rational feasible nomination within additive \(\varepsilon\) of the optimum and a certified value interval, computed in time polynomial in the input encoding length and \(\log(1/\varepsilon)\). Feasibility of the returned nomination means its box and balance constraints are satisfied exactly; the corresponding physical flow and potential need not be rational.

This covers the entry/exit booking nomination boxes of the cited MPD literature and permits more general signed intervals. It does not decide equality-sensitive booking feasibility in polynomial time. When used for booking checks, the conclusion is a tolerance or promised-gap guarantee. It does not remove the exact radical-comparison issue established in [the SRS result](../results/potential-flow-cactus-square-root-sum.md).

## Closest structural and algorithmic predecessor

Labbé, Plein, Schmidt, and Thürauf, *Deciding feasibility of a booking in the European gas market on a cycle is in P for the case of passive networks*, Networks (2021), DOI 10.1002/net.22003, is the central comparison. The open manuscript is dated November 20, 2020. Sections 4–5 first select physical flow extremes and then restrict nominations through boundary-node configurations. Theorem 6.4 reduces a configuration to at most nine real variables and 42 polynomial constraints; Theorem 6.5 and Corollary 6.6 give a polynomial Turing-time decision algorithm. The concluding section explicitly proposes trees attached to a cycle and cacti as next graph classes. Remark 6.7 extends its structural reasoning to continuous strictly increasing odd laws, while its complexity guarantee requires polynomial laws of the stated form. [Open manuscript](https://optimization-online.org/wp-content/uploads/2019/11/7472.pdf), [published paper](https://doi.org/10.1002/net.22003).

The candidate should not claim the first finite structural reduction or first use of real algebraic geometry for nonlinear MPD. The apparent advance is a simpler global structure that persists across arbitrarily many cactus blocks, followed by controlled approximate evaluation of the fixed blocks. Searches in the full single-cycle manuscript found no inverse-Laplacian adjoint argument or single global multiplier leading to the candidate's two-pivot structure.

## Direct prior for the electrical derivative ingredient

Misra, Vuffray, and Chertkov, *Maximum Throughput Problem in Dissipative Flow Networks with Application to Natural Gas Systems*, arXiv:1504.02370 (2015), Section III-A, Lemma 1(a), equation (19), identifies the gradient of a conjugate energy with the physical potentials. Lemma 1(b), equation (21), identifies its Hessian with the inverse Hessian of the potential energy. The adjacent discussion identifies the latter as a grounded weighted graph Laplacian, with inverse-law derivative weights. Thus the candidate's potential Jacobian and electrical adjoint follow from an explicit known identity, after its smoothing step ensures positive finite conductances. That paper develops throughput formulations and a mixed-integer convex relaxation; it does not give the cactus nomination-face theorem or the proposed bit-complexity bound. [Primary preprint](https://arxiv.org/abs/1504.02370).

Credit this identity directly. Implicit differentiation, electrical maximum principles, and the first-order optimality condition for a box intersected with one balance equation should not be presented individually as discoveries. The new claim is their use with the cactus block path to force one common threshold and a polynomial number of low-dimensional candidate faces, including zero-flow limits.

## Related monotone robust-flow theory has different recourse

Vuffray, Misra, and Chertkov, *Monotonicity of Dissipative Flow Networks Renders Robust Maximum Profit Problem Tractable: General Analysis and Application to Natural Gas Flows*, arXiv:1504.00910 (2015), proves monotonicity and reduces uncertain consumption scenarios to extreme cases. Section II-B fixes source injections and terminal potentials as operational variables; terminal injections adjust with uncertain customer withdrawals. Theorem 1 gives its robust reduction, and Corollaries 4–5 establish monotonicity of potentials and terminal production. Its uncertainty therefore does not require optimizing a potential difference over a balanced box constraining every nomination, as here. No cactus face enumeration or matching bit-time MPD algorithm was found. [Primary preprint](https://arxiv.org/abs/1504.00910).

This is useful conceptual prior and prevents an overly broad claim that uncertainty monotonicity in nonlinear flow networks is new. It does not subsume the candidate's optimization theorem: fixed boundary potentials and adjustable boundary injections materially change the optimization problem.

## Explicit motivation in the hardness literature and current overview

Thürauf, *Deciding the feasibility of a booking in the European gas market is coNP-hard*, accepted April 11, 2022, DOI 10.1007/s10479-022-04732-1, proves general-network MPD NP-hardness in Lemma 4.20, including a restriction with predetermined flow directions. Its conclusion says that the reduction uses cycles sharing arcs and identifies cacti as a next classification target. It also explicitly proposes approximation algorithms for MPD as a way to check bookings up to a tolerance. Thus both the graph class and the practical approximation question are established research directions; the proposed algorithmic answer was not found there. [Open published paper](https://d-nb.info/1265956588/34), [author manuscript](https://optimization-online.org/wp-content/uploads/2020/05/7803-1.pdf).

Pfetsch, Schmidt, Skutella, and Thürauf, *Potential-Based Flows—An Overview*, January 2026 draft, printed pages 9–10, defines the relevant MPD model with bounded entry/exit nominations and an arbitrary objective-node pair. It contrasts trees and single cycles with general-network hardness and lists nonlinear cactus MPD complexity as open. [Open overview](https://optimization-online.org/wp-content/uploads/2026/01/ch_potential.pdf).

The defensible significance statement is that the candidate answers the **additive-approximation version** of this cactus problem in polynomial bit time. Claiming an unrestricted resolution of its exact decision complexity would be inaccurate. In particular, polynomial dependence on \(\log(1/\varepsilon)\) does not by itself produce an exact equality test.

## Later and adjacent papers checked

Klimm, Pfetsch, Skutella, and Strubberg, *Approximating the Network Design Problem for Potential-Based Flows*, arXiv:2604.26882, posted April 29, 2026, concerns network design, not interval-nomination MPD. Remark 8, printed page 12, explicitly distinguishes irrational arithmetic from bounded-precision approximation. Section 4.1 uses known series-parallel effective-resistance composition in a network-design dynamic program. No replacement for the candidate cactus nomination optimization was found. [Primary preprint](https://arxiv.org/abs/2604.26882).

Raber's 2022 dissertation studies recovery of cactus networks from effective-resistance data, a different question. Brandenberg and Stursberg's 2025 cactus extreme-point characterization concerns a linear differential-flow polyhedron. These papers were audited in more detail in [the earlier arithmetic novelty note](potential-flow-cactus-arithmetic-novelty.md); neither supplies the nonlinear nomination theorem.

## Recommended contribution statement

Subject to the independent proof checks, a precise claim is:

> For passive quadratic potential flows on a cactus, maximum potential difference over a balanced rational nomination box admits additive approximation and rational nomination recovery in time polynomial in the input length and requested precision bits. The structural reason is that one optimum lies in a polynomially enumerable family of nomination faces with at most two free aggregated loads, both in one cycle block.

The strongest part is the globally valid nomination structure, rather than approximate evaluation of a fixed cactus or algebraic optimization in constant dimension. Together with the separate exact SRS result, it gives a coherent distinction between efficiently obtaining numerical accuracy and deciding arbitrary exact thresholds.

## Search scope and uncertainty

Queries combined cactus, gas, booking, nomination, maximum potential difference, potential-difference maximizing, potential-based flows, dissipative flow, approximation, adjoint, gradient, sensitivity, monotonicity, and recent publication filters. Primary full texts were inspected for the single-cycle algorithm, general-network hardness, both 2015 dissipative-flow papers, the 2026 overview, and the April 2026 network-design paper. Some broad searches returned irrelevant physical-potential material; those results supply no evidence either way. No matching theorem was found, and no contact with authors was attempted. Unindexed or unpublished work and a theorem stated in different terminology remain possible.
