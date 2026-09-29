# Recheck of the revised spatial-constrained note

Date: 2026-09-28. Target:
[`bb-complexity/spatial-constrained/instance-dependent-node-complexity.md`](../bb-complexity/spatial-constrained/instance-dependent-node-complexity.md),
as revised after [`spatial-constrained-review.md`](spatial-constrained-review.md).
Scope: the six substantive revisions listed in Section 13 of the note (items 4,
5, 8, 11 and 14 there). Pure wording fixes were not rechecked. The reviewer had
not seen the material before this recheck. The note was not edited, and nothing
was committed.

Scripts and logs are in [`spatial-constrained-recheck/`](spatial-constrained-recheck/).
They are floating-point checks and certify nothing. Each verdict below rests on
re-deriving the proof by hand. The scripts only test the stated constants and
claims on concrete instances.

## Verdict

No revised statement is false. Every revised proof is complete, apart from the
small gaps listed below. One minor problem remains that affects how a theorem
is applied (item 4: LICQ in Example 7.3 on the sphere). The other remaining
points are wording or constant-level nits.

| # | Revised item | Verdict | Remaining points |
|---|---|---|---|
| 1 | Remark 6.3a(ii): the `f_K` family with `alpha = 32` | correct | nits only |
| 2 | Headline characterization via `Phi_alpha` (Summary item 5, Theorem 6.3, Remark 6.3a(i)) | correct and consistent with the Section 6 proofs | the Munos semi-metric scaling is off by a constant factor; the upper factor `2^n` can be 1 |
| 3 | Theorem 8.2(d), written out | correct; constants re-derived exactly | citation-level nits |
| 4 | Theorem 7.1: finitely many minimizers; nonzero multiplier in (c) | correct | **minor:** under the note's own `P_ex` convention, LICQ fails on the sphere in Example 7.3, so the application needs one sentence |
| 5 | Lemma 5.5 hypothesis "`P_ex` polyhedral near `z*`", carried into Theorems 5.7 and 7.1(c) | correct and carried everywhere it is needed | `rho + t_1 < rho_ex` is implicit |
| 6 | Proposition 4.4(c): connected spiral | correct | "reach 0" is asserted without proof; the embedding sentence is imprecise |

## 1. Remark 6.3a(ii): a single-scale characterization fails

**What the gap hypothesis requires.** With exact alphaBB, `f_B = f - alpha q_B`.
- (G^pt_alpha) then holds with equality for any `f` and any `alpha`. Nothing
  about `f` is needed for the lower bound.
- The requirement on `alpha` comes from asking the relaxation to be a convex
  underestimator (Section 1.5): `alpha >= -min f''/2`, since `q_B'' = -2` in
  1D.
  - Termwise, `f'' = 4 pi^2 cos(2 pi K t) + (2 - 4u^2) e^(-u^2)` with `u = Kt`.
    The second term is at least `-4 e^(-3/2) = -0.8925`, so `alpha >= 20.19`
    suffices.
  - The note's cruder bound `-4 pi^2 - 2` needs `alpha >= 20.74`.
  - The numerical minimum of `f''` is `-40.2165` for `K >= 5`, which needs
    `alpha >= 20.11`.
  - So `alpha = 32` is valid for every `K`, as claimed.
- The two-sided gap is exact, so (U^q_32) holds, and hence (U_tau) with
  `tau = 8`. Also `kappa = 0`, `j_0 = 0`, and `L <= (2 pi + 0.86)/K`. All
  scheme constants are uniform in `K`.
- The covering step needs cubes of side `< 1/K` (the spacing of the `t_k`),
  which only requires `alpha > 8`. With `alpha = 32` and `eps < K^(-2)`, the
  side is `< 1/(2K)`, as the note says.

**Proof steps rechecked.**
- `1 - cos x >= 2x^2/pi^2` on `|x| <= pi` follows from Jordan's inequality
  `sin(x/2) >= x/pi`. So `m >= 8t^2` on `|t| <= 1/(2K)`. Numerically, the
  minimum of `m/(8t^2)` there is 1.11.
