# Independent audit of the series–parallel coefficient obstruction

Date: 2026-09-07. Reviewer: independent subagent `review_series_parallel`.

## Scope and verdict

The arbitrary-ratio construction in
[the candidate note](network-simplex-reopened-series-parallel.md) is correct.
The proof establishes a facet with product-coordinate coefficient ratio
\(M\) for every integer \(M\ge2\), even on a directed acyclic two-terminal
series–parallel unit-flow network with unit arc capacities. This is a statement
about the sparse hull in its original coordinates, including invariance under
adding equations from its affine hull. It is not a separation-hardness result.

The initial reviewed file had SHA-256
`57da5105f7db95d8d7d6581896ddba5d853d484ba0f0e976c6e51ff753abc4c8`.
The accepted M-family snapshot, after the correction below and the author's
computational results, has SHA-256
`aed7a3de67d2d2137001cb2758bba0ad8afedb054f4c64e01435b539e3bd5eb2`.
Later additions require separate review.

One error was found and corrected by the author: the \(M=2\) example has
**five**, not six, vertices. Its nine arcs and cycle rank five were correct.
No substantive proof error was found.

## Mathematical checks

1. **Hull semantics.** The reference model has simplex inequality
   \(\sum_j y_j\le1\), so simplex disaggregation normally includes a residual
   state. Here \(n\) explicit weights equal \(1/n\), forcing residual weight
   zero and therefore residual flow zero. Each explicit state has flow value
   \(1/n=2a\), bounds \([0,2a]\), and the stated product observations.
   No hidden original coordinate is left free: every \(x\), every \(y\), and
   every observed \(z\) other than \(u,v\) is fixed.
2. **Graph and counts.** There are \(k+2=M+3\) vertices, \(2k+3=2M+5\)
   arcs, cycle rank \(k+2=M+3\), and \(1+k(k-1)=1+M(M+1)\) observed
   products. The bypass and serial branch give one biconnected multigraph
   block. The underlying simple graph is a cycle; treewidth two and planarity
   follow. All arcs point forward, and recursive series/parallel construction
   is explicit. Parallel arcs are permitted by the original model.
3. **Aggregate point.** The two arcs in every serial gadget sum to \(p=1/2\).
   All displayed aggregate arc values lie in \([0,1]\). For example
   \(x_{a_0}=(k+1/4)/(2(k+1))<1/2\) and
   \(x_{a_i}=(k+7)/(8(k+1))<1/2\) for \(k\ge3\).
4. **Necessary inequality.** State conservation forces one common branch
   profile \(w\). The observation complements give the three displayed
   subset lower bounds. Taking \(k-1\) copies of \(S_0\) and one of each
   remaining set covers every state exactly \(k\) times. The constant terms
   cancel to give \((k-1)u+v\ge kc\).
5. **Local sufficiency.** Formula (7) sums to \(p\). In the prescribed open
   square, all profile values lie in \((7a/8,9a/8)\), all observations are
   positive and below \(a/2\), and \(0\le D<a/8\) on the proposed feasible
   side. Every displayed \(a_i\)-flow lies between zero and its profile
   value; subtraction therefore gives feasible \(b_i\)-flows. The bypass
   completes each state demand. Direct summation gives every fixed aggregate
   arc value, including gadget 1 where the two terms in \(t\) cancel.
6. **Facet inference.** The section contains a relatively open two-dimensional
   feasible set and an open boundary segment. Thus every ambient affine-hull
   equation restricts to an identity in \((u,v)\). In a finite ambient facet
   description, at a relative interior point of the segment at least one
   nonconstant restriction must be active, and it must support the same
   boundary line. Its \(u,v\) coefficients have ratio \(k-1\). Affine-hull
   modifications cannot change either coefficient because the coordinate
   plane has two-dimensional intersection with the hull. This establishes an
   actual ambient facet claim, rather than merely one valid section inequality.
