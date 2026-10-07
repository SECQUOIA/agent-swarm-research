# Independent editorial review of integrated mathematical draft R1

## Decision and scope

The frozen R1 manuscript resolves the serious editorial findings P1–P5 from the original Opus review. Its main claims now agree with the stated finite perturbation laws, exact output formats, parameter dependence, and limitations. I found no additional major editorial or substantive presentation blocker in the mathematical draft. Two small statement corrections are required below. The root agent reports that both have been repaired in the live sources; that report does not change this review of the immutable snapshot, and the repairs still need a focused check in the next snapshot.

This is a qualified editorial pass of the mathematical content, not approval for journal submission. The bibliography and final primary-source contract audit remain a publication blocker. The independent mathematical specialists' findings also remain outside this editorial verdict. I have not independently certified every appendix calculation or assessed the typeset PDF's layout.

The reviewed sources are exclusively the 20 TeX files in `evidence/snapshots/integrated-mathematical-draft-r1`, captured at `2026-10-06T03:49:31.635993+00:00`, and the supplied `evidence/literature-preliminary.md` for preliminary primary-source comparisons. The manifest labels this snapshot “Frozen complete mathematical revision; bibliography pending Luna final audit.” I independently checked the 20 file hashes and line counts against that manifest; all matched. The manifest SHA-256 is `c439935acba1b1adeb5d883e3718b1416f71ca45839ab672f5545060343d92cf`.

All source locators below refer to that frozen directory, not the changing live sources. I read all eleven main sections, `main.tex`, and `macros.tex`. I read the selected appendix proof chains described under checks below. I also read the independent review brief, the original Opus interim editorial review, the root editorial disposition, both root integration scope records, and all four Sol final author reports. Their assertions were checked against the frozen text rather than accepted as evidence of a repair.

## Remaining publication blocker

**B1 — Final bibliography and cited theorem contracts are pending.** The frozen manifest contains no `references.bib`, while `main.tex:43` requests `\bibliography{references}`. The supplied preliminary literature audit explicitly remains preliminary. This review therefore cannot approve author identities, publication versions, final citation keys, or every classical theorem contract.

The final audit needs to close the source contracts actually used by the manuscript, including the opening one-negative-eigenvalue hardness attribution (`sections/01-introduction.tex:7–8`), the finite-noise appendix's real-algebraic solver statement (`appendices/A-finite-noise.tex:331–350`), the refined Bézout and convex optimization primitives (`appendices/C-sparse.tex:27–59`), the quadratic and mixed-integer primitives (`sections/04-quadratic.tex:60–75`), the precise tube estimate used for recourse (`appendices/E-recourse.tex:90–97`), and the integer optimization citation (`sections/08-integer.tex:242–264`). It also needs to finalize the companion-paper identities and supported comparison claims. These are source-verification dependencies, not findings that those mathematical statements are false.

Concrete completion: integrate the Luna audit and final bibliography, resolve any contract mismatch in the corresponding theorem or argument, and check the resulting literature-integrated snapshot. No fresh literature search was performed in this review.

## Required minor corrections in frozen R1

**R1 — Qualify the sentence about output size.** At `sections/10-discussion.tex:83–93`, line 86 says, “Fallback outputs and global proof records have only expected size bounds.” Read literally, this is too broad. The generic fallback has an explicit, potentially large bound on each draw (`sections/02-model.tex:370–379` and the counting closure at `sections/03-counting.tex:539–570`). Selected native and flow/TU representations also have parameter-dependent size bounds on every draw (`sections/08-integer.tex:175–193,370–383,460–473`). The meaningful distinction is between those per-draw bounds and the smaller expected-length/work guarantees.

Repair the sentence by saying that generic semialgebraic fallback outputs and global proof records can be large on individual draws, while their expected lengths obey the stated work bounds; retain the stated per-draw size guarantees for the selected native, flow/TU, and small-core algebraic representations. Do not imply that every exact output has a short per-draw representation. The surrounding distinction between a finite descriptor and an improvement in optimization time is accurate and should remain.

Disposition: the root agent reports this correction in the live sources. Verification is pending against the next immutable snapshot.

