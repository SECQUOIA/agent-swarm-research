# Exact TU-constrained quadratic optimization with nonunique minimizers

Date: 2026-10-03. This note extends the deterministic TU filtered-grid
algorithm in two ways: exact output no longer requires a unique minimizer,
and keeping unions of surviving cells gives an accuracy-independent state
bound when each coordinate has finitely many optimal values. The number of
global optimizers may be exponential. The recovery lemma and rational
height mechanism are imported from earlier work; the contribution here is
their safe composition with feasible TU grids and the union-state bound.

## 1. Model and result

Use the model, integral data, supplied decomposition, and verifiable
continuous Hessian upper bound \(L>0\) of
[the TU algorithm](../../constraints/tu-filtered-grid.md):

\[
 X=\{(x,z):l\le x\le u,\ z_i\in Z_i,\ Ax+Bz\le b\},
 \qquad F(v)=\tfrac12v^THv+c^Tv+c_0.                 \tag{1}
\]

Here \(A\) is totally unimodular, the continuous bounds and \(B,b\) are
integral, and each \(Z_i\) is an explicitly listed finite set of integers.
The Hessian and objective coefficients are rational. All objective factors
and constraint rows fit in bags of size at most \(p\). Let \(n_c\) denote the
number of nonfixed continuous coordinates, \(d=\max(1,\max_i |Z_i|)\),
\(W=\max_{i\text{ continuous}}(u_i-l_i)\), \(I\) the complete input encoding,
and \(T\) the number
of bags plus factors and rows. The objective is allowed to be indefinite.
Empty instances can be detected by the initial grid DP. Assume below that
\(X\) is nonempty. Fixed coordinates are eliminated first.

Let \(S=\arg\min_X F\) and \(f^*=\min_X F\). No growth bound or optimizer is
supplied. Every such quadratic has some \(g>0\) satisfying

\[
 F(v)-f^*\ge g\operatorname{dist}(v,S)^2\quad(v\in X). \tag{2}
\]

This is the classical quadratic error bound on each optimal polytope
slice, combined with the positive gaps of the finitely many other integer
slices. It establishes existence only. Write \(\kappa=\max(1,L/g)\) when
describing complexity; the algorithm never uses it.

**Theorem 1 (arbitrary optimal sets).** A deterministic algorithm returns
an exact rational optimizer and exact optimum value for (1). Its finite
certificate is valid independently of (2): it contains the unconditional
TU-grid lower-bound history, a rational-height bound, and the returned
feasible point. The algorithm also works when \(S\) contains a continuum.
This statement alone makes no favorable bound on intermediate grid sizes.

**Theorem 2 (finitely many coordinate values).** Suppose each continuous
projection \(S_i=\{x_i:(x,z)\in S\}\) has at most \(r\) elements, with \(r\ge1\).
The same algorithm has table work

\[
 O\!\left(pT\,[K_0^p+(J+1)K^p]\right),\qquad
 K_0=\max\{d,W+1\},\quad
 K=\max\{d,r(5+\lceil2\sqrt{n_c\kappa}\rceil)\},       \tag{3}
\]

with polynomial rational-arithmetic overhead of absolute exponent, where
\(J=\operatorname{poly}(I)+O(\log\kappa)\) for exact output. For an additive
gap \(2^{-q}\), one may use \(J=O(I+q+1)\). Neither \(r\) nor \(g\) is required
as input. There can be as many as \(r^{n_c}\prod_i |Z_i|\) distinct optimizers.
The finite-projection hypothesis excludes positive-dimensional continuous
optimal components; Theorem 1, without its grid-size bound, still allows them.

Equation (3) is an XP-width result. It is not FPT in \((p,\kappa,r)\):
the global feasible-rounding error leaves a factor \(n_c^{p/2}\). The
initial capacity dependence is unchanged. The earlier aligned-mesh
variant also applies, with its explicitly stated initial grid cost.

If \(n_c=0\), ordinary finite-label DP solves the problem exactly. In that
case no growth, height reconstruction, or recovery step is needed.

## 2. Retain unions, not their hulls

At level \(j\), use the uniform mesh \(h_j=2^{-j}\). Each current continuous
domain is a finite union of closed mesh-aligned intervals, together with
possible singleton nodes. Form its entire set of mesh nodes. Start from
the original interval. Discrete domains are retained subsets of the
original lists.

Compute the exact feasible grid minimum \(v_j\), an attaining point \(y_j\),
and all coordinate min-marginals \(M_i(t)\) by the two-pass DP from the
parent TU algorithm. Use

\[
 E_j=n_cLh_j^2/8,\qquad U_j=v_j,\qquad b_j=v_j-E_j.    \tag{4}
\]

For each continuous coordinate, retain the **union** of adjacent mesh
cells contained in its current domain for which

