# Lean formalization

Machine-checked proofs for results in this repository's manuscripts.

The fixed-preconditioner minimax development is in `QipmFormal/Preconditioner/`.
Its [verification report](PRECONDITIONER.md) covers the actual signed path
matrices, extremal-eigenvalue condition numbers, every invertible congruence
factor, and the identity upper bound for all signed paths. Exact ramp summation
strengthens the former `m²/4` lower bound to `(4m²−1)/3` for every `m ≥ 1`.
The data-dependent preconditioning and quantum-query claims are separate.

The explicit fractional SDP spectrum development is in
`QipmFormal/FractionalSDP/`. Its [verification report](FRACTIONAL_SDP.md)
connects the unique log-det center to the actual reduced Hessian in the
Frobenius metric, proves all four ordered eigenvalue asymptotics and their
leading constants, and treats the two-eigenvalue restriction. The rational
parametrization covers every sufficiently small gap and barrier parameter.
The singularity-degree, diameter, and arbitrary-barrier results are outside
this development's scope.

The exact-center Newton coupling development is in `QipmFormal/Coupling/`.
Its [verification report](COUPLING.md) describes the LP equations, actual
block inverses, filtering criterion, regularity assumptions, and sparse
witnesses, with the corrections to the manuscript's witness qualifications.

The noncommutative SDP central-mixture development is in
`QipmFormal/SDPMixture/`. Its [verification report](SDP_MIXTURE.md) maps the
matrix variance identity, sharp Kantorovich sandwich, both centrality
conventions, sparse SDP residuals, and output soundness to Lean proofs.
It records the sharper KKT constant and the correction to the scope of the
dimension-dependent Frobenius guarantee.

The pathwise residual-certified refresh development is in
`QipmFormal/Refresh/`; its [verification report](REFRESH.md) covers the
actual normalized systems, scalar residual test, sequential refresh bound,
and the correction distinguishing safe acceptance from control of false
rejections. It does not formalize the subsequent IPM-tail or quantum-cost claims.

The sparse convex-mixture and scalar-centrality development is in
`QipmFormal/Mixture/`; its [verification report](MIXTURE.md) maps the
manuscript claims to proofs and records stronger multibit and KKT bounds,
the counterexample correction, and both neighborhood conventions.

The QCPM correction is developed in `QipmFormal/QCPM/`; see
[the verification report](QCPM.md) for its statements, source correspondence,
scope, and reproduction commands. The scalar-dilation certificate remains
in `QipmFormal/ScalarCert/`.

The integrated build and axiom audit passed on 2026-09-20 for 2701 project
declarations. The optional fresh-environment replay was not run.

Toolchain: Lean 4.33.1 with Mathlib `v4.33.1` (pinned in `lean-toolchain` and
`lakefile.toml`).

```sh
env PATH="$HOME/.elan/bin:$PATH" lake build     # build
./scripts/verify.sh                             # build + axiom audit
./scripts/verify.sh --replay                    # ... plus fresh-environment kernel replay
```

`.lake/packages` is a symlink to an existing local Mathlib build to avoid a
second 11G package tree. To build standalone, delete the symlink and run
`lake exe cache get`.

## Verification contract

Every result must be kernel-checked and depend only on the standard Lean
axioms `propext`, `Classical.choice`, `Quot.sound`. In particular:

- no `sorry` (`sorryAx`),
- no `native_decide` (`Lean.ofReduceBool`),
- no added `axiom` declarations.

`Verify.lean` prints the axiom dependencies of the headline results, then
checks every declaration in the imported `QipmFormal` modules against the
three-axiom allowlist. It also rejects project axiom declarations even when
unused. Declarations are selected by their defining module, including private
declarations and declarations outside the project namespace. Any violation
raises a Lean error and makes `scripts/verify.sh` fail. Large finite
arithmetic is discharged by `decide` over `ℕ`, which the Lean kernel
evaluates with GMP-backed arithmetic, so it is checked by the kernel rather
than trusted to the compiler.

The optional replay runs `leanchecker --fresh -v QipmFormal`, which rechecks
the entire import closure, including Mathlib, in a fresh environment. This
uses Lean's own kernel; it is not an independently implemented verifier.

## Topic 1 — the scalar-dilation certificate

