# Independent theorem-structure review (Opus), round 1

Date: 2026-10-06. Scope: the mathematical structure, assumptions, interfaces,
and expert readability of the complete manuscript. This is an independent
reconstruction, not a literature audit. The preliminary literature file was
used only to compare scopes. No experiment, solver, build, CI check, or
project-wide verification was run. No authored TeX, source note, or other
manuscript was edited.

## Verdict

**No fatal or central mathematical flaw was found, so root does not need to
be alerted.** Every main contract survives independent reconstruction under
its stated hypotheses. That includes every constant, degree ledger, and
explicit example I checked. No unresolved proof gap remains. The findings
below are:

- one moderate readability defect: notation that collides across sections
  and inside Section 6;
- several minor clarifications to scope and exposition;
- one optional, rigorous **extension**. It gives an `O(log r / r^2)` gap
  for continuous piecewise-affine projected multipliers on bags with two
  shared coordinates. This partly settles open problem 5 of
  `sec:discussion`. It is a new development, not a repair, and needs an
  independent check before any use.

The manuscript is coherent and clearly structured. Each technical section
starts by saying what it proves, and every theorem names its cone, its degree
convention, and whether it concerns every feasible point, the moment value,
or certificates. The earlier front-matter overstatements are fixed in the
current text (`front-root-r1.md` items 1–11; `theorem-structure-sol-r1.md`
front-matter rows). These include the paired-model scope of `2E_{2r}(h)`, the
activation/corner non-equivalence, the qualified Archimedean opening, and the
regime-specific grid baselines.

### Drafting status versus defects

When this review began, Sections 3–9 and Appendix B were absent. All of them
are now present, and all were reviewed in the snapshot below. No finding
below is a drafting-incompleteness item. Appendices A and C do not exist, and
`main.tex` does not input them; that is consistent.

### Snapshot reviewed (SHA-256)

| File | SHA-256 |
| --- | --- |
| `sections/00-abstract.tex` | `62d688f2d5b10d9e69c1cc6df5155c62f3d14db79c25c7864bbf55347eae5aee` |
| `sections/01-introduction.tex` | `e4896d54f29bc7f4491942d115285c96101a92dd2b7b82697f63bd95377b05d9` |
| `sections/02-setting.tex` | `0b69c1dd6bf4d8712d2891ca579ca9004099f12f1aea0ba9957aa399774315c6` |
| `sections/03-kernels.tex` | `d13c690cf52da022e8555b4639c510ce05d8b59d55a88a5dd2ee8e4eaa1f643a` |
| `sections/04-ordinary.tex` | `94e988857c6476493c3fc7b92403252baa610ce53d624a11e1fc8603a2593cc2` |
| `sections/05-sharpness.tex` | `9f6e5df9f447297fce0fedca96b80a5e438464178f190742da84165e106eae63` |
| `sections/06-recourse.tex` | `afc7a509b9c4828b28873ad9a82de539d5c9a352f9421a7ac0500bb251bd9042` |
| `sections/07-regularity.tex` | `67ae728c7d2e982eddd1b8c68b26b85ee6658b50a890215071328bb4b46a9510` |
| `sections/08-extensions.tex` | `88f01b9ad4b122be22dd617bd9b96164b5337647b783afbcfce98972293d3d98` |
| `sections/09-certificates.tex` | `16f211c8a1f5b5a99ca18dc5f0db761d1b6ad228433b28f3c586f1673f82548a` |
| `sections/10-discussion.tex` | `0f7309dc8c9de7d7fab20a01c48eb7ef7a7d4c8089d47b94b88443827a26582f` |
| `appendices/B-recourse.tex` | `4c2250b5d513be3f2f0dc8f9019abc05dc1fa27c9cecf55d6586266c9625240f` |
| `main.tex` | `405f420b6a35f3e11826b6c3b8e2248c6159393815ce82a479fb2c98de70f543` |
| `macros.tex` | `924ef1e21c7318277211f958fd79f5b38b81e6b25f7613bdbf421aeaa269139e` |

Line numbers below refer to this snapshot; labels identify the passages if
lines move.

## Findings

