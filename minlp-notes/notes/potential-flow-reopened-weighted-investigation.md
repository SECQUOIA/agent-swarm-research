# Reopening weighted cactus optimization through polynomial approximation

Date: 2026-09-06. Status: passed [independent full mathematical review](review-potential-flow-reopened-weighted.md), including exact capacities and slack recovery. Literature priority remains provisional. This note resolves the local-function summation obstacle for fixed-dimensional affine nomination families on cacti. The separate [reviewed nomination-face composition](../results/potential-flow-weighted-cactus-accuracy-bits.md) now supplies the unrestricted nomination-box, fixed-objective-support theorem for fixed laws.

## Proposed theorem

Fix `d`. Let a connected cactus have fixed positive rational asymmetric quadratic laws

```
g_e(x)=beta_e^+ x^2 if x>=0, and -beta_e^- x^2 if x<=0.
```

Let nominations be `b(z)=b0+Hz`, with rational data, for `z` in a nonempty compact rational polytope `P` in `R^d`. Assume `sum b(z)=0` on `P`. Let `c` be any rational potential-objective vector with `sum c=0`; its support need not be bounded. Then the maximum and minimum of `c^T pi(b(z))` admit certified rational additive value intervals and rational epsilon-optimal parameters in time polynomial in the input bit length and requested accuracy bits, for fixed `d`.

Take `0<epsilon<=1`; for a larger tolerance use `min(epsilon,1)`. The number of cycles, their lengths, the rank of the whole network, and the objective support are unbounded. The polynomial exponent may depend on `d`. There are no scenario-filtering operating constraints, variable resistances, or integer parameters in this theorem. This is a bit-complexity result; a practical implementation of the entire exact optimizer is not claimed.

The practical model is a fixed number of market, weather, production, or transfer factors affecting arbitrarily many loads, with an arbitrary weighted pressure objective. In particular, it covers one shared transfer through arbitrarily many cycles, the unresolved special case in [the prior obstruction note](potential-flow-bounded-block-weighted-obstruction.md).

## 1. Local cycle representation in a fixed-dimensional core

Choose a spanning tree and a fundamental-cycle orientation. On a cactus the cycles are edge-disjoint. Thus every bridge flow is affine in `z`, and on each cycle every oriented edge flow is

```
x_e=q+ell_e(z),
```

where `q` is that cycle's sole circulation and every `ell_e` is rational affine. Resistances are swapped between their positive and negative branches if the chosen cycle orientation reverses the original orientation. Cycle conservation is

```
F(z,q)=sum_e g_e(q+ell_e(z))=0.
```

The function `F(z,.)` is continuous and strictly increasing, with limits of opposite sign at infinity; consequently its real root is unique for every `z`.

The affine hyperplanes `q+ell_e(z)=0` have a polynomial number of cells in fixed dimension `d+1`. On the closure of each feasible cell the equation becomes

```
A q^2+B(z)q+C(z)=0,                                  (1)
```

where `A` is rational constant, `B` is affine, and `C` is quadratic. Edge zeroes cause no ambiguity because both laws agree there. A cycle path drop is also quadratic in `(z,q)`. A spanning-tree representation expresses the full objective as a rational weighted sum of such path drops and bridge drops, regardless of the support of `c`.

If `A!=0`, the physical root necessarily is

```
q=(-B(z)+sqrt(Delta(z)))/(2A),  Delta=B^2-4AC.          (2)
```

Indeed, at the physical point, `2Aq+B=sum_e 2 beta_e^{sign}|x_e|>=0`; this selects the plus sign in (2), even when `A<0`. Substituting (2) in a quadratic path drop gives

```
P(z)+L(z)sqrt(Delta(z)),                              (3)
```

with `P` quadratic and `L` affine, both rational. Nonnegativity of `Delta` is imposed on the exact branch domain.

If `A=0`, then at physical points with `B(z)>0`,

```
q=-C(z)/B(z),                                        (4)
```

and path drops are rational functions of bounded degree with denominator `B(z)^2`. No lower bound on `B` is assumed. The exceptional physical locus `A=B=0` has `x_e=0` for every cycle edge, since the nonnegative derivative sum vanishes only there. It is represented explicitly by `q=-ell_1(z)` and the rational affine equalities `ell_e(z)=ell_1(z)`; its drop is zero. This prevents any division by zero or unsupported cancellation assumption.

