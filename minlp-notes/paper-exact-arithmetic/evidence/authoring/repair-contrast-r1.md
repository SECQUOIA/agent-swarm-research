# Repair report: contrast round 1 (Appendices J and K)

Author: Opus implementation agent for the contrast repair. Date: 2026-10-05.

## Scope and inputs

Files changed: `appendices/J-quadratic-contrast.tex` and
`appendices/K-boundaries.tex`. This report is the only other file written.
No shared macro, `main.tex`, bibliography, other writer's file, author
report, review, or historical note was edited. No label was renamed, added,
or removed, and no macro was introduced.

Inputs read: `evidence/BRIEF.md`, `evidence/authoring/CONVENTIONS.md`,
`evidence/authoring/DECISIONS.md` (including the superseded D3: Q13–Q14 now
belong to Appendix L and were not touched here), the current
`evidence/literature-review.md` (including its new J/K contract rows), the
original author report `evidence/authoring/contrast.md`, the full Sol review
`evidence/reviews/contrast-r1.md`, the root-relayed independent findings, and
Luna's source-gate clearance relayed by the root.

Preserved as required: Q1–Q12 in Appendix J (Q7 brief), the odd-degree
independent-block feasible-output corollary `cor:qc-feasible-output`, and
all of Appendix K's results. No Q13/Q14 material was added.

Line numbers below refer to the files after this repair (J has 2717 lines,
K has 524).

## Responses to findings

### 1. Medium: weight quantifier in `thm:qc-blocks`(d) — fixed

Finding (root and Sol): (d) inherited arbitrary positive weights from (b)
and assumed only `omega_k >= 1`, while the proof uses `omega_i >= 1` and
`omega_i <= omega_k`. The claim is false without them.

Check: I reproduced the counterexample. For `k = 2`, `omega_2 = 1`, the
prescribed `eta = 1/(4 gamma_bar)` does not depend on `omega_1`. Every block
optimizer is nonzero, so stationarity at the old optimizer is equivalent to
`N mu = a` with `N = [[1, eta], [eta, 1]]`, whose unique solution has
`mu_2 = (lambda_2 - eta omega_1 lambda_1)/(1 - eta^2) < 0` for large
`omega_1`. The new rows have the Slater point `0`, so KKT conditions are
necessary and the old optimizer is not optimal. The lower bound is also
needed: for small `omega_1 > 0`,
`mu_1 = (omega_1 lambda_1 - eta lambda_2)/(1 - eta^2) < 0`.

Repair (J:1533–1535, 1574–1599): (d) now begins "Let the weights satisfy
`1 <= omega_1 <= ... <= omega_k`, as those of (c) do". The proof states where
each inequality is used (`a_i > 1` from `omega_i >= 1`;
`Sigma < k omega_k gamma_bar` from `omega_i <= omega_k`) and why `N mu = a`
is forced. A short paragraph after the proof of (d) records the `k = 2`
multipliers showing that neither condition can be dropped.

Downstream uses are unchanged and satisfy the new hypothesis: (e),
`cor:qc-no-fpt-output`, `thm:qc-sparse`, and the explicit-weight remark after
`lem:qc-weight` all use weights `t^{i-1}` with integer `t >= 1`.

### 2. Low: rational parameters and empty rows in `thm:qc-number-field-qp` — fixed

Finding (root and Sol): the precision formula divided by
`max_iota ||C_iota||_1`, which is zero or undefined for all-zero or empty
`C`; and `delta`, `epsilon` were formed from possibly irrational constants
(`U` as a norm bound, Hoffman constants, Lipschitz bound).

Repair:

- J:2549: the chart radius `R` is now a computable rational with `R >= 1`.
- J:2578–2585: the Hoffman constants are replaced by rational upper bounds
  `H_A, H_M >= 1` of polynomial length. They come from the separation bound
  for nonzero minors and entrywise bounds for `||N||`, which hold uniformly
  over all row sets, so no enumeration of row sets is needed.
  Inequality `eq:qc-hoffman` remains valid with upper bounds.
