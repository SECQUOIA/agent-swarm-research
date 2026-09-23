# Stage 2 independent review 4

Reviewed 2026-09-13. Scope: `sections/02-locality.tex`,
`appendices/locality-scope.tex`, the model and notation dependencies in
`sections/01-foundations.tex` and `macros.tex`, and the Stage 2 coverage map.
The principal focus was spacing, graph feasibility, calendar scope, and exact
counterexamples. I did not read any other reviewer report or use the author's
verification scripts. No manuscript file was changed.

## Verdict

**PASS. No MAJOR or MINOR correction is requested in the reviewed stage.**
The absence of later approximation, certificate, and computational sections is
intentional under the stage plan and is not a defect in this review.

## Mathematical assessment

- The innovation floor at `02-locality.tex:365` is valid. A history in a
  length-L calendar window contains at most floor(L/g) selected observations;
  each gap from one such observation to the next, including the last gap to
  the target, is at least g. The Riccati map increases with its input and with
  gap length, while its iterates from P decrease. Consequently replacing
  gaps by g and filling the permitted history count lowers the target
  innovation variance. This also covers L<g, where the history is empty.
- The near majorant at `02-locality.tex:374` correctly uses
  ell=max(g,L+1-h), rather than incorrectly rounding ell to a multiple of g.
  Distances need only be separated by g, so the decreasing sequence
  ell,ell+g,... is a valid packing upper bound. The stationary first-gain
  factor multiplies only surviving old-covariance terms. It is not applied
  to an empty-history far pair.
- The recurrence at `02-locality.tex:381` exactly maximizes the specified
  nonnegative distance weights over separated distances. Taking independent
  maxima to the left and right of an anchor is a valid bound and does not
  assume simultaneous attainability of all covariance majorants. Division
  by the common innovation floor bounds the two-sided normalization.
- The separated-mask count at `02-locality.tex:768` is correct, including
  L=0 and g>L. Its upper summation limit ceil(L/g) is the maximum possible
  number of ones. The explicit cooldown or max(L,g-1) feasibility memory at
  line 774 repairs the otherwise real loss of spacing information. The
  distinction between the information history and feasibility memory is
  clear. Count layering and negative scalar support weights do not create
  a difficulty for acyclic longest paths.
- The distinction at `02-locality.tex:783` between calendar windows and
  selected-count windows is mathematically sound. Reindexing selected
  scalar times preserves the variance/noise bounds and yields gap
  contractions at most rho, but the tuple of original indices is a
  different graph state. The manuscript does not infer grid-uniform
  scalability from a fixed per-index decay promise.
- The nonstationary covariance witness gives exactly -1/20, exceeding
  the invalid stationary-factor majorant 1/32 in absolute value. The
  random-intercept expression at `locality-scope.tex:95` is a correct
  telescoping sum, including L=0 and the complete-history boundary.
- The KL eigenvalue identity and its two-root relative sandwich are valid.
  The repeated-pair example gives eigenvalues 1±rho/2, total KL growing
  with the number of pairs, and the stated unnormalized Kaporin value at
  `locality-scope.tex:149`. It does not suggest that a global KL bound is
  insufficient to control mean information.
- The four rational pivot precisions, determinant ratios, and negative
  supermodular slack at `locality-scope.tex:201` are correct. The pivot-first
  marginal is a sum of marginal conditional-variance logarithms, not a
  joint conditional determinant. The fixed-order exponential-greedy
  contradiction is valid and is correctly withheld for the pivot-first
  convention, where pivot three is the greedy choice.
- I also read the residual transfer, general row lemma, scalar/full-block
  proofs, covariance-decay proof, and intrinsic partial-observation proof
  for broad consistency. In particular, the full-block sharp far identity
  does not require matrix commutativity, and the partial-observation
  transport uses covariance order and range factorization without an
  inverse of singular latent covariance. I found no invalid inference in
  those arguments.

## Independent checks

The review-only program is
`verification/stage02-review4/check.py`. It forms actual selected principal
covariances and recomputes each regression by direct linear algebra; it does
not invoke manuscript producer code. Execution with
`code/research_20260912/.venv/bin/python` passed:

- 9,696 stationary separated schedule/window cases on n=8, with all
  nonempty subsets that satisfy each gap, L=0,...,7, g=1,...,9, and three
  signal/noise/transition settings including a negative transition;
- innovation-floor, every residual-pair majorant, and final spectral-bound
  assertions in every such case;
- direct subset enumeration against each finite-row pricing recurrence;
- 195 independent mask-count comparisons for L=0,...,12 and g=1,...,15;
- SymPy exact arithmetic for the nonstationarity witness, all pivot
  determinant ratios and trace normalizations, the negative 175/256
  multiplicative slack, the integer inequality supporting the greedy
  contradiction, and random-intercept information for n=1,...,9.

These finite tests corroborate the proofs; they are not represented as
proofs of the universal claims.

## Primary-source and scope checks

I read `literature/AGENTS.md` and checked the relevant claims directly
against PDF text extracted from the originals, not only the repository's
literature summaries:

- `literature/papers/kaminetz2025-everything-is-vecchia-unifying-column/original.pdf`,
  printed pp.12–14: equations (4.8)–(4.10), Theorem 4.3, its fixed-order
  pattern statement, the additional factor 1/2 in its objective, and the
  subsequent greedy proof. The manuscript accurately locates the false
  marginal-identity/supermodularity step and distinguishes the alternative
  pivot-first interpretation.
- `literature/papers/kaminetz2026-everything-is-vecchia-unifying-low/original.pdf`,
  printed pp.2–3: Definition 1.1 raises the mean eigenvalue to the rank
  before dividing by the eigenvalue product. Thus the paper's Kaporin
  normalization and explicit warning about the dimension-normalized root
  are correct. This separate work should not receive the thesis's false
  supermodularity attribution; the manuscript maintains that distinction.

The Stage 2 coverage map matches the material inspected. It explicitly
reserves computational complexity and approximation-set obligations for
later stages. Known exact Markov hull machinery, Vecchia construction, and
covariance localization ingredients are credited, and the discussion makes
appropriately limited claims for the explicit constants and their later
design use.
