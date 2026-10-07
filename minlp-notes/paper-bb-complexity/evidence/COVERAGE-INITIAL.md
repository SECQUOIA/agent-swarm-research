# Initial claim coverage map

Date: 2026-10-05. Author: lead writing architect (Opus). Companion to
[ARCHITECTURE.md](ARCHITECTURE.md), whose Section 8 defines the planned
locations (§2–§15 are manuscript sections; A–K are appendices). This is the
initial map: it records each claim's hypotheses, source, proof status in the
source, reviews, planned location, literature dependence and evidence. Later
stages add the manuscript labels, Luna's literature verdicts and the review
resolutions. Nothing here was re-proved or rerun for this file except the
checks listed in ARCHITECTURE.md Section 6.3.

## Legend

**Sources.** Paths relative to the repository root.

| Abbrev. | File |
|---|---|
| CN | `research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md` |
| FE | `research-20260928b/bb-complexity/spatial-face-exact/face-exact-node-complexity.md` |
| CP | `research-20260928b/bb-complexity/cutoff-propagation/cutoff-propagation.md` |
| CB | `research-20260928b/bb-complexity/branching-competitiveness/competitive-branching.md` |
| ND | `research-20260928b/bb-complexity/branching-competitiveness/n-dimensional.md` |
| SO | `research-20260928b/bb-complexity/branching-competitiveness/separable-omega.md` |
| RB | `research-20260928b/bb-complexity/robust-branching-points/robust-branching.md` |
| IC | `research-20260928b/bb-complexity/integer-core/relaxation-intrinsic-bounds.md` |
| SR | `research-20260928b/bb-complexity/sparse-regression/phase-transition.md` |
| SR2 | `research-20260928b/bb-complexity/sparse-regression/stronger-relaxations/thresholds.md` |
| BL | `research-20260928b/bb-complexity/binary-least-squares/certification-thresholds.md` |
| SV | `research-20260928b/bb-complexity/solver-validation/scip-node-exponents.md` |
| MB | `research-20260928b/bb-complexity/minlplib-branching/branching-point-study.md` |
| RL | `research-20260929/rlct/rlct-node-complexity.md` |
| ST | `research-20260929/theory-face-exact/face-exact-exponential.md` |
| DC | `research-20260929/theory-decomposition/decomposition-certificates.md` |
| EA, AM, CU | `research-20260929/theory-decomposition/{extension-adaptive,adaptive-matching,covering-upper-half}.md` |
| RLB, RC | `research-20260929/theory-robust-lb/{robust-lower-bound,robust-chains}.md` |
| KC | `research-20260929/theory-consistency/consistency-relaxations.md` |
| SS | `research-20260929/computation/scaling-study.md` |

**Reviews.** `R8:` means `research-20260928b/reviews/`, `R9:` means
`research-20260929/reviews/`.

| Abbrev. | File |
|---|---|
| sbb | R8: `spatial-bb-review.md` (scout theorems, Fixes 1–2) |
| sc, scr | R8: `spatial-constrained-review.md`, `spatial-constrained-recheck.md` |
| fe8, fe8r | R8: `face-exact-review.md`, `face-exact-recheck.md` |
| cut, cutr | R8: `cutoff-review.md`, `cutoff-recheck.md` |
| cA, cB | R8: `closing-audit-a.md`, `closing-audit-b.md` |
| comp, compr | R8: `competitive-review.md`, `competitive-recheck.md` |
| sep | R8: `separable-omega-review.md` |
| rob | R8: `robust-branching-review.md` |
| ic, icr, bbc | R8: `integer-core-review.md`, `integer-core-recheck.md`, `bb-conflict-review.md` |
| se, sh, pwe, srr | R8: `sparse-easy-review.md`, `sparse-hard-review.md`, `pwe-verification.md`, `sparse-recheck.md` |
| s2, s2r | R8: `stronger-relaxations-review.md`, `stronger-relaxations-recheck.md` |
| me, mh, mr | R8: `mimo-easy-review.md`, `mimo-hard-review.md`, `mimo-recheck.md` |
| lean | `formal/topics/33-competitive-branching/reviews/statement-review.md` |
| rl, rlr, rlr2 | R9: `rlct-review.md`, `rlct-recheck.md`, `rlct-recheck2.md` |
| st, str | R9: `face-exact-review.md`, `face-exact-recheck.md` (single-tree note) |
| dec, decr, decnd | R9: `decomposition-review.md`, `decomposition-recheck.md`, `decomposition-nondyadic-check.md` with `-confirm-r1..r3` |
| cmp | R9: `computation-review.md` |

**Status in source.** P proved; P* proved, but later edits were not
rechecked by the review chain; S sketch only; C conjecture or open; H
heuristic; E empirical; I imported input (cited, not proved); W withdrawn
(false); K known in substance (credit, do not claim).

**Action.** keep; restate (scope or wording changes listed); repair (proof
task); lit (Luna must verify); audit (parallel math audit to confirm); open
(list in open problems, no claim); drop; excl (excluded from this paper).

## §2 Model and runs to certificates

| ID | Claim (key hypotheses) | Source | Status | Reviews | Location | Lit | Action |
|---|---|---|---|---|---|---|---|
| M1 | Node model: `R_B ⊇ F ∩ B`, `f_B ≤ f` on `F ∩ B`, `LB(B) = inf_{R_B} f_B`; certificate = partition of `X0` into boxes with `LB ≥ f* - eps`; `N_eps` least size | CN 1.2–1.3 | P | sc | §2 | — | keep; unify with FE `N_cov`, ST `N_cert` (cover versions) |
| M2 | Relative tolerance reduces to absolute with `eps := max(eps_abs, eps_rel |f*|)`; tolerance-accepted incumbents redefine `f*` | CN 1.2 | P | sbb §1.1 | §2 remark | — | keep |
| M3 | Gap hypotheses `(G^pt)`, `(G^LB)`, `(T)`, `(U_c)`, `(U^q)`, `(EB)`, `(Lip)`; (EB) from MFCQ by Robinson plus compactness | CN 1.4 | P/I | sc | §2 | Robinson 1976; Bonnans–Shapiro 2.87 | keep; rename `tau -> c_U`, `kappa -> c_E` |
| M4 | Which relaxations satisfy what: uniform alphaBB, secants of concave terms, alphaBB of constraints (tube), McCormick satisfies `(U^q_{|c|/2})` but no `(G^pt)` | CN 1.5, Lemma 1.1; FE Lemma 2.5 | P | sc, fe8 | §2 | McCormick 1976 | keep |
| M5 | **Theorem I (spatial)**: leaves plus per-round frame pieces form a family with disjoint interiors covering `X0`; `alpha`-valid under `(G^pt)` (under `(G^LB)` without R-rel); tube dichotomy under `(T)` without R-inf; `|P_F| ≤ #leaves + 2n #(R-rel rounds)` | CN Lemma 2.1 | P (corrected after sbb Fix 1) | sbb, sc, scr | §2, full proof | — | keep |
| M6 | Merged frames of several rounds can violate (V) (10–151 violations in an OBBT test); per-round frames needed | CN §2 remarks | E (review test) | sbb §1.3 | §2 remark | — | keep as remark citing the counterexample mechanism, not the review |
| M7 | If every R-rel round solves a relaxation, `|P_F| ≤ (2n+1)` times relaxations solved plus inherited-bound leaves | CN §2 remarks | P | sc | §2 | — | keep |
| M8 | Objective-cutoff propagation is neither R-inf nor R-rel; it empties the root of `t^2 - 2t^4` without a relaxation | CN §2; sbb §1.3 | P | sbb | §2, pointer to §10 | — | keep |
| M9 | Face-exact run lemma: leaves plus pieces form a valid cover; relaxations pointwise below termwise McCormick covered; RLT, SDP, lifted constraints, child bounds, lifted branching not covered | FE Lemma 1.2 | P | fe8 | §2/§7 | — | keep; merge into Theorem I |
| M10 | Single-tree run lemma with certifying ancestor boxes: leaves plus `2n` per tightening round `≥ N_cert` | ST Lemma 1.2 | P | st | §2 | — | merge into Theorem I |

## §3 Covering law

