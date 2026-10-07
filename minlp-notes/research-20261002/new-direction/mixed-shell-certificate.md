# Geometric shell certificates for a proposed mixed-box optimum

Date: 2026-10-02. Status: derivation, targeted exact checks, and fresh
independent review complete. No priority claim is made.

Integer feasibility prevents the continuous radial argument from extending
directly to mixed boxes. A finite family of physical shells avoids that
step. Each shell has a small geometric grid of feasible points, and
mean-preserving rounding gives a sound growth certificate. Below the
smallest shell, integer coordinates stay fixed and a continuous radial
inequality completes the certificate near the proposed point.

The shell construction has fixed-parameter bit complexity in interaction
bag size and curvature divided by growth. Its number of shells depends on
the encoded domain widths and lattice spacings. This is not the stronger
coefficient-height-independent arithmetic bound of the homogeneous
certificate. The entire argument uses one physical Euclidean metric.

## 1. Model and continuous first-order checks

Let `X` be a rational bounded box in `R^n`. Some coordinates are continuous;
each other coordinate belongs to a rational lattice `alpha_i+h_i Z`, with
`h_i>0`. Native integer variables have `h_i=1`. Replace lattice-coordinate
box endpoints by the first and last feasible lattice labels. Remove fixed
coordinates. Let

\[
 F(x)=x^TAx+b^Tx+c,\qquad A=A^T\in\mathbb Q^{n\times n},
 \qquad s\in X
 \tag{1}
\]

with `s` feasible for the lattice restrictions. The supplied decomposition
of the quadratic interaction graph has `N` bags of size at most `p`.
The encoding length `I` includes the objective, box, lattices, proposed
point, decomposition, and the supplied rational curvature bound

\[
                     L>0,\qquad A_{ii}\le L/2\quad\text{for every }i.
 \tag{2}
\]

The case `A_ii<=0` for every coordinate also has the simpler endpoint
certificate in Section 5, which needs no positive curvature scale.

All distances and curvature bounds below use these physical coordinates.
The best full-domain Euclidean growth constant, when positive, is

\[
 g=\inf_{x\in X,\ x\ne s}
       \frac{F(x)-F(s)}{\|x-s\|_2^2}>0.
 \tag{3}
\]

The certificate verifier does not receive or assume `g`. Check feasibility
of `s` first. If removal of fixed coordinates leaves a singleton, there is
no optimization problem to certify. Otherwise define `c_s=2As+b` and check

\[
 \varepsilon(c_s)_i\ge0
 \quad\text{for every continuous coordinate }i
 \text{ and available sign }\varepsilon\in\{-1,1\}.
 \tag{4}
\]

Failure gives a feasible continuous descent direction with all lattice
coordinates fixed, so `s` is not a local minimum. No first-order sign
condition is imposed on lattice coordinates. Condition (4) is vacuous
for a pure lattice problem.

This is the only radial ingredient borrowed from the
[continuous box-point certificate](geometric-box-point-certificate.md).
The coordinate normalization in that note is not used here.

## 2. Physical shells and grids

Let `w_i^+` and `w_i^-` be the positive and negative distances from `s_i`
to the effective coordinate endpoints, retaining only positive distances.
Define

\[
 r_0=\min\left(
       \{h_i/2:i\text{ lattice}\}
       \cup\{w_i^\varepsilon:i\text{ continuous},\ w_i^\varepsilon>0\}
       \right)>0,\qquad
 D=\max_{x\in X}\|x-s\|_\infty,\qquad
 J=\lfloor\log_2(D/r_0)\rfloor.
 \tag{5}
\]

After removing fixed coordinates the defining union is nonempty and
`D>=r_0`. For `j=0,...,J`, set `S_j=2^j r_0` and define

\[
 X_j=\{x\in X:S_j\le\|x-s\|_\infty\le2S_j\}.
 \tag{6}
\]

These shells cover all feasible points at distance at least `r_0` from
`s`. Every remaining feasible point has its lattice coordinates fixed at
their proposed values. The choice of `r_0` also permits scaling any such
nonzero displacement out to the bottom shell along its continuous ray.

