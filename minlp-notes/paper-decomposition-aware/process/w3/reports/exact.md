# W3 report: group `exact`

Files edited: `sections/exact.tex`, `sections/exact-localized.tex`,
`sections/appendix-localized.tex`, `sections/appendix-boundary.tex`.

## Summary of structural changes

- Section 6 now reads 6.1 Scaled data (`sec:exact-data`), 6.2 Stationary
  polytopes and rational height (new label `sec:exact-height`), 6.3 Acceptance
  and recovery (new label `sec:exact-accept`; ends with `rem:setgrowth` and the
  moved `rem:np`), 6.4 Exact output under point growth (new label
  `sec:exact-growth`), 6.5 Localized acceptance (`sec:localized`), 6.6
  Explicit polynomial factors (`sec:polynomial`).
- New introduction (Rewrite 9, adapted) and scope sentence (Rewrite 10).
- REC and EX are algorithm environments (`alg:rec`, `alg:ex`).
- `prop:accept` is stated with a denominator bound Omega' for OPT and any
  feasible set; Omega' = Omega for box QPs by `cor:height`(b).
- Corollary `cor:local` is now a statement about an explicit candidate rule
  (Definition `def:facecand`, "face candidate"), fully proved in Appendix B.1.
- Appendix B is one section "Exact output: deferred proofs" (new label
  `app:exact`) with subsections B.1 (`app:localized`) and B.2 (`app:boundary`).
  `appendix.tex` input order is unchanged (localized, then boundary).
- Appendix B.2 uses L_i := L for every coordinate (R4 M2) and cites
  `lem:commonmesh` (G2), (G4), (G5).

## 1. Adjudication

