# Second independent audit: one-parameter bounded planar path projection

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`.

**Verdict: PASS.** The quasipolynomial endpoint representation in [the candidate](one-parameter-path-projection-investigation.md) follows under its explicit fixed-degree, single-parameter, uniformly bounded path assumptions. No correction is required. This review does not establish novelty or extend the claim to dense aggregate constraints.

## Pointwise row bound and symbolic elimination

The [antecedent planar composition theorem](../results/pooling-degree-two-boundary-projection.md) supplies the required additive facet bound. I checked its envelope argument: a convex or concave inner graph crosses an outer knot level at at most two boundary points, and the maximum of convex piecewise-affine functions uses at most the union of their affine pieces. Bounded lower-dimensional cases are included.

The candidate correctly converts this bound into a small subset of Fourier--Motzkin candidate rows. Every facet of a full-dimensional polygon is supported by a row in any exact finite inequality description. A nontrivial segment has opposite affine-hull normals among the active rows and at most two endpoint restrictions. An irredundant description of a point in the plane uses at most four rows. Keeping the permanent bounding box adds only a constant. Thus pruning does not require creating new geometric rows with sample-dependent coefficients.

For fixed signs of the eliminated-coordinate coefficients, the stated positive Fourier--Motzkin multipliers are correct. The list is quadratic in the child row counts, and each output coefficient uses two polynomial products and a subtraction or addition. Pairs within one child are necessary and correctly retained. At a singleton where a coefficient vanishes, its original inequality becomes an endpoint inequality at that parameter; dropping the eliminated-coordinate term is valid there, even if that coefficient polynomial is not identically zero.

## Why one sample determines a valid row subset on a cell

The augmented minors record both normal independence and every intersection-versus-row sign. At the intersection of rows `i,j`, the slack of row `k` is an augmented determinant divided by the normal determinant, up to a fixed orientation sign. The recorded signs therefore determine whether each candidate intersection is feasible for any selected sublist and whether it satisfies each omitted row. Constant-only rows are also covered by the one-by-one minors.

Take a small sublist equivalent to the full candidate list at a sample, and retain the box. Every feasible vertex of the selected polyhedron at another parameter corresponds to an independent pair that was already feasible at the sample; that pair's omitted-row signs cannot change. Therefore every such vertex satisfies all omitted inequalities. Boundedness then gives the same conclusion for the whole selected polyhedron. The full candidate set is always contained in the selected set, proving equality.

This argument includes segments and points because every nonempty bounded planar polyhedron has a vertex with two independent active normals. Emptiness of the full candidate set is likewise invariant: the list of feasible independent intersections cannot change. A fiber that exists only at an isolated parameter is not inferred from neighboring intervals; the separate singleton calculation handles it directly.

## Balanced recursion and cell count

Write `t=ceil(log_2 h)` after padding with bounded identity relations if necessary. The retained-row recurrence gives at most `C^t` times a polynomial in the total input row count, hence a polynomial in `N`. Each common child cell therefore produces only polynomially many Fourier--Motzkin candidates and minor polynomials.

For one real parameter, overlaying two interval-and-point partitions consists of sorting the union of their breakpoints. Its size is proportional to the sum of the child sizes. There is no product of independently chosen parameter cells. Each local refinement inserts at most a polynomial number of roots because the number and degrees of its polynomials are polynomial. Thus

```
L_parent <= N^c (L_left+L_right)
```

for a fixed constant `c`. Summing over all nodes of a level and then over the logarithmic number of levels gives `N^{O(log(h+1))}` total work units and output cells, with only polynomial additional factors. Empty child cells can be propagated as false without elimination. A singleton child cell is processed at that one parameter, not repeatedly expanded into an unpruned quadratic row list.

## Degrees, heights, and algebraic arithmetic

Clearing each original row's rational denominators preserves its inequality if a positive common denominator is used. This has polynomial cost. At a balanced composition, the degree at most doubles. The root therefore has degree at most `d*2^t=O(dh)`. A coefficient-height bound has the form

```
H_next <= 2H_current + O(log(D_current+1)+1),
```

because polynomial convolution uses at most `D_current+1` summands per coefficient. Iteration over logarithmic depth is polynomial in the input length. Minors involve at most three rows and do not change this conclusion. They are used for partitioning, not recursively inserted as new endpoint rows.

Each boundary is a root of an integer polynomial with polynomial degree and height. Root comparison between polynomials from different nodes or different cells remains polynomial per comparison: a separation bound can be applied to a pair of such polynomials or to their product. It is unnecessary to form one product of all quasipolynomially many boundary polynomials. Therefore distinct boundaries, and rational samples between them, have polynomial-size encodings independently of the total number of cells.

At an isolated parameter `alpha`, all row evaluations remain in `Q(alpha)`. Selecting and comparing rows and vertices requires only a polynomial number of field or sign operations on polynomially encoded expressions. The symbolic rows carried upward are the original selected polynomial expressions; neither sampled values nor intersection coordinates become new coefficients. Consequently no chain of unrelated algebraic field extensions is introduced.

As a primary-source check of the standard algebraic ingredients, I directly read Basu's author survey, sections 2.4.1--2.4.2. It states polynomial univariate sign determination and gives the fixed-variable quantifier-elimination degree and integer bit bounds in Theorem 2.18. These support the use of exact algebraic comparison and fixed-dimensional feasibility as established tools. [Author survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf).

## Feasibility and witness clarification

The author's proposed existential-feasibility corollary is sound provided the final endpoint list is refined by its minors even when `h=1`: endpoint emptiness is then constant on each open cell, and singleton cells are tested separately. Sampling all cells decides whether any parameter admits a path within the same quasipolynomial bound.

A polynomial-degree witness exists. Choose the sampled parameter, rational on an open cell or algebraic on a singleton. The original bounded feasible path polyhedron has a vertex. Cramer's rule on independent original active rows expresses its coordinates as ratios of polynomials in that one parameter of degree at most `d(h+1)` and polynomial coefficient height. Thus witness coordinates need no extension beyond the sampled parameter field.

For constructive interval-slice recovery, a polynomial field degree alone is not a bit-height proof for arbitrary repeated inversions. Here a direct bound is available: keep rational-function affine expressions during balanced reconstruction. Each new coordinate uses a constant number of operations on its parent endpoints and selected symbolic child rows, and the recursion has logarithmic depth. The corresponding degree and height recurrences remain polynomial. This supports constructive recovery without claiming a bound for arbitrary externally supplied endpoint fields.

## Scope

The theorem excludes an exponential-in-`N` number of necessary cells for this explicit representation, since `h<=N` up to the input convention and `N^{O(log N)}=2^{O((log N)^2)}`. It supplies neither a polynomial bound nor a matching quasipolynomial lower bound. It is essential that there is only one shared parameter and that each projected fiber is a bounded planar relation.

Dense costs, pool mass sums, and pool attribute sums are not retained by endpoint projection. The candidate correctly declines to infer a global pooling theorem from local planar relations. The same proof would tolerate polynomially bounded initial degree, for example dense polynomial encoding, but that optional extension is unnecessary for the stated fixed-degree result and does not justify succinct high-degree inputs.

This audit is a complete symbolic argument check. No new numerical test is claimed: the antecedent planar lemma already has exact composition checks, while the new conclusions depend on sign invariance, recurrence bounds, and algebraic encoding arguments.
