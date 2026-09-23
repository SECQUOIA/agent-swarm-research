# Whole-paper round 01, reviewer 12

**Verdict: PASS.** I found no demonstrable major or minor defect in the frozen manuscript. This is a fresh whole-paper review, with additional attention to reproducibility and independent exact checks. Prior passing reviews and stored validation labels were not used as evidence of theorem truth.

The target is `process/snapshots/whole-round01/main.pdf`, 111 pages, SHA256 `912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084`. I checked that hash and every entry of the frozen input manifest (82 entries) and review-context manifest (10 entries), including a final check after the review. There were no mismatches. I did not edit the snapshot or manuscript, read other reports from this final round, or delegate the review.

## Coverage

I read the complete manuscript source, including every proof, appendix, and bibliography entry. Exact files, relative to the frozen directory, were `main.tex`, `macros.tex`, `references.bib`, and all of the following under `sections/`:

- `01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`;
- `07-positive-boxes.tex`, `08-exact-complexity.tex`, `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`;
- `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, `17-synthesis.tex`;
- `appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, `appendix-integer-comparison.tex`.

I also read frozen `README.md`, `PROCESS.md`, `process/review-protocol.md`, `process/whole-paper-review-assignment.md`, `process/scope-proposal.md`, `process/claim-coverage.md`, `process/stage-06-author.md`, `process/stage06-corrections.md`, the reviewer-focus assignment, and the review-context manifest. The full scope ledger was compared with the manuscript's proved results, bounded developments, classical comparisons, and stated open boundaries. No required topic was silently replaced by a result about a different notion of relaxation strength.

I read `../literature/AGENTS.md` before accessing originals. Primary-source checking was passage-specific, as follows; page numbers below are PDF pages unless explicitly described otherwise. These are actual independently inspected dependencies, not a claim to have reread every cited paper in full.

- Luedtke et al.: original pp. 21–23, particularly Conjecture 1 and its scope. Boland et al.: original pp. 4–6 and fulltext theorem/proof passages for the cut-range characterization and its extension. Davidson–Donsig: original pp. 1–4 and 6–9 for the real Schur multiplier/projective-norm framework and its distinct pattern formulations.
- Sherali: Theorem 3, fulltext pp. 8–9, with the original equation (13) on PDF p. 8 visually checked because extraction loses mathematical content. Hassin–Tamir: scanned original PDF p. 3, printed p. 381, visually checked for Theorem 3.1 and the recursive series-parallel convention. Cornuejols: Theorems 6.5 and 6.13 and surrounding arguments in the local source text for the Camion/minimal-non-TU and balanced-matrix dependencies. GLS: Theorem 6.4.9, printed p. 179, for the precise well-described-polyhedron oracle equivalence; I did not reprove the external algorithm.
- Schoenebeck: original pp. 7–11, including the width convention, Theorems 11–12, and the signed-character/Gram construction in Lemma 13; pp. 17–19 for Theorem 21, Proposition 22, and the random-formula width argument. I checked the manuscript's parameter substitution and degree conventions, and visually inspected p. 7.
- Kronqvist et al., P-split: original pp. 4–7 for assumptions, retained domain and formulation, and pp. 15–16 for Definition 4, Theorem 6, and its proof. Altschuler–Boix-Adsera: local fulltext pp. 53–56, Section 7, for the encoding and logarithmic-accuracy comparison; this check used fulltext rather than a fresh visual reading of those original pages.
- Fawzi–Parrilo: original p. 3 for Theorem 1 and its quantitative cone parameters. Lee–Raghavendra–Steurer: original p. 23, Theorem 3.8/equation (3.11), and pp. 32–34 for the pseudo-density input and subsequent bound; p. 23 was also visually checked. Braun et al.: original p. 18 for the hard correlation-polytope approximation pair and its LP scope. Starr: original pp. 12–13, Appendix 2, Lemma 2 and corollary, including their proof.
- Etessami–Yannakakis: original pp. 26–28, Theorem 5.2 and the signed-circuit normalization/amplification proof. Belotti et al.: original p. 14, Theorem 4.1 and its nonempty-limit qualification. Lubin et al.: original p. 12, Lemma 4.1 and its midpoint proof. Beach et al.: the cited combined preprint, original p. 21, Section 5.1.1, for the distinct upper- and lower-side dyadic square errors.

Local originals came from the literature packages and the existing source cache `/tmp/minlp-relaxation-limits-sources/`. No source access issue prevented these checks. Source-checking limits are listed below.