Source: `../central-path-cost/sections/appendix-scalar-certificate.tex`,
with the objects defined in `03-sharp-centrality.tex` (`eq:scalar-elementary`,
`thm:scalar-dilation`). The paper's own check of this appendix is the Python
script `../central-path-cost/scripts/verify_scalar_certificate.py`; the point
of this topic is to replace that trusted script with proofs.

Everything is phrased in the paper's `v` coordinate:

| Lean | paper |
|---|---|
| `Y v = 2 artanh v - √2 artanh (v/√2)` | `ρ x` |
| `A v = √(2-v²)/(1-v²)` | `p' (Y v)` |
| `P v = v * A v` | `p (Y v)` |
| `W v` | `W(v)` in the proof of `thm:scalar-dilation` |
| `ratio v = Y (W v) / Y v` | `p⁻¹(y p'(y))/y` at `y = Y v` |
| `cstar` | `c⋆` of `eq:cstar` |

### Modules

All 24 modules.

| File | Contents |
|---|---|
| `Defs.lean` | `Y`, `A`, `P`. |
| `Series.lean` | `hasSum_artanh`; `hasSum_Y`, the series `eq:Y-rational-series`. The `√2` cancels exactly, which is why the paper uses this series rather than the logarithms. |
| `Tail.lean` | `partial_le_Y` and `Y_le_partial_add_tail`: `S n ≤ Y z ≤ S n + 2z^{2n+1}/((2n+1)(1-z²))`. |
| `Monotone.lean` | `P_sq`: `P v ^ 2 = ((1-v²)⁻¹)² - 1`; strict monotonicity of `P` and of `Y`. |
| `Inverse.lean` | `Pinv`, the explicit inverse of `P`, and `W`; `P_W : P (W v) = Y v * A v`. |
| `Algebraic.lean` | Rational two-sided bounds for `A` and `P` by rational squaring. |
| `Certificate.lean` | `ratio`, `cstar`, and `ratio_gt_of_witness`, the paper's lower-certificate argument. |
| `Eval.lean` | Scaled-integer Horner evaluator `accLo`/`accHi` and its correctness against the real series. Structural recursion only, so the kernel reduces it. |
| `Enclosures.lean` | Bridges `Eval` to `Tail`: two-sided rational bounds on `Y z`. |
| `Witness.lean` | The lower certificate: `v₀`, `w₀`, `a₀`, the five displayed enclosures, the two margins, `exists_ratio_gt`. |
| `Elasticity.lean` | `Y_deriv`; `lt_Y`; `B`, `Y_lt_B`; `K`, `K_pos_lt_one`; `E`, `one_lt_E`. |
| `Upper.lean` | `hasSum_E`; `E_strictMonoOn`; `lt_of_two_lt_E` with `v₂ = 177/200`. |
| `KBound.lean` | `K_strictAntiOn`, `K_v2_lt`, `K_lt : 2 < E v → K v < 107/200`. |
| `Comparison.lean` | The elasticity identity `Y·E' = (E-K)·Y'`; `g`, `g_strictMonoOn_of_K_lt`; `E_comparison`; `logP_deriv_eq`; `Phi`, `Phi_pos`. |
| `LogBounds.lean` | The `artanh` series with tail estimate; rational bounds for `log(69/50)`, `log(50/19)`, `log 2`, `log(3449/2500)`, `log(2500/949)`. |
| `Final.lean` | `key_ineq`; `hgen`; `ratio_lt_of_hgen`; `ratio_lt_strict`; `bddAbove_ratio`; `cstar_lt`; **`cstar_bounds`**. |
| `Localization.lean` | Four further log bounds; the `E`-window `E_mem_window`; `maximizer_localization`. |
| `XLocalization.lean` | `xOf`, `xOf_vOf` (it is the inverse of `vOf`); `x_localization`; **`cstar_maximizer_location`**. |
| `Bridge.lean` | `bb`, `vOf`; `A_vOf`, `P_vOf`, `P_vOf_eq_bb_deriv`. |
| `Rho.lean` | `rho`; `Y_vOf_eq_rho`; `rho_hasDerivAt`. |
| `Correspondence.lean` | `scalar_elementary`; `rho_strictMonoOn`; `bb_second_div_rho_deriv`. |
| `Surjectivity.lean` | `artanh_le_Y`, `Y_le_two_artanh`, `Y_surjOn`. |
| `Attainment.lean` | Continuity of `ratio`, attainment of `cstar`, and localization of every point attaining it. |
| `Paper.lean` | The manuscript's `p`, its inverse and derivative, equality of the two suprema, and the certificate in the original coordinate. |

