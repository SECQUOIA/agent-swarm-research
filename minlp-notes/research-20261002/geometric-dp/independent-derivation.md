# Independent derivation: geometric grids with certified rounding penalties

Date: 2026-10-02. Status: mathematical derivation by a second research agent,
following the root agent's proposed construction. This is not an independent
literature audit or a completed adversarial review. The construction below
handles a product of continuous intervals and integer intervals. General
constraints are not included.

## Main point

An exact finite-state dynamic program can return a valid global lower bound
after subtracting explicit unary rounding penalties. Geometric coordinate
grids keep its state count logarithmic in resolution. Under global quadratic
growth, recentering these grids around the previous corrected-grid minimizer
gives a contraction in squared Euclidean distance. This avoids the need for
a dimension-independent sup-norm localization theorem.

The same construction permits long integer intervals to be represented by
geometric grids. Unit gaps incur no penalty because they contain no omitted
integer point. In a purely integer problem, the algorithm eventually gives
an exact certificate without enumerating every integer in each interval.

## 1. Assumptions and notation

Let

\[
 X=\prod_{i=1}^n X_i,\qquad
 X_i=[a_i,b_i]\quad\text{or}\quad
 X_i=[a_i,b_i]\cap\mathbb Z.
\]

Integer interval endpoints are integers. Coordinates with singleton domains
may be eliminated. Write \(s=\max_i(b_i-a_i)>0\). The objective
\(F=\sum_t a_t(x_{V_t})\) has a supplied tree decomposition with \(N\) bags
of size at most \(w+1\). A bag objective evaluation is one oracle operation.

Assume that \(F\) has an extension to the full continuous bounding box with
an \(L\)-Lipschitz gradient, \(L>0\). For example, if every bag function
has an \(M\)-Lipschitz gradient and each variable belongs to at most \(k\)
bags, \(L=kM\) suffices. More generally, if bag constants are \(M_t\),
\(L=\max_i\sum_{t:i\in V_t}M_t\) suffices for the Taylor upper bound used
below. Indeed, sum the bag Taylor bounds and collect squared coordinate
increments.

Assume a unique optimizer \(x^*\in X\) and global quadratic growth on the
actual, possibly mixed, domain:

\[
 F(x)-F(x^*)\ge c_g\|x-x^*\|_2^2\qquad(x\in X),\quad c_g>0.       \tag{1}
\]

No zero-gradient hypothesis at \(x^*\) is needed. All finite minimizations
and objective evaluations in the proof are exact. Arithmetic precision and
the cost of obtaining valid constants are separate issues.

## 2. Coordinate grids

Fix a feasible center \(c\), a core width \(h>0\), and \(0<\theta\le1/2\).
Each grid contains \(c_i\) and both domain endpoints. Build the two sides
outward from \(c_i\), clipping the last step to its endpoint.

For a continuous coordinate, from distance \(t\ge0\) take step
\(h+\theta t\). Before clipping, the distances are

\[
 t_j=\frac h\theta((1+\theta)^j-1).
\]

For an integer coordinate, take step

\[
 \Delta(t)=\max\{1,\lfloor h+\theta t\rfloor\}.                    \tag{2}
\]

This preserves integrality because the center and endpoints are integers.

At a grid node \(v\), let \(\ell_i(v)\) be the maximum of its adjacent
interval lengths. For integer coordinates, ignore intervals of length one;
set \(\ell_i(v)=0\) if no adjacent interval has length at least two. Then

\[
 \ell_i(v)\le h+\theta|v-c_i|.                                   \tag{3}
\]

For an interval starting at the inner endpoint, its length is at most
\(h+\theta\) times that endpoint's distance, unless it is a unit integer
interval, which was ignored. The distance at the outer endpoint is larger.
This proves (3) for each adjacent interval, including clipped intervals.

For a continuous side of length \(r\), there are at most

\[
 1+\left\lceil\frac{\log(1+\theta r/h)}{\log(1+\theta)}\right\rceil
\]

steps, using a harmless extra one for endpoint clipping. For an integer
side put \(H=\max\{h,1\}\). Every unclipped step in (2) satisfies

\[
 \Delta(t)\ge (H+\theta t)/3.                                    \tag{4}
\]

If \(h\ge1\), use \(\lfloor u\rfloor\ge u/2\) for \(u\ge1\).
If \(h<1\) and \(\theta t<2\), the right side of (4) is at most one.
If \(h<1\) and \(\theta t\ge2\), then
\(\Delta(t)\ge(h+\theta t)/2\ge(1+\theta t)/3\).
Thus \(t+H/\theta\) grows by a factor at least \(1+\theta/3\), until
the last step. The integer side needs at most

