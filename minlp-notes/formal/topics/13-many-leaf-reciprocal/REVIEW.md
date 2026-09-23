# Many-leaf reciprocal hull: review record

Status: complete. Independent reviews cover the full mathematical claim list,
including the executable membership/separation oracle, graph-witness producer,
and their stated arithmetic and bit-work models. All findings are resolved.

| Review | Scope | Record |
|---|---|---|
| Core mathematics | Actual graph hull, constructed least law, support counts, normalization, one-leaf specialization, and exact example | [Core review](REVIEW-CORE.md) |
| General probability and cuts | Arbitrary supported laws, quantile attainment, Fubini, endpoint domination, rational affine cuts, and completeness at real candidates | [Probability and separation](REVIEW-PROBABILITY-SEPARATION.md) |
| Fast envelope and evaluation | Executable sorting, parallel-line elimination, stack invariants, clipping, exact integration, arithmetic counts, and bit-work model | [Algorithm review](REVIEW-ALGORITHM.md) |
| Complete oracle | Actual rational cut production, every rejection branch, global validity, acceptance equivalence, and dispatch accounting | [Oracle review](REVIEW-ORACLE.md) |
| Rational graph witnesses | Candidate-to-witness construction, all moments, sharp support bound, reduced-fraction size, and executable construction boundary | [Rational witness review](REVIEW-RATIONAL-WITNESS.md) |

Review produced concrete changes. The general-law endpoint domination was
made explicit. Envelope clipping now counts both computational traversals,
and evaluator accounting includes coefficient negation and setup arithmetic.
Oracle accounting includes the second envelope construction when producing a
lower-bound cut. Rational witness existence is distinguished from the connected executable
producer. The completed producer emits all graph coordinates, proves their
moments, and supplies the full operation and bit-work bounds required by MR41.

The final complexity statement uses an explicit schoolbook arithmetic cost
model, with rational operand bounds and a counted Euclidean reduction.
It does not verify the compiled Lean rational backend or the Python script.
This distinction is part of the verification scope, not an empirical runtime
claim.

The root agent also checked the complete checker, oracle, and graph-witness
output by kernel reduction on the exact example and boundary branches. Actual commands and
final package checks belong in [VERIFICATION.md](VERIFICATION.md).
No review ran project-wide verification or inspected CI.
