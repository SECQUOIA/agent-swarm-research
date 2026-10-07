# Constraint and integer proof review, round 1

The mathematical arguments in Section 5 and Appendix D support C1–C8 and M1–M5 at their stated scopes. I found no blocking theorem error. Five local corrections below are needed before calling the current text journal-ready: a fixed-arc exception in the artificial-flow proof, a graph-size qualification in the flow operation count, two inaccurate statements about lower or upper bounds, and an explicit zero-dimensional branch after substituting fixed coordinates. None changes the claimed algorithms or complexity classes.

This is an internal review dated 2026-10-05. I independently reconstructed the actual manuscript proofs, including their dependencies on Section 3 and Appendix A; I did not treat the favorable prewriting reviews as proof. I read the brief, decisions, models and notation, the constraint author report, and the supplied literature report. An independent child review reconstructed the structured Newton, box-QP, and flow arguments. No manuscript file was edited. No literature search, experiment, mathematical script, project-wide verification, or CI inspection was performed.

The reviewed files were refreshed before this report. Their last-modified times were 2026-10-05 15:16:52 EDT. Locations below refer to that version. The source contracts are assessed against the supplied vetted literature evidence, not newly researched primary sources.

## Required local corrections

### R1. Fixed arcs are included in a false KKT equivalence

Severity: medium, local proof correction; no main-theorem blocker.

Location: `appendices/D-constraints.tex:809–826`, `lem:constraints-artificial`.

The lemma permits capacity intervals `[0,U_e]` with `U_e=0`. Its proof states that optimality is equivalent to a potential satisfying `r_e>=0` at `s_e=0` and `r_e<=0` at `s_e=U_e`. On a fixed arc these force `r_e=0`, which optimality does not require. For example, take two nodes, two opposite arcs with zero capacity, zero demands, and cost `C_e(s)=s` on each arc. The only feasible flow is optimal. Requiring zero reduced cost on both arcs would require simultaneously `pi_1-pi_2=1` and `pi_2-pi_1=1`.

Minimal repair: say that a fixed arc imposes no reduced-cost sign condition, or remove all fixed arcs before stating the three conditions. The residual graph already omits fixed arcs, and their contribution to the concluding convexity inequality is zero because `s'_e-s^*_e=0`. Thus the shortest-path potential argument and the strict exclusion of artificial flow remain valid. The application already substitutes fixed arcs at D:855.

### R2. The flow count omits isolated-node preprocessing

Severity: low, source-contract qualification.

Location: `appendices/D-constraints.tex:790–797`, contract E3c.

The stated `O(m'^4 log m')` operation count is expressed only in the number of arcs although arbitrary node demands are part of the input. A graph with one arc and arbitrarily many isolated nodes requires checking all isolated demands. The literal formula also degenerates at zero or one arc.

Minimal repair: explicitly remove isolated nodes, rejecting an isolated node with nonzero demand, in `O(|V|)` operations; then use the source count on the remaining graph with `log(m'+2)`. Alternatively state only the polynomial operation bound in `|V|+m'` needed by this manuscript. Both preserve the arithmetic Taylor-QP interface. The flow application should include this preprocessing alongside fixed arcs.

For clarity, the application can also state the elementary normalization before using the artificial-cost lemma: substitute `s=x-ell`, replace demands by `b-A_G ell`, capacities by `u-ell`, and a quadratic linear coefficient by `c_e+2a_e ell_e`. This is polynomial arithmetic and is implicit in the existing application.

### R3. An optimal multiplier does have some input-dependent bound

Severity: low, inaccurate explanatory sentence.

Location: `appendices/D-constraints.tex:1313–1316`, proof of `lem:constraints-residual-cut`.

The sentence that the chosen multiplier need not be “bounded by any function of L” is too strong. An independent active support exists. On that support, the multiplier is obtained by applying the inverse rational row-Gram matrix to the optimal gradient. Rational minor bounds, the computed optimizer radius, and the polynomial derivative bound supply a bound in the encoding length of the queried fiber. The proof correctly avoids using such a bound.

Minimal repair: “It need not be rational or unique, and no bound on its norm is used.” This preserves the intended distinction and the complementary-slackness identity that makes the proof work.

### R4. The binary coordinate has a general separation bound

Severity: low, inaccurate explanatory sentence.

Location: `sections/05-constraints.tex:993–997`, paragraph after `cor:constraints-binary`.

The statement that “no lower bound on |p_j| is available” conflicts with the shared algebraic separation lemma. The available general bound can be doubly exponentially small; it does not give the ordinary polynomial precision required to determine the bit from an approximate fiber value.

Minimal repair: “No inverse-polynomial lower bound on |p_j| is assumed, so a prescribed fixed objective accuracy does not certify the bit.” If the paragraph claims failure uniformly for the reduction family, point explicitly to the small-coordinate behavior of the rational optimizer construction. The hardness result itself follows directly from the sign encoding and does not depend on this explanatory sentence.

### R5. Make the reduced zero-dimensional branch explicit