| # | Severity | Locator | Finding | Repair |
| --- | --- | --- | --- | --- |
| F1 | Moderate (readability) | `06-recourse.tex` lines 56–121, 70, 622–626, 790–792, 905–913; `04-ordinary.tex` `eq:mod-D`, `eq:mod-eta`; `08-extensions.tex` line 179 | Symbols collide inside Section 6 and with Sections 3, 4, and 8. See F1 below. | Rename as listed in F1. No mathematics changes. |
| F2 | Minor (scope clarity) | `07-regularity.tex` lines 198–203, `thm:reg-cheb` | The weighted Chebyshev hypothesis excludes every kinked projection, even in one variable, so the natural parametric-QP output is covered only by `thm:reg-holder`. The text does not say this. | Add one sentence; see F2. Optional extension D in a separate section. |
| F3 | Minor (expert intuition) | `01-introduction.tex` lines 91–110 (`sec:intro-mechanism`) | A fixed private polytope can produce the corner `-|x|`, whose approximation error is of order `1/r`, yet the fixed-domain rate is `r^-2`. An expert will ask why. | Add one sentence on concave versus convex corners; proof in F3. |
| F4 | Minor (statement strength) | `04-ordinary.tex` `cor:mod-rate`, lines 511–514; `01-introduction.tex` line 169 | The `log^3 r/r^2` rate is stated only for sufficiently large `r`. A one-line trivial bound makes it hold for every `r >= d`, with the same dependence only on `w` and `d_infty`. | Add a remark; proof in F4. |
| F5 | Minor (readability) | throughout; e.g. `06-recourse.tex` lines 135–149, 1073–1080; `09-certificates.tex` lines 318–339; `07-regularity.tex` lines 356–362, 495–508 | Scope disclaimers repeat within a section and often restate the abstract and Section 1.5. The density slows expert reading without adding content. | Keep one definitive scope statement per theorem family and delete repetitions. |
| F6 | Nit | `08-extensions.tex` lines 68–83; `08-extensions.tex` `ass:global-error` | `sigma_0` is the Slater margin in `prop:convex-slater` but means an SOS multiplier everywhere else. `H` is the error-bound constant, but `H_b`, `H_J`, the Section 9 tuple `H`, and the constants `H_{bi}` also use `H`. | Rename the margin `s_0`, `gamma_0`, or `\varsigma_0`, and the error-bound constant `c_K` or `\kappa_K`. |
| F7 | Nit | `06-recourse.tex` lines 205, 488–489, `thm:fixed-recourse` | "Exact at every order `r >= w`" when no `H_b` entry depends on `x`. Exactness actually holds for every `r >= 1`: with `m=1` the kernel is `1` and the conditional-mean proof is unchanged. The `r >= w` restriction comes only from the theorem's general hypothesis and the lemma's `m >= 2` assumption. | Optional: either say "every `r >= 1`" and allow `m >= 1` in `lem:conditional-matrix`, or leave the claim as stated (it is true). |

### F1. Notation collisions (moderate)

The collisions are concrete and occur where readers check constants:

1. **`Gamma`.** Section 4 defines `Gamma_v=(1+eta)^v-1` for an integer bag
   size `v`. Section 6 defines `Gamma_alpha=prod_i gamma_{alpha_i}` (line 70)
   and also `Gamma_b=Lambda_b kappa_b ||E_b||_2` (line 625). In the proof of
   `thm:affine-sharp` (lines 908–913), "`Gamma_1=0`" and "`Gamma_2=sqrt2`"
   use the bag meaning. To a reader who has just finished Section 4,
   `Gamma_2` means `(1+eta)^2-1`.
2. **`Lambda`.** Section 4 uses `Lambda=s^2(N+1)/C_s` for the kernel norm.
   Section 6 uses `Lambda_b` for the private Lipschitz constant ("`Lambda_2=1/2`",
   line 908), and `prop:convexity-needed` uses `Lambda` for a linear
   functional (lines 573–589).
3. **`a_k`, `a_0`, `b_j`.** Section 6 redefines the Jackson kernel with
   `b_j` instead of Section 3's `tau_j` and keeps `a_k` for the
   autocorrelation (lines 56–121). In the same section `a_b` is the fiber
   right-hand side (`a_{bj}` in `lem:conditional-matrix`), and the sharp
   example sets "`a_2=(1,1)^T`" (line 792), while `lem:rec-kernel` uses
   "`a_0-a_2=4m-3`". Section 8 then reuses `a_0=1-delta` (line 179).
4. **`delta`, `D`, `tau`.** These are milder: Section 4's `delta` versus
   Section 6's `delta_m`; Section 4's `D` versus `D_b` (Section 7) and
   `D_C` (Section 9); and `tau` for the Section 3 kernel weights, the
   Section 6 degree reserve, the Section 8 label masses, and the Section 9
   slack.

