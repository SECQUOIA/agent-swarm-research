# Independent review: joint sharp multilinear gap dependence

Date: 2026-09-04. Reviewer: `review_scaling_characterization`.
Reviewed: `results/positive-multilinear-joint-gap-growth.md`.

## Verdict

The synthesis theorem and its simultaneous lower construction are correct on the
intended large-`q` asymptotic branch. It gives

```
C(n,d,k,δ) ~ min{k, ln q/ln ln q},
q=min(n,d,1/δ),
```

as that minimum tends to infinity, with `q` restricted to be sufficiently large.
The same proof establishes the two-sided marginal-strip version and the
incidence degeneracy and orientation versions. The lower family already has
unit coefficients. This is a proof audit of the synthesis, not a separate
literature priority assessment.

The final written theorem explicitly requires `q≥exp(e)`, as requested during
review. I checked that patch. This removes the pole at `q=e` from the allowed
parameter range and makes the implication from `r→∞` to `q→∞` valid. The final
statement and proof have no unresolved issue.

## Uniform upper bound along joint parameter sequences

The separate degree, dimension, and marginal-floor theorems give errors tending
to zero as their one scalar argument tends to infinity. Whichever of
`n,d,1/δ` attains `q`, its corresponding bound is
`(1+ε(q))φ(q)`, where `φ(q)=ln q/ln ln q` and `ε(q)→0`. The maximum of the three
error functions can be used, so changing which parameter is smallest along a
sequence introduces no loss of uniformity.

The incidence theorem gives `(1+η(k))k`, where `η(k)→0`, for treewidth,
degeneracy, and maximum orientation outdegree. Thus the joint upper bound is
at most

```
min{(1+ε(q))φ(q),(1+η(k))k}
 ≤ [1+max(ε(q),η(k))] min{φ(q),k}.
```

On a fixed sufficiently large branch, `r=min(k,φ(q))→∞` implies both `q→∞`
and `k→∞`. Both errors therefore vanish along every allowed joint sequence.
This argument does not require one parameter to dominate the others by a fixed
factor. Ties among controlling parameters are harmless.

## Floor choices and a uniform radix estimate

Set

```
r=min(k,φ(q)),
L=floor(r),
b=floor((q/2)^(1/L)),
m=b^L.
```

For large enough `r`, `L≥2`. Since `L≤φ(q)` and `q/2>1`,

```
b≥(q/2)^(1/φ(q))−1
 = ln q · exp[−(ln2)(ln ln q)/(ln q)]−1.
```

The last expression is `(1−o(1))ln q`, independently of `k` and `L`.
In particular, for a sufficiently large absolute threshold for `q`,

```
b≥(ln q)/2,
L/b≤2/ln ln q.
```

Hence `b≥L` eventually, again uniformly over all choices of `k`.
The hypothesis needed by the exact variable-radix gap and treewidth results
therefore holds. The floor in the radix is fully accounted for by the minus one;
it does not accumulate an uncontrolled error through the power `b^L`.

The exact inequality needed for the size restrictions is simply
`m=b^L≤q/2`, which follows directly from the radix definition. No lower estimate
on `m` is required.

## Every restriction is satisfied simultaneously

Use the previously reviewed `L`-level, radix-`b` construction. It has `m` leaves,
`L` anchors, unit coefficients, and exact ratio

```
L/[1+(L−1)/b].
```

Its dimension obeys

```
m+L≤q/2+φ(q)≤q≤n
```

for all sufficiently large `q`. Its largest monomial has degree `m/b+1`, so

```
m/b+1≤m+1≤q/2+1≤q≤d.
```

The original incidence graph has treewidth exactly `L`, since `b≥L`. Hence it
has treewidth at most `k`. Its degeneracy and minimum possible maximum
orientation outdegree are no larger than its treewidth, so the same single
construction meets either alternative structural restriction as well.

At the selected point the anchors have means `b^(−j)`, and the leaves have
means `1−1/m`. Since `q≤1/δ`, we have `δ≤1/q`. Moreover,

```
1/m≥2/q≥δ.
```

Thus even the smallest anchor mean is at least `δ`. The largest anchor is
`1/b≤1/2≤1−δ`. Because `m≥4` eventually, every leaf success mean is at least
`1/2≥δ`; its failure mean is `1/m≥δ`, so its success mean is also at most
`1−δ`. All coordinates therefore lie in the full strip `[δ,1−δ]`.

The number of monomials is
`Σ_(j=1)^L b^j=b(m−1)/(b−1)≤2m`, as stated, although no term-count restriction
is needed in this joint theorem. Every included term is nonlinear, so deleting
affine terms causes no change to this construction's graph.

## Explicit joint lower error

The floor error satisfies `L/r≥1−1/r`. Using the uniform radix estimate above,
the exact lower ratio divided by `r` is at least

```
(1−1/r)/(1+2/ln ln q).
```

This tends to one along every permitted joint sequence. It explicitly shows
that the lower proof is uniform even when `k` grows much more slowly than
`φ(q)`, when `φ(q)` grows much more slowly than `k`, or when they remain close.

Since the upper bound applies to all positive coefficients and the lower family
has unit coefficients and two-sided interior means, the same leading constant
holds under those additional restrictions. Combining the upper and lower
estimates proves the claimed joint asymptotic equivalence.

## Scope

The proof does not identify exact values when the minimum controlling parameter
stays bounded. In particular, it cannot be specialized to a claim about the
exact treewidth-two constant by sending only the other parameters to infinity.
Dimension and degree are upper limits, and the proof appropriately uses slack
in both. The graph statements concern the original support incidence graph.
For extensions to other boxes, incidence-preserving zero-lower-bound scaling
is legitimate, whereas positive-lower-bound expansion requires a separate
structural argument.
