# Stage 5, round 1 — independent review 02

**Verdict: accept after one minor citation-locator correction. No major or mathematical finding.**

## Scope and verification

Reviewed the frozen `process/snapshots/stage05-round01` inputs. The manifest digest is `c25d5edb69e64647034e54fea863d4637e410b2a22461e8d3d378741d67fd6b5`; all 13 entries match. I read the complete `sections/05-boundaries.tex` and `appendices/d-path-geometry.tex`, main/README/bibliography/coverage integration, and the relevant accepted prerequisites. All four preceding mathematical sections and three preceding appendices are byte-for-byte unchanged from stage04-accepted.

All verification is isolated in `verification/reviewer02/stage05/`. The copied manuscript builds successfully with latexmk. The final log has no LaTeX, citation, reference or box warnings; all 206 labels are unique and references resolve. Frozen hashes were rechecked after review. An independently written exact rational diagnostic passed 642 original-cube exposure edge checks, 18 padded target-equivalence checks, and the full-sign Lasso recursion through dimension five. These finite checks supplement the proofs, not replace them.

I did not modify manuscript or frozen source files, delegate, or read other current reviewer reports or root assessments. Literature instructions were read; no literature package or generated metadata was changed. Stage 6 computation/contact reconstruction and stage 7 synthesis remain later scope.

## Actionable finding

### R02-S05-01 — Minor: distinguish the PDF and HTML theorem numbering

**Location:** `sections/05-boundaries.tex:22–23`, the optional citation locator `Theorem~2.1 and Section~4` for `SugishitaCarvalho2026`.

The cited v2 PDF labels its main NP-completeness result **Theorem 1**, on printed p.3. The arXiv HTML rendering labels the same result **Theorem 2.1**. The current citation uses the HTML numbering without indicating that distinction, so a reader of the linked paper's PDF cannot find the numbered theorem. The substantive attribution is correct.

