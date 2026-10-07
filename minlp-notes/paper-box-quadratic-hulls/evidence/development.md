# Mathematical development: classification of strict edge-contact rays

The initial classification recorded here has been strengthened by the
reviewed continuation in `development-continuation.md`: the pair-minor
hypotheses can be removed, with affine squares added to the conclusion.
The current TeX files contain that stronger statement provisionally,
pending the integrating agent's receipt of the exact Hildebrand source
verification. This record preserves the original direct graph argument.

## New proved statement

The manuscript now contains a direct contact-graph classification in
`sections/05b-contact-classification.tex` and its complete proof in
`appendices/E-contact-classification.tex`.

Let `q=q0+a^T x+x^T Qx` generate an extreme ray of the cone of quadratics
nonnegative on `[0,1]^3`. Assume:

- `Qii>0` for all three coordinates;
- `Q12 Q13 Q23>0`;
- `Qii Qjj-Qij^2<0` for every pair;
- `q(v)>0` at every cube vertex.

Then a cube symmetry transforms `q` into the strict five-contact family

`(h-d1 x-d2 y+d3 z)^2+2d3 k z(1-x-y)+k[2(d1+d2-h)+k]xy`,

with `d1,d2,d3,k>0`, `0<h<min(d1,d2)`, and
`d3>d1+d2-h+k`. Conversely all those family rays satisfy the hypotheses.

The proof is independent of the archived contact enumeration, sampler
outputs, family fits, symbolic rank scripts, and external copositive
classification theorems. The independent classification reviewer found
the argument sound, including all five graph cases and the perturbation
bound. Its notation and direct strict-derivative suggestions were applied.

## Complete proof structure

1. Complement a coordinate to make all mixed coefficients positive.
2. Every zero lies in an edge interior: negative pair determinants rule out
   facet-interior minima, and they also rule out an interior minimum.
   Positive vertex values rule out vertex zeros.
3. Each such zero has positive inward derivatives in both neighboring
   facets. If one vanished, minimizing the second-order term over the free
   edge coordinate would give a feasible negative value because the relevant
   Schur complement is negative.
4. Value and edge-derivative equations for `m` zeros impose at most `2m`
   constraints on ten coefficients. Because inward derivatives and edge
   curvature are strict, every perturbation satisfying these equations is
   bounded by a constant times `q` near its zeros. It therefore gives a
   feasible two-sided perturbation. Thus extremality implies `m>=5` without
   assuming independence of the contact equations.
5. At two contact edges incident at a vertex, midpoint evaluation forces
   the local mixed coefficient to be at least `2 di dj`, where
   `di=sqrt(Qii)`. Since all global mixed coefficients are positive, the two
   coordinates must have equal bits at that vertex. Components consequently
   stay between adjacent Hamming-weight levels.
6. Three incident contact edges give an explicit nontrivial decomposition
   into an affine square and positive coordinate products. Extremality
   excludes them.
7. The contact graph is supported by the bottom three-edge star, central
   six-cycle, and top three-edge star, with contact degrees at most two.
   Five short analytic cases exhaust graphs with at least five edges. No
   contact-position genericity assumption is used.
8. Five central-cycle contacts imply the sixth by the alternating endpoint
   square-root equations. The polynomial is then
   `(sum di xi-h)^2+A[(1-x1)(1-x2)(1-x3)+x1 x2 x3]`, `A>=0`, hence
   decomposable in the nonnegative cone and in `D3`.
9. A bottom edge, three central edges and a top edge force contradictory
   diagonal orders `d3<d1` and `d1<d3` by two opposite-edge contacts on
   parallel facets. Two bottom edges, two central edges and a top edge
   give a square plus nonnegative terms that is strictly positive on the
   proposed top contact. Two edges in each outer star plus one central
   edge give three parallel contacts with the unconstrained coordinate
   minimizer strictly inside the entire remaining square, contradicting
   the proposed perpendicular bottom contact.
10. The only remaining graph is a four-edge central path plus an isolated
    outer edge. Cube symmetry gives exactly the five contacts of the
    existing family. Reconstructing coefficients gives `k=r-(d1+d2-h)`.
    A strictly positive inward derivative implies `k>0` directly.

## What remains open

The theorem does not establish the full family-completeness conjecture.
After the manuscript's sign-class reduction, an unclassified extreme ray
outside `D3` must have a vertex zero or at least one nonnegative pair
principal determinant. Existing family boundary results cover specific
vertex-contact limits, but do not show that they exhaust that entire
regime. A nonnegative pair determinant can allow a facet-interior zero,
so the contact graph used above no longer applies. No assertion that such
rays are in `D3`, nor any claim of complete classification, is justified.

I considered a general affine-square subtraction route. It would require a
proved uniform quadratic growth bound near all zeros and a careful treatment
of critical directions at boundary zeros. The notes' reference to a general
zero-span criterion was not taken as a license to assume that criterion in
this new proof. This route was not needed for the proved classification and
was not pursued into a speculative manuscript claim.

## Targeted checks actually run

- New, small finite cube-edge enumeration in `/tmp/box_edge_classify.py`
  checked the proposed graph cases during development. This enumerated only
  subsets of the 12 cube edges and applied exact graph rules; it did not
  solve quadratic programs, sample contact positions, or repeat an archived
  computational experiment. The manuscript proof replaces this enumeration
  with a complete five-case analytic argument.
- A one-off SymPy command verified the opposite-edge completion-of-square
  formula, its diagonal coefficients and endpoint restrictions, the
  two-parallel-facet formula and its coefficients, and the multilinear
  identity for the central-cycle residual. It printed
  `Contact-classification symbolic identities: PASS`.

No archived computational experiment, project-wide verification, or CI
inspection was run. TeX compilation belongs to the integrating agent.
