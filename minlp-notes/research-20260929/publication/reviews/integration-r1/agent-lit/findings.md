# Literature-label check (helper agent, read-only), saved by the lead reviewer

The helper agent could not write files; the lead saved its returned report here verbatim in substance.
S = open-instances-summary.md, R = publication/READINESS.md, C/N/Sm = literature control/network/small reports.

Latest verdicts: control r2 verified (7 minor, resolved C:706-744); network r2 verified (9 minor, resolved N:502-528;
two sources never obtained: Hijazi 2013 first version, AIChE 2025 KAN abstract, N:357,359); small r3 issues
(4 minor, author-resolved Sm:910-919, no round-4 review). R:45 states this correctly.

Problems found (lead spot-checked 1, 2, 3, 4):
1. S:161-162 two blank lines break the 43-row literature table.
2. S:163 "Martín" -> "Martin" (S:50, S:188 use Martin; PDFs print "Alexander Martin"). Also C:34,115,511,550.
3. Labels missing: camshape100 and eg_int_s "already solved globally in floating point" (C:51,84; Sm:41,461);
   camshape800 "prior global claim false" (C:26,87).
4. S:178-181 catmix "OSIL coefficients differ slightly from GAMS" sourced from minlplib-status/report.md:17, not control
   (C:91 "not the COPS 3.0 model"). Add link.
5. S:191 powerflow0030p: garbled "prevents unproved exact bound transport"; Oustry et al. "certified" (N:361).
6. S:192-193 "Prior moment/SDP results solve tapped case39": only Ghaddar et al. 2016 solved globally in fp (N:36,141-147).
7. S:200-201 KAN "exact network evaluation" -> 60-digit numerical evaluation (N:176,322,189).
8. S:189-190 CAMINO "claims" (one each); termination status not recorded (Sm:449,547). Same in R:38.
9. S:164-166 Göß PARA prints 0.00% (lnts50/100/200) and 0.01% (lnts400) (C:35,267,533).
10. S:167 Waki et al. scope: source model h*y^2, M=600-1000 (C:40,299-313,332).
11. R:27 garbled "Prior floating-point results are partly known"; R:33 "may have" vs report "very likely" (Sm:36,233).
12. Paper must cite: Göß-Burlacu-Martin publisher correction (Sm:423-429,463); hvycrash SIF value credit (Sm:174);
    lukvle10 SOLTN tolerance artifact (C:415).
13. Stale numbers inside track reports (not in S): N:277 waterno2_06 1.67%; Sm:494-496 eg_disc2_s sample-only.

Confirmed correct: all 43 rows present once; labels/facts for lnts, dtoc5, camshape200/400, lukvle10, optcdeg2,
chain, catmix, hvycrash, ex6_2_*, etamac, pricing050, pindyck, eg_*, powerflow (substance), waterno2, ann, KAN.
Commands: read-only cat/sed/grep/awk on S, R, C, N, Sm, reviews; pdftotext -l 1 on saved Göß PDFs; cat -A on S:159-164.
