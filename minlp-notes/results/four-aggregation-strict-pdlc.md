# Four aggregations suffice for strict three-quadratic PDLC hulls

Date: 2026-09-22. Status: complete proof with independent adversarial reviews
of the original argument, its simplification, and the final all-dimensions
version. The priority audit is complete; novelty remains provisional.
This result uses the published
Blekherman–Dunbar four-aggregation theorem as an input; it does not reprove
that theorem's topology.

## Main result and significance

**Theorem.** Let `n>=1` and let `Q1,Q2,Q3` be real symmetric `(n+1)`-square
matrices. Put

```
f_i(x)=(x,1)^T Q_i (x,1),
S={x in R^n : f_i(x)<0 for i=1,2,3}.
```

Assume `S` is nonempty and that there is a signed vector `theta in R^3`
with `sum_i theta_i Q_i` positive definite (PDLC). If `conv(S)` is proper,
there are `1<=r<=4` nonzero nonnegative multipliers `lambda^1,...,lambda^r`
such that

```
conv(S) = intersection_(j=1)^r {x:f_lambda^j(x)<0}.
```

Every `Q_lambda^j` has exactly one negative eigenvalue, and each inequality
is strictly valid on `conv(S)`: these are good aggregations in the
Blekherman–Dey–Sun definition. Linear independence is not required. The
number four is sharp for every `n>=3`, as verified below using their existing
Example 2.20.

There are no boundedness, nonsingularity, regularity, or no-points-at-infinity
assumptions on the original system. If the hull is all of `R^n`, the empty
family describes it. The upper bound includes dimensions one and two; the
sharpness proof below applies to every dimension at least three.

The new argument proposed here transfers the published regular, bounded
closed-set four-bound to arbitrary ordinary strict hulls. It combines inward
homogeneous perturbation, an elementary regular-level argument, and
preservation of strict goodness in a fixed-cardinality limit. The theorem
rules out the six-necessary assertion in BDS Conjecture
3.2 in the dimension range of that source, and also gives the upper bound in
lower dimensions.

The structural consequence is that at most four essential quadratic
aggregations suffice, or at most four oriented second-order-cone constraints
for the closed hull of the strict set. This is an existence theorem. It does
not provide an efficient method to discover the multipliers, and does not
establish a solver speedup.

## External input and proof organization

The main input is Blekherman–Dunbar (BD), *A Topological Approach to Simple
Descriptions of Convex Hulls of Sets Defined by Three Quadrics*, SIAM J.
Applied Algebra and Geometry 9(2), 2025, 310–342, Theorem 1.4. A linearly
independent PDLC triple whose nonstrict feasible set `C` has nonempty
interior, `C=cl(int C)`, and no points at infinity has its closed convex hull
described by at most four permissible good aggregations. No smoothness
hypothesis on the spectral curve is imposed in this theorem. Its proof
explicitly covers `n=1`, `n=2`, and `n>=3`, so the input is valid in all
dimensions used here.

We perturb the original triple by three fixed linearly independent positive
definite matrices. This produces independent triples except at finitely many
parameters, including when the original triple is dependent. The inward
perturbations give bounded regular nonstrict sets to which BD applies. We
then strictify their descriptions and pass to limiting multipliers.

## Lemma A: generic inward levels are regular

Let `h` be continuous on a topological space `M` with a countable base.
Except for at most countably many values `c`,

```
{z in M : h(z)<=c} = cl_M {z in M : h(z)<c}.
```

Proof. If equality fails, continuity shows there is a point `z` with
`h(z)=c` and an open neighborhood `U` containing no point with `h<c`.
Choose a member `B` of the countable base with `z in B subset U`.
Then `c=inf_(y in B) h(y)`. Every exceptional value is therefore the
infimum on one of countably many basis sets. This proves the claim.

## Lemma B: proper hulls have bounded inward perturbations

