# First manuscript review: heights, moments, and Gram certificates

Date: 2026-10-05. Independent GPT Sol review of the actual manuscript, not a
restatement of the source-note audits. Owned review file only; no manuscript
edits. Line numbers below refer to the files read during this review.

## Verdict

**Not submission-ready yet.** I found no false theorem or unresolved internal
proof gap in Section 07 or Appendix F. Their quantitative constructions,
certificate fields, and circuit theorem survive independent reconstruction.
The remaining substantive work is to finish bibliography integration, narrow two circuit-summary
claims, and correct one adjacent field-interface sentence. These are concrete
repairs; none invalidates the height topic or calls for new experiments.

## Findings, in severity order

### Resolved P1 — The essential rational-sampling contract is now confirmed

Locations: `sections/07-heights.tex:302`, `sections/07-heights.tex:655`,
`appendices/F-heights.tex:799` (especially lines 806–810).

The proof of `thm:interior-gram`(a) imports the assertion that every nonempty
open set defined by one strict integer polynomial inequality of degree at
most six and coefficient bit length tau contains a rational point whose
coordinate numerators and denominators have bit length
`tau * 6^{O(n)}`. The witness comparison uses the same assertion at degree
four. This is a **rational-coordinate height theorem**, not merely an
algebraic sampling theorem, an arithmetic-operation bound, or a bound on
coordinate magnitudes.

The application in Appendix F is correct under that exact contract:
positive denominator clearing preserves `{phi > 0}`, `phi(p) > 0`, the degree
is at most six, and the resulting integer coefficient length is polynomial
in L. However, `evidence/literature-review.md:42` supplies general recovery
context without the claimed BPR theorem locator or this explicit contract;
`evidence/authoring/heights.md:124` itself requests verification. I initially
reported this as a pending source-validation dependency, not a finding that
the theorem was false.

Resolution during review: the root relayed Luna's primary-source verification
of BPR 1996, JACM Theorem 4.1.2, printed pages 1031–1032, from the package
`basu1996-on-the-combinatorial-and-algebraic`. For integer polynomials of
coefficient bit length tau and degree at most d, each connected component of
a nonempty strict sign set has a rational point with reduced coordinate
numerator and denominator lengths `tau d^{O(n)}`. This is exactly the
contract used with one polynomial and degree at most six. The mathematical
source dependency and prior prewrite concern 7 are **cleared**. The vetted
bibliography key and final written source report still need integration.

### P1 — Fifteen owned-topic citation keys are absent from the active bibliography

Locations: citations throughout Section 07; `main.tex:43`–44 loads
`references.bib`.

A scoped inventory of the citations in Section 07 and Appendix F found
16 keys; only `SlotSteurerWiedmer2025` occurs in the active `references.bib`.
The missing keys are:

- `BasuPollackRoy1996`, `BorweinWolkowicz1981`,
  `ChuaPlaumannSinnVinzant2017`, `GaertnerMagronVallentin2026`,
  `HeltonNie2010`, `Jiang2021`, `KolmogorovNaldiZapata2024`,
  `Laplagne2020`, `Lasserre2009`, `ODonnell2017`, `PatakiTouzov2024`,
  `PeyrlParrilo2008`, `RaghavendraWeitz2017`, `SafeyElDinZhi2010`,
  `Zhang2020`.

Repair: integrate the vetted bibliography entries into the file actually
loaded by the manuscript, harmonizing duplicate source versions/keys with
Sections 00 and 08. This is routine integration but a submission blocker.
No journal proof should retain unresolved bibliography placeholders.

### P2 — The summary overstates what rational circuits can represent

Locations: `sections/07-heights.tex:39`–44 and 728–738.

“Shared rational circuits remove all of these expanded-size obstructions”
and “The expanded lower bounds disappear when outputs may be shared rational
circuits” sweep in the adjacent irrational optimizer and certificate-field
statements. A circuit using rational constants and rational arithmetic has a
rational value. It therefore cannot output an irrational optimizer, an
irrational maximal-rank optimal Gram, or an irrational exposing matrix whose
entry field must contain the optimizer field. Theorems about short strict
rational witnesses and rational positive definite Grams do not establish a
universal circuit representation for those objects.

