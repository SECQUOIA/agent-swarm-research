# Finite optimum sets: filtered unions help, but anchor compression remains open

Date: 2026-10-02. Status: a direct positive bound for uniform filtered
grids and a counterexample to one proposed anchor-count argument. The
stronger width-parameterized theorem stated below remains open. No external
search or priority claim is made.

## 1. Which parameter would make the extension substantive?

Use the product-domain, coordinate-upper-curvature \(L>0\), and sparse
factorization assumptions of the
[pruned coordinate-grid theorem](pruned-coordinate-grid.md). Replace its
unique optimizer by a finite nonempty optimal set \(S\), and assume

\[
 F(x)-f^*\ge g\operatorname{dist}(x,S)^2,
 \qquad \kappa=\max\{1,L/g\}.
 \tag{1}
\]

Write

\[
 S_i=\pi_i(S),\quad a_i=|S_i|,\quad
 A=\sum_i a_i,\quad a=\max_i a_i.
\]

Since \(A\ge n\), a bound \(f(p,A,\kappa)\operatorname{poly}(I+q)\)
already permits exponential dependence on dimension. Also
\(|S|\le\prod_i a_i\le3^{A/3}\). Thus that parameterization alone
does not establish a sparse improvement over a full-dimensional
quadratic-growth branch-and-bound argument. Purely continuous rational
box QP already admits exact active-face enumeration exponential in \(n\).

A stronger target is

\[
 f(p,a,\kappa)\operatorname{poly}(I+q),
 \tag{2}
\]

with an absolute polynomial exponent. This permits exponentially many
complete optima while keeping only a few optimal values per coordinate.
The [earlier anchor algorithm](projection-anchors.md) has polynomial work
in \(A,I,q\) at fixed width, but its accuracy exponent grows with width.

## 2. A simple positive result using uniform filtered unions

Keep each coordinate domain as a union of retained intervals, rather than
taking one hull across all surviving intervals. Start with a dyadic
\(h_0\) at least the largest original side length and use
\(h_j=h_0 2^{-j}\). For a continuous coordinate, use the lattice of
spacing \(h_j\) anchored at its original lower endpoint, clipped to its
current interval union. For an integer coordinate use spacing
\(H_j=\max\{1,h_j\}\). Integer spacings are integral powers of two until
they reach one. Include the original upper endpoint when clipping requires
it.

These meshes are nested. Refine retained cells only; each continuous cell
has at most two children, and an integer unit cell is left unchanged.
Define adjacency and the correction using intervals **inside retained
components**. Do not connect the last node of one component to the first
node of another across a removed gap. Isolated retained points have zero
adjacent width.

As usual, ignore integer unit intervals in \(\ell_i(v)\), and define

\[
 D(y)=\tfrac L8\sum_i\ell_i(y_i)^2,
 \qquad Q(y)=F(y)-D(y).
\]

Every corrected interval has width at most \(h_j\), so

\[
 0\le D(y)\le\tfrac18Ln h_j^2
 \quad\text{at every grid assignment.}
 \tag{3}
\]

The independent-rounding proof works within the component containing each
coordinate of a feasible point. Exact DP therefore gives a valid lower
bound \(b_j=\min Q\) and a feasible incumbent with

\[
 U_j-f^*\le U_j-b_j\le\tfrac18Ln h_j^2.
 \tag{4}
\]

Compute all coordinate min-marginals and retain an interval \([u,v]\)
exactly when \(\min\{m_i(u),m_i(v)\}\le U_j\). Keep their union.
The main theorem's conditional-rounding proof preserves all optima and
certifies every excluded point. It needs neither the anchors nor \(g\).

A retained interval has an endpoint \(v\) and a witnessing grid assignment
\(y\) with \(y_i=v\) and \(Q(y)\le U_j\). Equations (1), (3), and
(4) give

\[
 g\operatorname{dist}(y,S)^2
 \le U_j-f^*+D(y)\le\tfrac14Ln h_j^2.
\]

Thus its endpoint lies within \(\tfrac12\sqrt{n\kappa}\,h_j\) of
\(S_i\). Its entire interval lies within

\[
 \left(1+\tfrac12\sqrt{n\kappa}\right)h_j
 \quad\text{for a continuous coordinate,}
\]

