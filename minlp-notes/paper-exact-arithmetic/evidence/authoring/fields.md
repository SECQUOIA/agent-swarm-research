# Author report: fields (Sections 08–09, Appendices G–H)

Author: Opus main-writing agent `fields`. Date: 2026-10-05.

## Status and files

Writing is complete. The fresh Sol reviews `fields-r1.md` (F-R1–F-R6) and
`fields-r2.md` (R2-1–R2-6) are resolved in the live files. The root's
in-flight corrections are incorporated. File hashes for the final review
snapshot are listed at the end.

Written: `sections/08-fields.tex`, `sections/09-certificates.tex`,
`appendices/G-fields.tex`, `appendices/H-certificates.tex`, and this report.
No other manuscript file, shared macro, bibliography, main file, historical
note, or literature KB was edited. Scratch builds used `/tmp/exactbuild`
outside the repository.

## Coverage against the coverage map

| Map ID | Manuscript statement | Proof location |
| --- | --- | --- |
| F1 | `prop:fields-four`: four variables, point `(α,α²,β,β²)`, `α³=2`, `β³=5`; rational PD full Hessian Gram, `∇²f⪰I`, minimum zero, `f∉W^Q(p)`, SOS over the degree-nine field `Q(α,β)`. Positive perturbations: `cor:fields-nonattainment`. | App. G.4 (`app:fields-four`); corollary proved in §8.2 |
| F2 | `ex:fields-ternary`: 31 monomials, coefficients ≤448, `∇²F⋆⪰I`, SOS or PSD Gram over real `E` iff `2^{1/5}∈E`. Three variables are minimal: `cor:fields-dimension` (one variable by direct argument; two variables via `lem:algebraic-bivariate-descent`). Perturbations: `cor:fields-nonattainment`. | Finite convexity certificate printed in App. G.3 (`app:fields-ternary`); field statements proved analytically there; corollaries proved in §8.2 |
| F3 | `thm:fields-prime`: every prime `ℓ≥5`, `(ℓ+1)/2` variables, `O(ℓ²)` monomials, `O(log ℓ)`-bit coefficients and Gram entries, construction time polynomial in `ℓ` (not `log ℓ`); other scales in `rem:fields-prime-scales`. | App. G.2 (`app:fields-prime`); part (d) in §8.2 |
| F4 | `thm:fields-tower`: `f_{k,λ}=λF_{k,0}-r_{k,3}^2` in `3k` variables, every rational `λ≥λ_k`, least field `Q(2^{1/5^k})` for both certificate types. | App. G.5 (`app:fields-tower`) |
| F5 | `thm:fields-individual`: Galois individual-degree lemma for `D=ℓ^k`; some coefficient or Gram entry has degree `≥5^k`. Input-length consequence restricted to `λ=λ_k` or short `λ`. | App. G.6 (`app:fields-individual`) |
| F6 | `thm:fields-compact`: shared fifth-root circuit; auxiliary-variable rational SOS of degree four, or degree five modulo the `3k` chain residuals only; all sizes polynomial in `L_λ=k+bits(λ)`. | App. G.7 (`app:fields-compact`) |
| F7 | `thm:fields-tower-spaces` (five relations per gate, independent products, `J_3=0`, `J_4=W`, unique `S`) and `cor:fields-recognition` (zero test, linear step, one PSD test). | App. G.8 (`app:fields-spaces`); corollary in §8.4 |
| F8 | `thm:fields-descent` (descent criterion) and `cor:fields-product-independence`; `prop:fields-cyclic` (dimension `n+1` for all `n≥4`). Cyclic `J_4=W` remains open; finite diagnostics for `n=2` and `4≤n≤16` are labelled as diagnostics only. | §8.5; App. G.9 (`app:fields-cyclic`) |
| R1 | `ex:fields-ternary-multiplier` (`b^T N b=8ωF⋆`, `N-8I≻0`); `lem:fields-affine-denominator` (degree two is minimal); general existence `prop:fields-radial-finite`, with the nonnegativity hypothesis and the `x²-1` counterexample. | App. H.4 (printed `b`, `N`, 15 minors); lemma in §9.2; App. H.6 (`app:fields-radial-finite`) |
| R2 | `cor:fields-tower-denominator`: (a) tower with scale `λ'_k`; (b) prime family `f_ℓ^{(c)}`. Uses the actual normalized factors `G_k/(tν)`, `r_{i,j}/ν` and explicit membership scalars. | §9.2 |
| R3 | `thm:fields-multiplier`: several quadratics `R_a` with affine membership and any rational symmetric `J`. | App. H.1 (`app:fields-multiplier`, zero identity `eq:fields-zero-identity`); H.2 shows that affine membership is a real restriction |
| R4 | `thm:fields-higher-membership`: degree-`d` membership, multiplier `ω^d`, factors of degree `≤d+2`, size polynomial in `binom(n+d,d)`, denominator `ω^{⌈d/2⌉}`. | App. H.3 (`app:fields-higher`) |
| R5 | `thm:fields-radial`: `f_t(X)=t^{-2}f°(tX)`, fixed Hessian at the minimizer; every fixed multiplier `u` with `u(0)>0` fails for large `t`; adapted denominator of size `O(L)`. | App. H.5 (`app:fields-radial`) |
| R6 | `thm:fields-radial-height`: computable `τ_N`, `ν(f_t)=Ω(log log t/log log log t)=Ω(log L/log log L)`; each `ν(f_t)` finite by `prop:fields-radial-finite`. | App. H.5 |
| B1 | `lem:fields-lift`; `thm:fields-blocks` (no rational separated certificate for `k=1`, least separated field `Q(2^{1/5^k})`, degree `5^k`, singular joint Grams); `thm:fields-blocks-height` (`Ω(k2^k)` bits). | App. H.7 (`app:fields-lift`); theorem in §9.4; App. H.8 (`app:fields-blocks`) |
| B2 | `thm:fields-blocks`(a): `tilde g=g+T_kB_k`, both blocks with rational full Hessian Grams `⪰I`; `thm:fields-blocks-height` with strongly SOS-convex blocks. | §9.4, App. H.8 |
| B3 | `thm:quadratic-graph` (owned by algebraic) is applied in `thm:fields-blocks` to produce `B_k`. | Section 06 |

