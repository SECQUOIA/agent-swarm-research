# Publication audit: penalty encoding, calibration, and perturbation

Date: 2026-09-25. Independent audit of the publication scope and closest
antecedents of [the encoding lower bound](parametric-exploration.md),
[calibration hardness](minimum-penalty-hardness.md), and
[the rational perturbation bound](smoothed-penalty.md).
This audit does not replace the separate proof reviews or audit the
fixed-number-of-quadratics upper bound.

**Assessment:** these results can support a focused theoretical contribution
with the qualifications below. I found no source comparison or mathematical
scope issue that blocks presenting the accepted statements. This is not a
certificate of priority or an assessment that every result merits a separate
publication. The penalty-encoding boundary is the strongest organizing topic;
calibration hardness is a related computational limitation, and smoothing is
a useful companion based on classical conditioning ideas.

## Claims suitable for a potential publication

1. **A precise encoding obstruction.** A compact mixed-integer convex
   quadratically constrained model with one binary variable, a linear
   objective, one dualized scalar equality, and coefficients from a fixed
   finite set can require a sharp augmented-Lagrangian penalty with
   `2^n` ordinary binary digits. The lower bound survives optimization over
   every real multiplier and fixed additive dual-gap accuracy. Uniform
   strict native points and Slater points on equality-feasible slices do
   not prevent the obstruction.
2. **Restricted calibration inapproximability.** With a native binary box,
   a single linear objective term, one scalar equality, and a known unique
   primal optimizer, no polynomial-time algorithm can always return a
   sufficient optimized-dual penalty within any fixed polynomial factor
   of the least such penalty, unless `P = NP`. Every constructed instance
   nevertheless has the immediately available sufficient penalty one.
3. **A finite-grid companion.** For at most `K` compact convex slices with
   continuous convex objectives in a supplied interval of width `M`, the
   specified rational RHS grid gives, with probability at least
   `1-epsilon`, either infeasibility or value-exact zero-multiplier penalty
   `4 m K M / (sigma epsilon)`. Its encoding is polynomial in the supplied
   data and `log K`. A robust feasible slice removes the infeasibility
   alternative. The scalar examples show why numerical `K/epsilon`
   dependence and infinite expected numerical thresholds are possible.

The first statement is superpolynomial in the full input length and
exponential in chain length. Since the sparse input uses `O(n log n)` bits,
it must not be called an exponential lower bound in the full input length
without a different, justified encoding convention.

## Strong antecedents and what the claims add

