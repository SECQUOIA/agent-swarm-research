# W4 review C-consistency: global consistency

Paper: "Decomposition-aware global optimization: certified coordinate grids,
conditional recourse, and structural limits". Sources: `main.tex`,
`sections/*.tex` as of 2026-10-03; numbering from `/tmp/dpaper/out/main.aux`
(123 pages). Line numbers refer to the `.tex` files.

## Verdict

The paper is globally consistent. Every claim in the abstract, Theorem 1.1,
Theorem 1.2, Table 1, the extension paragraphs of the introduction and the
conclusion matches the corresponding theorem in hypotheses, parameters,
constants and bounds. All cross-references resolve and point to objects of the
announced type. No reference points to a deleted result, and every number
quoted in more than one place agrees, including with the raw experiment files.
The algorithm names TRIAL, CT, REC, EX, UC, CORE, TU-GRID, TU-EXACT, PROX and
DISC are used uniformly. The W2 consistency findings (R5 M1–M22, m1–m23) are
fixed, except where CONVENTIONS made a deliberate choice (for example `J` for
the free set in REC).

The remaining problems are minor:

* one table row uses the reserved `κ` where `κ_V` is meant;
* one summary bullet in Section 10 overstates Proposition 7.5;
* several reserved symbols take a second meaning, some inside one section
  (`s`, `e_i`, `m`, `r`/`r_i`, `η`, `P`, `q`, `ν`);
* two symbols are used before they are defined;
* a class used in theorem statements is defined inside a remark;
* an orphan source file remains;
* one sentence uses "width" in two senses.

None of these affects a main result.

## Findings

### C-consistency-1 (minor): Table 1, Theorem 7.10 row, uses the reserved `κ` instead of `κ_V`

*Location:* `intro.tex:331-335` (Table `tab:results`, row `thm:cv`).

*Problem:* The parameter column reads "`p, κ(L^+,g)`, `L^+` reduced", but the
bound column reads `f(p,κ)κ^C(I+q+1)^C` and `f(p,κ)κ^{C_1}(I+1)^{C_1}`. Table 2
reserves `κ` for `κ(L,g)`, where `L` is the largest **direct** coordinate
curvature of `F`. That is exactly the quantity Theorem 7.10 avoids. The theorem
states `f(p,κ_V)κ_V^C(I+q+1)^C` with `κ_V = κ(L^+,g)` (`recourse-convex.tex:199-204`).
The row above it, for Theorem 7.2, writes `κ_V` correctly. Read with the
paper's own notation, the row states the weaker, uncancelled parameter.

*Fix:* In the parameter column write "`p`, `κ_V=κ(L^+,g)` (`L^+` reduced)". In
the bound column write "`f(p,κ_V)κ_V^{C}(I+q+1)^{C}`; exact
`f(p,κ_V)κ_V^{C_1}(I+1)^{C_1}`; `2^{O(p)}poly(I)` if `L^+=0`".

### C-consistency-2 (minor): the Section 10 roadmap says that bag-local corrections are not valid lower bounds

*Location:* `limits.tex:39-44` (the bullet "Local corrections").

*Problem:* "Corrections charged to the coordinates of one bag are not valid
lower bounds (Proposition 7.5 …)". As written, this contradicts Theorem 7.4
(`thm:cr-filter`): bag-local corrections **are** valid when the outside
coordinates are minimized exactly or with a certified error. Proposition 7.5
refutes only constant corrections combined with **grid** min-marginals. The
introduction (`intro.tex:227-230`) and Section 10.7 (`limits.tex:678-683`)
state the qualification correctly; only the roadmap bullet drops it.

*Fix:* Replace the first sentence of the bullet with: "Corrections charged
only to the coordinates of one bag are not valid lower bounds when the other
coordinates are optimized on the grid (Proposition~\ref{prop:star} in
Section~\ref{sec:recourse}); with exact or certified recourse they are
(Theorem~\ref{thm:cr-filter})."

### C-consistency-3 (minor): reserved `s_i` and the letter `e_i` take further meanings inside Section 6