### Status

**Topic 1A — the strict lower certificate: proved, with the paper's own constants.**

All five displayed enclosures of the appendix and both margins of
`eq:lower-certificate-margins`:

| Result | Statement |
|---|---|
| `Y_v0_gt` | `2453756741730599/10¹⁵ < Y v₀` |
| `Y_v0_lt` | `Y v₀ < 12268783708653/(5·10¹²)` |
| `Y_w0_gt` | `134943211257327/(4·10¹³) < Y w₀` |
| `A_v0_gt` | `405367307458211/(4·10¹³) < A v₀` |
| `A_w0_lt` | `A w₀ < 25381942601625079/10¹⁵` |
| `margin_one` | `2071874360571/(2.5·10¹⁷) < Y w₀ - a₀ Y v₀` |
| `margin_two` | `2049519399569150216498389/(4·10²⁸) < Y v₀ A v₀ - w₀ A w₀` |
| `a0_lt_ratio_v0` | `a₀ < ratio v₀` |
| `exists_ratio_gt` | `∃ v ∈ Ioo 0 1, 68743/50000 < ratio v` |

`ratio_gt_of_witness` is unconditional — no boundedness hypothesis, hence no
dependence on the upper certificate.

Additional modules for 1A:

| File | Contents |
|---|---|
| `Eval.lean` | Scaled-integer Horner evaluator `accLo`/`accHi` with floor/ceiling rounding, and its correctness against the real series. Structural recursion only, so the Lean kernel reduces it. |
| `Enclosures.lean` | Bridges `Eval` to `Tail`, giving two-sided rational bounds on `Y z`. |
| `Witness.lean` | The witness `v₀`, `w₀`, `a₀`, the kernel-evaluated enclosures, the margins, and the conclusion. |

The enclosures are discharged by `decide` over `ℕ` at scale `10⁴⁰`, with 401
series terms at `v₀` and 801 at `w₀` (`w₀` is closer to `1`, so it converges
more slowly). `norm_num` cannot do this: the exact common denominator of the
series is astronomically large, and `decide` over `ℚ` is also unusable because
the kernel does not accelerate `Nat.gcd`. Scaled `ℕ` arithmetic *is*
GMP-accelerated in the kernel, so each enclosure checks in about two seconds.

Deviation from the paper: the appendix sums through `N = 1200`; 401 and 801
terms suffice for the displayed constants. The tail estimate is proved for
general `N`, so nothing is lost.

### Topic 1B — the upper certificate `c⋆ < 69/50`: **proved**

The appendix derives this from an elasticity `E(y) = y p'(y)/p(y)` satisfying
`dE/dlog y = E - K` with `E ≥ 1` and `0 < K < 1`, sharpened to `K < 107/200`
on the region `E > 2`. In the `v` coordinate these objects are simply

  `E v = Y v / v`,   `K v = Y v ² (1-v²)(2-v²)/(2v²)`,   `Y' v = 2/((1-v²)(2-v²))`,

and `E ≥ 1`, `0 < K < 1` are exactly `v < Y v < B v` with
`B v = √2 v/√((1-v²)(2-v²))`.

| File | Contents |
|---|---|
| `Elasticity.lean` | `Y_deriv`; `lt_Y : v < Y v`; `B`, `B_deriv`, `Y_lt_B`; `K_pos_lt_one`; `one_lt_E`. |
| `Upper.lean` | `hasSum_E`; `E_strictMonoOn`; `lt_of_two_lt_E : 2 < E v → v₂ < v`, `v₂ = 177/200`. |
| `KBound.lean` | `K_strictAntiOn`, `K_v2_lt`, and `K_lt : 2 < E v → K v < 107/200`. |
| `Comparison.lean` | the elasticity identity `Y·E' = (E-K)·Y'`; `g k v = (E v - k)/Y v` and `g_strictMonoOn_of_K_lt`; `E_comparison`; `logP_deriv_eq` (`d log P/d log Y = E`); `Phi`, `Phi_pos`. |
| `LogBounds.lean` | the `artanh` series with tail estimate, and rational bounds for `log(69/50)`, `log(50/19)`, `log 2`, `log(3449/2500)`, `log(2500/949)`. |
| `Final.lean` | `key_ineq`; `hgen`; `ratio_lt_strict`; `bddAbove_ratio`; `cstar_lt`. |

