# Stage 1 round 1 — independent review 08

**Verdict: MINOR.** The bilinear theorems and the envelope foundations are sound. One local qualification is needed in the spatial-certificate convention. No major defect found.

## Coverage

Read all frozen manuscript inputs under `process/snapshots/stage01-round01/`: `main.tex`, `macros.tex`, `sections/01-foundations.tex`, and `references.bib`. Read `process/review-protocol.md`, `process/stage-01-review-assignment.md`, `process/stage-01-author.md`, and the Stage 1 scope and shared notation in `process/scope-proposal.md`. Read both canonical bilinear result files in full and `results/positive-multilinear-degree-upper-bound.md`, including the foundational deficiency, independent-rounding, and box-transfer arguments. Existing review labels were not used as evidence. No other current-round review was read.

Following `literature/AGENTS.md`, checked relevant local primary-source passages:

- `[[luedtke2012-some-results-on-the-strength]] p.7-10`: recursive-product scope, vertex representation, and Theorems 4–5 on common upper envelopes; also checked its Theorem 8 statement and coloring argument in the extracted text. Inspected original PDF p.9 for the nonnegative expansion argument.
- `[[boland2017-bounding-the-gap-between-the]] p.3`, `p.6`, and `p.10-11`: the 600 sqrt(n) bound, induced-cut upper implication, and signed-cycle exactness. Inspected original PDF p.6 for Corollary 1 and its normalization.
- `[[davidson2007-norms-of-schur-multipliers]] p.3-7`: norm conventions and Theorems 1.2 and 2.4. Inspected original PDF pp.4, 6, and 7, because extraction omits important displayed formulas.
- `[[mccormick1976-computability-of-global-solutions-to]] p.1-3`: the historical factorable-underestimator and subdivision attribution.

Szarek's original proof was not available in a local package. The exact real Rademacher inequality and its attribution were checked against equation (1) of the primary research article [Eskenazis–Nayar–Tkocz, *Distributional stability of the Szarek and Ball inequalities*](https://arxiv.org/html/2301.09380v2). The sharp Khinchin theorem, Grothendieck theorem, and max-flow/min-cut theorem remain established external inputs, as declared in the manuscript.

## Findings

1. **R08-1 — MINOR: qualify relative-target incumbent monotonicity.** Location: frozen `sections/01-foundations.tex`, lines 180–183, especially “A size lower bound may grant the best incumbent U=f*: worse incumbents require weakly higher targets.” The preceding relative convention assumes only U>0 and does not constrain theta. The relative target has derivative 1-theta with respect to U. For theta=2, f*=1, and feasible incumbent U=2, the worse incumbent has target -2, which is lower than the best-incumbent target -1. Moreover, the assumptions permit f*<=0, when setting U=f* leaves the stated U>0 relative convention. These omissions do not affect any Stage 1 gap theorem or an asserted spatial lower-bound theorem, so I classify this as a local convention repair. **Repair:** explicitly take epsilon>=0 and 0<=theta<=1 (or the usual 0<theta<1), and say that the best-incumbent simplification applies without qualification to absolute certificates and applies to this relative convention when f*>0.

## Independent verification

### Envelope and domain checks

The independent endpoint law expresses each multiaffine graph point as a convex combination of vertex graph points. Compactness of the finite distribution polytope gives actual extrema; the finite polyhedral representation also justifies boundary continuity. The termwise comparison uses a common x and exact factor hulls, so its direction is T>=H. Affine summands shift both envelopes equally.

For a support anchored at a smallest mean u, subtracting max(0,u-S) from u gives min(u,S). Thus the deficiency identity is exact, including u=0, S=0, ties for the minimum, and zero coefficients. A single threshold law gives all upper expectations simultaneously. The independent-rounding estimates use only S>=0 and the indicated low/high cases; they do not substitute separately optimal factor laws for a common law.

On a nonnegative box, expansion preserves nonnegative coefficients and the maximum monomial degree. Convexifying an original factor is at least as strong as summing hulls of its expanded factors, so T_original<=T_expanded is the correct inequality. Expansion can change incidence, and the manuscript explicitly avoids transferring incidence claims. For bilinear factors, positive interval widths simply rescale coefficients and fixed coordinates turn incident products into affine terms. Thus the upper bounds are uniform over finite boxes, with no hidden lower bound on interval widths or coefficient magnitudes.

### Induced cuts and graph parameters

At a half-valued face, the symmetric law on s and -s enforces zero sign means while attaining either extreme of the quadratic character sum. Consequently H=R_W/2 and T=L_W/2. Fixing outside coordinates to one adds affine terms and does not alter this conclusion. Orthogonality of distinct degree-two characters ensures R_W>0 whenever L_W>0.