## Labels defined

Section 08: `sec:fields`, `sec:fields-models`, `def:fields-certificates`,
`lem:fields-tools` (parts (a)–(d) only), `sec:fields-prime`,
`eq:fields-prime-functional`, `lem:fields-prime-functional`,
`thm:fields-prime`, `cor:fields-nonattainment`, `ex:fields-ternary`,
`eq:fields-ternary`, `cor:fields-dimension`, `prop:fields-four`,
`sec:fields-tower`, `eq:fields-tower-relations`, `thm:fields-tower`,
`thm:fields-individual`, `thm:fields-compact`, `sec:fields-spaces`,
`thm:fields-tower-spaces`, `cor:fields-recognition`, `sec:fields-criterion`,
`thm:fields-descent`, `cor:fields-product-independence`, `prop:fields-cyclic`.

Section 09: `sec:fields-certificates`, `sec:fields-formats`,
`eq:fields-multiplier-to-denominator`, `sec:fields-multipliers`,
`lem:fields-affine-denominator`, `thm:fields-multiplier`,
`thm:fields-higher-membership`, `cor:fields-tower-denominator`,
`prop:fields-radial-finite`, `ex:fields-ternary-multiplier`,
`sec:fields-radial`, `thm:fields-radial`, `thm:fields-radial-height`,
`sec:fields-blocks`, `lem:fields-lift`, `thm:fields-blocks`,
`thm:fields-blocks-height`.

Appendix G: `app:fields`, `app:fields-tools`, `app:fields-prime`,
`eq:fields-prime-exposing-bounds`, `eq:fields-prime-quartic`,
`rem:fields-prime-scales`, `app:fields-ternary`, `app:fields-four`,
`app:fields-tower`, `eq:fields-gate-exposing`, `eq:fields-gate-bounds`,
`app:fields-individual`, `app:fields-compact`, `app:fields-spaces`,
`app:fields-cyclic`.

Appendix H: `app:fields-certificates`, `app:fields-multiplier`,
`eq:fields-zero-identity`, `app:fields-membership-example`,
`app:fields-higher`, `eq:fields-level-identity`,
`app:fields-ternary-multiplier`, `app:fields-radial`,
`app:fields-radial-finite`, `app:fields-lift`, `app:fields-blocks`.