Construct the exact domain of each local formula by eliminating its one circulation `q` from (1), the cell's affine sign constraints, the applicable conditions `A!=0`, `B>0`, or the all-zero case, and the rational bounding box for `z`. Elimination has fixed dimension and bounded initial degree, hence produces polynomially many rational polynomials of bounded degree (depending on `d`) and polynomial coefficient encoding. Formula (2) can be selected by adding `2Aq+B>=0`. Their projections can be disconnected; connectedness is not assumed.

Collect all resulting domain-boundary polynomials over all cycles, the bridge zero-flow hyperplanes `ell_e(z)=0`, and the defining polynomials of `P`, and decompose `P` into sign-invariant semialgebraic cells. The bridge hyperplanes select the correct asymmetric quadratic branch even when the network is a tree. In fixed `d`, their number and encoding are polynomial. On each cell select one valid formula for every cycle; overlaps are harmless since all valid exact formulas describe the unique physical flow. These domain polynomials also preserve the signs of every nonzero rational denominator. This common decomposition has polynomial size; enumerating all combinations of local branches would be an unnecessary exponential method.

## 2. An elementary rational piecewise-polynomial square-root approximation

This approximation ingredient is classical in principle. The following explicit construction removes any dependency on exact comparison of sums of radicals and keeps coefficient arithmetic rational.

For `0<eta<=1`, choose `J` with `2^-J<=eta`. On `[0,4^-J]` approximate `sqrt(x)` by zero. For `j=0,...,J-1`, use the interval `[4^(-j-1),4^-j]`, center

```
a_j=(9/16)4^-j,   sqrt(a_j)=(3/4)2^-j,
```

and Taylor polynomial

```
T_j(x)=sqrt(a_j) sum_(k=0)^K binom(1/2,k) (x/a_j-1)^k.
```

Every coefficient and breakpoint is rational. Throughout that panel `|x/a_j-1|<=7/9`, and `|binom(1/2,k)|<=1`. Therefore

```
|T_j(x)-sqrt(x)| <= (9/2)(7/9)^(K+1).
```

Choose `K` to make this at most `eta`. Thus there are `O(log(1/eta))` panels of degree `O(log(1/eta))`, with polynomial coefficient encoding and construction time. The branches need not agree at a shared endpoint; either branch has the stated error there. Their closed domains cover `[0,1]`.

For `sqrt(Delta(z))`, obtain a rational power of two `S>=1` with `Delta(z)<=S^2` throughout `P` whenever that radical branch applies. A rational bounding box for the compact input polytope and absolute coefficient sums supply such an `S` of polynomial bit length. Use `S*T_j(Delta/S^2)` with tolerance `eta/S` in the normalized construction. Its uniform absolute error is at most `eta`. The degree and encoding remain polynomial in the input and `log(1/eta)`.

## 3. Compile and optimize the sum

On a fixed exact-domain cell the objective is a sum of polynomial terms, rational terms of bounded degree with nonzero denominator, and terms of form (3). Rational coefficient sums on the bounding box yield bounds `M_i>=|L_i(z)|`. Choose the radical error tolerance

```
eta = epsilon/[16(1+sum_i M_i)],
```

using a sum over every possible local branch if more convenient; its number is polynomial. Each resulting objective surrogate differs from the physical objective by at most `epsilon/16` wherever its selected branches apply.

For every radical formula and every square-root panel boundary, add the polynomial `Delta(z)-S^2 a` to the common decomposition, where `a` is the relevant rational breakpoint. In fixed dimension this refinement still has polynomially many cells. On each refined cell choose one eligible polynomial square-root branch for every selected radical. The entire surrogate objective is now a rational function in `z` with rational coefficients, polynomial degree and polynomial coefficient bit length. Adding polynomially many rational terms only adds denominator degrees; it does not require a common algebraic coefficient field.

Clear denominators using their known nonzero signs, or multiply by their squares and keep the explicit nonzero constraints. Fixed-dimensional real quantifier elimination decides whether a surrogate value above a rational threshold is attained in that cell. Open cells and denominators approaching zero are allowed: optimize the supremum, and recover a point within the requested additive tolerance whenever the cell is nonempty. The physical objective is uniformly bounded on `P`, and the surrogate differs uniformly from it, so every such supremum is finite. Compactness of each individual cell is not required. Original branch boundaries, including the all-zero singular locus, are included as separate cells in the global decomposition.

Rational bisection on a polynomial-bit objective bound computes the global surrogate supremum to `epsilon/8`; an existential sample with value within `epsilon/8` of that supremum can be returned in fixed-dimensional real-algebraic representation. All iterations and sample encodings have polynomial complexity. The two uniform approximation errors and this optimization tolerance give a physical objective loss below `epsilon/4` at the resulting algebraic parameter. The same comparison gives a certified rational interval for the true optimum, with constants tightened if a prescribed total interval width is required.

