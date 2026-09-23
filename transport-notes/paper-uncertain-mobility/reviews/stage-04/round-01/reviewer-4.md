# Independent review: Stage 04, round 01, reviewer 4

Reviewer: `paper_reviewer_4`. Date: 2026-09-07.

**Verdict: no major or minor issue requiring correction found.** The generic order theorem follows under the explicit sufficient assumptions given, including its unrestricted scalar lower bounds and full-bulk interpretation.

## Snapshot and independence

Reviewed snapshot: `da3db325e0812991ad97d79560c4c8aeb99b83d7260ade75d6172d61d3b4aaa6`. I independently recomputed all twelve hashes in the manifest; all matched. I read the full new generic-fold section, its handoff, the prior accepted model/localization/design tools it invokes, and the scope updates. I did not read other reviewer reports or coordinator checks, did not delegate, and did not edit manuscript sources. This review did not require a build.

## Uniform geometric assumptions

The finite-cover root-count argument is valid. A fixed-sign first spatial derivative gives at most one zero in a product-neighborhood slice; a fixed-sign second derivative gives at most two. A finite cover of the compact zero set therefore gives a uniform finite count. Removing open neighborhoods of all multiple zeros leaves a compact simple-zero set with slope bounded away from zero. Uniform local derivative bounds then permit ordinary-root intervals of fixed radius. A sequence of distinct ordinary roots with separation tending to zero would converge to a multiple zero, excluded from that compact portion.

The partition argument also keeps the active fold roots inside their own retained spatial neighborhood by shrinking the parameter neighborhood first. Thus ordinary-root intervals and the active fold region can be chosen without losing a nearly merged root between them. On the remaining compact pieces, a rate tending to zero would limit to a zero covered by one of those intervals, a contradiction. This supports the uniform positive-potential remainder bound. Ordinary roots need not move with c for any of these arguments.

Uniform rate anchoring follows because the continuous function `c↦∫g(s,c)²ds` is positive at every c: an identically zero spatial realization would contradict the finite multiple-zero set. Compactness then gives a strictly positive minimum. This is enough for the accepted finite-bulk transfer; one does not need a separate lower bound on every root slope at a fold.

The direct fold coordinate has the asserted regularity. The spatial critical point z(c) exists by the implicit function theorem because gss is nonzero. The second-order Taylor coefficient is C² and bounded away from zero after shrinking, so its square root produces a C² spatial coordinate with bounded positive Jacobian. Differentiating the signed parameter gives `t′(cj)=-σj gc(sj,cj)`, since gs vanishes at the critical point. The shift of z(c) is O(|t|), lower order than the root distance sqrt(t). Thus roots, slopes, and root separation on the positive side all have the stated scale r.

The alternative zero curve `c=Cj(u)` has derivative zero and second derivative `-gss/gc` at the fold. On one chosen branch its derivative magnitude is comparable to root distance. The probability-density lower and upper bounds consequently turn a spatial root interval of length r at distance r into parameter probability of order r². The almost-everywhere density assumption is sufficient: on every retained shell the zero-curve map is a smooth monotone diffeomorphism with nonzero derivative, so the change of variables preserves null sets.

## Lower bounds over arbitrary L¹ designs

The sliding-bump proof uses only local mass, not pointwise mobility. For a test centered at u, derivative energy is B(u). Tonelli gives an upper bound `Cm/(r ell)` for its average over the root interval. Reaction energy is at most `Cr²ell³`, and the squared source is of order ell². Jensen for the convex negative power holds for every q>0. With `ell∼(m/r³)^(1/4)`, these terms balance and give `r^(2-5q/4)m^(-q/4)` after including parameter probability. The support condition follows from m≤c*r⁷ and a sufficiently small fixed width factor. If m=0, arbitrarily narrow tests give an infinite integrated lower bound, so no exceptional zero-mass case is omitted.

For the subcritical lower order, one fixed shell has positive sampling probability and satisfies the small-mass condition for all sufficiently small M. At criticality, a sufficiently sparse geometric sequence makes both enlarged spatial shells and their monotone parameter images disjoint. Each local mass is at most M and their sum is at most M. There are logarithmically many shells between a fixed radius and a sufficiently large constant times M^(1/7). Convex inverse-mass allocation then gives the factor `[log(1/M)]^(7/5)`.

Above the threshold, the fold bump uses all of the budget only as an upper bound on derivative energy. Taylor expansion gives rate O(R⁴) throughout a parameter interval of width R² and a spatial interval of width R. Thus derivative and reaction energies are bounded by M/R² and R⁵, respectively. With R=M^(1/7), the response is at least cR^(-3) on a sampled event of probability at least cR². Additional roots cannot invalidate a local trial. These lower bounds therefore cover arbitrary spikes, oscillations, zero sets, and discontinuities in D.

## Global upper designs and Neumann comparisons

