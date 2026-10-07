# Independent review: core-only noise with changing residual faces

Date: 2026-10-02. Verdict: **passed** for the actual
[composition theorem](core-only-noise-boundary-recourse.md).
The separate [supporting-lemma review](core-noise-boundary-lemmas-independent-review.md)
checks the active-pattern tube and quantitative small-multiplier proofs.
This review concerns their algorithmic composition, not publication priority.

The theorem correctly removes both residual noise and supplied conditional
interiority while retaining verified uniform residual strong convexity.
Its exact certificates do not assume that a probabilistic good event
occurred. Probability is used only to bound the search and fallback cost.

## Three exceptional events and one finite law

The global selector sensitivity and projected-to-full growth lift remain
valid with boundary residual minimizers. The two-block projected-growth
formula needs only the core noise marginals. In the active-core-gradient
tail, the draft correctly enlarges the face count to `3^n`, including
residual faces. Positive projected growth and uniform residual strong
convexity give full point growth, so the actual free stationary Hessian
is nonsingular. Fixing an active core coordinate removes its noise
coefficient from those stationarity equations. Thus the isolated-root
count and one-coefficient interval bound still apply.

The third exceptional event is also composed correctly. For each original
core face, the algorithm-independent active-pattern boundary and its
gradient image are defined before sampling. A core optimum within `2eta`
of that boundary gives a free-noise vector within `2H_V eta` of the image.
The union over faces is valid even though the optimizer chooses its face
after seeing the noise. Zero-dimensional faces require no tube event.

The definitions of `g`, `tau`, `eta`, and the lower bounds on `M` make
each of the three failure probabilities at most `rho=1/(6B)`. In
particular, the tube's finite-grid atom term is paid for separately, and
`sqrt(q)<=k` is a safe simplification. Their union is at most `1/(2B)`.
All constants defining the cutoff precede `M` and have polynomial binary
length. The eliminated algebraic sets are not constructed by the solver;
their effective degree bounds determine only the pre-draw budget.

## Stable branches and unknown multiplier classification

Outside the tube event, the optimum has a two-sided radius-`eta` ball
within the free coordinates of its original core face. Every residual
coordinate has constant bound status on that ball. The free residual
stationarity system is nonsingular by the uniform modulus, so its smooth
implicit branch exists there. Original active multipliers are nonnegative
throughout the ball, including any identically zero ones.

The supplied bounds justify `K_3=max{1,nT(1+H)^3}` uniformly across all
such patterns. The small-multiplier estimate gives the stated `theta`
and restored full Hessian modulus `nu`. It is applied only after active
core coordinates are fixed. Applying it in a one-sided unfixed core normal
direction would be invalid; the actual composition avoids this error.

The algorithm need not know the pattern or determine which multipliers
are small. Once its contained product patch is sufficiently narrow, strict
uniform signs fix every active residual bound whose multiplier exceeds
`theta`, and every active core bound whose gradient exceeds `tau`.
Additional sound fixings preserve the Hessian modulus as principal
restrictions. A zero multiplier cannot accidentally pass a strict uniform
sign test on a patch containing the optimum.

For a zero-dimensional optimal core face, the remaining problem is purely
residual and its Hessian already has modulus `mu`. The draft treats that
case directly rather than invoking a nonexistent two-sided core ball.

## Localization, exact closure, and bit work

The common analysis margin `g_*` is no larger than the full global growth
constant and than `nu/4`. Thus the inherited approximate-corner and
excluded-slab bounds use a valid global constant, while the final Hessian
test retains a separate local curvature reserve.

The omitted slabs at clipped original endpoints, use of certified excluded
lower values, and transfer across the core hull are all correct. They
preserve every original global optimizer on every draw. Under the good
events the excluded lower gap is at least `7g_*r^2/16`, exceeding the
`g_*r^2/4` transfer bound. The patch radius also makes both classes of
large derivative signs detectable. The remaining Hessian at the optimum
is at least `nu I>=4g_* I`; two midpoint-variation allowances leave the
claimed slack `3g_*-2Tr>=5g_*/2` in the final matrix test.

No residual interior slack or multiplier separation is inserted into the
input assumptions. Rational patches may touch original bounds. Exact
evaluation when all variables are fixed is now stated explicitly.

The same-draw fallback has the correct base-only exponential factor and
fixed polynomial dependence on sampling and later evaluation bits.
Ordinary output is an exact strongly convex implicit patch, with
polynomial-precision evaluation. It is not an expanded algebraic answer.
The compact descriptor and its full global pruning proof retain the
different size guarantees stated in the theorem.

## Significance qualification

The advance is the core-only finite-law exact guarantee with changing
residual faces and weak multipliers, controlled by the original core
upper curvature. Uniform residual strong convexity is still substantive.
The [rotating-fiber note](core-only-noise-rotating-fiber.md) shows that
qualitative strict convexity and even unique interior minimizers do not
suffice for this full-Hessian certificate.

There is also an important distinction from the earlier semidefinite-
residual rank-separation example. If the full Hessian norm is bounded
by `M` and `H_RR>=mu I`, then

```
alpha=M+M^2/mu,
H_F+alpha diag(I_core,0) >= 0
```

by the Schur complement. Therefore this uniformly strong-residual class
does admit a fixed rank-at-most-`k` concave-quadratic decomposition.
Its coefficients can be numerically much larger than the original `L`.
The new theorem avoids charging that convexification scale to its state
count; it should not be advertised as a structural separation from every
fixed low-rank convex difference.

## Verification record

I read the complete saved theorem and both supporting derivations, checked
the three finite-law budgets and all threshold transfers, and requested
the harmless all-fixed direct-evaluation clarification. The author applied
it. The author's boundary diagnostic is separate and was not rerun here.
An inline `python3` check passed for this review's local links, paired
code fences, and trailing whitespace. No external searches, root index
edits, project-wide checks, or CI inspection were performed.
