# Second independent audit of unbounded-rank series-parallel arc hardness

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`, independent of
the author and first reviewer.

Reviewed: [the unbounded-rank arc obstruction](potential-flow-unbounded-rank-arc-obstruction.md),
including the primary pressure-hardness import and its quantitative gap.

**Verdict: PASS.** The probe transfers the established pressure gap to
signed arc-flow optimization with fixed resistances and continuous nomination
boxes on series-parallel graphs. The NP-hardness, robust coNP-hardness,
and high-precision additive obstruction follow. No NP/coNP membership or
hardness at fixed block rank follows from this argument.

## Primary-source verification

I directly inspected [Thürauf's manuscript](https://optimization-online.org/wp-content/uploads/2020/05/7803-1.pdf):
the model and equation (2), printed pages 5–7; Figure 2 and equation (3),
page 10; Lemma 4.3, pages 11–12; and Lemma 4.17, page 24.
The stated graph, resistance values, and booking bounds match. Converting
entry/exit quantities to signed nominations gives exactly a rational box
intersected with balance. Equation (2) includes conservation and quadratic
laws but explicitly excludes the potential bounds. Lemma 4.3 supplies
value at least one for yes instances; Lemma 4.17 gives the stated strict
upper bound below one for no instances, including negative flows.
The source assumes at least three positive items, a harmless restriction.
Thus this is a valid unrestricted pressure-gap input, not a transfer from
a differently constrained booking-feasibility problem.

## Rational gap and bit length

The source's maximum expressions involve only fixed-degree rational
arithmetic and exact comparison. Their gap can also be simplified directly.
Write

```
eps=1-(1-1/(8K^2))^2.
```

For `K>=1`, one has `0<eps<1/4`. The difference between the second and
first entries of the source's first maximum is
`eps-eps^2*(1+1/K^2)>0`. Consequently its selected value is
`M0=1-eps^2/K^2`, and its next auxiliary quantity is
`eps_tilde=eps^2/(5K^2)`. The second maximum selects
`1-eps_tilde^2/(K^2*n^2)`, because
`0<eps_tilde<1<=K^2*n^2`. Hence

```
gamma=1-T=eps^4/(25K^6*n^2)>0.
```

This optional simplification confirms, without approximating radicals,
that the threshold and gap are rational and have bit length
`O(log K+log n)`. The candidate's use of the original maximum expressions
is equally valid. The notation `T(K)` follows the source even though its
formula also contains the number of items.

## Graph class and physical scenario domain

Adding the direct `s-t` edge creates another parallel branch alongside the
existing two-edge `s-t` branches. The main block is therefore two-terminal
series-parallel. Every pendant exit attaches at a single vertex and creates
only a bridge.

An explicit tree decomposition has bags `{s,t,z_i+}` joined along their
common pair `{s,t}`, with pendant bags `{z_i+,z_i-}` attached to the
corresponding main bag. Its width is two. The graph contains a triangle,
so its treewidth is exactly two. The main block has `n+2` vertices and
`2n+1` edges, hence cycle rank `n`. The total number of independent cycles
in that one block is unbounded; no fixed-block-rank theorem is contradicted.

All resistances, including the new one, are fixed positive rational data.
The original balanced nomination box is unchanged by adding the edge.
Only this nomination vector is optimized. Capacity tests are subsequently
applied to its unique unrestricted passive state. The auxiliary perturbed
nomination used in the proof is not a new feasible scenario requirement.

## Probe orientation, monotonicity, and signs

Denote the new edge's signed flow temporarily by `z` to distinguish it
from the terminal named `t`. Deleting the edge oriented `s->t` changes
the induced old-network nomination to

```
b(z)=b-z*e_s+z*e_t.
```

The signs are correct: the old outgoing flow at the source decreases by
`z`, and its old net outgoing flow at the sink increases by `z`.
Restricting the physical state therefore gives the old-network potential
difference `F_b(z)` and the exact equation `F_b(z)=M*z*|z|`.

For distinct `y,z`, strict constitutive monotonicity gives a positive
inner product of the flow difference with the constitutive-gradient
difference. Conservation rewrites it as
`-(z-y)*(F_b(z)-F_b(y))`. Distinct nominations force distinct flows, so the
inequality is strict. Thus `F_b` is strictly decreasing.

If `F_b(0)>0`, the new flow must be positive; otherwise its potential
equation would equate a positive quantity with a nonpositive quantity.
If `F_b(0)<=0`, the new flow is nonpositive, with equality permitted only
when the old drop is zero. Such a flow cannot violate the positive upper
capacity. For positive new flow, `F_b(z)<=F_b(0)`.

## Uniform bound and yes-instance preservation

The original nomination box has total absolute bound `3K`. Acyclicity of
the physical flow orientation gives `|x_e|<=3K`. Because the items are
positive integers, either two-edge main path has resistance sum at most
two. Summing its absolute drops gives the safe bound
`|F_b(0)|<=18K^2=:U`.

Set `H=1-gamma/2`, `M=H*D^2`, and
`D=ceil(1000K(3K+2)/gamma)`. Then `1/2<H<1`. For a yes-instance nomination
with original pressure at least one, its new flow is positive and satisfies

```
z<=sqrt(U/M)<=6K/D<1.
```

The original and induced nominations lie in an enlarged box of total
absolute bound at most `3K+2`: only the source's lower endpoint and the
sink's upper endpoint need enlargement by one. The induced nominations
may reverse an entry/exit sign, which is harmless for the auxiliary
unrestricted passive state and the general signed-nomination sensitivity
bound. The source pressure lemma is applied only to original nominations.

The same two-edge path gives Lipschitz coefficient at most `4(3K+2)`.
Since `||b(z)-b||_1=2z`,

```
0<=F_b(0)-F_b(z)<=8(3K+2)z
 <=48K(3K+2)/D<=0.048*gamma<gamma/4.
