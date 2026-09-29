# A topology-dependent loss of rounding order for switched control

Date: 2026-09-28. Status: candidate theorem with an independent adversarial proof review and a bounded primary-source audit. This is a new direction within this repository, not a claim of established publication priority. The rate classification is the main contribution; graph-constrained control rounding itself is established.

## Motivation and scope

A switched process may have to pass through an intermediate operating mode before changing between two productive modes. A continuous relaxation can mix the productive modes while assigning zero time to the intermediate mode. Refining the switching grid does not give the usual first-order rounding rate in this situation: avoiding long productive runs requires frequent visits to the intermediate mode, and those visits accumulate error.

The theorem below gives a complete worst-case rate classification for a fixed directed transition graph. On a fixed physical horizon, the uniform approximation order is `h` for complete transition graphs, `sqrt(h)` for strongly connected incomplete graphs, and a nonvanishing constant otherwise. The square-root obstruction persists in uniformly contracting linear state dynamics. Positive relaxed mass in every mode restores first-order accuracy.

These statements concern a relaxation in which arbitrary simplex controls are permitted, or the convex hull of graph-feasible mode sequences with free initial mode. They do not claim that a transition-aware nonlinear relaxation must have the same gap. They do not impose a fixed positive physical dwell time: every visited mode occupies at least one grid interval of length `h`, which tends to zero. Fixed positive dwell times lead to a different approximation question.

## Definitions

Let `G=(V,E)` be a directed graph on `m>=2` modes. Every vertex has a self-loop. The graph and `m` are fixed as the number of time slots `N` grows. Initial and final modes are free.

A pure control is a word `w_1,...,w_N` with `(w_k,w_{k+1}) in E`. Identify mode `i` with its coordinate vector `e_i`. A relaxed control is any sequence `alpha_k in Delta_m`, where `Delta_m={a>=0:sum_i a_i=1}`. Define

```
D(alpha,w) = max_{0<=k<=N, i in V} |sum_{t=1}^k (alpha_{t,i}-1{w_t=i})|,
R_G(N)    = sup_alpha min_{G-feasible w} D(alpha,w).
```

A word always exists because self-loops are present. At physical slot length `h=T/N`, the continuous-time primitive discrepancy of slotwise constant controls is exactly `h D(alpha,w)`: on each slot every coordinate primitive is affine, so its absolute maximum occurs at a slot endpoint.

Constants in asymptotic notation below depend on the fixed graph, not on `N` or the relaxed control.

## The rate classification

**Theorem 1.** For `m>=2`,

1. If every ordered pair of distinct modes is an arc, then `R_G(N)=Theta(1)`.
2. If `G` is strongly connected and misses an ordered pair, then `R_G(N)=Theta(sqrt(N))`.
3. If `G` is not strongly connected, then `R_G(N)=Theta(N)`.

For `m=1`, the discrepancy is zero. In physical units on fixed `T>0`, the three rates are respectively `Theta(h)`, `Theta(sqrt(T h))`, and `Theta(T)`.

### Complete graphs

The upper bound is the established sum-up-rounding bound. A simple self-contained version suffices. Before slot `k`, let

```
d_i = sum_{t<k}(alpha_{t,i}-1{w_t=i}),
b_i = d_i + alpha_{k,i}.
```

Choose a mode attaining `max_i b_i`, and subtract one from its updated discrepancy. The discrepancies sum to zero after each step. Inductively every discrepancy is greater than `-1`: unchosen coordinates only increase, and the selected coordinate has `b_i>=1/m` because `sum b_i=1`. Hence every discrepancy is less than `m-1`, giving a uniform bound. For `m=2`, the same conclusion means absolute discrepancy less than one. A first-slot target putting mass `1/2` on two modes gives discrepancy at least `1/2` for every choice, proving the lower order bound.

This part is classical and is included only to make the classification self-contained. Sharper unrestricted-rounding constants are already known.

### A closed-tour construction for strongly connected graphs

Fix a closed directed walk visiting every vertex. Write its cyclic vertex list as `v_1,...,v_L`, with arcs from consecutive vertices and from `v_L` to `v_1`. A walk with `L<=m(m-1)` exists by joining successive vertices and returning to the start along shortest directed paths. Let `r_i>=1` be the number of occurrences of mode `i` in the list, so `sum r_i=L`.

