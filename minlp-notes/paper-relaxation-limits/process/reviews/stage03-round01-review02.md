# Stage 3, round 1, independent review 02

**Verdict: PASS.** I found no demonstrable mathematical defect, missing required Stage 3 result, or incorrect central attribution in the frozen submission. The extra constants/algebra focus did not narrow the review.

## Coverage

I read the complete frozen versions of:

- `sections/04-incidence-interiority.tex`;
- `sections/05-feedback-frequency.tex`;
- `sections/06-treewidth-two.tex`;
- `sections/07-positive-boxes.tex`;
- `sections/08-exact-complexity.tex`;
- `sections/appendix-structural-auxiliary.tex`;
- `sections/appendix-positive-box-predecessors.tex`.

All paths above are under `process/snapshots/stage03-round01/`. I also inspected its `main.tex`, `macros.tex`, bibliography, and build record. Shared mathematical dependencies read and reconstructed were the envelope/vertex-law, common-upper, deficiency, independence, and box-transfer parts of `01-foundations.tex`; the exact dyadic construction and harmonic degree/dimension bounds in `02-universal-positive.tex`; and the elementary-symmetric envelope statement in the equal-means part of `03-cubic-equal-means.tex`. I read the positive-couplings appendix as background for the dyadic and harmonic alternatives. Unrelated accepted signed-bilinear and cubic extremal proofs are not required premises for the new Stage 3 proofs and were not independently re-audited in full.

I read the Stage 3 author assignment, review assignment and protocol, every Stage 3 scope row, the complete author source-to-label ledger, and `process/existing-idea-development.md`. I compared the submission with the canonical incidence, marginal, joint, feedback, frequency-two, cardinality, treewidth-two, arbitrary-factor, positive-box, lower-family, and single-product results. I also read the mapped asymmetric and symmetric predecessor notes, balanced-orientation closure, coefficient development, both unequal-box notes, both forest/compression and incidence investigations, width-three boundary, general-radix investigation, rational-power obstruction, and rank-one precision audit. I checked the relevant prior correction passages, including finite spreading in place of a derivative argument. I did not read another report from this round or spawn agents.

The ledger's additional scope is present: the later bipartite family approaching 3/2, signed arbitrary-box forest gluing, both auxiliary forest/compression lemmas, the forest-cover obstruction, asymmetric predecessor, failed all-high factor-two certificate, fixed-mixture optimality, and the completed coefficient-regularity refinement all have substantive proofs. Introductory integration belongs to Stage 6 and is not counted as a Stage 3 omission.

## Findings

None requiring correction. There are no major or minor finding IDs.

## Independent verification

### Incidence, radix, and marginal restrictions

For `thm:incidence-orientation`, the incoming variable-to-factor incidences of a high variable number at most r. Labeling them gives disjoint ownership in each round even when low anchors are shared. Consecutive arcs inside the anchor interval attain the capped owned sum; the extra failure mass outside it fits because q_i is at most one. Capped-sum subadditivity has the required direction when the rounds are averaged. The outgoing threshold law gives the stated s bound. The reduced-degree polynomial has deficiency no greater than the original polynomial under every law, so its hull gap is also no greater. This justifies adding the three polynomial-level estimates without assuming a stronger per-term conclusion from B(s+1). Empty incoming/outgoing sets and zero anchor means are covered.

For `thm:variable-radix`, integrating the capped first l−1 terms gives exactly (L−1)/b. The two resource profiles have the printed means, bracket one when b≥L, and attain the pointwise upper certificate even at l=0,1. Digit reversal gives all level hit counts simultaneously; coordinatewise modular shifts are transitive on the leaves for composite as well as prime radix. The elimination count is (j−1)+(L−j+1)=L, and the contracted K_(L,b) gives the reverse treewidth bound. Removing deepest degree-two factors before leaves establishes the stronger degeneracy result at L=k+1; orienting these factors outward establishes the stated orientation result. These do not incorrectly give treewidth k.

