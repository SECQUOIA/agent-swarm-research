# Author report: heights (Section 07 and Appendix F)

Author: Opus main-writing agent `heights`. Date: 2026-10-05.

## Files

Written: `sections/07-heights.tex` and `appendices/F-heights.tex`. No other
manuscript file, shared macro, bibliography, or historical note was edited.
Scratch compilation used `/tmp/heights-build` outside the repository.

## Coverage against the coverage map

| Map ID | Manuscript statement | Proof location |
| --- | --- | --- |
| H1 | `thm:heights-witness` (strictly feasible body, every rational point long, bounded box, circuit witness by citation) | Sketch in §7.2; full proof App. F.3 (`app:heights-witness`); construction `lem:heights-cube-chain` (F.2) |
| H2 | `thm:rational-height` (a), (b): quartic `f_k`, rational optimizer in `[-1,1]^n`, terminal denominators exactly `5^{2^k}` | `lem:heights-circle-denominators` (in §7.3, full proof), `lem:heights-circle-chain` and proof of the theorem (F.4) |
| H3 | `thm:rational-height` (c): rescaled quartic `\tilde f_k`, `2I ⪯ ∇²\tilde f_k(\tilde p) ⪯ (8(k+1)^2+1)I`, denominators divisible by `5^{2^k}` | F.4 |
| G1 | `thm:interior-gram` (a): `poly(L)2^{O(n)}` positive definite rational Gram and unweighted rational SOS | F.6 |
| G2 | `thm:interior-gram` (b), (c): family `h_k`, `0<m_k<M_k^{-2^{k+1}}`, short singular Gram, every PD Gram has `Ω(k2^k)` denominator bits | F.6 (`lem:heights-cube-moments`, `lem:heights-det-denominators`) |
| G3 | `thm:circuit-gram` plus validation limits (i)–(iv) | F.7 |
| G4 | `thm:heights-moment` (a)–(e), `rem:heights-moment-hypothesis`, `rem:heights-cyclic-fields` | F.5 |
| G5 | `cor:heights-gram` (a)–(d), and the homogenized Khachiyan remark | F.5 |
| G6 | `rem:heights-nullvector` (self-contained counterexample and the maximum-rank common-kernel fact) | in the remark |
| Shared T5 | `lem:taylor-sos` (a)–(e) with `rem:heights-gram-field` | F.1 |

The strictly feasible circuit witness of H1 is cited from Section 03
(`prop:upper-circuit-witness`) rather than reproved, following DECISIONS
("use the cleanest precise common statement once").

## Labels defined

Theorems and shared items: `thm:heights-witness`, `thm:rational-height`,
`thm:heights-moment`, `cor:heights-gram`, `thm:interior-gram`,
`thm:circuit-gram`, `lem:taylor-sos`.

Local lemmas and remarks: `lem:heights-circle-denominators`,
`lem:heights-cube-chain`, `lem:heights-circle-chain`,
`lem:heights-cube-moments`, `lem:heights-det-denominators`,
`rem:heights-gram-field`, `rem:heights-moment-hypothesis`,
`rem:heights-cyclic-fields`, `rem:heights-nullvector`.

Sections and appendix parts: `sec:heights`, `sec:heights-conventions`,
`sec:heights-witness`, `sec:heights-rational`, `sec:heights-moment`,
`sec:heights-gram-heights`, `sec:heights-interior`, `sec:heights-circuit`,
`sec:heights-summary`, `app:heights`, `app:heights-taylor`,
`app:heights-cube`, `app:heights-witness`, `app:heights-circle`,
`app:heights-moment`, `app:heights-interior`, `app:heights-circuit`,
`tab:heights-summary`, and equations prefixed `eq:heights-`.

Other chapters already reference `sec:heights`, `sec:heights-conventions`,
`app:heights`, `lem:taylor-sos`, `rem:heights-gram-field`,
`thm:rational-height`, `thm:interior-gram`, `thm:circuit-gram`, and
`thm:heights-moment`; all exist with the expected content.

## Shared lemma provided: `lem:taylor-sos`

Statement (Section 7.1): for a degree-at-most-four `f` with a real full
Hessian Gram `A` and any center `a`, with `d = X-a`, `b = ∇f(a)`:

