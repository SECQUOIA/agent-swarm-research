# Stage 6b independent review R2

## Verdict and scope

I found no major defect in the frozen Stage 6b manuscript or extracted delivery. I recommend correcting the two minor issues below before the Stage 6b gate. This is an independent review recommendation, not a declaration of stage acceptance or a substitute for the separate full-manuscript review cycle.

I read the complete main narrative, abstract, introduction, model and output definitions, principal statements, both main tables, examples, figures, conclusion, and bibliography. I compared the principal result groups with their included technical statements and inspected the materially relevant arguments: passive existence and block aggregation; adjoint saturation and the two perturbations; fixed-dimensional box elimination and recovery; cactus radical reductions; dense-law and fractional-law transfer; finite secants and envelope construction; the weighted face and local-candidate constructions; scalar interpolation and the exceptional-rank extension; cycle-root recovery and capacities; convex design, correlation hardness and dissipation duality; and rational energy, Bregman, support and curvature certificates. This review prioritizes the new main/appendix interface and literature claims. It is not a formal verification of every algebraic manipulation in the inherited 188-page technical/reference portion.

I did not read author reports, lead notes, adjudications, historical reviewer reports, or peer reports. I made no manuscript, code, bibliography, Paper B, or literature edits. This report is my only checkout edit. Downloads, extraction, builds, replays and regenerated packaging used `/tmp/s6b-r2-grzYyZ`.

## Required minor findings

### R2-1: The main-text weighted face bound drops the positive-rank convention and reuses the total-rank symbol

**Locations:** `complexity/sections/00-introduction.tex:71–73`; `complexity/narrative/04-weighted.tex:79–83`. Compare `complexity/sections/07-weighted-cactus.tex:68–83`, especially its explicit `r >= 1` hypothesis, and `complexity/narrative/01-model.tex`, which defines `r` as total cycle rank.

The introduction says the face theorem leaves `O(rp)` free coordinates when maximum block rank is at most `r`, without requiring `r >= 1`. The later main-text proof explanation repeats `O(rp)` and `n^{O(rp)}` without introducing a local block-rank-bound convention. The technical theorem deliberately assumes a positive rank bound; trees are treated using the bound one. This hypothesis should survive the summary. Reusing `r`, already defined as total rank, also makes the intended parameter unclear in the many-block discussion.

This is substantive at rank zero, though it does not threaten the correctly stated appendix theorem. Consider the path `0 -> 1 -> 2`, both resistances one, `c=(-1,2,-1)`, and the balanced nomination box

```
b_0 in [0,1], b_1=-1, b_2 in [0,1], sum b=0.
```

Write `b=(t,-1,1-t)`. Its flows are `(t,t-1)` and, grounding vertex 2, its objective is

```
W(t) = -t^2 - (1-t)^2 = -2(t-1/2)^2 - 1/2.
```

The unique maximizer has both variable nominations strictly inside their intervals. All three objective coefficients are nonzero; both objective cut flows are nonzero, so neither pruning nor zero-objective block contraction removes this example. There is no all-endpoint nomination face containing the optimum, whereas a literal `O(rp)` bound at `r=0` leaves no free coordinates.

**Repair:** use a distinct bound `r_0 >= 1` in both main-text passages and write `O(r_0 p)` and `n^{O(r_0 p)}`; alternatively define the parameter as `max{1,r_max}`. State that reductions precede the face count, as the current proof explanation already does. No technical proof or algorithm needs changing.

### R2-2: One final coverage row still labels completed uses as planned

**Location:** `coverage.md:47`, the row for `results/fixed-core-block-polyhedral-optimization.md`.

The row assigns A03, A04 and A06, but its note says “other assignments remain planned.” This conflicts with the inventory's claim to describe the complete included manuscript. These uses are actually present: A03 proves `lem:a-blk-boxlp`; A04 extends it in `lem:a-law-dense` and uses it in `thm:a-law-polynomial`; A06 uses it in the proof of `thm:a-weight-global`. I found no missing technical result behind this stale status.

**Repair:** replace the planned-status sentence with these concrete completed uses, or narrow the row's destinations to the intended provenance allocation. This is a coverage-document correction, not a mathematical coverage gap.

## Principal results and main/appendix agreement