- J:2588: `U = nR`, a rational bound for `||x||` on the box.
- J:2611–2617: `L_f = q U + c_bar`, with `c_bar >= 1` a rational bound for
  `||c||_1` from the power-basis coefficients and Cauchy's bound for `alpha`.
  The constants `U, q, L_f, H_A, H_M, T, W` are rationals fixed before
  `delta` and `epsilon` are chosen.
- J:2641–2652: the exact-output step uses
  `C_frak = max{1, max_iota ||C_iota||_1}`, with the inner maximum `0` for no
  rows, and a rational separation bound `g`. It now says explicitly that each
  computed slack is within `g/4` of the true slack, which justifies the
  threshold `g/2`.

Check of the parameter chain (unchanged formulas, now with rational
constants): `Gamma <= E^2/(16T^2) + E^2 U^2/(16 T^2 (U^2+1)) <= E^2/(8T^2) <= 1`,
`e <= E/2 + E/sqrt(8) < E`, and
`||y - p|| <= tau/16 + sqrt(tau^2/16 + tau^2/8) = tau/16 + sqrt(3) tau/4 < tau`.
The estimate `||y_hat||^2 - ||y||^2 <= 2Ue` uses that both points lie in the
box. The bounds `H_M >= 1` and `T >= 1` make `Gamma <= 1` automatic.

### 3. Medium: the eliminated object in the root penalty (K) — fixed

Finding (root and Sol): `R^{2^{-p(L)}}` is not a polynomial; eliminating the
chain gives polynomial *inequalities* of exponential degree.

Repair: the section introduction (K:352–361) now says that eliminating the
squaring chain leaves polynomial inequalities of exponential degree, and
eliminating all auxiliary variables returns the fractional power, which is
not a polynomial. `prop:bnd-penalty-limits`(a) (K:476–481) now gives the
inequalities `H_V s_0^{2^{p(L)}} >= h(x)`, one for each signed residual `h`.
The closing paragraph (K:513–521) distinguishes the degree-two nonconvex
lift, the exponential-degree inequalities with `s_0` kept, and the
non-polynomial term `R^varpi`. It now says that none of these is the
unconstrained minimization of an explicitly given globally convex polynomial
of bounded degree, so `thm:exact-upper`, which also needs a strong-convexity
bound or certificate, does not apply. "Signed residuals" are now defined in
the setting (K:369–373), before their first use in the theorem statement.

### 4. Medium (source contract): degree floor in the Basu–Mohammad-Nezhad bounds — fixed

Finding (root and Sol): the printed coefficient bound cannot hold literally
for degree one. Sol's example: quantify `z_1 = 2x`, `z_i = 2 z_{i-1}`,
`z_k >= 1`. The projection is `x >= 2^{-k}`, whose boundary needs `k`-bit
coefficients from constant-height linear input. This example is recorded
here and is not added to the paper.

Repair (K:378–394): both imported statements now carry their locators
(`[Theorem 4.1]` for one-block QE, `[Theorem 2.2]` for the Łojasiewicz-type
inequality) and state, as in the source, that the degree bound is at least
two. A description of lower degree is used with degree bound 2. The exponent
is now a positive integer `varrho <= (8d)^{2(n+7)}`, with a constant `C > 0`
and `log2 max(1,C) <= t d^{O(n^2)}`, matching Luna's verified contract. In
the proof (K:431–449), QE is applied with `d = 2` and `ell = 1` after clearing
denominators. The Łojasiewicz step uses the degree `2^{O(kappa)} >= 2` of the
eliminated description. The graphs of `g` and `e` are described by the
conditions defining `A` together with Boolean combinations of quadratic
conditions, so they obey the same bounds. All quadratic applications are
unchanged.

### 5. Low: uncertainty and regularization scope (K) — fixed

- K:14–21 (overview): the claim that singular equalities "cannot be
  certified" and that the exact model is "essential" is replaced. The new
  text says that enclosures of function values can fail to justify any
  accurate upper bound on the optimal value, even where a root exists robustly
  under perturbation, and that exact input removes this obstruction.