- (a) `f = f(a) + bᵀd + zᵀ T_a(A) z`, with the explicit Taylor Gram
  `T_a(B) = ½(C_U+C_V/3)ᵀB(C_U+C_V/3) + (1/36)C_VᵀBC_V`, and the scalar form
  `∫₀¹(1-t)(u+tv)²dt = ½(u+v/3)² + (v/6)²`;
- (b) `A ⪰ 0` gives `T_a(A) ⪰ 0`; `A ≻ 0` gives `ker T_a(A) = R z(a)`
  (positive definite on the translated nonconstant monomials);
- (c) gradient completion for `A ⪰ μI`: `f = zᵀQ_a z` with
  `Q_a = T_a(Ā) + (μ/2)C_affᵀC_aff + c_a e₀e₀ᵀ`, `c_a = f(a) - ‖b‖²/(2μ)`;
  `Q_a ≻ 0` when `c_a > 0`;
- (d) Gram-entry field: entries lie in any real field containing the
  coefficients of `f`, the entries of `A`, the coordinates of `a` (and `μ`);
- (e) square factors: with `A = Σ s_k ℓ_k ℓ_kᵀ`, an explicit sum of squares;
  for rational `A ⪰ 0`, a sum of rational-coefficient squares whose
  coefficients are rational polynomials of degree ≤ 2 in `a`; at a critical
  point, `f - f(a)` is SOS over every real field containing the coordinates
  of `a`.

`rem:heights-gram-field` separates Gram fields from SOS fields, proves the
`√2 X₁²` example over `Q(√2)`, and points to Section 08 for least SOS
fields. Section 08's `lem:fields-tools`(e) duplicates part (e); the root may
replace that part by a citation of `lem:taylor-sos`(e).

## External labels used, and the exact content relied on

All were checked against the current files on 2026-10-05.

| Label | Owner | Content used |
| --- | --- | --- |
| `lem:quartic-realization` | 06 | With `m = n` residuals and the lemma's `μ` renamed `m` in F.2: hypotheses `mI ⪯ H`, `‖H‖ ≤ Λ`, `‖T_j‖ ≤ 1`, `‖b_j‖ ≤ β`, `Σ b_jb_jᵀ ⪰ ν²I`, `‖ℓ‖ ≤ ε = t² ≤ min{1, m²/(2n), ν²m²/(36n(Λ+nβ)²)}`; conclusions (a)–(c): degree four, `n+1` rational squares, `∇²F ⪰ (3/2)I`, unique zero/minimizer, rational PD canonical Hessian Gram computed from the factors. No `‖p‖` bound or approximation of `p` is needed. |
| `lem:newton-circuit` | 03 | Part (a) with `L'` at least the lengths of `(f, μ)` and of the degree-six observable `h`; uniform gap `g_{L'}`, `|h(x̂)-h(p)| ≤ g_{L'}/8`, nonzero divisors, no oracle calls. |
| `prop:upper-circuit-witness` | 03 | `min f < 0 ⇒ f(x̂) < 0` for the shared Newton point; applied to `g_k` with `μ = 1`. |
| `thm:exact-upper` | 03 | Context for the Newton construction. |
| `thm:quartic-complete` | 04 | (i): strict comparisons `f* > 0` and `f* < 0` are PosSLP-complete for certified quartics (used for validation limits (i), (ii)). |
| `thm:rational-optimizer` | 04 | Contrast only (comparison hardness versus unconditional length). |
| `thm:algebraic-cyclic` | 06 | (a) PD integer canonical Hessian Gram, minimum zero; (b) `[Q(p):Q] = d_n`. |
| `lem:models-det-trace` | 01 | `ρ(A) = det A/(tr A)^{m-1}`, which this chapter calls `μ_A`. |
| `lem:models-hessian-gram` | 01 | Part (a): `A ⪰ μI ⇒ ∇²f ⪰ μI`. |
| `lem:models-rational-squares` | 01 | Positive rationals as rational squares; rational PSD Gram to rational SOS. |
| `sec:models`, `sec:upper`, `sec:algebraic`, `sec:fields` | 01, 03, 06, 08 | Section pointers. |

## Macros

