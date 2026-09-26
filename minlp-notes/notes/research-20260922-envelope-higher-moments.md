# Higher moments of smoothed parametric support dictionaries

Date: 2026-09-22. Status: two independent adversarial reviews checked the
continuous and finite-grid arguments without finding a substantive gap.
The author and coordinator independently rechecked the finite-grid extension.
Novelty remains provisional; the source comparison below identifies close
classical antecedents.

## Main result

All fixed moments of the number of distinct active supports have polynomial
bounds in every fixed parameter dimension. Quadratic structure is unnecessary.
The proof uses coordinate shattering of near-optimal supports, followed by a
finite parameter net. This concerns distinct supports, not connected regions:
even two Lipschitz branches can alternate infinitely often.

Let `Z` be a nonempty subset of `{0,1}^m`, with `m>=1`. On a nonempty compact
metric parameter space `T`, let every deterministic function `q_z` be `L`-Lipschitz. Let the
coordinates of `xi` be independent and have densities bounded by `phi>0`.
Write

```
F_z(t)=q_z(t)+xi dot z,
K=|{z: z minimizes F_w(t) over w in Z for some t in T}|.
```

The count includes supports that minimize only at isolated parameter points
or ties. No genericity assumption on the branch functions is required.
Compactness also makes the count measurable: a fixed support is active
exactly when the minimum over `T` of its nonnegative difference from the
envelope is zero. That minimum is continuous in the finite noise vector,
so each support's activity event is closed.

**Theorem.** Fix a real `p>=1` and set

```
delta_p = 1/[2m phi (m+1)^p].
```

If `L>0` and `T` has a `delta_p/(2L)`-net of cardinality `J`, then

```
E K^p <= e J^p.                                      (1)
```

In particular, for `T=[-M,M]^d` with Euclidean distance,

```
E K^p <= e [1+4ML sqrt(d) m phi (m+1)^p]^(dp).         (2)
```

This is polynomial for fixed `d,p`. The bound is deliberately coarse. It
does not claim the best dependence on `m`, the smoothing density, or `p`.
If `L=0`, all branches are constant on the nonempty parameter domain; since
the noise has densities, the minimizer is unique and `K=1` almost surely.
Under the atomic noise of Section 4, several supports may tie everywhere, so
uniqueness can fail; bound (5) with `delta=0` still controls the moments. The case `m=0` is also trivial. A common function may be
subtracted from every branch before imposing the Lipschitz assumption.

## 1. A near-optimal set rarely shatters many coordinates

Fix arbitrary deterministic real costs `g_z`, and define

```
v=min_z (g_z+xi dot z),
A_delta={z: g_z+xi dot z <= v+delta},
N_delta=|A_delta|,
D_delta=VCdim(A_delta).
```

Here a coordinate set `I` is shattered when the projections of `A_delta`
onto `I` contain every binary pattern on `I`. The maximum cardinality of a
shattered set is its VC dimension; a singleton family has VC dimension zero.

**Lemma 1.** For every integer `1<=k<=m`,

```
Pr(D_delta>=k) <= binom(m,k) (2phi delta)^k.           (3)
```

**Proof.** Fix a coordinate set `I` of size `k`, and condition on all noise
outside `I`. For every pattern `a` on `I`, define the conditional class cost

```
C_a=min_(z_I=a) [g_z+sum_(j notin I) xi_j z_j].
```

An empty class means `I` cannot be shattered. Otherwise every `C_a` is
finite and independent of the remaining random coordinates `xi_I`.
If `I` is shattered by `A_delta`, each class has a near-optimal
representative. Therefore its minimum satisfies

```
v <= C_a+xi_I dot a <= v+delta.
```

Use only the zero pattern and the `k` unit patterns. For each `i in I`,

```
|C_ei+xi_i-C_0| <= delta.
```

Thus `xi_I` lies in a fixed axis-parallel box with side lengths `2delta`.
Conditional independence and the density bounds give probability at most
`(2phi delta)^k`. Union over the `binom(m,k)` coordinate sets. If a larger
set is shattered, all its `k`-element subsets are shattered, so this union
also bounds the event in (3). QED.

The zero and unit pattern class minima are crucial. Merely conditioning on
coordinate-wise near ties would leave thresholds depending on other random
coordinates and would not justify multiplying probabilities.

## 2. Every fixed moment of a sufficiently narrow near-optimal set is bounded

The classical Sauer--Shelah bound gives

