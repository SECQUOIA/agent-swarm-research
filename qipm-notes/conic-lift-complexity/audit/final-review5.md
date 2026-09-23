# Independent whole-manuscript review 5

Reviewed on 2026-09-20. Recommendation: accept the mathematical draft after the one minor correction below. I found no major issue in the manuscript I reviewed. This is an independent review, not a guarantee against errors or a certification of priority.

## Scope and independence

I personally read `main.tex`, `macros.tex`, all 35 files in `sections/`, and the complete bibliography. This includes every stated result and proof, the introduction and synthesis, all six parts, and all four appendices. I did not delegate any review work or read another reviewer's report, an author/fixer report, or the workflow conclusions. I consulted the permitted source map for routing; its historical review-status statements were not evidence for my conclusions.

The section-file coverage was:

- `00-introduction`, `01-foundations`, `02-certificate-rank`, `03-products`;
- `04-global-regularity`, `05-support-orbits`, `06-restricted-barriers`, `07-concrete-barriers`;
- `08a-general-topology`, `08b-product-orbits`, `08c-restricted-kernels`, `08d-full-fibers`, `08e-topology-refinements`;
- all five files `09a` through `09e`;
- all seven files `10a` through `10g`;
- all four files `11a` through `11d`;
- all five files `12a` through `12e`, and `13-synthesis`.

I followed proofs across sections and checked model assumptions and quantifier changes. I also consulted primary online literature, the local Gouveia–Parrilo–Thomas and Güler–Tunçel literature records, actual workbench sources for the certificate-rank frontier, off-center PSD quotient, and dynamic scale maintenance, and the companion manuscript's norm-tree development. These external/source checks were targeted, not a second full review of every cited publication or all 201 workbench notes.

## Findings

### Minor 1: state that the tree dimension cap is an integer

**Location:** `sections/07-concrete-barriers.tex`, Corollary `cor:tree-cap-parameter`, immediately after its heading (currently line 113).

**Problem:** “Fix a Lorentz dimension cap $d\geq3$” permits a real upper bound on integer cone dimensions, whereas the formula and its proof use $A=d-2$ as an integer arity increment. As literally stated, the result is false for noninteger caps.

For example, take $N=4$ and $d=3.5$. The displayed definitions give $A=1.5$, $E=3$, $L_0=2$, and $\chi=0$, hence the claimed minimum is $3$. However, every admissible cone has integer dimension at most $3$, so all internal nodes are binary. A four-leaf tree has three internal nodes. The balanced tree has an all-internal root and parameter $2(3)-2=4$; a tree with a leaf at the root has parameter $5$. Thus the actual minimum is $4$.

**Fix:** write “Fix an **integer** Lorentz dimension cap $d\geq3$.” This preserves the intended theorem and proof. Alternatively, replace the real cap by its floor throughout, but that is unnecessary complexity. No change to the integer-cap mathematics is needed.

**Severity:** minor hypothesis omission. It does not undermine the intended result or any central contribution.

No other actionable major or minor issue was identified.

## Mathematical assessment

The main resource distinctions are maintained consistently. In particular, the entire-certificate-fiber minimax is not replaced by a bound for one convenient selection. The semialgebraic minimum-rank selection and dense-open lower bound justify the relevant quantifiers. The Peirce-perspective construction includes the exceptional Jordan algebra without assuming associative octonionic matrix multiplication. Product compression uses certificates inherited from the original lift, and the manuscript does not infer a universal aggregate-fiber lower bound from the existence of a high-rank aggregated certificate.

The global-selection statements retain their extra hypotheses. I checked the distinctions among local smooth strata, globally $C^1$ full-slack selections, joint kernels, and compact whole fibers of constant nullity. The norm-tree examples explain why nonsmooth or merely Lipschitz selections do not contradict the global bounds. The covering and orbit arguments are consistent with the exceptional real low-order cases. In the topology appendix, the equal-sphere-product restriction is explicitly necessary rather than a sufficiency classification; it does not misuse the sphere-total-space theorem for product sources. The bundle statements do not quietly assume that a subbundle of a trivial bundle is trivial.

For barriers, the standard restricted parameter and the optimum over all barriers remain distinct. The boundary-nullity, recession, one-channel rigidity, and compact-fiber arguments support their stated conclusions. The narrow-cap interval that is not completely classified is identified as such; it is not advertised as an exact optimum. The concrete norm-tree root correction, grouped/packed intrinsic lower bounds, balance slices, and shared spectral formulation calculations are compatible with these distinctions. The only defect I found in this material is the integer-cap omission above.

The additional body families retain the assumptions needed for their conclusions: whole-row identities versus contact-only data; necessary shared-face budgets versus attaining constructions; scalar power-cone versus higher-dimensional smooth-contact arguments; and sparse PSD completion versus sparse PSD matrices. The nonsymmetric and entropy material distinguishes existence of a barrier from efficient derivative evaluation. The approximation arguments retain conditioning, derivative control, and selector regularity rather than drawing an exact-rank conclusion from Hausdorff approximation alone. The compiler results are explicitly tied to their permitted translation, radial, feature, projection, or reusable-output operations.

