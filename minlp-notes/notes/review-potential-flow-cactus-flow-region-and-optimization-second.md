# Second independent audit of cactus flow regions and optimization

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-cactus-flow-region-and-optimization.md) correctly distinguishes an exact polynomial-time optimizing resistance scenario from exact comparison of its scalar value. Its parallelotope description, finite-set convex hull, endpoint recovery, additive estimate, and explicit Square-Root-Sum reduction pass independent review. Novelty of the geometry and circuit interpretation remains a source-audit question.

## 1. Exact scalar intervals and independence

With fixed balanced nominations, all bridge flows are fixed cut sums. Each cycle receives fixed effective nominations from its attached components. Orienting that cycle consistently gives `x_e=q+d_e`, where the offsets are rational and independent of resistance choices in every block. Its single consistency equation is a strictly increasing continuous function

```
H_beta(q)=sum_e beta_e(q+d_e)|q+d_e|.
```

The pointwise minimum and maximum over independent endpoint intervals can be selected term by term, exactly as written. For `H_min`, the lower resistance is selected on a positive flow and the upper resistance on a negative flow; the opposite choices define `H_max`. Each resulting summand is itself continuous and strictly increasing, so the two sums each have one zero. Their limiting signs at the infinities are opposite.

For every allowed scenario, `H_min<=H_beta<=H_max`, which gives `q_min<=q_beta<=q_max` with the stated ordering of roots. At either extreme root, independently choose resistance endpoints attaining the required summands. The resulting physical cycle equation is zero at that root, proving exact endpoint realization. This argument applies to interval endpoints and to the smallest and largest elements of each finite set.

The rational breakpoints `-d_e` separate quadratic pieces. Duplicate breakpoints cause no problem. Evaluating the envelope at these breakpoints locates its root; if it is not a breakpoint root, it lies on a nonconstant quadratic or linear piece. A constant nonzero-width piece is ruled out by strict increase. In fact all roots lie between the smallest and largest breakpoints, so no unbounded search is needed. The exact roots have degree at most two and polynomial coefficient encoding length. Comparing a root with rational breakpoints determines an attaining endpoint vector using only local algebraic comparisons.

Different cycle blocks have disjoint resistance sets and fixed effective nominations, even when they share articulation vertices. Each can therefore choose its circulation independently. Their cycle equations together are sufficient for the full vector of drops to be a potential gradient. This verifies that the product construction does not hide coupling through articulation potentials.

## 2. The entire region and the finite-set hull

For interval choices, a cycle circulation is a continuous scalar function of a connected compact resistance box. Its image is a connected compact set containing its minimum and maximum, hence exactly their closed interval. Combining independent blocks yields the displayed affine box image.

The signed cycle columns have disjoint edge supports, so they are linearly independent. The affine image is a parallelotope in the conserved-flow space, with reduced dimension when some circulation intervals are singletons. Any rational spanning-tree particular flow can be used, with consistent corresponding offsets and circulation coordinates.

For finite resistance sets, each cycle has a finite attainable circulation set containing those same two extremes. Its convex hull is their interval. Block independence makes the global circulation set the Cartesian product of the local finite sets, and the convex hull of this product is the product of the scalar convex hulls. Affine mapping preserves the equality. In particular every vertex of the interval flow region is realized by a simultaneous endpoint resistance scenario belonging to the original finite product.

For a continuous convex function on the flow region, a point is a convex combination of parallelotope vertices and its function value is bounded above by some vertex value. Thus a worst-case endpoint scenario exists. This conclusion also applies to the finite scenario set because it contains all those vertices. It is a structural vertex principle, not an algorithm for maximizing a general convex function over a box of growing dimension.

## 3. Exact resistance scenarios and additive values

A rational linear objective takes the form `C+sum_C A_C q_C`, with rational coefficients. Its maximizing circulation endpoint in each block is determined solely by the sign of the rational `A_C`. Each attaining resistance is a rational input endpoint recovered by the local root comparisons above. There is no need to compare sums of radicals or to enumerate combinations of block endpoints. Arbitrary bridge resistances and arbitrary choices on zero-coefficient cycles do not affect optimality. Consequently the claimed exact optimizing resistance vector is polynomial-time computable even when the number of cycles grows.

The associated flow on an edge is either a rational bridge flow or a rational shift and sign of one degree-at-most-two circulation. Its coordinatewise quadratic encoding is therefore polynomial in total size. The theorem correctly avoids promising one polynomial-degree common field for all coordinates or for the scalar objective. It also does not promise polynomial-size exact potentials obtained by summing drops across many blocks.

For value error `epsilon`, approximating every selected circulation within `epsilon/[2(1+sum_C |A_C|)]` makes the total weighted error less than `epsilon/2`. The rational constant is computed exactly. Quadratic root isolation or rational bisection on the strictly increasing envelope gives the requested local precision in polynomial time in coefficient size and accuracy bits. Rational magnitudes of the coefficients and intervals enter logarithmically through their binary encodings. Thus the stated additive value estimate is justified.

For a rational candidate flow, conservation and separate membership of its circulation coordinates in the computed quadratic intervals give exact polynomial-time membership in the interval region. The generic observation about arbitrary graphs is also correct: once a rational flow is fixed, each `x_e|x_e|` is rational, so cycle consistency is linear in interval resistance variables. This observation does not itself imply convexity of the union of all feasible flows on a general graph.

## 4. Exact scalar comparison and the radical gadget

In triangle `i`, the direct resistance is `a_i` and the total alternate-path resistance is one. Unit through-flow and equal drops give positive direct flow

```
x_i=1/(1+sqrt(a_i)).
```

For `a_i>1`, multiplying by the positive integer objective coefficient `a_i-1` gives exactly `sqrt(a_i)-1`. A chain of vertex-disjoint triangles joined by bridges has unit through-flow through every block. Its weighted flow objective is therefore `sum_i sqrt(a_i)-m`, and its weak upper comparison with `K-m` is exactly the explicitly defined weak `<=` Square-Root-Sum predicate. Equality is preserved; no complement convention is substituted.

Removing unit radicands subtracts their count from the source threshold. If no terms remain, the remaining comparison is rational and can be decided before output. If the adjusted threshold is negative while terms remain, the formula itself already represents a no instance, or a fixed no output may be used. Other trivial cases can likewise be handled by rational comparisons.

The fixed output triangle has direct resistance eight and alternate resistances one and one, so its direct flow is `1/3`. Objective coefficient three makes its scalar value exactly one. Threshold one is a yes instance and threshold zero is a no instance. These outputs belong to the same positive-integer, unit-nomination, single-triangle subfamily. Multiplying all nontrivial constructed resistances by two gives integer direct resistances `2a_i`, alternate resistances one, and bridge resistance two, leaving every flow unchanged.

The graph is simple and has maximum degree three: the triangle terminals each acquire at most one connecting bridge, while the third vertex has degree two. Only the first and last terminals have nonzero nominations, respectively one and minus one. Coefficients, thresholds, and the graph have polynomial binary encoding length. The direct coefficients are positive; all other objective coefficients are zero.

The primary `<=` SRS convention was directly checked in Etessami and Yannakakis, Sections 1 and 3, during the earlier arithmetic audit. [Primary manuscript](https://www.pure.ed.ac.uk/ws/portalfiles/portal/14011363/nash_focs07_full_j_spec_issue_sub.pdf). This is SRS hardness, not ordinary NP-hardness. The construction has a single fixed resistance scenario, so it highlights exactly why selecting an optimizing scenario can be easy while exact scalar comparison remains an arithmetic problem.