7. **Integrality claim.** An acyclic unit-flow network with unit capacities has
   directed-path incidence vertices. Combining these with all simplex vertices
   generates the sparse bilinear hull. Hence its vertices are 0/1. A primitive
   integer facet representative exists; the ratio forces a nonzero coefficient
   of magnitude at least \(M\). The rational section is not itself asserted to
   have integral vertices.

## Independent computation

The independent script
[series_parallel_vertex_audit.py](../code/network_simplex_review/series_parallel_vertex_audit.py)
does not import the author's implementation. For \(k=3,4,5,6\), it explicitly
enumerates every directed source-to-sink path, pairs each with every simplex
vertex (including the residual vertex), and builds the convex-combination LP
in the original \((x,y,z)\) coordinates. This is deliberately a different
formulation from the author's state-flow LP.

It checks four support minima and 172 local membership points, including the
central point, both directions along the proposed boundary, and random points
on both sides. All **176 path-vertex LP checks passed**. The support value is
\(kc\) in every instance. A second part reconstructs the full explicit state
flow using exact `Fraction` arithmetic, checking every observation, aggregate
flow, state demand, bound, and conservation identity for 150 witnesses with
\(3\le k\le29\) and \(k=50,100,1000\). All **150 exact witnesses passed**.

Command:

```sh
python code/network_simplex_review/series_parallel_vertex_audit.py
```

Output:

```json
{
  "path_vertex_lp_checks": 176,
  "exact_fraction_witnesses": 150,
  "status": "PASS"
}
```

## Relevant 2026 multiflow literature