| ID | Claim (key hypotheses) | Source | Status | Reviews | Location | Lit | Action |
|---|---|---|---|---|---|---|---|
| C1 | Covering lower bound `|P| ≥ 2^-n cN_inf(E(eta), 2 sqrt((eps+eta)/alpha))` for `alpha`-valid families | CN Thm 4.6 | P | sc | §3 | Munos; Bachoc et al. | keep |
| C2 | `liminf log N_eps / log(1/eps) ≥ dim_low(X*)/2` | CN Cor 4.7(b) | P | sc | §3 | — | keep |
| C3 | Localization: non-pruned level-`j` cube has a feasible `y ∈ E(Lambda s_j^2 - eps)` within one cell (needs `(U_c)`, (EB), (Lip)) | CN Lemma 6.1 | P | sc | §3 | Perevozchikov; Munos (level-by-level counts) | keep |
| C4 | Bisection versus any `alpha`-valid family, with `|P_F|` | CN Thm 6.2 | P | sc | §3 | Hansen–Jaumard–Lu (1D) | keep |
| C5 | **Theorem II**: `2^-n Phi_alpha ≤ N_eps ≤ |T_bis| ≤ 1 + 2^n[2^{n j_0} + 15^n max(1, ceil(2 sqrt(Lambda/alpha)))^n J Phi_alpha]` (cube `X0`, `(G^LB)`, `(U_c)`, (EB), (Lip)) | CN Thm 6.3 | P | sc, scr | §3, full proof | Bachoc et al. (Lipschitz analogue) | keep; state constants exponential in `n` |
| C6 | `Phi_alpha` within `2^n` of the running supremum over `eta ≥ eps` of a Munos-type profile | CN Remark 6.3a(i) | P (constants tightened) | scr | §3 | Munos 2011 (near-optimality dimension, constants) | keep |
| C7 | Single-scale covering does not determine `N_eps` with uniform constants (`f_K` family, `alpha = 32`, `N_eps ≥ K/2`) | CN Remark 6.3a(ii) | P | scr | §3 | — | keep |
| C8 | Under (QG), bisection bounded by `sum_j N_j(X*)` | CN Thm 6.4 | P | sc | §3 | — | keep |
| C9 | Exponent equals half the box-counting dimension of `X*` under (QG); finite `X*`: between 1 and `O(log 1/eps)` | CN Cor 6.5; §8.1 | P | sc | §3 | Neumaier 2004 §15 (heuristic) | restate with (QG) explicit (ARCHITECTURE 6.1(2)) |
| C10 | Bisection log factor attained: `f = 2|y - a| - (y - a)^2`, `a = 1/3`, certificate of 2 for every `eps`, bisection `Theta(log 1/eps)` | CN Example 3.4 | P | sbb §4 | §3 | — | keep; note nonsmooth interior minimizer |
| C11 | Bisection need not pay `log(1/eps)` when the minimizer has sparse binary digits (`liminf |T_bis|/log(1/eps) = 0`) | CN §3 correction | P | sbb §6 | §3 remark | — | keep |
| C12 | `O(1)` certificate at a sharp constrained minimizer for all `eps ≥ 0` (needs vertex-vanishing `(U^q)`, (EB), (Lip)) | CN Prop 6.8 | P | sc | §3 | Kannan–Barton (first order suffices with trivial critical cone) | keep |
| C13 | Bisection `Omega(log 1/eps)` when some coordinate of `z*` is rational with odd denominator | CN Remark 6.9 | P | sc | §3 | — | keep |
| C14 | Binary widest-side bisection: same bounds with modified factors | CN Remark 6.10 | P | sc | §3 remark | — | keep |
| C15 | Same-relaxation tightening cannot change the exponent and saves at most `O(log 1/eps)`; tightening with other information can change everything | CN Cor 8.1 | P | sc | §3 | companion `paper-adaptive-obbt` | keep |
| C16 | Scout Theorem A (`F = X0`, bisection within `4^n (sqrt(kappa n) + 2)^n J |P|`) | CN Thm 3.3 | P | sbb | §3 remark | — | subsumed by C4; remark only |
| C17 | Scout Theorem C under (QD); corrected sufficient condition for (QD) (`K = max(2, nM)`, needs `m ≥ 0` beyond `X0`); ratio of constants not `e^{O(n)}` | CN Thm 3.5, Lemma 3.6, Remark 3.7 | P | sbb §5 | App B | — | subsumed by I4 for `C^{1,1}`; keep the counterexamples to the scout's claims only as remarks |

## §4 Integral laws, strata and regular instances

| ID | Claim (key hypotheses) | Source | Status | Reviews | Location | Lit | Action |
|---|---|---|---|---|---|---|---|
| I1 | Arcsine bound `|P| ≥ (alpha n/pi^2)^(n/2) integral (m+eps)^(-n/2)`; sharp for `n = 1`; anisotropic and low-rank forms | CN Thm 3.1 + remarks | P | sbb | §4 | Bachoc et al. (Lipschitz analogue) | keep |
| I2 | Face lower bound `|P| ≥ (alpha d/pi^2)^(d/2) I_F(eps)` for every face of dimension `d ≥ 1` | RL Thm 3.1 | P | rl | §4 | — | keep |
| I3 | Projection to a face with fatness (descent lemma, `m ≥ 0` on `X0` only) | RL Lemma 3.2 | P | rl | §4 | — | keep |
| I4 | Bisection bound without (QD): `|T_bis| ≤ 1 + 2^n + 2^n[2·6^n sum_F Lambda_2^(d/2) I_F + sum_v N_v]`, `N_v ≤ min(J, J_v)` (`(U^q)`, gradient Lipschitz) | RL Thm 3.3 | P | rl, rlr, rlr2 | §4 | — | keep; also applies to McCormick (ARCHITECTURE 6.2(5)) |
| I5 | Optimal vertices add no log factor | RL Lemma 3.3a | P | rlr | §4 | — | keep |
| I6 | **Theorem III(a)**: `max(1, max_F (alpha d/pi^2)^(d/2) I_F) ≤ N_eps ≤ |T_bis| ≤ C_0 + C_1 sum_F I_F` (`C^{1,1}`, `(G^LB)`, `(U^q)`) | RL Cor 3.4 | P | rlr | §4, full proof | — | keep; constants depend on `n, alpha, alpha', L_grad, s0, min m(v)` |
| I7 | (QD) at interior minimizers (local version); CN Lemma 3.6 needs `m ≥ 0` beyond `X0`; (QD) fails at boundary minimizers with nonzero gradient | RL Lemma 3.5 | P | rl | App B | — | keep |
| I8 | Faces dominated when `m ≥ 0` on a neighbourhood of `X0` | RL Prop 3.6 | P | rl | §4 | — | keep |
| I9 | Key lemma: `integral_{S∩B∩A} q_B^(-d/2) ≤ C_{n,d} sum_I M^I(S; A∩B)` | CN Lemma 4.1 | P | sc | §4 statement, App A proof | Federer 3.2.20; Evans–Gariepy | keep |
| I10 | Two-point constant gives local multiplicity one; global count from reach | CN Lemma 4.2 + Federer remark | P/I | sc, scr | App A | Federer 1959 Thm 4.18(2) | keep |
| I11 | Graphs of bounded Hessian have two-point constant `≥ 1/K_2` | CN Lemma 4.3 | P | sc | App A | — | keep |
| I12 | Multiplicity cannot be dropped; bounded curvature is not enough (comb, infinitely many segments, connected spiral) | CN Prop 4.4 | P | sc, scr | §4 statement, App A proof | — | keep |
| I13 | Stratified integral lower bound (global and local forms; `d = n` case) | CN Thm 4.5 | P | sc | §4 | — | keep |
| I14 | Sum over strata | CN Cor 4.7(a) | P | sc | §4 | — | keep |
| I15 | Integral upper bound and two-sided characterization under stratified regularity (R1)–(R3) | CN Thms 6.6, 6.7 | P | sc | App B; remark in §4 | — | keep in appendix |
| I16 | **Theorem IV(b)**: KKT with LICQ, SC, SOSC, active strata `d ≥ 1`: `c_a (alpha/M_L)^(d/2) log(1/eps) ≤ N_eps ≤ |T_bis| ≤ C_a log(1/eps)`; unique vertex minimizer `N_eps ≤ C_b` for all `eps ≥ 0`; description independence | CN Thm 7.1(a)(b) | P | sc, scr | §4 statement, App B proof | Neumaier §15 (heuristic "n replaced by n - a"); Kannan–Barton | repair citation: QG from SOSC by a classical source, not the repository's cluster-free note |
| I17 | **Theorem IV(c)**: Morse–Bott manifold of dimension `p` with reach `tau_M`: `Theta(H^p(X*) eps^(-p/2))` | CN Thm 7.2 | P | sc | §4 | Niyogi–Smale–Weinberger Lemma 5.3 | keep |
| I18 | Quadratic forms on spheres and balls (`p = k - 1`); degenerate `-|y|^2 + y_2^4` gives `eps^(-1/4)` | CN Example 7.3 | P | sc, scr | §4 example | — | keep |
| I19 | Symmetry: orbit dimension at points of `X*` is a lower bound for `dim_box X*`; maximum orbit dimension over `F` is not; exact symmetry-breaking constraints restore a lower exponent (worked example) | CN §8.1 | P | sc, scr | §4 | — | keep; "gain in practice not examined" |
| I20 | Active constraints: the stratum carrying `X*` sets the exponent; the full-dimensional integral can be half an order too small | CN §8.2; Table 9.2 | P + E | sc | §4 | — | keep |

## §5 Singular minima and the order of the relaxation

