# Independent Stage 6b review — R5

The frozen Stage 6b manuscript is a coherent standalone presentation of the principal results. I found no major defect in the reviewed principal claims, their relation to the included technical statements, or the extracted delivery. I found two minor corrections below. I recommend resolving them before closing Stage 6b. This report does not declare acceptance and does not replace the separate whole-manuscript review cycle.

I read the supplied review instructions in full. I reviewed the abstract, introduction, all six narrative files, conclusion, principal statements and tables, examples, diagrams, bibliography, technical statements supporting those summaries, and the materially relevant proof mechanisms. Particular attention went to the complete scalar approximation proof and hybrid extension in Appendix J; the weighted face and cactus compiler in Appendix G; the exact root recovery and convex design arguments in H; the conic, sensitivity, and rational-witness arguments in I; and the energy/support/curvature arguments in K. The algebraic, arithmetic, hull, and hardness statements were cross-checked against A–F, including their output and quantifier restrictions. The preservation check below concerns all eleven technical source files. I did not use author, lead, peer, or historical review reports as evidence and did not change any manuscript or code.

## Required minor corrections

### R5-1. Restore the ordered-bound hypothesis in the main nomination-box definition

**Location:** `complexity/narrative/01-model.tex:36–42`, equation (2), printed page 7. Compare `complexity/sections/01-preliminaries.tex:424–432`.

The main definition specifies only `ell,u in Q^V` and immediately states that nonemptiness is equivalent to `sum ell <= 0 <= sum u`. This equivalence needs the coordinatewise assumption `ell <= u`, which the appendix explicitly includes and the main definition omits.

For example, on a graph with two vertices, take `ell=(1,-2)` and `u=(0,2)`. The displayed sum test passes, but the first nomination coordinate would have to be at least 1 and at most 0. The balanced set is empty. Calling the object a box suggests the intended ordered endpoints, but the standalone displayed definition and its exact nonemptiness claim should state them.

**Repair:** append `ell <= u` to the rational-data condition in equation (2), matching Appendix A. The intended algorithms and proofs are unaffected; their nonempty-domain hypotheses remain intact.

### R5-2. Finish the coverage record's transition from planned sections to included appendices

**Locations:** `coverage.md:47`; `process/completion-coverage.md:7,35`.

The final inventory assigns the fixed-core supporting result to A03/A04/A06 but still says “other assignments remain planned.” Those uses are already present: A03 proves the box specialization, A04 explicitly extends the box lemma to growing dense degree, and A06 invokes it in the fixed-global-rank weighted algorithm. The final map should identify these completed uses, or explicitly exclude any broader unused part of the supporting result.

Related stale wording remains in the completion map: line 7 reports the original checker's “18 planned sections,” while the current A-only checker actually reports **308 inventory files and 13 planned sections**; line 35 says “A05, no appendix” although A05 is now Appendix E. The reference to the *original* checker can reasonably be read as historical, but the current count should be supplied distinctly in this document labeled as the S6b completion map.

**Repair:** replace the planned-use language with the actual included theorem/lemma destinations; state the current A-only count separately from any retained historical count; remove or date the obsolete “no appendix” wording. I found no missing promoted theorem behind these stale descriptions, so this is a documentation correction, not a major scientific coverage finding.

## Principal-result and consistency assessment

