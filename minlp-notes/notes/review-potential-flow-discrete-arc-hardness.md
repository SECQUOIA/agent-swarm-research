# Independent audit of discrete-resistance arc-capacity hardness

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`.

Reviewed: [the discrete arc-hardness investigation](potential-flow-discrete-arc-hardness.md),
including its final monotonicity proof with `D=ceil(10000/Delta)` and its
NP/coNP membership section. The audit also uses the
[reviewed pressure reduction](review-potential-flow-discrete-resistance-hardness.md)
and the [exact arc-flow theorem](../results/potential-flow-exact-arc-capacity.md).

**Verdict: PASS.** The final construction proves NP-completeness of the
existence of a signed arc-capacity violation and coNP-completeness of robust
arc-capacity validation on the stated class. Its additive flow gap also
excludes polynomial dependence on input length and precision bits unless
`P=NP`. The new edge requires a perturbation proof; pressure hardness alone
would not imply these flow claims.

## Construction and graph restrictions

Start with the theta pressure gadget and its resistance-3 leaf at vertex
`4`, with distinguished nominations `(4,-5,3,-3,1)`. The common law is
`phi(x)=x|x|`. For the prescribed old objective `F_0=pi_4-pi_0`, every
resistance selection satisfies `5/6<F_0<=1`. A target subset attains one,
whereas every non-target selection satisfies `F_0<=1-Delta`, where

```
Delta=6/(31K+18S)^2.
```

Set `D=ceil(10000/Delta)`, `H=1-Delta/2`, `M=H*D^2`, and `c=1/D`.
The original nontrivial Subset-Sum instances give `0<Delta<1`, hence
`1/2<H<1`. Add a fixed-resistance edge oriented `4->0`, with resistance
`M`, leaving every nomination unchanged.

The new path `0-4-1`, together with the original theta, forms a subdivision
of `K4`: suppress vertex `4` and all internal cross-path vertices to see
this directly. Thus the whole graph is simple and biconnected, has both
block and global cycle rank three, and has maximum degree three. Original
vertices `0,1,2,3` have degree three; all remaining vertices have degree two.
There is no uncounted bridge in this final graph.

## Restriction and strict monotonicity

Let `t` denote the signed physical flow on the new edge. Restricting the
new physical state to the old graph changes its induced nominations to

```
b(t)=b+t*e_0-t*e_4.
```

In particular, the old net outgoing flow at vertex `0` becomes `4+t`,
while that at vertex `4` becomes `1-t`. These signs follow from the edge
orientation `4->0`. The restricted state satisfies the old laws, so by
physical uniqueness it is precisely the old graph's state for `b(t)` and
the chosen resistance vector. Its terminal drop is therefore `F(t)`, and
its new edge law is exactly

```
F(t)=M*t*|t|.
```

The old network has a unique physical state for every real `t`, because
`b(t)` stays balanced and the passive energy is coercive on conservation
spaces. For any two parameters `s!=t`, conservation and the potential
laws imply

```
(b(t)-b(s)) dot (pi(t)-pi(s))
 = sum_e beta_e*(phi(x_e(t))-phi(x_e(s)))*(x_e(t)-x_e(s)) > 0.