I separately reconstructed the general-radix completion. For q=s,s+1, the profile at level l is zero below q and b^(l−q+1) above it. Its mean is M_q, and both profiles attain the certificate sR+sum_(j≤l−s)b^j. Thus mixing them to mean one gives s+(L−s)b^(−s), not the simplified formula outside its range. The telescoping identity for the capacities and the fixed-b logarithmic conclusion have the correct constants.

For `thm:marginal-floor`, m_q≤q<1 makes completion valid and preserves the exact failure marginal. The clipped case really does give certain failure; the unclipped case gives the exponential union estimate. The substitution t=uz and division by u min(1,S/u) preserve the inequality direction. The lower integral estimate uses a lower bound on the linear term and an upper bound on the squared term, giving precisely the printed subtraction (Lambda−1)/(2 Lambda²). In the joint theorem, L≤phi(q) implies b≥(1−o(1))log q uniformly, so L/b tends to zero and all dimension, degree, treewidth, and two-sided marginal restrictions hold in the same construction. No fixed-small-width asymptotic is asserted.

### Feedback, frequency two, and algorithms

For `lem:feedback-repair`, a single favorable feedback-orientation pattern has mass 2^(−f_F) and realizes the minimum singleton event length. Both Q_F and Q_i therefore dominate the required local marginals. The residual rows sum to h_s, their total mass is 1−2^(−f_F), and conditional forest gluing preserves every repaired factor law. The physical-box proof uses a nonnegative deficiency on the original scope; it does not measure incidence after expansion. The flower identity AR+1_(R≥1)≤R+A gives H=1 and T=2−1/n as printed.

For `lem:degree-slab`, full column rank gives |J|≤|R|, while integer tight residual degrees and the two endpoints per fractional edge give 2|R|≤2|J|. Equality forces disjoint cycles and excludes fractional dummy edges. Even cycles have a null direction; odd cycles force halves. On a cycle of length l, matching/complement rounding gives coverage 1−1/(2l). Retaining b_v=1/2 at vulnerable vertices gives the factor 1−1/g after averaging. The convexity inequality E b_v(Z)≥b_v(p) is used in the correct direction.

For cardinality factors, adjacent-cardinality lower attainment is justified by integrality of the cube slab, and the secondary uncrossing objective rules out incomparable support sets. At a fractional-cycle vertex the rounding loss is exactly [phi(m)+phi(m+2)−2phi(m+1)]/(2l)=T_v(Z)/l. Concavity of local upper envelopes yields E T(Z)≤T(p), the direction needed in the global bound. Negative or nonmonotone convex sequences do not invalidate this reasoning.

I checked both binary-oracle reductions and their rational models. Negative edge costs can be fixed to one while retaining their endpoint vertices and zeroing their penalties. The hub/mate construction has the same optimum as prize-collecting edge cover. The two matching/cover inequalities establish equality of optimum values, despite possible duplicate cheapest completion edges. The cardinality gadget cannot have a singly activated coordinate when all mandatory endpoints are covered. Identical slot neighborhoods permit reassignment to the cheapest slots, and the bonus 2W+1 dominates every possible original-cost difference. The dual coefficient bound (n+1)!A is sufficient: a determinant expansion has at most (n+1)! terms, each containing one bounded right-hand-side entry. Clearing rational input denominators gives polynomial bit bounds. The claims concern scalar envelopes, not a compact full lifted formulation.

### Treewidth two and its boundaries

I checked every series terminal-type case and every parallel case in `thm:one-sided-coloring`. Series parity subtracts the shared factor once. Parallel parity subtracts the two shared terminals, contributing tau=1 exactly for mixed types. The even mixed component needed in the two conditional blocking cases cannot have a direct edge. In mixed parallel composition an active component and a blocking component prevent crossing monochromatic cycles; the direct-edge case correctly fixes odd parity. Distinct factor-terminal colors prevent every monochromatic terminal path. Block recoloring is consistent at factor articulation vertices.

The Camion application uses every Eulerian submatrix: its support decomposes into simple cycles, each with length divisible by four. The integer-slab argument consequently has TU, rather than only balancedness. The separately mentioned balanced proof is restricted to unit right-hand sides. Mixture deficiencies for general convex-cardinality factors are nonnegative in expectation, which is all the proof uses.

