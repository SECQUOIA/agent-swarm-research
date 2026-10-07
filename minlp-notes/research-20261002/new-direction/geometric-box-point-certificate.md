# A sparse geometric-grid certificate for a proposed box optimum

Date: 2026-10-02. Status: complete derivation that passed
[independent review](geometric-box-point-independent-review.md) and a
[normalization/bit review](geometric-box-point-normalization-review.md).
No priority claim is made.

A proposed rational point in a continuous box admits a finite rational
certificate of unique global optimality and quadratic growth, using one
tree-decomposition dynamic program at each geometric-grid trial. No growth
constant is supplied. If the point is the unique global minimizer, the
positive branch terminates and discovers a margin within a factor sixteen
of the best margin in an explicitly stated normalized metric.

This extends the [homogeneous copositive certificate](geometric-copositive-certificate.md)
to nonhomogeneous quadratics and arbitrary box faces. Feasible signs are
encoded in each variable's states, so no separate enumeration of orthants
is required. The dynamic program and mean-preserving rounding are reused;
the additional ingredients are a radial inequality, sign-preserving
normalization, and a scale that also handles linear growth.

## 1. Model, coordinates, and preliminary checks

Let

\[
 F(x)=x^TAx+q^Tx+c,\qquad A=A^T\in\mathbb Q^{n\times n},
 \qquad X=\prod_i[a_i,b_i],
\]

with rational data and a proposed rational point \(v\in X\).
Eliminate fixed coordinates and absorb their contributions into the
remaining quadratic; if none remain, the singleton problem is immediate.
Below \(n\ge1\) and each interval has positive length. The interaction
graph has edges \(ij\) for nonzero off-diagonal \(A_{ij}\); a supplied
tree decomposition has \(N\) bags of size at most \(p\). The input
length \(I\) includes \(v\), all endpoints, and the decomposition.

Translate the objective:

\[
 F(v+d)-F(v)=c_v^Td+d^TAd,\qquad c_v=2Av+q.
\]

For coordinate \(i\), set
\(w_i^+=b_i-v_i\), \(w_i^-=v_i-a_i\). Keep sign \(+\) only
when \(w_i^+>0\), and sign \(-\) only when \(w_i^->0\).
Let \(Z_i\) be \([0,1]\), \([-1,0]\), or \([-1,1]\), according
to the available signs. Define the coordinatewise bijection

\[
 d_i(z_i)=
 \begin{cases}w_i^+z_i,&z_i\ge0\text{ on an available positive side},\\
 w_i^-z_i,&z_i\le0\text{ on an available negative side},
 \end{cases}
 \qquad d_i(0)=0,
 \quad Z=\prod_i Z_i.
\]

This map is positively homogeneous: \(d(rz)=rd(z)\) for \(r\ge0\)
whenever both arguments lie in their domains. Put

\[
 f(z)=F(v+d(z))-F(v).
\]

First check the coordinate first-order conditions

\[
 s(c_v)_i\ge0\quad\text{for every available sign }s\in\{-1,1\}.
                                                               \tag{1}
\]

In particular an interior coordinate requires \((c_v)_i=0\).
These conditions imply \(c_v^Td(z)\ge0\) for every \(z\in Z\).
Failure supplies a rational feasible continuous descent point: on the
failing side the one-coordinate increment is \(\gamma t+a t^2\),
where \(\gamma=s(c_v)_iw_i^s<0\) and \(a=A_{ii}(w_i^s)^2\).
Take \(t=1\) if \(a\le0\), and
\(t=\min\{1,-\gamma/(2a)\}\) otherwise.

Next evaluate every available one-coordinate endpoint increment

\[
 e_i^s=s(c_v)_iw_i^s+A_{ii}(w_i^s)^2=f(se_i).
\]

An increment at most zero disproves unique global minimality at \(v\):
the displayed different feasible point has no larger value. Otherwise set

\[
 M=\min_{i,s}e_i^s>0,\qquad
 L=2\max\left\{M,\ \max_{i,s}A_{ii}(w_i^s)^2\right\}>0.
                                                               \tag{2}
\]

The maximum of the quadratic diagonal terms may be negative. The positive
term \(M\) makes (2) well defined in that case and when \(A=0\).
There is no requirement of positive quadratic diagonal entries.

## 2. The normalized growth margin and radial inequality

Define

