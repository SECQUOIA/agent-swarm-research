# Certifying nonunique optima with coordinate anchor sets

Date: 2026-10-02. Status: new mathematical result under separate adversarial
review and literature investigation. The coordinate-projection improvement
was proposed jointly with the root agent. It extends the
[corrected geometric-grid theorem](../geometric-dp/theorem.md); it is not an
extension of the original relaxed-copy certificate model.

## Main consequence

Global quadratic growth around one specified optimizer can be replaced by
quadratic growth toward the full optimal set. If the optimal coordinates
take only finitely many distinct values, the algorithm still has
polylogarithmic accuracy dependence at fixed structural parameters. Its
bound depends on the number of those coordinate values, rather than the
number of global optimizers.

For example, \(\sum_i(x_i^2-1)^2\) on \([-1,1]^n\) has \(2^n\)
global optimizers, but only two optimal values of each coordinate. The new
bound counts these \(2n\) coordinate values. The algorithm does not know
them: it discovers additional coordinate anchors from corrected-grid
minimizers.

More generally, for any compact optimal set, finite-resolution covering
numbers of its coordinate projections bound the work. These numbers can
grow with accuracy, so a positive-dimensional optimal set is not claimed
to have a polylogarithmic bound in general. Section 8 proves this limitation
is real for these corrected-grid certificates, even on a convex quadratic
with constant conditioning and a diagonal line of optimizers.

For purely integer gridded variables, the same method has an exact stopping
criterion despite multiple optima. This uses exact factor tables and
comparisons. No exact continuous-optimizer reconstruction is claimed.

## 1. Assumptions and representation

Let \(x\) have a product domain of continuous or integer intervals
\(X_i=[a_i,b_i]\) or \([a_i,b_i]\cap\mathbb Z\). Remove fixed coordinates,
and write \(n\ge1\), \(s_i=b_i-a_i>0\), and \(s=\max_i s_i\).
Integer endpoints are integral. Optional finite-state variables \(z\)
are fully enumerated in each bag, as in Section 6 of
[the grid extensions](../geometric-dp/extensions.md). Their states need no
metric. The common domain of \(x\) is independent of \(z\).

The objective \(F(x,z)\) has a supplied tree decomposition. It has upper
coordinate curvature \(L>0\) in \(x\), uniformly over fixed \(z\):
subtracting \(Lx_i^2/2\) makes each coordinate restriction concave.
Assume the projected global optimal set

\[
 S=\{x:\text{some feasible }z\text{ has }F(x,z)=f^*\}
\]

is nonempty and compact. For no finite-state variables this is simply the
optimal set. The new growth assumption is

\[
 F(x,z)-f^*\ge g\,\operatorname{dist}(x,S)^2\quad(g>0)            \tag{1}
\]

for every feasible pair. There need not be a unique point in \(S\) or a
unique optimal \(z\) at any such point. The nearest point of \(S\) used
in the proof need not share the current finite-state assignment.

All bounds below initially count exact objective-table evaluation,
arithmetic, and comparison operations. Rational arithmetic and certified
evaluation errors require their own budgets; the earlier grid extensions
cannot be transferred without checking the changed progress argument.

## 2. Algorithm

For target \(\varepsilon>0\), set

\[
 h=\frac{\sqrt\varepsilon}{2\sqrt{Ln}},\qquad
 0<\theta\le\min\{1/2,\tfrac12\sqrt{g/L}\}.                    \tag{2}
\]

A smaller \(h\) also works; for rational implementation it can be chosen
dyadic between one half and one times the displayed value. A dyadic
\(\theta\) within a constant factor of the threshold suffices.

Start with any feasible exposed vector and put its coordinate values in
anchor sets \(C_i\). Repeatedly:

1. For each anchor \(c\in C_i\), form the one-dimensional geometric grid
   of the original theorem, with core width \(h\) and ratio \(\theta\).
   Let \(G_i\) be the union of these grids, with duplicates removed.
2. At node \(v\in G_i\), let \(\ell_i(v)\) be its largest adjacent
   interval length. For integer coordinates ignore unit intervals. Define
   \(d_i(v)=L\ell_i(v)^2/8\) and \(D(x)=\sum_i d_i(x_i)\).
