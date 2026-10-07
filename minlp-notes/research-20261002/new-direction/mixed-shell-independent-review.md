# Independent review of the physical mixed-shell certificate

Date: 2026-10-02. Status: final review complete. Reviewed the unified
[mixed-shell draft](mixed-shell-certificate.md), including its bottom-shell
argument. The separate
[grid and bit audit](mixed-shell-grid-bit-review.md) checks the encoding
details independently. No external search or index edit was made.

**Verdict.** No substantive gap was found in the physical-shell construction.
It certifies a proposed point's global quadratic growth on a product mixed
box, using the actual physical metric and supplied upper diagonal curvature.
No growth premise is needed to verify a successful certificate. The
discovery bound is `sigma>=min{L/32,g/12}`, not a constant-factor estimate
of `g` when `g` greatly exceeds `L`.

## 1. Coverage and the only radial step

After effective lattice endpoints are computed and fixed coordinates are
removed, the stated `r0` is positive and at most the maximum feasible
displacement. A lattice displacement smaller than `r0` must be zero,
because `r0<=h_i/2` for every lattice coordinate. Every continuous
available side has width at least `r0`.

The shells with radii `r0,2r0,...,2^J r0` cover every feasible
displacement of infinity norm at least `r0`. The last shell reaches the
maximum displacement even when the latter is itself a shell endpoint.
For a smaller nonzero displacement, all lattice coordinates stay fixed.
Scaling its continuous coordinates to infinity norm `r0` preserves their
signs and feasibility. The continuous-coordinate KKT check then gives

```
F(s+t v)-F(s) >= t^2 [F(s+v)-F(s)]       (0<=t<=1).
```

Thus the bottom shell's physical quadratic-growth bound extends inward.
No radial argument is applied to a nonzero lattice direction, and no
first-order derivative sign is required on an integer coordinate. The
construction also covers pure continuous and pure lattice problems;
in the latter case the omitted inner region contains only the candidate.

## 2. Feasible rounding and finite certificate

The scalar lattice grid is feasible because the proposed point and every
grid displacement belong to the same supplied lattice. A one-step interval
has no feasible target in its relative interior, so its rounding variance
is zero. If the initial gap has at least two steps, the ceiling rule bounds
its length by `delta S/n`. Every later nonunit gap has length at most
`delta` times its lower absolute endpoint. The threshold insertion only
subdivides gaps. These facts prove the scalar variance bound used in the
draft, including clipped initial or final gaps.

The shell flag is preserved in every rounding outcome. For continuous
coordinates the inserted threshold is `S`; for lattice coordinates it is
`h_i ceil(S/h_i)`. A feasible target of absolute value at least `S` has
both its enclosing grid endpoints on or beyond this threshold. Reflecting
a negative side changes neither the variance calculation nor this flag.

Independent rounding therefore stays on the original mixed domain and
inside the same physical shell. It preserves all linear and off-diagonal
quadratic expectations. Only the summed diagonal terms contribute to the
error. The proposed unary correction yields

```
F(x)-F(s)-sigma||x-s||^2 >= m_S-sigma S^2/n.
```

Acceptance is correctly **nonstrict**: `m_S>=sigma S^2/n` already
certifies the positive margin `sigma`. This matters at the sufficient
threshold `sigma=g/3` when `n=1`, where equality can occur. There is no
need to strengthen the test to a strictly positive residual.

The OR flag in the tree DP is owned-variable based and records whether
any coordinate reaches the current shell threshold. It changes the state
space by a factor of two and creates no new graph edges. Checking shells
separately incurs their number once; it does not raise that number to the
bag size. The resulting proof consists of finitely many rational Bellman
tables and their root inequalities, plus the continuous KKT check.

## 3. Discovery and its original curvature parameter

For genuine growth `g`, every shell grid value after the unary correction
is at least `(g-2sigma)S^2`. Thus `sigma<=g/3` suffices for all shell
tests. Starting with `delta=1/2` gives `sigma=L/32`; a failed predecessor
of the first later success has margin `4sigma>g/3`. Consequently

```
sigma >= min{L/32,g/12},
L/sigma <= max{32,12L/g}.
```

The successful full-domain certificate also implies `sigma<=g`. The
smallest `g` need not occur on a shell, but the bottom radial proof is
why the final global implication still holds. These bounds control the
grid size through `max{1,L/g}` without assuming `g<=L/2`.

