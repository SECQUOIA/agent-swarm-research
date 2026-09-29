# Independent review: finite-grid perturbations and exact penalties

Date: 2026-09-25. This review verifies the originally proposed supporting-normal
chart proof, whose constant is quadratic in residual dimension. The final
[main note](smoothed-penalty.md) uses a stronger coordinate-fiber argument and
a centered-cell grid; that proof is checked separately in
[the second review](smoothed-penalty-review-second.md). The qualifications and
counterexamples below apply to both versions where indicated.

The original theorem and its chart proof pass review. Two additional reviewers
independently checked the geometry. No novelty certification is asserted.

## Statement checked

There are at most K nonempty compact convex native slices X_z, with K ≥ 1.
On each slice f is continuous and convex, and L ≤ f ≤ U throughout. The
same fixed affine map A takes values in R^m, with m ≥ 1; write C_z = A X_z.
The slices, maps, objectives, and bounds are fixed independently of sampled b.

Let σ > 0, 0 < ε < 1, and sample each coordinate of b independently from the
N-point endpoint grid spanning [b_0j − σ,b_0j + σ]. Choose

\[
 N\ge4mK/\varepsilon,\qquad d=\sigma\varepsilon/(4m^2K),
 \qquad\rho_0=(U-L)/d.
\]

With probability at least 1 − ε, b is at infinity-norm distance greater than
d from every boundary ∂C_z. On that event, whenever the sampled primal is
feasible, minimizing f + ρ_0‖A x − b‖_∞ over all native slices has the
original optimum value, with multiplier zero.

## The geometric proof

For a nonempty compact convex C, define the 2m charts

\[
 E_{k,s}=\{x\in C:\exists n\in[-1,1]^m,\ n_k=s,
 \ n^\top(y-x)\le0\ \forall y\in C\},\quad s\in\{-1,1\}.
\tag{1}
\]

They cover ∂C: every boundary point admits a nonzero supporting normal, whose
largest absolute component can be normalized to ±1. A point admitting such a
normal is not interior. For a thin C, its boundary is C itself, and a normal
orthogonal to its affine hull suffices.

These charts are compact. The corresponding pairs (x,n) form a closed set
in compact C × [−1,1]^m, since the support condition is equivalently
nᵀx = h_C(n), with h_C continuous. Projecting gives compactness. This avoids
arbitrary normal selection and any measurability issue.

Apply the supporting inequalities at two points x,y in the same chart to get

\[
 |x_k-y_k|\le\sum_{j\ne k}|x_j-y_j|.
\tag{2}
\]

Thus each chart is a partial graph, globally 1-Lipschitz in the one-norm of
the other coordinates. The common signed maximal normal component is essential
to this argument; the whole boundary need not be a single graph.

Fix b_{−k}. Chart points within infinity-norm distance d in these other
coordinates have k-coordinate range at most 2(m − 1)d. Thickening by d in
coordinate k gives an interval of length at most 2md. An interval of length
a contains at most a(N − 1)/(2σ) + 1 endpoint-grid points, so its probability
is at most a/(2σ) + 1/N. Condition on b_{−k} and sum over charts to obtain

\[
 \Pr\{\operatorname{dist}_\infty(b,\partial C)\le d\}
 \le 2m^2d/\sigma+2m/N.
\tag{3}
\]

This covers m = 1 and singleton or other thin sets. Empty slices are omitted.
Compactness ensures all tube events are measurable. Summing over at most K
slices and substituting the proposed parameters gives at most ε.

For this endpoint-grid proof the grid must span the stated interval. Merely
requiring equally spaced points contained in the interval allows arbitrary
clustering and would invalidate the σ-dependent bound. A uniform midpoint
grid also admits the required spacing estimate; the final note uses its own
centered-cell argument.

## Repair and exactness

Assume the boundary-separation event and put M = U − L. For a feasible slice,
b is interior to C_z and b + [−d,d]^m is contained in C_z. Thin slices cannot
be feasible on this event. Write v_z for the slice optimum at b.

Given native x, put u = A x and t = ‖u − b‖_∞. If t > 0, choose y in the
same slice with A y = b − d(u − b)/t. The convex combination