| ID | Claim (key hypotheses) | Source | Status | Reviews | Location | Lit | Action |
|---|---|---|---|---|---|---|---|
| S1 | Laplace and volume asymptotics on compact semianalytic sets; box faces qualify | RL Lemma 2.1 | I (hypotheses checked) | rl | App C | Lin 2017; Karamata (Bingham–Goldie–Teugels) | lit (theorem numbering of the version cited) |
| S2 | `I_a(eps)` from the RLCT in all three regimes | RL Lemma 2.2 | P | rl | §5 | — | keep |
| S3 | Newton-polyhedron bound and equality for nonnegative `h`; orthant version at boundary zeros proved | RL Lemma 2.3 | I + P | rl, rlr, rlr2 | App C | Lin 2017 Thm 1.3, Props 3.4, 4.3, 4.5, 4.12; Varchenko 1976 | lit |
| S4 | Interior minimizers: `lambda ≤ n/2`, with equality iff all minimizers nondegenerate (then finitely many, `theta = 1`) | RL Lemma 2.4 | P | rl | §5 | — | keep |
| S5 | **Theorem III(b)**: `c kappa* ≤ N_eps ≤ |T_bis| ≤ C kappa*`, `kappa* = max_F kappa_F` | RL Thm 4.1 | P (given S1) | rl, rlr | §5 | — | keep |
| S6 | Interior minimizers or `m ≥ 0` near `X0`: exponent `n/2 - lambda`; explicit constants under (i) | RL Cor 4.2 | P | rl | §5 | — | keep |
| S7 | Boundary counterexample: `x(1-x) + y^4 + z^4 + w^4`, predicted `eps^(-1/4)`, true `eps^(-3/4)` | RL Example 4.3 | P + E | rl (proposed), rlr | §5 | Kannan–Barton Cor 4 (fixed-width precedent of the face mechanism) | keep |
| S8 | Faces with `lambda_F = d/2`, `theta_F ≥ 2`: no governing instance known | RL Remark 4.1a | C (corner case sketched) | rlr2 | §15 open | — | open |
| S9 | Worked RLCTs: `x^2 y^2` `(1/2, 2)`; cusp `(5/12, 1)` with exponent `7/12`; `x^2 y^2 + z^4`; `x^2 + y^4`; coordinates matter | RL §5, Table 5.1 | P + E | rl | §5 table, App C derivations | Lin Remark 4.13 | keep |
| S10 | Reduced-rank regression, true rank 0: exponent `H(M+N)/2 - lambda_AW` | RL Prop 6.1 | P given I (Aoyagi–Watanabe via Drton–Plummer) | rl | §5 | Aoyagi–Watanabe 2005; Drton–Plummer 2017 | lit; do not tabulate rows `0 < r < H` |
| S11 | Noisy scalar toy: `N_eps ≍ eps^(-1/2)(1 + log(1/max(eps, delta^2)))` uniformly in `delta` | RL Prop 6.2 | P + E | rl | §5 | — | keep |
| S12 | Noisy two-regime behaviour in singular models | RL Conj 6.3 | S | — | §15 open | — | open |
| S13 | First-order gaps: covering form; bisection; `Theta(eps^(-n/2))` at nondegenerate minima as a lower bound for every tree; Morse–Bott `Theta(eps^(-(n+p)/2))`; integral form with a log | CN Thm 8.2 | P ((a),(e) known in substance) | sc, scr | §5 statement, App B proof | Du–Kearfott (upper estimates); Bachoc et al. | restate: credit (a),(e) |
| S14 | Order-`k` covering law, two-sided within `log(1/eps)` | RL Thm 7.1 | P | rl | §5 | Wechsung et al. (fixed-width scale law) | keep |
| S15 | Fatness only at scale `sqrt(eta)`; volume law for `k ≤ 2`; for `k > 2` the exponent lies in `[(n/k - lambda)_+, (n - 2 lambda)/k]` | RL Prop 7.2 | P | rl | §5 | Neumaier heuristic | keep |
| S16 | Order `k ≥ q` removes polynomial growth at Łojasiewicz order `q`; Morse–Bott `Theta(eps^(-p/k))`; same `lambda`, different exponents for `k = 3, 4` | RL Prop 7.3 | P ((b) reuses CN 7.2 as a sketch) | rl | §5, App C | Kannan–Barton Remark 4; Du–Kearfott; Kearfott–Du 1992; Bubeck et al. Example 3 | audit (b); credit sufficiency direction |
| S17 | Certified Lipschitz complexity of analytic functions has exponent `d - lambda` | RL Remark 7.4 | P | rl | §5 remark | Bachoc et al. Thm 3 | lit; keep as remark |

## §6 Constraint-gap schemes

| ID | Claim (key hypotheses) | Source | Status | Reviews | Location | Lit | Action |
|---|---|---|---|---|---|---|---|
| G1 | Modelling convention: exactly kept convex constraints belong to `P_ex` | CN §5 | — | sc | §6 | — | keep |
| G2 | Tube dichotomy: `v(z) > beta q_C(z)` or `f(z) - alpha q_C(z) ≥ f* - eps` | CN Lemma 5.1 | P | sc | §6 | — | keep |
| G3 | Infeasible-side covering bound `|P| ≥ 2^-n cN_inf(W(eps, nu), 2 sqrt(nu/beta))` | CN Thm 5.2 | P | sc | §6 | Kannan–Barton 2017 §3.2 (mechanism, upper estimates) | keep; credit |
| G4 | Flat optimal segment: isotropic loosening `Theta(eps^(-1/2))`; anisotropic loosening 3 leaves; exact propagation of the constraint gives 1 node | CN Example 5.3 | P + E | sc | §6 | — | keep |
| G5 | Lagrangian transfer under outward descent (covering form), `alpha_eff = mu_0 beta/(12 c_1)`; one-directional | CN Thm 5.4 | P | sc | §6, App D | — | keep |
| G6 | (OD) near KKT points with LICQ and `P_ex` polyhedral near `z*` | CN Lemma 5.5 | P (polyhedral); S (nonlinear exact constraints) | sc | App D | — | restate: polyhedral only |
| G7 | Integral form via a shift map | CN Prop 5.6 | P | sc | App D | — | keep |
| G8 | Constraint-gap schemes need `Omega(log 1/eps)` at KKT points with a relaxed active constraint, objective relaxed exactly | CN Thm 5.7; Thm 7.1(c) | P | sc | §6 | — | keep |
| G9 | Exact propagation of original constraints can remove the effect on flat strata; curved strata open | CN Remark 5.8; Open 3 | P/C | sc | §6, §15 | — | keep, open |

## §7 Face-exact relaxations

