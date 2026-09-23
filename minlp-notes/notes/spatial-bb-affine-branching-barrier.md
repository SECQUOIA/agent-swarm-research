# Why the spatial XOR transfer does not extend to affine branching

Date: 2026-09-05. Status: independently verified obstruction to the current
proof method, not an algorithmic upper bound for the constant-gap XOR family.
[Independent audit](review-spatial-bb-affine-branching-barrier.md).

The promoted [monomial-lifting result](../results/spatial-bb-monomial-lift-exponential-lower-bound.md)
allows any number of parity coordinates of bounded degree. Dense affine
auxiliaries behave differently. One balanced affine split can force the
substitution proof to fix linearly many original variables at linear node
order, although the split retains at least half the Boolean witnesses.
The parity-rank counting step therefore has no direct affine analogue.

## A single halfspace defeats preservation of the root moments

Let `E` be actual uniform expectation on `{-1,1}^n`, and let
`S(x)=sum_i x_i`. Its first and second moments are exactly realizable on
the whole cube. They are not realizable on the half-cube

```
H={x in [-1,1]^n:S(x)>=0}.
```

Indeed, those moments give `E[S]=0` and `E[S^2]=n`. Any actual distribution
supported in `H` with mean `S=0` must have `S=0` almost surely, contradicting
its positive second moment. The witness fraction of `H` is at least `1/2`.

Equivalently, introduce the affine coordinate `z=S/n`. On the node
`0<=z<=1`, the quadratic inequality `z^2<=z` is valid. Root moments give
`E[z]=0` and `E[z^2]=1/n`, so even that single quadratic node cut rejects
this preserved moment vector. This does not rule out another node
pseudoexpectation; it identifies the failure of unchanged marginal moments.

## Linear node order can force linear substitution cost

Consider the same uniform expectation, but now fix any coordinate set `C`
to a Boolean witness `w_C`, leaving the other coordinates independently
uniform. Write

```
t=|C|,  a=sum_{i in C} w_i,  s=n-t.
```

Suppose this substituted functional satisfies the order-`r` halfspace
localizers, in particular `L[S p^2]>=0` whenever `1+2deg(p)<=2r`.
Then it is necessary that

```
t >= min(r-1, ceil(n/2)).
```

*Proof.* Suppose instead that `t<r-1` and `t<ceil(n/2)`. Thus
`t<=r-2` and `s>=t+1`. If `a<0`, the localizer for `p=1` already fails.
Otherwise choose `a+1` unrestricted coordinates and let `p` be the product
of their negative-assignment indicators `(1-x_i)/2`. This is possible
because `a+1<=t+1<=s`. Its degree is `a+1<=r-1`, so the localizer has
permitted total degree. Under the substituted uniform distribution, the
selected coordinates sum to `-(a+1)` on the indicator event, while all
other unrestricted coordinates have conditional mean zero. Since `p^2=p`
on Boolean points,

```
L[S p^2]=(a-(a+1)) 2^(-(a+1)) = -2^(-(a+1)) < 0.
```

This contradiction proves the necessary bound. QED.

For `r` proportional to `n`, a single halfspace consequently requires
linearly many substitutions in this construction. But its Boolean witness
mass is at least one half. The old implication from many affected original
variables to exponentially small witness mass cannot hold for arbitrary
affine inequalities. This is a barrier to that implication, not a proof
that the XOR objective itself admits short affine-branch certificates.
The example uses a genuine uniform distribution, so the obstruction is
geometric and does not depend on an incorrect pseudoexpectation.

## What the proof-complexity literature says

[Beame et al., Stabbing Planes](https://arxiv.org/abs/1710.03219)
introduce branching on integer linear inequalities and their integer
negations; their system has short refutations for Tseitin parity formulas.
The abstract was inspected. Integer branching may discard an empty integer
slab, so this system is not identical to continuous halfspace subdivision.

[Fleming et al., On the Power and Limitations of Branch and Cut](https://arxiv.org/abs/2102.05019)
extend short Cutting Planes refutations to arbitrary inconsistent finite-field
linear systems and establish lower bounds for a coefficient-restricted
Stabbing Planes subsystem. The abstract and primary author-PDF introduction
were inspected. These are relevant warnings against transferring an SOS
parity obstruction directly to unrestricted affine branching.

The promoted family minimizes a **constant fraction** of violated parity
constraints. A short refutation of perfect satisfiability only proves that
at least one clause must fail; after normalization this is a bound of
`1/m`, which does not certify the target `1/16`. Thus those upper bounds do
not themselves refute the promoted fixed-gap lower bound under a stronger
affine-branch model. Establishing such an upper bound, or a lower bound for
that stronger model, remains open in this investigation.