For fixed-aspect sharpness, the large product is epsilon^R with E R=1. The bilinear gaps sum to alpha, and the upper correction is (1−epsilon^n)/n. Splitting at R>M cancels the tail first moment between the two estimates; M=sqrt(n) gives H_n→alpha and ratio two. The parity example has local ranges [0,1], global range [0,1], and factorwise width three. The independent-set extension states maximum payoffs only, so it does not silently infer general width ratios. K_(3,m), the all-ones TU example, finite searches, the planar Hall orientation, canonical forest residual law, twin compression, and K_(2,m) forest-color barrier all have the asserted limited scopes.

### Positive boxes and complexity constants

For `lem:box-coefficient`, pairwise opposite probability is 1/beta_N under every restriction of the fixed ambient law. The j=2 identity leaves the sum of two nonnegative differences. Pascal identities for deterministic coordinates do not condition on their coins. Under global-extrema spreading, the decreases in beta C_j and C_(j−1) are −beta Bh and −Dh. The independent correction increases by at most Dh and the orientation correction by at most beta Bh. Their sum is nonpositive, so a nonnegative boundary value proves the interior inequality. The overflow order d+1 is necessary and correctly retained. Multiplication by the physical-product coefficients gives rho_B and beta_N as the two mixture weights.

For `thm:coefficient-regularity`, the shifted sum is sum_(j≥2) a_(j+1)(C_j−P_j); no condition on a_2/a_1 is needed because affine deficiencies vanish. Bounding this sum by L(C_psi−P_psi), then adding the latter deficiency once, gives L+1+beta_N. L=0 and deterministic coordinates are included. Positive affine transfer uses T_original≤T_expanded and common upper attainment, both with the correct direction.

I checked the symmetric predecessor's 4R+6+2/R, its value 45/2 at R=4, and the older 3+64=67 specialization. The high-mass lower estimate g(1)≥eta³/8 and the asymmetric denominator 1−3/sqrt(rho) are positive in their stated ranges. The asymmetric proof does not reuse the low-at-most-one-half orientation inequality after changing the cutoff. The fixed-mixture obstructions give w/2 and (1−w)/rho, intersecting at w=2/(rho+2); their scope is correctly restricted to a fixed fair-orientation/independence mixture.

The positive-box radix correction D_L has a single negative sign in both the exact termwise gap and softened-coverage identity. The upper and feasible-law lower hull estimates converge to the same epsilon alpha coefficient, and the lower estimate remains strictly positive at finite L. The rational 7/6 example has T=7/4 and H=3/2. The later epsilon family's two residual lists, affine lower values, common upper value, ratio, and unit-coefficient rescaling agree algebraically.

In `thm:single-product-hardness`, the expansion gives the stated variance coefficient epsilon²/2, and 2 epsilon³ A³=epsilon²/(8K). The YES/NO intervals are separated by q=b+epsilon²/4. The affine NO certificate and tilted oracle identity have the correct constant −epsilon² A²/8 and linear coefficients. The upper envelope exceeds q in every reduced graph-membership instance. The n+1 and n+2 support-size certificates have polynomial rational bit lengths. Delta=epsilon²/32 leaves strict separation and logarithmic accuracy length polynomial in the PARTITION encoding. Dummy factors preserve rank one and every relevant optimum. Neither strong hardness nor fixed-additive-error hardness is inferred. The rational-power secant formulas and first nonzero Taylor coefficients also check.

### Independent exact computations

I wrote `verification/reviewer02/stage03-round01/check_exact.py` independently of the author checkers and ran it successfully. Its saved output is `check_exact.json` in the same directory. All arithmetic is rational.

