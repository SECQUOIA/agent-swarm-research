# A correlation-polytope face in the unit-capacity rank-one hull

Status (2026-09-04): theorem and conic lower-bound transfers independently audited; explicit exposure lemma independently audited. The face embedding below was derived in this investigation. A targeted open-literature search found no prior statement of this embedding or its conic-size consequences for the pooling rank-one block. This is a provisional novelty assessment, not a claim that an exhaustive search can certify novelty. The extension-complexity theorems used in the corollaries are established literature results and are credited explicitly.

## Main result and significance

Consider nonnegative rank-one matrices subject only to unit upper bounds on every row sum and every column sum. All lower bounds are zero. Their convex hull contains a face affinely isomorphic to the correlation polytope on half as many indices.

This gives unconditional lower bounds for **every exact conic extended formulation**, even one chosen nonuniformly with arbitrary real coefficients: exponentially many fixed-size semidefinite blocks, exponential total second-order-cone dimension, and a superpolynomial lower bound on unrestricted semidefinite matrix order. No assumption such as P != NP, efficient constructibility, bounded coefficient encoding, or numerical well-posedness is required.

The matrices are a standard single-pool flow block. The conclusion is about exact convexification of that block; it does not assert that all restricted cost classes, approximate relaxations, or practical pooling instances require that size.

## Definitions

For an integer n >= 1, write

```
R_n = { W in R_+^(n x n) : rank(W) <= 1,
        W e <= e, W^T e <= e },
K_n = conv(R_n).
```

The vectors `e` have the appropriate dimension. The set `R_n` is compact: its constraints are closed, including the vanishing 2-by-2 minors, and every entry belongs to `[0,1]`. Therefore `K_n` is compact and every point of it is a finite convex combination of points in `R_n`.

The correlation polytope is

```
COR(m) = conv{ xx^T : x in {0,1}^m }.
```

For a nonzero `W in R_n`, let `r=W e`, `c=W^T e`, and `S=e^T W e>0`. The familiar rank-one identity gives

```
W = r c^T / S,    0 <= r,c <= e,    e^T r = e^T c = S.
```

A proof of that identity appears as Lemma 1 in [the earlier rank-one note](rank-one-row-column-hardness.md). The zero matrix is handled separately throughout.

## Lemma 1: the trace face selects normalized binary outer products

For all `W in K_n`, `trace(W) <= 1`. Moreover,

```
K_n intersect {trace(W)=1}
 = conv{ a a^T / |A| : empty != A subset [n], a=1_A }.
```

**Proof.** For a nonzero generating matrix,

```
trace(W) = (sum_i r_i c_i)/S <= (sum_i r_i)/S = 1.
```

If equality holds, `sum_i r_i(1-c_i)=0`. Every summand is nonnegative. Thus `r_i>0` implies `c_i=1`. Using also `sum_i c_i=S` gives `sum_i c_i(1-r_i)=0`, so `c_i>0` implies `r_i=1`. Together these imply `r=c=1_A` for a nonempty set `A`, and `S=|A|`. Conversely, every displayed normalized binary outer product belongs to `R_n` and has trace one.

For a finite convex combination attaining trace one, every positive-weight generating matrix must itself attain trace one. The zero matrix has trace zero and cannot occur with positive weight. This proves the equality of sets. QED.

## Theorem 1: a correlation-polytope face

Let `n=2m`, and pair index `i` with `m+i`, for `i=1,...,m`. Define

```
F_m = { W in K_(2m) :
          trace(W) = 1,
          sum_(i=1)^m W_(i,m+i) = 0,
          e^T W e = m }.
```

Then `F_m` is a face of `K_(2m)` and is affinely isomorphic to `COR(m)`.

The forward map is

```
X = m W_[m],[m].
```

The inverse map, with `x=diag(X)`, is

```
             [ X              x e^T - X                  ]
W = (1/m) * [                                            ].
             [ e x^T - X      e e^T - x e^T - e x^T + X  ]
```

**Proof.** By Lemma 1, the trace equation selects the convex hull of the matrices `a a^T/|A|` with `A` nonempty. All entries are nonnegative, so the second equation selects exactly those generating matrices for which

```
A contains at most one element from each pair {i,m+i}.
```

Indeed, its value at a generating matrix is the number of fully occupied pairs divided by `|A|`. Consequently `|A| <= m` for every remaining generating matrix. Its total entry sum is

```
e^T (a a^T/|A|) e = |A|.
```

The third equation therefore selects exactly the generators with `|A|=m`, which contain one element from every pair. They have the form

