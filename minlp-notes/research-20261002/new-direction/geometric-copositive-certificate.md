# A sparse geometric-grid certificate for strict copositivity

Date: 2026-10-02. Status: complete derivation, targeted rational checks,
and a [fresh independent review](../reviews/geometric-copositive-certificate-review.md)
finding no substantive gap. No priority claim is made.

A single finite-state dynamic program can certify a positive Euclidean
margin for a sparse homogeneous quadratic on the nonnegative orthant.
The certificate does not assume a growth constant. Under strict
copositivity, a geometric search returns a verified margin within a
factor sixteen of the best margin. The grid size depends on the
coordinate-curvature/margin ratio and graph width, with no requested
accuracy or coefficient-height-dependent refinement count.

The ingredients are independent mean-preserving rounding and ordinary
tree-decomposition DP. The additional point is a relative rounding
correction after homogeneous normalization: it preserves sparsity and
turns an unknown margin into a checkable output. This is a specialized
certificate for a homogeneous quadratic at an orthant corner, not an
extension to arbitrary nonhomogeneous optimality certificates.

## 1. Result and certificate

Let

\[
 Q(x)=x^T A x,\qquad A=A^T\in\mathbb Q^{n\times n},\quad n\ge1.
 \tag{1}
\]

The interaction graph has an edge `ij` when `i != j` and `A_ij != 0`.
Its supplied tree decomposition has `N` bags of size at most `p`.
Let `I` include the matrix and decomposition input lengths. There is no
bound on how many bags contain a variable. First check `A_ii>0` for
every `i`; a failed check gives the vector `e_i` disproving strict
copositivity. Otherwise define

\[
 L=2\max_i A_{ii}>0,\qquad
 g=\min_{x\ge0,\ \|x\|_2=1}Q(x).
 \tag{2}
\]

The algorithm is promised to terminate only when `g>0`. It is not given
`g`. In that case `g<=min_i A_ii<=L/2`; write `kappa=L/g`.

For `delta=2^{-r}`, `r>=1`, set

\[
 \eta=\delta/n,\qquad \sigma=L\delta^2/8.
 \tag{3}
\]

Construct the shared grid by starting with `0,eta`, multiplying each
positive node by `1+delta`, and clipping the last step to `1`. Include
each endpoint only once. Call this grid `G_delta`. Compute exactly

\[
 m_\delta=
 \min_{y\in G_\delta^n,\ \max_i y_i=1}
       \bigl[Q(y)-2\sigma\|y\|_2^2\bigr],
 \qquad b_\delta=m_\delta-\sigma/n.
 \tag{4}
\]

**Certificate theorem.** For every such rational matrix and every
trial, regardless of the sign of `g`,

\[
 Q(x)\ge \sigma\|x\|_2^2+b_\delta\|x\|_\infty^2
             \qquad(x\ge0).
 \tag{5}
\]

Thus `b_delta>0` certifies strict copositivity and the positive
Euclidean margin `sigma`. The certificate consists of the grid,
the DP messages verifying (4), and the positive root quantity
`b_delta`; its verification does not use a growth promise.

**Margin-discovery theorem.** Try `delta=1/2,1/4,1/8,...` and stop at
the first positive `b_delta`. If `g>0`, this terminates and returns

\[
                  g/16\le\sigma<g.                            \tag{6}
\]

The total arithmetic work and certificate size are
`f(p,kappa) poly(n+N)`, excluding input reading. The bit work is
`f_1(p,kappa) poly(I)`, with an absolute polynomial exponent.
The arithmetic state count does not depend on coefficient height or
a requested tolerance. Bit work still depends on the input bit length.
In particular, `L/sigma<=16 kappa` is a trustworthy conditioning bound
that can be supplied to a later method; it is certified by the grid
tables rather than assumed as an input promise.

## 2. Relative rounding bound

Take `x in [0,1]^n` with `max_i x_i=1`. Round each coordinate
independently to the endpoints of its enclosing grid interval, with
probabilities preserving its mean. Write the result as `Y`.
Then `E Y=x`, and `max_i Y_i=1` with probability one, because an
original coordinate equal to one is left unchanged.

