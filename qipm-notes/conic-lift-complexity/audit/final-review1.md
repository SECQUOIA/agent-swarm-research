# Independent whole-manuscript review 1

Review date: 2026-09-20.

**Recommendation:** No revision required on the mathematical, scientific, attribution, or exposition grounds examined in this review. I found **no major issues and no minor issues requiring correction**. This is an independent assessment of the submitted source, not an inference from previous review outcomes.

## Scope and independence

I personally read `main.tex`, `macros.tex`, `bibliography.bib`, and every paragraph and proof in all 35 `sections/*.tex` files. The reading covered all six parts, the introduction and synthesis, and all four appendices. In particular, it included:

- `00-introduction`, `01-foundations`, `02-certificate-rank`, `03-products`, `04-global-regularity`, and `05-support-orbits`;
- `06-restricted-barriers`, `07-concrete-barriers`, and all five `08a`–`08e` files;
- all five `09a`–`09e` files and all seven `10a`–`10g` files;
- all four `11a`–`11d` files, all five `12a`–`12e` files, and `13-synthesis`.

I did not delegate any part of this review and did not read other reviewers' reports, assessments, author/helper reports, root preparation checks, or workflow conclusions. After completing the manuscript reading, I consulted the permitted source map for coverage routing and compared representative original workbench developments with their manuscript treatments. I consulted local literature records and primary online literature. I made no manuscript changes.

The composite SHA-256 of the reviewed source files is `51dd07601e5299da5107a92d0b9d869918b0ca461fb4a40c9e2e8bbccbc729cf`. This hash concatenates each relative filename, a zero byte, its contents, and a zero byte, in the order `main.tex`, `macros.tex`, `bibliography.bib`, followed by the lexicographically sorted 35 section files.

This was a proof and source review. I did not independently rebuild the PDF or inspect every rendered page; the parent reviewer is checking the final artifact. I did not read every original workbench note or every cited publication in full. My claim of complete reading applies to the manuscript itself.

## Mathematical assessment

### Curvature, certificates, and product sources

I checked the passage from normalized certificates on the entire affine slice to the differentiated slack identity. The distinction between genuine certificates and arbitrary boundary factorizations is maintained where it matters. The dimension-minus-two argument deals with zero and ray factors, and the symmetric-cone refinement correctly uses the mixed Peirce dimension `a p q`. The argument includes the exceptional algebra without treating octonionic matrices as associative matrices.

The order of quantifiers in the entire-fiber rank invariant is consistent throughout: the lift is fixed, the support is chosen, and rank is minimized over its whole certificate fiber. Semialgebraic minimum-rank selection and common stratification justify the dense-open lower bound without assuming global regularity. I checked the Peirce-perspective upper construction, its normalization, and its exceptional support. It supplies the asserted worst-support bound rather than merely a local construction.

The sequential compression argument retains certificates for the original affine representation while passing to appropriate faces. The product conclusions correctly distinguish existence of a high-rank aggregate certificate from claims about every aggregate certificate. Private curvature and the separate support quotients justify the additive statements that are actually made. I found no illicit exchange of minimization, maximization, or support selection.

### Global topology and whole fibers

I read the support-orbit, active-ray, covering, cup-product, submersion, and cylinder arguments, including the real low-order exceptions. Their hypotheses distinguish global selections from generic local selections. The real order-three exclusion uses the full slack identity, not merely a dimension count or a conjectured classification of sphere maps. The separate treatment of joint contact factorizations avoids importing a full-slack no-sharing theorem into a weaker model.

I checked the whole-fiber constant-nullity descent and the one-channel rigidity argument. Convexity of fibers, equality of the relevant supports, and compactness are used in the necessary places. The bounded narrow-cap interval is explicitly left as an interval; neither the introduction nor synthesis advertises a complete selection-free barrier classification.

The four appendices are substantive and consistent with the main text. In particular, the projective embedding obstruction concerns restricted kernels rather than a representation of the entire PSD cone. The approximate phase results retain the one-sided derivative and gauge assumptions they need. The conditioning counterexamples correctly separate raw coordinate conditioning from the invariant Schur operator.

### Barriers and additional cone families

I checked the boundary-nullity and recession lower tests, the root-incidence calculation for norm-tree parameters, and the marginal barriers of grouped and packed lifts. The statements keep ambient standard parameters, restricted standard parameters, and intrinsic optimal parameters distinct. The bounded-fiber argument used for an arbitrary barrier on a packed affine domain has the required convexity and recession justification.

The whole-row dimension arguments, shared-face inequalities, balance slices, norm and power cone constructions, spectral contacts, and chordal completion arguments have compatible dimensions and hypotheses. The power-cone conclusions do not assume smoothness at coordinate singularities. The spectral contact count includes the phase directions correctly. The nonsymmetric barrier discussion states parameter intervals and conditional constructions without elevating them to an unsupported classification. The entropy aggregation accounts for closure and zero columns.

The compiler sections distinguish a prescribed finite-statistic or reusable-output model from arbitrary extended formulations. The Farkas projection includes range equalities and lineality. The dilation and exponential-feature examples do not use feature rank as an unrestricted cone-lift lower bound. The projected quadratic compiler preserves the qualifications on objectives and auxiliary variables needed by its marginalization argument.

### Movement and the weighted-tree distance theorem

I checked the exposed-minor and Jordan-rank distance estimates, including the weighted normalization and the endpoint dependence. The primal–dual speed splitting uses the two complementary Hessian projections and is not substituted for a primal-only assertion. All iteration consequences retain a stated metric and bounded-chord contract.