## Findings

None. There are no major or minor finding IDs and no requested repairs.

In particular, the corrections documented in the frozen author record are present with the necessary mathematical qualifications: retained-domain P-split exactness, shared-scale and zero-scale conditions, full product localizers, the order-one quadratic law's possible departure from the lifted graph, and the nonempty-limit premise in the FBBT comparison. I independently checked the arguments supporting those qualifications.

## Independent verification

### Proof reconstruction and attempted falsification

For Sections 1–8 and the associated appendices, I checked the half factors in the bilinear cut-range formula, the distinction between full signings and unrestricted coefficient arrays, face reduction, and the zero-gap cases. The positive-coefficient expansion requires the stated common law; the balanced-box argument keeps its ambient law fixed as coefficients vary. I checked the dyadic/radix capacities and attainment argument, inactive mass and fixed-point mixing in the harmonic construction, finite constants, and limit versus finite attainment. The cubic mixture and coefficient-removal arguments cover their different parameter regimes; the exact certificates below provide additional independent evidence. In the structural results I checked incoming-variable ownership, the reduced outgoing polynomial, feedback gluing, odd-cycle slabs, matching-dual rational encodings, and the active/blocking alternatives in the series-parallel proof. The Camion argument is used under the relevant matrix hypotheses.

For the complexity reduction, I reconstructed the second-order expansion with the uniform remainder and rational precision budget. The manuscript proves weak hardness with accuracy encoded logarithmically; it does not turn that argument into fixed-error hardness. For Sections 9–15, I checked the fractional-cardinality homogenization and Gram identity, all assignment localizers and their allowed degrees, endpoint interpolation on arbitrary finite coordinate domains, and positivity of the tensor product through the relevant principal moment matrix. I checked the relative-gap block parameters and the treatment of the unique asymmetric block.

For XOR, deterministic substitution has the stated degree cost; it is not justified by treating it as probabilistic conditioning. I tracked the square/localizer degree through the `4rD` budget, checked the augmented PSD matrix used for exact quadratic realizability, and checked the support bound from independent parity rows. In particular, rank controls the union of supports through a basis, rather than by assuming all restricted equations involve disjoint variables. The lifted order-one argument retains its linear-objective and degree conditions. The two upper-certificate arguments use different orders with the appropriate premises.

For the comparison appendices I reconstructed the point-packing covariance construction and its analytic PSD proof; the shared-scale hull and zero-scale recession argument; the retained-box P-split counterexample and translated-ball projection; the rank-one exposed face and stability estimates; the FBBT least-fixed-point and primitive-update arguments; and the integer midpoint/area/width and shared binary-expansion comparisons. Exact representation, approximation, local node strength, and global extension size remain distinct. The external PSD-rank bound is substituted with its stated pseudo-density normalization and parameter restrictions.

### Fresh build and correspondence

All fresh build operations used my own copied inputs in the explicit working directory:

`verification/reviewer12/whole-round01/build/`.

Running `python verification/build_and_check.py` there completed with exit code 0. The newly generated `build/verification/build-report.json` reports no warnings, no duplicate labels, and a match between the printed Stage 02 checker and its source. The result is a 111-page PDF. Its SHA256 is `f24dfee853f02e5b39eb47622fd30344e0afbf0f2d067a4b3ac09c42ec8daa91`; I do not claim binary identity with the frozen PDF. PDF timestamps/metadata can differ. More directly relevant to content, independent `pdftotext -layout` extraction of the frozen and rebuilt PDFs produced byte-identical text across all 111 pages. The comparison is recorded in `verification/reviewer12/whole-round01/pdf-text-comparison.txt`.

The copied verification directory contains pre-existing artifacts as well as fresh outputs. Only the explicitly described fresh build and replays are evidence from this review; copying an old JSON file is not verification.

### Checker replays

I reran the following seven frozen scripts on the copied inputs using `/home/sgusev/miniconda3/envs/minlp-notes/bin/python`, with the build directory as explicit working directory. All exited 0. `verification/reviewer12/whole-round01/replay.json` records the script hashes, exit codes, stdout and stderr.

