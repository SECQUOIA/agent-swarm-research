# Pooling hardness with positive strict-quality tolerance

Date: 2026-09-05. Status: PASS in the [second independent audit](review-pooling-all-degrees-two-second.md).

This note extends [the all-degree-two result](../results/pooling-all-degrees-two.md).
It uses its notation and source approximation gap.

## Robustness extension


The zero strict-quality bound is convenient for exact identities but is not
essential for hardness. For the unit-capacity construction above, replace
every strict bound by `δ>0`, leaving other data unchanged. Write `P_δ*` for
its maximum profit. For any `η>0`, every feasible solution can be converted
in polynomial time into a feasible zero-bound solution with profit at least

```
P - 2n(η + δ/η).
```

Indeed, at a pool with quality `p_v≤η`, keep only a clean-to-strict flow of
`min(a_v,s_v)` and set its quality to zero. All arc flows decrease, and lost
profit is
`s_v+d_v-min(a_v,s_v)≤2d_v=2p_v t_v≤2η`.
At a pool with `p_v>η`, keep only dirty-to-lax flow `min(d_v,b_v)`, setting
quality one. Again all arc flows decrease. Since
`d_v-b_v=s_v-a_v≤s_v`, lost profit is at most `2s_v`.
Summing the strict quality constraints gives
`Σ_v p_v s_v≤δ Σ_v s_v≤δ n`. Therefore
`Σ_{p_v>η}s_v≤δ n/η`. Adding the two losses proves the claim; newly kept
strict flows all have quality zero and kept lax flows all have quality one,
so output feasibility is explicit. Empty pools can be assigned any bounded
quality and do not affect the proof.

In particular for rational `η` and `δ=η²`,

```
P_0* ≤ P_δ* ≤ P_0* + 4ηn.
```

Let `γ>0` be a fixed approximation-gap constant for the three-edge-colored
cubic independent-set source: no polynomial algorithm always obtains an
independent set of size at least `(1-γ)α(G)`, unless P=NP. Choose a fixed
positive rational `η<γ/32`, and put `δ=η²`. Suppose the positive-tolerance
pooling family had a PTAS. Use it with a fixed `ε<γ/6`. Starting from its
profit `P≥(1-ε)P_δ*≥(1-ε)P_0*`, apply the cleanup just proved, integral
replacement, and independent-set recovery. The resulting independent set
has size at least

```
P - 4ηn - n/2
≥ α(G) - εP_0* - 4ηn
≥ (1 - 3ε - 16η) α(G)
> (1-γ) α(G).
```

Here `P_0*≤3α(G)` and `n≤4α(G)` are the bounds already proved. This
contradicts the source gap. Thus there is a fixed rational strictly positive
tolerance `δ` for which this all-degree-two, unit-capacity pooling family
has no PTAS, and exact optimization is strongly NP-hard (all numerical data
are fixed rational constants). The exact integer optimum identity is only
asserted for `δ=0`; the positive-tolerance result uses approximation gaps.

Adding one to all input qualities and output bounds preserves feasible
flows by mass balance. The robustness result can therefore use input
qualities `{1,2}` and output bounds `{1+δ,2}`, so no zero quality value or
zero product specification is needed. This is an affine normalization,
not an additional reduction gadget.
