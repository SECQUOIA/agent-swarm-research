# Stage 2 author record

Date: 2026-09-05. Status: complete author draft, ready for the coordinator's frozen review. This record does not substitute for the required independent stage reviews.

## Manuscript organization

The stage adds `sections/02-universal-positive.tex`, `sections/03-cubic-equal-means.tex`, `sections/appendix-positive-couplings.tex`, and `sections/appendix-cubic-certificates.tex`. The two main files are inserted before the existing appendix switch. The existing Stage 1 section, its finite-signing appendix, and macros are unchanged. The main introduction and abstract remain available for the planned final integration stage; the new section openings state the Stage 2 outcomes directly.

The scalar graph-hull gap remains `H`, and the exact specified monomialwise gap remains `T`. The harmonic cutoff parameter is renamed `eta` in LaTeX, with its definition explicit, to avoid colliding with `rho_G` and `rho_B`. All ratio theorems exclude zero hull gap, while distribution inequalities cover zero term gaps and boundary means.

## Row-by-row coverage ledger

All source paths below are relative to the repository root. All labels refer to the current manuscript.

| Canonical Stage 2 source | Required claim or development | Manuscript labels and coverage |
| --- | --- | --- |
| `results/positive-multilinear-gap.md` | Sparse unit-coefficient dyadic family, dimension, degree, monomial and occurrence counts | `thm:dyadic-exact`, `eq:dyadic-polynomial`; explicit counts and strictly interior original means. |
| same | Exact hull formula and cutoff, including adjacent cutoff ties | `eq:dyadic-exact`, `eq:dyadic-cutoff`, `eq:dyadic-affine-certificate`; upper-tail rearrangement, exact affine upper bound, two resource profiles, convex mixture, bit-reversal/XOR implementation. |
| same | Arbitrary versus nested partitions | `eq:dyadic-surrogate`, `eq:arbitrary-partitions`, `prop:arbitrary-dyadic`, `eq:dyadic-log-sum`; exact attainment restricted to nested partitions, separate complete logarithmic proof for arbitrary level partitions. |
| same | Original conjecture resolution | Opening of `sec:positive-universal`, direct citation to Luedtke author manuscript p.22, Conjecture 1. The paper claims a mathematical counterexample and does not infer publication priority from a negative search. |
| same | Dense predecessor | `eq:dense-predecessor`, `eq:dense-count-lp`; exact count LP, both directions of realization, union-bound comparison. Floating-point dense values are deliberately not used as sparse hull values or proof. |
| same | Homogeneous reduction, boundary/interior distinction | Paragraph after `eq:arbitrary-partitions`; exact face preservation, continuity into the interior, unchanged monomial count, increased occurrence count. General strengthened reduction is `thm:coefficient-removal`. |
| `results/positive-multilinear-degree-upper-bound.md` | Distinct dyadic coupling and tail lemma | `app:dyadic-rounding`, `lem:dyadic-tail`, `eq:dyadic-tail`, `prop:dyadic-degree`; full probability normalization, scale selection, integral and mixture proof of `2(K+1)/c_0`. |
| same | Nonnegative-box transfer | Shared verified `prop:box-transfer`, invoked after each unit-cube upper proof; original termwise gap is at most expanded termwise gap, not an unjustified equality. |
| `results/positive-multilinear-sharp-degree-growth.md` | Harmonic global law and original explicit finite bound | `eq:harmonic-law`, `lem:harmonic-curve`, `eq:original-harmonic-finite`; proof of `24 Lambda/(c_0 log Lambda)` with `Lambda=max(16,1+log d)`. |
| same | Original leading-constant mixture | `eq:older-leading-mixture` and its surrounding complete argument, including `M=exp(Lambda-1)`, `b>=6`, the integration interval and inverse-guarantee weights. |
| same | Sharp degree/dimension asymptotics and interpolation | `thm:positive-growth`, `eq:positive-growth`; largest admissible dyadic example and unused-coordinate padding prove the all-integer limiting statements. |
| same | Universal simultaneous coupling independent of objective/supports | `eq:simultaneous-frechet`; explicit quantifiers and matching asymptotic guaranteed fraction. No exact-envelope algorithm claim. |
| `results/positive-multilinear-second-order-upper.md` | Optimized cutoff and complete scalar deficiency curve | `eq:harmonic-parameters`, `eq:harmonic-integral`, `lem:harmonic-curve`, `thm:harmonic-fixed-point`; `M>=d-1` is real, and zero gaps are excluded before divisions. |
| same | Fixed point, optimal scalar mixture, final mixture with independence | `eq:harmonic-fixed-point-bound` and proof; tangent mixture and crossing upper bound limit optimality to the two scalar guarantee curves. |
| same | Lambert certificate and second-order upper denominator | `eq:lambert-bound`, `eq:lambert-integral-certificate`, `eq:second-order-upper`; `w>=1`, explicit positive denominator, cutoff `M=(d-1)N`, and asymptotic proof. No second-order lower theorem. |
| same | Special original rho=1 cutoff and reciprocal refinement | `app:reciprocal-cutoff`, `eq:rho-one-finite`, `eq:rho-one-asymptotic`, `eq:rho-one-reciprocal`; manuscript uses `eta=1`, retains the finite `log Lambda>=4` certificate and full Taylor-remainder proof. |
| `results/positive-multilinear-coefficient-removal.md` | Exact preservation of both envelopes by cloning | `thm:coefficient-removal`, `eq:clone-envelopes`; equality of feasible expectation intervals in both directions, and separate exact termwise scaling. |
| same | Uniform random sampling, homogeneous/interior reduction | `eq:bounded-sum`, `eq:clone-union-bound`; all `2^(nm)` clone vertices plus termwise-gap event, positive probability, envelope error, fixed-original-instance limiting quantifiers. Hoeffding is attributed and proved. |
| same | Finite nonconstructive 25,000-variable bound | `eq:finite-25000-probability`, `eq:finite-25000-margin`; 464 m^3 candidate terms, m=1000, error t=m^3/10, strict margin, positive hull gap, explicit distinction from a generated sample. |
| `results/positive-cubic-gap.md` | Exact 18/24/192-variable witnesses | `prop:cubic-finite`, `eq:cubic-six-family`, `tab:cubic-finite`, `app:cubic-certificates`, `eq:cubic-integer-dual`, `tab:cubic-duals`, `tab:cubic-primals`; every coefficient, dual, primal probability and exact envelope is present. Standard-library checker is printed and supplied. |
| same | 25-variable homogeneous interior bound | `eq:homogeneous-25`; quadratic coefficient sum 1840, padding failure mean 1/1000, T=943, H<=80947/175, ratio>=165025/80947. This is explicitly a bound, not a new exact hull formula. |
| same | General endpoint orientation and cubic 8/3 | `prop:endpoint-orientation`, `eq:endpoint-bound`; full nested exclusion, exact geometric expectation, sorted-sum proof and monotonicity in degree. |
| `results/positive-cubic-analytic-family.md` | Continuous scalar minorant, convex elimination and exact Bernstein table | `lem:cubic-scalar`, `tab:cubic-bernstein`; positive Hessian determinant 248, boundary first-order proof on c<=3/10, unrestricted quadratic elimination on c>=3/10, all five rational polynomial identities. |
| same | Strongest slack improvement and limiting lower bound | `thm:cubic-analytic`, `eq:cubic-analytic-family`, `eq:cubic-count-expansion`, `eq:cubic-analytic-cav`, `eq:cubic-analytic-tgap`, `eq:cubic-analytic-finite`, `eq:cubic-interval`; minimum Bernstein coefficient 901/120000 yields 4830000/2229099=1610000/743033. The older 483/223 is identified as weaker. Only a supremum lower bound is asserted. |
| `results/positive-cubic-two-level-family.md` | Two-level family, continuous identity, exact limiting ratio 243/115 | `thm:cubic-two-level`, `eq:two-level-family`, `eq:two-level-scalar`, `eq:two-level-cav`, `eq:two-level-ratio`; both bounds and conditional Bernoulli equality atoms prove convergence of actual ratios, with m a positive multiple of four. Finite m=20 bound is retained. |
| same | Exact 32-variable 135/67 witness | `eq:two-level-16-dual`, `app:cubic-certificates`; all 289 inequalities, residual-minimum list, uniform fixed-count attaining law, exact envelope 1088. |
| same | Explicit homogeneous interior 52-variable, 4,320-monomial unit witness | `eq:unit-52`; entire polynomial, all means, exact termwise values, quantitative envelope loss 12/5 and ratio>=2700/1343. |
| same and its relevant audit | Marginal scope and older distinct rational parameter variant | Paragraph after `thm:cubic-two-level` covers all means>=1/2 and continuity to strictly>1/2. `app:two-level-variant`, `eq:two-level-variant-scalar` retain the alternate 33/16 family and finite m=50 bound 1617/800 with a complete proof. |
| `results/positive-cubic-rounding-upper-bound.md` | Global 18O/31+6I/31+7B/31 mixture and 31/12 bound | `thm:cubic-upper`, `eq:cubic-mixture`; all cubic low-coordinate classes, all four one-low subcases, separate quadratic cases, exact marginals and box transfer. |
| same | Mixture-family optimality only | Final portion of `thm:cubic-upper` proof; exact/limiting three test configurations and cancelling convex combination, explicitly no global optimality of R_3. |
| `results/positive-multilinear-equal-marginals.md` | Classical elementary-symmetric formula and exact finite optimization | `sec:equal-means`, `eq:sherali-symmetric`, `thm:equal-finite`, `eq:equal-finite`; explicit binomial convention, degree restriction, adjacent-count common law and attaining E_d. |
| same | Exact dimension-free supremum, optimizer, sharp two | `cor:equal-infinite`, `eq:equal-infinite`; fixed-degree limits, floor/ceiling optimizer, Bernoulli inequality, complete-graph sharpness. Exact unit-cube scope is stated. |