| Primary source and inspected part | Established result and comparison |
| --- | --- |
| Gu, Ahmed, Dey, *Exact Augmented Lagrangian Duality for Mixed Integer Quadratic Programming*, [arXiv:1907.00920v1](https://arxiv.org/abs/1907.00920v1), Definition 8 and Theorem 11; retained full text inspected | Polynomial binary encoding of exact norm penalties for a rational convex quadratic objective over a rational mixed-integer polyhedron. The lower bound changes native geometry to convex quadratic constraints; it does not contradict this result or finite-penalty existence. |
| Bienstock, Del Pia, Hildebrand, *Complexity, Exactness, and Rationality in Polynomial Optimization*, [v5, Section 6](https://arxiv.org/html/2011.08347v5#S6), checked against retained PDF text | Convex repeated-squaring chains and bounded quadratic examples with tiny infeasibility and constant superoptimality are prior art. The new part is the precise multiplier-independent penalty transfer, not the small-number mechanism. The PDF labels the relevant examples 6.1 and 6.2; the HTML converter displays them as Examples 3 and 4. |
| Beck, Bienstock, Schmidt, Thürauf, *On a Computationally Ill-Behaved Bilevel Problem with a Continuous and Nonconvex Lower Level*, [open manuscript](https://optimization-online.org/wp-content/uploads/2022/02/nearly-feasible-bilevel-preprint.pdf), Section 2 and Result 4; retained text inspected | A particularly close compact convex squaring-chain example already combines Slater regularity with severe sensitivity to tiny feasibility errors. Its conclusion concerns bilevel approximate feasibility. The penalty note therefore appropriately claims a specific sharp-ALD encoding result. |
| Alessandroni, Ramos-Calderer, Roth, Traversi, Aolita, *Alleviating the quantum Big-M problem*, [arXiv:2307.10379v4](https://arxiv.org/html/2307.10379v4), Observation 1 and Section IV.1, Lemma 1, directly inspected | Optimal exact QUBO penalties and supplied-penalty recognition are already hard, including a construction with a known trivial primal optimizer. The source uses a quadratic objective, squared vector residual, and no optimized linear multiplier. The present additions are the linear-objective scalar-residual binary-box restrictions, the optimized multiplier, and the polynomial-factor barrier. |
| Mirkarimi, Hoyle, Williams, Chancellor, *Experimental demonstration of improved quantum optimization with linear Ising penalties*, [arXiv:2404.05476v2](https://arxiv.org/html/2404.05476v2), Section 2.2, directly inspected | The knapsack discussion notes that uniformly successful polynomial-time tuning of a linear penalty would imply `P = NP`. It leaves the alternative that such linear penalties do not exist for some instances. This is useful prior motivation, but not the present theorem about approximating an always-existing positive norm-ALD threshold. |
| Alessandroni et al., *Scalable Determination of Penalization Weights for Constrained Optimizations on Approximate Solvers*, [arXiv:2604.02416v1](https://arxiv.org/html/2604.02416v1), Definition 1, Theorem 2, and complexity discussion, directly inspected | This successor studies probabilistic feasibility and objective guarantees for Gibbs solvers with squared penalties. It expressly leaves hardness of its new optimal probabilistic weight unproved. Its sufficient-weight algorithm has structural assumptions and does not state the polynomial-factor optimized sharp-ALD guarantee excluded here. The earlier audit's failed retrieval is resolved by this direct inspection. |
| Dunagan, Spielman, Teng, *Smoothed Analysis of Condition Numbers and Complexity Implications for Linear Programming*, [March 2009 manuscript](https://www.cs.yale.edu/homes/spielman/Research/lpcond.pdf), Theorem 2.3.3 and Lemma 2.3.4, directly inspected | Gaussian convex-boundary tube bounds and their conditioning use are established. The finite-grid note supplies a self-contained cube proof, a rounding term, and an exact-penalty application to finite convex disjunctions. A new general smoothed-conditioning principle is not claimed. |

The QUBO comparison has a concrete mathematical basis. On its binary
constraint `x = 0`, squared violation equals `sum(x_i)`, which an unrestricted
multiplier vector can reproduce with augmentation coefficient zero. Thus
that displayed reduction does not prove positive optimized-ALD thresholds.
This observation alone is not a broad originality claim: generic reductions
may be adaptable. The restrictions and approximation guarantee are the
stronger reasons to retain the calibration result.

The cube proof, convex repair lemma, union bound, and grid coupling are
elementary established ideas. Their combination may be useful, but the
smoothed result is best presented as a quantitative companion rather than
as a separate major novelty claim. The detailed older comparisons with
convex sensitivity, exact regularization, and robust feasibility remain in
[smoothed-penalty-novelty.md](smoothed-penalty-novelty.md).

## Exactness, source interpretation, and the correction

The [December 15, 2025 Lefebvre–Schmidt manuscript](https://optimization-online.org/wp-content/uploads/2024/07/exact-penalty-for-minlp-1.pdf)
defines exactness by equality of primal value and the supremum over
multipliers. Its conclusion asks the two encoding/calibration questions.
The growing-dimension constructions answer those versions; they do not
answer a fixed-total-dimension interpretation. Theorem 14 permits infeasible
integer slices and imposes Slater only on feasible slices.

I independently checked Example 13. Put `c = lambda + rho`. For `c >= 1/2`,
its two native branches give

```
L_rho(lambda) = min(c - 3/2, -1/(4c)).
```

For fixed `rho`, this approaches zero as `lambda` tends to infinity, so
the supremum-defined dual value is zero. No finite multiplier attains it:
on the zero-binary branch, choose `x_1 = -s, x_2 = s^2` with sufficiently
small positive `s`. Also, the second displayed branch dominates only for
`c >= (3 + sqrt(5))/4`, not for every `c >= 1/2`. This corrects the example's
interpretation, without contradicting the sufficient finite-penalty theorem.

Three notions must remain distinct in every summary and theorem:

- `D_rho = v`, allowing an unattained multiplier supremum;
- existence of a finite multiplier with `L_rho(lambda) = v`;
- agreement of the entire augmented and primal minimizer sets.

The two new lower-bound constructions explicitly attain their dual
envelopes, so their lower bounds address the first notion as well as the
second. Threshold ties make the third notion stricter. The calibration
construction is finite, so its relevant dual maximum is attained too.

## Limits that materially affect publication claims

- The encoding obstruction concerns ordinary numerator/denominator binary
  output and the prescribed residual and norm. Short power expressions,
  instance-dependent fractional penalties, rescaled/reformulated models,
  and preprocessing are different questions.
- The primal lower-bound instances are easy. This is not a primal
  optimization hardness result or evidence that a solver must explicitly
  form the huge penalty.
- Calibration hardness concerns closeness to the best value. It is
  compatible with a conservative sufficient coefficient computed at once.
  The binary-box result is weak hardness; the separate unit-data result
  has hard native stable-set optimization.
- Easy linear optimization over the native box does not mean easy
  augmented absolute-residual optimization.
- The smoothed theorem concerns the perturbed instance. It neither
  preserves the original optimal integer assignment nor gives a uniform
  conditional-on-feasibility probability without an additional feasible
  mass bound. Its promises and common objective bounds are supplied,
  not efficiently recognized.
- Polynomial encoding length does not imply polynomial numerical size,
  a useful coefficient in practice, or an efficient global solution
  method. The continuous-noise infinite-expectation example makes no
  claim about a finite grid conditioned on its good event.

## Readiness and audit record

There is no need to solve the further questions in the old exploration
notes to state the accepted theorems. They must be labeled as optional
extensions, not as unfinished assumptions or promised consequences.
The more substantial upper-bound result is assessed separately; this
audit gives no substitute for checking its algebraic-complexity sources.

The local proof formulas were checked directly: the two opposite residual
witnesses cancel the multiplier; the exhibited multiplier attains the
bound; the SUBSET SUM YES/NO thresholds remain separated after accounting
for the polynomial output-instance size; the grid bad-event bound sums
to at most `epsilon`. I found no correction needed to these statements.
The Example 13 correction was independently rederived from its displayed
native constraints, rather than inferred from the previous reviews.

Targeted primary-source searches included exact/minimum/smallest penalties,
polynomial-factor penalty approximation, ALD calibration complexity,
quadratic penalty encoding, and smoothed exact penalties. Searches found
the two adjacent quantum sources above but no equivalent theorem with
the full stated restrictions. Missing search hits do not establish
novelty. This audit inspected sources and mathematical arguments; it did
not rerun numerical checkers, Lean, project-wide verification, or CI.

Publication priority remains a qualified research judgment. The viable
claim is a specific encoding boundary and restricted calibration barrier,
supported by explicit comparisons and a reproducible mathematical record.
Claims of being the first exact-penalty hardness result, inventing repeated
squaring, or establishing solver speedups should not appear.
