# Independent check of noisy grids on products of unit simplexes

Date: 2026-10-02. Scope: geometric rounding, conditional expected bag-state
counts, original-face forcing, and the finite-noise active-multiplier tail
for the proposed simplex extension. The final exact convex evaluator is
outside this review. No external search was used.

**Verdict.** The proposed facewise probability cancellation is valid for
joint near-optimal bag states. Conditioning on one noise coefficient for
each saturated simplex face leaves exactly the independent coefficients
needed to match its dimension. A triangulation is unnecessary: simplex-
clipped grid cubes give the required rounding and nesting with exponential,
rather than factorial, dependence on the scalar bag dimension.
The three original-face forcing rules are sound and become complete under
strictly positive active multipliers. The multiplier tail follows by
counting transformed noise tuples; it does not require those transformed
coordinates to be independent.

## 1. Assumptions needed by the count

The domain is a product of disjoint blocks

\[
 \Delta_b=\{x\in\mathbb R^b:x_i\ge0,\ \sum_i x_i\le1\}.
\]

Each supplied decomposition bag contains whole blocks, and has at most
\(p\) scalar coordinates in total. Let \(n\) be the total scalar dimension.
The base objective has the verified bound
\(\nabla^2_{bb}F_0\preceq LI\) on every block, uniformly over the full
product domain, with \(L>0\). This is a joint block bound; separate upper
bounds on its diagonal entries alone do not suffice for the exchange
directions used below.

The perturbed objective is \(F_\gamma=F_0+\gamma^Tx\). Its ambient
scalar noise coefficients are independent uniform variables on
\([-\sigma,\sigma]\), or independent uniform draws from \(M\) equally
spaced points in that interval. The finite-law interval probability is
at most \(w/(2\sigma)+1/M\) for an interval of length \(w\).

All probability counts sum over the deterministic full grid, conditional
only on specified noise coefficients. They do not condition on an adaptive
pruning history.

## 2. Clipped cubes avoid a triangulation requirement

At mesh \(h=2^{-j}\), use block cells

\[
 C=\Delta_b\cap\prod_i[hk_i,h(k_i+1)],\qquad
 k_i\in\{0,\ldots,2^j-1\}.
 \tag{1}
\]

Keep the nonempty cells; boundary-only cells can alternatively be omitted
when already covered by adjacent cell closures. After putting
\(z_i=x_i/h-k_i\), a cell has the form

\[
 0\le z_i\le1,\qquad \sum_i z_i\le r,
 \qquad r=2^j-\sum_i k_i\in\mathbb Z.
 \tag{2}
\]

Every vertex of (2) is a zero-one vector. Otherwise a vertex has at most
one coordinate not fixed by a coordinate bound; the sum inequality must
then be active, and its integral right-hand side makes that remaining
coordinate integral as well. Thus all cell vertices belong to
\(\Delta_b\cap h\mathbb Z^b\), and there are at most \(2^b\) of them.

Every point of a cell is a convex combination of its vertices. Choosing
a vertex with those coefficients therefore gives mean-preserving rounding
\(\mathbb E Y=x\). Each scalar coordinate lies at the two endpoints of
an interval of width \(h\), so its variance is at most \(h^2/4\).
Consequently,

\[
 \mathbb E\|Y-x\|^2
 =\sum_i\operatorname{Var}(Y_i)\le b h^2/4.
\]

Correlations within a block do not enter this trace bound. Before the
physical mesh reaches one, rounding the whole simplex to its vertices
has the same bound, because every coordinate lies in \([0,1]\) and
\(h\ge1\).

Dyadic subdivision gives at most \(2^b\) children per cell. A grid node
belongs to at most \(2^b\) cells, because it belongs to at most that many
ambient grid cubes. Intersecting nested cubes with the same simplex keeps
the nesting. These bounds multiply to \(2^p\) for bag cells made from
products of block cells.

This provides the geometric properties needed by sparse cell-whitelist
DP without enumerating a simplex triangulation. An arbitrary triangulation
would need its own incidence and refinement bounds.

## 3. Rounding and conditional value functions

Joint block semiconcavity gives

\[
 \mathbb E F_\gamma(Y,x_{-b})
 \le F_\gamma(x)+\tfrac L2\mathbb E\|Y-x_b\|^2.
\]

Round the blocks independently, applying this inequality successively.
The resulting global error is at most

\[
 E_j=\tfrac18nLh^2.
 \tag{3}
\]

