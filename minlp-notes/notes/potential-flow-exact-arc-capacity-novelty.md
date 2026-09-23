# Novelty audit: exact arc-flow extrema and robust capacity validation

Date: 2026-09-05. Scope: a bounded primary-literature audit of [the exact arc-capacity result](../results/potential-flow-exact-arc-capacity.md), separate from its two proof reviews and the [joint-resistance audit](potential-flow-joint-resistance-novelty.md).

The proposed **polynomial bit-complexity guarantee at fixed maximum biconnected-block cycle rank** remains a plausible new contribution. No matching guarantee was found in the inspected sources. The underlying minimum/maximum arc-flow formulation, the resulting robust capacity criterion, and the exact bridge case are established. Exact polynomial decision results also exist for narrower cyclic models. The contribution should therefore be positioned as a structural algorithm for an established verification problem, with joint nomination/resistance uncertainty and exact algebraic extrema as material features.

## Closest primary comparisons

### The minimum/maximum arc-flow verification criterion is already explicit

Thürauf, Grübel, and Schmidt, [*Adjustable robust nonlinear network design without controllable elements under load scenario uncertainties*](https://link.springer.com/article/10.1007/s10107-025-02207-2), Mathematical Programming (2025), Problems (6)–(7) and Theorem 1, explicitly minimize and maximize every arc flow over the load uncertainty set. These problems omit **both** potential and flow bounds. Their optimum values verify the respective flow capacities; potential-difference problems separately verify potential bounds. See also the [local full text](../literature/papers/thurauf2025-adjustable-robust-nonlinear-network-design/fulltext.md), printed pp.8–9.

This is the same capacity-verification logic used in the candidate. The paper reduces verification to polynomially many nonlinear problems; that does not assert polynomial running time for solving each problem. Its design decisions determine fixed arc parameters in the verification problems. Section 6.3 omits the arc-flow adversarial problems in the reported gas experiments because the large flow bounds there are redundant. The proposed oracle does not make the paper's mixed-integer network-design problem polynomial-time solvable.

### Joint uncertainty and exact bridge bounds are established

Aßmann's [2019 thesis, *Exact Methods for Two-Stage Robust Optimization with Applications in Gas Networks*](https://d-nb.info/1196351791/34), equations (3.3)–(3.4), already permits balanced shifted demand boxes and independent positive resistance boxes. Section 5.2.3, printed pp.115–118, develops arc-flow bounds for preprocessing. Equation (5.46), printed p.116/PDF p.134, obtains exact extrema for arcs outside cycles from demand linear programs, independently of resistance uncertainty. Equation (5.48), printed p.117/PDF p.135, instead minimizes/maximizes flows over an LP relaxation for cyclic arcs; these are bounds, not guaranteed exact physical extrema. The inspected section contains no fixed-block-rank exact polynomial-time theorem.

Chapter 5 repeats and extends Aßmann–Liers–Stingl's 2019 Networks paper. The thesis was inspected directly; the complete final Networks article was not retrieved, as explained in the separate joint audit. Do not present the bridge formula or simultaneous uncertainty as new.

### Exact cycle decision under booking uncertainty predates this result

Labbé, Plein, Schmidt, and Thürauf, [*Deciding Feasibility of a Booking in the European Gas Market on a Cycle is in P for the Case of Passive Networks*](https://optimization-online.org/wp-content/uploads/2019/11/7472.pdf), inspected November 2020 preprint of the 2021 Networks article, gives an exact polynomial decision result in Corollary 6.6, PDF p.27. Theorem 6.4 bounds the reduced algebraic system's variable and constraint counts, and Theorem 6.5 treats strict inequalities and rational input complexity.

Its uncertainty model is the booking set in Definition 2.3: fixed entry/exit types, nonnegative nomination magnitudes between zero and a booking vector, and balance. Pressure-loss coefficients are fixed. Definition 2.4 imposes potential bounds, without separate arc-flow capacities. Thus this is an exact cyclic predecessor, not merely an additive approximation result. It does not state the candidate's joint-uncertainty guarantee for arbitrary shifted boxes and networks with an unbounded number of bounded-rank blocks.

### A fixed-nomination resistance-uncertain cycle already has an exact flow-threshold test

Aßmann, Liers, Stingl, and Vera, [*Deciding Robust Feasibility and Infeasibility Using a Set Containment Approach*](https://arxiv.org/pdf/1808.10241), arXiv:1808.10241, Proposition 4.7 already bounds circulation sign cells by `O(m^k)` at fixed global cycle rank `k`. More directly relevant, Proposition 4.9 and Lemma 4.10, PDF pp.20–21, express single-cycle flows for fixed nominations as `q_a=t-d_a`, with fixed offsets `d_a`, and characterize an interval for `t` through a monotone scalar equation. The authors explicitly observe that its endpoint conditions are linear in the uncertain resistance vector.

The following exact capacity consequence is our inference from that lemma, rather than a separately labeled theorem in the source. With positive resistance vector `beta`, write

```
h(beta,t) = -sum_a beta_a (t-d_a)|t-d_a|.
```

Its unique zero is the physical circulation. For rational upper arc capacity `u_a`, put `c=u_a+d_a`. Then

```
q_a(beta) <= u_a for every beta in U
    iff max_{beta in U} h(beta,c) <= 0.
```

The lower-capacity test uses `min h(beta,c)>=0`. For rational polyhedral `U`, both are rational LP tests. Thus exact uncertain-resistance flow-capacity testing on a fixed-nomination single cycle should not be claimed as new.

## Which capacity problem is being solved?

The candidate tests **prescribed arc-flow capacities over a prescribed uncertainty set**. It neither chooses the uncertainty set nor maximizes node bookings. This distinction matters when comparing [*Computing technical capacities in the European entry-exit gas market is NP-hard*](https://link.springer.com/article/10.1007/s10479-020-03725-2): its technical-capacity decision is about admissible booking domains. Section 4 studies a potential network model without arc-flow bounds, with potential bounds governing feasibility. That hardness statement neither contradicts nor is resolved by the present edge-capacity oracle.

The candidate also excludes potential bounds and controllable elements. Its extrema are taken over all original physical scenarios, not over scenarios conditioned on satisfying other operating limits. With variable target-edge resistance, maximizing endpoint potential difference and maximizing target-edge flow need not select the same resistance scenario; the proof correctly uses their monotone relationship only while resistance is fixed.

## Exact versus additive guarantees

The exact arc result is stronger than the repository's additive joint maximum-potential-difference guarantee in its own objective, but it solves a different extremum problem. Every target edge lies in one block. After aggregating nominations outside that block, its exact flow extremum comes from one fixed-dimensional algebraic optimization. A potential difference across many blocks can add independently generated algebraic quantities; that arithmetic issue remains outside this result.

Do not describe previous cyclic work collectively as approximate: the Labbé et al. booking theorem is exact, and the single-cycle threshold consequence above is exact. Conversely, a polynomial number of nonlinear worst-case problems, a convergent relaxation hierarchy, or a numerical global solution is not by itself a polynomial bit-time exact oracle.

The parameter guarantee is polynomial time **for each fixed rank bound**; the exponent may depend on the bound. It is not a fixed-parameter or strongly polynomial claim. Exact extrema may be irrational and are returned in a real-algebraic encoding, rather than as rational physical flows.

## Recommended contribution statement

> We compute exact signed arc-flow extrema and decide all prescribed rational arc-flow capacities under balanced interval nomination uncertainty and independent positive interval resistance uncertainty in passive quadratic networks. For every fixed upper bound on the cycle rank of a biconnected block, the algorithm runs in polynomial bit time and returns extremum values with polynomial-size real-algebraic encodings, while the number of blocks and total cycle rank may grow. The worst-case capacity criterion and narrower tree/cycle cases are established; the proposed contribution is the structural complexity guarantee for this joint uncertainty model. We found no equivalent theorem in the open primary literature inspected.

## Search scope and remaining uncertainty

Targeted searches combined `arc flow`, `flow bounds`, `capacity validation`, `worst-case`, `robust feasibility`, `uncertain resistance`, `cycle rank`, `biconnected`, and `potential-based`. The comparison used primary full text for the papers and Aßmann thesis above. Thürauf's [2022 thesis metadata](https://open.fau.de/items/990bac3b-d89a-46d2-b613-5d4287a06579) was found, but its full text was inaccessible through the institutional page; no access-control bypass was attempted. Its constituent cycle paper was inspected directly. PDF page numbers above count the linked PDF from one.

This is not an exhaustive forward-citation review. Before a publication-level novelty claim, inspect the final Networks 2019 article if an open copy becomes available, the full Thürauf thesis, and later work citing the cycle and robust-design papers. Mathematical proof approval is separate from absence of a matching result in this bounded search.