3. Use exact finite-state DP to minimize \(F(x,z)-D(x)\) over the product
   of the shared grids and all retained finite states. Let \((y,z_y)\)
   attain this value \(\operatorname{LB}\).
4. If \(D(y)\le\varepsilon\), return this lower bound and feasible point.
   Otherwise insert \(y_i\) into every \(C_i\), and repeat.

There is no need to know \(S\), its coordinate values, their separation,
or any covering number. The threshold for \(\theta\) uses \(g\) in
this version. The lower bound is valid for every positive ratio; Section 8
describes removing knowledge of \(g\).

The algorithm retains all anchors. Replacing a previous anchor by the latest
point would lose the monotonicity on which the proof relies.

## 3. Union grids and their correction

At every union-grid node,

\[
 \ell_i(v)\le h+\theta\operatorname{dist}(v,C_i).                \tag{3}
\]

To see this, fix any anchor and inspect its source grid. Each adjacent
union interval lies in a source interval on one side of that anchor. The
nearer source endpoint is at least as close to the anchor as the union
node. Its geometric step therefore bounds the union interval by
\(h+\theta|v-c|\). This applies to each anchor, so take their minimum.
For integer coordinates, a union interval longer than one cannot be
contained in a source unit interval, and the same argument applies.

The independent-rounding lemma for arbitrary shared grids consequently gives

\[
 \operatorname{LB}\le f^*\le F(y,z_y),\qquad
 F(y,z_y)-\operatorname{LB}=D(y).                               \tag{4}
\]

Write \(C_\times=\prod_i C_i\). From (3),

\[
 D(y)\le\frac L4\left[nh^2+
                    \theta^2\operatorname{dist}(y,C_\times)^2\right].
                                                                    \tag{5}
\]

The product \(C_\times\) need not be stored or enumerated as a collection
of complete centers. Only its one-dimensional anchor sets are stored.

## 4. A failed solve makes progress in an optimal coordinate

Choose any nearest optimizer \(s^*\in S\), and define

\[
 r=\|y-s^*\|,\quad e=\operatorname{dist}(s^*,C_\times),\quad
 A=\sqrt{Ln}h/2\le\sqrt\varepsilon/4,
\]

\[
 b=\sqrt L\,\theta/2,\qquad \lambda=b/\sqrt g\le1/4.
\]

Growth, (4), (5), and the triangle inequality give

\[
 \sqrt g\,r\le\sqrt{D(y)}\le A+b(r+e),
 \qquad
 \sqrt{D(y)}\le\frac{A+be}{1-\lambda}.                         \tag{6}
\]

If the stopping test fails, \(D(y)>\varepsilon\), so
\(be>\sqrt\varepsilon/2\). Put

\[
 R=\frac{\sqrt\varepsilon}{\sqrt L\,\theta},\qquad
 \tau=\frac R{\sqrt{2n}}.
\]

Then \(e>R\), and \(A<be/2\). The first inequality of (6) gives

\[
 r<\frac{3\lambda}{2(1-\lambda)}e\le e/2.                      \tag{7}
\]

Set \(e_i=\operatorname{dist}(s_i^*,C_i)\). Coordinates with
\(e_i>\tau\) carry more than half the squared distance \(e^2\):
the other coordinates contribute at most
\(n\tau^2=R^2/2<e^2/2\).

At least one such coordinate satisfies

\[
 |y_i-s_i^*|<e_i/\sqrt2.                                       \tag{8}
\]

Otherwise their contribution to \(r^2\) would exceed \(e^2/4\),
contradicting (7). After inserting \(y_i\), the distance from this optimal
coordinate value to its anchor set has decreased by a factor smaller than
\(1/\sqrt2\), from a value greater than \(\tau\). Every other distance
to every anchor set is nonincreasing because anchors are never removed.

The charged optimizer and coordinate are analysis devices. The algorithm
need not identify either of them.

## 5. Finite coordinate projections

Let \(S_i=\pi_i(S)\) be finite. Define

\[
 T_{\rm fin}=\sum_{i=1}^n |S_i|
   \max\left\{0,\left\lceil
               \log_{\sqrt2}(s_i/\tau)\right\rceil\right\}.    \tag{9}
\]