The simplest coherent repair:

- In Section 6, do not re-derive the kernel. Cite `lem:jackson` and state
  `lem:rec-kernel(a)` only through `gamma_k`:
  `1-gamma_1=3/D_m`, `1-gamma_2=3(4m-3)/(mD_m)`, and
  `(3-2m)/a_0=3(3-2m)/(mD_m)`. This removes `b_j`, `a_k`, and `a_0` from the
  section, and the identity `a_0-a_2=4m-3` can be proved once in Section 3
  or Appendix-level text.
- Write `gamma_alpha=prod_i gamma_{alpha_i}` for the tensor multiplier,
  extending the existing `gamma_k` naturally.
- Rename `Gamma_b` to `Theta_b` and `Lambda_b` to `Lambda^y_b` (or
  `G_b`), and rename the functional in `prop:convexity-needed` to `ell`.
- In Section 8, rename `a_0=1-delta` to `underline{omega}`. It is the lower
  bound on `omega`, which makes the formula easier to read.

### F2. Weighted Chebyshev regularity excludes kinks (minor)

If `a(u)=|u-c|` or `a(u)=(u-c)_+`, then its Chebyshev coefficients satisfy
`|a_k| asymp 1/k^2`, so `sum_k |a_k| max(1,2k)` diverges logarithmically.
Hence `thm:reg-cheb` excludes every projection with a kink, including the
sharp example's `-2x_+` and every piecewise-affine parametric-QP output.
Those cases enter only through `thm:reg-holder`, which requires each
component to depend on its own coordinate alone. The text after
`thm:reg-cheb` lists what satisfies the hypothesis (polynomials, geometric
decay) but not this exclusion. Suggested sentence:

> Piecewise-affine projections with a kink do not satisfy
> \eqref{eq:reg-cheb-assumption}, since their Chebyshev coefficients decay
> only like $k^{-2}$; such projections are covered by
> \cref{thm:reg-holder} when they are coordinatewise.

Section D below shows how to cover such kinks in two-coordinate bags with a
`log r` loss.

### F3. Why concave corners do not slow the fixed-domain rate (minor)

`sec:intro-mechanism` correctly limits the `2E_{2r}(h)` identity to the
paired models. The next paragraph says that `|x|` costs `1/r`. A careful
reader then notices that `min_{|y|<=1} xy=-|x|` is a fixed-polytope value
function with the same `1/r` approximation error, while
`thm:fixed-recourse` gives `r^-2`. The resolution is short and rigorous.

For a fixed polytope, `F_b(x)=min_{y in P_b} z^T H_b(x) z` is an infimum,
over a fixed compact set, of functions of `x` whose second derivatives are
uniformly bounded on the box. Hence `F_b - C|x|^2` is concave for some
`C`: `F_b` is semiconcave and can have only concave corners. The paired
lower-bound mechanism needs one bag whose value has a convex corner, `+h`.
Fixed polytopes cannot produce one. Moving fibers can, for example
`min{y: y>=x, y>=-x}=|x|`.

Suggested sentence after line 96:

> A fixed private polytope can create concave corners, such as
> $\min_{\abs y\le1}xy=-\abs x$, but not convex ones, because its value
> function is a minimum of uniformly smooth functions of the shared
> variables; the obstruction above requires a convex corner.

This is consistent with the existing explanation in lines 103–107: source
feasibility at the output point.

### F4. The ordinary-module rate holds at every order `r >= d` (minor)

Let `deg f_b <= r`. `lem:cheb-moment` gives `|L_b(T_alpha)| <= 1` for every
mode of `f_b`, so every feasible family has
`sum_b L_b(f_b) >= sum_b c_{b,0} - C_f`. Product arcsine integration gives
`f* <= sum_b int f_b dmu = sum_b c_{b,0}`. Hence `f*-rho^mod_r <= C_f` for
every `r >= d`. Let `r_0(w,d_infty)` be the threshold in
`eq:mod-threshold`. Note that `d <= w d_infty`. Let `K_1` bound
`r^2/ell_r^3` times the bracket in `eq:mod-rate` for `r >= r_0`. It is
finite and depends only on `w` and `d_infty`, because
`ell_r^{w+1}/r^3` is at most a `w`-dependent constant times
`ell_r^3/r^2` for all `r`. With
`K = max(K_1, max_{d<=r<r_0} r^2/ell_r^3)`, we get

