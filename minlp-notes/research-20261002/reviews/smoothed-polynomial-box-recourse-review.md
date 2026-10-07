# Independent review of smoothed polynomial recourse

Date: 2026-10-02. Reviewed the completed
[polynomial recourse draft](../new-direction/smoothed-polynomial-box-recourse.md),
including its tangent certificates, and the local finite-noise, exact
fallback, and convex-patch evaluation interfaces. No external searches,
index edits, project-wide checks, or CI inspection were used.

**Conclusion.** I found no substantive gap in the continuous polynomial
theorem. Certified approximate conditional values suffice for both core
pruning and excluded-region localization. The resulting strongly convex
patch gives an exact implicit optimizer, while the rare fallback supplies
an algebraic optimizer. These are different output representations, and
the draft states that distinction. Requested evaluation precision belongs
in the evaluation cost: the appropriate polynomial factor is
`poly_d(I+q)`, rather than `poly_d(I)` independent of `q`.
The author applied this clarification in the statement during review.

The theorem remains conditional on the stated polynomial-time recourse
interface. For its concrete convex-residual class, a supplied checkable
global residual-convexity proof is required. The proof does not assume
that arbitrary polynomial convexity can be recognized efficiently.

The error accounting in the core search is correct. Corner interpolation
contributes at most `e=kLh^2/8`, and the corner oracle contributes another
`e`, giving `U-f*<=2e`. At a corner minimizing a retained cell's lower
values, the true value is at most its lower value plus `e`. Retention
therefore gives

```
V(v) <= ell(v)+e <= U+2e <= f*+4e.
```

The corner attaining the best feasible upper value belongs to a retained
cell, since its lower value is no larger than that upper value. Thus its
rational completion and the retained core hull have the required relation.
This does not require the completion to be an exact conditional optimizer.

For a fixed grid tuple, true `4e`-near-optimality confines each interior
core-noise coefficient to an interval of length
`Lh+8e/h=Lh(1+k)`. The intervals depend only on the tuple and residual
noise after the other core linear terms cancel. Adaptive approximate
oracle outputs do not change this necessary event. Summing over the full
deterministic grid and then charging only queried tuples preserves the
product probability bound. The two endpoint choices and the finite-law
atom contribution give the stated counting factor when `M>=2^J`.

The approximate exclusion test uses the correct directions of both
bounds. For every slab, its returned lower bound is no larger than its
true conditional minimum. The incumbent `U` is a feasible value and is
no smaller than the unrestricted conditional minimum at the selected
core point. Consequently

```
ell_out-U > 2G diam_infinity(D)
```

implies the exact gap needed to transfer exclusion throughout `D`.
Replacing `ell_out` by a feasible excluded value would not be sound.
The use of closed artificial-boundary slabs, omission of sides at original
endpoints, and the `+infinity` convention for an empty collection are
correct, as in the reviewed quadratic mechanism.

The stopping constants cover both the ordinary and empty-core cases.
With `A_0=2+(kL+8)/g_0`, the retained hull is within `A_0 h` of the
optimizer coordinatewise and the incumbent completion is within that
distance in Euclidean norm. For `k>0`, these follow from the respective
`4e` and `2e` objective gaps. For `k=0`, the single query has error at
most `e=h^2`; the added `8/g_0` term safely supplies the same bounds.
The first cutoff condition implies `2e<=g_0 r^2/16` in both cases.

Each closed exclusion slab is at least `3r/4` from the optimizer in one
residual coordinate. Its true objective is therefore at least
`f*+9g_0 r^2/16`. The slab oracle loses at most
`eta_out=g_0 r^2/16`, and the incumbent loses at most another
`2e<=g_0 r^2/16`. Hence

```
ell_out-U >= 7g_0 r^2/16.
```

The other cutoff condition bounds the transfer term by `g_0 r^2/4`,
leaving a strict margin. When `k=0`, the core diameter is zero and the
same positive gap certifies residual localization directly.

The nonlinear closure checks are sufficient on every draw. The bound
`M_1` controls each gradient component's variation in infinity norm.
The third-derivative row-sum bound `T` controls the infinity operator norm
of Hessian differences; symmetry then controls their Euclidean operator
norm as well. Both bounds remain valid after fixing coordinates.