```
N_delta <= sum_(j=0)^D_delta binom(m,j) <= (m+1)^D_delta.
```

For the second inequality, encode a subset of size at most `D_delta` by its
increasing elements followed by zero padding in a sequence of length
`D_delta` over `{0,...,m}`. The case `D_delta=0` has both sides equal to one.

The classical combinatorial inequality can be checked by induction without
any probabilistic input. Split a binary family by its last coordinate and
project the two parts to families `A_0,A_1` on `m-1` coordinates. Their union
has VC dimension at most `D`; their intersection has VC dimension at most
`D-1`, since a shattered set in the intersection can be extended by the last
coordinate. The identity
`|A|=|A_0 union A_1|+|A_0 intersect A_1|` and Pascal's recurrence prove the
displayed bound, with the empty intersection treated separately.

**Lemma 2.** For every real `p>=1` and every `delta>=0`,

```
E N_delta^p <= exp[2m phi delta (m+1)^p].              (4)
```

**Proof.** Put `a=(m+1)^p`. Since `D_delta` is integer-valued,

```
E N_delta^p
 <= E a^D_delta
 <= 1+sum_(k=1)^m a^k Pr(D_delta>=k)
 <= sum_(k=0)^m [2m phi delta a]^k/k!
 <= exp(2m phi delta a).
```

We used (3) and `binom(m,k)<=m^k/k!`. At `delta=delta_p`, the bound is `e`.
The estimate is valid for arbitrary deterministic costs, arbitrary feasible
subsets of the cube, and arbitrary independent bounded-density noise. Noise
need not have bounded support, be identically distributed, or be unimodal.
QED.

## 3. A parameter net captures every active support

Let `t_1,...,t_J` be an `eta`-net, where `eta=delta_p/(2L)`. Suppose support
`z` minimizes at some `t`. Choose `t_j` within distance `eta`, and let `w`
minimize at `t_j`. The Lipschitz property gives

```
F_z(t_j) <= F_z(t)+L eta
          <= F_w(t)+L eta
          <= F_w(t_j)+2L eta.
```

Thus `z` belongs to the `delta_p`-near-optimal set at `t_j`, and

```
K <= sum_(j=1)^J N_delta_p(t_j).
```

Convexity of `x -> x^p` for `p>=1` gives

```
K^p <= J^(p-1) sum_j N_delta_p(t_j)^p.
```

Apply Lemma 2 separately at each deterministic net point and take
expectations. No independence between parameter points is used. This proves
(1). To obtain (2), partition every coordinate interval into at most
`ceil(M sqrt(d)/eta)` subintervals of length at most `2eta/sqrt(d)` and take
their Cartesian-product midpoints. The resulting Euclidean `eta`-net has
at most `[1+M sqrt(d)/eta]^d` points. QED.

## 4. Direct finite-grid theorem with logarithmic random precision

Assume instead that every independent noise coordinate satisfies

```
Pr(xi_i in J) <= phi length(J)+tau
```

for every closed interval `J`. The preceding argument works without change,
except that the probability of each shattering box is at most
`(2phi delta+tau)^k`. Thus

```
Pr(D_delta>=k) <= binom(m,k)(2phi delta+tau)^k,
E N_delta^p <= [1+(m+1)^p(2phi delta+tau)]^m
            <= exp[m(m+1)^p(2phi delta+tau)].          (5)
```

The first line is also valid at `delta=0`. Tied supports are all counted;
there is no need to deduplicate their polynomials, add infinitesimal noise,
or transfer a continuous result by a limiting argument.

For uniform noise on `N>=2` equally spaced points of `[-sigma,sigma]`, one
may use `phi=1/(2sigma)` and `tau=1/N`. Indeed the spacing is
`2sigma/(N-1)`, so an interval of length `ell` contains at most
`ell(N-1)/(2sigma)+1` grid points. Choose

```
delta_p = 1/[4m phi(m+1)^p],
N >= 2m(m+1)^p.
```

The exponent in (5) is at most one. Applying the same net argument proves

```
E K^p <= e [1+8ML sqrt(d)m phi(m+1)^p]^(dp).          (6)
```

Taking `N` to be the smallest power of two satisfying the displayed lower
bound uses `O_p(log(m+1))` independent random bits per coordinate. For
rational `sigma`, each perturbation has rational bit length polynomial in
the bit length of `sigma` and `log N`. The theorem itself does not establish
the bit complexity of subsequent algebraic computations.