`f*-rho^mod_r <= K_{w,d_infty} C_f log_2^3(r+2)/r^2` for every `r >= d`,

where `K` depends only on `w` and `d_infty`. A one-sentence remark after
`cor:mod-rate` would let the introduction's `C_f O_{w,d}(log^3 r/r^2)` be
read without a threshold.

### F5. Repeated disclaimers (minor, editorial)

Experts will accept a single precise scope statement. The current text
repeats "this is not a runtime claim", "no claim about conditioning", and
"the theorems supply no algorithm" several times per section (e.g.
`rem:rec-dimension`, the last paragraph of `rem:grid-baseline`, the closing
paragraphs of Sections 7 and 9). Section 1.5 and the Discussion already
state these limits once and well. Removing the in-section repetitions,
except where a specific theorem invites a specific misreading, would shorten
the paper noticeably without weakening any boundary.

## Independent reconstruction of the main contracts

The checks were done by hand from the manuscript text, with source notes
consulted where useful. Two concrete computations were also re-run (see
Verification).

### 1. Setting and finite SDP duality (`sec:setting`)

- `lem:zero-decomposition`: at a leaf, a coordinate outside the parent
  separator occurs in no other bag, so its monomials cannot cancel. The
  degree is preserved. Correct.
- `lem:compact`: the singleton localizer at `x^{alpha-e_i}` gives
  `L(x^{2alpha}) <= L(x^{2(alpha-e_i)})`; Cauchy–Schwarz then handles split
  exponents. Correct.
- `lem:slater`: product arcsine moments make every retained block positive
  definite. Primal Slater plus a finite value gives zero gap and an attained
  dual. Summing dual feasibility cancels the separator multipliers, and
  `lem:zero-decomposition` gives the converse. Correct.
- `lem:interval-sos`: the odd-degree padding through
  `1 +- x = ((1 +- x)^2+(1-x^2))/2` gives degrees `2j <= 2k` and
  `2j-2 <= 2k-2`. Correct.
- `def:rec-hierarchy`: the domain degrees in (R1)–(R3) are `2r` shared and
  at most two private. Rows with `epsilon_bj=1` reach shared degree `2r-1`.
  Correct. This hierarchy is at least as strong as both source
  hierarchies, so source upper bounds transfer. Actual-measure lower bounds
  hold for it.

### 2. Full preordering (`thm:pre`, `cor:pre-grid`)

- I re-derived `a_0=(2m^3+m)/3`, `a_0-a_1=m`, and
  `1-gamma_k <= k^2(1-gamma_1)=3k^2/D_m` for all `k`, beyond the kernel
  support included. The square degrees of the tensor certificate are
  `v_b(m-1)-|I| <= r-|I|`. Separator marginals have source degree at most
  `2|S|(m-1) <= 2r`.
- `rem:ker-degree`: the order-one counterexample has eigenvalues
  `0, 3/2, 3/2` and `L((1-x)(1-y))=-1/2`. Verified.
- Grid: `2N_g-1 >= 2(m-1)+d_infty`, exact Gauss–Chebyshev quadrature (the
  odd-`k` sum `i/sin theta`). Correct.

### 3. Ordinary module: exact signed correction (`thm:mod`, `cor:mod-rate`)

This is the paper's lead contribution. I reconstructed it completely.

- `lem:sos-kernel`:
  - `M_s=(C_s+R_s(T_2(x),1))/2` gives `0 <= z_s <= 1/2`.
  - The even-`N` identity
    `sum_{j<=N} z^j = (1/2)[1+sum_{j<N/2}(z^j(1+z))^2+z^N]` was checked by
    parity counting.
  - `omega=1-z^{N+1}` and `||z_s||=(C_s-1)/C_s`.
  - `||Phi_s(.,u)|| <= s`, so `Lambda=s^2(N+1)/C_s`.
- `lem:mod-defect`: I re-derived the pairing that gives
  `-(chibar_{l+k}-chibar_l)^2`, `-chibar_k^2`, and the symmetrized interior
  sum. The norm bound `k^2/s^2+3k^2/(2s)` uses
  `sum_l (chibar_{l+k}-chibar_l) <= k`.