Choose an integer block length `B>=L`. For each full block, let `a_i` be the relaxed mass of mode `i` in its `B` slots. Choose nonnegative integers `s_i` summing to `B-L` such that

```
|s_i - (B-L)a_i/B| < 1
```

with `s_i` equal to the target quantity whenever that quantity is integral. Such integers follow by rounding down and distributing the remaining units among positive fractional parts. Traverse the closed walk, and add `s_i` extra self-loop slots at one occurrence of mode `i`. The resulting count of mode `i` is `r_i+s_i`, and

```
|(r_i+s_i)-a_i| <= L+1.
```

The start of each block follows the end of the preceding block because the walk is closed. Hold the last mode on a final incomplete block. The discrepancy accumulated at full-block boundaries is at most the number of completed blocks times `L+1`; within a block each coordinate can change by at most `B`. Therefore

```
R_G(N) <= floor(N/B)(L+1) + B.                         (1)
```

If `B>N`, simply hold one mode and use `R_G(N)<=N`. Choosing `B` on the order of `sqrt(N(L+1))`, subject to `B>=L`, proves `R_G(N)=O(sqrt(N))`.

The construction is explicit and uses only rational summation, rounding and graph paths. It does not solve a mixed-integer optimization problem. It uses each block's relaxed masses, so this is an offline construction rather than a causal online controller. It is not claimed to have an optimal leading constant.

### The missing-arc obstruction

Suppose the arc `u -> v` is absent. Use the constant target

```
alpha_u=alpha_v=1/2,  alpha_i=0 for i not in {u,v}.
```

Let a feasible word have discrepancy `D`, and let `R` be its total number of slots outside `{u,v}`. At the final prefix, each relay mode has appeared at most `D` times, so

```
R <= (m-2)D.                                            (2)
```

Delete relay symbols from the word. Every transition from a projected `u` run to a projected `v` run requires at least one relay slot in the original word, because the direct arc is absent. These separating intervals are disjoint. There are at most `R` such transitions and at most `R+1` transitions in the reverse direction. Thus the projected word has at most `2R+2` runs.

The original interval spanning any one projected run contains none of the other active mode. Its length is at most `4D`: the discrepancy of the absent active mode increases at rate `1/2`, and the difference between its values at the two endpoints is at most `2D`. The number of projected symbols in the run is no greater than that span. Consequently,

```
N-R <= 4D(2R+2),
N   <= 8(m-2)D^2 + (m+6)D.                              (3)
```

For strongly connected incomplete graphs, `m>=3`, so (3) proves the square-root lower bound. Notice that only one missing directed arc is needed.

The target lies in the convex hull of graph-feasible controls: it is the mean of the all-`u` and all-`v` words. The obstruction is therefore not removed merely by replacing the simplex with the exact marginal convex hull of feasible words. This statement uses free initial mode; a fixed initial mode requires a separate transient convention.

### Failure of strong connectivity

Choose vertices `u,v` such that `v` is not reachable from `u`. Let `A` be all vertices reachable from `u`. This is a forward-closed set containing `u` and excluding `v`. Use the same half-`u`, half-`v` target.

For any feasible word, let `r` be the number of slots before its first entry into `A`, or `r=N` if it never enters. There is no `u` in the first `r` slots. There is no `v` after entry into `A`. Thus

```
D >= r/2,
D >= N/2-r.
```

The second inequality is harmless when its right side is negative. Their maximum is at least `N/6`. The universal bound `D<=N` finishes the proof.

## Interior relaxed controls recover first-order accuracy

**Theorem 2.** Suppose `G` is strongly connected and every slot satisfies `alpha_{k,i}>=eta>0` for every mode. Fix a closed visiting walk as above. For any integer `B` satisfying

```
B eta >= max_i r_i + 2,
```

there is a feasible word with `D(alpha,w)<=B+1`, independently of `N`.

**Proof.** At each full-block boundary `bB`, round the cumulative target masses `A_i(bB)` to integers `C_i(b)` summing to `bB`, with `|C_i(b)-A_i(bB)|<1`. Put `C_i(0)=0`. Successive increments

```
n_i(b)=C_i(b)-C_i(b-1)
```

sum to `B` and satisfy `n_i(b)>=B eta-2>=r_i`. In block `b`, traverse the closed walk and insert `n_i(b)-r_i` extra slots at mode `i`. The resulting cumulative mode counts at the boundary equal `C_i(b)`, so boundary discrepancy is less than one. Within a block it grows by at most `B`; the final partial block can hold the preceding last mode. If there is no full block, hold any mode. This proves the claim. The condition also ensures `B>=L`, since `eta<=1/m` and `m max_i r_i>=L`. QED.