\[
 1+\left\lceil\frac{\log(1+\theta r/H)}{\log(1+\theta/3)}\right\rceil
\]

steps. In particular, both coordinate types have
\(O(1+\theta^{-1}\log(1+\theta s/h))\) states; integer state counts stop
growing once \(h<1\).

## 3. A valid lower bound from rounding

Define unary penalties on the grids by

\[
 d_i(v)=L\ell_i(v)^2/8,\quad
 D(y)=\sum_i d_i(y_i),\quad
 Q=\min_{y\in\prod_i G_i}\{F(y)-D(y)\}.                          \tag{5}
\]

Then \(Q\le F(x^*)\).

To prove this, fix any feasible \(x\). If \(x_i\) is already a node, leave
it unchanged. Otherwise, round it independently to the two endpoints of
its containing grid interval, with probabilities that preserve its mean.
Write the resulting feasible random vector as \(Y\). Its coordinate
variance is at most one quarter of the squared interval length. For an
integer coordinate, an omitted integer point can only belong to an
interval of length at least two. The endpoints of every interval actually
used for random rounding therefore have
\(d_i\ge L\,\text{length}^2/8\). Consequently,

\[
 \mathbb E D(Y)\ge\frac L2\mathbb E\|Y-x\|_2^2.
\]

The Taylor upper bound and \(\mathbb EY=x\) give

\[
 \mathbb EF(Y)\le F(x)+\frac L2\mathbb E\|Y-x\|_2^2.
\]

Thus \(Q\le\mathbb E(F(Y)-D(Y))\le F(x)\), proving the claim at \(x=x^*\).
The argument uses no first-order optimality condition. It remains valid
at boundary optima and for integer optima.

If \(y\) minimizes (5), \(F(y)\) is a feasible upper bound, and its gap
against \(Q\) is exactly \(D(y)\).

## 4. Contraction and a complete algorithm

Choose

\[
 \theta^2\le\min\{1/4,c_g/(8L)\},\qquad
 B=\max\{1,4L/(11c_g)\}.                                        \tag{6}
\]

Start at any feasible center \(c_{-1}\). At stage \(j=0,1,\ldots\), set
\(h_j=s2^{-j}\), construct the grids centered at \(c_{j-1}\), minimize
(5), and set \(c_j=y_j\). Stop when \(D(y_j)\le\varepsilon\).

The following statements hold at every stage:

\[
 \|y_j-x^*\|_2^2\le Bnh_j^2,\qquad
 D(y_j)\le(7L/8)nh_j^2.                                         \tag{7}
\]

For the first bound, set \(E=\|y-x^*\|_2^2\) and
\(E_{\rm old}=\|c-x^*\|_2^2\). From (3),

\[
 D(y)\le\frac L4\left(nh^2+\theta^2\|y-c\|_2^2\right).
\]

Since \(F(y)-D(y)=Q\le F(x^*)\), quadratic growth gives

\[
 (c_g-L\theta^2/2)E
 \le Lnh^2/4+(L\theta^2/2)E_{\rm old}.
\]

By (6),

\[
 E\le\frac{4L}{15c_g}nh^2+\frac1{15}E_{\rm old}.                 \tag{8}
\]

At stage zero \(E_{\rm old}\le ns^2\). This and (8) imply
\(E\le Bns^2\): if \(L/c_g\le11/4\), the coefficient in (8) is at
most \(4/5\); otherwise compare it directly with \(4L/(11c_g)\).
At later stages, induction and \(h_{j-1}=2h_j\) give

\[
 E\le\left(\frac{4L}{15c_g}+\frac{4B}{15}\right)nh_j^2
 \le Bnh_j^2.
\]

Also \(\theta^2 B\le1/4\). For \(j\ge1\), the penalty estimate gives

\[
 D(y_j)\le\frac L4[1+2\theta^2(B+4B)]nh_j^2
 \le(7L/8)nh_j^2.
\]

The same estimate holds at stage zero because
\(E_{\rm old}\le nh_0^2\le4Bnh_0^2\). This proves (7).

Therefore an \(\varepsilon\)-certificate is available by stage

\[
 J=\max\left\{0,
 \left\lceil\log_2\left(s\sqrt{7Ln/(8\varepsilon)}\right)\right\rceil
 \right\}.                                                      \tag{9}
\]

