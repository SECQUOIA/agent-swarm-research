# Stage 3 round 1 — independent review 12

- **Verdict:** MINOR.
- **Findings:** R12-1, a local definition clarification in the asymmetric predecessor. No major finding.
- **Input:** `process/snapshots/stage03-round01/`; manuscript files were not edited. No other report from this round was read and no agents were spawned.

## Coverage

I read all five new main files and both new appendices in the frozen snapshot:

| File under `sections/` | Coverage |
| --- | --- |
| `04-incidence-interiority.tex` | Orientation and ownership, both outgoing estimates, variable/general radix, structural counts, marginal completion, finite estimates and uniform joint asymptotic. |
| `05-feedback-frequency.tex` | Domination and repair on original scopes, conditional gluing, flower sharpness, degree slabs, baseline-preserving odd-cycle rounding, cardinality factors, both matching reductions and rational scalar-envelope algorithms. |
| `06-treewidth-two.tex` | Every active/blocking invariant case, block transfer, Camion, cardinality and positive-aspect sharpness, parity counterexample, independent-set payoffs and width-three boundaries. |
| `07-positive-boxes.tex` | Fixed-ambient coefficient induction, finite spreading, unequal-box transfer, coefficient regularity, both positive-box lower families, both bipartite unequal-box examples and general comparisons. |
| `08-exact-complexity.tex` | PARTITION reduction, remainder and certificates, membership, ratio-type algorithm, weighted rank-one accuracy consequences and rational-power boundary. |
| `appendix-structural-auxiliary.tex` | Canonical pair residual law, twin compression, signed forest gluing, forest-color obstruction and fixed-radix capacity asymptotic. |
| `appendix-positive-box-predecessors.tex` | Complete symmetric/asymmetric predecessor arguments, exact all-high failure certificate, refined coarse constant and the fixed-mixture optimality calculation. |

Dependencies read include the envelope, vertex-law, deficiency, easy-term and positive-expansion foundations in `01-foundations.tex`, and the dyadic construction, harmonic law, fixed-point proof and leading asymptotic in `02-universal-positive.tex`. I also read `appendix-positive-couplings.tex` for the related multiscale context. Stage 3 does not require the cubic constructions as proof inputs. I checked the author assignment, Stage 3 scope rows including the linked additions, the full author source-to-label ledger, `process/existing-idea-development.md`, and the primary-source records. The canonical result/note proofs mapped by that ledger were compared with the new text, including the finite-step correction, fixed-ambient closure, later unequal-box family, structural auxiliary lemmas and rank-one precision correction. Stale exploratory claims were distinguished from the completed results.

The abstract and introduction are outside this assigned integration stage. I did not independently rerun a LaTeX build or the historical large graph searches.

## Findings

### R12-1 — MINOR: reset the separate-group upper values in the asymmetric proof

**Location:** `sections/appendix-positive-box-predecessors.tex:145–160`, especially the reuse of `C_L` in `D_{IL}=C_L-P_L`; compare its only displayed definition at lines 25–32.

The symmetric proof defines `C_L` using an integral over `[0,1/2]`. The asymmetric proof changes low means to `p_i <= 1-delta` and reuses `C_L` without explicitly replacing that integral or defining it as the new group's common-threshold upper value. That old integral cannot be retained: with `rho=64`, one low coordinate of mean `3/4`, and no high coordinates, it gives `C_L=65/2` while `P_L=193/4`, contradicting the asserted nonnegative group deficiency and the ensuing inequality. The intended common-threshold value is `193/4`, and the proof then works.

**Repair:** At the start of the asymmetric proof, explicitly define `C_L,C_H` as the separate groups' exact common-threshold upper values under the new split, and `P_L,P_H` as their independent values. Equivalently replace the low count integral by one over `[0,1]` (or `[0,1-delta]`) and the high count integral by one over `[0,delta]`. The canonical asymmetric source already defines these values directly. This is a local notation repair; no change to the theorem, constant or proof mechanism is needed.

## Independent verification

### Proof dependencies and compatibility

I found no circular mathematical dependency. The relevant chains are:

- Vertex laws and common upper attainment support the ownership, feedback and frequency arguments. The reduced-degree outgoing estimate uses the accepted universal degree theorem at polynomial level; it does not assume a per-term degree guarantee.
- The cardinality envelope lemma precedes both the frequency-two cardinality theorem and the TU transfer. The graph coloring argument is combinatorial and independent of either envelope conclusion. Its passage through Camion supplies arbitrary integer slabs; the separate balanced-matrix argument is confined to the unit-right-hand-side monomial case.
- The coefficient lemma depends on the independently proved cardinality envelope facts. Its product and coefficient-regularity consequences are obtained afterward. The positive-box lower family uses the earlier radix bound and width-two sharpness, neither of which depends on the coefficient theorem.
- The predecessor appendix may reuse the proved positive affine substitution. The main coefficient proof never uses either predecessor, so this forward reference does not form a cycle.
- The rational matching/dual machinery is proved before the fixed-ratio-type algorithm. The single-product hardness proof does not assume either algorithmic result. Its direct tilted-minimum reduction avoids an unproved transfer from transport-value hardness to oracle hardness.