\[
 x'=(d x+t y)/(d+t)
\]

is feasible for b. Therefore

\[
 v_z\le f(x')\le\frac{d f(x)+t U}{d+t},\qquad
 f(x)\ge v_z-\frac{U-v_z}{d}t\ge v_z-\frac{M}{d}t.
\tag{4}
\]

The t = 0 case is immediate. Adding ρ_0t dominates v_z and hence the global
feasible optimum v*. In a nonempty infeasible slice, the nearest image point
belongs to its boundary; thus every native point has t > d and

\[
 f(x)+\rho_0t\ge L+(M/d)t\ge U\ge v^*.
\tag{5}
\]

The inequality remains valid for M = 0. A primal optimum achieves equality
in the penalized problem. Compactness and continuity justify attainment.

There is a small strengthening. If M > 0, ρ_0 itself gives solution-set
exactness: for each feasible slice choose d < d' < dist_∞(b,∂C_z), and repeat
(4) with d'. A nonzero residual then has penalized value at least
v_z + Mt(1/d − 1/d') > v_z. Equation (5) is also strict for infeasible
slices. For M = 0, ρ_0 = 0 may admit infeasible minimizers, but any positive
penalty excludes them. The advertised conclusion for ρ > ρ_0 is safe.

## Conditional feasibility and preservation of the optimum

Without an anchor the guarantee is

\[
 \Pr\{\text{primal feasible and proposed penalty not exact}\}\le\varepsilon.
\]

It does not imply the same failure bound conditional on feasibility.

For a counterexample, take an odd endpoint-grid size N ≥ 3 on [−1,1], set
a = 1/(N − 1), h = a², and use the single convex compact native slice

\[
 X=\{(x,t):0\le x\le a,\ x^2\le t\le h\},\quad
 f(x,t)=-x,\quad A(x,t)=t.
\]

Its image [0,h] contains only the grid point zero. At b = 0 the primal value
is zero, but every finite zero-multiplier penalty gives a negative value:
take t = x² and positive x small enough that −x + ρx² < 0. Conditional on
feasibility, fixed-multiplier exactness therefore fails with probability one;
unconditionally this event has probability only 1/N. The ordinary optimized
Lagrangian supremum is still zero, so the example concerns finite-multiplier
attainment and the fixed-zero-multiplier conclusion.

A fixed anchor slice containing the sampling cube in its image guarantees
feasibility for every sampled b and removes this conditioning problem. It
does not preserve the unperturbed optimum. For example,

\[
 z\in\{0,1\},\quad -z\le x\le z,\quad f(x,z)=z,\quad A(x,z)=x
\]

has an anchor slice z = 1 for [−1,1]. The value is zero at b = 0 and one at
every nonzero b in that interval, however close to zero. All data are linear
with unit coefficients.

## Encoding and sampling

A finite-bit algorithmic statement needs rational supplied b0, σ, ε, L, U
and an encoded integer upper bound K on slice count, or an independently
justified procedure computing those bounds. The exact count is unnecessary.
Compactness alone does not give these bounds in polynomial time.

Then d and ρ_0 have bit length polynomial in the supplied data lengths and
log K. To infer polynomial size in the original model encoding, those supplied
lengths must themselves be polynomial in that encoding. This is a statement
about bit length, not numerical size or enumeration of grid points.

For exact sampling with a fixed polynomial number of random bits, choose N
to be a power of two above the required threshold. Draw log₂N independent
bits per coordinate. Arbitrary N can instead use rejection sampling with
expected polynomial cost. The distinction matters if a worst-case sampling
claim is made.

## Verification record

The primary reviewer checked all inequalities, the compactness and thin-set
cases, the repair argument, encoding conditions, and both counterexamples.
An additional reviewer and that reviewer's independent delegate separately
checked (1)–(3) and flagged the full-span grid and fixed-slice assumptions.
No numerical experiment or Lean formalization was used: the central issues
are the general proof and interpretation of its assumptions. No project-wide
verification or CI inspection was performed. Novelty requires a separate
literature comparison.