A stronger classical form of the same combinatorial lemma states that a
binary family has at most as many members as it has shattered coordinate
subsets. The preceding union/intersection induction proves this too:
shattered sets of the union persist without the last coordinate, while
shattered sets of the intersection persist with it. The two collections
are disjoint. Summing the probability bound for each shattered set gives
the sharper first-moment estimate

```
E N_delta <= (1+2phi delta+tau)^m.                    (7)
```

Consequently, for the first moment alone one can use
`delta=1/(4m phi)` and `tau<=1/(2m)`, removing the extra factor `m+1` from
the net bound. This refinement is not needed for the higher-moment or
algorithmic conclusions.

Independent reviewer `/root/review_higher_gap_cover` identified this direct
finite-grid consequence. Both the author and coordinator checked its
conditioning, constants, and treatment of persistent ties independently.

## Consequences and limitations

The theorem removes the higher-moment obstacle for algorithms whose running
time is polynomial in a fixed collection of distinct-support dictionary
sizes. For example, if `S` is the sum of at most `B` such sizes and the
running time is at most `C(1+S)^p`, convexity bounds its expectation by a
polynomial whenever `B,C`, the Lipschitz parameters, and the inverse noise
scale are polynomially bounded and parameter dimension and `p` are fixed.
No independence between those dictionaries is needed.

This is a representation theorem. It does not supply an enumeration
algorithm, a valid dynamic program, or a bit-complexity bound. Those require
separate proofs. It also does not control how many disconnected regions use
the same support. The sharper scalar and planar geometric bounds remain
useful when connected regions or sharp dependence on the smoothing scale
matter, but they are unnecessary for polynomial moments of distinct support
counts.

## Prior results and novelty status

The combinatorial ingredient is the classical Sauer--Shelah lemma, not a new
set-system theorem. The conditional class-minimum argument is a direct
relative of isolation and higher-gap arguments in smoothed optimization.

[Röglin and Teng, *Smoothed Analysis of Multiobjective Optimization*,
FOCS 2009](https://www.microsoft.com/en-us/research/wp-content/uploads/2009/04/Pareto.pdf)
already prove polynomial bounds on all fixed moments of smoothed Pareto
counts. The linked 18-page manuscript states its generalized winner gap as
Lemma 3.2, proves it in Appendix A, and applies it in Section 6.1. This
conditioning method is an especially relevant antecedent. A parallel local
investigation extends that method to arbitrary
deterministic offsets and reaches the present parametric conclusion through
a different rank argument. Therefore a claim to have introduced polynomial
moment bounds in smoothed optimization would be incorrect.

[Brunsch and Röglin, *Improved Smoothed Analysis of Multiobjective
Optimization*](https://arxiv.org/abs/1111.1546) sharpen earlier Pareto moment
bounds in a model with several perturbed linear objectives and one arbitrary
objective. The present statement concerns one common random linear penalty
added to an arbitrary uniformly Lipschitz family of deterministic parameter
functions. Its exact relationship to existing parametric and higher-gap
formulations still needs a focused priority review. Novelty is provisional;
the useful established content is the explicit proof and its applicability
to the local message algorithms.

Sources examined during this investigation: the Röglin--Teng open manuscript,
the Brunsch--Röglin arXiv abstract and bibliographic record, and the primary
[Beier--Röglin--Rösner--Vöcking 2023 article](https://link.springer.com/article/10.1007/s10107-022-01885-6),
whose related-work discussion distinguishes bounded-support and quasiconcave
assumptions in earlier moment bounds. The latter source is a comparison
aid; no theorem above depends on its claims.

## Verification status

The inequalities above were checked independently in the
[higher-gap and covering review](review-20260922-higher-gap-cover.md) and
[VC and finite-grid review](review-20260922-vc-grid-moments.md).
The latter prompted the compactness assumption and the explicit distinction
between continuous and atomic ties when the Lipschitz constant is zero.
No Lean formalization has been performed.

Targeted command actually run:

```
python3 code/research_20260922/check_envelope_higher_moments.py
```

It passed 2,295 exact finite-distribution cases, covering all nonempty
subsets of the three-dimensional cube, three deterministic cost functions,
and three near-optimality tolerances, including exact ties. The checker
examined 61,965 noise states, 48,813 conditional interval implications, and
6,885 rational moment inequalities. It uses exact integer and rational
arithmetic. These finite checks test the proof's combinatorial and atomic
edge cases; they do not establish the general theorem, net argument, or any
algorithmic running-time claim. No project-wide checks were run.
