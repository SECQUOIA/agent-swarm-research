# Accuracy-bit optimization with one resource-coupled polynomial follower

Date: 2026-09-05. Status: two independent full proof audits passed;
focused primary-source comparison is complete, with provisional novelty status.
[First audit](../notes/review-bilevel-one-resource-accuracy-bit-algorithm.md);
[second audit](../notes/review-bilevel-one-resource-accuracy-bit-algorithm-second.md). Section 9 extends the result to arbitrary dense strictly convex polynomial local costs, using a separately twice-audited inverse lemma and two audited transfer addenda. Its original scalar inverse-approximation dependency has passed
[two independent audits](../notes/certified-positive-polynomial-inverse-approximation.md).
This extends the [diagonal power result](../results/bilevel-bounded-power-accuracy-bit-algorithm.md)
by one resource equality, using an exact monotonicity identity.

## 1. Model and proposed theorem

Fix the leader dimension `r`. Let `X subset [0,1]^r` be an explicitly given
rational polytope, which may be lower dimensional. For `i=1,...,N`, let

```
g_i(z)=sum_(j=1)^(P_i) a_ij z^j,
a_ij>=0 rational,   G_i=g_i(1)>0,   P=max_i P_i.
```

The degrees need not be fixed. The complexity below is polynomial in their
numerical maximum `P`; dense or unary encodings give the usual polynomial
input-size guarantee. Let `ell_i(x)` and `b(x)` be rational affine functions,
and let `w_i` be arbitrary fixed rational coefficients, including negative
or zero coefficients. The follower solves

```
minimize F_x(z)=sum_i [integral_0^(z_i) g_i(s) ds-ell_i(x)z_i]
subject to z in [0,1]^N,   sum_i w_i z_i=b(x).                    (1)
```

Each integral is strictly convex on `[0,1]`; thus the feasible follower has
a unique minimizer `z*(x)`. The leader minimizes

```
H(x)=d_0+d^T x+sum_i c_i z_i*(x),                                (2)
```

with arbitrary signed rational coefficients. There are no additional upper
constraints involving the response. An infeasible follower makes that
leader infeasible.

**Theorem.** For fixed `r`, one can decide whether a feasible leader
exists and, if so, return a rational feasible leader `xhat` with

```
H(xhat)<=OPT+2^(-B)
```

and a rational estimate of `OPT` with absolute error at most `2^(-B)`, in
time polynomial in the rational input bit length, numerical `P`, and the
requested accuracy count `B>=1`. The rational leader has polynomial bit
length. Coefficient magnitudes, minimum positive resource weights, and
marginal curvature have no separate numerical dependence in the running
time. Exact common-field output for all follower coordinates is not claimed.

The power follower `g_i(z)=z^(p_i)` is a special case. All resource
coefficients are fixed with respect to the leader; this proof does not
cover `w_i(x)`. Its sharp residual identity proves a single equality. A separate
[fixed-resource extension](../notes/bilevel-fixed-resource-accuracy-bit-algorithm.md) treats fixed numbers of inequality and equality rows using a different error bound.

## 2. Exact leader feasibility and a bounded scalar multiplier

Define

```
b_min=sum_i min(w_i,0),   b_max=sum_i max(w_i,0),
W=sum_i |w_i|=b_max-b_min.
```

The image of the unit box under `z -> sum_i w_i z_i` is exactly
`[b_min,b_max]`: its two endpoints occur at the appropriate Boolean box
vertices, and their line segment realizes every intermediate value.
Consequently the feasible leaders form the rational polytope

```
X'=X intersect {b_min<=b(x)<=b_max}.                              (3)
```

Decide its emptiness by rational linear programming. If `W=0`, (3) is the
condition `b(x)=0`, and the follower is diagonal. The reviewed inverse
approximation lemma and the diagonal power algorithm, with its scalar
approximation step replaced by that lemma, prove the theorem directly.
Henceforth assume `W>0` and put

```
w_min=min_(i:w_i!=0) |w_i|>0.
```

