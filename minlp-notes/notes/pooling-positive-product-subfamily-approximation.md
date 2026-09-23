# An LP approximation scheme for the positive-product pooling subfamily

Date: 2026-09-05. Status: independent mathematical review PASS for the
lemma below; novelty unclaimed.

The [two-pool hardness construction](../results/pooling-two-pools-two-outputs-hardness.md)
has a useful exact-versus-approximate distinction. Its maximum profit is

```
OPT = max_{z in P} b(z)(1+1/a(z)),
```

where `P` is a nonempty bounded rational polytope and `a,b` are rational
affine functions satisfying `a>=1,b>=0` on `P`. This particular subfamily
admits a fully polynomial approximation scheme using linear programming,
even though exact optimization is NP-hard. No approximation statement for
arbitrary two-pool/two-output pooling follows.

**Lemma.** For rational `0<epsilon<1`, at most
`ceil(1/epsilon)+1` LPs produce a feasible point of value at least
`(1-epsilon)OPT`.

**Algorithm.** Put `N=ceil(1/epsilon)`. For each integer `k=0,...,N`, put
`g=k/N` and maximize `b(z)` over `P` with the additional constraint
`a(z)<=1/g` if `g>0`. For `g=0`, use `P` without an additional constraint.
Skip infeasible LPs. Evaluate the true objective at an LP optimizer from
each remaining problem and retain the best. LP solutions may be chosen as
rational vertices of polynomial encoding length.

**Proof.** Let `z*` be an optimum, and put `a*=a(z*)`, `b*=b(z*)`,
`t*=1/a*`. Since `a*>=1`, `t*` is in `(0,1]`. Choose
`g=floor(Nt*)/N`, so `g<=t*` and `t*-g<1/N`. The corresponding LP retains
`z*`, including when `g=0`. Its optimizer `z_g` therefore has
`b(z_g)>=b*` and `1/a(z_g)>=g`. Consequently

```
f(z_g) >= b*(1+g)
       >= b*(1+t*) - b*/N
       >= (1-1/N)OPT
       >= (1-epsilon)OPT.
```

The penultimate inequality uses `OPT=b*(1+t*)>=b*`. This also handles
`OPT=0`. All arithmetic, constraints, and LPs have encoding length
polynomial in the original input and `log N`; there are `N+1` LPs.
The guarantee has no dependence on a ratio between the largest and
smallest quality coefficients. □

Recover the pooling flows from the selected mixture using the exact
reverse construction in the hardness theorem. The resulting solution is
feasible and has precisely the evaluated profit. This scheme assumes the
described subfamily and its polytope/function representation are given;
it does not require or provide recognition of arbitrary equivalent pooling
instances.

An independent reviewer checked the grid selection, zero-grid endpoint,
nonnegative reward requirement, ratio guarantee, rational bit complexity,
and scope restriction. This is an elementary constructive corollary;
literature novelty has not been investigated and is not claimed.