```

Consequently `F_b(z)>1-gamma/4>H=M/D^2`, and `z>1/D`.
For a no-instance nomination, a nonpositive new flow satisfies capacity
directly. If it is positive, decrease gives `F_b(z)<=F_b(0)<T<H`, so
`z<1/D`. This proves the required existential equivalence.

## Additive flow separation

The capacity `c=1/D` corresponds exactly to pressure `M*c^2=H`.
For a yes witness the pressure margin exceeds `gamma/4`, and

```
M*(z+c)<=D^2*(6K+1)/D=(6K+1)D.
```

Rationalizing the difference gives the valid common lower gap

```
g_arc=gamma/[4(6K+1)D].
```

For a positive no-instance flow, its pressure is less than `T<1`, so
`z<2/D`. Its pressure deficit below `H` exceeds `gamma/2`, and its flow
deficit is at least `gamma/(6D)`, which dominates `g_arc` for `K>=1`.
A nonpositive flow has deficit at least `1/D`, which also dominates it.
Thus the maximum new-edge flow is at least `c+g_arc` in a yes instance
and at most `c-g_arc` in a no instance.

The integer `D`, rational resistance `M`, capacity, and arc gap all have
polynomial binary encoding length. A dyadic tolerance smaller than
`g_arc/3` therefore requires polynomially many precision bits. A certified
value interval or absolute-error approximation at that tolerance separates
the two cases by comparison with `c`.

## Capacity conventions and complexity scope

All physical flows in the new graph, at original nominations, remain
bounded by `3K`. Assigning capacities `[-3K,3K]` to every other edge
therefore adds no restriction. For the target edge an upper bound `c`
and a harmless lower bound `-3K` isolate the desired signed test.

Existence of a violating nomination is NP-hard, and satisfaction for all
nominations is coNP-hard by complementing the same reduction. This does
not show membership in NP or coNP for unbounded block rank: neither a
short rational physical-state certificate nor a polynomial exact verifier
has been established in that class. The proof also does not establish
strong hardness, exclude an FPTAS, or give hardness at fixed block rank.

The pressure reduction and its gap must be credited to Thürauf. The
additional contribution checked here is the quantitative probe conversion
that preserves the series-parallel graph class and yields an arc objective.
Whether that corollary already appears in the literature remains a separate
novelty question.

## Added explicit yes-witness check

The subsequently added closed form also checks. Put `r=z/K`. On one
balanced Partition class, the two main branch flows are
`S_i*(1-r)` and `-S_i*r`; on the other class their order is reversed.
Their signed-quadratic path drop is exactly `1-2r` in both cases.
Each class has total weight `K/2`, so the total old source flow is
`K/2-z`, as required after adding the probe. The positive root obeys
`0<z<K/2`, justifying the signs in these formulas, and satisfies

```
M*z^2+2*z/K=1,
z=1/(sqrt(M+1/K^2)+1/K).
```

This establishes the claimed full-network witness formula including the
sign changes from previously zero branch flows. I reran the 110-digit
checker: all 24 constructed yes states passed conservation, branch laws,
probe laws, and the stated gap bounds. These checks concern explicit yes
witnesses; the universal no-case bound remains the primary-source theorem.
