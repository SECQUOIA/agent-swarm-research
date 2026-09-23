# Stage 1 author report

Date: 2026-09-13. Scope: foundations, manuscript scaffold, topic coverage and
source-access map. This record precedes the required five-reviewer gate; it is
not a claim that the stage or paper has been accepted.

## Files authored

- `main.tex`: standalone build driver; blank author field; later abstract and
  introduction deliberately left to synthesis after accepted technical stages.
- `macros.tex`: packages, theorem environments, matrix/statistical notation.
- `references.bib`: primary foundation references plus a few established
  later-stage references. No fabricated manuscript author names.
- `sections/01-foundations.tex`: 452 lines of finished foundation prose, proofs,
  examples and scoped source comparison.
- `README.md`: current build, development status and seven-stage process.
- `process/coverage.md`: all substantive measurement-design families mapped to
  main sections/appendices; exact Markov and scalar prior-art corrections,
  related spectral/matroid results, all certificate families and empirical
  limitations included. Dynamic relaxation/storage/conflict work excluded with
  reasons, while kinetic sensitivity checks remain included.
- `process/literature.md`: actual source inspection, versions, primary links,
  access limits, corrected metadata, and bounded pointers for later authors.
- `build/main.pdf` and normal LaTeX products, including `build/stage01-build.txt`.

Root-owned `PROCESS.md` and `process/root-investigation.md` were preserved.
No files outside the new paper folder were edited. Existing source-audit code was
executed read-only; temporary source extraction/rendering used `/tmp/`.

## Content and interfaces

The model uses n candidate packets, packet dimensions d_t, parameter dimension p,
full known covariance R, nominal sensitivity F and PSD prior/regularizer J_0.
It derives true marginal Fisher information and distinguishes exact Gaussian
information from local design/estimator approximations, prior meanings and
parameter-dependent covariance terms. Criterion definitions separate trace
information from conventional A-optimality; positive definiteness, singular
ranges, coordinate changes and global rate-swap ambiguity are explicit.

The gating comparison includes its equality condition, noise-side-information
interpretation versus conditioning on actual responses, rational counterexamples,
monotonicity of true information, operator Kantorovich sandwich and rank refinement,
sharp design loss, weak-correlation expansion, diagonal/block scaling, and a valid
contract for reusing a gated upper bound after true-model re-evaluation. It also
proves independent-time pattern summation and states precisely which Wang
manuscript/software versions support the model correction.

Later sections can cite stable labels `eq:true-information`,
`eq:augmented-information`, `eq:certificate-contract`, `prop:gating`,
`prop:kantorovich`, `eq:rate-swap`, and `eq:source-covariance`.
The coverage record gives the revised stages agreed with root: 2 locality;
3 approximation; 4 relaxation/certification; 5 experiments; 6 synthesis;
7 whole-paper review. The supporting spectral/matroid result must be kept
separate from the implemented correlated-covariance solvers.

## Validation performed

1. Re-extracted primary Liu and Wang originals using `pdftotext -layout` and
   visually inspected the key Wang coefficient page (accepted-manuscript PDF
   p.10, printed p.9) and Liu Proposition 2/criteria page (PDF p.7, p.3515).
2. Executed the existing exact source-audit script with the actual unchanged
   author coefficient methods:

   ```sh
   code/research_20260912/.venv/bin/python \
     code/measurement_selection_source_audit.py \
     /tmp/minlp-measurement-source-audit-20260912/measurement-opt/measure_optimize.py
   ```

   All 64 six-channel selected-pattern Liu-identity/PSD comparisons and eight
   independent-noise controls passed; rational witnesses matched 1, 16/7,
   8/7 and 1/7, and the three-sensor optimizer reversal. Unchanged author
   methods returned 2.28571428571 and 1.14285714286. A pre-existing source string
   emitted a Python invalid-escape SyntaxWarning; checks completed successfully.
3. Exact SymPy recheck of source C_0 leading minors gave [1,399/100,791/25].
   Corrected a transient draft determinant transcription (15873/500) before
   handoff; positivity and every derived model statement remain valid. Root
   independently flagged the same transcription while it was being corrected.
4. Additional exact arithmetic exercised all 28 subsets of three rational
   2-parameter covariance examples of sizes 2,3,4, using R=I+BB^T,
   m=1, M=1+tr(BB^T), and a singular prior. Both gated PSD inequalities and
   common kernels passed. This is a finite sanity check; the paper gives the
   full proofs and the five reviewers must assess them independently.
5. Verified Pázman et al. final page range through the author-institution
   primary record and corrected it to 5659–5691. Hainy arXiv version and Lee
   publication date were checked online. Source/claim status is in literature.md.
6. Ran

   ```sh
   latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
   ```

   Current PDF: 7 pages. Final `build/main.log` has no warning, overfull-box or
   undefined-reference/citation matches. Blank author metadata confirmed by
   `pdfinfo`. Mathematical content is text/typeset equations; no generated
   illustration or copied source image is embedded.

## Newly identified issues and downstream obligations

No invalidating mathematical issue was found in the foundations. The draft's own
minor determinant and bibliographic transcriptions were corrected. Crucially,
several Sep12 priority notes have stale access statements: the local knowledge
base now contains Sep13 user-supplied full texts for Patan–Bogacka, Vecchia and
other relevant papers. Later authors should use current sources before supporting
novelty claims. The paper does not repeat old “unread” statements as current facts.

The current source-data D/conventional-A comparison is numerical, while trace is
already exact; root plans exact D/A ranking certification in stage 5. That is a
development obligation, not an assertion in the foundations. No broad practical
superiority, physical covariance validation, continuous uncertainty guarantee,
new path hull, first scalar FPTAS, or new filtering/matrix inequality is claimed.
The manuscript is intentionally not described as submission-ready at this stage.