- K:252–260 (subsection introduction): the same precise scope. It adds that
  other conclusions can survive, since robust root existence holds in the
  second example.
- K:30–35: "minimized approximately" is replaced by the vetted contract.
  The optimal value of a globally convex rational quartic on a rational
  polyhedron can be approximated in polynomial time with an additive
  objective-gap guarantee (`[Corollary 1.2]` of the version-1 entry
  `SlotSteurerWiedmer2025`). The guarantee concerns the value, not the
  distance to a minimizer. Quartics have fixed degree, so the unary-degree
  input condition recorded in Section 02 is automatic.
- K:162–174 (regularization): the text now concerns the nonzero comparison
  gap `|m - c|` for a rational threshold `c`. Once `epsilon R^2 < |m - c|`,
  the sign of `min f_epsilon - c` equals that of `m - c`. Lemma
  `lem:separation`(b) at degree four guarantees only
  `|m - c| >= 2^{-2^{O(L)}}`. Therefore an `epsilon` chosen from this uniform
  bound can require exponentially many printed bits. The text says
  explicitly that this does not show that a particular instance needs such an
  `epsilon`. Check: the gap is the singleton projection of
  `{z = f(y) - c, grad f(y) = 0}` because every critical point of a convex
  function is a minimizer. Lemma (b) gives
  `|m - c| >= 2^{-2 tau 4^{c_0 n}}`, which is `2^{-2^{O(L)}}` because
  `tau = O(L)` and `n <= L`.

### 6. Low: literal small cases in K — fixed

- `prop:bnd-robust-root`(c) proof (K:330–334): for `k >= 2` the bags
  `{x, y_i, y_{i+1}}`, `1 <= i < k`, arranged along a path, give width two.
  For `k = 1` the single bag `{x, y_1}` has width one. I also rechecked the
  Jacobian determinant at the regular preimage, `(2^k + 1) x^{2^k} > 0`.
- `prop:bnd-penalty-limits` (K:475): "Let `k >= 1` be the chain length in
  (b)–(d)."
- `thm:bnd-root-penalty` (K:398–400, 446–448): `p` is a polynomial with
  nonnegative integer coefficients and `p(0) >= 1`, independent of the
  instance. Thus `p(L)` is a positive integer, and the lift has `p(L) >= 1`
  squaring steps, as part (a) of the limits proposition needs. In the proof,
  `p >= a` on `[1, infinity)` gives `varpi varrho <= 1` and
  `varpi log2 max(1, C) <= 1`.
- Integer coordinates (K:418–424): rational bounds `l <= z <= u` are
  replaced by `ceil(l)` and `floor(u)` before binary expansion, with
  `J_z = floor(log2(u_z - ell_z))` bits (none if `u_z = ell_z`). The row
  `z <= u_z` is kept, and nonemptiness of `S` gives `ell_z <= u_z`.

### 7. Encoding of input lengths (J) — fixed

Finding (Sol, relayed by root): J's printed lengths use the native dense
matrix encoding defined at J:96–97. The global explicit format of
Definition `def:models-polynomial` attaches full exponent vectors. The
feasible-point corollary should state its length in both formats. The
conclusion is robust if the fixed `k` is enlarged.

Repair:

- J:96–104: printed input lengths refer to the native matrix encoding. The
  explicit format lists only nonzero coefficients but attaches `O(n)`-bit
  exponent vectors to at most `(n+1)(n+2)/2` monomials per quadratic. The
  two lengths are polynomially related: `L_exp <= L_mat + O((m+1) n^3)` with
  `(m+1) n^2 <= L_mat`, and `L_mat <= O(L_exp + (m+1) n^2)` with
  `m, n <= L_exp`. Bounds polynomial in `L`, including `L^{O(k+1)}`, therefore
  hold in either format.
- `thm:qc-blocks`(e) (J:1542–1545) and its proof (J:1601–1605) give both
  lengths: `O((k+1) n^2 (1 + k^2 log ell_k))` native and
  `O((k+1) n^2 (n + k^2 log ell_k))` explicit.
