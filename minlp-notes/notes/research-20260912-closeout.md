# September 12 research closeout

This record closes the current ideas at the user's request to finish and verify
them, stop opening new directions, and then stop. Independent mathematical,
implementation and completion reviews have passed, and the literature queue
is empty. The continuation is complete and stopped within that revised scope.
This record supersedes prospective task language in earlier notes.

The continuation produced independently reviewed mathematical results and
reproducible optimization prototypes. The strongest theoretical candidate is a
relative PSD approximation set for feasible paths and rationally represented
matroid bases. The strongest implemented capability is exact global
certification of measurement-selection problems with correlated errors.
Publication priority remains qualified. The evidence does not establish a
broadly superior MINLP solver or an experimentally validated process-design
advance; the theoretical approximation-set algorithm has not been implemented
as a competitive solver.

## Results and verification

“Independent review” below means a separate research agent's proof and/or code
audit. It is not journal peer review or machine-checked proof of every theorem.
Exact numerical certificates bound the stated rational input model. Supplied
kinetic sensitivities and stipulated noise covariances remain modeling inputs.

| Current result | Established scope | Verification and limits |
|---|---|---|
| [Relative PSD approximation sets on DAGs](research-20260912-dag-psd-approximation-set.md) | For fixed information dimension, polynomially many actual feasible paths approximate every feasible information matrix in both PSD directions, preserving singular kernels. D-, A-, E- and estimable-contrast criteria can be chosen afterwards. | [Fresh proof and exact finite-instance review](research-20260912-psd-approximation-set-independent-review.md). The exponent is large; the checker is not a practical implementation of the general algorithm. |
| [Rationally represented matroid extension](research-20260912-represented-matroid-psd-approximation-set.md) | The same relative cover over bases, with input matroid rank and fixed information dimension; deterministic FPTAS consequences under an explicit rational representation. | [Fresh review](research-20260912-represented-matroid-psd-independent-review.md), including rank preservation, contraction, exact profile interpolation and feasible recovery. Established Berstein et al. profile machinery is credited. This does not cover arbitrary independence-oracle matroids. |
| [Full-block](research-20260912-full-block-design-fptas.md), [partial-observation](research-20260912-partial-observation-memory-bound.md), and [general covariance](research-20260912-general-covariance-memory-bound.md) bounds | Uniform information control and approximation schemes under explicit fixed decay/contraction and noise promises. Full fixed observation packets allow input channel or latent dimensions in the stated results. | Separate [full-block](research-20260912-full-block-fptas-independent-review.md), [partial-observation](research-20260912-partial-observation-independent-review.md), and [covariance](research-20260912-general-covariance-memory-independent-review.md) reviews. Selecting individual channels has a reviewed hardness barrier; generic covariance constants are conservative. |
| [Exact correlated-design certificates](research-20260912-noisy-markov-certificates.md) | Rational local conditionals, integer support prices and log enclosures bound the original selected-covariance objective. Chemical D-optimal gaps below 0.001943 and four partial-observation trace gaps below 0.0604% are saved. | Independent [scalar exact review](research-20260912-noisy-exact-independent-review.md), [chemical-model review](research-20260912-noisy-markov-kinetics-independent-review.md), and [partial-trace certificate review](research-20260912-partial-trace-certificate-independent-review.md). These are local model-design cases, not measured experimental validation. |
| [All-diagonal virtual-noise comparison](research-20260912-diagonal-split-separation.md) | One exact chemical instance separates a memory upper bound from every member of the diagonal-split relaxation family by more than 0.09254 log units. | [Fresh review](research-20260912-diagonal-split-independent-review.md). The barrier concerns that family and its affine upper tangents; branching and other cuts are outside it. |
| [Robust three-scenario certificates](research-20260912-robust-design-certificates.md) | One common schedule; certified uncertainty in the individual optima used for standardization; completed dense comparison and local polishing. | Separate [solver](research-20260912-robust-solver-independent-review.md), [exact certificate](research-20260912-robust-certificate-independent-review.md), and [dense/polishing](research-20260912-robust-dense-independent-review.md) reviews. Robust scalarization and kinetic robust design have direct precedents. |
| [Latent-separator hierarchy](research-20260912-latent-separator-design.md) | Exact selected-information Schur representation; block-pattern pricing; nested anchor removal tightens the continuous mixture bound; arbitrary rational nuisance witnesses give global certificates. | Separate [proof](research-20260912-latent-separator-independent-review.md), [numerical implementation](research-20260912-latent-separator-implementation-independent-review.md) and [exact implementation](research-20260912-latent-separator-certificate-independent-review.md) reviews passed. The [priority audit](research-20260912-latent-separator-priority-audit.md) credits the existing criterion, conic formulation and mixture algorithm. Larger blocks have exponential local pattern cost. |

