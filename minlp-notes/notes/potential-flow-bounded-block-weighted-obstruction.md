# Why the weighted bounded-block extension needs a new summation argument

Date: 2026-09-05. Status: historical unproved route; the cactus target was resolved in the 2026-09-06 continuation. General bounded-rank blocks remain open.

Update, 2026-09-06: the exact-radical-sum route below remains unnecessary and unproved. The cactus optimization target is now resolved by [uniform polynomial approximation in fixed parameter dimension](potential-flow-reopened-weighted-investigation.md), the [weighted nomination-face reduction](potential-flow-reopened-weighted-face-reduction.md), and [local resistance elimination](../results/potential-flow-joint-weighted-cactus-accuracy-bits.md). The resulting joint theorem permits independent continuous resistance intervals and full balanced nomination boxes at fixed objective support. General noncactus bounded-rank blocks remain outside that algorithm. The original investigation is retained to explain why exact zero-count arguments were insufficient.

The [fixed-global-rank weighted theorem](../results/potential-flow-fixed-support-global-rank.md) places every cycle circulation in a fixed-dimensional core. The earlier pairwise-pressure theorem permits arbitrarily many blocks at fixed rank per block because a nomination optimum can be selected with only one active block; all other block contributions are then constants.

For a weighted objective with several active nomination blocks, this separation fails. Transfers of total nomination between active blocks change the through-load of inactive blocks between them. Those blocks contribute algebraic functions of a shared core, rather than fixed algebraic constants. A polynomial-time value oracle for each local block does not by itself give a polynomial-time global optimizer. A Lipschitz grid takes a power of `1/epsilon`, which is insufficient for the desired dependence on accuracy bits.

## A possible univariate cactus route

Suppose an inactive cycle has fixed internal nominations, fixed asymmetric-quadratic laws, and one varying terminal through-load `t`. On a cell in the two variables `(t,q)`, every edge flow is `q+a_e t+d_e`, with rational `a_e,d_e` and `a_e` equal to zero or one after choosing the cycle orientation and source-to-sink path. Cycle conservation of potential is

```
A q^2+B(t)q+C(t)=0,
```

where `A` is constant, `B` is affine and `C` is quadratic. If `A!=0`, a branch of the circulation is rational affine in `t` plus a constant multiple of the square root of a rational quadratic polynomial. Substitution into a quadratic path-drop expression yields a rational polynomial of degree at most two plus a rational affine factor times that square root. If `A=0`, the circulation and drop are rational functions of bounded degree. The sign cells form a planar hyperplane arrangement, so there are polynomially many local formulas. A joint interval-resistance cycle can first use its correct two-terminal envelope, if that envelope reduction has independently been established for the chosen orientation and objective.

This suggests studying additive optimization of sums of such one-variable algebraic functions. Away from their zeros and singularities, each nonzero term `f_i(t)=P_i(t)sqrt(Q_i(t))`, or a rational-function term, has a rational logarithmic derivative `f_i'/f_i`. Derivatives of each order can be represented as that same term times a rational function. Hence a Wronskian factors as

```
W(f_1,...,f_k)=(product_i f_i) det(R_ij(t)),
```

with rational `R_ij`. The numerator degree of the determinant appears polynomial in the number of terms and derivative orders for bounded-degree starting terms. A suitable nonvanishing-Wronskian partition could therefore support a Chebyshev-system or repeated-Rolle bound on the number of real zeros of a derivative sum.

This is only a route. The following gaps remain:

- Functional linear dependencies can make Wronskians identically zero. Removing them without constructing a large algebraic coefficient field needs care.
- A polynomial zero-count bound is not yet a polynomial-bit root-isolation or additive-optimization algorithm. Near cancellations, near multiple roots, exact equality, and robust approximate signs must all be controlled without an unproved square-root-sum separation bound.
- Switching between local cycle sign formulas must preserve certified errors near their algebraic boundaries.
- Several active blocks usually create more than one shared variable. The one-variable Wronskian argument does not address that coupling.
- General fixed-rank blocks have more complicated algebraic local functions than a single quadratic circulation root.

No exact or additive bounded-block weighted theorem is claimed from this observation. The local quadratic formula derivation is useful, but the global summation and optimization step remains open in this investigation.