- `cor:qc-no-fpt-output` proof (J:1617–1624): `k > 3C` (was `k > 2C`),
  `n < 2kR`, and `L = O_k(R^2 log R)` native or `O_k(R^3)` explicit. The
  degree `(2(R-1))^k` exceeds `phi(k) L^C` in both formats. The previous lower
  bound `n >= k(R-1)` was not used and is replaced by the needed upper bound.
- Explicit-weight remark (J:1665–1668): `L = O_k(R^6 log R)` holds in either
  format, because the weight bits dominate `n`. The threshold `k > 6C` is
  unchanged.
- `thm:qc-sparse` (J:1696–1698) now refers to the input lengths of
  `thm:qc-blocks`(e) up to constant factors. The shear keeps at most
  `O(n^2)` monomials per row and `O(k^2 log ell_k)`-bit coefficients.
- `cor:qc-feasible-output` (J:1882–1884, proof J:1926–1933):
  `L = O(k^3 d^2 log(k d varpi_k))` native and
  `O(k^3 d^2 [log(k d varpi_k) + k d])` explicit. The proof fixes `k > 3C`;
  then `L = O_k(d^2 log d)` native or `O_k(d^3)` explicit, and
  `d^k + 1 > phi(3k) L^C` eventually in both formats.

## Source contracts: status

This section supersedes the "unverified by Luna" status that
`evidence/authoring/contrast.md` gives for the items cleared below. That file
was not edited.

Cleared by Luna and now cited with locators:

- `BasuMohammadNezhad2024`, Forum Math. Sigma 12 (2024) e115, publisher
  version. Theorem 2.2 has the hypotheses `d >= 2`, closed bounded `A`, and
  continuous `f, g` with graphs of degree at most `d`, with
  `f^{-1}(0) ⊆ g^{-1}(0)`. It gives an integer `N <= (8d)^{2(n+7)}` with
  `|g|^N <= c|f|` and `log2 c <= tau d^{O(n^2)}`. Theorem 4.1 gives one-block
  QE degree `d^{O(k)}` and coefficient bits `tau d^{O(k)O(ell)}`. Cited at
  K:381 and K:387.
- `LuoZhang1999`, Comput. Optim. Appl. 13 (1999) 87–110, with the published
  metadata in the bibliography. The theorem was checked as Corollary 2 of the
  lawful 1997 report 97-122, pp. 6–7. It gives attainment for a feasible
  convex quadratic system with positive semidefinite objective and
  constraint Hessians and a finite infimum. Affine rows and split equalities
  are covered, and no compactness or Slater condition is needed. Cited as
  "Corollary 2, in the numbering of the 1997 report" at J:2384–2386 (epigraph
  attainment in `thm:qc-rational-infeasibility`) and J:2527–2528 (polyhedral
  case, alongside the attribution to `FrankWolfe1956` in
  `thm:qc-number-field-qp`).
- `SlotSteurerWiedmer2025`, arXiv v1, Corollary 1.2, already vetted as an
  objective-gap value-approximation result. Cited at K:33.

Still pending Luna verification (unchanged by this repair; listed separately
as Sol requested):

- Contracts used in proofs:
  - `MorganSommese1987` and `DedieuMalajovichShub2005`: isolated-root count
    with extra positive-dimensional components (`thm:qc-bezout`).
  - `NieRanestad2009`: generic count `2^s binom(n,s)`.
  - `Serre2008`: Hilbert irreducibility in density form.
  - `Rockafellar1970`: convex KKT with affine rows and strict nonlinear rows.
  - `KozlovTarasovKhachiyan1980`: exact rational convex QP.
  - `GroetschelLovaszSchrijver1988`: rational LP. The literature review now
    has a vetted GLS LP-output row (Theorem 6.4.12 / §6.5). No locator was
    added to J's two LP citations, because their use (a rational point of a
    possibly non-pointed polyhedron, or a feasibility decision) should be
    matched to that row at integration.
  - `KannanLenstraLovasz1988`: the KLL threshold in `thm:qc-kll`.
  - `vonzurGathenGerhard2013`: univariate exact arithmetic.
  - `BasuPollackRoy2006`: real-algebraic transfer.
  - `Davenport2000`: primes in progressions modulo 4.
  - `Neukirch1999`: Eisenstein, ramification, Hensel.
  - `BombieriGubler2006`: Weil-height conventions.
  - `Deimling1985`: Brouwer degree.
  - `Hoffman1952`: the explicit form is proved in the text.