Other chapters reference `sec:fields`, `sec:fields-certificates`,
`app:fields`, `app:fields-certificates`, `ex:fields-ternary`,
`thm:fields-prime`, `thm:fields-tower`, `thm:fields-individual`,
`thm:fields-compact`, `cor:fields-tower-denominator`, `thm:fields-radial`,
`thm:fields-blocks`, and `thm:fields-blocks-height` (from 00, 01, 03, 04,
06, 07, 11, and K). All exist, and the descriptions there match the
statements, with one wording exception reported below.

## External labels used and the exact content relied on

All were rechecked against the current files on 2026-10-05.

| Label | Owner | Content used |
| --- | --- | --- |
| `lem:taylor-sos` | 07 | (a) Taylor Gram identity with integral remainder; (c) gradient completion `Q_a≻0` when `f(a)-‖∇f(a)‖²/(2μ)>0`, at a rational center; (e) at a critical point `a`, `f-f(a)` is SOS over every real field containing the coordinates of `a` (all sufficiency arguments). |
| `rem:heights-gram-field` | 07 | PSD Gram over `Q(√2)` of a polynomial that is not SOS over `Q(√2)`. |
| `sec:heights-conventions` | 07 | `z(X)`, `w(X,v)=(v,X⊗v)`, full Hessian Gram conventions. |
| `thm:heights-moment` | 07 | The real SOS program at minimum zero attains zero, with an algebraic optimal Gram (context in §8.2). |
| `thm:heights-witness`, `sec:heights-witness` | 07 | The construction before the theorem: `M_k=1000^{k+3}`, quartic `F_k` (sum of `2k+1` rational squares, unique zero), rational PD full Hessian Gram `A_k`, affine `u_k` with `0<δ_k=u_k(p)≤M_k^{-2^k}`. Section 09 calls these `F_k°`, `A_k°` and now says so explicitly. |
| `lem:quartic-realization`, `eq:algebraic-realization-data`, `eq:algebraic-realization-eps` | 06 | With `m=n`: the hypotheses in the two displays; conclusions (b) `∇²f⪰(3/2)I` and (c) `Γ_f⪰γI` with the printed `γ`, `θ`. |
| `eq:algebraic-canonical`, `lem:algebraic-gram` | 06 | Canonical Gram blocks `2bb^T+4g_0T`, `Δ(b,T)`, `Ξ(T)`; (a) Hessian identity; (b) covariance `Γ=Ψ_c^TΓ_cΨ_c`. |
| `lem:algebraic-bivariate-descent` | 06 | A rational bivariate quartic that is nonnegative, has exactly one real zero, and has a PD quartic form is a rational SOS. `cor:fields-dimension` checks exactly these hypotheses. |
| `thm:algebraic-cyclic` | 06 | Cyclic point `p_i=2^{e_i/d_n}`, `[Q(p):Q]=d_n`, integer convex SOS quartic with PD Hessian at `p`. |
| `thm:sos-length` | 06 | A globally convex real quartic of degree exactly four, vanishing with PD Hessian at a point, is not a sum of fewer than `n+1` real squares. |
| `thm:quadratic-graph` | 06 | Certified strongly convex rational quartic `B_k` with rational PD full Hessian Gram `A_{B_k}` and unique zero `w_*`. |
| `lem:models-det-trace` | 01 | `μ_A=det A/(tr A)^{h-1}≤λ_min(A)`. |
| `lem:models-rational-squares` | 01 | Positive rationals are sums of rational squares; a rational PSD Gram gives rational squares. |
| `sec:algebraic` | 06 | Section pointer. |

## Macros

No new macro is needed and no local macro is defined. The files use the
shared macros `\C`, `\N`, `\Q`, `\R`, `\Z`, `\diag`, `\ip`, `\norm`, `\tr`,
and inline `\operatorname{den}`, `\operatorname{Tr}`, `\operatorname{Gal}`,
`\operatorname{ord}`, and `\operatorname{Sym}`.

## Notation

- Following Sections 06–07: `X`, `z(X)`, `w(X,v)`, `μ_A`, and the canonical
  Gram `Γ(g)` with constant term `g_0`. This pass renamed the constant term
  from `γ` to `g_0` in 08, G, and H, because Appendix G also uses `γ` for
  the shared realization margin.
