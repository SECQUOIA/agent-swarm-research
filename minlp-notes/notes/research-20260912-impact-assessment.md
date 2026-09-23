# Research impact assessment

Date: 2026-09-12. This is a historical assessment of significance and proposed
next steps, written before the completed robust dense/polishing comparison,
fixed physical grid benchmark, and latent-separator investigation. Its
recommendations below record that earlier decision point; they are not an
active work queue. See the [contribution map](research-20260912-contribution-map.md)
for the final status. This is not another proof review or a publication-priority
certification. It uses the contribution map, reviewed spectral-set results,
covariance bounds, exact design certificates, and strongest recorded prior
audits available when written.

**The current record does not yet establish the requested substantial,
original, practical MINLP contribution.** It contains a credible mathematical
candidate and a useful implemented certification method. Either could support
a paper after its remaining decisive question is answered. They should not
be combined rhetorically to make the unimplemented theorem appear practical
or the implemented method appear novel by inheritance.

For a mathematical optimization paper, the strongest candidate is the
conditioning-free relative PSD approximation set over explicit DAGs and
rationally represented matroid bases. For a contribution closely aligned with
process and energy optimization, the more promising lead is a demonstrated
ability to certify consequential correlated-measurement decisions that
competing methods cannot certify economically. That applied claim still
needs a convincing problem and matched end-to-end evidence. The existing
small chemical examples establish neither broad superiority nor experimental
validation.

| Candidate | What is established in the repository | Assessment of paper-level value |
|---|---|---|
| Relative PSD approximation sets | Reviewed two-sided cover by actual feasible paths or matroid bases; fixed information dimension; binary rational input; polynomial inverse-accuracy dependence; singular ranges preserved | Strongest theoretical candidate. A verified improvement from a PTAS to an FPTAS for a recognized design subclass could support a specialist optimization paper. Importance beyond that remains unproved. |
| Correlated-design global certificates | Exact discrete upper and lower bounds; useful small nominal and finite-scenario gaps; separation from every diagonal virtual-noise split on one kinetic instance | Strongest practical lead. The separation demonstrates relaxation strength, while a substantive method paper still needs matched solve costs and a consequential application. |
| General covariance-decay and partial-observation bounds | Reviewed uniform information control and weighted-trace approximation schemes, with explicit promises | Useful supporting analysis and potentially useful optimization scope. Much of the analytic mechanism has direct antecedents; the generic covariance constants are currently impractical. |
| Fully observed Markov information hull, robust tangents, dense oracle and exact arithmetic | Correct applications, implementations, repairs and verification | Supporting components. Direct reductions or routine constructions rule out presenting them as separate major algorithmic inventions. |

