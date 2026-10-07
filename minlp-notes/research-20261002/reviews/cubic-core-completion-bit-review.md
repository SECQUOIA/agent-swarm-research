# Focused review of cubic core completion and its bit bounds

Date: 2026-10-02. Status: fresh actual-file review passed. No correction
is requested.

This review covers
[cubic-core-full-point-oracle.md](../new-direction/cubic-core-full-point-oracle.md),
with emphasis on the completion penalty, rational error-bound data,
minimum-norm selector, and bit-cost composition. The inherited
[selected-core oracle](../new-direction/coupled-polytope-core-oracle.md)
and the referenced convex-cubic regularization argument were read for
their exact output and norm conventions. The separate full review and
author-owned composition diagnostic are not duplicated here.

## A positive completion penalty handles all draws

Using `beta=alpha+1` is sound and materially resolves the zero-shift
case. Convexity of `G_alpha` implies convexity of `G_beta`, while

```text
T_a(x)=F_c(x)+(beta/2)||v-a||^2
```

has minimum `f*` and optimizer set exactly `S_a`. This remains true
when the original sampled objective has several optimal core points.
Using `alpha` itself in this penalty would fail to select the fiber
when `alpha=0`.

The positive completion penalty is separate from the core-search
parameter. Its size enters only rational coefficient lengths and
requested precision. It does not introduce a new numerical
`1/sigma` factor in the expected cell-search bound. The zero-core and
zero-dimensional branches avoid the formulas that divide by `k` or
assume a positive reduced dimension.

## Rational rows and a possibly irrational right-hand side

The affine-hull reduction and the reflection argument operate in the
relative coordinates of the original polytope. The inner-ball reflection
gives `H(w)<=B_0 H_0`, so `ker H_0` is the common feasible Hessian
kernel. This does not assume ambient convexity outside the affine hull.

The target fiber is exactly the polytope intersected with the equalities
whose row blocks are

```text
H_0,  g_0',  E.
```

All three blocks are rational and base-computable. Their right-hand
side can be irrational without entering the row-height bound. The
core equality is essential: it replaces the unknown slope
`g_0-E'(beta a+c)` by the known rational row `g_0`.

The constants in the transverse estimate check. The endpoint Hessian
forms obey `s<=8R_0^2 B_0 M`; the cubic identity then gives

```text
(d'H_0 d)^2 <= 108R_0^2 B_0 M Delta.
```

The stated rational positive-eigenvalue lower bound and the deliberately
coarse `C_perp` are valid. The zero-rank branch correctly uses a zero
transverse term instead of an undefined positive eigenvalue.

For the remaining rows, the positive penalty gives
`||E d||<=2 sqrt(Delta)`. Also
`||beta a+c||<=k(beta+sigma)` because the core lies in the unit box.
Together with the gradient bound for `h-g_0'w`, these yield exactly
the `C_res` in equation (12), for `0<=Delta<=1`.

The polyhedral Hoffman argument is uniform in the equality right-hand
side. After clearing row denominators, the projection proof uses at
most the reduced dimension's number of independent integer rows.
Feasibility makes the active inequality contributions nonpositive;
only the stacked equality residual is charged. The integer minor
bound therefore gives equation (13). Lifting by `B_norm` proves (14)
with a computable rational `Gamma` of polynomial binary length.

In particular, `Gamma` does not require computing the exact selected
core or giving its algebraic height a polynomial bound. The known
noise magnitude bound is sufficient, independently of the sampled
coefficient denominators.

## One canonical minimum-norm completion

The target `S_a` is a nonempty compact convex set, so its minimum-norm
point `p_a` is unique. The selected core `a` is fixed by the inherited
core-first lexicographic contract. Thus the declared full selector is
the same on every precision query, including tied-core draws.

The regularization comparison gives

```text
e^4/Gamma^4 <= T_a(x_tau)-f* <= 2R_x tau e,
||x_tau-p_a||^2 <= 2R_x e.
```

With the stated `tau`, this gives `e<=epsilon^2/(8R_x)` and
`||x_tau-p_a||<=epsilon/2`. The required unregularized gap is at most
`tau R_x^2<=1`, so the fourth-root estimate is used within its stated
range. The zero-distance case is immediate and needs no division.

The rational surrogate drops only constants independent of `x`. For
a core approximation with Euclidean error at most `delta`,

```text
|Q_b(x)-Q_a(x)| <= beta sqrt(k) delta.
```

An `eta`-accurate feasible solution of `Q_b` consequently has true
regularized gap at most `eta+2 beta sqrt(k) delta`. The constants in
equation (15) make this at most `3 tau epsilon^2/16`, which is below
the claimed `tau epsilon^2/4`. Strong convexity from the original
Euclidean norm penalty then gives the remaining point error at most
`epsilon/2`.

No estimate on the unknown constant term of `T_a` is needed. The
comparison uses objective differences, and the original-coordinate
norm preserves the stated selector on nonunit and lower-dimensional
domains.

## Short outputs preserve the expected bit bound

The completion needs a short dyadic core vector, not an arbitrary
expanded algebraic record. The draft explicitly obtains that vector
by a sufficiently accurate core query followed by dyadic rounding and
clipping, and handles the exact fallback by direct dyadic refinement
of the selected algebraic core. Feasibility of this dyadic vector as
a projected core is unnecessary.

This safeguard matters: an expected output-length bound alone would
not justify applying a polynomial-time postprocessor to a rare,
exponentially long output. The new convex solve instead receives
coefficients of polynomial length on every draw. Any expensive exact
root work remains in the base-budgeted selected-core query.

The logarithms of `1/tau`, `1/eta`, and `1/delta` are
`poly(I)+O(q)`. The rational surrogate remains a total cubic, and the
convex value interface has polynomial bit cost in those lengths,
without an inverse-strong-convexity iteration factor. The original
core oracle's one common random work factor therefore suffices for
all completion precisions on the same finite sampled instance.

The optional objective-gap output is also sound: a tighter point
request controls the objective error by the uniform gradient bound,
and the existing value oracle supplies the remaining lower-bound
accuracy. Both requests use the same coefficient vector and selector.

## Verification performed

This was a complete actual-file read with the focused scope above.
A targeted document check passed this review's local links, paired
code fences, trailing whitespace, and final newline. No new agent,
numerical run, external search, main-file edit, index edit,
project-wide verification, or CI inspection was performed.
