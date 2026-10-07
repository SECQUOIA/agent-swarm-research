# Two-point resistance uncertainty creates hardness at block cycle rank two

Date: 2026-09-05. Status: two independent proof reviews passed: [first](../notes/review-potential-flow-discrete-resistance-hardness.md), [second](../notes/review-potential-flow-discrete-resistance-hardness-second.md). The [novelty audit](../notes/potential-flow-discrete-resistance-hardness-novelty.md) found prior circuit-extrema and discrete network-sizing hardness, but no equivalent result with the restrictions proved here. A directly relevant 1993 nonlinear-circuit source remains unread, so novelty is qualified.

The result separates independent two-point resistance choices from continuous resistance intervals. On the same graph parameter class, the [continuous-box theorem](potential-flow-joint-resistance.md) gives polynomial bit-time additive optimization; the discrete choices below encode Subset Sum.

## Theorem

Maximum potential difference for a prescribed terminal pair under independent two-point resistance uncertainty and the common quadratic law `pi_u-pi_v=beta_e x_e|x_e|` is NP-hard on simple graphs of maximum degree three with one biconnected block of cycle rank two and otherwise only a bridge. All nominations are fixed small integers; each uncertain edge has only two positive rational resistance options. The reduction has an explicit rational gap of polynomial encoding length. Consequently, a polynomial-time algorithm in input size and requested precision bits for additive pressure optimization on this class would imply `P=NP`.

All resistances and the comparison threshold can alternatively be made positive integers by a common polynomially encoded scaling. This is a hardness result for discrete resistance choices; replacing those choices by intervals is not an equivalent operation on these graphs. No strong NP-hardness claim is made.

## Subset-Sum reduction

Take positive integers `a_1,...,a_n` and target `K>0`, and set `S=sum_i a_i`. Instances with `K>S` can be decided directly. On vertices `0,1,2,3`, use the four fixed edges

```
0->2, 2->1, 0->3, 3->1,
```

with resistances `1/2,1/6,1/6,1/2`, respectively. Replace the cross edge `2->3` by a path of `n` edges with zero nominations at its internal vertices. On cross-path edge `i`, choose independently

```
beta_i in {1/(2n), 1/(2n)+a_i/(2K)}.
```

Writing the binary choice as `sigma_i`, the effective cross-path resistance is

```
tau = 1/2 + sum_i a_i sigma_i/(2K).
```

Initially give the four original vertices the fixed nominations `(4,-4,3,-3)`. The explicit theta solution has positive cross flow `q`, determined by

```
(12 tau+1) q²+10q-23=0,       0<q<2.
```

Its other edge flows are `(q+1)/2,(7-q)/2,(7-q)/2,(q+1)/2` in the displayed fixed-edge order. They satisfy conservation and the quadratic potential laws, and uniqueness identifies them with the physical solution. In particular,

```
pi_0-pi_1 = 2+(q-1)²/6.
```

Therefore the reverse pressure objective reaches `-2` if and only if `q=1`, equivalently `tau=1`, equivalently `sum_i a_i sigma_i=K`.

For a positive threshold, add a leaf vertex `4` and an edge `4->1` of resistance `3`. Set its nomination to `1` and change the nomination at vertex `1` from `-4` to `-5`. The other nominations stay unchanged, so the full fixed nomination vector on the five distinguished vertices is

```
(4,-5,3,-3,1).
```

The bridge carries exactly one unit and gives `pi_4-pi_1=3`. Thus the objective

```
F = pi_4-pi_0 = 1-(q-1)²/6
```

has maximum `1` if and only if the Subset-Sum instance is feasible. The graph remains simple, has maximum degree three, and has one theta block of cycle rank two plus one bridge.

## Explicit no-instance gap

If no subset sums to `K`, integrality gives `|tau-1|>=1/(2K)` for every choice. Subtracting the cycle equation evaluated at `q=1` from that at its physical root gives

```
|q-1| = 12|tau-1| / [(12tau+1)(q+1)+10].
```

Since `q<2` and `tau<=tau_U=(K+S)/(2K)`, its denominator is at most

```
36tau_U+13 = 31+18S/K.
```

Consequently,

```
|q-1| >= 6/(31K+18S),
F <= 1-Delta,
Delta = 6/(31K+18S)².
```

