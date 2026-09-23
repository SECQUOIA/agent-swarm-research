# Source assessment: exact counts for the degree-32 convex box-error family

Date: 2026-09-05. Bounded primary-source audit supporting
[the reviewed result](../results/convex-polynomial-box-error-exact-integer-gap.md).
No matching restricted-family exact-count theorem was identified. This
does not establish exhaustive publication priority.

The result gives `p_conv=n` and `p_bin=ceil(n log2 3)` for `n` independent
inputs, two convex degree-32 outputs per input, and fixed unit box error.
Both minima permit arbitrary finite convex continuous lifts. The
general-integer upper is a rational MILP with one ternary coordinate per
input and linear size. The exact binary upper is only a finite-size
existence claim. For one input it gives a genuine one-bit gap; the growing
gap requires growing input dimension.

## Classical mechanisms

[Lubin, Vielma, and Zadik, Mixed-integer convex representability](https://optimization-online.org/wp-content/uploads/2017/06/6082.pdf),
Lemma 4.1, gives the midpoint/parity obstruction and an integer-dimension
lower bound. Its Section 4.1 develops the finite-convex-fiber viewpoint for
binary formulations. Corollary 4.2 shows equality of the binary and
general-integer lower bounds for representing subsets of a Boolean cube.
These are direct antecedents. Using modulus three when a thirds
combination is forbidden is an elementary variation, not a new method.
The approximation theorem concerns a connected polynomial graph inside
a tolerance tube, rather than exact representation of a Boolean set.

[Dash, Gunluk, and Hildebrand, Binary Extended Formulations of Polyhedral Mixed-integer Sets](https://optimization-online.org/wp-content/uploads/2018/01/6403.pdf),
Sections 1--2, studies binarization of bounded integer coordinates and
includes logarithmic encodings. Its main comparisons concern branching
and split closures. A general advantage of integer coordinates over
binary ones is therefore not new. Even the finite set `{0,1,2}^n` has
exact counts `n` and `ceil(n log2 3)`: a convex fiber cannot contain two
of its distinct points, and equal modulo-three codes also contradict
its discreteness. The numerical count law alone is thus elementary.

[Zadik, Lubin, and Vielma, Shapes and recession cones in mixed-integer convex representability](https://optimization-online.org/wp-content/uploads/2021/03/8284.pdf),
Introduction and Section 2, distinguishes binary index sets from more
general integer index sets and studies recession cones and shapes of
their convex fibers. That is related structural context, but it does
not provide the fixed-tolerance convex polynomial graph example. In
particular, the present construction uses only bounded ternary indices;
it is not a separation in representability caused by unbounded integers.

## Defensible contribution

The useful example transfers a familiar ternary count advantage to
componentwise convex polynomial graphs while preserving ordinary box
error, fixed degree, and fixed numerical data. The nontrivial local
verification is that the entire middle integer slice of the three
labeled boxes stays inside the error tube, even though certain thirds
chords between exact contacts leave it. This supplies a precise boundary
for attempts to eliminate an additive term proportional to input
dimension in binary-versus-general-integer graph approximation.

It is appropriate to call this a new candidate supporting example after
two independent proof reviews. It should not be advertised as a new
general binarization phenomenon, a new lattice obstruction, or a solution
to the one-input unbounded-output-gap question. The earlier local
nonconvex scalar polynomial example and tilted-error convexification
have different restrictions; see
`notes/nonconvex-polynomial-binary-integer-gap-novelty.md` and
`notes/convex-vector-gap-and-overlay-source-audit.md`.

## Bounded search record

Queries included:

- `"mixed-integer convex" "binary" "convex functions" approximation dimension`
- `"integer dimension" "convex" "binary" graph approximation`
- `"mixed-integer convex representability" "modulo" approximation`
- `"convex polynomial" "binary" "integer dimension"`
- `"graph approximation" "general integer" convex`

The primary works above were opened and their relevant passages checked.
No direct fixed-degree, fixed-box-error example with the stated exact
minimum counts appeared in those sources or search results. A broader
unindexed or differently worded predecessor remains possible.
