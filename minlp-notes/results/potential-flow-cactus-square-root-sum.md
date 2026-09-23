# Square-Root Sum completeness of exact quadratic cactus potential comparison

Date: 2026-09-05. Status: both reduction directions passed [independent mathematical review](../notes/review-potential-flow-cactus-arithmetic.md), with the threshold-zero convention correction applied. The reduction and upper bound below are mathematical claims; novelty remains provisional. No NP-hardness is claimed.

## Theorem

For passive quadratic potential-based flows with one source and one sink, deciding whether the maximum source-to-sink potential difference is at least a rational threshold is polynomial-time many-one equivalent to **Square-Root Sum**. The lower bound holds on simple cactus graphs of maximum degree three, with every cycle a triangle, positive integer resistances, unit source and sink booking capacities, and all flow directions known in advance.

Here Square-Root Sum (SRS) has binary-encoded positive integers `a_1,...,a_n,K` and asks whether `sum sqrt(a_i) <= K`. The comparison is exact in the ordinary Turing bit model. This is an arithmetic complexity barrier, not an NP-hardness result or a hardness result for approximation.

The 2026 survey explicitly identifies the nonlinear MPD problem on cactus graphs as open (printed pp.9–10): [Pfetsch, Schmidt, Skutella, Thürauf, *Potential-Based Flows—An Overview*](https://optimization-online.org/wp-content/uploads/2026/01/ch_potential.pdf). The theorem resolves the arithmetic complexity of its single-entry, single-exit subclass; it does not resolve the complexity of unrestricted multi-entry, multi-exit cactus MPD.

The weak `<=` convention used here is explicitly the SQRT-SUM definition in [Etessami and Yannakakis, *On the Complexity of Nash Equilibria and Other Fixed Points*, Section 1](https://www.pure.ed.ac.uk/ws/portalfiles/portal/14011363/nash_focs07_full_j_spec_issue_sub.pdf), PDF page 4, and is repeated in Section 3, PDF page 22. No reduction from a complementary inequality convention is assumed.

## Model and decision problem

Let an oriented connected graph have positive rational resistances `beta_e`. A nomination has injection `b_s=q`, withdrawal `b_t=-q`, and zero load elsewhere, with `0 <= q <= 1`. Flow and potentials satisfy

```
sum_out x_e - sum_in x_e = b_v,
pi_u - pi_v = beta_e x_e |x_e|  for e=(u,v).
```

There are no potential or arc-capacity bounds in MPD itself. The decision problem asks whether

```
max_{0 <= q <= 1} (pi_s-pi_t) >= H.
```

Potentials have an arbitrary additive normalization. The unique flow follows, for example, by minimizing the strictly convex coercive energy `sum beta_e |x_e|^3/3` over the nonempty affine flow-conservation space. Its stationarity equations give the potential law. Homogeneity implies that all flows scale by `q` and all potential differences by `q^2`. The unit-flow source-to-sink drop is positive, because multiplying potential equations by flows gives `pi_s-pi_t = sum beta_e |x_e|^3 > 0`. Consequently the maximum occurs at `q=1`.

## A radical gadget

Let `a` be an integer at least two. Connect two terminals with two internally disjoint branches whose total resistances are

```
A=(a-1)^2,       B=(a-1)^2/a.
```

For total through-flow `q>=0`, the branch flows are nonnegative and sum to `q`. Equality of their potential drops gives

```
x_A = q/(sqrt(a)+1),
x_B = q sqrt(a)/(sqrt(a)+1).
```

The common drop is therefore

```
A x_A^2 = q^2 (sqrt(a)-1)^2
        = q^2 (a+1-2 sqrt(a)).                 (1)
```

Equivalently, the effective quadratic resistance of two parallel branches of resistances `A,B` is

```
R(A,B) = AB/(sqrt(A)+sqrt(B))^2.
```

This parallel-reduction formula is already known; the proposed new content is its use to embed exact SRS comparison and the corresponding classification. One branch can be a direct edge and the other a two-edge path, dividing its resistance equally between its two edges. The graph is then a triangle with positive rational resistances.

## Reduction to simple cacti of maximum degree three

Given an SRS instance, remove every `a_i=1` and subtract their number from `K`. If a convention allows `a_i=0`, remove those without changing `K`. If no terms remain, decide the integer comparison and output a fixed yes or no MPD instance (a single edge of resistance one and threshold one or two). The remaining integers satisfy `a_i>=2`; call their count `m>=1`.

Create `m` vertex-disjoint triangles. Triangle `i` has a direct edge of resistance `(a_i-1)^2` and a two-edge alternate path, each edge having resistance `(a_i-1)^2/(2a_i)`. Join the exit of triangle `i` to the entrance of triangle `i+1` by a resistance-one bridge. Let `s` be the first entrance and `t` the last exit. Orient both branches from entrance to exit and all bridges from left to right. There are `3m` vertices and `4m-1` edges. The undirected graph is a simple cactus, every cycle is a triangle, and maximum degree is three.

Every block carries the same total through-flow `q`. Equation (1) and addition of drops in series give

```
MPD = C - 2 sum_i sqrt(a_i),
C   = sum_i (a_i+1) + (m-1).                 (2)
```

Set `H=C-2K`. Then, including equality,

```
sum_i sqrt(a_i) <= K  iff  MPD >= H.         (3)
```

Thus weak SRS comparison maps to weak MPD comparison without a numerical tolerance or an approximation. The source and sink booking capacities are both one, and all others are zero. All nonzero-nomination flows follow the prescribed orientations. The zero nomination simply gives zero flows.

If nonnegative thresholds are required, an instance with `H<0` is automatically a yes instance: `C >= 2 sum sqrt(a_i)`, so `H<0` implies `K>C/2 >= sum sqrt(a_i)`. Output the fixed yes instance instead. The same applies to `H=0`, since the constructed MPD is positive.

To obtain positive **integer** resistances, multiply every resistance and `H` by

```
L = 2 product_i a_i.
```

All direct edges, alternate-path edges, and bridges now have positive integer resistances. The flow is unchanged, and all potential differences and MPD are multiplied by `L`. The threshold `LH` is an integer. There are `O(m)` vertices and edges; `log L = O(sum log a_i)`, and each resistance and threshold has polynomial binary encoding length. Integer multiplication and exact division construct the output in polynomial bit time. No prime factorization is needed.

## Matching upper bound for arbitrary single-source single-sink cacti

Take any connected cactus with positive rational resistances and distinct terminals `s,t`. Blocks not on the unique `s-t` path in the block-cut tree carry zero flow: such a component has no source or sink, and its unique potential flow with zero net load and one attachment is zero. Hence only the bridges and cycles on that block path matter.

A bridge of resistance `beta` contributes `beta` to the unit-flow drop. Each cycle contributes the effective resistance `R(A,B)`, where `A,B>0` are the sums of edge resistances along the cycle's two paths between its entrance and exit. For `A=B`, `R=A/4` is rational. Otherwise, rationalizing gives

```
R(A,B) = AB(A+B)/(A-B)^2
         - [2AB/(A-B)^2] sqrt(AB).            (4)
```

In particular the total unit-flow drop can be written in polynomial time as

```
MPD = Q - sum_{j=1}^r sqrt(r_j),             (5)
```

where `Q` and every `r_j` are positive rationals with polynomial encoding length. Specifically `r_j = 4 A_j^3 B_j^3/(A_j-B_j)^4`. If there are no unequal-branch cycles, the comparison is rational and can be mapped to a fixed SRS yes/no instance.

For the remaining case, `MPD>=H` is equivalent to `sum sqrt(r_j)<=T`, where `T=Q-H`. If `T<=0`, output a fixed no instance, since at least one radical remains and all radicals are positive. Write each `r_j=u_j/v_j` with positive integers and write `T=p/w` with `w>0`. Choose

```
D = w product_j v_j.
```

Then `N_j=D^2 u_j/v_j` and `K'=DT` are integers, of polynomial binary length, and

```
sum sqrt(r_j)<=T  iff  sum sqrt(N_j)<=K'.     (6)
```

This is a polynomial-time many-one reduction to SRS. It uses rational arithmetic only; the output does not require explicitly computing any square root. Together with (3), it proves the claimed SRS completeness of exact single-entry, single-exit cactus MPD threshold comparison.

## Exact comparison versus computation and approximation

The known series/parallel reduction constructs an expression for effective resistance in linearly many reduction operations. It does not by itself give a polynomial-time exact rational-threshold comparison in the Turing model. Equations (2)–(6) make that distinction explicit. The May 31, 2018 open manuscript underlying Groß et al., published in Networks 73(3), 306–324 (2019), discusses the Turing computational model and approximation of roots on printed p.3; its Lemma 4.2 and Theorem 4.3 give the parallel formula and reduction sequence on pp.10–12. [Open preprint](https://optimization-online.org/wp-content/uploads/2017/08/6185.pdf).

The 2020 preprint of Labbé, Plein, Schmidt, Thürauf gives an exact polynomial-time single-cycle booking algorithm by reduction to real algebraic geometry in fixed dimension (Section 6, printed pp.24–27). With an unbounded number of cycle blocks, the number of independently occurring radicals is unbounded. [Open preprint](https://optimization-online.org/wp-content/uploads/2019/11/7472.pdf).

The result does not obstruct computing polynomial-accuracy numerical approximations. On the constructed family, (2) directly allows an additive error `epsilon` by approximating each square root to error at most `epsilon/(2m)` before summation (or `epsilon/(2Lm)` after integer scaling). Exact classification of an instance without a promised gap remains different.

For current context on SRS, [Demaine, Gasarch, Hajiaghayi, *Computational Intractability*, July 2025 draft](https://hardness.mit.edu/drafts/2025-07-08.pdf), Section 12.7.2, states that polynomial-time decidability, NP membership, and NP-hardness remain open. Its displayed convention uses `sum sqrt(a_i)>=K`; this note explicitly defines and uses the `<=` convention. [Etessami and Yannakakis, *Recursive Concurrent Stochastic Games*](https://arxiv.org/abs/0810.3581) is a primary example of SRS-based lower bounds.

## Bounded novelty screening

On 2026-09-05, searched the open web for combinations of `potential-based flows`, `gas networks`, `network flow`, `square-root-sum`, and `sum of square roots`. No direct antecedent for this cactus MPD classification was found. The surveyed sources explicitly retain cactus MPD as open, and the known parallel-reduction formula is not new. This is a bounded search, not proof that the arithmetic reduction is absent from all literature. Both directions passed independent mathematical review. A [separate novelty audit](../notes/potential-flow-cactus-arithmetic-novelty.md) found no matching antecedent and records the bounded search and remaining uncertainty.

## Why this barrier matters for extension algorithms

The preexisting `code/potential_flow_mpd/` explores single-cycle load exchanges inside a cactus. A tempting extension of the single-cycle algorithm would enumerate one active cycle and add the already-determined drops on all other blocks. Even if the load-structure claim is proved, exact comparison of that sum can already encode SRS with no interior injections at all. Thus a successful algorithm must distinguish a real-arithmetic/approximation guarantee from an exact polynomial bit-complexity guarantee. No correctness claim about the earlier fractional-load experiments is used here.

## Verification artifacts

[`code/potential_flow_mpd/square_root_sum_reduction.py`](../code/potential_flow_mpd/square_root_sum_reduction.py) implements both exact rational encoders. On 2026-09-05 it passed symbolic gadget/rationalization identities and 120 deterministic randomized checks of topology, integrality, exact SRS decision equivalence, and nonlinear flow residuals (maximum residual `1.58e-12`). Run with `/home/sgusev/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/square_root_sum_reduction.py`; the default Python environment lacks `networkx`. The checks include radicands zero and one, all-rational cases, negative thresholds, and equal-resistance branches. They do not independently prove the bit-complexity claims.


The subsequent [multi-entry cactus approximation investigation](../notes/potential-flow-cactus-approximation-investigation.md) is separate research and is not included in this theorem's reviewed claims. The 2026 followup by Klimm, Pfetsch, Skutella, and Strubberg also distinguishes irrational arithmetic from bounded-precision approximation (Remark 8); it contains no cactus MPD arithmetic classification found by the audit. [Open preprint](https://arxiv.org/abs/2604.26882).