At a trial `delta=2^{-r}`, `r>=1`, set

\[
                         \sigma=L\delta^2/8.
 \tag{7}
\]

For a shell radius `S`, construct signed coordinate grids in displacement
coordinates `d=x-s`. Treat each available sign separately and include
zero only once. Let `U` be that side's maximum feasible displacement after
intersecting with `[0,2S]`. A side with `U=0` needs no positive label.

* For a continuous coordinate, start at
  `a_0=min{U,delta S/(2n)}`, repeatedly multiply a positive label by
  `1+delta`, and clip the last step to `U`. Include `S` if `S<=U`.
* For lattice spacing `h_i`, first replace the side bound by its largest
  lattice displacement `U<=2S`. Start with
  `a_0=min{U,h_i ceil(delta S/(2n h_i))}`. After a positive label `a`, use
  `min{U,a+h_i max{1,floor(delta a/h_i)}}`. Include
  `h_i ceil(S/h_i)` if that threshold is at most `U`.

The additional threshold label may split a grid interval. It never
increases the interval width. All lattice labels are feasible lattice
displacements; no artificial fractional labels are introduced there.
Translate back by `s` to obtain the product grid `G_{S,delta}`.

## 3. A shell certificate independent of the growth promise

Compute exactly

\[
 m_{S,\delta}=
 \min_{y\in G_{S,\delta},\ \|y-s\|_\infty\ge S}
    \bigl[F(y)-F(s)-2\sigma\|y-s\|_2^2\bigr].
 \tag{8}
\]

An empty minimum is positive infinity. For every input satisfying (1)--(2),
whether or not `s` is optimal,

\[
 F(x)-F(s)-\sigma\|x-s\|_2^2
       \ge m_{S,\delta}-\sigma S^2/n
       \qquad(x\in X_j).
 \tag{9}
\]

Consequently, the finite rational checks

\[
                  m_{S_j,\delta}\ge\sigma S_j^2/n
                         \quad(j=0,\ldots,J)
 \tag{10}
\]

certify growth with margin `sigma` on the union of the shells. Together
with (4), they prove unique global optimality and the verified bound

\[
 F(x)-F(s)\ge\sigma\|x-s\|_2^2
                           \qquad(x\in X).
 \tag{11}
\]

To cover the remaining region, take a nonzero feasible displacement `d`
with `rho=||d||_infinity<r_0`. Its lattice coordinates are zero. Set
`v=(r_0/rho)d` and `t=rho/r_0`. Every coordinate of `v` uses the same
available continuous sign as `d`, and has absolute value at most `r_0`,
so `s+v` is feasible and belongs to the bottom shell. By (4),
`c_s^T v>=0`. Quadratic expansion therefore gives

\[
 \begin{aligned}
 F(s+tv)-F(s)
 &=t\,c_s^Tv+t^2v^TAv\\
 &\ge t^2\bigl(F(s+v)-F(s)\bigr)
 \ge\sigma\|tv\|_2^2.
 \end{aligned}
\]

This proves (11) near `s`; the point `s` itself is immediate.

To prove (9), round each coordinate of an arbitrary `x in X_j`
independently to its enclosing grid endpoints while preserving its mean.
Write the rounded point as `Y` and its displacement as `Z=Y-s`. Threshold
labels ensure that a coordinate originally having absolute displacement
at least `S` still has absolute displacement at least `S` after rounding.
Thus `Y` is feasible and satisfies the constraint in (8) almost surely.

For every coordinate,

\[
 4\operatorname{Var}(Y_i)
       \le\delta^2\mathbb E Z_i^2+\delta^2S^2/n^2.
 \tag{12}
\]

For continuous coordinates the initial gap has width at most
`delta S/(2n)`, and subsequent gaps have width at most `delta a`, where
`a` is the smaller absolute displacement. For lattice coordinates a gap
of one lattice step has zero variance at every feasible target. If the
initial gap has at least two steps, its width is at most `delta S/n`:
`ceil(t)>=2` implies `ceil(t)<=2t`. Every later gap of at least two steps
has width at most `delta a`. Splitting intervals at threshold labels
preserves these bounds. Finally use
`4 Var(Y_i)<=gap_width^2` and `a^2<=E Z_i^2`.

