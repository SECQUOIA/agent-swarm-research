# Second independent review: weighted-potential hardness on one cycle

Date: 2026-09-05. Reviewer: `potential_flow_review`.

**Verdict: PASS for the reduction, membership, integer scaling, and continuous-box companion.** Reviewed [the full candidate](potential-flow-weighted-potential-cycle-hardness.md). One limitation sentence needed correction: an additional common integer scaling also proves fixed absolute-error approximation hardness. That consequence is derived below and was sent to the author and root. It does not establish strong NP-hardness or relative-error hardness.

The objective here is an arbitrary fixed weighted potential functional, not a single pairwise difference or edge flow. The nonzero nominations `(2,-3,1)` and objective coefficients `(-5,12,-7)` are the same three small integer vectors in every constructed instance. All scenarios are unrestricted physical states. The reduction has fixed resistances on two edges and two choices on each uncertain path edge.

## 1. Signs and the triangle identities

With cycle orientation `0->1->2->0`, conservation gives flows `q+2,q-1,q`. Their net nominations are exactly `(2,-3,1)`. For `-1/2<q<0`, their signs are positive, negative, negative. The directed sum of pressure drops is consequently

```
(q+2)^2-(q-1)^2-theta*q^2=6q+3-theta*q^2.
```

It is negative at `q=-1/2` and positive at zero. The sum of the three strictly increasing constitutive terms is strictly increasing, so this interval contains the unique physical circulation. The stated rationalized root

```
q=-6/(6+sqrt(36+12theta))
```

is the negative root of that equation.

The objective coefficient vector sums to zero and its pressure decomposition is correct:

```
-5*pi_0+12*pi_1-7*pi_2
 =-5*(pi_0-pi_1)+7*(pi_1-pi_2)
 =-5*(q+2)^2-7*(q-1)^2
 =-105/4-12*(q+1/4)^2.
```

Thus its upper bound is attained only at `q=-1/4`, which requires `theta=24`. At `theta=16/3,144`, substitution gives `q=-3/8,-1/8`, respectively, and objective `-423/16`. The interior advantage is `3/16`. In particular, this does not contradict any pairwise-pressure or arc-flow hull theorem.

## 2. The Subset-Sum construction

The source uses positive binary integers and `K>0`; instances with `K>S=sum a_i` can be mapped to the fixed no-instance described in the candidate. A path replacing the third triangle edge, with zero nominations and objective weights at its internal vertices, carries constant flow `q`. Its quadratic resistances add, independently of the negative sign of that flow.

The two positive, distinct options on path edge `i` give effective resistance

```
theta=12+(12/K)*sum_i a_i*sigma_i.
```

Therefore the objective reaches its global upper bound exactly when the selected subset sums to `K`. The threshold direction `max F>=-105/4` is correct, even though every value is nonpositive. The graph remains a simple cycle of maximum degree two, including the `n=1` triangle case. Only the three original vertices have nonzero nominations or objective coefficients. Rational numerators and denominators have polynomial total encoding length.

The reduction establishes hardness of a weighted-potential objective with fixed coefficients. It does not use varying objective weights to encode the source instance.

## 3. The explicit separation gap

Let `q_0=-1/4`. Subtracting the circulation polynomial at `q` and at `q_0` gives

```
(q+1/4)*(6+theta*(1/4-q))=(theta-24)/16.
```

Its second factor is positive. If no selected subset equals the target, integer spacing gives `|theta-24|>=12/K`. The bounds `q>-1/2` and `theta<=12+12S/K` imply

```
16*(6+theta*(1/4-q))<240+144S/K,
|q+1/4|>=1/(20K+12S).
```

Substitution in the objective identity yields the stated valid gap

```
Delta=12/(20K+12S)^2=3/(4*(5K+3S)^2).
```

The intermediate estimate is actually strict; weakening it to the displayed non-strict bound is harmless. This gap applies to every non-target subset, even in a yes instance containing other choices.

The rational performance threshold `J=-105/4-Delta/2` has a violating scenario exactly when the Subset-Sum instance is yes. This establishes the robust upper-bound direction. An additive value approximation with error below `Delta/4` separates yes and no cases, and a feasible discrete witness within that accuracy of a yes-instance optimum must encode an exact target subset. The required precision has polynomial binary length.

## 4. Integer scaling and an additional approximation consequence

Multiplying every resistance by `L=4nK` multiplies all potentials by `L` while leaving flows unchanged. This follows either by substitution in the physical equations or by multiplying the entire energy by `L`. The first two resistances become `4nK`, and the path options become

```
48K, 48K+48n*a_i.
```

All are positive integers. The equality threshold becomes `-105nK`. The nominations and objective weights remain the same fixed integers.