The global-law compatibility requirements are met. In ownership rounds each high variable has at most one owner, even if several terms share a low anchor. The universal feedback law dominates every required `(F,i)` law by the same factor; its residual masses agree on `F`, and forest gluing preserves the repaired conditional laws. On a physical nonnegative box, expansion constructs an affine majorant inside each original scope, preserving the incidence hypothesis. The arbitrary-payoff sharpness example is correctly distinguished from positive monomials.

### Structural and cardinality arguments

I reconstructed the radix capacity calculation: the quantile weights give `M_q=((L-q)(b-1)+b)/b^q`, both adjacent profiles attain the cutoff affine bound, and coordinatewise digit shifts make each leaf's conditional failure probability `R/b^L`. Composite radices cause no problem. The elimination order leaves at most `L` neighbors, and the specified `K_(L,b)` minor proves equality only in the asserted `b>=L` range. Deleting/orienting deepest factors gives the stronger degeneracy and orientation lower bounds for `k>=2`. The joint lower construction satisfies all four constraints at once; its error terms vanish when the minimum controlling parameter diverges.

In the marginal-floor proof, clipping is handled by certain failure rather than an invalid sum-of-clipped-probabilities estimate. The completion denominator is positive because `m_q<=q<1`, including `q=0`. Restricting the integral to `[1/Lambda,1]` gives the displayed lower asymptotic with the negative quadratic remainder in the correct direction.

For the degree slab, full column rank and the two-incidence count force disjoint odd cycles and exclude fractional private edges and parallel two-cycles. Averaging retains `E b_v(Z)>=b_v(p)`, which is essential to the claimed gap constant. At a cardinality cycle vertex the exceptional zero/two counts each have probability `1/(2l)`, giving exactly local gap divided by `l`; concavity of the upper envelope then gives `E T(Z)<=T(p)`. Negative or nonmonotone convex tables do not invalidate either argument.

I checked every listed series and parallel terminal-type case. In series composition the shared factor contributes the required XOR correction; in parallel composition mixed terminals contribute the other parity correction, and blocking removes the potentially bad crossing cycles. The direct-edge case uses simplicity to leave exactly one edge-containing component. Articulation factor colors can be matched by a global color swap within the child block. The Eulerian support then decomposes into cycles of length divisible by four, giving Camion's required entry sum. The six-variable example separately realizes both global endpoints; the independent-set extension only claims maximum-payoff identities. The `K_(3,m)` limitation is correctly confined to the stronger cycle property.

Both matching reductions work with signed input costs. Negative coverage edges are permanently selected before the nonnegative edge-cover reduction. An inclusion-minimal edge cover is a union of stars, yielding the stated matching objective in both directions. In the cardinality gadget, mandatory coverage forces simultaneous activation of both edge ends; identical slot neighborhoods permit reassignment to the cheapest occupied slots. The bonus `2W+1` exceeds the full possible difference in original matching costs. The dual has no line and an optimal vertex with a polynomial-bit determinant bound, including boundary marginal vectors.

### Positive boxes and exact complexity

For the coefficient induction, opposite-orientation probability is unchanged by restricting the fixed ambient law. Deterministic-coordinate deletion does not condition its coins. Orders zero/one, the overflow order, and the pair base case close the induction. The finite global-extrema move has changes `-beta B h`, `-D h`, at most `D h`, and at most `beta B h`, respectively, so it can only decrease the coefficient. This is sufficient without generic Schur concavity or differentiability. Reindexing the coefficient-weighted inequalities starts at order two because the lower-order deficiencies vanish; it yields `L+1+beta_N`, including `L=0` and deterministic cases, for each entire cardinality factor.

The positive affine unequal-box substitution is bijective and has nonnegative coefficients. The sum of expanded gaps dominates each original factor gap, while common upper attainment identifies its two-law deficiency with the sum of expanded deficiencies. The softened-coverage formulas give a positive finite hull denominator and limit `rho_B` at each fixed aspect ratio. The separate width-two positive-box flower gives the lower endpoint two. I checked the eight-vertex certificates and marginal laws in both unequal-aspect examples, including the endpoint `epsilon=2` and the unit-coefficient rescaling. The fixed-mixture obstruction takes the small-anchor limit before sending the number of high coordinates to infinity and proves only its stated per-term mixture limitation.

