# Independent review of the dtoc5 rational dual certificate

Reviewer: Codex review sub-agent. Date: 2026-10-04. Scope: dtoc5 only.

**Verdict: verified.** Theorem 1's model, exact feasibility, convex Lagrangian,
dual formula, lower bound and `7.21e-43` certificate gap all check out. I computed
the full rational dual value, independently of the dossier's code, and verified
its exact equality to the primal objective minus the completed-square losses.
The task brief's literal upper bound `7.2e-43` is too small. The numbered issues
below concern reporting and interpretation; none invalidates Theorem 1.

## 1. Independent reconstruction from OSIL

I parsed `/workspace/local-home/.cache/minlplib/minlplib/osil/dtoc5.osil` with Python's
XML parser, expanded the sparse-matrix compression, and converted every numeric
decimal string to a rational. I checked every entry, rather than sampling rows
or trusting the GAMS transcription. OSIL quadratic coefficients multiply the
listed variable products directly; there is no additional factor of one half.

The file has 99,999 continuous variables, 49,999 equality rows, 149,997 linear
matrix entries, and 149,997 quadratic terms. Of the quadratic terms, 99,998
belong to the objective and 49,999 belong to the dynamics. There are no other
model sections, linear objective terms, or objective/constraint constants.

Let `T = 49999`, `h = 1/50000`, and use zero-based OSIL variable indices.
The variable at index `t` is `u_t = x_{t+2}` for `0 <= t < T`; the variable at
index `T+t` is `y_t = x_{50001+t}` for `0 <= t <= T`. The only finite variable
bounds are `y_0 = 1`. All controls and the remaining states are free, including
`y_T = x100000`.

The objective and every dynamics row are exactly

\[
 f(u,y)=h\sum_{t=0}^{T-1}(u_t^2+y_t^2),\qquad
 -hu_t+y_t-y_{t+1}+4hy_t^2=0.
\]

In particular, `y_T` has no objective term; the fixed initial state contributes
the constant `h` when eliminated. The decimal coefficients `2e-5` and `8e-5`
are exactly `1/50000` and `1/12500`. This matches the model used in Proposition 1
and Theorem 1.

I also read the DTOC5 SIF block in
`literature/papers/luksan2026-cutest-source-forms-for-dtoc5/original.txt`.
Its `H = 1/N`, transition linear terms, `SQ` element `Z*Z`, and
`ZE TT(T) YSQ(T) H` give the state-square coefficient `h`, rather than `4h`.
The objective group scale `RN=N` gives the same objective coefficient `h`.
At the matching choice `N=50000`, the dynamics coefficient still differs by
four. The certificate therefore concerns the MINLPLib variant, not the CUTEst
variant. The SIF's default dimension is smaller; that is separate from the
coefficient difference.

Input SHA-256 hashes checked in this review:

| Input | SHA-256 |
|---|---|
| OSIL | `ac7b2d9472dbbfe9cb8aebc2c27a311b70c7fee18913084d76935508a794c783` |
| Point gzip | `6e963788952bede20fa3b9b9285784cd7674a2d28e1e4fb4bc74ab72c59975b5` |
| Saved primal rational | `8c110402913970d5eb3d5de46d99305dcc5a556e2c9c51b1bac900eb0dc3c160` |

## 2. Proof and multiplier convention

Keep `y_0=1` in the domain of the Lagrangian infimum, and define

\[
 c_t=y_{t+1}-y_t-4hy_t^2+hu_t,\qquad
 L=f+\sum_t\lambda_t c_t.
\]

Thus `c_t` is the **negative** of the OSIL row. Multipliers on the OSIL rows
themselves would have the opposite sign. This convention is essential.
Collecting coefficients from the model gives

\[
 L=h(1-4\lambda_0)-\lambda_0
 +\sum_{t=0}^{T-1}(hu_t^2+h\lambda_tu_t)
 +\sum_{t=1}^{T-1}\left[h(1-4\lambda_t)y_t^2
 +(\lambda_{t-1}-\lambda_t)y_t\right]
 +\lambda_{T-1}y_T.
\]

