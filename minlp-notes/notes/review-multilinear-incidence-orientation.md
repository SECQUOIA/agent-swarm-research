# Independent review: incidence-orientation bound for positive multilinear gaps

Date: 2026-09-04. Reviewer: `review_scaling_characterization`.
Reviewed construction: asymmetric incidence-orientation theorem proposed by
`new_directions`; full draft review is recorded below when available.

## Verdict on the derivation

The proposed proof is valid. If the incidence graph of a positive multilinear
polynomial on the unit box admits an orientation with variable outdegree at most
`r` and factor outdegree at most `s`, where `r,s` are nonnegative integers, it gives

```
tbtgap ≤ [r+s+2/(1−e^(−1))] chgap.
```

In particular, a common outdegree bound `k` gives
`2k+2/(1−e^(−1))`. The proof constructs compatible global laws, despite the
term-dependent packing of failure events. That compatibility depends on ownership
of high variables being disjoint within each round and on globally fixed low
variables. The theorem concerns unit boxes, and extends directly to boxes with
zero lower bounds; expansion on arbitrary nonnegative boxes does not automatically
preserve its structural hypothesis. This review makes no literature novelty claim.

## Deficiencies and the global partition of variables

Let `c=1−e^(−1)`. Remove affine terms, which do not affect either gap. Classify
variable `i` as low when its prescribed mean satisfies `x_i≤1/2`, and high otherwise.
For each factor choose a minimum-marginal coordinate, with marginal `u`, and write
`p_j=1−x_j` for the other failure marginals. Its term gap is
`T=min(u,Σ_j p_j)`, and its deficiency in any joint binary law is the event that
the selected coordinate is one and at least one other coordinate is zero.

Independent rounding supplies at least `(c/2)T` for every factor with zero or
at least two low variables, as proved in the independently reviewed degree
bound. The remaining factors have exactly one low variable. Its identity is
unambiguous, and every other variable of such a factor is globally high. In
particular no variable being assigned as a high variable in an ownership round
is simultaneously required to act as a low anchor elsewhere.

For a one-low factor split its high incidences into incoming incidences
`variable→factor`, denoted `I`, and outgoing incidences `factor→variable`, denoted
`O`. The unique low incidence can have either orientation and is not needed in
these two sets. Define

```
T_I=min(u,Σ_(j∈I)p_j),
T_O=min(u,Σ_(j∈O)p_j).
```

The split-gap inequality is in the required direction:

```
T=min(u,Σ_I p_j+Σ_O p_j) ≤ T_I+T_O.
```

It follows directly by considering whether either partial sum reaches `u`, or
whether both are smaller than `u`.

## Ownership rounds and simultaneous marginal feasibility

At each high variable, assign distinct colors from `{1,...,r}` to its outgoing
incidences that enter one-low factors. There are at most `r` such incidences,
so this local assignment is possible without any global edge-coloring theorem.
For a fixed color, every high variable is owned by at most one factor. A factor
may own many high variables, and this does not cause a conflict because ownership
sets of different factors are disjoint within that round.

Use one global uniform random variable `U∈(0,1)`. Every low variable is always
set to one when `U≤x_i`, in every ownership round. A factor's anchor event is
therefore the fixed window `[0,u]`.

For each factor's owned high group, choose failure subsets of `[0,1]` with the
prescribed measures `p_j` so their union inside `[0,u]` has measure
`min(u,Σ_owned p_j)`. Such subsets exist explicitly:

- If `u=0`, the target gain is zero and arbitrary prescribed-measure failure
  subsets can be used.
- If some `p_j≥u`, give that variable a failure subset containing all of `[0,u]`
  and enough of its complement to reach measure `p_j`. This is possible because
  `p_j≤1`. Choose the other variables' failure subsets arbitrarily with their
  prescribed measures.
- Otherwise every `p_j<u`. Place consecutive arcs of lengths `p_j` around the
  circle obtained by identifying the endpoints of `[0,u]`. Each arc has the
  required measure. Their union is an initial segment if their total length is
  below `u`, and the whole circle if it is at least `u`.

The failure subsets may be chosen independently for different factors because
they assign disjoint sets of high variables. Every unowned high variable receives
an arbitrary failure subset of measure `p_j`, such as `[0,p_j]`. This defines
one actual global law: high variable `j` fails exactly when `U` belongs to its
assigned subset. All marginals are correct, including the low anchors' marginals.
No conditional-independence assumption is needed in these ownership rounds.

Other high variables of a factor, perhaps owned elsewhere, cannot reduce its
deficiency: additional failures can only increase the union event. Thus a factor
gets deficiency at least `min(u,Σ_owned p_j)` in each round. Summing over the
`r` rounds gives at least

```
Σ_round min(u,Σ_owned_in_round p_j) ≥ min(u,Σ_(j∈I)p_j)=T_I.
```

This uses the same elementary subadditivity of the capped sum, now across rounds.
When `r=0`, the incoming set is empty and the bound is zero, so no ownership
rounds are needed.