- `lem:residual-products`:
  - Telescoping `delta^{2j}-H^2` multiplies one single-generator interval
    certificate by SOS factors in each term, with degree at most
    `(v+j)D <= 2r`.
  - `G(a+cH)^2` has square roots of degree `(v+j)D/2 <= r`, so
    `|L(GH)| <= delta^j L(G)` holds without division.
  - `L(G) <= Lambda^{v-j}` uses `deg G <= r`.
  - Terms with zero or one residual are nonnegative under the ordinary
    module alone.
- `thm:mod`:
  - The recursion `Delta_{v+1}=(Lambda+delta)Delta_v+v Lambda^{v-1}delta^2`
    was verified from Pascal's rule.
  - One common scalar `Delta_w` preserves equal separator marginals,
    because the reference density marginalizes to the constant one.
  - The identity `I^+ - Ibar = Delta_w(I - I^+)` compares two genuine
    probability expectations, so no probability inequality is applied to a
    signed density.
  - The total error is `sum_b C_b Gamma_{v_b} + Delta_w W`, with no edge or
    bag-count factor.
- `cor:mod-rate`: every inequality was checked, namely `N+1 <= (c_w+3)ell_r`,
  `wD <= r`, `delta <= s^{-c_w}/2`, `eta <= (3d_infty^2+1)(N+1)/s^2`, the
  Taylor bound `Delta_w <= binom(w,2) delta^2 (Lambda+delta)^{w-2}`,
  `w-2-2c_w <= -3`, and the final constant `binom(w,2)2^{w+3}w^3(c_w+3)^{w+1}`.
- `rem:calibration`: all four table values were recomputed exactly; see
  Verification.

**Contract met:** the transfer is exactly consistent with a signed density
and one common correction, the rate is `O(log^3 r/r^2)` normalized by
`C_f`, and there is no extra bag-count factor. The threshold depends only
on `w` and `d_infty`; see F4 for extending the bound to all `r >= d`.

### 4. Sharpness and exact orders (`thm:quad-sharp`, `prop:exact-orders`)

- Fibers `-phi`, `phi` with `phi=y_+^2`; `f=(y-x+z)^2+2xz`.
- Fejér witness: `Q_N=sin(2N t)F_N(t)` has frequencies `N+1..3N-1`; the
  pairing is `-2 sin(k pi/2)/(pi k(k^2-4))`; the odd weights sum to `N/2`.
  Hence `E_n(phi) >= 1/(27 pi (n+2)^2)`.
- Budgets `A(f_1)=4`, `A(f_2)=6`, and `C_f=23/4` were recomputed.
- Order one: the certificate identity; the atomic functional with
  `L(y)=0`, `L(y^2)=3/4`, `L(g_x)=0`, `L(g_y)=1/4`, `L(f_1)=-1/2`; and the
  reflected bag value `1/4`.
- Order two: certificate, minors, and witness re-expanded exactly; see
  Verification. The majorant remark's Cauchy–Schwarz contradiction,
  `1 <= sqrt2-1/2`, was also checked.

### 5. Fixed private polytope (`thm:fixed-recourse`, `prop:*-needed`, App. B)

- The conditional matrix `M_b(u) >= 0` follows from (R1) with the
  kernel's square roots. (R3) gives `Y_kk <= h`. A zero density gives
  `M=0` by its minors. The mean is feasible because `epsilon=0` keeps the
  allowance `r-|I|`.
- `lem:mixed-moment`: `|L(T_alpha z_i z_j)| <= 1` for `|alpha| <= r`.
- Jensen: the Schur complement times `Q_b >= 0`.
- Measurability: `{h>0}` is open and `ybar` is continuous there.
- Appendix B: the lowest-degree argument forces `k=3` (the factor `w_I` adds
  degree at least two). I re-checked the cubic-coefficient contradiction,
  including that the cross terms `2ch`, `2af`, `2be`, and `2cd` vanish. The
  closedness of `Pre_r` follows from the uniform-measure Gram bound.
  Normalization of the separator holds at every `r >= 3`. `L_R` is
  feasible.

### 6. Affine complete recourse, inverse-order rate, sharpness (`thm:affine-recourse`, `thm:affine-sharp`)

- One-degree reserve: `m = ceil(r/w) = floor((r-1)/w)+1`. The proof
  `(1-x_i^2) w_I p^2` with `i` in `I` becomes `w_{I\i}((1-x_i^2)p)^2`
  (degree checked).
- Source feasibility `ybar in P(xbar)`. The Hoffman repair with residual
  `(E(xbar-u))_+` is followed by `||phi-ybar|| <= kappa||E|| ||xbar-u||`.
