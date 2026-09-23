# Spatial box covers remain exponential with higher-order SOS relaxations

Date: 2026-09-05. Status: promoted after independent review to
`results/spatial-bb-higher-sos-exponential-lower-bound.md`. The derivation
below is retained as research history. This extends the reviewed
SDP–RLT result in `results/spatial-bb-sdp-rlt-exponential-lower-bound.md`.

## Proposed result and explicit relaxation

Use the continuous program `P_n` with objective `sum_i x_i(1-x_i)`, equality
`sum_i x_i=K=k+1/2`, and unit-box bounds. Fix an integer `r>=1`. On a box
`B=prod_i[a_i,b_i] subset [0,1]^n`, consider linear functionals `L` on real
polynomials of total degree at most `2r` satisfying:

1. `L[1]=1`.
2. `L[(sum_i x_i-K)q]=0` whenever `deg(q)<=2r-1`.
3. For every polynomial `q` and every product `g` of coordinate-bound slacks
   `x_i-a_i` and `b_i-x_i`, including the empty product, require
   `L[g q^2]>=0` whenever `deg(g)+2 deg(q)<=2r`.

Repeated slack factors are allowed. Define the node lower bound as the
infimum of `L[sum_i x_i(1-x_i)]` over these functionals. This is the full
truncated box preordering relaxation; it includes the usual order-`r`
moment and localizing constraints, all box RLT products through degree
`2r`, and all equality products through degree `2r`. It is valid by taking
`L` to be evaluation at any feasible point. At `r=1` it is exactly the
SDP–RLT model in the preceding result.

Let `n=k+m+z` with positive integer parts, `0<epsilon<1/4`, and define

```
h=m(1/2-2epsilon),
q_r = min{ k-2r+2, z-2r+2, h }.
```

**Candidate theorem.** If `q_r>0`, every cover of the feasible set by boxes
whose order-`r` node lower bound is at least `1/4-epsilon` has at least

```
min{ (n/(n-k))^(q_r/2), (n/(n-z))^(q_r/2) }
```

members. For `k=m=z=t` and any fixed `epsilon<1/4`, this is exponential in
`n=3t` whenever `r <= c t` for a constant `c<1/2`. In particular, at
`epsilon=1/8` the original `(3/2)^(n/24)` bound survives for every
`r <= 3t/8+1`. The precise inequality is `t-2r+2 >= t/4`.

This is a node-count/degree tradeoff. A high-order SDP is itself expensive;
the claim is that even granting it as a node oracle does not remove the
exponential spatial-cover obstruction at the stated orders.

## Elementary fractional-cardinality moment lemma

Write `(v)_a=v(v-1)...(v-a+1)` and `(v)_0=1`. Given `s` Boolean formal
variables `u_1,...,u_s` and a real number `t`, define a functional by reducing
monomials modulo `u_i^2=u_i` and putting

```
E_{s,t}[u_S] = (t)_{|S|}/(s)_{|S|}.
```

We only evaluate degrees below the number of variables, or at most that
number, so denominators are nonzero.

**Lemma A.** If `d>=1`, `s>=2d`, `t>=2d-1`, and `s-t>=2d-1`, then
`E_{s,t}[p^2]>=0` for every polynomial `p` of degree at most `d`.
The cardinality identity
`E_{s,t}[(sum_i u_i-t)p]=0` holds for every `deg(p)<=2d-1`.

*Proof.* The identity follows for squarefree `u_S`, `|S|=a`, from

```
a (t)_a/(s)_a + (s-a)(t)_(a+1)/(s)_(a+1) = t (t)_a/(s)_a.
```

It therefore holds for all allowed polynomials, using Boolean reduction.

To check positivity it suffices to check homogeneous squarefree polynomials
of degree exactly `d`. Indeed, for every `S` of size `a<=d`, define

```
H_S(u) = [sum_{T superset S, |T|=d} u_T] / C(t-a,d-a).
```

The denominator is positive because `t>=2d-1>=d`, except when `d=1`
where `t>=1` still suffices. Modulo the Boolean identities, the numerator is
`u_S (sum_i u_i-a)_(d-a)/(d-a)!`. Thus `u_S-H_S` is in the ideal generated
by `sum_i u_i-t` and `u_i^2-u_i`, with a representation of degree at most
`d`. The cardinality identities imply
`E_{s,t}[(u_S-H_S)v]=0` whenever `deg(v)<=d`. Replacing each monomial of `p`
by `H_S` gives a homogeneous `H` with `E[p^2]=E[H^2]`.