Keeping the original curvature scale is essential. For

```
F(x,y)=H[x(1-y)+y(1-x)]+epsilon(x^2+y^2),   H,epsilon>0,
```

on the unit box at zero, the exact growth is `epsilon`, attained at
`(1,1)`, and summed diagonal curvature is `2epsilon`. The minimum
axis endpoint increment is `H+epsilon`. Inflating `L` using that
increment would lose the original conditioning bound by an arbitrarily
large factor. Conversely, a linear term can make `g` arbitrarily larger
than `L`, so curvature-only initialization cannot promise a constant
fraction of `g` on its first successful trial. The minimum in the stated
guarantee resolves both cases.

## 4. Lattice ranges, side distances, and bit cost

For every shell, the number of coordinate states is bounded by
`O(delta^-1 log(2n/delta))`, independently of the numerical box widths
and lattice spacings. In a lattice side, at most `O(delta^-1)` labels
lie below `2h_i/delta`; thereafter the step is at least `delta a/2`.
If the first label is clipped to the side endpoint, that side has only
one positive label and needs no ratio argument. Otherwise the first
label is at least `delta S/(2n)`, giving the claimed multiplicative
range bound. Threshold insertion adds only one state per sign.

Small positive side distances and lattice spacings do affect the number
of shells. Their logarithmic ratio has polynomial binary length because
the proposed point, endpoints, and spacings are part of the input. This
adds a polynomial factor outside the bag-size exponent. It does not give
coefficient-height-independent arithmetic work.

Each lattice label is a rational multiple of its input spacing with a
polynomial-bit integer multiplier. Continuous labels consist of rational
input scales times geometric powers whose length is polynomial in
`I+rK`. All shells share the same rational base radius and dyadic scaling.
A common denominator therefore exists with the claimed bit bound. Every
finite DP message is a sum of assigned quadratic factors; denominator
growth does not multiply with tree depth. The advertised
`f(p,max{1,L/g}) poly(I)` bit bound is consistent with these operations.

## 5. Nonpositive diagonal curvature

The separate endpoint argument for `A_ii<=0` also checks. A unique
candidate must lie at a box endpoint in each remaining coordinate:
otherwise its one-coordinate concave restriction supplies another
endpoint with no larger value. This applies to lattice coordinates as
well as continuous ones and uses no lattice KKT condition.

For a corner candidate, endpoint DP with one OR flag finds the smallest
objective gap `Delta` among other corners. If `Delta>0`, independent
endpoint rounding gives, with full coordinate widths `w_i`,

```
F(x)-F(s) >= Delta Pr(Y!=s)
          >= Delta max_i |x_i-s_i|/w_i
          >= [Delta/sum_i w_i^2] ||x-s||^2.
```

The last inequality follows by bounding each squared normalized
displacement by its largest normalized displacement. Thus this branch
produces an exact growth certificate in ordinary endpoint-DP time,
including for linear objectives. It is an established coordinate-concavity
baseline, not an additional structural complexity claim.

## 6. Significance and checks performed

This is a direct, independently checkable growth certificate for a supplied
candidate, including integer optima that fail continuous KKT conditions.
It avoids the normalized-metric and endpoint-scale losses of the earlier
signed certificate. It does not find the proposed point, cover general
mixed constraints, or certify a nonunique optimal set by the point-growth
inequality. Applying the earlier exact conditioned optimizer to a
margin-subtracted auxiliary quadratic already supplies a more indirect
route to such certificates. The improvement here is the explicit physical
shell proof and its small finite-state realization, not a new conditioned
solvability class.

The command actually run after the checker was saved was

```
python3 -B research-20261002/new-direction/check_mixed_shell_certificate.py
```

It passed 1,276 exact scalar rounding cases, 156 mixed-shell and inner
radial cases, 289 endpoint-certificate and scale-inflation cases, and three
obstruction families. I inspected the code: it
tests nonunit lattice steps, clipped bounds, threshold preservation,
reflection, the exact rounding identity, the shell lower bound, and the
bottom radial inequality. Shell minima are computed by exact enumeration
in this diagnostic; it is not an implementation of the mixed OR-DP.
A premature invocation before the file was saved returned a missing-file
error. The first completed run passed; the command was run again after
the endpoint and scale checks were added, and the extended run also passed.
No project-wide verification or
CI inspection was performed.
