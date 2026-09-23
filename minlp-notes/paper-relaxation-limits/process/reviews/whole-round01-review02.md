# Independent final whole-paper review 02

**Verdict: PASS.** I found no major or minor defect requiring repair in the assigned frozen manuscript. This is an independent assessment of the final paper, not confirmation of earlier stage verdicts.

## Coverage

The target was `process/snapshots/whole-round01/main.pdf`, 111 pages, SHA-256 `912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084`. I verified that hash and all 82 entries of `manifest.json` and 10 entries of `review-context-manifest.json`, with no mismatch.

I read the entire frozen `main.tex`, `macros.tex`, and `references.bib`, including the abstract, introduction, roadmap, synthesis, every proof and appendix, and all bibliography entries. Specifically, the complete section files read were:

- `01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`, `07-positive-boxes.tex`, and `08-exact-complexity.tex`.
- `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`, `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, and `17-synthesis.tex`.
- `appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, and `appendix-integer-comparison.tex`.

I also read the frozen review protocol, whole-paper assignment, reviewer focus, scope proposal, complete claim-coverage ledger, Stage 06 author record and correction log, and README. I checked the coverage ledger against the manuscript; I did not freshly audit every underlying historical repository note. I did not read another report from this final round, delegate work, or edit the manuscript or snapshot.

Before inspecting local originals I read `../literature/AGENTS.md`. Primary-source checks were targeted at the inputs and comparisons used by the manuscript:

| Source | Material inspected |
| --- | --- |
| Luedtke–Namazifar–Linderoth | Original concluding Conjecture 1 and introductory formulation/upper-envelope distinctions. The conjecture's actual scope agrees with the manuscript's counterexamples. [Author-hosted paper](https://jlinderoth.github.io/papers/Luedtke-Namazifar-Linderoth-12-TR.pdf). |
| Sherali | Original pp. 252–253, equation (13), Theorem 3 and the opening proof, checked against the positive-box predecessor discussion. [Accessible original](https://math.ac.vn/uploads/files/9701245.pdf). |
| Davidson–Donsig | Original Theorems 1.1–1.2 and 2.3–2.7, including the weighted formulation and real Grothendieck norm comparison. |
| Cornuéjols | Theorems 6.5–6.6 and 6.13 and the mixed-right-hand-side balanced-matrix discussion/proof; the Camion characterization was treated as an external theorem. |
| Hassin–Tamir | Visually inspected scanned original p. 381, Theorem 3.1 and terminal series/parallel definitions; text extraction was unusable. |
| Schoenebeck | Random-instance model, Definition 10, Theorems 11–12, Lemma 13 and its construction/proof, the main proof's use of the lemma, and the relevant Proposition 22 appendix argument. |
| Fawzi–Parrilo | Original Theorem 1, its fixed-block constants, and the Lorentz-cone connection. |
| Lee–Raghavendra–Steurer | The quantitative Theorem 3.8 input, equation (3.11), and the fractional-cardinality pseudodensity construction and norm estimate used in the correlation-face comparison. |
| Braun et al. | Original fixed-dilution hard pair and Theorem 6(i). |
| Kronqvist–Misener–Tsay | Original formulation (including retained `X` and minimal auxiliary-variable convention), Corollary 3, Definition 4, and Theorem 6 with its complete proof. |
| Etessami–Yannakakis | Original Theorem 5.2 and the sign-normalization/complement-detector reduction used in the FBBT comparison. |
| Belotti et al. | Original Theorem 4.1 and the nonempty-limit qualification and discussion. |
| Lubin et al. | Original Lemma 4.1 and its midpoint-parity proof. |
| Beach et al. | Original section 5.1.1 maximum square-approximation error and its distinction from the smaller opposite error. |

I additionally checked the available Boland text's cut characterization and relevant theorem statements. These are targeted checks, not a claim to have proved every external source theorem or inspected every cited original. Remaining external-source limits are recorded below.

## Findings

None. No repair is requested.

In particular, I found the manuscript appropriately distinguishes supremum lower bounds from attained finite ratios, and distinguishes pointwise widths, exact scalar-envelope complexity, node relaxations, spatial certificate size, and global extension complexity. I found no unsupported transfer between those models in the complete reading.

## Independent verification

### Universal and cubic arguments

I reconstructed the vertex-law formulation, common positive upper envelope, term deficiencies and positive-box expansion. The direction of the box comparison is correct. I checked the signed bilinear cut/polarization argument, induced-grid restriction, fractional-flow density bound, random-sign lower bound, interior perturbation, and Schur-norm transfer.

For the dyadic universal lower family, I checked the cutoff lower bound without assuming nested anchor events, the two attaining count profiles, integer counts and bit-reversal hitting argument, and the XOR shift restoring individual marginals. The interpolation to all large integer dimensions preserves the claimed first-order asymptotic. I separately checked the generalized-radix cutoff and the joint parameter regime used for structural width.

For the harmonic upper bound, I integrated the proposed conditional failure law to recover each marginal, checked zero failure means and inactive failure mass, and derived the two deficiency guarantees. The fixed-point tangent argument produces the stated common mixture. I checked the finite Lambert bound and the distinction between its second-order upper certificate and the first-order two-sided asymptotic. In particular, the paper does not claim a matching second-order lower bound. The fixed-parameter reciprocal expansion and the optimized parameter expansion are used in their appropriate regimes.

I checked cloning in both directions: conditional expected clone products and a realization of every original law. The random unit-coefficient argument controls all vertices and total weight, and its dimension is allowed to grow. I also checked the finite probabilistic and explicit unit-coefficient consequences.

For cubics I reconstructed the three coupling guarantees, their boundary cases and the `31/12` mixture; its minimax assertion is confined to the specified mixture class. I rederived the scalar Hessian and the constrained and unconstrained minimizers underlying the positivity certificate. The analytic family establishes the claimed supremum lower bound `1610000/743033`; it does not establish convergence of actual family ratios to that number, and the paper explicitly says so. The two-level family has the stronger matching limiting statement supported by its square identity.

A new checker, `verification/reviewer02/whole-round01/check.py`, independently encodes these finite falsification attempts. It is not a rerun or copy of an author checker. It passed:

- Exact symbolic reconstruction of both scalar lower polynomials, all five quartic Bernstein identities, all 25 coefficients, their minimum `901/120000`, and the two-level square identity.
- Exact integer/rational verification at all 275,697 three-group count states for the 18-, 24-, and 192-variable examples. The minorants are valid everywhere, the listed laws have the required means and attain them, and independently reconstructed orbit envelopes give ratios `20891/10411`, `6601/3225`, and `7443345/3445256`.
- Exact verification of all 564 count states for the four small two-group certificates, recovering ratios `27/16`, `21/11`, `99/50`, and `135/67`.
- Exact interval integration of the two nontrivial cubic laws on 2,002 sorted pair/triple mean vectors with coordinates in `{0,1/20,...,1}`. This includes endpoints and half-mean ties and confirms the mixture deficiency inequality on that grid.
- Numerical unrestricted anchor-pattern/count linear programs for dyadic levels 2 through 7, with 20 through 16,512 states. These programs do not assume nested anchors or restrict to the proposed profiles. Their optima agree with the claimed hull values `3/2, 2, 5/2, 11/4, 3, 13/4`, with maximum observed discrepancy below `1.5e-14`.
- Exact generalized-radix profile, mass, mean and objective identities for bases 2 through 9 and levels 2 through 20: 152 cases.
- Numerical quadrature and root checks in 21 harmonic-parameter cases, including large degree scales, and the applicable finite Lambert inequality.

The exact computations establish the stated finite identities/certificates. The finite grid, numerical LPs and quadrature are falsification attempts, not proofs of the universal assertions. The latter assessment rests on the proof reconstruction above.

### Remaining manuscript

For the incidence, feedback, frequency and width results, I checked the ownership count, feedback distribution, odd-cycle matching obstruction, baseline/slab argument, convex-cardinality oracle, marginal completion, and both directions of the two-terminal active/blocking induction. The balance and total-unimodularity statements are not conflated. The positive-box finite perturbation uses extrema controlled on the full box and a fixed ambient balanced law; it does not silently resample that law after deleting coefficients. The physical-box normalization, additive corrections, order of limits, and unequal-box examples are consistent.

I reconstructed the near-one product PARTITION reduction, its variance margin and rational encodings, and checked the separation between exact envelope, membership and ratio claims. I checked the cardinality chord/cover arguments, the full RLT/SDP matrix, and the homogeneous Gram/Vandermonde proof for the preordering functional. All assignment localizers are accounted for. The arbitrary-coordinate-set and graph refinements use the appropriate degree-preserving endpoint interpolation; tensor positivity uses total degree correctly. The relative-block and symmetry-cut arguments respect their stated information restrictions.

For XOR I traced the source functional, signed-character closure and degree `4r`, then checked actual signed-Gram quadratic realizability, clause deletion, graph-identity pullback degree `4rD`, and the monomial support rank count. The order-one hypotheses cover the degree requirements. I checked both order-one upper constructions and their different representation assumptions. The affine comparison is limited to its defined certificate model.

I checked every supporting appendix proof: the point-packing PSD/RLT attainments and symmetry secants; zero-scale and recession cases, extensive perspective costs and rectangularity; the retained-domain P-split counterexample, its local repair, translated-ball projection, coordinate and exact-image comparisons; the correlation-face stability and amplification constants and the distinct LP/SOC/PSD size consequences; the fair-schedule FBBT limit and every-order primitive-update invariant; and the integer midpoint/area/volume comparisons. For the P-split correction I compared both the published formulation and the disputed proof directly, rather than inferring a contradiction from a changed domain convention.

### Reproducibility and PDF

All independent artifacts are under `verification/reviewer02/whole-round01/`. `check.json` and `check.log` record the new checker results. I extracted and executed the printed finite-signing checker, obtaining `[1, 2, 4, 4, 5, 8]`. I also extracted and executed both printed cubic blocks; all assertions passed. Their parsed executable statements match the supplied frozen Python file exactly. Raw concatenation has one additional blank line, which has no mathematical or executable significance; `integrity.json` records both comparisons explicitly.

I copied only the frozen TeX inputs into my own `build/` directory and ran a fresh `latexmk` build successfully. The rebuilt PDF's complete `pdftotext -layout` output is identical to the frozen PDF's. The final log has no unresolved citations/references or overfull boxes. It has three underfull-box messages; I found no corresponding substantive rendering defect.

I viewed contact sheets covering all 111 PDF pages, then inspected pages 16, 22, 23, 84, 86 and 87 at larger resolution, concentrating on the harmonic statement, scalar table, cubic ratios and certificates/code. I found no visible clipping, lost text, or unreadable table/code layout in those inspections. Overview contact sheets do not establish equation-level legibility on every page.

## Remaining limits

This is mathematical review with exact finite checks and selected numerical falsification attempts, not machine verification of the whole paper. The numerical checks use floating-point optimization/quadrature, not certified interval arithmetic. I did not reproduce randomized large-instance generation, run every historical verification program, or enumerate all Boolean vertices of the large examples; the exact orbit argument is what makes their finite certification exhaustive.

I did not independently reprove the external Grothendieck, sharp Khintchine, Camion, matching-polytope, optimization/separation, random-XOR, or extension-complexity theorems. Several were checked in their originals as detailed above; others remain standard cited inputs. Nor did I inspect every original behind the peripheral attribution and comparison bibliography, including all point-packing, scaling and discretization predecessors. Reading all bibliography entries is not an exhaustive priority search. The paper's disclosed source/version and unresolved bibliographic limits remain limits; I found no demonstrated central attribution error.

The scope ledger was checked against the submitted paper, not independently rebuilt from every earlier repository document. None of these limits creates a defect in the correctly bounded claims I reviewed.
