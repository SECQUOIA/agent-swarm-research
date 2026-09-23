# Investigation: unconditional conic complexity of a pooling rank-one hull

Date: 2026-09-04. This lane sought a stronger structural result than the existing conditional constructible-hull lower bound for two-sided rank-one constraints.

## Preserved result

The complete candidate and proof are in [the correlation-face result](../results/rank-one-correlation-face-conic-lower-bounds.md). For `K_n=conv{W>=0: rank(W)<=1, We<=e, W^Te<=e}`, the three equations

```
trace(W)=1,
sum_i W_(i,m+i)=0,
sum_ij W_ij=m
```

select a face of `K_(2m)` affinely isomorphic to `COR(m)`.

The central observation is that trace equality forces every generating matrix to be a normalized binary outer product. Paired entry zeros restrict the support to at most one index per pair; total mass then forces one per pair. The explicit affine inverse permits direct transfer of all cone lift lower bounds. The transferred results are established theorems, not new extension-complexity proofs:

- Fawzi–Parrilo, arXiv:1311.2571, Theorem 1 on PDF p.3: exponentially many blocks of fixed PSD order; for order two, `(9/7)^(m/2)/sqrt(7)` blocks.
- Lee–Raghavendra–Steurer, author manuscript `https://www.dsteurer.org/paper/sdpsize.pdf`, Theorems 1.1 and 5.4, PDF pp.5 and 34: unrestricted PSD order at least `2^(Omega(m^(2/13)))`.

Sources were opened and theorem statements checked. The result file records all metric and novelty limitations. The full written embedding and source transfers passed the [independent conic-lift audit](review-rank-one-extension.md). Later stability and approximate-hull reviews are linked below.

## Why this direction is useful

The family has zero lower bounds and uniform unit upper bounds. Thus the obstruction needs neither forced positive flows nor large numbers. Conic extension lower bounds are unconditional and nonuniform: they exclude small exact lifts even when coefficients are arbitrary reals and no efficient construction is requested. This is materially stronger than deriving an efficient-construction barrier from NP-hardness.

A finite LP extension-complexity lower bound alone would not be useful because `K_2` is already nonpolyhedral; the proof of that caveat is included in the result. The finite conic representation size is the meaningful target.

## Broader directions considered

The repository's open-problem map contains certification under singular equalities, network/simplex product hulls, sparse multilinear hierarchies, and switching control discrepancy. This lane chose conic complexity because the two-sided rank-one reduction already supplied a clean PSE block, but its conditional result left a nonuniform loophole. The correlation-polytope face closes that loophole for SDP and SOCP formulations.

An approximate-hull lower bound does not follow automatically. In particular, restricting an approximate outer set to an affine face can admit points that are far from the exact face, and exact-size lower bounds alone do not control approximate formulations. A quantitative face stability lemma or a slack-matrix approximation argument would be needed before claiming an approximation barrier.

## Subsequent quantitative results

The exact face was shown to be explicitly exposed by

```
g=m-T+(2m+1)B+(4m+1)(1-trace W),
```

with `g>=B+(1-trace W)>=0`. This lemma passed independent audit. A constructive rounding proof then gave `dist_1(W,F)<=(136m+10)g(W)`. The stability reviewer improved the outer-approximation transfer by preserving its intermediate dependence on `B`, the trace deficit, and total mass, yielding transfer factor `A_m=m(184m+6)`.

The full results are preserved in [the stability and approximate-LP note](../results/rank-one-correlation-face-stability.md) and [the approximate-SDP note](../results/rank-one-approximate-sdp-lower-bound.md):

- An LP outer hull with entrywise l1 error at most `1/A_m=Theta(m^-2)` needs exponentially many inequalities, by a robust correlation-polytope sandwich theorem of Braun–Fiorini–Pokutta–Steurer.
- Any SDP outer-hull family with error `o(m^-2)` needs superpolynomial total PSD order.
- At error at most `c A_m^-1(log m/m)^(2/13)`, the PSD order is `exp(Omega((m/log m)^(2/13)))`. A more conservative explicit error `1/(8mA_m)` also suffices.

The SDP proof shifts the centered-square slack used by Lee–Raghavendra–Steurer. Its negative pseudo-expectation survives the shift, and their quantitative rank theorem still applies. The independent SDP reviewer confirmed all original calculations and the facial-reduction/Slater step giving factorization order at most `q+1`, proposed the accuracy tradeoff, and passed the revised written additions. Exact and approximate extension-complexity machinery is established literature; the proposed new content is its transfer through this continuous pooling block with explicit geometric stability.

Audit files are [exact conic lift audit](review-rank-one-extension.md), [stability audit](review-rank-one-stability.md), and [the approximate-SDP audit](review-rank-one-approximate-sdp.md). Broader novelty search continued with combinations of `pooling semidefinite lower bounds rank one convex hull`, `rank-one matrices extension complexity`, and `rank-one approximate extension pooling`; no matching prior result was located in the search results, but this remains a provisional assessment.

## Stronger final approximate-SDP theorem and equivalent-object screening

A later independently checked improvement uses the sign correlation map

```
J(W)=m(W_11-W_12-W_21+W_22).
```

Its entrywise-l1 operator norm is `m`, and the centered-square slack has all nonzero coefficients `1/(4k^2)`. Consequently a fixed transferred error `eta<=1/2` preserves the pseudo-density gap for every `k`. The final approximate-SDP theorem therefore gives order `exp(Omega((m/log m)^(2/13)))` already at `epsilon<=1/(2A_m)=Theta(m^-2)`. This supersedes the weaker error scales above. The SDP reviewer reread and passed the final rewritten theorem.

A bounded screen through atomic gauges, correlation cones, CP lifts, Boolean/biclique polytopes, and mixed operator norms is recorded in [the equivalent-object novelty note](rank-one-conic-novelty.md). It identified relevant established mechanisms and clarified that one recent paper's “normalized correlation polytope” merely removes the zero vertex. No matching theorem for the continuous unit-capacity rank-one hull was found, but the novelty claim remains deliberately specific and provisional.