**R2 — Define the surviving event before assigning its probability.** At `sections/08-integer.tex:614–620`, the prose first describes noise *outside* the closed derivative interval, which pins the coordinate. It then calls “These” the bad events with probabilities `q_i`, although `q_i` was defined at lines 578–583 as the mass *inside* that interval. The subsequent component argument uses the correct inside-interval survival probability, as does the appendix calculation (`appendices/F-integer.tex:987–998`), but the antecedent in the main explanation can invert the reader's interpretation of the Bernoulli model.

Concrete repair: after the pinning sentence, state explicitly that the event `\(\gamma_i\in[-\overline\partial_i,-\underline\partial_i]\)` leaves coordinate `i` unpinned, is called bad, depends on one coefficient, and has probability `q_i`. Then state independence. The similar shorthand at `appendices/F-integer.tex:972–977` can use the same explicit definition for consistency. No change to the theorem or its component calculation is indicated by this editorial finding.

Disposition: the root agent reports the explicit inside-closed-interval definition in the live sources. Verification is pending against the next immutable snapshot.

## Verification of the earlier serious findings

| Earlier finding | Verified frozen text | Assessment |
| --- | --- | --- |
| P1: originality relative to the exact-arithmetic, foundation, and quartic companions | `01-introduction:447–472`; `07-recourse:507–526,556–572,732–738`; `09-boundaries:584–600,735–753`; `G-boundaries:179–182` | Resolved in the prose, subject to final source verification. The common law selected before precision queries and a per-draw work factor controlling all queries are expressly credited to the exact-arithmetic companion. A finite descriptor and global proof record are identified as representation distinctions, not independent runtime advances. All three quartic obstruction parts are credited. The cubic/core Schur-complement route is distinguished from the companion route by its actual domain, degree, and modulus assumptions. |
| P2: graded-grid comparison and overbroad negative claims about width | `01-introduction:474–499`; `05-sparse:694–746`; `10-discussion:105–118` | Resolved. The comparison identifies weighted growth `\(\bar\kappa\)`, Euclidean growth `\(\kappa\)`, the companion's parameter function and fixed input exponent, and the graded-grid count. The lower bound is restricted to its product model. The truncated-moment statement says why a linear small-growth tail does not justify the proposed inverse-growth integration; it does not claim that all width-FPT algorithms are impossible. |
| P3: bounded-box perturbation obstruction presented too broadly | `01-introduction:501–512`; `09-boundaries`, including the bounded-pair/gate constructions | Resolved. The binary-indicator result names the independent uniform grid, its minimum number of labels, its bounded box, and the numerical magnitudes held fixed in the expected-work claim. The wider ambient model is distinguished. The randomized implication is stated as the relevant containment, not an unconditional impossibility theorem. |
| P4: structural FPT claimed without numerical parameters | `00-abstract:6–17`; `01-introduction:56–65,84–85,100–101,130–199,286–294`; `02-model:385–406` | Resolved. The abstract, main table, and model state joint dependence on structure and numerical ratios. Polynomially growing ratios can yield `\(I^{O(k)}\)`, and this is not called FPT in `k` alone. |
| P5: unsupported practical applications and undisclosed strong-noise scales | `01-introduction:117–128`; `07-recourse:3–18,136–145`; `08-integer:124–126,641–650`; `10-discussion:11–17,39–48,95–101` | Resolved. Uses are conditional on the actual model. Recourse feasibility must be fixed before core noise; the coupled-feasibility counterexample makes the restriction concrete. The strong-field sufficient scale explicitly contains `\(c_d=2^{10000D}\)` for the nonquadratic continuous case and numerical integer label counts. The quadratic improvement is distinguished. Practical performance is left unsettled, rather than implied by theory or declared impossible. |

The supplied primary-source comparison evidence supports the narrowed comparison language editorially. Final bibliography integration must preserve these qualifications; in particular, it must not recast a precision-independent finite law as new or present an algebraic descriptor interface by itself as a runtime improvement.

## Coherence, meanings, and proof presentation

The front matter now gives a reader a usable account of what the paper solves. The main table (`sections/01-introduction.tex:130–199`) covers the principal low-rank, sparse, recourse, and integer routes with their perturbation laws, work scales, and output distinctions. The surrounding text explains which assumptions are supplied and what is counted in input size. The table is a summary of the principal results rather than a replacement for the more detailed domain-specific theorems; I found no missing principal route that made its account materially misleading.