This step does not compare the exact sum of independent square roots. It optimizes a rational surrogate with a proved uniform error, so near cancellation, multiple stationary points, and exact equality of original objective values do not create a square-root-sum separation requirement.

## 4. Rational feasible recovery

One may reuse the graph-independent nomination Lipschitz argument from [the reviewed cactus theorem](../results/potential-flow-cactus-additive-optimization.md). Here is a direct version valid also for the fixed asymmetric laws.

Let two physical states have balanced nominations `b,b'` and edge flows bounded by `B`. Write `dx=x-x'`, `d pi=pi-pi'`. Strict monotonicity gives `sign(dx_e)=sign((A^T d pi)_e)` whenever `dx_e!=0`. Orient every nonzero difference flow in its positive direction. The potential difference strictly decreases on each such arc, so the oriented support is acyclic. Its flow decomposes into paths from positive to negative components of `b-b'`; hence

```
|dx_e| <= ||b-b'||_1/2.
```

Since the edge laws on `[-B,B]` are Lipschitz with constant `2 beta_max B`, every edge potential-drop change is at most `beta_max B ||b-b'||_1`. After normalizing one reference potential, a simple path has at most `n-1` edges, giving

```
|c^T pi(b)-c^T pi(b')|
 <= ||c||_1 (n-1) beta_max B ||b-b'||_1.              (5)
```

A rational bound on all nominations gives a rational polynomial-bit `B`; for example bound every physical edge flow by the total possible positive nomination. Also `||H(z-z')||_1 <= (sum_ij |H_ij|)||z-z'||_infinity`. Thus (5) gives an explicit rational Lipschitz constant in parameter space.

Isolate the algebraic sample parameter coordinates in rational intervals of width `delta`, chosen so the Lipschitz loss is below `epsilon/4`. Intersect this box with the original rational polytope `P`. It contains the sample, so rational linear programming returns a rational feasible point of polynomial encoding length, including when `P` has lower dimension. The rounded point need not remain in the original semialgebraic branch cell: (5) compares actual physical objectives globally. This is why no lower bound on distance to a branch boundary or a rational-function denominator is needed. If the Lipschitz constant vanishes, any rational point in `P` suffices.

At the returned rational parameter, local cycle roots can be enclosed separately by rational bisection, and potential-objective sums can be evaluated with certified additive error. A common algebraic field is again unnecessary. Minimum optimization follows by replacing `c` by `-c`.

## What this does and does not resolve

The prior Wronskian route tried to bound the roots of exact radical sums. Uniform polynomial approximation plus a fixed-dimensional partition bypasses that issue altogether. It also handles several shared factors, rather than just one.

The separate [weighted nomination-face reduction](potential-flow-reopened-weighted-face-reduction.md), now independently reviewed, proves that an optimum lies on a polynomial family of faces with only a bounded number of varying nominations despite arbitrarily many blocks. Composing it with this note yields the unrestricted-box fixed-support cactus theorem; the existing global-rank theorem alone did not supply that reduction. Fixed-rank-per-block graphs beyond cacti have local algebraic functions of higher degree and would require a more general certified parameter-dependent approximation theorem; the one-variable monotone-polynomial-inverse lemma is not automatically that theorem. Joint resistance uncertainty is excluded from this fixed-law proof because its quadratic-root denominators can vary and become small. The separate [joint weighted cactus theorem](../results/potential-flow-joint-weighted-cactus-accuracy-bits.md) resolves independent interval uncertainty for symmetric quadratic laws by first eliminating the resistance variables with one-row LP duality; it does not extend the present asymmetric-law statement automatically.

## Literature positioning