- On `|t| >= 1/(2K)`, `m >= K^(-2)(1 - e^(-1/4)) = 0.2212 K^(-2)`. The
  numerical minimum is `0.625 K^(-2)`.
- `E(eps)` is an interval of length at most `sqrt(eps/2)`. So
  `N_inf(E(eps), c sqrt(eps)) <= 1/(sqrt 2 c) + 1`; the note's `+2` is also
  valid.
- The count of `t_k = k/K` with `0 < |k| <= K/2` is `2 floor(K/2) >= K - 1`,
  and `m(t_k) = K^(-2)(1 - e^(-k^2)) <= K^(-2)`.
- Theorem 4.6 with `eta = K^(-2)` gives `N_opt >= (K-1)/2`. Counting `t_0 = 0`
  as well gives `K/2`, which matches the Summary's "`K/2^n`".
- At `eps = 0.2 K^(-2)` the single-scale bound is `O(log K)`. The conclusion
  holds even if an additive constant `C_0` (uniform in `K`) is allowed, as in
  Theorem 6.3.
- The restriction to *uniform* constants is necessary and correctly stated. For
  fixed `K`, `N_opt` grows only by about 1.5 per decade as `eps -> 0`, while
  the single-scale covering number stays 1. So a `K`-dependent constant does
  work.

**Exact 1D computation** ([`remark63a_family.py`](spatial-constrained-recheck/remark63a_family.py),
[log](spatial-constrained-recheck/remark63a_family.log)).
- *Method.* `N_opt` was computed by the greedy furthest-reach sweep. This is
  exact because `LB` can only increase on a sub-interval. Each `LB` is a 1D
  convex minimization, solved by root-finding on the derivative.
- *Robustness.* Every greedy interval was re-validated on a 4001-point grid.
  Perturbing `eps` by `±1e-7` (relative) never changed a count.
- *Other quantities.* `E(eta)` was found by grid detection plus root
  refinement. Covering numbers were computed by the exact 1D greedy.
  `Phi_alpha` is the maximum over 160 values of `eta`.

| `K` | `eps K^2` | `N_opt` | `(K-1)/2` | `N_inf(E(eps), sqrt(eps)/2)` | `N_inf(E(eps), sqrt(eps))` | `Phi_32(eps)` | `sup_{eta>=eps} psi` | `|T_bis|` | Thm 6.3 upper bound |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 0.2 | 10 | 1.5 | 1 | 1 | 8 | 8 | 35 | 1203 |
| 16 | 0.2 | 35 | 7.5 | 1 | 1 | 26 | 27 | 131 | 5463 |
| 64 | 0.2 | 131 | 31.5 | 1 | 1 | 101 | 107 | 515 | 27273 |
| 128 | 0.2 | 259 | 63.5 | 1 | 1 | 202 | 214 | 1027 | 60603 |
| 256 | 0.2 | 515 | 127.5 | 1 | 1 | 403 | 427 | – | 132993 |
| 256 | 0.02 | 543 | 127.5 | 1 | 1 | 427 | 427 | – | 166533 |
| 256 | 0.002 | 547 | 127.5 | 1 | 1 | 427 | 427 | – | 179343 |

- `N_opt ≈ 2.0 K`, about four times the proved `(K-1)/2`. The single-scale
  covering number is 1 on every row.
- `N_opt/Phi_32 ≈ 1.3`, and `N_opt >= Phi/2` holds on every row, as Theorem
  6.3 requires.
- `N_opt <= |T_bis| <=` the Theorem 6.3 upper bound on every row with
  `K <= 128`.
- `sup_{eta>=eps} psi` lies in `[Phi, 2 Phi]` on every row. This is consistent
  with Remark 6.3a(i).

*Nit.* `N_opt >= K/2` holds (count `t_0`), which is a little stronger than the
Remark's `(K-1)/2`.

