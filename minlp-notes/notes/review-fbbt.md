# Independent audit of monotone-system FBBT hardness

Date: 2026-09-04. Reviewer: independent `review_fbbt` agent.

Status: the core mathematical transfer and the explicit restricted hardness construction in `results/fbbt-monotone-system-hardness.md` pass independent mathematical review, subject to the minor wording clarifications recorded below. Novelty is not certified by this audit.

## The convergence argument

Let `P` be a finite vector of polynomials with nonnegative coefficients, and suppose its Kleene limit `q = lim_k P^k(0)` is finite and belongs to the initial box `[0,1]^n`. Continuity gives `P(q)=q`. Consider nested boxes `[l^t,u^t]` produced by sound contractors, with `l^0=0`. Suppose, for each defining row `i`, the forward update

`l_i <- max(l_i, P_i(l))`

is applied infinitely often using the current bounds. Other sound tightening steps can be interspersed arbitrarily.

Soundness retains the feasible point `q`, so `0 <= l^t <= q <= u^t`. The increasing lower endpoints have a limit `l* <= q`. On a subsequence of times at which row `i` is updated, continuity gives `l*_i >= P_i(l*)`. Hence `P(l*) <= l*`. Induction gives `P^k(0) <= l*` for every `k`; taking the limit gives `q <= l*`. Therefore `l*=q`.

This proof addresses several possible objections:

- Reverse propagation cannot invalidate the result: a sound update cannot raise a lower endpoint above the feasible point `q`.
- Self-dependencies cause no problem. The proof does not assume that a defining variable is absent from its own right-hand side.
- Arbitrary fair schedules suffice; bounded gaps between row visits are unnecessary. Stale asynchronous reads require a separate eventual-freshness assumption.
- The proof uses a post-fixed upper bound on the Kleene sequence, `P(l*) <= l*`; it does not assume that every contractor is continuous or that its limit box is its own fixed point.
- `P` need not map the entire initial cube into itself. Only the least fixed point must lie in it.
- The equality model has a feasible point throughout. An argument based only on absence of detected infeasibility would be insufficient.
- Fixed numerical tolerances and fixed-precision rounding are outside this exact-arithmetic assertion.

For a primitive decomposition, apply this same argument to the enlarged nonnegative polynomial defining map. This avoids assuming that a complete original expression is evaluated in a single primitive visit.

## Source theorem checked

