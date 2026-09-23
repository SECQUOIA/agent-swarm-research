# Stage 2 independent review 5

Reviewed `sections/03-soundness.tex`, `sections/04-implementation.tex`, their integration with Sections 1–2, the Stage 2 author report, and the analytic-validation script and recorded output. I inspected relevant `safecut.py`, `convexity.py`, and `vipr.py` code. I independently ran the supplied analytic-validation script with the solver-lab virtual environment; it passed all exact identities and the complete quadratic replay (11 cuts, 39 derivations, bound 1/4). Source hashes matched the report. I made no manuscript or code changes.

## Verdict

**No major issues found.** One minor mathematical qualification should be corrected before proceeding. The safe-cut and proof-transfer arguments are valid under their stated hypotheses, and the exposition provides enough detail to follow the rational and discrete checking obligations without relying on repository notes. The software trust qualifications are appropriately separated from the mathematical theorems.

## Valid minor correction

1. **Minor — state the domain of the quadratic equivalence.** At `sections/04-implementation.tex:49`, “convexity is equivalent to Q positive semidefinite” needs “on all of R^n,” or an equivalent full-dimensional-domain qualification. Earlier sections allow degenerate boxes with fixed coordinates, on which an indefinite quadratic can restrict to a convex function. For example, `q(x,y)=x^2-y^2` is convex on `[0,1] × {0}`, although its full Hessian is indefinite. Suggested correction: “The quadratic is convex on R^n if and only if Q is positive semidefinite; this gives a sufficient test on any certified box.” The implementation's exact fixed-variable substitution and sufficient PSD recognizer remain sound; this is a domain qualification in the explanatory sentence, not a failure of Lemma 4 or the checker.

## Mathematical checks

- Both coordinate-correction tables have the correct signs. With a lower-bounded, upper-unbounded coordinate, the residual must be nonnegative; with an upper-bounded, lower-unbounded coordinate, it must be nonpositive. The interval tests enclose the exact correction and handle fixed/free coordinates correctly.
- The rounding example is correct, including the excluded feasible point, `b=-203/900`, the positive square-completion remainder, and the alternative half-line slope and intercept. It clearly distinguishes a sufficient intercept from the greatest possible one.
- Propagation preserves mixed-integer feasible points even though integer rounding need not preserve the continuous relaxation. The proof uses precisely the needed inclusion.
- The discrete invariant correctly conditions solution-cutoff inferences on the best supplied feasible witness. The subsequent lifting argument makes the bound unconditional on the master, and does not assume that the original master optimum is attained. The unsplit union retains cross-branch dependencies; zero multipliers do not add semantic dependencies. These details agree with the inspected kernel.
- The epigraph/constant-variable extension preserves the normalized objective, so the objective-sense and primal-completion results follow. No nonlinear feasibility is inferred from a master witness.
- The quadratic elimination proof, norm representation, monomial Hessian congruence, negative-exponent Schur complement, and one-variable fractional second derivative are correct. The product-range/curvature distinction prevents a mistaken claim that a nonnegative bilinear product is concave.
- The segment right-derivative bridge is correct. In particular, it does not infer a supporting vector merely from finite coordinate derivatives. The `-sqrt(x*y)` example explains the boundary pitfall accurately. The manuscript openly leaves correctness of the symbolic expression implementation in the trusted computing base, as is appropriate for this unmechanized checker; the theorem's support hypothesis must remain explicit in later formalization and summary claims.

## Scope, prior work, and remaining-stage boundary

The added proofs justify the implemented rules without presenting elementary convex-support inequalities, Hessian tests, or VIPR inference semantics as new theory. The Section 1 comparison remains consistent with these developments: the paper's case is its concrete integration and reliability evidence. The new sections do not establish end-to-end formal verification, and correctly avoid that claim.

The forthcoming formalization, experiment tables, and artifact supplement are still necessary to complete the paper, but their absence is not a Stage 2 defect. In particular, later results must keep historical replay separate from fresh generation, and the supplement must provide the small regression artifacts behind the pinned upstream-checker counterexamples. The current text already identifies the relevant scope and provenance obligations.

The current report supports accepting Stage 2 after the minor domain qualification. It does not independently establish absence of all possible parser or arithmetic-library defects, nor claim a second implementation of the full checker.
