# Certified MINLP: mathematical obligations

This inventory covers the current manuscript's mathematical assertions in
[Section 2](../../../paper-certified-minlp/sections/02-model.tex),
[Section 3](../../../paper-certified-minlp/sections/03-soundness.tex), and
[Section 4](../../../paper-certified-minlp/sections/04-implementation.tex).
It also checks the overlapping contracts in the
[soundness note](../../../notes/certified-minlp-soundness.md) and
[VIPR replay note](../../../notes/certified-minlp-vipr-replay.md).
The manuscript is authoritative where historical review notes describe an
earlier implementation. In particular, an earlier closed proving derivation
can suffice, but all later derivations must still pass.

The inventory separates mathematical coverage from executable correctness.
An entry is discharged only when its actual assertion follows from the cited
Lean declarations. A theorem assuming a support inequality does not discharge
the curvature or differentiation obligation that supplies it. A theorem
assuming every inference is semantically valid does not discharge inference
checking. `COVERAGE.md` records the achieved status of each entry; this file
is the obligation list, not a declaration that the work is complete.

At the start of this work the standalone package had three modules:
`Coordinates`, `SafeCuts`, and `Transfer`. Its existing
[coverage record](../../../paper-certified-minlp/formal/verification/baseline-COVERAGE.md)
covered CM13–CM15, the forward direction of CM16, generic/epigraph portions
of CM02 and CM32, weak-cutoff lifting within CM28, and CM33. It assumed
support and enclosure data and a master inclusion/bound at their respective
interfaces. It did not prove propagation, exact correction suprema or
necessity, curvature recognition, the VIPR invariant, or an executable
inference checker. Existing declarations may discharge unchanged obligations;
the new coverage map must distinguish reused results from new results.

All finite coordinate types are allowed, including the empty type. Boxes may
have fixed coordinates and any combination of bounded, half-line, and free
coordinates. Infinite endpoints are represented by cases, never by real
numbers used in arithmetic. All enclosure conclusions concern real values,
even when the certificate data are rational.

## Model, propagation, and normalization

| ID | Required assertion | Source and material scope |
|---|---|---|
| CM01 | Normalizing upper and lower nonlinear rows preserves their feasible-point meaning; sign normalization converts maximization bounds correctly. | Section 2 mathematical problem; Section 3 transfer. Convexity is required of the normalized function, not inferred from the unnormalized direction. |
| CM02 | The epigraph graph point preserves feasibility and objective; an affine objective constant represented by a coordinate fixed to one occurs exactly once. | Equations `epigraph`, Section 3 transfer; Section 4 master identity. No artificial bound on the epigraph coordinate. |
| CM03 | Pointwise lower bounds imply the lower bound on the extended-real infimum, including the empty feasible set; no attainment assumption. | Section 2 mathematical problem; Section 3 transfer. Real `sInf` alone cannot represent the empty-set convention. |
| CM04 | Exact binary leaf values in the coefficient-aggregation example sum to `-2^-55`; the resulting nonzero negative quadratic is concave and not convex on a nontrivial interval. | Equation `folding-example`. This arithmetic does not verify Pyomo extraction. |
| CM05 | A sign-selected endpoint bounds each affine term, and finite sums give valid lower and upper bounds for the row excluding one coordinate. | Section 3 propagation. Missing endpoints must supply no purported finite bound. |
| CM06 | Each of the four divisions in upper/lower-row propagation gives the stated implied bound, with the direction determined by coefficient sign. | Equation `propagate-upper` and its lower-row counterpart. The divided coefficient is nonzero and the residual bound is justified. |
| CM07 | Integer upper bounds may be rounded down and lower bounds rounded up; exact fixed substitution and binary intersections preserve mixed-integer feasible points. | Lemma `propagation`. These need not preserve the continuous relaxation. |
| CM08 | Any finite sequence of justified tightening/intersection steps preserves every original feasible point; an empty resulting coordinate interval implies original infeasibility. | Lemma `propagation`. No fixed-point or 20-sweep assumption; constant affine rows are tautologies or contradictions according to their exact relation. |

## Corrections, support, and examples