- Displacement: `int K(x-u)^2 = V_m + (3-2m)x^2/a_0`, using
  `a_0-a_2 = 4m-3` (re-derived from the differences 1, 2, ..., -2, -1).
- The sharp instance:
  - `A=1`, `Lambda_2=1/2`, `||E_2||=2 sqrt2`.
  - `kappa_2=1` is admissible: unit rows on an interval give the distance as
    the largest positive residual.
  - The total-degree certificate `f+delta_m`: `s_m` is odd with degree at
    most `2m-3`; `|x|-x s_m <= 2(int K(x-t)^2)^{1/2}`; the degrees are `2m`
    and `2m-1`.
  - The `|x|` witness: `c_{2l}=-4(-1)^l/(pi(k^2-1))`; the even weights sum
    to `N/2`.
- Merge and split identities expanded.

**Contract met:** the rate is inverse-linear, sharp in both hierarchies, and
proved separately for each.

### 7. Regular projected multipliers (`thm:reg-cheb`, `thm:reg-holder`, `lem:half-degree`)

- KKT identity and the plus sign of the correction
  `a^T(U-uh)`: the source-feasibility term is nonnegative.
- Commutator frequencies satisfy `sum ceil(alpha_i/2) <= v(m-1)+1 <= r`.
- The half-degree certificates: `1 +- T_{2q+1}` equals
  `(1 +- x)(U_q -+ U_{q-1})^2`, verified in angle form, and the parity
  identity was checked by expansion.
- The mode commutator
  `(1/2)(gamma_k-gamma_{k+1})T_{k+1} + (1/2)(gamma_k-gamma_{k-1})T_{k-1}`,
  with `|gamma_j-gamma_{j+1}| <= (2j+1)(1-gamma_1)`.
- The Hölder case uses a univariate certificate of degree at most
  `2m <= 2r`.
- `ex:reg-sharp`: the rescaled multiplier, `A=2`, and `M=H=2` were
  re-derived, including the box-row multipliers at `x <= 0` and `x=1`.
- `ex:strict-convex-insufficient`: the one-sided limits are forced, because
  only one non-box row is active on each punctured side.
- `prop:reg-qp`: the KKT matrix is nonsingular, LICQ makes the multiplier
  unique, and segments split into finitely many pieces. Correct.

**Contract met** as stated. On scope, see F2 and section D.

### 8. Global constrained error bounds (`thm:constr-pre`, `thm:constr-mod`, `prop:constr-dual`)

- Conditional violation `(-g(u))_+^2 h <= L(K (g(x)-g(u))^2)`, with no
  division at `h=0`.
- `J(g^2) - 2gJg + g^2` has degree at most `2d <= r`, and its norm is at
  most `12 ||g|| A(g)/D_m`.
- `lem:ext-difference`: the divided difference has degree `k-1` and
  modulus at most one. The weighted-square identity was verified
  algebraically (`sum_{l<k} w_l w_k(a_l-a_k)^2 = A sum w a^2-(sum w a)^2`).
- `lem:ext-displacement`: `J_s <= 2/s` by Parseval applied to
  `(1-e^{it})F_s`, and `p <= 2/C_s`.
- Domination `h^+ >= h/(1+Delta_w)`, with remainder mass at most
  `1+Delta_w-a_0^{v}`.
- `L_f = A` is a valid Euclidean Lipschitz constant.
- `prop:convex-slater` and the local/global example (`alpha <= 1/2`) are
  correct.
- `prop:constr-dual`: `1 +- x^beta` lies in the ordinary box module, so the
  constant is an interior order unit. Separation from the interior needs
  no closedness. Correct.

### 9. Labelled ordinary correction including zero mass (`thm:finite-state-mod`)

- Mass-scaled moment control `|L(T_beta)| <= tau`. When `tau=0`, the zero
  diagonal of the PSD form forces the whole functional through `2r` to
  vanish.
- The shift `Delta_w tau_{b,a}` preserves label masses, and fiber sums
  agree through (11) at `p=1`.
- The per-family bound weighted by labels is distinct from the data-only
  bound `C_mix(Gamma_w+2Delta_w)`.
- Pruning: masses of non-extendable labels are zero by discrete gluing.
  A positive law on `mathcal A` gives Slater for the pruned SDP, and the
  labelled dual identity was re-derived.

**Contract met.**

### 10. Real recourse strict-level certificates (`prop:rec-dual`)