The theoretical distinction is specific and worth testing. Brown, Laddha and
Singh already give fixed-dimensional PTAS results for several spectral design
criteria, using a guessed subset, normalization and filtering. Their inspected
matroid result uses an independence oracle and a randomized runtime with an
accuracy-dependent exponent. The candidate offers polynomial dependence on
inverse accuracy for supplied rational representations. That is a real
complexity distinction if priority survives, with a narrower representation
model. It is not an improvement over the full oracle theorem. The ordinary
D-, A- and E-design consequences are one result's consequences, not three
independent contributions. [Brown, Laddha and Singh, 2024](https://par.nsf.gov/servlets/purl/10548928),
and the [fresh matroid review](research-20260912-represented-matroid-psd-independent-review.md).

The main novelty threat is a short composition of existing tools. Berstein
et al. already compute all attainable fixed-dimensional integer profiles
over a rationally represented matroid, with polynomial dependence on maximum
integer weight, and permit arbitrary comparison-oracle objectives. Their
Theorem 1.3 and Proposition 2.2 were checked in the primary preprint for this
assessment. Consequently, enumeration of every profile and later choice of
objective are already present there. The potential new work is the reduction
from binary PSD data to bounded profiles through suitable normalization and
exact range handling. Brown's preceding normalization makes the remaining
distance smaller than a claim of a wholly new matrix-optimization paradigm
would suggest. This does not disprove originality; it identifies the actual
contribution to evaluate. [Berstein et al., primary preprint](https://optimization-online.org/wp-content/uploads/2007/07/1725.pdf).

Exact singular-range handling strengthens the theorem, but its applied
importance is not established by the current examples, which use positive
definite priors. Each feasible range is spanned by at most the fixed number
of information factors, explaining why their enumeration is possible. The
same-range cover is useful for estimability and reusable criteria, yet the
present numerical pipeline does not use it. Moreover, fixed information
dimension does not imply fixed-dimensional physics in a large energy network:
a spectral objective whose information dimension grows with network size
falls outside the favorable complexity regime. The DAG theorem also requires
an explicitly polynomial-size graph; it does not make arbitrary installation
or resource constraints cheap.

The worst-case construction is a substantial practical obstruction, not
merely missing engineering. From the DAG note's displayed state bound, the
full-rank trial contribution scales as
`M^p (N^2/eta)^(p(p+1)/2)`, suppressing dimension-dependent constants and
additional graph factors. At `p=3`, this already contains
`M^3 N^12 eta^-6`. This is a bound on the construction, not a lower bound
on all algorithms or a prediction of reachable states. It does explain why
tiny exact checkers do not justify implementing the entire theorem as the
next practical solver. [DAG construction and complexity](research-20260912-dag-psd-approximation-set.md).

The implemented certificates have more immediate value. Four local kinetic
designs have certified D-efficiency above 99.935%, and the all-diagonal-split
witness proves a relaxation gap of more than 0.09254 log units on one case.
This is stronger evidence than reporting an incompletely optimized competing
relaxation. Nevertheless, the witness excludes a specified continuous
relaxation and its affine support family, not branching or unrelated cuts.
The dense exact comparator certifies its own continuous optimum cheaply on
these small inputs. A tight root bound can improve a solver, but it does not
by itself establish the cost of reaching a requested discrete gap.
[Kinetic certificates](research-20260912-noisy-markov-kinetics-probe.md),
[all-diagonal separation](research-20260912-diagonal-split-separation.md),
and [exact dense comparison](research-20260912-exact-dense-design-certificates.md).

Three practical qualifications substantially affect the impact assessment.
First, the covariance models are stipulated. Second, trace of information
can increase while weak parameter directions remain unresolved; the existing
three-parameter reaction example also has a documented global rate-swap
ambiguity. Third, three nominal scenarios certify three scenarios, not a
continuous uncertainty region. Exact rational arithmetic certifies the
supplied decimal model; it does not remove any of these statistical limits.
The robust examples show useful protection against the saved nominal designs,
but completed exchange wins one incumbent comparison. This is compatible
with the certificate being valuable even when it does not invent a better
schedule. [Partial-trace scope](research-20260912-partial-trace-certificates.md)
and [robust results](research-20260912-robust-design-certificates.md).

There is also an application mismatch with the most direct Bernal Neira
motivation. The audited public reaction benchmark has independent time
blocks and six correlated channels per time, with partial channel and
installation decisions. Its exact marginal information can be precomputed
using at most 64 patterns per time. The temporal history method is unnecessary
for that supplied covariance, while assuming one indivisible observation
packet changes its decisions. An eventual application must justify the
temporal covariance and observation packets rather than borrow the motivating
paper's relevance without its model. This assessment does not claim that the
archived benchmark has been rerun. [Measurement model and code audit](research-20260912-measurement-source-audit.md).

A particularly informative failure test is already available. The current
48- and 96-candidate examples hold the correlation per grid step at 0.4 on
a fixed horizon, so they change the physical correlation scale. Keep instead
the same exponentially decaying latent covariance in physical time, anchored
at `rho=0.4` on the 48-point grid. On an `n`-point grid its step correlation
is `rho_n=0.4^(48/n)`. Applying the reviewed normalized partial-observation
bound with signal-to-noise ratio one gives the following approximate resource
estimates for precision error at most 0.001:

| Candidates | Step correlation | First sufficient window for that bound | Raw history masks |
|---:|---:|---:|---:|
| 48 | 0.4000000 | 8 | 256 |
| 96 | 0.6324555 | 18 | 262,144 |
| 192 | 0.7952707 | 41 | 2,199,023,255,552 |

These figures come from direct evaluation of the bound with
`gamma=rho_n`, `s=1`, and `kappa=1/2`. They are floating-point resource
estimates, not exact certificates, observed solve times, or necessary history
lengths. Better bounds, constraints or another representation may reduce
them. They expose the immediate scaling question that the fixed-step-correlation
experiments cannot answer. The more general covariance theorem is still less
practical: its own example needs windows 49, 58 and 71 for error 0.05, 0.01
and 0.001. [Normalized bound](research-20260912-partial-observation-memory-bound.md)
and [general-covariance constants](research-20260912-general-covariance-memory-bound.md).

Only two next investigations are recommended.

1. **Test whether the practical certificate remains useful on a fixed
   physical process and a consequential design decision.** Complete the
   already authorized shared-visit dense relaxation and local-polishing
   comparison. Then use one reproducible published process model, such as
   the already identified power-law kinetic model, with declared finite
   scenarios and a fixed physical covariance scale. Keep the physical sample
   budget and operational restrictions fixed when refining the candidate
   grid. A published mean model with added synthetic noise remains a modified
   benchmark; state that plainly. Compare time to the same certified gap,
   total proposal plus certificate cost, memory, true incumbent quality,
   and reference-normalization costs. Completed multistart exchange and a
   carefully solved dense common-selection relaxation are the essential
   first comparators; use an appropriate integer solver on tractable sizes
   to distinguish a stronger root bound from a faster global solve. The
   useful success is a materially tighter affordable certificate on a
   decision whose uncertainty or cost matters, not another very small gap
   at `rho=0.4`. If refinement makes histories unaffordable before useful
   resolution, record the failure and stop expanding the same benchmark
   family. The concrete research need would then be a representation or
   certificate with usable physical-memory cost, not further nominal-case
   multiplication. The [robust source audit](research-20260912-robust-scenario-design-priority-audit.md)
   supplies the process model and comparator rationale.

2. **Resolve the spectral-set result's exact priority and significance
   before extending it again.** Make one precise claim table: feasible
   family and representation, fixed versus growing dimensions, binary
   versus unary data, dependence on accuracy, singular matrices, and one
   feasible representative per target. Attempt the strongest direct
   reductions from existing profile optimization, normalization, cone-order
   approximation and spectral coreset results, including the pending Onn
   chapter. The decisive question is whether a standard existing reduction
   already yields the same FPTAS consequences on a recognizable subclass,
   such as rational partition-matroid E-design. If no such reduction applies,
   identify the exact missing step supplied here and whether the complexity
   improvement answers a recognized problem. If the result is only a short
   unrecorded composition, it may still justify a concise specialist note;
   do not call it a substantial practical MINLP advance. If the complete
   guarantee is already known, retain the proof and checker as supporting
   work and stop producing further corollaries. No new theorem family or
   additional full solver implementation is needed to answer this question.

The central prior warnings should remain visible during both investigations.
The fully observed Markov hull is a direct specialization of earlier
principal-inverse hull work; the scalar noisy-Markov existence claim has a
reviewed reduction to the 2012 Gaussian graphical-model approximation
algorithm; and covariance locality plus refitted local regressions have
direct earlier treatments. The plausible remaining optimization contribution
joins a uniform information bound to a finite discrete history model. These
reductions do not prove that combination is old, but they rule out counting
its familiar ingredients as separate innovations.
[Markov hull audit](research-20260912-markov-priority-audit.md),
[scalar prior reduction](research-20260912-scalar-gmrf-prior-reduction.md),
and [covariance-decay audit](research-20260912-covariance-decay-priority-audit.md).

For this assessment, the Berstein preprint's relevant statements were read
directly, and the Brown publisher introduction and existing primary full-text
extraction were checked. Other source-specific comparisons above rely on the
linked recorded primary audits, not a new claim of exhaustive reading. The
sole literature agent was asked for current direct-subsumption findings and
the pending Onn/cone-order comparisons. No new missing source was identified,
no literature-maintenance files were changed, and no additional paper draft
or theorem was created.
