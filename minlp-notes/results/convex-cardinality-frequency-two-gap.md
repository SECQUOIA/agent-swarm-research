# Sharp gaps for convex cardinality factors of variable frequency two

Date: 2026-09-04.

Status: the gap theorem, box corollary, and matching-based optimization corollary passed
[independent written review](../notes/review-convex-cardinality-frequency-two.md).
The root agent proposed the common-aspect-ratio extension and the convex-cardinality
formulation; the packing-audit agent derived the proof below independently. The
degree-polytope and single-factor envelope ingredients are classical. Novelty of
this combined gap theorem has not been established by a comprehensive search.

## Result and meaning of a factor

For each factor vertex `v`, let `S_v` be a set of coordinates and let
`φ_v(0),…,φ_v(d_v)`, where `d_v=|S_v|`, be a real sequence satisfying

```
φ_v(k+2)−2φ_v(k+1)+φ_v(k) ≥ 0,     0≤k≤d_v−2.
```

Let `f_v` be the unique multiaffine function on `[0,1]^{S_v}` whose value at a binary
vertex `z` is `φ_v(Σ_{i∈S_v}z_i)`, and put `f=Σ_v f_v`. These are the multiaffine
interpolants of the discrete cardinality costs. They are generally **not** the
continuous functions obtained by substituting `Σ x_i` into an extension of `φ_v`.
Affine summands may be added freely. Nonnegative factor weights can be absorbed
into their sequences; the sequences need not be positive or increasing.

Assume each coordinate belongs to at most two factor supports. Form the loopless
dual multigraph with a factor vertex for every `v`: each shared coordinate is an
edge between its two factors, and each private coordinate is an edge to its own
dummy vertex. Dummy factors have identically zero sequences. Parallel edges are
allowed. Let `g` be the shortest odd-cycle length, with `g=∞` for a bipartite graph.
Unused coordinates can be omitted throughout and independently sampled with their
prescribed means afterward. Constant and affine factors cause no difficulty.

At any point `p∈[0,1]^n`, define the gap of the factorwise relaxation and the scalar
graph-hull gap by

```
T(p)=Σ_v [cav f_v(p)−vex f_v(p)],
H(p)=cav f(p)−vex f(p).
```

**Theorem.** For finite `g`,

```
H(p) ≥ (1−1/g) T(p).
```

If the dual graph is bipartite, `H(p)=T(p)`. In particular, always `T(p)≤(3/2)H(p)`.
The constants are sharp already for positive bilinear factors on an odd cycle.
This is a scalar gap result; it does not assert equality of the full lifted factor
polytope with its factorwise relaxation.

## Single-factor envelopes and common upper attainment

Let `ψ_v` be the piecewise affine interpolation of `φ_v` between consecutive
integers. It is convex. Write `s_v(p)=Σ_{i∈S_v}p_i`. Then

```
vex f_v(p)=ψ_v(s_v(p)).                                      (1)
```

Indeed, for any binary distribution with mean `p`, Jensen's inequality bounds
`E φ_v(K)` below by `ψ_v(EK)`. Conversely, the polytope
`{z∈[0,1]^{S_v}: floor(s_v(p))≤Σz_i≤ceil(s_v(p))}` is integral. To see this directly,
a vertex with two fractional coordinates admits a small opposite perturbation;
a vertex with exactly one fractional coordinate cannot satisfy an integer sum bound
at equality and admits a small perturbation of that coordinate. Therefore `p` is a
mixture of binary vectors with these two adjacent cardinalities, attaining (1).

All factors also share a concave-envelope maximizing distribution: take `U` uniform
on `[0,1]` and `X_i=1[U≤p_i]`. Discrete convexity makes every vertex function `f_v`
supermodular. Its expected value cannot decrease when two incomparable sets in a
distribution are replaced, with equal mass, by their intersection and union. This
replacement preserves coordinate means. For completeness, maximize the expected
factor value and, among its maximizers, maximize the secondary quantity `E(Σ_i X_i)²`.
Any incomparable pair of support sets would permit such a replacement, preserving
the primary optimum and strictly increasing the secondary quantity. Thus a maximizing
law is supported on a chain. The chain law with prescribed Bernoulli marginals is
exactly the common-threshold law, up to zero-probability states. This proves common
attainment for every factor and therefore

```
cav f(p)=Σ_v cav f_v(p).                                    (2)
```

These arguments use vertex distributions legitimately because each function is
multiaffine: its graph at an interior point is a convex combination of its binary
vertex graph points, obtained by independent Bernoulli interpolation.

## Degree-slab decomposition

