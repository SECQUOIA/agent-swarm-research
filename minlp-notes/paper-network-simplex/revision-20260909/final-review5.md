# Independent whole-manuscript referee report 5

**Manuscript:** *Sparse convex hulls for network flows coupled to a simplex*, anonymous frozen `final-round1` submission candidate.

**Verdict: Accept.** I found no major defect and no mandatory minor correction. The paper makes a substantial structural contribution, the proofs support its central claims, and the computational claims are appropriately limited. My optional editorial suggestion below is not a condition of acceptance.

I read the entire manuscript source, including all proofs, examples, tables, the conclusion, and bibliography, and inspected the delivery interfaces and computational implementation. I did not read prior or concurrent referee reports or adjudications. All executions described below were mine, using private extractions under `final-review5-evidence/`; I did not change the frozen submission or spawn agents.

## R5-A01 — Mathematical assessment: no defect found

The arguments form a coherent chain rather than relying on numerical confirmation of the main theorems.

- **Foundations and block reduction.** The disaggregation proof explicitly handles empty flow polytopes and zero weights. The integral-flow corollary correctly distinguishes equality of hulls from a bound on the number of integral points in a decomposition. The circulation-space factorization justifies independent blocks at articulation vertices. Proportional refinement of locally merged states restores a common global simplex without creating incompatible blockwise weights.
- **Observation-sensitive compression.** The coefficient argument in `sections/02-compression.tex`, particularly the unit-minor lemma and pivot reconstruction, accounts for repeated observations and disjoint label columns. The nullity equals the cycle rank of the unobserved subgraph, including isolated vertices and loops. All residual capacity bounds survive elimination. The individual-product completion minimum is properly restricted to reconstruction on the ambient circulation space; it is not misrepresented as an extension-complexity lower bound. Fixed-arc preprocessing and the distinction between row counts and nonzeros are adequate.
- **Structured and bounded-rank oracles.** Theta support formulas include local nonemptiness and lower-dimensional sums. The parallel-path sufficiency proof establishes nonnegative shifted row targets before invoking transportation feasibility. Active-branch extraction has the correct global inequality direction. In `sections/04-bounded-rank.tex`, local positive circuits, edge directions, support rays, and dual bases collectively give complete separation. The stronger multiplier bound uses the transformed edge directions, not an unjustified bound on a product of matrices. Recovery includes ambient-rank bases for lower-dimensional feasible regions. Its sequential denominator argument supports polynomial encoding length without confusing arithmetic counts with bit complexity.
- **Coefficient obstructions.** The local coordinate-section lemma preserves the two free product coefficients under addition of affine-hull equations. The five-product K4 construction proves local sufficiency as well as necessity. The transportation transfer retains the designated products directly and checks the state capacities. The balanced-incidence and Fibonacci arguments likewise provide local feasible witnesses; they do not infer a sparse projected facet merely from a facet in a larger space. The simple maximum-degree-three transformation retains the same free section.
- **Fixed-label chains.** The complete profile system includes observations on both gadget arcs and the bypass, zero rows, nonnegativity, and the residual profile bounds. The three-label proof establishes completeness of the 16 circuits and checks repeated occurrences of original variables. Both exceptional bypass coefficients are repaired using a flow equation without increasing another coefficient beyond one. The four-label obstruction and the restriction to the specified flat topology are clear.

These conclusions are a referee's mathematical assessment, not a formal verification of every possible instance. I found no counterexample or essential missing hypothesis.

## R5-A02 — Novelty and significance: adequately supported

The manuscript does not claim novelty for simplex disaggregation, generic polynomial-time separation, common-factor elimination, transportation projection, or the general Minkowski support argument. Its narrower contributions are meaningful: an observation-sensitive exact construction with controlled original and auxiliary coefficients; structural separation and recovery bounds; and sharp or sparse obstructions concerning actual retained product coordinates. The coefficient results are particularly valuable because a small extended formulation or an integral underlying network alone does not settle this projected geometry.