| ID | Required assertion | Source and material scope |
|---|---|---|
| CM09 | The finite-interval exact shift supremum is the maximum of the two endpoint products, is attained, and is nonnegative when the support point belongs to the interval. | Table `shift`; equation `worst-shift`. Ordered endpoints, including equality. |
| CM10 | On a lower half-line the shift has a finite upper bound exactly when the residual is nonnegative; its supremum is the lower-endpoint product. | Table `shift`. A negative residual gives values exceeding every real bound. |
| CM11 | On an upper half-line the analogous necessary and sufficient sign is nonpositive, with the upper-endpoint product as supremum. | Table `shift`. A positive residual is unbounded above. |
| CM12 | On the real line a finite shift bound exists exactly for residual zero, and then the supremum is zero; fixed-coordinate corrections are zero. | Table `shift` and following enclosure discussion. |
| CM13 | All four rational enclosure acceptance tests bound the actual real shift; correction is nonnegative for an enclosed actual residual and a valid support point. | Table `enclosure`; Corollary `enclosure`. Ordered finite enclosures, membership, and actual containment must be explicit. |
| CM14 | Support, residual shift bounds, and a safe intercept imply affine underestimation after finite-dimensional summation, including the affine part of the row. | Theorem `safecut`. The support vector is real; sparse omission means coefficient zero and does not remove that coordinate's residual. |
| CM15 | The rational enclosure intercept test and any valid lower enclosure of the exact safe-intercept expression imply the safe-cut conclusion. | Corollary `enclosure` and outward-evaluation paragraph. Actual enclosure is an explicit premise; interval-library execution is separate. |
| CM16 | An affine underestimator gives a valid feasible-set cut; the converse fails in the stated `x <= 0` versus `2*x <= 0` example. | Section 2 underestimator discussion and Section 3 example following `rounding`. |
| CM17 | Directed slope choices enforce each half-line residual sign, and exact slope matching makes the free epigraph coordinate's residual zero. | Section 3 enclosure discussion. Includes epigraph coefficient `-1` and nonlinear derivative zero. |
| CM18 | The complete slope-rounding example has the stated infeasible rounded cut at `1/3`, residual, correction, safe intercept, strict square-completion margin, largest intercept, and valid half-line alternative. | Example `rounding`. Include the actual finite-box and half-line domains and the optimizing point for the largest intercept. |
| CM19 | Convexity and the stated right derivative along every feasible segment imply the supporting inequality. | Section 4 interval cut replay. A differentiable extension is sufficient; mere finite coordinate derivatives are not the premise. |
| CM20 | The boundary cautions have their stated mathematical content: `-sqrt(x)` has no finite supporting slope at zero, and zero coordinate-direction derivatives of `-sqrt(x*y)` at the origin do not make zero a support vector. | Section 2 support discussion; Section 4 interval cut replay. These are mathematical counterexamples, not assertions about SymPy execution. |

## Discrete proof and transfer

