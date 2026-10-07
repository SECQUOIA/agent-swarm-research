# Adjudication of the W2 review findings

Every one of the 222 findings of the second review round (W2, `process/w2/`) was
assigned to the owner of the affected files in revision round W3, decided, and
then checked by an independent verifier for that file group. The full decision
tables, with the change made for each finding, are in `process/w3/reports/<group>.md`
(and `<group>-verify.md`). Binding conventions for the revision:
`process/w3/CONVENTIONS.md`.

Decision key: ACCEPTED = fixed as proposed; MODIFIED = fixed differently or
partly, with the reason recorded; REJECTED = no change, with the reason recorded.
A finding that touched several file groups is MODIFIED if any group modified or
rejected its part.

## Totals

| Reviewer | ACCEPTED | MODIFIED | REJECTED | total |
|---|---|---|---|---|
| R1-math-core | 19 | 6 | 0 | 25 |
| R2-math-recourse | 18 | 4 | 1 | 23 |
| R3-math-constraints-sets | 10 | 5 | 0 | 15 |
| R4-math-limits | 17 | 1 | 0 | 18 |
| R5-consistency | 37 | 8 | 0 | 45 |
| R6-writing | 23 | 12 | 0 | 35 |
| R7-literature | 16 | 4 | 0 | 20 |
| R8-computation | 24 | 2 | 0 | 26 |
| R9-referee | 12 | 3 | 0 | 15 |
| all | 176 | 45 | 1 | 222 |

## Critical and major findings