| Group | Assessment |
| --- | --- |
| Foundations and block-rank pressure/arc algorithms | The coercivity proof covers bounded strictly increasing laws without an onto assumption. Aggregation uses the unfiltered balanced box and gives rational disaggregation. The adjoint proof localizes nominations rather than all uncertain parameters. The coefficient-box support construction keeps the number of real variables fixed and recovers leaves through polynomially many exposed zonotope vertices. The main theorem correctly distinguishes additive pressure sums from exact local algebraic arc values, and includes growing dense degree without claiming sparse-exponent tractability. |
| Cactus arithmetic and fractional laws | Both single-source/sink SRS reductions preserve weak equality and positive integer resistances after scaling. The full arbitrary-box exact cactus problem is not claimed equivalent to SRS. The fractional construction retains a fixed exponent family, positive rational fractions, uniform state error and original-law rounding. Its single-cycle exact arc lower bound is not presented as NP-hardness. |
| Hulls, graph classes and discrete boundaries | The main hull table matches the technical hierarchy: trees / cacti / cacti / series-parallel for weighted potentials / potential differences / linear flows / individual arcs. Independent fixed nominations and unfiltered scenarios are available at the table. The finite-secant proof handles zero flow. Quantitative positive-resistance restoration supports the universal converses; the whole-region statements are kept distinct from scalar endpoint equality. Table 2's membership statements stay within the fixed-rank or specifically proved families. Flow-gap scaling uses nominations, and finite realization remains an existential question. |
| Weighted objectives | The formal main theorem retains fixed nomination dimension versus fixed objective support, independent symmetric versus directional coefficient boxes, fixed global rank versus maximum block rank, and the summed exceptional rank `kappa`. The general face theorem is proved, not left open. The cactus compiler includes ties, flat candidates and zero-flow strata. The scalar compiler isolates real parts of complex exceptional parameters, uses a Lipschitz bound on short neighborhoods, and constructs rational interpolants in the original coordinate. Its degree, node precision and coefficient bounds are accounted for. The hybrid theorem keeps all noncactus circulations in one fixed core. The several-parameter unrestricted-higher-block sum is accurately left outside these guarantees. R2-1 concerns the informal face summary only. |
| Design, correlations and energy | The root theorem's uniform vertex height/separation bound justifies exact LP-vertex recovery without enumerating vertices. Capacity clipping and rational realization distinguish rational parameters from algebraic roots. Convex minimization treats irrational singletons with stored endpoint profiles. Few-measurement maximization uses rational directions rather than assuming all zonotope coordinates rational. The Max-Cut constructions justify the stated strong hardness under bounded network data; global-correlation membership is restricted to their fixed-field families. Maximum dissipation uses the correct factor three, concavity and a two-cone dual lift, with a quantitative relative-interior argument for rational feasible output. |
| Rational feasibility and certificates | The rank-two ordinary-capacity example really forces `7-4 sqrt(2)` as a resistance. Strict-margin recovery remains conditional and is not advertised as a search algorithm. The main certificate theorem matches the directional cubic conjugate, exact conservation, reverse Bregman identity, zero-curvature compatibility and rational KKT construction. Its sharpness is only over the stated conserved quadratic error set. Endpoint optimality certifies original parameters, not a rational exact physical state. Implementation and saved-witness claims are explicitly narrower than the abstract algorithms. |

The new main narrative gives a coherent reading order and enough mechanisms to understand why the theorems differ. It is a substantial theoretical contribution if the scoped results withstand the full manuscript cycle: unbounded total network size and cycle count are permitted in settings where local algebra alone would not control global arithmetic. Its relevance is chiefly complexity and verifiable computation; the paper appropriately does not imply that its loose XP bounds are practical implementations. The included appendix is long but organized by dependency, with a contents map and direct theorem links. I found no reliance on an unwritten companion, no missing principal proof, and no unsupported implementation of the general compilers.

## Primary literature and novelty assessment

I inspected original PDFs, not the managed `paper.md` summaries, for the comparisons below. Local originals were converted with `pdftotext -layout` into the isolated directory. Online originals were also retrieved where useful. The claims are narrowly enough drawn that a bounded search need not prove a negative priority statement.