- The order unit `1 +- g g'` uses `1-x^{2beta}` (singleton telescope) and
  (R3) with `I` empty. The sparse quotient includes private monomials,
  which belong to exactly one bag.
- Separation of `f-lambda` from the convex cone with nonempty interior
  gives `F` in `C_r^*` with `F(f-lambda) <= 0`, and `F(1) > 0`, which is a
  contradiction. This proof is cleaner than the audit's closure argument
  and avoids closedness.
- No boundary attainment is claimed, which is correct.

**Contract met.**

### 11. Rational Grams with objective slack (`thm:rational`, `cor:rational-mod`)

- Interior tuple: the complement identity was verified (both telescopes),
  the blocks have degree at most `r`, `H >= I/D`, and `tr <= r+1`.
- Outer bound: `(a+1)(a+3)` divides `(2r+3)!`, `det(q_0 W) >= 1`, and
  `lambda_min >= q_0^{-s} s^{-(s-1)}`.
- Right inverse: disjoint pivots give `||Z(c)||_F <= ||c||_1`.
- Rounding: `||G(Q^0-Q*)||_1 <= 2^{w+1}Vh` and `2+2^{w+1} <= 2^{w+2}`.
  The denominator is `2L`.
- Membership promise: `rho >= f* - E >= lambda + tau`, and attained finite
  duality gives real membership of `f-lambda-tau`. The time claim is
  correctly absent; only witness size and checkability are asserted.

**Contract met.**

## D. Optional development: finite-band directional regularity, and kinked multipliers in two-coordinate bags

This is a proposed strengthening of Section 7, not a defect repair. It
needs an independent check and a priority/literature decision by root and
Luna before any manuscript use.

**Setting.** Use the hypotheses and parameters of `sec:regularity`:
complete affine recourse, private convexity, `m = ceil(r/w)`, and a KKT
selection whose projection `a_b^dual` is bounded and Borel. For bag `b`,
component `i`, and `beta in {0,...,2m-2}^{B_b \ {i}}`, define

`phi_{bi,beta}(s) = c_beta int a_{bi}^dual(s,t) T_beta(t) dmu^{B_b\{i}}(t)`,
with `c_beta = prod_j (2 - [beta_j = 0])`.

Let `M_{bi,beta} >= ||phi_{bi,beta}||_infty`, and let `H_{bi,beta}` be a
Hölder seminorm of exponent `beta_H` in `(0,1]` on `[-1,1]`.

**Claim.**
`f* - rho^rec_r <= 3A/D_m + sum_{b,i} sum_beta Gamma_beta (3M_{bi,beta}/D_m + H_{bi,beta} V_m^{(1+beta_H)/2})`,
with `Gamma_beta = prod_j gamma_{beta_j}` in `[0,1]`.

**Proof.**

1. *Finite expansion.* `K_{m,b}` is a finite tensor Chebyshev sum, so
   integrating out `u_{-i}` gives exactly
   `R_{bi}(x) = sum_{beta: beta_j <= 2m-2} Gamma_beta T_beta(x_{-i}) R_{bi,beta}(x_i)`,
   where `R_{bi,beta}(x) = int K_m(x,s) phi_{bi,beta}(s)(x-s) dmu(s)`.
   No series convergence is needed.
2. *Pointwise bound.* The proof of `thm:reg-holder` gives
   `|R_{bi,beta}| <= eps_beta := 3M_{bi,beta}/D_m + H_{bi,beta}V_m^{(1+beta_H)/2}`
   on `[-1,1]`.
3. *Certificate.* The identity
   `eps - T_beta R = (1/2)[(eps+R)(1-T_beta) + (eps-R)(1+T_beta)]`
   is a product of a univariate interval certificate in `x_i` of degree at
   most `2m`, and a certificate for `1 +- T_beta` from `lem:half-degree` of
   degree at most `2 sum_{j != i} ceil(beta_j/2) <= 2(v_b-1)(m-1)`. The
   coordinates are disjoint, so the product lies in the shared preordering,
   with square degree at most `m + (v_b-1)(m-1) - |J| = v_b(m-1)+1-|J| <= r-|J|`.
4. *Conclusion.* Hence `L_b(T_beta R_{bi,beta}) <= eps_beta` and, since
   `Gamma_beta >= 0`, `L_b(R_{bi}) <= sum_beta Gamma_beta eps_beta`.
   Combine with `eq:reg-conditional`, `lem:rec-matrix-cost`, and the
   optimal-policy construction exactly as in Section 7.

**Consequences.**