| ID | Required assertion | Source and material scope |
|---|---|---|
| CM21 | The admitted exact row-domination tests imply the claimed row: matching coefficients with compatible direction and a stronger right-hand side, equality-to-inequality, or constant contradiction. | Section 3 discrete soundness. Include all admitted relation directions. |
| CM22 | Signed rational linear combinations preserve their checked relation; nonzero inequality terms must have a common resulting direction, while equalities are unrestricted. | Proposition `vipr-invariant`, rule 3. Zero terms affect neither the sum nor semantic dependencies. |
| CM23 | A rational linear form with integral nonzero coefficients only on declared integer variables evaluates to an integer; the floor/ceiling rounding rules preserve its upper/lower relation. | Proposition `vipr-invariant`, rule 4. Equality rounding is outside the rule. |
| CM24 | Complementary bounds on an integral linear form form an exhaustive disjunction; the two-branch inference preserves exactly the displayed union of dependencies after the respective single-assumption deletions. | Proposition `vipr-invariant`, rule 5. Cross-branch and unrelated assumptions remain. Actual assumption-row identity is required by the checker. |
| CM25 | Original rows, assumptions, and solution-cutoff rows satisfy their respective invariants. | Proposition `vipr-invariant`, rules 1–2. Cutoffs require actual checked feasible solutions and hold on the incumbent-restricted set. |
| CM26 | Induction over a finite derivation with strictly earlier references establishes the full assumption-dependent inference invariant for every admitted rule. | Proposition `vipr-invariant`. A typed/checked inference representation must provide the operational premises; they cannot be replaced by the desired semantic invariant. |
| CM27 | An executable Lean inference checker accepts only derivations satisfying the invariant and validates the whole supplied derivation, including rows after an earlier proving row. | Section 4 proof grammar/arithmetic; campaign scope. Its typed input representation and supported rules must be stated. This does not verify Python parsing or establish that the Python checker implements the Lean checker. |
| CM28 | A finite nonempty list of checked solutions has a best checked member, and its weak incumbent cutoff lifts a restricted bound to every master-feasible point. | Theorem `master-bound`. Cover minimization and maximization; no optimum-attainment assumption. |
| CM29 | An assumption-free proving row yields the unconditional requested master bound; a contradiction with no solution cutoff yields master infeasibility. | Theorem `master-bound`. A proving row need not be last, but every declared row is checked. |
| CM30 | A checked variable bijection, integrality correspondence, exact objective equality, and positive row scaling preserve master semantics. | Section 4 master identity. Include bounds as rows and the fixed-one objective constant; byte identity alone is not the semantic premise. |
| CM31 | Original affine rows, justified propagated bounds, integrality, and safe cuts give an actual feasible extension to the constructed master; its objective is the normalized original objective. | Theorem `transfer`. The composition must connect propagation and safe-cut results rather than assume the final inclusion as an unexplained premise. |
| CM32 | Master lower bounds and master infeasibility transfer through that extension; minimization/maximization signs have the stated interpretation. | Theorem `transfer`. The mathematical infeasibility implication does not enlarge the finite-bound public API. |
| CM33 | A feasible nonlinear witness and a finite objective enclosure give the infimum bound chain and both stated gap inequalities; a matching bound proves attainment and exact optimality. | Section 2 final paragraph; Corollary `primal`. Establish nonemptiness and boundedness before real-infimum use. A master witness is not a nonlinear witness. |
| CM34 | The small incorrect-inference examples are genuinely invalid: a feasible point refutes the million-unit lower bound, and a real point refutes continuous-variable rounding from `x >= 1/2` to `x >= 1`. | Section 4 failures. These claims do not assert that any external checker version accepts the examples. |

## Curvature, domains, and algebraic recognition

| ID | Required assertion | Source and material scope |
|---|---|---|
| CM35 | The four monotone/antitone convex/concave composition principles, sums, signed scaling, and absolute values of affine functions preserve the stated curvature. | Section 4 composition principle. Outer-domain/range containment and convex input domains are required. |
| CM36 | The exponential, logarithm, square root, and real-power composition cases in Table `composition` hold on their stated domains, including continuous zero endpoints where allowed. | Table `composition`. Distinguish powers `p >= 1`, `0 < p < 1`, and `p < 0`; power zero is constant only on its checked domain. |
| CM37 | Even integral powers admit all three stated input cases; positive reciprocal and constant-base variable-power cases satisfy their curvature conditions. | Table `composition`. Include constant base one and power one, affine inputs, and signs of `log k0`. |
| CM38 | A real symmetric quadratic is globally convex exactly when its quadratic matrix is positive semidefinite; negating the matrix gives the concavity test. | Section 4 quadratic forms. Rational off-diagonal coefficients split equally, and restriction to a certified box preserves a global conclusion. |
| CM39 | Positive-pivot square completion gives the Schur-complement equivalence; negative diagonal entries refute PSD; a zero diagonal in a PSD matrix forces that row/column to zero and permits removal. | Lemma `quadratic-recognition`. Include degenerate dimensions and a proof of the zero-pivot necessity. |
| CM40 | Repeated exact rational elimination using those pivot rules terminates and decides PSD. | Lemma `quadratic-recognition`, sentence “These rules give an exact rational test.” A one-step identity alone does not discharge the algorithmic statement. No polynomial bit-complexity claim is made in the source. |
| CM41 | A PSD homogenized quadratic matrix implies global nonnegativity of the quadratic and convexity of its square root as a norm of an affine map. | Lemma `quadratic-recognition`. A real factor need not be rational or computed; include singular matrices and norm origins. |
| CM42 | On the positive orthant, the real-exponent monomial has the stated Hessian factorization with middle matrix `alpha*alphaᵀ - diag alpha`. | Lemma `monomial-recognition`. Actual function derivatives, not just an abstract matrix identity. |
| CM43 | All nonpositive exponents make that monomial convex. | Lemma `monomial-recognition`. Include zero exponents and empty products. |
| CM44 | All nonnegative exponents with total at most one make that monomial concave. | Lemma `monomial-recognition`. Include the weighted Cauchy–Schwarz bound or an equivalent complete argument. |
| CM45 | Exactly one positive exponent with total at least one makes that monomial convex; the supporting block/inverse and Schur identities have the stated values. | Lemma `monomial-recognition`. For `(p,-b)`, cover `p >= 1 + sum b`, the zero-negative-exponent case, and removal of zero exponents. |
| CM46 | Where the positive-exponent monomial extends continuously to the nonnegative orthant, its interior convexity/concavity inequality extends to the boundary. | Lemma `monomial-recognition`. Definedness and continuity are essential; avoid an implicit `0^0` convention change. |
| CM47 | The one-variable linear-fraction decomposition and second derivative are exact; the sign tests imply convexity/concavity on a denominator-sign domain, with constant and constant-denominator cases handled. | Section 4 one-variable linear fractions. Nonzero denominators and `gamma != 0` are needed for the displayed decomposition. |
| CM48 | Rational endpoint bounds for sums, signed scaling, finite products, integer powers, and the stated sign-certified half-line products contain every actual operation value. | Section 4 domain and range enforcement. Four endpoint products are needed in the bounded product case; unsupported cases yield no bound. |
| CM49 | The algebraic/domain cautions are valid: cancellation cannot restore the original quotient's definedness at zero, and `sqrt(x^2) = x` requires the correct sign; nonnegativity of `x*y` does not imply concavity of the bilinear function. | Sections 2 semantics and 4 recognition. Use explicit domains and counterexamples; Lean's totalized division must not erase the expression-domain predicate. |

