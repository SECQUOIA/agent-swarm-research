# Pruned coordinate grids with fully enumerated finite modes

Date: 2026-10-02. Status: direct corollary of the
[pruned coordinate-grid theorem](pruned-coordinate-grid.md) and the
[finite-state extension, Section 6](../geometric-dp/extensions.md).
This note checks the additional scope and exact-output argument; it makes
no separate novelty claim.

## 1. Model and conclusion

Partition the variables into gridded coordinates \(x\) and finite modes
\(z\). Each gridded coordinate has a bounded continuous interval or a
bounded integer interval. Their product domain \(X\) is independent of
\(z\). Every mode has an explicitly listed finite domain, whose elements
may be categorical labels without a numerical metric.

Let \(\mathcal Z\) be the allowed mode assignments. It may impose local
forbidden combinations involving only modes. Supply a tree decomposition
covering the scopes of every objective factor and every such feasibility
relation. If \(A_t\) and \(B_t\) index the gridded coordinates and modes
in bag \(t\), the objective is

\[
 \min_{x\in X,\ z\in\mathcal Z} F(x,z),\qquad
 F(x,z)=\sum_t f_t(x_{A_t},z_{B_t}).
 \tag{1}
\]

For the bit and exact-output claims, each local mode combination selects
an explicitly supplied rational quadratic in the gridded coordinates of
that factor. Forbidden combinations may instead be marked infeasible.
The input length \(I\) includes all these local tables, coefficients,
domains, relations, and the supplied decomposition. No implicit succinct
encoding of a factor's exponentially large mode table is assumed.

Let \(P\) be the largest full bag size, including both variable types,
and let \(d\) be the largest individual mode-domain size, taking \(d=1\)
if no modes remain. Suppose a known rational \(L>0\) bounds upper
coordinate curvature in \(x\), uniformly over feasible mode assignments:
for each coordinate \(i\), with the other coordinates and \(z\) fixed,

\[
 t\longmapsto F(x_1,\ldots,t,\ldots,x_{n_x},z)-Lt^2/2
 \quad\text{is concave on the continuous interval.}
 \tag{2}
\]

Write \(f^*\) for the global optimum. Assume one vector \(x^*\) and
some \(g>0\) satisfy the projected growth condition

\[
 F(x,z)-f^*\ge g\|x-x^*\|_2^2
       \qquad(x\in X,\ z\in\mathcal Z).
 \tag{3}
\]

Thus every optimum has the same gridded vector \(x^*\); any number of
mode assignments can be optimal there. There is no distance penalty on
mode labels and no required positive gap between tied modes.

**Corollary.** Put \(\kappa=\max\{1,L/g\}\). A rational feasible pair
and a valid certificate of gap at most \(2^{-q}\) can be computed in

\[
 f(P,d,\kappa)(I+q+1)^C
 \tag{4}
\]

bit operations, for an absolute constant \(C\). An exact optimal pair and
the exact value can be computed in \(f_1(P,d,\kappa)(I+1)^{C_1}\),
with absolute \(C_1\). The algorithm need not know \(g\), and certificate
validity does not depend on growth. The returned mode assignment need not
be a prescribed member of the optimal set.

First check \(\mathcal Z\ne\varnothing\) by finite-state feasibility DP,
round integer endpoints inward, reject empty coordinate domains, and
substitute fixed coordinates. If \(n_x=0\), one exact finite-state DP
solves the problem, with no curvature, growth, or grid schedule. If a
uniform upper-curvature bound \(L\le0\) is available, use the two endpoints
of each remaining gridded coordinate and all mode states; separate
concavity makes this finite DP exact without (3).

No constraint or mode-dependent domain involving \(x\) is added by this
corollary. Those changes would need a separate feasible-rounding proof.

## 2. Only the gridded coordinates are filtered

Use exactly the grid construction, mesh schedule, unary correction, and
trial cap from the main theorem, with \(n_x\) in place of \(n\). Keep
every allowed mode value in each bag. At a stage define

\[
 D(y)=\tfrac L8\sum_{i=1}^{n_x}\ell_i(y_i)^2,
 \qquad Q(y,z)=F(y,z)-D(y).
 \tag{5}
\]

Compute its global minimum, a minimizing pair \((y,\widehat z)\), and
the gridded-coordinate min-marginals

\[
 m_i(v)=\min\{Q(y,z):y_i=v,
                  \ y\text{ is a grid vector},\ z\in\mathcal Z\}.
 \tag{6}
\]

For any feasible pair \((x,z)\), round only \(x\), keeping \(z\) fixed.
The common domain and mode-only feasibility relations preserve feasibility
under every rounding outcome. The interpolation proof therefore gives
a global lower bound and, for adjacent nodes \(a,b\),

\[
 \min\{m_i(a),m_i(b)\}\le F(x,z)
       \quad\text{whenever }x_i\in[a,b].
 \tag{7}
\]

