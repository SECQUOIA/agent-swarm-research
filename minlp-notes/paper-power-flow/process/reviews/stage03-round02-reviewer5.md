# Stage 3, round 2: independent reviewer 5

**Verdict: PASS on the mathematics; one required minor scope clarification in the abstract. No major issue found.**

All 18 files listed in the frozen `stage03-round02/manifest.json` match their SHA-256 hashes. I read `process/stage03-corrections.md`, but did not read other round-2 reports. I independently checked the revised statements and proofs, rather than relying on the printed Toolbox universality theorem. My round-1 approval of that general statement relied too heavily on its source theorem and missed the defective Boolean proof; the present review supersedes that part of my earlier report.

## Required minor correction

**Location:** `main.tex:35–36`.

The abstract says that rational equivalence “holds precisely for compact basic closed sets,” omitting the ground field. Section 5 correctly requires **basic closed over `Q`**. Without that qualifier, the abstract includes compact basic closed sets described with arbitrary real coefficients, which is false for rational equivalence over `Q` to rational RPF sets. For example, a singleton at a transcendental real number is basic closed over `R`, but cannot be rationally equivalent over `Q` to a singleton rational RPF voltage set. Every coordinate of such a singleton rational semialgebraic voltage set is algebraic.

**Fix:** change the phrase to “holds precisely for compact sets that are basic closed over `Q`.” The theorem itself already has the correct scope; this is a minor abstract correction.

## Appendix A: independent arithmetic verification

1. **Polynomial evaluation and scaling are correct.** Starting with a conjunction gives a globally defined polynomial evaluation coordinate for every auxiliary, with no inactive branches. Integer constants, negation, zero outputs, and nonnegative outputs can all be encoded as stated. Compactness bounds every evaluation coordinate. The two equations `w_x * w_y = q`, `epsilon * w_z = q` give exactly `x*y = z` when `w_x = epsilon*x`, and `q = epsilon^2*z` in the forward direction. The zero equation and halving chain fix their values uniquely. Choosing `k` so that `epsilon M <= delta`, with `delta <= 1`, bounds both scaled circuit values and the added product variables by `delta`. The proof makes an existence assertion, so it need not give a complexity bound for computing `M` or the chain length.

2. **The fixed constants really use only bounded addition and inversion.** The self-inversion fixes 1 uniquely because of positivity; the displayed additions fix `1/2, 3/2, 3/4, 2`, and inversion fixes `2/3`. The midpoint chain gives `D_i = 1 - 2^(-i)` and `E_i = 2 - 2^(-i)` within the common interval. Together with `A_d + Delta = 2`, it fixes `d = delta` uniquely. Taking the sufficiently small dyadic `delta` with exponent at least one is compatible with the rest of the range argument.

3. **Shifted equations are exact in both directions.** The coordinate equations force `B_s = s + 3/4` and `C_s = s + 3/2`, hence translate addition correctly. Direct elimination of the shifted-product gate yields `m = 1 + s + t + s*t`, `g = 3/4 + s + s*t`, and the final equality `u = s*t`. Nonnegativity is exactly the lower bound on `J_s = s + 1/2`; the forward smallness bound ensures that its upper bound adds no restriction on original solutions.

4. **Products from squares are correct.** In equation (45), `r = (a+b)/2`, `d = (a^2+b^2+1)/4`, and the final output is `a*b`. Every listed intermediate at `(a,b) = (1,1)` is `3/4`, 1, or `3/2`, strictly within the common interval. Repeated operands and identifying the final output with an existing coordinate do not destroy the deterministic evaluation of the fresh intermediates.

5. **Squares from reciprocals are correct.** Equation (46) gives `h = 2/a - 2/(a+1/2) = 1/(a*(a+1/2))`, so `i = a^2 + a/2` and `o = a^2`. At `a = 1`, the intermediate values match the stated finite list and every reciprocal denominator is nonzero. Each step has a unique solution once its input is fixed. The identity remains valid in any final feasible bounded assignment because every reciprocal equation excludes a zero denominator; the proof does not assume that arbitrary final assignments are near the base point in order to establish the converse.

6. **The nested continuity argument is sufficient.** First choose a neighborhood for the reciprocal gate around 1; then choose the product-input neighborhood so that its squared inputs enter that neighborhood; finally choose `delta` for the shifted inputs and auxiliaries. All gate types are fixed and finite, so this choice is uniform in the number of gates. Constants approaching the interval boundary in the midpoint chains are checked exactly rather than by an incorrect uniform interior-margin claim. The sole boundary auxiliary is `J_s` when `s = 0`, and it is handled separately.

7. **The full correspondence and designated coordinate follow.** On every original point there is one valid rational extension. Conversely, the final equations recover the small circuit and then the original conjunctive conditions, so there are no extra solution fibers. Each denominator is nonzero on the original compact set. Recovery of coordinate `t_i` is exactly `(A_{w_{t_i}} - 1)/epsilon`, giving the designated affine coordinate and continuous inverse required by Lemma 5.1. Empty sets are harmless.

