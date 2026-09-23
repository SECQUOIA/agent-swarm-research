# Stage 3, round 2 — independent reviewer 4

**Verdict: PASS on mathematical substance; one required minor abstract clarification. No major issue remains.**

I verified all 18 frozen input hashes and reviewed the repaired `sections/05-algebraic.tex`, full `appendices/arithmetic.tex`, new checker, abstract, bibliography, and the stage-3 correction report. I rechecked the structural and numerical dependencies against the previous frozen stage; structural text is unchanged and the numerical change correctly fixes D's copy description. I did not read another reviewer's round-2 report or edit the manuscript.

## Required minor correction

**m1 — Retain the coefficient field in the abstract's sharp characterization.** In `main.tex`, change “rational equivalence holds precisely for compact basic closed sets” to “rational equivalence holds precisely for compact basic closed sets over Q.” The formal theorem states the correct field restriction, but the unqualified abstract wording is broader: for example a singleton containing a transcendental real is basic closed over R and cannot satisfy the stated rational-data/rational-equivalence conclusion. This is an abstract scope clarification, not an error in the theorem or proof.

## Resolution of the prior major finding

The manuscript no longer relies on the invalid Boolean normalization to claim unrestricted rational universality. It proves the conjunction-only construction directly, gives a necessity argument for basic closedness, provides a correct explicit obstruction to the former unrestricted claim, and separately retains semialgebraic topological universality. The source-warning appendix accurately distinguishes the source transformation's preservation of existence from its failure of unique extension. The previous major finding is resolved.

## Independent proof audit

### The bounded arithmetic appendix

The integer polynomial circuit uses only deterministic arithmetic and globally imposed output conditions. Zero and negation are uniquely defined, and the circuit's solution set is the graph of a polynomial map over the original compact basic closed set. Thus a finite M bounding every circuit value exists. The scaled multiplication equations `w_x w_y=q` and `epsilon w_z=q` are equivalent to the original product because epsilon is a fixed positive rational. Both directions and uniqueness are valid. The q coordinates satisfy the stated small range, and this fact is inferred from recovered original solutions; it is not an extra restriction that could discard points.

I independently derived each shifted identity. The two coordinate equations give A_s=1+s, B_s=3/4+s, C_s=3/2+s. The shifted addition is exact. In the shifted product, substitution gives h=3/2+s+st, so B_u+B_s=h forces u=st. The built-in lower bound on J_s in J_s+1/2=A_s forces precisely s>=0; the other bounds admit all intended small nonnegative values.

The delta constant is genuinely encoded with allowed operations: the fixed positive solution of c_1^2=1 gives one, additions fix the displayed half/integer constants, midpoint recurrence gives D_i=1-2^-i, and A_d+D_ell=2 forces d=delta. The halving chain fixes epsilon, including k=0. There is no arbitrary rational constant being silently admitted to the final ETR-INV alphabet.

The product-from-squares identity simplifies exactly to ab. Its base values at (a,b)=(1,1) are strictly inside [1/2,2], and the three squared inputs approach one. The reciprocal chain has central value h=1/(a(a+1/2)); hence its last output is exactly a^2. I checked the actual base-value list, including 5/6, 4/3, and 7/4; none is at an interval endpoint or a reciprocal pole. These calculations were independently confirmed with symbolic factorization, rather than relying solely on the finite checker.

The nested continuity choice is rigorous: first select the reciprocal gate's neighborhood, then a product neighborhood whose squared inputs enter it, then delta small enough for the shifted gate inputs. There are finitely many gate types, so the same neighborhoods apply to arbitrarily many occurrences. The midpoint/halving constants already have exact ranges. The proof does not need an explicit quantitative bound because the lemma asserts existence without an input-size bound.

The reverse argument is also sound. Every final equation forces its gate identity whenever the reciprocal inputs are nonzero, which follows from final positive bounds. It therefore recovers the scaled circuit; compactness of the original set then supplies the intended small ranges for every recovered solution. This prevents unintended bounded solutions outside the chosen local neighborhoods from becoming spurious source solutions. Every auxiliary is uniquely determined in both directions, and the designated original coordinate is retained as A_(w_t)=1+epsilon*t. Empty sets and zero-dimensional source space cause no substantive exception.

### Basic closedness and the obstruction