```
a = (x, e-x),    x in {0,1}^m,
W = (1/m) (x,e-x)(x,e-x)^T.
```

The trace constraint exposes a face of `K_(2m)`. The zero-entry-sum constraint exposes a face of that face, and maximization of total entry sum exposes a face of the resulting face. A face of a face is a face. In particular, it is not necessary to claim that the three equalities can be combined into one exposing functional.

The projection `X=m W_[m],[m]` sends these generators onto `xx^T`. Expanding the four blocks of their outer products gives the displayed inverse at every binary generator. Since each coordinate of the inverse is affine in `X`, the identity extends to their convex hulls. Thus the maps are mutual inverses on `F_m` and `COR(m)`. QED.

## Lemma 1b: an explicit exposing functional

Write `T(W)=sum_ij W_ij`, `D(W)=1-trace(W)`, and `B(W)=sum_i W_(i,m+i)`. On `K_(2m)`,

```
T(W) <= m + 2m B(W) + 4m D(W).
```

Consequently the affine functional

```
g(W) = m-T(W) + (2m+1) B(W) + (4m+1) D(W)
```

satisfies `g(W)>=B(W)+D(W)>=0`, and `F_m={W in K_(2m): g(W)=0}`. Thus this particular face is exposed, with integer coefficients bounded in magnitude by `4m+2` in the linear part of `g`.

**Proof.** Consider a nonzero generator `W=rc^T/S`. For each pair, `r_i+r_(m+i)-r_i r_(m+i)<=1`, because `(1-r_i)(1-r_(m+i))>=0`. Summing gives

```
S <= m + sum_i r_i r_(m+i)
  <= m + sum_i r_i c_(m+i) + ||r-c||_1.
```

For `a,b in [0,1]`, `|a-b|<=a(1-b)+b(1-a)`. Therefore

```
||r-c||_1 <= sum_i [r_i(1-c_i)+c_i(1-r_i)] = 2S D(W).
```

The cross-product sum equals `S B(W)` and `S<=2m`. These facts prove the bound for every nonzero generator. The zero matrix also satisfies it. The inequality is affine in `W`, so it holds on their convex hull. Substituting it into `g` gives `g>=B+D`. Equality `g=0` forces `B=D=0`, then `T=m`; conversely the three face equations give `g=0`. QED.

This lemma is stronger than the nested-face argument, but the conic lower-bound proof does not need it. It will be used for [quantitative stability and approximate formulations](rank-one-correlation-face-stability.md).

## Lemma 2: conic lift sizes pass to affine sections and images

Let a convex set `K` have a lift over a cone `C`:

```
K = pi(C intersect L),
```

where `L` is an affine subspace and `pi` is a linear map. If `F=K intersect H` for an affine subspace `H`, then

```
F = pi(C intersect L intersect pi^(-1)(H)).
```

Composing with a linear projection does not change the cone. Therefore, a lift of `K_(2m)` over any cone gives a lift of `COR(m)` over the same cone. This elementary argument uses the three equations defining `F_m`; it does not require a proper or strictly feasible lift, an exposed-face property, or a closedness assumption about arbitrary projections.

If the convention permits affine output maps instead of linear ones, the same affine-section/image argument applies. Standard conic formulations with explicit scalar inequalities should count those inequalities as nonnegative scalar cone factors; they are not free resources.

## Corollary 1: exponentially many fixed-size PSD blocks

Fix an integer `d>=1`. If `K_(2m)` has an exact lift over

```
(S_+^d)^r,
```

then, for `m>=d`,

```
r >= kappa(d) c(d)^m,
c(d) = (1 - 3^(-d))^(-1/d) > 1,
kappa(d) = (3^d - 1)^(-(1-1/d)).
```

For `d=2`, the stronger specific bound is

```
r >= (1/sqrt(7)) (9/7)^(m/2).
```

**Proof.** Apply Theorem 1 and Lemma 2, then Fawzi and Parrilo's Theorem 1, PDF p.3, to `COR(m)`. Their exact formulas give the constants above. [Fawzi and Parrilo, *Exponential lower bounds on fixed-size psd rank and semidefinite extension complexity*, arXiv:1311.2571](https://arxiv.org/pdf/1311.2571).

Blocks of order at most `d`, including scalar inequality factors, may be padded to order `d` without increasing the number of blocks. Thus the same lower bound applies to that convention. A large number of uncounted scalar inequalities would invalidate a claim about only the number of non-scalar blocks; no such claim is made here.