\[
 g=\inf_{z\in Z\setminus\{0\}}\frac{f(z)}{\|z\|_2^2}.
                                                               \tag{3}
\]

This is the side-normalized metric, not silently the physical Euclidean
metric. Assume only that the first-order check (1) has passed. For
\(z=ry\), \(r=\|z\|_\infty\in(0,1]\), one has
\(y\in Z\), \(\|y\|_\infty=1\), and

\[
 f(ry)=r c_v^Td(y)+r^2d(y)^TAd(y)\ge r^2 f(y).           \tag{4}
\]

Consequently

\[
 g=\min_{y\in Z,\ \|y\|_\infty=1}
               \frac{f(y)}{\|y\|_2^2}.                 \tag{5}
\]

The shell is compact and excludes zero. Thus if \(v\) is the unique
global minimizer, its first-order conditions hold, \(f\) is positive
on the shell, and \(g>0\). Conversely \(g>0\) implies unique global
minimality. This direct argument proves the qualitative point-growth
fact needed here without taking a growth promise as an input.

For a successful unique optimum, evaluating the axis endpoints gives
\(g\le M\), so

\[
 L\ge2g,\qquad\kappa=L/g\ge2.                         \tag{6}
\]

The term \(M\) in (2) is necessary for this scale comparison. For
\(F(x)=x\) on \([0,1]\) at \(v=0\), the optimal margin is
\(g=1\) although every quadratic curvature is zero. A scale formed
only from the diagonal curvature would fail to start the search.

## 3. One finite certificate per trial

For \(\delta=2^{-r}\), \(r=1,2,\ldots\), let

\[
 \eta=\delta/n,\qquad \sigma=L\delta^2/8.
\]

Construct the positive grid \(G_\delta\subset[0,1]\) from
\(0,\eta\), successive multiplication by \(1+\delta\), and
one final clipped endpoint 1. For coordinate \(i\), use zero together
with the positive grid nodes for each available sign, reflected for the
negative sign. Call its state set \(S_i\). Compute exactly

\[
 m_\delta=\min_{z\in\prod_iS_i,\ \|z\|_\infty=1}
              [f(z)-2\sigma\|z\|_2^2],\qquad
 b_\delta=m_\delta-\sigma/n.                            \tag{7}
\]

For every trial following checks (1)--(2), the following inequality is
sound, even when \(v\) is not a global minimizer:

\[
 F(v+d(z))-F(v)\ge
       \sigma\|z\|_2^2+b_\delta\|z\|_\infty^2
       \qquad(z\in Z).                                 \tag{8}
\]

In particular \(b_\delta>0\) is a finite certificate of unique global
optimality and positive quadratic growth. It consists of the preliminary
checks, rational grid, exact DP messages for (7), and positive root
quantity \(b_\delta\). Verification does not assume that \(v\) is
optimal or that a growth bound exists.

To prove (8), first fix a shell point \(z\). Round each coordinate
independently to its adjacent grid nodes **on the same sign side**,
preserving its mean; leave zero unchanged. A coordinate with magnitude
one is unchanged, so the rounded vector \(Y\) stays on the shell.
On the selected side \(d_i\) is linear. Hence
\(\mathbb E d_i(Y_i)=d_i(z_i)\), and independence preserves every
off-diagonal quadratic expectation as well as the linear terms.

The same scalar variance bound as in the homogeneous theorem gives

\[
 4\sum_i\operatorname{Var}(Y_i)
 \le\delta^2\mathbb E\|Y\|_2^2+n\eta^2.
\]

For \(R(z)=f(z)-\sigma\|z\|_2^2\), its rounding error is exactly

\[
 \mathbb E R(Y)-R(z)
 =\sum_i[A_{ii}(w_i^{s_i})^2-\sigma]
                        \operatorname{Var}(Y_i),
\]

with zero contribution from a coordinate fixed at zero. By (2), each
coefficient is at most \(L/2\), regardless of its sign. Therefore

\[
 R(z)\ge
 \mathbb E[f(Y)-2\sigma\|Y\|_2^2]-\sigma/n
 \ge b_\delta.                                         \tag{9}
\]

Apply (9) to the shell point \(y=z/\|z\|_\infty\), then use
(4). This proves (8). No differentiability of the piecewise normalized
function at a sign change is used. Rounding never crosses that change.
The scale \(L\) bounds fixed-sign quadratic diagonals; it need not be
a global coordinate-semiconcavity bound across zero.

