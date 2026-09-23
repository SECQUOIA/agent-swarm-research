# Priority audit: covariance decay, local predictors, and design approximation

Date: 2026-09-12. Status: bounded primary-source audit. The proposed
covariance-general theorem is being proved and checked separately. This note
maps its relationship to prior work and does not certify priority.

The analytical locality principle is established. The likely useful research
claim is an explicit, computable certificate joined to an exact-cardinality
approximation scheme for correlated design. Neither the population local
regression formula nor qualitative inverse-factor decay should be presented
as new.

## 1. The proposed scope and two routine reductions

There are `n` chronologically ordered observation blocks of dimension `d`.
The rational covariance satisfies

```text
R >= m I,
||R_ts||_2 <= C rho^|t-s|,              t != s,
```

for fixed positive `m,C` and fixed `0<rho<1`. The proposed bound concerns
genuine regression on the selected observations in the preceding `L` calendar
times. Its desired form is a relative precision sandwich with error
`K theta^L`, where `K` and `0<theta<1` depend only on the fixed class
parameters, not `n,d`, or the selected subset. Input-sized weighted trace
then uses the same finite-memory dynamic program as the
[reviewed noisy-Markov scheme](research-20260912-full-block-design-fptas.md).

Two observations limit possible analytical novelty. Both passed independent
checking by the covariance-bound reviewer.

**Subset uniformity.** For any selected set, replace each deleted calendar
block by an independent Gaussian block with covariance `m I`, retaining the
original indices. The padded covariance preserves coercivity and the decay
envelope. All conditional regressions at selected times are unchanged because
the dummy blocks are independent. Therefore a class-uniform full-calendar
bound transfers immediately to every subset. Reindexing by selected position
alone would change the meaning of a calendar window; dummy padding avoids
that problem.

**No diagonal upper bound.** Set `D=blockdiag(R_tt)` and
`b=2 C rho/(1-rho)`. Block row sums imply `||R-D||_2<=b`. Since `R>=m I`
and `D>=m I`,

```text
D <= (1+b/m) R,                 R <= (1+b/m) D.
```

Consequently diagonal whitening gives spectrum in
`[m/(m+b),1+b/m]` and off-diagonal block bound
`(C/m)rho^|t-s|`. Thus older two-sided conditioning hypotheses can be
recovered uniformly in proof. The rational algorithm need not whiten. Lack
of a supplied diagonal upper bound is not, by itself, a substantial
distinction from older well-conditioned covariance classes.

## 2. Direct population predictor prior