For the extension away from the grid, a component of active coordinate/complement relations either has a fixed coordinate, has an odd-complement cycle forcing one-half, or has a local free parameter. In the last case sufficiently small perturbations preserve inactive strict inequalities too, so it cannot define a cell vertex. The gap H is concave; hence T-cH is convex on each cell. This proves the all-point comparison, including points where H=0, from the finite vertex comparisons.

Polarization gives Q(s)-Q(t)=2 v^T A u for disjoint complementary supports. The squared-weight locally maximal cut ensures at least half of each row's squared mass crosses. Applying the two Khinchin row estimates and then max(X,Y)>=(X+Y)/2 gives R>=sum_i ||a_i||_2/4. The flow cut capacity m-|E(U)|+t|U| proves the exact fractional load threshold rho. Weighted Cauchy–Schwarz then gives L<=sqrt(rho) sum_i ||a_i||_2. The maximum-degree and inherited-bipartition versions count each edge with the stated factors. Density, degeneracy, maximum degree, and the two part degrees are monotone under induced restriction; their use in the pointwise theorem is valid.

### Quantifiers, support, and asymptotics

The random-sign estimate is finite for every graph with an edge. There are 2^(h-1) representatives after global sign reversal and two exponential tails, yielding h log(2), and minimization in lambda gives sqrt(2mh log(2)). Independence is needed only across edge signs. Extending the densest induced signing arbitrarily to other edges preserves the face witness. Thus the lower bound has full support already and holds on each individual graph; it does not assert a lower bound for every coefficient vector.

For the center supremum C, zeroing edges outside an induced subgraph converts each induced ratio into a whole-graph ratio. Therefore Gamma=C. On L_V=1, R_V is continuous and strictly positive on a compact set, so the center supremum is an attained maximum. Perturbing zeros gives convergence of the center ratio and proves equality of the full-support supremum without assuming continuity of c*. This distinction is necessary: take a disjoint unit edge and a frustrated four-cycle with all cycle magnitudes epsilon. For every epsilon>0, c*=2, while at epsilon=0, c*=1. The center ratio is (1+4 epsilon)/(1+2 epsilon), which is continuous. The manuscript correctly avoids the false continuity step.

The graph-family characterization requires no closure assumption because its witnesses are induced faces inside the original graphs. The attached-leaf example has 2q^2 edges and q^2+2q vertices while retaining density at least q/2. Uniform scaling cancels from ratios, so the warning against unnormalized weighted density is valid. The positive complete-graph example tends to two and correctly distinguishes worst-over-signs growth from every-vector growth. The frustrated four-cycle supplies finite-parameter constants, and the text does not misuse it as a growing-density asymptotic witness.

### Exactness and the older norm transfer

R_V=L_V requires simultaneous attainment of the largest possible positive cut weight and smallest possible negative cut weight. With nonzero supported coefficients, this means the positive and negative edge sets are each cuts. The cycle-parity criterion characterizes precisely that property and is inherited by induced graphs. The nonempty-forest conclusion is correctly qualified.

For the symmetric pattern, each edge contributes at most one rectangle entry unless both endpoints lie in R intersect C. This proves beta<=rho; choosing R=C as a densest subset gives equality. The source's continuous weighted Theorem 2.4 gives 2 sqrt(beta), whereas Theorem 2.3 alone would introduce rounding. The real projective inequality in Theorem 1.2 has the direction used in the manuscript. Pairing with sign(A) gives 2L; decoupling gives ||A||_(infinity->1)<=4R; the resulting transfer is L<=4 K_G sqrt(rho) R. The Sidon comparison follows from the zero mean of Q and becomes equality in the bipartite case because its range is symmetric. These statements substantiate the limited historical claim actually made.

### Exact finite checker

`verification/reviewer08/check_quantifiers.py` passed with Python's exact integer and rational arithmetic. It checks all 729 coefficient vectors in {-1,0,1} on the six possible K4 edges for polarization, rectangle-density equality, positivity for nonzero support, and the squared density inequality. It also checks the support-discontinuity example for epsilon in {1,1/10,1/100,0} by enumerating induced ratios, and the relative-target counterexample above. Output: `PASS: 729 exact K4 coefficient cases; 4 rational support-limit cases; target counterexample.` These checks supplement the derivations; they do not establish universal theorems. Source-page images inspected during this review are retained in the same directory.

## Remaining limits

I did not reprove the established sharp Khinchin or Grothendieck theorems, resolve the Davidson–Donsig publication-page discrepancy, run a new broad priority search, or independently rebuild the PDF. None is needed to verify a new asymptotic claim beyond those actually stated. This review does not cover unwritten future stages. The best universal density constant and its growing-density counterpart remain distinct open questions, correctly left unresolved here.
