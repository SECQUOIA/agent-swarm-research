# Stage 6, round 1 — independent review 12

## Verdict

**PASS.** I found no demonstrable major or minor defect in the assigned frozen manuscript. This verdict concerns this integration stage, which precedes the separate final whole-paper review. It is not a claim that every external theorem has been independently reproved.

Frozen object: `process/snapshots/stage06-round01/main.pdf`, 111 pages, SHA256 `343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916`. Additional focus: exact checks, reproducibility, build, and correspondence between printed code and mathematical certificates. I did not consult other current-round reports or use prior PASS labels as evidence.

## Coverage

I read the frozen review protocol, Stage 6 reviewer and author assignments, `stage-06-author.md`, the scope proposal, the coverage ledger, README, `main.tex`, `macros.tex`, and the complete bibliography. I read all manuscript source files in full:

- `01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`, `07-positive-boxes.tex`, and `08-exact-complexity.tex`.
- `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`, `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, and `17-synthesis.tex`.
- `appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, and `appendix-integer-comparison.tex`.

I read `literature/AGENTS.md` before inspecting local originals. Primary-source checks were targeted to the actual dependencies, rather than complete readings of every cited paper:

- Kronqvist–Misener–Tsay: original PDF pp. 4–7, assumptions, retained domain, sharing convention, and formulation; pp. 15–16, Definition 4, Theorem 6 and its proof, and refinement statement. Anstreicher: original PDF pp. 12–13, Conjecture 4 and its precise moment model. Khajavirad: formulation definitions and Propositions 1 and 3 in the [2024 primary manuscript](https://arxiv.org/html/2404.03091v1).
- Balas: Section 2, Theorem 2.1 and proof, printed pp. 7–9. Wu et al.: original PDF p. 12, Lemma 3 and Theorem 3; I did not independently audit its supplemental proof or every upstream assumption. Starr: Appendix 2, Lemma 2, corollary and proof, printed pp. 35–36.
- Lee–Raghavendra–Steurer: Theorem 3.8/equation (3.11), and Theorems 5.3–5.4 with the displayed pseudo-density construction, PDF pp. 23 and 32–34. Braun et al.: Section 4.1, Theorem 6(i), PDF p. 18. Fawzi–Parrilo: Theorem 1 and its fixed-block model, PDF p. 3. The latter two lower-bound proofs were not reread in full.
- Etessami–Yannakakis: Theorem 5.2 and reduction construction, PDF pp. 26–28. Belotti et al.: PDF pp. 1–2, the classical limiting-bound/nonfinite-iteration scope. Stewart et al.: Section 4.1, equation (18), PDF pp. 21–22. Esparza et al.: Section 7, equation (14), Theorem 7.1 and proof, PDF p. 34. Lubin et al.: Lemma 4.1 and parity proof, PDF p. 12. Beach et al.: Section 5.1.1 of the cited combined version, PDF p. 21.
- Schoenebeck: the random model, Definition 10, Theorems 11–12, Lemma 13, the full signed-character construction and proof on printed pp. 9–11, and the appendix width argument, Theorem 21 and Proposition 22, printed pp. 17–19. This includes the source's proof machinery underlying the spatial transfer, not just its theorem label.
- Cornuéjols: Theorems 6.5 and 6.13, for the Eulerian/TU and graph-structure criteria. Luedtke et al.: Conjecture 1 and conclusion, PDF p. 22. Davidson–Donsig: Theorems 1.2 and 2.4, including the real Grothendieck/projective-norm formulation. Boland et al.: Lemma 1 and Corollary 1, printed pp. 4 and 6. Sherali: equation (13) and Theorem 3, printed pp. 252–253.

These locators describe what I actually inspected. I did not independently retrieve or read every bibliography entry, including the complete Hassin–Tamir, Coniglio, and Altschuler–Boix-Adserà sources. No attempted source access failed during this review; some dependencies remain unaudited rather than inaccessible. Coverage against repository developments was checked through the frozen scope and coverage records and manuscript, not by rereading every original repository note line by line.

## Findings

None. No repair request or finding ID is raised.

## Independent verification

### Build and executable certificates

All artifacts are under `verification/reviewer12/stage06-round01/`. I copied the frozen TeX, bibliography, and verification inputs into `build/` and built there. The frozen inputs were not modified. The fresh build exits successfully, produces 111 pages, reports no warnings or duplicate labels, and confirms the printed Stage 2 checker matches its file. All copied manuscript input bytes match the frozen files. Although generated PDF metadata changes the binary PDF hash, the complete extracted text of the rebuilt PDF is identical to that of the frozen PDF. See `build/verification/build-report.json` and `printed-replay.json`.

I independently extracted and executed the two complete Python verbatim listings from the frozen TeX, without importing the author's implementation. The signing enumeration returns `[1, 2, 4, 4, 5, 8]`. The cubic listing verifies the affine minorants at every relevant count state, nonnegative normalized attaining distributions, the three required means, equality of primal and dual values, and the reported ratios. Its three large examples return `20891/10411`, `6601/3225`, and `7443345/3445256`; all other assertions, including the small counterexamples and `135/67` certificate, pass. Files: `printed-appendix-finite-signings.py`, `printed-appendix-cubic-certificates.py`, and `printed-replay.json`.

To test the reader-facing artifact as well, I extracted the cubic listing directly from PDF pages 86–87 with `pdftotext -layout`, removed only page numbers and surrounding prose, and executed it successfully. The full output agrees with the TeX-derived replay. See `pdf-extracted-cubic-checker.py` and `pdf-extracted-replay.json`. This checks actual rendered character/indentation correspondence, not merely agreement between two repository files.

I visually inspected PDF pages 1, 85, 86, 87, 93, 96, 100, 104, 107, and 110, including both full cubic-code pages, the supporting theorem displays, and bibliography. These pages are legible and unclipped. This is a selected-page visual review, not a visual inspection of all 111 pages.

### Independent exact arithmetic

`check_independent.py` imports no manuscript checker and uses rational arithmetic throughout. Deterministically sampled cases are identified as finite tests. Its saved output, `check_independent.json`, records:

| Check | Completed cases | What was checked |
| --- | ---: | --- |
| Point-packing attaining matrices | 75, with 353,992 RLT inequalities | All stated secants, all pairwise box-product inequalities, and minimum attained distance; ordinary cases for n=2 through 40, symmetry cases for n=5 through 40 |
| Fractional-cardinality Gram expansion | 896 entries | Nonnegative coefficients and the exact falling-factorial/binomial identity at admissible half-integral parameters for degrees 1 through 4 |
| Rank-one rounding | 1,996 rational atoms | Exposure nonnegativity, one-per-pair rounded atoms, the intermediate error estimate and both stated final bounds, m=1 through 10 |
| Primitive FBBT | 4,356 transitions | Affine and product interval-hull lower-bound updates, invariant preservation, and the progress upper bound at four exact squaring scales |
| Overlapping parity supports | 350 systems | Basis union equals full support union, support size at most D times rank, and exactly 2^(n−rank) consistent assignments |
| P-split examples | 655 witnesses | The rational-coordinate witness inequalities and explicit retained-box lifts |

The packing checker verifies entries and inequalities; PSD is justified separately by the analytical projection-plus-diagonal decomposition. None of these finite tests alone establishes the universally quantified theorem.

### Proof reconstruction and attempted falsification

For the core envelope chapters I checked that vertex distributions preserve the complete mean vector, and that a separate law is not silently chosen for each positive monomial. The common upper law, the harmonic coupling's normalization/inactive mass, the two distinct exact-hull parameter regimes, and the coefficient-spreading argument have the necessary hypotheses. The graph arguments preserve the coverage baseline when gluing local laws; parallel/dummy edges and the series/parallel boundary invariant are accounted for. Positive-box statements keep the common-ratio restrictions where required. The sampled-clone transfer controls all clone vertices before transferring both envelopes. I found no promotion of a finite cubic computation to a sharp universal constant.

For the cardinality and spatial chapters I reconstructed the homogeneous Gram expansion and its degree restrictions, tensor positivity for globally coupled squares, endpoint interpolation for coordinatewise auxiliaries, and the exact degree-two realization from signed moments. In the monomial transfer, substitution of a degree-2r polynomial can require original degree 2rD, and positivity of its square requires 4rD; the manuscript uses the latter budget. An independent basis of parity rows has the same union of supports as all rows, so its size q gives both the support bound Dq and the witness count 2^(n−q), even with repeated or overlapping supports. This supports the denominator D in the cover exponent. The original cubic objective and quadratic lifted formulation retain their distinct minimum-order requirements. The affine-branching discussion correctly states an obstruction to this proof method, not a general affine-tree lower bound.

For Schoenebeck's input I checked the signed equivalence-class Gram construction: inner products depend only on the symmetric difference, consistent signs multiply, and the resulting functional is positive on the required squares. The manuscript's chosen constant density and nonzero denominator parameter fit the primary statement; the occurrence-deletion step does not require an event independent of the pseudoexpectation event. The degree and probability quantifiers were not inferred from a generic reference to “Lasserre hardness.”

For `prop:packing-values`, the averaging upper bounds agree with the explicit covariance witnesses. In the symmetric construction the first k coordinates use a multiple of `I−J/k`; remaining covariance entries are nonnegative diagonal blocks. This proves PSD directly and explains the n≥5/k≥2 threshold. The tightened diagonal secants and all RLT products are compatible with the claimed values. The manuscript correctly credits the four values to Khajavirad and preserves Anstreicher's absence of an xy moment block.

For `prop:scale-hull` and `prop:scale-perspective`, endpoint disaggregation preserves extensive quantities by distributing the scale, but a shared intensive variable need not be preserved by the same mixing. The common-variable counterexample therefore addresses a real missing constraint. The rectangularity criterion is the needed condition for replacing joint feasible choices by independent factor choices; the cost example defeats the earlier unrestricted factorization. The supporting discussion does not claim a new general disjunctive-hull theorem.

For `ex:psplit-exact-box`, both disks contain all four vertices of the retained box, so their convex hull is the whole box. The explicit auxiliary lift verifies exactness directly. This meets the published hypotheses while exposing both failures in the source's nonexactness proof: strict Jensen slack requires different component arguments, and a proposed outward perturbation must stay inside X. `prop:psplit-repair` restores precisely those conditions.

For `prop:psplit-balls`, at fixed transverse auxiliary c the two rectangles convexify to `a+b≤U+r²−sum(c)`. Downward closure permits substitution of the true squares. The resulting capsule error increases with squared transverse radius, since its derivative is `1/2+d/(4 sqrt((d/2+r)²−rho²/2))>0`; the stated maximum and limit follow. The rational rotation keeps the exact transformed domain, without asserting an additive-bound hierarchy there. For `prop:psplit-exact-image`, the midpoint of the two center images retains the original witness. In aligned coordinates the decreasing concave bound `d²+1−c+2d sqrt(1−c)` forces the two endpoint inequalities defining the capsule. This validates the stronger auxiliary-image comparison without confusing it with a graph hull.

For `prop:correlation-face` and `prop:correlation-stability`, rank-one marginals give the normalization and the exposed one-per-pair atoms. I checked the chain from the intermediate rounding estimate `4SB+58SD+5|S−m|` to `(136m+10)g`, and the separate total-mass form. The exact tests include unequal row and column marginals and totals on both sides of m. In `prop:rank-one-approximation`, the coefficient norms and the facial reduction are needed to transfer entrywise-l1 accuracy to a shifted slack matrix. The LRS substitution has the displayed k^(−23/4) prefactor and k^(13/2) log(m) denominator, yielding the stated `(m/log m)^(2/13)` exponent. Exact SDP size, approximate SDP size, fixed-block/SOC size, and spatial certificate count remain separate resources.

For `lem:fbbt-fixed-point`, every sound contractor retains the least fixed point, while fairness of the forward updates forces the limiting lower vector to dominate its defining monotone map; these two inequalities identify the limit. The hardness construction distinguishes rational least roots and an additive constant gap rather than asserting NP-hardness of PosSLP. For `prop:fbbt-iterations`, stronger upstream initialization is a valid monotonicity comparison. The invariant `0≤l_w≤c l_z` makes inverse product propagation ineffective, and every affine application obeys `l_z(new)≤b+c l_z`. Induction gives `l_z≤1−(1−b)^K≤Kb`, hence the exact count `2^(2^n−1)`. Upper endpoints do not invalidate this argument. The imported Newton examples are explicitly used to derive a Kleene bound, not misquoted as already stating one. The primitive-contractor and input-encoding qualifications are present.

## Remaining limits

The paper's open sharp constants, unequal-aspect frequency-two behavior, unrestricted affine branching, stronger coupled-cut localizers, and graph-hull reformulations remain open or outside scope as stated. This review does not resolve them. The introduction, synthesis and coverage ledger retain those distinctions; I found no integration claim that requires them to be solved.

The independent computations cover finite exact instances, not asymptotic lower-bound families. Source statements and selected proofs were checked as listed; remaining cited external theorems are dependencies, not newly verified theorems. The bibliography was read in full but was not independently revalidated entry by entry against publisher records. PDF text/build integrity was checked globally, while rendered-page inspection was selective. These are limits of this review and should carry forward to the separate final whole-paper loop.