Let `h_i(t)` be the clipped inverse of `g_i`: zero for `t<=0`, one for
`t>=G_i`, and `g_i^(-1)(t)` in between. For a scalar multiplier `lambda`, put

```
q_i(x,lambda)=h_i(ell_i(x)-lambda*w_i),
R(x,lambda)=sum_i w_i q_i(x,lambda).                              (4)
```

This `q` is the unique minimizer of the box Lagrangian
`F_x(z)+lambda*(sum_i w_i z_i-b(x))`. Obtain rational lower and upper
bounds `ell_i^-`, `ell_i^+` on each affine `ell_i` over the whole unit cube.
For every nonzero `w_i`, collect the four rational numbers

```
ell_i^-/w_i, ell_i^+/w_i,
(ell_i^--G_i)/w_i, (ell_i^+-G_i)/w_i.
```

Let `L` and `U` be the minimum and maximum of all these numbers. They have
polynomial bit length and `L<U`. At `lambda=L`, each positive-weight
coordinate is one and each negative-weight coordinate is zero. At
`lambda=U`, their roles reverse. Thus, for every `x in X'`,

```
R(x,L)=b_max,   R(x,U)=b_min.
```

The continuous function `R(x,lambda)` is nonincreasing, because each term
`w_i h_i(ell_i-lambda*w_i)` is nonincreasing. There is therefore a
`lambda* in [L,U]` with `R(x,lambda*)=b(x)`.
Its response is the follower optimum: Lagrangian minimization gives
`F_x(q)<=F_x(z)` for every resource-feasible `z`. This proof requires no
constraint qualification, including at endpoint resources or degenerate
feasible faces. All balancing multipliers produce the same response by
strict convexity.

Use the bounded parameter

```
lambda=L+(U-L)theta,   0<=theta<=1.                              (5)
```

Every inverse argument in (4) is now rational affine in the fixed number
`r+1` of variables `(x,theta)`.

The true response is continuous on `X'`. Indeed, for any convergent sequence
of feasible leaders, choose balancing multipliers in `[L,U]`, extract a
convergent subsequence, and use continuity of (4) and the balance equation.
Every resulting response limit is the unique optimum at the limiting
leader. Compactness then gives continuity and attainment of (2).

## 3. An exact balance-to-response identity

Fix a feasible leader `x` and any balancing multiplier `lambda*`. For any
`lambda`, monotonicity makes all nonzero terms

```
w_i [q_i(x,lambda)-q_i(x,lambda*)]
```

have the same weak sign. A zero-weight coordinate has the same response
at both multipliers. It follows exactly that

```
sum_i |w_i| |q_i(x,lambda)-z_i*(x)|
  = |R(x,lambda)-b(x)|.                                         (6)
```

In particular, with `c_max=max_i |c_i|`,

```
|sum_i c_i [q_i(x,lambda)-z_i*(x)]|
  <= (c_max/w_min) |R(x,lambda)-b(x)|.                           (7)
```

Zero-weight coordinates contribute zero to this difference. This estimate
has no derivative or strong-convexity constant. Signed resource coefficients
cause no cancellation in (6), since the sign reversal in the coordinate
response is accompanied by the sign of `w_i`.

## 4. Piecewise rational polynomial approximation in fixed dimension

Write `epsilon=2^(-B)`, and put

```
A=sum_i |c_i|,   C=c_max*W/w_min,
eta=epsilon/[32(1+A+C)].                                        (8)
```

If `A=0`, solve the leader LP over `X'` exactly instead. Otherwise `eta<1/2`,
and its encoding and `log(1/eta)` are polynomial in input length and `B`.
Apply the reviewed [positive polynomial inverse lemma](../notes/certified-positive-polynomial-inverse-approximation.md)
to each `h_i`, at uniform absolute tolerance `eta`. It constructs polynomially
many rational breakpoints and polynomial branches, of degree
`O(log(1/eta))`, with polynomial coefficient bit length, in time polynomial
in input length, `P`, and `log(1/eta)`.