The physical discrepancy is `O_G(h/eta)`. This result allows arbitrary time variation of the relaxed control. It does not assert an error bound uniform as `eta` tends to zero. Classical rotor-walk results already give bounded occupation discrepancy for fixed stationary distributions; this does not contradict Theorem 1, whose bad targets assign zero mass to relay modes.

## The sharp transition as relaxed relay mass vanishes

For `0<=eta<=1/m`, let `R_G(N,eta)` be the same worst-case discrepancy as before, restricted to relaxed controls satisfying `alpha_{k,i}>=eta` in every slot and coordinate. At `eta=0` this is `R_G(N)`.

**Theorem 3.** For a fixed strongly connected incomplete graph,

```
R_G(N,eta) = Theta_G(min{sqrt(N), 1/eta}),                 (4)
```

uniformly over `N>=1` and `0<=eta<=1/m`, with `1/0=+infinity`. Thus on a fixed physical horizon the sharp order is

```
Theta_G(min{sqrt(T h), h/eta}).
```

The statement permits `eta` to depend on `N`; it identifies a transition at relay mass on the order of `1/sqrt(N)`.

**Proof.** The upper bound is the minimum of the constructions in Theorems 1 and 2. The constants in both bounds are independent of `eta,N`.

For the lower bound, choose a missing arc `u -> v`, put `a=m-2`, and use the constant target

```
alpha_u=alpha_v=p=(1-a eta)/2,
alpha_i=eta for i not in {u,v}.
```

This target satisfies every lower bound because `eta<=1/m`. Moreover `p>=1/m`, and every coordinate is at most `1/2`; hence the first slot forces `D>=1/2`.

The total number `R` of relay slots satisfies `R<=a eta N+aD`. Deleting relay slots leaves at most `2R+2` runs, as before. A projected run spans an interval with no occurrence of the other active mode, so it contains at most `2D/p<=2mD` active symbols. Therefore

```
N-R <= 4mD(R+1),
(1-a eta)N <= 4ma eta N D + 4maD^2 +(a+4m)D.
```

Since `1-a eta>=2/m` and `D>=1/2`, define `C_m=4ma+2a+8m` to obtain

```
(2/m)N <= 4ma eta N D + C_m D^2.                         (5)
```

At least one term on the right is at least `N/m`. Consequently,

```
D >= min{1/(4m^2 a eta), sqrt(N/(m C_m))},                (6)
```

using the infinity convention at `eta=0`. This proves the uniform lower order bound. QED.

This theorem turns the qualitative boundary warning into a quantitative one. A positive mass floor helps only once it exceeds the square-root scale. It does not establish that imposing a floor is a good optimization policy: a floor can exclude an optimal relaxed control and can increase its objective substantially.

## Contracting dynamics do not remove the obstruction

Consider the stable diagonal system

```
x_i'(t) = -lambda x_i(t) + u_i(t),   lambda>0,
```

with the same initial state for a relaxed trajectory `x^alpha` and a pure trajectory `x^w`. Let `e=x^w-x^alpha`, `q(t)=int_0^t (w-alpha) ds`, and `E=max_i,t |e_i(t)|`. Then

```
e_i(t) = q_i(t)-lambda int_0^t exp(-lambda(t-s))q_i(s) ds,
q_i(t) = e_i(t)+lambda int_0^t e_i(s) ds.
```

It follows that

```
h D(alpha,w)/(1+lambda T) <= E <= 2 h D(alpha,w).         (7)
```

For fixed `lambda,T`, the classifications in Theorems 1 and 3 therefore also hold for worst-case uniform state approximation error. In particular, a common exponential contraction rate does not recover an `O(h)` bound when the transition graph has a missing arc.

There is also an upper bound independent of the horizon. Use the full-block construction from Theorem 1 with physical block duration `b=Bh` and per-block net coordinate error bounded by `a=(L+1)h`. The local primitive in each block has absolute value at most `b`. Integration by parts on a completed block bounds its state-error increment by `a+b(1-exp(-lambda b))`. Propagating completed-block increments and summing a geometric series gives at most `a/(1-exp(-lambda b))+b`. The contribution of the current partial block is at most `b`, since the input difference has absolute value at most one. Hence