*Location:*
* `s` as a minimizer: `exact.tex:64-67` (Definition 6.2: "For `s∈𝒮` … `x_i=s_i`"),
  `72-80`, `102`, `135`, and `204-226` (Lemma 6.8: "`s_i=ℓ_i`", "`|s_i-y_i|`");
  also `appendix-recourse-cuts.tex:73-74`.
* `s` with its reserved meaning in the same section: `appendix-localized.tex:86`
  (`h_j=s2^{-j}`, `log_2(s/h^*)`) and `appendix-boundary.tex:174`.
* `e_i` with three meanings in Section 6:
  * the fixed endpoint `e_i ∈ {ℓ_i,u_i}` (`exact.tex:211-225`);
  * the unit vector (`exact.tex:421`, Lemma 6.20);
  * the Section 5 exponent `4^{e_i-1}<L_i≤4^{e_i}` (`exact.tex:459,464`, proof of
    Corollary 6.22, in the same subsection 6.6 as Lemma 6.20).
* Two more meanings of `e_i` elsewhere: `e_i(v_i;x_i)` (`optsets.tex:270-276,352`)
  and the endpoint `e_k` (`appendix-boundary.tex:181`).

*Problem:* Table 2 reserves `s_i=u_i-ℓ_i`, and Section 5 uses it two pages
earlier (`growth.tex:37`, "`2^Er_i≥s_i`"). In Lemma 6.8, "`s_i=ℓ_i`" therefore
reads as "width equals lower bound". In 6.6, `e_i` changes meaning between a
lemma and the next corollary's proof.

*Fix:*
* Write the minimizer in Definition 6.2, Lemma 6.3, Corollary 6.4, Lemma 6.8
  and the proof of Theorem D.2 as `x^\circ∈𝒮` (coordinates `x^\circ_i`). This
  letter is unused in Sections 6 and D.
* In Lemma 6.8 write the fixed endpoint as `ξ_i∈{ℓ_i,u_i}`. `ξ` is unused in
  Section 6.
* In the proof of Corollary 6.22 write "the exponents `e_i` of
  Section~\ref{sec:growth} (`4^{e_i-1}<L_i\le4^{e_i}`)".

### C-consistency-4 (minor): `m` has three meanings in Section 8, and `r`/`r_i` have two meanings across Sections 5, 7 and 8–10

*Location:*
* `m` in Section 8:
  * number of rows of `A` (`constraints.tex:32,40,108,164,234,425,491`);
  * min-marginals `m_i`, `m_k` (`230-254`);
  * the minimizer coordinate `m∈(0,1)` of Proposition 8.15 (`594-631`;
    `appendix-tu.tex:319-322`).
* `r_i`:
  * the Section 5 scale `r_i=2^{-e_i}` (`growth.tex:35-38,104`; Appendix A);
  * the number of points of `𝒮_i` (`constraints.tex:337-345,375,400`).
* `r`:
  * the number of private blocks (`recourse-valuefn.tex:54-58`,
    `recourse-convex.tex:16`, `appendix-recourse-convex.tex:21,29,268`);
  * the number of optimal values per coordinate (`intro.tex:257,274`, Table 1,
    `constraints.tex:429-431`, `optsets.tex:8-9,199`).

*Problem:* In Proposition 8.15 the letter `m` names a point while `m_i` names
min-marginals on the same grids. Table 2 does not list `r`, although Table 1
and the introduction rely on it. The reader meets `r` first as a block count
(Section 7), then as a count of optimal values (Sections 8–9).

*Fix:*
* In Proposition 8.15, the example after it and Appendix E.4, rename the
  point `m` to `μ_0`.
* In Theorem 8.10(b), write `|𝒮_i|` instead of `r_i`; no new symbol is
  needed.
* Add to Table 2: "`r`: largest number of optimal values of a coordinate
  (Sections 8–10); in Section 7, the number of private blocks".

### C-consistency-5 (minor): other reserved symbols reused with a different meaning

*Location and problem:*
* `η`: Table 2 reserves `η_j` for the Section 5 scale (`growth.tex:37`). Section 8
  uses `η` for the TU mesh unit (`constraints.tex:37-43,68`). Section 9.3 and
  Appendix F use `η=Lθ^2/4` for a proximal weight (`optsets.tex:547-556`,
  `appendix-proximal.tex:71-114`).
