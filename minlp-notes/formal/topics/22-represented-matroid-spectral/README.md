# Represented-matroid spectral approximation sets

Status: complete within the [37 frozen claims](CLAIMS.md). Independent
reviews and all targeted checks passed: 65 Lean modules, a 1,680-declaration
axiom audit, three execution examples, and 65 individual kernel replays.
See the [verification record](VERIFICATION.md) and [final review](REVIEW.md).

Topic 22 concerns an explicit rational representation of a matroid, rational
PSD information matrices attached to its elements, a rational PSD prior,
and rational accuracy `0 < eta < 1`. The mathematical headline constructs actual
matroid bases that cover every attainable information matrix in both
relative PSD directions. Singular matrices retain exactly their kernels.
The information dimension `p` is fixed; the matroid rank `q` may grow.
Both output size and charged Turing bit work are proved polynomial in the
complete encoded input and `1/eta`.

- [Frozen claims](CLAIMS.md).
- [Independent source inventory and implementation risks](SOURCE-REVIEW.md).
- [Primary source note](../../../notes/research-20260912-represented-matroid-psd-approximation-set.md).
- [Historical mathematical review](../../../notes/research-20260912-represented-matroid-psd-independent-review.md).
- [Related paper](../../../paper-correlated-measurements/README.md).

The completed [DAG spectral package](../21-dag-spectral/README.md) supplies
generic rational factorization, normalization, spectral perturbation, and
criterion results. Topic 22 connects them to the represented-matroid
producer. Its new proofs include exact attainable-profile detection,
deterministic interpolation, recovery of actual bases with the original
rank preserved, and polynomial arithmetic at growing matroid rank. Merely
assuming a profile oracle or enumerating all bases does not establish the
algorithmic theorem.

The determinant profile algorithm is established work of Berstein et al.
The scope excludes priority claims, practical runtime claims, arbitrary
independence-oracle or finite-field inputs, matroid intersection, and
arbitrary simultaneous path and matroid constraints. Only targeted local
verification belongs to this work; project-wide verification remains CI's
responsibility.

The original-input entry point is
[`representedSpectralCover`](../../Formal/MatroidSpectral/Headline.lean).
`representedSpectralCover_complete` states the two PSD inequalities and exact
kernel/range preservation for every original column base.
[`representedCover_select_D`, `representedCover_select_E`, and
`representedCover_select_A`](../../Formal/MatroidSpectral/HeadlineCriteria.lean)
provide successful exact selectors, with additional rational contrast selectors.
The counted producer is
[`representedInputRun`](../../Formal/MatroidSpectral/InputExecution.lean).
`representedInputRun_value` identifies its result with the headline cover;
`representedInputRun_polynomial_work` gives the complete cost bound from
original input dimensions and encodings, with no assumed oracle or
continuation-cost bound.

The implementation uses one forced-owner profile coordinate instead of
constructing a contraction. Exact coefficient positivity, tensor Lagrange
interpolation, and one-pass deletion recover actual bases while preserving
the original rank. Variable-size determinants use cached division-free Bird
iterations. Uniform, partition, and graphic representations include explicit
base equivalences; graphic inputs allow labelled parallel edges and loops.

Cost proofs use the stated schoolbook arithmetic and finite scan/storage model.
They describe the arithmetic algorithm, excluding construction of proof and
cost-observer transcripts, and do not assert Lean wall-clock performance.
The polynomial degree depends on fixed information dimension; the result does
not assert fixed-parameter tractability or practical solver performance.

- [Claim-to-theorem coverage](COVERAGE.md).
- [Representation and recovery review](REVIEW-REPRESENTATION.md).
- [Algebra and graphic review](REVIEW-ALGEBRA.md).
- [Interpolation review](REVIEW-INTERPOLATION.md).
- [Cardinality review](REVIEW-CARDINALITY.md).
- [Criterion and subclass review](REVIEW-CONSEQUENCES.md).
- [Execution and complexity review](REVIEW-COMPLEXITY.md).