| ID | Claim (key hypotheses) | Source | Status | Reviews | Location | Lit | Action |
|---|---|---|---|---|---|---|---|
| F1 | McCormick gap formulas; zero iff a coordinate at a bound; `|c| d_i d_j ≤ Gamma ≤ |c| min(d_i w_j, d_j w_i)`; `≤ (|c|/2)(a_i + a_j)` | FE Lemma 2.1 | P/K | fe8 | §7 | McCormick 1976; Al-Khayyal–Falk 1983 | credit formulas |
| F2 | Gap-zero sets: joint envelope zero on a face iff `phi|_face` affine; termwise zero iff fixed coordinates form a vertex cover of `G` | FE Lemma 2.2 | P | fe8 | §7 | — | keep |
| F3 | Mixed-partial lower bound for joint multilinear envelopes | FE Lemma 2.3 | P | fe8 | §7 | — | keep |
| F4 | Chord bound in concave directions (alphaBB-type along chords) | FE Lemma 2.4 | P | fe8 | §7 | — | keep |
| F5 | Upper bounds: termwise `alpha'_T = max_i sum_j |c_ij|/2`; joint envelope `alpha'` from the Hessian | FE Lemma 2.5 | P | fe8 | §7 | Bompadre–Mitsos (second-order convergence) | keep |
| F6 | Gap graph (2.1), transversality, gap-nondegeneracy | FE Defs 2.6–2.8 | — | fe8 | §7 | — | rename `tau(V,E) -> vartheta(V,E)` |
| F7 | McCormick certificate integral: per-box integral of `Gamma^(-sigma)` finite iff `sigma < 1`; matching bound within `log^(2k)`; one log necessary on sharp instances | FE Lemma 3.1, Thm 3.2, Cor 3.3 | P | fe8 | App E; remark in §7 | Bachoc et al. (log loss analogue) | keep in appendix |
| F8 | Matching-slice bound along concave directions | FE Thm 3.4 | P | fe8 | §7 | — | keep |
| F9 | `Omega(log 1/eps)` at a smooth interior minimizer with an active bilinear term | FE Cor 3.5 | P | fe8 | §7 | — | keep |
| F10 | Flat strata: `N_cov ≥ vartheta(V,E)(alpha/((p+1)^2(eps+eta)))^(p/2) H^p(S)` | FE Thm 3.6 | P | fe8 | §7 | Minkowski–Radon | keep |
| F11 | `vartheta ≥ delta`; `delta > 0` iff transversal; `p = 1` formula; `p ≥ 2` gap-nondegenerate does not imply transversal | FE Lemma 3.7 | P | fe8 | §7 | — | keep |
| F12 | Curved transversal strata (hypothesis (H)) and its `C^1` criterion | FE Thm 3.8, Lemma 3.9 | P | fe8 | §7 | — | keep |
| F13 | Near-optimal cubes: exponent equals the fractional vertex cover number `tau*(G)`, attained; `tau* ≤ n/2` | FE Prop 3.10, Cor 3.11 | P | fe8 | §7 | Tutte (fractional perfect matching) | keep |
| F14 | Aligned strata with quadratic growth: via a constraint (RLT product removes it) and with box constraints only, `N_cov ≥ 1/(2 sqrt eps)`, `Theta(eps^(-1/2))` | FE Example 3.12 | P | fe8 (counterexample A), fe8r | §7 | — | keep |
| F15 | Tilted stratum: `(1/2) sqrt(theta/eps) ≤ N_eps ≤ (1/2) sqrt(theta/eps) + 2` | FE Prop 3.13 | P + E | fe8 | §7 | — | keep |
| F16 | Curved non-transversal surface: `N_cov ≥ 0.6148/(2 eps(1 + ln(1/(2eps))))`, all other tools `O(eps^(-3/4))` (Theorem 3.6 with `p = 2` at most `0.471 eps^(-3/4)`) | FE Prop 3.14 | P (due to fe8r; verified by cB) | fe8r, cB | §7 statement, App E proof | credit the construction to the development, not to an external source | keep; optional precision on `E` in step (d)2 per cB |
| F17 | Convex `g` affine on a segment has constant directional derivatives | FE Lemma 4.1 | P/K | fe8 | §7 | Rockafellar | credit |
| F18 | Optimal segments lie in concave or flat directions; transverse growth rates affine along flat ones | FE Thm 4.2 | P | fe8 | §7 | — | keep |
| F19 | Rank condition (R) makes interior optimal strata transversal | FE Cor 4.3 | P (matching fix) | fe8 | §7 | — | keep |
| F20 | 2D: a full aligned optimal segment gives a 2-box certificate for every convex `g` | FE Thm 4.4 | P | fe8 | §7 statement, App E proof | — | keep |
| F21 | Faces fixing star centres give `2^|K|` orthant certificates | FE Thm 4.5 | P | fe8 | §7, App E | — | keep |
| F22 | The star condition cannot be dropped: `Theta(1/eps)` on `|X1 - X2| + (X1 - X2) y` | FE Prop 4.7 | P (upper bound by fe8; exact certification by fe8r) | fe8, fe8r | §7, App E | — | keep |
| F23 | `F = X0`: `N_eps` bounded iff an exact certificate exists; no exact certificate with sublinear growth along a feasible concave direction | FE Prop 4.6 | P (polyhedral `Q` open) | fe8 | §7 | Al-Khayyal–Sherali; Shectman–Sahinidis (finite termination, not examined) | keep; lit |
| F24 | 2D dichotomy | FE Conj 4.8 | C | — | §15 | — | open |
| F25 | Bisection under second-order schemes: (a) under (QD); (b) `O(eps^(-p/2))` at sharp strata | FE Thm 5.1 | P | fe8 | §7 | — | (a) replaced by I4 for `C^{1,1}` `f`; keep (b) |
| F26 | Balanced widest-side rules within constants of bisection | FE Prop 5.2 | P | fe8 | §7 | — | keep |
| F27 | **Convergence order does not determine node counts**: McCormick and alphaBB with equal order and prefactor have `N_eps = 2` versus `Theta(eps^(-1/2))`; a first-order face-exact scheme also has `N_eps = 2` | FE Thm 6.1 | P | fe8 | §7 | Wechsung's thesis via Kannan–Barton p. 2 (first-order sufficiency at nondifferentiable minima) | keep; credit |
| F28 | Characterizations by the optimal set or by the lower-bound tools | FE Conj 7.1, 7.1' | W | fe8, fe8r | §7 remark | — | record as false |
| F29 | Does adding row-slice bounds restore a characterization? | FE Question 7.1'' | C | — | §15 | — | open |

## §8 Dimension at treewidth one

| ID | Claim (key hypotheses) | Source | Status | Reviews | Location | Lit | Action |
|---|---|---|---|---|---|---|---|
| D1 | Path family facts (`c = 0`): unique minimizer `0`, `m ≥ (1 - kappa - b)|x|^2`, (Q_2) with `r = 1`, convexity region | ST Lemma 1.1 | P | st | §8 | — | keep |
| D2 | Centre-volume lemma: `|P| ≥ 1/nu` with `nu = sup prod(1 - s_i)` over admissible `s` | ST Lemma 2.1 | P | st (adversarial box search) | §8, full proof | FE Prop 3.10 (same witness) | keep |
| D3 | One-variable inequality for `rho ≤ rho_max ≈ 1.99055` | ST Lemma 3.1 | P (threshold computed numerically) | st | §8 | — | repair: rigorous threshold `rho ≤ 1.99` (Sol) |
| D4 | **Theorem VI(a)**: `|P| ≥ (1 + 1/S)^n exp(-lambda_S(1 + eps/(b r^2)))`; for every `rho`, `exp((n - 1 - eps'')/(rho + 2))` | ST Thm 1 | P | st, str | §8 | Neumaier; Wechsung et al. (estimates); Basu et al., Dey–Shah, Cheng–Basu (MILP, ties) | keep; frame as relaxation-class statement |
| D5 | PROGRAM family: `N_cert ≥ (5/3)^n exp(-(5/9)(1 + 1.25 eps/r^2)) ≥ 0.574 (5/3)^n` (`eps ≤ 1e-4`, `r = 1`) | ST Cor 1.3 | P | st | §8 | — | keep (checked here, ARCHITECTURE 6.3) |
| D6 | Remarks: holds for the convex member; scale `sqrt(eps/b)`; tolerance up to `b r^2 n`; local minimizers; base ceiling `1 + 1/sqrt 2`; loss in the covering step | ST §3 remarks | P (other graphs: S) | st, str | §8 | — | keep; "other graphs" as sketch only (drop or label) |
| D7 | Per-factor convex envelopes (PROGRAM factorization): `c 1.205^n` | ST Thm 2, Lemma 4.1 | P (base from a floating-point 1-D maximization) | st | App F; mention in §8 | — | repair or qualify base (Sol, low priority) |
| D8 | Vertex covers at `x*` and a valid cube of half-side `sqrt(eps/(b(n-1)))` | ST Prop 5.1 | P | st | §8 remark | — | keep |
| D9 | Orthant boxes: two exactly valid, frustrated orthants lose `b^2 W^2/(4D)` | ST Prop 5.2 | P + E | st | §8 | — | keep |
| D10 | `log(1/eps)` factor with base 1.072 under (M^+) | ST Prop 5.3 | P | st | App F | — | keep in appendix |
| D11 | `c 2^n` and `c' beta^n log(1/eps)` | ST Conj 5.4 | C | — | §15 | — | open |
| D12 | Dyadic refinement `≤ 1 + (2^n - 1) J V_n (sqrt(tau/mu0) + sqrt n)^n`, per-variable factor 16.5–19.9; binary bisection no worse | ST Prop 5.5 | P | st | §8 | — | keep |
| D13 | Per-factor alphaBB centre-volume bases 1.33–1.52 | ST Prop 6.1 | P (bases numerical) | st | App F | — | keep in appendix |
| D14 | Chordal split of a positive definite path Hessian into PSD `2x2` blocks | ST Lemma 9.1 | P/K | st, str | §8 | Griewank–Toint 1984 Thm 4; Agler et al. 1988; Vandenberghe–Andersen 2015 | credit |
| D15 | Clique-wise PSD relaxation is exact for the convex member (one leaf) | ST Consequence A | P + E | str | §8 | Waki et al. 2006 | keep |
| D16 | A split factorization removes Theorem 2's mechanism near `x*` | ST Consequence B | P/K | str | §8 | Griewank–Toint (local convexification) | credit |
| D17 | Split envelopes need exponentially many leaves outside the convex region? | ST §9.3 | C | — | §15 | — | open |
| D18 | SCIP default is outside the class (minor separator); counts with and without | ST §7.4, §8 | E | st | §14 | SCIP `sepa_minor` | keep as evidence |

## §9 Decomposition contrast