\[
 \min\{M_i(a),M_i(b)\}-E_j\le U_j.                  \tag{5}
\]

Keep a singleton node if its own marginal passes the same test. Merge
overlapping or touching retained intervals only; do not fill gaps between
different components. For each discrete coordinate retain a label exactly
when its marginal minus \(E_j\) is at most \(U_j\). Refine the resulting
domains on the mesh \(h_j/2\).

The finite-tree DP needs no change beyond its supplied coordinate-label
lists. Disconnected domains do not add factors or enlarge scopes. The
retained domain is stored as a sorted list of intervals/nodes of size at
most its current grid list. Forming and merging it costs linear work once
the sorted labels and marginals are available.

For a feasible point in the retained domain, its surrounding uniform
cell is contained in the same retained component in every coordinate.
The parent TU cell-integrality argument therefore supplies a feasible
mean-preserving corner distribution in that domain, with expected
objective at most \(F(x,z)+E_j\). Connectedness of the full coordinate
domain was never needed. This proves

\[
 b_j\le f^*\le U_j\le f^*+E_j,                     \tag{6}
\]

and proves the validity of every removal in (5). Every global optimizer
and the grid incumbent survive. An incumbent from an earlier level is
still on the next grid, so \(U_j\) is nonincreasing. Save all removed-cell
decisions and finite messages; their replay certifies the lower bound for
the original feasible domain, exactly as in the parent algorithm.

## 3. State count around all optimal projections

An endpoint \(t\) passing (5), or a retained discrete label, has a feasible
grid witness \(w\) with

\[
 F(w)=M_i(t)\le U_j+E_j\le f^*+2E_j.
\]

By (2), some optimizer \(s\) obeys

\[
 \|w-s\|\le a_j:=\sqrt{n_cL/(4g)}h_j.               \tag{7}
\]

In particular \(\operatorname{dist}(t,S_i)\le a_j\). Every point of a
retained adjacent cell is within \(h_j\) of at least one passing endpoint,
hence the entire retained continuous domain is contained in

\[
 \bigcup_{s\in S_i}[s-a_j-h_j,\ s+a_j+h_j].           \tag{8}
\]

At spacing \(h_j/2\), an interval in (8) contains at most
\(5+\lceil2\sqrt{n_cL/g}\rceil\) grid nodes. Taking the union over at most
\(r\) optimal projection values gives (3); overlaps only reduce the count.
This argument does not associate different coordinates with one common
optimizer, nor enumerate any optimal combinations. The witnesses in (7)
may approach different components. Keeping the union is essential: the
hull of neighborhoods around separated optimal values can retain
\(\Omega(1/h_j)\) nodes even when \(r=2\).

## 4. Exact output without guessing growth or an optimal component

Use the original-data height and slack constants in
[the general-polytope recovery lemma](../../../research-20261002/new-direction/proximal-polytope-recovery.md),
Sections 2--4. That result gives explicitly computable positive rationals
\(\delta,\tau\) and a positive integer \(V\), each of polynomial binary length,
with the following properties:

1. The reduced denominator of \(f^*\) is at most \(V\).
2. Given a feasible \(y\) with \(\operatorname{dist}(y,S)\le\delta\), fix its
   integer labels, select the original scaled inequality rows whose slacks
   are at most \(\tau\), and impose those rows as equalities. Solve linear
   feasibility for the original inequalities, the fixed labels, and
   stationarity along the selected face. It is feasible, and every feasible
   output is a global optimizer.

Stationarity here means membership of \(Hv+c\) in the span of selected
row normals and integer-fixing rows. Its multipliers are **unrestricted**;
this is not an assertion of global sufficiency for ordinary KKT points.
The imported proof uses a bounded stationary polytope, common vertex
denominator bounds, and simultaneous slack snapping. No nondegeneracy,
positive-definite free Hessian, or unique optimizer is required.

To apply it to explicit integer lists, put each integer coordinate inside
the interval from its smallest to largest allowed label when forming the
analysis polytope. During recovery fix it to the actual allowed label in
\(y\). The proof only compares points in that one fixed-label slice, which
is exactly a feasible slice of (1); omitted labels create no new points
in that slice. The finite-slice growth and height arguments are likewise
unchanged. This observation extends the lemma's consecutive-integer-box
notation, not its recovery mechanism.

The algorithm proceeds as follows once (4) is available.

1. If \(E_j\ge1/(4V^2)\), refine.
2. Otherwise isolate the unique reduced rational with denominator at
   most \(V\) in \([b_j,U_j]\). It exists and equals \(f^*\) by the height
   bound and (6). Rational reconstruction uses polynomial bit work;
   distinct such rationals differ by at least \(1/V^2\).
3. Form the selected-face linear system from \(y_j\) and the fixed original
   threshold \(\tau\). If it is infeasible, refine. If it is feasible, obtain
   any rational feasible solution \(s\).