## Outgoing incidences and the threshold law

In one additional law, use the same low thresholds and let every high variable
fail when `U≤p_j`. For a one-low factor, the deficiency is exactly
`min(u,max_j p_j)`. The number of outgoing high incidences is at most `s`, since
the entire factor outdegree is at most `s`. Therefore

```
T_O ≤ s min(u,max_(j∈O)p_j)
    ≤ s · deficiency_threshold.
```

If `O` is empty its gap contribution is zero. If `s=0`, every such set is empty
and this law can be omitted. These conventions avoid division by zero or a
maximum over an empty set.

## Combining the laws

Let `Z=r+s+2/c`. Give each ownership round probability `1/Z`, the threshold
law probability `s/Z` when `s>0`, and the independent law probability `(2/c)/Z`.
The weights sum to one and every component has the same singleton means.

A one-low factor gets combined deficiency at least `(T_I+T_O)/Z≥T/Z`.
An easy factor gets at least `T/Z` from independence. All omitted contributions
are nonnegative. Multiplying by nonnegative factor coefficients and summing,
the full hull deficiency is at least `tbtgap/Z`, which proves the bound.

The argument applies to coefficients of any nonnegative magnitude and any
number or degree of factors. Zero coefficients can simply be omitted. Identical
positive monomials may be merged, but this is not needed for the argument if
separate factor nodes are retained.

## Structural consequences and limits

A graph of degeneracy at most `k` admits an orientation with every outdegree at
most `k`: repeatedly delete a vertex of degree at most `k` and orient its edges
toward vertices deleted later. A graph of treewidth at most `k` has this degeneracy
property, by taking a vertex present only in a leaf bag of a reduced tree
decomposition and then applying the same argument after each deletion. Thus a
bounded incidence treewidth gives the claimed constant independently of monomial
degree. This is a statement about the original bipartite variable-factor incidence
graph, not primal graph treewidth or a factor-only coloring.

A bounded variable occurrence count `r` gives another specialization: orient
every edge from its variable to its factor, so `s=0` and the bound is `r+2/c`.

On a finite box `[0,b]`, scaling each nonfixed coordinate preserves the factors
and their incidence graph and merely rescales positive coefficients. Coordinates
with upper bound zero can be fixed and removed. Thus the same bound applies.
On a box with positive lower bounds, expanding a single original factor can
create many new factors and increase variable outdegrees or incidence width.
The general positive-expansion argument used for degree bounds therefore does
not automatically yield this incidence bound for the original graph. Any such
extension needs a separate argument.

## Full written draft and optional improvement checked

I subsequently read the complete
`results/positive-multilinear-incidence-sparsity-gap.md`. Its ownership construction,
cyclic packing, zero cases, mixing weights, and structural scope agree with the
independently verified proof above. No mathematical issue was found.

The optional refinement is also correct:

```
tbtgap ≤ [r+min(s,B(s+1))+κ] chgap,
κ=2/(1−e^(−1)),
```

where `B` is any valid positive multilinear degree bound and `B(1)=0`.
For each hard original factor form its reduced monomial using the same anchor
and only the outgoing high variables, retaining its coefficient. Its deficiency
is pointwise at most that of the original factor. Thus the reduced positive
polynomial has full hull gap no greater than the original polynomial's hull gap.
Its term-by-term gap is precisely the weighted sum of the outgoing quantities
`T_O`, and its degree is at most `s+1`. A reduced term with empty outgoing set is
affine and contributes zero deficiency and zero gap. Duplicate reduced terms
can be merged without changing these identities.

Applying `B(s+1)` bounds the entire weighted outgoing gap sum by
`B(s+1) chgap_original`. This use requires only a polynomial-level gap theorem,
not an unjustified simultaneous termwise guarantee. The ownership law bounds
the weighted incoming gap sum by `r chgap_original`, and independence bounds
the easy gap sum by `κ chgap_original`. The threshold law supplies the alternative
`s` outgoing bound. Adding them proves the claimed refinement.

The stated frequency example is valid. With `r≥2`, the polynomial
`a Σ_(i=1)^r x_i+∏_i x_i` has anchor frequency `r` and other variable frequencies
two. At `a=1/r`, `x_i=1−1/r`, its term-by-term gap is `2−1/r` and its hull gap
is one, as in the previously audited feedback example.

A stronger asymptotic frequency lower bound also follows from the already verified
dyadic family: with `m=2^ell` leaves, the largest variable frequency is `m`, attained
by the final anchor; leaf frequency is only `ell`. Its ratio is asymptotic to
`ln m/ln ln m`. Choosing the largest power of two not exceeding a frequency
allowance `r` therefore gives

```
R_freq(r) ≥ (1−o(1)) ln r/ln ln r.
```

This does not alter the correctness of the draft's smaller fixed-`r` lower bound,
but shows that variable frequency cannot be omitted from all universal constants.