Write `A_i` for the leading `n`-square block of `Q_i`. If `conv(S)` is
proper, there is no nonzero `d` satisfying `d^T A_i d<0` for every `i`.
Indeed, if such a direction existed, for every `x in R^n`, both `x+td` and
`x-td` would satisfy all original inequalities for sufficiently large `t`.
Their midpoint is `x`, implying `conv(S)=R^n`.

Choose three linearly independent positive definite `(n+1)`-square matrices
`R1,R2,R3`. They exist for every `n>=1`; for example, with standard basis
vectors `e1,e2` in `R^(n+1)`, take

```
R1=I,
R2=I+e1 e1^T,
R3=I+(e1+e2)(e1+e2)^T.
```

Set `g_i(x)=(x,1)^T R_i(x,1)>0`. For `epsilon>0` put

```
Q_i^epsilon=Q_i+epsilon R_i,
f_i^epsilon(x)=f_i(x)+epsilon g_i(x),
S_epsilon={x:f_i^epsilon(x)<0 for every i},
C_epsilon={x:f_i^epsilon(x)<=0 for every i}.
```

The system for `C_epsilon` has no points at infinity. A nonzero direction
satisfying `d^T(A_i+epsilon R_i[1:n,1:n])d<=0` for every `i`
would satisfy `d^T A_i d<0` for every original `i`, since each leading
principal block of `R_i` is positive definite. This was excluded.
The same condition makes `C_epsilon` bounded: otherwise, normalizing an
unbounded feasible sequence and taking a convergent subsequence would give
a nonzero common nonpositive direction for all leading perturbed matrices.
The set `C_epsilon` is closed, hence compact.

Fix any `x0 in S`. For every sufficiently small epsilon it belongs to
`S_epsilon`. PDLC persists because, for a fixed PDLC certificate `theta`,

```
Q_theta^epsilon=Q_theta+epsilon sum_i theta_i R_i
```

remains positive definite for sufficiently small epsilon. The perturbed
matrices are linearly independent except at finitely many epsilon values:
choose a three-by-three coordinate minor of the vectorized `R_i` with
nonzero determinant. The corresponding minor of the vectorized
`Q_i+epsilon R_i` is a polynomial in epsilon with that nonzero determinant
as its cubic leading coefficient. It has only finitely many roots. This
argument covers dependent original triples as well.

Moreover `S_epsilon subset S`, and every fixed finite subset of `S` is
contained in `S_epsilon` for all sufficiently small epsilon.

Apply Lemma A to the continuous function on `R^n`

```
h(x)=max_i [f_i(x)/g_i(x)].
```

Choose `epsilon_k downarrow 0` small enough for the preceding properties,
avoiding both the finitely many dependence parameters and the countably
many exceptional levels `-epsilon_k`. Then

```
C_epsilon_k = cl(S_epsilon_k) = cl(int(C_epsilon_k)),
int(C_epsilon_k) != empty.
```

The second equality follows because the open set `S_epsilon_k` is contained
in `int(C_epsilon_k)`, while `C_epsilon_k` is closed. Thus every hypothesis
of the published BD theorem holds for these perturbed systems in the
original affine coordinates. No projective change of coordinates or initial
good aggregation is needed.

## Lemma C: strictifying the four-aggregation description

Fix one selected epsilon. BD provides at most four nonzero nonnegative
multipliers with at most one negative homogenized eigenvalue such that

```
cl(conv C_epsilon) = intersection_j {x:f_lambda^j^epsilon(x)<=0}.
```

Because `C_epsilon=cl(S_epsilon)`, its closed convex hull equals
`cl(conv S_epsilon)`. Discard every aggregate polynomial that is globally
nonpositive: its nonstrict inequality is redundant. At least one aggregate
remains because the hull is nonempty and bounded.

A quadratic polynomial `p` that is not globally nonpositive cannot vanish
at an interior point of `{p<=0}`. Such a point would be a local maximum at
zero; its gradient would vanish and its Hessian would be negative
semidefinite, making its global maximum zero. Consequently