For the exact weighted-tree coefficient, I checked both directions of the proof. The lower potential uses coefficient `omega_v` on active logarithmic support slacks and `omega_v/2` on inactive determinant terms. Its ambient dual norm gives the claimed sum of active weights plus half the inactive weights. Inactive subtree determinants are bounded by the objective gap through their active ancestors. For the upper curve, the slowly shrinking inactive subtrees produce the matching half-weight contribution; the remaining integration error has the stated logarithmic-logarithmic order. The fixed-tree, fixed-weight, fixed-objective asymptotic is essential and is stated explicitly. This is a developed sharp result, not just the earlier all-positive-objective lower bound transcribed into paper form.

### Newton elimination, work, and query models

I independently checked the off-center quotient-Hessian calculation. The allocation Gram matrix is the Gram matrix of the correct Riesz representatives, and its positivity follows from the source projectors. Exact source allocation gives the first-power comparison with the diagonal fiber center. The proof does not merely reuse the weaker generic squared bound. The reduced linear term is separately eliminated, and the sharp two-source example realizes the asserted condition factor. Access to the resulting matrices and preconditioner is not declared free.

The resource ledgers keep free coordinates separate from ambient cone coordinates. The small-order special cases and the sufficient packing constructions do not imply unproved global attainment. Sparse Newton elimination distinguishes field-operation bounds, numerical conditioning, and full-output contracts; the positive two-hub construction and the indefinite one-hub representation are used for their respective purposes.

The query sections specify what an oracle supplies and what an algorithm must output. The reusable compile-and-commit direct sum has the required recovery contract, while one coherent raw-backed evaluation is charged differently. The zero-or-one-mark exact search upper bound uses verification, so its multi-output upper bound does not silently need logarithmic error amplification. The central-state examples distinguish public norms and hidden scale information. Static input caching is explicitly allowed, and the paper does not multiply a one-shot query lower bound by geometric movement without a fresh-cost premise.

The active compiler lower bounds concern reusable classical descriptions or a stated service contract. They do not rule out an oracle wrapper that continues using the raw input. The fixed-objective and entropy examples state their margin, gap, and metric scales. I found no model mismatch that invalidates their separations.

## Attribution, novelty, and source integration

I read the introduction's related-work discussion and the complete bibliography. The manuscript treats cone factorization, Jordan structure, classical norm trees, chordal completion, self-concordant barrier theory, quantum search, and the adversary framework as prior tools. Its new claims are stated at the level of the precise resource, quantifiers, or comparison being proved.

I independently checked the following particularly relevant primary-source boundaries:

- Gouveia–Parrilo–Thomas is the established lift/factorization bridge, not evidence by itself for the present sharp rank frontier. The local literature record identifies the precise theorem and properness qualification; see [the primary paper](https://arxiv.org/abs/1111.3164).
- Fawzi–Parrilo studies extension complexity with fixed-size PSD blocks. The manuscript correctly treats this as prior work on the block-size resource rather than priority for this paper's smooth-curvature certificate invariant; see [the authors' paper](https://arxiv.org/abs/1311.2571).
- Kummer's results concern spectrahedral descriptions of balls, and Averkov's concern the minimum permitted LMI order in extended formulations of polynomial cones. The manuscript respects these distinct optimization classes; see [Kummer](https://arxiv.org/abs/1506.07699) and [Averkov](https://arxiv.org/abs/1806.08656).
- Scheiderer's version 2 gives SOC representability under the stated Nash-smooth positive-curvature assumptions. This is consistent with, and does not contradict, a quantitative cost or global-selector penalty for a particular class of lifts; see [the primary preprint](https://arxiv.org/html/2509.17121v2).
- The everywhere-differentiable inverse theorem is a potentially delicate dependency. Saint Raymond's primary abstract explicitly states the extension of finite-dimensional local inversion to differentiable maps whose Jacobian never vanishes. The manuscript does not silently invoke the ordinary continuously differentiable inverse theorem; see [the journal article](https://www.cambridge.org/core/journals/mathematika/article/abs/local-inversion-for-differentiable-functions-and-the-darboux-property/5BE7FE09B3537A86F87FBF705E1B20D0).
- Browder's Theorem 1 gives the homotopy-sphere alternatives needed by the sphere-fibration argument. I read the original two-page article through its author-uploaded text, including the connected-polyhedron hypotheses; see [Browder's article](https://www.researchgate.net/publication/251964661_Fiberings_of_spheres_and_H-spaces_which_are_rational_homology_spheres).

These checks support the manuscript's distinctions; they are not a proof of universal priority. I found no specific earlier result that contradicts the stated novelty boundaries, and the paper does not present an unsuccessful search as proof of novelty.

The source-map inventory is consistent with the families actually present in the manuscript. Representative comparisons included the original selection-free symmetric-cone rank frontier, the norm-tree movement note, the off-center PSD quotient-Hessian note, and the dynamic scale-maintenance note. The manuscript includes their material with the required model distinctions. It also develops the weighted-tree distance and first-power feasible-allocation comparison beyond those original statements. I identified no particular relevant development omitted from the manuscript within this coverage check.

## Overall structure and publication assessment

The paper is long, but the length follows the requested comprehensive scope. The introduction, model table, division into six parts, and synthesis make the dependencies and differences between models explicit. The appendix material is integrated by references rather than being required without explanation. The paper supplies proofs for its own results and identifies the external mathematical tools on which it relies.

I found no unsupported headline, internal contradiction, missing hypothesis, invalid proof step, or concrete exposition defect requiring revision. The remaining narrow-cap and nonsymmetric intervals are honestly delimited results, not hidden unfinished proofs of an advertised theorem. On the work examined here, the manuscript is suitable to proceed to submission preparation. Journal acceptance and absolute novelty remain matters for the journal and specialist readership, rather than conclusions that an internal review can certify.
