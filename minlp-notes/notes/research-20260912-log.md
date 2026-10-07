# MINLP research continuation — September 12, 2026

This continuation began as an open-ended research program. The user subsequently
requested that current ideas be completed and verified, with no new directions,
and that work then stop. The [closeout record](research-20260912-closeout.md)
supersedes the running-task language in historical entries. The research sought
substantial practical value backed by correct mathematics, reproducible
implementation and independent review. Quantum computing, privacy-aware
learning and separate research areas were excluded.

## Starting state and relevance

The repository was clean at the start. It already contains substantial work on
pooling and passive-flow complexity, approximation formulation size, multilinear
convexification, switching control, and structured bilevel optimization. The
initial search therefore prioritizes new algorithmic capability over extending
those families by default.

David Bernal Neira's classical research in discrete-continuous nonlinear
optimization, algorithms, open-source software, and chemical, energy and
infrastructure systems defines relevance. Primary profile checked September 12:
<https://engineering.purdue.edu/COOPS/people/ptProfile?group_id=301591&resource_id=286478>.
The local September 10 literature review supplies a starting agenda, not a
complete or final account of prior art.

## Initial investigations

- MINLP/GDP algorithms: compact hull recognition, valid decomposition bounds,
  and numerical certification.
- Energy and process models: useful structural relaxations or algorithms with
  a realistic comparison against existing methods.
- Experimental measurement selection: information-matrix MINLPs, connected
  directly to Bernal Neira's coauthored measurement-design work.
- Local investigation: implicit-state relaxations and reliable subproblem cuts.

These are selection investigations. No new theorem or novelty claim has yet
been established.

## Literature handling

One reusable agent, `/root/literature`, owns all knowledge-base maintenance,
including checks. It uses the identified-literature path in
`/workspace/skills/literature/SKILL.md`, with model `gpt-5.6-luna`, maximum
reasoning effort, and no inherited context. Research agents send new identified
sources to that queue. Its batch reports and complete unresolved-source lists
are retained in `literature/runs/`. The
[report index](research-20260912-literature-report-index.md) links available
human-readable batch reports and explains how to interpret their unresolved
requests. The queue is empty and the final integrity check passed. The
[final source-access report](research-20260912-missing-sources.md) retains
the current 56 missing full texts and three insufficient artifacts, separately
from the global knowledge-base unread count.

## Reproduction and resources

The initial machine reports 36 logical CPUs and 30 GiB RAM. Experiments should
normally use one solver thread, with explicit limits before concurrent batches.
The isolated environment lives in `code/research_20260912/`; its `uv.lock` records
resolved dependencies. Solver license checks and experiment evidence are
recorded below and in the linked implementation notes.

The Gurobi smoke test passed with version 13.0.3, one thread, optimal status,
and the expected binary objective. Python 3.13.11, NumPy 2.5.3, SciPy 1.18.1,
and SymPy 1.14.0 are recorded by the locked environment. BLAS/OpenMP threads
are capped at one in comparison runs. GAMS is installed but has not been
needed or license-tested in this continuation.

## Measurement-selection investigation

The leading initial candidate was an exact path formulation for measurement
selection with fully observed Markov error blocks. The derivation, comparison
with a dense correlated-noise formulation, and strict rational example are in
[the design note](research-20260912-design-opportunities.md).

**Priority correction:** the deeper source search identified Lee, Gómez, and
Atamtürk, *Convexification of Multi-period Quadratic Programs with Indicators*,
arXiv:2412.17178, DOI 10.1007/s10107-026-02379-5. The proposed fixed-covariance
information graph is a linear image of their selected-principal-inverse path
hull. Therefore it is not retained as a new hull theorem. Singular-transition
cases follow by ordinary limits and do not supply a substantial novelty claim.
The path solver remains useful as a formulation/application investigation.

