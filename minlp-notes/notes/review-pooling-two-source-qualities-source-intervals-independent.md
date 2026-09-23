# Independent audit: two source qualities with source supply intervals

Date: 2026-09-05. Reviewer: `close_pooling/interval_proof`.

**Verdict: PASS.** This audit covers Sections 1–6 of the
[candidate](pooling-two-source-qualities-convex-feasibility.md), including
arbitrary finite source supply intervals, positive feed lower bounds,
restrictive common pool upper capacity, multiple conserved attributes
with two distinct full source vectors, and the optional signed outlet
resource rows with nonnegative right-hand sides. No mathematical defect
was found. The conclusion is exact polynomial bit-time feasibility and
construction of a rational original feasible flow of polynomial encoding
length. It does not include general economic optimization or positive
outlet/common-pool lower bounds.

This was a separate full derivation and audit. I read the earlier reviews
to identify their scope, then checked the physical equations, convex
reduction, exact algorithm, and witness bounds directly. The verdict does
not establish novelty.

## Physical equivalence with variable source consumption

Normalize the two distinct source qualities to zero and one. Positive
product demands require a quality in that interval. For a zero-demand
product, nonnegative incoming flows must all vanish and its quality value
is immaterial. Missing feed or outlet arcs retain zero-flow bounds.

For an interior pool quality `q`, write `gamma_i=-q` for class zero and
`gamma_i=1-q` for class one. Both factors are nonzero and have known
sign. Multiplying supply, feed, and bypass intervals by their respective
factors therefore produces exactly affine intervals, with order reversed
in class zero. Positive feed lower bounds introduce no new nonlinearity.

Let `A_i` denote actual source consumption. The scaled equation
`t_i=h_i+sum_j w_ij` is equivalent to
`A_i=y_i+sum_j z_ij`. Exact product contracts determine
`A_0=sum_j b_j(1-B_j)` and `A_1=sum_j b_j B_j`; these are class totals,
not individual source contracts. The proposed two class equations are
exactly equivalent to `sum_class_0 A_i=A_0` and
`sum_class_1 A_i=A_1` after division by their nonzero factors.

At each product, eliminating its two bypass-class totals from mass and
quality conservation gives

```
W_0j+W_1j=b_j(B_j-q),
W_0j=q*b_j*(B_j-1)+q*(1-q)*v_j.
```

These identities use no restriction on the number or topology of bypass
arcs. They also hold with an empty bypass class. Since `q*(1-q)>0`, the
affine lower and concave quadratic upper bounds on `W_0j` are exactly the
physical interval `0<=v_j<=U_j`.

For reverse recovery, divide `t_i,h_i,w_ij` by `gamma_i` and recover
`v_j=b_j-sum_i z_ij`. All local bounds and conservation equations hold.
The class totals give total source consumption `sum_j b_j`; subtraction
of total bypass flow proves actual pool mass conservation. Independently,

```
sum_i h_i
 = -q*A_0+(1-q)*A_1-sum_j b_j(B_j-q)
 = 0.
```

This is the normalized physical pool quality balance
`sum_class_1 y_i=q*sum_i y_i`. Thus the added class equations replace
exact individual supply contracts without dropping either pool balance.
At zero throughput, nonnegativity makes every pool intake and outlet
zero. No division by throughput is required.

The exact-source version follows as the special case of singleton supply
intervals. Its preliminary two total checks are necessary; with variable
source supplies those checks are replaced by the two scaled class rows.

## Shared convex auxiliary and additional upper bounds

Summing the product identity gives the common pool upper-capacity row.
More generally, for any rational coefficients `alpha_j`, the row
`sum_j alpha_j*v_j<=U` becomes

```
sum_j alpha_j*W_0j
 <= q*sum_j alpha_j*b_j*(B_j-1)+U*(q-q^2).
```

The signs of the `alpha_j` are irrelevant to this identity. The relevant
sign is `U>=0`: replacing `q^2` by `r>=q^2` tightens its right-hand side.
This proves the optional resource extension, including restrictive common
pool capacity, using the same auxiliary `r` as every outlet upper bound.

