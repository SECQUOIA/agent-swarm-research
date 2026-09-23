# Second independent review: discrete arc-capacity hardness

Date: 2026-09-05. Reviewer: `benders_property`, independent of the author and first reviewer. Reviewed [the discrete arc-capacity candidate](potential-flow-discrete-arc-hardness.md), including the final choice `D=ceil(10000/Delta)` and its NP/coNP membership section, against the previously reviewed pressure gadget and exact continuous-box arc algorithm.

**Verdict: pass.** The reduction establishes NP-completeness of possible strict upper arc-capacity violation and coNP-completeness of robust capacity satisfaction on the stated rank-three graph class. Its encoded gap also establishes hardness of additive worst-flow optimization with polynomial dependence on requested precision bits. No strong NP-hardness or fixed-accuracy hardness follows. Literature priority remains separate.

## 1. Added-edge graph and nomination signs

The pressure gadget has a biconnected theta block of cycle rank two and the bridge `4->1`. Adding `4->0` turns the path `1-4-0` into an ear with distinct endpoints in that theta block. An ear addition preserves biconnectivity and increases cycle rank by one, so the entire resulting graph is one rank-three block. It remains simple. Vertex 0 has degree three, vertex 4 degree two, and every other degree is unchanged and at most three.

For new-edge flow `t` oriented from 4 to 0, deleting that edge decreases the required old-network outflow at vertex 4 by `t` and increases it at vertex 0 by `t`. Hence the old-network nomination vector is exactly `b+t*e_0-t*e_4`. The sign in the scalar equation `F(t)=M*t*|t|` is correct.

Physical existence and uniqueness hold for the full graph and every old-network balanced nomination vector under positive quadratic resistances. Thus the scalar equation is justified by the actual physical state, without needing to assume its solution in advance.

## 2. Monotonicity and uniform perturbation control

The finite state-comparison identity in equation (2) is correct. Every summand on its right is nonnegative, and their sum is strictly positive for different nomination vectors: otherwise strict monotonicity would make every flow coordinate equal, contradicting conservation. Its left side is `-(t-s)(F(t)-F(s))`, which proves that `F` is strictly decreasing. No differentiability at zero or inverse Jacobian estimate is needed for this conclusion.

Because the previously reviewed pressure gadget gives `F(0)>5/6`, a nonpositive new-edge flow cannot solve the scalar equation. Consequently `t>0` and `M*t^2=F(t)<=F(0)<=1`. Since `H=1-Delta/2>=1/2`, the bound `t<=2/D<1` follows. This is uniform over all discrete resistance choices, including very large effective cross resistance.

For the nomination Lipschitz step, both old-network input vectors belong to the box with node-0 interval `[4,5]`, node-4 interval `[0,1]`, and all other nominations fixed. Its sum of maximum absolute coordinates is 17, so the draft's bound 18 is safe. The undirected objective path `4-1-2-0` uses only fixed edges and has total resistance `11/3`. Reversing traversal direction on two edges does not change the positive derivative-resistance bound. Thus the reviewed pressure Lipschitz constant `2*18*(11/3)=132` applies independently of the cross-path choices.

The nomination difference has l1 norm `2t`. Therefore the claimed pressure loss satisfies

```
0 <= F(0)-F(t) <= 264t <= 528/D
                           <= (528/10000)Delta < Delta/8.
```

The ceiling in the definition of `D` preserves the inequality. This closes the perturbation estimate without a hidden coefficient depending on the Subset-Sum weights.

## 3. Strict capacity threshold and gap

The new resistance and capacity satisfy `M*c^2=H`. A target-subset scenario has `F(t)>1-Delta/8>H`, so `t>c`. Every non-target scenario has `F(0)<=1-Delta`, by the pressure gadget's integral subset-sum gap; monotonicity then gives `F(t)<H`, so `t<c`. This applies to non-target scenarios even when some other scenario is a target subset.

In a target scenario, `F(t)-H>3Delta/8`; in a non-target scenario, `H-F(t)>=Delta/2`. Both flows are positive. Since `t+c<=3/D` and `M<=D^2`, the exact difference-of-squares identity gives a separation stronger than the stated safe bound:

```
|t-c| = |F(t)-H| / (M*(t+c))
       >= Delta/(8D) >= 3Delta/(32D).
```

Thus no constructed scenario can sit on or cross the wrong side of the rational threshold through the perturbation error. In a yes instance, the maximum new-edge flow exceeds the threshold by the gap; in a no instance, all scenarios remain below it by the gap. An absolute objective error below `Delta/(64D)` distinguishes the cases. A sufficiently accurate near-optimal discrete scenario also decides the source instance by checking its selected item sum directly.

Robust upper-capacity satisfaction is the complement of existence of a strict violation, so it corresponds to a **no** Subset-Sum instance. Other capacities can safely be `[-16,16]`: the full fixed nomination vector has total absolute magnitude 16, and the acyclic passive-flow bound applies independently of all resistance values. The new edge may use lower bound `-16` and upper bound `c`.

## 4. Encoding and integer resistance scaling

With `A=31K+18S`, `Delta=6/A^2` and `D=ceil(10000*A^2/6)` have polynomial binary encoding length. So do `H=(A^2-3)/A^2`, `M=H*D^2`, the capacity, and the gap. The graph size is linear in the item count. The precision requirement has `O(log(K+S))` bits up to fixed constants; it is not an inverse-polynomial additive gap in the input length.

The common scaling factor `6nK*A^2` makes all old resistance options integers and makes the new resistance exactly `6nK*(A^2-3)*D^2`. These integers retain polynomial encoding length. Scaling every resistance multiplies every potential by the same factor but leaves every flow unchanged. Therefore the flow capacity `1/D` and its flow separation remain unchanged. This verifies the stated integer-resistance strengthening.

## 5. Membership without an algebraic witness assumption

The NP certificate can consist solely of one index in each explicitly listed finite resistance set. Its length is polynomial in the explicit input size. After fixing those choices, the exact fixed-resistance arc algorithm applies at fixed maximum block rank and determines whether any nomination in the balanced rational box violates a capacity. It compares algebraic extrema with rational bounds exactly, including strict inequalities. No finite rational encoding of an exact physical state needs to be guessed.

If the nomination box is empty, this can be checked first by rational LP, giving no possible violation and vacuous robust satisfaction. Otherwise the exact algorithm's nonempty-box hypothesis is met. For a validator with many capacities, run it for each edge and take the disjunction of violations; the number of calls is polynomial. Accordingly possible violation is in NP and robust satisfaction is in coNP. Combining membership with the rank-three reduction proves the claimed complete classifications.

This verifier relies on the independently reviewed **arc** algorithm. It does not transfer to arbitrary pressure differences across many blocks, where exact arithmetic has a separate obstruction. Explicitly listed finite choices are also material; no succinctly encoded family of resistance values is silently included.

## 6. Independent physical checks

The [second-review physical checker](../code/potential_flow_mpd/discrete_arc_second_review_checks.py) independently solves all three cycle equations of the final graph. It uses scaled new-edge flow `D*t` to avoid numerical loss from the small capacity, and 70-digit arithmetic. Across 378 scenarios from 18 deterministic Subset-Sum instances, it checked root signs, the pressure perturbation, the strict threshold, the claimed flow gap, and exact integer scaling. All passed; the largest cycle-equation residual was `3.04e-66` when rounded upward.

These computations supplement the exact proof; they are not certified interval solutions or an implementation of the NP verifier. Run with `python code/potential_flow_mpd/discrete_arc_second_review_checks.py` in an environment containing mpmath.