- **State model and output contracts (main §2; Appendix A):** the existence proof correctly derives coercivity even for bounded strictly increasing laws. Conservation, orientation reversal, gauge freedom, and primitive energy versus physical dissipation are distinguished. The main text separates rational parameter scenarios from generally irrational states; exact threshold comparison from additive intervals; and a list of algebraic summands from a common algebraic encoding. The sole definition correction is R5-1.
- **Cactus arithmetic, block rank, and laws (Theorems 3.1–3.2; B–D):** the summaries retain balanced nomination boxes, independent coefficient coordinates, and the absence of operating filters. The one-active-block argument and positive-source path perturbation explain the small nomination faces; the zonotope support construction handles many coefficients without enumerating all box corners. Local exact optimization is kept separate from summation across blocks. The exact single-source/sink SRS equivalence includes the weak equality convention and does not become an exact classification for general cactus boxes. The dense polynomial-law extension permits growing degree and pieces, while the fractional-power theorem fixes its finite exponent family. Its even-denominator exact arc hardness is a separate lower bound. The statements do not infer NP membership from SRS hardness or call a parameter-dependent exponent FPT.
- **Observable-dependent topology and discrete boundaries (Theorem 4.1, Tables 1–2; E–F):** the hierarchy agrees with the full statements: trees for weighted potentials, cacti for pairwise potentials and linear flows, and series-parallel graphs for individual arcs. Fixed nominations, independent compact sets, quadratic laws, and no operating filters are available at the table/theorem locations. The finite secant identity has the correct target-edge coefficient and supports the envelope argument. Quantitative restoration uses positive finite resistances; it does not treat a deleted edge or zero-resistance contraction as an admissible final witness. Region convexity is distinguished from coordinatewise extremum preservation. Table 2 retains restricted membership and separates weak hardness/gap scaling from strong hardness. Exact target-flow realization and existential capacity design are kept separate from robust validation.
- **Weighted results (Theorem 5.1; F–G and J):** fixed support, fixed affine nomination dimension, fixed global rank, fixed maximum block rank, and fixed total noncactus rank remain distinct. The full `O(rp)` face theorem is presented as completed. Its proof prunes and contracts before the two separate perturbations; it does not add positive sources before establishing the ordinary-chain ordering. The cactus compiler uses a common partition in the original nomination variables, covers tied coefficients, flat candidates and zero flows, and recovers original parameters. The exact fixed-nomination profile theorem correctly permits an interior rational coefficient and separately represented irrational local values. The capacity-filter theorem returns algebraic parameters unless the stated tightening margin is supplied, and compares the rational output to the tightened optimum.
- **Higher-block extensions (J):** the scalar lemma explicitly handles growing dense degree, nonsmooth branch switches, complex exceptional parameters, rational interpolation nodes and coefficient sizes. The Lipschitz exceptional neighborhoods and geometric analytic panels avoid a grid proportional to `1/epsilon`. Local roots are sampled separately. The hybrid theorem keeps exactly the exceptional circulations in a core of dimension `d+kappa(G)` and compiles only the cactus remainder. Both the main theorem and conclusion correctly describe `kappa` as a sum. The remaining several-parameter, arbitrarily-many-higher-block sum is explicitly delimited and is neither claimed solved nor used as a missing step in these theorems. The fixed-law dense-polynomial line extension is not silently expanded to uncertain polynomial coefficients.
- **Cycle design, correlations, energy, and witnesses (Theorems 6.1–6.2; H–I):** root-threshold LP tests, vertex attainment, uniform root separation and final LP-vertex recovery justify the exact rational parameter output. The convex design proof handles clipped irrational singleton circulation intervals using stored rational endpoint profiles. Few-measurement maximization restricts image dimension and does not claim exact comparison of growing algebraic sums. Global capacity recovery remains scalar-cycle LP reasoning. The Max-Cut and correlated hardness claims retain their separate bounded-data scopes and restricted-family memberships. Maximum dissipation uses the correct factor of three and an explicit compact convex body for rational output; a conic formulation alone is not treated as an exact scalar comparator. Strict-margin feasibility is conditional and does not locate the unknown strictly feasible point.
- **Certificates and implementation (Theorem 7.1; K):** the cubic conjugate, exact conservation requirement, reverse Bregman argument, rational support dual and constrained curvature KKT system agree with the narrative. Sharpness is explicitly over the conserved quadratic error set, not over all physical errors or the additional coordinate intervals. The zero-curvature circulation obstruction and zero-gap exception are retained. Original-instance envelope verification is distinguished from a deterministic-network certificate, and endpoint optimality certifies parameters rather than a rational exact flow. The producer and supplied-block weighted solver are accurately limited; neither is described as implementing every theoretical algorithm.

The abstract's substantive claims correspond to these result groups. I found no principal claim whose required fixed parameter, uncertainty independence, law encoding, filter, or output restriction was silently dropped, apart from the elementary ordered-bound omission in R5-1.