Because `y_T` is free, a nonzero `lambda_{T-1}` makes the infimum `-infinity`.
Convexity alone does not prevent this. Setting it to zero removes that linear
term. The point's last control is approximately `-1.958093118962868e-26`, so
using `-2u_{T-1}` without the override would give a nonzero positive terminal
coefficient, approximately `3.916186237925736e-26`. Smallness is irrelevant to
the unbounded infimum. The override is required for this certificate.

For the selected multipliers, every nonterminal control is strictly positive
(the smallest is approximately `1.460729008138572e-5`), hence every nonterminal
multiplier is negative; the final multiplier is zero. Let
`A_t = h(1-4lambda_t)`. All interior `A_t` are at least `h > 0`. The Hessian on
the free coordinates is diagonal, with entries `2h` for controls, `2A_t` for
interior states, and zero for the terminal state. The Lagrangian is jointly
convex, and is strictly convex in every free nonterminal coordinate. Its
extension before fixing `y_0` is also convex at these particular multipliers.

The global infimum is attained at

\[
 u_t=-\lambda_t/2,\qquad
 \bar y_t=\frac{\lambda_t-\lambda_{t-1}}{2h(1-4\lambda_t)}\quad(1\le t<T),
\]

with arbitrary terminal state. Completing the squares gives exactly

\[
 d(\lambda)=h(1-4\lambda_0)-\lambda_0
 -\frac h4\sum_{t=0}^{T-1}\lambda_t^2
 -\sum_{t=1}^{T-1}\frac{(\lambda_{t-1}-\lambda_t)^2}{4h(1-4\lambda_t)}.
\]

For **every exactly feasible point**, all dualized rows vanish, so

\[
 f(u,y)=d(\lambda)
 +h\sum_{t=0}^{T-1}(u_t+\lambda_t/2)^2
 +\sum_{t=1}^{T-1}A_t(y_t-\bar y_t)^2\ge d(\lambda).
\]

This identity is global: no state enclosure, sign restriction on a competing
point's controls, numerical feasibility tolerance, or finite bound on free
variables is needed. A feasible exact KKT point minimizing this convex
Lagrangian would give equality and global optimality, which is the
Mangasarian-type sufficiency argument. The committed rational point instead
has a small, strictly positive certified primal-dual gap; the lower bound does
not require it to satisfy exact stationarity.

## 3. Independent computation and comparison

My code is [review.py](/tmp/sol-dtoc5-review/review.py). It neither imports nor
runs repository scripts. It first copies the three data inputs into the scratch
directory, reconstructs the model, checks all 49,999 rows and all bounds in
`Fraction` arithmetic, and evaluates the objective from the OSIL terms.
The objective equals the saved primal rational exactly.

The code then assembles the diagonal and linear coefficients of `L` directly
from the parsed OSIL terms. It minimizes each free scalar quadratic as
`-b_j^2/(4a_j)`, using exact rational arithmetic throughout. Python `Fraction`
handles the individual terms; balanced additions through system `libgmp.so.10`
produce the full reduced rational, without rounding any division term.
The dual denominator has 9,071,237 bits. I separately summed the rational
losses `(2a_j*x_j+b_j)^2/(4a_j)` and verified their sum equals `f-d` **exactly**.
This checks the direct minimization against the completed-square identity.

Computed values below are decimal prefixes; the actual computations and saved
artifacts are exact rationals:

```text
d = 5.389672119181140467423966499136271868831312689336317054372987275151674143362875411645...
f = 5.389672119181140467423966499136271868831313409846661118171325584350095475787301100722...
f-d = 7.205103440637983383091984213324244256890775416653946341742...e-43
```

I also independently reproduced the dossier's rounding rule: round each
subtracted state-minimum term upward to `2^-256`. The resulting rational lower
bound has exactly the logged decimal prefix

```text
B_256 = 5.389672119181140467423966499136271868831312689336317054372987...
```

The full dual exceeds `B_256` by approximately `2.16732856797256e-73`, less
than the theoretical bound `49998 * 2^-256`. This agrees with both the dossier
and the critique. The old summary display `5.38967211918114` is safely below
this independently verified dual. Adopting the new point-derived certificate
removes the need to regenerate the earlier Newton-based multipliers.

Saved artifacts:

- [result.json](/tmp/sol-dtoc5-review/result.json): hashes, exact-check results,
  100-decimal outward enclosures, and safe displays.
