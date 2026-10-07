# Manuscript architecture

Status: initial architecture by the main writer, 2026-10-05. Binding for
notation, section ownership, and public labels. Request changes through
root; do not edit another writer's files.

## 1. Thesis and theorem spine

Working title: *Quantitative sparse sum-of-squares hierarchies and large
private convex recourse*.

One sentence: in a sparse moment-SOS hierarchy, local positivity can be made
as strong as one likes, yet the finite polynomial information exchanged
across separators limits the rate; we quantify that limit for box problems
(ordinary module and preordering) and for bags carrying large private convex
quadratic blocks, where the rate is `r^-2` for fixed private domains,
drops to `r^-1` in general for affine recourse, and returns to `r^-2` when
the projected recourse multipliers are regular.

Unifying mechanism (used in the introduction and repeated in each section's
first paragraph): a common normalized polynomial kernel turns every feasible
family of local truncated functionals into nonnegative local densities whose
separator marginals agree **exactly**, because the kernel preserves mass and
separator moments agree through degree `2r`. Junction-tree gluing then gives
a global law. Every upper bound is a quantitative rounding statement for
**every feasible moment point**. Every lower bound uses **actual local
measures** whose separator moments agree, so it limits any strengthening of
local positivity while separator exchange stays polynomial of degree `2r`.

Spine (public labels in brackets):

1. Full box preordering, `O(r^-2)` with explicit constant
   `3A/(2m^2+1)`, `m=floor(r/w)+1` [`thm:pre`]; grid extraction
   [`cor:pre-grid`]; real sparse certificate by Slater [`cor:pre-certificate`].
   **Rate not new**: asserted in Magron's slides (7 Jul 2025, 16 Feb 2026);
   published Korda–Magron–Ríos-Zertuche Theorem 6 gives `r^(-2/(w+3))`.
   Our contribution there: self-contained primal proof by compatible
   densities, explicit constants, rounding. Serves as the template.
2. Ordinary sparse box quadratic module, finite-order bound and
   `f*-rho^mod_r <= C_f O_{w,d}(log^3 r / r^2)` with constants independent of
   number of bags and tree shape [`thm:mod`, `cor:mod-rate`]; certificate
   [`cor:mod-certificate`]. Dense rate and SOS kernel: Gribling–de Klerk–Vera
   (arXiv 2605.31496). Candidate addition: sparse transfer by exactly
   normalized signed densities plus one common correction; no polynomial
   separator dual attainment assumed (contrast Gamertsfelder–Mourrain).
   This is the paper's lead box result; priority still qualified.
3. Sharpness and exact small orders [`thm:quad-sharp`, `prop:moment-matching`,
   `prop:exact-orders`]: fixed quadratic two-bag example, `Theta(r^-2)` for
   the sparse preordering, gap persists for actual local measures, dense
   order-two exact; `rho_1=-1/4` and `rho_2=8/3-14 sqrt3/9` for both cones.
4. Private convex recourse, fixed private polytope: `O(r^-2)` for the
   private-degree-two hierarchy [`thm:fixed-recourse`]; private quadratic
   bounds necessary [`prop:private-bounds-needed`]; convexity necessary
   [`prop:convexity-needed`].
5. Affine recourse with fixed matrix and complete recourse: `O(1/r)` by
   Hoffman repair [`thm:affine-recourse`]; sharp `Theta(1/r)` example
   [`thm:affine-sharp`], stated **separately** for the private-degree-two
   hierarchy and for the total-degree two-bag preordering.
6. Regular projected multipliers: `O(r^-2)` under weighted tensor-Chebyshev
   regularity [`thm:reg-cheb`], `O(r^-(1+beta))` under coordinatewise Hölder
   regularity [`thm:reg-holder`]; half-degree frequency lemma
   [`lem:half-degree`] is essential; sharp regular example [`ex:reg-sharp`];
   strict convexity insufficient [`ex:strict-convex-insufficient`].
   Not a theorem for arbitrary multivariate Lipschitz multipliers.
7. Extensions: polynomial constraints with a global Hölder error bound
   [`thm:constr-pre`: `O(r^-alpha)`; `thm:constr-mod`:
   `O((log r / r)^alpha)`]; convex Slater regime [`prop:convex-slater`];
   global versus local geometry [`ex:global-local`]; finite-state variables
   [`thm:finite-state`]. Primal statements only.