Pull every breakpoint back through the affine argument in (4)-(5), and
arrange these hyperplanes inside `X' times [0,1]`. Because `r+1` is fixed,
there are polynomially many rational cells. Include lower-dimensional
cells and use their closures. On each closed cell `Q`, choose a branch
`P_i(x,theta)` valid throughout that cell; at common endpoints either
adjacent branch has the required uniform error. Thus

```
|P_i(x,theta)-q_i(x,L+(U-L)theta)|<=eta,   (x,theta) in Q.         (9)
```

The functions need not agree exactly across cell boundaries. On `Q`, form

```
H_Q=d_0+d^T x+sum_i c_i P_i,
T_Q=sum_i w_i P_i-b(x).                                         (10)
```

All are rational polynomials in `r+1` variables, of polynomial degree and
bit length. Optimize `H_Q` over the compact semialgebraic set

```
(x,theta) in Q,   |T_Q(x,theta)|<=W*eta.                          (11)
```

Discard empty sets. At a true optimal leader, a balancing multiplier
exists; (9) makes its approximation feasible in (11) in an appropriate
cell. Hence at least one set is nonempty. Exact fixed-dimensional
real-algebraic optimization and comparison, as in the reviewed diagonal
algorithm, return a winning algebraic point `v*=(x*,theta*)` and cell `Q`
whose polynomial value satisfies

```
H_Q(v*)<=OPT+A*eta.                                             (12)
```

For explicit quantifier accounting, express membership in (11) by a
quantifier-free formula `E_Q(v)`. The minimizing set is
`E_Q(v) and not exists u [E_Q(u) and H_Q(u)<H_Q(v)]`.
There are `2(r+1)` total variables. Quantifier elimination and sampling
therefore have polynomial degree and bit bounds; the sampled coordinates
lie in one polynomial-degree algebraic field. Pairwise comparisons of
candidate values require only products of two such degrees, rather than
a field containing all true follower roots.

## 5. Rational leader recovery with one additional residual allowance

The set (11) may have no rational point. We preserve membership only in the
underlying rational polytope `Q`, and allow one more `W*eta` of polynomial
balance error. This is enough for (7).

For a rational polynomial `S(v)=sum_nu a_nu v^nu` on the unit cube, set

```
L(S)=max{1, sum_nu |a_nu| |nu|}.
```

This rational number has polynomial bit length and bounds the sum of
absolute partial derivatives. Thus `|S(v)-S(v')|<=L(S)||v-v'||_infinity`.
Let `L_H=L(H_Q)` and `L_T=L(T_Q)`. Choose a positive rational

```
delta<=min{1, epsilon/(8 L_H), W*eta/L_T}.                        (13)
```

The vertex-simplex rounding construction in the diagonal theorem returns
a rational `vhat=(xhat,thetahat) in Q` with
`||vhat-v*||_infinity<=delta`, in polynomial time and bit length.
For completeness, enumerate the vertices of the bounded rational polytope
`Q`, find a simplex of at most `r+2` vertices containing `v*`, and express
`v*` in barycentric coordinates. Round all but one coordinate down on a
fine rational grid, assigning the remainder to the last vertex. The
result remains in the same simplex and hence satisfies every exact
rational equality of a lower-dimensional cell. All algebraic comparisons
and barycentric calculations remain in the sampled field; the required
grid denominator has bit length polynomial in `log(1/delta)`.

Now `xhat in X'` is an exactly feasible leader, and

```
H_Q(vhat)<=OPT+A*eta+epsilon/8,
|T_Q(vhat)|<=2W*eta.                                             (14)
```

The true box-Lagrangian response at `vhat` has resource residual at most
`3W*eta` by (9). Applying (7), and then (9) to the upper objective, gives

```
|H(xhat)-H_Q(vhat)|<=A*eta+3C*eta.                               (15)
```

Consequently

```
H(xhat)<=OPT+epsilon/8+(2A+3C)*eta
        <=OPT+7epsilon/32 < OPT+epsilon.                         (16)
```

The rational number `H_Q(vhat)` itself estimates the optimum. From (14)
and `H(xhat)>=OPT`, (15) yields

