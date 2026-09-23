# Stage 1, round 1 — independent review 5

Reviewed `main.tex`, `macros.tex`, `bibliography.bib`, and all of sections 02–04, together with the four Stage 1 research notes identified in `audit/source-map.md`. I did not read other reviewer reports or edit the manuscript. The requested `../AGENTS.md` does not exist; the applicable repository instructions in `/home/sgusev/repo/qipm/AGENTS.md` were read. Joint accuracy, the LP application, and a full introduction/literature review are outside this review.

**Result: 0 major findings, 3 minor findings.** The staircase, including equality at every threshold and the exceptional coarse tier at `c=1`, is supported by the proofs. The minor findings concern explicit domains and definitions; none changes a claimed query exponent.

## Findings

### R5-1 — Minor: several auxiliary inequalities omit their bounded domains

**Location:** `sections/04-fixed-accuracy.tex:127`, `:161`, `:169`, and `:272`.

The pinned-gate tail is stated for `|x| >= C_0 delta`, with no upper bound on `|x|`. Its proof uses real `arcsin x` and establishes the estimate only on `[-1,1]`; that intended domain should be included. Likewise, `d(x)=1-x-S_N(x^2) in [0,1]` is asserted for all `x>=0`, although it is established only for `0<=x<=1`. The Fejér estimate `F_m(u)<=1/(m^2 u)` needs `0<u<=1`; for example, `F_3(u)=(1-4u/3)^2` disproves the unrestricted positive-domain assertion. Calling `G_r-e(y)` a “nonnegative polynomial” is also potentially misleading in a paper whose central constraint is global nonnegativity: this polynomial is nonnegative on `[1,rho]`, but negative outside that interval for sufficiently large `|y|`.

**Repair:** State `C_0 delta<=|x|<=1`, `0<=x<=1`, and `0<u<=1` in the respective claims. Say that `G_r-e` is nonnegative **on `[1,rho]`**. The proofs already use only these domains.

### R5-2 — Minor: make the integer index convention explicit

**Location:** `sections/04-fixed-accuracy.tex:2`, `:11`, the Exact thresholds theorem, the Nonnegative Taylor limit theorem, and the definition of `E_r`.

The text says “for `r>=0`” and minimizes over `j>=0` without stating that these are integer indices. This convention is inferable, but several literal statements require it: `T_{2r}` is introduced as a Chebyshev polynomial, the Taylor expansions use integer orders, and the parity argument removes an odd leading degree. Allowing arbitrary real `r` makes the stated Chebyshev formula inapplicable.

**Repair:** Introduce `r in Z_{≥0}` and `j in Z_{≥0}`, or declare once that all approximation-order indices are nonnegative integers. State positive integer `r` where needed.

### R5-3 — Minor: define general normalization before the normalization-boundary propositions

**Location:** `sections/02-model.tex:2–5` and `sections/03-exact.tex:19–34`.

The access section defines only unit normalization. Section 3 then introduces an “encoding with normalization `nu`” and uses the convention that its compressed block is `(I-H)/nu`. This standard convention is recoverable from the proof, but it is part of the claim and should be explicit for a standalone manuscript. Positivity is also needed: the proof of exact impossibility uses `2/nu>1`, which presumes `0<nu<2`.

**Repair:** Add that a normalization-`nu` exact encoding, with `nu>0`, satisfies `J_out^* V J_out=A/nu`, and state `0<nu<2` in the impossibility proposition. No additional approximation convention is needed for the current section, since its general-normalization statements are exact.

## Proof checks and source-note coverage

- **Implementation and oracle model:** The Hermitianization has compressed block `H` for every completion. Its walk has the displayed two-dimensional matrix, so the centered Laurent polynomial implements the desired spectral polynomial after compression. I checked the cited real-polynomial result against [Gilyén et al., Corollary 18](https://arxiv.org/pdf/1806.01838), and the arbitrary unit-circle polynomial result against [Motlagh–Wiebe, Corollary 5](https://arxiv.org/pdf/2308.01501). Both support the normalization and query-count uses here. For Hermitian inputs, a definite-parity singular-value transform agrees with the corresponding eigenvalue polynomial, including negative eigenvalues; the manuscript only needs the PSD case.
- **Exact support and the pairwise bound:** The quadratic factorization and its entire `[-1,1]` range are correct. The manuscript's error-aware complementary-norm estimates give the displayed positive lower-bound constant. The first source note's earlier argument displayed complementary amplitudes of the exact targets while announcing a nonzero approximation tolerance; replacing that argument with the present explicit error margins is appropriate. The manuscript also correctly explains that a local differentiated normalization bound cannot establish an attainable exact tradeoff below normalization two.
- **Threshold formula and asymptotics:** The exterior Chebyshev argument gives the lower bound, and the negative-lobe estimate suffices for global positivity of the proposed extremizer. Strict convexity establishes the unique stationary point. The large-order expansion gives the stated prefactor, and the bounded rounding term in the inverse threshold asymptotic is appropriate.
- **All-circuit lower bound:** A fixed scalar output amplitude is a trigonometric polynomial even with controlled calls and deferred bounded adaptivity. The interior derivative bound and Vandermonde compactness argument produce one coefficientwise limit valid at every fixed real point. Its global nonnegativity forces the even degree cutoff. This verifies the adaptive-hierarchy source note, including its vanishing-relative-error corollary and exact-interval impossibility.
- **Threshold equality and global contractivity:** The paired shifted kernels define an even algebraic polynomial. The tail exponent controls the growing nonnegative approximant outside the low interval. The extra low-band vanishing order at each positive-error contact absorbs leakage into the exact minimax slack. The signs in the final upper and lower error estimates are correct; no unallocated `o(delta)` overshoot remains.
- **Coarse tier:** The high-interval interpolation argument yields the logarithmic lower bound for every fixed `c<1`. The quartic pinned gate supplies an exact high-point zero when `c=1`, including `K=G_0`. This correctly repairs the source staircase's unqualified logarithmic coarse tier.
- **Definite parity:** The affine minimax value, explicit fourth-root lower-bound constant, odd-parity derivative bound, and squared endpoint-kernel construction check out. The comparison at `rho=2`, `K=1/32` is correctly limited to one definite-parity transform. The higher even-polynomial obstructions from the interval source note are retained; its elementary square-root lower bound is subsumed by the `r=0` case.

All substantive Stage 1 developments in the four source notes are retained or covered by stronger statements. The original ratio-two integrated-sign blend is replaced by the general even construction, so its separate formula is unnecessary. The strict-threshold unpinned construction is subsumed by the pinned equality construction. Source discussions of condition number, output-state overlap, normalization slack, and the scope of the parity separation remain represented. Priority claims and the fuller comparison with approximation-theory literature can wait for the planned introduction stage.

The current manuscript is mathematically standalone within its announced Stage 1 scope: proofs do not require another project manuscript or the research notes. The three minor repairs would make its domains and terminology fully explicit.
