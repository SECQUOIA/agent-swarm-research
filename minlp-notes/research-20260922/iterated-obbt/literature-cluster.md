# Iterated OBBT: cluster-problem and convergence-order literature check

Date: 2026-09-23. Status: targeted novelty check for `theory.md` (tangent map
`Phi`, limit `Q`, constant `r*(Phi)`, Theorems 4 and 6, Propositions 3, 7
and 8). This check supplements `literature.md`, which did not read these sources.

## Reading status

| Source | Access | What was read |
|---|---|---|
| Wechsung, Schaber, Barton, JOGO 58 (2014) | Initially journal PDF blocked; user-supplied journal PDF added and read in the 2026-09-26 inbox review | Initially thesis Ch. 2 (pp. 29–41); journal PDF pp. 8–9 confirms the prefactor thresholds |
| Wechsung, PhD thesis, MIT 2014 (`yoric.mit.edu/wp-content/uploads/2014/04/WechsungThesis.pdf`) | Open | Ch. 1 §1.1.2, §1.2.2; Ch. 2; App. A; grep of the rest |
| Kannan & Barton, JOGO 69 (2017), author manuscript (MIT OA) | Open | Full text: §§1–3, Lemmas 1–3 and 8, Theorem 3, Corollary 4, Remarks 5 and 9, Conclusion |
| Kannan & Barton, JOGO 71 (2018) | Open | Domain-reduction passages, Examples 6 and 16–18, Conclusion |
| Kannan, PhD thesis, MIT 2018 (`rohitkannan.github.io/PDFs/Kannan_MIT_PhDThesis.pdf`) | Open | §1.2, §2.3.2.2 (bounds tightening), §2.3.2.1.2 (review of BM 2012), Ch. 7; Ch. 5–6 are the two papers |
| Du & Kearfott, JOGO 5 (1994), preprint `interval.louisiana.edu/preprints/multcluster.pdf` | Open | Full text |
| Bompadre & Mitsos, JOGO 52 (2012) | **Not accessible** (closed; Caltech repository 403) | Only restatements in BMC 2013 §2 and Kannan thesis pp. 56–58 |
| Bompadre, Mitsos, Chachuat, JOGO 57 (2013), Imperial Spiral author version | Open | §§1–2, Appendix A |
| Neumaier, Acta Numerica 2004, §15 (local KB) | Open | Full §15 |
| Schichl, Markót, Neumaier, "Exclusion regions for optimization problems", JOGO 2014, preprint | Open | §2 (cluster effect), §3 |
| Locatelli & Schoen, SIAM 2013, §5.5 | **Not accessible**. The ETH table of contents confirms §5.4 "Convergence and finiteness results" (p. 326), §5.5 "Domain reduction" (pp. 335–357), and §5.6 "Fathoming rules" (p. 358). Google Books search was blocked by a captcha | — |
| Caprara & Locatelli, Torino technical report, 2008 | **Not found** online | — |

## Short answers