Consider

```
P(p)={z∈[0,1]^E:
       floor(s_v(p))≤Σ_{i incident to v}z_i≤ceil(s_v(p)) ∀v}.
```

Every vertex `z` of this polytope has fractional edges forming vertex-disjoint odd
cycles, all with value `1/2`. Here is the complete incidence argument. Let `F_z` be
the fractional edges and `R` the tight degree rows incident to them, counting a row
once if its two bounds coincide. Extremality requires full column rank on the
fractional edges, so `|F_z|≤|R|`. Each tight row has an integer residual right-hand
side, and hence at least two fractional incidences. Since every edge has two
endpoints,

```
2|R|≤number of fractional incidences at R≤2|F_z|.
```

Equality follows throughout. Every fractional edge has both endpoints in `R`, and
the fractional subgraph has degree two at every vertex. It consists of cycles.
Even cycles admit an alternating perturbation and cannot occur at a vertex. On an
odd cycle, the two fractional entries incident to each vertex sum to an integer
strictly between zero and two, hence to one; propagation around the cycle forces
both entries to equal `1/2`. This also handles parallel edges, whose two-edge cycle
is even, and private-coordinate dummy vertices.

Write `p=E Z` as a finite convex combination of these vertices. Since `ψ_v` is affine
on the allowed degree slab, (1) gives the exact identity

```
E vex f_v(Z)=vex f_v(p).                                    (3)
```

Concavity of each upper envelope consequently yields

```
E T(Z)≤T(p).                                               (4)
```

## Rounding loss equals the local curvature gap

Condition on `Z=z`. Keep integral coordinates fixed. On a fractional odd cycle of
length `L`, choose uniformly one of its `L` maximum matchings, then choose with
equal probability that matching or its complement in the cycle. Each edge has
marginal `1/2`. All vertices except one have exactly one selected cycle edge; the
exceptional vertex is uniform around the cycle and has zero or two selected edges
with equal probability. Different cycles can be rounded independently.

At a cycle vertex `v`, let `m` count its incident integral coordinates equal to one.
At `z`, its convex-envelope value is `φ_v(m+1)`. Its concave-envelope value is
`[φ_v(m)+φ_v(m+2)]/2`, attained by making the two half-valued coordinates equal.
Thus its gap is exactly

```
T_v(z)=[φ_v(m)+φ_v(m+2)]/2−φ_v(m+1)≥0.                     (5)
```

The rounding has conditional expected value

```
E[f_v(X)|Z=z]=vex f_v(z)+T_v(z)/L.                          (6)
```

Every vertex off the fractional cycles is evaluated exactly and has zero local
gap. Therefore, for finite odd girth `g`,

```
E[f(X)|Z=z]≤Σ_v vex f_v(z)+T(z)/g.
```

The rounded law has mean `E X=E Z=p`. Averaging and using (3)–(4) proves

```
vex f(p)≤E f(X)≤Σ_v vex f_v(p)+T(p)/g.
```

Subtract this inequality from (2) to obtain the theorem. In the bipartite case the
degree-slab vertices are integral, so their mixture attains all individual lower
envelopes simultaneously and proves equality. ∎

## Positive products on boxes with a common aspect ratio

Consider the original monomials

```
f(x)=Σ_v a_v ∏_{i∈S_v}x_i,   a_v>0,
x_i∈[l_i,r l_i],            l_i>0, r>1.
```

Normalize `x_i=l_i[1+(r−1)z_i]`. At a binary vertex, term `v` equals

```
φ_v(K)=a_v (∏_{i∈S_v}l_i) r^K.
```

This is a discrete convex cardinality factor. Hence the master theorem applies to
the **original monomial envelopes**, preserving their original frequency-two
incidence graph. Bipartite exactness and the sharp odd-girth bound both survive on
these boxes. No affine expansion into separate relaxation terms is used.

The ratio `r` may differ between connected components of the factor incidence
graph. Fixed coordinates can first be substituted. The limit `r=1` is trivial.
The zero-lower unit-box theorem is another direct case of the master theorem,
using `φ_v(K)=a_v 1[K=d_v]`, rather than requiring a limiting argument.

The positive-box counterexample in
[the investigation note](../notes/multilinear-frequency-two-positive-box-investigation.md)
has unequal coordinate aspect ratios. It therefore does not contradict this
extension. General positive boxes still require another argument.

Sharpness also holds within the positive-box corollary for every fixed `r>1`.
Take an odd cycle of bilinear factors with all `l_i=1` and normalized means `1/2`.
Expanding each bilinear factor introduces an affine part and the common positive
scale `(r−1)²` times its unit-box bilinear factor. Neither operation changes the
gap ratio, which is exactly `g/(g−1)`.