Two simplifications over the paper's route, both found by working in the `v`
coordinate:

* `E_strictMonoOn` follows directly from the series for `E` — its `k = 0` term
  is the constant `1` and the rest strictly increase — instead of from the ODE.
  This converts the appendix's region `E > 2` into an explicit interval.
* The appendix's differential inequality `E(ty) > k + t(E(y)-k)` is *equivalent
  to strict monotonicity of `g k = (E-k)/Y`*, since
  `g' = (k - K)·Y'/Y²`. Its integrated form is likewise the monotonicity of a
  potential `Φ`, whose derivative is `Y'·(g v - g v₀)`. So the whole step needs
  no integration and no reparametrisation.

`h₁ > 0` and `h_{107/200} > 0` are obtained from the tangent-line bound
`log x ≤ x - 1` plus the rational logarithm bounds, rather than from a convexity
analysis of `h`.

The paper obtains strictness of `c⋆ < 69/50` from attainment of the maximum.
Here `ratio_lt_strict` runs the same argument
with `a = 3449/2500 < 69/50`, which gives `cstar < 69/50` directly.
Attainment is established separately in `Attainment.lean`.

### Topic 1 conclusion

```lean
theorem cstar_bounds : (68743 : ℝ) / 50000 < cstar ∧ cstar < 69 / 50
```

This bounds `cstar` as defined in `Certificate.lean`, with no remaining
hypotheses. `Paper.cstar_eq` identifies it with the supremum of the
manuscript's original ratio, and `Paper.cstar_bounds` transfers the bounds.

### Maximizer localization — **proved**

`Localization.lean` and `XLocalization.lean` formalize the appendix's final
subsection, "Every scalar-dilation maximizer lies in a certified interval":

```lean
theorem cstar_maximizer_location {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1)
    (h : (68743 : ℝ) / 50000 < ratio v) :
    4611/5000 < v ∧ v < 9701/10000 ∧ 43/50 < xOf v ∧ xOf v < 943/1000
```

with `xOf v = v/√(2-v²)`, the inverse of `vOf`. This is
`eq:cstar-maximizer-location` in both coordinates. The `E`-window
`571/250 < E v < 773/250` is `E_mem_window`; the transfer to `v` uses
`E_strictMonoOn` together with kernel-evaluated enclosures of `Y` at
`4611/5000` and `9701/10000`, and the transfer to `x` is rational squaring, as
the appendix says.

### Topic 1D — bridge to the paper's original objects: **proved**

`Bridge.lean`, `Rho.lean` and `Correspondence.lean` connect the closed forms
used throughout to the paper's own objects: the barrier `b t = -log(1-t²)`,
the arclength `ρ x = ∫₀ˣ √(2(1+u²))/(1-u²) du`, and `p = b' ∘ ρ⁻¹`.

| Result | Statement |
|---|---|
| `Y_vOf_eq_rho` | `Y (vOf x) = ρ x` |
| `rho_hasDerivAt` | `HasDerivAt ρ (A (vOf x)) x`, i.e. `A ∘ vOf = ρ'` |
| `P_vOf_eq_bb_deriv` | `P (vOf x) = deriv bb x`, i.e. `P ∘ vOf = b'` |
| `scalar_elementary` | the three together |
| `rho_strictMonoOn` | `ρ` is strictly increasing on `(-1,1)` |

These are the identities `Y = ρ`, `P = p ∘ Y`, `A = p' ∘ Y` of
`eq:scalar-elementary`, in parametric form. `Y (vOf x) = ρ x` is proved by the
fundamental theorem of calculus; the third uses
`p' (ρ x) = b'' x / ρ' x = ρ' x` (`bb_second_div_rho_deriv`).

### Completeness of the `v`-parametrisation

`cstar` is a supremum over `v ∈ (0,1)`, whereas the paper takes a supremum
over `y > 0` with `y = Y v`. `Surjectivity.lean` proves these range over the
same set:

```lean
theorem Y_surjOn {y : ℝ} (hy : 0 < y) : ∃ v ∈ Ioo (0:ℝ) 1, Y v = y
```

via the series comparison `artanh v ≤ Y v ≤ 2 artanh v` on `[0,1)` — immediate
because the `k`-th series coefficient `2 - 2^{-k}` lies in `[1,2)` — together
with the intermediate value theorem at `tanh(y/4)` and `tanh(2y)`.

