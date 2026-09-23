# Priority audit: the March 2026 Vecchia paper and growing-rank design

Date: 2026-09-12. This bounded audit separates a newly identified paper from
the earlier thesis and reassesses the input-sized weighted-trace case. It
does not establish publication priority.

## 1. Source and strongest relevant statements

[Kaminetz and Webber, arXiv2603.05709v1](https://arxiv.org/abs/2603.05709),
*Everything is Vecchia: Unifying low-rank and sparse inverse Cholesky
approximations*, was submitted March 5, 2026. The PDF has 32 pages.
Inspected §§2–4 and Appendices A and B.1; searched the complete PDF text.
The numbering below is from the PDF; the HTML numbers theorems differently.

| PDF location | Relevant statement |
|---|---|
| Theorem 2.4, §2.2 | Partial Cholesky plus a Vecchia residual equals a Vecchia approximation with an augmented conditioning pattern. |
| Theorem 3.1, p.11 | Extends Kaporin's fixed-pattern optimality from positive definite to positive semidefinite matrices. |
| Proposition 3.2, p.12 | A normalized approximate direct solve has squared relative energy error at most `2 rank(A) log(kappa_Kap)`. |
| Propositions 3.3–3.5, pp.12–13 | Kaporin bounds for PCG and determinant estimation. |
| §4.1.1, p.14 | Defines adaptive pivot search, costing `O(r n^2)`. |
| Theorem 4.1, p.16 | Guarantees alternative pivot heuristics for distance functionals explicitly distinguished from Kaporin. |
| §4.2, pp.17–18 | Neighbor selection uses nearest-neighbor or orthogonal matching pursuit heuristics. |

No submodularity or supermodularity assertion appears in this version. The
[thesis counterexample](research-20260912-vecchia-supermodularity-independent-review.md)
therefore must not be transferred to this paper.

## 2. Implication for the present certificate

Our local regression factors belong to the established Vecchia class. Neither
their construction nor optimality within a fixed sparsity pattern should be
claimed as a contribution. Likewise, the implication from a relative precision
bound to a Fisher information bound is elementary matrix order, and the local
information graph is a standard finite-memory dynamic program.

The question left for our work is narrower: do the noisy Markov promises give
an explicit relative operator bound for a prescribed chronological-window
factor, simultaneously for every selected subset, independently of the number
of times and block dimension? Does that same window permit a polynomial-size
discrete optimization state with an accuracy guarantee for the original
covariance? I did not find those assumptions and conclusions together in the
inspected paper. This is a scoped reading conclusion. The
[earlier inverse-factor audit](research-20260912-noisy-markov-fsai-priority-audit.md)
still applies: older decay results may imply qualitative uniform convergence
through a different argument.

The distinction between global determinant metrics and a uniform relative
operator certificate is concrete. Consider `n=2m` scalar observations with
latent marginal variance one and independent observation noise variance one.
Let the latent transition be `rho` inside each consecutive pair and zero
between pairs; choose process variance `1-a_t^2`. This is an admissible model
for any fixed rational `0<rho<1`. With all observations selected,

```text
R = blockdiag( [[2,rho],[rho,2]], ..., [[2,rho],[rho,2]] ).
```

At window length zero the local approximation is `R_hat=2 I`, with precision
`Q=(1/2) I`. The eigenvalues of `R^(1/2) Q R^(1/2)=R/2` are
`1-rho/2` and `1+rho/2`, each repeated `m` times. Consequently,

```text
(1-rho/2) R^(-1) <= Q <= (1+rho/2) R^(-1),
kappa_Kap = (1-rho^2/4)^(-m),
log(kappa_Kap) = -m log(1-rho^2/4).
```

The relative precision error is exactly `rho/2`, independent of `m`, while
log Kaporin grows linearly with `m`. Substitution into the displayed
direct-solve bound gives a quantity growing quadratically with `m`. This
illustrates different metric scaling. It is not a counterexample to the
paper or a claim that sufficiently small Kaporin error cannot imply relative
precision control. Additional structure-specific estimates are needed for
the particular uniform bound used here. The
[fresh reviewer independently checked this example](research-20260912-kaporin-metric-independent-check.md).

## 3. The cleanest approximation-scheme statement

The [full-block theorem](research-20260912-full-block-design-fptas.md) permits
both block dimension `d` and parameter dimension `p` as input. Its simplest
useful specialization takes scalar observations, `d=1`, and permits the rank
of `F W F^T` to grow with the input:

```text
max_(|S|=k) tr[W (J0+F_S^T R_SS^(-1) F_S)],  W>=0.
```

Only recent selected calendar times determine the dynamic-programming state.
Local scalar regression coefficients are reused for all parameter columns.
With fixed contraction and signal-to-noise constants, the reviewed result
gives an exact-cardinality FPTAS polynomial in `p`; the exponent in accuracy
does not depend on rank.

This is a common-subset multiresponse regression objective. For the exact
algebra, take real factors `B^T B=R`, `W=C C^T`, and a response matrix `Z`
satisfying `B^T Z=F C`. Positive definiteness of `R` ensures their existence.
Then

```text
||Proj_(span B_S) Z||_F^2
 = tr[C^T F_S^T R_SS^(-1) F_S C]
 = tr[W F_S^T R_SS^(-1) F_S].
```

This is an interpretation only; the rational algorithm computes no square
roots. Separately optimizing each response would permit different subsets,
so summing those optima does not solve the common-subset problem.

The [2012 Gaussian graphical model reduction](research-20260912-scalar-gmrf-prior-reduction.md)
is strong prior for one scalar target. It does not directly settle growing
rank. The natural `p`-dimensional target hub enlarges separator precision
messages. Independent scalar copies instead require selection decisions
tied across copies. This limits that specific reduction; it is not a proof
that no other reduction or older algorithm covers the case.

## 4. Additional primary comparisons and remaining uncertainty

[Altschuler et al.2016, Theorem 1](https://proceedings.mlr.press/v48/altschuler16.pdf)
allows arbitrary response and candidate matrices. It obtains at least
`1-epsilon` of the optimum captured energy of `k` columns after choosing
`16 k/[epsilon sigma_min(OPT_k)]` columns, where `sigma_min` is the smallest
squared singular value for normalized columns. Thus its displayed guarantee
enlarges cardinality, even under favorable conditioning. The theorem, proof,
and general response-matrix formulation were checked, replacing the earlier
abstract-only reading.

[Liberty and Sviridenko2017, §5, Lemmas 14–15](https://doi.org/10.4230/LIPIcs.APPROX-RANDOM.2017.19)
also treats simultaneous multiple linear regression; its arbitrary-accuracy
guarantee increases common support size. The
[Tropp et al.2006](https://doi.org/10.1016/j.sigpro.2005.05.030)
coherence guarantees and the weak-submodular guarantees recorded in the
full-block note remain relevant competitors. These inspected results do not
give the present strict-cardinality arbitrary-accuracy statement.

[Sood and Hastie2025](https://doi.org/10.1093/jrsssb/qkaf023) establishes a
covariance/principal-variable interpretation of column subset selection and
develops covariance-input greedy and swapping algorithms. Inspected
§§1–4.1: swapping terminates at a local optimum; the main statistical theorem
concerns consistent recovery under a specified generative model. Its
supplementary special-case optimality results were not inspected. The
equivalent-objective interpretation should be credited as established; the
inspected results do not establish the temporal FPTAS.

Searches on 2026-09-12 included `Gaussian sensor selection multiresponse
regression FPTAS correlated noise bounded treewidth approximation scheme`,
`multiresponse regression subset selection approximation scheme Markov
covariance`, `multiresponse fully polynomial`, `Gaussian treewidth weighted
subset selection`, and `multiresponse Markov subset selection`, followed by
primary-source checks. Another identified method is
[Similä and Tikka2007](https://doi.org/10.1016/j.csda.2007.01.025), whose
publisher abstract describes sparsity-constrained convex cone algorithms;
its full text remains unread. Additions and available PDFs were routed to
the sole literature-maintenance agent.

This follow-up did not locate a result covering the growing-rank theorem,
but meaningful priority uncertainty remains. In particular, the older
noisy-chain observation-selection paper by Radovilsky, Shattah, and Shimony
(2006), requested in the scalar audit, remains unretrieved. Unread sources
must not be counted as excluded prior.

The best current presentation is a uniform noisy-Markov precision certificate
and an exact-cardinality trace-information approximation scheme polynomial
in parameter rank, with full blocks as an extension. Trace Fisher information
is used in the Bernal Neira coauthored
[Measure This, Not That](https://arxiv.org/abs/2406.09557), giving direct
process-design relevance. The result still needs practical evidence against
strong greedy, exchange, and mathematical-programming competitors. It does
not give an FPTAS for multi-parameter log-determinant design, trace-inverse
design, or arbitrary installation and budget constraints.
