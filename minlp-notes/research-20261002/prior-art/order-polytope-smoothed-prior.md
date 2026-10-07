# Prior-art audit: smoothed exact optimization on order polytopes

Date: 2026-10-02. This is a focused comparison of the completed
[order-polytope theorem](../new-direction/smoothed-sparse-order-polynomial.md)
and its counting and closure lemmas. The theorem has a separate completed
mathematical review. This note does not assess publication priority.

## Candidate and boundary

The candidate minimizes a fixed-degree rational polynomial plus independent
finite-grid linear noise over

```text
P = {x in [0,1]^n : x_i <= x_j for each listed edge i -> j}.
```

A supplied tree decomposition covers factor scopes and order edges. If its
largest bag has size `p`, expected bit work is bounded by

```text
C_0^p p! (p+1) [2+nH(p+1)/(2 sigma)]^p poly_d(I).
```

The width dependence is XP rather than FPT in `p`: `p!` is an allowed
parameter-only factor, but the bracket also contains `n^p`. For fixed `p`
the bound is polynomial when `H/sigma` is polynomially bounded. One
base-chosen finite rational noise law
works for all draws, each of which is solved exactly. The result concerns the
perturbed objective and does not promise recovery of an optimizer of the
unperturbed polynomial. Its three order-specific steps are common-threshold
feasible rounding with a full-Hessian Taylor bound, an expected count of
near-optimal bag rows using the at-most-`b!` order chambers, and certified
active-face closure followed by a convex patch. See the theorem and
[counting lemma](../new-direction/order-polytope-cell-count.md) for exact
hypotheses and constants.

## Classical order-polytope geometry

Stanley's primary paper, [“Two Poset Polytopes”](https://math.mit.edu/~rstan/pubs/pubfiles/66.pdf),
defines the order polytope by box and order inequalities. Its Corollary 1.3
identifies vertices with characteristic vectors of filters/upsets (printed
p. 12; extracted p. 4); its triangulation section partitions the order
polytope into simplices indexed by linear extensions (printed p. 17;
extracted p. 9). These results
cover the candidate's zero-one vertex property and the basic order-chamber
decomposition. A bag of size `b` has at most `b!` total-order chambers, which
is the relevant crude bound even if many permutations are infeasible.
Cycles in the candidate's directed presentation impose coordinate
equalities; contracting strongly connected components reduces them to a
poset. These are established geometric ingredients, not contributions of
the smoothed algorithm.

The candidate's conditional fiber description sharpens this geometry for
its count: over a fixed bag chamber, each outside coordinate at a fiber
vertex equals `0`, `1`, or one of the bag coordinates. Hence each fiber is
the convex hull of affine copy maps, and their convex combinations have
squared operator norm at most `n`. Stanley's polytope results do not state
this recourse-value semiconcavity bound or the resulting random near-optimal
grid-row count; those are proved in the project's
[order-polytope counting lemma](../new-direction/order-polytope-cell-count.md).

## Closest isotonic optimization precedent

