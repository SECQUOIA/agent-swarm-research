# Independent review: continuous nomination arc-hardness transfer

Date: 2026-09-05. Reviewer: `benders_property`. Reviewed [the candidate](potential-flow-unbounded-rank-arc-obstruction.md), its imported Thürauf pressure reduction, and the monotone probe argument.

**Verdict: pass**, retaining the source's positive Partition integers and `n>=3` restriction, with smaller cases handled separately if needed. The construction proves NP-hardness of possible strict arc-capacity violation and high-precision arc-extremum optimization, and coNP-hardness of robust capacity validation, for fixed rational resistances and balanced continuous nomination boxes on undirected series-parallel graphs. It gives no NP/coNP membership or strong NP-hardness claim.

## Source scope checked directly

In [Thürauf's April 2022 manuscript](https://optimization-online.org/wp-content/uploads/2020/05/7803-1.pdf), Figure 2 and equation (3), printed/PDF p.10, give the stated graph, booking bounds, resistances, and rational threshold. The source assumes positive Partition items and `n>=3` on p.9. Lemma 4.3, p.11, supplies a yes-instance nomination with drop one. Lemma 4.17, p.24, bounds the unrestricted-flow maximum strictly below `T(K)<1` in no instances; its proof explicitly includes negative flows. The discussion of problem (2), p.7, excludes restrictive potential bounds. Thus the transferred source result concerns the full physical nomination set, not only nominations already satisfying operating limits.

The notation `T(K)` suppresses its dependence on `n`. Explicitly, the source defines `eps=1-(1-1/(8K^2))^2`, `M0=max{1-eps+eps^2,1-eps^2/K^2}`, `eps_tilde=(1-M0)/5`, and `T=max{1-eps_tilde^2/(K^2 n^2),M0+4eps_tilde}`. These rational operations give `0<T<1` with polynomial encoding length. This is sufficient for the proof; the source hardness itself is credited prior work.

## Nomination set and topology

Use the outflow-minus-inflow convention. The entry intervals are `[0,K/2]` at `s` and `[0,S_i]` at each `z_i+`; exit intervals are `[-K/2,0]` at `t` and `[-S_i,0]` at each `z_i-`. Intersecting these with balance is exactly the source's booking nomination set. It is nonempty, compact, rational, and has total absolute coordinate bound `3K`. No new nomination restrictions are introduced by adding the probe.

The original main block is `K_{2,n}`. Adding `s->t` makes it a parallel composition of that edge and the `n` two-edge branches. It is a two-terminal series-parallel block, while the pendant exits are bridges. Thus the full undirected graph is simple and has treewidth two. The main block has `n+2` vertices and `2n+1` edges, giving cycle rank `n`. Degrees at `s,t` grow with `n`, and no bounded-degree assertion is made.

## Probe equation and monotonicity

Removing a positive flow `t` on the added edge from `s` to `t` leaves old-network nominations `b-t*e_s+t*e_t`, with the exact sign used in the draft. Comparing two old physical states by conservation and strict monotonicity of `x|x|` shows that their pressure difference `F_b(t)` is strictly decreasing in the transferred flow parameter. The new physical state therefore satisfies `F_b(t)=M*t*|t|`.

If `F_b(0)<=0`, a positive probe flow is impossible. If `F_b(0)>0`, a nonpositive probe flow is impossible, and monotonicity bounds the new drop above by the old one. This covers all signs, including `F_b(0)=0`, without imposing sign restrictions on other arc flows.

## Uniform perturbation and gap

For every original nomination, acyclic physical flow gives `|x_e|<=3K`. An old two-edge `s-t` path has total resistance `2/S_i^2<=2`, so `|F_b(0)|<=18K^2`. Since `H=(1+T)/2>=1/2`, a yes witness's probe flow obeys

```
0<t<=sqrt(18K^2/(H D^2))<=6K/D<1.
```

The old and perturbed nomination vectors belong to a rational box enlarged by at most one at each terminal. Its absolute coordinate bound is at most `3K+2`, even if an auxiliary perturbed nomination changes an entry/exit sign. These auxiliary old-network nominations need not satisfy the original booking; they are used only to analyze the same new-network scenario.

The pressure Lipschitz estimate on the old two-edge path is at most `4(3K+2)` per unit l1 nomination change. Hence the pressure loss is at most `8(3K+2)t`, which is at most `48K(3K+2)/D<gamma/4` for the proposed ceiling defining `D`. The path excludes the large probe resistance, and its bound does not depend on a hidden uncertain coefficient.

A yes witness consequently has new drop above `1-gamma/4`, exceeding `H=1-gamma/2`. Its probe flow is strictly above `c=1/D`. In a no instance, every positive probe flow has drop below the original drop, which is strictly below `T<H`, so every such flow is strictly below `c`; nonpositive flows satisfy the capacity directly.

For a yes witness, dividing the pressure margin by `M(t+c)` gives a flow margin at least `gamma/[4(6K+1)D]`. In a no instance, a positive probe flow is at most `2/D`, and its pressure margin below `H` is at least `gamma/2`; the flow margin is therefore at least `gamma/(6D)`. A nonpositive flow has margin at least `1/D`. Both no-case margins dominate the displayed yes-case bound for `K>=1`. Thus equality cannot obscure the reduction.

## Complexity and capacity interpretation

The graph and all rational data, including `gamma`, `D`, `M`, `c`, and the separation gap, have polynomial binary encoding length. The gap can be numerically very small, but its logarithm is polynomially bounded. A certified additive optimum estimate with error below a fixed fraction of that gap decides Partition by comparison with `c`. This proves the precision-bit complexity obstruction; it does not imply fixed-accuracy or strong hardness.

Existence of a strict upper-capacity violation corresponds to a yes Partition instance. Universal satisfaction corresponds to a no instance, giving the stated coNP-hardness. Other arc bounds may safely be `[-3K,3K]` because the full new network retains the original nomination box. There are no potential bounds or earlier flow-capacity constraints filtering the scenarios.

The reduction uses only fixed positive rational resistances; the continuous choice lies in nominations. It therefore establishes a different obstruction from the previously reviewed finite resistance-choice hardness. No exact-membership upper bound is inferred at unbounded block rank, where the fixed-rank arc algorithm is unavailable.

The author subsequently made the `n>=3` convention and explicit rational threshold formulas part of the candidate. I also reran [the added probe checker](../code/potential_flow_mpd/unbounded_rank_arc_probe_checks.py): 24 explicit Partition yes nominations passed complete branch/probe conservation, pressure, and flow-gap checks at 110-digit precision; the largest probe residual was `3.3265311e-111`. These checks supplement the exact source and perturbation arguments, without serving as a no-instance optimizer or certified interval algorithm.