### Attainment and the manuscript's constant

`Attainment.lean` adds continuity of `ratio` and `cstar_attained`. The proof
takes a maximum on `[4611/5000,9701/10000]`. The strict lower witness lies
inside this interval, and localization puts every value above the lower
threshold inside it too. Thus the compact maximum is a global maximum.
`cstar_location_of_eq` locates any point satisfying `ratio v = cstar`.
Locating every maximizer and proving that a maximizer exists are separate
statements.

`Paper.lean` defines `rhoInv` on positive arguments and defines
`Paper.p y = deriv bb (rhoInv y)`, exactly the manuscript's definition on
the domain needed by the certificate. It proves the inverse identities,
`p (Y v) = P v`, and `deriv p (Y v) = A v`. The explicit `Paper.pInv`
is proved to be an inverse on positive arguments. `Paper.ratio_image`
equates the sets of ratio values, and `Paper.cstar_eq` equates their suprema.
`Paper.cstar_attained` supplies a positive maximizing argument, and
`Paper.cstar_isGreatest` states that the manuscript's constant is the maximum
of its ratio values.
The QCPM verification pass also checked these scalar modules and repaired
proof elaboration errors in `Attainment.lean` and `Paper.lean`, without
changing their theorem statements.

## Deviations from the appendix

These are places where the Lean development does something different from the
paper. None weakens a stated conclusion.

1. **Strictness of `c⋆ < 69/50`.** The appendix obtains it from attainment of
   the maximum. Here `ratio_lt_strict` runs the same argument with
   `a = 3449/2500`, which is `< 69/50`, giving `cstar_lt` directly.
   Attainment is proved separately using localization and compactness.
2. **Series truncation lengths.** The appendix sums through `N = 1200`; the
   enclosures here use 401 terms at `v₀`, 801 at `w₀`, and fewer elsewhere.
   The tail estimate is proved for general `N`, so nothing is lost.
3. **`h₁`/`h_k` positivity** is obtained from the tangent-line bound
   `log x ≤ x - 1` rather than from a convexity/monotonicity analysis of `h`.
   The resulting margins are very slightly weaker than the appendix's displayed
   ones (e.g. `6.47e-5` vs `6.4727e-5` at `h₁(2)`) but have the same sign,
   which is all that is used.
4. **The differential inequality** `E(ty) > k + t(E(y)-k)` is proved as strict
   monotonicity of `g k = (E-k)/Y`, and its integrated form as monotonicity of
   a potential `Φ`. This avoids integration and reparametrisation entirely.
5. **Two intermediate arguments are replaced, not reproduced.** The appendix
   reaches `E > 2 ⟹ x > 4/5` via `D(x) = (3/2)artanh x - x/2` and
   `ρ ≤ √2 D`, and reaches `K < 107/200` via `G(x) = D(x)²(1-x²)/(x²(1+x²))`
   and its monotonicity. Neither `D` nor `G` appears here. The conclusions —
   `lt_of_two_lt_E` and `K_lt` — are proved instead from `E_strictMonoOn`
   plus a certified enclosure of `E`, and from `K_strictAntiOn` plus
   `K_v2_lt`. So the appendix is covered at the level of its *conclusions*;
   two of its intermediate lemmas are not formalized because they are not
   needed.

## What is NOT formalized

- **The full signed inverse of `rho`.** `Paper.lean` needs the inverse only
  for `y > 0`, the domain of the manuscript's scalar certificate. It does
  not establish an inverse correspondence on all of `ℝ`.
- **Two general-`k` lemmas are off the critical path.** `E_comparison` and
  `Phi_pos` (`Comparison.lean`) require `StrictMonoOn (g k) (Ioo 0 1)`, which
  holds at `k = 1` but is false at `k = 107/200` (since `K v → 1` as `v → 0`).
  The certificate uses the interval-restricted `Phi_pos'` instead.
- **`log_69_50_ge` and `log_50_19_le`** reproduce the appendix's own displayed
  constants but are not used, since the certificate runs at `a = 3449/2500`.
- **The closing stationary-point identity** of the appendix
  (`Y(v)[Y'(v)A(v)+Y(v)A'(v)] = Y(W(v))Y'(v)A(W(v))`). The appendix states it
  as a remark and explicitly infers nothing from it.
