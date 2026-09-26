# Research output of AI agent swarms

This repository holds the research corpus described in the paper "AI Agent
Swarms as Researchers: Progress, Challenges, and Open Questions" by Sergey
Gusev and David E. Bernal Neira. The paper's research inventory (appendix) lists
the potential papers in the corpus, with IDs such as M1 or Q12, and links to
the drafts below.

## What this is

Everything here was written by AI agents during the runs described in the
paper: notes, checks, code, review records, Lean proofs, and paper drafts. The
authors of the paper have not edited it and, except where the paper says
otherwise, have not verified its claims. It stands as it was before any human
input on its content; the authors' part in producing it was limited to the
process and editorial instructions described in the paper. The drafts are not
final papers: the authors intend to take them further, and later versions may
include human input.

This is a snapshot of 25 September 2026. The runs continue, so the source
repositories have moved on since.

The compiled PDF of the power-flow draft (M10), which the source repository
does not track, was built from the sources here and added.

## Folders

Each folder is a copy of the committed content of the notes repository for one research area.

| Folder | Field | Source commit |
|---|---|---|
| `minlp-notes` | Mixed-integer nonlinear programming | `3cd905d5` |
| `qipm-notes` | Quantum interior-point methods | `5c152d2` |
| `thermo-notes` | Molecular thermodynamics | `3485e1d` |
| `transport-notes` | Transport theory | `de45280` |
| `aggregation-kinetics-notes` | Aggregation kinetics | `c69aeed` |
| `catalysis-notes` | Heterogeneous catalysis (proposed experimental programs) | `57e3202` |

## Drafts

| ID | Draft | PDF |
|---|---|---|
| M1 | Sharp gaps for positive multilinear relaxations | [`minlp-notes/paper-multilinear-gap/main.pdf`](minlp-notes/paper-multilinear-gap/main.pdf) |
| M2 | Verified bounds for positive cubic relaxation gaps | [`minlp-notes/paper-cubic-gap/main.pdf`](minlp-notes/paper-cubic-gap/main.pdf) |
| M3 | Checkable lower bounds for convex mixed-integer nonlinear optimization | [`minlp-notes/paper-certified-minlp/main.pdf`](minlp-notes/paper-certified-minlp/main.pdf) |
| M4 | Convex relaxation gaps and spatial certificates in nonlinear optimization | [`minlp-notes/paper-relaxation-limits/main.pdf`](minlp-notes/paper-relaxation-limits/main.pdf) |
| M5 | Integer dimension in convex mixed-integer approximation of nonlinear graphs | [`minlp-notes/paper-integer-dimension/build/main.pdf`](minlp-notes/paper-integer-dimension/build/main.pdf) |
| M6 | Rounding switching controls under a hard switch budget | [`minlp-notes/paper-switching-control/main.pdf`](minlp-notes/paper-switching-control/main.pdf) |
| M7 | Sparse convex hulls for network flows coupled to a simplex | [`minlp-notes/paper-network-simplex/main.pdf`](minlp-notes/paper-network-simplex/main.pdf) |
| M8 | Topology, uncertainty, and precision in passive potential-flow optimization | [`minlp-notes/paper-potential-flow/complexity/main.pdf`](minlp-notes/paper-potential-flow/complexity/main.pdf) |
| M9 | The complexity of pooling | [`minlp-notes/papers/pooling/main.pdf`](minlp-notes/papers/pooling/main.pdf) |
| M10 | Exact feasibility of resistive and AC power networks | [`minlp-notes/paper-power-flow/build/main.pdf`](minlp-notes/paper-power-flow/build/main.pdf) |
| M11 | Structured bilevel optimization with many follower variables | [`minlp-notes/paper-structured-bilevel/paper.pdf`](minlp-notes/paper-structured-bilevel/paper.pdf) |
| M12 | Globally certified measurement selection with correlated errors | [`minlp-notes/paper-correlated-measurements/build/main.pdf`](minlp-notes/paper-correlated-measurements/build/main.pdf) |
| M13 | Radial and point separation for perspective outer approximation | [`minlp-notes/paper-lbesh/main.pdf`](minlp-notes/paper-lbesh/main.pdf) |
| M14 | Quadratic aggregation: certificates, finite descriptions, and approximation | [`minlp-notes/paper-quadratic-aggregation/paper.pdf`](minlp-notes/paper-quadratic-aggregation/paper.pdf) |
| Q1 | Objective sublevels and central-path Hessian conditioning | [`qipm-notes/conditioning-paper/main.pdf`](qipm-notes/conditioning-paper/main.pdf) |
| Q2 | The cost of following the central path | [`qipm-notes/central-path-cost/main.pdf`](qipm-notes/central-path-cost/main.pdf) |
| Q3–Q11 | Summary document on quantum interior-point methods | [`qipm-notes/paper/main.pdf`](qipm-notes/paper/main.pdf) |
| Q12 | Curvature, support certificates, and barrier complexity of conic lifts | [`qipm-notes/conic-lift-complexity/main.pdf`](qipm-notes/conic-lift-complexity/main.pdf) |
| Q13 | Classical and quantum query complexity of scalar Newton quantities | [`qipm-notes/scalar-newton-paper/main.pdf`](qipm-notes/scalar-newton-paper/main.pdf) |
| Q14 | The quantum cost of unit-normalized spectral shifting | [`qipm-notes/spectral-shift-paper/main.pdf`](qipm-notes/spectral-shift-paper/main.pdf) |
| TD1 | Finite reservoirs at phase coexistence | [`thermo-notes/paper-finite-reservoirs/main.pdf`](thermo-notes/paper-finite-reservoirs/main.pdf) |
| TP1 | Designing surface transport under uncertain kinetics | [`transport-notes/paper-uncertain-mobility/main.pdf`](transport-notes/paper-uncertain-mobility/main.pdf) |
| AK1 | Sampling-law separation and finite nonlinear corrections in additive coagulation–fragmentation | [`aggregation-kinetics-notes/paper-additive-coagulation/main.pdf`](aggregation-kinetics-notes/paper-additive-coagulation/main.pdf) |
| CA1–CA4 | Document ranking the proposed catalysis programs | [`catalysis-notes/manuscript/main.pdf`](catalysis-notes/manuscript/main.pdf) |

Inventory rows marked "Notes only" in the paper have no draft; their results
are in the notes of the same folder.