- `λ_k` is the tower scale in Section 08. The heights scale
  `⌈3/μ_{A_k}⌉` is written out in Section 09 to avoid a clash.
- Appendix G uses `\mathcal T` locally for a tridiagonal matrix. This is
  distinct from the heights Taylor Gram `\mathcal T_a`, and both are defined
  where used.
- `L` is binary input length; `L_λ=k+bits(λ)` is defined in
  `thm:fields-compact`.

## Citation keys, locators, and source contracts

Status is relative to the 33-entry `references.bib` of 2026-10-05.

| Key | Status | Locator and claim in the text | Used in a proof? |
| --- | --- | --- | --- |
| `BurgdorfScheidererSchweighofer2012` | present; contracts verified by Luna (literature review, rational radial row) | Thm 2.5 (pure-state positivity gives `r·g∈C`, integer `r>0`); Cor 4.12 (two pure-state types split at `ψ(u²)`, for an archimedean preordering `S` and an `S`-pseudomodule `C⊆I`); Prop 5.3(a) with Rem 5.5(1) (order unit `Σb_i²` of `(I²,M∩I²)`; the needed case is also proved directly); Thm 6.2 (archimedean positivstellensatz with an integer multiple). | Yes, H.6. The rational conclusion is derived in the rational sphere ring; BSS Thm 7.11 (real coefficients) is not used. |
| `Scheiderer2016` | present; Thm 4.1 verified by Luna (root message) | Thm 4.1: classification of rational nonnegative ternary quartic forms that are not rational SOS (behind `lem:algebraic-bivariate-descent`). Context only: Thm 2.1 and Cor 2.11 (real SOS not rational SOS; excluding any prescribed real number field); Thm 1.2 (trace-form totally real descent). | Thm 4.1 only, through the shared Section 06 lemma |
| `ChuaPlaumannSinnVinzant2017` | present | Lemma 1.6 (rational PSD Gram ⇔ rational SOS) and Remark 1.7 (failure over general ordered fields). | No |
| `Laplagne2024` | present | Section 3.1: a quaternary quartic form, attributed to Capco, Laplagne, and Scheiderer, that is SOS over `Q(2^{1/3})` but not over `Q`; it is not convex. | No |
| `Hillar2009` | **missing** | Thm 1.4: SOS over a totally real number field descends to `Q`. Thm 1.2: a rational polynomial with a PD real Gram has a rational one. Recorded notes disagree on the totally-real locator (Thm 1.4 versus Thms 1.4–1.5); please verify both locators. | No |
| `PeyrlParrilo2008` | **missing** | Rounding and projection of numerical Grams with a strict margin to exact rational certificates (recorded locator Prop. 8). | No |
| `DavisPapp2022` | **missing** | Rational interior weighted SOS have rational SOS decompositions (recorded locator Thm 2.6). | No |
| `KaltofenLiYangZhi2012` | **missing** | Exact certification via SOS of rational functions with rational coefficients; rounding plus exact verification. | No |
| `AhmadiParrilo2013` | **missing** | Thm 3.1: first-order convexity characterization of SOS-convex polynomials (`f(y)-f(x)-∇f(x)^T(y-x)` SOS). | No; context for `thm:fields-compact`(b) |
| `Reznick2005` | **missing** | Thm 1 and Cor 2: no single multiplier, and no finite menu, works for all nonnegative forms of a given degree and number of variables outside Hilbert's cases; scaling and closedness method. | No |
| `KojimaKimWaki2005` | **missing** | Real sparse/block SOS decompositions (context only; no specific theorem is used). | No |

The seven missing keys are the only undefined citations from these four
files in the scratch build. Every main proof is internal apart from the BSS
imports and Scheiderer's classification, which goes through the shared
bivariate lemma. Both of those source contracts are verified.

## Finite certificates (D6)

- `ex:fields-ternary` (App. G.3): `M⋆` is specified exactly by the center
  `(3/4,1,1/2)`, the canonical Gram formula, and the signs. The twelve
  leading principal minors of the integer matrix `2(M⋆-I)` are printed.
  This is the only finite computation for `F⋆`.
