# Contribution map and research priorities

Date: 2026-09-12. This map distinguishes the results and their evidence limits.
The [closeout record](research-20260912-closeout.md) gives the final status
after the user requested completion of current ideas without new directions.
Independent review here means review by a separate research agent.

The work currently has two main candidates. The most general theoretical
candidate is a relative spectral approximation set for feasible matrix sums.
The strongest practical evidence concerns global certificates for discrete
measurement selection with correlated errors. They share information-matrix
optimization, but their implemented algorithms and evidence should remain
clearly distinguished.

## Relative spectral approximation sets

For fixed matrix dimension, the
[DAG theorem](research-20260912-dag-psd-approximation-set.md) produces a
polynomial-size set of feasible paths that approximates every feasible PSD
information matrix in both directions. Singular matrices retain the same
kernel. A criterion may be selected after the set is built; D-, A-, E- and
estimable-contrast guarantees follow with explicit objective comparisons.
The theorem and an exact all-basis checker passed
[fresh review](research-20260912-psd-approximation-set-independent-review.md).

The [rationally represented matroid extension](research-20260912-represented-matroid-psd-approximation-set.md)
uses established determinant-polynomial profile machinery. Its
[fresh review](research-20260912-represented-matroid-psd-independent-review.md)
passed, including exact coefficient recovery, contraction and deletion tests.
Matroid rank can grow, while information dimension is fixed.
The input representation is a substantive restriction: this is not a result
for arbitrary independence-oracle matroids.

The potential contribution is the complete integral matrix sandwich with
polynomial dependence on inverse accuracy, binary input data and exact
singular-range handling. Approximate Pareto sets, signed profile algorithms,
normalization by selected vectors, and covariance pruning are established
antecedents. The notes compare their precise guarantees. No matching complete
statement has been found in the sources inspected so far; absence from that
search is not proof of originality.

The principal limitation is practical cost. The polynomial exponent depends
on matrix dimension and the construction enumerates many bases and profiles.
Small independent checkers establish mathematical consistency, not competitive
solver performance. The practical calendar-hull solver below does not implement
this approximation-set construction.

## Correlated measurement selection and global certificates

Finite-history local Gaussian conditionals make a tractable additive
information graph. A uniform PSD error bound transfers support prices to
the true selected covariance problem. The
[full-block weighted-trace scheme](research-20260912-full-block-design-fptas.md)
allows channel and trace-weight dimensions as input; the
[general covariance version](research-20260912-general-covariance-memory-bound.md)
does not require a supplied Markov realization. The
[partial-observation version](research-20260912-partial-observation-memory-bound.md)
allows fixed packets that reveal only part of an input-sized latent state.
These results have separate independent reviews.

Classical covariance locality and filter stability account for much of the
analysis. A first scalar latent-Markov FPTAS claim is unsafe because of the
reviewed reduction to earlier Gaussian message passing. Current priority
questions concern the broader optimization scope and usable certification
combination, not the invention of filtering or sparse inverse approximation.

The practical evidence includes:

- Exact D-optimal certificates on smooth local kinetic models, with
  [four gaps below 0.001943 in log units](research-20260912-noisy-markov-kinetics-probe.md).
- An [all-diagonal virtual-noise relaxation comparison](research-20260912-diagonal-split-separation.md)
  with an exact separation of more than 0.09254 log units on one chemical
  case. Its common fractional witness survives every split and every affine
  upper tangent in that family. Branching and other cut families remain outside
  that barrier.
- [Two-mode partial-observation trace certificates](research-20260912-partial-trace-certificates.md)
  with four relative gaps below 0.0604%, in about 0.6–1.3 seconds per
  certificate. The dense numerical comparator is faster on these small cases,
  but gives wider bounds.
- [Robust three-scenario design certificates](research-20260912-robust-design-certificates.md)
  that propagate uncertainty in the individual optima used to standardize
  D-efficiency. In the original unpolished comparison, greedy/exchange wins
  one feasible-design comparison and the shared-path method wins the other;
  the latter provides the upper bound.
- A [completed dense robust comparison and polishing](research-20260912-robust-dense-comparison.md),
  with an exact standardized log gap of `0.011487999119` after polishing the
  96-candidate design. The dense relaxation converges tightly but has wider
  bounds and worse rounded-and-polished designs in these two cases.
- A [fixed-physical-grid comparison](research-20260912-fixed-physical-grid-benchmark.md)
  that exposes a limitation of calendar memory under grid refinement. With
  budget fixed at 16 observations, the numerical gap target of 0.01 is reached
  at 48 candidates but missed at 96 and 192 candidates.
- A [latent-separator hierarchy](research-20260912-latent-separator-design.md)
  that retains the original covariance and tightens as nested anchor sets are
  removed. Its [exact certificates](research-20260912-latent-separator-certificates.md)
  improve the tested 192-candidate upper bound, with a best saved log gap of
  `0.157284408207`. This is useful strengthening, but it misses the 0.01 target
  and larger blocks have exponential pattern cost.

All timings refer to the declared prototypes and inputs. Noise covariances
are stipulated, and the information criterion is local to supplied nominal
sensitivities. The original reaction example with unknown amplitude also has
a documented global rate-swap ambiguity. These limitations rule out claims
of experimental validation or general algorithmic superiority.

## Assessment at closeout

The inspected prior work does not establish the complete relative spectral-set
statement or the specific separator-removal hierarchy. That limited search
result leaves publication priority unresolved. Established normalization,
profile enumeration, Schur design criteria and complete-design mixture methods
are explicitly credited. The separator's special structure and measured bound
strengthening are the candidate contribution; its generic conic formulation
and optimization criterion are established.

The current ideas have been developed as theorems, checked examples and
reproducible prototypes. Their evidence does not establish a broadly superior
MINLP solver, a practically efficient implementation of the spectral-set
theorem, or a substantial experimentally validated process-design advance.
Those are material limits, not unfinished checks being silently treated as
success. The [independent impact assessment](research-20260912-impact-assessment.md)
records why the two main candidates should be judged separately. Its suggested
fixed-physics and stronger robust comparisons have now been performed; their
mixed outcomes are retained above.

The [research log](research-20260912-log.md) retains the full line of work,
including useful negative results and corrected claims. The
[literature report index](research-20260912-literature-report-index.md)
retains ingestion reports and unresolved-source requests. Unretrieved sources
remain bibliographic entries, not evidence of what their full text contains.