- [dual_exact.txt](/tmp/sol-dtoc5-review/dual_exact.txt),
  [primal_exact.txt](/tmp/sol-dtoc5-review/primal_exact.txt), and
  [gap_exact.txt](/tmp/sol-dtoc5-review/gap_exact.txt): full rational values.
- [dossier_lower_exact.txt](/tmp/sol-dtoc5-review/dossier_lower_exact.txt):
  independently reconstructed `B_256`.
- [review.log](/tmp/sol-dtoc5-review/review.log) and
  [boundary_checks.log](/tmp/sol-dtoc5-review/boundary_checks.log), plus the
  final [display check log](/tmp/sol-dtoc5-review/check_displays.log).

## 4. Numbered issues

1. **Unsafe gap in the task brief.** The literal claim `f-d <= 7.2e-43` is false:
   the exact gap is greater than that rational decimal. Use `7.21e-43` as in
   Theorem 1, or `7.3e-43` for the width of its displayed interval.

2. **Distinguish exact arithmetic from the exact dual value.** The dossier's
   computation produces `B_256 <= d`, rather than the full rational `d`.
   Its description of the rounding rule is correct, and its theorem is safe.
   A paper should call this a rigorous rational evaluation below the dual
   function, or a certified lower bound on the dual value. My full rational
   evaluation confirms that the rounding error has no effect on the claimed
   digits or gap bound.

3. **Do not infer exact equality from convexity at these multipliers.** The
   dossier's proposed phrase “the duality gap is zero up to rounding of the
   data” should be replaced by the explicit certified gap. The committed pair
   has `f-d > 0`, and this calculation does not establish exact KKT conditions
   or exact zero optimal Lagrangian duality gap. Similarly, its proposed
   interval “around” the shortened decimal ending `...8313` is misplaced:
   that decimal is below the certified interval. Give the endpoints.

4. **Two informal model descriptions need qualification.** Dossier §1.1 says
   “No variable has finite bounds”, although `y_0` is fixed at one. Use “all
   unfixed variables are free”. Its opening dynamics description
   `dot y = y^2-u` describes the CUTEst coefficient; the MINLPLib certificate
   uses the Euler dynamics `dot y = 4y^2-u`. The displayed model and proof
   already use the correct coefficient and fixed initial state.

## 5. Safe paper displays

Round the dual down and the primal up:

\[
\boxed{
5.38967211918114046742396649913627186883131268
\ \le\ f^*\ \le\
5.38967211918114046742396649913627186883131341.
}
\]

The rounded endpoints have width **`7.3e-43`**. The gap between the exact
primal objective and the exact dual value is at most **`7.21e-43`**;
the dossier's `B_256` also supports this latter bound. These are different
quantities and should be labeled accordingly. For a more detailed certificate
gap display, **`7.205104e-43`** is rounded upward and safe.

Suggested paper sentence: “For the MINLPLib dtoc5 model with dynamics
coefficient `8e-5`, an exactly feasible rational point and a jointly convex
Lagrangian give the displayed bracket; the certified primal-dual gap is at
most `7.21e-43`.”

## 6. Targeted commands and resource limits

Executed from `/tmp/sol-dtoc5-review/`:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -u /tmp/sol-dtoc5-review/review.py > /tmp/sol-dtoc5-review/review.log 2>&1
python -u /tmp/sol-dtoc5-review/boundary_checks.py > /tmp/sol-dtoc5-review/boundary_checks.log 2>&1
python -u /tmp/sol-dtoc5-review/check_displays.py > /tmp/sol-dtoc5-review/check_displays.log 2>&1
```

All three passed. The main computation took 16.93 seconds and pinned itself to one
CPU core. The boundary check also used one core and confirmed an exact row
violation after perturbing `x500` by `1e-60`, the nonzero terminal slope without
the override, and negative state curvature under the wrong row-sign convention.
The final check compared the authored endpoints and gap displays with the
independent rational enclosures and confirmed the interval width exactly.
Only these topic-specific checks were run; no project-wide verification or CI
status/log inspection was performed. No repository script was executed or
imported, and no commits were made. Working files were written only under
`/tmp/sol-dtoc5-review/`; this review is the sole repository file authored.