Repair: narrow the first passage to the proved strict-feasible-point and
interior-Gram output contracts, and name the rational circle family separately.
For example: “Shared rational circuits give polynomial-size strict feasible
points and interior Gram matrices despite their expanded rational height
bounds. The rational circle optimizers and their moment and exposing matrices
also have short squaring circuits.” Begin the circuit subsection with the
same restricted statement. Algebraic/root circuits may address irrational
outputs, but they are a different declared output model. This concern is
new at manuscript level; prewrite concern 8 is otherwise resolved.

### P2 — The table attributes generic validation hardness to fixed positive families

Locations: `sections/07-heights.tex:802`–804, 814–818, and 833–837.

The table says every row uses the displayed family, then labels validation
of the `g_k` circuit witness as PosSLP-complete and validation of the `h_k`
Gram as PosSLP-hard. Each displayed `g_k` has negative minimum and each
displayed `h_k` has positive minimum; the corresponding constructed witness
or Gram validation predicate is always true on that fixed family. The proof
at lines 774–783 establishes hardness **over arbitrary certified quartic
inputs**, not over the all-yes displayed subfamilies.

Repair: qualify these two cells as “validation over general certified
quartic inputs is PosSLP-complete/hard,” or move the hardness statements to
the prose outside the family-size table. Keep the correct generic reductions
in Section 7.7. This is a scope repair, not a flaw in those reductions.

### P2 — The adjacent field chapter calls a singular full-basis Gram positive definite

Location: `sections/08-fields.tex:106`–109, citing
`rem:heights-gram-field` at `sections/07-heights.tex:198`–203.

The field chapter says the remark gives a “positive definite Gram” over
`Q(sqrt(2))`. The example is `sqrt(2) X_1^2`, which vanishes at zero. It has a
positive semidefinite Gram on the declared full degree-at-most-two basis,
and the scalar Gram `(sqrt(2))` is positive definite only on the reduced
one-element basis `(X_1)`. A positive definite Gram on the full basis
containing 1 is impossible at a zero.

Repair: change the adjacent sentence to “positive semidefinite Gram,” and
prefer an explicit full-basis diagonal Gram in the example if consistency
requires it. The field/SOS obstruction itself is sound. This is an interface
error, already reported to the root for the field owner.

### P3 — D is reserved for polynomial degree but reused for the polynomial Gram order

Locations: `sections/01-models.tex:30`, `sections/01-models.tex:464`,
`sections/07-heights.tex:87`, and throughout Appendix F.

The models reserve D for input polynomial degree and already use N for
`binom(n+2,2)`. Section 07 and Appendix F use D for the latter size. No proof
depends on the letter, but the shared notation is inconsistent.

Repair: use N for the polynomial Gram order in the heights chapter and
appendix, retaining D for degree. This is editorial, not a correctness
blocker.

### P3 — The circle-approximation description accidentally includes the initial non-dyadic point

Location: `appendices/F-heights.tex:440`–449.

The proof sets `hat z_0 = (3+4i)/5`, then says all `hat z_j` have dyadic real
and imaginary parts. The initial point is rational but not dyadic.

Repair: say “For j >= 1, the rounded parts are dyadic; the fixed initial
parts also have constant bit length.” The induction, approximation guarantee,
and bit bound are unaffected.

## Independent proof reconstruction and resolved prior concerns

The reconstruction checked the actual statements and complete proofs,
including the relevant realization proof in Appendix E. The following are
accepted internally, rather than accepted merely because an earlier audit
said they were correct.

- **Taylor identity, strict kernel, and fields.** Integrating the Hessian
  biform yields the coefficients `1/2`, `1/3`, and `1/12`; completing the
  square gives the stated `1/36` residual. The rows representing `d_i` and
  `d_i d_j` span the quadratic polynomials vanishing at the center, so the
  strict Taylor kernel is exactly `R z(a)`. Gradient completion uses
  `A - mu diag(I,0) >= mu diag(0,I)`; translated quadratics, completed affine
  terms, and 1 span the full polynomial space, proving positive definiteness
  when `c_a > 0`. The rational Hessian factorization and binary splitting of
  positive rational weights give actual square factors over `Q(a)` without
  adding square roots. The general-field PSD/SOS distinction is preserved.