The independently written path-pricing solver and the two Gurobi OA formulations
live in `code/research_20260912/`. An initial eight-instance comparison is saved
at `code/research_20260912/results/initial_comparison.json`, including every
limit. Cases are small synthetic designs (12 or 24 times, three parameters,
five selections), with either generic sensitivities or a local two-step reaction
model. They are not a reproduction of a published industrial case. The path
formulations closed every case within their five-second limits; the dense OA
formulation closed two of eight. This is preliminary evidence from specific
implementations and settings, not a state-of-the-art solver claim. In particular,
the dense scalar noise split and root-cut initialization need fairer ablations.

Independent implementation review found two issues in the first path B&B draft:
tolerance-pruned node bounds were omitted from the final upper bound, and
malformed warm paths were accepted. Both were corrected. Input checks now reject
asymmetric/nonfinite priors and noninteger face indices. The review preserves
the counterexamples and checks the corrected implementation.

The separate [source audit](research-20260912-measurement-source-audit.md)
confirms a distinction between gating a full inverse covariance and inverting
the selected covariance in the inspected *Measure This, Not That* manuscripts
and code. It records affected and unaffected cases, conditional-mean semantics,
source versions, and limits. The subsequent
[kinetics re-evaluation](research-20260912-kinetics-selection-recheck.md)
enumerates all 2,347 nonempty schedules allowed by the inspected source model.
At a $3,000 budget, correcting the trace-information criterion changes the
selected plan and avoids a 3.11% loss relative to the corrected optimum. All
other tested trace budgets and all tested D-optimal and conventional A-optimal
choices agree. Exact rational comparisons certify every trace optimum, and a
[fresh review](research-20260912-kinetics-independent-review.md) independently
reproduces the schedules, criteria and certificates. This is a source-model
re-evaluation using the archived sensitivity data, not a claim to reproduce
stored published selections or regenerate physical experimental data.

A strengthened comparison uses a dense noise split of 0.99 and up to 200 root
LP cuts, recorded in `code/research_20260912/results/strengthened_comparison.json`.
The dense method closes three of eight cases and both path methods close eight.
These remain limited implementation comparisons: split and initialization were
changed together, incomplete LP runs remain capped, and stronger competing
implementations have not been tested. The
[independent OA review](research-20260912-oa-solver-independent-review.md)
checks 213 fresh OA calls and every saved record against independent enumeration.
It finds no invalid tested bound, documents numerical conditioning limits, and
identifies a reporting defect: exceptions lost partial cases. The benchmark
driver now saves each solve and records solver exceptions before continuing.

The [gated-information bound note](research-20260912-gated-information-bounds.md)
applies the classical operator Kantorovich inequality to quantify this model
distortion and certify corrected objective gaps. Its
[independent review](research-20260912-gated-bound-independent-review.md)
passes the stated claims with the Gaussian fixed-covariance and positive
eigenvalue assumptions made explicit. No new matrix inequality is claimed.

## Current direction: dynamic MINLP relaxations

The [ODE opportunity note](research-20260912-second-opportunities.md) develops
a restricted regularity proof and globally valid support construction for
extended McCormick state relaxations with affine invariants. It targets explicit
regularity and subgradient questions in Ye and Scott (2025). The current scope
is polynomial expressions with fixed valid interval bounds and specified
convex, monotone refinement operations. Fresh mathematical and implementation reviews passed, with corrections
recorded below. The supporting comparison mechanism is established; the
remaining potential is a useful certified implementation and a stronger
comparison against existing dynamic global optimizers.

The first [certified ODE support prototype](research-20260912-ode-prototype.md)
now compiles exact rational affine supports and propagates them with certified
linear-integration error allowances. Twelve small cases cover closed
dimerization and a stylized five-species energy-reaction system. They establish
functionality, not a solver improvement. Review found and prompted correction
of an integer-metadata division bug that could invalidate a bound by a small
exact amount. A separate limitation is retained: fixed broad state boxes leave
nonzero gaps even for singleton parameter boxes. Validated time-dependent tubes
and conservative coefficient rounding are now implemented and independently
reviewed; the prototype note records their convergence conditions, exact
counterexamples and initial timing improvements. No comparison against a
competing dynamic global optimizer has yet been made.

