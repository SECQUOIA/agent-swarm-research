# Topic 27 declaration coverage

This map was reviewed against the Lean source declarations. It records
semantic coverage, not the outcome of a machine check; actual command results
belong in `VERIFICATION.md`. All names below are in namespace
`QuadraticAggregation`; `System.` names refer to its nested namespace.

| Claim | Declarations and source |
|---|---|
| Q01 | [Model.lean](../../Formal/QuadraticAggregation/Model.lean): `q`, `System`, `System.eval`, `System.homEval`, `System.feasible`, `System.homFeasible`, `System.aggA`, `System.aggB`, `System.aggC`, `System.Certificate`; `System.agg_q`, `System.agg_dot`, `System.agg_eval`, `System.agg_homEval`, `System.aggA_isSymm`. The input already consists of symmetric real matrices, so no abstract-to-matrix bridge is assumed. |
| Q02 | [Model.lean](../../Formal/QuadraticAggregation/Model.lean): `hyperplane`, `System.HHC`, `System.AsymptoticHC`, `hyperplaneLinear_ne_zero`, `ker_hyperplaneLinear`, `System.HHC.asymptoticHC`. [DefinitionsSequence.lean](../../Formal/QuadraticAggregation/DefinitionsSequence.lean): `exists_strictMono_tendsto_atTop_of_unbounded`, `System.AsymptoticHCSequence`, `System.asymptoticHC_iff_sequence`. |
| Q03 | [Model.lean](../../Formal/QuadraticAggregation/Model.lean): `System.agg_eval_neg`, `System.trivial_aggC_neg`. |
| Q04 | [EasyDirection.lean](../../Formal/QuadraticAggregation/EasyDirection.lean): `System.Certificate.convexHull_ne_univ`. Its private helpers `matrixQuadratic_convex` and `matrixQuadratic_not_everywhere_negative` prove convexity and properness of the aggregate strict sublevel set, covering both quadratic and linear nontriviality. |
| Q05 | [Recession.lean](../../Formal/QuadraticAggregation/Recession.lean): `System.convexHull_eq_univ_of_negative_recession`, `System.no_negative_recession`. The first proof constructs two feasible points with the specified midpoint. [Model.lean](../../Formal/QuadraticAggregation/Model.lean): `System.homEval_zero`, `System.dehomogenize_mem`. |
| Q06 | [Hyperplanes.lean](../../Formal/QuadraticAggregation/Hyperplanes.lean): `System.exists_strict_support`, `System.sweep_disjoint`, `System.exists_unbounded_certificates`. [Model.lean](../../Formal/QuadraticAggregation/Model.lean): `System.isOpen_feasible`, `System.homEval_eq_sq_mul_eval`, `dot_dehomogenize`. |
| Q07 | [ConeGeometry.lean](../../Formal/QuadraticAggregation/ConeGeometry.lean): `exists_uniform_cone_separation`, `exists_uniform_infDist_cone_separation`. [ConeClosed.lean](../../Formal/QuadraticAggregation/ConeClosed.lean): `finiteCone`, `isClosed_finiteCone`, `isClosed_nonnegative_span`. [Coefficients.lean](../../Formal/QuadraticAggregation/Coefficients.lean): `System.coefficientCone`, `System.isClosed_coefficientCone`, `System.coefficientCone_smul`. |
| Q08 | [Hyperplanes.lean](../../Formal/QuadraticAggregation/Hyperplanes.lean): `exists_simplex_separator`, `System.hyperplane_certificate`, `System.exists_unbounded_certificates`. The hyperplane restriction is parameterized by arbitrary `x` and `t=(alpha·x)/s`; positive levels give `s!=0`. Nonzero normalized weights follow from their sum being one. |
| Q09 | [SweepBounds.lean](../../Formal/QuadraticAggregation/SweepBounds.lean): `System.sweep_constant_elimination`. [LimitCompactness.lean](../../Formal/QuadraticAggregation/LimitCompactness.lean): `exists_nonzero_psd_limit`. [Headline.lean](../../Formal/QuadraticAggregation/Headline.lean): `System.exists_certificate_of_proper` supplies the continuous linear functional `q_A(x0)+2 b·x0` as the upper replacement for the negative constant. |
| Q10 | [SweepBounds.lean](../../Formal/QuadraticAggregation/SweepBounds.lean): `System.sweep_pair_ne_zero`. [LimitCompactness.lean](../../Formal/QuadraticAggregation/LimitCompactness.lean): `exists_nonzero_psd_limit`. [Coefficients.lean](../../Formal/QuadraticAggregation/Coefficients.lean): `System.certificate_of_coefficientCone`. [Headline.lean](../../Formal/QuadraticAggregation/Headline.lean): `System.exists_certificate_of_proper` constructs a nonzero PSD limit in the actual coefficient cone and therefore a nontrivial certificate directly. This is stronger than merely contradicting the assumption that every certificate is trivial. |
| Q11 | [Headline.lean](../../Formal/QuadraticAggregation/Headline.lean): `System.proper_hull_iff_certificate`, `System.proper_hull_iff_certificate_of_sequence`. Both concern the original real symmetric matrices, strict feasible set, and ordinary convex hull. |
| Q12 | [Headline.lean](../../Formal/QuadraticAggregation/Headline.lean): `System.proper_hull_iff_certificate_of_hhc`. |

The headline has no extra positive-dimension or minimum-constraint-count
premises. It therefore covers the source's positive finite dimensions as
well as consistent zero-dimensional or empty-index boundary cases. The easy
implication needs neither feasibility nor a hidden-convexity assumption.

The proof uses the single compactness route documented in
[SOURCE-REVIEW.md](SOURCE-REVIEW.md). It does not claim to formalize the
source's eigenvalue bound or its intermediate simplex-limit subsequence as
independent results. Lemma 3's uniform distance bound is proved separately;
`ConeGeometry.lean` must be imported and audited explicitly even though the
headline proof does not use it.

Corollaries 1–5, Lemma 4, example classifications, novelty assessments, and
numerical SDP or complexity guarantees remain outside these twelve claims.