No new macro is required. The files use existing macros (`\R`, `\Q`, `\Z`,
`\norm`, `\ip`, `\tr`, `\diag`, `\rank`, `\Span`, `\height`, `\bits`,
`\poly`, `\PosSLP`) and inline `\operatorname{den}`,
`\operatorname{coef}`, `\mathcal T_a`, `\mathcal Q_a`.

## Notation decisions the root should reconcile

- This chapter uses capital `X` for variables, `z(X)` for the
  degree-at-most-two monomial vector of length `D = binom(n+2,2)`, and
  `w(X,v) = (v, X⊗v)` for the Hessian basis. Section 08 adopts these via
  `sec:heights-conventions`; Sections 03, 06 and Appendix E also use
  `w(x,v)`. Section 01 instead names the Hessian basis `z(x,v)` and the
  monomial vector `m_2(x)` with length `N`. Recommend unifying on `z`/`w`/`D`.
- `μ_A` here is `ρ(A)` of `lem:models-det-trace`; the text says so.
- `e = z(p)` in §7.4–7.5; the Hessian-basis coordinate vector in §7.2/7.6 is
  `ι_k` to avoid a clash.
- `M_k = 1000^{k+3}`, the same symbol Section 09 uses for the block family.
- Curvature upper bounds use `Λ`, per DECISIONS.

## Citation keys (proposed; Luna must verify statements and locators)

| Key | Source and locator relied on | Claim made in the text |
| --- | --- | --- |
| `BasuPollackRoy1996` | Basu, Pollack, Roy, *On the combinatorial and algebraic complexity of quantifier elimination*, J. ACM 43(6) (1996); Thm. 4.1.2, printed pp. 1031–1032 | Every connected component of a nonempty set `{P_1>0,…,P_s>0}` (integer polynomials, degree ≤ d, coefficient bits ≤ τ) contains a rational point with numerator and denominator bit size `τ d^{O(n)}`. Used with `s = 1`, `d = 6` (G1) and `d = 4` (comparison for H1). Verify the exact dependence on `s` and that the bound is for rational coordinates. |
| `SafeyElDinZhi2010` | Safey El Din, Zhi, *Computing rational points in convex semialgebraic sets and SOS decompositions*, SIAM J. Optim. 20 (2010); arXiv:0910.2973, Prop. 2.5 | Restates the strict-set rational sampling bound `ℓD^{O(n)}`. |
| `PatakiTouzov2024` | Pataki, Touzov, *How do exponential size solutions arise in semidefinite programming?*, SIAM J. Optim. 34 (2024) 977–1005; arXiv:2103.00041v2, pp. 2–3 | Recalls Khachiyan's system `x_i ≥ x_{i+1}²`, `x_m ≥ 2`. Also used as "compare" for the homogenized blocks. |
| `Lasserre2009` | Lasserre, *Convexity in semi-algebraic geometry and polynomial optimization*, SIAM J. Optim. 19(4) (2009) 1995–2014; arXiv:0806.3784v3, Thms. 2.6, 3.3 | Exactness and first-moment extraction for SOS-convex problems. **Section 00 cites the same paper as `Lasserre2008`; reconcile.** |
| `HeltonNie2010` | Helton, Nie, *Semidefinite representation of convex sets*, Math. Program. 122 (2010); arXiv:0705.4068, Lemmas 7–8 | SOS Taylor-integral principle for SOS-convex polynomials. |
| `ChuaPlaumannSinnVinzant2017` | *Gram spectrahedra*, Contemp. Math. 697 (2017); arXiv:1608.00234, Lemma 1.5 | Compactness of Gram spectrahedra. Key aligned with Sections 00/01; **Section 08 uses `...2016` for the same paper.** |
| `Laplagne2020` | Laplagne, *Facial reduction for exact polynomial sum of squares decomposition*; arXiv:1810.04215, Prop. 3.2, Sec. 3.2 (Prop. 3.4) | Real zeros as Gram kernel vectors and conjugate rational relations. |
| `KolmogorovNaldiZapata2024` | *Certifying solutions of degenerate semidefinite programs*, arXiv:2405.13625 | Algebraic exact SDP solutions and certification are established. |
| `GaertnerMagronVallentin2026` | *Sums of squares in polynomial time*, arXiv:2606.25118v1, Cor. 1.3 | Exact rational Gram in polynomial time given a supplied eigenvalue margin with its encoding. |
| `Jiang2021` | Jiang, *Minimizing convex functions with rational minimizers*, arXiv:2007.01445, Thm. 1.6, Def. 2.6 | Exact algorithm parameterized by a common-denominator (LCM vertex complexity) bound. |
| `Zhang2020` | J. Zhang, PhD thesis, *Complexity aspects of fundamental questions in polynomial optimization* (2020), Example 2.5.3 | Exponentially long rational local minimizers of nonconvex cubics via large magnitudes. |
| `BorweinWolkowicz1981` | Borwein, Wolkowicz, *Facial reduction for a cone-convex programming problem*, J. Austral. Math. Soc. Ser. A 30 (1981) | Facial reduction notion. |
| `PeyrlParrilo2008` | already used by Sections 00/08 | Rounding and projection to exact rational Grams. |
| `ODonnell2017`, `RaghavendraWeitz2017` | already used elsewhere; ITCS 2017 Thm. 1; ICALP 2017 Thm. 2 | Exponentially large coefficients in some constrained SOS proofs. |
| `SlotSteurerWiedmer2025` | in `references.bib` (v1) | Norm and approximation bounds do not bound denominators. |