- **(a)** None of these sources defines a limiting scaled relaxation like `Q`. None defines a direction- or shape-dependent quantity like `r*(Phi)`. Every result uses one scalar upper-bound prefactor (`K` or `tau`) and compares it with one scalar curvature constant: the smallest Hessian eigenvalue `lambda_1` or the growth constant `gamma`. One precise link exists. The scalar no-clustering threshold (`K <= lambda_1/8`, or `tau* <= gamma/8` in Kannan and Barton's version) is the same number as the contraction threshold `tau < mu/4` in `theory.md` Proposition 3, with `mu = lambda_1/2` or `gamma/2`. See §3.
- **(b)** None of these sources analyzes bound-tightening or OBBT rates. Domain reduction appears in three roles only:
  - an optional acceleration device (Du–Kearfott; Wechsung §1.1.2);
  - a set `X(Z)` that raises the convergence order in reduced space (Kannan–Barton 2018);
  - backboxing or exclusion regions (Neumaier; Schichl–Markót–Neumaier).

  Kannan's thesis states the related question as open.
- **(c)** No result implies Theorem 4, Theorem 6, Proposition 7 or Proposition 8. Proposition 3's threshold corresponds to Wechsung–Schaber–Barton (WSB) Theorem 1(a) and Kannan–Barton 2017 Theorem 3 case 1, so Proposition 3 should cite them.
- **(d)** The known results are sufficient, scalar, worst-case covering bounds for branch and bound. `r*(Phi) < 1` is a strictly weaker (broader) condition for OBBT contraction, and it comes with a matching lower bound on the rate and a stall certificate. See §4.

## 1. Source statements, summarized

### Wechsung–Schaber–Barton 2014 (= Wechsung thesis, Ch. 2)

- **Definition 2.1** (p. 31). Convergence order is defined by the gap between minima rather than by pointwise error: for β ≥ 1, there must be K > 0 with `min_{x∈X} f(x) − min_{x∈X} f̌_X(x) ≤ K w(X)^β, ∀X ∈ IC`.
- **Assumption 2.3** (p. 34): the algorithm visits exactly one box X̃ with w(X̃) = δ containing x*, and x* lies at the center of that box.
- **Theorem 2.1(a)** (journal Theorem 1; p. 36): with λ1 > 0 the least eigenvalue of ∇²f(x*) and r = sqrt(2ε/λ1), the case δ ≥ 2r, equivalently (ε/K)^{1/β} ≥ 2 sqrt(2ε/λ1), gives N = 1. Here `δ = (ε/K)^{1/β}`, and N bounds the number of width-δ boxes needed to cover B̃.
- **§2.2 and Table 2.2** (pp. 37–38): K ≤ λ1/8 suffices for no clustering (N = 1). Larger prefactors permit dimension-dependent growth: linear when K ≤ λ1/4, and quadratic when K ≤ 3λ1/8.
  - The table rows are: `K ≤ λ1/8: 1`; `λ1/8 < K ≤ λ1/4: 1+2n`; `λ1/4 < K ≤ 3λ1/8: 1+2n²`; … `K > 9λ1/4`: exponential in `n`.
- Page 31: for second-order bounds with a sufficiently small prefactor and a minimizer always interior to a box, exponential growth with dimension can be avoided. Thus second-order schemes can behave differently in high dimension.
- **Domain reduction.** §1.1.2 (p. 23) treats reduction as optional for convergence, while allowing it to save iterations. Appendix A (p. 159) gives a one-shot subgradient bound update (Theorem A.1). No iteration or rate appears anywhere in the thesis.

### Kannan–Barton 2017 (= Kannan thesis, Ch. 5)

- **Lemma 1:** the node containing `x*` can be fathomed, in the worst case, only if `w(X*) ≤ (ε/τ*)^{1/β*}`.
- **Lemma 8:** if `∇f(x*)ᵀd + ½dᵀ∇²f(x*)d ≥ γ dᵀd` on feasible `d`, then the ε-optimal feasible set near `x*` lies in `{γ‖x−x*‖² ≤ 2ε}`.
- **Theorem 3.1:** for δ = (ε/τ*)^{1/β*} and r = sqrt(2ε/γ), case 1 takes N = 1 when δ ≥ 2r. The remaining cases have the same polynomial and exponential dependence as WSB. In the unconstrained setting, the paper identifies Theorem 3 with Theorem 1 in [29], taking γ as half the least eigenvalue of ∇²f(x*).
- **Remark 9.1:** a small enough prefactor together with second-order convergence suffices to avoid clustering on X3.
- **Abstract:** the paper gives sufficient prefactor conditions for complete removal of clustering.
- Page 2: minimizers are assumed to lie in the relative interiors of the boxes. The paper cites epsilon-inflation [16] and back-boxing [21, 27] as ways to obtain this placement.

### Kannan–Barton 2018 and Kannan thesis

- Page 17 (Definition 14 context): X(Z) may be an interval subbox produced by bounds tightening. When OBBT is used, the containment requirement X(Z) ⊃ F_X(Z) need not hold.
- After Example 6 (`f = −xy`, `x + y ≤ 1`, `f^cv_Z(0.5,0.5) = −0.25 − ε²`): FBBT does not increase the convergence order in this example.
- **Thesis §2.3.2.2** (p. 63) defines OBBT as the FBBT problem plus the constraint `f^cv(x) ≤ UBD`. It gives no analysis.
- **Thesis p. 307, footnote 2:** full-space B&B can mitigate clustering without domain reduction, although reduction often accelerates convergence empirically.
- **Thesis §7.2** (p. 309): the thesis leaves open which conditions on domain reduction would let reduced-space B&B mitigate clustering.

### Du–Kearfott 1994

- **Abstract:** the analysis uses interval-arithmetic bounds and the midpoint test, without acceleration.
- **Theorem 1:** `x*` is a vertex of the grid, and the extension has order α with constant K (Hausdorff excess width). Then at most `N = (2⌊sqrt(2K/λ_{1,0}) · ε^{(α−2)/2}⌋ + 1)^m` boxes remain. The proof uses the sufficient rejection condition `K w(X)^α < ½ (nε)² λ_{1,0}` (eq. 12).
  - For α = 2 and `2K < λ_{1,0}`, this gives N = 1. The paper does not state this case explicitly. Corollary 1(2) describes a bounded cluster, potentially with a constant number N > 1 of boxes.
- **Conclusions:** the proposed extension is to add acceleration, for example interval Newton.

### Bompadre–Mitsos 2012 (via BMC 2013 §2 and Kannan thesis pp. 56–58)

- **Definition 9 (pointwise convergence):** `sup_{z∈Y} |h(z) − h^cv_Y(z)| ≤ τ w(Y)^γ`.
- **BM Theorem 2:** a nonlinear C² function has pointwise order at most 2.
- **BM Theorem 10:** envelopes have pointwise order at least 2.
- **BMC 2013, Appendix A:** an example shows that tight estimators early in B&B can help in ways not measured by either convergence order. It says nothing about domain reduction, and it has no limit of `h^cv/w²`.

### Neumaier 2004 §15 and Schichl–Markót–Neumaier 2014

- **Neumaier p. 44:** the argument gives sufficiency of o(ε²). This means the bounding error must be `o(w²)` relative to the quadratic model, which is the same order as the remainder in `theory.md` Assumption (T).
- **Backboxing:** reduction is repeated until improvement is negligible. With second-order reduction, the resulting z is generally very small or empty.
- **Schichl–Markót–Neumaier §2:** the required approximation order is at least cubic (k = 3), whereas constraint propagation has `k = 1`.
- **Schichl–Markót–Neumaier §3:** the inclusion-region iteration x_{n+1} = K(z, x_n) has quadratic convergence, so the authors expect only a few steps to be needed. This is an iterated Krawczyk contraction for an inclusion region. It is not OBBT.

## 2. What no source contains

None of these sources defines any of the following:

- a limit such as `lim w^{-2}(phi_{x*+wD(d)}(x*+wξ) − f*)`;
- the dependence of the relaxation error on the box shape `d` and the position `ξ` inside the box;
- a box-to-box map built from the relaxation's sublevel set;
- a spectral-radius or Collatz–Wielandt quantity.

The only "second-order description" in these papers is a scalar inequality: an upper bound `K w²` or `τ w²`, compared with `λ1/2` or `γ`. The worked examples compute `f^cv` at one point for one box. Kannan–Barton 2018 Example 6 finds `−0.25 − ε²` at the center, which is one value of a `Q`-like function, but the paper does not define `Q`.

## 3. Prefactor thresholds and Proposition 3

The following was derived here, not taken from a source. Write `mu` for the ∞-norm growth constant of Proposition 3. Since `‖x‖₂ ≥ ‖x‖∞`, quadratic growth `f − f* ≥ (λ1/2)‖x−x*‖₂²` gives `mu = λ1/2`. Kannan–Barton's growth condition gives `mu = γ/2`.

- **Proposition 3** contracts iff `2 sqrt(tau/mu) < 1`, that is, `tau < mu/4`. With `mu = λ1/2` this is `tau < λ1/8`.
- **WSB Theorem 1(a):** N = 1 iff `K ≤ λ1/8`.
- **Kannan–Barton 2017 Theorem 3 case 1:** `δ ≥ 2r` iff `tau* ≤ γ/8`, which is `mu/4` with `mu = γ/2`.

These are the same threshold with the same geometry. Each compares the box half-width `w/2` with the radius `w·sqrt(tau/mu)` of the set where the relaxation gap can hide the growth. The prefactors differ in kind:

- WSB's `K` bounds the gap in minimum values, `min f − min f̌`.
- Kannan–Barton's `tau*` bounds the gap of the lower-bounding problem.
- Proposition 3's `tau` bounds the pointwise gap over the whole box, which is at least as large as either of the others.

**Consequence.** Proposition 3 should be presented as the domain-reduction analogue of WSB Theorem 1(a) and Kannan–Barton 2017 Theorem 3, and cited as such. Its derivation is new but elementary.

## 4. Comparison with the contraction criterion `r*(Phi) < 1`

1. **Object.** The cluster papers bound how many boxes of width `δ = (ε/K)^{1/2}` are needed to cover the ε-suboptimal set. They assume `x*` is at the box center and that the prefactor bound is attained in the worst case. `r*(Phi)` instead describes the dynamics of one box containing `x*` under repeated tightening: its rate, the shape it approaches, and the floor `O(sqrt(ε))`.
2. **Sufficiency and comparison.** Under (T), the scalar pointwise bound `phi_B ≥ f* + mu‖x−x*‖∞² − tau w²` gives `Q(1, ξ) ≥ mu‖ξ‖∞² − 4 tau`, hence `r*(Phi) ≤ 2 sqrt(tau/mu)`. So the WSB/KB-type threshold `tau < mu/4` implies `r* < 1`, but the converse fails.
   - Example: `x² + y² + xy` with McCormick has `tau = K = 1/4`, `lambda_1 = 1` and `mu = 3/4`. It fails `K ≤ λ1/8` and `tau < mu/4`. In WSB's table it falls in the band `λ1/8 < K ≤ λ1/4`, where N ≤ 1+2n. Yet `r* = 0.7247` (Proposition 7).
   - The scalar criteria lose information in three ways: they use the smallest eigenvalue for every direction, the largest gap at every point, and a cubic box.
3. **Lower bounds.** The cluster literature proves only upper bounds on N. Du–Kearfott's Remark 1 says "there may" be clusters, and Kannan's thesis notes that its analyses are asymptotic. `theory.md` has a matching lower bound on the rate (when `Phi(u) = rho u`) and Theorem 6, which certifies that the iteration makes no progress at any scale.
   - The closest published statement is WSB's `K > 9λ1/4` regime, where N is exponential in `n`. That is a covering estimate, not a certificate.
   - Proposition 8's row condition (accumulated McCormick gap at `x*` exceeding the coordinate curvature) matches the "large prefactor relative to curvature" intuition of WSB §2.2, but nothing like it is proved there.
4. **Role of domain reduction.** In every source, domain reduction is optional for full-space branch and bound, and nobody gives it a rate. Kannan (thesis p. 309) states that sufficient conditions on domain reduction are open for reduced-space branch and bound. `theory.md` §5's planned link from `r* < 1` to width-tight reduction and cluster-freeness answers a neighbouring question, not that exact one.

## 5. Recommended edits to `theory.md`

- Proposition 3: cite WSB (2014) Theorem 1(a) and Table 2, and Kannan–Barton (2017) Theorem 3, as the same `mu/4 = λ1/8` threshold for branch and bound.
- Assumption (T): note Neumaier's (2004, p. 44) remark that `o(ε²)` accuracy is what matters.
- Novelty statement: after this check, Theorems 4 and 6, Propositions 7 and 8, and the definitions of `Q`, `Phi` and `r*` still have no counterpart in the sources read. Locatelli–Schoen §5.5, the 2008 Torino report and Bompadre–Mitsos 2012 remain unread. A negative search does not prove novelty.