I checked the published [De Loera–Onn paper](https://math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf), especially Theorems 1.1–1.2 and Section 3.3, printed page 816. The explicit first-layer injection supports the precise imported property needed here. I also downloaded and inspected the published [Khademnia–Davarnia article](https://par.nsf.gov/servlets/purl/10546393): the complete EC&R theorem and its treatment of equality balances support the manuscript's characterization of this predecessor. The paper appropriately separates that complete framework from its particular tree and forest constructions. These primary PDFs and extraction records are in my evidence directory.

I have not independently surveyed every cited geometric or elimination predecessor exhaustively. Within the central prior-work comparison checked here, I found no priority claim requiring correction. The scientific contribution is primarily polyhedral and algorithmic structure, rather than an experimentally demonstrated advance in general-purpose optimization speed.

## R5-A03 — Computational claims and intended use: supported within the stated scope

`sections/08-computation.tex` makes the crucial distinctions consistently. Exact rational assembly followed by HiGHS optimization is numerical evidence; `numerically_feasible` is not promoted to exact membership. The Farkas routine accepts a cut only after exact nonnegativity, auxiliary cancellation, and rational violation checks. I inspected that implementation. The reconstruction adapter used in the optimization experiment is expressly limited to these synthetic instances.

The principal comparators retain elementary improvements: unused labels are merged globally, fixed weights permit native state-flow bounds, two positive states permit a one-flow membership LP, and uncoupled fixed-weight optimization permits independent network solves. Inspection of `strong_baselines.py` and `paper_stage06.py` supports the described objective substitutions, additional-row handling, state removal, timing boundaries, and unsuccessful-solver semantics. The all-labels-observed control isolates a graph-local reduction that global merging cannot explain. The budget control correctly compares intersections of the component hull with a common row.

The reported results justify formulation-size and exact-certificate benefits. They do not establish superiority for industrial workloads, callbacks, warm-started solves, or general nested series–parallel graphs. The manuscript already says this, records cases where ordinary LPs win, and describes the transportation application as an interpretation. Its modest computational claim is therefore proportionate to the evidence. Requiring an industrial benchmark would enlarge the paper's stated claim rather than correct a current defect.

## R5-A04 — Standalone reproduction and anonymity: checks passed

I extracted both delivery ZIPs independently. All three delivery artifact hashes match the delivery manifest. Both payload manifests pass. Regenerating the five table/value files from the canonical raw data succeeds and leaves their payload hashes unchanged. The LaTeX archive builds to a 50-page PDF **byte-identical** to `delivery/submission.pdf`; the final LaTeX log has no undefined-reference or box warnings. PDF metadata has an empty author and no identifying date or path metadata. A text scan of the supplement found no local home paths or author-account strings. This is a practical anonymity check, not a guarantee against every possible inference about authorship.

The documented Python interfaces, index convention, numerical statuses, dependency distinction, preserved comparator layout, and table regeneration commands make the supplement usable without the development repository. The historical timing environment is distinguished from the package-validation environment. My initial attempts used the extraction container rather than the ZIP's internal package root; those were my path errors, resolved by entering the directory containing the supplied README, and are not packaging failures.

Actual checks, with logs in `final-review5-evidence/`:

| Check | Result |
|---|---|
| Documented principal unittest command | 23 tests passed |
| Table generator and both payload manifests | Passed; table bytes unchanged |
| Standalone LaTeX build | Passed; delivered PDF reproduced exactly |
| General compressed implementation audit | 600 objective comparisons, 758 membership comparisons, 476 exact Farkas cuts; passed |
| Independent flat implementation audit | 233 numerical path-hull comparisons, 192 exact decompositions, exact rejection checks; passed |
| Independent exact contract check | 2,196 queries, including 1,117 zero-weight and 498 tiny-weight queries; passed |
| Incidence/elimination/completion check | 1,180 cycle minors, 1,408 observation sets, 1,484 pivots; passed |
| Independent mathematical constructions | 1,681 exact theta Minkowski pairs, 8,360 recoveries, reduced circuits and Fibonacci witnesses; passed |
| Fibonacci facet and three-label repair checks | Passed, including both exceptional repair families and the four-label obstruction |
| Documented stage checks and structural integration | All six stage checks passed; integration recovered ratios 2, 5, and 21 |
| Standalone quick measurement protocol | All six cases passed; principal objective reproduced as approximately −6.981916795 |

I used the available Python environment rather than creating a fresh dependency environment. The quick benchmark used one recorded repetition and ran alongside other audits; its timings are not an independent replication of the published speed ordering. I did not rerun the complete five-repetition measurement campaign or independently implement arbitrary transportation universality. Numerical LP comparisons remain numerical checks even where the accompanying cuts or decompositions were checked exactly.

## R5-O01 — Minor, optional editorial preference

**Location:** `sections/02-compression.tex`, observation-sensitive construction and forest-complement example.

The main reduction is less visually immediate than the later flat-chain construction. A small drawing marking observed edges, a spanning forest of the unobserved edges, and the remaining completion edges would help a reader see why the residual count is a cycle rank. This would be an accessibility improvement only. The existing definitions, equations, and K4 example are sufficient, and no theorem or claim depends on adding a figure.

**Required corrections:** none. **Major findings:** none. **Mandatory minor findings:** none.
