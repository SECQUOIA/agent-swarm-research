# Independent Stage 1 review — reviewer 1

Reviewed: 2026-09-07. This review concerns the inventory, research direction, literature positioning, bibliography and scaffold. It does not certify results that have not yet been written.

## Decision

**No major issues identified.** The proposed core development is mathematically plausible, the scope is coherent, and the plan correctly treats its stronger assertions as proof obligations. The newly identified Xiong–Freund antecedent materially improves the novelty audit. The classical attribution of the degenerate-LP endpoint result is appropriate.

## Minor finding requiring a planning correction

**MINOR 1 — Apply the compactness/relative-interior audit explicitly to any retained Netlib instance.** The inventory requires numerical accuracy and disclosure of data transformations, but its explicit compactness warning is attached only to examples in the degenerate-LP note. The survey solves presolved standard-form systems with nonnegative variables and no general upper bounds (`scripts/netlib_conditioning_survey.py`, the optimization calls near lines 28–31). Such a representation is not automatically compact, nor is strict feasibility automatic before facial/presolve reductions. The original survey's slope fits do not establish these hypotheses. Add an explicit Stage 5 obligation to certify the hypotheses for each numerical instance used as evidence for the theorem, prove an applicable compact-sublevel extension, or label the computation as outside the theorem's verified scope. If a box or a face reduction is used, identify the resulting feasible representation and metric. This is a minor omission in the plan, not an assertion that the existing datasets necessarily violate the hypotheses.

## Independent checks and findings supporting acceptance

1. **Difference-body direction.** Let the tangent Dikin ellipsoid be centered at the origin. For any vector in its closed unit ball, choose the sign with nonpositive objective change. Dikin containment and passage to the boundary show that the corresponding endpoint and the central point belong to the same closed sublevel. Their difference contains the original signed vector because the difference body is symmetric. Thus the proposed inner inclusion is valid. Asymmetric containment supplies the outer inclusion by the triangle inequality. This supports the proposed equal-gap comparison; the proof must still spell out the constants and the reversed order between ellipsoid inclusion and positive-definite forms.

2. **All-barrier upper rate.** Homothety of a fixed relative interior ball about an optimum puts a ball of radius `r g / Delta` inside the sublevel, for the appropriate objective range `Delta` and range of `g`. Its difference body contains the origin-centered ball of twice that radius. The proposed outer difference-body containment therefore bounds the largest Hessian eigenvalue by the stated order `g^{-2}`. Together with the original smallest-eigenvalue lower estimate this supports the stronger all-barrier condition-number law. There is no evident counterexample to this direction under the compactness and fixed-metric assumptions.

3. **Approximate-gap transfer.** The proposed estimates have a valid geometric basis. Dikin containment gives the dual local norm of the projected objective at most the exact center's primal gap. A displacement of local norm at most `r` changes the gap by at most `r g`. Homothety about a fixed optimum proves `D(t g) <= t D(g)` whenever the compared sublevels are defined. The later theorem must retain the strict `r < 1` condition and the appropriate local Hessian comparison.

4. **Coverage.** The inclusion of the later degenerate-LP limiting spectrum resolves a real gap in the original conditioning/spectrum package. Excluding full oracle lower bounds, local-metric iteration lower bounds, contact sensitivity and the SOCP preconditioning algorithm is consistent with the selected topic. Section 5 of the original manuscript principally concerns normal equations and quantum filtering, so its omission as a full section does not create an evident topical completeness gap.

5. **Primary-source comparison.** I independently opened Xiong–Freund's [July 2024 primary PDF](https://optimization-online.org/wp-content/uploads/2024/06/arXiv_0715.pdf), especially Fact 5.2 and Remark 5.1, and its [arXiv record](https://arxiv.org/abs/2406.01942). These explicitly connect primal–dual sublevels, self-concordant containment and Hessian eigenvalues. They therefore justify the plan's warning against claiming the first such geometric connection. The displayed statements do not themselves assert the proposed equal-primal-gap comparison of two different tangent primal barrier Hessians. The plan appropriately requires a precise final comparison rather than assuming novelty from differing application areas.

6. **Literature honesty.** The proposed qualified wording correctly distinguishes a new theorem formulation from standard proof tools. The sharper asymmetric-containment constant is appropriately withheld pending a primary verification or direct proof. The current scaffold makes no premature theorem or novelty claims, and the bibliography distinguishes the two Wright authors and the online versus issue year for Waki–Muramatsu.

## Checks reserved for subsequent stages

The oscillatory barrier is a reasonable lead, but its complete self-concordance and barrier-parameter bounds must precede any claimed sharpness result. The singularity-degree SDP needs the promised analytic verification and exact normalization of its four eigenvalue scales. None of these unfinished tasks is a defect in a clearly marked planning stage.
