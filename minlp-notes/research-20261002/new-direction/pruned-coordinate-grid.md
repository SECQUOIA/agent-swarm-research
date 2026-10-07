# Min-marginal filtering removes the accuracy exponent from coordinate grids

Date: 2026-10-02. Status: candidate theorem with independent mathematical and
bit-complexity reviews finding no substantive gap and targeted exact
dynamic-programming checks passing. The interpolation bound,
min-marginal filtering, rational
reconstruction, and finite-state dynamic programming are established tools.
The proposed contribution is their conditioning-dependent complexity bound;
the external prior-art audit is separate.

## 1. Result

Consider a rational mixed-integer box quadratic program

\[
 \min_{x\in X}F(x),\qquad X=\prod_{i=1}^n X_i,
\]

where each factor of the quadratic objective is assigned to a bag of a
supplied tree decomposition. Let \(p\) be the largest bag size, \(N\) the
number of bags, and \(I\) the total binary input length. An individual
variable may occur in arbitrarily many bags. Each \(X_i\) is a bounded
continuous interval or its intersection with the integers. Round integer
endpoints inward, reject empty domains, and eliminate fixed coordinates.
The case with no remaining coordinate is immediate.

Let \(L>0\) be a known bound on the upper coordinate curvature:

\[
 t\longmapsto F(x_1,\ldots,t,\ldots,x_n)-Lt^2/2
 \quad\hbox{is concave for every fixed choice of the other coordinates.}
\tag{1}
\]

For a quadratic, take the largest positive diagonal entry of its Hessian.
This bound concerns the summed objective, not an individual bag Hessian.
If all Hessian diagonal entries are nonpositive, endpoint DP solves the
problem exactly with at most two states per coordinate, without a growth
assumption.

Assume a unique optimizer \(x^*\), write \(f^*=F(x^*)\), and suppose

\[
 F(x)-f^*\ge g\|x-x^*\|^2\qquad(x\in X)
\tag{2}
\]

for some \(g>0\). Put \(\kappa=\max\{1,L/g\}\). The condition is on
the actual mixed domain; nearly tied integer assignments can make \(g\)
small even when the continuous extension is strongly convex.

**Theorem.** There is a deterministic algorithm that returns a rational
feasible point and a rational certificate with gap at most \(2^{-q}\) in

\[
 f(p,\kappa)(I+q+1)^C
\tag{3}
\]

bit operations, for an absolute constant \(C\). It does not require \(g\)
or \(\kappa\) as input. There is also an exact algorithm for the unique
optimizer and optimum value in \(f_1(p,\kappa)(I+1)^{C_1}\) bit operations,
with an absolute \(C_1\). Certificate validity does not depend on the
growth assumption.

Thus the parameters are bag size and the coordinate-curvature/growth ratio.
There is no occurrence parameter, no full-Hessian norm parameter, and no
accuracy exponent depending on bag size. This is not FPT in width alone.
The [finite-mode corollary](pruned-grid-finite-modes.md) permits tied
fully enumerated modes outside the growth metric. In particular, ordinary
QP coordinates with nonpositive Hessian diagonal may become two-endpoint
modes; only the remaining coordinates then need projected growth.
As proved in [exact-box-qp.md](../geometric-dp/exact-box-qp.md), a rational
quadratic with a unique optimizer on a compact mixed box always has some
positive \(g\). The algorithm therefore terminates on every such instance;
the quantitative ratio governs its running time.

The arithmetic argument below applies more generally to exactly evaluable
coordinate-semiconcave factor objectives, but the bit and exact-output
claims in (3) concern rational quadratics.

## 2. Corrected grids and conditional lower bounds

Maintain a product box \(B\subseteq X\), with the same integer/continuous
coordinate types, that contains every global optimizer. Choose a feasible
center \(c\in B\), a base mesh \(h>0\), and \(0<\theta\le1/4\).
In each coordinate start at \(c_i\), build outward, and clip at the current
domain endpoints. At distance \(t\) from the center, the continuous step is
\(h+\theta t\). The integer step is \(\max\{1,\lfloor h+\theta t\rfloor\}\).
All resulting grid points are feasible.

