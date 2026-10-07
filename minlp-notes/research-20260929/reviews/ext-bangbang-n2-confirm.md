# Confirmation review of the revised `theory-bangbang/extension-n2.md`

Date: 2026-09-30. Referee: independent. I did not write the note, the first review
([Rev] = `reviews/bangbang-n2-review.md`), or the revision.
Scripts and logs: `reviews/ext-bangbang-n2-confirm-checks/` and its `logs/`.

## Verdict

**Verified. All nine review issues are fixed correctly. A few minor edits remain; none changes a
conclusion.**

- I recomputed every number that changed with my own code. I derived the model from the problem
  statement in Section 6.1 (sympy for `τ` and `σ`) and did not import `model.py` or
  `discrete.py`. Every changed number reproduces to the digits shown.
- I rechecked the new or rewritten proofs line by line: the short proof of Theorem 1, Lemma 14,
  Proposition 15, the revised Proposition 12, and the corrections to Propositions 4 and 6,
  Corollary 3 and Theorem 9. I found no error. Proposition 12 has two harmless imprecisions
  (item 4 below).
- No claim was silently strengthened, with one exception of wording: the bold "Consequence"
  sentence in Section 4.1 does not repeat that the blow-up of `P̄` is a floating-point result
  (item 1 below). Every withdrawn or corrected claim is marked where it appears and is listed in
  Section 11.

## Issue-by-issue check

| Review issue | Fix in the note | Result |
|---|---|---|
| 1a. The local result does not feed into [R, Theorem 4.1] | New Lemma 14, Proposition 15, Section 4.1, Summary item 4, Scope paragraph in Section 7, new open item | Correct (proofs and numbers below) |
| 1b. Theorem 2's calibrations violate (F) and the (H3) margin | New table in Section 7 | Reproduced exactly; also holds on the true reachable set |
| 1c. Qualifiers "(G-global)" and "continuous existence only" | Summary, Proposition 13 heading, Section 7 | Present |
| 2. Blow-up distances in example B | `singular_riccati_after` returns `t_events`; new values | Reproduced (table below); the code fix is correct |
| 3. Theorem 1: tangency is implied | Short proof; "no tangency is assumed" and "tangential or not" reworded; Summary says `C³` in `(t,x)` | Correct |
| 4. Lyapunov negative control | Section 6.2 and Summary say it is mainly a margin and far-region failure | Reproduced; see the observation in item 7 below |
| 5. Example C recursion, full `N` sequence | Table in Section 5 | Reproduced exactly, including the new `N = 500` entry |
| 6. B2 extrapolation | Labelled "expected behaviour, not tested" | Done |
| 7. "0.00575 for every `N`" | "Within one stage of 0.00575", with the measured values | Correct; break stages reproduced |
| 8. Proposition 12 needs `C²` in `t` | Time-averaged proof; piecewise-continuous `S_t` | Correct; two harmless imprecisions (item 4) |
| 9. Small errors and sources | Propositions 4 and 6, Corollary 3, Theorem 9; O–M line; citations | Correct; one citation can be completed (item 6) |

### Theorem 1 (short proof)

- **Step 2 (tangency at `τ+`).** Bounded derivatives up to order 3 make `S_t`, `S_x`, `S_xt` and
  `S_xx` uniformly continuous on the tube. So `r` and `∇_x r` extend to `t = τ` from the right.
  `r(t, x*, u) = σ(t)(u − u_b)` follows from exactness and `S_x = ψ`, so `r(τ+, x*(τ), ·) ≡ 0`.
  Minimality then gives `∇_x r = 0` at both vertices, and their difference is `Δβ(τ+)`. The step
  is correct.
- **Step 3 (comparison).** At `u*`, `r_xx(t, x*, u*) = M(t, u*)`, because the terms
  `S_xxx[g(x*, u*)]` in `r_xx` and in `Ṗ` cancel. With `E = Q_ε − P`,
  `Ė = −AᵀE − EA − (M − 2εI)`, and `E(T) ⪰ 0` gives `E ⪰ 0`. This is correct.
