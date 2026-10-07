# Algebraic cone arithmetic: changed-scope R2

Date: 2026-10-05. Scope: the repaired integer-radius proof in actual Appendix L, the source contract it now uses, and all downstream cone dependencies affected by that radius. This supplements the full internal reconstruction in cones-r1.md.

## Verdict and exact versions

Pass. R1 Finding 5 is resolved in the actual manuscript. The primary Khachiyan–Porkolab theorem was sound; the two earlier relays misplaced or omitted quantified-block dependence. Luna's magnified primary-source reread confirmed the original product inside the degree exponent. The manuscript now uses a simpler proof: fixed-block quantifier elimination first, then only the quantifier-free integer-witness theorem. I independently reconstructed that proof from the actual repaired text and the exact source contracts supplied through root.

No unresolved cone proof or source-contract finding remains within this review's scope. This is a scoped manuscript review, not an independent literature search or approval of the entire submission.

Final reviewed SHA-256 hashes:

    L-further-arithmetic.tex:
    eb1b9e925d0299e07f6eed8e742a1e0522789164522bb267b719b2d72a292a74

    J-quadratic-contrast.tex:
    96a543bc359cd7fd25670752d80e35decec486d7865b6d5390eb58f82d15759f

I reread the final L radius paragraph after its last qualifier was added, including \(d_*\ge2\). The final J change adds the vetted Section 5, Theorem 5.1 locator for the classical multihomogeneous Bézout statement; it does not alter a mathematical interface used by the cone proof.

## Revised radius derivation

The exact projection construction remains the one reconstructed in R1: all active affine subsets and rank charts, one common finite perturbation grid whose selected element may depend on \(z\), nonzero-denominator guards, and one fixed radius outside the universal small-parameter quantifier. After reducing field arithmetic modulo the dense input polynomial and adding its one isolated generator variable, the quantified blocks have dimensions
\[
 2,\quad1,\quad h+1.
\]
The individual integer polynomial degrees and coefficient bits are polynomial in \(L\), including the varying dense input field degree \(D\le L\).

The repair adjoins the fixed-zero objective coordinate before elimination. The free set is \(\{0\}\times Y\subset\mathbb R^{t+1}\); it is convex, possibly nonclosed, and has exactly the same integer-feasibility question as \(Y\). The new equality has degree one, no new quantified variable, and a constant coefficient bound. Thus the quantified blocks stay \(2,1,h+1\), while the free dimension supplied to QE is \(\ell=t+1\).

The supplied primary contract for Basu 2014, Theorem 2.27, gives per-output-polynomial bounds
\[
 d_*^{O(n_\omega)\cdots O(n_1)},\qquad
 b_*d_*^{O(n_\omega)\cdots O(n_1)O(\ell)}
\]
for degree and integer coefficient bits. It does not make output count or algorithmic runtime independent of atom count. The manuscript states these distinctions explicitly. The three blocks give
\[
 d'=L^{O(h+1)},\qquad
 b'=L^{O((h+1)(t+1))}.
\]
The implicit constants are absolute for this fixed three-block specialization. The condition \(d_*\ge2\) is now explicit, so affine or degree-one special cases can use a valid upper degree bound.

QE yields an equivalent quantifier-free Boolean formula for the same convex set, rather than an approximation or its closure. Its formula may be very large. Neither the formula nor its elimination is constructed by the feasibility algorithm. Only the effective individual degree and coefficient bounds are used.

The quantifier-free case of Khachiyan–Porkolab Theorem 1.1 has the empty quantified-block product. By the supplied primary contract, an optimal integer point in free dimension \(t+1\) has coordinate-bit bound
\[
 b'(d')^{O((t+1)^4)},
\]
independent of the number of predicates. Minimizing the first coordinate, which is fixed to zero, makes every feasible integer point an optimizer. Hence an integer optimum exists exactly when \(Y\cap\mathbb Z^t\) is nonempty. This remains true for a nonclosed set: no limiting objective argument is needed because the objective is identically zero.

The exponent accounting is
\[
 b'(d')^{O((t+1)^4)}
 \le L^{C_1(h+1)(t+1)+C_2(h+1)(t+1)^4}
 \le L^{C(h+1)(t+1)^4}.
\]
This proves the displayed effective \(B_z\) with an absolute enlarged constant. The fixed-zero coordinate does not introduce a second uncharged factor in the free dimension. The \(t=0\) case continues to skip the integer-radius step.