The [contribution map](research-20260912-contribution-map.md) explains the
relationships between these results. The earlier
[impact assessment](research-20260912-impact-assessment.md) remains a useful
historical judgment: mathematical scope, practical capability and originality
are separate questions. The requested robust-comparison and fixed-physics
followups were performed and produced mixed results.

## Practical outcomes and negative results

The robust 96-candidate design improves after completed local polishing. Its
exact standardized log gap is `0.011487999119`, with a worst D-efficiency lower
bound of approximately 97.173780% and a guaranteed fraction of the robust
optimum of approximately 99.617799%. The 48-candidate gap is
`0.008525235239`. Separate rational comparisons establish at least 3.33% and
0.80% improvement over the two saved central-scenario schedules before the
later 96-point polishing. Those comparisons do not cover all possible nominal
algorithms or all nominal-optimal schedules. Dense relaxation and polishing
costs, including incumbent generation, are retained in the
[comparison record](research-20260912-robust-dense-comparison.md).
The original consecutive first-order reaction model with unknown amplitude
also has a documented global rate-swap ambiguity. The local information
criterion and finite scenario tests do not resolve that global identifiability
issue or cover a continuous uncertainty region.

The [fixed-physical-grid experiment](research-20260912-fixed-physical-grid-benchmark.md)
keeps the physical horizon, covariance and budget of 16 observations fixed.
The calendar method's refined numerical gap is `0.005971` at 48 candidates.
At 96 candidates, a separate smaller-window diagnostic reaches `0.037097` in
about 28.05 seconds. Primary finer-grid runs complete no support price within
their budgets. Its [fresh review](research-20260912-fixed-physical-grid-independent-review.md)
reconstructs the saved prices and checks model nesting and cost accounting.
This is evidence of a scaling limitation of the current implementation, not
a theorem that high correlation requires exponential time.

The separator method gives useful strengthening at 192 candidates:

| Block size | Exact lower bound | Exact upper bound | Exact log gap | Numerical solve seconds | Certificate seconds | Accounted total including shared setup/greedy |
|---:|---:|---:|---:|---:|---:|---:|
| 12 | 14.953046919008 | 15.139311234872 | 0.186264315864 | 1.247 | 1.238 | 5.511 |
| 16 | 14.953046919008 | 15.110331327215 | 0.157284408207 | 14.409 | 20.587 | 38.023 |

The tested dense OA run returns a numerical upper bound of `15.625545906`
after its 30-second pipeline budget. The separator improves this saved bound
but still misses the target log gap of 0.01. The 16-point block's numerical
solve fits the budget; generation plus exact certification does not. At 96
candidates, the refined calendar result has a tighter upper bound than the
tested separator configurations. The
[separator certificate record](research-20260912-latent-separator-certificates.md)
preserves all five rational certificates, costs and reproduction commands.
Accounted totals sum separately recorded runs; there are no statistical runtime
or general solver-ranking claims.

Other retained negative results include the full-snapshot cases where greedy
selects the same schedule and dense bounds are tighter, nonzero mixture gaps
even with exact covariance, the near-unit-correlation failure of earlier dense
algebra, and the nonstationary counterexample to a stationary pair refinement.
They prevent the favorable examples from being presented as universal gains.

## Corrections and smaller completed findings

The investigation explicitly withdrew or narrowed claims where earlier work
or counterexamples applied:

- The noiseless selected-inverse path hull is established prior work of Lee,
  Gómez and Atamtürk. Its software application is retained without claiming a
  new hull theorem.
- A [reviewed reduction](research-20260912-scalar-gmrf-prior-reduction.md) to
  earlier Gaussian message passing makes a first scalar noisy-Markov FPTAS
  claim unsafe. The different finite-history construction remains documented.
- [Measurement-source auditing](research-20260912-measurement-source-audit.md)
  distinguishes marginal selected covariance inversion from gating a full
  inverse. Exact counterexamples and the model re-evaluation are retained;
  there is no claim of reproducing the entire published computational study.
- [Polynomial ODE support and flow prototypes](research-20260912-ode-prototype.md)
  have reviewed rational supports, propagation and polynomial tubes. Review
  corrected exact metadata arithmetic and an avoidable tube-construction
  failure. Fixed broad boxes alone do
  not give a convergent parameter-branching solver; no improvement over a
  competing dynamic global optimizer was established.
- The [storage investigation](research-20260912-energy-opportunities.md)
  retains a reviewed exact `9/8` example and a sharp balance-aware inequality.
  A proposed trajectory-hull novelty claim was rejected after prior-art checks.
- The [quadratic-conflict example](research-20260912-algorithm-opportunities.md)
  and its [review](review-20260912-quadratic-conflict-example.md) establish a
  small exact multiplier-repair example. No integrated conflict-learning solver
  or performance claim is made.

Implementation review also repaired numerical failure handling, extreme finite
scenario-weight normalization, and a false exchange-local-optimum status.
Historical artifacts are retained with their original source hashes when the
repair did not change their successful calculations. Review notes explain the
version distinction. Numerical failure statuses are not exact certificates.

## Reproduction and source access

The isolated [implementation directory](../code/research_20260912/README.md)
and its `uv.lock` record the environment. Recorded versions are Python
3.13.11, NumPy 2.5.3, SciPy 1.18.1, SymPy 1.14.0 and Gurobi 13.0.3. The
Gurobi license smoke test passed; GAMS was not needed or license-tested.
Numerical comparisons use one solver/BLAS thread. Time limits are cooperative,
and workspace estimates are not operating-system RSS limits.

Implementation and certificate notes link the relevant inputs, checkers,
outputs and reproduction commands.
The independent review scripts preserve the important boundary cases and
regressions. Rational certificates can be replayed without rerunning a
historical numerical optimization or accepting its floating-point labels.
Unchanged reviewed components were not repeatedly retested merely to increase
test counts; new integration, repairs and artifacts received targeted review.

The [literature-maintenance index](research-20260912-literature-report-index.md)
retains sequential ingestion reports and the final missing-source report.
Bibliographic entries without lawful retrieved full text remain explicitly
unretrieved and unread. Missing sources limit priority conclusions; they do
not invalidate algebra independently proved in the notes. No request for a
missing copy blocks this closeout.

## Closure boundary

The current mathematical claims, implemented prototypes, comparisons and
certificates are the scope being completed. A practically efficient general
spectral-set implementation, larger source-based robust process models, new
separator algorithms, and a production MINLP solver are further research
projects. They are not being opened under the user's final instruction.
There is no claim that all meaningful future research has been exhausted.

The [independent completion audit](research-20260912-completion-audit.md)
found no unresolved material correctness claim in its inspected scope. It
checked 39 provenance hashes and replayed all 15 represented-matroid fixtures
against their preserved deterministic counters. The separate separator reviews
then accepted the final repaired producer and all five exact certificates.
A final root documentation check found 835 resolving local links across 106
Markdown files and confirmed the final separator/scorer source hashes.
These bounded checks support the stated claims and their documented limits;
they are not a guarantee that no future review can discover an error.

The [final source-access report](research-20260912-missing-sources.md) preserves
56 packages without usable full text and three with only insufficient artifacts.
The final knowledge-base integrity check passed. Complete retained texts from
this session were read, including the final Baxter promotion; version and
possible-preview caveats remain explicit. All reported implementation defects
were resolved or the affected legacy method was explicitly excluded from
accepted numerical claims. No current research, verification or literature
task remains active.