[Bickel and Levina2008](https://arxiv.org/abs/0803.1909), *Regularized
estimation of large covariance matrices*, DOI10.1214/009053607000000758,
§2.2, reprint pp.5–6, defines exactly the population approximation used
here: regress each coordinate on its nearest `k` predecessors and insert
the coefficients and residual variances into the inverse modified Cholesky
factorization. These are refitted local coefficients, not truncated full
coefficients. Section3.4, Theorem3, proves operator-norm consistency for an
estimated version under bounded eigenvalues and a uniform tail bound on
the inverse-Cholesky coefficients. Its Appendix, Eqs.A19–A20, separates
sampling and deterministic approximation terms. The stated matrix class is
scalar and assumes factor-tail decay rather than the present block covariance
envelope. This is nonetheless direct construction and population-precision
prior; adding a sampling interpretation does not make its deterministic
approximation irrelevant. The proof was inspected for scope, not independently
reproved in this audit.

[Ding and Zhou2023](https://arxiv.org/abs/2112.00693), DOI10.1214/23-AOS2288,
§2.1, Theorem2.4, compares full and finite-history population linear predictor
coefficients under uniform covariance coercivity and covariance decay.
Assumption2.2 treats polynomial decay; Remark2.3 introduces exponential
decay. Remark2.6 supplies corresponding exponential rates with finite-array
remainders. Theorem2.5 also bounds the error of an autoregressive process
approximation. These results concern general nonstationary scalar arrays;
local stationarity is required only for later specialized results. The
printed exponential rate must not be assumed to retain an arbitrary supplied
covariance rate unchanged: inverse decay can depend strongly on coercivity
and amplitude. Treating an unspecified weaker rate as part of the conclusion
is the safe comparison. This audit does not allege an error in that source.

The finite-array remainders in Ding–Zhou do not establish a substantial gap
from the desired qualitative result. For a fixed covariance, append
arbitrarily many independent dummy observations after its end. Original full
and local predictors stay identical as the array length grows. If the source
constants are uniform over the fixed covariance class, such padding removes
array-length remainders. Geometric coefficient bounds can then be combined
with row and column estimates to control the population precision factor.
This is an inference about applying established arguments, not a completed
black-box derivation of our explicit constants. The precise uniform dependence
of constants and the passage to block operator norms still need to be checked.

[Inoue, Kasahara, and Pourahmadi2018](https://doi.org/10.3150/16-BEJ897),
*Baxter's inequality for finite predictor coefficients of multivariate
long-memory stationary processes*, gives matrix-valued predictor
representations in Theorems5.2–5.4. Theorem6.9, pp.1228–1229, gives an
operator-norm sum inequality for finite versus infinite predictor coefficients
of stationary vector FARIMA models with a common fractional order. Its
introduction traces the short-memory vector predecessor to
[Cheng and Pourahmadi1993](https://doi.org/10.1007/BF01197341). The latter's
publisher abstract was read, but full text remains unretrieved. These sources
make multivariate finite-predictor convergence established prior. Their
inspected statements do not provide the present arbitrary nonstationary
covariance-class constants independent of input block dimension.

## 3. Inverse-factor locality remains strong prior

The [earlier inverse-factor audit](research-20260912-noisy-markov-fsai-priority-audit.md)
already covers Jaffard, Benzi–Tuma, and related decay-algebra results.
The supplied [Benzi–Boito–Razouk2010 technical report](https://www.cs.emory.edu/technical-reports/techrep-00207.pdf),
*Decay properties of spectral projectors with applications to electronic structure*, §6,
pp.17–19, is especially explicit: uniformly conditioned banded positive
definite matrices have uniformly exponentially decaying inverse Cholesky
factors, permitting norm approximation with bandwidth independent of matrix
size. The discussion says exponential covariance decay can replace exact
bandedness. This statement is about inverse factors and their truncations;
the comparison with refitted local coefficients still requires a projection
or perturbation argument. It strongly discourages claiming qualitative
size-independent inverse-factor localization as new.

[Benzi and Boito2014](https://people.cs.dm.unipi.it/boito/bb13.pdf),
DOI10.1016/j.laa.2013.11.027, §5, Theorems6–7 and Remark5, extends
analytic-function decay to matrices whose entries belong to a C*-algebra.
Its explicit spectral-interval, function, and bandwidth parameters control
operator-norm decay of the entries. Taking the algebra to be matrix blocks
shows that dimension-free block inverse decay is also established prior for
banded matrices. The bounds and their derivation were read in the published
author PDF; the absence of a block-dimension factor is apparent in the
functional-calculus argument. The source does not by those statements
identify the refitted finite-calendar factor for the present dense covariance
envelope. Nonetheless, merely replacing scalar absolute values by block
operator norms should not be claimed as a new locality principle.

Combining this locality theory with the genuine population construction in
§2 makes the scalar precision bound close to a standard consequence. A
self-contained proof with rationally usable constants and dimension-free
block norms can still be useful, particularly for certifying an optimization
result, but should be described as an explicit specialization and extension
unless a substantive missing theorem is demonstrated.

## 4. Closest discrete optimization results

[Das and Kempe2008](https://david-kempe.com/publications/regression.pdf)
is the closest approximation-scheme prior. Theorem4.1, §4, gives an FPTAS for
fixed covariance bandwidth, with displayed runtime containing
`(k/epsilon)^(beta^2)`. Corollary4.2 adds an entrywise covariance perturbation
bound with loss proportional to `k` times the perturbation. Their §7 exact
algorithm assumes the identity `R_ij=a^|y_i-y_j|`, not a general exponential
upper bound. The conclusion explicitly leaves multiple prediction targets
and broader dependence structures for future work. These statements were
checked in the primary paper again for this audit.

For a general exponential envelope, applying the printed Corollary4.2 with
entrywise threshold of order `epsilon/k` makes `beta` of order
`log(k/epsilon)`. Substituting into the displayed runtime does not give an
FPTAS. A stronger elementary operator-norm tail estimate can remove the `k`
dependence in the bandwidth choice: the row tail is at most
`2 C rho^(beta+1)/(1-rho)`, independent of matrix size. With fixed coercivity,
this permits `beta=O(log(1/epsilon))`. But their continuous-message rounding
still has an exponent depending on `beta`, so this improved route gives at
most a PTAS from the displayed bound, not an FPTAS. This is our inference
from their algorithm, not a claim made by that paper.

The candidate distinction is optimizing an additive local-information
surrogate with `2^L` discrete history states, rather than rounding a
continuous boundary covariance/response state of dimension depending on
bandwidth. Provided the uniform geometric error is proved with fixed class
constants, `L=O(log(1/epsilon))` yields polynomial dependence on accuracy.
The transition from analytic locality to this finite discrete state is the
plausible new algorithmic combination.

An older direct objective match is
[Sestok2003, MIT PhD thesis](https://dsp-group.mit.edu/wp-content/uploads/2024/11/CSestokThesis.pdf),
*Data Selection in Binary Hypothesis Testing*. Chapter2 maximizes
`s_S^T R_SS^(-1)s_S`. Section2.5 gives an exact interval-fragment algorithm
for tridiagonal covariance: §2.5.5 reports `O(N^3)` optimization after
`O(N^5)` naive fragment evaluation. Section2.5.6 treats larger bandwidth,
but requires the best fragment for every length, count, and start. It reports
polynomial post-initialization optimization and only a lower bound on
initialization cost. No polynomial upper bound for finding all those best
fragments was located. Therefore the reported post-initialization runtime
must not be treated as a complete polynomial algorithm for general bandwidth.

Two later primary checks did not resolve the general case:

- [Qian et al.2015, Definition4 and Theorem2](https://papers.neurips.cc/paper_files/paper/2015/file/b4d168b48157c623fbd095b4a565b5bb-Paper.pdf)
  retains the exact exponential-line covariance identity. Its randomized
  optimization result does not by that statement cover an exponential envelope.
- [Dutta, Wilde, and Smith2022](https://arxiv.org/abs/2203.16070), §III,
  Eqs.12–13, uses the same summed explained-information objective with
  squared-exponential covariance plus a nugget. It proposes centroid-greedy
  spatial selection. Propositions1–4 concern special geometry, cost, and
  marginal evaluation; no arbitrary-accuracy global guarantee was located.
  This is a useful comparator for the general-covariance application.

The [2012 Gaussian graphical model reduction](research-20260912-scalar-gmrf-prior-reduction.md)
continues to cover the earlier scalar latent-Markov model. It does not
dispose of the present scalar dense-covariance case: no bounded-width Gaussian
realization is supplied or guaranteed. Arbitrarily factorizing a covariance
creates a model whose graph width may grow with the input. Thus even `d=p=1`
remains an algorithmic candidate for the broader class; growing rank and
block dimension are further scope distinctions.

## 5. Assessment and search record

The proposed covariance-class extension is potentially more useful than a
full-state observation restriction. Fixed partial observations of a stable
latent process can satisfy an observation-covariance decay envelope when
observation maps and latent marginal covariance are bounded and nugget
covariance has a positive lower bound. A selected observation packet must
still be acquired as a whole. This motivation is not a claim that arbitrary
partial-sensor choices or parameter-dependent covariance are covered.

The literature found here does not disprove the proposed FPTAS combination.
It does substantially reduce the novelty that should be assigned to the
analytic bound alone. Publication claims should lead with the discrete
optimization capability, state fixed class parameters explicitly, credit
population Cholesky regression and matrix decay, and retain uncertainty
until both the proof and practical value are established.

Searches on 2026-09-12 included `subset selection covariance decay algorithm`,
`sensor selection exponentially decaying`, `regression approximation scheme
banded`, `selection FPTAS Gaussian`, `banded Cholesky approximation exponential
covariance operator norm`, and source-title/reference searches for Baxter
and Bickel–Levina. Primary mathematical sections are identified above.
Additional inspected sources include
[Qian, Bian, and Feng2020, Theorem1](https://doi.org/10.1609/aaai.v34i03.5621),
which gives a weak-submodular constant-factor guarantee, and the author
abstract of [Wu and Pourahmadi2003](https://www.stat.uchicago.edu/~wbwu/papers/May19.pdf),
a direct predecessor of the sequential covariance-regression construction.
New sources and available PDFs were sent to the sole literature-maintenance
agent. No local knowledge-base entries were edited by this audit.

Unretrieved Cheng–Pourahmadi1993 and the previously requested noisy-chain
observation-selection work by Radovilsky, Shattah, and Shimony2006 remain
unread. They are not excluded prior. No exhaustive absence claim is made.