```
E <= 2Bh + (L+1)h/(1-exp(-lambda Bh))
  <= 2Bh + (L+1)h + (L+1)/(lambda B).                    (8)
```

Choosing `B` on the order of `sqrt((L+1)/(lambda h))`, with `B>=L`, yields `E=O_G(sqrt(h/lambda)+h)` independently of `T`. This statement is limited to the specified diagonal filter; it is not a general theorem for nonlinear contracting dynamics.

The lower bound can also be phrased as an objective gap, rather than only a rounding metric. Set the reference state equal to the relaxed trajectory for the constant witness and minimize uniform tracking error. The relaxed optimum is zero. Every graph-feasible pure control has the error lower bound in (7), so the best pure objective has the corresponding gap. This is already a mixed-integer linear dynamic model, which is a subclass of MINLP; no nonlinear state-equation claim is needed.

## What this could enable

The proved consequence is a uniform accuracy barrier for a common relaxation-and-rounding pipeline, not a lower bound on every MINLP algorithm. To obtain physical error `epsilon` on a fixed horizon, worst-case graph-constrained rounding may require grid step on the order of `epsilon^2`; unrestricted rounding requires only order `epsilon`. This distinction can change the number of binary time variables materially.

A transition-aware relaxation might avoid the bad boundary mixture by reserving relay occupancy, or an adaptive algorithm might detect when a relaxed support lacks the necessary direct transitions. The interior theorem gives one sufficient certificate for a first-order rate. These are plausible algorithmic uses, not established speedups. A usable solver method still needs a practical transition-aware relaxation, useful constants, dynamics-specific error propagation and comparison against existing CIA shortest-path and branch-and-bound methods.

The filter example is an idealized model of modes feeding stable inventories, thermal states or actuator filters. No assertion is made that every such application has exactly these dynamics or accepts the same transition semantics.

## Prior results, novelty and verification

See [the primary-source audit](graph-rounding-literature.md). The closest sources already formulate transition restrictions in CIA and allow combinatorial restrictions in shortest-path rounding. In particular, Robuschi, Zeile, Sager and Braghin, *Multiphase Mixed-Integer Nonlinear Optimal Control of Hybrid Electric Vehicles* (Automatica, 2021), [open manuscript](https://optimization-online.org/wp-content/uploads/2019/05/7223.pdf), Assumption 5 assumes a first-order CIA bound; Remark 6 explicitly identifies this as critical when transition or dwell constraints are present. Theorem 1 identifies a fixed-graph setting where that bound fails uniformly. Their model also includes phase and physical dwell-time conditions beyond the present graph model. Their inspected results do not supply the topology-dependent uniform exponents proved here. That bounded search does not establish novelty. The model, unrestricted rounding and stationary graph occupation mechanisms must be credited to existing work.

The candidate was checked by [an independent adversarial proof review](graph-rate-review.md). The main script [check_graph_rounding.py](check_graph_rounding.py) performs exact finite dynamic programming for the half-`u`, half-`v` witness on complete, directed-cycle, bidirected-path and one-way graphs, at `N=8,16,32,64,128`. It also checks constant interior targets at `eta=1/32,1/8,1/3`, for `N=16,32,64,128`, and checks inequality (5). Its output is [graph_rounding_checks.json](graph_rounding_checks.json). The command actually run was:

```
python research-20260928/applications/check_graph_rounding.py > research-20260928/applications/graph_rounding_checks.json
```

It passed. This checks finite witness instances and inequalities (3) and (5), not the asymptotic theorem, every graph or floating-point differential-equation integrations. Only topic-targeted checks were run; no project-wide checks or CI inspection were performed. Lean verification has not been attempted.

## Limitations and next questions

The graph is fixed, all self-loops are allowed, and initial mode is free. Constants can grow with graph size. The upper construction is intentionally simple and its leading constants are not known to be optimal. A specified initial mode, a fixed positive dwell time, time-varying transition graphs and forbidden self-loops need separate treatment.

Theorem 3 settles the order of the transition for a uniform mass floor. A more consequential next question is a less conservative bound using the actual support geometry and separate mode mass budgets. Another question is whether adding explicit relay-budget inequalities to a relaxation produces useful first-order certificates without making the continuous relaxation as difficult as the original switching problem. No result here settles those questions.