| id | verdict | reason | change |
|---|---|---|---|
| F8 | ACCEPTED | roadmap and scope were stale; rem:np belongs to Section 6 | New opening (Rewrite 9 with exact Theorem bound), scope "In this section, except in Section 6.6, F is a quadratic with rational data". rem:np copied to the end of 6.3 (as the conventions and the task specify, not 6.2). optsets must delete its copy (currently duplicate label). |
| F10 | MODIFIED | conventions fix the form: one acceptance proposition parameterized by a denominator bound, cited by Sections 7 and 8; the TU stationary-face argument has different constants and stays with the tu group | `prop:accept` restated for any feasible set with OPT of denominator <= Omega'. Height/snap for polytopes not merged (other groups' files). lem:cr-semiconcave / prop:tu-tight not in my files. |
| F11 | ACCEPTED (my part) | duplicated comparisons | rem:np keeps only the Section-6-specific comparison (explicit constants, box case, NP/coNP observation). Exclusion-box comparison (Neumaier) stays local to 6.5. related.tex already points to rem:np (front). |
| F12 | MODIFIED | renames in my files done per the conventions table | P=Delta H -> \hat H; gradient ell(x) deleted; ell_i everywhere; S -> \mathcal S. Rejected the part "Delta -> delta_F": the conventions reserve Delta for the Section 6 denominator. |
| F13 | ACCEPTED (my part) | terminology | App B uses "TRIAL (Algorithm alg:trial) with a common mesh", "CT with a common mesh"; "pruned-grid trials", "capped pruned-grid algorithm" removed. |
| F22 | ACCEPTED (my part) | ell(x) clashes with bounds | "with gradient ell(x)" deleted in 6.5. setting-growthcert is core's. |
| F29 | ACCEPTED (my part) | "rounder constants 22/15" was wrong | Sentence deleted; App B.2 uses (G2)'s 17/15 and states the radius 4.2 <= 5 explicitly as a weakening. |
| F39 | ACCEPTED (my part) | S1 needed a real pointer | 6.5 points to Section 11.6 (`sec:comp-localized`) and states what the experiments used. Remaining items are computation's. |
| F41 | ACCEPTED (my part) | notation | \hat H; ell_i. Section 7 renames not mine. |
| F42 | ACCEPTED (part d) | stale scope | Scope sentence and opening rewritten (see F8). Parts a-c are other groups'. |
| F49 | ACCEPTED (part a, my files) | terminology | see F13. |
| F57 | ACCEPTED (my part) | constants quoted inconsistently | App B.1 and B.2 cite `lem:commonmesh` (G2) (incl. 17/15), (G4) radius 4.2 (+1), (G5) cap; no restated (G1)-(G4) list; 7/8 and 22/15 removed. |
| F58 | ACCEPTED | P overloaded | Matrix renamed \hat H; I_C^+ = I_C cap P stated in eq:exact-constants. |
| F59 | ACCEPTED (my part) | S overloaded | \mathcal S for the optimal set; J_0, J_\partial for interior/active coordinates (Cor local, App B); vertex free set T -> J_v (T is the tree). |
| F61 | ACCEPTED (my part) | gamma overloaded | Smallest inward derivative lambda_A in 6.5, 6.6 and App B.2; B_gamma -> B_lambda; gamma_m -> c_m in lem:intcurv. |
| F63 | ACCEPTED (my part) | ell(x) | deleted. |
| F64 | ACCEPTED | roadmap/order | exact-localized is 6.5 (coordinator moved the input); opening and scope fixed. |
| F65 | ACCEPTED (my part) | hand-numbered algorithms | REC, EX as `algorithm` environments with labels alg:rec, alg:ex; App B cites alg:trial and lem:commonmesh. |
| F67 | MODIFIED | same as F10 | prop:accept parameterized; Section 6 keeps the box stationary-face lemma (conventions: TU details in appendix-tu). |
| F70 | ACCEPTED (my part) | local re-definition of set growth | thm:transfer cites eq:setgrowth (Def 3.2); rem:setgrowth says "has set growth with some constant g_S". |
| F72 | ACCEPTED (my part) | l_i | All l_i -> \ell_i in appendix-boundary (and appendix-localized). |
| F77 | ACCEPTED (my part) | S1 unreported | 6.5 keeps a short pointer to 11.6 with the numbers the computation paragraph reports. |
| F78 | ACCEPTED | dangling "(F)" | Proof rewritten; uses Prop prop:filter / Lemma commonmesh (x* in X^(j)). |
| F82 | ACCEPTED | rem:cf comparison wrong in general | "needs 2^{-q} <= g/(64n^2R^2), which is the weaker requirement when R^2 >= 2n^2"; both routes need 2^{-q} <= 1/(2 Omega^2). |
| F84 | ACCEPTED (no rename) | f_1, f_d are already indexed names | Added "for a computable function f_1 / f_d" in Thm exact, Cor poly, Thm boundary. |
| F91 | not applicable | the forward references listed are in setting.tex / grids.tex / recourse | no change in my files. |
| F92 | not applicable (my part unchanged) | Lemma 6.1 is the PD diagonal version and Rem heights already says "Hadamard's inequality for rows" | recourse handles Lemma 7.17. |
| F104 | ACCEPTED | stale scope | see F8. |
| F106 | ACCEPTED (my part) | unions-of-cells sentence removed from Section 6 | opening no longer mentions it. |
| F145 | MODIFIED | attribution added; locators changed | Before lem:statpoly: "The argument follows Vavasis [Vavasis1990] (see also [DelPiaDeyMolinaro2017]); we need its explicit constants." No "Section 2"/"Theorem 3" locators: the bib entry Vavasis1990 is the IPL paper (R7's "Sec. 2" refers to the TR) and the DPDM theorem number was not verified. Contesse cited at lem:unique-growth. Hadamard proof replaced by citation \cite[Theorem~7.8.1]{HornJohnson2013} (new bib entry, verified, below). |
| F146 | ACCEPTED (my part) | attribution of monotonicity tests | App B.2: Bernstein bounds \cite{Garloff1986}; "standard in interval global optimization \cite{Hansen1980,HansenWalster2004,ArayaTrombettoniNeveu2010}". limits/lbproduct parts are not mine. |
| F153 | ACCEPTED | = R1 M1 | see F8; 6.5 now precedes 6.6. |
| F154 | ACCEPTED (option 1) | Cor local proved only a property of x* | New Definition `def:facecand` (face candidate: copy y_j on integer and singleton coordinates; fix a continuous coordinate of J_+ at a bound of X_i contained in its narrowed interval; solve the stationarity equations of the rest). Cor local now states: at every stage with h_j <= h* that ends by filtering, the face candidate exists, equals x*, and passes Prop local; h* gains the term delta_X/6 (delta_X = distance from x* to the bounds it does not attain, >= 1/R) and the separate delta_C term is subsumed. Full proof in App B.1. Text states that experiment S1 used the incumbent-face rule, which the corollary does not cover. |
| F156 | ACCEPTED (my part) | variant unstated | core added lem:commonmesh; my files cite it. |
| F158 | ACCEPTED (my part) | "g exponentially small" says nothing | Replaced by "As noted after Definition def:growth, the lemma gives no bound on the condition number, which can be exponential in I." |
| F169 | ACCEPTED | conflated bounds | Opening: "exact output in f_1(p,kappa)poly(I) bit operations (Theorem thm:exact)". |
| F170 | MODIFIED | renames per conventions | \hat H, I_C^+ = I_C cap P, \mathcal S, J_+ instead of W in 6.5, J' instead of E in lem:snap. Rejected renaming R -> R_ht: the conventions reserve R for the Section 6 height (radius R_ij is core's). |
| F171 | ACCEPTED | "=" should be "<=" | log2(1/eps_S) <= poly(I) + max{0, log2(1/g_S)}. |
| F172 | ACCEPTED | L = 0 case | Proof: "If L=0, EX stops after one call of CT. Otherwise L >= 2/Delta"; the L >= 2/Delta fact is stated in 6.1. |
| F173 | ACCEPTED | = F82 | see F82. |
| F174 | ACCEPTED | undefined symbols | Cor poly proof uses Gamma_X 2^alpha, Gamma_F (now also clearing the L_i), common denominator 8 Gamma_F (Gamma_X 2^alpha)^d, |e_i|, |E| = O(dI). Prop lattice uses Gamma_F instead of Q_0 (Q is the corrected objective). |
| F175 | ACCEPTED | wording | "so g = 3 is a growth constant and kappa <= 4"; (c) "growth constant 1/2". |
| F176 | ACCEPTED | defects in Cor local proof | ell(x) deleted; dangling (F) gone; ell_i; H_{J0J0} >= 2gI proved inline for the mixed box; h* is finite whenever n >= 1 (a bracketed term always remains), so no +infinity case; log Gamma <= poly(I) + log kappa is proved in the stage count. |
| F179 | ACCEPTED (first option) | localization was used for L_i = 0 coordinates | App B.2: "every coordinate uses the single curvature bound L, that is, L_i := L for all i"; L = 0 handled (first stage exact, zero gap); proof uses (G4) for every coordinate. |
| F187 | ACCEPTED (my part) | label filter vs (C1) | core extended (C1) with a second alternative (w(J)=0, endpoints outside have m >= beta); Lemma labelfilter(i) now proves that removed intervals satisfy it. |
| F188 | ACCEPTED | 22/15 not needed | see F29. |
| F189 | ACCEPTED | L = 0 | "If L = 0, trial 2 succeeds at stage 0 with zero gap; assume L > 0." |
| F193 | ACCEPTED (my part) | clashes in prop:margin | function h -> chi, coefficient beta_i -> b_i, box [alpha_i, beta_i] -> [alpha_i, alpha_i'], residuals r_i -> rho_i (r is the half-width), F_n -> Phi_n; prop:weakcompl polynomial W -> Psi (W is a denominator). moments/limits parts not mine. |
| F194 | ACCEPTED | zero-gap output missing from Thm boundary(a) | (a) now lists the incumbent after a zero certified gap. |
| F195 | ACCEPTED (my part) | terminology | see F13; "does real work" is not in my files. |
| F198 | ACCEPTED (my part) | 2^{-50}..2^{-350} were the code's constant | 6.5 now says the thresholds 1/(Omega W) for the paper's constants range from about 2^{-315} to 2^{-21} on the E4 instances (n <= 6); verified with R8's script (21.3 to 315.0 bits). |
| F199 | ACCEPTED | off-by-one, inflated comparison | 6.5: "accepted 29 of 30 ... within five stages, whereas one CT run reaches the threshold of Prop accept with the constants of eq:exact-constants only after 51 to 73 stages on the five instances on which EX used the most stages, and the implementation of EX, which restarts for every q, used up to 542 stages", citing 11.6. |

Specific tasks from the coordinator, all done: roadmap/scope; rem:np moved;
notation (\hat H, \mathcal S, no ell(x), lambda_A, B_lambda, I_C, ell_i);
parameterized prop:accept; R1 M2 (explicit candidate rule, proved); R4 M2
(L_i := L); R8 sentences; R1 minors (thm:exact L=0, rem:cf, cor:poly symbols,
EX/thm:approx conflation, ex:polylimits, rem:setgrowth "<=", Vavasis
attribution at lem:statpoly); REC/EX algorithm environments.

## 2. Labels deleted or renamed

None deleted or renamed. New labels:
`sec:exact-height`, `sec:exact-accept`, `sec:exact-growth` (subsections 6.2-6.4),
`alg:rec`, `alg:ex`, `def:facecand` (face candidate), `app:exact` (Appendix B
section). `rem:np` now lives in `exact.tex` (end of 6.3).

## 3. Requests for other files

- **optsets**: delete Remark `rem:np` from `optsets.tex` (currently a duplicate
  label). Also `optsets.tex` defines `\label{eq:setgrowth}` a second time
  (line 13); Def 3.2 now owns it, so the local equation should go (F70); until
  then `thm:transfer` renders "set growth (9.1)".
- **computation** (11.6, `sec:comp-localized`): consider adding one sentence:
  "The face candidate of Definition~\ref{def:facecand}, which
  Corollary~\ref{cor:local} covers, accepted the same 29 instances with the
  same optimal values, within nine stages (0-based stage index at most 8)."
  Source: `process/w3/checks/exact-face-candidate-s1.py` (re-runs the S1 grid
  solves, about 3 s; it also reproduces the incumbent-face stages of
  `results/raw/S1_*.json`). If added, the script should move into
  `experiments/` (e.g. a `face_candidate` function in `localized.py`). Please
  also fill the 11.5 placeholders for the paper's constant with 21 to 315
  bits (R8's `r8_height_constants.py`: 21.3 to 315.0), which 6.5 now quotes.
- **recourse** (`recourse-balanced.tex` ~141 in the old version, Rewrite 16):
  if any text still says Theorem thm:exact uses "rational reconstruction", it
  should say "snapping recovery (Lemma~\ref{lem:snap})".
- **all**: Section 6 now says "point growth" (Def 3.2(a)) instead of
  "quadratic growth"; Section 6.5 is "Localized acceptance" and 6.6 is
  "Explicit polynomial factors" (labels unchanged).
- **core**: my files use `lem:commonmesh` items (G2) (including the 17/15
  witness bound), (G4) and (G5) exactly as currently stated in `growth.tex`;
  please keep that numbering. App B.2 Lemma labelfilter relies on the second
  alternative of (C1) as currently written in `grids.tex`.
- **coordinator**: add the BibTeX entry below.

## 4. New BibTeX entries

Verified: Crossref metadata for DOI 10.1017/CBO9781139020411 (Matrix
Analysis, 2nd ed., Horn and Johnson, Cambridge University Press, ISBN
9780521839402 / 9780521548236); Theorem 7.8.1 of the second edition is
Hadamard's determinant inequality for positive definite matrices (cited as
"[HJ, Theorem 7.8.1]" for exactly this statement in arXiv:2112.01462, whose
bibliography lists the 2013 second edition).

```bibtex
@book{HornJohnson2013,
  author    = {Horn, Roger A. and Johnson, Charles R.},
  title     = {Matrix Analysis},
  edition   = {2},
  publisher = {Cambridge University Press},
  address   = {Cambridge},
  year      = {2013},
  isbn      = {978-0-521-83940-2},
  doi       = {10.1017/CBO9781139020411}
}
```

## 5. Checks run (targeted, local; not CI)

- `latexmk -pdf -interaction=nonstopmode -outdir=build/exact main.tex`
  (several times; final run): no LaTeX errors, no overfull boxes from my four
  files. Remaining warnings from my files: undefined citation
  `HornJohnson2013` (new entry above). Other warnings (undefined `tab:scip`,
  duplicate `rem:np` and `eq:setgrowth`, overfull boxes in optsets and
  appendix-moments) belong to other groups. One intermediate run hit a
  transient `main.bbl` error caused by a concurrent `references.bib` edit
  (Werner2007); the next run was clean.
- `python3 process/w3/checks/exact-constants.py`: ALL PASS. It checks the
  numerical constants of the proofs in App B.1 and B.2 (integer-step bounds,
  3.6/5, 5.2/6 < 1, 5/5.2 >= 1/2, 1 + 10/10 <= 2, 4^{mu*} <= 32 kappa,
  patch margin), the identities and derivative claims of prop:margin
  (n = 1, 2, 3) and prop:weakcompl with sympy, and, on 389 random small mixed
  box QPs with a unique minimizer (exact oracle of `experiments/oracle.py`):
  x* in rho^{-1}Z with Delta | rho <= R, W <= Omega, delta_X >= 1/R and
  lambda_A >= 1/(Delta R).
- `python3 process/w3/checks/exact-face-candidate-s1.py`: on the 30 S1
  instances the face candidate of Def facecand is accepted on the same 29
  instances as the incumbent-face rule, with equal optimal values, at 0-based
  stage at most 8; the incumbent-face stages reproduce `results/raw` (at most
  4). The candidate assertion y_j in the narrowed box held at every stage.
- `python3 process/w2/checks/r8_height_constants.py` (R8's script): paper
  constant needs 21.3 to 315.0 bits on the E4 instances (used in 6.5).

## 6. Unresolved

- The experiments of Section 11 use the incumbent-face candidate, which
  Corollary cor:local does not cover; the text says so. Whether to switch
  `experiments/localized.py` to the proved face candidate is for the
  computation group (my check shows the same acceptance count).
- The S1 numbers quoted in 6.5 (29 of 30, five stages, 51 to 73, 542) must
  match what computation writes into the placeholders of 11.6.

## Verification (group `exact`, verifier)

Files verified and, where noted, edited: `sections/exact.tex`,
`sections/exact-localized.tex`, `sections/appendix-localized.tex`,
`sections/appendix-boundary.tex` (diffed against
`process/w3/sections-before-w3/`).

### V1. Adjudications

Every finding in `assign/exact.json` was checked against the current text.

- Confirmed as applied, correctly and completely: F8, F11, F13, F22, F29,
  F39 (my part), F41, F42(c, d), F49(a), F57, F58, F59, F61, F63, F64, F65,
  F70, F72, F77, F78, F82/F173, F84, F104, F106, F153, F154, F156, F158,
  F169, F171, F172, F174, F175, F176, F179, F187, F188, F189, F193 (my part),
  F194, F195, F198.
- MODIFIED or REJECTED parts that are justified: F10/F67 (CONVENTIONS fix the
  parameterized `prop:accept`, and Sections 7 and 8 do cite it with their own
  Omega'; checked in `constraints.tex`, `appendix-tu.tex`,
  `recourse-cuts.tex`, `appendix-recourse-cuts.tex` and
  `appendix-recourse-convex.tex`); F12 and F170 (Delta and R are reserved by
  CONVENTIONS); F145 (locators omitted: the `Vavasis1990` entry is the IPL
  paper, and the DPDM theorem number is unverified); F91 and F92 (nothing to
  change in these files).
- F199 was incomplete. Section 6.5 said "51 to 73 stages" (R8's script,
  threshold 1/(2 Omega W)). The rerun of the computation group gives 40 to
  72 (`experiments/results/summary.json`, S1
  `single_run_stages_lemma_range_top5 = [40, 72]`, threshold 1/(Omega W)),
  and Section 11.6 now says 40 to 72. **Fixed** in 6.5 (see V3).
- Cross-file requests in Section 3 of this report that are already done:
  `optsets.tex` no longer defines `rem:np` or `eq:setgrowth`. Each label now
  occurs once (grep), and `thm:transfer` cites Definition 3.2's equation.
  Section 11.5 now gives 21 to 315 bits for the paper's constant; this
  matches 6.5 and `E4_exact.csv` (`required_gap_bits_lemma` is 21.3 to 315.0
  over the 18 certified instances, and 48.5 and 50.9 for the two segment
  instances, so the range holds for all 20). The F67 sentence in
  `recourse-balanced.tex` ("rational reconstruction") is gone.

### V2. Mathematics checked line by line

- 6.1 to 6.4: scaled data (`\hat H` integral; L >= 2/Delta); Lemma
  `lem:statpoly` (a) to (c), including J_v as a subset of J_0 and of
  I_C^+, the Cramer step and Delta <= rho <= R; `cor:height` (including
  Delta | rho and the endpoints in rho^{-1}Z); `rem:heights` (the diagonal
  bound is at most both alternatives); `prop:accept` with Omega'; REC and
  `lem:snap` (1/Delta >= 1/R = 4n tau, phi(s) < 1/R, vertex argument);
  `thm:transfer` (tau^2/4 = 1/(64 n^2 R^2)); `rem:setgrowth` (the inequality
  with max{0, .}); `rem:np` (content kept from optsets; "OPT > t"
  certificates is the correct complement); `lem:unique-growth`; EX and the
  L = 0 paragraph (REC fixes every coordinate of a vertex, because
  u_i - l_i >= 1/Delta > tau); `thm:exact` (q* >= 1 since eps_S <= 1/2,
  largest q < 2q*, O(log q*) calls, thm:approx(b) with kappa >= kappa-bar,
  H_{J0J0} positive definite under uniqueness); `rem:cf` (the threshold
  comparison holds iff R^2 >= 2n^2).
- 6.6: `lem:intcurv`, `prop:lattice` (Gamma_F is the product of the
  denominators, a common denominator with O(I) bits), and `cor:poly` against
  the current bit-length paragraph of Appendix A (alpha = J + max|e_i| +
  |E| + mu K_mu, so |e_i|, |E| = O(dI) changes alpha by O(dI); the common
  denominator is 8 Gamma_F (Gamma_X 2^alpha)^d because d >= 2).
  `ex:polylimits` (a) to (c) were re-derived (the factorization
  (x - sqrt2)^2 (x + 2 sqrt2), F(1/2, 0) = 1/4 - 2^{-2^k-1}).
- 6.5 and B.1: `lem:node`, `prop:local`, the claim that y_j lies in the
  narrowed box, Definition `def:facecand`, and every step of the new proof of
  `cor:local` (the coordinate split; the cases i not in P, I_Z cap P (steps
  of length one up to distance 5, radius 3.6 + 1 <= 5), continuous P;
  J_+ = J_0 cup A; candidate = x*; mu_i >= (5/5.2) Gamma; the Schur
  complement; the stage count with delta_X >= 1/R and
  lambda_A >= 1/(Delta R)). Gamma > 0 whenever A is nonempty, because
  H_ii > 0 on A. h* is finite for n >= 1.
- B.2: L_i := L and the L = 0 case; Lemma `lem:labelfilter` (i), including
  the second alternative of (C1) as now stated in `grids.tex`, and (ii)
  (h_j + theta t <= 1/10 + 1/2 < 1, (17/1500) < 1; the extra filter keeps
  x* and the centers, so lem:commonmesh still applies); `lem:monotone`;
  `lem:patch`; Theorem `thm:boundary` (a) and (b) (4^{mu*} <= 32 kappa,
  2 C_3 r <= L/(4 * 4^{mu*}) <= g/32, lambda_A - 2 C_2 r >= lambda_A/2,
  phase accounting 2^{q*} <= 2 * 2^{mu*} A_*); `prop:margin` and
  `prop:weakcompl` after the renames (the identity, chi = (x_n + rho_n)/2,
  the diagonal bound 35/16, g = 9/64, kappa = 140/9, the denominator
  argument).

### V3. Fixes made by the verifier

1. `exact-localized.tex`, S1 paragraph: "51 to 73" -> "40 to 72" (to match
   Section 11.6 and the rerun); the long sentence is split; "neighbourhood"
   -> "neighborhood".
2. `exact-localized.tex` and `appendix-localized.tex`, Corollary `cor:local`:
   the reviser had redefined J_partial locally as
   {i in I_C cap P : x*_i at a bound}. Section 3 and the notation table
   reserve J_partial for *all* coordinates at a bound (integer coordinates
   included). The corollary now uses J_partial as defined in Section 3 and
   the subset A = J_partial cap I_C^+, which fits the lambda_A name. Gamma,
   h*, strict complementarity and the whole proof in B.1 use A. The statement
   now opens with "Let F have point growth with constant g at x*".
3. `appendix-boundary.tex`, Theorem `thm:boundary`(b): the same clash
   (J_partial := {i in I_C : ...}) is replaced by A = J_partial cap I_C in
   the statement and the proof.
4. `exact-localized.tex`, setup of 6.5: "every x with F(x) <= U lies in
   X^(j+1)" needs every earlier filtering threshold to be at least U. The
   text now says that the thresholds are values of feasible points and at
   least U, as in a trial, where the incumbent value never increases.
5. `appendix-localized.tex`: the inline argument for H_{J0J0} >= 2gI is
   replaced by a citation of Lemma `lem:growthcert`(b), which is now stated
   for mixed boxes. The positive length of X~_i for continuous i in P is now
   justified ("X_i does, and filtering replaces an interval of positive
   length by a hull of grid intervals of positive length"). The first use of
   CT in Appendix B now carries "(Algorithm~\ref{alg:ct})", as CONVENTIONS
   require.
6. `appendix-boundary.tex`: L must be nonnegative to be a valid curvature
   bound, so the assumption is now L >= max{0, max_i sup d_ii F}.
7. `exact.tex`, `rem:cf`: "Both routes also need 2^{-q} <= 1/(2 Omega^2)" ->
   "In both routes, 2^{-q} <= 1/(2 Omega^2) makes the recovered minimizer pass
   the acceptance test". The old wording called a sufficient condition
   necessary.

No labels were deleted or renamed by the verifier.

### V4. Checks run (targeted, local; not CI)

- `python3 process/w3/checks/exact-constants.py`: ALL PASS (0.8 s).
- `python3 process/w3/checks/exact-face-candidate-s1.py`: the face candidate
  and the incumbent-face rule each accept 29 of 30 S1 instances with equal
  values; largest 0-based stages 8 and 4 (2.5 s).
- New `python3 process/w3/checks/exact-verify-corlocal.py`: an independent
  exact implementation of TRIAL with a common mesh (brute-force grids,
  Fractions). It uses random mixed box QPs (n = 2, 3, up to two integer
  coordinates) with a unique minimizer (`experiments/oracle.py`) and a growth
  constant certified by Lemma `lem:growthcert`(a). It runs the trial with
  theta = 2^{-mu}, mu = max{2, ceil(log4(8 kappa))}. At every stage it
  checks (G2), (G4), and that y_j lies in the narrowed box. When the face
  candidate passes the test, it checks that the candidate is optimal
  (soundness). At the first two stages with h_j <= h* (Gamma from spectral
  norms rounded up), it checks every claim of `cor:local`: narrowed
  singletons, J_+ = J_0 cup A, candidate = x*, and that the test passes.
  Result: 120 instances checked, ALL PASS. Coverage: J_0 nonempty on 36,
  A nonempty on 73, I_Z cap P nonempty on 45, a coordinate outside P on 77;
  the first stage with h_j <= h* ranged from 4 to 14.
- `latexmk -pdf -interaction=nonstopmode -outdir=build/exact-verify
  main.tex`: final run exit 0, no LaTeX errors, no overfull boxes, no
  undefined references, no "??" in the PDF text. A first attempt failed on
  a `main.out` that another process was writing at the same moment in the
  paper directory, and an intermediate run had a bibtex error and two
  undefined citations (ChenEtAl2006, CyganEtAl2015, page 120). None of these
  came from my files.

### V5. Remaining

- The S1 counts that Section 6.5 quotes (29 of 30, five stages, 40 to 72,
  542) must stay in sync with Section 11.6 if computation reruns S1 again.
- Section 11.6 reports only the incumbent-face rule. The face candidate that
  Corollary `cor:local` covers is checked only in
  `process/w3/checks/exact-face-candidate-s1.py` (29 of 30, stage <= 8).
  `experiments/localized.py` now contains `face_candidate` and
  `first_face_acceptance`, so computation could report it in one sentence
  (request in Section 3 above).
- Minor overloads were left unchanged because they are local and defined
  where used: omega_j (B.1) next to omega_0 (common denominator in
  `prop:margin`, B.2); rho (height denominator) next to rho_i (residuals in
  `prop:margin`); and J for the free set (REC, `def:facecand`) next to the
  stage limit J of TRIAL.

## Verification, second pass (group `exact`, verifier)

Independent re-verification of the four files after the first verification
pass (files unchanged between the passes). Diffed against
`process/w3/sections-before-w3/`.

### W1. Adjudications

All 52 findings of `assign/exact.json` were re-read (full issue and fix text)
and checked against the current files. Every ACCEPTED fix is present and
correct. The MODIFIED/REJECTED parts are justified: F10/F67 (CONVENTIONS fix
the parameterized `prop:accept`), F12/F170 (Delta and R reserved by
CONVENTIONS; the free set is J by CONVENTIONS, vertex free set J_v), F145
(no locators: the `Vavasis1990` package in `literature/` is unread, and DPDM's
"Theorem 3" is the numbering of the 2014 arXiv text in
`research-20260927/nonconvex-prior-sources/`, not verified for the journal
version), F91/F92 (nothing in these files). Two adjudications needed a
follow-up in the text (see W3): F199/F39/F77 (Section 11.6 now reports the
face candidate, so 6.5 must too) and F84 (thm:boundary reused the name f_d of
cor:poly for a different function).

No label was removed; the new labels are `sec:exact-height`,
`sec:exact-accept`, `sec:exact-growth`, `alg:rec`, `alg:ex`, `def:facecand`,
`app:exact`, `rem:np` (moved). No label in `sections/*.tex` is defined twice.

### W2. Mathematics re-derived

Every changed statement and proof, line by line: scaled data (L >= 2/Delta),
`lem:statpoly` (a)-(c) (Cramer step, J_v in J_0 cap I_C^+, Delta <= rho <= R),
`cor:height`, `rem:heights` (the diagonal bound is below both alternatives,
which now carry max{1,.}), `prop:accept` with Omega', REC and `lem:snap`
(1/Delta >= 1/R = 4 n tau > 2 tau, phi(s) <= 3/(8R)), `thm:transfer`,
`rem:setgrowth`, `rem:np` ("OPT > t" is the right complement of the
NP-complete question "OPT <= t"), `lem:unique-growth`, EX with the L = 0
paragraph, `thm:exact` (q* >= 1, largest q < 2q*, monotonicity of f in kappa,
H_{J0J0} positive definite), `rem:cf` (comparison iff R^2 >= 2n^2),
`lem:intcurv`, `prop:lattice`, `cor:poly`, `ex:polylimits` (a)-(c); in 6.5
the setup paragraph, `lem:node`, `prop:local`, y_j in the narrowed box,
`def:facecand`, `cor:local` and its full proof in B.1 (coordinate split,
cases i not in P / I_Z cap P / continuous P, J_+ = J_0 cup A, candidate = x*,
mu_i >= (5/5.2) Gamma with Gamma > 0, Schur complement, stage count); in B.2
L_i := L, `lem:labelfilter` (i) including (C1) in the combined case where the
regular filter and the extra filter both shrink the interval, (ii),
`lem:monotone`, `lem:patch`, the procedure, `thm:boundary` (a) and (b),
`prop:margin` (identity, b_i, Phi_n, diagonal bound 35/16, g = 9/64,
kappa = 140/9, lambda_A = 3a_n/2, the denominator argument) and
`prop:weakcompl`.

Gaps found and fixed are listed in W3. No error was found in the statements.

### W3. Fixes made in the second pass

1. `exact-localized.tex`, S1 paragraph: Section 11.6 now tests both
   candidates (face candidate accepted on 29 of 30 instances within nine
   stages, incumbent rule within five; `experiments/results/summary.json`:
   `face_candidate_accepted = 29`, `face_candidate_max_stage_index_0based =
   8`, `max_first_stage_index_0based = 4`). Section 6.5 reported only the
   incumbent rule and said "the candidate was" the incumbent rule. It now
   reports the face candidate (which `cor:local` covers) first and the
   incumbent rule as the uncovered rule, with the same numbers as 11.6.
2. `exact.tex`, `rem:cf`: "Snapping recovery needs 2^{-q} <= g/(64n^2R^2)"
   stated a sufficient condition as a requirement; now "succeeds once ...
   (Lemma~\ref{lem:snap})".
3. `exact.tex`, proof of `cor:poly`: "Gamma_F now also clears the L_i" left
   open whether the redefined Gamma_F still has O(dI) bits. The proof now
   states that the L_i lie in (Gamma_F Gamma_X^{d-2})^{-1} Z (coefficients
   of d_ii F are integer multiples of coefficients of F; range endpoints are
   products of at most d-2 box endpoints), so 8 times a correction
   L_i w^2/8 has a denominator dividing Gamma_F (Gamma_X 2^alpha)^d because
   d >= 2. Gamma_F keeps its Appendix A meaning.
4. `appendix-boundary.tex`, opening: "We use TRIAL ... under point growth"
   suggested that the procedure assumes growth (part (a) holds without
   assumptions). Now "We use TRIAL ... Under point growth with
   8 kappa theta^2 <= 1, (G4) places ...".
5. `appendix-boundary.tex`, `prop:margin`: omega_0 ("a common denominator of
   the data") clashed with omega_j = sqrt(n kappa) h_j of Appendix B.1 at
   j = 0. Replaced by Gamma_X = 2^{n+2}, the product of the endpoint
   denominators (the symbol of Appendix A); the proof cites Appendix A for
   the node denominators Gamma_X 2^{j + mu K} under h_j = s 2^{-j}. The bound
   becomes j + mu K >= 4*2^n - 2 - log2 Gamma_X = 4*2^n - n - 4.
6. `appendix-boundary.tex`, `thm:boundary`(b): the computable function is
   now f_d' (cor:poly's f_d is a different function; F84). The proof calls
   the per-trial cost A_*, bounds it by a computable function of (p, kappa)
   times poly(I + B_lambda), and ends "which proves (b)" after the
   O(sqrt(kappa) A_*) phase bound, so the sqrt(kappa) factor is visibly
   absorbed. The L = 0 case now says that the phase accounting applies with
   mu_* = 2 and j_* = 0 (it previously gave no cost).

No labels were deleted or renamed; no requests for other files arise from
these fixes.

### W4. Checks run (targeted, local; not CI)

- `python3 process/w3/checks/exact-constants.py`: ALL PASS (0.7 s).
- `python3 process/w3/checks/exact-verify-corlocal.py`: 120 instances
  checked, ALL PASS (first stage with h_j <= h* from 4 to 14).
- New `python3 process/w3/checks/exact-verify-denominators.py`: ALL PASS.
  It checks, on random explicit polynomials (exact fractions), that the L_i
  of `lem:intcurv` lie in (Gamma_F Gamma_X^{d-2})^{-1} Z and that L_i w^2
  has a denominator dividing Gamma_F (Gamma_X 2^a)^d (fix 3); on
  [0,1/2]^m with h_j = s 2^{-j} and theta = 2^{-mu}, that graded-grid nodes
  of stage j have denominators dividing Gamma_X 2^{j + mu K} (fix 5); and the
  `rem:cf` comparison (iff R^2 >= 2n^2).
- `latexmk -pdf -interaction=nonstopmode -outdir=build/exact-verify main.tex`
  (three runs). The run after the main edits exited 0 with no errors, no
  warnings and no overfull boxes. The final run (after a line reflow in
  6.5) exited 12 because BibTeX read a `main.aux` that lacked `\bibdata`
  while other processes were compiling in the paper directory and editing
  `references.bib` and `appendix-growth.tex` at the same time; the final
  `build/exact-verify/main.log` has no errors, no warnings (no undefined or
  multiply defined references or citations) and no overfull boxes, and
  `pdftotext` of the whole PDF shows no "??".

### W5. Remaining (minor, not changed)

- The lemma title "Integer-label filter" keeps the word "label" (grids.tex
  refers to it by that name); "Integer-node filter" would match the
  CONVENTIONS terminology but needs the same change in `grids.tex` (core).
- sigma is the convexity margin in `lem:patch` and sigma_mu, while
  CONVENTIONS reserve sigma(t) for the grid step; the step function is not
  used in Appendix B.2, so the local meaning is unambiguous. rho_i
  (residuals in `prop:margin`) and rho (height denominator, B.1) are in
  different subsections.
- Locators for Vavasis1990 and DelPiaDeyMolinaro2017 remain omitted (see
  W1).
- Section 6.5 and Section 11.6 quote the same S1 numbers (29 of 30; nine and
  five stages; 40 to 72; 542); they must change together if S1 is rerun.