* `P`: reserved for `{i:L_i>0}`. The proof of Theorem 7.2(b)
  (`appendix-recourse-convex.tex:12-15`) names two polynomials `P_L` and `P`,
  in the same proof that runs CT, whose stage rule uses `n_P`.
* `q`: reserved for the accuracy `2^{-q}`. In Appendix B the same letter is a
  phase index (`appendix-boundary.tex:125-127,208-210`), while the theorem
  there still concerns certified gaps.
* `ν`: negative curvature in `recourse-convex.tex:276`,
  `appendix-recourse-convex.tex:485-541`, `limits.tex:687-698`,
  `conclusion.tex:39` and Appendix G. It is an integer counter in
  `growth-sharp.tex:38-42`, `appendix-growth.tex:82-101` and
  `appendix-tu.tex:249-304`.
* ETH is stated twice with different symbols: "`δ>0`, 3-SAT with `m` variables"
  (`intro.tex:162-164`) and "`c>0`, … `n'` variables" (`limits.tex:282-284`).

*Fix:*
* Proximal weight `η` → `ω_η` (or write `Lθ^2/4` explicitly). Add the TU mesh
  unit `η` to Table 2.
* Polynomials `P_L`, `P` → `π_L`, `π_0`.
* Phase index `q` → `φ` (with `q_*` → `φ_*`).
* Integer counter `ν` → `k_0` in Corollary 5.7, its proof and Lemma E.6.
* State ETH once, with the symbols of Section 10.3, and refer to it from the
  introduction.

### C-consistency-6 (minor): two symbols are used before they are defined

