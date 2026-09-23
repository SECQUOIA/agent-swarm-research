# Priority audit: robust discrete sampling with correlated errors

Date: 2026-09-12. This is a bounded source audit, not a novelty certification.
It accompanies [the shared-schedule certificate draft](research-20260912-robust-design-certificates.md).
The existing measurement source audit and exact dense certificate note were
checked first. No production code, certificate derivation or knowledge-base entry
was changed in this audit.

Robust nonlinear experimental design, maximin D-optimal sampling, uncertainty in
observation correlation, scenario generation, and conic or tangent support bounds
all have close antecedents. The useful question for this project is whether its
finite-history representation produces materially tighter, independently checked
global bounds for actual discrete schedules. A contribution should be framed
around that demonstrated capability and its scope, rather than around the
scenario epigraph or the robust-design application alone.

## Direct antecedents and their limits

**Duarte, Sagnol and Wong (2018)** is the closest conic optimization and chemical
kinetics predecessor. Their method uses a finite parameter-scenario master SDP
and nonlinear worst-parameter search, with delayed constraint generation and
efficiency bounds. It optimizes approximate-design weights on a discretized
design domain. Section 4.3 gives consecutive power-law reactions, observes the
intermediate species, and provides the following model:

```text
A' = -pi1 A^alpha1
B' =  pi1 A^alpha1 - pi2 B^alpha2
C' =  pi2 B^alpha2
(A(0),B(0),C(0)) = (1,0,0),  t in [0,20]
(pi1,pi2,alpha1,alpha2) in [0.5,1] x [0.1,0.5] x [1,2] x [1,2].
```

