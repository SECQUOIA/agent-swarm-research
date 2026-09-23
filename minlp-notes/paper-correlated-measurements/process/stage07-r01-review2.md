# Final whole-manuscript review 2

**Recommendation:** accept this review gate. I found no major or minor issue requiring correction in the frozen manuscript. This is an independent internal review, not external peer review or a guarantee against future findings.

## Scope

I read the entire manuscript source: the abstract/introduction, foundations, locality, approximation, certification, computations, discussion/conclusion, and all four appendix files. I also read the complete bibliography, macros and main file, repository-paper README, supplement README and source-data README. I checked the assembled PDF text for the principal approximation statements and unresolved reference markers. This was a mathematical/content review rather than a page-by-page typography review.

The deep focus was Section 4 and Appendices B–C, together with their consequences in Corollary 5.6 and the introduction/discussion. I reviewed the other sections for correctness, compatible assumptions, logical dependencies, consistent interpretation of numerical evidence, and sufficient explanation. I did not rerun every historical numerical producer or the complete 46-certificate suite, and I did not independently retrieve all 58 cited works. Those limits do not qualify the specific proof checks reported below.

All 204 files listed in `stage07-r01-freeze.json` retained their expected SHA-256 hashes at the end of the substantive review. I made no manuscript or supplement changes.

## Main proof assessment

1. **Rational weighted-trace FPTAS, Theorem 4.1.** The fixed promise envelopes yield a polynomial calendar graph, including the full-history cap. The bound on `2^L` uses the failed preceding accuracy test and also covers an early cap. The count/cooldown extension correctly retains spacing when the information window is shorter than the exclusion period. Zero signal/contraction, empty schedules, zero objective and conflicting restrictions are treated without invalid divisions. Rational covariance construction and local elimination have polynomial encoding length even with growing packet, latent and parameter dimensions. The common PSD prior and weight preserve the transfer inequality. The individual-channel hardness construction does not contradict this theorem because it changes the selection units.

2. **Exact-range normalization, Lemma 4.4.** Rational rank-one peeling works for singular PSD atoms. Labels retain their owners, including multiple independent labels from the same owner. Forcing the distinct owners supplies all basis terms with their multiplicities and hence the identity lower floor. The rectangular reconstruction uses both the range test and symmetry. The maximum-volume proof only establishes existence; the algorithm enumerates rational labels and computes no irrational maximum-volume basis. Dyadic scaling has polynomial bit length even for very small nonzero pivots. Every target's maximum-volume trial survives the per-atom magnitude filter.

3. **All-target path cover, Theorem 4.3.** Signed floors work for negative off-diagonal entries. Their residuals lie in a common interval even for paths with different lengths, so equal profiles give an entrywise absolute error bounded by the maximum path length times the grid. The forced identity floor turns that into relative PSD order. State merging retains feasibility because the vertex, forced-owner mask and accumulated profile carry all continuation-relevant state in the explicit graph. The separate zero-atom path search is necessary and correct. State counts, output reconstruction and bit bounds are polynomial for fixed information dimension. The output is explicitly an integral feasible object, and the theorem does not claim an oracle feasibility model or a practical small polynomial exponent.

4. **Represented matroids, Theorem 4.6 and Appendix C.** Restriction must preserve the original rank, as stated. Contraction by a basis extension gives the correct optional represented matroid, including dependent forced-owner rejection and the zero residual-rank case. Binet–Cauchy gives positive squared minors, so coefficients identify precisely attainable profiles in characteristic zero. Shifting signed profiles is legitimate because every optional base has the same size. The product-grid Vandermonde interpolation is an exact alternative to the predecessor's moment-curve interpolation; dimensions and coefficient/evaluation bit lengths remain polynomial for fixed profile dimension. Deletion keeps the original row count, so a rank drop produces zero rather than a smaller-base false positive. Monotonicity of deletion feasibility proves that its final witness has exactly the required base size. Zero-information handling and reconstruction respect the original matroid.

5. **Criteria and finite scenarios.** The determinant, eigenvalue, inverse-trace and estimable-contrast consequences use the right monotonicity directions and domains. Singular ranges are preserved; pseudoinverse order is never extended between different kernels. True/local transfer is applied once on each side. Corollary 5.6 uses one common block-diagonal cover, not independently optimized scenarios. The estimated normalizers produce two approximation factors, and its rational determinant-ratio comparisons avoid a hidden logarithm or root oracle. The appendix's tie example really realizes the squared factor and limits only the stated same-set recipe.