## Proof and source checks

I read the Stage 2 assignment and scope proposal, the current main file/macros and all foundational lemmas used here, every canonical Stage 2 result in full, and the relevant audit corrections. The proof checks were performed afresh while writing: correct expectation directions, exact singleton marginal preservation, nonnegative deficiencies under omitted mixture components, finite versus asymptotic quantifiers, and positive denominators were checked explicitly. The older dyadic and original harmonic proofs remain full proofs rather than citations to repository notes.

The most important reconciliation was the analytic cubic headline. The canonical family note's title retains 483/223, while its final paragraph and independent audit certify a uniform slack. The manuscript uses 1610000/743033 as its strongest lower endpoint and includes the coefficient table proving that slack. It never turns a lower-bound sequence into a claimed attained finite optimum. No new mathematical defect in the canonical core proof was found during this authoring pass.

Primary sources checked:

- Read `literature/AGENTS.md` before local source use. No original copyrighted source was copied into the paper directory.
- Luedtke–Namazifar–Linderoth author manuscript: local original and extracted text, p.22, Conjecture 1. The claim is the nonnegative-box positive-coefficient uniform-constant conjecture. The manuscript uses this directly checked numbering; it does not rely on a secondary published-version conjecture number. Existing Stage 1 attribution for common upper attainment and positive bilinear two remains in place.
- Sherali, *Convex Envelopes of Multilinear Functions over a Unit Hypercube and over Special Discrete Sets*, Acta Mathematica Vietnamica 22(1), 245–270 (1997): read the local primary text and extracted the original PDF pp.252–253 (PDF pages 8–9) with `pdftotext -layout` to check equation (13) and Theorem 3. The explicit whole-cube maximum-of-affine-functions formula is reproduced with attribution, and the equal-mean specialization is proved independently. Open primary URL: https://math.ac.vn/uploads/files/9701245.pdf.
- Hoeffding, *Probability Inequalities for Sums of Bounded Random Variables*, JASA 58(301), 13–30 (1963): opened the primary PDF https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf, downloaded an ephemeral copy under `/tmp`, and visually read its cover metadata and printed p.16 (PDF page 5), Theorem 2/equation (2.6), with the independent bounded-range assumptions. The paper attributes its two-tail specialization and also includes a short proof. The image-only PDF did not support text extraction; the visual inspection was the source check.