| ID | Claim (key hypotheses) | Source | Status | Reviews | Location | Lit | Action |
|---|---|---|---|---|---|---|---|
| K1 | Decomposition certificate: cells and affine minorants on separators, leaf covers of bags, (CM), (LC); size | DC Def 1.2 | — | dec | §9 | — | keep |
| K2 | DP margin identity `m = sum_t g_t` | DC Lemma 1.1 | P | dec | §9 | — | keep |
| K3 | Validity; pairs that only touch may be omitted | DC Lemma 1.3 + remark | P | dec, decnd (remark) | §9 | — | keep |
| K4 | Chain inequality (virtual boxes) | DC Lemma 1.4 | P | dec | §9 | — | keep; Figure 4 |
| K5 | Unfolding: the root bound is a Lagrangian relaxation of the copy constraints | DC Lemma 1.5 | P | dec | §9 | — | keep |
| K6 | Fixed-slope algorithm; Berenguel et al. as precursor for one shared variable | DC §1.5 | — | decr §4 | §9 remark | Berenguel et al. JOGO 2013 | lit |
| K7 | Integer separator variables: lemmas unchanged | DC §1.6 | P (remark) | dec | §9 remark | — | keep or drop for space |
| K8 | Single-tree alphaBB integral bound `0.068 sqrt(n)(2e/pi)^(n/2) log(0.2/(n eps))` | DC Cor 2.1 | P | dec, decr | App F | — | keep |
| K9 | Bag lemma (integral form) | DC Lemma 2.2 | P | dec | App F | — | keep (used for Theorem 4.1(c)) |
| K10 | Width lower bounds: `exp(Omega(w))` above `pi/(4e)`; flat blocks; covering on bag projections | DC Props 2.3, 2.4, Thm 2.5 | P | dec | — | Zhang–Sun; ETH obstruction | excl (one-sentence remark at most) |
| K11 | Constant child minorants need `≥ |lambda*|/(6 sqrt(M_F eps))` cells | DC Prop 2.6 | P (child of the root, 1D separator); S (deeper) | dec | §9 | Robertson–Cheng–Scott 2025 (first-order copy error) | restate scope |
| K12 | Shell partitions; telescoping identity for slopes | DC Lemmas 3.1, 3.2 | P | dec | App F | — | keep |
| K13 | Worst case `(C n/eps)^{O(w)}` with zero slopes | DC Thm 3.3 | P/K | dec | §9 remark | Zhang–Sun 2022 Cor 1; Bienstock–Muñoz 2018 | credit; no novelty claim |
| K14 | **Theorem VI(b)**: certificate of size `2|T|(4/theta)^(tw+1)(log2(s0/h) + 2)` under (QG), (L^{1,1}), (U^q), (T1)–(T3); inexact centre and multipliers allowed | DC Thm 3.4, Remark 3.5 | P* (`x̂ ∈ X0` fix of §8.1 not rechecked) | dec, decr | §9 statement, App F proof | none found (LA C2) | audit; state as existence result centred at `x*` |
| K15 | Copy drift above the `theta` threshold accumulates along the chain | DC Remark 3.6 | E | dec | §9 remark | — | keep as observed |
| K16 | Two-sided covering characterization for decomposition certificates | DC Conj 3.7 | C | — | — | — | excl (partly addressed in EA, CU) |
| K17 | **Theorem VI(d)**: separation ratio `≥ 3e-10 (2e/pi)^(n/2)/sqrt(n)` for `n ≥ 3`, `eps ≤ 1e-4` (alphaBB); `c (5/3)^n/(n log(n/eps))` for McCormick; decomposition lower bound `0.2778 (n-1) log(1 + 0.6/eps)` | DC Thm 4.1 | P* (base-rounding fix not rechecked) | dec, decr | §9, full proof | Basu et al.; Dey–Shah; Cheng–Basu (MILP with ties); Dechter–Mateescu (discrete) | audit; keep `(2e/pi)^(n/2)`, never a rounded base |
| K18 | Crossovers: `n = 29` (proved single-tree bound against computed certificates, `eps = 1e-6`), `n = 49` proved against proved; toy bisection exceeds the certificate at `n = 9` | DC §4 scope | E/P | dec | §9 | — | keep as calibration of the qualitative nature |
| K19 | Factorization dependence: balanced split removes the proved mechanism; toy growth 2.3–2.5 per variable unproved | DC §4.1 | P/E/C | dec | §9 | — | keep; open part to §15 |
| K20 | No lower bound uniform over functional splits for relaxations exact at factor minima; measure form | DC Obs 4.2 | P* (scope fix not rechecked) | decr | §9 | Vorob'ev 1962; Lasserre 2006 | audit; credit measure form |
| K21 | Adaptive algorithms without `x*` (LS, GR), level-synchronous lower bound | EA Thm A.5, Prop A.6; AM Thm 2 | P | R9 adaptive reviews | — | — | excl (state that finding certificates without `x*` is outside scope) |
| K22 | Graded exact split and covering upper half | CU | P (partial) | R9 covering reviews | — | — | excl |
| K23 | Split-robust lower bounds (tiny bases); balanced split gives `n`-independent covers on uniform chains | RLB Thm 4.3; RC Thm A.2, C.3 | P | R9 robust reviews | — | — | excl |
| K24 | Consistency relaxations (gap identity, tree sandwich, kinks) | KC | P | R9 consistency reviews | — | — | excl |

## §10 Objective-cutoff propagation

| ID | Claim (key hypotheses) | Source | Status | Reviews | Location | Lit | Action |
|---|---|---|---|---|---|---|---|
| R1 | Representation DAG, revise operators, runs, hull consistency | CP §1.1 | — | cut | §10 | Benhamou et al. 1999 | keep |
| R2 | Greatest hull-consistent box; runs keep it; fair exact runs converge | CP Lemma 1.1 | P/K | cut | §10 | Belotti–Cafieri–Lee–Liberti (greatest fixed point) | credit |
| R3 | HC4 forward and backward steps are run steps; their fair limit is `Z*` | CP §1.1 | P | cut | App G | — | keep |
| R4 | Monotonicity, closedness, `Z ⊆ Z0(Pi_x Z)` (constant-node caveat) | CP Lemma 1.2 | P | cut, cA | App G | — | keep |
| R5 | `pi_cD` is a node bound: `F_lo ≤ pi ≤ pi(C, y) ≤ f(y)`; runs remove only points with `pi(C, y) > c` | CP Def 1.3, Prop 1.4 | P | cut | §10 | — | keep |
| R6 | Hybrid leaf-and-piece family; propagation phases merge into one frame (chain-minimum argument; no incumbent monotonicity) | CP Lemma 2.1 | P (corrected; verified) | cut, cutr, cA | §10 statement, App G proof | — | keep |
| R7 | Transfer principle `(Π ⇒ V_beta)` | CP Thm 2.2 | P | cut | §10 | — | keep |
| R8 | No representation-free lower bound (`abs` node trick) | CP Prop 2.3 | P/K (folklore) | cut | §10 | Neumaier p. 29 (`x - x` example) | credit |
| R9 | Fixed point of flat sums: `Z* ≠ ∅` implies `Phi_fs(Z') ≤ c`; equality form for flat separable sums | CP Thm 3.1 | P + E (450 random instances; review 200) | cut, cutr | §10 statement, App G proof | Araya et al. 2010 (single use; monotonicity) | keep |
| R10 | Chains and trees of binary sums | CP Remark 3.2 | P | cut | App G | — | keep |
| R11 | One-sided representations are exact | CP Cor 3.3 | P | cut | §10 | — | keep |
| R12 | Dichotomy at a stationary point (one-sided or first-order loss) | CP Remark 3.4 | P | cut | §10 | — | keep |
| R13 | Separable identity; loss is cross-coordinate | CP Cor 3.5 | P | cut | §10 | Neumaier p. 40 (separable reduction); Domes–Neumaier | keep |
| R14 | Box-likeness in lifted coordinates | CP Prop 3.6 | P | cut | §10 | — | keep |
| R15 | Examples: `t^2 - 2t^4`, `nondeg1s`, `linediag`, `rot_kappa`, `nd2` | CP Examples 3.7 | P | cut | §10 | — | keep |
| R16 | `eps`-independent node count under local exactness (idealized propagation) | CP Thm 3.8 | P/K (principle known) | cut | §10 | Du–Kearfott p. 9; Wechsung et al. p. 8 | credit; state idealization |
| R17 | `Theta(eps^(-1/2))` rounds iff some base has cancelling term derivatives | CP Heuristic 3.8a | H | cutr, cA | §10 remark (labelled heuristic) | — | keep as observation |
| R18 | HC4 needs `≥ (pi/8 - o(1)) a eps^(-1/2)` rounds on `s^2 - 2as + a^2` | CP Prop 3.9 | P | cut | §10, App G | Vu–Schichl–Sam-Haroud; Faltings (non-termination in general) | keep |
| R19 | `O(log log(1/eps))` rounds for the lifted form `u - 2u^2`, `u = t^2` | CP Prop 3.10 | P | cut | §10 | — | keep |
| R20 | Bounded rounds keep the exponent when some base has cancellation | CP Conj 3.11 | C (one undecided numerical case) | — | §15 | — | open |
| R21 | Witness lemma `pi(C, y) ≤ Phi_full(U')`; general DAG form | CP Lemma 4.1, Remark 4.1a | P | cut, cutr, cA | §10 | — | keep |
| R22 | Fixed point gains at most one term's width over forward evaluation | CP Cor 4.2 | P | cut | §10 | Moore single-use theorem | keep |
| R23 | Rotated quadratic: diagonal chord `O(eps/a)` | CP Example 4.3 | P | cut | §10 | — | keep |
| R24 | First-order loss; CND and ND1 | CP Lemma 4.4 | P | cut | §10 | — | keep |
| R25 | CND localizes propagation removals at vertices; `alpha_F = D0/(2 n s0)` | CP Thm 5.1 | P | cut | §10 | — | keep |
| R26 | Two-sided localization | CP Prop 5.1a | P | cutr | §10 | — | keep |
| R27 | **Theorem VII**: (V)-based lower bounds survive with `alpha_eff = min(alpha, alpha_F)` for every hybrid run | CP Thm 5.2 | P | cut | §10 | none found (CP §8) | keep |
| R28 | `linediag` constants (`D0 = 2.352`, `alpha_F = 0.140`) | CP Example 5.3 | P + E | cut | §10 example | — | keep |
| R29 | Under ND1, `log(1/eps)` survives at isolated minima | CP Thm 5.4 | P | cut | §10 | — | keep |
| R30 | Face localization cannot be strengthened to vertices (`iso2` strip) | CP §5 | P + E | cut | §10 remark | — | keep |
| R31 | Transversal optimal curves keep `Omega(eps^(-1/2))` under ND1 | CP Thm 5.5 | P | cut | §10 | — | keep |
| R32 | Face-type loss for `p ≥ 3` | CP Remark 5.6 | C | — | §15 | — | open |
| R33 | Same `f`, same relaxation: 1 node or `Omega(eps^(-1/2))` depending only on the DAG | CP §6 table | P + E | cut | §10 Table 3 | — | keep |
| R34 | Joint constraint propagation excluded (counterexample with `F = {x ≥ 1/2}`) | CP §2 | P | cutr, cA | §10 | — | keep |
| R35 | Schichl–Markót–Neumaier's order-1 statement: holds in node-count form for flat sums with first-order loss; fails for one-sided representations | CP §8 | — (literature reading via a delegated reader) | cut | §1, §10 | SMN 2014 preprint and journal version | lit before any wording |

