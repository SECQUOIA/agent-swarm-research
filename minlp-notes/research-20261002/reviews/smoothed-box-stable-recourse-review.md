# Independent review of smoothed box-stable recourse

Date: 2026-10-02. Reviewed the actual complete draft of
[smoothed-box-stable-recourse.md](../new-direction/smoothed-box-stable-recourse.md),
including the stated finite sampling law. The review also checked the
referenced local growth-tail and active-gradient arguments. No external
searches, index changes, project-wide checks, or CI inspection were used.

**Conclusion.** I found no substantive gap in the continuous unit-box
theorem. The excluded-region test supplies the missing exact completion
without making the terminal mesh depend on sampled denominators. The
result requires an exact residual optimizer and value on every rational
coordinate subbox, with a uniform polynomial bit bound. It does not follow
from an oracle that handles only unrestricted residual boxes.

The forest corollary uses the exact rational forest oracle already recorded
and reviewed locally. This review checks its interface with the new proof;
it does not independently establish publication priority or re-prove that
external forest algorithm.

The conditional value has the required upper coordinate curvature because
the residual feasible set is fixed when core coordinates vary. Independent
corner rounding cancels off-diagonal quadratic terms, so the error is
`e_j=kLh_j^2/8`, with no residual-dimension multiplier. Every retained cell
has a corner within `2e_j` of the global value. Conditioning on residual
noise leaves independent core coefficients. For a fixed deterministic
grid tuple, the neighbor comparisons restrict each interior coordinate's
noise to an interval of length `Lh_j(1+k/2)`, independently of the other
core coefficients. Summing over the full deterministic grid is valid even
though the algorithm queries only an adaptive subset. The two endpoint
choices and the finite-law atom contribution give the stated factor
`3+(1+k/2)L/(2sigma)` when `M>=2^J`.

The localization test is sound on every draw. The bound `G` controls the
core gradient in the norm dual to the infinity norm, throughout the
original box and for every allowed noise vector. Both unrestricted and
restricted conditional values are therefore `G`-Lipschitz. Since the
chosen corner `c` belongs to `D`, every `v in D` satisfies
`||v-c||_infinity<=d`. For any excluded slab, its conditional value at `v`
is at least `V_out(c)-Gd`, whereas an unrestricted feasible completion has
value at most `V(c)+Gd`. The strict gap in equation (11) excludes every
outside conditional optimizer, including ties.

The draft correctly uses closed slabs at artificial patch boundaries.
The complement of a closed patch can be open, so its minimum need not be
attained. Closed slab minima remain valid exclusion barriers. In the
continuous product-box setting, continuity also identifies their minimum
with the infimum over the excluded region. A side that reaches an original
endpoint must be omitted; otherwise its closed slab could include an
original-bound optimizer and destroy the useful gap. An empty collection
of slabs correctly has value `+infinity`.

The gradient tests are uniform on `D times P`, and they fix only original
bound coordinates. This is essential. First-order necessity on the
original continuous box makes each fixing valid at every global optimizer
in the certified patch. The Hessian test covers all remaining coordinates,
including core-residual cross terms. Exact convex minimization on a
remaining box containing these optimizers therefore returns an original
global optimum. Requiring `A_JJ>=g_0 I` is stronger than the PSD condition
needed for soundness, but the good-event argument proves that this stronger
test passes.

The quantitative stopping argument has sufficient slack. Write
`A_0=2+kL/g_0`. A retained corner is within
`h sqrt(kL/(4g_0))` of the unique optimizer; allowing one cell width gives
the stated coordinate distance bound `A_0 h` for the entire retained hull.
The incumbent completion is within `sqrt(e/g_0)<=A_0 h`. The first
condition in equation (14) places that completion within `r/4` and implies
`e<=g_0 r^2/16`. Every artificial exclusion slab is then at least `3r/4`
from the optimizer in one residual coordinate, giving

```
V_out(c)-V(c) >= g_0 r^2/2.
```