Let `R(x)=F(x)-F(s)-sigma||x-s||_2^2`. Independence preserves the means
of the linear and off-diagonal terms, so (2) and (12) give

\[
 \begin{aligned}
 \mathbb E R(Y)-R(x)
 &=\sum_i(A_{ii}-\sigma)\operatorname{Var}(Y_i)\\
 &\le\frac L2\sum_i\operatorname{Var}(Y_i)\\
 &\le\sigma\mathbb E\|Y-s\|_2^2+\sigma S^2/n.
 \end{aligned}
 \tag{13}
\]

Rearranging proves (9). No feasible ray, stationarity condition in an
integer coordinate, or assumed growth constant enters the shell proof.
The radial step used only in the inner region changes continuous
coordinates alone.

## 4. Discovery, dynamic programming, and bit complexity

If (3) holds, every grid point in (8) satisfies

\[
 F(y)-F(s)-2\sigma\|y-s\|_2^2
      \ge(g-2\sigma)\|y-s\|_2^2.
\]

In particular, all checks (10) hold whenever `sigma<=g/3`. Trying
`delta=1/2,1/4,...` and stopping at the first successful shell trial
therefore terminates under (3). It returns

\[
 \sigma\ge\min\{L/32,g/12\},\qquad
 \delta^{-1}\le\max\{2,\sqrt{3L/(2g)}\}.
 \tag{14}
\]

Indeed, the initial margin is `L/32`. At a later first success the
previous margin was `4sigma`, and failure implies `4sigma>g/3`.
There are `O(1+log^+(L/g))` trials. The minimum in (14) is necessary for
this curvature-only initialization: on `z in {0,1}`, the objective
`z^2+Hz` has growth `1+H` but permits `L=2`. The complete soundness result
(11) gives `sigma<=g`. In particular, the returned certified conditioning
satisfies `L/sigma<=max{32,12L/g}`; a constant-factor estimate of `g`
itself is not claimed when `g` is much larger than `L`.

In this bounded mixed-box setting, a unique global minimizer necessarily
has `g>0`. To see this, the compact set of feasible points with
`||x-s||_infinity>=r_0` has a strictly positive minimum objective gap.
Dividing that gap by `nD^2` gives positive quadratic growth there.
The continuous first-order conditions hold at the minimizer, so the same
bottom-shell radial argument extends that growth to the inner region.
Thus unique global optimality alone guarantees termination. Without
unique optimality, a finite failed trial is inconclusive; no general
negative-branch termination is claimed.

Every coordinate grid has

\[
               K=O\!\left(\delta^{-1}\log(2n/\delta)\right)
 \tag{15}
\]

labels, independently of `S`, `D`, and the lattice spacings. For a
continuous side the ratio of its maximum label to its initial label is
at most `4n/delta`. For a lattice side there are at most `O(1/delta)`
labels below `2h_i/delta`; afterwards the step is at least `delta a/2`.
The ratio traversed in this latter part is at most `4n/delta`, using
`a_0>=delta S/(2n)` unless the initial label is clipped immediately to
`U`. In that case the side has at most two positive labels after adding
the threshold. Clipping and the single threshold label do not alter the
bound.

For one shell, the ordinary decomposition DP has one Boolean state:
whether some variable owned in the subtree has absolute displacement at
least `S`. Assign each objective term to a bag containing its variables,
assign unary corrections to variable owners, and combine flags by OR.
The root entry with flag true is (8). Child flags can be combined one
child at a time. The work is `poly(p) O(N K^p)` arithmetic operations.

There are `J+1=O(1+log(D/r_0))=O(I)` shells. They may be checked separately,
or within one DP whose messages also contain one shared shell index.
All bags use the same index in a given evaluation; this gives
`(J+1)K^p` assignments per bag, not `(J+1)^p K^p`. This is a direct sum
of shell DPs. A certificate records their messages and the inequalities
(10); a verifier recomputes all Bellman minima.