8. Exact rational certificates with slack [`thm:rational`,
   `cor:rational-mod`]: specialization of strict-feasibility rational SOS
   methods (Peyrl–Parrilo; Davis–Papp); polynomial in expanded SDP size.

Integration decisions after independent reviews (root, 2026-10-05):
- `prop:rec-dual` ACCEPTED (AUDIT-RECOURSE §7; reviews/recourse-duality-sol-r1.md).
  Recourse writer integrates with full proof in Section 6: order unit,
  sparse quotient, compact attained primal, dual supremum equals
  `rho^rec_r`, every `lambda < rho^rec_r` is certified. No boundary
  attainment, no closedness claim, real coefficients only.
- `thm:finite-state-mod` ACCEPTED (AUDIT-EXTENSIONS §6;
  reviews/developments-sol-r1.md). Extensions writer integrates with
  label-mass-scaled correction `Delta_w tau_{b,a}`, zero-mass labels
  (functional vanishes identically), empty continuous bags, all-discrete
  case exact at order zero, mass-weighted bound and data-only bound
  `C_mix(Gamma_w + 2 Delta_w)`.
- Constrained ordinary theorem via exact-density domination ACCEPTED
  (AUDIT-EXTENSIONS §4). Extensions writer may present `thm:constr-mod`
  through the common correction, which removes the separate tree
  disagreement term; the constants still scale with the summed generator
  budgets, `H`, and `L_f`.
- Rational: polynomial-bit witness existence and exact rounding/correction
  are proved. The polynomial-time *construction* sentence is conditional on
  Luna locating an exact rational strong-feasibility (ellipsoid) theorem;
  otherwise drop it. The ordinary-module rational statement is already in
  the source and is not new. Use the rational majorant `eta_rat` (replace
  `sqrt(2(D+1)) delta` by `2(D+1) delta`) for the ordinary promise.

Excluded: curvature convex covers, algebra/control/submodular topics,
approximate-consistency tree repair as a headline (may appear as a remark in
Section 4), numerical experiments (at most one sentence in Section 5 /
Discussion marking higher-order equality as a conjecture).

## 2. Section ownership

| File | Owner | Content |
|---|---|---|
| `main.tex`, `macros.tex` | main writer | skeleton, shared notation |
| `sections/00-abstract.tex` | main writer | abstract |
| `sections/01-introduction.tex` | main writer | motivation, contributions, prior work summary, organization |
| `sections/02-setting.tex` | main writer | notation, cones, hierarchies, standard lemmas |
| `sections/03-kernels.tex` | kernel writer | Jackson kernel; `thm:pre` and corollaries |
| `sections/04-ordinary.tex` | kernel writer | SOS kernel; `thm:mod` and corollaries |
| `sections/05-sharpness.tex` | kernel writer | quadratic example, exact orders |
| `sections/06-recourse.tex` | recourse writer | fixed-domain and affine recourse, boundary example |
| `sections/07-regularity.tex` | recourse writer | regular multipliers |
| `sections/08-extensions.tex` | extensions writer | constraints, finite-state |
| `sections/09-certificates.tex` | extensions writer | rational certificates |
| `sections/10-discussion.tex` | main writer | limits, comparisons, open problems |
| `appendices/A-kernels.tex` | kernel writer | optional long proofs |
| `appendices/B-recourse.tex` | recourse writer | optional long proofs |
| `appendices/C-extensions.tex` | extensions writer | optional long proofs |
| `literature.bib`, `evidence/LITERATURE.md` | Luna | bibliography |
| `evidence/ARCHITECTURE.md`, `evidence/COVERAGE.md` | main writer | this plan |

`main.tex` loads each file with `\InputIfFileExists`; a missing file only
prints `MISSING FILE`. Section files start with `\section{...}\label{sec:...}`
using the labels below. Appendix files start with `\section{...}` (they are
loaded after `\appendix`).

## 3. Binding notation

Use the macros in `macros.tex`. Do not redefine them. Section-local symbols
are fine if they do not collide with this table.

