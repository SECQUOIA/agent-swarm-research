# Independent review: core-only noise with strong interior recourse

Date: 2026-10-02. Verdict: **passed** for the actual
[restricted theorem](core-only-noise-strong-recourse.md).
This is a mathematical review, separate from the author's targeted
diagnostic and from any claim of publication priority.

The theorem removes residual perturbations under two substantive premises:
a verified uniform residual strong-convexity modulus, and qualitative
interiority of every original-box conditional minimizer. It does not
extend automatically to arbitrary convex residual fibers or to merely
strict convexity.

## Growth, curvature, and finite noise

The sensitivity constant `H=M_1/mu` is valid. The full symmetric Hessian's
row-sum bound controls its Euclidean operator norm and hence the cross
block. Combining strong residual monotonicity with the two variational
inequalities gives the stated Lipschitz bound for the unique selector.
This step works even for boundary conditional minimizers; the later
interiority premise is used elsewhere.

The lift from projected growth is correct:

```
F_gamma(v,z)-f* >= g_V ||v-a_C||^2 + (mu/2)||z-s(v)||^2,
||v-a_C||^2+||z-a_R||^2
 <= (1+2H^2)||v-a_C||^2+2||z-s(v)||^2.
```

Thus `g_F=min{g_V/(1+2H^2),mu/4}` supplies full point growth.
Neither `1/mu` nor the cross-derivative magnitude enters the numerical
cell-count parameter; their logarithms enter the localization precision.
The original core upper curvature remains valid by partial minimization.
The Schur-complement identity gives the same conclusion directly where
the interior implicit selector is differentiated.

The projected-growth formula in Section 3 has the right quantifiers.
At `v=a`, its universal residual comparison makes `z_0` a conditional
minimizer. Minimizing over every other residual slice then gives exactly
the projected point-growth condition. Conversely, that growth condition
and a minimizing completion supply the existential witness. There are
two blocks of `n` real variables and only `k` sampled marginals. The
existing coefficient-height-independent section bound therefore applies
without explicitly eliminating the selector or raising the quantifier
alternation count.

The active-core gradient argument also checks. On a fixed core face,
the stationarity equations for all residual and free core coordinates
exclude the coefficient of any fixed core coordinate. Positive projected
growth and the growth lift make the corresponding free Hessian positive
definite, so the relevant stationary root is nonsingular. The isolated-root
bound `max(1,d-1)^n` remains valid even when other stationary components
are singular. Counting `3^k` core faces and at most `k` active core
coordinates gives the displayed union factor. Conditional gradient events
are intervals for the one remaining independent coefficient. No residual
gradient coefficient is implicitly randomized in this proof.

## Closure and output

Certified convex recourse on restricted subboxes remains available even
when their conditional minimizers lie on the new artificial boundaries.
The global interiority premise concerns only the original residual box;
it is not incorrectly imposed on these oracle calls.

With the lifted `g_0`, the inherited approximate-value and excluded-slab
constants apply unchanged. Their witnesses are genuinely feasible full
points, and the excluded values are certified lower bounds. The sound
core gradient tests fix all active original core bounds on the good event.
Every original residual coordinate is interior at the actual optimizer,
so two-sided directions in the full growth inequality give Hessian at
least `2g_0 I` on all remaining coordinates. The midpoint test and its
`g_0/2` slack are therefore correct.

No lower bound on residual distance to its original endpoints is required.
Arbitrarily short feasible two-sided directions suffice for the Hessian
argument. The returned rational patch may touch those endpoints. Requiring
the patch itself to be strictly inside the original residual box would be
an unjustified and potentially expensive extra condition.

The budget order is sound: all constants defining the cutoff precede the
choice of finite grid size `M`; their binary lengths are polynomial in the
base input. The two exceptional events each have probability at most
`rho`, so the same-draw algebraic fallback has polynomial expected
contribution. Additional sampled coefficient bits and requested evaluation
bits enter with fixed polynomial exponents. The exact implicit patch and
rare algebraic output remain distinct formats. The compact patch is not
by itself the entire global pruning certificate.

## Significance and boundaries

This is more than substituting a supplied bounded-degree polynomial
selector: that easier case already reduces to deterministic algebraic
optimization in the small core. Here the selector can be a dense coupled
polynomial-gradient system, need not be explicitly expanded, and need not
separate into the independent scalar equations covered by the earlier
implicit-graph theorem. Moreover, the value's upper curvature stays at the
original `L`; a generic graph substitution can increase that parameter
through mixed derivatives.

The extra assumptions remain important. The
[rotating-fiber example](core-only-noise-rotating-fiber.md) defeats every
full-dimensional convex patch under core-only noise despite uniformly
good projected growth. Its strictly convex residual variant has a unique
interior optimizer and still defeats this patch mechanism because the
residual Hessian lacks a positive uniform modulus. These are limits of
the present certificate, not impossibility results for exact optimization.

I requested only one minor edge-case wording clarification: if the residual
set is empty, the same core-corner algorithm with direct objective values
and no slab calls preserves the displayed counting constant. There is no
need to invoke a different sparse-DP bound for that case.

## Verification record

This review read the complete saved theorem and checked its links to the
reviewed polynomial-recourse, finite-tail, fallback, and convex-evaluation
interfaces. No additional optimization diagnostic or external literature
search was run. An inline `python3` check passed for this review's local
links, paired code fences, and trailing whitespace. No index edits,
project-wide tests, or CI inspection were performed.