For homogeneous monomials indexed by `d`-subsets `I,J`, the moment matrix is

```
N(I,J) = (t)_(2d-|I intersect J|)/(s)_(2d-|I intersect J|).
```

For `j=0,...,d`, let `P_j(I,J)=C(|I intersect J|,j)`. Each `P_j` is PSD:
it is the Gram matrix of incidence vectors whose entries indicate whether
a fixed `j`-subset lies in `I`. The falling-factorial Vandermonde identity
gives

```
N = sum_{j=0}^d [ (t)_(2d-j) (s-t)_j / (s)_(2d) ] P_j.
```

To verify an entry with intersection size `ell`, factor
`(t)_(2d-ell)/(s)_(2d)` and apply Vandermonde to
`(t-2d+ell)+(s-t)=s-2d+ell` at falling-factorial order `ell`.
Every coefficient is nonnegative under the hypotheses. Hence `N` is PSD,
which proves the lemma. QED.

The positivity condition is deliberately sufficient rather than optimal.
Classical Grigoriev bounds allow larger degree than this elementary
positive-Gram decomposition needs.

## Positivity for all truncated box products

**Lemma B.** Suppose `r>=1`, `s>=2r`, and `t,s-t>=2r-1`. Then `E_{s,t}`
is nonnegative on every `g p^2` with `deg(g)+2deg(p)<=2r`, where `g` is a
product of the slacks `u_i` and `1-u_i`.

*Proof.* Boolean reduction turns `g` into zero if conflicting factors occur,
or into the indicator

```
I_{A,B}=prod_{i in A}u_i prod_{j in B}(1-u_j)
```

for disjoint sets `A,B`. Let `a=|A|`, `b=|B|`, `v=a+b`, so `v<=deg(g)`.
Its expectation is

```
pi = (t)_a (s-t)_b/(s)_v >=0.
```

The formal conditioning identity is

```
E_{s,t}[I_{A,B} p^2]
= pi E_{s-v,t-a}[p(1_A,0_B,u_remaining)^2].
```

For `pi>0`, this identity follows by expanding monomials and canceling
falling factorials. If the original `p` is nonconstant, then
`a+b<=deg(g)<=2r-2`; since `t,s-t>=2r-1`, both falling-factorial factors
are strictly positive, so `pi>0`. If `pi=0`, the original `p` must be
constant and the desired inequality is simply `pi p^2>=0`.

If the restricted polynomial is constant, nonnegativity follows from
`pi>=0`. Otherwise put `d=deg(p(1_A,0_B,u_remaining))>=1`. We have
`2d+v<=2r`, hence `s-v>=2d`, and

```
t-a >= 2r-1-a >= 2d-1,
(s-v)-(t-a) = s-t-b >= 2r-1-b >= 2d-1.
```

Lemma A applied to the remaining variables proves the claim. QED.

*Boundary detail.* If `v=s`, the restricted polynomial is constant and
no conditional functional with denominator zero is needed.

## Proof of the cover bound

Use the same witnesses `w=1_H+p 1_M`, `p=1/(2m)`, with uniformly random
ordered partitions of sizes `k,m,z`. In a containing box define
`R={i:a_i>0 or b_i<1}` and `U=[n] minus R`.

Suppose `|R|<q_r`. Since `|R|` is an integer and
`|R|<k-2r+2,z-2r+2`, at least `2r-1` coordinates of `H` and at least
`2r-1` coordinates of `Z` remain in `U`. Put `s=|U|` and

```
t=|H intersect U| + p |M intersect U|.
```

Then `t>=2r-1` and `s-t>=2r-1`; also `s>=2r` (for `r=1`, at least one
coordinate of each endpoint type remains; for `r>=2`, `s>=4r-2>=2r`).

Define the node functional by substituting `x_i=w_i` on `R` and applying
`E_{s,t}` to the remaining variables. Every interval in `U` is `[0,1]`.
On `R`, bound slacks become nonnegative constants. Thus Lemma B proves
all preordering inequalities, including products using restricted and
unrestricted coordinates. The functional satisfies the global equality
products by the cardinality identity. Normalization is immediate.

All objective terms on `U` have zero expectation, and those on `R` equal
`w_i(1-w_i)`. Hence this feasible node functional has objective

```
|M intersect R|p(1-p) <= |R|p(1-p) < h/(2m) = 1/4-epsilon.
```

Therefore a pruned box containing a witness must have `|R|>=q_r`.
Writing `R=A union D` as in the preceding SDP–RLT result gives
`|A|>=q_r/2` or `|D|>=q_r/2`, and the identical uniform-subset avoidance
and cover counting argument proves the theorem. QED.

