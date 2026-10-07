# W3 report: group recB (cut-based recourse, balanced quadratics)

Files edited: `sections/recourse-cuts.tex` (7.4), `sections/recourse-mixed.tex`
(now a remark inside 7.4), `sections/recourse-balanced.tex` (7.5), new
`sections/appendix-recourse-cuts.tex` (Appendix "Cut-based recourse: deferred
proofs", label `app:recourse-cuts`). `appendix-smoothed.tex` was not touched
(it is dropped from the build by the coordinator); no text in my files points
to it any more.

Main-text length of my part in `build/recB/main.pdf`: 7.4 starts in the last
quarter of p. 41, Section 8 starts at the top of p. 47, so about 5.2 pages
(before: about 8 pages, pp. 40-48 of the previous build).

## Summary of the new structure

7.4 Separately concave residuals and minimum cuts (`sec:cuts`):
class (R1)-(R2) written with $F=\frac12x^\T Hx+b^\T x+c$ (same form as 7.5 and
Section 6); Lemma `lem:balance` (moved here from 7.6, used for (R2) and for
balanced quadratics); Lemma `lem:cr-endpoint`; Proposition `prop:cr-cut`, now
(a) the network identity for any binary quadratic with nonpositive pair
coefficients and (b) the expansion of $F(v,y(z))$; Theorem `thm:cr-oracle`;
Remark `rem:cr-cut-prior` (technical comparison only); CORE as
`\begin{algorithm}[CORE: core search]\label{alg:core}`; Theorem
`thm:cr-search`; Proposition `prop:cr-growth` (with the old Lemma
`lem:cr-charge` folded into its proof); Example `ex:cr-flat`; a paragraph
"Exact output" that states the result of Theorem `thm:cr-exact` and cites
Proposition `prop:accept` with the denominator bound $\Omega_{\mathcal K}$;
Remark `rem:cr-mixed` (concave-convex residuals, in `recourse-mixed.tex`).

7.5 Corrected grids without a tree decomposition (`sec:balanced`):
Definition `def:balanced`, Lemma `lem:chaincut` (statement; proof in the
appendix; it now reuses Proposition `prop:cr-cut`(a)), one sentence on prior
constructions, Theorem `thm:balanced` (parts (a) validity on every instance,
(b) bounds under point growth; proof of (a) in the main text, work count in the
appendix), Corollary `cor:core`, one sentence comparing with 7.4, one sentence
pointing to Section 2.

Appendix D (`app:recourse-cuts`): D.1 Lemma `lem:cr-height` (now derived from
Corollary `cor:height` with $\Delta=\Delta_{\mathcal K}$; no fourth height
argument), Theorem `thm:cr-exact` (acceptance via Proposition `prop:accept`);
D.2 Propositions `prop:cr-submod` and `prop:cr-greedy`; D.3 proof of Lemma
`lem:chaincut` and the work count of Theorem `thm:balanced`(b).

Notation changes in my files (CONVENTIONS section 4 and R2 M4): core
$\mathcal C$/$C$ -> $\mathcal K$; residual stays $\mathcal R$
($=\mathcal R_-\cup\mathcal R_+$ in the concave-convex part, old
$\mathcal D\cup\mathcal P$); $W_{\mathcal C}$ -> $V$; signed widths $d_i$ ->
$\delta_i$; binary labels $y$ -> $z$, endpoint vectors $x(y)$ -> $y(z)$,
completions $z(v)$ -> $y(v)$; $m_i=\abs{G_i}-1$ -> $k_i$; grid nodes $g_{i,k}$
-> $a_{i,l}$; unary terms $\eta_i$ -> $\chi_i$, $\Phi(y)$ -> $F_\chi(y)$;
generic function $\theta$ -> $\varphi$; balanced signs $\sigma$ -> $o$ (same
letter as (R2)); set function $g(S)$ -> $\Phi(S)$, $h(S)$ -> $\hat\Phi(S)$,
label $\zeta(S)$ -> $y_-(S)$, residual quadratic $q$ -> $F(v,\cdot)$; greedy
vectors $b^\pi$ -> $a^\pi$; LP variables $(\beta,y)$ -> $(t,\xi)$; retained
cells $\mathcal K_j$ -> $\mathcal Q_j'$; cell bound
$\beta_V(C)=\min_{\text{corners}}V-e_j$ (analogue of $\beta(C)$ in Section 4);
height constants $T_0,H_0,D_0$ -> $\Delta_{\mathcal K}$ and $\Omega_{\mathcal K}$
(the $\Omega$ of `eq:exact-constants`); $\Phi(z)$ in the height lemma ->
$\Psi(y)$; core condition number -> $\kappa_{\mathcal K}=\kappa(L,g)$;
$f(k,\kappa)$ -> explicit $8^k(1+\sqrt{k\kappa_{\mathcal K}})^k\poly(I)$;
$l_i$ -> $\ell_i$; "labels per coordinate" -> "nodes per coordinate";
"capped algorithm"/"Algorithm 2" -> CT, EX, REC with `alg:` references.
New symbols ($\chi_i$, $F_\chi$, $a_{i,l}$, $\Psi$, $\Delta_{\mathcal K}$,
$\Omega_{\mathcal K}$, $\kappa_{\mathcal K}$, $\beta_V$, $\mathcal Q_j$) were
checked to be unused elsewhere or used only locally.

## (1) Adjudication of assigned findings

"N/A" means that the finding has no part in recB files; it is listed for
completeness and left to the owning group.

| id | decision | reason | change made (recB files) |
|---|---|---|---|
| F7 | ACCEPTED (my part) | "of the report" is a drafting artifact | Replaced by "Corollary cor:core complements Section sec:cuts: residual coordinates may now have positive diagonal, but they are gridded and filtered like the core, so their curvature enters $\kappa$ and growth of $F$ in all coordinates is needed; the residual graph may still be dense." (merges Rewrite 14 with the price stated in F79/F120). optsets "FG" part: N/A (optsets). |
| F9 | ACCEPTED (my part) / MODIFIED | Section 7 too long; 7.4 (concave-convex) unconnected | Concave-convex subsection reduced to Remark rem:cr-mixed, explicitly connected to CORE; lem:cr-height, thm:cr-exact, prop:cr-submod, prop:cr-greedy, proof of lem:chaincut and the work count of thm:balanced moved to Appendix D; smoothed text removed. Title "other exact grid oracles" not adopted: CONVENTIONS fixes "Corrected grids without a tree decomposition". recourse-convex parts: N/A (recA). |
| F10 | ACCEPTED (my part) | four height lemmas | lem:cr-height is now a corollary of cor:height (box QP $F_y$ on $[0,1]^k$ with $\Delta=\Delta_{\mathcal K}$); its own Leibniz/Cramer argument is deleted. thm:cr-exact uses prop:accept instead of re-deriving the separation. Other items: N/A. |
| F11 | ACCEPTED (my part) | prior work repeated | rem:cr-cut-prior keeps only what is specific to Theorem thm:cr-oracle (empty-core case, conditional form, contrast with Del Pia-Khajavirad Thm 4, role of (R1)). The remark "Position of Theorem thm:balanced" was deleted because related.tex ("Cuts and submodularity") now contains the same comparison; a one-line pointer to Section 2 replaces it. The untitled remark after lem:chaincut became one sentence. The BuntonTabuada/GomezHan comparison in the concave-convex part became a pointer to Section 2. |
| F12 | ACCEPTED (my part) | notation overload | calR now always residual; core is calK; $\ell_i$ throughout; see notation list above. Notation table: N/A (core). |
| F13 | ACCEPTED (my part) | unstable algorithm names | "capped algorithm", "Algorithm 2" -> CT (Algorithm alg:ct), EX (alg:ex), REC (alg:rec); "labels per coordinate" -> "nodes per coordinate". |
| F15 | N/A | recourse-valuefn (recA) | -- |
| F20 | ACCEPTED | ungrammatical "condition~Definition"; "rational reconstruction" wrong | "the condition of Definition def:curvature"; exact part now says EX uses CT, REC (Algorithm alg:rec) and Proposition prop:accept. |
| F24 | ACCEPTED (my part) | duplicate headings | "Search over a continuous core." paragraph followed by the CORE algorithm environment; the second heading is gone. Roadmap: recA (done in recourse.tex). |
| F25 | ACCEPTED (my part) | untitled remarks | Untitled remark after lem:cr-height deleted (one sentence kept in the appendix); untitled remark after lem:chaincut replaced by a sentence. All remaining remarks in my files have titles. |
| F26 | ACCEPTED (no change needed) | no British spellings in my files | checked by grep. |
| F29 | ACCEPTED (my part) | "this effect" in appendix-smoothed | The smoothed appendix is deleted; the main-text paragraph pointing to it is removed. Other items: N/A. |
| F30 | ACCEPTED (my part) | "box-stable" undefined | Replaced by an explicit sentence in thm:cr-oracle ("The same holds after the residual box is replaced by a rational subbox, after residual coordinates are fixed, and after rational linear terms are added"). |
| F34 | ACCEPTED (my part) | overfull boxes | No overfull box from my files in build/recB. |
| F35 | ACCEPTED (my part) | paper too long | Smoothed count deleted from my text; concave-convex part reduced to a remark with citations; lem:cr-height, thm:cr-exact, prop:cr-greedy moved. The split into two papers is not adopted (CONVENTIONS: one paper). |
| F41 | ACCEPTED (my part) | calR clash, $\ell_i$ | as F12. |
| F42 | ACCEPTED (part a) | "of the report" | as F7; (b)-(d): N/A. |
| F43 | N/A | optsets, recourse-convex, intro | -- |
| F45 | N/A | recourse-valuefn | -- |
| F46 | N/A | recourse-convex | -- |
| F49 | ACCEPTED (my parts a, e) | terminology; dangling "this effect" | "capped algorithm" -> CT, "labels" -> nodes; App C text deleted. Other parts: N/A. |
| F56 | N/A | recourse-convex | -- |
| F58 | N/A | P clashes elsewhere | (my files no longer use $\mathcal P$ for the convex part). |
| F59 | ACCEPTED (my part) | S overloaded | The interior set $S$ in the old lem:cr-height proof is gone (lemma now cites cor:height). $S$ remains only as a subset of $\mathcal R_-$ in the submodular part, which is standard. |
| F60 | ACCEPTED (my part) | Section-7 scheme | core $\mathcal K$, residual $\mathcal R=\mathcal R_-\cup\mathcal R_+$, $v=x_{\mathcal K}$, $y=x_{\mathcal R}$, value function $V$, no $W$; cor:core uses $\mathcal K$. |
| F63 | ACCEPTED (my part) | $d_i$ and $m_i$ collisions | signed widths -> $\delta_i$; $\abs{G_i}-1$ -> $k_i$ (CONVENTIONS; R2 suggested $r_i$). |
| F65 | ACCEPTED (my part) | algorithm names | as F13. |
| F67 | ACCEPTED (my part) | exact output developed four times; "rational reconstruction" | thm:cr-exact cites prop:accept with bound $\Omega_{\mathcal K}$; lem:cr-height cites cor:height; thm:balanced cites EX/REC/prop:accept. |
| F68 | N/A | other files | -- |
| F69 | N/A | recourse-valuefn | -- |
| F70 | ACCEPTED (my part) | core growth $\kappa$ | Prop cr-growth now defines $\kappa_{\mathcal K}=\kappa(L,g)=\max\{1,L/g\}$ with the general convention; thm:balanced says "point growth with condition number $\kappa$". |
| F71 | ACCEPTED / MODIFIED | 7.5 never used | Remark rem:cr-mixed: "Proposition prop:cr-greedy ... supplies, for concave-convex residuals, the exact oracle required by CORE (Theorem thm:cr-search and Proposition prop:cr-growth), with a certificate checkable by its part (d) without optimization." The reviewer and the task text say "required by Theorem 7.33 / thm:cr-oracle"; Theorem 7.33 was thm:cr-search, which is what requires an exact oracle, while thm:cr-oracle supplies one for (R1)-(R2). The remark says so. Roadmap/intro mention: requested below. |
| F72 | ACCEPTED (my part) | $l_i$ vs $\ell_i$ | $\ell_i$ everywhere in my files. |
| F79 | ACCEPTED / MODIFIED | artifact and overclaim | as F7 (states the price: gridding, curvature in $\kappa$, growth in all coordinates). |
| F81 | ACCEPTED | "rational reconstruction" wrong | as F20. |
| F84 | ACCEPTED (my part) | $f$ reused | thm:cr-exact states $8^k(1+\sqrt{k\kappa_{\mathcal K}})^k\poly(I)$ explicitly; no $f$. |
| F87 | N/A | recourse-convex | -- |
| F88 | N/A | recourse.tex, limits.tex | -- |
| F89 | ACCEPTED (my part) | $h_j$ defined four ways | 7.4 says $h_j=2^{-j}$ is the common mesh of Section 5 with $s=1$; no new $\eta$ in my files ($\eta_i$ unary terms renamed $\chi_i$). |
| F91 | ACCEPTED (my part) | forward reference to App C | removed with the smoothed text. |
| F92 | N/A | recourse-convex | -- |
| F93 | ACCEPTED | dangling phrase in App C | App C deleted (coordinator drops the file). |
| F94 | ACCEPTED (my part) | common $L$ unexplained | CORE takes one $L\ge L_i$ for all core coordinates; the proof uses $e_{\mathcal K}(C)=\sum_{i\in\mathcal K}L_iw_i^2/8\le e_j$ (recA's per-coordinate form). |
| F110 | N/A | recourse-convex | -- |
| F111 | N/A | recourse-convex | -- |
| F112 | N/A | recourse-valuefn | -- |
| F113 | ACCEPTED (my part) | symbol clashes | calR residual only; $H_0$, $D_0$ removed; $g(S)\to\Phi(S)$; $|G_i|-1\to k_i$; atom count $M$ removed with smoothed text; balanced signs $\sigma\to o$; pair index $b$ replaced by pairs $(i,l)$; $\beta$ in prop:cr-greedy -> $t$; core $C\to\mathcal K$; $\ell_i$. |
| F115 | N/A | recourse-convex | -- |
| F116 | N/A | recourse-valuefn | -- |
| F117 | ACCEPTED (my part) | core search vs global $L$ | Proof of thm:cr-search applies lem:cr-cell with $B=\mathcal K$ and $e_{\mathcal K}(C)\le kLh_j^2/8=e_j$, which holds with recA's per-coordinate $e_B$. |
| F118 | N/A | recourse-convex | -- |
| F119 | ACCEPTED / MODIFIED | wrong recovery step | as F20; I cite thm:exact, alg:rec and prop:accept (not cor:height, whose role is inside prop:accept). |
| F120 | ACCEPTED / MODIFIED | artifact; price hidden | as F7. |
| F121 | N/A | recourse-local | -- |
| F122 | N/A | recourse-local | -- |
| F123 | ACCEPTED / MODIFIED | "(R1) is essential" unproved; DPK described wrongly | Now: "Condition (R1) is what reduces the residual to endpoint vectors. Without it the conditional problem is a continuous submodular box QP, whose complexity is open [BNW, footnote 2]". DPK: "their polynomial classes [DPK, Theorem 4] restrict the structure of these coordinates (logarithmic treewidth and logarithmic interfaces to the others) and the rank of their coupling to the others, whereas (R2) restricts only signs". Verified against `literature/papers/pia2026-treewidth-and-the-complexity-of/fulltext.md` (Theorem 4: tw$(G_{V^-})\in O(\log|V|)$, $|D\cap N_G(V^+)|\in O(\log|V|)$, rank$(Q_{V^+,N_G(V^+)})\in O(1)$). |
| F124 | N/A | recourse-convex | -- |
| F125 | N/A | recourse-convex | -- |
| F126 | N/A | recourse-convex | -- |
| F127 | N/A | recourse-local | -- |
| F128 | N/A | recourse-local | -- |
| F129 | ACCEPTED (my part) | smoothed text | main-text paragraph deleted, together with the whole smoothed result (CONVENTIONS). |
| F130 | ACCEPTED / MODIFIED | network construction proved twice | Prop cr-cut(a) now states the identity for any binary quadratic with nonpositive pair coefficients; lem:chaincut's proof applies it and only adds the infinite chain arcs; one name $\operatorname{cap}(S_z)$; lem:balance stated once (in 7.4) and cited for (R2) and for balanced quadratics. Instead of moving lem:chaincut before 7.4 (reviewer's suggestion), the shared part is the binary identity, which keeps 7.4 free of grid labels. |
| F131 | REJECTED | move 7.6 out of Section 7 | CONVENTIONS (binding) keeps it as 7.5 in Section 7; recA's roadmap states that it does not use recourse; it shares the cut machinery of 7.4 and cor:core links them. |
| F132 | N/A | recourse-valuefn, recourse-convex | -- |
| F150 | ACCEPTED / MODIFIED | "of the report" | as F7 (the reviewer's "of Theorem thm:cr-oracle" would also be accurate; the chosen sentence states the trade-off). |
| F151 | N/A | recourse-valuefn, recourse-convex | -- |
| F203 | N/A | computation.tex | -- |

## (2) Labels deleted or renamed

| label | status | references should become |
|---|---|---|
| `lem:cr-charge` | deleted (folded into the proof of Prop `prop:cr-growth`) | `prop:cr-growth` (only `appendix-smoothed.tex` cited it) |
| `sec:cr-mixed` | deleted (no subsection any more) | `rem:cr-mixed` (Remark, "Remark~\ref{rem:cr-mixed}") |
| `sec:cr-search` | deleted (paragraph label) | `alg:core` |
| `sec:cr-exact` | deleted (paragraph label) | `thm:cr-exact` |
| `thm:cr-smoothed`, `lem:cr-law`, `rem:cr-smoothed`, `app:smoothed` | deleted with `appendix-smoothed.tex` | none; delete any sentence that relies on the smoothed count |
| `rem:balanced-position` | created and then deleted in this round (duplicate of related.tex) | -- |
| `lem:balance` | moved from 7.6 to 7.4 (statement now for a symmetric $m\times m$ matrix) | unchanged |
| `lem:cr-height`, `thm:cr-exact`, `prop:cr-submod`, `prop:cr-greedy` | moved to Appendix D | unchanged |
| `prop:cr-cut` | content changed: (a) general cut identity `eq:cr-cutid`, (b) expansion | unchanged |
| new | `alg:core` (CORE), `def:balanced`, `rem:cr-mixed`, `app:recourse-cuts` | -- |

## (3) Requests for other files

1. recA (`recourse.tex`, roadmap). Current text: "Section~\ref{sec:local} and the
   extension of the cut oracle to concave--convex residuals are side results".
   Please add the reference: "... and the extension of the cut oracle to
   concave--convex residuals (Remark~\ref{rem:cr-mixed}) are side results".
   One-line roadmap entry if a separate sentence is preferred: "Remark~\ref{rem:cr-mixed}
   extends the oracle to residuals with a convex part: submodular minimization
   then supplies the exact oracle that the core search CORE
   (Algorithm~\ref{alg:core}) requires."
   Also: thm:cr-search's proof uses Lemma `lem:cr-cell` with $B=\mathcal K$, the
   per-coordinate $e_B(C)=\sum_{i\in B}L_iw([a_i,b_i])^2/8$, $V_{\mathcal K}=V$,
   and Theorem `thm:cr-filter` with $\underline V=V$ and $\eta=0$ (current
   recourse-local.tex). Please keep these forms.
2. exact group (`exact.tex`). My files cite: `eq:exact-constants` (I use that
   $\Omega$ depends only on $\Delta$ and the Hessian when all endpoints lie in
   $\Delta^{-1}\Z$ and $\ell_i<u_i$), `cor:height`(a),(b), `lem:statpoly`(c)
   (vertex $v$, $T=J_0(v)$, $\hat H_{TT}\succ0$), `prop:accept` in its new form
   with a denominator bound $\Omega'$, `alg:rec`, `alg:ex`, `thm:exact`
   (proof: EX stops at $q=\poly(I)+O(\log\kappa)$; under growth REC needs only
   Gaussian elimination) and `thm:transfer`. If any of these labels or
   properties change, the proof of `lem:cr-height`/`thm:cr-exact` must be
   updated (tell recB/coordinator).
3. core group (`grids.tex`, `growth.tex`, `appendix-growth.tex`). My files cite
   `alg:ct`, `lem:dp`, `prop:cellwise`, `prop:filter`, `thm:certificate` (C1),
   (C2), `lem:inv`, `lem:states`, `thm:approx`(a),(b) (in the proof of (b): the
   first successful trial has $2^\mu\le6\sqrt{\bar\kappa}$, the caps
   $K_\mu$, $J+1=O(I+q+1)$), `app:growth` (bit lengths: nodes with
   denominators dividing $\Gamma_X2^\alpha$, values and corrections dividing
   $8\Gamma_F\Gamma_X^24^\alpha$, $\alpha=J+O(I)+\mu K_\mu$), `def:curvature`,
   `sec:growth` (common mesh $h_j=s2^{-j}$). Please keep these.
4. front group (`related.tex`). I deleted the remark "Position of
   Theorem~\ref{thm:balanced}" because "Cuts and submodularity" now contains the
   same comparison (BNW open question, Bach discretization, polynomial in
   $\log(1/\varepsilon)$ and $\kappa$, does not settle the question). Please keep
   it there; 7.5 ends with "Section~\ref{sec:related} compares
   Theorem~\ref{thm:balanced} with methods for continuous submodular
   minimization." Also, Remark `rem:cr-mixed` now points to Section 2 for
   BuntonTabuada2022/GomezHan2025 ("the same composition underlies the mixed
   continuous--discrete methods cited in Section~\ref{sec:related}"); please
   keep that sentence of related.tex. Optional (F71/R5 M22): in the intro's
   recourse paragraph, after "only a small core is searched
   (Section~\ref{sec:cuts})", add "; a convex part of the residual is handled by
   submodular minimization (Remark~\ref{rem:cr-mixed})".
5. Anyone citing the smoothed core count (`thm:cr-smoothed`, `app:smoothed`):
   none found by grep outside `appendix-smoothed.tex`.

## (4) New BibTeX entries

None. I added the citation `EdmondsKarp1972`, which is already in
`references.bib` (Edmonds and Karp, J. ACM 19(2):248-264, 1972,
doi:10.1145/321694.321699). All other keys used are existing:
Harary1953, Padberg1989, BurerNatarajanWillemsen2026v3, DelPiaKhajavirad2026,
KozlovTarasovKhachiyan1980, Topkis1978, GrotschelLovaszSchrijver1988,
Edmonds1970, SchlesingerFlach2006, Ishikawa2003.

## (5) Checks run

- `cd paper-decomposition-aware && latexmk -pdf -interaction=nonstopmode -outdir=build/recB main.tex`
  (several times; one run needed `BIBINPUTS=../..: bibtex main` in `build/recB`
  after a bibtex failure caused by an incomplete aux of a concurrent state).
  Final result: no LaTeX errors; no undefined reference or citation from my
  files; no overfull box from my files (remaining overfull boxes are in
  recourse-local, recourse-convex, optsets, limits/appendix files).
- `python3 -B process/w3/checks/recB-cuts.py` (exact Fractions), all passed:
  Prop cr-cut(a) identity and max-flow value on 200 random binary quadratics;
  Prop cr-cut(b) second differences $=H_{ij}\delta_i\delta_j$ and endpoint
  optimality (Lemma cr-endpoint) on 100 random (R1)-(R2) instances;
  Lemma chaincut (threshold encoding, infinite arcs, own Edmonds-Karp) against
  brute force on 80 random balanced instances with nonuniform grids and
  arbitrary unary terms, including all min-marginals of coordinate 1, and the
  node and arc counts; Lemma balance (BFS) against brute force on 300 sign
  patterns.
- `python3 -B process/w3/checks/recB-exact.py` (exact Fractions), all passed:
  Lemma cr-height with $\Omega_{\mathcal K}$ from `eq:exact-constants` on 568
  label values (120 random instances) and the 1/8 example; CORE invariants of
  Theorem cr-search (a)-(c) at every level and the full pipeline of Theorem
  cr-exact (stop at gap $<\Omega_{\mathcal K}^{-2}$, face enumeration,
  acceptance test of prop:accept passes and the output value equals OPT) on 23
  random instances with $k\le2$; the query bound of Prop cr-growth on 10
  instances with core growth; Prop cr-submod (submodularity of $\Phi$, lower
  bound by $\min\Phi$ on sampled points) and Prop cr-greedy (a) and the
  Lovasz-extension identity and maximality of the sorted order used in (c) on
  60 random concave-convex instances.
- Literature: DPK Theorem 4 and BNW footnote 2 checked in
  `literature/papers/.../fulltext.md`.
- No project-wide verification and no CI inspection.

## (6) Unresolved

- The proofs in Appendix D depend on the final forms of `eq:exact-constants`,
  `cor:height`, `lem:statpoly`(c), `prop:accept` (exact group) and of the bit
  analysis in `app:growth` (core group); they match the versions in the tree at
  the time of this report.
- F131 (move 7.5 out of Section 7) rejected per CONVENTIONS; if the coordinator
  moves it later, only the first paragraph of 7.5 and the sentence after
  cor:core need rewording.
- Intro/abstract mention of the concave-convex remark is left to the front
  group (request 4).

## Verification (recB-verify)

Scope. Files: `sections/recourse-cuts.tex`, `sections/recourse-mixed.tex`,
`sections/recourse-balanced.tex`, `sections/appendix-recourse-cuts.tex`.
The task named `assign/recB-verify.json`, which does not exist; I used
`assign/recourse.json` (68 findings). The table above has exactly one row
for each of the 68 ids (checked by script).

### What was checked

1. Adjudications. For every finding that touches these files (F7, F9, F10,
   F11, F12, F13, F20, F24, F25, F26, F29, F30, F34, F35, F41, F42, F49,
   F59, F60, F63, F65, F67, F70, F71, F72, F79, F81, F84, F89, F91, F93,
   F94, F113, F117, F119, F120, F123, F129, F130, F131, F150), the claimed
   change is present in the files. The decisions are justified: F130 MODIFIED
   (sharing the binary cut identity, Prop. cr-cut(a), instead of moving Lemma
   chaincut before 7.4) removes the duplicate proof and keeps 7.4 free of grid
   notation; F131 REJECTED is required by CONVENTIONS section 1 (7.5 stays in
   Section 7); F71 correctly names thm:cr-search (the theorem that needs an
   exact oracle), not thm:cr-oracle. The N/A rows concern only files of other
   groups.
2. Mathematics, line by line: Lemma balance; Lemma cr-endpoint; Prop. cr-cut
   (a) identity and (b) expansion; Thm cr-oracle (weak duality, Edmonds-Karp
   bit lengths, stability under subboxes, fixing and linear terms); Remark
   cr-cut-prior against DPK Theorem 4 and BNW footnote 2 (local full texts);
   CORE and Thm cr-search (a)-(d) against Lemma cr-cell and Thm cr-filter as
   now stated in recourse-local.tex; Prop. cr-growth (charging argument,
   lattice count); Example cr-flat; Lemma cr-height against eq:exact-constants
   and Cor. height in exact.tex; Thm cr-exact against Lemma statpoly and
   Prop. accept; Props. cr-submod and cr-greedy (lattice submodularity, greedy
   inequality, Edmonds min-max, LP and its dual, Abel summation, basic dual
   solutions; GLS Theorem 6.4.9 and Lemma 6.5.15 checked in the local copy);
   Remark cr-mixed; Lemma chaincut (threshold encoding, infinite arcs, node and
   arc counts); Thm balanced (a) against CT, TRIAL, Thm certificate (C1)-(C2),
   Thm approx, EX and Thm exact as now stated, and (b) against the bit-length
   paragraph of Appendix A; Cor. core.
3. CONVENTIONS: notation table (calK/calR, v, y, V, delta_i, k_i, ell_i,
   kappa(L,g), J_0, reserved P, r, w_i), algorithm names and first-use
   references, terminology, absence of artifacts and banned phrases (grep).
4. Moved material: lem:balance, lem:cr-height, thm:cr-exact, prop:cr-submod,
   prop:cr-greedy keep their labels; the proofs of lem:cr-charge (folded into
   prop:cr-growth), of the old balanced case L<=0 (now the sentence after
   def:balanced plus the P=empty branch of CT) and of lem:chaincut survive.
   No reference to a deleted label remains in any section file.

### Problems found and fixed

- Thm cr-exact and the "Exact output" paragraph ran CORE "until
  U - min{lambda_j,U} < Omega^{-2}", but CORE stops on a non-strict test
  (<= eps), and Prop. accept needs a strict gap. Now: accuracy
  eps = Omega_K^{-2}/2 and level limit J = first level with e_J <= eps; the
  proof states that CORE stops by level J with U - beta <= eps < Omega_K^{-2}.
- Thm cr-exact proof used "the set T of coordinates in (0,1)" (T is the tree;
  CONVENTIONS reserve J_0) and attributed the face argument to Cor. height(a).
  Now: a vertex v of the stationary polytope of a minimizer is a minimizer by
  Lemma statpoly(b), and the Hessian block on J_0(v) is positive definite by
  Lemma statpoly(c).
- Prop. cr-greedy: the convex combination was called w (reserved for widths
  w_i(v), w(J)) and the proof of (a) used prefixes P_s (P is reserved).
  Renamed w -> \bar a; (a) now uses positions l_s with i_s = pi(l_s) and
  prefixes S^pi_{l_s-1}, and states where Phi-hat(empty)=0 is used.
- Example cr-flat used r for the number of pairs (r is the private-block count
  of Section 7); now "k even" with t = 1..k/2.
- Thm balanced proof (a): the list of results "depending on F only through"
  was imprecise and omitted the branch of CT for P = empty (minimization over
  prod{ell_i,u_i}, which is also a grid problem). Rewritten: the tree
  decomposition enters CT, EX and the cited proofs only through Lemma dp,
  including that branch; the rest uses F directly. The growth clause now
  reads "under weighted growth, the success of a trial with
  2^mu <= 6 sqrt(kappa-bar)", matching Thm approx(b).
- Work count (Appendix D) and Cor. core used 2^mu <= 6 sqrt(kappa) without
  justification (Thm approx(b) is stated with kappa-bar). Added: point growth
  with constant g gives weighted growth with gamma = g/L since
  ||d||_L^2 <= L||d||^2, so kappa-bar <= kappa; the L = 0 case (one cut); the
  trial count (at most log2(6 sqrt(kappa))); infinite capacities replaced in
  computation by one plus the sum of finite capacities (changes neither the
  minimum cuts nor the flow value); "CT (Algorithm ct)" and "EX (Algorithm ex)"
  at first use in the appendix.
- Lemma chaincut: G_i subset R -> G_i subset Q (the lemma claims rational
  operations).
- Lemma cr-height proof: "1/2 H_ii and H_ij for i,j in K" -> "1/2 H_ii for
  i in K, H_ij for i<j in K" (monomial coefficients).
- Remark cr-cut-prior: "Without (R1) the conditional problem is a continuous
  submodular box QP" is false when residual coordinates are integer; now
  restricted to continuous residual coordinates and phrased as "submodular
  after sign changes".
- Smaller wording: y(z) "ranges over all residual endpoint vectors"; in the
  cut identity proof "exactly one of the arcs i->j, j->i when z_i != z_j, none
  otherwise"; Thm cr-search proof cites Thm cr-filter with
  \underline V = V and eta = 0 (recA's notation); "CORE stops at the latest at
  the first level with e_j <= eps, provided that J is at least this level";
  the sentence after Cor. core now says "point growth of F is needed instead
  of growth of V in the core coordinates" (replacing "growth of F in all
  coordinates").

### Checks run (local, targeted)

- `python3 -B process/w3/checks/recB-cuts.py`: all 4 checks pass.
- `python3 -B process/w3/checks/recB-exact.py`: all checks pass.
- New `python3 -B process/w3/checks/recB-verify-checks.py` (Fractions; scipy
  floats only for the LP in item 4): all pass.
  1. Example cr-flat: CORE simulated for k=2 (levels 0-6) and k=4 (levels
     0-3); at every level U = 0, lambda_j = -e_j and at least 2^{jk/2} cells
     are retained.
  2. Lemma cr-height, sharper than recB-exact.py: 712 endpoint values on 150
     random instances with k <= 3 and residual bounds of denominators up to 5;
     Delta_K clears every monomial coefficient of F_y, W <= Omega_K, and W
     divides Delta_K rho^2 with rho = Delta_K det(hat H_JJ) for the face that
     yields the minimizer; the 1/8 example.
  3. Thm cr-exact with eps = Omega_K^{-2}/2: 12 instances stop by level J,
     pass the acceptance test of Prop. accept and output OPT.
  4. Prop. cr-greedy(c): on 40 submodular set functions (m <= 4), the dual LP
     value equals min hat Phi and the primal LP value equals -min hat Phi.
- `latexmk -pdf -interaction=nonstopmode -outdir=build/recB-verify main.tex`:
  no errors, no undefined references or citations, no overfull boxes in the
  whole log. Pages: 7.4 p. 39, 7.5 p. 43, Section 8 p. 45, Appendix D
  pp. 108-111.
- No project-wide verification and no CI inspection.

### Remaining

- Request to recA/coordinator (recourse.tex roadmap) still open: add
  "(Remark~\ref{rem:cr-mixed})" after "the extension of the cut oracle to
  concave--convex residuals". Optional intro sentence for the front group as
  in request 4 above.
- Notation kept on purpose: B(hat Phi) for the base polytope (standard, local,
  always with an argument, so no clash with bags B_t); K = O(sqrt(kappa) log n)
  in Cor. core is asymptotic for n >= 2 (the exact value is
  K_{mu*} <= 60 sqrt(kappa) ceil(log2(n_P+2))).
- Thm balanced(b) states the CT bound under point growth (as intro and
  related.tex quote it); the proof gives it under weighted growth with
  kappa-bar as well. Not changed, to keep the statement quoted elsewhere.
- Dependencies on other groups' statements (exact.tex: eq:exact-constants,
  Lemma statpoly(b),(c), Cor. height(b), Prop. accept with Omega', Thm exact;
  growth.tex: Thm approx(b) with 2^{mu*} <= 6 sqrt(kappa-bar), K_mu; Appendix A
  bit lengths; recourse-local.tex: Lemma cr-cell with per-coordinate e_B and
  Thm cr-filter with \underline V and eta) match the tree at the time of this
  verification.

## Verification, second pass (recB-verify, 2026-10-03)

Scope: the four recB files, against `assign/recourse.json` (68 ids;
`assign/recB-verify.json` still does not exist), CONVENTIONS, the
pre-revision copies in `sections-before-w3/`, and the current statements in
other groups' files that recB cites.

### What was checked

1. Adjudications. I re-checked every row that touches recB files (F7, F9,
   F10, F11, F12, F13, F20, F24, F25, F26, F29, F30, F34, F35, F41, F42, F49,
   F59, F60, F63, F65, F67, F70, F71, F72, F79, F81, F84, F89, F91, F93, F94,
   F113, F117, F119, F120, F123, F129, F130, F131, F150) against the files.
   Every ACCEPTED fix is present. The MODIFIED and REJECTED decisions are
   justified: F130 (the shared binary cut identity instead of moving Lemma
   chaincut), F131 (CONVENTIONS keeps 7.5 in Section 7), F71 (CORE,
   Theorem cr-search, is what needs an exact oracle). The N/A rows concern
   only other groups' files. R6 Rewrites 14, 15 and 16 (recB lines) are
   applied.
2. Mathematics, line by line, re-derived: Lemma balance (odd cycle of
   positive entries), Lemma cr-endpoint, Prop. cr-cut(a) (identity
   `omega z_i z_j = omega/2 (z_i+z_j) - omega/2 |z_i-z_j|`, cut accounting,
   `rho z = max{rho,0}z + max{-rho,0}(1-z) + min{0,rho}`) and (b); Thm
   cr-oracle (weak duality, Edmonds-Karp arc and node counts, integrality
   after scaling, stability under subboxes, fixing and linear terms); Remark
   cr-cut-prior against DPK Theorem 4 (its assumptions 1-3) and BNW
   footnote 2 and its Padberg Prop. 10 sentence, in the local full texts;
   CORE and Thm cr-search (a)-(d) against Lemma cr-cell and Thm cr-filter as
   they now stand in recourse-local.tex; Prop. cr-growth (charging, lattice
   count, `V(v*)=OPT` implied by the hypothesis); Example cr-flat (the first
   level with `e_j <= eps` has `4^j >= k/(4 eps)`, giving
   `Omega(eps^{-k/4})`); Lemma cr-height against `eq:exact-constants`,
   Cor. height(b); Thm cr-exact against Lemma statpoly(b),(c), Prop. accept
   and the level count `J = O(log Omega_K + log(kL) + 1)`; Props. cr-submod
   and cr-greedy (lattice submodularity, diminishing returns, Edmonds'
   min-max, the LP and its dual derived again, Abel summation with weights
   summing to one, basic dual solutions with at most m+1 positive weights);
   Remark cr-mixed; Lemma chaincut (threshold bijection, telescoping
   formulas, sign of `H_ij delta_{i,l} delta_{j,l'}`, infinite arcs, node and
   arc counts); Thm balanced (a) against CT, TRIAL, Thm certificate (C1),
   (C2), Thm approx(a),(b), Thm transfer, Thm exact and EX; the work count
   against Lemma states, the caps `K_mu` and the bit-length paragraph of
   Appendix A; Cor. core.
3. Moved or deleted material, compared with `sections-before-w3/`. Nothing
   proved was lost unintentionally: lem:cr-charge is inside the proof of
   prop:cr-growth; the old Thm balanced(1) (`L <= 0`) is the sentence after
   def:balanced together with the `P = empty` branch of CT; the old
   "fewest interior coordinates" height argument is replaced by
   cor:height/lem:statpoly; only the smoothed count (CONVENTIONS) and the
   optional `S_0^3` denominator variant were removed. No section file
   references a deleted label (grep, excluding the dropped
   appendix-smoothed.tex).
4. CONVENTIONS: notation (calK/calR, v, y, V, delta_i, k_i, ell_i,
   kappa(L,g), J_0, K, W of Prop. accept), algorithm names with first-use
   references per section (CORE, CT, EX, REC), terminology ("nodes per
   coordinate"), no banned phrases, artifacts or British spellings (grep).

### Problems found and fixed in this pass

- Thm cr-search, proof of (b),(c): it applied Thm cr-filter "with eta = 0",
  but recA has renamed the oracle error of Thm cr-filter to
  `\varepsilon_{\mathrm{or}}`. Now "`\varepsilon_{\mathrm{or}}=0`".
- Thm cr-search, proof of (a): "its child containing x*_K" assumed a unique
  child; a point on a cell face lies in several. Now "every child of C that
  contains x*_K belongs to Q_{j+1}".
- "Exact output" paragraph (7.4): the denominator bound for OPT needs (R1)
  (Lemma cr-height), but the paragraph follows the general CORE material and
  said only "For rational data". Now "Under (eq:cr-class) and for rational
  data".
- Appendix D.1: `Lambda_c`, `Lambda_e` were "a positive common denominator",
  which does not give `log Omega_K = O(I^2)`. Now "the least positive common
  denominator ...; both have O(I) bits".
- Lemma cr-endpoint: "a box with inward-rounded integer bounds" read as if
  all bounds were integers. Now "a box whose bounds are integers for integer
  coordinates".
- "label" was used in Thm cr-oracle and Remark cr-mixed without being
  defined. It is now defined where `y(z)` is introduced ("For a label
  z in {0,1}^R ...").
- Section 7.5: "(R2) says that the residual block of H is balanced" applied
  "balanced" (defined for quadratics) to a matrix block. Now "(R2) says that
  F becomes balanced once the core coordinates are fixed".
- Thm balanced: the comma in "Run CT, and EX (...), with" is removed. In
  (a), "each dynamic program is replaced by a minimum cut" is wrong, because
  one stage needs up to `1+nK_mu` cuts. Now "the dynamic programs are
  replaced by minimum cuts with flows of equal value". In the proof of (a),
  "these statements hold verbatim" also covered the operation counts of
  Lemma dp and Thm approx(b), which do change. Now "the validity and
  termination statements of these results hold verbatim, ...; only the
  operation counts change".

### Checks run (local, targeted; no project-wide verification, no CI)

- `python3 -B process/w3/checks/recB-cuts.py`: all 4 checks pass.
- `python3 -B process/w3/checks/recB-exact.py`: all checks pass.
- `python3 -B process/w3/checks/recB-verify-checks.py`: ALL OK.
- New `python3 -B process/w3/checks/recB-verify-cutbits.py` (Fractions, brute
  force), ALL OK. It checks three claims that no earlier script covered:
  1. Work count of Thm balanced(b): replacing every infinite capacity by
     1 + (sum of finite capacities) keeps the minimum cut value and the set
     of minimum cuts (150 random chaincut networks, all cuts enumerated).
  2. With grid nodes of denominators dividing `Gamma_X 2^alpha` and
     `chi_i = -d_i`, every capacity of Lemma chaincut has a denominator
     dividing `8 Gamma_F Gamma_X^2 4^alpha` (120 instances, nonuniform grids).
  3. Cor. core: beta and every min-marginal, computed as minima over core
     node vectors of chaincut problems, equal brute force (60 instances, F
     not balanced on the core).
- `latexmk -pdf -interaction=nonstopmode -outdir=build/recB-verify main.tex`
  (after the edits): no errors, no undefined references or citations, no
  overfull or underfull boxes in the log. 7.4 starts on p. 39, 7.5 on p. 43,
  Section 8 on p. 45, and Appendix D is on pp. 108-111.

### Remaining

- Coordinator/recA (`recourse.tex`, roadmap): still lacks the reference to
  "(Remark~\ref{rem:cr-mixed})" after "the extension of the cut oracle to
  concave--convex residuals". This is request 1 above.
- Kept on purpose: `r_{ij}` (capacities) and the LP slack vector `r` in
  Prop. cr-greedy, although `r` without subscript counts private blocks in
  Section 7.1; `lambda_j` (CORE) and `lambda_pi` (weights) in different
  subsections of Appendix D; `Phi` for the binary function minimized by a cut
  in Prop. cr-cut(a), Lemma chaincut and Appendix D.2. Each use is local
  and defined at the place of use.
- `K = O(sqrt(kappa) log n)` in Cor. core is asymptotic for `n >= 2`. The
  exact bound is `K_{mu*} <= 60 sqrt(kappa) ceil(log2(n_P+2))`. Section 5
  uses the same notation.
- The cross-group dependencies listed under "Unresolved" above
  (`exact.tex`, `growth.tex`, Appendix A, `recourse-local.tex`) still hold
  for the files in the tree at 11:53 on 2026-10-03.