- `check_complete_signings.py`: exact exhaustive switching representatives for K2 through K7, giving minimum cut ranges `1, 2, 4, 4, 5, 8`, together with witness/face checks. The K6 extension witness has the stated full ratio `21/10` and face ratio `3`.
- `check_stage02_finite.py`: exact finite three-group and two-level enumeration, including 275,697 three-count states and 564 two-count states. The finite ratios and the small/large examples agree with the text.
- `check_stage02_symbolic.py`: exact polynomial identities and five Bernstein rows, including uniform slack `901/120000`, lower bound `1610000/743033`, and the stated finite m=36 bounds.
- `check_radix_cutoffs.py`: 120 exact finite profiles. These are checks on the general digit-reversal proof, not a proof of it by enumeration.
- `check_unequal_box_bipartite.py`: 16 symbolic vertex residuals, four exact marginal laws, and ratio `2*(epsilon+3)/(3*epsilon+4)` with limit `3/2`.
- `check_order_one_upper.py`: 3,375 boxes and 216,000 exact quadratic inequalities/identities. For 250 examples, SciPy LP output selected candidate distributions and rational reconstruction then checked the claimed feasible-law equations and inequalities exactly. This is not an independent exact LP-optimality certificate. The examples include 242 supports outside the lifted graph and 226 values strictly below the actual node graph minimum, supporting the manuscript's qualification.
- `check_point_packing.py`: 55 rational constructions and 151,032 RLT inequalities, with the pair distances checked exactly. PSD is supplied by the analytic projection-block proof, not a numerical eigensolver assertion.

### Checks written independently for this review

`verification/reviewer12/whole-round01/independent_exact.py` uses rational arithmetic and SymPy, independently of the manuscript checker implementations. Its final output is saved as `independent_exact.json`.

- I integrated the actual balanced-orientation outcomes, with exact interval lengths, for 456 nondecreasing mean vectors from the quarter grid in dimensions 2–6. The coefficient inequality holds for every relevant order, including boundary means.
- I checked 80 instances of the Gram coefficient identity as polynomial identities in the free parameter t, for degrees 1–5 and several ambient sizes. Thus these checks do not rely on division by a possibly vanishing falling factorial.
- I constructed the full remaining-variable assignment-localizer matrices for `s=7`, `t=7/2`, `r=2`, for all 15 symmetry representatives of zero/one assignments of size at most 4. SymPy certified positive semidefiniteness using exact rational matrices.
- I exhausted all subsets of nonempty parity rows of support size at most 2 on four variables, checking rank, the support-union bound, and every consistent right-hand side generated by a Boolean witness: 16,384 systems. The exact number of satisfying assignments is `2^(4-rank)`.
- I checked the exact PARTITION expansion remainder and separating construction on all 363 lists of lengths 1–5 with entries 1–3, after the reduction's doubling step. This checks the finite YES witnesses and NO integer-separation condition, not a numerical approximation to the scalar envelope.
- I checked the primitive FBBT recurrence with exact rational arithmetic for three small circuit sizes. The first crossings of one half occur at updates 3, 11, and 178 and satisfy the stated doubly exponential lower estimate.

### Rendered manuscript

I visually inspected rendered frozen PDF pages 1, 3, 12, 21, 37, 52, 65, 78, 86, 96, 103, 107, and 111, including the opening material, dense mathematical pages, appendix material, code, and bibliography. I found no clipping or broken layout on this sample. Renders and contact sheets are in my `visual/` artifact directory. The whole-document text/build checks cover all pages; visual inspection does not.

## Remaining limits

This review is not formal proof verification. Finite exhaustive computations establish their finite claims, symbolic identities establish the checked identities, and neither alone establishes every universal theorem. The general inequalities, PSD constructions, complexity reductions, and algorithms were assessed by reading and reconstructing their proofs.

I did not independently rerun every verification script or validate every stored historical JSON artifact. No proprietary solver was needed for the checks reported here. The one numerical LP search described above was followed by exact feasible-certificate checks, with the stated optimality limit. The build was reproduced in the available environment, not a newly provisioned operating-system/container matrix, and binary PDF reproducibility was not established.

I read all bibliography entries, but did not independently audit every cited original or reprove every external theorem. In particular, the sharp real Khintchine constant, the full classical matching and oracle-equivalence algorithms, and the complete external LP/SOC/PSD lower-bound proofs remain cited dependencies. I inspected the needed statements and selected proofs of the latter where listed above; this does not audit their entire dependency chains. I did not newly inspect the originals for all contextual or historical references, including every point-packing predecessor, Balas/Wu comparison, and recent proof-complexity comparison. The manuscript's self-contained arguments in those portions were read. These limits do not reveal a missing assumption or unsupported extension of the cited results in the frozen text.

The manuscript explicitly leaves several sharper constants and broader formulations open. I found no place where those boundaries were used as if already proved. No further repair is required by this review.
