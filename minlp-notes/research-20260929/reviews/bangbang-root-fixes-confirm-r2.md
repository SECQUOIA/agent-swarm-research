# Confirmation of the third revision of `theory-bangbang/report.md`

Date: 2026-09-30. Referee: independent. I did not write the report, the
verification, the earlier confirmations or any of the revisions. Scope: the
three issues raised in `reviews/bangbang-root-fixes-confirm-r1.md` and the
reviser's list of applied changes (Section 9.3 of the report). Scripts and
logs: `reviews/bangbang-root-fixes-confirm-r2-checks/` (`r2_checks.py`,
`logs/r2_checks.log`).

## Verdict

**All three issues are fixed correctly, and every changed number
reproduces. Nothing was refused, so there are no refusals to judge. No claim
was strengthened.** One optional nit remains in the new Theorem 4.1
parenthetical. It changes no conclusion.

I compared the revised text with the pre-revision text, which the round-2
confirmation had read. I recomputed the scalar example with my own script,
using methods that differ from the reviser's `revision3_checks.py`:

- the exact data come from hand-derived closed forms in rational arithmetic
  (Python `Fraction`, not sympy integration);
- `F'(τ)` and `F''(τ)` come from exact finite differences of `F(θ)`, which
  is a cubic in `θ`;
- the global-form blow-up comes from two methods: the linearization,
  integrated with mpmath's Taylor-series ODE solver at 30 digits, and a
  direct LSODA integration of `P` to the event `P = −1e8`.

I checked the title against the PDF and the mathdoc record myself.

## Item-by-item check

| item | result |
|---|---|
| 1. Remark 3.3, sign of `η_L` in the global form | **Fixed.** See the details below. |
| 2. Theorem 4.1 regularity | **Fixed.** See the details below. |
| 3. Maurer–Osmolovskii title | **Fixed.** Page 1 of the linked matwbn PDF (30 pages, "Control and Cybernetics vol. 32 (2003) No. 3") prints "Second order optimality conditions for bang–bang control problems". The mathdoc record gives "Second order conditions for bang-bang control problems" (`citation_title`), with pages 555–584. The entry now uses the printed title and notes the record's shorter one. The Sources preamble says that the title was checked against the PDF. |
| Section 9.3, header, status table, Section 8 item 9 | Accurate. The header records the round-2 confirmation and says that the third revision has not been re-checked. The Proposition 3.1 row's note, "re-derived step by step by the round-2 confirmation", matches that report. The numbers in C1 match my recomputation (below). |

### Issue 1 (Remark 3.3)

**The text.** The false sentence is gone. It now reads "`η_L < 0` forces the
blow-up even when the SSC holds". This direction is correct in both forms:

- The singular term is positive semidefinite, so backward comparison gives
  `P̂ ⪯ Q_ε`.
- If `η_L < 0`, then `η_ε < 0`, and the coefficient `1/|σ|` is not
  integrable, so the solution blows up after `τ`.

Changing "in the layer after `τ`" to "after `τ`" is right for the global
form, where the blow-up need not be in the layer.

The new bullet correctly says three things:

- the singular term acts on the last arc;
- `η̂ = bᵀ(P̂b − w) ≤ bᵀ(Qb − w) → η_L`, as in [E, Theorem 8];
- `P̂` can blow up with `η_L > 0`, at a conjugate point of the relaxed LQ
  problem ([E, Summary item 3]: "can appear on both arcs").

"Need not lie near `τ`" is shown by the example itself. The qualifier "if
`P̂` is still finite there" makes the near-`τ+` dichotomy consistent with
that example.

**The numbers** (my `r2_checks.py`):

- Data: `x(0) = 101/100`, `k = 399/1000`, `ψ(T) = −51/100`.
- On `(0, 1]`, `σ(τ − s) = s/100 + s²/2 > 0` and `σ(τ + s) < 0`, so the
  minimum-principle signs hold.
- `σ̇(τ) = −1/100`, `D = 1/50` and `η_L = 1/10`, all exact.
- `F'(τ) = 0` and `F''(τ) = 21/50 = D + 4η_L`, exact.
- Global-form blow-up: `t_b = 1.5873281` for `ε = 0` and `1.5963495` for
  `ε = 0.01`. The mpmath linearization and LSODA on `P` agree to 7 digits.
- The report's "`t = 1.587`, 0.587 time units after `τ`" and
  "`t = 1.596` for `ε = 0.01`" are correct, and they are labelled float.
- Local formulation: `P` stays bounded, with `P(τ + 1e-12) = 0.00046` for
  `δ_0 = 0.05` and for `δ_0 = 0.2` (Section 9.3 rounds this to 0.0005).
- Second set (`x(τ) = 0.5`, `Φ_xx = −1.1`): `η_L = −1/10`, `D = 1` and
  `F''(τ) = 3/5`, all exact. The global form blows up at `t = 1.3777696`.
  The local formulation blows up at `s = 7.008e-4` (`δ_0 = 0.05`) and
  `1.385e-2` (`δ_0 = 0.2`). All values match Section 9.3.

**The Scope paragraph after Theorem 4.1.** The new sentence is correct. The
example has constant `b` and `ℓ_1 = 0`, so [E, Lemma 14] turns (H3) into
`Ṗ > −1 + P²/|σ|` for `t ≠ τ`. An exact terminal term gives
`P(T) ≤ Φ_xx = P̂(T)`. The blow-up is after `τ`, where `|σ|` is bounded away
from 0, so ordinary backward comparison gives `P ≤ P̂`. That rules out a
bounded `P = S_xx(t, x*(t))`. Unlike Example C, this needs no comparison
through the singular point.

