# Closure author report

Authored `sections/05-closures.tex`, `appendices/C-closures.tex`, and the
claim-by-claim `evidence/audit-closures.md`. The main section develops the
coefficient geometry, tight limiting cuts, smooth-face characterization,
strict A/B/BP closure obstruction, support-one improvement, and finite and
unbounded approximation factors. The appendix supplies complete general
certificate implications, compact rational witnesses and all retained
closure-specific numerical records.

## Proof map

| Source content | Full manuscript proof or final disposition |
| --- | --- |
| Orbit-closure Lemma 1(a)–(c) | `cl:blocking`, including converse separation and positive-cost single-cut limit |
| Theorem 2 | `cl:tight`, including bounded aggregate, zero-weight unbounded slots, all-minimizer tightness and affine Carathéodory |
| Proposition 3; Corollary 4 | `cl:smooth`, `cl:one-unused`, with full off-support characterization and direct bilinear regularity proof |
| Proposition 5 | `cl:gain`, supporting-face proof and abstract sharp example |
| Family parametrization; Lemmas 6–8 | `cl:bilinear`, `cl:point-parameters`, `cl:certificate-tools`, `cl:halfspace`, `cl:kept-boundary`; algebraic completion classification in `fd:completion` |
| Theorem 9 | `cl:counterexample`, conceptual proof from `fd:counterexample`; all finite universal certificates in `cl:finite-certificates` |
| Starting larger A example | Main paragraph after `cl:counterexample`; foundation geometry plus `cl:one-unused`; B claim retained only numerically |
| Proposition 10 | `cl:support-one`, `cl:support-one-certificate`, complete three-cut rational dual plus exact upper membership cover |
| Theorem 11(a) | `cl:bp-factor`, including new exact infimum attainment witness and rational recession certificate |
| Theorem 11(b)–(d) | `cl:unbounded`, `cl:wcorner-proof`, all integer data, elementary completion proof, and analytic sharp BP proof |
| Lemma 12 | Qualitative recession argument inside `cl:wcorner-proof` |
| Proposition 13 | `cl:finite-factor`, proof in main text |
| Corollary 14 | `cl:no-uniform`; qualitative dependence `dp:vanishing`, quantitative rate `dp:certified-sharpness` |
| §6.2 factor certificate | `cl:local-factor`, exact six-edge lower-corner proof and completed-family closure point |
| §6.3 comparison | Final main paragraph using ABP2018, with explicit differing hypotheses |
| §7 numerical survey | `cl:numerical-records`, all eleven rows, one-sided interpretation and 17/18 comparison count |
| §8 numerical rebasing | `cl:numerical-records`, all six trajectories and zero-cost limitation |
| Lemmas 15–16 | `cl:box-certificate`, `cl:sdp-certificate`, full proofs and coverage/free-coordinate conditions |
| Unrestricted fixed-corner closure | `cl:unrestricted`, using `fd:dominant` |
| Polyhedron rank-one counterexample | `cl:unrestricted`, using full proof at `fd:rank-one-example` |
| Process/review/failed-search records | Evidence audit, not mathematical dependence |
| Open extensions | Final appendix paragraphs; no established result depends on them |

The appendix’s finite certificate table requires packaging five box JSONs,
three current SDP JSONs and the saved sixty-set record. The audit gives exact
original paths and SHA-256. The checkers have complete instance inputs and no
knowledge-base or repository-module dependency. Box verification requires
SymPy in addition to the standard library; SDP verification requires only the
standard library. Their names in the appendix are relative supplement file
names so the manuscript itself has no repository-path dependency.

## Corrections and strengthening

The four-ray auxiliary A lower bound now has the necessary range
0<ε≤√2. BP coefficient a₁=7/2 attainment is proved exactly. The W BP proof
uses an exact congruence exchanging rays, removing two fragile admissibility
displays from the original argument. The support-one lower proof needs only
three rational sets and an explicit rational dual, while preserving the
archived sixty-cut optimum as a finite-relaxation value. The general
smooth-face theorem now states the complete unused-coordinate convex
domination criterion. BP is explicitly the transformed point-rule completion
family; its uniform zero guarantee is proved, not left open.

The appendix does not promote any numerical closure estimate to an upper
certificate or equality. It labels support-one B nonexactness at that corner
as uncertified. It keeps the local Thm14 A/B finiteness question open.
Numerical survey labels R1–R8 have complete vertex/ray coordinates and
original identifier mapping in the evidence audit. Defined analytic corners
use semantic example names and cross-references; old experiment identifiers
do not appear as undefined manuscript examples.

## Targeted checks

Exact symbolic/rational checks are itemized in `audit-closures.md`; no
computational experiment or archival verifier was rerun. A temporary
LaTeX harness containing only the two authored fragments and shared macros
compiled with `pdflatex -interaction=nonstopmode -halt-on-error` to 12 pages,
without errors or overfull boxes. Cross-section references and bibliography
remain for integration. Scoped `git diff --check` passed. No project-wide
verification or CI inspection was performed.