There are at most \(T_{\rm fin}\) failed solves and
\(T_{\rm fin}+1\) DP solves in total. To prove this, charge each failure
to one pair \((i,s_i^*)\) satisfying (8). Its initial distance to the
anchor set is at most \(s_i\). Each charge decreases that distance by a
factor smaller than \(1/\sqrt2\), and a charge requires its old distance
to exceed \(\tau\). This gives exactly (9).

Finite coordinate projections and a finite set \(S\) are equivalent in
finite dimension. The improvement is the dependence on
\(\sum_i|S_i|\), which can be exponentially smaller than \(|S|\).
No lower bound on the separation between distinct optimal coordinates is
required.

For the separable double-well example,

\[
 F(x)=\sum_i(x_i^2-1)^2,\qquad x\in[-1,1]^n,
\]

the optimal set is \(\{-1,1\}^n\). Its upper coordinate curvature is
\(L=8\), and

\[
 F(x)=\sum_i(1-|x_i|)^2(1+|x_i|)^2
      \ge\operatorname{dist}(x,\{-1,1\}^n)^2.
\]

Thus \(g=1\), and (9) counts \(2n\) optimal coordinate values instead
of \(2^n\) optimizers. This illustrates the parameter distinction; it is
not a claim that the generic algorithm beats direct separable optimization
on this particular example.

## 6. General compact optimal sets

For each coordinate, let \(T_i\subseteq S_i\) be a finite net with radius
\(\rho=\tau/16\): every point of \(S_i\) is within \(\rho\) of a
net point. Compactness ensures such nets exist. These nets are used only
in the analysis.

For a charged value \(s_i^*\), choose a net point \(a\) within \(\rho\).
Before insertion of \(y_i\), let \(q=\operatorname{dist}(a,C_i)\).
Since \(e_i>\tau\),

\[
 q\ge e_i-\rho>15\tau/16,\qquad q\ge15e_i/16.
\]

After insertion,

\[
 q_{\rm new}\le|a-y_i|<\rho+e_i/\sqrt2
    \le(1/16+1/\sqrt2)e_i<(5/6)q.                              \tag{10}
\]

The last strict inequality uses
\(1/16+1/\sqrt2<25/32=(5/6)(15/16)\).

Consequently, if \(\mathcal N_i(\rho)\) is the minimum cardinality of
such a net in \(S_i\), the total number of failed solves is at most

\[
 T_{\rm cov}=\sum_i\mathcal N_i(\tau/16)
    \max\left\{0,\left\lceil
        \log_{6/5}\frac{s_i}{15\tau/16}\right\rceil\right\}.    \tag{11}
\]

This proves finite termination under (1) for every compact optimal set.
It also gives an explicit accuracy dependence through the coordinate
projection covering numbers. Formula (9) is the sharper finite-projection
corollary. The factor count alone does not control these covering numbers;
they are an additional instance parameter.

## 7. Table work and exact integer stopping

One anchor contributes at most

\[
 q_0=O\bigl(1+\theta^{-1}\log(1+\theta s/h)\bigr)
\]

nodes to a coordinate grid. The integer count is smaller once \(h<1\),
as in the original theorem. After \(t\) failures, each coordinate has at
most \(t+1\) anchors, hence at most \((t+1)q_0\) grid nodes.

The grids can be maintained incrementally. Generate each new source grid
in sorted order and merge it with the retained union, removing duplicates.
The merge costs \(O(|G_i|+q_0)\). Total grid-generation and merge work is
\(O(nq_0(T+1)^2)\). Up to factors in bag width, this is dominated by the
table bound below: every gridded coordinate belongs to some bag with at
least one gridded coordinate. Repeatedly sorting all source grids is
unnecessary.

Let \(p_t\) be the number of gridded coordinates in bag \(t\), let
\(d_t\) be its product of fully enumerated state-domain sizes, and put
\(a_t=1+|\operatorname{ch}(t)|+m_t\), where \(m_t\) counts assigned
factors. With \(T\) equal to either bound (9) or (11), total table work
is at most

\[
 O\left(\sum_t a_t d_t q_0^{p_t}(T+1)^{p_t+1}\right),           \tag{12}
\]

