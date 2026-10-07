# Literature-wording check (helper agent; recorded by the lead reviewer)

The harness prevented the helper from writing this file; the lead copied its findings
and spot-checked the starred items (`*`). The helper created `render_check.py` here.
S = open-instances-summary.md; C/N/Sm = publication/literature/{control,network,small}/report.md;
St = publication/minlplib-status/report.md; E = publication/eg-recheck/report.md; R = READINESS.md.

## Issue 6 and "Also for the paper": all applied and faithful
- 6.1 Martin: S has no "Martín". C still has it at C:34, 115, 511, 550 (*).
- 6.2 labels: camshape100 (S:172; C:51, 84, 372), eg_int_s (S:192; Sm:41, 461), camshape800 (S:175; C:87, 388, 530, 578) ok.
- 6.3 catmix: coefficient-check link on S:182-185; St:17 has the OSIL/.gms statement. If a size is added, catmix's maximum is 1.78e-16 (St:180); 2.4e-16 is the all-family maximum (methanol50 2.38e-16, St:137).
- 6.4 powerflow0030p (S:195): N:30, 121, 123, 135; N:361 "certified" for Oustry et al. ok.
- 6.5 powerflow0039p/r (S:196-197): N:36, 141 (Ghaddar et al. 2016, globally in floating point); SDP gaps 0.00/0.01/0.005% (N:61, 150). ok.
- 6.6 KAN (S:204-205): N:173, 176. ok.
- 6.7 CAMINO (S:193-194): Gurobi 13.0.0 at Sm:42, 43, 54, 436, 541; one claim per instance (Sm:490, 517); status unrecorded (Sm:449, 547); cause unknown (Sm:450). The eg_int_s row (S:192) keeps the shorter wording and a curly apostrophe; Sm:41, 446, 449 apply the same version and caveat to eg_int_s.
- 6.8 lnts (S:168-170): C:35, 80, 267, 533 ok. S:167 (lnts50) could also say "0.00%" (C:35).
- 6.9 dtoc5 (S:171): C:40, 83, 299-313, 332 ok.
- Publisher correction (S:211-214): DOI matches Sm:423; "not read" and Table 17 caveat match Sm:429. hvycrash −0.21850 (Sm:35, 170, 174); lukvle10 SOLTN (C:65, 410, 415, 535) ok.
- Rendering: markdown-it-py 4.0.0 and `pandoc -f gfm` give one table with 43 body rows of 3 cells; links resolve.

## Issue 15 in the literature reports
- N:277 waterno2_06 "282.888038, listed (≤ 1.68%)": exact primal 282.888037386… ≤ display; exact gap 1.67396% ≤ 1.68%. ok.
- Not fixed, same defect class (*): N:278 "914.012 (10.8%)" (exact 10.812%, S shows ≤ 10.82%); N:279 2233.821 below exact 2233.8213456 (S: 2233.821346); N:281 6963.795 below exact 6963.7951802 (S: 6963.795181); N:280 "4.9%" and N:281 "5.9%" happen to be ≥ exact (4.867%, 5.895%).
- Sm:494-496 agree with E, eg-recheck-review-r1 and S/R. ok.
- Not fixed (*): Sm:391 eg_int_s 6.4531031593842274 and Sm:468 eg_disc_s 5.7605396164535106 lie below the exact objectives (S and the package README now use …2275 and …5107). Sm:517 "unless the separate full recheck has replaced it" is stale.
- Response notes at N:504 and Sm:912 sit inside earlier review-response sections (placement only).

## READINESS rows 30-48
No contradiction. R:41 typo "closure; For". S:187-188 say "likely" where R:36/Sm say "very likely" (S is weaker, not overstated).

## Packaging (*)
`publication/literature/` is ignored by the root `.gitignore:2` rule `literature/`. 25 paths in
`publication/reproduction/files-to-commit.json` are ignored (list in
`../scratch/ignored_files_to_commit.txt`), including the three literature reports that S links
44 times and R links in rows 33, 35, 36, 43, 48.