- **Wording.** The reworded remarks ("tangency is not a hypothesis, but the hypotheses imply
  it") are accurate. The Summary now says `C³` in `(t,x)` with bounded derivatives up to order 3.

### Lemma 14 and Proposition 15

- **Lemma 14.**
  - For quadratic `S`, `S_xxx = 0`, so `r_xx(t, x*, u°) = M(t, u°)`.
  - For `N = 0`, `M(t, u°) = M(t, u*)`, so the third-derivative term at `u°` never enters.
  - In both cases the margin gives
    `M(t,u°) − (Δ/(2|σ|))ββᵀ ⪰ (μ − Δ|β|²/(2|σ|))I ≻ 0`.

  The restriction to these two cases is appropriate. For non-quadratic `S` with `N ≠ 0`,
  `r_xx(t, x*, u°) − M(t, u°) = ω°·(third-derivative terms)`, so (H3) gives a condition on `S`,
  not on `P` alone.
- **Proposition 15.** I checked the identity `β̄β̄ᵀ − ββᵀ = Ebβ̄ᵀ + β̄bᵀE − EbbᵀE` and the
  resulting `Ė ⪯ −(ĀᵀE + EĀ) − cEbbᵀE`. Backward Lyapunov comparison from `E(τ−) ⪰ 0` is valid
  because `cβ̄ = O(1)`. Step 1 uses (J), Corollary 3 and Proposition 4 correctly.
  - The proof uses tangency of `P` only at `τ+`, so the hypothesis `β = O(|t−τ|)` for `P` is
    stronger than needed. That is safe.
  - The backward equation also has solutions with `β̄ → 0` logarithmically. They lie below the
    `O(|t−τ|)` solution, so they do not affect the argument. The numerical result does not
    depend on the start offset, which indicates that the integration follows the maximal
    solution.
- **Consequence for [R, Theorem 4.1].** (H3) includes tangency and, after [R]'s correction,
  `S_xx` Lipschitz in `t`, so `β = O(|t − τ|)`. An exact terminal term for `h → 0` gives
  `P(T) ⪯ Φ_xx`. Example C has `N = 0`. So the conclusion holds for every `S`, conditional on the
  float blow-up of `P̄`.

### Proposition 12 (revised proof)

- **Step 1.** Replacing `g(z̄_t)` by `g(y_θ, ū_t)` and `(s, y_θ)` by `(s, x*(s))` costs
  `O(hη_h)`, using the Lipschitz bounds on `S_xt` and `S_xx`.
  - On the switch stages the integrand is exactly `(ū_t − u*(s))β(s)`, and linear-rate tangency
    makes it `O(η_h)`.
  - The switch stages lie within `O(e_h + h)` of `τ`, by the KKT signs in (H4) and
    `|σ| ≥ γ_1|t − τ|`.
- **Step 2.** Only the chain rule along `θ` and Lipschitz continuity in `x` are used. Piecewise
  continuity of `S_t` in `t` is enough.
- **Steps 3–4 and the terminal term.** Correct. The radius `r_0 + e_h + Ch` is right.
- **Two imprecisions** (item 4 below). Neither affects the result.

### Small fixes

- **Proposition 6, `ξ < 0`.** On `[τ−|ξ|, τ]`, `σω = γΔ(τ − t)` and
  `ωβ_Lᵀd = Δ²η_L(t − τ + |ξ|)`. The integral is `½(D + Δ²η_L)ξ²`, which is correct.
- **Proposition 4 and Corollary 3.**
  - The case `η_ε = 0 ⇒ Xb = 0 ⇒ β_ε = 0` is correct.
  - The limit `bᵀ(Q_ε − P)(τ+s)b → η_ε` holds even if `P(τ+)` does not exist, because
    `bᵀPb = bᵀ(β + w)`.
- **Sources.** I downloaded Maurer–Osmolovskii (2003) and checked it:
  - Theorem 3.2 (Condition B ⇒ strict strong minimum) is quoted correctly;
  - Theorem 4.4 (`b_1 ≥ 0` plus `ω_0 > 0` on `K_0`) is quoted correctly;
  - Proposition 4.3, eqs. (56)–(57), is quoted correctly;
  - the reference-list entries for Maurer–Pickenhain and Noble–Schättler match the note.

## Recomputed numbers (independent code)

All runs are float. "Radau/LSODA" means plain-time integration with `rtol = 1e-12`. "log" means
DOP853 in `log(t − τ)`.

| Quantity | Note | My result |
|---|---|---|
| `τ` for A / B / B2 / C | 1.31546 / 1.19803 / 1.59551 / 1.40561 | 1.315455 / 1.198027 / 1.595511 / 1.405606 |
| B global model, `s_b` (`ε = 0` / `0.02`) | 5.754e-3 / 1.321e-2 | 5.7536e-3 / 1.32096e-2 (Radau, LSODA and log agree to 9 digits) |
| B local model, `δ_0 = 0.2 / 0.1`, `ε = 0` | 4.01e-3 / 2.40e-3 | 4.0061e-3 / 2.3958e-3 |
| same, `ε = 0.02` | 8.63e-3 / 4.99e-3 | 8.6269e-3 / 4.9872e-3 |
| Leading-order prediction / numerics | 1.40, 1.17 | 1.4014, 1.1717 |
| B2 `s_b`, `ε = 0` / `0.02` | 3.38e-7 / 1.10e-5 | 3.3765e-7 / 1.1047e-5 (LSODA and log; Radau stops with "step size too small" at `s = 3.3766e-7`) |
| Blow-up threshold `10¹⁰` instead of `10⁸` | — | changes `s_b` by `< 1e-9` |
| C, `P̄` from `P_max`, blow-up time (`ε = 0` / `0.02`) | 0.3520 / 0.4965 | 0.352020 / 0.496456 (Radau and DOP853; start offsets `10⁻¹⁰`, `10⁻⁷`) |
| same, eigenvalues at the event | `λ_min ≈ −1.2e8 / −1.4e8`, `λ_max = 0.081 / 0.024` | −1.237e8 / −1.432e8, 0.0806 / 0.0240 |
| A, `P̄` from `P_max` | no blow-up | no blow-up; `P̄(0)` agrees to 9 digits |
| localF: box-min of `r`, A (`ε = .02 / .01`) | −6.55 / −6.72 | −6.5467 / −6.7234 |
| localF: box-min of `r`, C (`ε = .02 / .01`) | −2.55 / −2.90 | −2.5511 / −2.8975 |
| localF: min (H3) margin, A / C (`ε = .02`, `.01`) | −70, −144 / −7.1, −15.6 | −69.98, −144.46 / −7.110, −15.611 |
| localF: fraction of sampled `t` failing | every `t` | 100% for both (F) and the margin |
| `|β|` of `Q_ε` on `[τ+0.02, T]`, A / C | 1.01–1.71 / 0.53–0.57 | 1.013–1.707 / 0.530–0.573 (union over `ε = .02, .01`) |
| lyapW5: (W5) fails on | `[0.349, 2]` | `[0.349, 2]`, one contiguous interval |
| lyapW5: `|β|` on the last arc | 0.99–1.69 | 0.9936–1.6869 |
| lyapW5: box-min of `r` negative on | `[τ − 0.183, T]` | `[1.1325, 2]` = `[τ − 0.18295, T]` |
| C recursion, `max|P|` at `ε = 0`, `N = 500 … 16000` | 11.4, 4.6, 22.7, 10.2, 88.0, 11.0 | 11.440, 4.582, 22.700, 10.239, 87.995, 10.996 |
| C recursion, interior stage | 500, 2000, 8000 | stages 351, 1405, 5622 (`N = 500, 2000, 8000`); none otherwise; one KKT point per `N` |
| C recursion, break at `ε = 0.02` | 42 (`N = 2000`), 378 (`N = 8000`), none otherwise | identical; `max|P| = 67.0` at `N = 500` |
| C recursion, `m_t` at the interior stage (`ε = 0`) | ≈ 0.27 | 0.2717, 0.2669, 0.2641 |
| B recursion, break stages after the switch | 2, 3, 6, 11, 23, 46 / 4, 6, 13, 26, 53, 106 | identical |

My discrete code enumerates KKT points with 0, 1 or 2 adjacent interior stages and checks every
sign condition. It finds the same interior stages as the author's active-set refinement, including
the two adjacent interior stages in B at `N = 500`.

**Extra check: box versus true reachable set.**

- Section 7 says Theorem 2's calibrations "are not calibrations on the reachable set", but the
  table uses the reachable *box*, which is an outer bound.
- I also minimized `r` over the true reachable set `R_t` of the double integrator (for each final
  `x_2`, the `x_1` range comes from the two tent paths). The minimum stays negative at every
  sampled `t` on `[τ+0.02, T]`:
  - A: −3.91 (`ε = 0.02`), −4.31 (`ε = 0.01`);
  - C: −2.55, −2.90 (same as the box).

  So the note's statement holds as written.

## Remaining problems (minor, most important first)

1. **The float caveat is missing from the bold "Consequence" sentence (Section 4.1).** "No `S`
   satisfies (H3) of [R, Theorem 4.1] together with an exact terminal term in example C" rests on
   the numerical blow-up of `P̄`. The Summary (item 4) and the status table say so. Section 4.1's
   bold sentence, and the Section 4 bullet "After review this is established for every
   global-model calibration", do not.
   - Suggested fix: add "given the (float) blow-up of `P̄` at `t = 0.352`".
   - The blow-up is robust: two independent implementations, four integrator/offset
     combinations, and `λ_min → −1.2·10⁸` while `λ_max` stays at 0.08. Still, it is not a
     rigorous certificate.
2. **Broken table in Section 9.** The section starts with a table header (`| item | status |`,
   `|---|---|`), then a paragraph, then the real table header. In GitHub-flavoured Markdown the
   paragraph lines become table rows. Delete the first two lines.
3. **Section 5, example C remark.** "At the vertex stages `m_t ≥ 0.45` when there is no interior
   stage": the minimum is 0.448 at `N = 4000` (`ε = 0`), in both the author's log and mine. Write
   "`≥ 0.44`".
4. **Proposition 12, step 1: two imprecisions with no effect on the result.**
   - "`a_t = O(e_h)` by (H4)". (H4) compares `p_{t+1}` with `ψ(t_t)`, so directly
     `a_t = p_t − S_x(t_t, x̄_t) = O(e_h + h) = O(η_h)`. Only `a_N = O(e_h)` holds as written.
   - The later bounds use `O(hη_h)` anyway, so nothing downstream changes.

   Now that I have checked the proof, the status line "revision not re-checked" can be updated.
5. **"(H3) implies (G-global)" versus Lemma 14.**
   - Definition 1.2 defines (G-global) for a given `ε > 0`. Lemma 14 gives (G) with `ε = 0`,
     strict at each `t ≠ τ`, which is what Proposition 15 needs.
   - The Scope paragraph in Section 7 and item 1 of Section 11 say "(H3) implies (G-global)".
     Suggested wording: "(G) with `ε = 0` at every `t ≠ τ`", as in Summary item 4.
6. **The Noble–Schättler journal version exists.** It is J. Noble, H. Schättler, *Sufficient
   conditions for relative minima of broken extremals in optimal control theory*, J. Math. Anal.
   Appl. 269 (2002) 98–128.
   - Found as reference [20] of arXiv:1506.00569. That paper also says the work covers broken
     extremals "with conjugate points occurring at or between switching times".
   - I did not read the paper. The note can cite it with "details from a secondary citation".
7. **Observation (optional): the pre-`τ` part of the Lyapunov failure depends on the box.**
   - Over the true reachable set, the continuous `Q_ε` residual of the Lyapunov control is
     negative only on about `[τ + 0.005, T]`, sampled every 0.01. The 0.183 time units before `τ`
     come from box states that cannot be reached.
   - The note compares box with box (discrete screening against the continuous box minimum), so
     its statements are correct. One sentence would prevent a reader from taking the pre-`τ`
     failures as intrinsic.
   - Related: in all five examples `x*(t)` lies on the boundary of `R_t`, because one-switch
     bang-bang trajectories bound the planar reachable set. Theorem 1 therefore concerns
     calibrations valid on full tubes, as its hypotheses state and as the standing assumption
     "`x*` interior to the state domain" requires. For `t > τ`, `x*(t)` is interior to the box,
     so it also covers box-valid calibrations after the switch.
8. **Pre-existing, not introduced by the revision.**
   - Section 4 says the example C continuations blow up "for every `δ_1` tried".
     `logs/caseC.log` shows one failed integration (`ε = 0.02`, `δ_1 = 0.05`, "step size too
     small").
   - Section 10 attributes the failure recorded in `logs/caseC.json` to `δ_1 = 0.1`, but the
     logged failure is at `δ_1 = 0.05`.
   - Both are minor, and Proposition 15 now makes them irrelevant to the conclusion.
9. **Wording nit in Theorem 1, step 1.** "`r_xx(t, x*, u) = M(t,u)` with `M` affine in `u`; for
   general `C³` `S`, `M(t,u°) − M(t,u*)` is bounded" is ambiguous. For non-quadratic `S`,
   `r_xx(t, x*, u*) = M(t, u*)`, but at `u°` there is an extra third-derivative term (as Lemma 14
   says). Step 3 uses only `u*`, so the proof is unaffected.
10. **Bibliographic nit.** Publication records give the Maurer–Pickenhain title as
    "Second-order sufficient conditions for *control problems* with mixed control-state
    constraints". The note copies the wording of the Maurer–Osmolovskii reference list ("optimal
    control problems"). I did not see the article itself.

## Not checked

- Theorem 2's construction, the cmax/clin/clin+3h screening, and the exact certificates. The
  revision did not change them, and [Rev] covered them (apart from the screening families).
- The sketches (Theorems 8 and 9) beyond the added necessity note.
- The Agrachev–Stefani–Zezza theorem itself, and the Noble–Schättler and Maurer–Pickenhain papers.
- Whether the discrete C recursion eventually breaks with `ε = 0` for larger `N` (open in the
  note).

## Commands run

All runs used `OMP_NUM_THREADS=1` (and `OPENBLAS_NUM_THREADS=1` for the continuous part) from
`reviews/ext-bangbang-n2-confirm-checks/`, each under `timeout`. These are targeted checks only:
no project-wide verification, no CI inspection, no commits. The longest run took about 3 minutes.

1. `python3 c_cont.py blowup` → `logs/c_cont_blowup.{log,json}`
2. `python3 c_cont.py cpre localF lyapW5` → `logs/c_cont_rest.log`,
   `logs/c_cont_{cpre,localF,lyapW5}.json`
3. `python3 c_disc.py C 500 1000 2000 4000 8000 16000` → `logs/c_disc_C.{log,json}`
4. `python3 c_disc.py B 500 1000 2000 4000 8000 16000` → `logs/c_disc_B.{log,json}`
5. Inline: Radau diagnostic for B2 (status message only).
6. Sources: Maurer–Osmolovskii (2003) PDF, read with `pdftotext` in `/tmp` (Theorems 3.2 and 4.4,
   Proposition 4.3, reference list); arXiv:1506.00569, reference list only; two web searches.

Files: `c_common.py` (model derivation, `τ`, `σ`), `c_cont.py` (Riccati, Lyapunov and far-region
checks), `c_disc.py` (Euler KKT enumeration and maximal recursion).

## Sources

- H. Maurer, N. P. Osmolovskii, *Second order conditions for bang-bang control problems*, Control
  Cybern. 32(3) (2003), [PDF](http://matwbn.icm.edu.pl/ksiazki/cc/cc32/cc3238.pdf).
- J. Noble, H. Schättler, J. Math. Anal. Appl. 269 (2002) 98–128, as cited in
  [arXiv:1506.00569](https://arxiv.org/pdf/1506.00569), ref. [20]; thesis record
  [mathgenealogy 38317](https://www.mathgenealogy.org/id.php?id=38317).
- Maurer–Pickenhain title: search results including
  [numdam AIHPC 2009](https://www.numdam.org/item/AIHPC_2009__26_2_561_0).
