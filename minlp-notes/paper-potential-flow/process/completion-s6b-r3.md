# Stage 6b independent review R3

## Verdict and scope

I found no major mathematical, algorithmic, novelty, coverage, or delivery defect in the frozen Stage 6b artifact. I found two minor accuracy defects that should be corrected: the main text misdescribes the proof of the sharper coefficient sensitivity estimate, and one coverage row retains an obsolete statement that assignments are planned. Neither changes a theorem or requires a new argument. I recommend that the lead adjudicate these corrections. This report does not declare stage acceptance or replace the separate full-manuscript review cycle.

I reviewed the complete main narrative, abstract, introduction, definitions, principal statements and tables, worked examples, proof explanations, diagrams, conclusion, and relevant bibliography records. I reviewed the included technical statements throughout A01–A11 and the proofs materially supporting the main claims. In particular, I read the complete weighted, weighted-cactus, design, scalar/hybrid, and certificate developments and the material correlation proofs. For the earlier localization and law sections I checked their principal statements and the proof mechanisms on which those extensions depend. I inspected the coverage documents, delivery scripts, manifests, actual archive, extracted build and executable evidence. I did not read author, lead, peer, or historical review reports, and made no artifact repairs.

## Required findings

### R3-m1 — Incorrect description of the sharper sensitivity proof (minor)

Location: `complexity/narrative/05-design.tex:185–186`, referring to `prop:a-corr-sharper` in `complexity/sections/09-correlations-energy.tex`.

The main text says that the proposition proves the displayed estimate “through finite comparison.” The actual proof, beginning at approximately line 699 of A09, interpolates coefficients, adds a positive linear regularization, differentiates the state using the implicit-function theorem, bounds the resulting electrical response, integrates in the interpolation parameter, and passes to the limit as the regularization vanishes. This is not the finite circulation comparison used for the preceding, weaker bound. The distinction matters because the proof explanation is directing the reader to a particular treatment of zero and reversing flows.

The sharper estimate itself is supported. The regularized Jacobian is positive definite on the circulation space; the single-edge forcing formula and unit electrical flow bound give the stated constant; compactness and uniqueness identify the limiting endpoint states. Zero flows and reversals are covered.

Repair: replace “through finite comparison” with “by regularized electrical sensitivity and a limiting argument,” or an equally accurate short description. Retain the zero-flow/reversal claim.

### R3-m2 — Obsolete planned-assignment language in the final coverage map (minor)

Location: `coverage.md:47`, the row for `results/fixed-core-block-polyhedral-optimization.md`.

The row assigns the supporting result to A03, A04 and A06, but says “A03 proves the needed box specialization directly; other assignments remain planned.” This is inconsistent with the completed final inventory and actual included development. A04's `lem:a-law-dense` gives the dense-law extension using the fixed-core machinery, and A06's `thm:a-weight-global` uses the fixed-dimensional core for weighted optimization. I found no missing theorem here; the defect is the stale description of completion status and use.

Repair: describe A03 as the direct proof of the required box specialization, A04 as its dense-law extension, and A06 as its weighted-core application. Continue to exclude broader polyhedral/pooling applications from the paper's claimed scope.

## Scientific assessment

