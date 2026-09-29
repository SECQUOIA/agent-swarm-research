# Research output of AI agent swarms

This repository holds the research corpus described in the paper
[AI Agent Swarms as Researchers: Progress, Challenges, and Open
Questions](https://arxiv.org/abs/2609.35719) by Sergey Gusev and David E.
Bernal Neira. To cite this work, see [Citation](#citation). The paper's
research inventory (Appendix C) lists the potential papers and proposed
experimental programs in the corpus, with IDs such as M1 or Q12. The
[inventory below](#research-inventory) is the current version of that list and
links to the drafts.

## What this is

At tag `paper-v1` (commit `84c6be7`), the version the paper describes, the
folders contain only material written by AI agents during the runs described in
the paper: notes, checks, code, review records, Lean proofs, and paper drafts.
This snapshot holds the agents' output as of 25 September 2026. The authors
of the paper have not edited it and, except where the paper says otherwise,
have not verified its claims. It contains no scientific input from the authors;
their part in producing it was limited to the process and editorial
instructions described in the paper. The drafts are not final papers: the
authors intend to take them further.

The runs continue, and later versions of this repository may add topics and
results, some with the authors' scientific input.

## Folders

| Folder | Field |
|---|---|
| `minlp-notes` | Mixed-integer nonlinear programming |
| `qipm-notes` | Quantum interior-point methods |
| `thermo-notes` | Molecular thermodynamics |
| `transport-notes` | Transport theory |
| `aggregation-kinetics-notes` | Aggregation kinetics |
| `catalysis-notes` | Heterogeneous catalysis (proposed experimental programs) |

## Research inventory

The 56 potential papers and 8 proposed experimental programs in the corpus,
with the IDs and status values used in the paper. The paper also states the
claimed contribution of each. Items marked *Notes only* have no draft; their
results are in the notes of the folder for that area.

This inventory reflects the current state of the repository. The paper's
inventory (Appendix C) describes the repository at tag `paper-v1`, and its
links point to that commit. The two lists may differ as the runs add topics,
drafts, and Lean proofs. Items M23–M33 were added after `paper-v1` and are
not in the paper, and M18 has since gained a full paper and a new title. For
the inventory as the paper describes it, see the
paper or
[this README at `paper-v1`](https://github.com/SECQUOIA/agent-swarm-research/blob/paper-v1/README.md#research-inventory).

### Mixed-integer nonlinear programming

| ID | Working title | Write-up | Lean |
|---|---|---|---|
| M1 | Sharp gaps for positive multilinear relaxations | [Full paper](minlp-notes/paper-multilinear-gap/main.pdf) | Done |
| M2 | Verified bounds for positive cubic relaxation gaps | [Full paper](minlp-notes/paper-cubic-gap/main.pdf) | Done |
| M3 | Checkable lower bounds for convex mixed-integer nonlinear optimization through rational outer approximations | [Full paper](minlp-notes/paper-certified-minlp/main.pdf) | Done |
| M4 | Convex relaxation gaps and spatial certificates in nonlinear optimization | [Full paper](minlp-notes/paper-relaxation-limits/main.pdf) | Partial |
| M5 | Integer dimension in convex mixed-integer approximation of nonlinear graphs | [Full paper](minlp-notes/paper-integer-dimension/build/main.pdf) | Partial |
| M6 | Rounding switching controls under a hard switch budget: sharp minimax bounds and exact algorithms | [Full paper](minlp-notes/paper-switching-control/main.pdf) | Partial |
| M7 | Sparse convex hulls for network flows coupled to a simplex | [Full paper](minlp-notes/paper-network-simplex/main.pdf) | Partial |
| M8 | Topology, uncertainty, and precision in passive potential-flow optimization | [Full paper](minlp-notes/paper-potential-flow/complexity/main.pdf) | Partial |
| M9 | The complexity of pooling: algebraic barriers and structural algorithms | [Full paper](minlp-notes/papers/pooling/main.pdf) | Not applicable |
| M10 | Exact feasibility of resistive and AC power networks | [Full paper](minlp-notes/paper-power-flow/build/main.pdf) | Not applicable |
| M11 | Structured bilevel optimization with many follower variables: global responses, accuracy, and structural boundaries | [Full paper](minlp-notes/paper-structured-bilevel/paper.pdf) | Possible |
| M12 | Globally certified measurement selection with correlated errors | [Full paper](minlp-notes/paper-correlated-measurements/build/main.pdf) | Partial |
| M13 | Radial and point separation for perspective outer approximation of convex generalized disjunctive programs | [Full paper](minlp-notes/paper-lbesh/main.pdf) | Not applicable |
| M14 | Quadratic aggregation: certificates, finite descriptions, and approximation | [Full paper](minlp-notes/paper-quadratic-aggregation/paper.pdf) | Partial |
| M15 | Exact convex hulls for a reciprocal factor shared by many variables | Notes only | Done |
| M16 | Ill-posed heat-exchanger network instances in MINLPLib | Notes only | Not applicable |
| M17 | Convex envelopes of two-variable monomials with real exponents on a wedge | Notes only | Possible |
| M18 | Sparse indicator quadratics: exact complexity and smoothed separator messages | [Full paper](minlp-notes/paper-sparse-indicator-quadratics/paper.pdf) | Not applicable |
| M19 | Convex envelopes of univariate functions of a linear form | Notes only | Possible |
| M20 | Contraction theory of iterated optimality-based bound tightening | Notes only | Possible |
| M21 | Joint relaxation of several nonlinear terms in one variable | Notes only | Not applicable |
| M22 | Separable concave terms on few linear rows | Notes only | Possible |
| M23 | Encoding and calibration of exact norm penalties in mixed-integer convex optimization | [Full paper](minlp-notes/paper-exact-penalties/main.pdf) | Partial |
| M24 | Exact optimization of convex quadratic and second-order cone programs with a small Hessian span | Notes only | Not applicable |
| M25 | Exact arithmetic complexity of strongly convex quartic optimization | Notes only | Not applicable |
| M26 | Irrational minimizers and certificate coefficient fields for strongly convex quartics | Notes only | Partial |
| M27 | Convergence rates of sparse moment–sum-of-squares hierarchies with private convex recourse | Notes only | Possible |
| M28 | Phase transitions of perspective branch-and-bound in random sparse regression | Notes only | Not applicable |
| M29 | Instance-dependent node complexity of spatial branch-and-bound | Notes only | Possible |
| M30 | Relaxation-intrinsic lower bounds for integer branch-and-bound: class number, random closest-vector problems, and MIMO detection | Notes only | Possible |
| M31 | Competitive branching points for spatial branch-and-bound | Notes only | Partial |
| M32 | Separating split inequalities for integer quadratic programming is NP-complete | Notes only | Not applicable |
| M33 | A priori integrality-gap bounds for shortest paths in graphs of convex sets | Notes only | Possible |

### Quantum interior-point methods

| ID | Working title | Write-up | Lean |
|---|---|---|---|
| Q1 | Objective sublevels and central-path Hessian conditioning | [Full paper](qipm-notes/conditioning-paper/main.pdf) | Partial |
| Q2 | The cost of following the central path | [Full paper](qipm-notes/central-path-cost/main.pdf) | Partial |
| Q3 | Access models and right-hand-side mass in Newton solves | [Summary document](qipm-notes/paper/main.pdf) | Partial |
| Q4 | Winner-take-all condensation in block log-determinant SDPs | [Summary document](qipm-notes/paper/main.pdf) | Possible |
| Q5 | Accuracy curves for hidden-block state conversion | [Summary document](qipm-notes/paper/main.pdf) | Not applicable |
| Q6 | Condition-one linear programs with hard loading and recovery | [Summary document](qipm-notes/paper/main.pdf) | Not applicable |
| Q7 | Limits of parity-gadget lower-bound constructions | [Summary document](qipm-notes/paper/main.pdf) | Partial |
| Q8 | Loading and recovery hardness for semidefinite programs | [Summary document](qipm-notes/paper/main.pdf) | Not applicable |
| Q9 | Trade-offs between preconditioning and state interfaces | [Summary document](qipm-notes/paper/main.pdf) | Partial |
| Q10 | Conditional speedups for sparse quantum interior-point methods | [Summary document](qipm-notes/paper/main.pdf) | Partial |
| Q11 | A correction to the complexity analysis of the quantum central path method | [Summary document](qipm-notes/paper/main.pdf) | Done |
| Q12 | Curvature, support certificates, and barrier complexity of conic lifts | [Full paper](qipm-notes/conic-lift-complexity/main.pdf) | Possible |
| Q13 | Classical and quantum query complexity of scalar Newton quantities | [Full paper](qipm-notes/scalar-newton-paper/main.pdf) | Not applicable |
| Q14 | The quantum cost of unit-normalized spectral shifting | [Full paper](qipm-notes/spectral-shift-paper/main.pdf) | Not applicable |
| Q15 | Exponential-cone scenario compression for entropic risk | Notes only | Not applicable |

### Molecular thermodynamics

| ID | Working title | Write-up | Lean |
|---|---|---|---|
| TD1 | Finite reservoirs at phase coexistence: full-state accuracy and phase correlations | [Full paper](thermo-notes/paper-finite-reservoirs/main.pdf) | Not applicable |
| TD2 | Survival-conditioned thermodynamic integration | Notes only | Possible |
| TD3 | Interfacial tension from bulk response in nonlocal double-parabola models | Notes only | Not applicable |
| TD4 | Capacity certificates for reversible nucleation kinetics | Notes only | Not applicable |

### Transport theory

| ID | Working title | Write-up | Lean |
|---|---|---|---|
| TP1 | Designing surface transport under uncertain kinetics: moment thresholds and measurement precision | [Full paper](transport-notes/paper-uncertain-mobility/main.pdf) | Not applicable |
| TP2 | Kinetic defects in adsorbing channels | Notes only | Not applicable |

### Aggregation kinetics

| ID | Working title | Write-up | Lean |
|---|---|---|---|
| AK1 | Sampling-law separation and finite nonlinear corrections in additive coagulation–fragmentation | [Full paper](aggregation-kinetics-notes/paper-additive-coagulation/main.pdf) | Not applicable |
| AK2 | Survival under unobserved sister-type dependence in multitype branching | Notes only | Possible |

### Heterogeneous catalysis: proposed experimental programs

| ID | Working title | Write-up | Lean |
|---|---|---|---|
| CA1 | Physical water management in Fischer–Tropsch synthesis | [Program document](catalysis-notes/manuscript/main.pdf) | Not applicable |
| CA2 | Steam compatibility of cyclic oxides in chemical looping | [Program document](catalysis-notes/manuscript/main.pdf) | Not applicable |
| CA3 | Catalyst demand in polymer ethenolysis | [Program document](catalysis-notes/manuscript/main.pdf) | Not applicable |
| CA4 | Nickel and the useful life of promoted silver epoxidation catalysts | [Program document](catalysis-notes/manuscript/main.pdf) | Not applicable |
| CA5 | Tungsten coordination and retention in sugar conversion | Notes only | Not applicable |
| CA6 | Product-rich liquid Ti-zeolite epoxidation | Notes only | Not applicable |
| CA7 | Oxygen fate and self-cleaning in zirconia-catalyzed styrene production | Notes only | Not applicable |
| CA8 | Acid-site assays and zeolite aging | Notes only | Not applicable |

### Status values

**Write-up**

- *Full paper*: a complete, compiled manuscript.
- *Summary document*: part of the long document that collects the quantum
  interior-point results, which the authors asked for instead of separate
  papers.
- *Program document*: a chapter of the document that ranks the proposed
  catalysis programs.
- *Notes only*: the results exist only as the agents' notes and checks.

**Lean**

- *Done*: the main mathematical results are proved in Lean, with no unproved
  steps; software and experiments are not covered.
- *Partial*: some of the results are proved in Lean, but not all.
- *Possible*: not done, but the main claims are mathematical statements that
  could be formalized with current libraries; this is a judgement, not a check.
- *Not applicable*: the main claims rest on numerical evidence, experiments, or
  modelling assumptions, or require a framework that current formal libraries
  do not provide, such as complexity classes, quantum query models, or limit
  theorems for stochastic processes.

## Citation

If you use this repository or refer to its contents, please cite the paper:

> Sergey Gusev and David E. Bernal Neira. AI Agent Swarms as Researchers:
> Progress, Challenges, and Open Questions. arXiv:2609.35719, 2026.
> https://arxiv.org/abs/2609.35719

```bibtex
@misc{gusev2026swarms,
  title         = {{AI} Agent Swarms as Researchers: Progress, Challenges, and Open Questions},
  author        = {Gusev, Sergey and Bernal Neira, David E.},
  year          = {2026},
  eprint        = {2609.35719},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CY},
  url           = {https://arxiv.org/abs/2609.35719}
}
```

## License

This repository is released under the [MIT License](LICENSE).