For a grid node \(v\in G_i\), let \(\ell_i(v)\) be its largest adjacent
interval length. For integer coordinates ignore adjacent intervals of
length one, and use zero if none remain. Define

\[
 d_i(v)=L\ell_i(v)^2/8,\quad D(y)=\sum_i d_i(y_i),\quad
 Q(y)=F(y)-D(y),\quad b=\min_{y\in\prod_iG_i}Q(y).
\tag{4}
\]

The interpolation lemma from the
[coordinate-grid theorem](../geometric-dp/theorem.md) gives

\[
 b\le \min_{x\in B}F(x)=f^*,\qquad F(y)-b=D(y)
\tag{5}
\]

for a minimizer \(y\) of \(Q\). It independently rounds each coordinate
of \(x\) to its enclosing grid endpoints, preserving its mean. The summed
upper-curvature error is at most the expected unary correction in (4).
For an integer coordinate a unit interval has no feasible interior, which
justifies omitting its correction.

Compute the exact coordinate min-marginals

\[
 m_i(v)=\min\{Q(y):y_i=v,\ y\in\prod_kG_k\}.
\tag{6}
\]

**Conditional interpolation lemma.** For adjacent grid nodes \(a,b\),

\[
 \min\{m_i(a),m_i(b)\}\le F(x)
 \quad\text{for every }x\in B\text{ with }x_i\in[a,b].
\tag{7}
\]

Indeed, the same independent rounding has its \(i\)-th coordinate in
\(\{a,b\}\), so its corrected expectation is bounded below by the
left side of (7) and above by \(F(x)\). The argument also includes an
endpoint or an integer unit interval.

Two passes of min-sum DP compute (4), a minimizing assignment, and all
min-marginals (6). Assign each unary correction once to a containing bag.
For each bag, sum its assigned factors and incoming directed-tree messages;
minimizing this calibrated bag table over every coordinate except \(i\)
gives (6) for any containing bag. Accumulate child messages by sums and
exclusions, avoiding a product over children. With at most \(K\) grid
points per coordinate, the work is