## 4. Unknown-margin discovery and width-preserving DP

Try the stated dyadic values and stop at the first \(b_\delta>0\).
If \(v\) is the unique global minimizer, then \(g>0\) by (5).
Every grid shell point has squared norm at least one. Whenever
\(\sigma\le g/4\),

\[
 m_\delta\ge g-2\sigma,\qquad
 b_\delta\ge g-(2+1/n)\sigma\ge g/4>0.
\]

Thus the positive branch terminates. Trials divide \(\sigma\) by four.
A failed preceding trial implies \(\sigma>g/16\) at the first success;
if the first trial succeeds, (6) gives
\(\sigma=L/32\ge g/16\). From (8),
\(g\ge\sigma+b_\delta/n>\sigma\). Consequently

\[
                    g/16\le\sigma<g.                  \tag{10}
\]

No termination assertion is made for a nonunique optimum or an arbitrary
incorrect candidate that passes the preliminary checks. Such a finite
failed trial is inconclusive. The algorithm discovers a verified margin;
it is not an algorithm for finding the proposed point \(v\).

The normalized objective has unary terms
\((c_v)_id_i(z_i)+A_{ii}d_i(z_i)^2-2\sigma z_i^2\) and pair
terms \(2A_{ij}d_i(z_i)d_j(z_j)\). Thus its interaction graph is
unchanged; piecewise signs create no new edges or bags. Assign variables
and factors to bags exactly as in the homogeneous certificate. A message
has a separator assignment and one bit recording whether an **owned**
coordinate in its subtree has magnitude one. Combine local and child bits
by OR, with sequential two-state convolutions. The root bit-one value is
(7). There is one DP per trial, no anchor enumeration and no enumeration
of \(2^n\) sign patterns. High bag degree costs a sum of child work.

If the positive grid has \(K\) nodes, a signed state set has at most
\(2K-1\). At the final trial,

\[
 \delta^{-1}\le\sqrt{2\kappa},\qquad
 K=O(\sqrt\kappa\log(2n\sqrt\kappa)).
\]

The \(O(1+\log\kappa)\) trials therefore take
\(f(p,\kappa)\operatorname{poly}(n+N)\) arithmetic work, plus input
reading, by the same logarithmic-power absorption as in the homogeneous
theorem. Verification of the finite DP certificate obeys the same bound.
There is no bound on how many bags contain a variable.

The signed grid nodes have the same common denominator as the unsigned
ones. Multiplying by the rational side widths and translated coefficients
adds only polynomial input-bit cost. Pair interactions remain rational
tables. Assigning each term once makes every finite DP message a sum of
a subset of these tables; message addition does not multiply denominators
across bags. Grid construction, exact comparisons, stored witnesses, and
certificate verification therefore take
\(f_1(p,\kappa)\operatorname{poly}(I)\) bit work with an absolute
polynomial exponent. Requested accuracy and coefficient height do not
separately dictate the number of grid states; their effect through
\(\kappa\) is not removed.

## 5. Physical coordinates and metric distortion

The certificate can be written without normalized variables. For a
nonzero displacement coordinate choose its corresponding side width and
set

\[
 \|d\|_v^2=\sum_{i:d_i\ne0}(d_i/w_i^{\operatorname{sign}(d_i)})^2,
 \qquad\rho_v(d)=\max_i|d_i|/w_i^{\operatorname{sign}(d_i)},
\]

with zero contributions for zero coordinates. The physical grid is
simply the signed normalized grid multiplied by the appropriate rational
width. Equation (8) becomes

\[
 F(v+d)-F(v)\ge\sigma\|d\|_v^2+b_\delta\rho_v(d)^2.
                                                               \tag{11}
\]

Let \(w_{\min},w_{\max}\) be the smallest and largest **positive**
side widths. If \(g_E\) is the optimal physical Euclidean point-growth
constant and \(g_E\ge0\) (in particular, in the positive-margin
case), then

\[
 w_{\min}^2g_E\le g\le w_{\max}^2g_E.
\]

