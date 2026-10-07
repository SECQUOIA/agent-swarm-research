# Adaptive OBBT source ledger

Audit date: 2026-10-03. Primary manuscripts, publisher full text, and pinned
software source support the claims below. Locations refer to printed pages
where available. Short quotations identify the relevant passage; they are
not substitutes for the assumptions in the source. The earlier repository
review was read for context, but its full-text reading claims are not
repeated as new reading in this pass.

## Tightening and computational tradeoffs

### GBMW2017 — filtering, ordering, and reusable dual bounds

- Source: Gleixner, Berthold, Müller, Weltge, *Three Enhancements for
  Optimization-Based Bound Tightening*, JOGO 67, 731–757 (2017),
  DOI [10.1007/s10898-016-0450-4](https://doi.org/10.1007/s10898-016-0450-4).
  [Read manuscript](https://optimization-online.org/wp-content/uploads/2016/03/5356.pdf).
- Read: §§1.3, 2–3; computational discussion. Supporting passage, manuscript
  p.1: “filtering strategies to reduce the number of solved LPs”.
- Supports: feasible relaxation points screen directions; dual LP solutions
  yield Lagrangian variable bounds; ordering exploits warm starts.
- Boundary: ordinary screening is relative to the current relaxation. It
  does not certify the tail of an arbitrary sequence of rebuilt relaxations.
  Remark 5, p.10, also identifies a cost of filtering: a zero-tightening call
  can still produce a nontrivial Lagrangian variable bound.

### Cengil2025 — dynamic learned variable selection

- Source: Cengil, Nagarajan, Bent, S. Eksioglu, B. Eksioglu, *Learning to
  accelerate tightening of convex relaxations of the AC optimal power flow
  problem*, COAP 92, 761–786 (2025), published August 13.
  [Publisher full text](https://link.springer.com/article/10.1007/s10589-025-00715-7).
- Read: §§4.1–4.2, 5.1, 5.6–5.9. Supporting passage, introduction:
  “adaptively updates which variables to tighten at each OBBT iteration”.
- Supports: dynamic subsets and learned ranking are prior work.
- Boundary: experiments tighten phase-angle differences, use 60 threads, and
  test held-out load profiles. Training/ranking cost is discussed separately
  in §5.7. Reported speedups concern OBBT relaxation strengthening; they are
  not generic MINLP branch-and-bound speedups or certified remaining-benefit
  bounds.

### GCGGR2025 — learned configuration selection in polynomial optimization

- Source: Gómez-Casares, González-Rodríguez, González-Díaz,
  Rodríguez-Fernández, *Impact of domain reduction techniques in polynomial
  optimization: A computational study*.
  [Version 2, September 1, 2025](https://arxiv.org/html/2403.02823v2).
- Read: §§3–4 and computational tables. Supporting passage, §1:
  “the impact of some of the Lagrangian-based enhancements”.
- Supports: RAPOSa comparisons include conic OBBT, dual-information FBBT, and
  learned instance-level configuration selection.
- Boundary: selection is not an online per-node budget policy. The present
  learning tables use out-of-bag evaluation; do not describe all of them as
  a distinct held-out test set. Table 8 distinguishes pace and gap gains;
  adjacent prose appears to mix those metrics, so use the table values.

### BGMS2024 — bound quality versus cost in ReLU models

- Source: Badilla, Goycoolea, Muñoz, Serra, *Computational Tradeoffs of
  Optimization-Based Bound Tightening in ReLU Networks*.
  [Version 2, January 30, 2024](https://arxiv.org/html/2312.16699v2).
- Read: §§2.2–5. Supporting passage, §1: “the tradeoffs between the time
  spent computing tight activation bounds and the time gained”.
- Supports: LP, MILP, and simple propagated bounds have different costs and
  downstream effects.
- Boundary: §3 explicitly separates OBBT cost from verification time because
  bounds may be reused. A single-solve comparison must add that cost itself.

### PM2025 — selective integrality and total cost

- Source: Pineda and Morales, *The Sweet Spot of Bound Tightening for Topology
  Optimization*. [Version 1, July 22, 2025](https://arxiv.org/html/2507.16496v1).
- Read: §§III–V. Supporting passage, §IV: “the total time”.
- Supports: topology selects retained binary decisions in bounding problems;
  experiments report tightening, final solve, and their sum separately.
- Boundary: the IEEE 118-bus transmission-switching study is evidence for a
  particular problem family. Its best tested partial relaxation is not a
  universal prescription for general MINLP.

### GGG2025 — tighter representations can change solver behavior

- Source: González-Díaz, González-Rodríguez, Gómez-Casares, *Bound tightening
  in lifted formulations: (sub)solver-dependent impact on performance in
  RLT-based algorithms*.
  [Version 1, September 23, 2025](https://arxiv.org/html/2509.18731v1).
- Read: §§4–6. Supporting passage, §6: “while theoretically redundant, can
  substantially affect solver performance”.
- Supports: explicit lifted bounds have mixed computational effects across
  auxiliary solvers and test sets; §5 investigates branching and LP costs.
- Boundary: this is computational evidence, not a theorem that tightening
  always helps or always hurts. It reinforces the need for complete-solve
  measurements rather than node counts alone.

## Mathematical foundations

### Tarski1955 — order and fixed points

- Source: Tarski, *A Lattice-Theoretical Fixpoint Theorem and Its
  Applications*, Pacific J. Math. 5, 285–309 (1955).
  [Original article](https://people.csail.mit.edu/carroll/probSem/Documents/Tarski.pdf).
- Read: §1, especially Theorem 1 and its proof.
- Supports: extremal fixed-point principles for increasing self-maps of
  complete lattices.
- Boundary: persistence of a known fixed box beneath a monotone iteration is
  an elementary induction. Neither its abstraction nor the underlying
  fixed-point principle should be claimed as a new OBBT theorem.

### BCLL2012 — bound tightening already has fixed-point theory

- Source: Belotti, Cafieri, Lee, Liberti, *On feasibility based bounds
  tightening*.
  [2012 manuscript](https://optimization-online.org/wp-content/uploads/2012/01/3325.pdf).
- Read: §§2.5, 3–4; Theorems 3.1, 3.3, 4.1.
  Supporting passage, p.12: “the greatest fixed point of the fbbt operator”.
- Supports: FBBT lattice semantics, potentially infinite iteration, and an LP
  characterization for the linear case.
- Boundary: these are FBBT results. The correspondence to a rebuilt OBBT
  operator needs its own assumptions and proof.

### JK2016 — classical matrix contraction

- Source: Jachymski and Klima, *Around Perov's Fixed Point Theorem for
  Mappings on Generalized Metric Spaces*, Fixed Point Theory 17, 367–380
  (2016).
  [Journal PDF](https://www.math.ubbcluj.ro/~nodeacj/download.php?f=162-ja-kl-1396-final.pdf).
- Read: §§2–4, Theorems 3.2–3.4 and their proofs. Supporting passage, p.367:
  “this result is subsumed by the classical Banach contraction principle”.
- Supports: nonnegative-matrix Lipschitz majorants with spectral radius below
  one, including reduction to a scalar contraction metric.
- Boundary: residual-tail bounds obtained by summing matrix powers are
  elementary consequences. The audit did not obtain Perov's 1964 original;
  this paper gives a directly inspected proof of the foundation used here.

### BBM2003 — fixed-matrix multiparametric LP

- Source: Borrelli, Bemporad, Morari, *Geometric Algorithm for Multiparametric
  Linear Programming*, JOTA 118, 515–540 (2003).
  [Author-hosted journal PDF](https://cse.lab.imtlucca.it/~bemporad/publications/papers/jota-mplp.pdf).
- Read: §§2–3, Theorem 2.4, critical-region construction, degeneracy
  discussion. Supporting passage, p.520: “convex and piecewise affine”.
- Supports: affine-right-hand-side parameterization, basis/active-set regions,
  and piecewise-affine values.
- Boundary: changing a McCormick box usually changes the constraint matrix.
  Fixed-matrix sensitivity does not directly cover that dependence. A local
  basis certificate also does not cover unexamined active-set switches.

### WN2011 — acceleration is a candidate-generation technique

- Source: Walker and Ni, *Anderson Acceleration for Fixed-Point Iterations*,
  SIAM J. Numer. Anal. 49, 1715–1735 (2011),
  DOI [10.1137/10078356X](https://doi.org/10.1137/10078356X).
  [Author-hosted article](https://users.wpi.edu/~walker/Papers/Walker-Ni,SINUM,V49,1715-1735.pdf).
- Read: Algorithm AA, §2, practical discussion. Supporting passage, p.1717:
  “a useful general tool for accelerating fixed-point iterations”.
- Supports: established residual-based mixing and its linear-case connection
  to GMRES.
- Boundary, inferred from Algorithm AA: coefficients sum to one but need not
  be nonnegative. Therefore the algorithm alone gives no enclosure-preserving
  OBBT reduction. Independent verification is needed before accepting any
  proposed claim about the accelerated box.

## Computation selection

### HMW2018 — adaptive solver components

- Source: Hendel, Miltenberger, Witzig, *Adaptive Algorithmic Behavior for
  Solving Mixed Integer Programs Using Bandit Algorithms* (2018).
  [Primary manuscript](https://optimization-online.org/wp-content/uploads/2018/07/6725.pdf).
- Read: §§2–3, computational discussion. Supporting passage, p.1:
  “concentrate its computational budget on those components that perform well”.
- Supports: online selection for LP pricing, large-neighborhood search, and
  diving, with component-specific rewards and costs.
- Boundary: empirical benefits of a particular scheduler do not establish
  that OBBT, cuts, and branching share a stationary reward process.

### CGLP2023 — scheduling different heuristic classes together

- Source: Chmiela, Gleixner, Lichocki, Pokutta, *Online Learning for Scheduling
  MIP Heuristics* (2023).
  [Version 1](https://arxiv.org/pdf/2304.03755).
- Read: §§1, 3–4; Algorithm 1. Supporting passage, p.2:
  “two different classes of heuristics are treated simultaneously”.
- Supports: one online learner can schedule diving and large-neighborhood
  search using observed rewards; numerical evaluation is part of the claim.
- Boundary: this is not a regret or universal runtime guarantee for arbitrary
  solver-strengthening actions. The paper is a computational scheduling
  baseline, not a certificate of OBBT's remaining benefit.

### HRTS2012 — value of computation and stopping

- Source: Hay, Russell, Tolpin, Shimony, *Selecting Computations: Theory and
  Applications*, UAI 2012, 346–355.
  [Version 1](https://arxiv.org/pdf/1207.5879).
- Read: §§1–3, Definitions 1–3, Theorems 4–10.
  Supporting passage, p.2: “when to stop deliberating and execute a real action”.
- Supports: a specified metalevel probability model, explicit computation
  cost and stopping, and distinctions from ordinary bandit rewards.
- Boundary: bounds proved for that model require its assumptions. OBBT
  changes subsequent solver states and cannot inherit those guarantees merely
  by calling its policy a bandit or a value-of-computation rule.

## Software

### SCIP — pinned current implementation

- Commit: `a01de2cfde013503da3f948ba8cdd492227d9a20`, October 2, 2026.
  [prop_obbt.c](https://github.com/scipopt/scip/blob/a01de2cfde013503da3f948ba8cdd492227d9a20/src/scip/prop_obbt.c).
- Read: defaults, lines 80–128; LVB construction, 523–640; filtering,
  959–1073 and 1292–1445; gating/budget, 3179–3204.
- Supports: compiled defaults enable trivial filtering and generalized bounds;
  aggregate filtering is optional. The work budget depends on root LP effort.
  A source TODO near line 33 concerns gating expensive root reruns on new
  incumbents or cuts.
- Crucial separate behavior:
  [prop_genvbounds.c, lines 1991–2003](https://github.com/scipopt/scip/blob/a01de2cfde013503da3f948ba8cdd492227d9a20/src/scip/prop_genvbounds.c#L1991)
  already detects improved cutoffs and propagates cached generalized bounds.
- Boundary: compiled defaults are not every user's effective configuration.
  A TODO is an implementation observation, not evidence of research novelty.

### Coramin — pinned filtering implementation

- Commit: `6e74d30f54edc0a322e4bbd0d7cb5393e6ba0e03`, October 27, 2023,
  current `main_branch` at audit time.
  [filters.py](https://github.com/Coramin/Coramin/blob/6e74d30f54edc0a322e4bbd0d7cb5393e6ba0e03/coramin/domain_reduction/filters.py).
- Read: `filter_variables_from_solution`, lines 15–64; `aggressive_filter`,
  lines 67–193.
- Supports: feasible-point filtering, aggregate-objective filtering, and
  stopping based on work or newly filtered variables. Source attribution
  points to Gleixner et al.
- Boundary: these rules concern the current relaxation; they do not certify
  future rebuilt rounds or total solving time.

## Historical sources carried forward and access limits

The September review directly read Caprara–Locatelli (2010),
[DOI 10.1007/s10107-008-0263-4](https://doi.org/10.1007/s10107-008-0263-4),
and Caprara–Locatelli–Monaci (2016),
[DOI 10.1007/s10589-015-9818-5](https://doi.org/10.1007/s10589-015-9818-5).
Their iterated-OBBT limit characterizations and stalling examples remain
required historical context. They were not newly read in full in this pass.

The 1964 Perov original was not obtained. Attempts to open a Banach original
scan and an author-hosted Kelley book failed; no claim depends on having read
those texts. The accessible JK2016 proof supplies the matrix-contraction
foundation. No result is claimed absent from all inaccessible literature.

Search families included selective/adaptive/learned OBBT; filtering and
Lagrangian bounds; OBBT remaining-benefit certificates; fixed-point
acceleration; multiparametric LP and active-set sensitivity; metareasoning;
and MIP heuristic scheduling. Queries included 2025 and 2026 work. Later
publication labels returned by search were not used to infer pre-audit
availability without a dated primary version.