Severity: low, routine boundary case.

Location: `appendices/D-constraints.tex:752–760` and `853–864`, box and flow corollary proofs.

Substituting every fixed coordinate or arc can leave no continuous variable. The transfer proof assumes `n>=1`, and the box procedure's initial maximum is not defined for an empty index set.

Minimal repair: after substitution, state that if no variable remains, evaluate the substituted observable rationally and return the original fixed bounds as active. This avoids invoking either procedure on an empty problem. No new algorithmic ingredient is needed.

## Reconstruction and coverage

| Item | Actual argument and audit conclusion |
| --- | --- |
| C1 | The complete active mask is the nondeterministic witness. Scanning its rows in increasing order supplies a canonical independent row basis. An independent system has a rational identity-block affine chart for every right-hand side; inconsistent extra guessed equalities are rejected by the exact slack mask. The chart map remains strongly monotone with the original modulus. The normal-cone test uses one common polynomial encoding bound over all rational vertices and one shared Newton circuit. Minimizing the approximate circuit objective and then testing the selected vertex's true observable is sound even with zero values and ties. Exactly one mask passes. Complement machines share the same witness and opposite final Boolean tests; empty inputs and invalid checked certificates are deterministic branches. |
| C2 | The supplied slack margin gives an ordinary exactly feasible approximation, hence a correct complete active mask by thresholding. Stationarity on the active affine space gives the unconstrained chart problem. Appendix A explicitly handles a zero-dimensional chart and does not require nonzero multipliers. The margin is an input promise, not derived from the doubly exponential algebraic bound. |
| C3 | The VI arguments use the variational inequality and strong monotonicity, without an objective or symmetry assumption. Existence on an unbounded polyhedron follows by a compact-ball projection argument and an interior solution; uniqueness follows by adding the two VI inequalities. The upper dependency provides a non-gradient warm start by rational residual evaluation and rounded central cuts preserving a fixed ball. It does not silently replace the map by a gradient. |
| C4 | Consistency follows from feasibility of `p_G`. Locality follows because a nonviolated smaller-set solution remains a solution on the larger feasible set, and uniqueness identifies the points. For every inclusion-minimal violator basis, an independent normal-cone support has the same solution and hence the same violators; minimality forces equality with that support. The dimension bound is therefore `rank A` for every subproblem, not merely the final support size. Each primitive enumerates at most `2^r` supports but still solves a map in the ambient remaining dimension; its exponent in L is absolute. Sampling uses polynomial-length row indices and binary multiplicities, and only the expected time is claimed. |
| C5 | Derivative coefficient rows compute the nonlinear kernel exactly. Translation invariance follows from commuting directional derivatives of the quartic part. On every possible independent active chart, splitting `ker(UZ)` eliminates a positive definite quadratic block by rational linear algebra. The residual affine map has full column rank because `UD=YT_0`. Its curvature modulus is the stated determinant/trace bound. A fixed number of matrix operations and degree-four substitutions bounds all coefficient heights by one polynomial with an absolute exponent, uniformly over unknown faces. Singleton QE supplies a gap whose exponent is linear in that height and exponential only in k. Ordinary convex value approximation at the corresponding accuracy recovers every observable sign, including zero, and all slacks. No `L^{F(k)}` step or complex-isolated-critical-point assumption is used. |
| C6 | Adding the two first-order inequalities gives the constrained Newton error at most `Lambda ||x-p||^2/(2mu)` without identifying a face. The warm start is exactly feasible, lies within `1/(2 kappa)` of the minimizer, and induction keeps every iterate in the derivative-bounding box. The KKT singleton formula permits nonunique multipliers and proves separation from the original explicit input. Polynomially many exact QP solves on shared circuits yield the final robust strict, weak, and equality tests. A generic bit-polynomial QP algorithm is not substituted for the required arithmetic solver. |
| C7 | Forest sign conjugation proves positive definiteness of the comparison matrix, but does not by itself supply an admissible vector. The actual construction `d=M(H)^{-1}1`, `v=(H+M(H))d/2` does: the proof gives `d>0`, `v>=1`, and positive principal-system solutions by an invariant-box Jacobi contraction. The pivot proof allows nonnegative slopes, excludes division by zero slopes, processes ties one index at a time, and preserves KKT conditions across degenerate events. Each index moves only lower-to-free-to-upper, so at most `2n` pivots occur. Fresh principal factorizations give polynomial arithmetic cost independent of coefficient expansion. R5 makes the empty reduced case explicit. |
| C8 | The Taylor Hessian is diagonal and positive, so the flow subproblem is a rational separable quadratic flow. Inactive truncation supplies finite printed capacities without changing the optimizer. Endpoint derivatives bound the absolute quadratic derivatives at every optimal flow; `M_0>(N_0-1)C_0` then excludes every artificial arc by strict reduced-cost positivity. Costs and all QP data can be constructed as rational circuits. The vetted source contract is an elementary arithmetic-and-comparison algorithm returning the exact rational optimum, with no hidden root oracle. R1–R2 correct its fixed-arc boundary and graph-size statement. |
| M1 | The unrestricted-fiber selection algorithm is polynomial for every fixed integer dimension. The full-Gram padding explicitly represents all joint tensor blocks; its off-diagonal term is absorbed using the supplied positive Gram margin and the chosen quartic coefficient. The result preserves the minimum and forces the added integer block to zero. This establishes the stated certified hardness padding, not a claim that separability alone preserves a full joint Gram. |
| M2 | The approximate projected gradient has norm error at most `mu/4`. Strong convexity and the unit distance between distinct integer points yield the integer cut with quadratic margin `mu/4`. A linear cut valid at all relevant integer blocks is valid on their entire convex hull; the manuscript correctly declines whole continuous-sublevel separation. For runtime, the answer transcript is valid for a fixed empty target. For completeness, an omitted optimal block gives a fixed singleton target receiving exactly the same deterministic transcript. Thus every optimal block is listed, including all ties. A zero cut implies unique integer optimality. Radius, cut and candidate encoding lengths are charged. The parity midpoint argument proves the sharp `2^t` tie bound. |
| M3 | Infeasible fibers give rational Farkas cuts valid on the projected domain. On feasible fibers, joint strong convexity plus rational primal–dual residuals gives a cut valid for all other integer blocks of no larger value. Complementary slackness bounds the dual slack product by a gradient times the primal displacement, without a multiplier norm estimate. The residual quadratic minimum is attained because the relevant finitely generated cone is closed and its sublevel image is compact. Exact rational convex QP then returns the needed multiplier. The same empty/singleton transcript proof gives every optimum, without Slater or differentiability of the projected value. The initial mixed feasibility cost is kept as `F(t)L^C`. |
| M4 | Product fibers have continuous constraint rank `2r` and curvature at least mu. Their difference observable equals the exact difference of fiber minima. A strict tournament on a lexicographically sorted complete list preserves the first optimal block; additional equality comparisons recover every tie. The number and total length of calls are deterministically FPT-bounded. Conditional expected bounds and linearity of expectation justify the composed Las Vegas time. Nonlinear-dimension selection likewise uses at most `2k` on product fibers and an absolute input-length exponent. Zero-dimensional fibers are rational branches. |
| M5 | The unique rational zero has a nonzero designated sign coordinate. Exactly one binary fiber contains it, proving the known value `1/4`, unique optimal bit, and continuous rank one. The base joint Hessian is at least `3I/2` but lacks a full joint Gram. The added terms vanish on both integer fibers. Their displayed joint Hessian matrix includes every formal basis direction; a Schur-complement bound proves positive definiteness on the full formal vector space, followed by rational congruence back to the original basis. The text correctly says this correction need not retain modulus `3/2` or the original objective square factors. |

