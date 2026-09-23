# One-input convex vector box gaps: lattice tools and remaining question

Date: 2026-09-05. Bounded independent investigation requested after the
[curvature-rank theorem](../results/convex-vector-curvature-rank-precision.md).

The remaining question is whether a universal constant `C` satisfies
`p_bin<=p_conv+C` for every continuous componentwise convex vector graph
on one compact interval with box error, independently of the number or
curvature rank of the outputs. The current repository bounds have overhead
logarithmic in output dimension or curvature rank. Its growing-power family
does not provide a growing gap between these two minima.

## A concrete improvement, with limited scope

The investigation produced [an explicit one-bit example](convex-vector-one-bit-box-gap-investigation.md):
two convex degree-32 rational polynomial outputs on one interval have
`p_conv=1` and `p_bin=2` at unit box error. The example and product counts have passed both audits linked from [the promoted theorem](../results/convex-polynomial-box-error-exact-integer-gap.md).
The stronger version uses `(7/4)((1-x)^32,x^32)` and three rational boxes
whose general integer labels are zero, one, and two.

Taking independent input products gives the verified exact counts
`p_conv=n`, `p_bin=ceil(n log2 3)` for `n` inputs and `2n` outputs. The
lower bound uses thirds combinations and residues modulo three. This
demonstrates why an additive loss proportional to input dimension can be
necessary for this class; it does not answer the one-input question.

The one-input example excludes the exact equality `p_bin=p_conv`. It is
fully compatible with a universal overhead of one, two, or another constant.
Neither a naive direct product nor substituting oscillatory coordinate maps
can be advertised as a one-input amplification: direct products add inputs,
and oscillatory substitutions generally destroy componentwise convexity.

## Relevant primary lattice results

Lubin, Vielma, and Zadik,
[Mixed-integer convex representability](https://arxiv.org/abs/1706.05135),
provides the representability and midpoint-obstruction foundation already
credited by the repository. Finite fixed-integer fibers are convex, and
same-parity integer witnesses have an integral midpoint. Approximation
tolerance makes this weaker than forbidding all chords. The existing
positive-power family explicitly demonstrates the loss from using only
midpoint tests. This primary source does not by itself turn midpoint
compatibility into an output-independent error-preserving interval cover.

Averkov and Weismantel,
[Transversal Numbers over Subsets of Linear Spaces](https://arxiv.org/pdf/1002.0948),
Theorem 1.1, gives the mixed Helly identity
`h(R^k x Z^p)=(k+1)2^p`. It bounds sizes of infeasibility certificates
for convex sets. It does not assert that a graph admitted by a convex
integer lift can be covered by that many convex error-valid pieces.
Applying it to the complete lifted space also brings in the unrestricted
continuous auxiliary dimension. Eliminating those variables must precede
any use that hopes to depend only on `p` and one input coordinate, and
the necessary convex sets or certificate interpretation still need proof.

Onn, [On the Geometry and Computational Complexity of Radon Partitions in the Integer Lattice](https://epubs.siam.org/doi/10.1137/0404039)
(1991), proves that the integral Radon number is of order between `2^p`
and `p2^p` in its stated bounds and equals six in dimension two. The
publisher abstract was checked; the full linked mirror was inaccessible.
An integral Radon partition requires an integer point common to the convex
hulls of two disjoint subsets. This is stronger than the parity observation
that a convex hull has a nonvertex integer point. In particular, one must
not assume that `2^p+1` points always have an integral Radon partition.
The definitions and related estimates are also discussed after Theorem 1.4
of the opened Averkov–Weismantel manuscript.

Even a valid integral Radon partition has no ordering guarantee for the
corresponding scalar inputs. Their two supports can interleave, and the
two induced lifted points may have different input coordinates. A proof
still needs to show that these two mixtures force an error violation in
one common output. This implication was not established here.

## A useful formulation of the geometric obstacle

For an admissible convex lifted set `C`, a componentwise convex output
`F_j` has a convex strict upper-violation set

```
{(x,w,z,aux) in C : w_j>F_j(x)+epsilon_j}.
```

Convexity follows because this is the strict epigraph inequality for a
convex function in `(x,w_j)`. Its projection onto the integer coordinates
is convex and contains no integer point: such a point would correspond
to an invalid feasible integer slice. This connects each component to
ordinary lattice-free convex geometry.

The difficulty is simultaneous control. The union of these violation sets
over outputs need not be convex. Replacing that union by its convex hull
can introduce integer points without contradicting the original
formulation, since a convex combination of violations in different
components need not violate any component. Thus a lattice-free argument
for each output separately cannot simply be merged. The existing
scalarization/refinement proofs pay precisely for this simultaneous issue.

This is a reduction of the obstacle, not a theorem resolving it. It also
explains why an ordinary Helly number or a maximal lattice-free facet bound
does not immediately yield a constant-overhead formulation theorem.

## Source and investigation status

No inspected primary result resolved the exact one-input constant-overhead
question. That absence is not evidence of a positive or negative theorem.
The usable outcomes of this pass are the explicit strict one-bit example,
its correctly scoped growing-input product, and the distinctions between
parity, integral Radon, mixed Helly, and simultaneous lattice-free
violations. The output-independent one-input upper bound and a growing
one-input gap both remain unproved in this investigation.