The primary source is Etessami and Yannakakis, *Recursive Markov Chains, Stochastic Grammars, and Monotone Systems of Nonlinear Equations*, JACM 56(1), 2009, Theorem 5.2. The [author-hosted manuscript](https://homepages.inf.ed.ac.uk/kousha/final_rmc_jacm_version.pdf) states a polynomial many-one reduction from PosSLP to distinguishing termination probability at most `epsilon` from probability one, for every fixed positive `epsilon`. Its proof explicitly constructs that reduction. It also states SQRT-SUM many-one hardness, while omitting that direct construction and giving a Turing-reduction route through PosSLP.

Consequently, an explicit restricted construction from PosSLP establishes PosSLP many-one hardness and SQRT-SUM Turing hardness for those restrictions. The stronger SQRT-SUM many-one wording requires a separate restricted reduction or further justification. The unrestricted source statement alone does not transfer all restrictions of the PosSLP construction to its omitted SQRT-SUM construction.

## Required scope distinctions

- Coefficients `{0,1/2,1}` mean coefficients of the oriented right-hand sides. Moving all terms to the left introduces negative coefficients.
- A constant bound on SCC size means SCCs of the directed defining-map dependency graph. It does not establish bounded treewidth, bounded undirected component size, or bounded SCCs of the graph of bidirectional propagation rules.
- PosSLP hardness concerns binary/Turing computation. It does not rule out a short computation in a unit-cost model with exact arithmetic on arbitrarily large integers or rationals.
- A constant absolute-error approximation to a designated limiting endpoint is distinct from approximating the residual of one FBBT sweep. Tiny residuals need not certify proximity to the limiting endpoint.
- The result concerns continuous feasible bilinear systems, a subclass of MINLP. It does not need an integrality restriction.

## Audit of the direct restricted construction

The full draft was checked independently after its arrival.

1. **Layer normalization.** Alternating homogeneous layers can be obtained in polynomial size. Assign each original gate a suitably typed layer after all its predecessors, and fill skipped layers by addition of zero or multiplication by one. Maintain integer zero and one gates in each layer. This preserves both integer outputs and gives them a common scaling denominator.
2. **Scaled gate values.** The recurrence `M_new=2M_old` on addition layers and `M_new=M_old^2` on multiplication layers is correct. Induction gives all scaled values in the unit interval and `M_L <= 2^(2^L)`.
3. **Complements.** The equations `p_new=p_j*p_k`, `v=p_j*r_k`, `r_new=r_j+v` correctly produce `r_new=1-p_new`. Each new coordinate is in `[0,1]` at its fixed value. The map need not preserve the whole cube away from the fixed point.
4. **Sign detector.** For `c+d=1`, the roots of `a=d+c*a^2` are one and `d/c` when `c>0`. The minimum is one for `c<=1/2` and `d/c` for `c>1/2`, with the `c=0` endpoint handled directly. For the positive integer difference `Delta=U-V`, the gap `1-a*=2*Delta/(M+Delta) >= 1/M` is correct.
5. **Small constant.** Starting at one half and squaring `L+2` times gives exactly `b=2^(-2^(L+2))`. The bound `bM<=1/8` follows for `L>=1`. The representation length is polynomial although a fully expanded denominator would be huge.
6. **Amplification.** With `e=(1-b)a`, the equation `z=b+ez` gives `z=1` at `a=1`, and `z<=b/(1-a)<=1/8` at the smaller detector root. Approximation error one quarter gives separated intervals, at most `3/8` versus at least `3/4`.
7. **Full-system minimum.** The displayed assignment is a nonnegative fixed point in the cube. Its existence bounds the global Kleene least fixed point. Since that least fixed point cannot select a detector root below `a*` and is bounded above by the displayed assignment, it selects `a*`; the remaining coordinates are then determined. This supplies a short completely global justification. Merely citing monotonicity of `z(a)` on `[0,1]` is less explicit when claiming leastness among all nonnegative fixed points.
8. **Sparsity.** The copied quadratic detector uses precisely four mutually dependent variables. The amplifier uses two. Every other component is acyclic. Copying equal product inputs introduces no additional cycle outside the explicitly counted detector. Every primitive equation has at most three distinct variable names.
9. **Feasible-set size and rationality.** The constructed unit-cube feasible set has at most two points, all rational. The upstream DAG uniquely fixes rational values. The detector roots are one and `d/c`, with `c=0` treated directly. Every root in `[0,1]` uniquely determines its auxiliaries and the amplifier. Thus there is one feasible point when `U<=V`, and exactly two when `U>V`. This restriction follows without any extra construction. In particular, testing uniqueness on these promised instances also decides the PosSLP comparison.

No mathematical counterexample was found. A prose sentence claiming that hardness “rules out an unconditional extension” should be weakened: polynomial-time approximation would imply `PosSLP in P`, which is a major open consequence, not a proved impossibility.

## Audit of the companion iteration lower bound

The companion construction uses an acyclic paired-square circuit to fix `b=2^(-2^n)` and `c=1-b`, followed by two primitive rows `w=c*z` and `z=b+w`. It has a unique solution with `z=1`. Standard interval-hull propagation on these two separate rows needs at least `1/(2b)` applications that update the lower bound of `z` through the affine row before that bound reaches one half.

It is enough to prove this after giving the algorithm the exact singleton bounds for all upstream circuit variables for free, together with `upper(z)=1` and `upper(w)=c`. Exact primitive hull contractors are monotone with respect to box inclusion, so this strengthening can only accelerate tightening relative to the original initial cube under the same schedule.

Write the lower endpoints as `l_z,l_w`. The invariant `l_w <= c*l_z` holds initially. A forward product update preserves it with equality. A reverse affine update can only raise `l_w` to `l_z-b`, and

`l_z-b <= (1-b)*l_z = c*l_z`

because `l_z<=1`. A forward affine update only increases `l_z`, preserving the invariant. Therefore the reverse product update `l_z <- max(l_z,l_w/c)` never increases `l_z`. Upper endpoints remain at their exact values. Only the forward affine update can increase `l_z`, and it satisfies

`l_z(new) <= b+c*l_z(old)`.

After `N` such applications, induction gives

`l_z <= 1-(1-b)^N <= N*b`.

Hence reaching one half requires `N >= 1/(2b) = 2^(2^n-1)`. Exact hull computation for each individual row, including its reverse effects, does not defeat the lower bound.

This statement must explicitly retain the two-row primitive formulation and the specified local contractors. Eliminating `w` and solving the combined linear equation `z=b+c*z`, or contracting the whole two-row component jointly, gives `z=1` immediately once `b,c` are known. Thus the iteration bound is an algorithmic result about primitive FBBT, not a lower bound for every sound tightening method. The constant-error endpoint-computation hardness theorem above has a different, conditional scope.

## Literature cross-check

Targeted searches included `bound propagation PosSLP`, `bounds consistency square root`, and `interval propagation monotone polynomial`. No directly matching continuous FBBT hardness result appeared in these searches. This is search evidence, not a novelty proof.

Belotti, Cafieri, Lee, and Liberti's *On feasibility based bounds tightening* distinguishes integer bound-propagation hardness from polynomial computability of the limiting closure for continuous linear constraints. That distinction is consistent with the proposed bilinear result; it must not be described as contradicting their linear theorem. Further novelty review should use their primary manuscript and its citations.
