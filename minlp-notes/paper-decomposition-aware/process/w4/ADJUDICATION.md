# Adjudication of the W4 review findings

W4 was the second independent review (10 reviewers; `process/w4/*.md`). Every
critical or major finding was checked by an adversarial verifier
(`process/w4/all-results.json`). The non-refuted findings were assigned to file
groups and resolved in revision round W5 (`process/w5/reports/<group>.md`, each
with a verification section), following `process/w5/CUTPLAN.md`.

No W4 reviewer found a mathematical error. The confirmed major findings were
editorial: main-text length (80 pages; now about 70), introduction length, the
growth-scope caveat, the missing Hochbaum-Shanthikumar comparison, and the
explanation of SCIP's primal bounds.

Totals: ACCEPTED: 53, MODIFIED: 18, REJECTED: 1

| id | severity | verified severity | location | decision | groups |
|---|---|---|---|---|---|
| M-core-1 | minor |  | sections/growth.tex:259-260; sections/appendix-growth.tex:129 | ACCEPTED | coreB |
| M-core-2 | minor |  | sections/growth.tex:146 and 340-350; sections/growth-sharp.tex:22,26; sections/a | MODIFIED | coreB |
| M-core-3 | minor |  | sections/growth.tex:22-23 | ACCEPTED | coreB |
| M-exact-1 | minor |  | sections/exact.tex:373-374 (proof of Thm 6.14 thm:exact, 'Bound under growth') | ACCEPTED | exact |
| M-exact-2 | minor |  | sections/exact.tex:64-69 (Def 6.2), 71-125 (Lemma 6.3), 135-140 (proof of Cor 6. | ACCEPTED | exact |
| M-recourse-1 | minor |  | sections/recourse-convex.tex:207-209 (Thm 7.10(iv)); also :197-206 (iii) and sec | ACCEPTED | recA |
| M-recourse-2 | minor |  | sections/recourse-valuefn.tex:48-50 | ACCEPTED | recA |
| M-recourse-3 | minor |  | sections/recourse-local.tex:1 (title of Section 7.2) | ACCEPTED | recA |
| M-recourse-4 | minor |  | sections/recourse-convex.tex:202-206; sections/appendix-recourse-convex.tex:359- | ACCEPTED | recA |
| M-recourse-5 | minor |  | sections/recourse-cuts.tex:113-115 (last sentence of Thm 7.17) | ACCEPTED | recB |
| M-tu-optsets-1 | minor |  | sections/constraints.tex:86-103 (rem:tu-curv), :320-323 (certificate record), :4 | ACCEPTED | tu |
| M-tu-optsets-2 | minor |  | sections/constraints.tex:260 (prop:tu-sound) and :331-332 (thm:tu-states) | MODIFIED | tu |
| M-tu-optsets-3 | minor |  | sections/constraints.tex:553-560 (thm:tu-exact(c)) | ACCEPTED | tu |
| M-limits-1 | minor |  | sections/limits.tex:21-22 (bullet), limits.tex:362 (title); also abstract.tex:22 | ACCEPTED | coreB, front, limits |
| M-limits-2 | minor |  | sections/limits.tex:609-613; intro.tex:206-208 | ACCEPTED | front, limits |
| M-limits-3 | minor |  | sections/limits.tex:346-349 and 355-357 | ACCEPTED | limits |
| M-limits-4 | minor |  | sections/appendix-lbproduct.tex:31-33; limits.tex:202-204 | ACCEPTED | limits |
| M-limits-5 | minor |  | sections/limits.tex:623-624; intro.tex:210-212 | MODIFIED | front, limits |
| C-consistency-1 | minor |  | sections/intro.tex:331-335 (Table tab:results, row thm:cv) | ACCEPTED | front |
| C-consistency-2 | minor |  | sections/limits.tex:39-44 (roadmap bullet 'Local corrections') | ACCEPTED | limits |
| C-consistency-3 | minor |  | sections/exact.tex:64-67, 72-80, 102, 135, 204-226 (s as a minimizer); exact.tex | MODIFIED | exact, optsets, recB |
| C-consistency-4 | minor |  | sections/constraints.tex:32-491 (m = rows), 230-254 (m_i), 594-631 and appendix- | MODIFIED | coreB, front, optsets, tu |
| C-consistency-5 | minor |  | growth.tex:37 vs constraints.tex:37-43,68 vs optsets.tex:547-556 and appendix-pr | ACCEPTED | coreB, exact, front, limits, optsets, tu |
| C-consistency-6 | minor |  | sections/growth.tex:262 (proof of Thm 5.9); sections/exact.tex:496 | ACCEPTED | coreB, exact |
| C-consistency-7 | minor |  | sections/optsets.tex:519-520 (definition in Remark 9.11); uses at 600-605 (Thm 9 | ACCEPTED | optsets |
| C-consistency-8 | minor |  | sections/appendix-smoothed.tex; figures/E3_plateau_vs_n.pdf | ACCEPTED | coordinator: unused figure moved to process/w5/, smoothed appendix deleted |
| C-consistency-9 | minor |  | sections/intro.tex:253-257 | ACCEPTED | front |
| C-writing-1 | major | major | whole paper (main.tex 11-25); sections 7-10 | ACCEPTED | front |
| C-writing-2 | major | minor | intro.tex 194-217, 219-246, 248-268, 270-294, 299-370 | ACCEPTED | front |
| C-writing-3 | major | minor | intro.tex 137-145; setting-growthcert.tex 59-66 (Remark 3.4); CONVENTIONS §5 | ACCEPTED | coreA, front |
| C-writing-4 | minor |  | abstract.tex 2-26 | MODIFIED | front |
| C-writing-5 | minor |  | growth.tex 266-284 (Rem 5.10); intro.tex 124-131; related.tex 54-56; limits.tex  | MODIFIED | coreB, front, limits |
| C-writing-6 | minor |  | exact-localized.tex 131-139 | MODIFIED | exact |
| C-writing-7 | minor |  | growth.tex 179; growth-sharp.tex 9-10, 35-37 | MODIFIED | coreB |
| C-writing-8 | minor |  | grids.tex 274-282; growth.tex 224-225 | ACCEPTED | coreA, coreB |
| C-writing-9 | minor |  | limits.tex 3-45 | ACCEPTED | limits |
| C-writing-10 | minor |  | setting.tex 146-147, 174-175; exact.tex 64-67, 102, 187, 204-226, 465; intro.tex | ACCEPTED | coreA, coreB, exact, front, limits |
| C-writing-11 | minor |  | exact-localized.tex 112-116 | ACCEPTED | exact |
| C-writing-12 | minor |  | exact.tex 495-497 | ACCEPTED | exact |
| C-writing-13 | minor |  | intro.tex 100 | ACCEPTED | front |
| C-writing-14 | minor |  | growth.tex 216-217 | ACCEPTED | coreB |
| C-writing-15 | minor |  | main.tex 3-6 | REJECTED | coordinator: the title is the one given in the user request |
| C-writing-16 | minor |  | intro.tex 37 | ACCEPTED | front |
| C-writing-17 | minor |  | appendix-localized.tex 1; appendix-recourse-convex.tex 1-2; appendix-recourse-cu | MODIFIED | exact, recB |
| C-writing-18 | minor |  | computation.tex §11.2-11.8; Table 3 caption 229-234; Table 6 caption 435-437 | MODIFIED | computation |
| C-writing-19 | minor |  | intro.tex 281-356; related.tex 156-167; exact.tex 6, 9; recourse-local.tex 54-13 | MODIFIED | exact, front, optsets, recB |
| C-writing-20 | minor |  | intro.tex 323-335 (Table 1) | ACCEPTED | front |
| C-writing-21 | minor |  | recourse.tex 3-5 | MODIFIED | recA |
| C-literature-1 | major | major | related.tex:113-116 (only mention); related.tex:141-143; related.tex:203-207; co | ACCEPTED | front, tu |
| C-literature-2 | minor |  | related.tex:188-191 | ACCEPTED | front |
| C-literature-3 | minor |  | grids.tex:45-49 (also intro.tex:53-57) | ACCEPTED | coreA, front |
| C-literature-4 | minor |  | related.tex:43-44 | ACCEPTED | front |
| C-literature-5 | minor |  | limits.tex:286-288; limits.tex:374-376; intro.tex:214-217 | ACCEPTED | front, limits |
| C-literature-6 | minor |  | related.tex:90-97 | ACCEPTED | front |
| C-literature-7 | minor |  | related.tex:150-153; exact.tex:186-196 (alg:rec, lem:snap) | ACCEPTED | exact, front |
| C-literature-8 | minor |  | related.tex:110-113 | ACCEPTED | front |
| C-literature-9 | minor |  | related.tex:122-143; related.tex:40-42 | ACCEPTED | front |
| C-literature-10 | minor |  | recourse-balanced.tex:41-43 | ACCEPTED | recB |
| C-literature-11 | minor |  | references.bib:215 and 1215; sections/appendix-smoothed.tex:74 | ACCEPTED | coordinator: provenance comments corrected |
| C-computation-1 | major | major | sections/computation.tex:369-375 (also Table 5 caption 394-398; experiments/READ | MODIFIED | computation |
| C-computation-2 | minor |  | sections/computation.tex:104-105; experiments/README.md 'Planted nonconvex famil | ACCEPTED | computation |
| C-computation-3 | minor |  | sections/computation.tex:90-93 vs 346-347; experiments/README.md 'Experiments an | ACCEPTED | computation |
| C-computation-4 | minor |  | sections/computation.tex:34-41 (items (d), (e)); 45-54 (item (g)) | ACCEPTED | computation |
| C-computation-5 | minor |  | sections/computation.tex:173-187 (E2), 189-199 (E3) | ACCEPTED | computation |
| C-computation-6 | minor |  | experiments/README.md 'Reproduce'; experiments/chain/run_chain.py and experiment | ACCEPTED | computation |
| C-computation-7 | minor |  | sections/computation.tex §11.3-11.7 (labels E6, E4, S1, E5) | MODIFIED | computation |
| R-referee-1 | major | major | whole paper; Sec. 7 (pp. 31-44), Sec. 8 (44-53), Sec. 9 (53-62), Sec. 10.4-10.7  | ACCEPTED | front |
| R-referee-2 | minor |  | intro.tex:37-297 (pp. 2-7), especially 152-158 and 219-294; lower-bound summary  | MODIFIED | coreB, front, limits |
| R-referee-3 | minor |  | intro.tex:137-145; setting-growthcert.tex:59-70 (Remark rem:nonconvex) | ACCEPTED | coreA, front |
| R-referee-6 | minor |  | intro.tex:124-131; growth.tex:265-271 (Remark rem:fpt); setting.tex:98-103 | ACCEPTED | coreA, coreB, front |
| R-referee-4 | minor |  | growth.tex:35-37; appendix-growth.tex:118-125; appendix-recourse-convex.tex:22;  | MODIFIED | coreA, coreB, exact, optsets, recB, tu |
| R-referee-5 | minor |  | intro.tex:3-8; computation.tex:5-7 and 454-470 | MODIFIED | computation, front |
