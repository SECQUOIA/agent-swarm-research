# Independent review of Jacobi normalization and residual clipping

Date: 2026-10-02. Status: passed. Reviewed the complete
[normalization note](../new-direction/jacobi-copositive-residual.md), including
the randomized clipping argument. This review derives the main inequalities
independently; it does not assess external priority.

**Verdict.** The exact diagonal-scaling optimum, rational factor-four
approximation, margin-preserving clipping, fixed-threshold conic
equivalence, and local-sum composition are correct under their stated
hypotheses. No substantive correction is required. They do not establish
existence or efficient discovery of a suitably conditioned extraction.

## Scaling and rational arithmetic

For any positive diagonal congruence, put `m=max_i d_i^2 R_ii` and
`h=g(D R D)`. Substitution in the growth inequality gives copositivity of
`R-h D^(-2)`. Since `D^(-2)>=J/m` on the diagonal, adding the resulting
nonnegative diagonal proves `R-(h/m)J` copositive. Thus `h/m<=gamma(R)`.
Jacobi scaling has unit diagonal and growth exactly `gamma(R)`, so it
attains the displayed optimum `2/gamma(R)` rather than only approaching
an infimum. Strict copositivity is sufficient to make every inverse and
growth constant in this argument well defined.

The dyadic factors with `1<=d_i^2 R_ii<4` have polynomial encoding length
for rational positive diagonal data. Congruencing the normalized margin
inequality gives growth at least `gamma(R)` and coordinate curvature at
most eight. This is precisely a factor-four loss from the best ratio.
It supplies rational scaling once the residual is given; it does not
bound the encoding of an independently sought extraction.

## The clipping process has the correct inequality direction

Let `C` cap all off-diagonal entries of a copositive `B` at
`a>=max_i B_ii`, with `a>0`. Choose an edge actually changed by this
operation whose two current coordinates are positive. If their sum is
`s`, replace `(x_i,x_j)` by `(s,0)` with probability `x_i/s` and by
`(0,s)` otherwise. This preserves the conditional mean of the full
vector.

On the transfer segment, the coefficient of the squared transfer
coordinate in `x'Cx` is `B_ii+B_jj-2a<=0`. All terms involving a
third coordinate are affine. Thus endpoint randomization decreases
the conditional expected capped objective. In the unit-diagonal case
with cap one, that coefficient is zero and expectation is unchanged.
This is the asserted supermartingale direction.

Each transfer removes a positive coordinate without activating a zero
one outside the selected pair. After at most `n-1` transfers, no changed
edge has two active endpoints, so every terminal outcome satisfies
`Y'CY=Y'BY`. Padding stopped paths by identity steps makes the finite
expectation argument explicit. Consequently

```
x'Cx >= E[Y'BY] >= g(B) E||Y||^2 >= g(B)||x||^2.
```

The last step uses both mean preservation and `g(B)>=0`. Copositivity
is therefore a material hypothesis, not an assumption that can be
discarded from the clipping lemma. Conversely `C<=B` entrywise bounds
its Rayleigh quotient above by that of `B` on nonnegative vectors.
Together these inequalities prove `g(C)=g(B)`, including the zero-margin
case. The finite random process is a proof device and adds no randomized
algorithm or probabilistic certificate requirement.

The diagonal is unchanged. Two-coordinate copositivity gives
`B_ij>=-sqrt(B_ii B_jj)`, so capping the dyadically scaled matrix at four
does yield a rational matrix with every entry in `[-4,4]`, unchanged
growth, and unchanged coordinate curvature. Clipping and diagonal
congruence introduce no new nonzero edges.

## Extraction and local composition

At a fixed positive threshold `tau`, the strict diagonal condition and
copositivity of `R-tau diag(R)` imply strict copositivity of `R`.
The scaling optimum therefore proves both directions of the stated
existential equivalence. Every matrix expression is affine when `tau`
is fixed. This does not make copositive feasibility tractable, remove
the strict inequalities, or show that an optimal extraction is attained.
The note makes none of those stronger claims.

Embedding a bag-copositive matrix into global coordinates preserves
copositivity: a nonnegative global vector restricts to a nonnegative
bag vector. Summing the local inequalities commutes exactly with taking
diagonals, including repeated occurrences. Coverage of every global
coordinate ensures the assembled residual has positive diagonal.
Thus the same `tau` survives without an occurrence factor. This uses
a supplied decomposition satisfying all local conditions; global
strict copositivity and bounded width alone do not establish those
conditions. The explicit support restrictions and the warning about
changed box side lengths correctly limit the algorithmic conclusions.

## Verification record

The proof review used the actual file and the displayed cone and
conditional-expectation arguments. A scoped Python document check passed
for this review and the source note: trailing whitespace, paired display
math delimiters, and local links. No numerical optimization test, external
search, delegation, project-wide check, CI inspection, or index edit was
performed. No claim of novelty follows from this review.