## Reopened measurement lead: noisy scalar Markov errors

The [finite-history investigation](research-20260912-noisy-markov-memory.md)
addresses additive observation noise, which destroys the exact observed-chain
Markov property used earlier. It applies established Vecchia conditionals and
derives an explicit spectral error bound uniform over all selected subsets.
A calendar-bitmask graph then gives an exact hull of the surrogate information
and a corrected upper bound on the true design objective. Fresh review finds
the initial proof sound and has suggested sharper constants. The practical
state multiplier is reasonable only for some moderate-correlation cases;
high persistence can make it prohibitive. The completed implementation,
independent reviews and qualified prior-art comparisons are recorded below.

An [exact certificate implementation](research-20260912-noisy-markov-certificates.md)
now recomputes the design bound using rational local conditionals, integer
dynamic programming and rigorous logarithm enclosures. Initial independent
checks pass. In a 48-candidate synthetic case, window eight achieves a certified
logdet gap of `0.00270073`, with about 0.58 seconds for the numerical hull solve
and 0.90 seconds for certification. The stronger dense baseline solves the
smaller cases quickly, correcting an initially overstated comparison. Multiple
seeds and larger instances have now been tested: six window-eight cases at
48 and 96 candidates have independently recomputed exact gaps between
`0.00178161` and `0.00387283`. This remains a synthetic benchmark. A
[structured dense oracle](research-20260912-structured-dense-oracle.md) removes
avoidable cubic covariance algebra using classical methods. Fresh review has
identified loss of numerical accuracy near unit correlation despite a
well-conditioned observation covariance; that limitation is being retained
with a reproducible witness. A
[covariance-space innovation adjoint](research-20260912-covariance-dense-oracle.md)
now passes independent review and removes the demonstrated invalid cuts. It
uses established filtering and smoothing identities. The review also found
and helped fix an intermediate smoothed-mean subtraction failure at extreme
signal-to-noise ratios. Floating-point tangents remain separate from exact
certificates. The
[exact rational comparator](research-20260912-exact-dense-design-certificates.md)
has now passed [fresh review](research-20260912-dense-certificate-independent-review.md).
For all six cases, a feasible continuous-relaxation objective is strictly larger
than the memory certificate's upper bound on the original discrete optimum.
The measured difference is `0.02430` to `0.05043` in log determinant. This
certifies weakness of that continuous relaxation independently of its numerical
solve time or the optimality of any supplied incumbent. The [all-splits comparison](research-20260912-all-splits-separation.md) also
passed fresh review, extending the conclusion to every scalar virtual-noise
split for these cases. The
[arbitrary-diagonal comparison](research-20260912-diagonal-split-separation.md)
also passed fresh review on the 48-candidate early-peak chemical case. Its
single feasible fractional witness survives the pointwise all-split envelope
and every affine upper tangent from that family, at least `0.0925444` above
the memory certificate's integer upper bound. This is a root-relaxation
barrier for those cuts; it does not cover branching or other cut families.

Four [smooth chemical-kinetics cases](research-20260912-noisy-markov-kinetics-probe.md)
now have exact gaps below `0.001943`. Fresh review verifies their mass-balance
sensitivities and reconstructs all saved information matrices and certificates.
These use an explicitly stylized error covariance and a local Fisher criterion;
they do not establish global parameter identifiability or an experimentally
validated noise model. A
[minimum sampling-gap refinement](research-20260912-noisy-markov-spacing.md)
has passed exact proof checks. It tightens the residual bound and removes
infeasible calendar masks. The constrained producer and exact certificate have
passed independent review. On the 96-candidate, minimum-gap-two example,
[verified outward integer arc scores](research-20260912-spacing-certificates.md)
reduce certificate time from 36.61 seconds to 1.09 seconds while increasing
the upper bound by exactly `1e-8`.
The [reviewed pair-bound integration](research-20260912-refined-spacing-integration-review.md)
then reduces the same incumbent's certified gap from `0.01155766` to
`0.00972559`, rounded upward, in about 1.09 seconds.

