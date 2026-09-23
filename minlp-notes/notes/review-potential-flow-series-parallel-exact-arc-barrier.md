# Independent audit of the exact arc comparison barrier

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS**, after the author replaced trivial yes/no outputs by instances inside the stated restricted family. The proof establishes polynomial-time many-one equivalence with the explicitly defined `sum sqrt(a_i)<=K` version of Square-Root Sum on the probe-cactus family. Its extension to arbitrary series-parallel graphs is a lower bound only. Novelty of this corollary was not independently established by this audit.

Reviewed [candidate](potential-flow-series-parallel-exact-arc-barrier.md) and [earlier cactus reduction](../results/potential-flow-cactus-square-root-sum.md), including both arithmetic reduction directions.

## 1. Inequality convention and primary sources

The `<=` convention is used explicitly by Etessami and Yannakakis in *On the Complexity of Nash Equilibria and Other Fixed Points*, Section 1, fourth PDF page, and again at the start of Section 3. The inputs there are positive integers and an integer threshold, exactly matching the present source problem. [Primary manuscript](https://www.pure.ed.ac.uk/ws/portalfiles/portal/14011363/nash_focs07_full_j_spec_issue_sub.pdf).

This citation matters because their different paper *Recursive Concurrent Stochastic Games*, Section 5, defines SRS using `>=`. That convention should not be substituted silently in a many-one completeness statement. The candidate explicitly uses `<=` throughout and needs no reduction between the two conventions. [Other primary paper](https://arxiv.org/html/0810.3581v3).

The physical identities used by the reduction are prior work: Groß, Pfetsch, Schewe, Schmidt, and Skutella, Lemma 4.2, gives series addition and the parallel law; the quadratic formula is displayed on printed page 11. Theorem 4.3 counts reduction operations, without by itself supplying polynomial bit-time exact threshold comparison of the resulting radical expressions. [Open manuscript](https://optimization-online.org/wp-content/uploads/2017/08/6185.pdf).

## 2. Forward reduction

For each remaining `a_i>=2`, the earlier triangle gadget has unit effective resistance `a_i+1-2sqrt(a_i)>0`. A chain of these triangles and unit bridges has effective resistance `C-2sum sqrt(a_i)`. Multiplying all resistances and the comparison threshold by `L=2 product a_i` gives positive integer resistances and the integer threshold `H=L(C-2K)`. Its binary length is polynomial, even though its numerical magnitude need not be. If `H<=0`, positivity makes the source instance a yes instance; cases with no remaining radicals are decided by integer arithmetic. Consequently the nontrivial probe construction may assume `D>0` and `H>0`.

Adding two resistance-one terminal bridges gives `D'=D+2`; a parallel probe of resistance `H+2` has positive integer resistance. Under total demand one, the positive branch flows satisfy

```
q+x=1,       D'q^2=(H+2)x^2,
x=sqrt(D')/(sqrt(D')+sqrt(H+2)).
```

All square roots here are positive. Thus

```
sum sqrt(a_i)<=K  iff  D>=H  iff  x>=1/2.
```

Equality is preserved at every step. In particular, the direction of the probe flow is correct: increasing the resistance of the other branch increases probe flow.

The graph restrictions also hold. The old terminal degrees are two, so attaching the terminal bridges raises them only to three; the new terminals each have degree two. No old edge connects the new terminals, so the probe creates no multiple edge. The construction is a two-terminal series-parallel composition. For `m` triangles it has `3m+2` vertices and `4m+2` edges, hence cycle rank `m+1`. It is biconnected: the outer probe reconnects the two portions left by deleting a connecting vertex, while deletion of a triangle's third vertex leaves its direct entrance-exit edge. Deleting either new terminal also leaves the rest connected. Thus the unbounded rank occurs inside one biconnected block.

For trivial outputs, the original draft's triangle was outside the literal stated family with two extra terminal bridges. The author corrected this: use an old triangle with direct resistance two and alternate-path resistances one and one. Its effective resistance is `1/2`; after the two unit bridges it is `5/2`. Probe resistance one gives `x>1/2`, and probe resistance nine gives `x<1/2`. Both fixed outputs satisfy every graph and integrality restriction and belong to the same probe-cactus family.

## 3. Converse for arbitrary rational thresholds

For an arbitrary probe-cactus instance, let `R>0` include the resistance of its entire non-probe cactus branch. For rational `c`, comparisons with `c<=0` are true and those with `c>=1` are false. For `0<c<1`, positivity permits squaring without changing the comparison:

```
x>=c  iff  (1-c)sqrt(R)>=c sqrt(beta)
         iff  R>=beta*c^2/(1-c)^2.
```

The last threshold is rational with polynomial binary length. The earlier cactus reverse reduction applies to exactly this weak lower comparison. Only blocks on the terminal block path carry flow. Each unequal-branch cycle contributes

```
AB(A+B)/(A-B)^2 - sqrt(4 A^3 B^3/(A-B)^4),
```

while equal branches contribute `A/4`. Adding bridge contributions gives `R=Q-sum sqrt(r_j)` with positive rational radicands and polynomial rational encoding length. Writing `r_j=u_j/v_j` and `T=Q-H=p/w>0`, the integer `M=w product v_j` produces integer radicands `M^2 u_j/v_j` and integer threshold `MT`. This is a direct many-one reduction to the same `<=` SRS problem. Rational-only cases and `T<=0` are handled by fixed SRS outputs. No root computation or factorization is needed.

The upper bound requires the cactus branch structure. It does not extend merely by invoking a series-parallel expression, where nested radicals can arise. The candidate preserves this restriction.

## 4. Interpretation and checks

This is an exact arithmetic barrier, with no promised numerical separation. It neither gives NP-hardness nor obstructs approximation to a requested additive tolerance. The use of fixed nominations and singleton resistance choices makes it directly relevant to the exact-versus-additive distinction in the companion optimization theorem. The fixed-block-rank exact algorithm is consistent with the construction because its single block has growing cycle rank.

The independent audit checked the rational identities and graph argument directly. I also reran `series_parallel_exact_arc_barrier_checks.py` using `/home/sgusev/miniconda3/envs/minlp-notes/bin/python`: 48 full graph/state/threshold checks, 20 nonpositive-threshold preprocessing cases, and three exact equalities passed. The largest potential residual was `9.8833106e-83`. These calculations are additional numerical evidence, not a proof of comparison or bit-complexity claims.
