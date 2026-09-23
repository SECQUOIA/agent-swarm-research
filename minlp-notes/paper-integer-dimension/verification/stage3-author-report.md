# Stage 3 author report

Date: 2026-09-05. Author agent: `/root/stage3_author`.
Status: mathematical draft completed; build and handoff checks recorded below. This is not a stage gate or a claim of formal verification.

## Scope and organization

The new file `sections/03-scalar-nonlinear.tex` contains five LaTeX sections: finite scalar convex geometry; certified scalar compilation; positive polynomial systems and allocation; pure powers and inverse interpolation; relative-error and rational-encoding boundaries. All eleven stage 3 canonical result rows are mapped in `coverage.md`. All twelve previously explicit substantive supporting rows are mapped, and the general signed P/Q endpoint gadget is added as a thirteenth stage 3 row (34 substantive supporting developments overall; existing notes index unchanged).

The material includes complete proofs of scalar finite two-bit comparison and three-piece refinement; truncated curvature mass and its potential estimate; raw-mass and allocation counterexamples; positive-sector and signed adaptive-panel certified quadrature; stronger input-accurate normalized quantiles; the seven-bit mass compiler; the eleven-bit hybrid convex-polynomial compiler; finite and constructive separable comparisons; direct feature geometry; baseline and sharper scalarized allocation laws; dense exact prefixes and sparse rounded endpoint circuits; finite pure-power counts; explicit positive rational Stieltjes approximation; general P/Q endpoint products; reciprocal and binary rational-exponent constructions; near-zero relative-error impossibility and truncated double-logarithmic count; tight rational MILP encoding and the same-four-bit MISOCP separation.

Accepted sections 01/02, macros, and main were not edited by this author. Root added the main input. New bibliography entries were appended; source citations and coverage mappings were added in the author-owned files.

## Mathematical checks and interpretation

I read all eleven canonical source files and their substantive dependencies in full, including the signed and positive integration notes, feature curve identities, allocation gap, Stieltjes proof, finite pure-power precursor, relative-error note, scalar two-bit lemma, general P/Q gadget, and LP/conic encoding arguments. Existing source review labels were not used as proof substitutes. I reconstructed the branch-mass estimate, telescoping potential, inverse modulus, adaptive Taylor-tree depth/count, quadrature rational conditioning, supporting-multiplier homeomorphism argument, layer curvature bound, rounded-power induction, inverse-log/exp error arithmetic, and row-wise determinant bound while drafting.

The stage develops source sketches into a coherent standalone dependency chain. In particular the accepted stage 2 block-logdet oracle is specialized explicitly instead of reproving its scalar special case, and the positive and signed curvature proofs share a fully stated numerical conditioning argument. The two inverse-power algorithms and the dense Stieltjes alternative remain distinct. Finite real existence, polynomial dense or sparse construction, rational encoding, and solving time are distinguished. The conic construction is outside the paper's binary-linear `p_bin` definition. Its exact optimality equations give no numerical tolerance-stability claim.

Root read the entire draft in successive chunks and requested local clarity repairs before freeze: polynomial length of a common output denominator; dispatching zero curvature before defining degree; explicit bracket-endpoint update directions; nondecreasing rather than strictly increasing curvature; nondegenerate rational interval; bounded chord slopes rather than Lipschitz slopes; outward normal-cone definition; and one literal TeX tab typo. These were corrected. No substantive theorem was weakened and no open boundary was represented as solved.

Root independently ran sixteen existing stage 3 scripts plus a new 465-case exact general P/Q interpolation check. Their provenance is in `verification/stage3-20260905T190112Z/manifest.json`; this author does not claim to have implemented the full certified quadrature or final generated MILP circuit. The explicit analytical constructions prove the bit-time assertions; numerical scripts are supporting evidence.

## Primary-source checks and attribution

