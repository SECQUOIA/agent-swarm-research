# Stage 2 correction record

Correction agent: `stage1_fixer`, distinct from `stage2_geometry_author`.
Date: 2026-09-07. All five reports `reviews/stage2-r1.md` through
`stage2-r5.md` were read. No reviewer identified a major issue; the
coordinating author accepted all three minor findings below.

| Finding | Correction |
|---|---|
| Reviewer 2: standalone wording | The directed-exit introduction now says “A center-dependent chord construction”; development history remains in internal notes. |
| Reviewer 3: parameter ambiguity | Defined the inverse gap map μ_F and separate gap functions x̂_F, Ĥ_F, κ̂_F in `02-setup.tex`. Updated the rate corollary and canonical constants consistently, retaining x_F(μ) for the barrier-parameter path and H_F(x), κ_F(x) for pointwise objects. The canonical display explicitly relates g and μ. |
| Reviewer 5: tighter spectral intervals | Both radial and directed-exit bounds now use the plus profile in the lower denominator and the minus profile in the upper denominator. The proof applies the lower Rayleigh estimate to the minimum-over-dimension formula and the upper estimate to the maximum-over-codimension formula, displaying both reciprocal transformations. |

The width definitions, original ordering, endpoint identities, hypotheses and constants
are unchanged. The immediate reverse comparisons w_j^-≤2Cw_j^+ and
v_j^-≤Cv_j^+ are also stated and follow by combining the tighter bounds.
The tighter bounds follow from the same pointwise inequalities;
no extra theorem assumption or novelty claim was added. The author notes now
record the final notation and intervals for subsequent section authors.

Verification: `make -C conditioning-paper` passes. The final log has no
undefined references/citations, warnings, or overfull/underfull boxes. A source
search confirms that authored sections no longer use unhatted gap-path
notation. No original manuscript or `central-path-cost/` file was modified.
These minor corrections are ready for the coordinating author's check; the
accepted process does not require a further five-reviewer round.
