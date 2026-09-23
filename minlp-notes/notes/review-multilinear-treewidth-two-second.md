# Second independent audit: incidence treewidth two

Reviewer: `review_scaling_characterization`. Date: 2026-09-04.

**Conclusion:** the complete analytic proof in
[the candidate result](../results/positive-multilinear-treewidth-two-exact.md)
is correct. I found no unresolved mathematical issue in the factor-coloring
lemma, its balanced-matrix consequence, the gap transfer, or sharpness. This
audit is independent of the finite-state closure calculation and does not use
that calculation as a certificate. Novelty remains a separate question.

## Meaning of the state invariant

I checked the invariant against actual colored graphs, not only transition
signatures. A path counts its factor endpoints in its factor parity. In series
composition, the common factor is counted twice before correcting the parity;
the correction is therefore its type, `delta`. In parallel composition, each
factor terminal is counted twice in the two paths but once in the resulting
cycle; the correction is the parity of the number of factor terminals.

The active alternative guarantees both existence and parity purity of the
selected-color paths. Its prohibition on other-color paths is essential only
for variable-variable terminals; a factor terminal of the selected color
already excludes them otherwise. Blocking alternatives are required only in
the precise cases stated in the draft. These are existence guarantees for
possibly different colorings. They need not characterize every attainable
signature, and the proof does not incorrectly assume they do.

All cycles in a series composition belong to one child. A simple cycle using
both children of a parallel composition traverses one simple terminal path in
each child: the children share only their two terminals. It cannot alternate
between the children more often without revisiting a terminal. Thus the stated
cycle-parity test covers every new cycle, even if the paths have chords.

## Exhaustive composition check

The active series alternatives always glue: choose a common active color, and
when the identified vertex is a factor this also matches its actual color.
All resulting terminal paths have parity
`epsilon_1 XOR epsilon_2 XOR delta`.

Here is my independent check of all required non-active series alternatives.
Outer-terminal reversal accounts for both orders of the mixed type.

| Outer terminals | Middle type | Required alternative and why it exists |
|---|---|---|
| VV | V | Opposite child active colors prevent either color from crossing. |
| VV | F | Output parity zero requires opposite child parities. The even mixed child cannot have a direct edge, so it can block while preserving the shared factor color. |
| VF/FV | V | Give the VV child the active color opposite the outer factor color. |
| VF/FV | F | Give the common factor the color opposite the outer factor. The FF child then has different endpoint colors and blocks. |
| FF, same endpoint color | V | Output parity one requires opposite child parities. The even mixed child has no direct edge and supplies its prescribed-endpoint blocking alternative. |
| FF, same endpoint color | F | Color the middle factor oppositely. Both children use their different-endpoint alternatives. |
| FF, different endpoint colors | V | Each mixed child takes the active color prescribed at its own outer endpoint. |
| FF, different endpoint colors | F | Choose either middle color. Each FF child uses its same-color active or different-color alternative as appropriate. |

These rows cover the eight ordered type triples up to reversal, with the two
FF endpoint-color requirements separated. A nontrivial series composition has
no direct outer terminal edge, and the mixed blocking cases above cover this
new requirement.

For parallel composition:

* VV children with equal parities may both be active in the same color. Even
  children can both block when needed. With unequal parities the even child
  blocks and the odd child is active. Output parity is their Boolean OR.
* FF children with the same prescribed endpoint color behave dually: unequal
  parities use the even child actively and block the odd child. Two odd children
  can both block. Output parity is their Boolean AND. Distinct prescribed
  endpoint colors automatically prohibit any crossing monochromatic cycle.
* Mixed children without a direct terminal edge both have a blocking option
  with either prescribed factor-terminal color. Activate just one for an active
  output and block both for a blocking output. Either child's parity can be
  chosen as the output invariant parity, consistently for both colors.
* If a mixed network has a direct edge, simplicity implies that exactly one
  child contains it. That child's invariant parity is one. Activate it and
  block the other child. No blocking output is required.

Whenever both parallel children are active, the terminal types agree and the
path parities agree, so the new cycle has even factor parity. In the mixed
cases at most one child has monochromatic terminal paths. This completes the
analytic induction, without a numerical closure assumption.

## Coverage of all incidence graphs