Set `kappa=L/g`. At the final trial, (14)--(15) give
`K=O(max{1,sqrt(kappa)} log(2n max{1,sqrt(kappa)}))`.
Powers of `log n` can be absorbed into a function of `p` times an
absolute power of `n`, as in the
[homogeneous certificate](geometric-copositive-certificate.md).
Thus the shell search, certificate size, and verification have bit cost

\[
                         f(p,\kappa)\operatorname{poly}(I).
 \tag{16}
\]

For completeness, every shell radius has `O(I)` bits. Lattice labels are
rational multiples of input spacings with integer multipliers bounded
by the encoded domain-to-spacing ratios, so their lengths are `O(I)`.
Continuous geometric labels have length `O(poly(I)+rK)`. Input endpoints,
threshold labels, and all geometric labels admit a common denominator
of that length: include denominators for the input coordinates, lattice
spacings, and computed `r_0`, then geometric denominators contribute only
powers of two and the common factor `2n`. Lattice floors and ceilings
introduce no new denominator. Together with a common denominator for the
objective and `L`, this bounds all local factors and messages by
`poly(I+rK)` bits. Messages add assigned terms; they do not multiply
denominators across bags. Exact arithmetic therefore yields (16).

The preliminary checks and bottom-shell radial argument add only
polynomial work, so (16) applies to the complete certificate. The shell
count may grow with encoded widths or small positive side distances,
even with fixed curvature and growth. This note does not remove that
dependence from arithmetic work. The curvature scale in (2) is not
inflated by axis endpoint values or linear coefficients. That distinction
is necessary: on `[0,1]^2`, for `H,epsilon>0`,

\[
 F(x,y)=H(x+y-2xy)+\epsilon(x^2+y^2)
\]

has unique optimum zero, exact growth `g=epsilon`, and valid curvature
`L=2epsilon`. The first term is nonnegative and vanishes at `(1,1)`,
which proves the exact growth claim. Every nonzero one-coordinate
endpoint increment is `H+epsilon`. Defining a new curvature scale from
these increments would replace conditioning two by an arbitrarily large
number.

## 5. Nonpositive coordinate diagonals

If every `A_ii<=0`, a simpler complete certificate is available. First
check that the proposed point is an endpoint in every unfixed coordinate.
Otherwise its one-coordinate objective restriction is concave, so one
of that coordinate's feasible endpoints gives a different point of no
larger value. Unique optimality is impossible.

For a proposed corner, run the ordinary DP over the two endpoint labels
of each coordinate, with one owned-variable OR flag recording a value
different from the proposed corner. Let

\[
 \Delta=\min_{y\text{ an endpoint assignment},\ y\ne s}
                      \bigl[F(y)-F(s)\bigr].
\]

If `Delta<=0`, its witness disproves unique optimality. If `Delta>0`, let
`w_i>0` be the full width of coordinate `i`. Independently round any
feasible `x` to those endpoints while preserving its mean. Coordinate
concavity gives `F(x)>=E F(Y)`. With `t_i=|x_i-s_i|/w_i`,

\[
 \begin{aligned}
 F(x)-F(s)
 &\ge\Delta\Pr(Y\ne s)
  =\Delta\left(1-\prod_i(1-t_i)\right)\\
 &\ge\Delta\max_i t_i
  \ge\frac{\Delta}{\sum_iw_i^2}\|x-s\|_2^2.
 \end{aligned}
\]

The last step uses `|x_i-s_i|^2=t_i^2 w_i^2<=max_j(t_j) w_i^2`.
Endpoint rounding remains feasible for lattice coordinates. This gives
a sound positive margin and a complete decision for unique optimality
of the proposed point when all diagonals are nonpositive. Its arithmetic
work is `poly(p) O(N 2^p)` and its bit work is `f(p) poly(I)`. This is the
classical endpoint-DP case, not an additional novelty claim.

## 6. Exact obstructions to radial extensions