The distinction between solving the perturbed objective and approximating the original objective is explicit. The calibration result uses the actual noise coordinates and their widths (`sections/02-model.tex:469–514`), and the strong-field discussion discloses the correspondingly large original-objective regret. The scientific uses are concrete but conditional: a specified uncertainty law, suitable separability or interaction structure, fixed recourse feasibility, and supplied certificates or numerical bounds. There is no unsupported claim of observed computational performance.

The finite-law contract is clear. The model permits countably supported rational laws where appropriate, while a worst-case sample bit bound forces finite support (`sections/02-model.tex:142–144`; `sections/03-counting.tex:274–279`). Samplers are selected from the base instance, rather than changed for each requested precision. Aligned noise can be correlated in original coordinates; the text does not call it independent ambient noise (`sections/02-model.tex:118–130`; `sections/10-discussion.tex:5–8`). Uniform ambient low-rank noise uses a conditional volume argument rather than an unjustified product count. Special chart and order arguments are separated from the direct product mechanism (`sections/01-introduction.tex:232–280`).

The exactness claims distinguish an optimizer, an algebraic representation, an implicit patch, rational evaluation, and global certification. A descriptor alone is not treated as a global optimality certificate (`sections/01-introduction.tex:309–316`; `sections/02-model.tex:342–349`; `sections/05-sparse.tex:133–136`). Quadratic rational outputs are restricted to the appropriate rational box/polyhedral domains; charted variants can be irrational. Shared-root component representations and symbolic sums do not silently promise exact threshold comparisons of unrelated algebraic numbers (`sections/02-model.tex:328–379`; `sections/08-integer.tex:645–648`). The comparison with Cauchy names is explicit and avoids a canonical-selection claim for the ordinary descriptor output. R1 above is the remaining broad output-size sentence.

The width-conditioned recourse interface is presented as a sufficient oracle contract, not an implemented general oracle or a necessary condition for every prospective algorithm (`sections/05-sparse.tex:583–692`; `sections/10-discussion.tex:105–118`). Its feasible witnesses and noise-dependent evaluation-error envelopes matter to the count and are not omitted. The main recourse chapter separates fixed feasible fibers, certified moduli, and cubic residual structure from qualitative convexity or moving feasibility. The quartic section makes both the bounded-box gate construction and its decision-model consequences visible.

The scientific proof chain is internal apart from named classical tools. The inspected appendices contain actual finite tails, same-draw fallback and refinement arguments, joint sampler schedules, patch evaluation, constrained-domain closure arguments, recourse stopping and work calculations, component solver bounds, and boundary reductions. They are not merely promises to consult source notes or author reports. The paper's length supports these contracts; I do not recommend deleting their mathematical qualifications or compressing the proofs to produce a shorter draft.

## Optional prose improvement

At `sections/01-introduction.tex:243–245`, “Under uniform noise on all coefficients of the low-rank route they are not” has a distant antecedent. Replace it with a direct statement that the factor coefficients and residual noise are generally dependent under uniform ambient noise in that route. The following conditional-volume explanation is sound. This is an optional readability edit, not a mathematical blocker.

## Checks actually performed

- Read all eleven numbered main sections, `main.tex`, and `macros.tex` in the immutable snapshot, using numbered source text.
- Inspected appendix structure and read the main finite growth, shared-root, and fallback chain in A (`228–675`); the joint schedule and main proof in B (`639–757`); the algebraic/convex patch and fallback tools in C (`1–223`); the implicit graph, simplex, and order closure/evaluation chains in D (`268–332,495–699,1026–1080`); the stated recourse tools and core-only schedule/probability/stopping/work chain in E (`1–118,700–819`); the explicit solver constant, arbitrary core-face argument, and strong-field component/evaluation proof in F (`330–373,806–865,962–1017`); and the attribution, sign, amplification, bounded encoding, gate, and decision-model portions of G (`177–262,343–439`).
- Read the required editorial, root-integration, and author-report evidence, then verified their claimed prose repairs in the actual frozen sources.
- Read the supplied preliminary literature comparison evidence. Did not browse, discover additional sources, or perform independent literature research.
- Used read-only `cat`, `nl`/`sed`, and `rg` source inspection, plus a local SHA-256/line-count fingerprint of the 20 frozen TeX files. These were evidence checks, not compilation or mathematical testing.
- Did not run TeX compilation, optimization experiments, project-wide checks, or inspect CI. Did not visually review the 175-page scratch PDF. No manuscript source was changed by this review.