The repeated-\(d\)-th-power diagnostic in R1 no longer contradicts the imported bound. Its one existential block of dimension \(m\) is first eliminated with degree \(d^{O(m)}\); that degree, rather than the original degree \(d\), enters the quantifier-free witness theorem. The corrected primary direct theorem also charges this dependence inside its degree exponent, but the final paper does not need to transcribe that grouping.

## Affected downstream interfaces

The resulting integer-coordinate bound is the same \(B_z=L^{C(h+1)(t+1)^4}\) used previously. For fixed \(t,h\), integer substitution in the printed box therefore still has uniformly polynomial encoding length. The nonconvex field-radius lemma prints one continuous box meeting every nonempty original fiber. No integer assignment, fiber, projection formula, or QE output is enumerated.

I reread the actual residual epigraph, uniform gap, rational coefficient approximation, cone lift, and outward-rounding proof. They continue to use the original exact system's continuous Hessian span, including every cone sign. The epigraph adds no Hessian direction. All original residuals of a rounded lifted point are strictly below the exact gap; in particular the displayed cone bound remains \(66\Delta/256<\Delta/2\). The final MILP remains rational, with exactly the original integer variables and an unrestricted continuous dimension. Its returned integer assignment has a nonempty original exact fiber; its displayed continuous coordinates need not satisfy the cones.

The repair does not enlarge the input number field or change canonical continuous point recovery. The tuple \((\alpha,x^*)\) still has a relative joint degree bound over the input field and an absolute bound after multiplication by \(D\). It is reconstructed by the actual Appendix J common-field recovery interface at one fixed selected tuple. The representation retains the input generator map and checks its isolator, every original affine row, every squared cone row, and every cone sign. The continuous output degree and length remain \(L^{O(h+1)}\), while runtime remains conservatively \(L^{C_h}\).

For mixed output, the returned polynomial-bit integer assignment is substituted in the original exact field system. Only that fiber's canonical continuous point is recovered. Its input length is charged, and the overall statement remains polynomial for fixed \(t,h\), without a sharp continuous output exponent in the original mixed input.

The rational-original-data threshold and fractional corollaries remain valid. The threshold belongs to the augmented exact system before boxes and gap are derived; a supplied true finite infimum permits an attainment query but does not supply unknown-value computation. The fractional corollary explicitly assumes rational original cone data, uses one field \(\mathbb Q(\theta)\), and encodes \(d>0\) by the reciprocal cone with residual \(4-4ds\) and sign \(d+s\ge0\). It contributes at most one continuous Hessian direction.

The final classifications remain P for the continuous fixed-span and fixed-\(t,h\) conic models, NP for supplied bounded integer domains and fixed span, and no unrestricted unbounded-integer NP assertion. Neither the revised radius nor the output bounds assert FPT.

## Prior findings and source provenance

- R1's cone-lift spacing typo and internal-vertex count correction remain fixed in the actual manuscript.
- The prewrite fractional-field scope correction remains present.
- R1 Finding 5 is superseded by the actual QE-first repair and the corrected primary-source grouping. It was a manuscript/import transcription problem, not a defect in the primary theorem.
- The optional R1 observation that construction time includes an arbitrary rational tolerance's encoding length remains only a general contract clarification. The actual tolerance is explicitly constructed with polynomial encoding length.
- Basu's fixed-block degree/height contract and the quantifier-free Khachiyan–Porkolab empty-block contract were verified by the designated Luna literature lead and relayed through root. This review independently checks their mathematical composition and actual use; it does not claim to have performed primary-source research.

A delegated read-only audit also checked the new zero-coordinate placement, exponent calculation, guards and unbuilt-QE semantics. It found no substantive gap.

## Verification record

I read the full R1 review and current author report, the actual changed radius text, its preceding selected-field projection, and the downstream gap, lift, witness and known-level sections. I inspected the current J locator change and checked the final hashes after the repaired text was present.

Only scoped read-only source inspection and version/document checks were run: rg, cat/sed and sha256sum. No manuscript edits, source research, builds, tests, experiments, CAS, mathematical scripts, project-wide checks or CI inspection were performed in this review. Root's compilation is not counted as a reviewer-run check.

The final repeated sha256sum check matched both recorded hashes. A direct rg check of this evidence file found no trailing-whitespace matches. These are document/version checks, not mathematical verification or CI results.