Store a feasible incumbent pair \((x^{\rm inc},z^{\rm inc})\) whose value
is the current upper bound \(U\), updating it when
\(F(y,\widehat z)<U\). Retain intervals whose bound in (7) does not
exceed \(U\), take their hulls, and recenter at \(y\). No mode-domain
filtering is required. The saved
conditional bounds certify the regions removed from the original box,
as in the main theorem.

The only modification to its growth argument is the replacement of
\(F(y)-f^*\) by \(F(y,\widehat z)-f^*\). Equation (3) bounds exactly
the same gridded-coordinate distance. A retained interval has a complete
grid-and-mode witness \((u,z')\) with \(Q(u,z')\le U\), so (3) also
gives the same witness-distance bound. Consequently its entire hull lies
within

\[
 5\sqrt{n_x\kappa}\,h
 \quad\text{of the new center, or}\quad
 1+5\sqrt{n_x\kappa}\,h
 \quad\text{for an integer coordinate}.
 \tag{8}
\]

The integer additive one has the same role as in the main proof: a unit
interval can survive through a good endpoint despite having zero unary
correction. The effective integer grid step \(\max\{h,1\}\) absorbs it.

Thus the admissible trial still uses at most

\[
 K=100\theta^{-1}\lceil\log_2(n_x+2)\rceil
 \tag{9}
\]

grid points per gridded coordinate at every stage. The same generation cap
keeps unsuccessful trials within this bound, and the same unknown-growth
search terminates. Ties among optimal modes change none of these estimates.

## 3. The table count records both variable types

For bag \(t\), let \(p_t\) count its gridded coordinates and put

\[
 d_t=\prod_{z_j\in V_t}|\mathcal Z_j|.
\]

Its table has at most \(d_tK^{p_t}\) entries; forbidden entries can be
skipped. Two directed passes give the minimum and all min-marginals (6).
A conservative per-stage table-work bound, excluding separately counted
factor evaluation costs, is

\[
 O\left(P\sum_t(1+\deg_T(t))d_tK^{p_t}\right).
 \tag{10}
\]

Child states are summed through messages, not multiplied across children.
When infeasible entries are represented by \(+\infty\), incoming-message
exclusions can use a sum of finite entries and a count of infinite entries;
they need not form an undefined \(+\infty-(+\infty)\).

Equation (10) gives a more informative bound than charging every variable
the larger of a mode-domain size and a grid size. For the uniform FPT
claim, use \(d_t\le d^P\), \(p_t\le P\), and

\[
 \lceil\log_2(n_x+2)\rceil^P\le(C_0P)^P(n_x+2).
\]

Mode-only bags have \(p_t=0\); their work can repeat in each stage and
trial. The stage count and number of trials already cover those repetitions
in (4). In a bound retaining each \(d_t\) separately, their trial count
must be included rather than absorbed into a nonexistent geometric factor
\(\theta^{-p_t}\).

Conditional mode choices introduce no new denominator mechanism. Choose a
common denominator after fixed-coordinate substitution, covering every
resulting rational table coefficient, the remaining endpoints, and \(L\).
Substitution has polynomial bit cost but can introduce coefficient
denominators absent from the original tables. For a fixed
trial the grid denominator and all finite message denominators therefore
obey the main theorem's bounds, uniformly over selected modes. Table lookup,
quadratic evaluation, and symbolic infeasibility tests have the required
polynomial bit cost. Equations (9)--(10) prove (4).

For these quadratic tables, the supplied uniform \(L\) can also be checked
without enumerating complete mode assignments. For each gridded coordinate,
maximize its summed Hessian diagonal over the mode-only feasibility model
by finite-state DP, then compare to \(L\). The local diagonal tables have
scopes already covered by the supplied bags.

## 4. Uniform rational heights do not enumerate global modes

Write each local quadratic, for a fixed local mode combination, in the
convention \(x^TQ_{t,z}x+b_{t,z}^Tx+a_{t,z}\), with symmetric \(Q_{t,z}\).
After fixed-coordinate substitution, let \(D\) be a common positive
denominator for all resulting finite local table coefficients, remaining
box endpoints, and \(L\), including the factor of two needed to represent
off-diagonal monomials symmetrically. Its binary length is polynomial in
the explicit input length.

For each factor choose

\[
 C_t=\max_{\text{listed finite local modes}}\max_{i,j}
                 |D(Q_{t,z})_{ij}|,
 \qquad C=\max\{1,\sum_t C_t\}.
 \tag{11}
\]

An empty quadratic matrix contributes zero. These bounds are computed by
reading local input tables. For every feasible complete mode assignment,
its assembled integral quadratic matrix has entries of magnitude at most
\(C\), and every assembled coefficient has denominator dividing \(D\).
Neither this conclusion nor computing (11) requires enumerating complete
mode assignments. Both \(\log D\) and \(\log C\) are polynomial in \(I\).

Choose an optimal mode assignment \(z^*\) for the existence argument.
The rational mixed-box quadratic \(F(\cdot,z^*)\) has the unique minimizer
\(x^*\), by (3). The rational-height lemma in
[the exact box-QP proof](../geometric-dp/exact-box-qp.md) therefore gives
the uniform bounds