The normalization of the proposed design has the correct finite-set behavior: finite integral for α<1, a logarithm for α=1, and a power R^(1-α) for α>1. With the prescribed R, it gives `a_R∼R^(6+α)` in all three regimes and an exact budget M. For each fixed M, the field is bounded and has a positive global lower bound of order a_R. This lower bound need not stay positive as M tends to zero, and the later text correctly excludes a prescribed positive floor.

Capping the grading exponent below by zero is appropriate. A simple root for one parameter may occupy a spatial site that is a fold for another parameter. Using a negative exponent would reduce its mobility, whereas the selected nonnegative exponent gives the uniform floor protecting all such roots. For q≤2/3, uniform mobility already attains the required order, so this choice loses no claimed precision. The theorem asserts orders rather than cosine sharp constants.

The Neumann upper comparison has the correct direction. Replacing mobility and potential by lower bounds decreases the energy and increases the response. Allowing separate endpoint values on the partition pieces further increases it. The resulting harmonic interval has uniformly bounded scaled response whenever its scaled half-width is bounded away from zero; increasing interval size does not introduce uncontrolled constants because the tails have integrable reciprocal quadratic potential.

At an active fold-side root, the actual mobility is comparable to `a_R r^(-α)` throughout an interval of radius ηr. The potential is comparable to `r²(s-u)²`. The ratio of oscillator width to r is `(R/r)^((6+α)/4)`, so the interval is long enough on the harmonic scale for r≥CR. The root contribution is `a_R^(-1/4)r^(-3/2+α/4)`. The local complementary reciprocal integral is of order r^(-3), smaller by `(R/r)^((6+α)/4)`, so it is legitimately absorbed.

In the central window, scaling `s-sj=Ry` and `c-cj=R²τ` produces a uniformly positive diffusion coefficient on a fixed interval and a potential converging uniformly to `(γj y²+βj τ)²`, with both coefficients nonzero. The uniform Neumann coercivity argument is sound: vanishing energy of unit-L² functions would force convergence to a nonzero constant, but no limiting nonzero quadratic-square potential annihilates such a constant. Choosing the interval sufficiently large contains all local roots and leaves a reciprocal-potential remainder of order R^(-3). This proves the stated core upper bound without imposing Dirichlet data or assuming a uniformly nonzero kinetic floor.

On the rootless side, the normal-form Jacobian is bounded and the reciprocal integral of `(|t|+x²)^(-2)` has size |t|^(-3/2). Ordinary roots elsewhere cost at most a_R^(-1/4) each by their nonzero slopes and the global mobility floor. The finite root count makes the sum uniform. The remaining positive-potential pieces give a constant. Thus the upper proof includes roots not associated with the active fold, including stationary root branches and roots located at another fold's site.

## Integration and physical interpretation

For a fixed positive q, the qth power of a finite sum is bounded by a fixed multiple of the sum of qth powers; this is valid for q<1 as well as q≥1. Parameter integration of the fold-side contribution then gives `a_R^(-q/4)∫_R^{r*}r^(e-1)dr`, with `e=2-3q/2+αq/4`. For α=0 and q≤2/3, e is positive. With the positive grading formula, e equals `(8-5q)/(q+4)`. I independently checked this identity symbolically.

The ordinary-root contribution is O(a_R^(-q/4)). The local core contribution is O(R^(2-3q)), while rootless integration is bounded, logarithmic, or of this latter order depending on whether q is below, at, or above 2/3. I independently checked that the core-to-ordinary ratio is R^e and the ordinary-to-supercritical ratio is R^(-e). These give the stated dominance in each regime. At q=8/5, the core/rootless term is `M^(-2/5)[log(1/M)]^(2/5)`, exactly one logarithmic factor below the main critical term. The possible q=2/3 rootless logarithm is smaller than the polynomial main order. No term is omitted at a borderline exponent.

The exact ratio of physical and scalar optimal moments follows from the accepted same-budget theorem because the generic family is uniformly bounded and anchored, and each scalar order dominates the required logarithmic growth. It does not assign a sharp scalar coefficient or prove that the explicit graded trial is a sharp optimizer. Directly on that trial, its mobility floor is algebraic in M up to a logarithm, so the bulk remainder bound is at most logarithmic. Fixed positive bulk diffusivity, constant affinity, nonzero V, and the connected one-dimensional wall remain part of the physical interpretation.

The conclusion is therefore appropriately limited: transverse folds with positively sampled two-sided neighborhoods produce the same optimized threshold even without cosine symmetry. It does not cover uncertain fold locations, simultaneous or spatially coincident folds, higher degeneracies, rate-amplitude collapse, or different sampling singularities. No Gaussian field theorem, generic sharp constant, or limiting optimizer uniqueness is implied.

## Findings and recommendation

No actionable defect was found in the theorem, arbitrary-design lower bounds, graded response estimates, integration, or physical transfer. The direct coordinate construction is sufficiently explicit and does not need an additional high-regularity normal-form theorem. The proof uses accepted earlier localization tools at the appropriate order level. Subject to the coordinator's adjudication of all five independent reports, Stage 04 can be accepted.