On the good event, the full patch lies within `5r/4` of the optimizer,
and its midpoint radius is at most `r`. The midpoint gradient's error
relative to an active optimizer gradient, together with its uniform
radius allowance, is at most `9M_1r/4<tau/2`. Every active original
bound is fixed. A free coordinate cannot pass a strict uniform sign
test because its gradient is zero at the optimizer contained in the box.
These fixings use continuous first-order optimality; they do not extend
to integer coordinates without an additional argument.

The remaining optimizer is interior relative to its original free
coordinates. Two-sided Taylor expansion of point growth gives a free
Hessian at least `2g_0 I` at that point. The midpoint is within `r_Q`
of it, so the matrix in equation (13) is bounded below by

```
[g_0-2T r_Q] I >= (g_0/2) I.
```

Thus the exact rational midpoint test passes at the stated cutoff. On any
draw where it passes, Hessian variation proves strong convexity throughout
the remaining box. Combined with global containment, this proves the
implicit output's exact global meaning, even when the optimizer is
irrational or lies on a remaining patch boundary.

An independent delegated audit checked Section 2 against the linked local
GLS statements. It confirmed that objective approximation requires only
convexity. After zero-width coordinates are removed, the capped epigraph
contains the ball centered at `(midpoint(B),W+1)` with radius equal to
the smaller of `1/2` and the coordinate half-widths. The radius has
polynomial encoding length even for thin rational boxes. Convex tangent
separation is valid, and homothety toward this ball accounts for the GLS
comparison with the eroded body.

Near-feasibility repair also has the stated constants. Clipping the
returned point to the box gives
`f(y)<=t+(G_f+1)epsilon`, while the objective comparison gives
`t-A_f epsilon<=f*`. The interval width is therefore at most
`(A_f+G_f+1)epsilon`, exactly the denominator used in equation (6).
No strong-convexity or distance-to-optimum estimate enters this oracle.

The direct tangent certificate in equation (6a) is correct. Convexity
makes the endpoint linearization minimum a global lower bound. For its
gap, smoothness along the segment to the minimizing endpoint gives

```
gap <= delta/t + K_f t/2.
```

If `eta<=2K_f`, the chosen `t=eta/(2K_f)` and
`delta<=eta^2/(8K_f)` bound the two terms by `eta/4` each. If
`eta>2K_f`, taking `t=1` gives a sum below `3eta/4`. Thus the asserted
certificate width holds in both regimes. Fixed-degree rational value,
gradient, and endpoint evaluation make this certificate directly
checkable; the verifier does not need the convex solver's internal trace
or its claimed stopping accuracy. The extra requested precision has only
polynomial bit length.

The finite sampling and exceptional branch use the supplied interfaces
correctly. The growth section count is independent of threshold and
sampled coefficient height. The active-gradient count only needs the
nonsingular stationary roots forced by positive growth, so singular
stationary families cause no missing cases. The fallback's exponential
factor is base-only; sampled coefficient bits and requested evaluation
bits enter with fixed polynomial exponents. These properties are exactly
what the new proof needs, and are separately established in the linked
notes.

All constants defining `J` precede the choice of `M`. Their logarithms,
including those of the fallback budget and reciprocal growth and gradient
thresholds, have polynomial base-input length. Equation (17) gives failure
probability at most `rho` for each of the two events and retains
`M>=2^J` for the core counting bound. The same-draw fallback is therefore
invoked with probability at most `1/(2B)`. Its work, representation size,
and later evaluation cost are paid for by that probability. No
noise-dependent rational separation or exact algebraic recourse comparison
is introduced.

The normal output specifies the unique minimizer of an explicitly given
strongly convex rational polynomial on a rational box. Its KKT system is
an exact descriptor of the primal point, without an assertion that all
coordinates have short expanded algebraic representations. The evaluation
lemma gives feasible rational approximations and certified value intervals.
Objective accuracy `min(2^-q,(g_0/2)2^-2q)` implies both the stated value
error and Euclidean point error. Its bit cost is polynomial in `I+q`.
The exceptional algebraic representation can be large, and the theorem
appropriately gives an expected bound rather than a per-draw compactness
claim.

No additional optimization diagnostic was run for this review. The
author's reported command and nonlinear irrational-optimizer fixture are
recorded in the draft; they are separate from this mathematical audit.
The prior quadratic diagnostic was not reused as evidence for nonlinear
recourse or Hessian variation. The scoped command
`git diff --check -- research-20261002/reviews/smoothed-polynomial-box-recourse-review.md`
passed. A separate inline `python - <<'PY'` check passed for this review's
trailing whitespace, local link, and paired code fences. These are local
checks, not CI results.