The same rounding preserves any specified bag cell. Shared nested block
cells also preserve all earlier bag-cell whitelists: every rounded block
vertex stays in the chosen fine cell and its ancestors. This is the
specific feasible-rounding property needed here; it does not authorize
arbitrary coupled constraints.

Shared boundaries cause no inconsistency. Mean-preserving rounding of a
point on a supporting face uses vertices on that face: a nonnegative
slack with expectation zero vanishes almost surely. In particular, an
original simplex facet or a grid-coordinate boundary remains fixed under
the relevant rounding. The rounded point therefore also stays in every
specified containing cell at a shared boundary.

The existing sparse bag-cell argument then supplies, for each retained
cell, a globally consistent witness corner with objective at most
\(f^*+2E_j\). For a bag \(B\), condition on noise outside \(B\) and
define

\[
 V_B(u)=\min_{x_{-B}\text{ in the original product domain}}
                 [F_0(u,x_{-B})+\gamma_{-B}^Tx_{-B}].
 \tag{4}
\]

Because bags contain whole blocks, the outside feasible set is independent
of \(u\). Subtracting \(L\|u_b\|^2/2\) for one block leaves an infimum
of concave functions of that block. Hence \(V_B\) has the same block
semiconcavity and is independent of every noise coefficient inside \(B\).
Every retained-cell witness therefore belongs to the deterministic set
of bag nodes satisfying

\[
 V_B(u)+\gamma_B^Tu\le f^*+\eta,
 \qquad \eta=2E_j=nLh^2/4.
 \tag{5}
\]

This reduction uses joint bag min-marginals and complete witnesses. Products
of separately retained block lists do not automatically satisfy (5).

## 4. Original simplex faces give the right independent coordinates

Fix a deterministic bag node \(u\). In each block let \(I\) be the
support of its positive coordinates.

If \(\sum_i u_i<1\), the original simplex face has dimension \(|I|\).
Every positive coordinate and the remaining slack are positive integer
multiples of \(h\). Thus both \(u\pm h e_i\) are feasible for each
\(i\in I\).

If \(\sum_i u_i=1\), its original face has dimension \(|I|-1\).
Choose a fixed anchor \(j\in I\), for example its least index. For each
\(i\in I\setminus\{j\}\), both
\(u\pm h(e_i-e_j)\) are feasible. A vertex has dimension zero and
requires no comparison.

For either direction \(d\), condition (5) and comparison with the two
feasible neighbors imply

\[
 \frac{V_B(u)-V_B(u+hd)-\eta}{h}
 \le\gamma_B^Td\le
 \frac{V_B(u-hd)-V_B(u)+\eta}{h}.
 \tag{6}
\]

The interval's length is at most

\[
 Lh\|d\|^2+2\eta/h
 \le(2+n/2)Lh.
 \tag{7}
\]

For an unsaturated face, these constrain the independent \(\gamma_i\).
For a saturated face, condition additionally on \(\gamma_j\) and then
read them as intervals for the remaining independent \(\gamma_i\),
since \(\gamma^T(e_i-e_j)=\gamma_i-\gamma_j\). Condition on all
inactive-coordinate noise as well. Do this separately for every block
in the bag. All remaining coordinates are still mutually independent.
The interval endpoints depend only on the fixed node, outside-bag noise,
and the chosen anchor coefficients, not on the other remaining noise.

Thus a bag node in a product face of dimension \(r\) has conditional,
and hence unconditional, probability at most

\[
 \left[\frac{(2+n/2)L}{2\sigma}h+\frac1M\right]^r
 \tag{8}
\]

of satisfying (5), omitting \(1/M\) for continuous noise. The anchor
selection must be determined by the fixed node's face, not by the noise.

## 5. Counting nodes, cells, and the finite-law atoms

Put \(N=1/h\). A fixed original simplex face of dimension \(r_b\)
has exactly \(\binom{N-1}{r_b}\) grid nodes in its relative interior,
with the usual zero count if \(r_b>N-1\). For a face containing the
origin this counts positive integer coordinates with total at most
\(N-1\); for a saturated face it counts positive compositions of \(N\).
In either case it is at most \(h^{-r_b}\).

A product face of total dimension \(r\) therefore has at most
\(h^{-r}\) nodes. Multiplying by (8) cancels the mesh powers. A
\(b\)-dimensional simplex has \(2^{b+1}-1\) nonempty faces, so a bag
has at most \(4^p\) product faces. Writing
\(A=(2+n/2)L/(2\sigma)\), a safe expected node bound is

