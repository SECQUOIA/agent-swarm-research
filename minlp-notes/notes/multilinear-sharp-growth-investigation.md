# Sharp growth investigation for positive multilinear gaps

Date: 2026-09-04.

## Outcome

The maximum-degree and dimension-dependent worst ratios both have sharp asymptotic growth, including leading constant one:

```
R(d) ~ ln d/ln ln d,
C(n) ~ ln n/ln ln n.
```

The full new theorem is in [positive-multilinear-sharp-degree-growth.md](../results/positive-multilinear-sharp-degree-growth.md). Two independent reviewers checked the complete written proof, degree/dimension interpolation, and extension to the original term-by-term relaxation on finite nonnegative boxes. Novelty screening is separate.

## Search direction and why the upper bound was decisive

The initial lower-bound idea was to vary the dyadic anchor probabilities, block sizes, and weights. In the shared-failure-count surrogate, a level with anchor probability 1/b and normalized weight alpha contributes alpha A min(b,R), with E A=1/b and E R=1. Geometric scales with uniform level weights give a hull gap of order log(number of levels). Faster scale growth might reduce this hull gap but also raises the largest degree. No stronger lower-bound theorem was obtained from that route.

The existing universal O(log d) proof mixed O(log d) conditional-failure distributions, each selecting one scale. I instead considered a single conditional profile containing a continuum of scales:

```
q_p(t)=min(1,p/t)/(1+ln min(M,1/p)),
0<t<=min(Mp,1),
```

with q=0 outside its support and M>=d. The 1/t profile distributes one coordinate's failure mass across scales while retaining the exact marginal p. This captures a logarithmic interval for every hard monomial rather than assigning each monomial only one scale.

## Main estimate

For a monomial with one low-probability anchor u, let S be the sum of the other variables' failure probabilities and T=min(u,S). If its largest failure probability is large, a simple threshold coupling supplies the required deficiency. Otherwise, on a suitable interval of t, every failure probability is less than t. Excluding coordinates with p<t/M loses total mass at most (d-1)t/M<=t. The remaining failure mass is therefore almost T, and the harmonic profile gives a sum of conditional failure probabilities proportional to T/(t ln d).

Integration over an interval with logarithmic length asymptotic to ln ln d gives deficiency asymptotic to T ln ln d/ln d. Conditional independence converts the sum of small failure probabilities into an almost equal union probability. The construction is shared by all monomials and preserves every coordinate mean.

The first proof used a fixed conservative constant, yielding ratio at most 24L/[(1-exp(-1))ln L]. The multilinear agent then supplied the leading-constant refinement: use an interval from T/a to beta T with a=L/(ln L)^2 and beta=1/ln L, and mix the harmonic, threshold, and independent distributions with weights proportional to their reciprocal guarantee coefficients. I independently checked this refinement and incorporated it. Two reviewers then checked the full text.

## Consequences for abandoned lower-bound searches

The universal upper bound rules out an Omega(log d) counterexample and any improvement over the dyadic lower family's asymptotic leading constant one. Changing the scale base, monomial weights, or overlapping block design can still improve finite-degree values or lower-order terms, but cannot improve the asymptotic leading order or leading constant.

The result does not determine the exact finite-degree function R(d), its second-order asymptotics, or the optimal distribution achieving the hull gap for general positive multilinear polynomials. Those remain meaningful follow-up directions. Likewise, sign-changing boxes or coefficients fall outside the positive expansion and deficiency argument.

## Verification record and literature relation

The existing lower construction is separately audited in the positive-multilinear result and its two review files. The new upper proof passed full written reviews by the packing-audit and scaling-characterization agents; [the second review](review-positive-multilinear-sharp-upper-second.md) records the complete checks. The preceding O(log d) result contains the independently checked positive-box expansion comparison.

The primary conjecture source is [Luedtke, Namazifar, and Linderoth's open technical report](https://jlinderoth.github.io/papers/Luedtke-Namazifar-Linderoth-12-TR.pdf), p.22. The sharp growth theorem is stronger than merely refuting its constant-ratio conjecture: it identifies precisely how the worst ratio grows. A dedicated equivalent-problem novelty screen is being recorded in notes/positive-multilinear-degree-novelty.md. The conditional rounding mechanism may have precedents in correlation-gap or random-scale literature; the novelty claim should concern the specific relaxation-gap theorem unless that broader mechanism is independently established as new.