Their initial parameter pool contains the 16 corners, 32 random edge points and
two random interior points. The inspected text does not give those random seeds.
All corners therefore provide a reproducible, literature-motivated finite test;
adding AR-plus-nugget observation noise changes the benchmark. Although the
source calls the vessel a CSTR, the displayed equations have no feed/dilution
terms. Read scope: publisher sections and author-uploaded manuscript, especially
Algorithm 1 and equations (26)–(27); no complete PDF was retrieved here.
[Paper](https://doi.org/10.1016/j.csda.2017.09.008),
[author-uploaded text](https://www.researchgate.net/publication/320600207_An_algorithm_based_on_semidefinite_programming_for_finding_minimax_optimal_designs).

Its 2015 conference predecessor by **Duarte, Sagnol and Oliveira** already gives
robust minimax SDP formulations for dynamic-model parametrization and a two-step
reaction example. The primary author page and author-uploaded abstract/formulation
were inspected. This makes a claim of first robust conic design for consecutive
kinetics untenable.
[Paper and author repository](https://www.zib.de/userpage/sagnol/publication/dso15_escape/).

**Wang and Yue (2020)** directly studies discrete robust sampling of an enzyme
reaction system. Section 2 assumes independent, identically distributed Gaussian
measurement errors. Section 4.1 calls its D-design algorithm Powell's method,
but describes repeated one-for-one replacement of selected times, from several
random initial selections. A completed multistart exchange search is consequently
a close operational baseline. Its SDP treatment is for E-optimality under its
stated information-perturbation assumptions; it is not a global certificate for
the discrete D-design problem.

Section 5 selects 21 of 201 times `0:30:6000` seconds, jointly measuring five
outputs. Three uncertain rates have nominal values `(100,200,5000)` and bounds
`(50,100,2500)` to `(200,400,7500)`. Shared Latin-hypercube draws are used, without
a reproducible seed in the inspected paper. The ten-state model and nominal data
are supplied in Yue, Halling and Yu (2013), Appendix A. Those equations were
retrieved, so the case is reproducible with newly declared scenarios. All six
pages of the 2020 article were inspected, concentrating on Sections 2–5.
[2020 paper](https://strathprints.strath.ac.uk/73195/),
[2013 model PDF](https://skoge.folk.ntnu.no/prost/proceedings/dycops2013-and-cab2013/media/CAB/files/0034.pdf).

**Wang and Yue (2026)** is a distinct, newer preprint, not the 2020 paper. It
compares maximin and pseudo-Bayesian sampling for an enzyme network and enzymatic
biodiesel production, reporting distributions of D-performance. Only its primary
SSRN abstract and metadata were retrieved; its full text remains unread after a
403 response. It is a material unresolved source for a publication-level audit.
[Preprint, posted 28 March 2026](https://doi.org/10.2139/ssrn.6484802).

**Chowdhary, Attia and Alexanderian**, arXiv 2409.09137v2, is the strongest recent
binary robust correlated-design antecedent inspected. Problem 3 and Algorithm
3.1 impose an exact sensor-count budget using conditional Bernoulli policies.
The outer policy update uses an expanding uncertainty pool; an inner nonlinear
optimization supplies new adverse parameters. Section 3.3 explicitly allows a
general utility. Section 4.2 has 64 candidate sensors, budget eight, uncertain
variances and exponential spatial error correlation. Their nonlinear Bayesian
PDE utility uses low-rank, fixed-MAP approximations to expected information gain.
Projected-gradient or iteration stopping and sampled final designs do not give
the discrete global upper certificate sought here. Read scope: Sections 2.2,
3.1, 3.3, 4 and conclusion; the approximation derivation was not independently
verified.
[Preprint](https://arxiv.org/abs/2409.09137v2),
[related journal article](https://doi.org/10.1137/24M1693921).

Their precursor **Attia, Leyffer and Munson** treats robust A-optimal Bayesian
design and uncertainty in inverse-problem elements. It already compares
relaxation and probabilistic formulations. Their criticism of replacing a binary
optimizer by a continuous optimizer does not invalidate a valid relaxation used
only as an upper bound, with an independently evaluated feasible schedule.
[Preprint](https://arxiv.org/abs/2305.03855),
[2025 journal DOI](https://doi.org/10.1137/24M1667543).

**Burclová and Pázman (2015)** provides a particularly direct support-bound
antecedent. Theorem 1 and Section 3.1 express design criteria through affine
supports, solve finite cutting-plane LPs and stop using upper/lower bounds.
Section 3.2 handles maximin efficiencies with separately computed criterion
optima. Replacing point information matrices by whole-schedule information
matrices gives the same abstract approximate-design master problem. Pricing
whole schedules efficiently and controlling correlated-information approximation
are the additional tasks in this repository. Neither arbitrary SPD tangent
references nor combining robust efficiency constraints is new by itself.
[Primary full text](https://arxiv.org/abs/1504.06226).

**Maus et al. (2010)** combines A/D-optimal temporal experimental design with
uncertain AR(1) error correlation. Equations (11)–(12) define relative-efficiency
maximin design. Their numerical search selects among designs generated at 51
correlation values using a genetic algorithm; it does not exhaust all feasible
stimulus sequences. The experiment controls stimulus timing, rather than
selecting observations of a fixed kinetic trajectory, but directly precedes
robust temporal D-design under correlation uncertainty. Read scope: methods,
equations (11)–(12), numerical search setup and discussion.
[Author-repository PDF](https://orbi.uliege.be/bitstream/2268/113212/1/maus,NIMG2010.pdf).

**Watson and Pan (2023)** compares local, greedy and reverse-greedy searches for
correlated experimental units, including spatial and longitudinal examples.
Section 5 considers a weighted average over model specifications and explicitly
excludes minimax from its supermodularity argument. This supplies practical
exchange/deletion baselines, not a maximin D-optimality guarantee. No asserted
supermodularity property from that paper is used in this project; arbitrary
correlated D-information and its scenario minimum need separate analysis.
[Primary full text, Section 5](https://doi.org/10.1007/s11222-023-10280-w).

Older direct sources remain important: **Pronzato and Walter (1988)** formulates
robust nonlinear experiment design by maximin optimization; **Asprey and
Macchietto (2002)** applies robust expected-value and maximin criteria to dynamic
process experiments, including sampling decisions and a bioreactor. Primary
abstracts/introduction were inspected, but complete articles remain unretrieved.
**Bischoff (1996)** studies maximin D-efficiency over covariance classes, including
tridiagonal covariance. Its bibliographic record/abstract was found, not its
full text. These sources must be credited without suggesting they were fully read.
[Pronzato–Walter](https://doi.org/10.1016/0025-5564(88)90097-1),
[Asprey–Macchietto](https://doi.org/10.1016/S0959-1524(01)00020-8),
[Bischoff institutional record](https://publikationen.bibliothek.kit.edu/206496).

## Recommended matched comparison

The primary bound comparison should use the **dense correlated-information
relaxation with a common selection vector and one epigraph constraint per
scenario**. It solves the same finite-scenario criterion and preserves the
same cardinality restriction. Its continuous optimum is an upper bound; rounding
and completed exchanges provide separate feasible lower bounds. Numerical solver
status must not replace independent evaluation of either bound. The Liu split
parameter should be strengthened or varied as in the existing single-scenario
comparison, rather than chosen to weaken this competitor.

For feasible schedules, retain completed multistart exchange, greedy followed by
exchange, reverse deletion followed by exchange, and the best nominal-scenario
schedule. Report the score in every scenario. A uniform schedule is useful
context but is insufficient as the main optimization comparator.

A bounded additional published heuristic is **conditional-Bernoulli REINFORCE**.
For a fixed scenario list, supply the scalar black-box utility

```text
h(S) = min_s [log det J_s(S) - c_s].
```

Then the general budget optimizer needs no derivative of the kinetics, design
or uncertain parameter. It evaluates `h` on exact-cardinality samples; the outer
uncertainty-generation loop of the robust PDE algorithm is unnecessary. The
latest inspected budget paper is **arXiv 2406.05830v2, 29 June 2026**, not merely
the original 2024 submission. Algorithm 3 uses conditional sampling and policy
gradients. Remark 4.4 explicitly limits its convergence interpretation to
stationary/local solutions. Its Section 5 configuration uses 100 gradient
samples, learning rate 0.5, up to 500 iterations, 100 final samples and a
per-component baseline. A time/function-evaluation matched comparison should use
multiple seeds and preserve the best feasible point throughout the run.
[Primary paper](https://arxiv.org/abs/2406.05830v2).

The exposed PyOED implementation has a generic
`ConstrainedBinaryReinforceOptimizer`, accepting `fun`, `size`, `budgets=[k]`
and a random seed. Its documented source imports generic optimization and
probability modules; installation/import dependencies were not tested here.
The inspected `Bernoulli_random_sampler` property selects its conditional
sampler for the exact option `sum-as-variable`. Some prose instead says
`sum-as-random-variable`; do not substitute that spelling without checking the
installed revision. Assert sample cardinality. The exposed older implementation
also uses a scalar baseline, with nonnegative clipping, rather than the newest
paper's per-component baseline. These differences require versioned reporting.
[API](https://web.cels.anl.gov/~aattia/pyoed/pyoed.optimization.binary_optimization.constrained_binary_optimization.html),
[inspected source](https://web.cels.anl.gov/~aattia/pyoed/_modules/pyoed/optimization/binary_optimization/constrained_binary_optimization.html).

No PyOED experiment was run by this audit. If implementation effort is limited,
the dense epigraph plus completed exchange is the more informative next
comparison for a claim about certified bounds. A new independent implementation
of the probabilistic algorithm should be described as an adaptation, not as a
reproduction of the upstream package or its latest numerical study.

## Raw and standardized objectives

For common parameter dimension `p`, distinguish

```text
raw(S) = min_s log det J_s(S)
standardized(S) = min_s (log det J_s(S) - b_s*) / p,
b_s* = max_feasible_T log det J_s(T).
```

Exponentiating the standardized score gives worst-scenario D-efficiency.
Raw maximin is a legitimate specified utility, but can emphasize scenarios
whose achievable information is intrinsically smaller. Scenario-dependent
parameter coordinate changes can add different log-determinant constants.
Standardization cancels these constants when all information and priors are
transformed consistently. A common fixed nonsingular linear parameter change
already preserves the raw criterion's optimal schedules.

For certified references `ell_s <= b_s* <= u_s`, subtract `u_s` in the
incumbent lower bound and `ell_s` in a global upper bound. This is ordinary
interval propagation, not a separate claimed innovation. Count reference solves
and their uncertainty in the total cost and final gap. Do not silently replace
`b_s*` by a locally optimized nominal design.

For pseudo-Bayesian comparisons, specify the function being averaged.
`mean(log det J_s)`, `log det(mean J_s)` and
`mean(det(J_s)^(-1))` are different criteria. Their scenario averaging cannot be
interchanged by applying the monotonicity of the logarithm. This matters when
adapting process-design implementations that use different D-criterion scales.

## Search record and unresolved sources

Searches on 2026-09-12 covered robust/maximin experimental design with correlated
errors, sampling-time design for uncertain dynamic systems, robust D-optimal
cutting-plane/SDP formulations, standardized maximin efficiencies, and public
PyOED budget optimization. Representative queries included:

```text
"robust" "D-optimal" "correlated" "cutting"
"robust optimal experimental design" "correlated" "mixed integer"
"Robust sampling time designs for parametric uncertain systems"
"An algorithm based on semidefinite programming for finding minimax optimal designs"
"On maximin designs for correlated observations" pdf
PyOED conditional Bernoulli robust design budget constraints
```

Primary full texts inspected locally were Wang–Yue2020, Yue–Halling–Yu2013,
Burclová–Pázman2015, Chowdhary et al.2409.09137v2, Attia et al.2305.03855,
Attia2406.05830v2 and Maus et al.2010. Watson–Pan2023 was inspected in publisher
HTML. Focused reading scope is recorded above. Downloads used the authorized
literature helper; PDFs and extracted text are retained under
`/tmp/research-20260912-*.pdf` and matching `.txt` paths, and were submitted to
the sole literature-maintenance agent for durable ingestion.

Further relevant entries were routed to that agent: Körkel et al.2004
(10.1080/10556780410001683078); Attia–Constantinescu2022 correlated-observation
OED (10.1137/21M1418666, arXiv2007.14476); Attia–Leyffer–Munson2022 stochastic
binary design (10.1137/21M1404363); the PyOED software paper
(10.1145/3653071, arXiv2301.08336); Attia2026 trajectory-policy design
(arXiv2601.11473); Aarset2025 global sensor-placement conditions
(10.1088/1361-6420/add9bf, arXiv2410.16590); Hui Yu's 2018 biochemical OED
thesis; and Das et al.2015/Das–Lin2011 invariant robust correlated designs.
These are leads/adjacent antecedents unless a reading scope is stated above.

Existing KB entries for Patan–Bogacka2007, Uciński–Atkinson2004 and the 2026
correlated-design review still lack full text; this audit found no new lawful
download for them. Their unresolved status, together with Wang–Yue2026 and
the unretrieved older robust articles, prevents a categorical absence-of-prior
claim. No missing-source request was sent to the user, and no author was contacted.

The source audit supports a practical certified-computation investigation. It
does not establish a new robust-design principle, a continuous-uncertainty
guarantee, or a computational improvement before matched experiments are run.