- Attribution only:
  `Canny1990`, `GrigorievPasechnik2005`,
  `AdachiIwataNakatsukasaTakeda2017`, `GiesbrechtRoche2010`,
  `JiaChoiMourrainWang2011`, `LiangLiBai2013`, `JeyakumarLi2014`,
  `Lenstra2002`, `Rouillier1999`, `Kollar1999`,
  `FranekRatschanZgliczynski2016`, `JiaoPhamTuyen2025`, `Nesterov2025`,
  `Vavasis1990`, `DelPiaDeyMolinaro2017`, `BienstockDelPiaHildebrand2023`,
  `SafeyElDinZhi2010`, `FrankWolfe1956`.

Bibliography state: 30 keys cited by J and K are absent from both
`references.bib` and `evidence/literature.bib` at present. They are exactly
the pending keys above other than `KozlovTarasovKhachiyan1980`,
`GroetschelLovaszSchrijver1988` and `NieRanestad2009`, which are present in
`references.bib`. All 30 were cited before this repair, and the repair
introduced no new citation key. `LuoZhang1999` and `BasuMohammadNezhad2024`
now resolve.

## Cross-file labels

Newly referenced: `def:models-polynomial` (Section 01, the explicit
exponent-vector format) and `lem:separation` (Section 03, the separation
bound for the regularization paragraph). Both exist. All other external
labels are unchanged: `thm:exact-upper`, `thm:singleton-field`,
`cor:algebraic-three-quadrics`, `lem:convex-value`,
`def:models-representations`, `sec:constraints`, `sec:heights`,
`sec:fields-certificates`.

## Items outside these files

- Sol notes that Section 06:116–118 still calls an irrational coordinate's
  alternative a "shared arithmetic circuit" without the root-selection
  qualification. The root has commissioned that repair; it is not in J/K.
- The main-text summaries of J and K (Sections 00:773–777, 01:617–619,
  11:156–164) remain consistent with the repaired scopes.

## Points for the R2 review

Check the new statement and the necessity remark in `thm:qc-blocks`(d); the
rational constants and `C_frak` in `thm:qc-number-field-qp`; the two-format
lengths and the `k > 3C` thresholds; K's overview, subsection introduction,
Hesse sentence and regularization paragraph; the imported Basu–Mohammad-Nezhad
statements and their application with degree bound at least two; the
integer-valued `p`; the integer-bound rounding; the elimination statements;
and the treewidth bag for `k = 1`.

## Checks run

All checks were scoped to J and K. No experiments, mathematical scripts,
historical checks, project-wide checks, or CI inspection were run. The
mathematics was checked analytically, as recorded above.

1. Scratch compile outside the repository, in `/tmp/qc-repair-r1/`. A
   wrapper with the main preamble and `macros.tex` inputs only J and K, plus
   `\bibliography` pointing to the manuscript's `references.bib`. Commands:
   `pdflatex -interaction=nonstopmode -halt-on-error wrapper.tex`, then
   `bibtex wrapper`, then `pdflatex` twice more. All four runs exited 0 with
   no LaTeX errors. There is one overfull line of 0.24pt at J:191, in the
   unchanged `lem:qc-heights` proof. Unresolved references are only the
   cross-file labels listed above, all of which exist in the manuscript.
   bibtex reported exactly the 30 pending keys as missing.
2. Targeted `grep` over J and K for stale wording ("dense input length",
   `k>2C`, `omega_k\ge1`, "universal polynomial", "integral bounds",
   "eliminated penalty"): no matches remain.
3. Targeted `grep` over J and K for TODO/FIXME, "companion proof",
   "independently reviewed", and repository paths: none.
4. Targeted `grep` over `sections/` and `appendices/` to confirm that the
   newly referenced labels exist and to find main-text references to J and K.