or \(H_j+\tfrac12\sqrt{n\kappa}\,h_j\) for an integer coordinate.
At the next mesh, both radii divided by the appropriate lattice spacing
are at most \(2+\sqrt{n\kappa}\). Packing lattice points in the union
of these neighborhoods gives

\[
 K_i\le 8a_i(1+\sqrt{n\kappa})
 \tag{5}
\]

as a safe bound on the next coordinate grid size. Original clipped
endpoints only change the constant. Stage zero has at most two nodes per
coordinate.

Consequently the per-stage table work is bounded, up to bag-index factors,
by

\[
 O\left(\sum_t(1+\deg_T(t)+m_t)
             \prod_{i\in V_t}8a_i(1+\sqrt{n\kappa})\right),
 \tag{6}
\]

where \(m_t\) counts factors assigned to bag \(t\). In particular this
is at most \(f(p) (N+M)a^p(n\kappa)^{p/2}\) per stage. There are
\(O(I+q+1)\) stages to achieve gap \(2^{-q}\), using rational comparisons
of (4). The algorithm needs no growth estimate or failed-parameter trials.

For rational quadratics, all grid coordinates have a common denominator
dividing \(D2^j\), where \(D\) clears all coefficients after fixed-coordinate
substitution, the remaining endpoints, and \(L\). Quadratic values,
penalties, and finite DP messages
have denominator dividing \(8D^3 2^{2j}\). Their bit lengths are
polynomial in \(I+j\), with an absolute exponent. Hence this construction
removes the width-dependent accuracy exponent of the earlier anchor
algorithm. It still has an \(n^{p/2}\) factor, so it does **not** prove
(2). Substituting \(n\le A\) gives the weaker requested FPT bound in
\((p,A,\kappa)\), subject to the significance qualification above.

## 3. Why qualifying nodes cannot simply become a few fine anchors

Consider the separable convex quadratic

\[
 F(x)=\sum_{i=1}^n x_i^2,\qquad x\in[-1,1]^n.
\]

Here \(S=\{0\}\), \(a=1\), \(L=2\), \(g=1\), and \(\kappa=2\).
Take an aligned uniform grid of spacing \(h\), containing zero and the
box endpoints. Every node has \(\ell_i=h\), so

\[
 D(y)=nh^2/4,
 \qquad m_i(v)=v^2-nh^2/4.
 \tag{7}
\]

The incumbent is \(U=0\). Therefore every grid node with

\[
 |v|\le\tfrac12\sqrt n\,h
 \tag{8}
\]

qualifies for the filter. If the displayed interval stays inside the box,
there are \(\Theta(\sqrt n)\) qualifying nodes per coordinate. Covering
all of them to a constant multiple of mesh accuracy requires
\(\Omega(\sqrt n)\) anchors, despite one optimal coordinate value.

This is actual slack in the corrected certificate, not merely a loose
distance estimate. It rules out proving (2) by assuming that all
qualifying coordinate nodes admit an \(O(a)\)-size fine cover. It does
not obstruct a better algorithm: the unique-point theorem handles this
example with one common center.

Keeping every qualifying endpoint also gives a useful but insufficient
coordinate-cover observation. If the old anchor grid obeys
\(\ell_i(v)\le h+\theta\operatorname{dist}(v,C_i)\), an interval
containing an optimal coordinate has a retained endpoint. Adding all such
endpoints moves that coordinate within its interval width of the new
anchor set. The unresolved step is compressing these endpoints without
losing the aggregate error control needed for the next solve. Coarse
merging can introduce another factor of \(n\) in that control, while
fine packing encounters (7)--(8).

## Verification record

An independent exploration obtained the uniform-union bound and the
separable counterexample, and checked the integer-mesh and component-
adjacency qualifications. This is a mathematical derivation, not an
implementation of the filtered DP. An inline `python3 - <<'PY'` command
used exact fractions to check (7)--(8) in dimensions 4, 16, 64, 256, and
1,024 at mesh width \(1/128\). All 1,285 min-marginal identities and the
five qualifying-node counts passed. A scoped `git diff --check` and a
second inline Python check of whitespace, math delimiters, and the two
local Markdown links also passed. No external search,
knowledge-base access, project-wide verification, or CI inspection was
performed.