No novelty is claimed from a failed search. The text credits Khachiyan-type
witnesses, strict-set sampling, Lasserre's exactness, Laplagne's kernel
relations, Kolmogorov–Naldi–Zapata, and the classical rank-versus-height
phenomenon, and states the contribution as the specific restricted
realizations.

## Responses to `evidence/reviews/prewrite-heights.md`

1. One input length `L`; families have `L_k = poly(k)`; every lower bound is
   stated as exponential in `n` and superpolynomial in `L_k`, never as
   `2^{Ω(L_k)}` (§7 introduction, each theorem, table). Done.
2. Witness bound stated for every rational point of the closed sublevel set,
   including the boundary (`thm:heights-witness`(b) and the localization in F.3). Done.
3. Moment relaxation stated precisely (unconstrained, order two, `y₀ = 1`,
   indices through degree four); the strict full Hessian Gram is the
   hypothesis; `rem:heights-moment-hypothesis` gives the SOS-convex
   counterexample and notes sufficiency is not necessity. Done.
4. Optimal-Gram height bound restricted to rank `D-1`; exposing claim
   restricted to PSD matrices orthogonal to all real optimal Grams; short
   lower-rank Grams stated in `cor:heights-gram`(d); rational-candidate
   restrictions excluded explicitly. Done.
5. Local conditioning kept local, with the explicit list of what is not
   claimed. Done.
6. Interior lower bound restricted to PD Grams in the full monomial basis;
   short singular rational Grams and unweighted SOS stated; all-PSD question
   stated as open. Done.
7. Upper bound described as a size bound with a supplied strict Hessian
   Gram, via the strict-open sampling theorem, not an algorithm in `L`.
   Done.
8. Circuit Gram: polynomial-size shared circuit, no sign oracle, identity on
   every valid input, `Q ≻ 0 ⇔ min f > 0`; no cheap validation, no
   unweighted SOS circuit. Strengthened: deciding PD of these circuit
   matrices is PosSLP-hard by `thm:quartic-complete`(i). Done.
9. No NP-nonmembership or certificate-finding lower bounds are claimed. Done.

Common quantitative lemma: provided by Section 06 as
`lem:quartic-realization` with canonical-Gram covariance; my appendix
restates exactly the hypotheses used (F.2). Specialized cubic realization:
adopted (F.2), with sharper constants (below).

## Simplifications and corrections relative to the source notes

None of the source theorems needed a mathematical correction. Changes:

1. **Cube chain without normalization or boxes.** Since `ξ_i = 1 + δ_i > 1`,
   the normalization `κ` is unnecessary (`κ = 1`), and the interval
   certificates of the general signed-root theorem are not needed; the
   approximation of `ξ_i` uses the contraction `|φ'(s)| ≤ 2|s|` of
   `φ(s) = (1+3s²)^{1/3} - 1`.
