# Recourse repair, round 1

Author: recourse repair writer (Opus). Date: 2026-10-05.

Scope: apply every required local correction and wording cleanup recorded
in `evidence/reviews/recourse-r1.md` to `sections/10-recourse.tex` and
`appendices/I-recourse.tex`. No other manuscript file was edited. No
bibliography, macro, or KB change was made.

Inputs read: `BRIEF.md`, `authoring/CONVENTIONS.md`, `authoring/DECISIONS.md`,
`literature-review.md` (including its later update with the source-contract
table), `authoring/recourse.md`, the whole of `reviews/recourse-r1.md`, both
owned files in full, `lem:convex-value` in Section 2, Definition
`def:models-rational` and the Las Vegas definition in Section 1, and the
conventions and classical-subroutine paragraph of Appendix C.

## File hashes

At the start, both files matched the reviewed hashes, so the review's line
numbers applied directly. Line numbers below refer to those reviewed
versions.

| File | Reviewed (before) | After repair |
| --- | --- | --- |
| `sections/10-recourse.tex` | `0d44bbd004cd26f3044bb4bacb661bdb426138be538b97b4672fe457f31478d9` | `c14e1318e8ba797d68d69d8387f00ac183b6e8eaeffc9210e7a8042dc2ff1454` |
| `appendices/I-recourse.tex` | `a38ad7007300b3ef385d3755519de6bca02b0765e80acf569a4713cb2db58bbc` | `c62d2b729a3d946d2447e54a868360d1872ee716a4c532f01abe4e982024cc32` |

The unconditional V1–V5 and RQ1–RQ4 theorems and their promises are
unchanged. No theorem was narrowed, no conditional oracle was introduced,
and no label was renamed. References to recourse labels from Sections 00,
01, and 11 therefore remain valid.

## Required corrections

1. **Rational Γ majorants (moderate; I:1365, I:1472).**
   - Case (ii) of `lem:recourse-convexified-error`: `(n+1)^{(D-1)/2}` became
     `(n+1)^{\lceil(D-1)/2\rceil}` in the bound and in `C_res`. The proof now
     states the reason. The vector `N_{\psi_a}d` has at most
     `binom(n+D-1,D-1) <= (n+1)^{D-1}` entries, each at most `C_psi E^{1/D}`,
     so its norm is at most `(n+1)^{(D-1)/2} C_psi E^{1/D}`, which is at most
     the integer-exponent bound. The rest of the chain is unchanged.
   - Proof of `prop:recourse-fiber`(c): `M_* sqrt(m)` became `M_* m` in the
     gradient-row bound, in the bound on `||Td||`, and in `Γ`. Lemma
     `lem:recourse-transverse`(b) with `rho = sqrt(m)/2` gives
     `E + M_*(sqrt(m)/2)||Pi d|| <= E + M_* m ||Pi d||`. The result is
     `Γ = (mC_B)^{m-1} mu^{-1}(1+(M_A+M_* m)C_perp)`, which is rational
     because `C_perp` already was.

2. **Tolerance encoding (moderate; I:42).** The interface cost
   `P_D(L_Q+log(2+1/eta))` became `P_D(L_Q+<eta>)`, matching
   `lem:convex-value`. The conventions now define `<r>` as the bit length of
   Definition `def:models-rational`. Each call's accounting was updated:
   - cell oracle: `e_h = kappa_+ k 2^{-2j-3} > 0` with `<e_h> <= 2j+P_D(L)`;
   - Corollary `cor:recourse-joint`: `<delta> <= 2q+P_D(L)`;
   - Theorem `thm:recourse-convexified`: `<eta_q> <= (2D_e+2)q+P_D(L)`, with
     solve data of bit length `P_D(L+q)`;
   - cubic completion: `<eta_q> <= 8q+poly(L)`.

   No cost bound changes.

3. **Exact convex QP on a thin fiber (moderate; I:1019–1022).** The proof of
   `cor:recourse-qp` now reduces `X_a` to its affine hull before calling
   Kozlov–Tarasov–Khachiyan. It gives the example `-z^2` on `{0}`. It then
   applies `lem:recourse-relative` to `X_a`, which yields `z_0`, a matrix `B'`
   of full column rank `m'`, and a polytope `R'` that contains a ball about
   the origin. If `m'=0`, it puts `z^*=z_0`. Otherwise the reduced quadratic
   is convex on a set with nonempty interior, so its constant Hessian
   `B'^T A_zz B'` is positive semidefinite. Exact convex QP then returns a
   rational `w^*`, and `z^* = z_0+B'w^*`. Since `a` is an optimal core,
   `min_{X_a} f_gamma(a,.) = f_gamma^*`. The cost statement now includes the
   linear programs of `lem:recourse-relative`. The tools paragraph now states
   KTK's positive-semidefinite Hessian hypothesis explicitly.