## §11 Branching rules

| ID | Claim (key hypotheses) | Source | Status | Reviews | Location | Lit | Action |
|---|---|---|---|---|---|---|---|
| B1 | Information models I0, I1 (germ of `f` at the relaxation minimizer), I_inf; competitive ratio against `T_opt = 2 N_guill - 1` | CB §1.4 | — | comp, compr | §11 | — | keep; germ caveat |
| B2 | 1D structure: validity iff `r ≤ rho(c)`, minimizers are proximal points, `rho` 1-Lipschitz, certificates are `rho`-nets | CB Prop 1 | P | comp | §11 | — | keep |
| B3 | **1D theorem**: `R_min` uses at most 3 interior splits per certificate interval and `T ≤ 8N - 9` | CB Thm 1, Lemmas 1–2 | P (Lean 4 formalization, statement review) | comp, compr, lean | §11, full proof | Hansen–Jaumard–Lu 1991 (Lipschitz precedent) | keep; Lean mention per root decision |
| B4 | Inexact minimizers: `T ≤ 8 N(eps - 2delta) - 9`; stronger form open | CB Cor 1 | P (corrected; edge case `N = 1`) | comp, compr | §11 | — | keep; open part to §15 |
| B5 | Arbitrary node order and incumbents within `g < eps`: `T ≤ 8 N(eps - g) - 9` | CB §4.1 | P | comp | §11 remark | — | keep |
| B6 | `N_eps = 2` implies `T ≤ 5` | CB Prop 2 | P (proof due to review) | comp, compr | §11 | — | keep |
| B7 | Worst ratio of `R_min` lies in `[11/5, 4)` (exact instance with `N = 3`, `T = 11`) | CB §4.2 | P | comp | §11 | — | keep |
| B8 | Oblivious rules: ratio `≥ (2 n log_36(alpha/(9eps)) + 1)/(2^(n+1) - 1)` | CB Thm 2 | P (script corrected) | comp | §11 | — | keep |
| B9 | Fixed clamped convex combinations `R_{mu,beta} ≠ R_min` need order `log(1/eps)` nodes on one instance with `N_eps = 2`; table of solver-like parameters | CB Prop 4 | P (exact checks) | comp | §11, App H | Speakman–Lee Table 1; Belotti et al. 2009 | lit (parameter values); keep |
| B10 | SCIP 10.0.2 default (midpull 0.75 scaled below relative width 0.5 with global bounds; clamp 0.2 with local bounds) needs order `log(1/eps)` on `2 alpha |y - 3/238|` | CB Prop 4' | P | compr (source `branch.c` v10.0.2) | §11, App H | SCIP source/documentation | keep; it is a model statement, not a SCIP performance claim |
| B11 | Every I1 rule has ratio `≥ 5/3` (deterministic) and `≥ 4/3` (randomized) on piecewise-quadratic classes | CB Thm 3 | P (exact rational instances) | comp, compr | §11, App H | — | restate: non-analytic classes |
| B12 | Full information makes 1D trivial | CB Prop 0 | P | comp | §11 remark | — | keep |
| B13 | In `n ≥ 2` only the "if" half of the radius criterion survives | ND §2.1 | P (examples) | compr | §11 remark | — | keep |
| B14 | Splitting all coordinates at the minimizer (`multi`) is not competitive (`f = x^2` on `[0,1]^2`) | ND Thm N3 | P | compr | §11, App H | — | keep |
| B15 | `N_guill ≤ (2N_eps - 1)^n`; `N_guill ≤ 1 + C_n log(1/eps) N_eps`; BSP bounds (2D `2N - 1`; `O(N^((n+1)/3))`) | ND §4 | P (self-contained parts); I (BSP, abstracts only) | compr | §11 remark | Berman–DasGupta–Muthukrishnan 2002; Hershberger–Suri–Tóth 2005 | keep self-contained parts; BSP only if lit verifies |
| B16 | Every deterministic I1 rule (with corner germs) has ratio `≥ 7/3` on separable convex instances with `N_eps = 2`; randomized `(7 - 4/n)/3` | SO Thm C, Lemma 6.1 | P (verified `n = 2..40`) | sep, cA | §11, App H | — | restate: node-local, incumbent `f* = 0` |
| B17 | Iterated ambiguity: ratio `≥ (2G(n) + 1)/3`, `G(2..6) = 3, 5, 9, 15, 25`; analytic `max_i N_i ≥ (2^(n+1) - n - 3)/(n - 1)`; order `2^(n+2)/(3n)` | SO Thm C' | P + computer-assisted DP (`G(6)` from cA) | sep, cA | §11, App H | Yao's principle | restate per ARCHITECTURE 6.2(7) |
| B18 | `omega` uses `2^(n+1) - 1` nodes on `A_n` and on a tie-free variant, `N_eps = 2` | SO Prop 6.2 | P | cA | §11 | — | keep |
| B19 | `N_eps` is not a function of the 1D certificate sizes (log factor off in both directions on two families) | SO Prop D | P | sep | App H remark | — | keep as remark |
| B20 | Phase Lemma; `omega ≤ 112 N_opt` with one sharp coordinate; `n - 1` sharp coordinates | SO Thms A, B | P (B for `n - 1`: S) | sep | — | — | excl |
| B21 | Is `omega` `C_n`-competitive? | CB Conj 1; SO §7 | C | — | §15 | — | open |
| B22 | Oblivious rules on the McCormick kink family: expected counts over random kinks `≥ beta sqrt(|c|/(8eps))` | FE Thm 5.3 | P | fe8 | §11 | DDM (averaging over families, different rule class) | keep |
| B23 | Kink family: relaxation minimizers lie on the face; unclamped point 3 nodes; clamp bounded off `K_beta` with blow-up near it; incumbent branching 3 nodes (ties to `x`) | FE Prop 5.4 | P (corrected after fe8; tie rule after fe8r) | fe8, fe8r, cB | §11, App H | Shectman–Sahinidis; Tawarmalani–Sahinidis p. 243 (BARON) | keep; tie-rule and point-test caveats |
| B24 | Clamp misses the face on an uncountable null Cantor set; at `a = 1/6`, `beta = 1/5`: `≥ 0.0745 eps^(-1/2)` nodes against `N_eps = 2`; no uniform rate on the whole set | FE Prop 5.5 | P (construction due to fe8; exact counts by fe8r, cB) | fe8, fe8r, cB | §11, App H; Figure 5 | — | keep |
| B25 | Fixed midpoint weight `< 1` misses the face for all but countably many kinks | FE Prop 5.6 | P | fe8 | §11 | Couenne 0.25 (Belotti et al. p. 18) | keep; SCIP's box-dependent weight not covered |
| B26 | Min-score strong branching with Couenne's point: `≥ 0.0287/eps - 1` nodes | FE Prop 5.7 | P (exact rational path) | fe8 | §11, App H | — | keep |
| B27 | Conjecture 5.8 false; Question 5.9 | FE §5.4 | W/C | fe8 | §15 | — | open |
| B28 | Every deterministic clip schedule misses an uncountable null set; `Omega(log 1/eps)` in 1D at alternating trap points; McCormick bound `2K' + 1` at alternating points, `2K' - 1` at run-length-2 points | RB Thm A | P (scope corrected by cA) | rob, cA | §11, App H | — | restate per cA |
| B29 | Randomized clamp: bounded expected count uniformly in `eps` in 1D and with `x`-only selection | RB Thm B | P | rob | App H | — | keep |
| B30 | Price of safety: every `theta0`-safe rule needs `J + 1` splits | RB Prop C | P | rob, cA | §11 | — | keep |
| B31 | Recentring clamp: exactly `J + 1` splits (split-optimal among safe rules for `theta ≤ 1/3`); McCormick bound `1 + 2/(theta^2(1 - theta) d0)` | RB Prop D | P (strengthened by rob; direct argument by cA) | rob, cA | §11 | — | keep |
| B32 | Randomized clamp under widest-side selection: `E[T] ≥ c log(1/eps)` proved; `eps^(-gamma)` conjectured | RB Prop E, Conj E' | P/C | rob | App H | — | keep proved part |
| B33 | Incumbent rule creates at most one sub-`theta` child per incumbent value and coordinate on a path | RB Prop F | P | rob | App H | — | keep |
| B34 | Safe rules halve boundary chains within about `ln 2/theta0` splits | RB Lemma 0 | P | rob | App H | — | keep |