| Original source and locator | What I checked and its implication |
| --- | --- |
| Pfetsch, Schmidt, Skutella and Thürauf, *Potential-Based Flows—An Overview*, local original, pp. 9–10; bibliography URL | The nonlinear cactus MPD question is explicitly open in that account. The manuscript resolves the additive version and an exact subclass; it does not claim the full exact question solved. |
| Labbé, Plein, Schmidt and Thürauf, [cycle booking manuscript](https://optimization-online.org/wp-content/uploads/2019/11/7472.pdf), Section 6, Assumption 6.1, Theorems 6.4–6.5, Corollary 6.6 | Rational booking, law and potential-bound data are explicit. The constant-dimensional reduction and Turing-time result precede this manuscript. The main text gives the four correct authors and credits that precedent. |
| Groß, Pfetsch, Schewe, Schmidt and Skutella, local original of *Algorithmic Results for Potential-Based Flows*, Section 2.1, Lemma 4.2 and Theorem 4.3 | Homogeneous series/parallel reductions and discussion of Turing root approximation are present. The manuscript does not dismiss this as merely real arithmetic; its new exact SRS comparison distinction is properly separated. |
| Thürauf, local April 6, 2022 manuscript, Section 4, Figure 2, Lemmas 4.3, 4.17 and 4.20 | The supplied nomination-hardness construction is expressly credited. Inspection supports its use as an unbounded-rank boundary, not a contradiction to fixed maximum block rank. |
| Misra, Vuffray and Chertkov, [arXiv:1504.02370](https://arxiv.org/abs/1504.02370), Section IV-A, Lemma 1, equations (19)–(21) | Potentials as conjugate gradients and the inverse grounded weighted Laplacian are antecedents. The manuscript correctly treats the adjoint mechanism as classical and adds smoothing/localization arguments. |
| P. Chauffoureaux and M. Hasler, original ISCAS 1990 PDF, pp. 395–398, Theorem 3 and conclusion; [DOI](https://doi.org/10.1109/ISCAS.1990.112055) | The original title page confirms both authors, despite the managed directory beginning with Hasler. The principal theorem concerns source-to-resistor transfer monotonicity under a linear structural criterion; parameter extensions are discussed. The manuscript's qualified comparison is consistent, and it does not claim this source supplies its full uncertainty algorithm. |
| Changlu Wang and Martin Hasler, [undated original report](https://infoscience.epfl.ch/bitstreams/d2fb4e43-bb7e-42b7-977c-39560d9e7d46/download), Theorems 1, 4 and 5, especially p. 13 | These are scalar transfer-characteristic convexity criteria as a source changes, with ladder applications. They are not full-vector attainable-region convexity under resistance uncertainty. The manuscript correctly uses the original author order and avoids treating the directory's 1997 label as a verified date. |
| Gotzes, Heitsch, Henrion and Schultz, [WIAS original](https://www.wias-berlin.de/people/heitsch/GHHS16_Preprint.pdf), submitted September 24, 2015, Theorem 6 and equation (44), p. 18; concluding p. 24 | The quadratic-radical ray formula and discussion of node-disjoint cycles with attached trees are present. The paper credits these local formulas while stating stronger common-coordinate and accuracy-bit output requirements. The web reader failed on this URL, but direct download succeeded and I inspected that PDF. |
| Vigneron, original author manuscript dated October 21, 2011, Section 2.3, Theorem 6 and Section 3.2; [author PDF](https://antoinevigneron.github.io/manuscripts/rational.pdf) | The source works with bounded nonnegative constant-description functions and a multiplicative approximation scheme. Its bit-model extension remains polynomial in `1/epsilon`. The manuscript accurately distinguishes this from its accuracy-bit summation contract. |
| Borcea, Bøgvad and Shapiro, [arXiv:math/0409353v2](https://arxiv.org/pdf/math/0409353v2), Theorems 2–3 | The exponential convergence statement is away from an exceptional locus and concerns a dominant branch. It does not itself assert the manuscript's uniform branch-selection and coefficient-bit interface across exceptional parameters. |
| Yomdin, [arXiv:1406.1719v2](https://arxiv.org/pdf/1406.1719v2), Definitions 5.1–5.2 and Theorem 5.6 | The logarithm-cubed bound is for degree-based complexity of parametric approximations of planar semialgebraic sets. The paper's distinction from a rational bit algorithm in a prescribed original function coordinate is accurate. |
| Binyamini and Novikov, [original preprint](https://arxiv.org/pdf/1802.07577), Section 1.1.1, Theorem 1 | The polynomial chart-count and semialgebraic-complexity bounds are present. They are not, in the stated theorem, a common-original-coordinate rational summation algorithm. The manuscript does not assert that such a development is impossible. |
| Klimm, Pfetsch, Skutella and Strubberg, local [arXiv:2604.26882v1](https://arxiv.org/abs/2604.26882), Corollary 4 and Theorem 11 | Correct original authors; no-fixed-cost convexity and the bounded-conductance, positive-variable-cost series-parallel FPTAS have the stated scope. Installed topology/conductance investment is not equated with resistance scenarios or globally linear resistance correlations. |
| Dadush, [original thesis](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf), Theorem 2.5.9, p. 48 | The theorem actually returns a rational point in the centered convex body with an additive objective guarantee. This supports the exact-feasibility interface used after the manuscript establishes a relative-interior ball. Direct PDF download succeeded after the web reader timed out. |

The manuscript also explicitly credits classical primitive energy, electrical confluence, Fenchel/Slater duality, Bregman divergence, convex optimization and zonotope methods. I did not independently reopen every one of those bibliography items. In particular I did not obtain the full Hasler–Wang 1993 tolerance paper, and I do not use its inaccessible contents to support priority. The manuscript's own caveat is appropriate. The online search was a bounded comparison, not proof of firstness. I found no material novelty overclaim in the frozen text.

## Coverage, preservation and reproduction

Start checks matched the supplied freeze:

```
process/completion-s6b-manifest.json
a530e917bd4fee2ab9fd90af8f7c29ecddcbb64936abffab32b559f61c2dafb0
dist/potential-flow-paper-a.tar.gz
23119436776b23c7e17d97293ee5376806d772bda5009e8dd009861b06ef30a2
```

I recomputed all 23 source-input hashes and all 43 stage-file hashes: no mismatch. All eleven technical sections equal their recorded preservation hashes. This verifies preservation against the freeze's recorded baseline; I did not inspect historical acceptance reports. Every one of the archive's 63 manifested payload files matches both its internal manifest and the freeze's payload map. Including `manifest.json`, the archive has 64 files. The packaged PDF is the frozen PDF.

Read-only corpus checks found matching main/worktree hashes for all 43 promoted result files, 173 potential-flow notes and 73 Python modules. I also compared all 308 linked inventory sources against the main checkout: no missing or differing source. The current coverage checker passes with 308 files and **13** planned section files. Its update changes the section target map to Paper A; the corpus patterns and direct-dependency inventory remain visible. The detailed completion map's reference to the original checker's 18 sections is historical, not the current output. R2-2 is the remaining stale row status, not missing coverage. `git diff --name-only HEAD` reports no tracked changes under Paper B or managed literature.

Actual commands, all run from the extracted top-level directory unless stated otherwise:

```
tar -xzf <frozen archive> -C /tmp/s6b-r2-grzYyZ
/home/sgusev/miniconda3/envs/minlp-notes/bin/python \
  paper-potential-flow/reproducibility/build_paper.py
/home/sgusev/miniconda3/envs/minlp-notes/bin/python -S \
  paper-potential-flow/reproducibility/reproduce.py \
  --output /tmp/s6b-r2-grzYyZ/exact-replay.json
/home/sgusev/miniconda3/envs/minlp-notes/bin/python \
  paper-potential-flow/reproducibility/reproduce.py --numerical \
  --output /tmp/s6b-r2-grzYyZ/numerical-replay.json
/home/sgusev/miniconda3/envs/minlp-notes/bin/python \
  paper-potential-flow/reproducibility/package.py \
  --output /tmp/s6b-r2-grzYyZ/repacked
```

The A-only build passed: 216 PDF pages, 28 main-text pages, zero errors, undefined references, undefined citations, duplicate labels and overfull boxes. Exact replay passed **18/18** commands; optional scientific replay passed **28/28**. The latter used NumPy 2.5.2, SciPy 1.18.1, SymPy 1.14.0, NetworkX 3.6.1, CVXPY 1.9.2 and Clarabel 0.11.1. The replay scripts copy inputs before running producers, and the exact paths explicitly include `-S -O`. Repackaging from extraction succeeded and produced 64 files without a parent-repository dependency.

I inspected rendered pages 6, 9, 11, 14, 16 and 207, including both topology/localization diagrams, the long computational-boundary table and representative mathematical prose/proofs. The inspected elements fit and remain readable; no clipping or overlapping content appeared. The long table occupies much of page 16, but is usable. This is representative visual inspection, not visual examination of every page.

The archive contains only Paper A sources/PDF, selected code/data, build/replay scripts and evidence. Executable names containing `review` are diagnostic programs, not agent reports. I found no Paper B, managed PDF literature, raw INP dataset, internal review prose or temporary build files. Instructions distinguish standard-library exact checks from the optional numerical environment and accurately limit the producers' guarantees. No invented authors, funding, license or external acceptance claim appears in the manuscript or archive.

End integrity checks repeated the manifest, archive, source-input and stage-file hashes with no mismatch. The extracted payload hashes also remain unchanged after the build/replays/repackaging; generated build output and regenerated deliverables lie outside the frozen payload.