4. **Lattice input in the unit box (low; sec10:457–458).** The statement of
   `lem:recourse-lattice` now requires `hat a in [0,1]^r`. Its proof says that
   both `a` and `hat a` lie in `[0,1]^r` before it applies the 2-Lipschitz
   bound. The acceptance-soundness paragraph records that clipping gives
   `hat a in [0,1]^r` and does not increase any coordinate error, because the
   box contains `a_F`. The algorithm already clipped, so it is unchanged.

5. **Zero restricted Hessian (low; I:1458–1461).** The proof of
   `prop:recourse-fiber`(c) now proves `||Pi d|| <= C_perp E^{1/4}` first, in
   two branches. If `H_A=0`, then `K_A=R^m` and `Pi=0`. If `H_A != 0`, the
   proof uses `lambda_0^A` and the displayed intermediate inequality
   `d^T H(v,c_z) d >= 2 delta d^T H_A d`. It also records `H_A d = H_A Pi d`.

6. **Optimal-slice necessity (low; I:1329–1330).** The proof now defines
   `R_a = {w in R : x_0+Bw in S_a}`, the optimal set, and proves
   `R_a = {w in R : J(w-u)=0}`. The forward direction reads "if `w` is
   optimal, then `E=0` and the bounds give `Jd'=0`". The converse now ends
   with "so `E=0` and `w` is optimal". The Hoffman step then uses
   `S_a = x_0 + B R_a`, which follows from the definition.

7. **Open outer ball (low; I:1219–1220, I:1236).** `R_0 = 1+sum_j m_j`, and
   `||w|| <= ||w||_1 <= sum_j m_j < R_0`. The proof also notes that the closed
   inner ball, and hence the open one, of radius `r` lies in `R`. The
   downstream uses (`w' = -(r/R_0)w in B(0,r)`, `beta_0 = 1+R_0/r`, and
   `rho = R_0`) remain valid.

8. **Symmetric quadratic matrix (low; I:964).** `lem:recourse-qp-height` now
   assumes `A=A^T`, so that `grad q = Ax+c`. The corollary's proof writes
   `f_gamma = (1/2)x^T A x + c^T x + c_0`, where `A` is the constant
   symmetric Hessian of `f` and only `c` depends on `gamma`.

9. **Sampled bit length (low; I:28).** The bound is now `b <= L+2log_2 M`,
   with a proof. A grid point is `sigma(2j-M+1)/(M-1)`, so its numerator and
   denominator are those of `sigma` times integers of absolute value less
   than `M`. Under `def:models-rational`, with `M` a power of two, its bit
   length is at most `<sigma> + 2log_2 M`. This implies the review's
   `L+2log_2 M+O(1)`.

10. **Las Vegas qualifier (low; sec10:29–30).** The text now reads "Las Vegas
    algorithms with expected polynomial running time". The proof of
    `rem:recourse-quartic` received the same qualifier. It also notes that a
    draw uses `log_2 M` fair coins, because `M` is a power of two.

11. **Product-box qualifier (low; sec10:25–26).** The text now reads "On
    product boxes, values and one selected core are available under residual
    convexity alone; on coupled polytopes they need a supplied convexifier."
    The full-point sentence now matches `thm:recourse-convexified`(i)/(ii): a
    supplied convexifier, together with a cubic objective or a convexified
    objective that is convex on all of `R^n`. The summary in
    `sec:recourse-scope` repeated the unqualified claim, so it received the
    same qualification.

## Wording cleanup from the review

- sec10:343–347: `prop:recourse-fiber`(c) now begins "Let
  `delta in (0,1/2]` and `mu in (0,1]` be supplied rational margins". It
  states that `Γ` is computed from `f`, `A`, `delta`, and `mu` in time
  polynomial in `L` and the bit lengths of `delta` and `mu`. The appendix
  proof now ends with `L+<delta>+<mu>`. In I.16, the acceptance paragraph now
  bounds `<delta>+<mu> = O(log s+log B+log T+log Delta) = poly(L)`, where it
  previously said "`log Γ` polynomial in `L+log T`".
- I:841: the text now says that `x_q` is a witness that the cell oracle
  produced at a level at most `J`, possibly an earlier one, and that `ell_q`
  is computed from its value.
- I:721: `lem:recourse-growth`(a) now asserts the growth inequality for every
  finite `t in (0,g(gamma)]`. The proof derives it: the witness has value
  `f_gamma^*`, its core is `a(gamma)`, and `gamma in G_t` for every finite
  `t <= g`. The callers use only `t = g_0`.
- I:1338–1339: `B_F = max{1, sum_{i,j}|B_ij|}`.

## Additional consistency fixes outside the review's list

These fixes address the same defect classes as the review items.