```
conv(S_epsilon) = intersection_j {x:f_lambda^j^epsilon(x)<0}.
```

To see the equality explicitly, `conv(S_epsilon)` is a nonempty open convex
set and hence the interior of its closure. Every point of that interior is
an interior point of each quadratic sublevel, and therefore strictly
satisfies every retained inequality. Conversely, strict satisfaction of
finitely many inequalities gives an interior point of their intersection.
All remaining multipliers are thus strict-good for `S_epsilon`. Their
matrices have exactly one negative eigenvalue because their polynomials are
strictly negative at the feasible point `x0`.

## Lemma D: bounded-cardinality strict aggregation survives the limit

Take the sequence `epsilon_k downarrow 0` selected in Lemma B.
For each `k`, use the four-bound representation of `conv(S_epsilon_k)`.
Duplicate an existing multiplier if necessary to have exactly four, and
normalize each by `sum_i lambda_(k,j),i=1`. Pass to a common subsequence
such that `lambda_(k,j)->lambda_j` for all four indices.

Every limit lies in the nonnegative simplex and is nonzero.
The matrices

```
M_(k,j)=sum_i lambda_(k,j),i Q_i
        + epsilon_k sum_i lambda_(k,j),i R_i
```

converge to `M_j=Q_lambda_j`: the perturbation term is bounded in norm by
`epsilon_k max_i ||R_i||`. The set of matrices with at most one
negative eigenvalue is closed, and `f_lambda_j(x0)<0` at any fixed
`x0 in S`. Thus each limit has exactly one negative eigenvalue.

It remains essential to prove *strict* goodness; nonstrict validity alone
would be insufficient. Choose unit negative eigenvectors `v_(k,j)` of
`M_(k,j)`, oriented to have positive scalar product with `(x0,1)`.
After subselection they converge to a unit negative eigenvector `v_j` of
`M_j`. For each fixed `x in S`, both `x` and `x0` eventually belong to
`S_epsilon_k`. The strict-good property of the kth aggregation implies
that their lifts are in the same negative-cone component, so

```
v_(k,j)^T(x,1)>0.
```

Taking limits gives `v_j^T(x,1)>=0`. But `f_lambda_j(x)<0` because all
three original constraints are strict and the limit multiplier is in the
simplex. A vector on the hyperplane perpendicular to the unique negative
eigenvector cannot have negative quadratic value. Therefore the scalar
product is strictly positive. All lifts of `S` lie in a single convex
component of `{z:z^TM_jz<0}`. Consequently `lambda_j` is strict-good for
`S`, and its inequality holds strictly throughout `conv(S)`.

Conversely, if `x` strictly satisfies all four limiting inequalities, then
by convergence it strictly satisfies all four kth inequalities for all
large `k`. Hence `x in conv(S_epsilon_k) subset conv(S)`. We obtain

```
conv(S) = intersection_(j=1)^4 {x:f_lambda_j(x)<0}.
```

No interchange between closure and convex hull is used in this final step.
The proof relies on fixed-cardinality compactness *and* the negative-cone
orientation argument; ordinary pointwise limits of closed inequality
representations would not suffice.

## Dependent triples need at most two

The unified perturbation proof already covers dependent triples. A stronger
known bound is available in that case. Strict feasibility makes the cone
generated by the original matrices pointed: evaluation at a fixed feasible
lift is strictly negative on every nonzero nonnegative combination. If the
span has dimension at most two, this cone has at most two extreme rays,
each generated by an original matrix. All other inequalities are nonzero
nonnegative combinations of these. The feasible set therefore reduces to
at most two strict quadratic inequalities. Yıldıran (2009), Theorem 1,
gives at most two good aggregations in every dimension. This additional
observation is not needed for the main theorem.

## Sharpness: the existing four-necessary example, checked directly