Treewidth at most two excludes a K4 minor and hence a subdivision of K4.
Hassin and Tamir's Theorem 3.1 states that every biconnected component of a graph
without a K4 subdivision is series-parallel; the recursive terminal definition
on the same page is exactly the one used here. I inspected the scanned primary
page directly: [*Efficient algorithms for optimization and selection on
series-parallel graphs*, printed p.381](https://www.math.tau.ac.il/~hassin/sp.pdf).
The usual terminal recursion is also explicit in
[Eppstein's primary paper, pp.1–2](https://www.ics.uci.edu/~eppstein/pubs/Epp-IC-92.pdf).

The recursive children may be taken as subgraphs of the final simple bipartite
block. They are therefore themselves simple and bipartite; the proof does not
need to color temporary edges introduced by an elimination algorithm. Bridges
are base networks. Root the block-cut forest, flip all colors in a new block
when its attaching factor vertex requires it, and continue. Each block attaches
through only one previously colored articulation vertex. Every cycle lies in
one block. Isolated factor vertices may receive either color; I suggested
making this harmless final case explicit.

Deleting the factor vertices of the other color cannot create a cycle that
was absent from the original graph. A forbidden odd-order cycle submatrix of
a 0/1 incidence matrix gives a simple incidence cycle containing an odd number
of factors. The good coloring prohibits such cycles, so both color matrices
are balanced. The proof is stronger than merely eliminating induced odd Berge
cycles, which creates no difficulty.

## Stronger total-unimodularity consequence

The first reviewer also proposed the stronger conclusion that each color matrix
is totally unimodular. I independently verified it using Camion's criterion,
stated as Theorem 6.5 on printed p.76 of the same Cornuéjols manuscript. Given
any submatrix with even row and column degrees, decompose its bipartite graph
into edge-disjoint simple cycles. Every such cycle lies in the monochromatic
incidence graph, so its length is divisible by four. The total number of ones
in the submatrix is therefore divisible by four. Camion's criterion applies
and proves total unimodularity. Thus the graph theorem supplies a partition
into two TU row submatrices, not just two balanced row submatrices. This
consequence does not require any additional graph argument.

## Balanced exactness, marginals, and the ratio

I checked the precise mixed-inequality theorem in
[Cornuéjols' author manuscript, Theorem 6.13, printed p.82](https://www.andrew.cmu.edu/user/gc0v/webpub/notes.pdf).
For a balanced 0/1 matrix it indeed gives integrality with an arbitrary mixture
of packing and covering rows at right-hand side one, and with unit-cube bounds.
It is not necessary to assume that packing-only and covering-only integrality
survive intersection; the cited theorem supplies that stronger conclusion.

For each color, the prescribed failure-mean vector belongs to its corresponding
mixed polytope. Since the polytope is bounded and integral, a convex combination
of binary vertices supplies one global law with exactly those singleton means.
Packing rows have at most one failure in every support point and therefore
attain union probability equal to the sum of their failure means. Covering rows
have a failure in every support point. At a row whose mean sum is exactly one,
the packing choice still gives union probability one.

Thus every term of the selected color attains its individual lower envelope
under the same law. Deficiencies of the other color are nonnegative pointwise.
The half-half mixture keeps all singleton means and achieves at least half of
every term's deficiency, simultaneously. Positivity of coefficients and the
common comonotone upper-envelope law give the claimed full gap inequality.
Zero means, unit means, zero coefficients, empty color classes, and zero gaps
cause no division or conditioning issue. Affine and constant terms are safely
discarded.

The stated box extension is correctly restricted to zero lower endpoints.
Expanding positive-lower-endpoint monomials into smaller positive monomials can
change balancedness and incidence treewidth, so that route would not establish
an additional extension here. The draft explicitly avoids that claim.

## Exact lower family

For `f(a,x)=a sum_i x_i+product_i x_i`, at `a=1/n` and `x_i=1-1/n`, each
bilinear gap is `1/n`, and the product gap is `(n-1)/n`. Thus `T=2-1/n`.
With binary anchor `A` and leaf failure count `R`, the total deficiency is
`E[AR]+Pr(R>=1)-1/n`. The pointwise inequality

`AR+1[R>=1] <= R+A`

holds separately for `A=0` and `A=1`, including `R=0`. Since `ER=1` and
`EA=1/n`, it bounds `H` by one. A uniformly chosen single failed leaf and an
independent anchor attain one.

The incidence graph has a width-two decomposition with path bags
`{a,e_0,x_i}` and a leaf bag `{a,x_i,e_i}` attached at each corresponding path
bag. All occurrences of every vertex are connected. For `n>=2` the graph
contains a cycle, so its treewidth is exactly two. Ratios approach two; the
statement correctly claims a sharp supremum, not attainment of ratio two by
one finite member of this family.

## Extension audit: a fixed positive common aspect ratio

Root subsequently proposed a lower family valid on `[epsilon,1]` for every
fixed `epsilon` in `(0,1)`. Put `alpha=1-epsilon` and use

\[
f(a,x)=\alpha^{-1}a\sum_{i=1}^n x_i+\prod_{i=1}^n x_i,
\]

with normalized means `EA=1/n` and `EX_i=1-1/n`, so the original variables are
`a=epsilon+alpha A` and `x_i=epsilon+alpha X_i`. I independently verified the
following calculation.

The nonlinear part of each normalized bilinear term is `alpha A X_i`; all
remaining terms are affine. Their summed termwise gap is `alpha`. Write `R`
for the number of failed leaves, so `ER=1` and the product equals `epsilon^R`.
Its concave-envelope value is `1-(1-epsilon^n)/n`, attained by comonotone
leaves. Its convex-envelope value is `epsilon`, by Jensen's inequality for
the convex function `r -> epsilon^r`, with equality under a law with exactly
one uniformly selected failure. Hence

\[
T=2\alpha-\frac{1-\epsilon^n}{n},\qquad
H=\max_P\mathbb E_P[\alpha AR+1-\epsilon^R]
  -\frac{1-\epsilon^n}{n}.\tag{2}
\]

For any real `M>0`, the following pointwise bound is valid:

\[
\alpha AR+1-\epsilon^R
\le \alpha R+\alpha MA\,\mathbf1_{R\le M}+\mathbf1_{R>M}.
\]

On `R<=M`, use `AR<=MA` and `1-epsilon^R<=alpha R`; on `R>M`, use `AR<=R`
and `1-epsilon^R<=1`. Therefore

\[
H\le\alpha+\frac{\alpha M}{n}+\frac1M.
\]

The law with exactly one failure and an independent anchor gives

\[
H\ge\alpha+\frac\alpha n-\frac{1-\epsilon^n}{n}.
\]

Taking `M=sqrt(n)` proves `H -> alpha>0`, while `T -> 2alpha`. The ratio
therefore tends to two for every fixed positive aspect ratio `1/epsilon>1`.
The incidence graph is unchanged and has exact treewidth two. All monomial
coefficients are positive; the bilinear coefficient depends on the fixed
aspect ratio, which the claim permits.

The matching common-aspect upper has a direct TU mechanism. For each factor,
its normalized product is a positive constant times `epsilon^{R_e}`. At a
prescribed mean `S_e=ER_e`, the minimum expectation is the linear interpolation
of the values at `floor(S_e)` and `ceil(S_e)`. This follows from the convex
piecewise-linear interpolation of the sequence `epsilon^r` and Jensen's
inequality. For each TU color matrix `A`, the polytope

\[
0\le z\le1,\qquad \lfloor Ap\rfloor\le Az\le\lceil Ap\rceil
\]

is integral and contains `p`. Its vertex decomposition produces one law
attaining all these factor minima simultaneously. Mixing the two laws gives
half the sum of individual gaps: any other factor's expected value is at most
its own concave-envelope value, and the full positive polynomial has a common
comonotone upper-envelope law. This also explains why TU, rather than the
weaker balanced property, is useful for the positive-common-aspect extension.

I then reread the author's final section, **Convex cardinality factors and
common-ratio positive boxes**, including its more general corollary for
arbitrary discrete-convex vertex sequences. That full extension also passes.
The floor/ceiling argument applies to the convex interpolation of any such
sequence, not only exponentials. The factor's vertex set function is
supermodular, even if the sequence is negative or decreasing. Thus the same
common-threshold law simultaneously maximizes all factor expectations. The
usual uncrossing justification is rigorous: among maximizing distributions,
maximize the expected square of the support-set size. Replacing two
incomparable positive-mass sets by their intersection and union cannot
decrease the supermodular objective, preserves singleton means, and strictly
increases the secondary potential. Hence an optimal distribution has chain
support, which is the common-threshold law for the given means.

This proves the simultaneous upper-envelope identity needed for the mixture
argument. The proof never assumes arbitrary nonnegative local payoff tables,
so it is consistent with the separate parity-factor counterexample at width
two. The positive-box condition is correctly imposed separately within each
original scope; shared variables automatically enforce compatible ratios
where those scopes overlap. No product expansion or incidence modification
is used. Both displayed tail inequalities and the final scaling to `[1,rho]`
in the author's final version agree with the independently checked lower
calculation above.