## Polynomial-time vertex optimization and scalar envelopes

Suppose the sequences and any linear coordinate costs `c_e` are rational and given
explicitly. The binary optimization problem

```
min_F Σ_v φ_v(deg_v(F))+Σ_{e∈F}c_e                         (7)
```

reduces to ordinary weighted matching. Polynomial-time convex degree-sequence
optimization is established in Deza and Onn, Theorem 1.2, whose proof also uses
incremental-cost slots and matching. The construction below makes linear coordinate
costs and private variables explicit; neither the basic tractability nor a new
matching algorithm is claimed.

At each factor or dummy vertex `v`, create `d_v` slot vertices. Slot `k` has charge
`δ_v(k)=φ_v(k)−φ_v(k−1)`, which is nondecreasing in `k`. For each original coordinate
edge `e=uv`, create two mandatory gadget vertices `e_u,e_v`, joined by an edge of
cost zero. Connect `e_u` to every slot at `u`, with edge cost equal to that slot's
charge plus `c_e`; connect `e_v` to every slot at `v`, with edge cost equal to that
slot's charge. Either endpoint can be chosen to carry the linear cost. Zero dummy
sequences give zero slot charges for private coordinates.

A matching covering all mandatory gadget vertices has exactly two possibilities
for each coordinate. Its gadget vertices are matched to each other, meaning the
coordinate is zero, or both are matched to slots at their respective endpoints,
meaning the coordinate is one. Mixed activation cannot cover both gadget vertices.
Every coordinate set `F` is representable because at most `d_v` slots are needed
at vertex `v`. If `k` coordinates are active there, the cheapest possible choice
uses the `k` least costly slots: all slots have the same possible gadget neighbors,
so they can always be reassigned this way. Their cost telescopes to
`φ_v(k)−φ_v(0)`. Consequently the minimum matching cost plus `Σ_vφ_v(0)` equals (7).

Mandatory coverage itself needs no special oracle. Let `W` be the sum of the
absolute values of all gadget edge costs before bonuses and choose `M=2W+1`.
Subtract `M` from an edge's cost for each mandatory endpoint it covers. The matching
using every inactive gadget edge covers all mandatory vertices and is feasible.
Any matching missing at least one mandatory vertex has a bonus disadvantage of at
least `M`, exceeding any possible difference in unmodified matching cost. Thus an
optimal unconstrained minimum-weight matching covers all mandatory vertices. The
gadget has `O(|E|)` vertices and `O(Σ_v d_v²)` edges. Its rational encoding length is
polynomial in the original explicit input. Ordinary weighted matching therefore
solves (7) in polynomial time, including negative slot increments and linear costs.

For rational `p`, the scalar convex envelope is the finite distribution LP

```
min Σ_{z∈{0,1}^n} λ_z f(z),
Σ_zλ_z=1,   Σ_zλ_z z=p,   λ_z≥0.
```

Its dual has variables `(α,π)` and inequalities `α+π·z≤f(z)` for every binary `z`.
The matching oracle for (7), with costs `c_e=−π_e`, separates these inequalities.
For an explicit dual search bound, set
`A=Σ_v max_k |φ_v(k)|` and `B=max{1,(n+1)! A}`. Add the absolute constant and linear
coefficient sum to `A` if separate affine summands are present. The dual feasible
polyhedron is pointed because its constraint rows `(1,z)` span `R^{n+1}`. Its finite
optimal face therefore contains a vertex. Each such vertex solves a nonsingular
`(n+1)`-square integer system with 0/1 coefficient entries and right-hand sides
bounded in absolute value by `A`. Cramer's rule bounds each coordinate by `B`,
because the nonzero integer determinant has absolute value at least one. Thus
adding `|α|,|π_i|≤B` preserves an optimum and supplies polynomial-bit bounds,
including at boundary points `p`. The standard rational optimization/separation
equivalence now gives polynomial-time
evaluation of `vex f(p)` and a supporting affine function. The concave envelope is
evaluated directly by the common-threshold law, with at most `n+1` states. Sorting
the coordinates also supplies a supporting affine upper function. This gives
polynomial-time evaluation and separation for the scalar graph hull. It does not
assert a polynomial-size explicit formulation of the full lifted factor polytope.

