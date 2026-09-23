# Source audit: binary versus general-integer precision for nonconvex polynomials

Date: 2026-09-05. Status: bounded primary-source audit; independent mathematical
reviews remain separate.

The [candidate](nonconvex-polynomial-binary-integer-gap.md) gives a family of
one-input, one-output dense rational polynomial graphs at fixed absolute
tolerance `1/4`, with `p_conv<=2` but `p_bin>=ceil(log2 M)`. Its degree is
at most `1024 M^2`. Here both minima permit arbitrary convex continuous
lifts, while only the latter requires every integer coordinate to be binary.
The finite upper bound for a graph with `s` convexity intervals is
`p_bin<=p_conv+ceil(log2(3s))`; hence the worst-case degree dependence is of
order `log D`. Section 3 additionally claims a polynomial-time rational MILP
construction for any dense rational degree-`D` polynomial, with
`p_out<=p_conv+12+ceil(log2 D)`. This extension has been read for source scope;
its independent proof reviews and the inherited convex-hybrid dependency
reviews remain provisional. The upper formulations can be linear.

I did not find this polynomial-graph restriction and paired quantitative
bound in the checked primary literature. Broad separations between binary
and general-integer counts are elementary and established, so novelty should
be claimed only for the stated smooth connected graph family and its degree
dependence. This is a useful boundary complement to the convex-polynomial
results, rather than a new general binarization phenomenon.

## Binarization is the direct predecessor

[Dash, Gunluk, and Hildebrand, Binary Extended Formulations of Polyhedral Mixed-integer Sets](https://optimization-online.org/wp-content/uploads/2018/01/6403.pdf),
Sections 1--2, study replacing bounded integer variables with binary variables;
the paper explicitly includes logarithmic representations and credits earlier
work by Glover, Sherali--Adams, and Roy. Its main comparisons concern split
closures and branching, not minimum graph-approximation integer dimension.
This is the appropriate reference for the fact that the number of binary
coordinates can scale with the logarithm of a general integer's range.

The broad count separation can already be seen without a research theorem:
the set `{0,...,M-1}` has a one-general-integer formulation. In a binary
convex formulation, a fixed binary assignment cannot contain two distinct
points of this finite set, because their entire segment would also be
admitted. It therefore needs at least `ceil(log2 M)` binary coordinates.
The candidate transfers this repeated-discrete-structure advantage to an
approximation of a connected polynomial graph, with a fixed nonzero error
margin and no restriction on the competing binary lift.

It is worth saying explicitly that the two general integer coordinates in
the proposed upper formulation are bounded: one period index has `M`
possible values and the orientation bit has two. The result does not depend
on an infinitely large integer range, irrational coefficients, or a
nonpolyhedral upper formulation.

## Periodicity and convex representability

[Lubin, Vielma, and Zadik, Mixed-integer convex representability](https://optimization-online.org/wp-content/uploads/2017/06/6082.pdf),
Section 4.1, characterize binary convex representability through finite
unions of projected convex sets. This is the conceptual source for the
fixed-assignment chord obstruction. Their Theorem 1.1 recalls the
Jeroslow--Lowe rational MILP characterization, while Section 5 and
Proposition 5.1 discuss periodicity and recession structure. These results
explain why repeated motifs and integer shifts are natural modeling tools.
They do not provide the candidate's polynomial degree bound or contradict
its bounded period-index formulation.

The polynomial `q_M` is not being represented as an exactly periodic
nonconstant polynomial. Its *surrogate* is a repeated triangular motif on a
bounded interval, and a rational error band contains the polynomial graph.
The model represents an outer approximation, not the exact nonconvex
polynomial graph. Likewise, the lower bound uses a whole chord in a fixed
binary slice, not a midpoint/parity argument applied to unrestricted
integer coordinates. That distinction is necessary for consistency with
the small general-integer upper bound.

## Bernstein smoothing is classical

The approximation step is the usual probabilistic Bernstein argument. If
`B_N f(x)=E[f(X/N)]` for `X~Bin(N,x)` and `f` is `L`-Lipschitz, then

```
|B_N f(x)-f(x)| <= L E|X/N-x|
                 <= L sqrt(x(1-x)/N) <= L/(2 sqrt(N)).
```

No new approximation theorem or hidden numerical oracle is needed.
For a checked primary research antecedent,
[Gunturk and Li, Approximation with one-bit polynomials in Bernstein form](https://arxiv.org/pdf/2112.09183),
Section 1, recalls the classical Bernstein operator, and Section 3.1 discusses
its Lipschitz approximation rate before adding quantization constraints.
Their "one-bit" and unrestricted-integer alternatives concern polynomial
*coefficients*, not optimization decision variables. They are not a matching
binary-versus-general-integer formulation theorem.

The candidate's explicit rational Bernstein samples and polynomially bounded
dense expansion make the smoothing step appropriate for its encoding claim.
Preserving separated high peaks and low troughs by a uniform error margin
then gives the binary lower bound through elementary convexity. The choice
`N=1024 M^2` is a convenient degree bound, not a claim of best polynomial
approximation degree.

## The finite upper bound and compact extension

Partitioning at sign changes of the second derivative is standard. The
candidate applies the repository's scalar convex finite comparison on each
piece and codes the resulting union. Existing scalar approximation methods
also split by convexity: the
[hybrid source audit](compiled-convex-polynomial-hybrid-novelty.md) identifies
LinA's greedy segmentation and its explicit cost for such splitting.
The potentially new conclusion here is the comparison to the minimum
integer count of every convex lift, with an upper bound depending only
logarithmically on the number of pieces.

The finite bound allows real algebraic split points and unrestricted continuous
size. Section 3 supplies a separate compact construction: rational narrow
brackets cover roots of `f''`; complementary intervals use the convex hybrid,
with output reflection on concave intervals; brackets use direct chord bands.
One global index addresses the sum of the actual local cell counts, including
the differing band orientations. The number of pieces is at most `2D`, yielding
the stated `12+ceil(log2 D)` overhead. Rational root isolation and finite-union
compilation are established, as documented in the linked hybrid audit. The
potentially new constructive conclusion depends on the reviewed local hybrid
and its indexed form, not merely on the finite real-coefficient theorem.

The worst-case order is sharp in the sense of an `O(log D)` upper bound
for all degrees and a family with an `Omega(log D)` gap. It does not identify
the optimal leading constant, show a gap for every polynomial, or assert
that degree alone determines either minimum. It concerns integer counts,
not stronger relaxations, faster solving, or approximation hardness. A
bounded search found no matching combined theorem, but this remains a
qualified source assessment rather than proof of priority.