## Scope and sources

This is a stronger but more expensive node relaxation than the preceding
SDP–RLT model. It does not allow arbitrary valid inequalities that cannot be
obtained within the stated degree from box slacks and the equality. Symmetry
breaking, non-coordinate branching, and objective-cutoff localizing
constraints need separate analysis. Feasibility-based box tightening is
covered because it preserves the feasible-set cover; objective-based
cutoffs are covered only through explicitly charged discarded certified
slabs as in the preceding result.

The fractional-cardinality moment functional is classical, associated with
Grigoriev's knapsack lower bound. [Potechin (2019), Theorem 1, Example 18,
and Theorem 44](https://drops.dagstuhl.de/storage/00lipics/lipics-vol124-itcs2019/LIPIcs.ITCS.2019.61/LIPIcs.ITCS.2019.61.pdf)
provide a primary-source account. The incidence-Gram matrices `P_j` are
standard Johnson-scheme objects. The candidate contribution is the
continuous arbitrary-box cover tradeoff, not these moment ingredients.
A dedicated literature comparison for the combined theorem remains pending.


## Targeted checks

`code/spatial_bb_lower_bound/check_higher_sos.py` passed exact
falling-factorial Gram coefficient identities, 540 homogenization identities,
and all conditioning identities/localizer pattern sizes for nine parameter
triples through `r=3`. Numerical PSD checks covered full moment matrices up
to dimension 232 and all tested localizing matrices. The exact proof above
supplies positivity independently of floating-point checks.

## Perturbed objective: unique minimizer and no permutation symmetry

This corollary applies both to the new order-`r` result and to the reviewed
SDP–RLT result at `r=1`.

Let `0<d_1<...<d_n` and `sum_i d_i<=eta`, and replace the objective by

```
F_d(x)=sum_i x_i(1-x_i)+sum_i d_i x_i.
```

The domain remains the same. Its **unique** global minimizer is

```
x_i=1 for i<=k;  x_(k+1)=1/2;  x_i=0 for i>=k+2,
```

with value `OPT_d=1/4+sum_{i<=k}d_i+d_(k+1)/2`. Distinct linear coefficients
remove every nonidentity variable-permutation symmetry of the model.

*Proof of uniqueness.* Strict concavity implies that every minimizer is a
vertex. At a vertex there are `k` ones and one half coordinate. If the half
coordinate is `j>k`, the cheapest possible choice of ones is `1,...,k`,
and the cheapest such half coordinate is `k+1`. If it is `j<=k`, the
cheapest choice of ones is `{1,...,k+1} minus {j}`. The linear cost then is
`sum_{i<=k}d_i+d_(k+1)-d_j/2`, which exceeds
`sum_{i<=k}d_i+d_(k+1)/2` because `d_j<d_(k+1)`. Every other choice of ones
has strictly greater linear cost. Hence the displayed vertex is the unique
minimizer. QED.

For `epsilon+eta<1/4`, put

```
h_eta=m(1/2-2epsilon-2eta),
q_(r,eta)=min{k-2r+2,z-2r+2,h_eta}.
```

If `q_(r,eta)>0`, any cover that certifies `epsilon`-optimality using the
same order-`r` relaxations requires at least

```
min{ (n/(n-k))^[q_(r,eta)/2], (n/(n-z))^[q_(r,eta)/2] }
```

boxes. Indeed `OPT_d>=1/4`, and the constructed functional has first
moments in `[0,1]`, so its linear perturbation contributes at most `eta`.
When `|R|<q_(r,eta)`, its objective is therefore strictly below
`h_eta/(2m)+eta=1/4-epsilon<=OPT_d-epsilon`, preventing pruning. The same
witness count applies. All other steps are unchanged.

For an explicit family take `d_i=2eta i/[n(n+1)]`, which has total mass
`eta`. With `n=3t`, `epsilon=1/8`, and `eta=1/32`, the cover bound is
`(3/2)^(3t/32)=(3/2)^(n/32)` whenever `r<=13t/32+1`. At `r=1`, this is an
exponential SDP–RLT spatial lower bound with a unique optimizer and no
nontrivial variable-permutation symmetry.

If also `eta<epsilon`, an `O(2^n)` upper certificate follows from the
original chord tree at tolerance `epsilon-eta`: its base-objective bound
is at least `1/4+eta-epsilon>=OPT_d-epsilon`, and the added linear term is
nonnegative. Thus the explicit family just given has `2^{Theta(n)}`
certificate size under the same model.