I checked the exposed-minor movement derivations, their primal–dual counterparts, and their composition with certificate ranks. These proofs use the same exposing certificate where that is required. The weighted-tree distance coefficient correctly treats active and inactive nodes differently; the lower-bound potential and the explicit upper path agree to leading order for a fixed objective. The manuscript does not exchange that fixed-objective asymptotic with an objective depending on the target accuracy. The central-length and shortest-distance assertions remain separate.

The PSD quotient section tracks both the eliminated Hessian and the right-hand side. Its first-power comparison uses feasibility and the source allocation equations at the same projected point. The generic squared comparison is not silently improved without those equations, and the sharp example is feasible. The Newton comparisons distinguish exact arithmetic from bit complexity, conditional operator access from an explicit matrix, and a readable classical direction from a quantum state. The dynamic scale theorem uses the stated nondestructive reusable-value contract; it is not promoted to a lower bound on the Newton trajectory of one fixed program. The sparse-list maintenance and fixed-data cache examples correctly delimit the query lower bound. The output and compiler arguments keep full-output/search costs separate from dense writing costs and from representation-independent algorithmic lower bounds.

## Literature, novelty, and coverage

The introduction gives concrete, limited novelty claims for three formulas and their quantifiers. It attributes the classical ingredients and explicitly acknowledges overlapping movement results in the companion manuscript. The proofs needed here are reproduced, so the paper is mathematically standalone despite that companion's unpublished status.

My targeted primary-source checks support the literature distinctions made in the introduction:

- [Gouveia–Parrilo–Thomas](https://arxiv.org/abs/1111.3164) supplies the lift/factorization framework.
- [Fawzi–Parrilo](https://arxiv.org/abs/1311.2571) treats fixed-size PSD product lifts and lower bounds for polytope formulations; it is not presented as the same certificate-fiber invariant.
- [Kummer](https://arxiv.org/html/1506.07699) studies direct spectrahedral descriptions; the manuscript correctly distinguishes these from projected cone products.
- [Saunderson](https://arxiv.org/html/1902.06401) uses neighborliness and face-chain restrictions for nonexistence results. The manuscript's quantitative representable-body conclusions have a different scope.
- [Scheiderer, version 2](https://arxiv.org/html/2509.17121v2), Theorem 1.2, establishes SOC representability under the stated smoothness and curvature conditions. The manuscript accurately separates that existence theorem from its factor-count, certificate, and global-selection questions.
- [Browder's primary paper](https://www.researchgate.net/publication/251964661_Fiberings_of_spheres_and_-spaces_which_are_rational_homology_spheres), Theorem 1, supports the connected-fiber statement used in the appendix. I checked the reproduced article text, not a secondary summary.
- [Apers–Gribling](https://arxiv.org/html/2311.03215), including its row-access convention, supports treating the cited quantum LP results as access-dependent algorithmic comparators.

These checks do not establish that no other literature contains an equivalent result. The manuscript's narrow formulation of its contributions is appropriate; no broader priority claim should be inferred from this review.

I independently checked that the source-map inventory has 201 distinct workbench paths, exactly matching the 201 current active/parked notes, with no missing or extra path. That verifies the inventory, not the correctness of every routing disposition. My targeted comparisons confirm that the selected certificate frontier and dynamic-scale developments are represented, and that the manuscript develops the off-center quotient comparison beyond the workbench's generic squared estimate. The companion norm-tree material is acknowledged rather than repackaged as entirely new. I found no concrete omission within the stated paper scope. I have not independently certified all 136 included-source dispositions at the individual-result level.

## Organization and build

The manuscript is long, but its model table, notation table, six-part structure, cross-references, appendices, and closing synthesis make its scope navigable. The introduction identifies the three central formulas and explains which later sections supply applications and computational qualifications. I do not regard its length alone as a mathematical or presentation defect given the requested comprehensive scope; journal format and length policy remain editorial choices.

I built a source-only isolated copy in `/tmp/qipm-finalreview5-mnsmwbch` using the `qipm` environment and the supplied Makefile. After including the repository's required `macros.tex` in that copy, the clean build succeeded and produced a 183-page PDF. The final log contained no LaTeX warnings, undefined references/citations, or overfull boxes. This was a compilation check, not an independent visual inspection of every PDF page. No manuscript source or shared build artifact was changed during this review.

## Disposition

There are **zero major findings and one minor finding**. Correct the integer hypothesis in `cor:tree-cap-parameter`; I found no further issue that warrants delaying completion of the mathematical draft. This conclusion reflects an analytical peer review of every manuscript proof, supplemented by the bounded literature, coverage, and compilation checks described above; it is not formal proof verification or exhaustive literature verification.