For an interval `[a,b]` the scalar variance is
`(x_i-a)(b-x_i)<= (b-a)^2/4`. On the initial interval `[0,eta]`,
therefore, `4 Var(Y_i)<=eta^2`. Every other interval has
`b-a<=delta a`, so

\[
 4\operatorname{Var}(Y_i)\le\delta^2 a^2
                           \le\delta^2\mathbb E Y_i^2.
\]

Summing a bound valid for both kinds of intervals gives

\[
 4\sum_i\operatorname{Var}(Y_i)
       \le\delta^2\mathbb E\|Y\|_2^2+n\eta^2.                 \tag{7}
\]

Put `R(x)=Q(x)-sigma||x||_2^2`. Its `i`th quadratic diagonal
coefficient is `A_ii-sigma<=L/2`. Independence leaves every
off-diagonal expectation unchanged, even when its coefficient is
arbitrarily large. Consequently

\[
 \begin{aligned}
 \mathbb E R(Y)-R(x)
   &=\sum_i(A_{ii}-\sigma)\operatorname{Var}(Y_i)\\
   &\le \frac L2\sum_i\operatorname{Var}(Y_i)\\
   &\le \sigma\mathbb E\|Y\|_2^2+\frac{Ln\eta^2}{8}
    =\sigma\mathbb E\|Y\|_2^2+\frac\sigma n.
 \end{aligned}                                                 \tag{8}
\]

Hence

\[
 R(x)\ge
 \mathbb E[Q(Y)-2\sigma\|Y\|_2^2]-\sigma/n
 \ge b_\delta.                                                  \tag{9}
\]

For an arbitrary nonzero nonnegative vector, apply (9) to
`x/||x||_infinity` and use homogeneity. The zero vector is immediate.
This proves (5). In particular, the grid check cannot produce a false
positive when the strict-growth promise is absent.

## 3. Unknown margin and the factor-sixteen guarantee

Suppose now `Q(x)>=g||x||_2^2` on the orthant, with the optimal
constant `g>0`. Every normalized grid point has `||y||_2^2>=1`.
When `sigma<=g/4`,

\[
 m_\delta\ge g-2\sigma,\qquad
 b_\delta\ge g-(2+1/n)\sigma\ge g/4>0.                         \tag{10}
\]

Thus the search must succeed. Each failed trial halves `delta` and
divides `sigma` by four. If the first successful trial is not the
initial one, its predecessor failed and therefore had `4sigma>g/4`.
This gives `sigma>g/16`. At the initial trial,
`sigma=L/32>=g/16` by (2). Finally (5), `b_delta>0`, and
`||x||_infinity^2>=||x||_2^2/n` show
`g>=sigma+b_delta/n>sigma`. This proves (6).

There are `O(1+log kappa)` trials. The last trial satisfies
`delta^{-1}<=sqrt(2 kappa)`, by (3) and (6). The theorem says nothing
about finite termination when `g=0`. This positivity-only test also
does not decide every noncopositive instance with positive diagonal
entries; Section 7 adds a negative-witness test. A finite failed
positivity trial is simply inconclusive.

## 4. One DP with a two-state flag

The constraint `max_i y_i=1` does not require `n` separate anchored
problems. Root the decomposition. Assign each variable to the bag
nearest the root among bags containing it; connectedness makes that
owner unique. Assign each matrix term to one bag containing all its
variables, and assign `-2sigma y_i^2` to the owner of `i`.

A message from bag `t` is indexed by its separator assignment and
one bit. The bit records whether some variable **owned** in the
subtree has value one. For each bag assignment, form the local bit
from variables owned there and combine it with the child bits by
logical OR. Minimize the sum of local factors and child messages for
each resulting bit. Child messages can be combined one at a time
using a two-state OR convolution; there is no exponential factor
in the number of children. The root entry with bit one is (4).

Let `K=|G_delta|`. Exact evaluation and DP take

