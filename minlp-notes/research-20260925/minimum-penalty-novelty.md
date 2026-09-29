# Independent novelty and significance audit: minimum exact ALD penalty

Date: 2026-09-25. Scope: literature and significance audit of the proposed
SUBSET SUM reduction for the smallest exact sharp augmented-Lagrangian
penalty. This file does not certify the reduction's proof.

The credible contribution is a restricted hardness and approximation result,
not the first hardness theorem for choosing exact penalties. The strongest
candidate statement uses a linear objective, a native binary box, one scalar
equality, and an optimized unrestricted scalar multiplier. The native set
therefore admits trivial linear optimization. The claimed lack of any
polynomial-factor guaranteed upper approximation is more consequential than
exact computation hardness alone, subject to a careful input-length argument.

## Closest prior hardness result

[Edoardo Alessandroni, Sergi Ramos-Calderer, Ingo Roth, Emiliano Traversi, and Leandro Aolita,
*Alleviating the quantum Big-M problem*](https://www.nature.com/articles/s41534-025-01067-0),
npj Quantum Information 11, 125 (2025),
[open preprint](https://arxiv.org/pdf/2307.10379), was inspected in arXiv v4,
30 July 2025, especially Observation 1 and Section IV.A, Lemma 1.
It proves hardness of an optimal exact quadratic penalty and of testing a
supplied penalty under a separation promise. Its reduction has the known
constrained optimum at the all-zero assignment. Thus hardness despite an
easy original optimum is already present. Its objective is quadratic, its
penalty is squared equality violation, and it does not optimize a linear
Lagrange multiplier. No multiplicative approximation lower bound was found
in the inspected theorem. This negative search conclusion also rests on
reading the Results and Discussion sections and searching the full v4 PDF
for `approximation`, `factor`, and `optimal M`. The approximation ratios
found concern solutions returned by quantum algorithms, not approximation
of the minimum penalty parameter. This is an inspection report, not a
claim that every possible implication of the paper has been ruled out.

There is an essential mathematical distinction. Their constraint is
`x = 0`, so its squared violation on binary variables is `sum(x_i)`.
An unrestricted multiplier vector can reproduce this term when the
augmentation coefficient is zero. Their displayed reduction consequently
does not establish the proposed optimized-ALD hardness. Conversely, changing
the penalty type alone would not suffice as a novelty argument: on that
binary residual, the squared Euclidean and one-norm penalties agree.

The proposed scalar residual has both signs among objective-improving
assignments. This is what prevents the optimized multiplier from eliminating
the need for augmentation. The linear objective and easy native box further
distinguish the proposed reduction. Generic hardness for an optimized ALD
could plausibly be obtained by symmetrizing a known penalty construction;
that observation is a significance caution, not a verified alternative
reduction.

## Other primary sources examined

| Source and inspected part | Relevant comparison |
| --- | --- |
| [Gusmeroli and Wiegele, *EXPEDIS: An Exact Penalty Method over Discrete Sets*](https://arxiv.org/pdf/1912.09739), inspected January 2021 preprint, Section 5, especially Lemma 6 and Proposition 8 | Gives exact squared-penalty choices from bounds on objective values over feasible and infeasible binary points. The text observes that the exact extrema are difficult to compute. This is useful prior theory for upper bounds, rather than the proposed multiplier-optimized threshold hardness. |
| [Marcos Diez García, Mayowa Ayodele, and Alberto Moraglio, *Exact and Sequential Penalty Weights in Quadratic Unconstrained Binary Optimisation with a Digital Annealer*](https://ore.exeter.ac.uk/rest/bitstreams/185242/retrieve), GECCO 2022 Companion, DOI 10.1145/3520304.3528925, abstract and Sections 2–3 | Gives computable sufficient upper bounds and sequential methods. Its objective-range bound does not provide a multiplicative approximation guarantee relative to the least valid penalty. It uses agreement of optimal solutions, so ties at a threshold must be distinguished from dual-value exactness. |
| [Maksim V. Dolgopolik, *Minimax Exactness and Global Saddle Points of Nonlinear Augmented Lagrangians*](https://jano.biemdas.com/issues/JANO2021-1-5.pdf), J. Applied Numerical Optimization 3 (2021), 61–83, DOI 10.23952/jano.3.2021.1.05, Definitions 3.1–3.2, Theorem 3.1, and Section 4 | Provides established terminology for least minimax exact parameters and relates exactness, saddle points, and dual attainment. Its principal results concern existence and localization, rather than finite-input computational complexity. A least parameter indexed by a fixed tuning multiplier must be distinguished from minimizing over that multiplier. |
| [Bihani, Kužel, Povh, and Pucher, *Quantum and Simulated Annealing-Based Iterative Algorithms for QUBO Relaxations of the Sparsest k-Subgraph Problem*](https://arxiv.org/pdf/2509.08544), 11 September 2025, Section 3.3, Lemma 20 | Gives an explicit sufficient multiplier/penalty pair for a cardinality-constrained quadratic binary problem. It does not characterize the smallest jointly optimized augmentation coefficient. Its earlier multiplier intervals concern the unaugmented Lagrangian. |
| [Lefebvre and Schmidt, *Exact Augmented Lagrangian Duality for Nonconvex Mixed-Integer Nonlinear Optimization*](https://optimization-online.org/wp-content/uploads/2024/07/exact-penalty-for-minlp-1.pdf), local 15 December 2025 version, conclusion | Explicitly conjectures that computing the smallest gap-closing penalty cannot be done in polynomial time. The proposed sharp-ALD theorem addresses this question. Attribute the question to this inspected version and separately acknowledge earlier QUBO hardness. |

The local review `parametric-penalty-literature-review.md` was also consulted.
Its nonlinear precision construction is a separate issue: representation
length of a sufficient penalty differs from computational difficulty of
finding a near-minimum one.

The Dolgopolik title above was checked directly on the published PDF's first
page. Although that article discusses general merit functions, its published
title ends in *Nonlinear Augmented Lagrangians*, not *Merit Functions*.

## Claims and limitations that should remain explicit

- Define exactness as equality of the optimized dual value and the primal
  value. Distinguish this from the requirement that every minimizer of a
  penalized problem be primal feasible. The latter can require a strict
  inequality at the same infimum threshold.
- The fixed-`K` SUBSET SUM family establishes ordinary hardness with
  binary-encoded integer data. It should not be described as a strong
  hardness result. The separate stable-set construction can have unit
  data, but loses the easy native linear optimization property.
- A polynomial-factor upper approximation must return an exact coefficient
  bounded above by a polynomial in the full encoded instance length times
  the optimum. The chosen `K`, coefficient multiplication, and resulting
  instance length must all be accounted for. The optimum is positive on
  this construction, avoiding a zero-optimum approximation convention.
- A universal easily computed sufficient penalty is compatible with these
  lower bounds. The obstruction concerns guaranteed closeness to the
  least coefficient, not existence or computability of some sufficient
  coefficient.
- The result gives a calibration barrier, not a solver speedup or a general
  impossibility of useful adaptive choices. Its practical implications
  require analysis of structured model classes, heuristic calibration, or
  a tradeoff between penalty size and subproblem difficulty.

## Search and verification record

Open-web searches included minimum/smallest/least exact penalty parameters,
sharp augmented Lagrangian complexity, NP-hardness and coNP-hardness of
penalty validity, QUBO optimal penalties, minimax exactness, and penalty
inapproximability. A separate reviewer searched QUBO collisions and located
the Alessandroni paper and the Bihani paper; their important distinctions
were then checked directly against the primary PDFs.

That reviewer also examined the 2026 successor
[Alessandroni et al., *Scalable Determination of Penalization Weights for
Constrained Optimizations on Approximate Solvers*](https://tore.tuhh.de/dspace-cris-server/api/core/bitstreams/ca63fdf1-b348-44a0-8c7f-9fb9b2694575/content).
The reviewer reports squared penalties for probabilistic feasibility under
Gibbs solvers, with hardness of the new minimal probabilistic penalty stated
as an expectation rather than proved. The present auditor's attempt to
open that PDF failed, so this comparison remains independently reported
and is not part of the directly inspected source conclusions above.

No equivalent theorem with all the proposed restrictions or the stated
approximation barrier was located. This limited search does not establish
novelty. The strongest justified framing is a refinement and extension of
known exact-penalty hardness to a sharply restricted optimized-ALD setting,
with a direct response to the inspected conjecture.

Targeted local actions were `rg` searches in the existing literature review
and Lefebvre–Schmidt text, and reading the existing penalty notes. Primary
source PDFs were inspected through the web tool. No repository-wide tests
or CI checks were performed; this audit contains no formal or computational
proof verification.