The shell construction does not use any of the following invalid
extensions of the continuous argument.

First, on `z in {0,...,M}`, with `M>=2`, let

\[
                     q(z)=z^2-z/2.
\]

The proposed point zero has exact growth `g=1/2` and curvature `L=2`,
independently of `M`. Its derivative at zero is negative, and
`q(1/4)=-1/16`. More strongly, the continuous radial inequality fails
even between feasible integer points:

\[
                    q(1)=1/2<(1/2)^2q(2)=3/4.
\]

Second, zero derivative does not repair the issue. On binary coordinates,

\[
                 q(z,w)=z^2+4w^2-(9/2)zw
\]

has values `1,4,1/2` at `(1,0),(0,1),(1,1)`. Thus zero is its unique
binary optimum with exact growth `g=1/4`, curvature `L=8`, and bag size
two. Yet `q(1,9/16)=-17/64`. The full continuous normalized-shell
certificate fails even though the gradient at the candidate is zero.
Disjoint copies retain these constants and bag size as dimension grows.

Third, a natural homogeneous lower bound can lose strict positivity.
For arbitrary `M>=1`, on `{0,...,M}^2`, set

\[
            q(z,w)=z^2+w^2-(9/8)zw-(3/4)z.
\]

Its exact growth is `g=1/16`, with `L=2` and bag size two. To verify this,

\[
 16\bigl(q-(z^2+w^2)/16\bigr)
             =15z^2+15w^2-18zw-12z.
\]

For `z=0` this is nonnegative. For `z=1` it equals
`3(5w-1)(w-1)>=0` at every nonnegative integer `w`. For `z>=2`, use
`-12z>=-6z^2` to lower-bound it by `9(z-w)^2+6w^2`.
Equality holds at `(1,1)`. However, replacing `-(3/4)z` by the valid
integer lower bound `-(3/4)z^2` gives

\[
 H(z,w)=(1/4)z^2+w^2-(9/8)zw,\qquad H(1,9/16)=-17/256.
\]

All three examples become genuinely mixed by adding an independent
continuous variable `u in [0,1]` and the term `u^2`. These examples
obstruct the particular radial or homogeneous reductions; they do not
show impossibility of finite mixed-integer certificates.

The result supplies a direct certificate and verified conditioning for
an already proposed point. It does not find that point or establish a
new conditioned optimization class. The
[focused prior-art comparison](../prior-art/mixed-shell-certificate-prior.md)
records the relevant finite-domain DPs, global quadratic solvers, and
treewidth approximation results. The comparison makes no priority claim
for the shell construction.

## 7. Verification

The targeted checker `check_mixed_shell_certificate.py` checks the lattice
and continuous rounding bounds with exact rational arithmetic, threshold
preservation, the displayed counterexamples, a complete small mixed shell
inequality, the bottom-shell extension, and the endpoint certificate.
It does not replace the proofs. The author's targeted command
`python research-20261002/new-direction/check_mixed_shell_certificate.py`
passed 1,276 scalar rounding cases, 156 mixed-shell and inner radial cases,
three obstruction families, and 289 endpoint-certificate and scale cases.
The independent proof reviewer separately ran
`python3 -B research-20261002/new-direction/check_mixed_shell_certificate.py`
with the same passing counts; the grid and bit reviewer inspected the
checker without rerunning it.
The diagnostic enumerates small product-grid minima; it does not implement
the sparse OR-message DP. The
[independent proof review](mixed-shell-independent-review.md) and
[lattice-grid and bit review](mixed-shell-grid-bit-review.md) found no
substantive gap; their requested input-length and clipping clarifications
are incorporated above. A further
[independent composition review](../reviews/mixed-shell-certificate-review.md)
ran `python research-20261002/reviews/check_mixed_shell_review.py`: its
separate diagnostic matched 47 full shell DPs against enumeration, checked
two fixtures demonstrating why threshold insertion is necessary, and
passed 162 endpoint-growth checks. That review adds sparse-DP composition
and extreme-scale fixtures beyond the author's enumerated minima.
No project-wide verification or CI inspection was performed.