6. **Scalar predecessor.** The focused-target construction retains the target in every separator until a singleton terminal bag. Thus all earlier private costs are zero, and the positive terminal cost avoids the identified inverse/private-block-order issue. Observation restrictions remove choices while retaining witness paths in the predecessor's induction. Rational rescaling bounds signal/noise magnitudes; added process variance supplies a polynomial condition bound. The posterior-variance-to-information conversion uses a valid positive singleton lower bound and pads only in the cardinality-only setting. The manuscript explicitly separates this predecessor's spectral-rounding operation model from its own independent rational Turing proof.

## Independent exact tests

I authored `verification/stage07-review2/check.py` without importing manuscript or historical audit helpers. It passed under the available Python/SymPy environment and wrote `results.json` there.

- 69 rational normalization trials and 93 accepted normalized objects, including 60 actual profile collisions.
- Coverage of 18 target objects across a branch-realizable variable-length family and represented-matroid bases.
- Oblique rank-two ranges in three ambient dimensions, signed entries, zero and singular targets, more than one factor belonging to one atom, a `2^-100` scale and a `2^-85` oblique coordinate.
- 35 exact contraction/base equivalences with input matroid rank three, parallel columns, a loop, and one dependent forced-owner rejection.
- 18 exact tensor interpolation runs, agreement with exhaustive squared-minor coefficients, detection of a rank-losing deletion without reducing the row count, and recovery of three actual target-profile bases.

These are distinct finite adversarial checks. They support the proof review but do not substitute for the general mathematical arguments or benchmark the theoretical algorithms.

## Primary literature checks and novelty

I read `literature/AGENTS.md` and inspected the local primary Mahalanabis–Štefankovič text around Definition 18, the message recurrences, Observation 31, spectral rounding and Theorem 43. Its operation-model distinction and the focused recurrence adaptation are accurately described.

I independently inspected the online primary Berstein et al. author report, especially Theorems 1.1 and 1.3, Lemmas 4.3–4.4 and profile recovery. It explicitly supplies the algebraic machinery used here; the manuscript correctly credits that machinery and does not substitute the fixed-number-of-distinct-weights independence-oracle theorem for its changing rounded profiles. Source: [2007 author report](https://optimization-online.org/wp-content/uploads/2007/07/1725.pdf).

I retrieved and read the relevant published Brown–Laddha–Singh theorem and normalization/general-matroid passages from the primary NSF-hosted article. It establishes the broader independence-oracle randomized fixed-dimensional PTAS and the guessed-subset normalization/filtering precedent. The manuscript's narrower deterministic rational-representation claim and polynomial accuracy dependence are correctly distinguished. Source: [published article](https://par.nsf.gov/servlets/purl/10548928). The web reader timed out for this PDF, but a direct open download succeeded; temporary files remained outside the manuscript.

I read the primary Bansal–Xu v1 theorem, partition definition, inverse construction, gap lemma and bit-length argument. The new discussion sentence uses a valid weaker consequence: polynomial-factor approximation in growing information dimension is excluded for A/E partition design unless P=NP, even with all feasible matrices invertible. It does not assert weighted-trace hardness or contradict the fixed-dimensional cover. Source: [arXiv:2608.05468v1](https://arxiv.org/html/2608.05468v1).

The qualified novelty language concerns a precise combination of all-target quantification, two-sided PSD order, exact singular ranges, feasible integral witnesses, deterministic accuracy dependence and explicit rational representations. No priority claim is made for normalization, profile interpolation, objective independence or PSD pruning separately. I found no unsupported novelty escalation in the abstract or conclusion.

## Whole-paper integration

The statistical target remains the selected covariance throughout. The larger algorithmic claims clearly require more structured feasible families than the arbitrary finite-family certificate statements. The partial-observation and complete-channel boundaries agree with the experiments. PSD priors in the approximation results are separated from SPD priors in practical logdet/separator certificates. The computations distinguish actual feasible schedules, feasible mixtures, numerical proposals and exact upper witnesses, including negative comparisons and failed or capped numerical searches. The practical experiments explicitly do not claim to implement the high-degree spectral-set algorithms. The discussion correctly restricts the known-covariance, local-sensitivity and finite-scenario conclusions.

I found no contradiction between the technical claims, the integrated contribution summary, the numerical interpretation or the portable-package documentation that requires a correction.