Gotzes, Heitsch, Henrion, and Schultz, *On the quantification of nomination feasibility in stationary gas networks with random load* (2016), already derive continuous piecewise quadratic-radical or rational circulation formulas on affine nomination rays in Theorem 6; their final section extends the method to node-disjoint cycles with attached trees. These local representations are a direct precursor and are not claimed as new here. See the [open author manuscript](https://www.wias-berlin.de/people/heitsch/GHHS16_Preprint.pdf) and the [independent source comparison](potential-flow-reopened-weighted-literature.md), which records the verified locators `[[schultz2016-on-the-quantification-of-nomination]] p.18-22` and `p.25-26`. The new combined claim concerns fixed-dimensional load factors, arbitrary weighted objectives, unbounded cactus rank, and certified accuracy-bit complexity.

No novelty is claimed for piecewise polynomial approximation, rational square-root approximation, fixed-dimensional real-algebraic optimization, or polynomial root isolation. [Newman's 1964 paper](https://people.math.ethz.ch/~hiptmair/Seminars/RAP_22/NEW64.pdf) establishes root-exponential rational approximation to absolute value; square-root approximation is a classical consequence. [Trefethen, Nakatsukasa, and Weideman, *Exponential node clustering at singularities for rational approximation, quadrature, and PDEs*](https://people.maths.ox.ac.uk/trefethen/clustering.pdf), discusses the square-root case and its integral quadrature construction. The repository already contains independently reviewed and more general [positive polynomial inverse approximation](certified-positive-polynomial-inverse-approximation.md) and [monotone polynomial inverse approximation](certified-monotone-polynomial-inverse-approximation.md) lemmas; the elementary square-root panels above are a simple specialization.

The potentially new network combination is the fixed-dimensional affine-load cactus theorem with arbitrary weighted objective, unbounded total cycle rank, polynomial accuracy-bit complexity, and rational feasible recovery. The [completed focused source comparison](potential-flow-reopened-weighted-literature.md) found no inspected matching combined theorem while identifying and crediting the direct local-formula and approximation predecessors. This bounded search does not establish priority by absence.

## Reproducible mechanism checks

[`reopened_weighted_checks.py`](../code/potential_flow_mpd/reopened_weighted_checks.py) checks the new square-root panels using exact rational arithmetic: it proves each sampled error bound by squaring rational interval endpoints, without a floating-point square root. The run covered 360 inputs at 4, 8, 12, and 20 requested bits, including every panel boundary and the zero region. The respective polynomial degrees were 17, 28, 39, and 61.

The same script independently solved 1,200 asymmetric cycles with two shared affine load factors by monotone scalar root finding and compared the selected formula (2) or (4), including 577 cases with `A<0`, 557 with `A>0`, and 66 with `A=0`. Maximum circulation disagreement was `2.84e-14`; maximum weighted-drop disagreement was `2.14e-11`. An explicit all-zero `A=B=0` stratum passed separately. These are exact approximation mechanism checks plus numerical local network checks; they do not implement or certify global semialgebraic optimization.

## Additional extension: exact capacities with algebraic recovery

The same compilation argument permits exact rational edge-flow capacity bounds, including positive symmetric limits `|x_e|<=u_e`. Add these affine inequalities in `(z,q)` to each cycle's local projection, and impose bridge capacities directly in `z`. More generally, a polynomial-size list of bounded-degree rational semialgebraic constraints defining a closed set and involving `z` and the flow coordinates of one cycle or bridge can be projected locally. The compact feasible parameter set can be nonconvex, but the sum-approximation proof and fixed-dimensional supremum search still apply. The conclusion is a certified additive value interval and an **algebraic** epsilon-optimal feasible parameter of polynomial representation size. For this extension feasibility can also be decided exactly. The rational LP recovery of Section 4 is not claimed, and constraints involving global potential differences across arbitrarily many cycles are not covered by this local projection argument.

Rational feasible output cannot be guaranteed under exact capacities, even on one four-edge cycle with strictly positive capacities. Let the oriented cycle flows, for one parameter `t in[1,2]`, be

```
x=(q+t-1, q-2, q, q-2),    beta=(1,1,1,2).
```

These flows realize the balanced affine nomination vector

```
b=(t+1,-t-1,2,-2).
```

Impose capacities `|x_3|<=1`, `|x_4|<=1`, and `|x_1|,|x_2|<=10`. The first two constraints force `q=1`. Cycle conservation is then

```
t^2-1+1-2 = t^2-2 = 0.
```

Thus the feasible parameter set is exactly `{sqrt(2)}`. All data, nominations as affine expressions, and strictly positive capacities are rational. This small example is a concrete obstruction to extending the rational-output statement through arbitrary exact capacity filters; it does not obstruct polynomial-size algebraic feasible output.

For practical rational output with capacities, a supplied slack margin gives a precise conditional recovery statement. Optimize over capacities tightened from `u_e` to `u_e-sigma`, with rational `sigma>0` and a nonempty tightened feasible set. Round an algebraic epsilon-optimal parameter by rational LP in `P` as in Section 4, choosing its coordinate error `delta` also so that

```
(sum_ij |H_ij|) delta / 2 <= sigma/2.
```

The difference-flow bound then preserves the original capacities, and the objective loss remains controlled by (5). This gives rational output feasible for the original capacities and near-optimal **relative to the tightened problem**. No closeness between the tightened optimum and the original capacity-constrained optimum is claimed without an additional assumption.