There is a further elementary strengthening. Let

```
T=(5K+3S)^2.
```

Multiply every resistance once more by the positive integer `T`. All data still have polynomial binary encoding length, and the objective threshold becomes the integer

```
H=-105nK*T.
```

The no-instance gap is now

```
L*T*Delta=3nK>=3.
```

Hence a value approximation with absolute error at most one separates yes and no instances: yes estimates are at least `H-1`, whereas no estimates are at most `H-2`. Comparing with `H-3/2` decides the source instance. Likewise an additive-error-one feasible resistance witness must encode a target subset in a yes instance.

Thus constant absolute-error approximation is NP-hard on the further-scaled integer family. The original sentence that the reduction does not imply a fixed-accuracy obstruction was too broad and should be replaced by this consequence or explicitly limited to its unscaled gap. This scaling argument **does not** imply strong hardness: the numerical magnitudes still depend on binary Subset-Sum data. It also does not imply hardness for fixed relative error or an objective normalized to a bounded range.

## 5. Exact verification on one cycle

For fixed rational resistance choices and rational balanced nominations, choose a rational particular conserved flow and consistently orient the cycle. All flows are `q+d_e` for one scalar `q`. The physical equation

```
sum_e beta_e*(q+d_e)*abs(q+d_e)=0
```

is continuous, strictly increasing, and tends to opposite infinities. Its breakpoints are rational. Their order and the function values at them can be computed exactly in polynomial bit time. A breakpoint root is rational. Otherwise the unique root lies in one sign interval, on which the equation is quadratic or linear with rational coefficients of polynomial encoding length. A constant zero polynomial cannot occur on a nonempty interval because the original function is strictly increasing.

The root therefore has algebraic degree at most two and polynomial encoding length. Every potential drop is a signed quadratic polynomial in this same root; all potentials and the weighted objective lie in the same degree-at-most-two field. Summing path drops introduces no independent radical extensions. Comparisons with rational thresholds, including equality and strict violation, are exact polynomial-time operations.

Selecting one explicitly listed option per uncertain edge is a polynomial-size certificate. This proves NP membership for the existential target-threshold and upper-bound-violation problems, and coNP membership for robust upper-bound satisfaction. Combined with the reductions, the NP/coNP-completeness assertions hold on the claimed fixed-nomination, fixed-weight, one-cycle subclass.

## 6. The continuous interval companion

For fixed global cycle rank `r` and fixed nominations, a fundamental-cycle parameterization writes all flows as affine functions of `r` core variables. The hyperplanes at which these flows vanish have polynomially many cells for fixed `r`; lower-dimensional cells and their closures are included. On a sign cell, each pressure drop is `beta_e*p_e(z)` with rational quadratic `p_e`.

The `r` cycle equations are necessary and sufficient for these drops to be a potential difference vector. Expressing normalized potentials along a spanning tree makes any rational zero-sum weighted objective another sum of such drops with rational coefficients. The resulting objective and linking equations therefore fit the reviewed fixed-core theorem with fixed core dimension, scalar interval leaves, fixed linking dimension, and degree two. The number of uncertain resistance leaves can grow with the input. An optional objective coordinate increases the fixed dimension by one only.

Compact core bounds are valid: in a fundamental-cycle basis, circulation coordinates equal chord flows because the tree-supported particular flow is zero on chords. The passive acyclic-flow bound gives `|z_i|<=B=sum|b_v|`. With one potential normalized, the stated bound

```
|F|<=B^2*||c||_1*sum_e beta_e^upper
```

is conservative and polynomially encoded. Every physical state satisfies these bounds, so imposing them removes no valid optimizer. Positive finite resistance intervals ensure compactness and physical uniqueness. Exact algebraic optimization and witness recovery then follow from the fixed-core theorem already audited in the repository.

On trees, conservation fixes every flow, making the objective linear in the independent resistances. Choosing the appropriate listed extremum on each edge solves the finite-set problem exactly. Consequently a single cycle is indeed the first possible global cycle rank for this discrete obstruction. Neither positive argument uses the nomination-face theorem for pairwise pressure objectives, and neither claims tractability for arbitrary nomination uncertainty.

## Verification and limits

I reran the supplied checker: three symbolic identities and three rational triangle states passed, as did 1,776 resistance scenarios across 44 cycle instances, including 68 exact target subsets. The maximum reported cycle-pressure residual was `1.7642055e-90`. The proof and encoding checks above are independent of these numerical experiments.

The construction and positive companion are mathematically sound. The additional scaling consequence corrects an overly restrictive approximation caveat rather than weakening the theorem. No separate novelty clearance is supplied by this review; classical circuit optimization and the precise one-cycle weighted-objective boundary still require their own source comparison.