For hardness, doubling PARTITION entries preserves the answer and ensures an integer half-total. The nonnegative remainder is at most `epsilon^2/8`; NO instances force variance at least one. The basic feasible distribution supplies at most `n+1` states for threshold evaluation and at most `n+2` for hull membership, with rational polynomial-bit certificates. The midpoint upper endpoint exceeds the reduction threshold. Fixed ratio-type counts permit exact enumeration after sorting arbitrary dual costs. The tilted objective is a square plus the same small remainder, so accuracy `epsilon^2/32` distinguishes the two cases. Dummy binary modes preserve rank one and values while meeting the cited entry-bit convention. No strong or fixed-additive-error hardness is inferred. The rational-power example's two Taylor orders and its change after logarithmic reparameterization are correct.

### Independent exact computation

I wrote and ran `verification/reviewer12/stage03-round01/check_independent.py`, using only Python's exact rational arithmetic and no existing manuscript checkers. Its saved result is `check_independent.json` in the same directory. All checks passed:

- 288 marginal vectors with ambient dimensions 2–7 and support sizes up to five; direct integration of all ambient balanced orientation patterns, moment inequalities, applicable finite-extrema moves, and 864 cardinality inequalities with `L` in `{0,1/2,2}`.
- Both exact values of the four-coordinate failed arbitrary-spreading certificate.
- 240 `(b,L)` pairs, `b=2,...,11`, `L=2,...,25`, checking both profile means, cutoff mixture values and capacity telescoping.
- 5,100 binary vertices from 80 PARTITION instances, checking the remainder, tilted-square identity and two-sided accuracy separation exactly.
- All 64 vertices of the parity example, with 16 states of each of its four possible payoff vectors.

These are finite corroborating checks. The universal conclusions above rest on the written proofs, not on extrapolation from this computation.

### Direct primary-source checks

I read `literature/AGENTS.md` before inspecting local sources. I independently checked:

- Camion's precise rectangular Eulerian-submatrix statement, visually on printed p.76, and the distinct balanced mixed-row statement on printed p.82 in [Cornuejols's author manuscript](https://www.andrew.cmu.edu/user/gc0v/webpub/notes.pdf).
- The block characterization and recursive series/parallel conventions in Hassin–Tamir, printed p.381, visually from the author scan. The browser PDF request failed; the already available local original and its rendered page were readable. [Author original](https://www.math.tau.ac.il/~hassin/sp.pdf).
- The fixed-degree scope and rank/count proof of [Barrus, Theorem 2.1](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i2p18/pdf). The manuscript proves the additional slab/multigraph scope itself.
- The weighted matching primitive in [Edmonds, Section 1](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p125_A1b.pdf), and the complete incremental matching construction in [Deza–Onn, Section 3](https://arxiv.org/html/1908.09278v1).
- Theorem 6.4.9 and its separation-to-optimization proof, printed pp.179–180, in the local extraction of the [GLS original](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf). It applies to well-described rational polyhedra without a full-dimensionality assumption.
- The common-aspect envelope formulas, visually on Adams–Gupte–Xu's printed p.22, and the relevant Sherali symmetric-envelope passages in the local primary texts. The individual formulas are correctly treated as established inputs. [Adams–Gupte–Xu original](https://www.pure.ed.ac.uk/ws/files/137020380/1704.00424.pdf).
- Del Pia–Khajavirad's Theorem 7 and its proof in the local original extraction, printed pp.1057–1058. Its Berge-acyclic full-polytope theorem supports the contextual forest attribution; the paper supplies its own scalar gluing proof. [Published article](https://doi.org/10.1137/16M1095998).
- Karp's completeness list and PARTITION definition, visually on original pp.94 and 97 in the authorized reprint. Signed entries in that definition can be replaced by absolute values in the equivalent zero signed-sum formulation. [Authorized reprint](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf).
- The rank-factorization convention, rational-entry convention, Theorem 7.4, its subsequent precision question and Corollary 7.5 in Altschuler–Boix-Adserà, including visual inspection of PDF p.55. The comparison matches the weighted oracle and explicitly restricted bit model. [Published primary article](https://link.springer.com/article/10.1007/s10107-022-01868-7).

## Remaining limits

I did not prove the classical matching, oracle-equivalence or complexity-completeness theorems from first principles, or conduct an exhaustive later-literature priority search. The cited scopes were checked directly. I did not audit the implementation of the historical width-three searches; their finite evidence is not used by any universal proof. Exact higher-width, finite-aspect and unequal-aspect bipartite optima remain open at precisely the boundaries stated by the manuscript. Those limits do not undermine the proved Stage 3 results.
