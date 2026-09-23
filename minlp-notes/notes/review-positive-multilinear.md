# Independent audit of the positive multilinear gap counterexample

Date: 2026-09-04. Reviewer: independent audit agent, separate from the construction's
initial author and from the root agent's sparse simplification. Reviewed file:
`results/positive-multilinear-gap.md`, including its unit-coefficient block construction.

**Outcome:** the sparse theorem and its logarithmic upper bound on the hull gap are
mathematically correct under the stated assumptions. No unresolved proof gap was found.
This is an independent mathematical agent audit, not journal peer review, formal proof
verification, or certification of literature priority.

## Original conjecture and scope

I read the local extracted text and visually checked page 22 of the original PDF at
[[luedtke2012-some-results-on-the-strength]] p.22. The conjecture concerns positive
multilinear functions on boxes with nonnegative lower bounds and a uniform constant
bounding the term-by-term gap divided by the convex-hull gap. The constructed unit-box
family is inside that scope. The [authors' open technical report](https://jlinderoth.github.io/papers/Luedtke-Namazifar-Linderoth-12-TR.pdf)
contains this statement as Conjecture 1. The published version identifies it as
Conjecture 4.1, as visible in the author's uploaded
[published text](https://www.researchgate.net/publication/228577706_Some_results_on_the_strength_of_relaxations_of_multilinear_functions).

Three independent web queries on 2026-09-04 combined “multilinear,” “positive
coefficients,” “conjecture,” “gap,” “Luedtke,” “Conjecture 4.1,” and
“term-by-term gap counterexample.” They found the original conjecture but no prior
resolution. This is limited negative search evidence, not proof of novelty.

## Algebra and convexification checks

1. Let `m=2^L`, `u_j=2^(−j)`, and partition the leaves into `2^j` blocks of size
   `k_j=m/2^j`. The polynomial `Σ_j Σ_{B∈P_j} a_j ∏_{i∈B}z_i` has exactly
   `2m−2` distinct monomials, each with coefficient one. The total number of variable
   occurrences is `Lm+2m−2`. No partition nesting is needed for the bound.

2. At `a_j=u_j`, `z_i=1−1/m`, the exact lower envelope of every product is
   `max(0,u_j+k_j(1−1/m)−k_j)=0`. The exact upper envelope is `u_j`.
   Each level consequently contributes one to the term-by-term gap.

3. These product upper envelopes can all be attained in one vertex distribution.
   With `U` uniform on `(0,1)`, set `A_j=1[U≤u_j]` and
   `Z_i=1[U≤1−1/m]`. Every anchor event is contained in every leaf-success event.
   All required means hold and every included product has mean `u_j`.
   Hence `cav f(x)=tbt_upper(x)=L`, not merely `cav f(x)≤L`.

4. A multilinear graph over the cube has the same convex hull as its binary-vertex
   graph. One way to see this is to represent a point in the graph by independent
   Bernoulli variables with its coordinates as means. Therefore its convex envelope
   at the specified point is a minimum expected value over vertex distributions
   with precisely those means. This justifies the probabilistic formulation.

5. For a vertex, let `R` be the number of failed leaves and `N_j` the number of
   hit blocks at level `j`. The pointwise identity is
   `f=Σ_j A_j(2^j−N_j)`. Because `E R=1` and `2^j E A_j=1`,
   the hull gap is exactly `max E Σ_j A_jN_j`. Disjoint blocks imply
   `N_j≤min(2^j,R)` for every vertex, regardless of dependence among the leaves.

6. Replacing `N_j` by its count bound and dropping leaf geometry is an **upper
   relaxation**. It need not preserve the exact sparse hull gap. The author corrected
   this distinction while preparing the sparse draft. The dense symmetric model's
   failure-count LP is exact for that dense model, and its numerical table is now
   explicitly separated from the sparse theorem.

## Coupling and analytic bound

For fixed law of `R`, a binary variable of mean `u` maximizes `E[A g(R)]`, for
nondecreasing `g`, by selecting the upper `u`-tail, allowing fractional selection
within an atom. This follows by exchanging selected mass at a smaller `R` with
unselected mass at a larger `R`. A single decreasing quantile `r(t)` represents the
law of `R`, and all anchor optima are simultaneously feasible in the upper relaxation:
set `A_j=1[t≤2^(−j)]`. There is no missing consistency condition between anchors,
because only their separate means have been imposed. Thus

```
H_L ≤ sup ∫ Σ_{j:t≤2^(−j)} min(2^j,r(t)) dt,
        r≥0, ∫r=1.
```

The supremum displayed here also drops quantile monotonicity and integrality. This is
safe for an upper bound. The draft's subsequent argument does not require either.

The interval `t≤2^(−L)` contributes less than two, using the finite geometric sum.
The interval `t>1/2` contributes zero. On the remaining interval, with
`l=floor(log₂(1/t))`, splitting terms at `floor(log₂ r)` proves

```
Σ_{j=1}^l min(2^j,r) ≤ r[3+log₂⁺(1/(tr))].
```

I checked separately `r=0`, `0<r<2`, `2≤r<2^l`, and `r≥2^l`. The endpoints are
harmless and the inequality holds for real `r`, not just integer counts.

Let `D=(2^(−L),1/2)`, `M=∫_D r≤1`, and `B=(L−1)ln 2`. Replacing the positive
logarithm by `ln(1+s)` gives an entropy integral. Jensen under probability measure
`r(t)dt/M` yields

```
∫_D r ln(1+1/(tr)) dt ≤ M ln(1+B/M) ≤ ln(1+B).
```

The integral is zero if `M=0`. At `r=0`, the integrand has limit zero. The last
inequality follows from monotonicity in `M`, since
`ln(1+s)−s/(1+s)≥0`. All integrals are over a domain bounded away from zero, so
the Jensen argument remains valid after removing the zero-density set.

Consequently `H_L≤5+log₂(1+(L−1)ln2)`. The gap is strictly positive: independent
Bernoulli coordinates give every monomial a value strictly below its upper-envelope
value. Combining positivity, `tbtgap=L`, and this upper bound proves the divergent
ratio. Since `n=2^L+L`, the stated rate `Ω(log n/log log n)` follows.

An independently derived alternative uses `r(t)≤1/t` for decreasing quantiles and
Jensen relative to base measure `dt/t`; it gives the same logarithmic order. The
draft's `ln(1+s)` argument is cleaner and avoids using quantile monotonicity after
it has been dropped.

## Supplementary exact finite checks

For consecutive dyadic partitions, I independently enumerated every binary vertex
and solved the full convex-envelope LP for `L=2` and `L=3`. I then reconstructed
both a primal distribution and a dual vector as rational numbers with Python
`fractions.Fraction`, checking all mean equations, nonnegative primal weights,
every dual inequality over every vertex, and equality of primal and dual values.
These are exact rational certificates after floating-point discovery.

| L | Variables | Binary vertices | Convex envelope | Concave envelope | Hull gap | Gap ratio |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 6 | 64 | 1/2 | 2 | 3/2 | 4/3 |
| 3 | 11 | 2048 | 1 | 3 | 2 | 3/2 |

The defect identity and every bound `N_j≤min(2^j,R)` were also checked at every
one of these vertices. These checks support the algebra and interpretation; the
proof of unboundedness is the analytic argument above.

## Limits that should remain explicit

The theorem concerns the specified term-by-term product-hull relaxation. It does
not give a lower bound for every recursive reformulation that shares auxiliary
products or adds additional valid inequalities. The degree grows with `L`, the anchor
means range down to `1/m`, and leaf means approach one. The result does not settle
fixed-degree or uniformly interior subclasses. The logarithmic upper bound is not
claimed to be the exact hull gap, and no optimality claim is made for the asymptotic
ratio rate.

## Addendum: exact hull gap for nested dyadic blocks

The author subsequently proposed an exact formula for the sparse model with consecutive
nested dyadic blocks. I independently checked this stronger result. The argument is
correct and gives

```
B_q=(L−q+2)/2^q  (1≤q≤L),    B_{L+1}=0,
choose s with B_{s+1}≤1≤B_s,
H_L=s+(L−s)/2^s.
```

The formula is independent of the threshold choice when an equality makes two choices
possible. The following supplies the details I checked, including integrality and
simultaneous attainment of all block counts.

Partition `(0,1/2]` into intervals with `l` active anchors. Their lengths are
`w_l=2^(−l−1)` for `1≤l<L`, and `w_L=2^(−L)`. The utility on such an interval is
`S_l(r)=Σ_{j=1}^l min(2^j,r)`. Its successive marginal slopes are `l` on `[0,2]`,
`l−1` on `[2,4]`, and so on, ending in slope `1` on `[2^(l−1),2^l]` and zero
thereafter. The cumulative resource filled by all slopes at least `q` is therefore

```
Σ_{l=q}^L w_l 2^(l−q+1) = (L−q+2)2^(−q) = B_q.
```

An explicit upper certificate avoids relying only on the informal instruction to fill
slopes in decreasing order. Define `r_l^(q)=2^(l−q+1)` if `l≥q` and zero otherwise.
For every `r≥0`, the piecewise-linear concave function satisfies

```
S_l(r) ≤ s r + Σ_{q=s+1}^L r_l^(q).
```

This is its supporting affine upper bound with slope `s`. Integrate across the
quantile intervals, use total resource `∫r=1`, and allow unused resource outside
`(0,1/2]`. This yields

```
H_L ≤ s + Σ_{q=s+1}^L B_q = s+(L−s)/2^s.
```

For the reverse inequality, put `R=r_l^(s)` or `r_l^(s+1)` on interval `l`.
Use the same independent mixing probability

```
p=(1−B_{s+1})/(B_s−B_{s+1})
```

at each interval, taking the first profile with probability `p`. Let `R=0` when no
anchor is active. Every count is an integer between zero and `m`, and the mixture
has `E R=1`. Keep the anchor events `A_j=1[U≤2^(−j)]`; their prescribed means
are unaffected by the extra mixture. Between the two profile counts, the utility
has constant slope `s` whenever the counts differ. Both profiles thus attain the
supporting affine bound, including cases where they coincide.

It remains to realize the count upper bound by actual failed leaves. Label leaves
by the `L`-bit integers `0,…,m−1`. In bit-reversal order, the first `R` labels hit
exactly `min(2^j,R)` blocks of the partition by the first `j` bits: the sequence of
such prefixes cycles through all `2^j` possibilities before repeating. Therefore
this single failed set simultaneously satisfies `N_j=min(2^j,R)` at every level.
Apply a uniformly random XOR mask to all its labels. This permutes every dyadic
partition, so it preserves every hit count, while each leaf belongs to the failed
set with conditional probability `R/m`. Consequently every leaf has unconditional
failure probability `E R/m=1/m`, as required. No extra relaxation remains in this
attainment construction, proving equality with the upper certificate.

The exact formula implies `H_L=log₂ L+O(1)` and hence the ratio is
`L/(log₂ L+O(1))`. The threshold inequalities give `2^s` comparable to `L`,
while `(L−s)/2^s` stays bounded. This exact result requires the nested dyadic
partitions used in its attainment proof; the earlier logarithmic upper bound is
valid for arbitrary partitions of the prescribed sizes.

Supplementary checks: exact rational arithmetic verified the threshold and sum
identities for `L=1,…,200`. Exhaustive checks of all prefix counts `R` and every
partition level verified the bit-reversal hit-count assertion for `L=1,…,8`.
The exact formula also agrees with the independently certified full-vertex hull
values for `L=2,3` above. These finite checks supplement the all-`L` proof.

## Elementary restriction explaining the boundary dependence

A supplementary bound gives context without a novelty claim. Remove affine terms,
which do not affect either gap. Suppose every remaining monomial has at least two
coordinates whose prescribed means are at most `1−ε`, where `ε>0`. Write `cav_e`
for that monomial's upper-envelope value, namely its smallest coordinate mean.
Under independent Bernoulli coordinates, the product mean is at most
`(1−ε)cav_e`. Since all coefficients are positive, simultaneous comonotone coupling
attains the sum of all monomial upper envelopes, whereas the independent coupling
is feasible for the convex-envelope minimization. Therefore

```
chgap ≥ cav f − E_independent f ≥ ε cav f ≥ ε tbtgap.
```

The final inequality uses the nonnegative term-by-term lower bound on the unit box.
Hence the ratio is at most `1/ε` on this subclass. In particular, a uniform bound
away from one on every coordinate suffices; a bound away from zero is unnecessary
for this elementary argument. The counterexample violates this restriction because
each monomial contains one small anchor and leaves whose means approach one.