4. Check every original constraint and label membership and the exact
   rational equality \(F(s)=f^*\). Accept only if all checks pass. If an
   equality check fails, refine.

Every acceptance is sound because (6) is unconditional and the final
point attains the isolated global value. Premature snapping can be
infeasible or return a nonglobal stationary point, but it cannot cause a
false acceptance. Neither a guessed growth constant nor the recovery
lemma's distance premise is trusted by the verifier.

For termination, (6) and (2) give
\(\operatorname{dist}(y_j,S)^2\le E_j/g\). Thus all recovery outputs are
optimal once

\[
 E_j<1/(4V^2),\qquad E_j\le g\delta^2.               \tag{9}
\]

The algorithm need not detect the second inequality. Since \(E_j\) tends
to zero and some positive \(g\) exists, it eventually succeeds even for a
continuum of minimizers. The thresholds have polynomial binary length
and \(g\ge L/\kappa\), so (9) holds by
\(J=\operatorname{poly}(I)+O(\log\kappa)\). Under finite projections,
combine this level bound with (3). General rational LP returns a
polynomial-height feasible solution even when the multiplier lift has
lineality. Large denominators of \(y_j\) are used only in the row-selection
comparisons; they are not substituted into the recovery coefficients.

The exact certificate records the reconstructed value's height-isolating
interval and the final feasible point. Replaying the stationary LP is
unnecessary for soundness: it is the discovery method, while objective
equality with the isolated optimum is the acceptance proof.

## 5. Example: exponentially many optima and a genuine hull penalty

For each independent block use \(0\le x,t,z\le1\), the TU equality \(x+t=z\),
and

\[
 F_b(x,t,z)=(2x-z)^2+\tfrac14z(1-z).                 \tag{10}
\]

Both terms are nonnegative. Its two optimizers are \((0,0,0)\) and
\((1/2,1/2,1)\). On the feasible equality, put \(w=x-z/2\). For \(z\le1/2\),
the squared distance to the first optimizer is \(2w^2+3z^2/2\), while
\(F_b\ge4w^2+z^2/4\); the symmetric calculation holds above \(1/2\).
Therefore \(F_b\ge\operatorname{dist}((x,t,z),S_b)^2/6\). A full-Hessian
bound is \(L=12\) by the maximum absolute row sum. For \(m\) independent
blocks, \(g=1/6\) and \(L=12\) still work, \(p=3\), every coordinate has
two optimal values, and there are \(2^m\) optimizers.

The hull algorithm keeps every \(z\) value between 0 and 1 forever because
both endpoint optima must survive. Its \(z\) grid has \(2^j+1\) labels.
The union algorithm eventually deletes the middle and has a bounded
number of labels at each later level by (3). This example demonstrates
the state-representation distinction. Its explicit nonnegative objective
also makes it easy for specialized methods; no general speedup claim is
drawn from it.

## 6. Prior results and verification

TU feasible rounding, exact tree DP, and rational reconstruction are
classical mechanisms already used by the parent note. The stationary-face
recovery is proved in the imported companion and is not reproved as a new
result here. Qualitative set growth comes from Luo and Sturm,
[*Error Bounds for Quadratic Systems*](https://link.springer.com/chapter/10.1007/978-1-4757-3216-0_16),
Theorem 3.3, whose primary-source statement is recorded in the repository's
[source note](../../../literature/papers/luo2000-error-bounds-for-quadratic-systems/paper.md).

The added results are the union-preserving feasible filtration, the bound
for finitely many optimal coordinate values, and exact acceptance with
no supplied growth constant on the full TU quadratic class. The general
FPT problem for arbitrary unknown optimal sets remains open.

The targeted command actually run was

```sh
python3 -B research-20261002-decomposition/completion/theory/check_nonunique_tu.py
```

It passed three exact block-family runs (1, 4, and 16 blocks), each through
13 mesh levels; 67 feasible mean-preserving corner distributions in
disconnected TU domains, including 54 cases with positive rounding error;
and one adversarial premature-recovery rejection. At level 12, each family
had six retained `z` grid labels, while a hull must contain 4,097. The
script evaluates this separable family directly; these are state-count
diagnostics, not timings of the reusable constrained solver. Its
[saved results](nonunique-tu-results.json) include every level.

In the rejection example, `F(x,t)=x-x^2` on `x=t`, `0<=x,t<=1`, has global
value zero. Selecting only the equality at `(1/2,1/2)` produces a feasible
stationary point with value `1/4`; the isolated global-value equality
correctly prevents acceptance. This checks the reason that ordinary
stationarity is not the exact-output certificate.

The [independent review](reviews/nonunique-tu-review.md) checks the union
rounding, recovery import, constants, and complexity. No project-wide
verification or CI inspection was run. The finite diagnostics do not
replace the proof or establish empirical superiority.