The mixed unambiguous composition also passes: the ordinary complete list is computed first, one full mask is guessed for every fiber, and exactly one joint tuple passes all verifiers. The final minimum relation is a Boolean combination of exact chart minima. It does not become a deterministic one-sign reduction merely because the tuple is unique.

The deterministic structured one-sign corollary meets the actual compiler hypotheses. Its operation count and query-description length are polynomial in the original printed input and do not inspect expanded rational values. A clock handles all oracle histories and nonpromised inputs. Appendix A's interpreter validates answer-dependent query strings, enumerates bounded addresses rather than answer transcripts, and evaluates malformed queries as no. Its integer arithmetic/threshold circuit therefore fits the uniform error proof. Strict, weak and equality predicates use different robust final signs. Active masks remain a list of output bits; parameterized construction remains FPT; Las Vegas and nondeterministic algorithms are not compiled away.

## Imported contracts and verification

The source obligations that matter are stated explicitly in the manuscript: GLS 6.6.3 must support circuit-objective LP through elementary rational arithmetic and bounded-range rounding; Basu 2014 Theorem 2.27 must bound integer coefficient height linearly in input height; the rounded GLS central-cut method must preserve the fixed inner ball while keeping query centers short; Végh Theorem 20 must return an exact rational quadratic flow with a uniform arithmetic count; the violator-space theorem must invoke bounded-size bases and supply its reweighting count; and the deterministic integer-query theorem must admit empty and singleton closed convex targets in original coordinates, with uniform oracle answer and query-length bounds. The supplied literature report supports the intended interfaces. The root should retain their exact versions and locators and the R2 graph preprocessing, rather than broaden them from an approximation result or an arbitrary bit-polynomial QP theorem.

Verification here consisted of line-numbered source inspection with `sed`/`rg`, analytic reconstruction, and the independent structured-QP review. The targeted command `git diff --no-index --check /dev/null paper-exact-arithmetic/evidence/reviews/constraints-r1.md` produced no whitespace diagnostics; status 1 records that the new file differs from the empty file. A final `stat` and targeted `rg` refresh confirmed the manuscript version and the unchanged findings. No executable mathematics or CI check supports this verdict.
