# Stage 4 independent review 4

Reviewed frozen `reviews/revision-stage4-round1/source`, including all 1,308 lines of `sections/04-vector.tex`, the complete abstract, introduction, conclusion and bibliography, and the required scalar compiler, parity/disjunction and rational allocation dependencies. I read the author and literature records as leads, but no other Stage 4 reviewer report or adjudication. The author block is blank as requested.

## Findings

No supported major or minor issue identified. No manuscript change is requested by this review.

## Critical checks and coverage

- Reconstructed the finite and compiled overlays, their shared interpolation weight, repeated-knot handling, curvature-row reductions, maximum-product allocation, both oracle spanners and the explicit band in the effective nonlinear image. In the fixed-grid lemma, the inner-ball repair gives exact feasibility; the fixed denominator and determinant growth bound jointly control subsequent inverse and objective lengths. The positive-polar separator supplies weak membership or a valid rational separator without assuming a strong polar oracle. The rank-zero arguments and affine-output treatment are sound.
- Checked the separable packing argument with a common output basis across all inputs. Recomputed all six table constants from the packing denominators and the factors 12 and 5832. In particular, the compiled oracle factor is `5832*219 < 2^21`; the one-input oracle factor is `486*144 < 2^17`. Rounding is allocated across coordinates before summing the bands.
- For the degree-32 product example, checked the full integer sections, not only the three original boxes: label one forces weights `(t,1-2t,t)`, keeps the input in the middle interval and every admitted output below one. Exact rational arithmetic independently confirms the box widths, middle-output bound and both oriented-thirds inequalities. Products provide exactly `n` general integers, while the `3^n` contacts require exactly `ceil(n log_2 3)` binaries. The manuscript correctly states the possible exponential continuous size of its binary upper construction.
- Verified the positive-power obstruction, modulo-three and cap-set arguments, and the limits claimed for them. Pair incompatibility first makes the residue assignment injective; the three-distinct-contact violation then excludes nontrivial zero-sum triples. These bounds concern the minimum itself but do not establish a growing binary/general-integer gap for that family. The affine shear is explicitly distinguished from nonnegative monomial coefficients.
- Checked all hinge integer sections and the Bernstein perturbation margins, including graph containment after thickening. Checked the triangular-wave period/orientation formulation at period boundaries and `x=1`, its graph-containing band, peak/trough binary lower bound, and degree-dependent upper comparison. The signed-polynomial overlay handles curvature-root brackets, concave cells, directed rounding and singleton cells with the claimed error budgets. The tilted-body construction preserves the scalar difference obstruction and has the stated diverging condition ratio; the finite conditioning and simplex-band estimates use only the stated inner/outer inclusions, including for nonsymmetric error sets.
- The abstract, introduction and conclusion accurately distinguish finite existence from polynomial rational construction, general integer dimension from binary dimension, and dimension from encoding length. The open one-input box question is not presented as resolved. Its strict upper-violation set is convex, but the union over outputs need not be; the mixed Helly identity therefore does not supply the missing error-preserving cover.

## Independent primary-source checks

Read the relevant primary passages, rather than relying on their audit summaries:

- Awerbuch–Kleinberg, Section 2.3, Propositions 2.2 and 2.4: maximum-determinant spanners and optimizer-driven exchanges are established ingredients. Plevrakis–Hazan, published Section 3.3, explicitly combines approximate linear optimization with spanner construction. The manuscript credits both and proves its narrower rational interface locally.
- Lyu–Hicks–Huchette, local preprint Section 3, Proposition 1, PDF pages 7–8: merged breakpoint sets and a common SOS2 interpolation are prior work. The introduction makes that attribution and locates the additional comparison and implicit compilation contributions precisely.
- Kelly–Maulloo–Tan, Section 2, published page 239: the logarithmic objective and proportional-fairness inequality support the maximum-product attribution. The use on a general unconditional body is justified by the manuscript's own first-order proof and rational allocation dependency.
- Ellenberg–Gijswijt, arXiv:1605.09223v1, Theorem 4 and its proof, PDF pages 2–3: the bound is `3 m_{(q-1)p/3}`. Setting `q=3` and bounding the monomial count gives the stated constant with `t=(sqrt(33)-1)/8`. The version-specific theorem locator is correct.
- Averkov–Weismantel, arXiv:1002.0948v2, definition and Theorem 1.1, PDF pages 1–2: the finite-intersection Helly number is `(q+1)2^p`, with the continuous-dimension factor retained in the manuscript.
- Cevallos–Weltge–Zenklusen, local primary full text pages 2–3, and Schade–Sinha–Weltge, pages 3–4: their formulation-size/count setting and convex-hull/optimization contracts support the introduction's distinction from the present graph-sandwich problem. Earlier reviewed GLS actual-body weak optimization and the locally proved log-determinant repair supply the precise oracle dependencies used here.

These are targeted checks of the cited contracts and this stage's claims, not a claim that every result in every bibliography entry was independently reproved.