The `d=1` statement is formally valid but is not the principal contribution: the unit-capacity hull itself is nonpolyhedral already for two rows and columns, so it has no finite LP lift. The useful new conclusions concern conic formulations that do exist for these rank-one hulls.

## Corollary 2: exponential total SOCP dimension

Every exact second-order-cone lift of `K_(2m)` has total cone dimension `2^(Omega(m))`, counting nonnegative scalar cone factors.

**Proof.** A Lorentz cone

```
L_k = { (t,z) in R x R^k : ||z||_2 <= t }
```

with `k>=2` has a lift using `k-1` copies of `L_2`; see Fawzi and Parrilo, PDF p.3. The cone `L_2` is linearly isomorphic to `S_+^2`. The cone `L_1` is linearly isomorphic to two nonnegative scalars, and each scalar can be embedded in one `S_+^2` block. Hence a lift of total cone dimension `D` yields a lift with at most `D` blocks of order two. Corollary 1 implies

```
D >= (1/sqrt(7)) (9/7)^(m/2).
```

The conclusion concerns total cone dimension. It does not assert an exponential count of Lorentz cones when their dimensions are unrestricted. QED.

## Corollary 3: unrestricted SDP lifts have superpolynomial order

There is an absolute constant `alpha>0` such that every exact lift of `K_(2m)` over a single positive semidefinite cone `S_+^q` satisfies

```
q > 2^(alpha m^(2/13)),    m>1.
```

**Proof.** A lift of that order gives one of the same order for `COR(m)`. Apply Lee, Raghavendra, and Steurer's Theorem 1.1 (PDF p.5), also stated as Theorem 5.4 (PDF p.34). [Lee, Raghavendra, and Steurer, *Lower bounds on the size of semidefinite programming relaxations*, author-hosted manuscript](https://www.dsteurer.org/paper/sdpsize.pdf).

Here `q` is the order of the PSD matrix, not the number of scalar entries. Several blocks with total order `q` can be combined into one block-diagonal cone of order `q`, so the bound also applies to total block order in a general SDP lift. Linear inequalities count as blocks of order one. These are bounds on exact representations with arbitrary real coefficients, not merely on efficiently constructible formulations. QED.

## A direct check of the nonpolyhedral caveat

For `n=2`, take the face of `K_2` where the first row and column sums both equal one. Each nonzero generator on this face has

```
r=c=(1,t),  0<=t<=1,
W(t) = [1,t; t,t^2]/(1+t).
```

Writing `q=W_11=1/(1+t)`, the lower-right entry is

```
W_22 = q + 1/q - 2,     1/2 <= q <= 1.
```

This function is strictly convex, so every point of its graph is extreme in the convex hull of the graph. Therefore `K_2` has infinitely many extreme points and is nonpolyhedral. The same applies to `K_n` for `n>=2` by fixing all entries outside a 2-by-2 principal block to zero. This is why an unconditional finite-LP-size lower bound alone would provide little information here.

## Relationship to existing rank-one convexification work

The earlier repository result proves strong NP-hardness for two-sided rank-one bounds with fixed positive lower bounds on one row and one column. Its formulation-size conclusion excludes polynomial-time constructible compact hulls under P != NP. The present theorem uses zero lower bounds and uniform unit upper bounds, and excludes small exact conic lifts unconditionally, whether or not they can be constructed algorithmically.

The result is compatible with finite, potentially exponential SOCP descriptions of general two-sided rank-one hulls: the claim is a lower bound on their size, not nonrepresentability by SOCP. The targeted local literature is Dey, Kocuk, and Santana's rank-one pooling convexification work, and Jalilian and Kocuk's two-sided rank-one hull work. The fixed-block and unrestricted-PSD lower bounds are transferred from existing correlation-polytope theorems; the proposed new contribution is the explicit face inside this unusually simple continuous rank-one flow set.

## Novelty search and verification record

The open-primary-source search on 2026-09-04 used combinations including `rank-one row column correlation polytope`, `rank-one pooling extension complexity`, and `rank-one row and column semidefinite convex hull complexity`. It located the established correlation-polytope lower bounds but no prior matching face embedding in the two-sided unit-capacity pooling rank-one hull. Relevant full-text pages of the two lower-bound papers were opened and their theorem statements checked. A broader search and review of later pooling literature remain appropriate before any submission-level novelty claim.

Independent proof audit passed; see [the audit record](../notes/review-rank-one-extension.md). Exact rational enumeration for m=1,...,6 checked the selected atom counts and every entry of the affine inverse. These computations supplement the proof; they do not establish its general case.