[Almoghrabi, Skutella, and Warode (2026), *Integer and unsplittable multiflows
in series-parallel digraphs*](https://link.springer.com/article/10.1007/s10107-026-02392-8)
is an important antecedent. Its Theorems 1 and 2 concern aggregate arc flows.
Remark 1 explicitly distinguishes these from the full commodity-flow vector
and gives a three-commodity nonintegrality example. Section 2 defines capacities
on the sum of commodity flows, without prescribed individual arc-flow entries.
Thus their integrality results do not contradict this obstruction. The
distinction between total flows and commodity profiles should be attributed
to that work; the candidate contribution here is the unbounded original
product-coordinate facet ratio on a very restricted unit-flow graph family.
This comparison is not an exhaustive novelty search.

## Stronger Fibonacci extension: accepted

The additional general lemma and the final sparse-complement Fibonacci family
in section 8 have now been reviewed independently. The accepted source snapshot
has SHA-256
`2544fa5b14b502958d37158431ceb8f7f3be29f2f4bb3569a226e68001c2a765`.
**Both pass.** No additional correction was needed.

The balanced-incidence lemma uses every hypothesis correctly. Invertibility
provides the perturbation profile; positive balancing weights give a valid
combination of the subset inequalities; proper rows provide a free observed
coordinate; nonempty rows provide a permissible state on which to absorb the
nonnegative row slack. Setting all aggregate flows, simplex weights, and other
observations leaves exactly the intended coordinate plane. The aggregate flow
on an observed arc is less than \(p\) because its allowed set is proper. The
displayed construction is a full disaggregation, not just a necessary subset
test. The two-dimensional section and ambient-facet argument therefore apply
without modification.

For an explicit neighborhood, put \(R=\alpha_r/\alpha_s\),
\(K=\|A^{-1}\|_\infty\), and

\[
\varepsilon=\frac{a}{16(1+R)(1+K)}.
\]

If both free-coordinate perturbations have magnitude less than
\(\varepsilon\), the right-hand side \(-\delta+\tau\) has only entries
\(-\delta_r\) in row \(r\) and \(R\delta_r\) in row \(s\).
Consequently \(\|d\|_\infty<a/16\) and, on the feasible side,
\(0\le\tau_s<a/16\). These bounds imply every strict inequality required
by the continuity argument. The same formula applies with \(B\) in the
sparse-complement construction. An explicit neighborhood is optional for the
proof but useful for exact computational verification.

The Fibonacci matrix has \(N=2q-1\) rows and columns, and exactly
\(5q-4\) incidences. Subtracting paired column equations forces the primary
row weights to follow the Fibonacci recurrence; the last column kills the
remaining kernel parameter. Thus the nonsingularity argument is exact.
The positive weight formula balances every column. Every column is proper,
so \(\sigma=\sum_i\alpha_i>\beta\). The stated rank-one argument proves
that \(B=\mathbf1\mathbf1^T-A\) is invertible and balanced by the same
weights, with positive total \(\sigma-\beta\).

Applying the lemma to \(B\) gives exactly the claimed free observations:
\(u\) is row \(P_q\), last column; \(v\) is row \(P_1\), first column.
Both cells belong to \(A\), so they are observed in the \(B\)-allowed
construction. The section normal is \((F_q,1)\), and the facet ratio follows.
The final family has \(2q\) vertices, \(4q-1\) arcs, cycle rank \(2q\),
\(2q-1\) explicit simplex coordinates, and only \(5q-4\) observed products.
Its original nonlinear description has linearly many variables, constraints,
and nonzero entries, with \(O(q\log q)\) sparse encoding length. The exponential
ratio in \(q\) is therefore superpolynomial in that encoding length. This
is not a claim that coefficient bit lengths are superpolynomial, nor a claim
with fixed simplex dimension.

The independent script
[fibonacci_vertex_audit.py](../code/network_simplex_review/fibonacci_vertex_audit.py)
constructs both the original incidence and its complement from the column
definitions, inverts them exactly, and solves independently for the balancing
weights. It checks all full state flows using rational arithmetic for
\(q=3,\ldots,12,20,30\). This includes ratio \(F_{30}=832040\).
It also builds the hull directly from all directed-path/simplex-vertex pairs
for \(q=3,4\), then checks support values and membership on the boundary and
both sides. No author's code is imported.

Both versions passed **60 exact full-flow witnesses and 16 vertex-mixture LP
checks each**: 120 exact witnesses and 32 LP checks in total. For the final
sparse version, these are independent verification of the exact coordinates
used in the candidate note. Together with the initial family audit, the scripts
reported in this review passed 270 exact witnesses and 208 path-vertex LP checks.

```sh
python code/network_simplex_review/fibonacci_vertex_audit.py
```

The strongest result is ready to be promoted to a result file from the
standpoint of mathematical correctness. Novelty remains subject to the broader
literature review; this audit establishes no priority claim.

## Final promoted theorem and fixed-state complement: accepted

The final bounded extensions have been independently reviewed and pass:

- [Promoted coefficient theorem](../results/network-simplex-series-parallel-coefficient-growth.md),
  SHA-256 `ea64f1a12c21c1979bf22549f8cb98eb712fc1fa2dca4daedeac08ee53cc9936`.
- [Fixed-state flat-chain theorem](../results/network-simplex-flat-chain-fixed-states.md),
  SHA-256 `a14d6a7ef47e148436d71ce939e44e2060e222f8a542d3bada913f0fb127f7a7`.
- The corresponding development note, including section 9, SHA-256
  `60987a702b617b3b5346fd0de1c9981078c72d126ad9f127432d92ce67a12d70`.

The simple-graph corollary is correct. Splitting each of the \(N-1\) internal
joins adds one vertex and one connector arc; subdividing each of the \(N\)
second arcs adds another vertex and arc. Starting from \(N+1\) vertices and
\(2N+1\) arcs gives \(3N\) vertices, \(4N\) arcs, and unchanged cycle rank
\(N+1\). There are no parallel arcs afterward. Sources and sinks have degree
three, split joins have degree three, and subdivision vertices have degree two.
The directed series–parallel construction remains explicit. Each old flow has a
unique feasible extension to the new arcs and each new flow restricts to an old
flow. This affine correspondence preserves the unchanged observed coordinates.
Fixing the new coordinates in the original two-coordinate section consequently
preserves its local edge and the facet coefficient ratio. New unit capacities
are redundant because all such flows are nonnegative acyclic unit flows.

The fixed-state theorem's reduction is exact for arbitrary observations on the
first arc, second arc, both arcs, or bypass. In particular, if both arcs of a
gadget are observed in a state, nonnegativity and
\(w_j=u_j+v_j\) imply that both observed values lie in \([0,w_j]\); separate
upper bounds are unnecessary. Observations on only the second arc yield the
positive \(\sum_B v_j\) term in \(R\). Unobserved first-arc entries range
independently over full intervals, making the two aggregate endpoint inequalities
sufficient. The original aggregate flow equalities then supply the second-arc
totals. Zero state weights force zero profile and state arc entries automatically.
The residual state has weight \(1-\sum_jy_j\) and no observations; the same
argument covers both zero residual weight and zero explicit weights. The weights
may vary throughout the simplex, rather than being fixed equal weights.

One algorithm clarification was requested and added: first check original
flow/conservation, capacity, simplex, and product-nonnegativity conditions.
The profile system alone must not be advertised as a complete separator without
these original constraints. In particular, its aggregate formulas do not use
the second-arc coordinate directly. The final result now includes the precheck.

The determinant bound also passes. The Farkas cone is pointed since its vectors
are nonnegative. A nonzero extreme ray has a minimal positive dependence on at
most \(d+1\) nonzero rows, or is the singleton ray for a zero row. For a
support of size \(s\), choose \(s-1\) independent columns; the primitive
dependence coefficients divide the corresponding minors of order \(s-1\).
Each selected row is either a 0/1 vector or its negative, so changing whole-row
signs bounds these determinants by \(\Delta_d\). Each original flow/product
coordinate appears with coefficient at most one in magnitude in any individual
right-hand side. Summing at most \(d+1\) such rows gives
\((d+1)\Delta_d\), including possible appearances in several selected rows.
No assertion that each original variable occurs in only one selected row is
needed. This constructs an integer inequality description and controls
coefficient ratios at fixed \(d\); it is not an assertion about every arbitrary
rescaling or affine-hull modification of facet equations.

The circuit separator has the stated parameter dependence. Replacing repeated
identical left-hand sides by their minimum right-hand side preserves feasibility.
Every circuit of the present distinct rows is a circuit of the full signed-subset
universe. That universe has at most \(2(2^d-1)\) nonzero rows, so enumerating
supports of size at most \(d+1\) takes \(2^{O(d^2)}\) candidates. Exact
nullspace calculations decide which are positive circuits. At a query point,
freezing the row attaining each minimum gives a globally valid original-space
affine inequality, even when the minimizing rows change at other points. Zero
rows are separate scalar inequalities. Constructing the profile rows and their
right-hand sides takes \(O(dL+|O|+m)\) arithmetic operations; recovering the
explicit cut or checking the parameter-sized circuit list is absorbed by the
parameter-only term. Rational bit lengths remain polynomial in the encoded
input. The grouped LP and greedy interval filling also give the stated feasible
state-flow recovery. This analysis is restricted to the stated flat topology
and unit balance/capacity data.

### Independent final checks

The additional script
[flat_chain_profile_audit.py](../code/network_simplex_review/flat_chain_profile_audit.py)
does not import author code. It compares the profile feasibility system against
the full convex hull of all directed-path/simplex-vertex pairs in **320 cases**,
using one to four explicit simplex coordinates and one, two, three, or five
gadgets. Observation sets vary over both gadget arcs and the bypass. Half the
trials perturb an observed product. All comparisons passed: 171 feasible and
149 infeasible. These cases include 104 trials with zero residual state weight
and 80 trials with zero first-explicit-state weight.

The script also constructs the simple maximum-degree-three graphs directly and
checks their counts, distinct edges, degrees, and every lifted old path for
\(N=3,5,7,9\): **684 path lifts passed**, each with exact binary arc values
and conservation. These are distinct checks from the original facet-section
experiments.

Finally, independently enumerating signed-subset row supports and computing
their exact nullspaces reproduces **1, 5, and 41 positive circuits** for
\(d=1,2,3\), with largest primitive weights **1, 1, and 2**, respectively.

```sh
python code/network_simplex_review/flat_chain_profile_audit.py
```

No further extension to arbitrary nested series–parallel graphs was attempted
in this audit. Those graphs remain outside the accepted positive theorem.