## §12 Integer branching: the class number

| ID | Claim (key hypotheses) | Source | Status | Reviews | Location | Lit | Action |
|---|---|---|---|---|---|---|---|
| Z1 | Projected relaxation `phi` is convex, `phi ≤ f` on `F`; exactness condition (E) | IC §1.1 | P | ic | §12 | — | keep |
| Z2 | `P`-covering convex-piece trees; `tau`-certificates; B&B runs give certificates (infeasibility, bound, integrality pruning) | IC Defs 1.1–1.2, Lemma 1.3 | P | ic | §12 | — | keep |
| Z3 | Classes, midpoint and segment graphs; `omega(G^mid) ≤ ... ≤ kappa`; counting bound | IC Def 1.4, Lemma 1.5 | P | ic, bbc | §12 | DDM (midpoint argument); Kaibel–Weltge (hiding sets) | credit |
| Z4 | **Theorem IX**: every `P`-covering `tau`-certificate has `≥ kappa_tau(P)` leaves | IC Thm 1.6 | P | ic | §12, full proof | — | keep |
| Z5 | Hemispace separation | IC Lemma 1.7a | P/K | icr | App I | Kakutani 1937; Stone | credit |
| Z6 | Exactness for arbitrary convex pieces: multiway and binary hemispace trees; closed halfspaces for MILP relaxations | IC Thm 1.7 | P (proof replaced after ic; additions after icr) | ic, icr | §12 statement, App I proof | — | keep |
| Z7 | Cuts in integer variables and feasibility reductions keep `L ≥ kappa(F)`; incumbent-certified removals give `kappa ≤ L + sum s_v`, `N ≥ kappa/(2n+1)` for one pass per node, `kappa/(n+1)` for binaries; changes in continuous variables not covered | IC Thm 1.8 | P (restated after ic; `+1` after icr) | ic, icr | §12 statement, App I proof | — | keep |
| Z8 | Pure ILP with `m` constraints: `kappa ≤ m + 1`; MILP: facets of the projected sublevel polyhedron | IC Prop 2.1 | P | ic | §12 | relaxation complexity (Kaibel–Weltge; Averkov et al.) | keep |
| Z9 | Compact MILP with `2n` rows and `kappa = 2^n` | IC Example 2.1a | P | ic | §12 | — | keep |
| Z10 | Unconstrained convex objective: `kappa` equals the least number of facets of a lattice-free polyhedron containing the open sublevel set; `1 ≤ omega_mid ≤ kappa ≤ 2^n` | IC Thm 2.2 | P | ic | §12 | lattice-free sets literature | lit; novelty "low to moderate" per ic |
| Z11 | Split trees `2^(n^(1/6 - o(1))) = 2^(L^Omega(1))` while `kappa ≤ L` (also unconstrained convex PL objectives) | IC Thm 2.3 | P given I | ic | §12, App I | Gläser–Pfetsch (statement, exponents 1/12, 1/14, 1/8) | lit |
| Z12 | Quadratic Jeroslow: `kappa = 2`, 3-node split tree, `≥ C(n+1, (n+1)/2)` leaves under variable branching | IC Prop 2.4 | P | ic | §12 | Jeroslow 1974 | credit |
| Z13 | Fixed dimension: split-tree size bounded in terms of `n` | IC Prop 2.5 | P given I | ic | §12 remark | Reis–Rothvoss (flatness) | lit |
| Z14 | Split trees versus `kappa` for convex quadratics | IC Open 2.6 | C | — | §15 | — | open |
| Z15 | Random CVP: `omega_mid ≥ 2^((0.2075 - o(1))n)` for `delta ∈ (0, 0.08)` | IC Thm 3.4 | P | ic, bbc | §12, App I | Siegel 1945 | keep |
| Z16 | Random CVP: `kappa ≥ 2^((0.2925 - o(1))n)` for every basis (all continuous-relaxation B&B, incl. sphere decoding) | IC Thm 3.5 | P | ic | §12, App I | Siegel 1945; DDM Lemma 12 (counting mechanism) | keep (basis invariance checked here) |
| Z17 | `omega_mid ≤ 2^((0.2612 + o(1))n)`, `kappa ≤ 2^((1/2 + o(1))n)` | IC Prop 3.6 | P given I | ic | §12, App I | Kabatiansky–Levenshtein | lit |
| Z18 | True CVP exponents; Gaussian bases | IC Conj 3.7, 3.8 | C | — | §15 | — | open |
| Z19 | Perspective relaxation needs `2^k` leaves on gadgets where the `2x2` block hull is exact at the root; asymmetric gadget with a unique optimum | IC §4 | P (exact rational) | ic, bbc | §12 statement, App I | perspective and 2x2 hull literature | keep one gadget |
| Z20 | Path lemma; C1 iff root probing with the optimal incumbent fixes every variable; C1 implies `kappa ≤ 2n + 1` and `≤ 2n + 1` nodes for binaries; gap up to factor `n` | IC §5, Prop 5.2 | P (corrected) | ic | §12 | — | keep (used in §13) |

## §13 Random instances

