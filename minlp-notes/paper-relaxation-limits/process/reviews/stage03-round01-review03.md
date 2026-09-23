# Stage 3, round 1, independent review 03

- **Verdict:** MINOR. No major defect found in the Stage 3 mathematical arguments. One local convention conflict should be clarified.
- **Input:** frozen `process/snapshots/stage03-round01/`.
- **Reviewer emphasis:** boundary cases, zero gaps, empty supports and degenerate parameters. The review covered the complete stage.

## Coverage

I read all five new main files and both new appendices in the frozen snapshot:

- `sections/04-incidence-interiority.tex`
- `sections/05-feedback-frequency.tex`
- `sections/06-treewidth-two.tex`
- `sections/07-positive-boxes.tex`
- `sections/08-exact-complexity.tex`
- `sections/appendix-structural-auxiliary.tex`
- `sections/appendix-positive-box-predecessors.tex`

I checked the shared vertex-law, deficiency, affine-invariance and nonnegative-box-transfer foundations in `sections/01-foundations.tex`, and read the used universal degree/dimension, harmonic-law and exact dyadic results in `sections/02-universal-positive.tex`. I also inspected the macros and bibliography. The signed-bilinear and cubic material is not a new proof dependency of this stage. Introduction and abstract integration remains Stage 6.

I read the review assignment/protocol, Stage 3 author assignment, Stage 3 scope table, and author source-to-label ledger, including the linked additions. I compared the manuscript with the canonical incidence, radix, marginal-floor, joint, feedback, frequency-two, cardinality, treewidth-two, parity, positive-box and single-product-hardness result files. I also inspected the predecessor, balanced-orientation closure, coefficient-regularity, unequal-box investigation, canonical-pair/compression, width-three, second-order radix and rational-power notes listed in that ledger. Superseded constants and stale open statements in those source notes are correctly reconciled in the frozen manuscript. I did not read another report from this review round or use another review as a theorem input.

Primary-source checks were independent of the author’s inspection claims. After reading `../literature/AGENTS.md`, I inspected:

- Cornuéjols’s original Theorems 6.5 and 6.13, including the displayed rectangular Eulerian criterion and the mixed unit-right-hand-side integrality statement; I visually checked the former on printed p.76.
- Hassin–Tamir’s original printed p.381, visually checking Theorem 3.1 and the terminal series/parallel framework. The manuscript supplies its own additional coloring invariant.
- Barrus’s original Theorem 2.1 and the rank/cycle proof passage. Its graphic fixed-degree setting is narrower than the manuscript’s slab lemma, which is proved locally. [Original paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i2p18/pdf).
- Edmonds’s original abstract and Section 1 weighted-matching statement. [Original paper](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p125_A1b.pdf).
- Deza–Onn’s Theorem 1.2 and Section 3 incremental matching proof. Its attribution is appropriate; the manuscript explicitly proves the extra signed-cost/private/parallel-edge details. [Original manuscript](https://arxiv.org/html/1908.09278v1).
- GLS Theorem 6.4.9 in the downloaded original, at its stated well-described-rational-polyhedron scope.
- Sherali’s elementary-symmetric-envelope section and Theorem 3; Adams–Gupte–Xu’s Proposition 4.1 and proof, with the latter’s common-aspect formulas visually checked on printed p.22; Del Pia–Khajavirad’s Theorem 7 and forest exactness proof.
- Karp’s authorized reprint, visually checking original printed pp.94 and 97: completeness of the listed problems and the PARTITION definition. Its signed-integer formulation reduces to positive integers by absolute values and omission of zeros, using the equivalent zero signed-sum condition.
- Altschuler–Boix-Adserà’s rational-entry convention and the Section 7.2 accuracy question; I visually checked the original page containing Theorem 7.4, the following question and Corollary 7.5. The paper’s bit-model and accuracy qualifications are retained.

The coordinator/author source records were read as access and scope records. They were not substituted for the inspected passages above. I did not independently reprove the general weighted-matching or GLS oracle-equivalence algorithms.

## Findings

### R03-01 — MINOR: explicitly retain zero-weight factor vertices in the independent-set graph statement

**Location:** `sections/06-treewidth-two.tex:226–248`, especially line 233 (`prop:independent-payoffs`), together with `sections/04-incidence-interiority.tex:14–15`.

The proposition allows nonnegative vertex weights and states that the constructed incidence treewidth equals `max{2,tw(G)}` whenever `G` has an edge. Its graph proof correctly applies to the construction retaining one factor vertex per vertex of `G`, including zero-weight factors. However, the stage-wide convention discards affine factors before measuring structural parameters unless their retention is explicit. A zero-weight payoff is identically zero and therefore affine.

For example, take `G=K_2` with weights `(1,0)`. After the stated affine-factor deletion, the surviving equality/inequality payoff has two variables and one factor; its incidence graph is a tree of width one. Retaining the zero-weight factor instead gives the intended four-cycle and width two. The payoff identities and the positive-weight sharp examples are unaffected.

**Repair:** insert “For the incidence graph retaining all constructed factor vertices, including zero-weight factors, …” before the width equality. Alternatively impose strictly positive weights for that particular graph statement. This is a local convention clarification; no central gap bound or lower example needs to change.

## Independent verification

### Incidence and marginal laws

The ownership law is globally compatible because each high coordinate has at most one owner in each round; sharing a low anchor does not create a second assignment of any high coordinate. Incoming and outgoing zero parameters are correctly omitted. Empty outgoing scopes have zero gap and the reduced-degree polynomial only requires a polynomial-level bound. The statements never divide by a zero deficiency.

For general radix, I reconstructed the capped affine certificate and both count profiles. The cutoff exists because `M_1>1` and `M_L=b^(1-L)<1`; strict decrease makes the mixture denominator positive. At cutoff equality the mixture is allowed to put all mass on one profile. Both profiles have counts between zero and `b^L`, preserve all anchor means, and attain the affine certificate at every level. Coordinatewise digit shifts are valid for composite radices. The elimination order and the `K_(L,b)` clique-minor construction prove exactly the stated width range; the stronger degeneracy/orientation examples only use `k>=2`, as required by the deepest factor’s degree two.

The marginal completion has `m_q<=q<1`, so its denominator remains positive, including `q=0`. Clipping is correctly separated in the exponential union estimate. The lower integral estimate uses the shifted denominator in its positive term and the unshifted denominator for the negative quadratic remainder, with the correct directions. In the joint lower construction, the floors lose a vanishing relative amount when the stated minimum parameter diverges; `m+L<=q` and the two-sided marginal strip hold eventually. The text makes no fixed-small-width asymptotic claim.

### Feedback, frequency and algorithms

I checked the feedback reference law entrywise, the residual normalization, empty outside scopes, empty feedback set and null conditioning states. The gluing incurs one domination factor, and the physical-product affine majorant stays on each original factor scope. The flower’s pointwise inequality and exact attaining law give the printed values, including `n=2`.

In the slab lemma the two rank/incidence inequalities force every fractional edge to meet two tight rows and every such row to have fractional degree two. This excludes parallel fractional two-cycles and private dummy edges. The odd-cycle law retains the coverage baseline after averaging; the cardinality version loses exactly the local curvature gap divided by cycle length. Empty scopes and affine tables have zero local gaps, and negative/decreasing convex tables are permitted without changing the argument.

I reconstructed both binary-oracle reductions. Including negative-cost coverage edges before the edge-cover reduction is valid; the hub handles isolated remaining vertices. A minimal nonnegative edge cover is a star forest, so the matching formula has both required directions. The cardinality gadget’s mandatory-pair alternatives are exhaustive, and its bonus `2W+1` exceeds every possible unmodified cost difference. The dual coordinate bound follows from a nonsingular `(n+1)`-row zero-one system; it has polynomial bit length and preserves an optimum even at boundary means or when all objective coefficients vanish. Scalar-envelope separation is the justified conclusion.

### Treewidth and auxiliary reductions

I checked the active/blocking invariant through all seven series cases and every parallel terminal type. The parity correction counts a shared factor once in series and both factor terminals appropriately in parallel. A direct terminal edge is mixed and fixes odd active parity; simplicity prevents both parallel components from containing it. Block color swaps are sufficient at factor articulations. An Eulerian submatrix’s cycle decomposition then makes its number of ones divisible by four, giving the claimed TU conclusion through Camion. The balanced alternative is correctly limited to the unit-right-hand-side monomial argument.

For the positive-aspect flower, `1-epsilon^r<=alpha*r` and the tail split at `M=sqrt(n)` give the stated limiting hull gap; `alpha>0` is fixed. The parity example has the exact local and global minima needed for a width ratio. The independent-set extension claims only maxima. The forest residual law `2Q-P` preserves singleton marginals and retains the union baseline, including an empty target. Twin compression works at `w=0`, at deterministic means and with empty outside scope; adding the same nonnegative increment to both widths transfers inequalities without division.

### Positive boxes and complexity

The finite coefficient induction handles orders zero, one and above the support size separately. Deleting a deterministic coordinate restricts the same ambient orientation law; it never conditions or resamples coins. In the interior step the common-threshold changes are exact even at ties, the independent-moment change is bounded by Pascal’s identity, and the orientation Lipschitz bound works without independent coins. Summing with `a_(j+1)<=L*a_j` gives the candidate `L+1+beta_N` bound, including `L=0`, with entire factors retained. Unequal-box transfer uses nonnegative affine expansion and common upper attainment, not box inclusion.

The coarse and asymmetric predecessor proofs cover empty low/high groups and both mass regimes. Their constants and fixed-mixture limits check algebraically. The positive-box lower family’s correction is bounded and its displayed lower hull estimate is strictly positive for every finite `L`. The later unequal-box family has nonnegative residuals throughout `0<epsilon<=2`, with exact equality restored at `epsilon=2` and no claim at the excluded zero endpoint.

The PARTITION expansion has a uniformly nonnegative remainder bounded by `epsilon^2/8`; the NO variance lower bound uses the integer half-total correctly after doubling. The rational certificate sizes follow from basic solutions and polynomial-bit vertex products. The graph-hull reduction separately checks its upper endpoint. The tilted-square identity gives the claimed `epsilon^2/32` separation with polynomial logarithmic precision, including the stated randomized assumption and padding. It does not imply fixed-additive-error hardness or strong NP-hardness. The rational-power example’s strict curvature and two Taylor orders give the stated divergence, while the logarithmic coordinate change makes the two convex secants add.

### Exact finite checks and build

I wrote and ran `verification/reviewer03/stage03-round01/check_boundaries.py`, independently of the author’s checkers. Its saved JSON records:

- 1,812 exact coefficient vectors for ambient dimensions 2–5 and all support sizes, including empty/proper supports and means in `{0,1/3,1/2,1}`;
- 5,436 corresponding coefficient-regularity cases with `L` in `{0,1,2}`;
- both printed arbitrary-spreading counterexample values;
- 77 general-radix profile/cutoff/telescoping checks, for `b=2,…,8` and `L=2,…,12`;
- all 64 parity assignments and 32 unequal-box residual vertices at four rational parameters including `epsilon=2`.

All arithmetic in that checker is exact integer/Fraction arithmetic. It tests the formulas and boundary implementation on finite sets; it does not prove universal inequalities or replace the written induction.

An isolated `latexmk -pdf -interaction=nonstopmode -halt-on-error` build of the frozen main file completed successfully, producing a 62-page PDF under the assigned verification directory. The final log has no undefined references/citations or overfull boxes; it contains one underfull-box warning. No manuscript or literature package was edited.

## Remaining limits

The review does not establish publication priority or rule out later antecedents. The standard general matching and oracle-equivalence inputs remain cited classical results, rather than newly reproved algorithms. I did not rerun the exploratory width-three searches or treat their finite counts as universal statements. I did not perform a full page-by-page visual layout audit of the 62-page cumulative manuscript.

The stated open boundaries remain open: exact `W_k` for `k>=3`, larger-width balanced/TU partitions, sharp planar constants, the finite-aspect-ratio optimum and the unequal-aspect bipartite supremum in `[3/2,2]`. None is promoted by the text to a proved theorem. Later-stage content and introduction/abstract integration are outside this review’s omission assessment.