apart from nonunit factor-evaluation costs and indexing factors in bag
width. The bound includes the growth of union grids and the final
successful solve. With no finite states, at most \(p\) coordinates per
bag, and \(M\) factors, it simplifies to
\(O((N+M)q_0^p(T+1)^{p+1})\).

At fixed \(\sum_i|S_i|\), width, and conditioning, (9) and (12) have
polylogarithmic accuracy dependence. Dimension and the number of optimal
coordinate values are not being treated as fixed in the explicit formulas.
Compared with the unique-point theorem, this bound generally has a worse
dependence on dimension and logarithms; it handles an assumption that the
single-center argument does not cover.

### Purely integer gridded variables

Suppose every gridded coordinate is integer; fully enumerated finite states
are still allowed. Request \(\varepsilon=L/4\). The corresponding
displayed core width is \(h=1/(4\sqrt n)\). Every nonzero integer penalty
is at least \(L/2\), since a retained interval has integer length at least
two. Therefore a successful stop with \(D(y)\le L/4\) forces
\(D(y)=0\). By (4),

\[
 \operatorname{LB}=F(y,z_y)=f^*.
\]

The method thus produces an exact optimal point and value certificate even
with multiple optima. This conclusion uses exact factor evaluations and
comparisons; positive table-evaluation uncertainty cannot be silently
discarded merely because the geometric correction is zero. The result
does not assert exact reconstruction of continuous optimal coordinates.
The projection-cardinality or covering-number factors remain in its work
bound; they can grow with the integer domain lengths when many values are
optimal. Exactness does not remove that dependence.

## 8. An intrinsic obstruction from optimal coordinate projections

For any shared grids and the same correction formula, define the conditional
margin at node \(v\in G_i\) by

\[
 W_i(v)=\inf_{x_{-i},z}\{F(x_i=v,x_{-i},z)-f^*\}.
\]

Fix coordinate \(i\) at \(v\), and independently round all the others
at a conditional minimizer, or along a sequence approaching its infimum.
The ordinary rounding argument cancels the other coordinates' curvature
errors with their penalties. The fixed coordinate has zero rounding variance
but still pays \(d_i(v)\). Hence

\[
 \operatorname{LB}\le f^*+W_i(v)-d_i(v).                        \tag{13}
\]

For any feasible incumbent \(U\), a certificate
\(U-\operatorname{LB}\le\varepsilon\) therefore requires

\[
 d_i(v)\le\varepsilon+W_i(v)\quad\text{for every grid node}.    \tag{14}
\]

In particular, at nodes in \(S_i\), the conditional margin vanishes.

Consider \(F(x_1,x_2)=(x_1-x_2)^2\) on \([0,1]^2\). Its optimal set is
the diagonal segment, its coordinate curvature is \(L=2\), and

\[
 F(x)=2\operatorname{dist}(x,S)^2,
\]

so \(g=2\). Its interaction graph has treewidth one. Nevertheless
\(W_i(v)=0\) for every coordinate value. At an endpoint of an interval
of length \(\Delta\), the penalty is at least \(L\Delta^2/8\).
Thus (14) forces

\[
 \Delta\le2\sqrt\varepsilon,\qquad
 |G_i|\ge\left\lceil\frac1{2\sqrt\varepsilon}\right\rceil+1.   \tag{15}
\]

No choice of anchors, regridding, or endpoint grids can make this particular
corrected-grid certificate polylogarithmic in accuracy on the example.
An explicit table for its two-variable bag has
\(\Omega(\varepsilon^{-1})\) entries. This is a limitation of the specified
certificate formula, not an optimization-hardness result: the objective is
a simple convex quadratic and has immediate zero lower bounds by other
methods. The example explains why the marginal covering numbers in (11)
cannot simply be omitted from the analysis.

## 9. Unknown growth constants and limitations

### Finite convergence without a growth assumption

The same algorithm terminates at any fixed positive \(\theta\), even
without (1). A failed solve and (5) imply

\[
 \operatorname{dist}(y,C_\times)^2>
          (4\varepsilon/L-nh^2)/\theta^2.
\]

The numerator is positive by (2). Some coordinate is therefore farther
than

\[
 \delta=\frac1\theta
       \sqrt{\frac{4\varepsilon/L-nh^2}{n}}
\]