- **Model, localization and computational output (A01–A04).** Existence/uniqueness follows from the strictly convex primitive energy on conserved flows. The block decomposition, endpoint reduction, one-interacting-block argument, and bounded-dimensional box core support the stated topology-dependent algorithms. The cactus face argument preserves the two-free-load bound; the general block argument uses the stated rank-dependent face dimension. The bit-complexity statements concern rational additive values and rational nomination witnesses, with algebraic state evaluation handled separately. The dependence on block rank is correctly described as XP-type, not FPT. Fixed dense polynomial laws, fixed numbers of nonzero terms, and uncertain quadratic coefficients are not treated as interchangeable representations. I found no silent extension to arbitrary global operating constraints.
- **Exactness, observables and boundaries (A02, A03, A05).** The square-root-sum equivalence has the restricted graph/data scope stated in the main text and table. It is not promoted to general NP membership or to an exact polynomial-time algorithm. Arc-flow and simultaneous-state statements are distinguished from scalar potential values. Coordinatewise envelopes give safe hulls, whereas finite realization, restoration, and whole-region convexity have separate statements and obstructions. The pressure-filter and realization reductions retain their appropriate promise and threshold scope. Weak hardness and the later bounded-data strong gap constructions are distinguished.
- **Weighted potentials (A06–A07).** The tree case reduces to a rational quadratic problem; fixed global rank and fixed potential support give the claimed fixed-dimensional core. The general weighted face argument really establishes the stated O(rp) reduction and is not left open. Its two perturbation stages preserve the relevant aggregate information and control the free coordinates. The cactus compiler addresses sums of many block contributions through rational panels and a common sign treatment. The threshold-LP candidate construction includes ties; rounding and filter-margin hypotheses are explicit. Universal corner-hull, series-parallel/Wheatstone, deletion, nonlinear-law, and finite-restoration statements have distinct scopes. No claim equates convexification with exact finite realization.
- **Design and correlations (A08–A09).** The monotone polynomial-root result uses LP threshold tests, uniform coefficient/root separation bounds, and exact recovery of a rational optimizing polytope vertex. The capacities-to-linear-inequalities reduction has appropriate prior attribution. Independent cactus coefficient intervals produce exact attainable circulation intervals; the rational reconstruction argument handles a singleton interval separately, rather than assuming every physical circulation is rational. Convex minimization uses an inner rational box and a quantitative Lipschitz budget. Convex maximization and globally correlated families have separate strong hardness constructions with bounded data and a constant gap. The few-measurement result uses fixed-dimensional zonotope enumeration. The conic formulation includes a quantitative relative-interior ball, which is essential for its convex-oracle invocation. Operating filters can force irrational coefficients even at low rank; the rational feasibility recovery is conditional on supplied strict slack, with a separate polytope version. The sharper sensitivity theorem is sound, subject to R3-m1's description correction.
- **Completed many-block extensions (A10).** The scalar result treats arbitrary numbers of higher-rank blocks when the rank of each block is fixed. I checked the annihilating-polynomial construction, squarefree reduction, complex exceptional roots and their real projections, rational endpoint neighborhoods, disk/root bounds, geometric interval panels, and rational interpolation. These details matter: a claim about analytic approximation alone would not provide the required original-coordinate, rational-bit algorithm. The compilation and summation bounds are polynomial in the accuracy bit count under the fixed parameters. Fixed polynomial laws have their separately stated scope. The hybrid construction limits total noncactus rank and nomination dimension, combines that core with the cactus compiler, and does not require bounded total cactus rank. The remaining external question is specifically the higher-dimensional nomination case with arbitrarily many higher-rank blocks (fixed rank per block), beyond the scalar and fixed-total-noncactus-rank cases. It is not the already proved weighted face reduction, nor a claim to have resolved the general exact cactus question from the 2026 overview.
- **Certificates (A11).** The primitive-energy gap, rational lower bounds, reverse Bregman refinement, endpoint sign compatibility, goal-specific dual support and saved-data verification have distinct roles. The energy certificate covers zero and reversing flows. Endpoint optimality certifies an original coefficient scenario, not necessarily a rational physical state or potential value. Goal-support sharpness is over the specified quadratic circulation error set. Rational strict-Slater recovery is a witness statement with its stated hypotheses, not a general polynomial-time completeness claim. The implementation evidence does not purport to implement every abstract optimization algorithm in the paper.

I found the main/appendix relationship coherent. The main text provides usable definitions and proof ideas, and its references lead to included technical arguments rather than unwritten notes or a required companion paper. The anonymous title block is appropriate; I found no invented authors, funding, license or acceptance statement. The full PDF is long, but the 28-page main narrative, grouped results and appendix contents provide a usable reading order. I do not treat length alone as a defect.