**Other places.** The Summary, the Section 6 open list and the status-table
row are consistent with the corrected Remark. Each says that the sign of
`η_L` decides only in the local formulation, and each labels the blow-ups
as float results.

### Issue 2 (Theorem 4.1 regularity)

**The parenthetical** now requires three things:

- `∂_tS` is `C²` in `x`;
- `∂_tS`, `∇_x∂_tS` and `∇²_x∂_tS` are continuous on each side of `τ` and
  extend continuously up to `τ` from each side;
- `S_xx` is Lipschitz in `t`.

This covers the one-sided hypotheses on `∂_tS` in Proposition 3.1. It also
covers the `∇²_x∂_tS` term inside `∇²_x r` in (H3).

**The tangency-redundancy remark.** I re-derived it. Take `t ≠ τ` and put
`d = x − x*(t)` and `ω = u − u*(t)`. The following identities hold at
`x*(t)`:

- `r = σω`, and `σω ≥ 0` by the sign condition;
- `∇_x r = βω`, from the costate equation, because `S_x(t, x*(t)) = ψ(t)`;
- `∇²_x r ⪰ μI` on the convex tube.

Together they give `r ≥ |ω|(|σ| − Δ|β|²/(2μ)) ≥ 0` on the tube. Then
Proposition 3.1 applies.

**Step (c).** With the new regularity, a Schwarz-type interchange gives
`∂_t S_xx = ∇²_x∂_tS` on each side, and `S_xx` is Lipschitz across `τ`. So
the difference quotient `(S_xx(t_{t+1}) − S_xx(t_t))/h` is an average of
`∇²_x∂_tS`. It tends to `∇²_x∂_tS` uniformly on each side (uniform
continuity on each closed side of a compact tube). At the stage containing
`τ`, it is a convex combination of the two one-sided limits. The other
terms of `∇²_xρ_t/h` involve `S_x`, `S_xx` and `∇³S`, which are continuous
across `τ`. So `∇²_xρ_t = h[r_xx + o(1)] ⪰ hμ/2`, as stated.

Replacing `O(h + e_h)` with `o(1)` weakens the step, and the `O(·)` rate
would indeed need a Lipschitz condition on `∇²_x∂_tS` in `t` that is not
assumed. Only `⪰ hμ/2` is used downstream. Step (e) still uses the Lipschitz
condition on `S_xx`, which is assumed. No conclusion changes.

## Remaining issue (optional nit)

**Theorem 4.1 parenthetical and Section 9.3, C2: "These conditions include
the regularity hypotheses of Proposition 3.1" is not quite literal.**
Proposition 3.1 assumes that `S`, `S_x` and `S_xx` are continuous in
`(t,x)`. Section 9.3 argues that "`S` and `S_x` are continuous in `t`
because `∂_tS` and `∇_x∂_tS` are bounded on each side". Bounded one-sided
derivatives give continuity on each side and one-sided limits at `τ`, but
not continuity across `τ`.

- For `S_x`, continuity across `τ` still holds, for a different reason:
  `S_x(t, x*(t)) = ψ(t)` is continuous, and `S_xx` is jointly continuous
  (it is Lipschitz in `t` and `C²` in `x`). Integrating `S_xx` along the
  segment from `x*(t)` to `x` gives continuity of `S_x` at `τ`.
- `S` itself can jump at `τ`, but only by a constant (take `S + c·1{t > τ}`).
  The proof of Proposition 3.1 never uses `S` itself, so nothing breaks.

*Fix (optional):* add "`S` continuous in `t`" to the list. Alternatively,
say that the list gives Proposition 3.1's hypotheses except continuity of
`S` itself at `τ`, which the proof does not use. The reasoning in Section
9.3 could cite `S_x(t, x*(t)) = ψ(t)` for `S_x`.

## Noted, no change requested

The Summary's phrase "the global form that Theorem 4.1 needs" was already
there before this revision. Strictly, (H3) implies the global form only for
quadratic `S`, or when `b` is constant and `ℓ_1` affine ([E, Lemma 14]). The
Scope paragraph and Section 6 state that condition, and both examples
satisfy it. This is not an issue that this revision introduced.

## Commands run

All from `reviews/bangbang-root-fixes-confirm-r2-checks/`, with
`OMP_NUM_THREADS=1`. These are targeted checks only. I ran no project-wide
verification and inspected no CI.

1. `OMP_NUM_THREADS=1 timeout 300 python3 r2_checks.py > logs/r2_checks.log`
   (the scalar example and the second parameter set; under 1 s). The first
   run built the fractions from binary floats. I fixed that to use decimal
   strings and reran it; the log is from the second run.
2. `cat theory-bangbang/logs/revision3_checks.log` and
   `theory-bangbang/revision3_checks.py`: I read the reviser's script and
   log for comparison only. My values agree with them.
3. `curl` of `http://matwbn.icm.edu.pl/ksiazki/cc/cc32/cc3238.pdf`
   (`pdfinfo`: 30 pages; `pdftotext` of page 1) and of
   `https://geodesic.mathdoc.fr/item/CC_2003_32_3_a8/` (`citation_*` meta
   tags), both in `/tmp`, deleted afterwards.
4. I read [E] (`theory-bangbang/extension-n2.md`): Summary items 1–4,
   Theorems 1, 2 and 8, Corollaries 3 and 7, Proposition 6, Lemma 14 and
   Proposition 15. I read the pre-revision text of the report from the
   round-2 confirmation's session record, to compare the before and after
   versions.