## Frozen source fingerprints

Each file below matched its manifest SHA-256 and line count when reviewed.

| File | Lines | SHA-256 |
| --- | ---: | --- |
| `main.tex` | 44 | `e22e0015a0b032eedbd618b75c6be0fb8c120f6789e12acb0b9cafc5420b9000` |
| `macros.tex` | 32 | `ac79fc04907f0edc4f964033bbcfa9c1d4d5b07b36428ad0466c72a34d6c8abd` |
| `sections/00-abstract.tex` | 27 | `2b1dd7bfef41dd05d68d527afcba9c1526ce5b4ca243d96d926f63b2236bfbc2` |
| `sections/01-introduction.tex` | 524 | `c3b27472e13d0c6a94d1cb6693d264d6ac0f6137c7e64d039bc613eb3d35ba56` |
| `sections/02-model.tex` | 559 | `0a9267cd7a893497d212e5ccb0fbb6433b6428c4784793dd9fc79ec4f4e38a63` |
| `sections/03-counting.tex` | 754 | `9818728f37864c878ab2e7d0bb1690bb79e8d53f3a338e2f316e31787692b049` |
| `sections/04-quadratic.tex` | 909 | `020d70a1f2d3380776aa908dc25a5d9351c126674c0571a74e73a7dab867edd5` |
| `sections/05-sparse.tex` | 1145 | `df3ef7c7f7c08d415044d9d93e3f9daa9b8a5d6c301954b950c3130c6718f047` |
| `sections/06-constraints.tex` | 818 | `9467eb72e20f355b3afb70d844bfedcf0a7fe52ba8f53d2483327162ad9db898` |
| `sections/07-recourse.tex` | 740 | `6dbb5f51199e261d613afbe67a88b4bd9f8f43dfc3c2fd6bb34a22243f659c6b` |
| `sections/08-integer.tex` | 775 | `27809e4472aa7e53c36e8a211bf91d348f5e25c651d74f75936e9d5df7e3f573` |
| `sections/09-boundaries.tex` | 824 | `1acb7217806f6e53e27a653e9ca36df3adfa3d37cc25a428b45c4770cb8e7bf8` |
| `sections/10-discussion.tex` | 144 | `d1e176dc2598a40d80d9bc6e13773cd634a713cd6f8e236d5b6e992ebfc49c56` |
| `appendices/A-finite-noise.tex` | 822 | `4ff3fe30e76466dcc744389e88deaa9759fc19a2709c1104cba89612379c39cd` |
| `appendices/B-quadratic.tex` | 888 | `c15f3a6f76d6a65ab4b6a4f2e861597d0b1c21f35baa41b1b4f670ad63308d31` |
| `appendices/C-sparse.tex` | 278 | `a93e0493bd253e24e72b5fa1d903f360f8422a84222ec04d80eed069ca9b2974` |
| `appendices/D-constraints.tex` | 1080 | `c0b90de5054e469a278c2d09f560ce39a746c5b1025c79ecf4aee75ca0f4e66b` |
| `appendices/E-recourse.tex` | 894 | `e3bba43cbcfa9cfd373661b350711c3f890ebb73a9994dc6dfc13fae49676e1f` |
| `appendices/F-integer.tex` | 1127 | `c561d9401b3cc15e9072ab7bffe843f6205a894886fba219a8ee02150a472ef0` |
| `appendices/G-boundaries.tex` | 481 | `163333352717c3b090f62924f8a8b90eea63cf7c4fc50bf1da0dafd4556f1553` |

The next editorial readiness check should be focused on the two live repairs, the final bibliography and companion/source-contract integration, and any changes required by the independent mathematical reviews. This report does not approve those unreviewed changes in advance.