\[
 4^p\max\{1,A+(Mh)^{-1}\}^p.
 \tag{9}
\]

For a preselected terminal level \(J\), choosing \(M\ge2^J\)
makes \((Mh)^{-1}\le1\) at every processed level. Equation (9) is then
at most \([C(1+nL/\sigma)]^p\) for an absolute constant \(C\).
The vertex-incidence, child, and corner bounds from Section 2 contribute
only additional absolute factors to the power \(p\). The finite-noise
resolution must be fixed from a valid terminal-level analysis; an arbitrary
fixed coarse noise grid does not give an accuracy-independent count.

The actual algorithm must generate sparse child lists from retained parent
cells and use joint bag min-marginals, as in the box theorem. Counting
surviving nodes does not justify first enumerating the full fine grid.
Subject to that implementation, the simplex geometry and noise independence
introduce no defect in the proposed expected state bound.

## 6. Original-face forcing and completeness

Let a rational coordinate hull contain every original optimizer. The
three strict tests in the main note are sound, with each sign verified
throughout that hull:

- If \(\partial_jF>0\), a positive \(x_j\) permits a small decrease
  with negative directional derivative. Thus every optimizer has \(x_j=0\).
- If \(\partial_jF<0\) for some \(j\), a slack budget permits a small
  increase in that coordinate. Thus every optimizer has tight budget.
- If \(\partial_iF-\partial_jF>0\), a positive \(x_i\) permits a
  small transfer from \(i\) to \(j\) with negative directional
  derivative. Thus every optimizer has \(x_i=0\).

Evaluate each sign at an original optimizer. The descent need only be
feasible in the original simplex, and need not remain in the artificial
hull. The argument works independently in every block, with native
integers held fixed.

At an optimizer \(a\), write

\[
 \partial_iF(a)+\lambda_B-\lambda_i=0,
 \qquad \lambda_B,\lambda_i\ge0.
 \tag{10}
\]

The active original normals are independent. For a slack budget they
are coordinate normals. For a tight budget the additional all-ones
normal has a nonzero coordinate on the nonempty positive support, where
all active coordinate normals vanish.

For a slack budget, every active multiplier \(\lambda_i>\tau\)
gives \(\partial_iF(a)>\tau\). For a tight budget choose any positive
coordinate \(j\). Its derivative is \(-\lambda_B\), so
\(\lambda_B>\tau\) triggers the second test. A zero coordinate has
\(\partial_iF(a)-\partial_jF(a)=\lambda_i>\tau\), triggering the
third test. The algorithm may test every pair, so it need not identify
this anchor beforehand. Its positive coordinate can be arbitrarily
small: only an arbitrarily short feasible direction is needed. There
is no missing lower bound on positive coordinates.

Write \(A_0=2+nL/g_0\). If the coordinate hull lies within distance
\(A_0h\) of the optimizer in every coordinate, midpoint derivative
enclosures from the full Hessian row-sum bound \(M_1\) differ from
the optimizer's derivative by at most \(2M_1A_0h\), and derivative-
difference enclosures by at most \(4M_1A_0h\). Therefore
\(h\le\tau/(8M_1A_0)\) makes every required sign strict.
The bound \(M_1\) must hold on the ambient coordinate box: its midpoint
and other hull points can lie outside the simplex. The main note now
makes this domain explicit.

On the good event, forcing identifies the optimizer's smallest original
product face. Point growth gives
\(Z^TH(a)Z\succeq2g_0Z^TZ\) on its tangent space: apply growth
along both signs of a tangent direction and send the step to zero.
This also requires no quantitative distance to that face's boundary.
It checks the curvature input to the matrix test; the final exact convex
evaluator remains outside this review.

## 7. Finite-noise multiplier tail by counting tuples

Fix an integer assignment and an original product face, with \(k\)
free continuous coordinates. Put \(N=n_c\). In a tight block with
positive support \(S\), select a fixed anchor \(j\) and transform

\[
 \eta_i=\gamma_i-\gamma_j\ (i\in S\setminus\{j\}),
 \qquad \zeta_B=\gamma_j,
 \qquad \zeta_i=\gamma_i\ (i\notin S).
 \tag{11}
\]

For slack blocks, the positive-support coefficients are tangent noise
and the zero-coordinate coefficients are normal noise. The joint map
is unimodular, hence injective. On a tight face the linear noise becomes
\(\gamma_j+\sum_{i\in S\setminus\{j\}}\eta_i x_i\). Thus normal
coefficients affect only a constant or vanish, and the free stationarity
system depends only on tangent noise, even when the objective couples
blocks.

