# Stage 1, round 1 — independent review 03

Reviewed snapshot: `process/snapshots/stage01-round01`.
SHA256 of its `SHA256.json`: `2230f1e9da9d015278c6bbf424d04167961f6c7911646ca287e899b9ccae36de`.
All five manifest entries were independently verified.

Recommendation: **minor corrections**. I found no major defect in the current model, selection definitions, substitution lemma, or stated compactness distinctions. The three findings below concern the scope of two introductory promises and an incomplete assignment in the coverage inventory. Main theorem proofs, final abstract, and integrated comparison are intentionally later-stage work; their absence is not a finding.

I read all of frozen `main.tex`, `sections/01-foundations.tex`, `references.bib`, `README.md`, and `process/coverage.md`. I did not consult the other current reviewer reports or use historical PASS records as verification. I made no manuscript or snapshot edits.

## Findings

### R03-1 — Minor: restrict the blanket algorithm feasibility promise

**Locator:** `sections/01-foundations.tex:190–191`: “All algorithms report infeasibility separately, and state whether the finite optimum value is attained.” Related assignment: `process/coverage.md:60`, the response-constraint approximation package.

**Problem and evidence:** This is correct for the exact compressed-response algorithms, but “All algorithms” also covers the approximation algorithms assigned later in the inventory. Their promises are deliberately weaker. In `results/bilevel-response-constraint-accuracy-bit-algorithm.md`, Section 4, Theorem 1 can return a point satisfying relaxed upper rows without certifying original feasibility; Theorem 2 reports emptiness of an inner surrogate, which explicitly does not certify original infeasibility (lines 98–104). The exact-feasible approximation corollary additionally assumes finite `V(0)` and a supplied tightening modulus (lines 137–143).

A simple example explains the distinction: minimize `z^2/2` on `[0,1]`, so the true response is `z=0`, and impose the upper row `z<=0`. The original problem is feasible, while every positive tightening of that row is infeasible. Inner-surrogate emptiness must not be presented as original infeasibility. Attainment in the approximation subclass follows under its continuity and compactness assumptions, but the approximation procedures do not universally decide original feasibility and attainment as the exact engine does.

**Requested fix:** Change the sentence to apply explicitly to the exact algorithms in this section. Add, or rely on the following arithmetic paragraph to explain, that approximation procedures distinguish original infeasibility certificates, inner-surrogate emptiness, and relaxed feasible output according to each theorem. This is a local scope correction; it does not require changing any selection definition.

### R03-2 — Minor: carry the numerical-degree qualifier into the output bound

**Locator:** `sections/01-foundations.tex:211–213`: output degree, coefficient lengths, and combined coordinate encoding are “bounded polynomially in the input size in the stated fixed dimensions.” Compare lines 198–205, which correctly separate `L` from numerical degree `delta`.

**Problem and evidence:** The preceding paragraph permits a general bound polynomial in `(L,delta)` and only derives a bound in `L` under an encoding/degree condition. The output paragraph does not carry that qualifier, so read literally it restores a polynomial-in-encoding-length output promise for unrestricted binary exponents. The canonical exact source already contains the counterexample at `results/bilevel-fixed-aggregate-response-algorithm.md:322–327`: `C={x in [1,2]:x^(2^t)=2}`, a trivial positive quadratic follower, and objective `x`. The input has `O(t)` bits but every polynomial defining an extension containing the optimum has degree at least `2^t`, by Eisenstein at 2. Using a nonminimal polynomial or rational coordinate functions does not avoid the field-degree lower bound.

**Requested fix:** Say that these output quantities are polynomial in `(L,delta)` for the stated fixed dimensions, and hence polynomial in `L` under the preceding degree convention. The intended mathematics is already present immediately above; the correction prevents the output contract from losing it.

### R03-3 — Minor: explicitly assign the zero/negative local-curvature boundaries

**Locator:** `process/coverage.md:46` and `:51`, the scalar theorem assignments; stage 5 deliverables at lines 23–27.

**Problem and evidence:** The canonical scalar source is assigned to stage 2 for compression and compactness, and its Section 6 is assigned to stages 4–5 for arithmetic/degree barriers. Neither entry explicitly retains the two different local-curvature counterexamples in `results/bilevel-fixed-aggregate-response-algorithm.md:313–320`:

- With zero local cost, every box point is a follower optimum; upper Boolean quadratic equations and linear clause rows encode 3SAT.
- With negative local quadratic coefficients, minimizing `sum_i z_i(1-z_i)` on the unit box makes the optimum set the Boolean cube; linear upper clause rows then suffice.

These are distinct structural boundaries for the required positive-definite local blocks, rather than versions of the dense-SPD hardness or arithmetic barriers currently named for stage 5. The inventory's general instruction to inspect all negative examples makes eventual inclusion possible, but it does not specify their required treatment as precisely as the other substantive findings.

**Requested fix:** Add them to the stage 5 assignment, either as a short proposition/example pair or with an explicit reason for exclusion. Retain the difference between quadratic upper equations in the zero-curvature example and linear upper rows in the negative-curvature example; make no novelty claim for these elementary reductions.

## Mathematical checks and positive conclusions