- **Cube realization and sharper witness constants.** The exact exposing
  quadratics have the displayed local matrices and only predecessor cross
  terms. With weights `2^{-10(i-1)}`, their total cross contribution is less
  than `0.21` times the weighted squared norm; rational coefficient
  perturbations preserve exact vanishing and meet the quantitative
  realization bounds. Canonical covariance supplies the rational full
  Hessian Gram directly from the rational factors. For every point of the
  closed sublevel set, strong convexity gives radius at most
  `(2+sqrt(6)) delta_k`. The first-coordinate nonzero integer cubic expression
  is less than `16 b^3 M_k^{2-2^k}`, proving the stronger stated denominator
  bound, including every boundary point. The clean bound `log_2 b > k 2^k`
  is valid for every k >= 2. Prewrite concerns 1 and 2 are resolved.
- **Circle denominator and local-conditioning distinction.** The Gaussian
  integer `3+4i` is idempotent modulo 5, so the original terminal fractions
  have reduced denominators exactly `5^{2^k}`. The circle-exposer identity
  has predecessor term `-2 kappa_j (t_{j-1}^T u)^2`. Unscaled weights `8^{-j}`
  provide the claimed positive quadratic margin. In the rescaled chain,
  `||T|| <= 1`, `||J^{-1}|| <= k+1`, and weights `k+1-j` give exposing
  eigenvalues between 1 and k+1. The Hessian at the zero is
  `2 ell ell^T/(epsilon nu^2) + 2(k+1)^2 J^T J`; its bounds are
  `2I <= H <= (8(k+1)^2+1)I`. The extra term is less than I under the
  realization epsilon bound. Powers of 2 cannot cancel the denominator's
  power of 5. The theorem correctly separates exact original denominators
  from rescaled divisibility and keeps conditioning local. Prewrite concern
  5 is resolved. The current introduction also makes this two-family
  distinction at lines 359–365.
- **Moment uniqueness, strict complementarity, and entry fields.** Evaluation
  and the Taylor Gram attain the same value. An optimal moment matrix has
  range in the one-dimensional Taylor kernel; its constant normalization
  fixes it to `ee^T`. All moments through degree four occur as matrix
  entries. Gaussian moments and `Q_* + e_0 e_0^T` give strict feasibility.
  Normalizing the kernel of any rank-N-minus-one Gram over E recovers p in E.
  Rational rows lie in the rational evaluation kernel of dimension N-r.
  Pairing an exposing PSD matrix with `Q_*` forces it to be `c ee^T`; entry
  ratios recover p, and evaluation belongs to the coefficient-map adjoint,
  giving one real facial-reduction step. The rational-system caveat when
  `f_*` is irrational is explicit. Prewrite concerns 3 and 4 are resolved.
- **Long maximal-rank and exposing rational certificates.** The nonconstant
  principal block of a rank-N-minus-one optimal Gram is positive definite.
  Row denominator clearing and Cramer's rule yield the per-entry bound with
  denominator `N^2-1`, as well as the stated sum-of-all-entry-lengths bound.
  Ratios of two exposing entries give `B >= H_k/2`. These statements do not
  extend to the short supplied lower-rank Gram. The sum-of-all-entry
  convention agrees with the rational matrix convention in Section 01.
- **Interior heights and short singular alternative.** Coercivity and the
  nonzero gradient at the cube-chain point give
  `0 < m_k < delta_k^2 <= M_k^{-2^{k+1}}`. Binary splitting of the integer
  multiplier gives a short unweighted rational SOS. The uniform cube moment
  bound is `W_n >= I/(15(n+1))`, controlling every PSD Gram's trace. The
  Rayleigh quotient at the cube-chain point bounds the least eigenvalue;
  squared upper-triangular denominators clear the determinant expansion.
  Taking logarithms yields the exact lower bound in the theorem and its
  `Omega(k 2^k)` total consequence. Singular Grams have zero determinant and
  escape the argument, as explicitly stated. Prewrite concern 6 is resolved.
  The sampling-dependent upper-size argument is correct under
  the now-verified BPR contract above; elimination and binary weight splitting preserve
  the `poly(L) 2^{O(n)}` form.