Bach's primary NeurIPS paper, [“Efficient Algorithms for Non-convex
Isotonic Regression through Submodular Optimization”](https://proceedings.neurips.cc/paper/2018/file/6ea9ab1baa0efb9e19094440c317e21b-Paper.pdf),
is the closest direct algorithmic comparison. It studies nonconvex
continuous submodular objectives under isotonic constraints. For twice
differentiable objectives, its submodularity assumption requires nonpositive
mixed second derivatives (Definition, printed p. 2). It embeds the problem
in a convex optimization over one-dimensional probability measures and
uses one common quantile threshold across coordinates; first-order
stochastic dominance then represents the order constraints (Proposition 1,
extracted p. 3). This common-threshold coupling is a close antecedent to
the candidate's feasible grid rounding and should be credited as an
established idea.

The guarantees differ materially. Bach's algorithms discretize that
measure-space convex problem and give accuracy-dependent function-oracle
costs; for smooth objectives the paper reports an
`O(n^4 L_1 L_2 epsilon^(-5/2))` value-oracle bound (printed p. 5). The
candidate does not assume submodularity, instead using an upper Hessian
bound; its common-threshold rounding is a proof device for a fixed-cell
lower bound, not a measure-space reformulation. The candidate combines
sparse tree-decomposition DP, a finite-noise expected count of continuous
near-optimal bag tuples, a rational LP margin certificate for the optimizer's
active order equalities, and same-draw exact fallback. Bach does not state
that sparse expected exact bit-time guarantee. Conversely, both sparse-box
and order-polytope bounds contain an `n^p` term and are XP in bag size; the
order-polytope bound adds a `p!` chamber factor. These are differences in
assumptions and guarantees, not a novelty conclusion.

The order candidate permits directed cycles, which force equalities. Bach
states a DAG model in the main formulation. Contracting strongly connected
components is routine and makes the candidate's input an ordinary poset;
the cycle allowance does not itself create a distinct isotonic model.

## Rounding, face exposure, and genericity

Mean-preserving rounding of a point in an aligned grid cell to feasible
corners is a standard integrality consequence for totally unimodular
constraints. The project's separate
[TU rounding lemma](../new-direction/tu-feasible-rounding.md) records that
argument and its full-Hessian error `n H h^2/8`; order inequalities are a
special case. Bach's common-quantile construction gives the even closer
order-specific rounding mechanism. The candidate's proof must retain the
full-Hessian premise because the common-threshold choices are correlated;
the box theorem's diagonal-curvature estimate does not transfer unchanged.

Linear optimization exposes a face of a polytope, and rational LP dual
certificates for objective gaps are standard. The candidate uses this
operation with a rational gradient hull: it fixes an order equality only
when the competing face's LP gap exceeds a certified gradient-error bound.
This avoids assuming that small coordinate gradients reveal active order
constraints or that inactive inequalities have positive slack. The
[face-closure lemma](../new-direction/order-polytope-face-closure.md)
provides the algorithm-specific soundness argument and finite-noise margin
bound. Stanley's face description supports the zero-one vertex step, but
does not provide this quantitative closure test.

The project's already-audited Lee–Phạm genericity sources establish
qualitative conclusions under their stated semialgebraic regularity or
full-polynomial-coefficient perturbation assumptions. They do not provide
the candidate's quantitative finite-grid growth and face-gap tails,
sparsity-dependent expected row count, or exact all-draw solver. In
particular, generic uniqueness, local second-order conditions, and
positive growth by themselves are not substitutes for these numerical
finite-law bounds. The detailed assumption comparison and theorem locators
are in the existing
[sparse polynomial audit](sparse-smoothed-polynomial-prior.md).

## Relation to sparse smoothed exact optimization

The closest algorithmic ancestor is the project's reviewed sparse-box
polynomial theorem in the existing
[sparse polynomial audit](sparse-smoothed-polynomial-prior.md). That work
already supplies the finite-noise transfer, sparse bag-cell DP, expected
near-optimal row counting, exact algebraic exceptional branch, and convex
patch output for product boxes. Generic discrete smoothed-analysis results
and expected low-rank quasi-concave optimization are also covered there.
None is an exact order-polytope solver by itself.

The constrained extension is therefore a composition around the order
polytope: feasible common-threshold rounding, a `b!` chamber count for
conditional fibers, and LP-based active-face closure. Its input class is
more structured than arbitrary TU constraints; a generic TU rounding lemma
does not give the fiber chamber count. Its width dependence is comparable
to the cited smoothed sparse-box polynomial theorem: both are fixed-width
polynomial bounds with an `n^p` term, and the order bound adds a `p!`
chamber factor. The factorial is parameter-only; it is not the reason the
bound is XP. The project's deterministic, growth-conditioned
[filtered-grid theorem](../new-direction/pruned-coordinate-grid.md) gives
an FPT bound in bag size and the curvature/growth ratio, assuming positive
point growth for termination and runtime analysis. It does not require the
growth constant as input; its trial procedure discovers the unknown
conditioning. This is a separate deterministic result, not a noise-only
predecessor. The precise possible contribution is
this specific expected exact finite-bit composition, subject to independent
verification of the complete proof and implementation; the established
polytope, coupling, LP, and genericity facts above should not be claimed as
new.

## Sources examined

- Richard P. Stanley, “Two Poset Polytopes,” *Discrete & Computational
  Geometry* 1 (1986), 9–23. Primary author-hosted PDF linked above; local
  [source package](../../literature/papers/stanley1986-two-poset-polytopes/);
  Cor. 1.3 (printed p. 12) and triangulation (printed p. 17).
- Francis Bach, “Efficient Algorithms for Non-convex Isotonic Regression
  through Submodular Optimization,” *NeurIPS* 2018. Primary proceedings PDF
  linked above; local
  [source package](../../literature/papers/bach2018-efficient-algorithms-for-non-convex/);
  common-quantile extension and Proposition 1 (extracted p. 3), discretization
  contribution (extracted p. 2), smooth oracle complexity (printed p. 5).
- Existing local comparisons: Lee–Phạm genericity, TU feasible rounding,
  sparse smoothed polynomial optimization, and the two order-polytope
  lemmas linked above. No new KB/index mutation was made for this audit.

The Stanley and Bach primary sources were directly inspected and are now
stored in the linked local packages. Failure to find a stronger match is not
evidence of novelty.