- Read `literature/AGENTS.md`; no original research or local literature package was modified.
- Avis et al., arXiv:1408.0807v5, local original and text, Section 3/Lemma 1, pp. 7–8: continuous circuit gate variables are forced by Boolean inputs. Bibliography uses the corresponding 2019 Discrete Applied Mathematics article metadata. No generic compiler priority is claimed.
- Adams–Henry, `SAND2012-0505P`, fetched from OSTI; Section 2 explicitly represents discrete function values and their continuous-weight products with the original index binaries. Cited as the checked report rather than assuming final journal pagination.
- Sagraloff–Mehlhorn, arXiv:1308.4088v2 (2015), fetched and read Theorem 36: integer-polynomial real-root isolation/refinement is polynomial in degree, coefficient bits, and requested output precision. Rational square-free preprocessing and exact sign testing are described separately.
- NIST DLMF Section 3.5(v), opened on 2026-09-05: Gaussian positivity/exactness is credited, while the manuscript proves the specific Taylor error and rational conditioning needed here.
- Codsi–Ngueveu–Gendron, CIRRELT-2021-39, fetched; root checked Sections 3–5 for greedy maximal segmentation, dichotomy per enumerated segment, and additive piece-splitting costs. The manuscript cites the report and distinguishes random access/compact representation from an explicit segment list.
- Simchowitz et al., arXiv:1808.04523v3, root's fresh extraction checked at Lemma 2.1 and Definition 1: the chord/midpoint bound and accuracy-dependent endpoint-corrected sampling measure have direct antecedents. Their target is sampling complexity.
- Teles–Castro–Matos, local 2013 JGO article, title page and opening modeling discussion checked: radix disaggregation and polynomial/signomial MILP approximation are established. The separate EJOR univariate-parameterization publisher page could not be opened in this pass; no full-proof access to that source is claimed.
- Bonito–Pasciak, arXiv:1307.0888, opened and checked Section 3.3/equation (37)/Lemma 3.4: substitution lambda=1/t gives positive resolvent sums for t^gamma. The manuscript's rational bit bounds and exact endpoint normalization are proved explicitly. Local metadata supplies the 2015 Mathematics of Computation publication.
- O'Donnell2017 local primary text, opening discussion and repeated-squaring example checked; root additionally checked pp. 1–4. Wang2024 local primary metadata and root's pp. 1–6 check support narrow credit for logarithmic power-cone lifts. No new conic-duality or general long-solution phenomenon is claimed.

Downloaded author source-cache artifacts (PDF SHA-256):

- `sagraloff2015.pdf`: `ebe5df34d8114ba956d00c298ca610a0c59857f1d3a86d3a5429d9844da10c9e`.
- `codsi2021.pdf`: `0f0d524f1348f7392416f7f8c565eb8bd7ad4d715e94fdb2ee9821b6aa7a581b`.
- `adams2012.pdf`: `bb820eef92fe0c6e36cc0a2b5045e0baffe3dbf672ce94ff76bc0a904e68d4d0`.

Bounded source checks establish precise antecedent credit, not exhaustive priority. General convex sparse polynomials and arbitrary coupled mixtures do not inherit the dense scalar constant-gap theorem without further work. Later vector developments remain stage 4.

## Build and handoff

The combined `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` build succeeds: 63 pages. `verification/check_manuscript.py` reports 198 labels and 32 bibliography entries, with no duplicate labels/keys or unresolved references/citations. The final TeX log has no Warning, Overfull, Underfull, or undefined entry. Initial typography warnings and one label collision were corrected before handoff. The final build transcript is `build/stage3-author-build.log`.

Rendered and visually inspected pages 44 (signed adaptive quadrature proof) and 59 (LP encoding proof and conic section transition); equations, margins, and text are legible. Images are `build/stage3-author-page44.png` and `build/stage3-author-page59.png`. Active coverage local links were checked, including the added P/Q source row. No unrelated research files were modified. The source hashes in `verification/stage3-author-hashes.json` identify the handoff state. Editing is stopped for the root freeze and fifteen-reviewer stage loop.