Every physical interior point extends with `r=q^2`. Conversely, every
point in the proposed linear polytope satisfying `q^2-r<=0` satisfies all
original upper bounds. The restriction `r<=1` removes no physical point.
The new `t,h` variables and all `w` variables have finite bounds from the
given rational intervals. Hence the extended linear feasible set is a
rational compact polytope of polynomial description size. The only
nonlinear constraint is a sublevel set of the rank-one convex quadratic
`F=q^2-r`.

Positive outlet or common pool lower bounds would reverse the required
curvature and are outside this proof. A resource inequality with negative
right-hand side is likewise outside the optional extension as stated.

## Exact decision and rational recovery

The original physical LPs at `q=0,1` must be checked separately, retaining
supply intervals and every resource row. At fixed quality both pool
balances and all product equations are linear. The singular transformed
endpoint equations are not used as physical certificates.

The margin LP over the compact linear polytope decides whether it has
any point with `0<q<1`. A positive optimum supplies a rational point `p`
of polynomial encoding length, without needing quadratic feasibility.

I opened the original Kozlov–Tarasov–Khachiyan
[1980 paper, printed pages 1320–1321](https://www.mathnet.ru/php/getFT.phtml?jrnid=zvmmf&option_lang=eng&paperid=5189&what=fullt).
It states a polynomial binary-time algorithm that returns the exact
convex quadratic optimum and an attaining point. Its active-system
determinant argument gives rational coordinate and value bounds. Clearing
the present rational input denominators has polynomial bit cost. This
supports the exact QP primitive used here; generic exact SOCP feasibility
is not needed.

For the exact minimum `m` of `F`, all three cases are correct:

- `m>0` excludes the quadratic sublevel set.
- If `m=0`, two minimizers with different qualities would have a midpoint
  whose objective is `-(q_1-q_2)^2/4<0`. Thus every minimizer has the same
  `q`, and checking the rational optimizer's quality decides whether an
  interior quadratic-feasible point exists.
- If `m=-rho<0`, take
  `lambda=rho/[2*(rho+1)]`. The point `(1-lambda)*x*+lambda*p` has interior
  quality and, because `F(p)<=1`, objective at most `-rho/2`. It is a
  rational physical certificate after reverse recovery.

These operations preserve polynomial encoding length. Division by `q`
or `1-q` also does: the denominators are nonzero rational numbers with
polynomial encodings, even when their magnitudes are very small. No
unstated positive feasibility margin is used. Endpoint certificates are
rational LP solutions.

With several attributes and two distinct full source vectors, select one
coordinate in which the vectors differ. Its rational affine coordinate
parameterizes their entire line. Check every other coordinate of each
positive-demand product, and reject points outside the source segment.
Each remaining attribute equation is an affine combination of scalar
quality and mass conservation. This proves the vector extension with
polynomial rational arithmetic. Zero-demand product vectors impose no
restriction.

## Exact arithmetic stress checks

I ran an independent standard-library `Fraction` check, with deterministic
seed `310905`, on 240 constructed rational networks with variable source
consumption and arbitrary sparse or dense bypass patterns. The checks
used interior qualities as small as `2^-80` and as large as `1-2^-80`.
They verified 1,222 source conservation/scaled interval rows, 913 output
identities and reverse recoveries, 480 common-capacity or signed resource
rows, and 2,739 conserved-vector component equations. Cases included 243
zero-demand products, 35 inactive pools, and 1,051 positive feed lower
bounds. All passed exactly.

The lifted points used `r=q^2+q*(1-q)/4`, exercising the soundness direction
with strict auxiliary slack, not only the equality construction. Chosen
upper bounds made both the individual and aggregate strengthened rows
feasible. Source intervals were non-singleton. The arithmetic checks
confirm signs, balances, and recovery across these cases; the proof above
establishes the general decision algorithm and its bit complexity.

The candidate's remaining “audits required” statements can now be updated
by its author. The separate source assessment must still govern any
priority claim.