## 2. The restated headline characterization

Checked against Lemma 6.1, Theorem 6.3 and Remark 6.3a(i).

- *Lower bound.* `2^(-n) Phi_alpha <= N_opt` is Theorem 4.6, applied for every
  `eta`. It needs only (G^LB_alpha).
- *Upper bound.* Every step checks:
  - a closed cube of side `s_j` meets at most `3^n` closed level-`j` cells;
  - the rescaling factor is `max(1, ceil(a))^n` with
    `a s_j = 2 sqrt((eps + t)/alpha)` at `t = Lambda s_j^2 - eps`;
  - there are at most `J` levels.

  So `|T_bis| <= 1 + 2^n [2^(n j_0) + 15^n max(1, ceil(2 sqrt(Lambda/alpha)))^n J Phi]`,
  as stated.
- *"Within `C log(1/eps)`"* is accurate with an eps-independent additive
  constant, or for `eps <= eps_0`. `J ~ (1/2) log2(Lambda s0^2/eps)`, and
  `Phi >= 1` absorbs `C_0`.
- *Remark 6.3a(i).*
  - For `eta >= eps`, the `eta`-term lies in `[2^(-n) psi(eta), psi(eta)]`.
  - For `eta < eps`, the term is at most `psi(eps)`. Both steps are correct.
  - In fact `Phi <= sup_{eta >= eps} psi` with factor 1, so the upper `2^n` is
    valid but loose.
  - The numbers above agree: `Phi <= sup psi <= 2 Phi`.
- The Summary item 5, the Interpretation after Remark 6.3a, and the Section 10
  row (Perevozchikov/Munos) all state the result consistently. The claim that
  the running supremum "is a lower bound for every certificate" holds up to
  `4^(-n)`.

**Nit (constant-level).** Remark 6.3a(i) calls `psi_alpha(eta)` a covering by
"balls of radius `eta` for the semi-metric `ell = (alpha/4)|x - y|_inf^2`".
- A cube of side `2 sqrt(eta/alpha)` has sup-radius `sqrt(eta/alpha)`. For that
  `ell`, it is a ball of `ell`-radius `eta/4`, or equivalently a set of
  `ell`-diameter `eta`.
- For radius `eta`, the semi-metric should be `ell = alpha |x - y|_inf^2`.
- Munos (2011) defines the near-optimality dimension with *packings* by
  `ell`-balls of radius `nu eta`, with a free constant `nu`. So the
  identification holds up to constants, and "Munos-type profile" is fair. The
  literal wording is off by a factor 4 in the radius.

## 3. Theorem 8.2(d), written out

All steps were re-derived.
- *Normal-bundle bijection.* For `R < tau_M`,
  `(y, nu) -> y + nu` is a bijection from the open normal `R`-disc bundle onto
  `N_R(M)`.
  - Injectivity holds because the nearest-point projection of `y + nu` is `y`
    when `|nu| < reach` (Federer 1959, Theorem 4.8(12)). The note says "by the
    definition of reach"; it is really this theorem.
  - Surjectivity holds because nearest points exist.
- *Jacobian.* The Jacobian is `det(I_p - A_nu)`, since the normal-connection
  part is block-triangular. `<A_nu u, u> = <II(u,u), nu>` and `|II| <= 1/tau_M`
  give eigenvalues in `[-|nu|/tau_M, |nu|/tau_M]`. Integrating over the fibre
  gives the stated `(1 ∓ R/tau_M)^p` bounds.
  - Niyogi–Smale–Weinberger (2008) state their Proposition 6.1 for smooth
    manifolds. For `C^2` manifolds the same bound follows directly from
    Federer's two-point inequality along curves in `M`. The note already uses
    that inequality (after Lemma 4.2), so citing it would close the gap.
