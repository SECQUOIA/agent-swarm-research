# Stage 4C: nonsymmetric-barrier author audit

Written file: `sections/10a-nonsymmetric-barriers.tex`.
Status: complete and frozen for integration and the required independent review.
I did not edit `main.tex`, shared bibliography, or earlier sections.

## Sources read completely and disposition

- `2026-09-04-pcone-product-barrier-premium.md`: root definition and strictness of h; positive-branch product lemma; arbitrary coupled LH premium; p-order duality branch; restriction to larger blocks; minimum-space consequence; rational SOC no-transfer warning. All retained. Its informal statements about every ambient barrier were corrected throughout to LH barriers where cross-ratios are used. Rational SOC atom-count optimization is not needed for the no-transfer theorem and is subsumed by the already cited exact representation literature.
- `2026-09-04-three-dimensional-pcone-optimal-barrier-frontier.md`: characteristic necessary scale and strict separation; dual-characteristic distinction; nested-log and defining-function failures; bounded-transverse-correction failure; elementary two-LHSC classification and the distinction between nonattainment and a positive infimum gap; endpoint expansions; literature boundaries. All retained. The three-dimensional characteristic integral is subsumed by the proved higher-dimensional integral and exponent. Numerical examples and weaker projective-Dikin bounds are not presented as additional results.
- `2026-09-04-grouped-perspective-p-barrier-newton-frontier.md`: exact duality; scalar and high-dimensional sections; coupled product bounds; canonical upper bounds; full grouped characteristic and p-order comparator proof including derivatives and tails; exact scalar-power partial minimization; scalar multiplier and Hessian-vector formulas; full capped representation ledger with corrected tree atom count. All retained. The phrase computable oracle is qualified by scalar root and inverse evaluation; there is no finite-operation exact root claim. The existential barrier parameter is never paired with the different explicit barrier's oracle.
- Current Section 09d and `audit/root-stage4-preparation.md`: read fully. The global Young construction is referenced, not duplicated.
- Local literature `lee2021-universal-barrier-is-n-self/paper.md`: checked for dimension-parameter existence and its explicit warning that evaluation complexity is separate.

## Independent mathematical work

Recomputed the dual perspective cone from the convex conjugate; verified the diagonal Hölder-dual map. Derived the characteristic Jacobian alpha*s^(r+1), integrated rho and s, and justified differentiated asymptotics for orders 0--3 using the anisotropic integrable dominator. The required inequality is r+1 > 1/2+(r-1)/q. Off-neighborhood tails are integrable because q(r+1+j)>r. Coefficient ratios follow from the homogeneous beta integral, not merely undifferentiated regular variation. Recomputed the p-order cap-volume exponent independently.

Checked the positive-product proof in projective coordinates. The norm-cone p>2 case must dualize the entire same-p product. Scalar power cones instead use the positive branch after swapping their two axial coordinates.

Checked both rational inequalities in the strict characteristic gap, including the sign of the cubic numerator and the logarithmic derivative. Checked the nested-log necessary boundary coefficient and the bounded-correction blow-up. The two-LHSC elementary proof is included only as nonattainment evidence; h(p)>2 proves the stronger infimum statement.

## Primary literature checks (20 September 2026)

- Hildebrand, DOI 10.1007/s10107-012-0576-1, primary full preprint https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf: Theorem 5.4 positive branch and Sections 7.1/7.2 inspected directly. Confirms scalar-power positive branch and norm-cone negative branch for p>2; the proof respects that distinction.
- Hildebrand, Canonical Barriers on Convex Cones, DOI 10.1287/moor.2013.0640: publisher record and author's publication list confirm MOR 39(3) (2014), 841--850 and dimension bound. No efficient evaluation assertion is made.
- Roy--Xiao primary author PDF https://www.microsoft.com/en-us/research/wp-content/uploads/2018/01/powercones-5a71024933c4b.pdf confirms Euclidean-output generalized power cones. DOI endpoint failed, but author source and preparation audit supply the publication metadata. This theorem is expressly not transferred to lp-vector outputs.
- Pirau--Hildebrand, DOI 10.1007/978-3-032-15791-1_5, publisher page directly confirms LNCS 16426 (2026), 65--75, and explicitly states optimal parameters for three-dimensional power and p-norm cones remain unknown. Related primary arXiv:2507.01812v1 was inspected; it concerns a convex relaxation of barrier design, not an exact optimum.
- Glineur--Terlaky and Chares are credited for the grouped cones, scalar barrier, and partial minimization. Existing `Chares2009` is used; Glineur--Terlaky metadata matches the preparation audit. Direct DOI endpoint failed in this session.
- `ChenGoulart2025` was added by the parent and is cited for established sparse-plus-low-rank nonsymmetric Hessian structure, without priority claims for the specialization.

New bibliography entries are supplied separately in `audit/stage4c-barriers.bib`. Existing keys used: Hildebrand2013, Chares2009, Wang2024, LeeYue2021, ChenGoulart2025.

## Validation

A standalone syntax build with pdflatex succeeded (six pages), with no overfull or underfull boxes. Expected missing cross-reference and bibliography warnings arise in that isolated syntax build; the integrated manuscript must resolve them with the shared bibliography and earlier sections. Build files reside only in `/tmp/stage4c-barriers-check*`.

The section explicitly preserves the classical unresolved exact optimal-barrier question. This is a limitation of the available theorem, not a conjecture silently used in a proof or a promised result left incomplete.
