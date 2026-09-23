# Second independent review: exact arc comparison on series-parallel graphs

Date: 2026-09-05. Reviewer: `benders_property`, independent of the author and first reviewer. Reviewed [the probe-cactus candidate](potential-flow-series-parallel-exact-arc-barrier.md) and both directions of its imported [cactus arithmetic reduction](../results/potential-flow-cactus-square-root-sum.md).

**Verdict: pass.** The restricted probe-cactus family has a weak lower arc-comparison problem polynomial-time many-one equivalent to the stated Square-Root Sum problem. The construction yields the claimed lower bound on simple degree-three series-parallel graphs with fixed positive integer resistances and unit source/sink nominations. It does not establish an SRS upper bound for arbitrary series-parallel graphs or ordinary NP-hardness.

## Convention and forward reduction

I directly checked the [Etessami–Yannakakis primary manuscript](https://www.pure.ed.ac.uk/ws/portalfiles/portal/14011363/nash_focs07_full_j_spec_issue_sub.pdf), Section 1, PDF p.4: its definition uses positive integer radicands and the weak comparison `sum sqrt(a_i)<=K`. The candidate therefore uses an explicitly sourced convention and does not need to transform a complementary strict comparison.

The imported triangle encoder has positive effective resistance `a+1-2sqrt(a)` for `a>=2`. Series composition gives `D=C-2sum sqrt(a_i)` before common scaling. The lower comparison `D>=C-2K` is exactly the source weak inequality. Scaling all old resistances and that threshold by `2 product a_i` preserves flows and makes both resistance data and the nontrivial positive threshold integers with polynomial encoding length.

In the new graph, the two unit terminal bridges give cactus-branch resistance `D+2` and the probe has resistance `H+2`. Under unit total demand, both branch flows are strictly positive: the common terminal drop is positive, and each branch has a positive effective resistance. Their sum is one. Thus

```
x=sqrt(D+2)/(sqrt(D+2)+sqrt(H+2)),
x>=1/2 iff D>=H.
```

No sign ambiguity or approximate root evaluation enters this equivalence. Equality in SRS gives exactly `x=1/2` and is retained as a yes instance.

## Trivial cases and graph restrictions

Removed unit radicands are subtracted from the source threshold; zero radicands, if admitted as a preprocessing convenience, contribute nothing. When no radicals remain, the answer is an integer comparison. With a nonempty encoded chain, `H<=0` is a yes case because its effective resistance is positive. All these decided cases may be mapped to the fixed family members described in the candidate.

Those fixed outputs are valid. The old triangle has two equal branch resistances of two, hence effective resistance `1/2`. The terminal bridges give `5/2`; probe resistances one and nine place the flow strictly above and below `1/2`, respectively. Every resistance is a positive integer, and the graph remains a cactus branch with two terminal bridges and a probe.

For `m` nontrivial triangle gadgets, the new graph has `3m+2` vertices and `4m+2` edges. Its cycle rank is `m+1`. The old source and sink have degree two and rise to three; the new terminals have degree two; all other degrees remain at most three. The probe cannot duplicate an old edge because both its endpoints are new.

The chain is a two-terminal series composition of triangle networks and bridges, and adding the probe is a parallel composition, proving the stated series-parallel property. The resulting lower-bound graph is biconnected: the probe reconnects the two sides of any old connecting vertex, while deletion of a triangle's third vertex leaves its direct branch intact. Deleting either new terminal also leaves the remaining old branch connected. Thus the growing cycle rank belongs to a single block and does not contradict a fixed-block-rank exact algorithm.

## Converse and bit complexity

For any member of the restricted family, let `R>0` be the effective resistance of its entire cactus branch and `beta>0` that of the probe. The target flow belongs strictly to `(0,1)`. Therefore `x>=c` is true for `c<=0` and false for `c>=1`, including equality at one. For `0<c<1`, all quantities being squared are positive and

```
x>=c iff R>=beta*c^2/(1-c)^2.
```

The new rational threshold has polynomial encoding length. In the cactus branch, off-terminal-path blocks carry zero flow. Each unequal-branch cycle contributes

```
AB(A+B)/(A-B)^2 - sqrt(4A^3 B^3/(A-B)^4),
```

while an equal-branch cycle contributes the rational value `A/4`. Bridge values are rational. This gives `R=Q-sum sqrt(r_j)` with positive rational radicands and polynomial coefficient bits. The lower comparison therefore becomes the same weak SRS comparison with rational data. If no radicals remain, decide it rationally; if radicals remain and the resulting right side is nonpositive, the answer is no, including equality at zero.

For positive right side `T=p/w` and radicands `u_j/v_j`, multiplying by the positive integer `L=w product v_j` gives integer radicands `L^2 u_j/v_j` and integer threshold `LT`. Their binary lengths are polynomial, and positive scaling preserves the weak inequality. Fixed SRS yes/no outputs handle all decided cases. Neither factorization nor evaluating radicals is needed in either reduction direction.

The converse uses the explicit sum-of-radicals representation of a cactus branch. A general series-parallel expression may have nested radicals, so this argument supplies no analogous upper bound outside the stated restricted family. It also does not convert this weak lower comparison into strict capacity violation by ignoring equality.

## Verification and scope

I read and reran `series_parallel_exact_arc_barrier_checks.py` in the repository's designated Python environment. It passed 48 complete graph/state/threshold checks, 20 nonpositive-threshold preprocessing checks, and three exact-equality checks. The maximum potential residual was `9.8833106e-83`. The fixed triangle-based trivial outputs were checked algebraically above. These computations supplement the exact reductions and are not a proof of a numerical separation bound.

No separation promise is present or needed. The result concerns exact arithmetic comparison and does not rule out additive approximation to a prescribed tolerance. The known parallel resistance identity and the imported cactus encoder remain credited ingredients; this review does not establish publication priority for the probe corollary.