8. **The source defect is accurately described.** I reread the relevant original Toolbox Lemma A text. Its weak-inequality substitution introduces nonnegative auxiliaries within Boolean branches before eliminating disjunctions. The appendix's example at `(-1/2, 1/2)` indeed has arbitrary `u >= 0` with `v = 1/2`. Thus the old coordinate-projection bijection does not follow. The new construction no longer uses that step, and the decision-hardness source needed elsewhere only needs preservation of existence.

## Section 5: exact scope and topology

- **Basic-closedness invariance is proved correctly.** Nonzero denominators of `F` and nonzero polynomial numerators of the composed denominators of `G` admit a common positive rational lower bound in absolute value on compact `S`. The square lower bounds therefore define a basic closed domain where every rational expression is well defined. Multiplication by positive even powers clears denominator signs without changing weak inequalities. On this domain, `F(t) in T` and `G(F(t)) = t` are necessary and sufficient for `t in S`. In the reverse direction, the fact that `G` maps every point of `T` into `S` excludes ambient extraneous points. The argument does not require a globally defined extension of either rational map.
- **The three-quadrant obstruction is sound.** The leading nonzero homogeneous form of a defining polynomial vanishing at the origin must be nonnegative on all three included quadrants. Odd degree is impossible because the second and fourth quadrants are negatives of one another. Even degree transfers nonnegativity from the first to the third quadrant. A direction avoiding the finitely many leading-form zero sets makes every such form positive in the excluded quadrant. Sufficiently near the origin, all defining inequalities would then hold. Polynomials with positive constant term and identically zero polynomials are addressed. This establishes the claimed local obstruction without relying on the defective source.
- **The rational-equivalence characterization follows.** Sufficiency now uses the proved appendix lemma; necessity uses invariance and the visibly basic closed RPF constraints. Both directions retain compactness and the field `Q` in the theorem statement. All structural restrictions survive through the previously proved construction.
- **Topological universality remains valid with its weaker map class.** The finite standard-simplex realization has rational polynomial constraints. A vector belongs exactly when its positive support is a face: otherwise the nonface equal to its support violates its product equation. The barycentric maps agree on shared faces and give the standard piecewise linear homeomorphism to a geometric realization. Semialgebraic triangulation of a compact semialgebraic set supplies the remaining homeomorphism. This is not asserted to be rational, defined over `Q`, or computable with polynomial output size. I independently checked [Ohmoto–Shiota v2, p.2, Theorem 1.1 and Section 1.2](https://arxiv.org/pdf/1505.03970v2): the stated triangulation is semialgebraic and the compact case uses a finite complex.
- **The singleton field theorem now has a valid foundation.** An algebraic singleton isolated by rational polynomial conditions is compact basic closed. The appendix gives both unique rational extension and the designated affine coordinate. Therefore every voltage lies in `Q(alpha)`, and one retained voltage generates that field. The rational case, degree examples, structural transformations, and reference-fixed AC claims remain correct.

## Sections 4 and 6 and integration

Section 4 is byte-identical to the previous snapshot. I rechecked its dependence on arithmetic universality: it starts from bounded ETR-INV and does not use Boolean-to-conjunction rational equivalence. Its planarization, wider copy bounds, repeated inversion ports, connecting path, and even electrical subdivisions therefore remain sound independently of the source correction.

The only Section 6 change replaces the inaccurate description of D's neighbors by one complemented `x` copy of weight two and one complemented `y` copy of weight one. This matches the graph and retains the valid `3*delta` contribution. I rechecked the residual-transfer and tiny-family arguments, the epigraph's connected compactness and quadratic JPT specialization, the promised certificate statement, and the reactive-energy/spectral constants; I found no new issue or dependency on the corrected source claim.

The revised main text distinguishes rational basic-closed universality from general semialgebraic topological universality. Apart from the abstract's omitted ground-field qualifier above, this distinction is maintained consistently.

## Verification

- Manifest: all 18 listed file hashes match.
- Frozen arithmetic checker: PASS on 1,681 composed gate profiles, 49 valid disk profiles, 72 outside profiles, 49 inconsistent circuit profiles, nine exact constant-chain configurations, and 35 simplex-support profiles.
- Frozen developments checker: PASS on the structural, residual, tiny-family, and graph-inequality checks.
- Independent `latexmk` build: 24 pages; no final undefined citations/references or overfull/underfull diagnostics. I inspected the rendered dense gate page and extracted manuscript layout; the equations are readable without clipping.
- Artifacts are in `verification/reviewer5/stage03-round02/`: checker logs, build, extracted layout, and rendered appendix page. Finite checks support the algebraic audit; they do not prove the quantified characterization, compactness arguments, or triangulation theorem.

## Optional improvements

No additional mathematical development is required to accept this stage after the minor abstract correction. The abstract can still be shortened during full-paper integration, but that editorial choice is not an acceptance condition here.