- Coordinate bounds with polynomial endpoints on compact `C` give uniform boundedness for each input instance. At each feasible leader, `P(x)` is a closed bounded polyhedron, so the polynomial follower objective attains its minimum. Empty follower fibers are consistently excluded from optimistic, pessimistic, and robust feasibility; `v(x)` is never evaluated there.
- The optimistic definition selects an upper-feasible true global response. The pessimistic definition requires every true global response to obey every upper row before evaluating the worst objective. This matches `results/bilevel-compressed-response-infimum-semantics.md`, Section 2, including the possibility of a nonclosed pessimistic feasible domain.
- Fixed-leader maxima exist because `S(x)` and `S_rho(x)` are compact. This does not imply a leader minimizer. I independently checked the canonical fixed-normal quartic example: `f(x,z)=z^2(1-z)^2+xz` on `[0,1]^2`, upper objective `x+z`. Its worst value is `x` for `x>0` and `1` at `x=0`, yielding an unattained pessimistic infimum of zero. This verifies that the current caution about pessimistic attainment is substantive.
- The fixed-normal optimistic graph is closed by the stated Hoffman argument: along a convergent sequence of feasible leader-response pairs, every competitor at the limiting leader can be repaired into nearby nonempty fibers. The argument requires nonempty fibers along that sequence, not follower feasibility at every leader. Thus the draft's lack of a global feasibility promise is compatible with its intended exact attainment theorem.
- The moving-normal exception is legitimate: in `xz=0` with `x,z in [0,1]` and follower objective `(z-1)^2`, the response changes from `0` for `x>0` to `1` at `x=0`. The fixed-normal Hoffman conclusion cannot be imported into that extension.
- The near-optimal set uses the true nominal global value and includes nonstationary points. Its measurement restriction is properly distinguished from arbitrary polynomial upper data in the exact optimistic model. Inspection of the robust source's fiber argument and criterion-by-criterion elimination confirms why the restriction and separate-witness caveat belong in the foundations.
- The approximation paragraph correctly leaves its leader-domain and data assumptions to its own theorem. The actual base resource sources use rational polytopes and fixed resource normals, which support rational leader recovery. The foundations do not silently extend that recovery to arbitrary compact semialgebraic leader domains.
- The substitution lemma is correct. An input monomial clears to `a*x^nu*prod_i Z_i^gamma_i*D^(delta-|gamma|)`, with nonnegative denominator exponent. Fixed ambient dimension bounds the expanded monomial count polynomially; coefficient lengths remain polynomial under the indicated finite products. Positive `D` preserves inequality signs, including on regimes with zero signs elsewhere.

## Source, coverage, and presentation checks

I inspected the actual scalar and block compression proofs, the infimum/pessimistic source, the robust source's model and Sections 2–5, and the resource/response-constraint approximation statements and relevant proof interfaces. I also read `notes/bilevel-paper-scope.md` and `notes/bilevel-response-complexity-map.md` when auditing the assignment map.

After reading `literature/AGENTS.md`, I checked the fixed-dimensional algebraic tools against the primary extracted source, `[[basu1996-on-the-combinatorial-and-algebraic]] p.3-4` (Theorem 1.3.1 and integer bit complexity) and `p.24-28` (common univariate representations and sample points). The quoted theorem/section locators exist and support the claimed fixed-variable consequences. I checked the fixed-matrix error-bound argument against `[[hoffman1952-on-approximate-solutions-of-systems]] p.1-2`; its proof chooses constants from the normals and uses translation to remove the right-hand side. I did not conduct a new comprehensive bibliographic or publication-priority audit, and I did not independently verify every related-work claim against every original PDF.

The inventory names the intended exact, robust, accuracy, hardness, path, and computational families, including the two distinct path constructions, near-optimal witness field limitations, approximation margin qualifications, negative screening evidence, and the difference between a fixed-price oracle and a complete leader baseline. A path existence check found all 71 explicitly named repository paths in the inspected `results/`, `notes/`, and `code/` families. This check does not certify the content or completeness of later proofs.

The prose is accessible for the intended mathematical optimization reader. The opening explains the structural question before notation; response selection and arithmetic guarantees are separated clearly. The draft avoids claiming that KKT conditions alone establish nonconvex global optimality or that a polynomial bound establishes practical solver performance. No additional prose-accessibility defect warrants a requested change in this stage.

## Independent verification artifacts and limitations

Artifacts are confined to `verification/reviewer03/stage01-round01/`:

- `check_foundations.py` and `checks.json`: manifest validation, explicit inventory path checks, a symbolic substitution diagnostic, the quartic nonattainment identities, an inner-tightening feasibility example, and small-degree irreducibility checks supplementing the general Eisenstein argument.
- `build/`: independent copy of the frozen TeX sources and compiled six-page PDF.
- `build.log`: fresh `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` run. It completed successfully. The final `build/main.log` has no undefined references/citations, warnings, or overfull/underfull boxes. Transient first-pass citation warnings in the combined build transcript were resolved by latexmk's subsequent passes.

The finite symbolic diagnostics do not establish the later asymptotic algorithms. I did not implement general quantifier elimination, audit all later theorem proofs, rerun benchmarks, or inspect every PDF page visually. These are not missing stage 1 proofs: the current review verifies foundations and their assignments while identifying the limited corrections above.
