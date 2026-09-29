# Independent review of the succinct root-penalty theorem

Date: 2026-09-27. Scope: [the proposed theorem](succinct-root-penalties.md)
and [its prior-art audit](holder-penalty-prior.md). This review was performed
independently of their derivation.

**Assessment:** the theorem is correct under its intended convention that
all additional inequalities are weak. The coefficient-sensitive elimination
step is explicitly supported by the inspected primary source. I found no
counterexample to the stated quadratic, explicitly bounded input model.
This is a useful encoding consequence of established effective
semialgebraic inequalities, with no demonstrated solver improvement and no
established priority claim. The additional inequalities should explicitly
be called weak, and the source audit should say that both `X` and `S` are
compact in the quoted compact-domain penalty result.

## Primary-source check

I inspected the open publisher full text of Basu and Mohammad-Nezhad,
[*Improved effective Łojasiewicz inequality and applications*](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/improved-effective-lojasiewicz-inequality-and-applications/022BF859F5714FDA8050F6DC1992E48B),
especially Theorems 2.2 and 4.1 and the coefficient argument in the proof of
Theorem 2.2.

Theorem 4.1 explicitly states that integer input coefficients of bit size
`tau` yield integer output coefficients of bit size

\[
 \tau d^{O(k_\omega)\cdots O(k_1)O(\ell)},
\]

where the quantified block sizes are `k_i` and there are `ell` free
variables. It also gives output degree
`d^{O(k_omega)...O(k_1)}`. Thus the coefficient claim is part of the
displayed elimination theorem, not merely inferred from a later proof.
Theorem 2.2 supplies its integer-coefficient bound with the fixed integer
exponent `q=(8d)^{2(n+7)}`. The weaker of its two coefficient bounds,
`log_2 C <= tau d^{O(n^2)}`, suffices here. These are exactly the quantitative
dependencies the proposed proof needs.