\[
 R=D(2n_xC)^{n_x},\qquad V=DR^2:
 \tag{12}
\]

the coordinates of \(x^*\) share a denominator at most \(R\), and
\(f^*\) has reduced denominator at most \(V\). In brief, fix its integer
coordinates and active continuous bounds, then apply Cramer's rule to
the nonsingular free continuous Hessian. Every determinant is bounded by
\((2n_xC)^{n_x}\). The fixed integer coordinates have input-bounded
encoding length. Fixing \(z^*\) and those integers is an existence proof,
not a step of the algorithm.

The value-denominator bound remains available without the growth promise:
choose an optimal mode and apply the minimum-face form of the same height
lemma. This matters because certificate acceptance should not trust an
unknown growth constant.

## 5. Exact recovery chooses an optimal mode after recovering the coordinates

Use the main theorem's precision schedule \(q=1,2,4,\ldots\), including
its capped unknown-growth trials. Isolate the unique rational value of
denominator at most \(V\) in a sufficiently narrow global objective
interval. It is \(f^*\). Use the bounded-denominator reconstruction test
near the gridded component \(x^{\rm inc}\) of the saved feasible incumbent
pair whose objective equals \(U\), then check the candidate vector
\(\widehat x\) for box membership and required integrality. The current
corrected-grid minimizer can have objective greater than \(U\), so the
certified gap must be applied to the saved incumbent.

Fix \(\widehat x\) and run one exact finite-state DP minimizing
\(F(\widehat x,z)\) over \(z\in\mathcal Z\). Accept its returned pair
only if its rational objective equals the isolated \(f^*\). This test
is sound without growth and allows any tied optimal mode assignment.

For a certified gap at most \(2^{-q}\), projected growth gives
\(\|x^{\rm inc}-x^*\|^2\le2^{-q}/g\). Thus increasing the requested
precision forces the saved incumbent's gridded component toward the unique
\(x^*\), so coordinate reconstruction eventually succeeds.
At that vector the final mode DP has value exactly \(f^*\). The necessary
precision is polynomial in \(I+\log\kappa\), and (12) has polynomial
binary length. Rational evaluation at \(\widehat x\) and the final mode
DP obey the same uniform bit and full-width bounds. This proves the
exact-output part of the corollary without selecting or identifying a
particular optimal mode in advance.

## 6. Nonpositive-diagonal coordinates can become endpoint modes

For an ordinary rational box QP, any coordinate whose Hessian diagonal is
nonpositive can be restricted to its two box endpoints and treated as a
finite mode. This applies to continuous coordinates and to integer
coordinates with arbitrarily large bounded ranges. For a quadratic whose
coefficients depend on existing modes, require that diagonal to be
nonpositive for every feasible mode assignment.

To prove the reduction, fix all other coordinates and modes. The objective
is concave in the selected coordinate, so one endpoint has objective no
larger than its current value. Repeating this replacement for each selected
coordinate never increases the objective. For every fixed assignment of
the remaining coordinates and original modes, the minimum over selected
coordinates is therefore attained at their endpoint choices. The reduced
problem has exactly the original optimum value, and any reduced optimizer
is feasible for the original problem. This is the standard endpoint
argument for a separately concave objective; no new endpoint theorem is
claimed.

Only the remaining gridded coordinates appear in (3). If every nonpositive-
diagonal coordinate of an ordinary QP is replaced, these are exactly the
coordinates with positive Hessian diagonal, after fixed-coordinate
removal. It suffices to assume projected growth on the
reduced endpoint model; endpoint choices may tie freely. Their numerical
ranges affect coefficient bit length but their state count is at most two.
If no gridded coordinates remain, finite-state DP is exact without growth.

Replacing a coordinate by an endpoint label preserves its bag incidences
and the full bag size. Each original local factor can be evaluated at
endpoint combinations as needed, or expanded into at most \(2^P\) local
tables. Thus the reduction preserves the stated FPT bound, with mode-domain
parameter \(\max\{d,2\}\). All substituted coefficients still have
polynomial encoding length. If \(D_0\) clears the original quadratic
coefficients and endpoints, \(D_0^3\) clears every coefficient produced by
endpoint substitution, uniformly over all endpoint choices; this also
preserves the polynomial-bit height bounds without global enumeration.

## Verification status

This note reuses the main theorem's grid, filtering, and arithmetic checks;
it does not assert a new implementation or duplicate those tests. A fresh
review found the additional mode feasibility, projected growth, table
count, uniform height bound, and reconstruction arguments sound. Its scope
and arithmetic qualifications are included above. An exact-artifact read
also identified the need to choose common denominators after fixed-value
substitution, now stated explicitly. The endpoint specialization applies
the existing separate-concavity reduction. The targeted commands
actually run were `git diff --check -- research-20261002/new-direction/pruned-grid-finite-modes.md`
and an inline `python3 - <<'PY'` document check. Both passed; the latter
checked trailing whitespace, paired inline and displayed math delimiters,
and all three local Markdown links. No external search,
knowledge-base access, project-wide verification, or CI inspection was
performed.