BDS Example 2.20 uses `s=x1`, `rho=sum_(i=2)^n x_i²`, and

```
f1=-s²+1+rho,
f2= s²+5s-4+rho,
f3=-s-rho.
```

The identity

```
-7f1-3f2-15f3=4s²+5rho+5
```

proves PDLC in every dimension. Strict feasibility holds at `s=-3,rho=4`.
Any feasible point has `s<-1`: the first inequality requires `|s|>1`, while
the second excludes `s>=1`. In particular `f1` is good because the feasible
points lie in its negative `s` Lorentz component. The ball inequality `f2`
is convex and good. Combining `f3<0` with each of the first two inequalities
shows respectively

```
s < alpha=(-1-sqrt(5))/2,
s > beta=-2-2sqrt(2).
```

Therefore `f1+f3` and `f2+f3` are good as well: each is a quadratic in `s`
with one negative homogenized eigenvalue, and the indicated interval contains
all feasible `s`. These four inequalities are the hull description stated
in BDS.

Here is an independent proof that no three good aggregations can suffice.
For a nonnegative multiplier `(a,b,c)`, the coefficient of `rho` is
`a+b-c`. If it were negative, the homogenized matrix would have at least
`n-1>=2` negative eigenvalues. Thus every good multiplier lies in

```
K={(a,b,c)>=0 : c<=a+b}
 = cone{(1,0,0),(0,1,0),(1,0,1),(0,1,1)}.
```

The following four points, specified by their `s,rho` values, make exactly
one of the four displayed extreme-ray aggregates zero and the other three
strictly negative:

| Designated multiplier | `s` | `rho` |
|---|---:|---:|
| `(1,0,0)` | `-2` | `3` |
| `(0,1,0)` | `-4` | `8` |
| `(1,0,1)` | `alpha` | `0` |
| `(0,1,1)` | `beta` | `0` |

For example take `x2=sqrt(rho)` and all remaining coordinates zero.
Since every good multiplier is a nonnegative combination of these four
rays, at the designated witness it is strictly negative unless it is a
positive multiple of that designated ray. Each witness lies outside
`conv(S)` because its designated good inequality is zero. Every exact
strict-good aggregation family must therefore include all four rays. This
establishes sharpness for all `n>=3` without relying only on the source's
assertion of necessity.

## Closed hull: four oriented SOC constraints

For each selected good matrix write

```
Q_j=P_j-v_j v_j^T,  P_j>=0,
```

using its unique negative eigenvalue and its positive eigenvalues; choose
the sign of `v_j` so `v_j^T(x0,1)>0` for one fixed `x0 in S`.
The chosen homogeneous negative component is

```
||P_j^(1/2) (x,1)||_2 < v_j^T(x,1).
```

All of `conv(S)` lies in that component. Their intersection equals
`conv(S)`, since it contains the hull and is contained in the intersection
of the corresponding four strict quadratic inequalities. Moreover,

```
cl(conv(S)) = {x : ||P_j^(1/2)(x,1)||_2 <= v_j^T(x,1), j=1,...,r}.
```

To prove the reverse closure inclusion, take any point satisfying all these
closed SOC constraints and mix it with `x0` with a positive weight on
`x0`. Convexity of the norm makes each SOC slack strictly positive, since
its slack at `x0` is positive. The mixture is in `conv(S)` and approaches
the given point as that weight decreases to zero.

This is the closure of the hull of the **strict** feasible set. It need not
be the hull of the original nonstrict feasible set, which can contain
additional lower-dimensional components. Nor can a strict aggregation
representation always be closed merely by replacing `<` by `<=` and
forgetting the chosen components. For example, in any `n>=3`,

```
f1=-x1²+x1,  f2=||x||²-1,  f3=-||x||²-1
```