| ID | Claim (key hypotheses) | Source | Status | Reviews | Location | Lit | Action |
|---|---|---|---|---|---|---|---|
| Q1 | Sparse regression model, `f(S) = y' M_S^{-1} y`, perspective relaxation, B&B conventions | SR §1 | — | se | §13 | — | keep; local notation (`N` samples, ridge `nu`) |
| Q2 | Exact midpoint formula for supports | SR Lemma 1.5 | P | se | §13 | — | keep |
| Q3 | Removal-half C1 gives a `2k + 1` certificate | SR Lemma 1.3 | P | se | §13 | — | keep |
| Q4 | Exactness characterization of the Boolean relaxation | SR Cor 2.4 | P/K | se | §13 | PWE Corollary 2 | credit |
| Q5 | Root exactness iff `tau^2 ≥ (2+eps) log p` (converse below `(2-eps) log p`); sample form `N ≥ (2 + o(1)) k log p` (regime `log^6 p ≤ N ≤ p`, `k ≤ C0 N/log p`, `sqrt N ≤ nu ≤ N/log^2 p`) | SR Thm 3.1, Cor 3.4 | P (asymptotic; total-energy remark) | se, srr, cB | §13 statement, App J proof | Lasso-style technique; Wainwright | keep; state regime |
| Q6 | C1 (every single wrong fixing prunable, strict) iff `tau^2 ≥ (2+eps) log(p nu/N)`; linear trees for every variable-branching rule (incumbent available or best-bound) | SR Thm 3.2 | P | se, srr | §13, App J | — | keep |
| Q7 | Sample forms: C1 at `N ≈ 2k log(p/sqrt N)`; window `2 - gamma < alpha < 2` for `k = p^gamma` | SR Cor 3.3, 3.4 | P | se | §13 Table 4 | — | keep |
| Q8 | PWE Theorem 2 (per-entry noise, `rho = sqrt n`) is false as stated: exactness probability tends to `(1 - 2 Phibar(w_min/gamma))^(d-k) < 1` (0.123 in an example); proof hides a normalization mismatch | SR Remark 3.5 | P (self-contained) + E (independent verification) | se, pwe, cB | §13 remark | PWE 2015; Pilanci thesis 2016; Dong; Bertsimas et al. | lit; user decision on contacting authors |
| Q9 | Fixed ridge `nu = sqrt N` with fixed SNR: no `k log p` threshold for C1 in the asymptotic regime; finite-size balance (seed 1007: exactly four failing nulls of 3195) | SR §3.5, §6.3 | P + E | se, cB | §13 remark | — | keep; cite 2.79 (all nodes) not 2.75 |
| Q10 | Pure noise and low total SNR: conflict cliques `C(p,k)^(c')` for `x < x0 = 1.2564`, `k -> inf`, `k/N -> 0`, `nu = o(N)`; `c' < 3 - 2 sqrt 2` | SR Thms 4.3, 4.4 | P (asymptotic; constants corrected by cB) | sh, srr, cB | §13, App J | DDM (transfer of the clique argument); Gilbert–Varshamov | keep; constants per cB |
| Q11 | Below the information-theoretic threshold, cliques `exp(Omega(k))`; rule-dependent regime | SR Conj 5.2, Q 5.1 | C | cB | §15 | Bandeira et al. (low-degree) | open |
| Q12 | Observed C1 transitions at about half the first-order threshold, second-order explanation | SR §6.7 | H | se | §13 remark (heuristic) | — | keep labelled |
| Q13 | `x*` is a box minimizer iff every KKT sign `zeta_i ≥ 0`; probability exactly `2^-n` at every SNR | BL Prop 1.1 | P | me | §13 | — | keep |
| Q14 | Root exact with probability `≤ ((1 + 2(1 + 4 rho)^(-beta/2))/2)^n` | BL Thm 1.2 | P | me | §13, App J | — | keep |
| Q15 | Face law for projections onto Gaussian cones, extended to sign-symmetric column laws | BL Thm 1.3 | P/K | me | App J | Hug–Schneider; McCoy–Tropp; Godland–Kabluchko–Thäle | credit |
| Q16 | Root gap linear in `n`: `W - R ≥ (beta/(1 + 2beta) - o(1)) n` | BL Thm 1.7 | P | me | App J | — | keep |
| Q17 | ML threshold `rho beta = 2 log n` | BL Thm 2.2 | P/K (`beta = 1` achievability known) | me | §13 | Hansen–Hassibi–Dimakis–Xu; Hassibi et al. 2014 | credit |
| Q18 | Midpoint conflicts vanish above `8 log n`; cliques `exp(n^(1 - c/8 + o(1)))` below | BL Thms 2.3, 5.1 | P | mh | App J remark | — | keep as remark if space |
| Q19 | C1 iff `rho > (1 + o(1)) n/(4(2beta - 1))` (`beta > 1` unconditional; `beta = 1` given Hu–Lu); every single fixing fails below `(1 - eps) n/8` | BL Thm 3.1 | P (conditional part) | me, mr | §13, App J | Hu–Lu 2020 | lit; keep conditional |
| Q20 | Static-order variable branching: `≤ (n+1) exp((1 + o(1))(n/(4(2beta - 1) rho)) log rho)` nodes | BL Thm 4.1 | P (hockey-stick count per cB) | mh, mr, cB | §13, App J | — | keep the corrected count |
| Q21 | Class number `log kappa ≥ c_1 (n/rho) log rho - log(8n)` for `71 ≤ rho ≤ c'_1 n` (`c_1 = 1.8e-5`, `c'_1 ≈ 1.4e-4`); entropy lemma | BL Thm 4.3, Lemma 4.2 | P (vacuous below `n ≈ 1.7e7`) | mh, mr | §13, App J | — | keep; state the vacuity |
| Q22 | Sharp constants | BL Conj 3.3, 4.5 | C | — | §15 | — | open |
| Q23 | Shor SDP exact at `x*` iff `A'A + diag(zeta) ⪰ 0`; w.h.p. for `beta > 1` at `rho ≥ (1+eps) 2beta log n/(sqrt beta - 1)^4` | BL Thm 6.2 | P given I | me, mr | §13 | Jaldén–Martin–Ottersten 2003 | credit |
| Q24 | Eigenvalue-shift relaxation exact from the same SNR; sharp for the shift | BL Prop 6.3 | P | cB | §13 | — | keep |
| Q25 | At `rho = c log n` (square systems), ML recovery is polynomial while box-relaxation certificates are superpolynomial | BL §4 | I (unverified 2026 citation) | mh | §13 interpretation | Papailiopoulos 2026 | lit; drop the search half if unverified |
| Q26 | Stronger lifted relaxations (optimal-perspective SDP, rank-one, `2x2` hulls) keep the sharp constants when `r N log p = o(p)` | SR2 | P | s2, s2r | — | — | excl |

## §14 Computational evidence (archived; not rerun)

| ID | Evidence | Source and archive | Status | Reviews | Location | Wording limits |
|---|---|---|---|---|---|---|
| E1 | Toy sphere/ball B&B: exponents `0, 1/4, 1/2, 1`; leaves/LB 30–45 (2D), 100–125 (3D); ball follows the boundary stratum | CN §9; `spatial-constrained/logs/` | E (floating point; dual bounds validated) | sc | §14 Table 5 | not certified counts |
| E2 | RLCT bisection sweeps: slopes within 0.021; leaves/LB within factor 2.2 over 5–11 decades; leading constants to 3–5 digits | RL §5; `rlct/logs/` | E | rl, rlr | §14 | idealized bisection |
| E3 | Face-exact rule tables; exact `Q(sqrt 2)` replays for the kink family | FE §8; `spatial-face-exact/`; closing audit B scripts | E (exact rows and floating rows labelled) | fe8, fe8r, cB | §14 | label arithmetic per row |
| E4 | Single-tree toy B&B with certified bounds: 2.7–3.1 per variable; SCIP default 2.1–2.3, without the minor separator 2.9–3.5; grid optima (upper bounds) | ST §7; `theory-face-exact/logs/` | E | st, str | §14 | toy is not SCIP; two seeds; grid optima are upper bounds |
| E5 | Propagation node and round counts (Table 7.1) | CP §7; `cutoff-propagation/logs/` | E (floating point, no outward rounding) | cut | §14 | — |
| E6 | SCIP 10.0.2 node exponents under the model setting; five departures with causes | SV; `solver-validation/results/` | E | none (not independently reproduced) | §14 Table 6 | one solver, one machine |
| E7 | MINLPLib branching-point study: LP point 1.03 (CI 0.83–1.26), no clamp 2.19 (CI 1.43–3.39), midpoint 1.15; boundary chains (378,210-node path on `ex4_1_5`) | MB; `minlplib-branching/results/` | E | not independently reviewed; default and LP-point counts reproduced exactly by RB | §14 Table 7 | seed noise large; one solver |
| E8 | Safe rules on MINLPLib: randomized clamp 0.96, recentring 0.92 (CI 0.71–1.14), no clamp 2.00 (CI 1.43–2.96); synthetic SCIP kinks | RB §6; `robust-branching-points/results/` | E | rob | §14 Table 7 | neutral beyond seed noise |
| E9 | Chain scaling: SCIP ~5x per two variables at `n = 4..10`; chain DP B&B certified instances to `n = 8192` (work `n^1.6–1.8`); heavy tails on probe3 | SS; `research-20260929/computation/` | E | cmp | §14 Table 8 | exponential and degree 5–6 power laws fit equally well; prototype bounds by a rounding analysis |
| E10 | Computed decomposition certificates; `theta` threshold; copy drift; crossovers | DC §5; `theory-decomposition/logs/` | E (floating point; pair test widened after decnd) | dec, decnd | §9, §14 | — |
| E11 | Sparse regression and binary least-squares computations | SR §6; BL §7 | E | se, sh, me, mh, cB | §13 remarks, §14 | outside the theorems' regimes |
| E12 | Random lattice numerics `n = 8..32` | IC §3.7 | E | ic | App I remark | onset of the Gaussian-basis obstacle only |

## Excluded or out-of-scope repository developments

| Development | Source | Reason (see ARCHITECTURE 3.3) |
|---|---|---|
| Stronger lifted relaxations for sparse regression | SR2 | length; separate paper |
| Adaptive decomposition algorithms LS, GR | EA, AM | algorithmic decomposition theory; separate paper |
| Graded exact split, covering upper half | CU | decomposition relaxations, not tree size |
| Consistency relaxations | KC | decomposition relaxations, not tree size |
| Split-robust lower bounds | RLB, RC | qualitative, tiny bases |
| Calibrations, bang-bang, singular arcs | `research-20260929/theory-calibration`, `theory-bangbang` | different topic |
| Open MINLPLib certificates, bound audit | `research-20260929/open-instances*`, `bound-audit` | covered by `paper-open-minlplib` |
| Treewidth census, dense coupling | `research-20260929/treewidth-census`, `theory-coupling` | not needed; census not independently reviewed |
| GCS gap bounds, split separation, intersection cuts | `research-20260928b/gcs`, `side-results`, `sfree` | different topics |
| Scout first-pass results | `research-20260928b/scouting/` | unreviewed; must not be cited |

## Open items for later stages

1. Luna: every row with a `lit` action; Section 10 of ARCHITECTURE.md.
2. Parallel math audit: rows marked `audit` (K14, K17, K20, S16) and the
   unrechecked edits of ARCHITECTURE 6.2(12).
3. Sol: D3 (rigorous threshold), D7 (base, optional).
4. Root: the decisions of ARCHITECTURE Section 13.
5. Writers: replace "Location" by manuscript labels; add review-resolution
   entries as rounds complete.
