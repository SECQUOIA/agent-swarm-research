# Terminology and notation (paper and supplement)

Date: 2026-10-04. This file fixes one term or symbol for each recurring
object, so that later editors use the same words in `main.tex`,
`supplement.tex`, the table generators (`data/make_tables.py`,
`make_points_table.py`, `make_campaign_table.py`) and the figure scripts.
It records the choices made for style-check-r1 group T (items T1–T20), the
related items J1, J2, J10, H2 and L11, and numbers-check-r1 items 3, 14 and
15. Edit the generators, never the generated tables. Round 2 (2026-10-04,
adjudication G7-08) updated the status words, "separately written", the
closure terms, "best listed dual bound", the first/second code names and the
rule that main-text certificate sentences carry no tier.

Rule for labels: no single capital letter names a class, status, level,
construction or method. Labels are short words, defined once in Section 2 or
in the caption of the table that uses them, and set in italics where a
caption or a sentence defines them.

## 1. Labels

| object | label(s) | defined in | replaces |
|---|---|---|---|
| categories of disagreement | category A (tolerance artifact), category B (invalid claim); always with the word "category" | Def. 2.4 (`def:sem-categories`) | — (kept) |
| arithmetic tags | `\arith{E}` exact, `\arith{I}` mpmath interval, `\arith{F}` own outward-rounded binary64, `\arith{L}` library hypothesis (unused) | §2.5; caption of `tab:trust` (Table 2 has no arithmetic column since round 1) | bare E/I/F in table cells; F+I is written `\arith{F}+\arith{I}` |
| evidence levels (`\evid{}`) | `\evid{hand}` proof written out in full, without computation (the name refers to the form of the proof, not to who wrote or checked it); `\evid{stored}` stored finite certificate checked by exact or outward-rounded replay; `\evid{rerun}` check that reruns a search or the numerical computation that produced its data, because these are not stored (also `catmix`, `emfl`, `topopt`); combined as `\evid{hand}+\evid{stored}` | §2.5 | P, C, S |
| status of a statement | *proved*; *verified by a separately written implementation*; *computed* (single implementation, not presented as proved); *floating-point output* (solver output and published values, compared with our results, never premises). In `tab:trust` and the register: *verified*; *weaker second*, *partial second* (proved, and a separately written implementation certifies a weaker bound or part of the domain); *proved* (no separately written second implementation: `hvycrash`, a written proof; `ann_cumene_tanh`, whose second code is not separately written, §2.6); *shared core* (both KAN paths use one rigorous exponential and interval core). The claim index maps the statuses per instance (`artifact/README.md`) | §2.6; `tab:trust` caption | "proven", "independently verified" |
| replay tiers | Tier 1 under 10 minutes, Tier 2 under one hour, Tier 3 longer, by recorded wall time per instance (summed over its parts); KAN enclosure: `r3` models Tier 1, `r5` models Tier 2 | defined in §10; printed only in Table 7 (`tab:repro-tiers`), the certificate boxes, the register (S7.3) and `artifact/README.md`; main-text certificate sentences give no tier (round 2) | tiers by cost class |
| certificate classes | *staged* (§4), *comparison* (§5.1), *dense rows* (§5.2), *convexity* (§5.3), *identity* (§5.4), *reduced space* (§5.5); in prose "the staged class", "the reduced-space class" | §3.2; §5 opening | A, A′, B, C, D, E |
| prior status | *fp closure*, *fp near-closure*, *listed solve*, *related model* (a twin, a rounded copy or another related model; `camshape200` and `camshape800`, whose rounded QPLIB copies are listed as solved, are related model since round 1), *value only*, *unread source*, *none* | §3.4; S3.2 (`app:literature-table`) | F, f, Lst, T, K, U, N ("codes") |
| point constructions | explicit exact points, triangular definitions, interval existence proofs, strictly interior points; table labels *exact point*, *triangular*, *existence proof*, *interior point* | §6.1 (description list); `tab:points-all` caption | (A)–(D), "construction (A)" |
| audit proof methods | listed-point check, Krawczyk proof, shifted Krawczyk proof, dedicated proof; table labels *listed point*, *Krawczyk*, *shifted Krawczyk*, *dedicated* | §7.3; `tab:audit-pairs` caption | routes A–D, route (B) |
| data readings of a code | exact, outward, rounded, binary64 reading; in `tab:trust` "exact, then outward" and "X / Y" (the family's codes use both) | App. A.2 (`app:semantics-codes`); `tab:trust` caption | types E, O, M, B; E→O, E/O, O/M |
| camshape checks | (K1)–(K6), with (K6) $c_H\le2$ | §5.1, S1.3 | (C1)–(C5) and "$c_H\le2$" |
| MINLPLib's solved mark | "solved mark"; once: "shown as the letter S on the instance pages" (§1.1); "marked solved"; in tables $^{\checkmark}$ | §1.1 | "S mark", "S-marked", superscript S |
| audit classes | (i) *invalid* (margin at least $u(s)$), (i-r) *invalid as displayed* (positive margin below $u(s)$), (ii) *proved valid*, (ii$'$) *not refuted after repair* (evidence), (iii) *undecided*; for the flagged pairs, the screen's slack of half a unit gives the same classes | §7.1; S4.1 | "proven valid", "(ii) repair" |
| supplement numbers | prefix S (Section S1, Table S3) only | `supplement.tex` note | — |

## 2. Words

| concept | use | do not use |
|---|---|---|
| MINLPLib entry | instance (`\inst{}`); "the six KAN instances of our set", "ten KAN instances" | "KAN models" for entries |
| mathematical content | model, stored model $\model$, $\RP$, $\Rnet$ | — |
| Kolmogorov–Arnold network | expanded at first use: §1.1 ("Kolmogorov–Arnold networks (KANs)"), S1.9 title; then KAN | "trained KANs" before the expansion |
| artificial neural network | name the instance (`ann_cumene_tanh`) or say "neural network" | ANN |
| split | split $\varphi=(\varphi_t)$, split functions, *split form* (the set of functions allowed for the $\varphi_t$: affine, quadratic, cellwise affine), split data (stored arrays) | "split class", "verification functions $S_t$", "calibration arrays", "calibrations" for stored data |
| relation to classical terms | defined once in §4.1: split functions are Krotov's verification functions; a split with $B(\varphi)=\vstar$ is a discrete calibration. Since round 2 the abstract does not use the word (it names the classical devices Lagrangian duality, Sturm comparison and Taylor models) | — |
| open | "listed as open" (no solved mark); "open by our selection rule" | "open in sense (a)/(b)"; "open" for B&B boxes in the main text, triangles, undecided audit pairs |
| ann search partition | pruned regions and unsplit leaf boxes (S1.9 adds "its open boxes" once) | "closed regions", "final open boxes" |
| floating-point closure, floating-point near-closure, tolerance-level closure | defined once in §2.2 (`sec:semantics-cert`): a solver run's optimality or gap below its tolerance under its own tolerances; a printed relative gap of at most 10⁻⁴; a floating-point closure whose dual bound is valid. The supplement (S3) points there | "closed within its tolerances", "closure to MINLPLib's tolerance", a second definition in the supplement |
| dual value in MINLPLib's instance list | "dual bound in the instance list" (main text); "instance-list dual", "instance-list gap" (S1.1, S3.4) | "listing dual(s)", "listing gap" |
| best listed dual bound | best single-solver bound on the instance page (§2.1); "best listed dual bound" in prose; table headers and figure legends may keep "best listed dual" where the caption defines it | "listed duals" for instance-list values; "best listed dual" in prose |
| certificate family | a row of `tab:trust` (§2.6) | — |
| separately written | "separately written implementation/code" only in the sense of §2.6 (round 2): a second implementation, written later in a separate agent session, whose checking computation neither imports nor runs the first implementation and, as far as the records show, contains no code copied from it; the session may have read the first code (most did). The second `ann_cumene_tanh` code is not separately written | "independent" without the §2.6 definition, "a separate code", "re-derived by a separate check" in `tab:trust` |
| first and second implementation | "the first code" (first implementation: the code that produced the certificate) and "the second code" (second implementation); also "first/second search, script" | "the authors' code", "the verifier's code", "the verifier's re-certifier" (they suggest human-written code) |
| who checked | "a separate agent session" | "second party", "different party", "separate review", "peer review" |
| "by hand" | only as the name of the evidence level `\evid{hand}` (a proof written out without computation); in prose "a written proof" | "built by hand", "proof by hand" for certificates or points |
| proved | proved | proven |
| file format | OSIL; "OSiL" only for the schema name in the §2.1 footnote | OSiL conventions, OSiL default |

## 3. Solver names

Vendors' spelling everywhere, including tables, captions and figure legends:
BARON, Gurobi, SCIP, ANTIGONE, LINDO (MINLPLib's label for LINDOGlobal),
COUENNE, Octeract, MINOTAUR, CPLEX, BONMIN, SHOT, HiGHS, MAiNGO.
MINLPLib's pages and `results_table.csv` write GUROBI; the generators map it
through `solver_name()` in `make_tables.py`, and the `tab:closures` caption
says so once. Internal data keys stay `GUROBI`.

## 4. Notation

| quantity | notation | where | replaces |
|---|---|---|---|
| optimal value of a model | $\vstar(\cdot)$, infimum over the feasible set (Def. 2.2) | everywhere | — |
| KAN optima | $\vstar(\Rnet)\le\vstar(\RP)$; theorem: $L\le\vstar(\Rnet)\le\vstar(\RP)\le U$ | §3.3, §5.5, `tab:kan`, Fig. 1, S1.9, S6 | $\min_{\Rnet}F$, $\min\RP$, $\min_{\RP}F$ |
| exactly feasible set | $\feas$ (`\feas`) | also in `tab:claims` | $F(M)$ |
| KAN relaxation in tables | $\Rnet$ (`\Rnet`) | `tab:solvers`, claims tables | $R$ |
| dtoc5 dual function | $q(\lambda)$, $q(\hat\lambda)$ | §4.2, S1.2, `tab:trust`, claim register | $d(\lambda)$ |
| optcdeg2 split | $\varphi_{t-1}(y,v)=p^y_ty+p^v_tv+\tfrac{q_t}2(v-\bar v_t)^2$ acts on the state $(y_t,v_t)$, i.e. on the separator between stages $t-1$ and $t$ (index convention of §4.1) | §4.3, S1.2 | $S_t$ |
| decimal value of a string | $\dval{\sigma}$; in the audit $d=\dval{s}$ (C5 and §7.4 write $\dval{s}$) | §2.1, §7.2 | bare $d$ without definition |
| audit: upper end of the objective enclosure | $\varphi$ (and $\varphi_{\mathrm{lo}},\varphi_{\mathrm{hi}}$ in S4.1) | §7.1, `tab:audit-pairs`, S4, `fig:audit-margins` | $f$ |
| Krawczyk map | $G$ with components $G_i$; interval vector $\mathbf v\ni G(y)$; fixed-point map $T$ | Thm. 6.1, S2.1, S4.3 (`lem:audit-krawczyk`) | $F$, $\mathbf f$, $g(z)$ |
| pindyck price set | $P=\{p\ge0:d_t(p)\ge0\}$ | §5.3, S1.5 | $F$ |
| powerflow buses 30 and 2 | bus numbers as indices: $W_{30,30}$, $W_{2,2}$, $e_{30}$, $f_2$, $w^R_{30,2}$, $P_{30\to2}$ | §5.3, S1.6 | $L$, $N$ |
| waterno2 pump speed bound | $\ell$ ($\ell^2$, $\ell^3$, $\fl(\ell)^k$) | §8.2, S6 | $L$ |
| waterno2 horizon constant | $r_T$ | §4.5, S1.8 | $c_T$ (clashed with pump coefficients $c$) |
| shortest-path distance (App. B) | $\dist_t(D)$ | `app:splitproofs-cellwise` | $d_t(D)$ |
| chain residual in a proof | $\Xi$ | S1.4 | $\mathcal R$ (reserved for the KAN relaxation) |

## 5. Displays, dates and units

- One display per quantity: the `camshape100` listed-dual gap is
  $1.22\cdot10^{-6}$ (§1.4, §3.1, §5.1, S3.4; exact 1.2157e-6 against the
  optimum and 1.2161e-6 against the listed point, rounded up); the CAMINO
  margins are 4.33%, 7.48% and 80.5% (§1.3 C6, §8.2, S8; exact 4.335%,
  7.487%, 80.598%, rounded down). `lnts50` keeps $3.9\cdot10^{-5}$.
- Dates: ISO `YYYY-MM-DD` for every full date, in prose and tables (the
  audit table converts the page dates with `iso_date()`). Ranges of whole
  days are written out ("2026-10-01 to 2026-10-04"); month-only references
  stay in words ("the December 2021 version").
- Memory of the host: GiB (47 GiB); the run cap: 8192 MiB.

## 6. Certificate boxes

Since round 1, certificate boxes appear only in the supplement (one per
result); the main text gives one certificate sentence after each theorem
(arithmetic, displayed bound, second implementation, evidence level; since
round 2 no tier, which Table 7 and the box give). Every box
has these six fields in this order (`development/labels.md`):

1. Inputs — files with "SHA-256" prefixes, multipliers, points;
2. Computation — what is computed, with arithmetic tags;
3. Data reading — exact / outward / rounded, and the readers;
4. Implementations — which code certifies the display, what the second one certifies;
5. Evidence level — `\evid{hand}`, `\evid{stored}`, `\evid{rerun}`, per instance where they differ;
6. Replay — "Tier~$k$; time", per instance where they differ.

Field contents start with a lowercase letter. Tiers follow the rule of §10.