The invariance proof includes both forward denominators and the cleared numerators of inverse denominators after substitution. All are nonzero on compact S, so a common strictly positive rational lower bound exists. Squared denominator guards make every rational expression well defined at candidate ambient points. Membership F(t) in T and the identity G(F(t))=t can then be expressed by polynomial equalities and weak inequalities using positive even powers for clearing. The converse argument uses that G maps the entire T into S; it therefore excludes extraneous ambient points without assuming an identity outside the original domain. This proves necessity over Q exactly as stated.

The local three-quadrant obstruction is valid. A lowest nonzero homogeneous part must be nonnegative on all included quadrants. An odd degree would force it to vanish on an open quadrant by antipodal symmetry, which is impossible for a nonzero polynomial. Even degree propagates nonnegativity into the excluded quadrant. A direction avoiding finitely many nonzero zero sets then makes all active lowest forms strictly positive; for sufficiently small radius every defining inequality holds on an excluded ray. Constants and equalities are handled correctly. Thus the restriction to basic closed sets is substantive, not just a conservative repair.

Combining the proved arithmetic lemma with the accepted electrical construction gives the stated iff theorem and all simultaneous graph restrictions. Compositions retain nonvanishing rational denominators on their actual domains.

### Topological universality and algebraic singletons

I independently checked the primary [Ohmoto–Shiota v2 text](https://arxiv.org/html/1505.03970v2), Theorem 1.1 and Section 1.2. It supplies semialgebraic triangulation and explicitly identifies the compact case with a finite complex. The manuscript only needs this topological fact, not its additional C1 regularity.

For a finite complex, the nonface product equations together with nonnegative barycentric coordinates and total sum one select exactly the face supports. This is a compact basic closed set over Q. The simplexwise affine map into a geometric realization is bijective and agrees on common faces, hence gives the required semialgebraic homeomorphism. The proof correctly avoids rationality and polynomial-size claims for the general triangulation.

The singleton algebraic construction now depends on the independently proved arithmetic lemma. Its forward coordinates lie in Q(alpha), its designated scalar-affine recovery gives equality of the designated coordinate field, and all electrical transformations preserve that coordinate and unique extension. Rational alpha, all prescribed degrees via Eisenstein, AC magnitude uniqueness, and reference-fixed rectangular uniqueness are correctly handled.

### Structural and numerical dependencies

I rechecked the simultaneous planar/connected/bipartite/unit-conductance/girth construction and its use in the repaired theorem. It requires polynomial-time bounded ETR-INV input only for the hardness theorem; the appendix's purely existential scaling for arbitrary basic closed sets is not misused as a polynomial-time claim.

The two-sided residual constants, the exact infeasible recurrence family, JPT epigraph application, promised rational certificates, and reactive stability estimates remain correct as assessed in the first review. The text no longer calls D's weight-two x neighbor two separate copies. The revised algebraic scope does not affect any of these arguments. The conditional NP statement continues to follow from the original independently sourced ETR-INV hardness, not from universality.

## Verification evidence

Artifacts are under repository-relative `paper-power-flow/verification/reviewer4/stage03-round02/`:

- `manifest-check.log`: all 18 frozen SHA-256 hashes agree.
- `arithmetic-check.log`: 1,681 composed product/reciprocal profiles; the full 332-variable, 330-equation disk circuit on 49 valid, 72 outside, and 49 inconsistent profiles; nine constant-chain configurations including k=0; and 35 simplex-support profiles all passed. The checker evaluates final allowed equations and actual variable bounds and does not mistake samples for a quantified proof.
- `symbolic-check.log`: independent exact symbolic factorization confirms product-from-squares, the reciprocal square core, the full square output, and shifted-product identities. A preliminary direct `cancel` equality test did not normalize one nested reciprocal fully; factoring the exact expression produced zero. This was a symbolic normal-form issue, not a failed mathematical identity.
- `build.log`, `build/`, and `manuscript-layout.txt`: the frozen manuscript builds to 24 pages in a separate output directory, with no final warnings, undefined references/citations, or overfull/underfull boxes. Compiled text was extracted for checking.

No further mathematical correction or optional development is necessary for stage closure in my judgment. Correct the abstract's field qualifier, and this stage can be accepted without another major-issue review cycle.

Artifact packaging note: the review artifacts were relocated byte-for-byte from the repository-root `verification/reviewer4/` directory into `paper-power-flow/verification/reviewer4/`. Historical command and build logs retain their actual original paths.