\[
 O\!\left(\operatorname{poly}(p)
       \sum_t(1+\#\operatorname{children}(t))K^{|B_t|}\right)
       =\operatorname{poly}(p)O(NK^p)                         \tag{11}
\]

arithmetic operations, plus reading and assigning factors. Absent
message states have value positive infinity. Store the messages and,
if desired, minimizing choices. A verifier recomputes the same local
Bellman minima, checks the grid construction and root inequality,
and applies the proved rounding bound. This verification is a finite
rational calculation; it requires neither `g` nor an SOS identity.

Since `log(1+delta)>=delta/2` for these trials,

\[
 K=O\!\left(\delta^{-1}\log(2n/\delta)\right)
   =O\!\left(\sqrt\kappa\log(2n\sqrt\kappa)\right)             \tag{12}
\]

at the last trial. All previous trials have no larger bound. Powers
of `log(2n)` can be absorbed into a parameter-dependent constant
times `n`: for example `t^p e^{-t}<=p^p e^{-p}` with
`t=log(2n)`. Equations (11)--(12) and the trial count therefore give
the asserted `f(p,kappa) poly(n+N)` arithmetic bound. In particular,
this is fixed-parameter tractability in bag size and conditioning,
not merely a polynomial whose exponent is the bag size.

## 5. Rational size

At trial `delta=2^{-r}`, each unclipped positive grid node is

\[
             \frac{(2^r+1)^j}{n\,2^{r(j+1)}}.                 \tag{13}
\]

All nodes, including zero and one, have a common denominator dividing
`n 2^{r(K+1)}`. Since the nodes are in `[0,1]`, their numerator and
denominator lengths are `O(log n+rK)`. At the successful trial,
`r=O(1+log kappa)` and (12) bounds `K`.

Take a common denominator for the input matrix entries; its bit length
is at most their total encoding length. Together with (3) and (13),
this gives a common denominator for every finite local-table entry.
Every finite message is a sum of a subset of those assigned objective
terms evaluated at grid values. Additions and minima do not multiply
denominators across bags. Magnitudes and bit lengths are bounded by
the input coefficient lengths, `O(log n+log N)`, and a polynomial
in `rK`. Exact comparisons, stored messages, grid generation, and
certificate verification consequently fit `f_1(p,kappa) poly(I)`.

This is not a claim that coefficient bit lengths have no cost. The
claim is that they do not dictate the number of grid states or
refinement trials; the numerical conditioning may itself be large.

## 6. Scope and relation to earlier certificates

The [pruned coordinate-grid theorem](pruned-coordinate-grid.md) already
uses corrected rounding and tree DP for conditioned global optimization.
The present specialization removes the need for a target accuracy,
moving centers, min-marginal pruning, or rational optimum recovery.
Homogeneity converts one normalized shell into a global certificate,
and the relative correction yields a verified growth constant. The DP
and rounding principles themselves are not claimed as new.

The [box-preordering obstruction](box-preordering-growth-obstruction.md)
gives a five-variable matrix with margin `g=1/5`, curvature `L=12/5`,
and no finite unmultiplied box-preordering certificate. Its connected
chains retain bounded conditioning and bag size five. They fall within
the theorem here. There is no conflict: the DP-plus-rounding proof is
a different certificate family.

The same obstruction note gives a classical Pólya-style escape:
`(sum_i x_i)^{d-2} Q` has nonnegative coefficients for
`d>=n max_i A_ii/g`. That is already a finite certificate of strict
copositivity, and an FPT bound when the entire dimension is the
parameter. Its dense coefficient expansion does not by itself give
the present dependence on **interaction width** for growing `n`.
No impossibility result for sparse multiplier certificates is asserted.

The [focused prior-art audit](../prior-art/box-quadratic-jet-certificate-prior.md)
compares Pólya and Bernstein certificates, Bienstock--Muñoz treewidth
LP approximations, and sparse copositive Moment-SOS relaxations. The
relevant distinction from generic discretized treewidth LPs is the
`L/g` relative resolution and verified margin, not finite-state DP or
positivity certification alone. This note does
not claim a complexity result for arbitrary tangent cones, mixed
constraints, general boundary-copositive forms, or nonhomogeneous optima.

## 7. Optional negative-witness search

The same grid also permits a two-sided search when `g!=0`. Use
`L=2 max_i max(A_ii,0)>0`, omitting the preliminary rejection for a
zero diagonal. At each trial run a second DP on the same normalized
grid, minimizing the uncorrected `Q(y)`. A negative minimum and its
backtracked rational point are an independently checkable
noncopositivity witness. The corrected positive test remains sound.

For a positive grid interval the sharper inequality
`4 Var(Y_i)<=delta^2 x_i^2` holds, since its lower endpoint is at
most `x_i`. Thus the same independent rounding gives

\[
 \mathbb E Q(Y)\le Q(x)+\sigma\|x\|_2^2+\sigma/n.
 \tag{14}
\]

If `g<0`, take a minimizing unit vector in (2) and rescale it so
`max_i x_i=1`. Homogeneity gives `Q(x)=g||x||_2^2`. When
`sigma<=|g|/4`, the coefficient `g+sigma` is negative and
`||x||_2^2>=1`, so

\[
 \mathbb E Q(Y)\le(g+\sigma)\|x\|_2^2+\sigma/n
             \le g+\sigma(1+1/n)\le g/2<0.                  \tag{15}
\]

Some normalized grid point therefore has negative objective. The
positive case is already covered by Section 3. The two-DP search
terminates for `g!=0` in
`f(p,max(1,L/|g|)) poly(I)` bit work, and outputs either the verified
positive margin or a rational negative witness. The trial and state
bounds follow from the same threshold `sigma<=|g|/4`, with the
initial trial handled separately when `L/|g|` is small. There is
still no general termination assertion at `g=0`.

If `L=0`, the objective is concave in each coordinate separately.
Independent endpoint rounding to `{0,1}` cannot increase its
expectation. The normalized endpoint DP therefore decides
copositivity exactly by homogeneity: a negative endpoint is a
witness, while a nonnegative minimum certifies `Q>=0`. Strict
copositivity is impossible in this case. A zero diagonal alone must
not be reported as a negative witness; it disproves strict
copositivity but does not disprove copositivity.

## 8. Verification

The targeted command

```
python3 -B research-20261002/new-direction/check_geometric_copositive.py
```

passed six positive fixtures, ten margin-search trials, 39,908 exact
bag assignments, ten comparisons against direct normalized-grid
enumeration, 1,330 rational interval-variance checks, and six checks
on a boundary-copositive or negative quadratic. The fixtures include
a branching decomposition, a path, a cross coefficient of `10^50`,
a diagonal margin of `1/1024`, and the five-variable non-SPN example.
The small diagonal margin requires five trials and returns `sigma=g/4`.
An additional narrow negative cone takes four uncorrected-grid trials
before producing a rational negative witness. All four minima match
direct enumeration, and the witness objective is checked exactly.

For the non-SPN example the first trial has eight grid nodes and gives

\[
 \delta=\tfrac12,\qquad \sigma=\tfrac3{40},\qquad
 b_\delta=\tfrac{15561}{256000}>0.                             \tag{16}
\]

The exact DP messages therefore certify
`Q(x)>=(3/40)||x||_2^2+(15561/256000)||x||_infinity^2` on the
nonnegative orthant, without a finite unmultiplied box-preordering
identity. These finite diagnostics test the implementation and
specific algebraic inequalities; the proofs above establish the
general statements. The checker is not a production solver.

The [independent review](../reviews/geometric-copositive-certificate-review.md)
checked the full written argument, including the signed-margin
extension and rational size bound, and found no substantive gap. It
inspected the diagnostic source and explicitly records those runs as
author-run evidence. No project-wide verification or CI inspection
was performed. Scoped whitespace, display-math/fence balance, and
local Markdown-reference checks passed for the note and its checker.