The [factorization priority audit](research-20260912-noisy-markov-fsai-priority-audit.md)
finds strong established locality theory. The explicit noisy calendar-window
constant and design certificate remain the candidate combination; neither the
Vecchia approximation nor the implication from precision/KL bounds to Fisher
bounds is new. The audit also preserves a freshly verified counterexample to
a thesis's general supermodularity claim, with its exact scope and ordering
caveats.

The [scalar approximation scheme](research-20260912-scalar-noisy-design-fptas.md)
is correct, but a [reviewed reduction](research-20260912-scalar-gmrf-prior-reduction.md)
to earlier Gaussian message passing makes a first-FPTAS claim unsafe. The
current [full-block theorem](research-20260912-full-block-design-fptas.md)
has passed independent review with channel count and weighted-trace rank as
input dimensions. The error bound and history-state exponent are dimension
independent, whereas the generic prior reduction's treewidth grows. The audit
has not found an older theorem with the complete stated scope; priority remains
qualified. A reviewed hardness reduction shows why full-block acquisition
matters: selecting individual channels has no deterministic FPTAS unless
P=NP, even with covariance condition number at most 5/3.

The [coupled spectral-snapshot prototype](research-20260912-block-snapshot-probe.md)
passed [fresh implementation review](research-20260912-block-snapshot-independent-review.md).
Its first two cases are inexpensive
but do not show a solution-quality advantage: greedy chooses the same schedule,
and the dense Liu relaxation gives tighter numerical upper bounds. The block
dynamic program's state count remains 64 masks in both 4- and 16-channel cases.
These are stylized local-kinetics probes with full snapshot acquisition.

Two broader theoretical results have now passed independent review. The
[general covariance theorem](research-20260912-general-covariance-memory-bound.md)
requires temporal covariance decay and a positive covariance lower bound,
without a supplied Markov realization. Its
[priority audit](research-20260912-covariance-decay-priority-audit.md) finds
strong established analytical locality theory; the discrete approximation
scheme remains the candidate combination. Its explicit constants are too
conservative to improve the current experiments.

The [fixed-parameter D-optimal scheme](research-20260912-fixed-parameter-doptimal-fptas.md)
handles rational positive semidefinite matrix sums along an explicit acyclic
graph, including singular priors. A guessed factor basis controls matrix
scales, and a dynamic program rounds signed matrix entries. Fresh review
confirms the determinant guarantee and polynomial bit complexity for fixed
parameter dimension. Combining it with finite-history information bounds
gives a D-optimal design FPTAS. This is a theoretical capability with large
runtime bounds; no practical implementation or publication-priority claim is made.

A [sharper partial-observation theorem](research-20260912-partial-observation-memory-bound.md)
uses a positive process-noise contribution and a bound on signal covariance
relative to measurement noise. Its baseline and normalized, coordinate-invariant
refinement passed independent review. Whole fixed sensor packets may observe
only part of an input-sized latent state. The
[two-mode drift probe](research-20260912-partial-observation-trace-probe.md)
applies the resulting weighted-trace algorithm to four chemical-kinetics cases.
The numerical implementation and
[new exact certificates](research-20260912-partial-trace-certificates.md)
passed separate fresh reviews. All four exact certificate gaps are below
0.0604%, with certificate times of about 0.6–1.3 seconds, excluding design
generation. The dense numerical comparator is faster but gives wider bounds.

The [PSD path approximation set](research-20260912-dag-psd-approximation-set.md)
also passed fresh independent review. For fixed matrix dimension, a
polynomial-size collection of feasible paths approximates every feasible
matrix in both directions under PSD order, including singular matrices with
the same kernel. The collection can serve D-, A-, E- and estimable-contrast
criteria chosen afterwards. Its exponent is large and its priority remains
unresolved; older multiplicative covariance pruning is explicitly credited.
The [represented-matroid extension](research-20260912-represented-matroid-psd-approximation-set.md)
also passed [fresh review](research-20260912-represented-matroid-psd-independent-review.md).
It replaces path pricing by the established exact profile machinery of
Berstein et al. and preserves original matroid rank through filtering,
contraction and recovery. Its deterministic FPTAS consequences concern fixed
information dimension and an explicit rational representation; they do not
cover arbitrary independence-oracle matroids.