| id | reviewer | severity | location | decision | groups |
|---|---|---|---|---|---|
| F0 | R6-writing | critical | abstract.tex 30-32; intro.tex 110-113 (vs Prop. lim:prop:constraints and the paragraph aft | MODIFIED | front, limits |
| F1 | R6-writing | major | abstract.tex 1-38 | MODIFIED | front |
| F2 | R6-writing | major | intro.tex 36-179 (Main results + Contributions) | ACCEPTED | front |
| F3 | R6-writing | major | intro.tex ~45 (after Definition growth sentence); abstract line 2 | ACCEPTED | front |
| F4 | R6-writing | major | intro.tex 116-118 (Theorem thm:cells claim) | ACCEPTED | front |
| F5 | R6-writing | major | conclusion.tex 12-15 | ACCEPTED | front |
| F6 | R6-writing | major | conclusion.tex 31-33 (open question 1) | MODIFIED | front |
| F7 | R6-writing | major | recourse-balanced.tex 163-164; optsets.tex 45 and 92 | ACCEPTED | optsets, recB |
| F8 | R6-writing | major | exact.tex 3-15 and 19; optsets.tex 234-252 (rem:np) | ACCEPTED | exact, optsets |
| F9 | R6-writing | major | Section 7 (recourse*.tex), esp. recourse-convex.tex 734-798, recourse-mixed.tex, recourse- | MODIFIED | recA, recB |
| F10 | R6-writing | major | cor:height, lem:cv-height, lem:cr-height, cor:tu-height; lem:snap/lem:tu-snap; prop:accept | MODIFIED | coreB, exact, recA, recB, tu |
| F11 | R6-writing | major | related.tex 87-106 vs growth.tex 243-254 (rem:cluster); related.tex 'Exact rational output | MODIFIED | coreA, coreB, exact, front, recA, recB, tu |
| F12 | R6-writing | major | throughout (examples: setting.tex P vs exact.tex P=Delta H; recourse-valuefn R vs recourse | MODIFIED | coreA, coreB, exact, recA, recB |
| F13 | R6-writing | major | growth.tex, optsets.tex 45, recourse-balanced.tex 3/96/113, recourse-convex.tex 6/354, lim | ACCEPTED | computation, coreA, coreB, exact, limits, optsets, recA, recB, tu |
| F14 | R6-writing | major | optsets.tex 540-556 (thm:diagdiscovery), 588 | ACCEPTED | optsets |
| F15 | R6-writing | major | recourse-valuefn.tex 32-103 | ACCEPTED | recA, recB |
| F35 | R9-referee | major | Whole paper (104 pp.); Section 7 (pp. 24–48), Section 8 (pp. 48–59), Section 9 (pp. 59–68) | MODIFIED | recA, recB, tu |
| F36 | R9-referee | major | abstract lines 30–32; intro.tex:109–114; constraints.tex:419–428; limits.tex:591–595 | MODIFIED | front, limits, tu |
| F37 | R9-referee | major | intro §1.1; setting.tex §3.3; setting-growthcert.tex:42–58 (Lemma growthcert, Remark nonco | ACCEPTED | coreA, coreB, front |
| F38 | R9-referee | major | abstract; intro.tex:72, 152; conclusion.tex:9; growth.tex Remark rem:fpt | ACCEPTED | coreB, front |
| F39 | R9-referee | major | computation.tex:100–158 (Tables 1–2); exact-localized.tex:96–98; experiments/results/summa | ACCEPTED | computation, exact |
| F40 | R9-referee | major | sections/abstract.tex (≈370 words); intro §1.1 vs §1.2; table of contents | ACCEPTED | front |
| F41 | R9-referee | major | recourse-convex.tex:14 (𝓡 = retained) vs recourse-cuts.tex:7–9 (𝓡 = residual) vs recourse- | MODIFIED | coreA, coreB, exact, recA, recB |
| F50 | R5-consistency | major | abstract.tex 30-32; intro.tex 109-114; Thm 8.11 (thm:tu-approx); Rem 8.22 | ACCEPTED | front, tu |
| F51 | R5-consistency | major | conclusion.tex 12-15, 38-40; Remark 5.8 (growth.tex 237-239) | ACCEPTED | coreB, front |
| F52 | R5-consistency | major | limits.tex 14-17 (opening bullets); abstract.tex 24-25; intro.tex 129-131; Prop 10.7 (prop | ACCEPTED | front, limits |
| F53 | R5-consistency | major | optsets.tex 229-231 (Remark 9.4) vs limits.tex 443-461 (Prop 10.9) | MODIFIED | optsets |
| F54 | R5-consistency | major | conclusion.tex 30-33 (open problem 1) | MODIFIED | front |
| F55 | R5-consistency | major | intro.tex 121-123; Thm 9.12 (optsets.tex 550-555, 571-578); Prop 9.13 (606, 626); remark a | ACCEPTED | front, limits, optsets |
| F56 | R5-consistency | major | recourse-convex.tex 341-342 (eq:cv-L), 380 (proof of Thm 7.18(iii)); Prop 7.24 proof 640-6 | ACCEPTED | recA, recB |
| F57 | R5-consistency | major | growth.tex 155-158; appendix-boundary.tex 17-23, 99, 180; appendix-localized.tex 2-16; exa | ACCEPTED | computation, coreB, exact |
| F58 | R5-consistency | major | setting.tex 50 (P={i:L_i>0}); exact.tex 31 (P=ΔH); constraints.tex 435 (P=ΔH); Def 7.11 /  | ACCEPTED | coreA, coreB, exact, optsets, recA, recB, tu |
| F59 | R5-consistency | major | setting.tex (𝒮); exact.tex 27 (S); constraints.tex 65 ('S=𝒮'); optsets.tex 3,14 vs 36,175; | MODIFIED | coreA, coreB, exact, limits, optsets, recA, recB, tu |
| F60 | R5-consistency | major | Section 7: recourse-valuefn.tex 2-5, 32-44, 105-120; recourse-convex.tex 13-45; recourse-c | MODIFIED | recA, recB |
| F61 | R5-consistency | major | setting.tex 79-83 (γ weighted); setting-growthcert.tex 12-13, 29, 54-55 (γ Euclidean); exa | ACCEPTED | coreA, coreB, exact |
| F62 | R5-consistency | major | constraints.tex: N 40/116/140/483/556; K 219/397-400/507; M 215/449; E 63/493; W 62/526/54 | ACCEPTED | tu |
| F63 | R5-consistency | major | recourse-cuts.tex 38 and recourse-mixed.tex 10 (d_i signed widths) vs recourse-balanced pr | ACCEPTED | coreA, coreB, exact, optsets, recA, recB |
| F64 | R5-consistency | major | exact.tex 10-15 and 19; placement of exact-localized.tex (Section 6.6) | ACCEPTED | exact |
| F65 | R5-consistency | major | optsets.tex 45, 92 (FG); growth.tex 41, 166; appendix-boundary.tex 27, 98; limits.tex 281, | ACCEPTED | computation, coreB, exact, limits, optsets, recB |
| F66 | R5-consistency | major | optsets.tex 540-547 (Thm 9.12); appendix-proximal.tex | ACCEPTED | optsets |
| F67 | R5-consistency | major | Section 6 (Def 6.2, Lemma 6.3, Cor 6.4, Prop 6.6, REC, Lemma 6.7, EX, Rem 6.12) vs Section | MODIFIED | exact, recA, recB, tu |
| F68 | R5-consistency | major | Lemma 7.2 (recourse-valuefn.tex 46-58); Lemma 9.2 (optsets.tex 141-168); Prop 8.19 (constr | MODIFIED | coreB, front, limits, optsets, recA, recB, tu |
| F69 | R5-consistency | major | recourse-valuefn.tex 32-103 | ACCEPTED | recA, recB |
| F70 | R5-consistency | major | setting.tex 72-84 (Def 3.2); exact.tex 223; constraints.tex 67-71; optsets.tex 12-16; Lemm | ACCEPTED | coreA, coreB, exact, limits, optsets, recA, recB, tu |
| F71 | R5-consistency | major | recourse-mixed.tex (Section 7.5, Props 7.40-7.41) | ACCEPTED | recB |
| F95 | R3-math-constraints-sets | major | sections/optsets.tex:39-51 (statement) and :91-100 (proof), Proposition 9.1 prop:twocenter | ACCEPTED | optsets |
| F96 | R3-math-constraints-sets | major | sections/intro.tex:113-114; sections/constraints.tex:12-15, 674-679, 729-730 | ACCEPTED | front, tu |
| F97 | R3-math-constraints-sets | major | sections/abstract.tex:30-32; sections/intro.tex:111-113 | ACCEPTED | front |
| F110 | R2-math-recourse | major | sections/recourse-convex.tex l.53-83 (Def. def:leaf, checking paragraph l.69), Thm thm:cv( | ACCEPTED | recA, recB |
| F111 | R2-math-recourse | major | sections/recourse-convex.tex Lemma lem:cv-height l.305-334; proof of Thm thm:cv(iii) l.395 | ACCEPTED | recA, recB |
| F112 | R2-math-recourse | major | sections/recourse-valuefn.tex Thm thm:valuefn l.127-131, proof l.138-140 | MODIFIED | recA, recB |
| F113 | R2-math-recourse | major | sections/recourse-valuefn.tex l.2-3,105-118; recourse-convex.tex l.13-41,267,437; recourse | MODIFIED | recA, recB |
| F114 | R2-math-recourse | major | sections/conclusion.tex l.31-32 | MODIFIED | front |
| F133 | R7-literature | major | references.bib @misc entries at lines 279, 303, 443, 672, 696, 731, 978, 1358, 1381, 1558  | ACCEPTED | bib |
| F134 | R7-literature | major | sections/limits.tex:550-583 (Prop. lim:prop:constraints); limits.tex:25-26; intro.tex:134- | MODIFIED | front, limits |
| F135 | R7-literature | major | sections/optsets.tex:334-358 (Thm thm:endpointset), 373-394 (Cor. cor:facecsp), 440-446 (a | ACCEPTED | front, optsets |
| F136 | R7-literature | major | sections/intro.tex:145-148 (contribution (i)) versus sections/grids.tex:149-153 and 225-23 | ACCEPTED | coreA, coreB, front |
| F137 | R7-literature | major | sections/related.tex:55-69 ('Dynamic programming with coarse states') and 35-53 | MODIFIED | front |
| F153 | R1-math-core | major | sections/exact.tex lines 10-15 and 19 (Section 6 intro; 'Throughout Sections \ref{sec:exac | ACCEPTED | exact, front |
| F154 | R1-math-core | major | sections/exact-localized.tex lines 70-74 and Corollary cor:local (lines 76-93); appendix-l | ACCEPTED | exact |
| F155 | R1-math-core | major | sections/growth-sharp.tex lines 45-49 | MODIFIED | coreB |
| F178 | R4-math-limits | major | sections/limits.tex 455-458 and 481-487 (Prop lim:prop:setgrowth); summary sentences at li | ACCEPTED | front, limits |
| F179 | R4-math-limits | major | sections/appendix-boundary.tex 5-8, 17-23 (localization claim), 36-37 and 48-54 (Lemma lem | ACCEPTED | exact |
| F196 | R8-computation | major | sections/computation.tex:72-75; Figure 2 caption :80-84; experiments/figures.py:113-118; e | ACCEPTED | computation |
| F197 | R8-computation | major | sections/computation.tex:95-98 (E3) and the κ=2 point of Figure 2; experiments/instances.p | ACCEPTED | computation |
| F198 | R8-computation | major | sections/computation.tex:25-27, 134-137; solver/exact_output.py:15-37 (rational_heights);  | ACCEPTED | computation, exact |
| F199 | R8-computation | major | sections/exact-localized.tex:95-98 (cites Section 11); experiments/README.md S1 | ACCEPTED | computation, exact |
| F200 | R8-computation | major | sections/computation.tex:220-226 (Limits, QPLIB); conclusion.tex:24-25 | ACCEPTED | computation, front |
| F201 | R8-computation | major | sections/computation.tex:143-179 (SCIP text and Table 2); experiments/run_all.py:196-249,  | ACCEPTED | computation |
| F202 | R8-computation | major | sections/computation.tex:18-25, 70-72; solver/certified_grid.py:412-416; experiments/run_a | ACCEPTED | computation |
| F203 | R8-computation | major | sections/computation.tex:38-39, 192-193; solver/convex_recourse.py:391-508; solver/verify_ | ACCEPTED | computation, recB |
| F204 | R8-computation | major | sections/grids.tex:223-225 ('checking costs about as much as the successful run'); section | MODIFIED | computation, coreA, coreB |

## Modified and rejected decisions with reasons

Reasons are quoted from the group reports (truncated); see the reports for the full text.

- **F0** (R6-writing, critical): [limits] MODIFIED: confirmed | TU paragraph matches CONVENTIONS §5. The abstract and intro belong to front.
- **F1** (R6-writing, major): [front] MODIFIED: Rewrite 1 still had "two checkable quantities" (growth is not checkable), "must grow linearly", "(I+q+1)^{O(1)}" and an unqualified exact claim. | New abstract of about 230 words; corrections listed above.
- **F6** (R6-writing, major): [front] MODIFIED: Rewrite 21 kept the "answers this" phrasing, but the theorem only covers a subclass. | Open problem (1) asks for time f(p, kappa_nu) poly(I+q) with kappa_nu = max{1, nu/g}. "Theorem cv and Corollary cv-nu give such a bou
- **F9** (R6-writing, major): [recA] MODIFIED: Valid. Rewrite 19's sentence ("pieces that contain no near-optimal point") is false for K = {x} in prop:cv-limit (the stiff piece [0,x_c] contains the minimizer) | Deleted 734-798, cv-energy, cv-envelope; one accurate se / [recA] MODIFIED: Confirmed; replacement sentence completed | last paragraph of 7.3: no unproved necessity claim; "global constants cannot be used" follows from prop:cv-limit
- **F10** (R6-writing, major): [coreB] MODIFIED: My part is only `prop:sharp`/`prop:tu-tight`. The height, snap and accept unification and `lem:cr-semiconcave` belong to exact/tu/recourse. | Cor `cor:uniformgrid` made self-contained (mesh, center, theta=0 stated) so th / [coreB] MODIFIED: Confirmed. Cor `cor:uniformgrid` is self-contained, and `constraints.tex`/`appendix-tu.tex` now cite it and `prop:sharp` instead of `prop:tu-tight`. Pass 2 adds "if that stage is run". / [exact] MODIFIED: conventions fix the form: one acceptance proposition parameterized by a denominator bound, cited by Sections 7 and 8; the TU stationary-face argument has different constants and stays with the tu group | `prop:accept` re / [recA] MODIFIED: Confirmed (cr-semiconcave deleted; lem:cr-cell from prop:cellwise(a); thm:cv(iii) cites prop:accept) | none / [tu] MODIFIED: Duplicates removed where an existing result covers the TU case. The TU height lemma and TU snapping are not covered by Section 6, whose Lemma `lem:statpoly` uses principal minors and whose REC fixes coordinates; TU rows  / [tu] MODIFIED: Confirmed. `prop:tu-accept` and `prop:tu-tight` are gone and nothing references them. Keeping the TU height and snapping lemmas is justified: `lem:statpoly`(c) uses principal minors and REC fixes coordinates, while the T / [tu] MODIFIED: confirmed | none / [tu] MODIFIED: Confirmed. `prop:tu-accept` and `prop:tu-tight` are gone and nothing references them. Keeping the TU height and snapping lemmas is justified: `lem:statpoly`(c) uses principal minors and REC fixes coordinates, while the T / [tu] MODIFIED: confirmed | none
- **F11** (R6-writing, major): [coreB] MODIFIED: Accepted the deletion of `rem:cluster`. Rewrite 12's replacement sentence repeats related.tex lines 103–106 (CONVENTIONS: one place per comparison), so a pure pointer is used instead. | `rem:cluster` deleted. "Section~\r / [coreB] MODIFIED: Confirmed. `rem:cluster` deleted; a one-sentence pointer to Section 2 remains, and `related.tex` 98–108 holds the only comparison. / [recA] MODIFIED: Confirmed; rem:cv-instances checked against DPK's account of Khajavirad | none (see (3)) / [tu] MODIFIED: Only `rem:tu-bm` is mine. | Kept only the technical Bienstock–Muñoz comparison (i)–(iv). Deleted the Hochbaum–Shanthikumar paragraph; that reference is still cited in `related.tex`. / [tu] MODIFIED: Confirmed. `rem:tu-bm` keeps only the Bienstock–Muñoz comparison; `HochbaumShanthikumar1990` is still cited in `related.tex`. | (iv) matched to the corrected size bound (see fix 4) / [tu] MODIFIED: confirmed | `rem:tu-bm`(iii)–(iv) made consistent with Section 8.5 (fix 3) / [tu] MODIFIED: Confirmed. `rem:tu-bm` keeps only the Bienstock–Muñoz comparison; `HochbaumShanthikumar1990` is still cited in `related.tex`. | (iv) matched to the corrected size bound (see fix 4) / [tu] MODIFIED: confirmed | `rem:tu-bm`(iii)–(iv) made consistent with Section 8.5 (fix 3)
- **F12** (R6-writing, major): [coreB] MODIFIED: My parts only. | Graph Γ→𝒢 and Δ→Δ_𝒢 (ex:family); B→X′/X^{(j)}; S_t→ξ_t; H→ĥ; σ (coupling) removed; r→ν; q_k→Q_k. ℓ_i was already used throughout. / [coreB] MODIFIED: Confirmed: 𝒢, Δ_𝒢, X', X^{(j)}, ĥ, ξ_t, ν, Q_k. No ℓ_i/l_i, B_i or σ clash remains. / [exact] MODIFIED: renames in my files done per the conventions table | P=Delta H -> \hat H; gradient ell(x) deleted; ell_i everywhere; S -> \mathcal S. Rejected the part "Delta -> delta_F": the conventions reserve Delta for the Section 6 
- **F19** (R6-writing, minor): [coreB] MODIFIED: Combined with F159 (same issue). | TRIAL: "and the incumbent x̂=ℓ with value U=F(ℓ), or a better feasible point and its value if one is known"; explicit incumbent update in step (ii).
- **F21** (R6-writing, minor): [computation] MODIFIED (merged with F76, F214): See F76/F214: E4 text states set growth without point growth and cites the proved lower bound lim:prop:setgrowth.
- **F25** (R6-writing, minor): [recA] MODIFIED: Confirmed | none
- **F28** (R6-writing, minor): [coreA] MODIFIED: Convention changed as F70 and CONVENTIONS require, instead of "largest constant". The largest weighted constant need not exist: if `P = ∅`, every `γ > 0` is valid. Statements hold for every valid constant anyway. | Def 3 / [coreA] MODIFIED: Confirmed: there is no largest weighted constant when `P = ∅`. **Second pass:** the convention sentence after Def 3.2 was corrected (item 1 below).
- **F33** (R6-writing, minor): [front] MODIFIED: The catalogue structure was valid criticism, but the peripheral items cannot be moved into other owners' files, and no other section discusses Benders, MPC condensing, DEE or cascades. | Related work reorganized around t
- **F35** (R9-referee, major): [recA] MODIFIED: Confirmed | none / [tu] MODIFIED: CONVENTIONS keep one paper. | All §8.6 proofs moved to the appendix. Algorithm boxes added. `prop:tu-tight` and `rem:tu-hybrid` removed. The misaligned-grid and `ex:tu-sum` verifications moved to D.4. / [tu] MODIFIED: Confirmed. | none / [tu] MODIFIED: Confirmed. | none
- **F36** (R9-referee, major): [limits] MODIFIED: confirmed | As F0.
- **F41** (R9-referee, major): [coreB] MODIFIED: My parts only (same as F12). | See F12. P stays {i: L_i>0}. / [coreB] MODIFIED: Confirmed (as F12).
- **F53** (R5-consistency, major): [optsets] MODIFIED: R5's wording ("no corrected-grid certificate has accuracy-independent grid size") is false after F178: R4's n=2 certificate has a 2-node last grid. | `rem:grading`: open for finite 𝒮; for a continuum, `lim:prop:setgrowth
- **F54** (R5-consistency, major): [front] MODIFIED: Same content as F6 and F114. | See F6.
- **F59** (R5-consistency, major): [coreB] MODIFIED: My part: chain states. | Chain states written ξ_t in App. A; the example no longer names them. / [coreB] MODIFIED: Confirmed: chain states are ξ_t, and the objective is named Ψ_m as in `lim:prop:messages` (pass 2).
- **F60** (R5-consistency, major): [recA] MODIFIED: Scheme of CONVENTIONS used (phi_t block objective, psi_t value factor) instead of the reviewer's f_t/phi_t | 7.1 and 7.3 use one scheme; W_B -> V_B, V_h -> V^G / [recA] MODIFIED: Confirmed (CONVENTIONS scheme) | none
- **F67** (R5-consistency, major): [exact] MODIFIED: same as F10 | prop:accept parameterized; Section 6 keeps the box stationary-face lemma (conventions: TU details in appendix-tu). / [recA] MODIFIED: Confirmed (REC needs a box; slices of 7.3 are polytopes) | none / [tu] MODIFIED: See F10. §8.6 now keeps only the TU constants, TU-EXACT and the theorem statement. | `prop:tu-accept` deleted. Theorem 7.18/7.46 are not mine. / [tu] MODIFIED: Confirmed: 8.6 keeps the constants, TU-EXACT and the theorem, and cites `prop:accept` (its current form takes the denominator bound `Ω'`). | none / [tu] MODIFIED: Confirmed: 8.6 keeps the constants, TU-EXACT and the theorem, and cites `prop:accept` (its current form takes the denominator bound `Ω'`). | none
- **F68** (R5-consistency, major): [coreB] MODIFIED: (c) and (d) are mine; (e) is resolved by deleting Remark 5.9; (a) and (b) belong to others. | (c) Cor `cor:uniformgrid` kept as the single statement. (d) Example `ex:chain` shortened to a pointer to Prop `lim:prop:messag / [coreB] MODIFIED: Confirmed. (c) Cor `cor:uniformgrid` is the single statement; (d) `ex:chain` is a pointer plus the proved rescaled κ bracket. / [recB] N/A: other files | -- / [tu] MODIFIED: Confirmed that a separate TU-GRID proof is needed. The proof cited `prop:sharp` "with σ=0", but `prop:sharp` was changed concurrently and now has the parameter `g`. | fix 8 / [tu] MODIFIED: confirmed; `lem:tu-uniform` re-derived against the current `prop:sharp` | wording (fix 5) / [tu] MODIFIED: Confirmed that a separate TU-GRID proof is needed. The proof cited `prop:sharp` "with σ=0", but `prop:sharp` was changed concurrently and now has the parameter `g`. | fix 8 / [tu] MODIFIED: confirmed; `lem:tu-uniform` re-derived against the current `prop:sharp` | wording (fix 5)
- **F76** (R5-consistency, minor): [computation] MODIFIED: The exact count 4(⌊√(n/4)⌋+1)+1 is an empirical formula for the separable κ=2 instances; attributing it to Prop. prop:tu-tight (TU instance, being deleted) or to Cor. cor:uniformgrid (a different family, and a lower boun
- **F89** (R5-consistency, minor): [coreB] MODIFIED: CONVENTIONS §4 fixes the common mesh as h_j, not h_j^c; η_j appears only in Section 5. | The common mesh is h_j = s2^{-j} in `lem:commonmesh` and Cor `cor:uniformgrid`. / [coreB] MODIFIED: Confirmed. CONVENTIONS fixes the common mesh as h_j. / [tu] MODIFIED: The finding allows η to stay the TU mesh unit. | `h_j=η2^{-j}` kept, with one sentence: "common to all continuous coordinates, with base η instead of s". No other η role occurs in my files. / [tu] MODIFIED: Confirmed. | mesh sentence clarified (fix 2) / [tu] MODIFIED: confirmed | none / [tu] MODIFIED: Confirmed. | mesh sentence clarified (fix 2) / [tu] MODIFIED: confirmed | none
- **F99** (R3-math-constraints-sets, minor): [tu] MODIFIED: Wrong part reference. The proposed clause "which holds for some g>0 when S={v*}" is not proved for TU feasible sets: Lemma `lem:unique-growth` covers box QPs only. | `rem:tu-cf` (now in D.3) assumes (8.3) with `\mathcal  / [tu] MODIFIED: Confirmed. Uniqueness implies growth is proved only for box QPs, so assuming growth is right. | feasibility check added to `rem:tu-cf` (fix 12) / [tu] MODIFIED: Confirmed. Uniqueness implies growth is proved only for box QPs, so assuming growth is right. | feasibility check added to `rem:tu-cf` (fix 12)
- **F101** (R3-math-constraints-sets, minor): [optsets] MODIFIED: Same issue as F53. | Same fix as F53, with wording aligned to limits' revised Prop (b).
- **F102** (R3-math-constraints-sets, minor): [optsets] MODIFIED: The citation was imprecise. Citing lem:cells's proof would not work: that proof now has no rounding argument. | The proof of Lemma `lem:proximal`(ii) applies Prop `prop:cellwise`(a) to `F~ = F + η||·−c||²` (upper coordin
- **F103** (R3-math-constraints-sets, minor): [optsets] MODIFIED: The factor 10 was unexplained. A direct count is tighter. | Lemma `lem:graded`(b) gives `|G_i| <= 3 + (8/θ)ln(n+2) <= 7θ^{-1}ceil(log2(n+2))`, and `K_theta = 8θ^{-1}ceil(log2(n+2))` (the same cap as CT with a common mesh
- **F108** (R3-math-constraints-sets, minor): [tu] MODIFIED: The width is renamed to `s` (reserved meaning), so `W` remains only the reduced denominator, as in `prop:accept`. A separate `W_F` is therefore unnecessary. | Row set → `\mathcal J`; saddle → `\mathsf K`; row basis → `\m / [tu] MODIFIED: Confirmed. | none / [tu] MODIFIED: Confirmed. | none
- **F112** (R2-math-recourse, major): [recA] MODIFIED: The proposed statement keeps f(p,kappa) unchanged; that is not justified because grid nodes have encoding length O((1+mu 2^mu)(I+q+1)) and the oracle cost is polynomial in it, which adds a factor kappa^{O(1)} | thm:value / [recA] MODIFIED: Completed: the constant also depends on the encoding-length bound of the L_i^V, F_0's factors need exact polynomial-time evaluation, and (c) needs the box model | statement of thm:valuefn and App C.1 rewritten (see recA. / [recB] N/A: recourse-valuefn | --
- **F113** (R2-math-recourse, major): [recA] MODIFIED: CONVENTIONS scheme used instead of the reviewer's | recA renames: leaf count R -> N_Pi; constraint index k -> s; multiplier support calK -> calE; tangent space calT -> calW; D_0 -> Delta_H; beta (height lemma) -> beta_H; / [recA] MODIFIED: Confirmed | none
- **F114** (R2-math-recourse, major): [front] MODIFIED: See F6. | See F6.
- **F117** (R2-math-recourse, minor): [recA] MODIFIED: Per-coordinate e_B(C) = sum (L_i/8) w^2 (R6 Rewrite 17, CONVENTIONS) is sharper than L_B; the lemma needs L_i only for i in B, so the core search's core-only L is covered (take L_i = L) | 7.2 bag-cell block / [recA] MODIFIED: Confirmed (per-coordinate L_i is sharper; core search takes L_i = L) | none
- **F131** (R2-math-recourse, minor): [recB] REJECTED: move 7.6 out of Section 7 | CONVENTIONS (binding) keeps it as 7.5 in Section 7; recA's roadmap states that it does not use recourse; it shares the cut machinery of 7.4 and cor:core links them.
- **F134** (R7-literature, major): [front] MODIFIED: Item (v) no longer exists (list removed). The credit and novelty statement were placed in the intro's limits summary. | "... a path of local affine equalities makes the problem NP-hard at bag size three and kappa = 1, by
- **F137** (R7-literature, major): [front] MODIFIED: R7's sentence calls both methods "without a bound on the number of partition points". Gupte-Koster-Kuhnke use discretizations of fixed size (KB p. 5-8; DataCite abstract), so that is false for them, and the closing sente
- **F139** (R7-literature, minor): [front] MODIFIED: The Bajaj-Hasan full text is not reachable (Springer blocks scripted access; Semantic Scholar elides the abstract), so whether they use one global bound or per-coordinate bounds cannot be confirmed. | related.tex makes n / [coreA] MODIFIED: The full text of Bajaj–Hasan 2020 is paywalled. Searches found only the abstract (AIChE and Springer pages). The theorem number and the constant convention cannot be verified. | Removed "Theorem 1". The text says what th / [coreA] MODIFIED: Confirmed: the theorem number is unverifiable. **Second pass:** "we use one bound `L_i` per coordinate" was added (item 2).
- **F145** (R7-literature, minor): [exact] MODIFIED: attribution added; locators changed | Before lem:statpoly: "The argument follows Vavasis [Vavasis1990] (see also [DelPiaDeyMolinaro2017]); we need its explicit constants." No "Section 2"/"Theorem 3" locators: the bib ent
- **F155** (R1-math-core, major): [coreB] MODIFIED: Option 1. R1's sentence "filtered uniform grids also have O(√(nκ)) nodes" would assert an unproved bound for the hull grids of TRIAL with θ=0. I attribute the bound only to UC, which `thm:cells` analyzes. | "Uniform grid / [coreB] MODIFIED: Confirmed. Option 1 is correct, since R1's sentence would assert an unproved bound for TRIAL's θ=0 hull grids. Pass 2 adds "polynomial in I+q and κ for fixed p".
- **F158** (R1-math-core, minor): [coreA] MODIFIED: "κ can be exponential in I (Example 5.11 unit-box; Prop 10.1)" is not proved by those citations. The unit-box chain gives `κ = 2^{Θ(√I)}`, and Prop 10.1 gives only an upper bound on κ. | Replaced by a proved two-variable / [coreA] MODIFIED: Confirmed. The two-variable example was re-derived. Request E5 has been applied (exact.tex 330).
- **F159** (R1-math-core, minor): [coreB] MODIFIED: Combined with F19 (R6 Rewrite 11 wording plus an explicit incumbent). | See F19. / [coreB] MODIFIED: Confirmed (as F19).
- **F168** (R1-math-core, minor): [coreA] MODIFIED: Accepted the typo fix. The renaming uses `J_0`, `J_∂` (CONVENTIONS §4) instead of `I_int`, `I_act`. `J_0` matches `J_0(s)` of Section 6 exactly: continuous coordinates strictly inside. | `ζ^T d`; `S, A` → `J_0, J_∂`. / [coreA] MODIFIED: Confirmed.
- **F170** (R1-math-core, minor): [exact] MODIFIED: renames per conventions | \hat H, I_C^+ = I_C cap P, \mathcal S, J_+ instead of W in 6.5, J' instead of E in lem:snap. Rejected renaming R -> R_ht: the conventions reserve R for the Section 6 height (radius R_ij is core'
- **F177** (R1-math-core, minor): [coreA] MODIFIED: Forbidding degenerate subboxes (R1's first fix) would break the label filter (App. boundary, lem:labelfilter(ii) fixes integer coordinates to one value) and the localized rule `B'_i = {x*_i}`. The alternative fix was use / [coreA] MODIFIED: Confirmed: degenerate subboxes are needed by `lem:labelfilter` and `prop:local`.
- **F186** (R4-math-limits, minor): [limits] MODIFIED: Whose widths was unclear. | Chose the reviewer's second option, which needs no extra hypothesis: occupied width ω_i(μ) is defined per feasible point; the proposition gives a feasible point μ with value 1/4−(2r+1)/(16r) a / [limits] MODIFIED: confirmed | Occupied widths are defined per feasible point.
- **F204** (R8-computation, major): [computation] MODIFIED: The solver must stay unchanged, so the checker hot loop is not hoisted. | Section 11.1: "On the replayed runs below with a solve time of at least 0.1 seconds, replay took between 0.8 and 2.5 times as long as the solve" (
- **F214** (R8-computation, minor): [computation] MODIFIED: Remark 9.4 says only "open"; Prop. lim:prop:setgrowth is a proved lower bound for the same structure. | See F21; both time limits (30 s, 5 s) stated.