- `ex:fields-ternary-multiplier` (App. H.4): the basis `b` (15 cubics), the
  15×15 integer matrix `N` with entries of absolute value at most `4240`,
  and the fifteen leading principal minors of `N-8I` are printed.
- The counts "31 monomials" and "coefficients ≤448" are descriptive finite
  data about the displayed integer polynomial.
- No main theorem depends on a finite computation. The cyclic diagnostics
  are labelled as diagnostics and are not used in proofs.

The printed `N` rows, the 15 minors of `N-8I`, and the 12 minors of
`2(M⋆-I)` were compared as text against the recorded matrix literal and
review data (see Checks). They were not recomputed.

## Responses to reviews and root instructions

Prewrite `prewrite-sos-fields.md`:

- Arbitrary-field necessity is proved separately for square factorizations
  and for PSD Grams: obstruction functionals with kernel restriction
  `Qz(p)=0`, and the odd-radical lemma over arbitrary real fields. Every
  sufficiency proof exhibits squares via `lem:taylor-sos`(e).
- Canonical-Gram covariance replaces second approximations. It is used
  directly (`lem:algebraic-gram`) in G.3, and through
  `lem:quartic-realization` in G.2, G.4, and G.5.
- Minimum-zero promises are explicit.
- The dimension boundary is stated only under the strict full Hessian Gram
  hypothesis.
- Nonattainment is called rational certificate nonattainment, not a real
  SDP gap.
- The cyclic all-dimension descent application is not claimed.
- Format-specific scope is stated in both section introductions.

Prewrite `prewrite-descent-criterion.md`: the criterion is proved by the
segment-to-first-singular-PSD-point argument, including degree-four
preservation and uniqueness of `S`. Cyclic `I_2` has dimension `n+1` for
every `n≥4`. `J_4=W` is recorded only as finite diagnostics.

Sol R1 (`fields-r1.md`):

- F-R1: `L_λ` is used in `thm:fields-compact` and its proof.
- F-R2: nonnegativity is mandatory, and `x²-1` shows why. Finiteness has a
  complete rational proof in H.6 with verified BSS imports.
- F-R3: the cyclic diagnostic range is stated, and the notation `d_n`,
  `e_i`, `a` is defined locally.
- F-R4: the duplicate Taylor proof and private labels are removed in favour
  of the shared lemmas.
- F-R5: the actual normalized factors `G_k/(tν)` and `r_{i,j}/ν` are used,
  the affine membership `R=ν x_k(r_{k,2}/ν)-ν y_k(r_{k,1}/ν)` is explicit,
  and the prime family uses the `N_0/N_1` scalars.
- F-R6: `cor:fields-dimension` is restored with a full proof through
  `lem:algebraic-bivariate-descent`.

Sol R2 (`fields-r2.md`):

- R2-1: the order unit is required to lie in the cone, with a positive
  integer bound.
- R2-2: the BSS imports are specialized to an archimedean preordering and an
  `S`-pseudomodule. Corollary 4.12 is split at `ψ(u²)`, the conclusions are
  integer multiples, and rational SOS rescaling removes the integer.
- R2-3: the input-length consequence of `thm:fields-individual` is
  restricted to `λ_k` or short scales.
- R2-4: the derivation proof of algebraicity is given.
- R2-5: the exponent of `ω` depends on the quartic.
- R2-6: the Section 08 summary now states the `O(log ℓ)` bound per
  coefficient and per Gram entry.

Root in-flight instructions are all incorporated:

- PSD, not PD, wording in the Gram-field discussion.
- Citation of `lem:taylor-sos`(e) instead of a duplicate proof.
- The key `ChuaPlaumannSinnVinzant2017`.
- The recognition corollary wording, including the explicit zero.
- F2 minimality and radial finiteness restored with full proofs, without
  conditional demotion.
- Overfull lines at G270–277, G322–328, and H39 broken; the scratch build
  shows no overfull or underfull boxes in these four files.

Final-pass corrections (2026-10-05):

1. `γ` renamed to `g_0` for the constant term of a quadratic, to remove the
   clash with the realization margin `γ` in Appendix G.
2. Section 08 summary (d) now matches `thm:fields-descent`: minimum zero at
   `p` with PD Hessian, and a degree-four baseline. The old wording
   "nondegenerate zero" did not force `∇F(p)=0`.