## Operational obligations and the remaining trust boundary

The following are separately tracked software assertions in Sections 2 and 4.
They are not discharged merely by the mathematical results above. A verified
Lean function gives a formal reference implementation for its typed inputs;
connecting source files and the Python executable to that representation is a
separate obligation.

| ID | Software assertion or execution assumption | Required evidence and formal boundary |
|---|---|---|
| CS01 | Model loading, exact leaf reconstruction, expression identity, domain-before-cancellation checks, and consistent symbolic differentiation. | Source review and focused regressions can support current behavior. No claim that Pyomo, SymPy, or executed Python model construction is formally verified. |
| CS02 | Range/interval arithmetic supplies actual enclosures and extracts final rational endpoints exactly. | Mathematical enclosure rules can be verified; mpmath arithmetic, transcendental implementations, dyadic conversion, and library execution remain separate. |
| CS03 | The Python propagation, curvature recognizer, cut evaluator, serialization, and master matcher implement the proved rules. | A mathematical soundness theorem does not prove refinement of these executables. Include their sufficient-rule rejection behavior in the coverage boundary. |
| CS04 | VIPR parsing enforces grammar, exact counts, token syntax, unique and valid indices, prior references including zero terms, actual assumption rows, witness checks, lifetimes, global-marker checks, and complete EOF consumption. | A typed Lean inference checker does not verify the ASCII parser, python-flint, mutable storage, or the Python implementation. Full end-to-end software verification would require these explicit connections. |
| CS05 | Only complete successful checks return a finite certified bound; partial mode and all error/rejection cases return none. | An acceptance model can prove this policy; executable control flow requires its own evidence. |
| CS06 | Two-pass streaming frees rows only after their actual last use and uses the stated storage accounting. | The finite-array arithmetic is mathematical; the exact 8-byte storage representation, measured memory, parser buffer size, and actual liveness algorithm are software claims. The manuscript explicitly gives no constant-memory guarantee. |
| CS07 | Bundle hashing, frozen replay, process-group timeouts, manifest/resume matching, record completeness, and external-checker corroboration work as described. | These are operational/provenance claims. Stable input contents and trusted execution are assumptions, not consequences of hashes. |
| CS08 | Historical external-checker defects, regression counts, benchmark outcomes, timings, and literature/novelty statements have the reported evidence. | Historical source audits, tests, measurements, and cited literature; no such claim becomes Lean-verified through the mathematical package. |

No claim of certificate completeness, polynomial certificate size, recognition
of every convex function, or universal termination of numerical search is made.
The finite typed proof checker and exact matrix elimination do have their own
termination obligations. Likewise, sufficient cut and curvature rules need not
accept every valid cut or convex expression.

Local validation is limited to the changed topic's modules and supporting
checks. Project-wide verification belongs to CI and is neither run locally nor
queried during this task, as requested by the user.