This positive rational `Delta` has polynomial binary encoding length. An additive optimum-value interval of width less than `Delta/3`, or an equivalently certified value approximation with that error, separates yes instances from no instances. The number of requested precision bits is `O(log(K+S))`, polynomial in the original input size. This proves the claimed obstruction to polynomial high-precision additive optimization unless `P=NP`.

## Integer-resistance scaling

Multiply every resistance and the pressure threshold by `6nK`. The four fixed theta resistances become `3nK,nK,nK,3nK`; the uncertain cross-path options become

```
{3K, 3K+3n a_i};
```

and the leaf bridge resistance becomes `18nK`. Every resistance is a positive integer. Common scaling preserves the physical flow and multiplies every potential difference by `6nK`. The threshold becomes `6nK`, and the gap becomes `6nK*Delta`, still of polynomial encoding length. Nomination values are unchanged.

## Interpretation and limits

The already-reviewed continuous interval-resistance algorithm is polynomial in input and precision bits for fixed block cycle rank, including rank two. This reduction uses discrete choices whose interval hull allows an interior effective cross resistance to realize a larger pressure value. Thus discrete uncertainty cannot be replaced by its interval hull in this topology.

Together with the [cactus hull investigation](../notes/potential-flow-cactus-uncertainty-hulls.md), this gives a sharp topological comparison: cactus graphs retain interval-hull extrema for independent scalar uncertainty and hence inherit high-precision algorithms, while a single theta block permits Subset-Sum hardness for two-point resistance choices. The proof concerns unrestricted passive physical states, not additional pressure or capacity feasibility restrictions. It is an adversarial discrete-parameter optimization result, and does not by itself prove hardness of every network-design objective on the same graphs.

Both independent reviews verified the leaf nomination sign, series resistance aggregation, rational gap algebra, maximum-degree count, and integer scaling. The source audit compares related discrete circuit and network-design results and records the unresolved source-access limit.

## Reproducible evidence

[`discrete_resistance_hardness_checks.py`](../code/potential_flow_mpd/discrete_resistance_hardness_checks.py) verifies the gadget balance, cycle, span, and leaf-shift formulas as exact symbolic identities. It exhaustively checks 1,976 resistance scenarios from 48 small Subset-Sum instances, including 14 yes and 34 no instances, at 80-digit precision. Every claimed no-case gap passed, with the smallest observed actual gap divided by the stated lower bound equal to about `1.88`. Topology checks confirm maximum degree three and block ranks `[0,2]`; integer resistance scaling is checked exactly with rational arithmetic. These checks are independent mechanism evidence alongside the reduction proof.

Run with `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/discrete_resistance_hardness_checks.py`.

The [second review](../notes/review-potential-flow-discrete-resistance-hardness-second.md) also includes an independent implementation, [`discrete_resistance_second_review_checks.py`](../code/potential_flow_mpd/discrete_resistance_second_review_checks.py), which passed 2,550 scenarios across 40 instances and four exact symbolic identities. These independent checks supplement the proof; they do not establish novelty.

The precision-gap argument also applies to an algorithm that returns a discrete near-optimal resistance choice: on a yes instance, an error below `Delta` forces its selected subset to sum exactly to `K`. The selection can be checked using integer arithmetic, without evaluating the physical pressure. This particular rank-two gadget does not establish edge-flow hardness: its individual edge flows are monotone in the total cross resistance.

## Further scaling: fixed absolute-error hardness

A later audit of the weighted-objective extension identified a useful strengthening of this pressure result. After the integer resistance scaling `6nK` above, multiply every resistance once more by `T=(31K+18S)^2`. The objective peak becomes the integer `6nK T`, and the no-instance gap becomes

```
(6nK) T Delta=36nK>=36.
```

All data still have polynomial binary encoding length, while the fixed small nominations and graph class remain unchanged. Therefore absolute-error-one maximum-pressure approximation is NP-hard on the unnormalized integer-resistance class: compare its output with the peak minus 18. This is not a strong-hardness or relative-error statement, because the resistance magnitudes and objective range can grow with the binary input values. Common resistance scaling changes pressures, so a caveat excluding fixed absolute-error hardness would be incorrect here. In contrast, it leaves arc flows unchanged, and does not amplify the fixed-small-nomination arc-flow gap.

Two current independent weighted-cycle reviewers checked this scaling principle; the earlier pressure reduction and its exact gap are unchanged.