At a positive-growth optimizer the tangent Hessian is nonsingular by
Section 6. For fixed tangent noise, there are at most \(D^k\) such
stationary roots, where \(D=\max\{1,d-1\}\). The isolated-root bound
counts all nonsingular roots, including when other components of the
same polynomial system are positive-dimensional. For \(k=0\) there
is one empty root; for degree one and \(k>0\), positive growth excludes
a stationary relative-interior optimizer.

For a fixed root and all other normal labels, each active multiplier
has slope \(1\) or \(-1\) in a selected remaining normal label:

\[
 \begin{aligned}
 \lambda_i&=\partial_iF_0(a)+\gamma_i
   &&\text{(slack budget, zero coordinate)},\\
 \lambda_B&=-\partial_jF_0(a)-\gamma_j
   &&\text{(tight budget)},\\
 \lambda_i&=\partial_iF_0(a)-\partial_jF_0(a)+\gamma_i-\gamma_j
   &&\text{(tight budget, zero coordinate)}.
 \end{aligned}
 \tag{12}
\]

This fixes transformed labels, without asserting a product conditional
law. Let \(s\le k\) count tangent difference coordinates. There are
at most \((2M-1)^sM^{k-s}\) tangent tuples and \(M\) labels for
each normal coefficient. For a fixed tangent tuple, one of its at most
\(D^k\) roots, and the other normal labels, the slab
\(|\lambda|\le\tau\) permits at most
\(B_\tau=\tau(M-1)/\sigma+1\) labels of the selected coefficient.
Its grid spacing is \(2\sigma/(M-1)\) and the interval length is
\(2\tau\). Counting tuples with no feasible preimage in the original
noise cube only enlarges this upper bound. Dividing by \(M^N\) gives

\[
 \begin{aligned}
 \Pr\{\text{positive growth and }|\lambda|\le\tau\}
 &\le \frac{(2M-1)^s M^{k-s}D^kM^{N-k-1}B_\tau}{M^N}\\
 &\le 2^kD^k\left(\frac\tau\sigma+\frac1M\right).
 \end{aligned}
 \tag{13}
\]

An active multiplier entails \(N-k\ge1\). Noise on integer
coordinates can be conditioned on throughout: at a fixed integer
assignment it adds only a constant to the continuous objective. The
bound is uniform in that conditioning.

A \(b\)-simplex has \(2^{b+1}-1\le3^b\) nonempty faces. Union
bounding over product faces, at most \(2n_c\) original continuous
facets, and \(R_Z\) integer assignments gives the stated safe factor

\[
 K=\max\{1,2n_cR_Z3^{n_c}(2D)^{n_c}\}.
 \tag{14}
\]

Positive growth is part of the counted event; no step conditions the
noise distribution on that event. Mixed tight and slack faces across
multiple coupled blocks introduce no additional independence assumption.

## Verification status

The derivation was checked directly, including mixed saturated and
unsaturated faces across different blocks, finite-law atoms, and the
distinction between joint witnesses and separate block lists.

An inline `python3 - <<'PY'` command using exact fractions passed 143
clipped-cell checks and 168 original-face counts in block dimensions one
through four. It checked lattice vertices, rounded-point distances,
child counts, and node incidence. A second part used the bag
\(\Delta_2\times\Delta_1\), three mesh levels, and five independent
noise values per coordinate. Its conditional value function was the
minimum of two coupled quadratic branches with the same block curvature
bound. All 99 bag nodes, 958 near-optimal events, and 900 conditional
probability-group checks passed. The reference near-optimal events used
the exhaustive grid minimum; the neighbor implications remain necessary
for this larger event, so the diagnostic checks the asserted containment
and independence calculation without assuming a continuous optimizer.
That diagnostic used the previous, looser allowance \(E_j=nLh^2/2\).
The sharper constants now stated follow from the exact coordinate-variance
calculation. The diagnostic was not rerun and is not claimed as a check
of those sharper numerical constants.

A scoped `git diff --check` and an inline Python whitespace and paired-
math-delimiter check passed. The added forcing and multiplier-tail proofs
were checked algebraically, including every type of active simplex facet
and the dependence between transformed noise labels. This review does not
duplicate the final exact convex evaluator. No external search,
project-wide verification, or CI inspection was used.