```
-(A+3C)*eta <= H_Q(vhat)-OPT <= A*eta+epsilon/8.
```

In particular its absolute error is at most `5epsilon/32<epsilon`.
No exact resource-balancing multiplier or root-sum comparison is needed
at the output stage. The returned rational leader is feasible even though
the auxiliary approximate response generally is not exactly balanced.

## 6. Complexity and limits

The inverse lemma has `O(P^2 log(1/eta))` branches per coordinate.
The arrangement dimension is `r+1`, independent of the number of follower
coordinates. Its number of cells, the dense polynomial expansions, and
the fixed-dimensional quantifier-elimination computations are polynomial
for fixed `r`. All rational thresholds, multiplier bounds, normalized
weights, gradient bounds, and rounding denominators have polynomial bit
length. A small `w_min`, tiny marginal coefficients, or a large multiplier
interval increase the logarithmic precision requirement, not a separate
inverse-weight or condition-number factor.

The algorithm is polynomial in numerical `P`. The sparse binary-power
rational-output obstruction in the diagonal theorem still applies: add a
zero-weight resource equality `0=0`, or add an independent resource-fixed
coordinate if a nonzero row is required. Exact sum-of-square-roots
comparison also remains embedded in the diagonal special case. The
result concerns additive approximation with rational feasible leader
output, not exact algebraic-sum optimization.

The proof relies on a single multiplier and the no-cancellation identity
(6). With two resource rows the coordinate changes need not have a common
signed balance direction; neither (6) nor this proof transfers directly.

## 7. Source and novelty status

This is a candidate combination of scalar separable convex resource
allocation, certified inverse approximation, and fixed-dimensional
polynomial optimization. None of those general methods is claimed as
new. The proposed contribution is the explicit polynomial accuracy-bit
bound for signed upper objectives of many algebraic resource-coupled
responses, with exact rational leader feasibility. The [focused primary-source comparison](../notes/bilevel-resource-accuracy-bit-novelty.md) found no matching combined theorem in the checked literature, while crediting established resource-allocation algorithms and accuracy-bit convex optimization. This is bounded evidence rather than proof of priority. The existing
[diagonal source audit](../notes/bilevel-bounded-power-accuracy-bit-novelty.md)
credits prior approximation of algebraic sums; it does not establish
priority for the resource-coupled extension.

## 8. Exact diagnostic

[Signed balance checker](../code/bilevel_one_resource/check_signed_balance.py)
passed 7,200 exact rational identity and upper-error certificates across
160 linear-marginal instances. Cases include signed, zero, and tiny
resource weights; endpoint resources; saturated coordinates; and global
multiplier endpoint bounds. The inverse approximation and rational simplex
recovery are separately checked in their reviewed dependencies.

## 9. Arbitrary strictly increasing polynomial marginals

The same theorem holds when each marginal is a rational dense strictly increasing polynomial with arbitrary signed coefficients. Replace a marginal `h_i` by `g_i=h_i-h_i(0)` and its affine coefficient by `ell_i(x)-h_i(0)`, and write `G_i=g_i(1)>0` for the shifted marginal. Replace only the positive-coefficient approximation lemma by the twice-audited [general monotone-polynomial inverse lemma](../notes/certified-monotone-polynomial-inverse-approximation.md). Its rational branch count, degree, construction time, and coefficient encodings are polynomial in numerical degree, input length, and `log(1/eta)`; the sharper explicit positive-coefficient branch-count estimate is not needed.

Every other step of the proof uses only strict monotonicity and continuity of the clipped inverse: the endpoint multiplier bounds, no-cancellation balance identity, exact leader feasibility, fixed-dimensional algebraic optimizer, and rational recovery all apply unchanged. No derivative lower bound is required, including at interior zeros of the marginal derivative. Equivalently the theorem covers arbitrary dense strictly convex univariate polynomial local follower costs in this one-resource model. This extension's transfer is included in the independent audits of the [fixed-resource theorem](../notes/bilevel-fixed-resource-accuracy-bit-algorithm.md); its original positive-coefficient proof retains the two linked dedicated reviews.