- *Lower bound.* The following hold:
  - `N_R(M) subset X0` because `R <= r_0 <= dist(M, ∂X0)`;
  - `m < eps` on `N_R(M)`;
  - part (a) with `eta = eps` gives cubes of side `4 eps/alpha`;
  - covering needs at least `vol/delta^n` cubes.

  The constant `2^(-n-p) 2^((n-p)/2) 4^(-n) omega_(n-p) H^p alpha^n M_f^(-(n-p)/2) eps^(-(n+p)/2)`
  was checked symbolically (ratio exactly 1).
- *Upper bound.*
  - With `kappa = 0`, `v ≡ 0` and `j_0' = 0`, the `2^(n j_0')` term of part (b)
    is an empty sum, so dropping it is correct. The `3^n` could even be 1 here,
    because the witness lies in `D`, but `3^n` is valid.
  - (QG) gives `E(t) subset closure N_{r(t)}(M)`. Cells meeting the tube lie in
    the `(r + sqrt(n) s_j)`-tube.
  - The level conditions reduce to `s_j <= s_* = min(Lambda_1/(n c_g), c_g tau_M^2/(16 Lambda_1))`.
    This was checked symbolically.
  - The per-level bound and the final constant
    `2^(n+1) 3^n (3/2)^p 2^(n-p) omega_(n-p) H^p (Lambda_1/c_g)^((n-p)/2) (Lambda_1/eps)^((n+p)/2)`
    were checked symbolically (ratio exactly 1).
  - The geometric sum is at most 2, since `(n+p)/2 >= 3/2`.
  - The closed-versus-open tube issue is handled by continuity, since
    `2 r_j < tau_M`.
  - (Lip) is listed but unused (`kappa = 0`); this is harmless.
- *Numerics* ([`thm82d_check.py`](spatial-constrained-recheck/thm82d_check.py),
  [log](spatial-constrained-recheck/thm82d_check.log)).
  - Tube volumes of an ellipsoid with axes `(1, .8, .6)`, by Monte Carlo with
    4e6 points, match Weyl's formula `2RA + (8 pi/3) R^3` within 1–2 standard
    errors. They lie inside the `(1 ∓ R/tau)^2` bounds.
  - Exact counts of closed dyadic cells meeting the `r_j`-tube of a circle in
    `[0,1]^2` and of a sphere in `[0,1]^3` are 0.23–0.46 of the per-level
    bound on every level with `s_j <= s_*`.

## 4. Theorem 7.1: finitely many minimizers; nonzero multiplier in (c)

**Correct.**
- *(QG) with `N` minimizers.* The cluster-free Theorem 1, applied to degenerate
  boxes, gives `m >= (gamma/4)|y - z*|^2` on `F ∩ B(z*, rho)` at each `z*`.
  Outside the union of the balls, compactness gives `m >= c' > 0`. Then
  `c_g = min(gamma/4, c'/(n s0^2))` works with `dist_inf`; `c'/s0^2` would
  also work.
- The upper bound is Corollary 6.5(b) with `|M| = N`. The lower bound in (a)
  uses one minimizer with `d >= 1`, so the number of minimizers does not enter.
- Part (b) still assumes `N = 1`, which Proposition 6.8 needs.
- *(c).* "Some active non-exact constraint has a nonzero multiplier" is exactly
  `A' ≠ ∅` in Lemma 5.5.
  - Under (SC), active non-exact inequalities have `mu* > 0`. Equalities may
    have `lambda* = 0`, as the note says.
  - The upper bound of (a) uses Theorem 6.4, which does not use (G^LB). So
    "holds unchanged" is right.

**Remaining minor problem: LICQ in Example 7.3 on the sphere.** Theorem 7.1
counts active constraints of `P_ex` among the `g_j`. Example 7.3 follows the
Section 5 convention: `|y|^2 <= 1` is in `P_ex`, and the sphere adds
`g = 1 - |y|^2 <= 0`.
- At `±e_1` both constraints are active, with gradients `±2 e_1`. So LICQ
  fails, the multipliers are not unique, and `a = 2` would give `d = n - 2`
  instead of `n - 1`.