**Evidence:** independently downloaded [arXiv:2510.21126v2 PDF](https://arxiv.org/pdf/2510.21126v2), read and visually checked p.3. A retained rendering is `verification/reviewer02/stage05/sugishita-p3.png`. The [HTML rendering](https://arxiv.org/html/2510.21126v2) has the conflicting label. Section 4 is the correct reduction location in both.

**Correction:** cite “Theorem 1 and Section 4” using the PDF numbering. Alternatively explicitly identify both versions, e.g. “Theorem 1 (Theorem 2.1 in the HTML version), Section 4.” No theorem or bibliography-content change is needed.

## Mathematical assessment

### Dense and near-identity hardness

The active-status certificate in `lem:box-np` is sufficient: positive definite principal systems give polynomial-length rational affine responses, and weak free-coordinate bounds include degeneracy. A nonempty rational leader polyhedron supplies a polynomial-size rational witness. This NP argument is restricted to affine upper data and is not silently reused for arbitrary quadratic upper rows.

For `thm:dense-hardness`, I checked the ternary leader encoding, residual signs, geometric tail and auxiliary feedback bounds. The smallest base residual margin still exceeds the combined feedback. Conditional minimization yields the minority-distance and clause-shortfall identities at every response. Distinct variables in each clause justify the unsatisfiable rounding bound, yielding zero versus at least two without response upper rows. The weighted triangular residual map is nonsingular, so the Hessian is positive definite. The distinction between the jointly convex squared representation and removal of a leader-only term is correct.

For `thm:conditioned-hardness`, the feedforward states and inactive residuals have the stated ranges. Positive diagonal scaling preserves that feedforward computation, while the actual quadratic optimizer has a backward residual term. The proof controls relative coordinate error rather than only a small absolute error. The nilpotent nonnegative inverse, the bound on the reverse scaled matrix, and absorption of the error term justify the final readout gap. Decreasing the scaling ratio preserves these bounds. Both row and column norms control the symmetric Hessian perturbation, its eigenvalues and diagonal dominance. The threshold and all rational scales have polynomial encoding even with the additional tolerance. The no-accuracy-bit conclusion uses the small encoded gap and does not imply a constant normalized gap or strong hardness.

### Conditioned approximation and leader structure

In `thm:conditioned-grid`, the endpoint saturation tests are valid also at equality. On a closed saturation cell, response changes vanish outside the unsaturated coordinates; the summed variational inequalities therefore use only the remaining cost differences. The maximum-minor row basis controls all such differences with coefficients bounded by one. Its coordinate widths are bounded by `K`, although offsets may have large numerical magnitude. Minimizing the direct leader cost inside each grid preimage avoids a numerical dependence on that cost's Lipschitz constant. The stated count is polynomial for fixed leader dimension and numerical `K,1/epsilon`.

The exact follower oracle is also valid. Projected gradient contracts by at most `1-1/K`; the explicit iteration count exceeds the required precision. Clearing all input denominators bounds optimum-coordinate denominators by principal determinants. The separation and continued-fraction argument recovers the unique bounded-denominator rational, including endpoint coordinates. Iterates have polynomial bit length in the allowed numerical runtime parameters. The `N=0`, `r=0`, and zero response-objective cases are covered.

For `thm:growing-leader`, the cited source supplies a gap on continuous inputs, not merely discrete witnesses. Restricting to a polynomially bounded box preserves the yes witness and cannot improve the no maximum. Scaling each affine input prevents upper clipping; polynomial duplication then restores the constant absolute gap with bounded coefficients. Every resulting follower still depends on at most two leaders. Polynomial output size and `r=k` preserve the W[1] and ETH parameters.

The separate mixed-radix proof checks out: the alternating clipped sum equals twice the label distance, and the pair interpolation is nonnegative and 1-Lipschitz. A bad rounded pair yields the stated gap. The scaled two-ReLU identity holds on the entire leader box, and its duplication count remains polynomial.

The bounded-core algorithm enumerates all relevant arrangement vertices with independent noncore normals. Box facets cover degeneracy. Candidate values become affine after the first core partition, so pairwise comparison refinement is legitimate. On closures the selected candidates remain feasible; completeness at an optimal relative cell handles candidates that become feasible only at boundaries. The runtime claim is polynomial for fixed core/component bounds, without an FPT claim.

The leader-path Subset Sum identity follows in both directions from telescoping and cumulative subset paths. The last-coordinate modification proves the exact distance message without leaving the leader box. The repeated half-gain factor has the stated weighted telescope and dyadic terminal set; its final tail accounts for the odd piece count. These message-size examples are correctly separated from NP-hardness and from the follower-constraint path.

### Sparse path geometry, the new padding transfer, and strips

The Klee–Minty endpoint descriptions, edge directions and terminal-coordinate injectivity are correct. The appendix reproduces the actual sparse-shadow coefficients and exposing prices from Gärtner et al. Its leading-term sign calculation gives unique exposure; backward elimination evaluates the value without constructing its exponential set of pieces. The terminal message count includes both extreme terminal values. The epigraph lower bound correctly uses vanishing on each distinct boundary line and excludes extended/quantified representations.

The telescoping polynomial is nonnegative and vanishes exactly at original path vertices. Its parabolic exposure identity is exact. For the quadratic follower, terminal denominators give the squared separation used in the linear-score loss. Writing a point as a convex combination of vertices controls both its distance and the possible decrease of the squared norm. The perturbation `tau=Delta/(2n)` preserves strict optimality, including a nontrivial one-sided price interval at each endpoint. Rescaling the complete follower objective makes the Hessian exactly identity without changing responses.

I independently checked the new padded identity-Hessian reduction in detail. Padding bounds force lower endpoints only after the nonnegative vertex polynomial has forced an original full-cube vertex; they do not falsely identify all vertices of the truncated polytope with the original vertices. Every free-bit assignment extends to a feasible original vertex. Its response inequality was proved on the whole original cube, hence remains valid on the padded subset. The free-coordinate error is at most `4^(-(r+1))`, giving the same weighted `1/8` and integrality `3/8` bounds. Full-dimension terminal denominators, `tau`, and identity rescaling have polynomial bit lengths. Thus both directions and the restricted NP certificate survive padding.

The slab-only feasibility and attainment statements use continuity of the true unique response, with zero and the all-free-one pattern supplying the endpoint sums. The nonconvex quadratic row remains essential to this reduction. Fixed local inequality alphabets do not imply bounded aggregate weights or bounded rescaled costs; the text says so explicitly.

The equal-gain strip projection handles signs correctly. Nonzero gains normalize to two-sided difference constraints; nonnegative backtracks justify unique-path shortest distances. The all-pairs inequalities are both necessary and sufficient, and minimum-of-upper-propagations recovery respects retained values. Zero gains add bounds at the original head. An arbitrary tree can use reciprocal gains when traversed backwards, with no new field extension. Removing a fixed total number of nonforest edges leaves only a fixed number of additional retained states. Polynomial products and denominator clearing in fixed parameter dimension establish the symbolic bounds. The statement keeps its restrictions on eliminated-state objectives and on infimum versus attainment.

### Curvature and arithmetic

Both zero- and negative-curvature reductions use precisely optimistic existential semantics. The new single-power examples force a positive leader no larger than `(5/8)^P`, so reduced rational denominators have exponential numerical size and linear bit length in `P`. The second example indeed has a convex reduced row and a strict anchor; neither removes numerical-degree dependence. The sparse upper equation has the claimed Eisenstein degree with a trivial positive quadratic follower.

The multiquadratic induction is sound: simultaneous sign-change eigenspaces are one-dimensional in the radical-product basis, and prime-valuation parity prevents the next radical from belonging to the previous field. Distinct signed sums give the full degree. The cubic followers have uniform curvature on their supplied intervals. Singleton quadratic leaves encode exact Square Root Sum, while the text properly separates an exact comparison problem from an NP-hardness assertion and from short radical-expression output.

## Primary-source checks and limitations

- **Mairal–Yu:** read Proposition 2, equation (4), and the square invertible recursive construction in the [primary paper](https://arxiv.org/pdf/1205.0079), p.3–6; visually checked equation (4). Deriving the dual with `u=A^T residual/lambda` yields exactly the displayed Hessian and linear term. Full primal support makes `u` its sign vector. Induction over the source recursion supplies all full sign vectors with positive last coordinate. The manuscript correctly labels the Boolean consequence as an inference and does not obtain hardness encoding bounds from path length alone.
- **Sugishita–Carvalho v2:** checked the actual PDF and current HTML main theorem and Section 4 digit/penalty construction. The scalar-leader/no-upper-row linear-bilevel predecessor is correctly credited, subject to the locator correction above.
- **Froese–Grillo–Hertrich–Stargalla v3:** accessed the [actual September 3, 2026 text](https://arxiv.org/html/2509.22849v3) and downloaded its PDF. Read Proposition 4.1's proof, the greedy Sidon bound, node/edge ReLU expressions, Theorem 5.3 and Corollary 5.5. Polynomial label magnitudes, unary/binary neuron support, and the continuous one-unit gap support this specific transfer. The proof uses the explicit ReLU spike expression; no discrete-input assumption is needed.
- **Gärtner–Helbling–Ota–Takahashi:** read [Section 4](https://arxiv.org/pdf/1308.2495), especially Definition 11 and Lemma 12 on p.8–9; visually compared the source coefficients and exposing-price formula. The appendix attributes the exact construction it uses.
- **Scaling and lifted energies:** read [El Ghaoui et al.](https://arxiv.org/pdf/1908.06315), §2.5, equations (2.6)–(2.7), and [Zach–Estellers](https://arxiv.org/pdf/1905.02507), §2, equations (1)–(4). They support the credited diagonal scaling and weak-feedback convex-energy precedents. The manuscript supplies its own rational error and hardness bounds.
- **Conditioned approximation:** checked [Awerbuch–Kleinberg](https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf), Proposition 2.2, p.4, for the determinant proof; [Bemporad–Filippi](https://cse.lab.imtlucca.it/~bemporad/publications/papers/cdc01-sub-mpqp.pdf), Theorem 4, p.5, for the uniform optimizer-error claim. Read the local primary Giesen–Jaggi–Laue text, p.1–3, and Giesen–Mueller–Laue–Swiercy, p.1–3, Lemma 4/Theorem 5. Their guarantees are described as precedents, and the parameter-range/slope factors are not discarded.
- **Decomposition and messages:** the Dvořák et al. publisher/author repository material supports the limited broad comparison with integer programs and fracture backdoors; no detailed theorem transfer is asserted. Read [Meuleau–Morris–Yorke-Smith](https://homepage.tudelft.nl/0p6y8/papers/n58.pdf), Lemmas 1–2 and Theorem 1, p.3–4. Closure is correctly distinguished from a polynomial bound on intermediate message size.
- **Square Root Sum:** checked the local primary Eisenbrand–Haeberle–Singer text, p.1–2, and its [published source](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2024.54). A current search found no resolution superseding the stated open exact polynomial-time comparison question. This is a bounded literature check, not proof of novelty or an exhaustive search.

Some accessed texts are primary preprints of the cited publications; these are identified above. I did not need inaccessible detailed theorems to support a mathematical conclusion. The report's analytical checks and finite diagnostic do not establish a general implementation's performance, and the paper makes no such stage 5 claim.
