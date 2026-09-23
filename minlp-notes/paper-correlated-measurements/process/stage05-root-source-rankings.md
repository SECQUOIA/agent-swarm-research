# New exact source-model ranking development

The coordinator independently developed the remaining exact determinant and
conventional A comparisons rather than retaining their floating-point status.
The complete experiment is in `verification/stage05-root/source_kinetics/`.
Its README specifies provenance, constraints, mathematical conventions and
reproduction commands. The Stage 5 author may copy it verbatim into the
standalone supplement for the five-reviewer gate.

Two independent enumerations give 2,347 nonempty acquisition schedules.
Every local gating difference is checked PSD (160 time/pattern instances),
and both information matrices are SPD for every schedule (4,694 checks).
Exact trace, determinant, and inverse-trace evaluations give 66 unique
formula/criterion/budget optima, compared in 33 pairs. All 11 D and all 11
conventional A choices agree. Only trace at budget 3000 changes, with relative
true regret approximately 0.031128003967883486.

A separate SymPy program, importing no generator functions, builds the full
48-response covariance in a different row order, directly inverts every
selected covariance, and forms the information inverse rather than using
cofactor sums. All 14,082 objective equalities match exactly. It independently
validates every schedule, the total combinatorial count, every ranking and
runner-up margin. Both programs and their outputs are standalone apart from
the checker's declared SymPy dependency.

This develops a stronger verification result on the supplied decimal input;
it does not establish the sensitivity-generation provenance or reproduce
uninspected stored author solutions. The original source files, archived
results and unrelated manuscript were not changed. All new material is to
be assessed in Stage 5's independent review gate.