- **Shared circuit Gram and validation.** The degree-six observable
  `h = f - ||grad f||^2/(2mu)` has polynomial expanded input length and
  `h(p)=f(p)`. The shared Newton lemma applies with the enlarged input
  length, and its uniform gap makes `h(hat x)>0` whenever the minimum is
  positive. Appending the exact completed Taylor formula preserves the
  polynomial identity for every valid input. Its only new divisors are the
  positive rational mu and fixed nonzero constants. A positive definite Gram
  on a basis containing 1 forces an attained positive minimum. The generic
  PosSLP-hardness reduction for PD validation is valid. Weighted SOS circuits
  are asserted only on the positive side, and no unweighted short circuit
  or cheap identity-validation theorem is claimed. Prewrite concerns 8 and
  9 are resolved apart from the summary/table scope findings above.
- **Arbitrary nullvector counterexample.** The two blocks of W are PSD
  simultaneously exactly at `x=sqrt(2)`; `Y(2,0)` is rational positive
  definite with the stated six eigenvalues. Imposing the rational nullvector
  relation on `Y(0,sqrt(2))` forces `t=0`, then the sole irrational feasible
  point. The maximum-rank/common-kernel argument is valid. No rational
  nullvector of an arbitrary selected feasible point is promoted to a
  certificate preserving all real feasible points.

## Exact source contracts for the root to route to Luna

No literature search was performed by this reviewer. The essential
strict-open sampling contract above is cleared. The following attribution/comparison
contracts should be confirmed in the literature evidence or pared back:

1. `HeltonNie2010`, Lemmas 7–8, and `Lasserre2009`, Theorems 2.6 and 3.3:
   the Taylor-integral SOS principle and exact low-order SOS-convex moment
   relaxation with first-moment extraction under the hypotheses being
   credited. The new strict-kernel/field assertions here are proved internally.
2. `GaertnerMagronVallentin2026`, Corollary 1.3: the precise polynomial bit-time
   recovery theorem, including the encoding and role of the supplied positive
   Gram eigenvalue margin. The manuscript must not silently replace
   polynomial dependence on an inverse margin by polynomial dependence on
   its bit length.
3. `Jiang2021`, Theorem 1.6 and Definition 2.6: whether the algorithm's
   denominator parameter is the numerical denominator, its logarithm, or the
   LCM/vertex-complexity encoding. Section 07 line 407 currently identifies
   the parameter with `2^k log_2 5`, so that unit must match the source.
4. `PatakiTouzov2024`: the recalled Khachiyan repeated-squaring system and
   the rank/height comparison; `Zhang2020`, Example 2.5.3: the nonconvex cubic
   local-minimizer comparison through large coordinate magnitudes.
5. `Laplagne2020`, Proposition 3.2 and Section 3.2: real-zero kernel vectors
   and rational/conjugate kernel relations; `ChuaPlaumannSinnVinzant2017`,
   Lemma 1.5: compactness for the declared Gram spectrahedron basis. These
   are background comparisons; the specific kernel and trace claims here
   are proved directly.
6. Harmonize `Lasserre2008`/`Lasserre2009` and
   `ChuaPlaumannSinnVinzant2016`/`ChuaPlaumannSinnVinzant2017` only after the
   cited preprint/published versions and locators are clear.

The manuscript makes restrained, construction-specific contribution claims;
I found no novelty claim based on an unsuccessful search. The all-PSD
certificate-height question remains explicitly open and is not used in any
proved result.

## Scope and checks actually run

Read Section 07 and Appendix F in full; read `main.tex`, `macros.tex`, the
models, the referenced theorem interfaces in Sections 03/04/06/08, and the
canonical-Gram/realization proof in Appendix E. Read the brief, author report,
vetted literature report, the prewrite height audit, and the relevant field
and quadratic-contrast audit passages. Checked the current introduction's
height interface and the dependent block-height theorem in Section 09.

Commands actually run were scoped `nl -ba`/`sed`, `rg`, `wc -l`, a Python
document inventory restricted to the two owned-topic files' references and
citations, and the final document-integrity/whitespace checks recorded below.
The inventory found 51 referenced labels, all defined, and the bibliography
missing-key result in P1. No project-wide verification, CI inspection,
mathematical script, symbolic computation, historical experiment rerun, or
literature discovery was performed. No result here is presented as a CI result.

Final targeted checks: an inline Python read of this review checked its final
newline, trailing whitespace, and control characters (passed, 299 lines before
this results paragraph was added); `git diff --check --
paper-exact-arithmetic/evidence/reviews/heights-r1.md` exited 0 with no output.
The file is new, so the direct Python check supplies its whitespace validation
independently of Git tracking.