## 5. Dynamic-programming cost

Unary penalties can be assigned to any bag containing their coordinate.
The corrected objective retains the supplied tree decomposition. A usual
finite-state tree dynamic program minimizes it exactly in

\[
 O\left(\sum_t(1+|\operatorname{ch}(t)|)
                    \prod_{i\in V_t}|G_i|\right)
\]

bag-state operations: compute a table for each bag, add child message
values, and minimize over the coordinates private to its parent separator.
There is no multiplication of all child state spaces.

At stage \(j\), every continuous grid has
\(O(\theta^{-1}(j+1))\) nodes because \(s/h_j=2^j\); integer grids obey
the same upper bound. Summing over stages through (9) gives

\[
 O\left(N\theta^{-(w+1)}(J+1)^{w+2}\right)                       \tag{10}
\]

bag-state operations. With (6), the dependence on \(L/c_g\) is
\(O(\max\{1,L/c_g\}^{(w+1)/2})\), apart from constants depending on
\(w\). This is an oracle operation bound, not a bit-complexity theorem.

## 6. Exact termination for purely integer problems

Assume every coordinate is integer. At the first stage \(j\) with
\(Bnh_j^2<1\), (7) forces \(y_j=x^*\), since distinct integer vectors
are at squared Euclidean distance at least one.

At stage \(j+1\), the center is therefore \(x^*\), and (7) again forces
\(y_{j+1}=x^*\). Since \(h_{j+1}<2\), the first outward step from each
center coordinate is one, or there is no step if it is at the domain
endpoint. Hence \(\ell_i(x_i^*)=0\) for every coordinate. The penalty is
zero and (5) returns \(Q=F(x^*)\), an exact certificate.

It is enough to run
\(O(1+\log_+(s\sqrt{Bn}))\) stages. Integer grids have at most
\(O(1+\theta^{-1}\log(1+\theta s))\) states throughout. Their domain
lengths enter logarithmically. The hypothesis (1), including a useful
positive constant, remains substantive: it may encode an arbitrarily
small objective separation between integer points. This result does not
give a strongly polynomial algorithm for general integer optimization.

## 7. What is new enough to investigate, and what remains limited

Finite-state tree dynamic programming, unbiased randomized rounding,
Taylor estimates, and geometric meshes are established tools. Their use
alone is not a novelty claim. The candidate contribution is their
combination into a valid corrected-grid lower bound and a recentering
contraction, with the explicit cost (10), including compressed integer
grids and exact pure-integer termination. Priority needs a targeted
literature audit.

This algorithm does not use per-bag alphaBB or McCormick relaxations, does
not reuse the earlier relaxed-copy certificate model, and does not prove
its open branching-tree localization conjecture. It is a different
certificate construction. Its lower bound follows directly from (5).

Material limits are:

- The feasible domain is a product. General nonlinear or linear coupling
  constraints can invalidate the rounding argument. Adding an exact
  penalty needs a separate theorem and can damage \(L/c_g\).
- Global quadratic growth selects one optimizer and supplies a global
  conditioning constant. Several global optima require a different
  localization argument; a nearly tied distant local optimum can make
  \(c_g\) very small.
- Constants \(L\) and \(c_g\) are supplied in this version. The lower
  bound remains valid for any grid if \(L\) is valid; \(c_g\) is used
  only to choose a refinement parameter and prove its complexity.
- Evaluations, comparisons, and DP messages are exact here. Certified
  interval evaluations and their accumulated error need to be included
  before claiming an implementable exact arithmetic bound.
- Large treewidth still gives exponential cost. The operation count does
  not measure factor evaluation complexity or the cost of finding a tree
  decomposition.

## 8. Targeted checks

A standalone inline Python check was run locally, using NumPy and direct
enumeration. It checked the integer-grid penalty inequality (3) and node
count over integer domains of lengths 1 through 30, all possible centers,
seven widths, and three grading ratios. It also generated 40 three-variable
strictly convex quadratic integer problems on \([-6,6]^3\), computed their
exact discrete optima by enumeration, derived their actual quadratic-growth
constants on that finite domain, and ran the corrected-grid minimizations
by enumeration. The checks assert lower-bound validity, both inequalities
in (7), and exact termination at the true optimizer. The command was
`python3 - <<'PY'` with that inline checker. It completed successfully:
10,395 grid cases passed; all 40 optimization cases certified their exact
optimizer, in at most four stages. These floating-point checks support the
derivation; they are not proofs. No project-wide verification or CI logs
were run.
