# Extensions and corrections to binary-count lower bounds

Written 2026-09-05 during independent review. These proofs were derived
independently of the original note. The integer-dimension argument was
also independently identified by the graph novelty agent. The epigraph
counting argument is an elementary established-method consequence and is
not claimed as new. Root review remains appropriate before promoting any
extension as a principal result.

## Unrestricted integer variables obey the same lower bounds

Let a closed convex lifted set `K` define a relaxation of the graph of a
continuous function `f` on a compact box `B`, using `p` integer variables
`z in Z^p` and arbitrarily many continuous variables. The set need not be
polyhedral, and the integer ranges need not be bounded. Suppose its
vertical error is at most `ε`.

For each parity vector `a in {0,1}^p`, let `S_a` contain all `x in B` for
which `(x,f(x))` has a feasible lift whose integer coordinates have parity
`a`. These sets cover `B`. If `u,v in S_a`, choose such lifts. The average
of their integer vectors is integer, and the average of their full lifts
belongs to `K` by convexity. Therefore

```
|[f(u)+f(v)]/2 - f((u+v)/2)| <= ε.
```

The same inequality holds for every pair of points in `closure(S_a)` by
continuity. These closed subsets of the compact box cover `B`, so all
measure and diameter arguments in the original note apply unchanged with
`N=2^p`. No measurability or closed-projection assumption on `S_a` is needed.

Consequently, the square lower bound `ε >= 2^(-2p-2)`, the strongly convex
volume bound, and the product lower bound `ε >= 1/(16 ln(2) 2^p)` all bound
**integer dimension**, even for unrestricted integer variables in arbitrary
mixed-integer convex lifts. Binary sawtooth/NMDT constructions give the
same upper bounds, so general integer variables cannot improve these
accuracy-versus-dimension rates.

This is the parity mechanism of the published midpoint lemma, followed
by the original note's diameter/area estimates. Credit:
[[lubin2022-mixed-integer-convex-representability]] p.11-12,
[open primary source](https://optimization-online.org/wp-content/uploads/2017/06/6082.pdf).

## Square epigraphs require logarithmic LP extension size

Let `P` be any finite-dimensional polyhedron described by `m` linear
inequalities and any number of linear equalities. Its coordinate
projection `R` contains

```
{(x,w): 0 <= x <= 1, w >= x^2}
```

and has one-sided error at most `ε > 0` on `[0,1]`. Then

```
m >= log2(1/(2 sqrt(ε))) = (1/2) log2(1/ε) - 1.
```

Proof. The projected polyhedron is full-dimensional because it contains
the epigraph. Every valid inequality involving `w` must have a nonpositive
coefficient on `w`, since the epigraph is unbounded upwards. Thus over
`[0,1]` its lower boundary has the form `g(x)=max_(k=1,...,q) l_k(x)`, where
the `l_k` are affine and correspond to its distinct lower facets. Error
control implies `x²-ε <= g(x) <= x²`.

Each lower facet is active on an interval `I_k` (possibly clipped by the
box). If that interval has length `h`, its endpoints `a,b` obey
`l_k(a) >= a²-ε` and `l_k(b) >= b²-ε`. At the midpoint `c`, linearity gives

```
l_k(c) >= [a²+b²]/2 - ε = c² + h²/4 - ε.
```

Since `l_k(c) <= c²`, necessarily `h <= 2 sqrt(ε)`. The facet intervals
cover `[0,1]`, hence `q >= 1/(2 sqrt(ε))`.

Each lower facet of `R` is the image of a distinct nonempty exposed face
of `P`: pull back its supporting linear functional along the projection.
Different facets give different exposed faces, since the projected face
is exactly that facet. A polyhedron described by `m` inequalities has at
most `2^m` faces: each face is determined by the subset of inequalities
that are identically tight there. Equalities and lineality do not alter
this upper bound. Hence `q <= 2^m`, proving the claim.

The zero-binary sawtooth epigraph relaxation has `O(log(1/ε))` inequalities
and continuous variables, so the logarithmic order is sharp. This
counting result does not assert a sharp leading coefficient, and it does
not count or restrict coefficient bit lengths.

## Interaction graphs and unequal tolerances

Independent derivation converged with root's investigation: for the
simultaneous graph `w_ij=x_i x_j` on the unit cube, binary/integer dimension
is asymptotic to `τ*(G) log2(1/ε)`, where `τ*(G)` is fractional vertex cover.
Each parity class has coordinate widths `d_i` obeying `d_i d_j <=20ε`
for every edge. A fractional cover LP bounds the volume of its enclosing
box, and an unequal-depth shared binary expansion matches that bound up
to an additive graph-dependent constant.

The more precise theorem for unequal edge tolerances, its compact
formulation, and detailed proof are developed in
`results/bilinear-graph-binary-complexity.md`; the independent audit is
`notes/review-bilinear-graph-binary-complexity.md`.

## A width-constant obstruction worth retaining

A tempting strengthening of the product-difference width lemma from
`d_x d_y <=5δ` to `d_x d_y <=4δ` is false, even for four points. Let
`s=sqrt(5)-2` and take

```
a=(0,(1-s)/2), b=(1,(1+s)/2),
c=((1+s)/2,0), d=((1-s)/2,1).
```

Both coordinate widths are one. Every one of the six pairwise absolute
products of coordinate differences equals `s`, since `1-s²=4s`.
Therefore a universal bound `d_x d_y <=Cδ` requires
`C>=1/s=2+sqrt(5)>4`. The retained bound `C=5` remains valid.
This finite example does not settle an area inequality or realizability
as a positive-volume contact set, and no sharpness claim for `2+sqrt(5)`
is made. It prevents an incorrect constant improvement based only on
axis-aligned diamond intuition.
