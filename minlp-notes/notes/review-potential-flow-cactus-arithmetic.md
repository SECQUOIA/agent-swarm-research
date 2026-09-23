# Independent review: exact potential comparison on cactus networks

Date: 2026-09-05. Reviewer: independent `potential_flow_review` agent.

Reviewed draft: [potential-flow-mpd-cactus-investigation.md](potential-flow-mpd-cactus-investigation.md).

**Verdict:** the mathematical lower reduction and matching upper reduction are correct, subject to the minor zero-threshold convention correction below. This audit supports the stated polynomial-time many-one equivalence with the explicitly defined weak-comparison problem `sum sqrt(a_i) <= K`. It does not independently establish novelty, NP-hardness, or approximation hardness.

## Model check

The draft uses a passive connected graph, signed flows, positive rational resistances, quadratic law `pi_u-pi_v = beta_e x_e |x_e|`, and only two nonzero nominations: `b_s=q`, `b_t=-q`, with `0<=q<=1`.

This is precisely the unit-booking, one-entry, one-exit special case of equations (6) of the [2026 potential-flow survey](https://optimization-online.org/wp-content/uploads/2026/01/ch_potential.pdf), printed pages 9–10. Those equations impose flow conservation, potential laws, and booking bounds; they impose no additional arc-capacity or potential bounds. The source and sink can be chosen as the two objective nodes. The survey explicitly identifies nonlinear cactus MPD hardness as open on printed page 10. Its broader question allows multiple entries and exits, so the draft appropriately limits its classification to the single-entry, single-exit subclass.

For the draft's model, existence and uniqueness follow rigorously from minimizing `sum beta_e |x_e|^3/3` over the nonempty conservation affine space. The objective is continuous, coercive, and strictly convex. Optimality on that affine space yields the potential law because the gradient belongs to the row space of the incidence matrix. If `(x,pi)` realizes unit nomination, `(q x,q^2 pi)` realizes nomination `q>=0`. Conversely uniqueness identifies this with the physical flow. At `q=1`, summation by parts gives

```
pi_s-pi_t = sum_e beta_e |x_e|^3 > 0.
```

Thus maximizing over bookings selects `q=1`. No assumption that branch flows are rational is made or needed.

## Lower reduction

For a gadget radicand `a>=2`, let `A=(a-1)^2` and `B=(a-1)^2/a`. Equal drops and branch-flow conservation imply

```
x_A=q/(1+sqrt(a)),
x_B=q sqrt(a)/(1+sqrt(a)),
A x_A^2 = B x_B^2 = q^2(a+1-2sqrt(a)).
```

Both flows are strictly positive for `q>0`; a reversed-flow alternative cannot solve the physical equations. Indeed the common drop determines both branches' flow signs, and their sum is positive. Splitting branch `B` into two equal positive-resistance edges preserves its flow and total drop exactly.

Using disjoint triangles and joining consecutive terminals with bridges gives `3m` vertices and `4m-1` edges. Every cycle is a triangle. Each terminal is incident to two triangle edges and at most one bridge, so maximum degree is three. Bridge conservation forces each triangle's total flow to equal `q`.

The unit drop is `C-2 sum sqrt(a_i)` with `C=sum(a_i+1)+(m-1)`. Therefore the direction is correct:

```
sum sqrt(a_i)<=K  iff  MPD>=C-2K.
```

Equality is preserved. Removing radicands zero or one is valid. If the resulting integer threshold `K` is negative, the formula still works without a special case: the resulting MPD threshold exceeds `C`, whereas the physical drop is below `C`. The all-removed case is directly decidable.

With `L=2 product a_i`, each scaled alternate-path edge has integer resistance `L(a_i-1)^2/(2a_i)`; all other scaled resistances and `L(C-2K)` are integers. Common resistance scaling leaves flows unchanged and scales every potential difference by `L`. If the total input bit length is `S`, `log L=O(S)` and every output integer has `O(S+log m)` bits. The output has `O(m)` such integers. This is polynomial binary output size, even though the integer magnitudes can be exponential. Neither factorization nor radical evaluation is used.

The optional preprocessing of nonpositive MPD thresholds is valid: each gadget has strictly positive drop for `a>=2`, so a nonpositive threshold is automatically satisfied. Fixed yes/no single-edge instances meet all graph restrictions, with the cycle condition holding vacuously.

## Matching upper reduction

In a cactus, the blocks on the unique terminal-to-terminal path in the block-cut tree form a series chain of bridges and two-terminal cycles. Everything attached outside this chain has zero flow. One direct argument is that restricting flow conservation to such an attached subnetwork also gives zero net injection at its sole attachment; replacing all its flows by zero preserves conservation and strictly reduces energy if any removed flow was nonzero. Uniqueness therefore excludes any such flow.

For a chain cycle with branch-resistance sums `A,B>0`, equality of the two branch drops gives

```
R=AB/(sqrt(A)+sqrt(B))^2.
```

The `A=B` case is `R=A/4`. In the other case, rationalization yields

```
R=AB(A+B)/(A-B)^2 - sqrt(4A^3B^3/(A-B)^4).
```

The square-root coefficient has the correct sign and its absorption into the radicand is exact because all quantities are positive. Consequently all irrational summands have the same negative sign. Summing bridges and cycles gives `MPD=Q-sum sqrt(r_j)`, with rational `Q>0,r_j>0`. No difficult mixed-sign radical comparison is hidden in this representation.

For input bit length `S`, summing input resistances gives rational branch sums with polynomial encoding size. Each displayed operation uses only a fixed number of products, differences, and fixed powers of those sums. Summing the resulting rational terms and clearing all denominators also gives polynomial encoding size: denominator products have bit lengths bounded by the sum of their factors' bit lengths. Near equality `A≈B` can make values large, but does not create superpolynomial bit length. The exact equality case `A=B` is checked by integer cross multiplication.

When at least one radical remains, set `T=Q-H`. For `T>0`, write `r_j=u_j/v_j` and `T=p/w` with positive denominators, and set `D=w product v_j`. Then

```
N_j=D^2 u_j/v_j > 0,
K'=DT > 0,
sum sqrt(r_j)<=T  iff  sum sqrt(N_j)<=K'.
```

`N_j,K'` are integers because every denominator divides `D`. Their encodings and their number are polynomial. This proves the reverse many-one reduction.

## Minor correction requested

The reviewed draft initially used `if T<0, return a fixed no instance`. Since it defines SRS with **positive** integer `K`, it should use `T<=0` when at least one radical remains. Otherwise `T=0` produces `K'=0`, outside that convention. The answer is certainly no because every radicand is positive. This is a domain-handling correction, not an algebraic or complexity obstruction. The author was notified.

## Scope of certification

This review independently checked the algebra, zero and equality cases, booking interpretation, graph restrictions, binary encoding bounds, and both reduction directions. It does not rely on floating-point computations. The known parallel formula itself is not a new result. Whether its exact arithmetic classification has appeared before requires the separate literature audit. Polynomial evaluation in a real-arithmetic model, or numerical approximation with a prescribed tolerance, does not contradict the exact bit-model statement.