The second cutoff condition gives

```
2G diam_infinity(D) <= 4G A_0 h <= g_0 r^2/4.
```

Thus the strict localization test passes. Every point of the full patch
is within `5r/4` of the optimizer in infinity norm. Since
`r<=tau/(16M_1)`, gradient variation is at most `5tau/64`, below the
required `tau/2`. Every active original bound is identified. No originally
free coordinate passes a strict sign test, since its gradient is zero at
the optimizer. Two-sided feasible variations in the free coordinates
then give `A_JJ>=2g_0 I` from point growth.

The finite-law argument is not circular. The base quantities `B`,
`C_tail`, `K`, `rho`, `g_0`, `tau`, `r`, `A_0`, and `G` determine `J`
before `M` is chosen. Their logarithms have polynomial base-input length.
The growth tail contributes at most `rho`: its continuous term is
`n g_0/sigma=rho/2`, and equation (17) bounds its atom term by `rho/2`.
For each nonsingular stationary face candidate, an active gradient is
its own noise coefficient plus an affine function independent of that
coefficient. Counting at most `nB` face-coordinate pairs gives the
active-gradient failure bound `K(tau/sigma+1/M)<=rho`. Positive growth
ensures that the actual optimizer belongs to this nonsingular candidate
family. Consequently failure to close by `J` has probability at most
`2rho=1/(2B)`.

The face-enumeration fallback is exact even on tied or flat draws, and its
cost is `B` times a polynomial. Its expected contribution is therefore
polynomial. The adaptive recourse outputs and patch endpoints have
polynomial encoding length by the oracle interface. Their random centers
do not affect the base choice of `J` or the atom bound. There is no rational
reconstruction threshold hidden in this part of the proof.

Three qualifications matter for possible extensions:

- Noise only on the core does not supply the full-vector growth and
  active-gradient events used here. The actual theorem correctly samples
  every original coordinate.
- Binary residuals would require a separate exact oracle closed under the
  exclusion restrictions. A radius below half the lattice spacing makes
  a certified patch contain only the incumbent binary assignment, which
  can then be fixed. Continuous gradient signs cannot replace this step:
  `z^2-3z/2` on `{0,1}` is minimized at `z=1`, despite its positive
  derivative there. Any remaining integrality must be preserved.
- Integer core coordinates require feasible integer cells, eventual
  singleton cells, the corresponding counting argument, and a mixed
  fallback count. The continuous proof alone does not establish that
  extension. Likewise, an oracle for a continuous forest does not by
  itself cover an arbitrary mixed residual forest.

A separate algebraic check confirms why center-only gradient signs would
be insufficient. For

```
f(u,y)=y^2+(1/1000-u)y,
D=[0,1/100], c=0, Y=[0,1], P=[0,1/2],
```

the center completion is `y=0`, the outside gap is
`501/2000>2G diam(D)=1/50` with `G=1`, and the center derivative in `y`
is positive. Fixing `y=0` leaves a PSD core Hessian but loses the true
minimum, attained at `u=1/100`, `y=9/2000`, with value
`-81/4000000`. The draft avoids this failure through its uniform tests.

The targeted command actually run was an inline `python - <<'PY'`
exact-arithmetic diagnostic using `fractions.Fraction`, seed `2026100217`.
It enumerated stationary faces of 600 rational two-variable box QPs.
There were 548 successful localization certificates; all 11,508 sampled
conditional slices stayed in their certified patches. All 548 subsequent
uniform-gradient and PSD closures matched the exact original optimum.
The same command checked the center-gradient example and the binary
derivative example above. It exited with status zero. These finite checks
support the certificate algebra; the general conclusions rely on the
proof review, not on sampling conditional slices.

The scoped command
`git diff --check -- research-20261002/reviews/smoothed-box-stable-recourse-review.md`
and a separate inline Python check of this review's trailing whitespace,
local link, and paired code fences also passed. These are local checks,
not CI results.