3. Section 09: the Kojima–Kim–Waki sentence now claims only that real sparse
   decompositions are studied there. Real separation for these quartics
   follows from `thm:fields-blocks`(b) with `E=R`. The sentence "real
   block-separated certificates exist whenever the blocks have zero minima"
   was false in general (it fails for non-SOS nonnegative blocks). It is now
   scoped to certified blocks via `lem:taylor-sos`(e).
4. `thm:fields-blocks-height` states that `F_k°` and `A_k°` are Section 07's
   `F_k` and `A_k`, and that the variables are renamed `ξ`.
5. Reznick locator added, with scope stated as nonnegative forms of a given
   degree and number of variables.
6. "route" wording in §8.2 and §8.5 replaced by direct statements.

## Cross-interface notes for root (files I do not own)

- `sections/00-introduction.tex` lines 434–441 describe the descent
  criterion with "every rational convex quartic with a nondegenerate zero at
  that point". `thm:fields-descent` requires `F(p)=0`, `∇F(p)=0`, and
  `∇²F(p)≻0`, that is, minimum zero at `p` with PD Hessian. A convex quartic
  can vanish at `p` with nonzero gradient. Suggested wording: "every rational
  convex quartic with minimum zero at that point and positive definite
  Hessian there".
- The introduction cites `Laplagne2023` (absent from `references.bib`) for
  cubic-field quartic forms; Section 08 cites `Laplagne2024`, Section 3.1.
  If these are versions of one paper, unify the keys.

## Checks actually run

- Scoped scratch builds: `pdflatex -interaction=nonstopmode
  -output-directory=/tmp/exactbuild main.tex` (several passes), plus
  `bibtex main` in `/tmp/exactbuild` with a copy of `references.bib`. The
  build is needed to resolve cross-file labels; diagnostics were filtered to
  these four files. Final result: 0 LaTeX errors, no undefined or
  multiply-defined labels anywhere, and no overfull or underfull boxes in
  08/09/G/H. The one remaining overfull box is in
  `appendices/J-quadratic-contrast.tex`. Undefined citations from these
  files are the seven missing keys above.
- Visual check: `pdftoppm` renders of the scratch PDF pages with the
  12-minor table (G.3) and the 15×15 matrix `N` (H.4). Both are legible and
  unclipped.
- Text comparison (Python regex, no execution of any check script): the
  printed `N` rows against the matrix literal in
  `research-20260927/check_ternary_rational_sos_quadratic_multiplier.py`;
  the 15 minors of `N-8I` against
  `research-20260927/rational-denominator-certificate-fresh-review.md`; the
  12 minors of `2(M⋆-I)` against
  `research-20260927/ternary-rational-sos-convex-counterexample.md`. All
  matched.
- `grep` scans of the four files for labels, references, citation keys,
  macros, disallowed phrasing (companion/independently reviewed/repository
  history/local links), and symbol reuse.
- Not run: mathematical scripts, experiments, project-wide verification,
  CI inspection, browsing, or literature research.

## Limits and open questions

- Cyclic `J_4^Q(p)=W^Q(p)` for all `n≥4` is open. Finite diagnostics for
  `n=2` and `4≤n≤16` are not proofs.
- `prop:fields-radial-finite` gives no bound on the exponent and no
  certificate size. The radial lower bounds do not use it.
- All size lower bounds are format-specific: dense or individual algebraic
  coefficients, prescribed radial multipliers, and block-separated
  certificates. None is a bound for unrestricted certificates or a
  complexity lower bound for deciding nonnegativity. The question of the
  size of all PSD rational Grams remains open.

## Final snapshot hashes

SHA-256 of the owned manuscript files at completion (2026-10-05):

```text
9632246abe6bae143ce0bdb876f3be63566605e895cc56b7e5391f8311af53e8  sections/08-fields.tex
e324e1a841f5ef489714111aeb8ed6d3b920595f6802a1e89788e334e1e45045  sections/09-certificates.tex
5be7a9e5525935d2cba80d49035f60c680148b9cc52739a87b1f0ea23dc2d7a0  appendices/G-fields.tex
37ca5a03d9cbb382b9ffe327ab6894e3b43664f9a2c9e405527a37fa47f1a7c5  appendices/H-certificates.tex
```