- The theorem still applies if the sphere is described as the equality
  `h = |y|^2 - 1 = 0` with `P_ex = R^n`. With that description:
  - LICQ holds, (SC) is vacuous, and (SOSC) holds since `c_1 > c_2`;
  - (G^LB) is unchanged;
  - (U_tau) holds, because `v = 1 - |z|^2 <= q_B` on `R_B`;
  - (EB) holds with `kappa = 1`, because `||z| - 1| <= ||z|^2 - 1|` on all
    of `X0`.
- The proof of Theorem 7.1(a) uses (KKT)–(SOSC) only to obtain (QG) and the
  graph structure of `S_loc`. Both depend only on `F` near `z*`.

*Suggested fix:* one sentence saying that (KKT)–(SOSC) may be verified in any
`C^2` description of `F` near `z*`. Alternatively, state the equality
description in Example 7.3. The same applies to the symmetry-breaking example
in Section 8.1, whose "LICQ holds on the half circle" also needs the equality
description.

The ball instances (`|y|^2 <= 1` alone active) are unaffected. The sphere is
exactly the case (`k = 1`, `±e_1`) that motivated the extension.

**Other nits.**
- Section 8.2's first bullet says "`O(1)` for the best certificate if `a = n`".
  This uses part (b), which needs a unique minimizer.
- The Section 10 Neumaier row still says "prefactor `(alpha/M_L)^((n-a)/2)`"
  without "lower-bound". Section 13 lists only 7.1, 8.2 and the comparison
  paragraph.

## 5. Lemma 5.5's polyhedral hypothesis

**Correct and carried through.**
- The hypothesis is in the statement of Lemma 5.5, and the proof uses it where
  it is needed. Active exact constraints have `grad·e = 0` and are affine, so
  they are constant along `y + te`; inactive ones keep their slack.
- Theorem 5.7 states it explicitly: "These include LICQ, `P_ex` polyhedral near
  `z*`, and some active non-exact constraint with a nonzero multiplier".