In the bipartite case the lower envelope already has the explicit formula
`vex f(p)=Σ_vψ_v(s_v(p))`; no matching oracle is needed for evaluation.
For the common-aspect-ratio monomial corollary, rational coefficients and rational
box endpoints generate the tables `φ_v(0),…,φ_v(d_v)` in polynomial time and with
polynomial encoding length by repeated rational multiplication. Hence this
algorithmic statement also applies to that monomial input format.

## Prior ingredients and remaining review

- Warren Adams, Akshay Gupte, and Yibo Xu, *Error bounds for monomial convexification
  in polynomial optimization*, Proposition 4.1, printed p.22 in the open manuscript,
  explicitly gives the envelopes on `[1,r]^n`, citing earlier work by Tawarmalani,
  Richard, and Xiong and by Harold P. Benson. Its convex-envelope formula is equivalent to
  (1) for the exponential sequence above. This envelope formula is not new here.
  [Open primary manuscript](https://www.pure.ed.ac.uk/ws/files/137020380/1704.00424.pdf),
  [published article](https://doi.org/10.1007/s10107-018-1246-8).
- The half-integral degree-polytope structure and odd-cycle rounding are classical
  fractional matching ingredients; see the primary-source discussion in
  [the unit-box theorem](positive-multilinear-frequency-two-gap.md).
- Polynomial-time weighted matching is classical: Jack Edmonds, *Maximum Matching
  and a Polyhedron with 0,1-Vertices* (1965),
  [open primary paper](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p125_A1b.pdf).
- Gabriel Deza and Shmuel Onn, *Optimization over Degree Sequences of Graphs*,
  Theorem 1.2 and Section 3 (2019 preprint; Discrete Applied Mathematics 296, 2021,
  2–8), prove polynomial-time minimization of sums of arbitrary convex degree
  functions by a minimum-cost perfect-matching reduction with incremental-cost
  slots. This directly anticipates the central algorithmic ingredient of the
  optimization corollary. The inspected paper does not discuss the present
  envelope-gap ratio or odd-girth estimate.
  [Open primary paper](https://arxiv.org/html/1908.09278v1).
- Yibo Xu, Warren Adams, and Akshay Gupte, *Polyhedral Analysis of Symmetric
  Multilinear Polynomials over Box Constraints* (2021 manuscript), Section 1.1.1
  and Section 5, explicitly identify the symmetric-supermodular single-factor
  convex envelope and the comonotone concave envelope as established results,
  crediting Tawarmalani–Richard–Xiong and the classical polymatroid literature.
  This confirms that both single-factor envelope ingredients of the master theorem
  belong to the prior literature.
  [Open primary paper](https://arxiv.org/html/2012.06394v2).
- The proof above is self-contained. The possible contribution is the sharp scalar
  gap guarantee for this factor class and the common-aspect-ratio product corollary,
  rather than the individual envelopes or half-integrality. A dedicated novelty
  comparison remains necessary; the independent mathematical review is complete.

The reproducible verifier
[`code/multilinear_convex_cardinality_verify.py`](../code/multilinear_convex_cardinality_verify.py)
passed 175 exact rational checks of the cycle curvature identity and 240 seeded
full vertex-distribution LP comparisons. The latter include negative and nonmonotone
convex sequences, boundary and unequal marginals, parallel and private variables,
and 181 bipartite equality cases. Floating-point LP checks corroborate the proof;
they are not exact certificates for the global hull values.

The independent reviewer's
[`code/audit_convex_cardinality_matching.py`](../code/audit_convex_cardinality_matching.py)
also passed 100 exact integer comparisons between exhaustive gadget matching and
exhaustive original binary minimization, including signed costs and private and
parallel coordinates.

## Lean verification

[Topic 19](../formal/topics/19-structural-multilinear/COVERAGE.md) formalizes the
single-factor envelopes, simultaneous upper attainment, frequency-two `3/2`
and odd-girth bounds, and bipartite exactness for the multiaffine interpolants
of discrete-convex cardinality tables. Tables may be signed or nonmonotone.
The full theorems start from the original scopes and frequency assumption;
the degree-slab extreme-point structure, finite convex decompositions and
rounding laws are constructed in the proof.

The common-aspect positive-box products are connected to their original
cardinality tables, without replacing their scopes by expanded monomials.
Odd-cycle examples establish sharpness on every fixed box `[1,rho]` with
`rho>1`. The unequal-aspect `7/6` example is also formalized; it rules out
bipartite exactness on general positive boxes, while a universal `3/2` bound
there remains unresolved.

The [verification record](../formal/topics/19-structural-multilinear/VERIFICATION.md)
identifies the checks and reviewed source snapshots. The matching-based
optimization/separation corollary below the gap results and its bit complexity
remain outside this package's scope.