## Standalone reading and rendered layout

The main text has a useful sequence: model and outputs; localization and arithmetic; topology by observable; weighted extensions; design/correlations; certificates; conclusion. It supplies explanations and small concrete examples rather than only an index of appendix results. The proofs are included in the same PDF in dependency order. The appendix notation is locally introduced, and the main cross-references resolve. The 28-page main narrative, eight pages of references, four-page contents/navigation material, and technical development produce the stated 216-page artifact.

I rendered and visually inspected printed pages 8–11, 13–16, 28, 33–34, and 36–39, including both diagrams, both main tables, reference entries, and the contents; I also inspected representative technical/certificate pages. The topology drawings distinguish the four classes correctly. Figure 2 distinguishes fixed nominations from still-variable coefficients. Table 2 is dense but readable and keeps assumptions aligned with conclusions. I found no clipped equations, colliding labels, unreadable table cells, or diagram-scope error in these inspections. The main theorems sometimes cross page boundaries, and page 36 holds the last reference entry alone; these are optional typesetting refinements, not required findings.

The eleven technical section hashes equal their supplied accepted-preservation hashes. This verifies that the reorganization did not alter those technical source files relative to the supplied preservation record; it is not an independent certification of every historical review decision. The main manuscript does not require an unwritten companion or repository note to supply a missing proof. No invented author, funding, license, or journal-acceptance claim appears in the delivered manuscript/README.

## Primary-literature checks

I inspected these original sources directly for claims material to this review:

1. Pfetsch, Schmidt, Skutella and Thürauf, *Potential-Based Flows—An Overview*, [original PDF](https://optimization-online.org/wp-content/uploads/2026/01/ch_potential.pdf), printed pp. 9–10, equations (6) and the following MPD discussion. It asks the nonlinear cactus complexity question. The manuscript correctly distinguishes its additive result and exact single-source/sink classification from a general exact resolution. The online record is dated January 28, 2026 and updated February 20, 2026.
2. Klimm, Pfetsch, Skutella and Strubberg, *Approximating the Network Design Problem for Potential-Based Flows*, [arXiv v1 full text](https://arxiv.org/html/2604.26882v1), Corollary 4 and Theorem 11/§4.3. The manuscript accurately describes the no-fixed-cost convex formulation and the series-parallel FPTAS with positive variable costs and conductance bounds. It preserves the distinction from prescribed passive resistance-scenario optimization.
3. Antoine Vigneron, *Geometric optimization and sums of algebraic functions*, [author manuscript](https://antoinevigneron.github.io/manuscripts/rational.pdf), dated October 21, 2011, §2.3, Theorem 6 and §3.2 (printed pp. 7–10). I downloaded the PDF after the browser tool failed to open it. The explicit theorem bound depends polynomially on `1/epsilon`; §2.3 supplies a bit-model extension, and §3.2 avoids exact sum comparison by approximate values. The manuscript's comparison gives that work appropriate credit and accurately states the stronger accuracy-bit/original-coordinate interface it needs.
4. Daniel N. Dadush, *Integer Programming, Lattice Algorithms, and Deterministic Volume Estimation*, [original thesis](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf), Theorem 2.5.9, printed p. 48. I downloaded the PDF after the browser fetch timed out. Its conclusion explicitly returns a rational vector in the centered convex body with an additive objective bound. This supports the exact-feasible-output use in H and I; the manuscript separately constructs the centered body and Lipschitz extension/bounds rather than omitting those prerequisites.

I also checked the bibliography's stated source versions and the corresponding attribution passages. I did not independently retrieve every one of the 56 references. In particular, I make no theorem-level or priority inference from the inaccessible Hasler–Wang 1993 paper. The manuscript candidly identifies that access gap and limits its novelty claim. Classical energy, adjoints/confluence, LP/QE, approximation, convexity, zonotope and dual-certificate ingredients are credited. These checks support the scoped comparisons, not an exhaustive claim of publication priority.

## Coverage and extracted delivery

The inventory contains 308 distinct linked research/code/data rows and maps all 43 promoted `results/potential-flow-*.md` files. Mechanical file comparison found all 43 promoted results, all 173 potential-flow notes, and all 73 Python modules byte-identical between the main checkout and writing worktree. The current coverage checker passes with 308 inventory files and 13 section files. Its A-only change removes the legacy second-paper section requirement while retaining the source inventory and link checks; it does not prove semantic theorem coverage on its own. The included technical map supplies the latter, subject to R5-2's stale wording.

`git diff HEAD -- paper-potential-flow/uncertainty literature` and the untracked-file query for those paths were empty. Thus Paper B and managed literature are unchanged in this worktree relative to its tracked baseline. I also compared all 3,850 managed-literature files against the main checkout mechanically and found no differences. A comparison of Paper B to a different checkout is not the relevant stage-preservation baseline.

I extracted the actual final archive to `/tmp/s6b-r5-kx8os182/potential-flow-paper-a`. Its manifest lists 63 payload files; every hash matched, with no unlisted payload other than `manifest.json`. The archive has the complete A source and PDF, selected scientific code and rational fixtures, replay/build evidence and instructions. It contains no Paper B, managed literature PDF, raw external INP dataset, research-agent report, or temporary build file. Files named `check_*review.py` are diagnostic programs, not reviewer prose. The dataset attribution clearly identifies synthetic quadratic proxy data.

Commands and results, using `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python`:

```sh
# From the extracted archive root:
python paper-potential-flow/reproducibility/build_paper.py
python -S paper-potential-flow/reproducibility/reproduce.py --output /tmp/s6b-r5-kx8os182/exact.json
python paper-potential-flow/reproducibility/reproduce.py --numerical --output /tmp/s6b-r5-kx8os182/numerical.json
python -S paper-potential-flow/reproducibility/package.py --output /tmp/s6b-r5-kx8os182/repack
pdftotext -layout paper.pdf /tmp/s6b-r5-kx8os182/paper.txt
pdftotext -layout paper-potential-flow/complexity/build/main.pdf /tmp/s6b-r5-kx8os182/rebuilt.txt
cmp /tmp/s6b-r5-kx8os182/paper.txt /tmp/s6b-r5-kx8os182/rebuilt.txt
```

The A-only build passed: zero errors, undefined references, undefined citations, duplicate labels and overfull boxes. `pdfinfo` reports 216 pages. The rebuilt and distributed PDFs have identical extracted layout text. Exact replay passed all 18 commands, including the `-S -O` verifier variants and saved original-instance/energy certificates. Numerical replay passed all 28 commands. Reported packages were NumPy 2.5.2, SciPy 1.18.1, SymPy 1.14.0, NetworkX 3.6.1, CVXPY 1.9.2 and Clarabel 0.11.1. The replay runner isolates code/data before programs that rewrite neighboring JSON. Standalone repackaging succeeded and produced 64 archive files including its manifest, without parent-repository dependencies.

The read-only coverage command was run with a temporary working directory:

```sh
python -S /workspace/minlp-notes-potential-flow/paper-potential-flow/verification/check_coverage.py
```

It printed `PASS: 308 inventory files and 13 planned sections.` All build, download, rendering, extraction, replay and packaging outputs stayed outside the checkout. A first attempted PyMuPDF render failed because `fitz` was unavailable; Poppler's `pdftoppm` was used successfully instead. These replays establish the saved finite witness/diagnostic claims, not every universal theorem or the general theoretical algorithms' implementation.

## Source integrity

At the beginning and end, the review-safe manifest hash was

`a530e917bd4fee2ab9fd90af8f7c29ecddcbb64936abffab32b559f61c2dafb0`

and the archive hash was

`23119436776b23c7e17d97293ee5376806d772bda5009e8dd009861b06ef30a2`.

Every file listed in `stage_files_sha256` matched at both checks. All eleven technical source hashes matched the supplied preservation record. The distributed PDF hash matched its manifest. The only checkout file authored for this review is this report. No agents, commits, manuscript repairs, bibliography changes, code edits, or managed-literature updates were made.