A positive certificate proves physical Euclidean growth at least
\((\sigma+b_\delta/n)/w_{\max}^2\), and the simpler returned value
\(\sigma/w_{\max}^2\) is at least
\(g_E(w_{\min}/w_{\max})^2/16\). Thus (10) is not an
aspect-free factor-sixteen guarantee for \(g_E\). On a vertex of a
unit box the metrics coincide. On unequal boxes or close to a face, this
normalization can substantially worsen the conditioning. No intrinsic
physical-curvature/margin FPT theorem is inferred by suppressing that
distortion.

For a strictly interior proposed point, (1) forces \(c_v=0\). A unique
quadratic minimum there already implies \(A\succ0\): all directions
are locally feasible, and a null direction would give a line of equal
values. Positive-definiteness testing supplies a simpler baseline in
that case. The extension's additional scope is nonhomogeneous corners
and arbitrary face points; it is not a solver-advantage claim for fully
interior quadratic minimizers.

### The endpoint scale can worsen curvature conditioning

The term \(M\) is needed for this note's factor-sixteen comparison with
\(g\), but it can be much larger than the quadratic diagonal curvature.
For rational \(H,\varepsilon>0\), consider on \([0,1]^2\)

\[
 F(x,y)=H(x+y-2xy)+\varepsilon(x^2+y^2).
\]

The first term is nonnegative because
\(x+y-2xy=x(1-y)+y(1-x)\). The origin is the unique minimum,
and the optimal physical and normalized margins both equal
\(\varepsilon\), attained in the ratio at \((1,1)\). The original
coordinate-curvature bound is \(2\varepsilon\), but (2) selects
\(L=2(H+\varepsilon)\). Thus this note's conditioning parameter can
be arbitrarily worse than diagonal-curvature divided by growth, even on
a unit box. The enlarged scale is a material limitation, not a harmless
normalization.

The separate [physical-shell investigation](mixed-shell-certificate.md)
is intended to preserve a supplied diagonal-curvature bound and instead
return a margin bounded below relative to \(\min\{L,g\}\), without
requiring a constant-factor estimate of arbitrarily larger \(g\).
That stronger framework has its own proof and review obligations.

## 6. Mixed-integer boundary of the result

A continuous-box certificate is also sound on any mixed-integer subset
containing \(v\). Its discovery guarantee, however, requires growth on
the continuous box. Discrete optimality alone does not justify (1),
radial rescaling, or the real geometric-grid rounding.

For example \(F(x)=x^2-x/2\) on \(\{0,1\}\) has unique minimum
at zero and discrete growth \(1/2\), but its continuous derivative at
zero is negative. The preliminary descent point is fractional, so it
does not disprove the integer optimum.

Even passing (1) and all endpoint checks is insufficient for a discrete
growth promise to imply continuous growth. On \(\{0,1\}^2\),

\[
 F(x,y)=x^2-xy+y/10
\]

has unique minimum at \((0,0)\) and discrete Euclidean growth \(1/20\).
Its first-order signs hold and its axis endpoint values are positive,
but \(F(1/2,1)=-3/20\). The present procedure certifies the continuous
relaxation, not this integer optimum. No new mixed-integer certificate or
integrality-preserving radial argument is claimed.

## 7. Verification and scope

The independent reviews found no substantive gap. They required two scope
clarifications, now explicit: metric comparison assumes a nonnegative
margin, and fixed-sign curvature does not imply global semiconcavity of
the transformed objective.

The targeted command

```sh
python research-20261002/new-direction/check_geometric_box_point.py
```

passed five positive fixtures and seven discovery trials, with every
signed DP minimum compared against direct grid enumeration. It verified
50 exact independent-rounding identities, 150 radial certificate bounds,
and two nonunique cases that did not produce a positive certificate.
Fixtures include a linear objective, a negative quadratic diagonal,
asymmetric interior sides, a nonhomogeneous face minimum, and a signed
star decomposition. The fresh reviewer separately checked 69 rational
certificate/radial probes and 163 rounding atoms; those checks were not
rerun here.

This note does not assert novelty for rounding, tree-decomposition DP,
or the qualitative point-growth fact. The earlier exact conditioned
optimizer can in principle certify a candidate by optimizing
\(F(x)-F(v)-\gamma\|x-v\|^2\) for a suitable margin trial.
The present direct DP proof avoids an optimization-accuracy target and
exact-value recovery; it does not establish a new conditioned solvability
class by itself. Its endpoint-scale and side-metric limitations above
remain material. No project-wide checks or CI inspection were performed.