Two verified primary entries, `Sherali1997` and `Hoeffding1963`, were appended to the paper-local bibliography. No claim is made that these classical tools or the standard sampling mechanism originate here.

## Validation

- `python verification/check_stage02_finite.py`: passed. This file is extracted directly from the appendix's printed executable block. It checks every one of the 343+729+274625 three-group integer inequalities, all exact primal probabilities and means, primal–dual equality, all displayed ratios, and all 289 two-level count inequalities. No solver is used.
- `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python verification/check_stage02_symbolic.py`: passed. It reads the actual manuscript's five Bernstein rows, expands them exactly, checks both eliminated quartics, verifies their uniform slack and reduced limiting ratio, and checks both rational two-level sum-of-squares identities. Output is `verification/stage02-symbolic.json`.
- The coordinator's five existing repository checks in `verification/repository-checks/global.json` all passed before authoring. Those cover the original finite cubic, analytic family, two-level, cubic rounding and harmonic-special-case scripts. I did not treat those statuses as substitutes for the proofs or rerun unrelated checks.
- The separate root cutoff check in `verification/check_harmonic_cutoffs.json` covers 24 numerical parameter cases. It remains supplementary numerical evidence, not a proof of the full cutoff theorem.
- `python verification/build_and_check.py`: final compile and label/layout record in `verification/build-report.json`; no LaTeX warnings, overfull boxes, undefined citations/references, or duplicate labels.
- Visually inspected the scalar Bernstein table and derivation pages, finite cubic values table, exact dual/primal tables, and printed checker/bibliography pages. No clipping or illegible certificate layout was observed.
- A final integrity check compares the unchanged Stage 1 mathematical files against `process/snapshots/stage01-accepted`. Its output and the final build metadata are recorded in `verification/stage02-author-validation.json`.