| Symbol | Meaning |
|---|---|
| `x in [-1,1]^n` | shared (smoothed) coordinates in every model |
| `B_1..B_t`, `Tree`, `E(Tree)` | bags, junction tree, its edges |
| `v_b=|B_b|`, `w=max_b v_b` | bag size, width (also for shared bags in recourse; the source notes' `S_b,k_b,s` become `B_b,v_b,w`) |
| `S_e = B_b ∩ B_c` | separator of edge `e=bc` (letter `S` reserved for separators) |
| `f=sum_b f_b(x_{B_b})`, `f*` | decomposed objective, true minimum |
| `r` | relaxation (moment) order; certificate/moment total degree `<= 2r`. Use `r` everywhere, including the ordinary-module section (source notes use `R`). |
| `d` | max total degree of the local data; `d_inf` max coordinate degree |
| `T_k, U_k, T_alpha` | Chebyshev polynomials, tensor products |
| `\arcs` (`mu`) | normalized arcsine probability measure; `mu^{B}` product |
| `\chebnorm{p}` | sum of absolute tensor Chebyshev coefficients |
| `C_b, \Cf=C_f` | nonconstant local Chebyshev norm, its sum over bags |
| `\Abud(p)`, `\Abud` | `sum_alpha |c_alpha| sum_i alpha_i^2`; `\Abud` alone = sum over bags (matrix version in recourse with entrywise norms) |
| `\Mod_r(B)`, `\Pre_r(B)` | truncated ordinary box module, full box preordering on bag `B` (Def. `def:cones`) |
| `\rhomod_r, \rhopre_r, \rhorec_r` | moment values of the three sparse hierarchies |
| `\lammod_r, \lampre_r` | certificate (dual) values |
| `L_b` | local truncated linear functional; never called a measure |
| `nu`, `nu_b` | rounded global / local probability laws |
| `\Kj(x,u)`, `\kmult_k`, `\Dm=2m^2+1` | Jackson-type kernel, multipliers (`1-gamma_k<=3k^2/D_m`), constant |
| `u` | kernel output point (source notes use `y` or `v`) ; densities `h_b(u)` |
| `xi_j` | Chebyshev grid nodes |
| `Phi_s, p_{s,N}, Psi, omega, varrho, delta, Delta_w, Gamma_v, eta` | SOS-kernel objects in Section 4: Fejér source kernel, geometric multiplier, squared kernel `p_{s,N}(x)Phi_s(x,u)^2`, mass polynomial, residual `1-omega`, `2^{-(N+1)}`, common correction, tensor error, univariate error. (Source names `S_s, Q, n, r` collide.) |
| `y_b in R^{p_b}` | private vector of bag `b`; `\zy=(1,y^T)^T` |
| `P_b` or `P_b(x)` | private polytope / fiber `{y in [-1,1]^{p_b}: A_b y <= a_b + E_b x_{B_b}}` (matrix `E_b`, not `B_b`, which is the bag; source `B_b` becomes `E_b`) |
| `c_b, q_b, Q_b(x)` | private objective `c_b+q_b^T y + y^T Q_b y`; `H_b(x)` its augmented matrix |
| `pi_b(x)` | KKT multipliers (source `lambda`); projected multiplier `a_b^{dual}=D_b^T pi_b`, with `D_b=[E_b;0;0]` the stacked shared matrix |
| `kappa_b` | Hoffman constant (source `h_b^H`) |
| `g_{bj}` | polynomial constraints (Section 8) |
| `lambda` | certificate value / rational target (source `gamma`) |

Degree conventions: scalar hierarchies use total degree `<= 2r` for every
certificate summand and moment. The recourse hierarchy uses shared total
degree `<= 2r` and private degree `<= 2`. Never compare the two by
inclusion without checking each generator and degree.

Terminology (fixed):
- "ordinary (box) quadratic module" vs "full (box) preordering".
- "private-degree-two hierarchy" (synonym in proofs: rectangular hierarchy)
  vs "total-degree hierarchy".
- "moment value" `rho` vs "certificate value" `lambda`; "primal rounding"
  vs "dual certificate attainment".
- "exact separator consistency" (functionals agree on separator moments
  through degree `2r`) vs "consistent measures".
- "fixed width" constants `O_{w,d}` vs "normalized by `C_f`".

## 4. Section 2 interface (written by main writer)

Section 2 provides, with these labels, so other sections must not reprove
them:
- `def:junction-tree`: bags, running intersection, separators.
- `lem:zero-decomposition`: a sum of bag polynomials equal to zero is a
  signed sum of separator polynomials (degree preserved).
- `lem:weak-duality`, `eq:weak-duality`.
- `sec:chebyshev`: Chebyshev notation, `\chebnorm`, `\Abud`, submultiplicativity
  `lem:cheb-product`.
- `def:cones`: `\Mod_r(B)`, `\Pre_r(B)`.
- `def:sparse-hierarchy`: `\rhomod_r`, `\rhopre_r`, `\lammod_r`, `\lampre_r`,
  weak duality `eq:weak-duality`.
- `def:rec-model`, `def:rec-hierarchy`: recourse model and the
  private-degree-two hierarchy with degree allowances; block-size count
  `eq:rec-size`. Conditions are labelled (R0)--(R4); (R2) uses degree
  allowance `r-|I|-eps_bj`, `eps_bj=1` iff row j of `E_b` is nonzero. This
  is at least as strong as both source hierarchies, so all upper bounds
  transfer; actual-measure lower bounds hold for it. Fixed-domain proof uses
  `m=floor(r/w)+1`, affine/regularity proofs `m=floor((r-1)/w)+1`.
- `lem:interval-sos`: univariate interval positivity with degree bounds.
- `lem:moment-cs`: positive semidefinite forms and Cauchy–Schwarz.
- `lem:cheb-moment`: `|L(T_alpha)| <= L(1)` for `|alpha| <= r` under `\Mod_r`
  (hence `\Pre_r`).
- `lem:gluing`: junction-tree gluing of laws with consistent separator
  marginals, including null separator events.
- `lem:compact`: every local moment of a feasible ordinary-module (hence
  preordering) family is bounded by one in absolute value; the feasible
  set is compact and the moment value is attained (AUDIT-KERNELS argument).
- `lem:slater`: product arcsine moments are strictly feasible for the
  box-only hierarchies; with the finite SDP Slater theorem this gives zero
  gap, dual attainment, and the sparse certificate form
  (`eq:sparse-certificate`). Sections 3–4 cite it instead of reproving.

Section 5 must also state that the same actual-measure witnesses give an
`Omega(r^-2)` lower bound for the ordinary module (upper bound there has
logarithms; no log-sharpness claim).

Section writers keep their own kernel lemmas (Jackson kernel properties in
Section 3, SOS-kernel properties in Section 4, half-degree Chebyshev bound
in Section 7, displacement certificates in Section 8).

## 5. Section plans for technical writers

### Kernel writer: Sections 3–5 (+ Appendix A)

**Section 3** `sec:kernels` — "Exactly consistent rounding for the full
preordering". Source: `solver/sparse-kernel-rounding.md`; audit
`evidence/AUDIT-*kernel*`.
- `lem:jackson`: explicit kernel `K_m`, nonnegativity via cosine formula,
  normalization, multipliers `gamma_k in [0,1]`, `1-gamma_k <= 3k^2/D_m`,
  rational coefficients. Cite classical Jackson/squared Fejér; do not claim new.
- `lem:pre-density`: preordering positivity of `h_b`; exact separator
  marginal formula; degree ledger `2 v_b (m-1) <= 2r`.
- `thm:pre`: rounding bound `3A/(2m^2+1)`; corollary gap `<= 3w^2A/(2r^2)`.
  Add the compactness/primal-attainment detail from the audit.
- `cor:pre-grid`: Chebyshev grid `N=m+floor(d_inf/2)`, tree DP; state that
  grid+DP is established (Piazzon–Vianello) and that the corollary
  compares the grid with every SDP point.
- `cor:pre-certificate`: Slater via product arcsine moments; real certificate.
- Attribution remark `rem:pre-prior` (must be explicit): Magron slides,
  KMR Theorem 6, Laurent–Slot dense, de Klerk–Hess–Laurent kernel,
  Catala et al. Remark 3.7, Lasserre 2006 gluing.

**Section 4** `sec:ordinary` — "The ordinary sparse quadratic module".
Sources: `sparse-putinar-kernel.md` (kernel and coefficient estimates),
`sparse-putinar-exact-consistency.md` (main theorem),
`signed-kernel-final-audit.md` (parameter choice, normalization obstruction).
- `lem:sos-kernel`: `Phi_s`, `p_{s,N}` (even `N`, SOS identity), `Psi`,
  mass `omega=1-z^{N+1}`, residual bounds, univariate approximation estimate
  `eta`; attribute construction to Gribling–de Klerk–Vera, note degree and
  evenness repairs.
- `lem:residual-products`: weighted Cauchy–Schwarz bound
  `|L(G H)| <= delta^j L(G)`, ordinary-module degree ledger.
- `thm:mod`: finite-order bound `sum_b C_b Gamma_{v_b} + Delta_w W`.
- `cor:mod-rate`: explicit parameters, `C_f O_{w,d_inf}(log^3 r/r^2)`,
  constants independent of `t` and tree; SDP size still grows with `t`.
- `cor:mod-certificate`.
- `rem:normalization-obstruction` (cannot be both SOS and exactly
  normalized), `rem:calibration` (conservative constants, optional table
  from the audit), optional `rem:approx-consistency` (older TV-repair
  variant with tree term).

**Section 5** `sec:sharpness` — "Separator information is the
obstruction". Sources: `quadratic-sharpness.md`,
`quadratic-exact-gap-frontier.md`.
- `prop:moment-matching`: `v_n = -2E_n(h)` (credit Han–Jiao–Weissman Lemma 25).
- `lem:fejer-lower`: `E_n(h) >= 1/(27 pi (n+2)^2)`.
- `thm:quad-sharp`: `Theta(r^-2)` for the sparse preordering and also for
  actual-local-measure relaxations; dense order two exact.
- `prop:exact-orders`: order one and two exact values for both cones, Gram
  certificates and witnesses; order-one truncated witness is not a measure.
- Comparison remark: Nie–Qu–Tang–Zhang Ex. 6.7 (qualitative), Baldi–Slot
  dense lower bound (different obstruction). Higher-order equality only as
  a conjecture.
- Section 5 also exports `lem:moment-matching-general` (the identity for an
  arbitrary continuous separator function) for reuse by Section 6.

### Recourse writer: Sections 6–7 (+ Appendix B)

**Section 6** `sec:recourse` — "Large private convex quadratic blocks".
Sources: `partial-kernel-rounding.md`, `affine-recourse-kernel-upper.md`,
`affine-recourse-rate-boundary.md`, `affine-recourse-upper-prior.md`
(sharpness transfer to the rectangular hierarchy, grid/QP baseline).
Use `def:rec-model`, `def:rec-hierarchy` from Section 2 (do not redefine).
- `lem:mixed-moment`: `|L_b(T_alpha z_i z_j)| <= 1`.
- `lem:conditional-matrix`: PSD conditional matrices, feasibility of
  conditional means, zero-density handling.
- `thm:fixed-recourse`, `prop:private-bounds-needed` (Motzkin example,
  unbounded at every order), `prop:convexity-needed`.
- `thm:affine-recourse` with Hoffman constants; displacement `V_m`.
- `thm:affine-sharp`: (a) private-degree-two hierarchy lower bound
  `1/(9 pi (r+1))` from actual measures; (b) total-degree sparse preordering
  with the generator lists, upper certificate `2 sqrt 6 / sqrt(2r^2+1)`.
  Keep (a) and (b) as separate statements; no cone inclusion.
- `rem:merge-split`: merged bags or a split at `x=0` give exact low-order
  certificates (instance property only).
- `rem:grid-baseline`: grid/QP DP achieves the same exponents without SDP;
  our theorems concern every feasible SDP point.
- Optional `prop:rec-dual` if reviewed.

**Section 7** `sec:regularity` — "Regular multipliers restore the
inverse-square rate". Source: `active-region-rates.md`,
`active-region-prior.md`.
- KKT inequality and commutator identity.
- `lem:half-degree`: `|L(T_alpha)| <= 1` when `sum_i ceil(alpha_i/2) <= r`
  under the shared preordering. State why `|alpha|<=r` is insufficient.
- `thm:reg-cheb`, `thm:reg-holder`.
- `ex:reg-sharp` (`Theta(r^-2)`), `ex:strict-convex-insufficient`.
- `rem:mpqp`: Tøndel–Johansen–Bemporad, Baotić give sufficient conditions;
  prior; boundary convention. Explicitly: arbitrary multivariate Lipschitz
  projected multipliers are not covered.

### Extensions writer: Sections 8–9 (+ Appendix C)

**Section 8** `sec:extensions` — "Polynomial constraints and finite-state
variables". Sources: `general-constraints-kernel.md`,
`general-constraints-prior.md`, `mixed-discrete-extension.md`.
- `thm:constr-pre`, `thm:constr-mod` (state that the objective term keeps
  `log^3 r/r^2` while squared violation is `log^2 r/r^2`; overall
  `O((log r/r)^alpha)`); primal only, no dual attainment claim.
- `prop:convex-slater`, `ex:global-local`; prior: Tran–Toh (dense
  preordering `O(r^-alpha)`), Heijmans-Kuryatnikova–Vera–Zuluaga lift plus
  GdKV composition (`log^{3/2}`), KMR Theorem 8 local geometry.
- `thm:finite-state` (preordering). Pending `thm:finite-state-mod`.

**Section 9** `sec:certificates` — "Exact rational certificates". Source:
`rational-sparse-certificates.md`. `thm:rational`, `cor:rational-mod`;
prior Peyrl–Parrilo, Davis–Papp, Magron–Safey El Din, Grötschel–Lovász–
Schrijver.

## 6. Cross-reference rules

- Public labels listed above must be defined exactly once by the owner.
  The introduction and discussion cite them.
- Private labels carry a section tag: `ker-`, `mod-`, `shp-`, `rec-`,
  `reg-`, `ext-`, `cert-`, `set-` (e.g. `eq:rec-hoffman`, `lem:ext-displacement`).
- Use `\cref`. Use `\eqref` only inside sentences that already name the object.
- Citations: use keys from `literature.bib` (Luna). Until it exists, use the
  provisional keys in Section 8 below; root/Luna will reconcile. Do not
  add bibliography entries yourself.

## 7. Style rules (all writers)

- Plain, direct prose for optimization experts. Lead each section with what
  is proved and why it matters, then the proof.
- Full proofs. Standard results (interval positivity, regular conditional
  laws, Hahn–Banach/Riesz, finite SDP duality, Hoffman bound, ellipsoid
  method) are cited, not reproved.
- Each theorem states the cone, degree convention, and whether the claim is
  about every feasible moment point, the moment value, or certificates.
- Attribution in the text next to each borrowed ingredient; novelty language
  only "to our knowledge" plus the specific distinction. Never "first".
- No runtime, practical speedup, or MINLP complexity claims. Grid/DP
  baselines must be acknowledged where an exponent could be misread as an
  algorithmic advance.
- No internal process words in sources (no "audit", "reviewer", "note",
  "repository", agent names, dates of research).

## 8. Provisional citation keys (replace with Luna's keys)

`magron2025slides-lorentz`, `magron2026slides-tenors`,
`korda2025-convergence-rates-sparsity`, `laurent2023-effective-schmudgen`,
`dklerk2017-improved-upper-bounds`, `gribling2026-squared-kernels`,
`gribling2026-revisiting-hypercube`, `baldi2024-putinar-hypercube`,
`gamertsfelder2025-countable-gmp`, `lasserre2006-convergent-sdprelaxations-in-polynomial-optimization`,
`catala2024-singular-measures`, `magron2026-convergence-rates-for-polynomial-optimization`,
`tran2026-truncated-moment-rates`, `nie2026-sparse-tightness`,
`grimm2007-structured-sparsity`, `waki2006-sparse-sdp`,
`han2018-local-moment-matching`, `piazzon2018-chebyshev-grids`,
`bienstock2018-lp-formulations-for-polynomial-optimization`,
`lasserre2009-convexity-sdp`, `guo2025-robust-pmi-sos-convex`,
`fang2021-sos-sphere`, `miller2025-sparse-matrix`, `lasserre2010-joint-marginal`,
`zhong2024-two-stage-polynomial`, `zhang2025-wasserstein-moment`,
`hoffman1952-approximate-solutions`, `pena2018-hoffman-constants`,
`tondel2003-mpqp`, `baotic2016-value-gradient`,
`heijmans2026-degree-bounds-general`, `tran2026-psd-rates`,
`baldi2023-effective-putinar-moment`, `henrion2026-univariate-rate`,
`peyrl2008-rational-sos`, `davis2024-rational-dual-certificates`,
`magron2021-on-exact-reznick-hilbert-artin`, `grotschel1988-geometric-algorithms`,
`lasserre2001-global-optimization`, `putinar1993-positive-polynomials`,
`schmudgen1991-k-moment`, `bental2001-lectures-modern-convex` (conic duality),
`kallenberg2002-foundations` (regular conditional laws),
`kahl2005-globally-optimal-estimates`, `powers2000-univariate-interval` (Markov–Lukács
degree form), `vorobev1962-consistent-families`, `lauritzen1996-graphical-models`.

## 9. Known unresolved dependencies

- Literature: all keys above; exact theorem numbers for Lau–Womersley,
  published Tran–Toh numbering, a precise source for the degree-bounded
  Markov–Lukács interval theorem, Lasserre 2006 gluing lemma number.
- Mathematics: compactness/primal attainment detail (kernel audit);
  `prop:rec-dual`, `thm:finite-state-mod`, density-domination constrained
  variant (pending fresh review).
- Publication priority of every candidate addition remains unestablished;
  introduction wording is deliberately qualified.

## 10. Addenda (main writer)

- Section 2 states `w>=1`, `r>=1` only for Sections 2–7 and the box parts
  of Sections 8–9, and defers to Section 8 for bags without continuous
  coordinates and all-discrete models. **Extensions writer:** state those
  conventions explicitly in Section 8 (empty kernel product equals one,
  label masses only, order zero exact when `w=0`, no `r/w` expressions).
- Section 2 now also provides `lem:zero-decomposition` and
  `lem:weak-duality`; the private-degree-two hierarchy conditions are
  (R0)–(R4), with `E_b` the shared matrix in the fiber.
- Final packaging (root): replace `\inputpart` by hard `\input` and list
  only appendices that exist.
- Citation keys used in the main writer's sections (00, 01, 02, 10), for
  Luna's reconciliation: baotic2016-value-gradient,
  bental2001-lectures-modern-convex, bienstock2018-lp-formulations-for-polynomial-optimization,
  davis2024-rational-dual-certificates, dklerk2017-improved-upper-bounds,
  gamertsfelder2025-countable-gmp, gribling2026-squared-kernels,
  grimm2007-structured-sparsity, guo2025-robust-pmi-sos-convex,
  han2018-local-moment-matching, heijmans2026-degree-bounds-general,
  hoffman1952-approximate-solutions, kahl2005-globally-optimal-estimates,
  kallenberg2002-foundations, korda2025-convergence-rates-sparsity,
  lasserre2001-global-optimization,
  lasserre2006-convergent-sdprelaxations-in-polynomial-optimization,
  laurent2023-effective-schmudgen, magron2025slides-lorentz,
  magron2026slides-tenors, nie2026-sparse-tightness,
  parrilo2003-semidefinite-programming, peyrl2008-rational-sos,
  piazzon2018-chebyshev-grids, powers2000-univariate-interval (must contain
  the degree-bounded Markov–Lukács theorem for even and odd degree),
  tondel2003-mpqp, tran2026-truncated-moment-rates,
  vorobev1962-consistent-families, waki2006-sparse-sos.
- Public labels cited by Sections 1 and 10 that technical writers must
  define: thm:pre, cor:pre-grid, cor:pre-certificate, thm:mod,
  thm:quad-sharp, prop:exact-orders, thm:fixed-recourse,
  prop:private-bounds-needed, prop:convexity-needed, prop:rec-dual,
  thm:affine-recourse, thm:affine-sharp, rem:merge-split, rem:grid-baseline,
  thm:reg-cheb, thm:reg-holder, lem:half-degree, ex:reg-sharp,
  ex:strict-convex-insufficient, thm:constr-pre, thm:constr-mod,
  thm:finite-state, thm:finite-state-mod, and the section labels
  sec:kernels … sec:certificates.
