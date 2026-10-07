# Stage 5, round 1 — independent reviewer 07

- **Verdict:** PASS.
- **Findings:** None. No major or minor repair is required on the evidence reviewed.
- **Focus:** The new order-one upper certificate, especially the quadratic identity and the distinction between graph equations on moments and graph support of a realizing distribution. This focus did not narrow the full-stage review.

## Coverage and access account

I read the complete frozen files `process/snapshots/stage05-round01/sections/13-xor-quadratic-hulls.tex` (333 lines), `14-monomial-reformulations.tex` (228 lines), and `15-finite-certificates-affine.tex` (218 lines). I checked the frozen notation in `macros.tex`, the four new bibliography entries, and the dependencies in `sections/01-foundations.tex` through its certificate-model subsection (lines 1–194), all of `11-coordinate-domains-lifts.tex`, and all of `12-relative-blocks-cuts.tex`. The new arguments do not invoke the earlier fractional-cardinality positivity theorem; I did not re-review its full proof or unrelated earlier gap chapters. There are no new Stage 5 appendix proofs to review.

I read `process/review-protocol.md`, `process/stage-05-review-assignment.md`, `process/stage-05-author-assignment.md`, the complete author ledger `process/stage-05-author.md`, focus 07 in `process/stage05-reviewer-focus.json`, the order-one candidate `process/order-one-monomial-refinement.md`, and the scope proposal's stage, notation, dependency, and Stage 5 coverage requirements. I checked the frozen primary-source record. I did not read other reports from this round, delegate work, or edit manuscript files. Previous audit verdicts were not used as proof.

I read all three canonical sources and every mapped correction/audit source, relative to the repository root:

- `results/spatial-bb-quadratic-cut-exponential-lower-bound.md`;
- `results/spatial-bb-monomial-lift-exponential-lower-bound.md`;
- `notes/spatial-bb-affine-branching-barrier.md`;
- `notes/review-spatial-bb-beyond-clique.md`;
- `notes/review-spatial-bb-beyond-clique-second.md`;
- `notes/review-spatial-bb-bounded-monomial-lift.md`;
- `notes/review-spatial-bb-affine-branching-barrier.md`.

I read `literature/AGENTS.md` before accessing originals. All four primary originals listed in `verification/stage05-primary-sources.json` were accessible. I extracted their text independently into my verification directory and verified that their SHA-256 digests equal the ledger's recorded digests. I also opened the author URL and explicit arXiv version pages. Source inspection was as follows:

- [Schoenebeck, author full version](https://schoeneb.people.si.umich.edu/papers/LasserreNew.pdf): read the complete mathematical text, including the sampling definition, Theorems 11–12, the entire signed-character construction of Lemma 13, and the appendix width argument. Visually inspected printed pages 7, 8, 10, and 11 from the original. The width rule bounds the resulting support; the signed Gram construction supplies the required positivity. The printed norm-zero sentence on page 10 is inconsistent with the immediately displayed unit constant vector. The manuscript correctly uses normalization and does not import that typo. Theorem 11 supplies a positive constant; choosing gamma=1/4 avoids the three-variable boundary denominator.
- [Ahmadi–Dash–Hua–Stellato, arXiv 2605.28674v1](https://arxiv.org/abs/2605.28674v1): read the introduction, Definitions 1–2, Theorem 1 and its surrounding scope, the simplicial/copositivity discussion adjoining Section 6, Sections 6.1–6.2's regions, lower-bound oracles and termination statements, and the conclusions. Visually inspected printed page 32. The manuscript's limited comparison is supported. I did not independently prove every theorem or audit the numerical experiments in this paper.
- [Beame et al., arXiv 1710.03219v3](https://arxiv.org/abs/1710.03219v3): read the abstract and introduction through its result statements; visually inspected PDF page 4, printed page 3. The integer-negation disjunction and quasipolynomial Tseitin statement match the manuscript. I did not reprove the full simulation or refutation constructions.
- [Fleming et al., arXiv 2102.05019v2](https://arxiv.org/abs/2102.05019v2): read the abstract and introduction through Theorems 1.1–1.5; visually inspected PDF page 5, printed page 4. Theorem 1.3 concerns a CNF encoding, and Theorem 1.4 concerns SP* with coefficient restrictions. Both qualifications are preserved. I did not independently audit their full proofs.

No original was changed. Initial rendering attempts with `fitz` failed because the module was absent in both Python environments tried; rendering with `pdftoppm` succeeded. There is no unresolved source-access failure. Earlier literature supporting accepted dependency sections was not re-audited except where its relevant elementary argument is supplied in the frozen text.

## Independent reconstruction

**Unlifted transfer and local oracle — section 13, lines 26–156.** The functional fixes excluded Boolean endpoints deterministically and uses the remaining marginal. It does not condition on a possibly zero-mass event. An allowed term with generator-degree sum a and square multiplier degree d has a+2d<=2r. Endpoint expansion gives nonnegative coefficients times assignment indicators I; repeated or conflicting factors remain covered. The square (IP)^2 has degree at most 2(a+d)<=4r. Local equalities vanish after Boolean reduction within the same budget. Marginalizing the genuine quadratic Boolean law and fixing the restricted coordinates reproduces every first, diagonal, and cross moment, with finite support in the actual domain. This proves the stronger nonclosed-set hull membership as written.

At most Delta|R| clauses change, each substituted cost is in [0,1], and thus LB<=Delta|R|/m. A witness-containing domain has exactly 2^(n-|R|) Boolean witnesses. The reciprocal union bound applies to overlapping covers and charges discarded certified regions. It does not imply a lower bound after free deletion. The precise linear use of full-box quadratic inequalities is maintained throughout.

**Signed law, source width, and existence — section 13, lines 158–313.** Unit Gram vectors with entries 0 or signs divide into orthogonal signed classes. Fixing the constant class to one and independently randomizing other classes gives all prescribed first and second moments, including nonzero means. In the width construction, I~J is transitive because the resulting I symmetric-difference K has size at most 2 floor(w/2)<=w. Consistent signs give a Gram representation for arbitrary polynomial squares. Defining moments directly through w also handles odd top degree; no unsupported split into two half-width supports is needed. The required source widths are 4r and 4rD.

For each assignment the random violation count is Bin(8n,1/2). The displayed exponential-moment bound at t=1 is exp(-n), and multiplication by 2^n tends to zero. The occurrence generating-function derivative gives 48(1+3/n)^(8n-1); its stated tail estimate is valid, as is the stronger elementary integer check using e<3. Markov plus the two vanishing failure probabilities yields existence for every sufficiently large n without independence between events. Deletion retains 7n<=m<=8n, Delta<=64 and at least n violations, so OPT>=1/8. Absolute 1/16 and relative 1/2 both require target at least 1/16 even with the best incumbent, yielding exponent 7n/1024. Restriction of one source functional proves simultaneous orders. The derivative/Hessian bounds at lines 315–333 correctly count two mixed derivatives per incident clause.

**Lifted transfer and order one — section 14, lines 7–168.** Every available lifted polynomial pulls back through degree 2rD. Each parity-indicator product has degree at most Da, remains idempotent despite dependencies or inconsistent factors, and gives square degree at most 2D(a+d)<=4rD. All allowed multiplied graph identities vanish as literal polynomials; Boolean-only objective agreement would not suffice. The lifted augmented matrix is PSD because a linear form pulls back through degree D, and each entry is a signed character of degree at most 2D. Its signed-law realization is inside the full coordinate domain: an endpoint mean fixes each restricted coordinate almost surely. It need not lie on the nonlinear graph.

The affected-clause cost estimate is available since a character of degree at most three is within the source square-polynomial budget 2rD>=4. No step secretly uses r>=2. Thus r>=1, rD>=2 and an available objective are sufficient. The unlifted cubic still needs r>=2. With C the restricted-support union, LB<=Delta|C|/m. A basis chosen from the restricted incidence rows has the same support union as all rows, so |C|<=D rank. Its consistent signed fiber has exactly 2^(n-rank) witnesses. This proves the count with arbitrary numbers of repeated auxiliaries.

**Formulation and asymptotics — section 14, lines 170–228.** The two equations per clause determine the exact continuous graph. D=3, N=n+2m<=17n, source width 12r, exponent 7n/3072 and its N-form 7N/52224 are correct. Taking logarithms gives the stated necessary D=Omega(n/log n) only within 4rD<=an. The text appropriately measures a general lift in original n and does not transfer the earlier coordinatewise interpolation argument to multivariable auxiliaries.

**Both upper certificates — section 15, lines 9–118.** For every epsilon>0, M=ceil(3/epsilon)>=1 and h=2/M<=2epsilon/3. This includes epsilon>=3. The eight-corner interpolation has nonnegative corner-minus-minimum coefficients and degree-three products of bound slacks. Order two supplies it, and the separate cubic graph identity transfers the certificate with total degree three. Averaging individual clause minima gives at least F(a)-3h/2>=OPT-epsilon.

For the new order-one proof, define e1=u-x_i x_j and e2=v-u x_k. On the entire lifted box, |u(x_k-a_k)|<=h and |a_k(x_i x_j-a_i a_j)|<=2h. Therefore the displayed quadratic q is nonnegative there for either sign, and direct expansion gives

```
Phi_clause-c_clause(a)+3h/2 = q - (b_clause/2)(e2+a_k e1).
```

Every term has lifted degree at most two. Applying its valid quadratic inequality linearly and the two equality moments proves the target for every feasible node functional and hence its infimum. The probabilistic proof is the same argument using actual first/second moments, without graph support or cubic moments. The lower corner maps to a feasible original graph point, so F(a)>=OPT. Leaving all auxiliaries unpartitioned still covers the full graph with M^n regions. At epsilon=1/16 this is 48^n and suffices for relative tolerance 1/2 in the stated family.

**Affine boundary — section 15, lines 120–218.** A nonnegative random S with mean zero must vanish almost surely, contradicting the preserved second moment n; the normalized z inequality yields the same obstruction. Symmetry retains at least half of the witnesses, including even-n boundary mass. If t<r-1 and t<ceil(n/2), then n-t>=t+1. The negative-assignment indicator on a+1 free coordinates has degree <=r-1 and gives exactly -2^(-(a+1)); r=1 is correctly vacuous. These prove a method obstruction, not an affine upper certificate for the XOR family. An unsatisfiability refutation supplies only the direct normalized 1/m bound; multiaffinity carries that Boolean bound to the continuous cube but does not turn it into 1/16. The literature comparison preserves the differences in thresholds, regions and oracles.

## Independent verification artifacts

All new check artifacts are under `verification/reviewer07/stage05-round01/`.

- `check.py` and `check.json`: successful run with `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python verification/reviewer07/stage05-round01/check.py`. All arithmetic is symbolic or exact rational. Checks include the quadratic identity and its degree, the distinct cubic graph identity, the full Bernstein identity, the deletion integer inequality, and the three exponents/base 48.
- The checker verifies nonnegativity of q in 108,000 signed vertex cases over 3,375 boxes, including singleton and unequal-width coordinates. This is finite corroboration; the universal full-box proof is the triangle inequality above.
- Four explicit exact two-atom laws test the essential graph-support distinction. For t in {1/32,1/8,1/2,1}, take x_i=x_j=0, (x_k,u)=(-t,-1) or (t,1) equally, and v=t. Both graph residuals have expectation zero, although every atom violates the first graph equation. The clause-cost mean is (1-t)/2, strictly below the graph minimum 1/2 on this node, while satisfying the claimed error bound with h=2t. Thus the check actually exercises distributions outside the graph, rather than testing only graph evaluations.
- `manifest-check.json`: all 68 frozen manifest entries match their SHA-256 hashes. This authenticates the inspected frozen inputs; it is not a proof check.
- Independent PDF text extractions and source renders record the reading above. I visually inspected frozen manuscript PDF pages 73–74, covering both upper proofs and the quadratic identity; no clipping or readability defect appeared. I did not rerun a LaTeX build and do not claim independent build validation.

## Remaining limits

The random-XOR width theorem remains a classical external asymptotic input, inspected directly rather than established by finite computation. The exact quadratic-box-hull oracle is not claimed to be tractable. General affine branching, arbitrary coupled-cut localizers, graph-hull oracles and degrees beyond the stated source budget remain outside the lower bounds. The focused source comparisons do not establish priority or an exhaustive literature survey. None of these limits contradicts a claim made in the reviewed stage.