I also inspected Jiao, Pham, and Tuyen,
[*Exact penalty functions in optimization with unbounded constraint sets*](https://arxiv.org/html/2507.03424v2),
Theorem 5.2 and Remark 5.3(ii). The remark assumes compactness of the native
domain `X` as well as the nonempty subset `S`, and gives both value and
minimizer-set exactness. It attributes the subanalytic compact-domain
result to Warga and Dedieu. I did not inspect the older originals, so this
review does not upgrade that attribution to an independent audit of them.

## Independent encoding calculation

Write `N` for the original ordinary binary input length. There are at most
polynomially many variables and monomials. Every rational coefficient and
bound has polynomial bit length, and a quadratic monomial evaluated on the
input box has absolute value at most `2^{poly(N)}`. Summing the termwise
bounds and rounding up gives positive integers `B,H` with polynomial bit
length. This does not require optimizing either the objective or residual.

For an integer coordinate, use
`k=ceil(log_2(u-ell+1))` bits after rounding its rational bounds to integral
bounds. The case `u=ell` has `k=0`. Keeping the affine relation between the
coordinate and its bits, together with the original upper bound, gives
exactly the intended integer interval. It neither enumerates its values
nor permits the surplus binary codes above `u`. The coefficients `2^j`
have `j+1` bits. The total number of bits, constraints, and coefficient
digits is polynomial in `N`. The quadratic equations `b(1-b)=0` are exact
over the reals. The lifted domain is closed and bounded.

Clear each rational row using a positive common denominator. A product of
the row denominators is sufficient; its bit length is their summed bit
length. This operation preserves every sign comparison. All input
polynomials for elimination then have degree at most two and coefficient
bit size `tau_0=poly(N)` in `K=poly(N)` variables.

The set

\[
 I=[-B,B]\cap\{t:\neg\exists y\,[y\in S'\ \wedge\ f(y)<t]\}
\]

uses a single quantified block of size `K`, one free variable, and only
rational data. The already imposed binary equations are part of `S'`;
there are no remaining discrete quantifiers. Applying the verified
elimination statement with `d=2` yields

\[
 d_I\le 2^{\operatorname{poly}(N)},\qquad
 \tau_I\le 2^{\operatorname{poly}(N)}.
\]

The elimination formula can be long; it is used in the existence proof
and is not part of the final polynomial-size quadratic lift.

The function `h=R` has a direct quantifier-free graph: list the finitely
many residual polynomials, including zero and both signs of each equality
residual; require `Hs` to dominate them all and equal at least one. The
graph of `g=max(0,t-f(w))` similarly has two branches. Restriction to
`A=X' times I` uses the same rational description. Their graph degrees
and coefficient bits are therefore bounded by
`d,tau <= 2^{poly(N)}`, while the ambient dimension remains polynomial.
Consequently

\[
 \log_2 q=O(n\log d)=\operatorname{poly}(N),\qquad
 \log_2\log_2\max\{2,C\}
 \le O(1)+\log_2\max\{1,\tau\}+O(n^2\log d)
 =\operatorname{poly}(N).
\]

This proves the asserted common bound `q, log_2 max(1,C) <= 2^{a(N)}`.
Choosing an integer-valued polynomial `p` large enough is legitimate. Its
existence is uniform over all inputs of size `N`. The source bounds are
effective, but the note does not evaluate their universal constants and
therefore does not supply a numerically specified recipe for `p`.

## Exactness and the auxiliary formulation

Because the additional constraints are closed and `S` is nonempty, the
optimum `v` is attained and `I=[-B,v]`, even when `v=-B`. On `A`, `h=0`
means that `w` is feasible, and hence `t<=v<=f(w)`. This proves the needed
zero-set inclusion. Infeasible integer fibers are retained in `X'`; they
cause no omission or invalid application of a fiberwise estimate.

Let `M=2B>=1`, take `C>=1`, and choose
`alpha=2^{-p(N)}` with `alpha q<=1` and `alpha log_2 C<=1`. For `h>0`,
put `theta=alpha q`. Direct interpolation gives

\[
 g\le\min\{M,C^{1/q}h^{1/q}\}
 \le M^{1-\theta}C^\alpha h^\alpha
 \le2M h^\alpha.
\]

For `h=0`, the zero-set inclusion gives the same result. Restricting to
`t=v` yields `f+(2M+1)h^alpha >= v+h^alpha`. This strict positive slack
at every infeasible point proves equality of the full minimizer sets,
not just equality of infima. Continuity and compactness also ensure that
the augmented minimum is attained.

For the lift, nonnegative variables and the equations
`t_{j+1}=t_j^2` imply `t_p=t_0^{2^p}`. Therefore `Ht_p>=V` is equivalent
to `t_0>=R^{1/2^p}` within the specified bounds. Every original point has
such a lift, and the positive coefficient in the objective selects its
smallest possible `t_0`. The polynomial count, coefficient bits, and
variable count remain polynomial. At a global minimizer the original
point is feasible and all auxiliary `t_j` are zero.

The proposed warning about reversing the inequalities is correct: with
`t_{j+1}>=t_j^2`, one could set `t_0=...=t_{p-1}=0` and `t_p=R`, paying
no penalty. This is not a convex representation of the desired root.

## Adversarial examples and limits

These elementary examples use familiar squaring-chain mechanisms. They
are verification examples, not new priority claims.

**Exponent size can be necessary.** Take the native compact quadratic
curve

\[
 0\le x_i\le1,\qquad x_{i+1}=x_i^2\quad(0\le i<k),
\]

with objective `-x_0` and additional constraint `x_k=0`. The feasible
optimum is zero and the residual is `x_0^{2^k}`. A penalty with finite
coefficient `rho` has augmented objective
`-s+rho s^{alpha 2^k}`. If `alpha 2^k>1`, this is negative for all
sufficiently small positive `s`, whatever finite `rho` is. Thus exactness
requires `alpha<=2^{-k}`. At equality, minimizer-set exactness requires
`rho>1`; with `rho=1`, every native point ties. For `alpha<=2^{-k}` and
`rho>1`, exactness holds because `s^{alpha 2^k}>=s` on `[0,1]`.

**Infeasible integer fibers exhibit the coefficient tradeoff.** Take
`z in {0,1}`, `y_0=1/2`, `y_{i+1}=y_i^2`, and all variables in `[0,1]`.
Minimize `-z` and penalize the additional quadratic equation `z y_k=0`.
There are just two native points, with feasible optimum at `z=0`. The
other point has residual `2^{-2^k}`. Strict minimizer-set exactness is
equivalent to

\[
 \rho>2^{\alpha 2^k}.
\]

For a fixed exponent this requires exponentially many coefficient bits
in chain length; a dyadic exponent of order `2^{-k}` reduces the required
coefficient to a constant. The input has `O(k log k)` bits under ordinary
indexed sparse encoding. Exponential claims here concern chain length,
not the full binary input length.

**Small equation errors can defeat the lift.** In the first example, the
native point `x_0=1/2` has residual `r=2^{-2^k}`. In a root lift with
`p>=k`, set all auxiliaries except the last to zero and set `t_p=r`.
Every lift equality except the last holds exactly; the last has absolute
error `r`. An absolute feasibility tolerance at least `r` accepts zero
penalty and objective `-1/2`, despite the true exact augmented minimum
being zero. This verifies the stated numerical limitation quantitatively.

The sparse high-degree objective counterexample in the source audit is
also correct: at `x=1`, the residual equals one for every exponent and
the objective deficit is `2^{2^k}-1`. No exponent choice reduces the
coefficient required at that point. Explicit bounded-degree data or an
appropriate objective-range bound is therefore material.

## Significance and verification record

The result provides a precise way to trade large penalty coefficients
for small rational exponents while retaining a polynomial description.
It addresses a representation question excluded by the earlier norm-penalty
lower bound. The new lift still imposes residual inequalities and adds
nonconvex equations; it need not reduce problem size, improve relaxations,
preserve useful local minima, or improve conditioning. Its currently
established role is a supporting representation theorem.

The prior-art audit appropriately treats qualitative fractional exactness,
effective inequalities, and repeated squaring as established tools. My
additional searches for fractional exact penalties, coefficient/exponent
encoding, and bit complexity did not identify an equivalent explicit
encoding theorem. Those unsuccessful searches do not establish novelty.
Older compact-domain originals and further citation searches remain needed
for any stronger priority claim.

Targeted checks consisted of reading the two reviewed notes, the earlier
local publication priority audit, and the identified primary full texts;
checking every displayed transformation symbolically; and deriving the
counterexamples above. The local extracted Basu--Pollack--Roy book text was
unreadable, so it was not used as evidence. No numerical test, Lean proof,
project-wide verification, or CI inspection was performed. This review
checks the application of the cited source theorems, not a formal proof of
those source theorems themselves.