- 959 mean/support/ambient cases, covering N=2 through 7, support sizes zero through min(N,5), and nondecreasing means from {0,1/4,1/2,3/4,1}; 5,663 coefficient-order checks, including overflow orders and proper ambient restrictions.
- 359 finite global-extrema spreading checks and 2,877 coefficient-regularity checks with L=0,1/2,3.
- Exact reproduction of both arbitrary-spreading counterexample values and their difference 231/10000000.
- 290 radix pairs, b=2 through 11 and L=2 through 30, checking both profile means, all levelwise equality identities, the cutoff mixture value, and capacity telescoping.
- 560 binary vertices from all four-item multisets with entries in {1,2,3,4}, doubled before reduction, checking the remainder bound and tilted-square identity.
- The unequal-box lower affine inequalities at four exact epsilon values, including epsilon=2.

These finite checks support the analytic review; they do not establish universal inequalities or computational complexity classifications.

### Direct classical-source checks

I read `literature/AGENTS.md` before local original use. Relevant source statements were inspected directly, in addition to reading the coordinator's and author's records:

- Cornuejols's original manuscript, printed pp.76 and 82, Theorems 6.5 and 6.13. I visually checked the Camion statement and read the mixed-integrality statement with its right-hand sides. [Original manuscript](https://www.andrew.cmu.edu/user/gc0v/webpub/notes.pdf).
- Hassin–Tamir's original scan, printed p.381, Theorem 3.1 and terminal constructions, visually inspected. It supplies the classical block decomposition, not the manuscript's coloring invariant. [Author scan](https://www.math.tau.ac.il/~hassin/sp.pdf).
- Barrus, Theorem 2.1 and surrounding fixed-degree setup: the graphic-list scope and the classical fractional-matching attribution agree with the manuscript's qualified comparison. [Original article](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i2p18/pdf).
- Edmonds's original weighted-matching statement and algorithm discussion, and Deza–Onn's Theorem 1.2 and Section 3 proof. [Edmonds original](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p125_A1b.pdf), [Deza–Onn author manuscript](https://arxiv.org/html/1908.09278v1).
- GLS first edition, Definition 6.2.2 and Theorem 6.4.9 with the separation-to-optimization proof, from the downloaded original's text. This is strong rational oracle equivalence for well-described polyhedra. [Author-hosted original](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf).
- Sherali's equation (13) and Theorem 3, printed pp.252–253, visually checked; Adams–Gupte–Xu Proposition 4.1, manuscript p.22, visually checked; Del Pia–Khajavirad Theorem 7 and its proof in the local primary text. These confirm the particular classical envelope and forest antecedents used, without extending them to sparse arbitrary factors. [Sherali original](https://math.ac.vn/uploads/files/9701245.pdf), [Adams–Gupte–Xu manuscript](https://www.pure.ed.ac.uk/ws/files/137020380/1704.00424.pdf), [Del Pia–Khajavirad article](https://doi.org/10.1137/16M1095998).
- Karp's authorized reprint, original printed pp.94 and 97, visually checked for the completeness statement and PARTITION definition. Passing from signed entries to absolute values and omitting zeros preserves the signed-sum partition question. [Authorized reprint](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf).
- Altschuler–Boix-Adsera, Section 2 encoding convention and Section 7.2 historical accuracy question, including visual inspection of the page containing Theorem 7.4 and Corollary 7.5. The rational-bit limitation in the manuscript is appropriate to this comparison. [Published article](https://link.springer.com/article/10.1007/s10107-022-01868-7).

## Remaining limits

This is a proof and coverage review, not exhaustive priority certification. I did not reconstruct the full classical weighted-matching algorithm, the full GLS oracle-equivalence development, or every source theorem cited in accepted earlier stages. The Deza–Onn publisher full-text endpoint returned 403; its primary author manuscript was readable, and publisher-indexed metadata confirmed the bibliography. No new Stage 3 proof depends on an inaccessible nonclassical result.

I inspected the frozen build record, which reports a successful 62-page build without warnings or duplicate labels; I did not independently rebuild or audit every rendered page. The manuscript's retained open problems—exact W_k for k≥3, wider matrix partitions, sharp planar and finite-aspect constants, and unequal-aspect bipartite supremum in [3/2,2]—are not defects. Fixed-mixture optimality and finite searches are not promoted to those stronger conclusions.