- `lem:recourse-fallback`, last part: the lemma declares
  `G >= max{1, sup||grad f_gamma||}` rational, but the construction used
  `+sigma sqrt(k)` and omitted the maximum with 1. Now
  `G = max{1, G_f + k sigma}` with `k sigma >= ||gamma||`. The irrational
  accuracy `2^{-q}/(2 sqrt(n) G)` became precision `q+1+ceil(log_2(nG))`.
  The bound `||x~ - x#|| <= sqrt(n) 2^{-q-1}/(nG) <= 2^{-q}/(2G)` is now
  written out.
- Rejection branch in I.16: the accuracy `2^{-q}/sqrt(n)` became precision
  `q+ceil(log_2 n)`. The resulting `infinity`-accuracy is at most
  `2^{-q}/n`, so the Euclidean accuracy is at most `2^{-q}`.
- Tools paragraph: the rational-LP citation now uses the vetted pinpoint
  already used in Appendix C, GLS Theorem (6.4.12) and Section 6.5.
- Paragraph after `thm:recourse-qe`: it now states which statement each part
  uses. Part (a) uses the real-number-model statement of Renegar's
  Theorem 1.1, with noise values and thresholds as real coefficients. Part
  (b) uses the separate integer bit-model statement, applied after
  denominators are cleared. This matches the vetted contract row in the
  updated `literature-review.md`.

## Deliberately unchanged

- Theorem statements, probability bounds, expected-work bounds, parameter
  orders, and labels.
- `rem:recourse-low-dim` reads `kappa_+/g` as 0 when `g=+infinity`, the
  natural convention. It is a remark that no theorem uses.
- Accuracy targets used only to choose an integer precision from a
  base-computable rational, such as `2^{-q-1}/G` in
  `rem:recourse-value-certificate`.

## Source gates still open

No proof depends on an unproved internal step. The following are open
bibliography and pinpoint items for root and Luna.

1. Eight cited keys are missing from `references.bib`:
   `AndroulakisMaranasFloudas1995`, `BasuPollackRoy2006`, `EvansGariepy2015`,
   `Hoffman1952`, `Renegar1992QE`, `Rockafellar1970`, `Schrijver1986`, and
   `SpielmanTeng2004`. Root will insert the Luna-vetted records. No other
   chapter cites these sources under a different key. Three keys are also
   cited outside these two files: `BasuPollackRoy2006` (Appendices E and J),
   `Hoffman1952` (Section 2 and Appendix J), and `Rockafellar1970`
   (Appendix J). The other five are cited only in the recourse chapter.
2. Renegar 1992, Part III, Theorem 1.1. Root reports that Luna cleared this
   theorem (printed pp. 330–331). The updated literature review records its
   separate real-model and integer-model statements, and the manuscript now
   states this split. Root may add the page pinpoint at bibliography
   integration.
3. Basu–Pollack–Roy 2006 pinpoints are absent from the vetted report:
   Chapter 14 for the secondary block-QE cross-reference, and Chapters 8 and
   10 for `thm:recourse-univariate` (squarefree part, real-root isolation,
   sign determination, and refinement). Luna should verify or correct them.
4. Pinpoints for classical facts still need verification: Rockafellar 1970,
   Theorems 23.4, 23.5, 25.1, and 25.5; Evans–Gariepy 2015, Section 2.4; and
   Schrijver 1986 on continued fractions and Legendre's theorem.
5. The `KannanRademacher2009` sentence awaits Luna's confirmation. It
   describes optimizing a convex objective plus a low-dimensional polynomial
   perturbation to a prescribed objective accuracy. This is consistent with
   the vetted report's description of an approximation result.
6. The recourse row of `literature-review.md` names `thm:recourse-completion`,
   but the manuscript label is `prop:recourse-completion`. Luna owns that
   file.
7. The shared GLS contract for `lem:convex-value` belongs to the points
   writer. The updated literature review now lists the WOPT/WSEP and
   Corollary 4.2.7 contracts.

## Verification actually performed

- Read-only inspection with `sed`, `grep`, `cat`, and `sha256sum`.
- A scratch compile of only the two owned files in `/tmp/recourse-r1-scratch`,
  outside the repository, using the manuscript preamble and `macros.tex`,
  with `pdflatex` run twice. It exited 0 with no LaTeX errors and no overfull
  or underfull boxes, and produced 30 pages. Undefined references were only
  shared labels owned by other files, all of which exist in the manuscript.
  Citations were undefined because the scratch build has no bibliography.
- An inline Python check of the two files against the labels of all
  manuscript files. All 70 distinct references resolve, and the two files
  define no duplicate labels. Of 12 citation keys, 8 are missing from
  `references.bib` (listed above). The files contain no unfinished-text
  markers and none of the reviewed irrational constant forms.
- Visual inspection of two rendered scratch pages: the proof of
  `cor:recourse-qp` and the proof of `prop:recourse-fiber`.

I ran no experiments, historical scripts, full-manuscript or project-wide
checks, or CI inspection. I did no literature research, made no KB or
bibliography edits, and made no commits. These document checks are distinct
from the analytic reconstruction of the changed steps recorded above.