```

Every term is nonnegative by strict increase. At least one is positive
because distinct nominations force distinct flow vectors. The left side
is `-(t-s)*(F(t)-F(s))`. Hence `F` is strictly decreasing. This proof needs
neither differentiability of the physical solution map nor a positive
lower bound on the constitutive derivative.

Since `F(0)=F_0>0`, a physical solution cannot have `t<=0`: its left side
would be positive and its right side nonpositive. Thus `t>0`, and

```
0<M*t^2=F(t)<=F_0<=1,
t<=1/sqrt(M)<=2/D<1.
```

This also proves that signed and absolute capacity tests agree on the
new edge for every resistance selection.

## Uniform pressure perturbation

Both the original and induced nominations lie in the box with
`b_0 in[4,5]`, `b_4 in[0,1]`, all other distinguished nominations fixed,
and subdivision nominations zero. Its total absolute nomination bound is
at most `18` (in fact `17` suffices). The fixed old path `4-1-2-0` has
resistance sum `3+1/6+1/2=11/3`. The reviewed signed-quadratic nomination
Lipschitz bound thus gives the valid coefficient

```
C_b=2*18*(11/3)=132.
```

Because `||b(t)-b||_1=2t`, strict decrease and Lipschitz continuity give

```
0<=F_0-F(t)<=264*t<=528/D<=0.0528*Delta<Delta/8.
```

The uncertain cross path does not occur in the chosen comparison path,
so the estimate is uniform even if its total resistance is very large.
The underlying Lipschitz theorem remains valid at zero flows by its
reviewed positive-linear-smoothing argument. The numerical comparison in
this display is an exact rational inequality, not a numerical estimate.

## Rational flow threshold and gap

By construction, `M*c^2=H`. A target subset has
`F(t)>1-Delta/8=H+3Delta/8`. Every non-target selection has
`F(t)<=F_0<=1-Delta=H-Delta/2`. Thus a target subset produces `t>c`,
while all non-target selections produce `t<c`.

The quantitative conversion uses the exact factorization

```
|t-c|=|F(t)-H|/[M*(t+c)].
```

Both flows in the denominator are positive. Since `t<=2/D`, `c=1/D`,
and `M<=D^2`, the denominator is at most `3D`. This even gives the
stronger gap `Delta/(8D)` in the weaker of the two cases. In particular,
the proposed value

```
g=3Delta/(32D)
```

is valid: some target selection has `t>=c+g` in a yes instance, and
all selections have `t<=c-g` in a no instance. Strict versus non-strict
capacity conventions do not affect the reduction.

The displayed requested approximation error `Delta/(64D)` is below `g/3`,
so comparing an approximate maximum flow with `c` separates the cases.
A certified near-optimal resistance selection with error smaller than `g`
must choose a target subset on a yes instance. Indeed, every non-target
selection lies below `c-g`, while the optimum lies above `c+g`. The
selected item sum can be checked using integer arithmetic, without
computing its exact physical flow.

## Encoding and capacity conventions

The graph has linear size in the number of items. The existing two-point
options have polynomial rational encoding length. Computing `Delta`,
the integer ceiling `D`, and the rational `H,M,c` takes polynomial bit
time, and all their binary lengths are `O(log(K+S))`. The flow gap has
polynomial encoding length as well. Thus the requested number of additive
precision bits is polynomial in the Subset-Sum input size.

A common multiple of the original resistance denominators and the
rational denominator of `M` has polynomial bit length, even if constructed
by a product. Scaling every resistance by it makes every resistance a
positive integer. This multiplies all energies and potentials by one
common factor, so the unique physical flow and the capacity `c` remain
unchanged. This scaling gives no bound on the numerical magnitudes that
would establish strong hardness.

If a validator requires capacities on every edge, assign `[-16,16]` to
all other edges. The fixed nominations have total absolute magnitude
`16`, so the acyclic passive-flow bound guarantees these capacities for
every resistance choice. The new edge can have lower capacity `-16` and
upper capacity `c`; positivity also permits the equivalent absolute
capacity formulation. Capacity restrictions are checked after evaluating
all unrestricted passive scenarios and do not alter the state space used
in the reduction.

## Membership and complete classifications

For any fixed maximum block cycle rank, a certificate selects one entry
from each explicitly listed finite positive rational resistance set. Its
length is polynomial in the input length. Holding that vector fixed
reduces the remaining question to exact edge-flow optimization over the
finite rational nomination box intersected with balance.

The already-reviewed exact arc-flow theorem solves that fixed-resistance
problem in polynomial bit time, including comparisons of its algebraic
maximum and minimum with rational capacities. Hence a deterministic
verifier can test whether a violating nomination exists for the selected
resistances. It can either examine all arcs in polynomial time or use an
additional selected arc index. No physical-state certificate or rational
nomination witness is required.

Thus existence of a violating scenario belongs to NP, and robust
satisfaction of all arc capacities belongs to coNP. The reduction proves
NP-hardness of the first problem and coNP-hardness of the second: robust
satisfaction holds precisely on no Subset-Sum instances. Together these
give NP-completeness and coNP-completeness already on the stated rank-three
subdivision class with fixed nominations. The membership argument also
covers the larger explicitly finite resistance-choice model with
continuous nomination boxes at fixed maximum block rank.

The verifier's polynomial bound depends on fixing the structural rank.
It must not be cited as NP membership for arbitrary-rank networks, or for
pressure-threshold problems that add algebraic values across many blocks.

## Supplementary energy bound and scope

The initial, larger-resistance proof route is also valid but unnecessary
for the final monotonic construction. In the old gadget, eliminating
`tau*q^2` from its exact energy gives

```
E_old=(5q^2-46q+209)/36<209/36<7,  0<q<2.
```

Extending that state by zero on the new edge proves
`|t|<(21/M)^(1/3)`. With the earlier alternative choice
`D=ceil(10^6/Delta^2)`, this implies pressure error below `Delta/8` via
`264|t|`. It does not supply that precision with the final smaller `D`;
the strict monotonicity argument above is the reason the smaller choice
works. The exact energy identity was independently verified symbolically.

The final proof therefore establishes the stated complexity classification
and high-precision additive obstruction. It does not prove strong
NP-hardness, rule out an FPTAS, or establish arc-flow hardness at rank two.
The continuous interval-resistance algorithm remains consistent with this
finite-choice hardness. Literature novelty requires a separate review.