## Primary-source checks and novelty

I inspected original statements, not only abstracts or search summaries. Online originals were downloaded only into the isolated temporary directory; local managed originals were read without alteration.

- Birkhoff and Díaz (1956), Section 5, Theorems 2′ and 3′, printed p. 438: primitive-energy stationarity, convexity/minimum and existence principles. These support the paper's attribution of the classical foundation.
- Duffin (1965), Theorem 0 and its proof, and Theorem 1 (printed pp. 306–308): electrical confluence and the embedded Wheatstone obstruction. The paper's passive nonlinear applications do not make these underlying principles new.
- Assmann, Liers, Stingl and Vera, original arXiv:1808.10241 manuscript, Assumption 4.8, Proposition 4.9, Lemma 4.10 and Proposition 4.11 (printed pp. 20–21): cycle monotonicity and capacity inequalities. The manuscript credits this antecedent and distinguishes its rational parameter recovery extension.
- Gotzes, Heitsch, Henrion and Schultz, [WIAS original preprint](https://www.wias-berlin.de/people/heitsch/GHHS16_Preprint.pdf), Theorem 6 and equations (43)–(44), and the discussion of node-disjoint cycle extensions: the explicit quadratic cycle formula and earlier computational setting are real antecedents, not replaced by a novelty claim about solving one cycle.
- Vigneron, original manuscript dated 21 October 2011, Section 2.3 and Theorem 6, printed pp. 7–8: bit-RAM approximation and its dependence on reciprocal accuracy. I compared the actual bounds and hypotheses with the paper's narrower polynomial-in-accuracy-bits claim.
- Binyamini and Novikov, [arXiv:1802.07577v2](https://arxiv.org/abs/1802.07577), Theorem 1, printed p. 2; Yomdin, [arXiv:1406.1719v2](https://arxiv.org/abs/1406.1719), Definitions 5.1–5.2 and Theorem 5.6, printed pp. 22–24; Borcea, Bögvad and Shapiro, [arXiv:math/0409353v2](https://arxiv.org/abs/math/0409353), Theorems 2–3 and surrounding hypotheses: these provide analytic/semialgebraic approximation antecedents. Their actual chart or exceptional-locus statements do not directly furnish the paper's same-coordinate rational panels and complete many-block optimization interface. The manuscript's narrow distinction is supported; this is not evidence of exhaustive priority.
- Dadush, [original dissertation](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf), Theorem 2.5.9, printed p. 48: centered convex body, weak membership, Lipschitz objective and rational feasible additive optimizer. I checked the exact feasibility conclusion, since weakening it would undermine the design/conic applications.
- Onn and Rothblum, original arXiv:math/0309083v1, Lemmas 2.1–2.3: fixed-dimensional zonotope enumeration/exposing directions. The few-measurement construction properly uses a classical principle.
- Klimm, Pfetsch, Skutella and Strubberg, original arXiv:2604.26882, Corollary 4 and Theorem 11: convex no-fixed-cost conductance design and an approximation result under its positive variable-cost/bounded-conductance assumptions. I verified that these are not equated with passive resistance uncertainty.
- Pfetsch's original 2026 overview, printed p. 10: the general nonlinear cactus hardness question remains stated there. The paper accurately separates its additive result and restricted exact square-root-sum classification from that broader exact question.
- Thür­auf's original 2022 booking manuscript, problem definitions and discussion on printed p. 7: maximum potential-difference optimization excludes the operating potential bounds it tests. This supports the manuscript's unfiltered-model distinction.

Limitations: I did not independently obtain the inaccessible Hasler–Wang full text, and do not use it for a theorem-level comparison. I did not independently verify Petras's full original paper in this review. The scalar approximation proof was checked directly rather than inferred from that citation. The checks above support the specific distinctions made in the manuscript; they do not establish an exhaustive novelty search.

## Coverage, archive and reproduction

The coverage inventory resolves to 308 distinct existing direct source paths, including 43 promoted potential-flow result files, 173 potential-flow note files, and 73 Python modules. I independently compared all 308 mapped files with the main checkout: they are byte-identical. Supporting dependencies, historical evidence and auxiliary checks are identified as such; they are not counted as additional new theorems. I inspected the Paper A-only scope of `verification/check_coverage.py` and the current delivery instructions. R3-m2 is the only coverage defect I found. I checked that Paper B (`paper-potential-flow/uncertainty`) and managed literature have no worktree changes.

All extraction, building, downloads and replays used `/tmp/s6b-r3-giknljda`, outside the checkout. The actual final archive extracted to `/tmp/s6b-r3-giknljda/potential-flow-paper-a`. All 63 payload hashes in its manifest matched; the 64th archive file is the manifest itself. The archive contains the selected scientific sources, verification code and retained evidence. I found no Paper B, managed copyrighted PDFs, raw external data, agent review reports or temporary build files in its payload. Generated Python caches appeared only after executing the extracted code.

Commands below ran from that extracted root unless indicated otherwise. `PY` denotes `/home/sgusev/miniconda3/envs/minlp-notes/bin/python`.

```text
PY paper-potential-flow/reproducibility/build_paper.py
PY -S paper-potential-flow/reproducibility/reproduce.py --output /tmp/s6b-r3-giknljda/exact.json
PY paper-potential-flow/reproducibility/reproduce.py --numerical --output /tmp/s6b-r3-giknljda/numerical.json
PY paper-potential-flow/reproducibility/package.py --output /tmp/s6b-r3-giknljda/repackage
```

Results:

- The Paper A-only build passed: zero errors, undefined references, undefined citations, duplicate labels and overfull boxes. I did not invoke the old two-paper build CLI. The built PDF has 216 pages and its extracted text is identical to the frozen PDF's text.
- Exact replay: 18 of 18 commands passed. This includes normal and optimized standard-library verification, saved base/envelope/goal/design witnesses, malformed-witness rejection, supplied-block cactus checks and asymmetric/sensitivity checks.
- Numerical replay: 28 of 28 commands passed, including the exact suite, scalar and structural diagnostics, Stage 6a experiments and the 10-case benchmark producer. Retained witnesses and numerical production are appropriately distinguished.
- Packaging from the standalone extraction succeeded and produced 64 files. I inspected the package selection, build wrapper, replay wrapper, README and dependency instructions.
- The scientific environment was Python 3.12.14 with numpy 2.5.2, scipy 1.18.1, sympy 1.14.0, networkx 3.6.1, cvxpy 1.9.2 and clarabel 0.11.1, matching the retained pins.

I inspected rendered PDF pages 7, 9, 10, 11, 13, 16, 20, 27, 199, 211 and 214, including both diagrams, the principal hull/boundary tables, the design statements and representative appendix/certificate material. The tables and diagrams are readable without clipping or collisions. I did not visually inspect all 216 pages. Successful replay validates the supplied evidence and verifier behavior, not every abstract algorithm asserted in the manuscript.

## Freeze integrity

At the start I verified the supplied manifest and archive hashes, all 43 `stage_files_sha256` entries, and the preservation record for the 11 technical sections. At the end I repeated the manifest, archive, PDF and all 43 stage-file checks; all remained unchanged. The only checkout file authored by this review is this report.

```text
process/completion-s6b-manifest.json
  a530e917bd4fee2ab9fd90af8f7c29ecddcbb64936abffab32b559f61c2dafb0
dist/potential-flow-paper-a.tar.gz
  23119436776b23c7e17d97293ee5376806d772bda5009e8dd009861b06ef30a2
dist/paper-a.pdf
  3421a6d8bd793665031aa535962d17f030805ccc3fdf8044625cd6d9e98054ee
```