- Theorem 7.1(c) states it, as do Open problem 9 and the status table ("sketched
  only" for nonlinear exact constraints).
- Theorem 5.7 also needs `Z_eps(S) subset X0 ∩ P_ex` for Proposition 5.6. This
  follows from (OD).
- The descent constant `mu_0` and the violation constant `c_1` were re-derived.
- *Implicit condition.* Rays must stay inside `B(z*, rho_ex)`, where `P_ex` is
  polyhedral, so `rho + t_1 < rho_ex` is needed. This is covered by "for small
  `t`" and is harmless.

*Numerics* ([`lemma55_rays.py`](spatial-constrained-recheck/lemma55_rays.py),
[log](spatial-constrained-recheck/lemma55_rays.log)). The instance is
`min |y - c|^2`, with `c = (.5, -.3, 0)`, subject to the non-exact constraint
`|y| >= 1`.
- *Polyhedral case.* With `P_ex = {y_2 >= 0}`, `z* = (1,0,0)` has
  `mu = (0.5, 0.6)` and `d = 1`. The Lemma 5.5 direction is `e = (-1,0,0)`,
  with `mu_0 = 1/2` and `c_1 = 2.6`. It satisfies all three (OD) inequalities
  on 20,000 points of `F` near `z*`.
- *Nonlinear case.* Replacing `P_ex` by the curved `{y_2 >= 4(y_1-1)^2}` keeps
  the same KKT data and `e`. But the ray leaves `P_ex` immediately, already at
  `z*`: `P(z* + 1e-3 e) = 4e-6 > 0`.
- So the ray construction genuinely needs the new hypothesis. The conclusion
  (OD) may still hold with tilted rays, which is the sketched extension.

## 6. Proposition 4.4(c): the connected spiral

**Correct.**
- `r < rho < 2r`, `|rho'| < r` and `0 < rho'' < 2r` bound the polar curvature
  numerator by `10 r^2` and the denominator from below by `r^3`.
- `|c'| >= rho > r` makes the length infinite.
- On `B = [-2r, 2r]^2`, `q_B = 8r^2 - |c|^2 in (4r^2, 7r^2)`, so the integral
  is infinite.
- Injectivity and embedding follow because `|c(t)| = rho(t)` is continuous and
  strictly decreasing, so `c^(-1) = rho^(-1)(|·|)` is continuous on the image.

*Numerics* ([`spiral_check.py`](spatial-constrained-recheck/spiral_check.py),
[log](spatial-constrained-recheck/spiral_check.log)).
- The integral for `T = 10, 100, 1000` is 4.9802, 39.963 and 381.12. The
  note's 4.98, 40.0 and 381 are reproduced.
- The slope tends to `1/sqrt 7`.
- The actual supremum of the curvature is `1/r`, so `10/r` is valid but loose.

**Nits.**
- The embedding sentence says the curve "accumulates only on the circle of
  radius `r`". It also accumulates at `(2r, 0)` as `t -> 0+`. That point is not
  on the curve either, so the conclusion stands. The radius argument above is
  cleaner.
- "Reach 0" is asserted without proof. A one-line proof: points at the same
  angle on consecutive turns are `Delta = rho(t) - rho(t + 2 pi) -> 0` apart,
  with a nearly radial chord. Federer's two-point inequality then forces
  `reach <= Delta sqrt(rho^2 + rho'^2)/(2 rho) -> 0`. The log shows `Delta`
  going to 0: `3.3e-2`, `5.8e-4` and `6.2e-6` at `t = 10, 100, 1000`.

## Remaining problems (all minor)

1. **Theorem 7.1 / Example 7.3 (sphere) and the Section 8.1 half-circle
   example.** Under the `P_ex` convention, LICQ fails at the minimizers. Add
   that (KKT)–(SOSC) may be checked in any `C^2` description of `F` near `z*`,
   or use the equality description in the examples (Section 4 above).
2. **Remark 6.3a(i), Munos scaling.** Cubes of side `2 sqrt(eta/alpha)` are
   `ell`-balls of radius `eta/4` for `ell = (alpha/4)|·|_inf^2`. Use
   `ell = alpha |·|_inf^2`, or say "up to constants". The upper `2^n` in
   Remark 6.3a(i) can be 1.
3. **Theorem 8.2(d) citations.**
   - "By the definition of reach" should cite Federer's Theorem 4.8(12).
   - For `C^2` manifolds, the curvature bound `1/tau_M` follows from Federer's
     two-point inequality; NSW state it for smooth manifolds.
4. **Proposition 4.4(c).**
   - Add the one-line proof of reach 0.
   - Fix the "accumulates only on the circle" sentence.
5. **Wording leftovers.**
   - The Section 10 Neumaier row should say "lower-bound prefactor".
   - Section 8.2's "`O(1)` if `a = n`" needs a unique minimizer.
   - Remark 6.3a could state `N_opt >= K/2`.

## Commands run

All from `research-20260928b/reviews/spatial-constrained-recheck/`, at low
priority where they were longer than a few seconds:

- `python3 remark63a_family.py > remark63a_family.log` (about 45 s)
- `python3 spiral_check.py > spiral_check.log`
- `python3 thm82d_check.py > thm82d_check.log`
- `python3 lemma55_rays.py > lemma55_rays.log`

These are targeted checks of the revised statements. No project-wide checks
were run, CI was not inspected, the author's and the first reviewer's scripts
were not re-run, and nothing was committed.

## Not rechecked

- The pure wording revisions (Section 13, items 1–3, 6, 7, 9, 12, 15–17),
  except where noted above.
- Item 10 was checked by hand only. Dropping `eps <= t_0` in Theorem 6.7 is
  harmless: if `eps > t_0`, no level `j >= j_1` has a non-pruned cube, and the
  lower bound never used `t_0`.
- The Section 8.2 `B3_iso` numerics (item 13).
- The Section 9 sweeps.
- Literature claims.