2. **Sharper witness constant.** Using `ξ₁³ = (M_k²+3)/M_k²` instead of a
   denominator `B < M³` gives
   `log₂ b > ((2^k-2)(k+3)log₂1000 - 4)/3`, and the clean consequence
   `log₂ b > k2^k` for all `k ≥ 2` (source: `(2^k-3)(k+3)log₂1000/3 -
   log₂270/3`).
3. **Interior family constants.** With `κ = 1`,
   `0 < m_k < M_k^{-2^{k+1}}` and the lower bound loses the `-1` (source:
   `4M^{-2^{k+1}}` and `-1`). Section 09's block result quotes
   `0 < m_k < 4M_k^{-2^{k+1}}`, which remains true.
4. **Cube exposing quadratic.** The audit's `E_i = y_i² - c_ix_i - ξ_is_i +
   ξ_i²r_i`, with a proof of `E_i = P_{ξ_i} + (ξ_i - x_i)(c_i - ξ_i³)`, the
   sharper local bound `H_i ⪰ I/2`, and explicit weights `2^{-10(i-1)}`.
5. **Canonical Gram covariance** (accepted improvement 1): no Gram
   approximation or coefficient projection anywhere in this chapter.
6. **Circle chains unified** in one lemma for radii `1` and `2^{-j}`, with the
   exact identity `E_j(P+u) = ‖u_j‖² - 2κ_j(t_{j-1}ᵀu_{j-1})²`; the
   Neumann-series bound gives `ν = 2^{-(k+1)}` and `β = 3` for `f_k`
   (source: `V = 4N`, `ν = V^{-(N-1)}`).
7. **Total-length form** of the maximal-rank Gram bound
   (`≥ H_k - log₂((D-1)!)` total bits) is proved alongside the per-entry
   bound.
8. **Validation limits** made precise: PD-ness of the circuit Gram is
   PosSLP-hard; the circuit witness's sign is PosSLP-complete; elimination
   pivots can vanish when `min f ≤ 0`.
9. **Taylor lemma** now has an explicit kernel statement, gradient
   completion, Gram-field and square-factor parts.

## Items flagged for the root

- **G6 ownership.** DECISIONS D10 gives G1–G6 to heights but also gives
  "nullvector boundaries" to contrast (K). I wrote a compact, self-contained
  `rem:heights-nullvector`; remove one copy if K also has it. The source
  note's comparison with the Burgdorf–Klep–Povh online manuscript (Thm.
  1.81(ii)) is deliberately not in the text; add it only after Luna verifies
  that manuscript.
- **Introduction wording.** `00-introduction.tex` (around the rational-points
  paragraph) attributes both the exact `5^{2^k}` denominators and the
  polynomial Hessian condition number to one family. In
  `thm:rational-height` these are `f_k` and `\tilde f_k`, respectively;
  `\tilde f_k` has denominators divisible by `5^{2^k}`.
- **Duplication with Section 08.** `lem:fields-tools`(e) duplicates
  `lem:taylor-sos`(e).
- **Length.** The main text is about 11 pages against the 6–8 page budget in
  `architecture.md`; the full witness proof was moved to the appendix. The
  remaining length is motivation, contracts, and source comparison. Further
  cuts are possible in the prior-work paragraphs if needed.

## Open questions stated in the text

Whether some certified family forces long encodings of every rational PSD
Gram (the all-PSD question) is stated as open; `h_k` shows that the interior
argument cannot settle it. No claimed theorem depends on an open question.

## Checks actually run

- Two `pdflatex` passes of a scratch harness in `/tmp/heights-build` that
  loads the paper preamble, `macros.tex`, `sections/07-heights.tex`, and
  `appendices/F-heights.tex`, with stub targets for the external labels
  listed above. Result: exit 0, no undefined references, no overfull or
  underfull boxes; only undefined citations, because the harness loads no
  bibliography (15 proposed keys plus `SlotSteurerWiedmer2025`). The two
  files render to about 22 pages (main text about 11).
- A scoped Python inventory of labels, references, citations, and macros in
  the two owned files, and a check for repository paths or unfinished-text
  markers: none found.
- Read-only inspection of other authors' current files to verify the shared
  interfaces above.

No project-wide verification, CI inspection, experiment, or mathematical
script was run. The full manuscript build was not run because other
chapters and Luna's bibliography are still in progress.
