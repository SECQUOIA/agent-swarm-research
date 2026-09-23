# Independent audit: nonlinear power-law attainable regions

Date: 2026-09-05. Reviewer: potential_flow_review. Verdict: PASS for the
qualitative fixed-exponent statement.

I independently checked the complete argument in
[the extension candidate](potential-flow-power-law-region-convexity-extension.md).
For every fixed real `p>0`, `p!=1`, it proves the stated cactus classification
for universally convex flow regions and tree classification for universally
convex normalized potential or joint regions on connected simple graphs.
It does not give polynomial encoding bounds or settle the exponent `p=1`.
This review does not establish literature priority.

## The local theta calculation

The four outer flows satisfy conservation for nominations `(2,-2,0,0)`.
At `(a,q)=(1,0)`, the displayed outer-cycle function has

```
F_a=8p,       F_q=-5p,
F_aa=0,      F_aq=-p(p-1),       F_qq=p(p-1).
```

Implicit differentiation gives `a'=5/8` and

```
a''=-(F_aa(a')^2+2F_aq a'+F_qq)/F_a=(p-1)/32.
```

All four outer flows equal one at this reference point, so their power
functions are smooth in a neighborhood for every real `p>0`. The cross-edge
flow zero here is only a reference point of the deleted-edge problem; the
proof does not differentiate the cross-edge power law at zero or claim that
this reference state has a finite cross resistance.

The cross-terminal drop is
`P(q)=2(2-a(q))^p-a(q)^p`, with `P(0)=1`. Choose a compact sufficiently small
interval of strictly positive `q`. Then all five flows are positive,
`P(q)>0`, and `beta=P(q)/q^p` is finite and positive. Nonzero curvature
persists on this interval. Strict monotonicity of the deleted network gives
injectivity of the resistance parametrization; alternatively, locally
`P'(0)=-15p/8`, so direct differentiation of `P(q)/q^p` also gives the
required strict monotonicity for sufficiently small positive `q`.

The endpoint secant in the `(q,a)` projection has a strict interior signed
gap. Choosing the sign of its affine defining functional gives a linear
flow objective with strict interior advantage. A constant term in that
functional does not affect the comparison.

## The triangle calculation

The path flows `a,a+1` and direct flow `2-a` satisfy the displayed fixed
nominations. For `0<a<2`, all are strictly positive. The resistance formula
has a positive strictly increasing numerator and a positive strictly
decreasing denominator, so it is strictly increasing.

With the stated normalization, differentiating the two potential
coordinates gives

```
d pi_0/d pi_1=1+(a/(a+1))^(p-1).
```

Its derivative in `a` has the nonzero sign of `p-1`; the derivative of
`pi_1` is positive. Thus the potential curve has strict curvature on every
compact interior parameter interval. The linear secant objective has the
claimed interior advantage after selecting its sign. Nonconvexity of the
potential projection also proves nonconvexity of the joint region.

## Embedding and uniform restoration

In a simple theta subgraph, at most one branch-to-branch path has no
internal vertex. The other two provide the distinct internal nomination
terminals of the theta construction. Splitting the remaining links creates
only zero-nomination subdivision vertices. For the common exponent, path
resistances add because all series-edge flows are identical. The described
positive rational splitting, including reserving a fixed resistance below
the varying link's lower endpoint, is valid. Any simple cycle similarly
contains a subdivision of the triangle with three distinct vertices.

For the restoration step, let `B` be total positive nomination. Every
passive physical flow has edge magnitudes at most `B`: its positive-flow
orientation has no directed cycle, since potential drops are strictly
positive along such a cycle, and hence it decomposes into source-to-sink
flows of total value `B`. This uses strict monotonicity, not differentiability.

A selected-subgraph physical flow extended by zero is feasible on the full
graph. Its energy is uniformly bounded on the compact uncertain interval.
The full energy minimum therefore gives a uniform bound
`|x_e|<=C R^(-1/(p+1))` on every extra edge. Restricting conservation to the
selected subgraph gives nomination perturbations tending uniformly to zero.

For completeness, uniform convergence of selected flows can be proved
directly by compactness: any contrary sequence has a subsequence of bounded
flows and uncertain resistances converging to limits. Conservation converges
to the original selected nominations, and the selected cycle-law equations
pass to the limit by continuity. Strict convexity of the energy identifies
the limit with the unique selected physical flow, contradicting failure of
uniform convergence. This proof remains valid for `0<p<1`.

After normalizing at a selected vertex, each selected potential is a sum
of selected path drops. Selected resistances stay bounded and positive,
so these potentials converge uniformly too. Potentials at added vertices
need not remain bounded; assigning them zero coefficients in the preserved
objective is sufficient and avoids any unsupported global potential bound.

The strict three-setting interior advantage therefore survives for finite
sufficiently large `R`.

## The injective-coordinate conclusion and rational data

After deleting the varying cyclic edge, two different prescribed own-edge
flows give different remaining-network nominations. For their states,

```
0 < sum_f (g_f(x_f')-g_f(x_f))(x_f'-x_f)
  = -(q'-q)(P(q')-P(q)).
```

Thus `P` is strictly decreasing. The equation
`P(q)=beta sign(q)|q|^p` has either the constant zero-flow state for every
resistance or a strictly monotone own-edge flow parametrization. In the
latter case its terminal potential difference also parametrizes the curve
injectively. The preserved strict advantage excludes the constant case.

If a flow or potential curve were convex, the segment between its endpoint
states would contain a point at every intermediate value of this linear
scalar coordinate. Uniqueness above that coordinate would force the full
curve to be this segment, contradicting the interior linear-objective
advantage. This justifies using the restored advantage as a nonconvexity
certificate; the advantage alone, without the injective coordinate, would
not suffice for a higher-dimensional state image.

All inequalities used to preserve the advantage are strict. Continuous
dependence therefore allows rational perturbations of the uncertain interval
endpoints and the interior resistance setting, while maintaining their
ordering, positivity, and the advantage. A sufficiently large rational `R`
also exists. The nominations and fixed gadget resistances are already
rational. This establishes existence of rational resistance data for every
fixed exponent, including irrational exponents; it does not establish an
algorithm or a uniform bound on their encoding lengths.

## Positive graph classes

On a cactus, a fixed conserved flow plus one circulation variable per cycle
parametrizes all conserved flows. Cycle supports are edge-disjoint, so the
strictly convex energy separates over these variables and their disjoint
resistance boxes. Each cycle's continuous scalar circulation image of a
compact connected box is an interval. Independent cycle parameters therefore
give an affine product of intervals, hence a convex full flow region.

On a tree, conservation fixes the entire flow. Every edge drop is then its
fixed signed power times its resistance. Normalized potentials, and the joint
state, are affine images of the resistance box. These arguments include
zero flows and require only continuity and strict monotonicity of the laws.

The local derivative obstruction vanishes at `p=1`, so the excluded linear
case correctly remains outside the negative conclusion. No unresolved
mathematical issue was found in the claimed scope.