## Bounded development and retained uncertainty

The second rational two-level parameterization was present in its canonical audit but not the final result note. I retained it compactly in an appendix and completed its finite correction and two-sided ratio proof; its exact identity is included in the symbolic check. This is a bounded completion of the same mechanism, not a new optimum claim. The main family remains the stronger 243/115 construction.

No open optimization question was closed by unsupported extrapolation. The exact finite-degree constants (including R_3), a matching second-order lower asymptotic, and global optimality beyond the specified rounding-mixture families remain unresolved. Cloning does not preserve fixed dimension or give a small deterministic support. The 25,000-variable claim is nonconstructive; the 52-variable example is explicit. Equal-mean exact formulas are stated only for the unit cube. This stage makes no spatial-certificate consequence from its positive gap examples.

## Correction addendum after Stage 2, round 1

Date: 2026-09-05. The separate correction pass implemented every accepted finding in `process/stage02-round01-adjudication.md`. The original record above describes the first author draft; this addendum updates its coverage and validation for the corrected draft. A fresh complete review round remains required.

| Source or finding | Added or corrected coverage |
| --- | --- |
| `notes/review-positive-cubic-two-level.md`, R11-01 | `tab:two-level-small` contains the affine minorants, attaining counts, exact convex envelopes, common upper envelopes/termwise gaps, and ratios for m=4,8,12. Its surrounding proof constructs uniform fixed-count subset laws with all singleton means. The printed and executable checker verify every one of the additional 25+81+169 count inequalities and all attainment/envelope equalities. |
| Same finite refinement | `thm:cubic-two-level` and its proof now state and prove that, among positive multiples of four in `eq:two-level-family`, the ratio exceeds two if and only if m>=16. The three smaller exact ratios are below two; m=16 has ratio 135/67; monotonicity of the existing lower bound gives at least 4617/2300 for every m>=20. This is not a minimum-dimension assertion over other families. |
| `results/positive-cubic-analytic-family.md` and its audit | The final paragraph of the `thm:cubic-analytic` proof explicitly specializes `eq:cubic-analytic-finite` at m=36 to the weaker bound 16985/8436>2 when the slack is dropped. The full positive-slack bound remains unchanged and is strictly stronger. |
| S02R01-R02-01 | The first interval in the `prop:arbitrary-dyadic` proof contributes **at most** the geometric sum, which remains strictly below two. |
| R13-M1 | The `prop:arbitrary-dyadic` proof defines `log_2^+ v=max(0,log_2 v)` for v>0 before its first use in `eq:dyadic-log-sum`; the existing zero-integrand convention remains. |
| R13-M2 | The checker is printed in two complete blocks: imports/data/function on page 31, then all loops and closing assertions/output on page 32. Concatenating the two blocks reproduces `verification/check_stage02_finite.py` exactly. `verification/build_and_check.py` now checks this identity and fails on a mismatch. |

The extended finite and symbolic checks passed, including an exact m=36 evaluation with and without slack and the positive derivative of the two-level lower bound. The build completed without warnings, overfull boxes, unresolved references/citations, or duplicate labels. Changed PDF pages 20, 22, 23, 26, 30–33 were inspected visually, including both complete code blocks and the new table. The three accepted Stage 1 source files, main file, bibliography, and universal-positive section were checked byte-for-byte against their relevant snapshots and remain unchanged. The complete correction record is `process/stage02-corrections.md`; current validation is `verification/stage02-corrections-validation.json`. Historical reviewer checkers and snapshots remain unchanged; any checker extracting the revised printed program must concatenate **both** verbatim blocks.