from all its existing anchors. Charge the failure to that coordinate.
Charged insertions in its bounded interval are pairwise more than
\(\delta\) apart. At most
\(\sum_i(1+\lfloor s_i/\delta\rfloor)\) charges are possible.
Uncharged insertions only make future distances smaller. This is a crude
packing bound with inverse-square-root accuracy dependence; it does not
give the fast rate proved using growth and small optimal projections.

### Removing knowledge of the growth constant

The validity test does not use \(g\). Knowledge of \(g\) can be removed
by restarting ratios \(\theta_m=2^{-m-1}\) under doubling budgets for
grid construction, table entries, and DP operations. At a sufficiently
large budget, one admissible ratio completes the finite run bounded above.
For example, in round \(r\ge1\), run indices \(0\le m<r\), each with operation
budget \(2^r\), enforced before work is performed. If admissible trial
\(m^*\) requires at most \(W^*\) operations, every round
\(r^*\ge\max\{m^*+1,\lceil\log_2 W^*\rceil\}\) is sufficient.
The total work is at most \(2r^*2^{r^*}\). This is a logarithmic overhead
relative to the maximum of the successful work bound and \(2^{m^*}\).
One may absorb the latter into a coarser upper bound containing
\(\theta_{m^*}^{-p}\). Nonunit oracle costs must be budgeted or stated
separately.

The growth assumption toward \(S\) remains substantive: a distant local
minimum whose value is almost global can make \(g\) very small. The method
also depends on valid global curvature bounds and exact shared grids.
Arbitrary coupled constraints are excluded, for the reasons proved in the
[constraint barrier](../geometric-dp/constraint-barrier.md).

Coordinate projections can be large even for a low-dimensional optimal
manifold, and different coordinate systems can have very different covering
numbers. An arbitrary rotation can destroy sparse factorization. No free
change of coordinates or invariant choice of metric is claimed here.

The mathematical ingredients—geometric grids, interpolation bounds,
coordinatewise distance estimates, and finite-state DP—are established.
The candidate contribution is their use in a certified discovery algorithm
whose progress is charged to optimal coordinate values or covering nets.
A literature audit is required before making a priority claim.

### Rational grid denominators

Fixed \(h\) and \(\theta\) simplify rational arithmetic. If
\(\theta=2^{-r}\), every source-grid offset before clipping is
\(h\sum_{\ell=0}^{k-1}(1+2^{-r})^\ell\), with \(k\le q_0\).
All offsets therefore have a common denominator dividing
\(\operatorname{den}(h)2^{rq_0}\). A new anchor is an old anchor plus
or minus one such offset, or an original domain endpoint. Induction gives
a fixed common coordinate denominator, independent of the number of
anchor additions. Its bit length is
\(O(b+\operatorname{bits}(h)+rq_0)\), where \(b\) bounds the rational
input endpoint and initial-anchor bit lengths.

Thus rational polynomial factors of numerically bounded degree admit the
same type of common-denominator table and message bounds established in
the earlier grid extension. Together with (12), this gives polynomial bit
work at fixed width and polynomially bounded conditioning and optimal
projection complexity. Exact real-function oracles and binary-encoded
unbounded polynomial degrees are not covered by that statement.

## 10. Verification status

A separate Astra agent derived the finite-optimum version. A fresh Astra
agent adversarially checked the stronger coordinate-projection charge,
including the union-grid inequality, parameter constants, finite-state
extension, and total-table-count requirement. It then checked the compact-set
net argument, exact-integer corollary, and conditional-margin obstruction;
no substantive error was found. The root agent also checked the fixed
denominator argument and incremental grid-construction count.

Targeted command run:

`python3 research-20261002/new-direction/projection_anchor_checks.py`

All checks use exact rational arithmetic. Nine continuous double-well runs
at three accuracies and three initial centers certified a gap within the
requested tolerance, with at most two failed solves and at most 131 final
grid nodes. An integer double well on `[-1024,1024]` certified an exact
optimizer after two failed solves, using 513 final nodes instead of all
2,049 integer values. Six pairs of irregular grids passed the diagonal
conditional-margin obstruction. The script also checks the union mesh bound
and the charged-distance contraction in its one-dimensional runs. These are
targeted corroborating examples, not a performance study or proof of the
general theorem. No project-wide or CI checks were run.