\[
 O\bigl(p(N+\#\mathrm{factors})K^p\bigr)
\tag{8}
\]

table operations, up to ordinary indexing factors depending on \(p\).
No separate global DP is needed for each variable or each grid node.

## 3. Safe domain filtering

Maintain a nonincreasing feasible upper bound \(U\), together with the
feasible incumbent point realizing it. After finding \(y\), replace
\(U\) by \(\min\{U,F(y)\}\) and update its stored point when needed.
Retain the adjacent interval
\([a,b]\) of coordinate \(i\) exactly when

\[
 \min\{m_i(a),m_i(b)\}\le U.
\tag{9}
\]

Replace that coordinate's domain by the hull of its retained intervals.
For a singleton domain retain that singleton. The next center is \(y\).

Every global optimizer survives: (7) bounds its containing intervals by
\(f^*\le U\). Also every coordinate of \(y\) survives, since
\(m_i(y_i)\le Q(y)=b\le f^*\le U\). Thus the next center is feasible in
the new box without a projection step. Taking interval hulls can reintroduce
points from discarded interior intervals; this only weakens filtering and
preserves correctness.

The retained certificate includes all filtering stages, not just the final
grid. Each removed point belongs to a removed coordinate interval at the
stage it is first excluded. Equation (7) proves that its value exceeds that
stage's \(U\), hence the final nonincreasing upper bound. Together with the
last DP lower bound, these records certify a bound on the original box.
Neither the filter nor this verification uses \(g\).

## 4. Contraction survives restriction

Put \(s=\max_i(b_i-a_i)>0\) for the original box and \(h_j=s2^{-j}\).
At stage \(j\), use the filtered box from the previous stage and center
\(c=y_{j-1}\); at stage zero choose any rational feasible center, for
example the lower endpoint vector. The mesh inequality is unchanged:

\[
 \ell_i(v)\le h_j+\theta|v-c_i|.
\tag{10}
\]

Assume for analysis that

\[
 \theta^2\le 1/(8\kappa),\qquad
 B_0=\max\{1,4L/(11g)\}\le\kappa.
\tag{11}
\]

Because the restricted box still contains \(x^*\), the original contraction
proof applies without change. If \(E_j=\|y_j-x^*\|^2\), then

\[
 E_j\le\frac{4L}{15g}nh_j^2+\frac{E_{j-1}}{15},\quad
 E_j\le B_0nh_j^2,\quad
 D(y_j)\le\frac{7L}{8}nh_j^2.
\tag{12}
\]

For clarity, (10) implies, for any grid assignment \(z\),

\[
 D(z)\le\frac L4nh_j^2+
          \frac{L\theta^2}{2}
             \bigl(\|z-x^*\|^2+\|c-x^*\|^2\bigr).
\tag{13}
\]

Use \(gE_j\le F(y_j)-f^*\le D(y_j)\), absorb the first distance term,
and induct with \(h_{j-1}=2h_j\). The initial distance is at most \(ns^2\).
This gives (12) by precisely the argument in the coordinate-grid theorem.
In particular the incumbent satisfies

\[
 U_j-f^*\le 7Lnh_j^2/8.
\tag{14}
\]

## 5. Filtering bounds the next grid independently of accuracy

For a retained interval, choose an endpoint \(v\) with \(m_i(v)\le U_j\).
There is a complete grid assignment \(z\) attaining that min-marginal.
Using (13), (14), and \(\|c-x^*\|^2\le4B_0nh_j^2\), quadratic growth gives

\[
 \begin{aligned}
 g\|z-x^*\|^2
 &\le D(z)+U_j-f^*\\
 &\le\frac{9L}{8}nh_j^2+
       \frac{L\theta^2}{2}
       \bigl(\|z-x^*\|^2+4B_0nh_j^2\bigr).
 \end{aligned}
\]

Consequently

\[
 \|z-x^*\|^2
 \le\left(\frac{6L}{5g}+\frac{4B_0}{15}\right)nh_j^2
 \le\frac{22}{15}\kappa nh_j^2.
\tag{15}
\]

In particular the qualifying endpoint lies within
\((\sqrt{22/15}+1)\sqrt{n\kappa}\,h_j\) of the new center coordinate
\((y_j)_i\). For a continuous interval its entire length is at most

\[
 h_j+\theta|v-c_i|
 \le h_j+\theta(\sqrt{22/15}+2)\sqrt{n\kappa}\,h_j.
\]

Since \(\theta\sqrt\kappa\le1/\sqrt8\), every retained interval,
and therefore its coordinate hull, lies within

\[
 5\sqrt{n\kappa}\,h_j
\tag{16}
\]

of \((y_j)_i\). For an integer coordinate the actual adjacent length
can be one even when its corrected length is zero. Its corresponding
radius is bounded by

\[
 1+5\sqrt{n\kappa}\,h_j.
\tag{17}
\]

This additive one cannot be omitted: an interval joining a good integer
node to its bad neighbor can survive because of the good endpoint.

At the next stage use \(h_{j+1}=h_j/2\). Continuous grids have an outward
step count bounded by

\[
 1+\left\lceil
 \frac{\log(1+\theta R/h_{j+1})}{\log(1+\theta)}
 \right\rceil,
\]

where \(R\) is the distance to the relevant endpoint. For integer grids
replace the denominator by \(\log(1+\theta/3)\) and the base mesh inside
the numerator by \(H=\max\{h_{j+1},1\}\). This standard recurrence bound
is proved in the coordinate-grid theorem. Equations (16)--(17) imply in
both cases that the numerator is at most \(\log(2+8\sqrt n)\).
Thus a safe common bound on the **total** grid nodes per coordinate is

\[
 K(\theta,n)=100\theta^{-1}\lceil\log_2(n+2)\rceil.
\tag{18}
\]

Stage zero has at most three nodes per coordinate, since \(h_0=s\).
Unlike a grid covering the original box at every stage, (18) has no
dependence on \(j\), the domain diameter, or the requested accuracy.

Taking the \(p\)-th power of a logarithm in \(n\) does not prevent FPT:
for a constant \(C_0\),

\[
 \lceil\log_2(n+2)\rceil^p\le(C_0p)^p(n+2).
\tag{19}
\]

For example, apply \(\sup_{t\ge0}t^pe^{-t}=(p/e)^p\), absorbing the
change of logarithm base and the ceiling. This absorption would fail for
the old factor \((I+q)^p\); it succeeds here because \(n\) is already
part of the ordinary input-size factor and the bound is uniform in \(p\).

## 6. Unknown growth and stage-count control

Let

\[
 J=\max\left\{0,\left\lceil\frac12
       \log_2\frac{7Lns^2}{8\varepsilon}\right\rceil\right\}.
\tag{20}
\]

Rational comparisons against powers of four compute this integer without
an exact transcendental oracle. For a trial indexed by \(\mu=2,3,\ldots\),
set \(\theta=2^{-\mu}\), restart from the original domain, and run stages
zero through \(J\), stopping as soon as the verified gap is at most
\(\varepsilon\). During grid generation, abort the trial if any coordinate
would exceed the cap (18). Do not allocate its DP tables first.

This cap is necessary for the claimed FPT analysis: an inadmissibly coarse
earlier trial might fail to filter its domains and otherwise incur an
accuracy factor to the power \(p\). Every trial remains mathematically
sound; aborting only prevents excessive work.

The first \(\mu\) with \(2^{-2\mu}\le1/(8\kappa)\) satisfies
\(2^\mu\le6\sqrt\kappa\), passes the cap by (18), and succeeds by
stage \(J\). Earlier trial work is bounded by the geometric sum of their
capped state spaces and arithmetic costs. The number of stages is
\(O(I+q+1)\), independently of \(p\) and \(\kappa\), because the
quantities in (20) have polynomial input bit length.

Approximate termination itself does not require growth or uniqueness.
For a sufficiently small trial \(\theta\le h_J/s\), every corrected
interval length at stage \(J\) is at most \(2h_J\), so the returned gap
is at most \(Lnh_J^2/2\le4\varepsilon/7\). Continuous grids through that
stage have at most \(s/h_j+3\) nodes; integer grids have at most
\(2s/h_j+3\) when \(h_j\ge1\), and at most \(s+2\) when \(h_j<1\).
These counts fit (18), so such a trial cannot abort. Without growth this
can be exponentially costly in the accuracy bits. Growth proves the FPT
rate.

## 7. Rational arithmetic and exact output

After substituting fixed coordinates, choose a common positive denominator
\(D\) for all resulting rational coefficients, remaining endpoints, and
\(L\). Substitution and this denominator have polynomial bit complexity;
the new coefficients may have denominators absent before substitution.
Within a fixed trial, let \(K=K(\theta,n)\) and \(\theta=2^{-\mu}\).
The \(k\)-th unclipped continuous outward distance is

\[
 h_j\frac{(1+\theta)^k-1}{\theta}
 =h_j\frac{(2^\mu+1)^k-2^{\mu k}}{2^{\mu(k-1)}}.
\tag{21}
\]

Since \(s\) has denominator dividing \(D\) and \(k\le K\), all stage
\(j\) nodes have denominator dividing

\[
 A_j=D2^{j+\mu K}.
\tag{22}
\]

This follows by induction: previous centers and retained endpoints have
denominator dividing \(A_{j-1}\), which divides \(A_j\); a new displacement
also has denominator dividing \(A_j\). Integer steps and floors preserve
integrality. Clipping selects an inherited endpoint. Denominators do not
multiply with the number of stages.

All quadratic factor values, unary penalties, messages, and min-marginals
have denominator dividing \(8DA_j^2\). Summing factors or messages changes
numerators without introducing additional denominators. Their bit lengths
are polynomial in \(I+j+\mu K\): all nodes stay in the original bounded
box, and input magnitudes and factor counts bound the numerators. Combined
with (8), (18)--(20), and \(2^\mu=O(\sqrt\kappa)\), this proves (3) with
an absolute polynomial exponent. The same estimates bound the stored
filtering-history certificate and its exact verification time.

The exact-output step uses the rational-height lemma from
[exact-box-qp.md](../geometric-dp/exact-box-qp.md). It supplies computable
denominator bounds \(R\) on the unique optimizer and \(V\) on the optimum
value, with \(\log R,\log V\) polynomial in \(I\). Refine until the
certified value interval isolates one rational of denominator at most
\(V\), and reconstruct that value by continued fractions. As precision
increases, growth forces the feasible points toward \(x^*\); eventually
coordinate reconstruction recovers its denominator-bounded coordinates.
Check box membership, integrality, and exact equality to the isolated
optimal value. These checks certify the output without knowing \(g\).

Concretely, run the certified approximate solver at
\(\varepsilon=2^{-q}\) for \(q=1,2,4,8,\ldots\). Once the gap is at
most \(1/(4V^2)\), reconstruct the unique denominator-at-most-\(V\)
value in the interval. For each coordinate of the feasible incumbent use
the reconstruction window of radius \(1/(4R^2)\), returning failure for
that attempt if it contains no rational of denominator at most \(R\).
Such a window contains at most one candidate. Check the complete candidate
in the original box, including integrality, and evaluate its objective
exactly. Accept only if that value equals the isolated optimum.

This succeeds once

\[
 \varepsilon\le
 \min\{1/(4V^2),\ g/(32R^4)\}.
\tag{23}
\]

Indeed, growth then puts the feasible incumbent within
\(1/(\sqrt{32}R^2)<1/(4R^2)\) of \(x^*\) in Euclidean norm. The
required exponent is \(\operatorname{poly}(I)+O(\log\kappa)\), using
\(g\ge L/\kappa\). Doubling \(q\) overshoots it by at most a factor
of two and preserves the FPT bound. The height constants come from the
original quadratic program, not the refined hull endpoints. This uses no
discrete objective gap between arbitrary feasible continuous points.

## 8. Scope of the advance and remaining audit

This result concerns the shared-coordinate point-grid algorithm. It does
not repair the previous overlapping-cell affine-message certificate;
the occurrence-sensitive drift and isotropic-curvature counterexamples to
that certificate remain valid. Its mechanism is classical safe domain
filtering combined with a growth-dependent bound on the surviving domain.

The main substantive implication, if the remaining audits hold, is an exact
mixed-integer solver capability under supplied bounded width and bounded
coordinate-curvature/growth ratio, with an input and accuracy exponent
independent of width. The constant may still be large, and global quadratic
growth can be weak on difficult near-tie instances. No comparable speed
bound is claimed on unpromised instances or for coupled feasible
constraints. Practical dominance has not been established.

Review records: [independent mathematical review](pruned-grid-adversary.md)
and [arithmetic/mixed-domain audit](pruned-grid-bit-audit.md). Prior-art
priority is not asserted by this note.

## 9. Targeted verification

The actual two-pass junction-tree DP, all coordinate min-marginals, grid
construction, interval filtering, and hull recentering are implemented in
[check_pruned_grid.py](check_pruned_grid.py). The command run was

```sh
python research-20261002/new-direction/check_pruned_grid.py > research-20261002/new-direction/check_pruned_grid-results.json
```

The [saved results](check_pruned_grid-results.json) pass nine instances,
70 refinement stages, 26,589 bag-table states, and 526 pruned intervals.
Fixtures include non-grid interior optima, a nonconvex nine-variable fan,
a branching ten-variable star, mixed and unit integer domains, aspect
ratio 1,024, singleton grids, and empty separators. Two stages explicitly
have a corrected-grid minimizer whose true objective is worse than the
saved incumbent, testing retention of both points.

Every stage checks the global objective bracket, the known-growth
contraction and gap bounds, and retention of the optimizer, incumbent,
and next center. On instances with at most five variables, a separate
full active-face enumeration verifies the global optimizer. The larger
fixtures have independently proved analytic optima and growth constants.

Separately, exhaustive finite-grid enumeration verifies all coordinate
min-marginals across nine selected case grids and one explicit two-bag
trace, totaling 21,034 assignments. This comparison is not repeated at
every adaptive stage. The saved trace contains all local tables, both
directed messages, and every min-marginal. Independent code review found
no substantive implementation error.

The checker does not implement unknown-growth trial caps, rational
reconstruction, or a standalone verifier for stored pruning history;
those parts are covered by the mathematical and arithmetic reviews, with
the reconstruction ingredients also developed and checked in the earlier
exact-QP work. Scoped syntax, whitespace, local-link, and result-JSON
checks passed. No project-wide verification or CI inspection was run.