- With only `beta = 0` nonzero, the claim is exactly `thm:reg-holder`.
- It is not comparable with `thm:reg-cheb`, because Chebyshev mode `k` in
  `u_i` has Lipschitz constant `k^2`, not `2k`.
- It newly covers non-coordinatewise projections, for example
  `a_{b1}(u) = -2(u_1)_+ g(u_2)` with summable Chebyshev coefficients
  of `g`.

**Kinked projections in two-coordinate bags.** Let `v_b <= 2`, and let each
projection component be continuous and piecewise affine with finitely many
polyhedral pieces, as delivered by `prop:reg-qp` under its LICQ hypotheses.
Fix `i` and let `t` be the other coordinate.

- For each `s`, `t -> a(s,t)` is Lipschitz and piecewise affine with a
  uniformly bounded number of kinks. Two integrations by parts in
  `theta = arccos t` give `M_k = O(1/k^2)`.
- The difference quotient `(a(s,t)-a(s',t))/|s-s'|` is an average of
  `partial_s a(.,t)`. That derivative is piecewise constant in `t`, with a
  uniformly bounded number of jumps of size at most `2 Lip(a)`, so the
  quotient's total variation in `t` is uniformly bounded.
- One integration by parts then gives `H_k = O(1/k)` with Hölder exponent
  one.

Therefore
`sum_{k <= 2m-2} (3M_k/D_m + H_k V_m) = O(1/m^2) + O(log m / m^2)`, and

`f* - rho^rec_r = O(log r / r^2)` for width-two bags with continuous
piecewise-affine projected multipliers, including oblique region boundaries.

If confirmed, this changes open problem 5 of `sec:discussion`: Lipschitz
piecewise-affine projections with oblique boundaries are handled up to a
`log r` factor at width two. Width at least three, general multivariate
Lipschitz projections, and the necessity of the logarithm remain open.

The extension also strengthens `prop:reg-qp`: its LICQ regime would cover
bags of size two, not only scalar bags. The `beta`-sum grows like
`m^{v-1}` for wider bags. Tensor coefficients of difference quotients with
oblique kinks in two or more remaining coordinates need not be summable at
a polylogarithmic rate, so I make no claim for `v >= 3`.

## Verification actually performed

Commands run for this review, all targeted:

- Read-only `cat`, `sed`, `grep`, `wc`, `ls`, and `sha256sum` on the
  assigned evidence files, all section and appendix sources, `main.tex`,
  and `macros.tex`.
- `/workspace/local-home/miniconda3/bin/python3 -I -c '...'`: recomputed the four
  rows of `rem:calibration` from the formulas of `thm:mod`. The values
  match the table to the displayed precision: `0.035389`, `0.59993`,
  `1.869e8`, `1.2056`. The cutoff `s` is maximal in the first three rows
  (`s+1` violates `wD <= r` under the prescription).
- `/workspace/local-home/miniconda3/bin/python3 -B /tmp/sos-review-check/check5.py`
  (SymPy 1.14.0; the first `-I` attempt could not import SymPy, which is in
  the user site directory). Results:
  - both identities in `eq:shp-p-identities`: zero residual;
  - the Gram identity `eq:shp-gram`: zero residual;
  - `(b+1)(b+a)/b = 3b`;
  - the leading minors equal the stated values;
  - witness mass one with vanishing first and third moments;
  - objective `+2E_*` gives zero;
  - `p_* - phi` takes the values `0, 2E_*, 0, 2E_*, 0, 2E_*` at the six
    contact points.

These are checks of specific finite identities and constants. All general
statements were checked by the proof reconstructions above. No CI result,
build, experiment rerun, or literature search is claimed.

## Final verdict

**ACCEPT the mathematical structure, with no fatal or central defect.** All
of the following contracts hold as stated:

- the exactly consistent ordinary-module transfer, normalized by `C_f`,
  with no bag-count factor;
- the fixed-domain inverse-square rate;
- the affine inverse-linear rate and its sharpness;
- regular projected multipliers restoring inverse-square;
- the global constrained error bounds and strict-level constrained
  certificates;
- the labelled ordinary correction including zero mass;
- the recourse order-unit duality;
- rational Grams with slack.

Before submission, F1 should be repaired, because the colliding `Gamma`,
`Lambda`, and `a` symbols appear exactly where referees check constants.
F2–F4 are one-paragraph additions. Development D is optional, and root
decides whether to pursue it after independent verification.