*Location:* `growth.tex:262` (proof of Theorem 5.9: "over the common
denominator `8Γ_FΓ_X^24^α`"); `exact.tex:496` (`B_λ=⌈log_2max{2,C_2/λ_A}⌉`).

*Problem:*
* `Γ_F` is defined only in Appendix A (`appendix-growth.tex:116-117`) and in
  Proposition 6.21. The sentence in the proof of Theorem 5.9 defines `Γ_X` but
  not `Γ_F`.
* `C_2` is defined only in Appendix B (`appendix-boundary.tex:10-15`).

*Fix:*
* `growth.tex:258`: "where `Γ_X` and `Γ_F` are the products of the
  denominators of the box endpoints and of the coefficients".
* `exact.tex:496`: "…in the smallest inward derivative `λ_A` at the active
  bounds, where `C_2` bounds the row sums of `|∂_{ij}F|` over the continuous
  coordinates (Appendix~\ref{app:boundary})".

### C-consistency-7 (minor): the class `𝔇` used in theorem statements is defined inside a remark

*Location:*
* Definition: `optsets.tex:519-520` (Remark 9.11, "Call the instances
  satisfying (a)–(c) the diagonal certificate class `𝔇`").
* Uses: Theorem 9.15(a),(b) (`600-605`), Proposition 9.16 (`624-642`),
  `651-656`, and Appendix F.

*Problem:* Theorem 9.15 and Proposition 9.16 are stated in terms of `𝔇`, but
`𝔇` is defined only in a remark that the theorems do not cite.

*Fix:* Add to the end of Lemma 9.10(iii): "We write `𝔇` for the class of
continuous box QPs for which (a)–(c) hold (the *diagonal certificate
class*)." Shorten Remark 9.11 to start with "Convex box QPs belong to `𝔇`".

### C-consistency-8 (minor): orphan source files

*Location:* `sections/appendix-smoothed.tex` (76 lines, labels `app:smoothed`,
`lem:cr-law`, `thm:cr-smoothed`, `rem:cr-smoothed`); `figures/E3_plateau_vs_n.pdf`.

*Problem:* CONVENTIONS §1 deletes the smoothed core count. No file inputs the
appendix, and the paper never refers to it. The file still sits in
`sections/` and would ship in a source bundle (arXiv or journal). Its first
sentence, "remove this effect", dangles. The E3 figure is unused, because E3
is reported in text only.

*Fix:* Remove both files from the submission tree, or move them to
`process/`.

### C-consistency-9 (minor): "width" has two meanings in one sentence of the introduction

*Location:* `intro.tex:253-257`.

*Problem:* "the algorithm is polynomial for fixed width when … the box widths
measured in mesh units (`s/η`) … are polynomially bounded". The first "width"
is the decomposition width `p-1`; the second is the box width `s`. Section 8.5
(`constraints.tex:458-461`) says "for fixed `p`".

*Fix:* "the algorithm is polynomial for fixed bag size `p` when …".

## What was checked and found correct

**Abstract, Theorem 1.1 and Theorem 1.2 against the body.**
* Theorem 1.1(a)–(c) against Theorems 4.7, 5.9 and 6.14, Lemma 5.5 and
  Remark 5.10: the same hypotheses (explicit rational quadratic, mixed box,
  `L_i=max{0,∂_iiF}`), and the same bounds:
  * `f(p,κ̄)(I+q+1)^5` with `f=c_0(c_1p√κ)^pκ(1+log_2κ)^2`;
  * `O(√κ̄ log(n+2))` nodes, via `K_{μ*}≤60√κ̄⌈log_2(n_P+2)⌉` and
    `2^{μ*}≤6√κ̄`;
  * `f_1(p,κ)(I+1)^{C_1}`.
* The function `f` is identical in the intro, Theorem 5.9, `limits.tex:188`,
  the conclusion and Appendix G.
* Theorem 1.2(a)–(d) against Proposition 10.1, Corollary 10.2,
  Propositions 10.5, 10.6 and 10.3 (bag size three, `log κ=O(I)`, `κ̄≤κ≤2`,
  `f(p)(κI)^{p/ψ(p)}`, `(κ/(8p))^{p/2}-1`, `κ≥8p`).
* The sentences after Theorem 1.2: exponent `p/2+O(1)` (Appendix G derives
  `κ^{p/2+2}`), the oracle gap `(C√p log(p+2))^p`, and `κ≤80` for the chain.
* Abstract claims, including that the rETH bound needs no qualifier because
  integer box QPs lie in the stated class.

**Table 1, every row against its theorem.**
* The `valuefn` row (`κ_V=κ(L^V,g)`; `C`, `C_1` depend on the polynomials).
* The `cr` rows (`8^k(1+√(kκ_𝒦))^k poly(I)`; one max-flow per query).
* The `balanced` row (`(nκ(I+q+1))^{O(1)}`).
* The TU row (`K_0≤max{K_Z,s/η+1}`; `K=max{K_Z,r(5+⌊2√(n_cκ_c)⌋)}`;
  `O(I+q)` levels).
* The `cells` row (`K_S=12r(2√(nκ_S)+1)`).
* The `endpointset` and `diagdiscovery` rows.
* The four lower-bound rows.
* The only mismatch is C-consistency-1.

**Extension paragraphs of the introduction and the conclusion.**
* Recourse: Lemma 7.1, Theorems 7.2 and 7.4, Proposition 7.5, Theorem 7.10,
  Proposition 7.9(c), Theorems 7.17, 7.20 and 7.26, Proposition 7.13.
* TU: Theorems 8.12 and 8.14, Section 8.7, Proposition 8.15, Example 8.16,
  Remark 8.17, Proposition 10.10.
* Several minimizers: Proposition 9.1, Theorems 9.4 and 9.7, Corollary 9.8,
  Theorem 9.15.
* Snapping threshold
  `k=poly(I)+max{0,log_2(1/g_S)}`: Theorem 6.9 and Remark 6.10.
* The conclusion's open problems against Corollary C.8, Propositions 7.13,
  8.15 and 10.8, Example 8.16, Theorem 8.12 and Proposition B.6.
* The roadmaps of Sections 6, 7, 8, 9 and 10.

**Notation.**
* No `l_i` anywhere: only `\ell_i`; `l_s` in Appendix D is an index.
* `κ`, `κ̄`, `κ_S`, `κ_c`, `κ_V`, `κ_𝒦`, `κ̂` are used with their defined
  meanings everywhere except C-consistency-1. Section 9.3, Appendix F and
  Section 10.5 use `κ_S`; Section 8 uses `κ_c`; Theorem 7.26 and
  Corollary 7.27 use `κ`, with `κ̄≤κ` noted.
* `γ` is used only for weighted growth.
* The "Defined in" pointers of Table 2 are correct.
* The CONVENTIONS renames are applied:
  * `ζ` for gradients;
  * `\underline V`, `ε_or`;
  * `Ĥ`, `I_C^+`;
  * `𝒦`/`ℛ` throughout Section 7;
  * `E_t`, `ξ_t`, `Q_η`, `L_i^+`, `g_0`, `λ_A`/`B_λ`;
  * `δ_i` for signed widths, `k_i` for `|G_i|-1`;
  * `R_TU`, `Ω_TU`, `τ_TU`, `N_Π`, `ϑ`, `V_B`, `V^G`.

**Cross-references.**
* All `\ref` targets exist.
* A script compared each "Theorem/Lemma/Proposition/Corollary/Remark/Example/
  Definition/Algorithm/Section/Appendix/Table/Figure~\ref" with the cleveref
  type in `main.aux`: no mismatch.
* No reference to a deleted result: `lem:cr-semiconcave`, `rem:cluster`,
  `rem:tu-hybrid`, `lem:cv-energy` and `lem:cv-envelope` are gone, and
  `eq:cv-energy` exists.
* Unreferenced labels are only sections, equations and remarks.
* Every "Section X shows/gives/treats/uses …" sentence checked is true, and
  each forward pointer to an appendix proof leads to that proof.
* `latexmk` log: no undefined or multiply defined references, no overfull
  boxes, no BibTeX warnings.

**Numbers quoted in several places.** They agree:
* `κ≤80` and `2^{m-1}` pieces; chain table vs `experiments/chain/results.csv`;
  warm-start `-2%…+8%`;
* 11 certified-growth instances (sum of Table 3); 28 + 11 + 1 = 40;
* S1 numbers in Section 6.5 vs 11.6: 29/30, nine and five stages, 40–72,
  542;
* the threshold range `2^{-315}…2^{-21}` vs 21–315 bits;
* 21 E5 instances and nine `n≥32` paths;
* replay ratio 0.81–2.54, recomputed from E6, chain and recourse CSVs
  (maximum 50.927/20.019);
* the implementation cap `12.5×` and `0.4%`;
* `16.8√(nκ)+3`;
* `K_S` with `r=1` in `growth-sharp.tex:53`;
* `κ_S≤40`, `123`, `8` vs `2M+8`, `(4M-1/2)/3`, `2(3+√5)`, `21/4`.

**Exact checks** (`process/w4/checks/C-consistency-numbers.py`, Python
`fractions`):
* the 11-node graded grid with center 3/10: nodes as printed, only `0` and `1`
  common with its reflection, largest interval `3831/20480`,
  `δ=27/1280`;
* Example 8.16: grid `{0,1,9/4,3}`, the corrections, and the seven
  corrected values (minimum `31L/64`);
* the constants in the proofs of Lemmas 5.5 and 5.11 (`7.296<7.3`,
  `φ(1)<16.3`, `φ(2)<18.6`, `ψ(1)<12.4`, `ψ(2)<14.4`, `4.148<4.15`);
* `0.23^2/20>1/379`;
* `(√(2(n_c-2))+1)^2≥n_c`;
* the moment-relaxation values `1/4-(2r+1)/(16r)=λ(r-1/2)`.

By hand:
* Remark F.1: `Δ=128`, `R=2^{23}`, `τ=2^{-26}`, `J=28,28,29`, eigenvalue
  `-1/64`;
* the claims of the `n=2` example after Definition 3.2 (`κ≥2^{k+2}`), the
  example in Remark 9.11, and Example C.2;
* Proposition 10.8's example certificate (`n=2`, `ε=1/50`).

**Terminology.**
* "nodes per coordinate" and "table entries" are used as fixed.
* "graded"/"grading" is used; "geometric" and "slope" do not appear.
* No drafting markers (TODO, ??, report, agent) and no banned filler phrases.