satisfies PDLC because `-Q3=I`. Its strict set and hull are the open half-ball
`{x1<0,||x||<1}`, described by the two strict good inequalities `f1<0` and
`f2<0`. The corresponding nonstrict inequalities also contain the isolated
point `e1`, outside the closed half-ball. This is the mechanism of BDS
Example 2.22, padded with a redundant PDLC constraint.

## Literature comparison and verification

Primary sources inspected:

- Yıldıran, *Convex hull of two quadratic constraints is an LMI set*, IMA
  Journal of Mathematical Control and Information 26(4), 2009, 417–450,
  [accepted author text](https://www.researchgate.net/publication/220386378_Convex_hull_of_two_quadratic_constraints_is_an_LMI_set),
  Sections 2–3.2 and Theorem 1, including Assumption 1 and its inertia
  convention. This supplies the optional stronger two-bound for dependent triples; it is
  not an input to the main four-bound proof.

- [BDS full text](https://arxiv.org/html/2210.01722v1), with a local copy at
  `literature/papers/blekherman2024-aggregations-of-quadratic-inequalities-and/`.
  The cited source has the six upper bound, four lower bound, and Conjecture
  3.2. The lower-bound construction is credited to that source.
- [BD arXiv full text](https://arxiv.org/html/2405.18282v1) and
  [published text](https://epubs.siam.org/eprint/VRNXYR5GPAAPTF5RJHV3/full).
  The published four-bound retains both regularity and no-points-at-infinity
  assumptions. The proposed contribution is the transfer removing them for
  strict hulls, not the original four-bound for regular bounded systems.
  Proposition 3.15 and Section 8 of the inspected arXiv version already use
  negative-eigenvector limits to study good aggregations for a fixed set.
  That is an antecedent of Lemma D; the present proof combines inward
  compactification with a limit whose feasible sets also vary.
- Alex Dunbar's 2025 dissertation,
  [record](https://etd.library.emory.edu/concern/etds/vq27zq10w),
  [PDF](https://etd.library.emory.edu/downloads/2j62s637x?locale=en).
  Theorem 5.0.5 is stated with regularity and nonempty interior but without
  a no-infinity assumption. The priority reviewer retrieved its complete
  text through a public text proxy and found that its proof invokes
  Propositions 5.3.12 and 5.3.13, which explicitly assume no points at
  infinity. The apparent stronger statement is therefore not a safe input
  without resolving that dependency. See the [complete priority audit](../notes/review-20260922-pdlc-priority.md).
  Our proof uses only the published theorem with all its hypotheses.

No inspected source explicitly states this universal strict four-bound;
this is not proof of novelty. A search failing to find the transfer does not
establish priority.

The coordinator independently rederived the original argument, the direct
compactification, the countable-base lemma, the independent positive
perturbations, strict limiting goodness, and the oriented SOC corollary.
The [first proof review](../notes/review-20260922-pdlc-transfer.md) and
[second proof review](../notes/review-20260922-pdlc-second.md) checked the
original argument and rechecked the substantive simplifications. A
[fresh review of the final proof](../notes/review-20260922-compact-pdlc.md)
independently checked positive definite perturbations for dependent triples,
all positive dimensions, and the limiting quantifiers. No mathematical gap
was found. These are internal research reviews, not journal peer review.
The primary-source priority audit records the dissertation discrepancy and
retrieval limits explicitly.
The full investigation is preserved in
[the research note](../notes/research-20260922-pdlc-frontier.md).

The proofs are mathematical, not Lean-verified. The targeted command
`python3 code/research_20260922/check_four_aggregation_pdlc.py` verified the
PDLC identity, strict feasibility at `s=-3,rho=4`, and all four witness
slack vectors, including radical signs. All assertions passed; an earlier
Python/SymPy heredoc checked the same identities. These computations
check the finite algebraic identities, not the universal regularization and
limit arguments. No repository-wide verification or CI inspection was performed.
The proof does not establish an
efficient multiplier algorithm, rational coefficient bounds, or a result for
arbitrary nonstrict feasible sets.