The [robust three-scenario prototype](research-20260912-robust-kinetic-design.md)
uses one common schedule and propagates uncertainty in the individual optima
used to standardize D-efficiency. Its
[exact certificates and nominal comparisons](research-20260912-robust-design-certificates.md)
passed fresh independent review. At 48 and 96 candidates, the standardized
log gaps are exactly `0.008525235239` and `0.016642464577`; all three individual
reference certificates are recomputed. Conservative rational comparisons prove
at least 3.33% and 0.80% improvement over the saved central-scenario schedules.
Greedy/exchange supplies the better incumbent in the first case and generated
paths in the second. The subsequently completed
[dense comparison and polishing](research-20260912-robust-dense-comparison.md)
passed [fresh review](research-20260912-robust-dense-independent-review.md).
Polishing the 96-candidate hull design gives a new exact standardized gap of
`0.011487999119`, with a worst D-efficiency lower bound of about 97.173780%.
The earlier artifacts remain intact. The
[robust priority audit](research-20260912-robust-scenario-design-priority-audit.md)
finds direct prior work on robust kinetics and binary correlated-noise design;
robust scalarization and tangent bounds are not new principles.

The [fixed-physical-grid benchmark](research-20260912-fixed-physical-grid-benchmark.md)
and its refined transfer passed
[fresh review](research-20260912-fixed-physical-grid-independent-review.md).
It holds the physical covariance, horizon and budget of 16 observations fixed
while refining 48, 96 and 192 candidates. The refined numerical log gaps are
0.005971 at 48 points and 0.037097 for a separate smaller-window 96-point
diagnostic. The primary finer-grid memory runs completed no price within their
caps. This retained negative result limits the earlier favorable fixed-step
correlation comparisons; it is not a necessity lower bound for every method.

The [latent-separator construction](research-20260912-latent-separator-design.md)
addresses that representation cost by conditioning on latent block boundaries.
It expresses the original selected information exactly as an augmented
information Schur complement. Removing nested anchors tightens its mixture
relaxation. Its [mathematical review](research-20260912-latent-separator-independent-review.md)
passed, including exact bridge filtering and the arbitrary-witness certificate.
The [prototype](research-20260912-latent-separator-implementation.md) and
[rational certificates](research-20260912-latent-separator-certificates.md)
passed separate fresh
[numerical](research-20260912-latent-separator-implementation-independent-review.md)
and [exact implementation](research-20260912-latent-separator-certificate-independent-review.md)
reviews. Both reported numerical failure cases were repaired and rechecked;
all 13 saved numerical witnesses and all five rational certificates passed.
The best saved exact
192-point gap is `0.157284408207`; its numerical solve takes about 14.4 seconds
and exact certification adds about 20.6 seconds. This improves the tested dense
upper bound but misses the 0.01 target. The refined calendar bound remains
better at 96 candidates. Established Schur design, conic formulations and
mixture optimization are credited in the
[priority audit](research-20260912-latent-separator-priority-audit.md).

## Other findings retained

The [storage investigation](research-20260912-energy-opportunities.md) rejected
a prospective trajectory-hull theorem because of warehouse prior art. It retained
a three-period quadratic-cost convexification gap of exactly 9/8 and a sharp
balance-aware conic inequality. A
[fresh independent review](research-20260912-storage-independent-review.md)
passed the mathematical claims. They are useful examples, with no publication
priority or performance claim.

The [algorithm investigation](research-20260912-algorithm-opportunities.md)
retained an LP that repairs local infeasibility multipliers to yield a globally
convex aggregate of original quadratic rows, with an exact two-row example.
Its [independent review](review-20260912-quadratic-conflict-example.md) passed
after stated corrections. Aggregation and diagonal-dominance mechanisms are
established; practical benefit and algorithmic novelty remain to be tested.
