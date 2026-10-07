# Independent review of the completed lower-reductions manuscript

Reviewed 2026-10-05. Scope: `sections/04-reductions.tex` and
`appendices/B-reductions.tex`, against the actual contracts in `main.tex`,
`macros.tex`, `sections/01-models.tex`, `sections/03-upper.tex`,
`appendices/A-upper.tex`, `sections/06-algebraic.tex`, and
`appendices/E-algebraic.tex`. I also read the relevant Taylor-SOS and
interior-Gram statements and proofs in Section 07/Appendix F, the brief,
the reductions author report, and the vetted literature report. The prior
prewrite review was supplementary; the proof assessment below reconstructs
the completed manuscript itself.

This is an internal analytic review, not external peer review. No literature
discovery, source browsing, computational experiment, or mathematical script
was run. Two independent delegated analytic checks covered the cube-root
compiler/comparison proof and the quaternion compiler/realization. No
manuscript file was edited.

## Readiness and findings

No theorem-blocking defect was found in the reductions. The signed odd-root
and quaternion realizations satisfy the actual quantitative realization
lemma, including its requirement of positive definiteness on the entire
Hessian-Gram coordinate space. The min-sign perturbation, nonzero-value
promise, rational-optimizer promises, and strict/weak completeness
substitutions are valid. Equality is correctly given only an upper bound.

The proof chain is ready for integration after the local text corrections
below and completion of the specific source-credit checks. These corrections
do not require another construction or a computational experiment. This
assessment does not certify unrelated chapters or publication priority.

Severity: **P1** would block a theorem; none found. **P2** identifies a false
or insufficiently sourced statement to correct before submission. **P3** is
a minor encoding or wording correction that does not affect the result.

1. **P2 — Qualify the block-sum Gram obstruction.**
   `sections/04-reductions.tex:712–716` says that the block sum in
   Proposition `prop:reductions-sums` has no positive definite full Hessian
   Gram. The proposition permits one summand, and in that case its certificate
   is precisely the positive definite certificate supplied by
   `thm:singleton-field`. The empty-list fallback `z^2+z^4` also has the
   positive definite Gram `diag(2,12)` on `(v,zv)`. The obstruction is valid
   when at least two nonempty variable blocks are present: a cross monomial
   `x_j^2 v_i^2`, with `x_j` in one block and `v_i` in another, has coefficient
   zero and arises only from the diagonal Gram entry for `x_j v_i`, which
   therefore vanishes. Repair: say that the block sum has a rational PSD
   Hessian Gram, and that **with at least two nonempty blocks** it has no
   positive definite Gram on the full basis. No change to A1 is needed.

2. **P2 — Restrict the explanation after the naive-lifting example to this
   construction.** `sections/04-reductions.tex:220–222` says that “only a
   quadratic whose own quadratic part is positive definite can dominate”
   indefinite squared quadratics far from the zero. This is too broad as a
   necessity claim. The identity
   `(x^2-y^2)^2+(2xy)^2=(x^2+y^2)^2` gives a globally convex quartic even
   though both displayed quadratic matrices are indefinite; adding
   `x^2+y^2` makes it globally strongly convex. Repair: explain instead that
   **the construction here** uses the square of a quadratic with positive
   definite quadratic part to dominate the negative terms. The proposition
   and its counterexample are correct.

3. **P3 — Count the first parameter radicand's printed bits.**
   `appendices/B-reductions.tex:315` says that all coefficients other than
   the boxes have constant size. The first parameter radicand at lines
   301–304 is `1+3*1000^{-2(Q+3)}`, whose rational encoding has `O(Q)` bits.
   Repair: “The boxes and first parameter radicand have `O(Q)` bits each;
   the remaining coefficients have constant size.” The stated `O(T^2)`
   total encoding bound remains correct.

4. **P3 — Distinguish derived parameters from arbitrary input constants.**
   `appendices/B-reductions.tex:1002` says that all constants have
   `O(k+N log N)` bits. Proposition
   `prop:reductions-quaternion-realization` permits explicitly supplied
   rational generators of arbitrary input bit length. Their coordinates
   occur in the constant-gate residuals and are kept exact. The derived
   scales, approximation tolerances, and dyadic mesh have the stated bound;
   the input constants need not. Repair: replace “All constants” by “All
   derived scale and rounding parameters,” and, if desired, state that all
   output coefficients have bit length polynomial in the total input length.
   The actual algorithm already has that polynomial bound.

5. **P2 — Complete source-credit integration without broad priority
   language.** `sections/04-reductions.tex:154–158` still asks for verification
   of `EY2010`, Lemma 5, and its precise bounded-circuit comparison contract.
   Lines 164–171 discuss near-identity commutators without a citation. The
   current vetted report already identifies Dawson–Nielsen and
   König–Lohrey as relevant antecedents, with source locators. Insert the
   vetted citations and settle the exact EY lemma/predicate through the
   designated literature agent. The comparison at lines 172–177 is already
   correctly restricted to Hesse's arXiv version 1. These literature points
   do not enter the self-contained reductions proof, but they matter to the
   requested journal-ready presentation.

## Proof reconstruction

### Input, validity, and the shared assembly contract

Section 04:59–82 fixes shared DAG size, integer constants, the nonzero
integer `W=2V-1`, and the checked full rational Hessian Gram. Coefficient
comparison and rational symmetric elimination are polynomial in the
explicit certificate size. The determinant/trace bound supplies a positive
curvature modulus with polynomial bit length. The malformed-input branch
at Section 04:618–622 maps every comparison language, including equality,
to a fixed no-instance. Coordinate indices and circuit topology are part
of the declared format.

I checked the actual `lem:quartic-realization` statement at Section
06:248–288 and its proof at Appendix E:361–427. Both applications here use
`n=m=N`, residual quadratic-part norm at most one, gradient bound `beta`,
Jacobian lower bound `nu`, and a vanishing rational quadratic `G` with
`mu I <= H`, `||H|| <= Lambda`, and `||grad G(p)|| <= epsilon=t^2`. Both
use exactly the required bound

`epsilon <= min(1, mu^2/(2N), nu^2 mu^2/[36N(Lambda+N beta)^2])`.

The lemma proves a full-space Gram bound by a Schur complement, rather than
only on tensor vectors `(v,u tensor v)`. The centered quartic block is at
least `2 mu^2 I`; its negative residual terms are retained. Canonical Gram
covariance then transfers positivity to the rational matrix computed from
the rational square factors. Entries are fixed degree-two expressions in
those factors' coefficients. Thus neither construction needs an oracle
for the exact point or a second approximation to its Gram. The resulting
matrix has polynomial dimension and polynomial coefficient bit length.

### Cube-root analytic compiler and comparison language

The direct interval certificate at Appendix B:109–150 is independent of
the signal estimates. Affine radicands have coefficient sum at most six;
the square gate's independently evaluated power and root intervals lie
inside `[1-13w,1+13w]`; the next box grows by the factor 1000. Repeated
wires can only decrease the combined coefficient sum. All boxes are
positive and avoid zero.

For the analytic lemma at Appendix B:160–208, integrating the complex
derivative gives `|phi(z)| <= 2|z|` on radius `1/12`. The multiplication
gadget is analytic beyond the closed radius-`1/100` polydisk and has norm
below `0.0032` there. Evenness of `theta` gives exact vanishing on both
axes. Cauchy's coefficient bound and the geometric tail on radius `1/400`
give

`|mul(x,y)-xy| <= (16/9)*10^6 |xy|(|x|+|y|) < 2^24 |xy|(|x|+|y|)`.

The axis factor is essential and is actually proved. It is not replaced by
an absolute cubic remainder that could swamp an unbalanced product.

The signal arithmetic at Appendix B:224–256 bounds addition error by
`34 Theta^2 delta^(d+1)` and multiplication error by
`(3 Theta^2 + 2^28 Theta^3) delta^(a+b+1)`, both within the stated
`2^30 Theta^3` budget. No argument divides by a leading coefficient, so
zero coefficients, cancellation, and repeated signals are covered.
The numerator/denominator schedule at lines 258–285 adds only equal-order
signals and never computes the integer gate values. The nine raw root
gates at lines 287–299 implement the displayed gadget exactly; their
coefficients are `3` and `3/8`, with the stated coefficient-sum bounds.

The recurrence solves to `log2 Theta_t = 16*3^t-15`; the parameter chain
length `2T+5` dominates its error budget. The final coefficient `W` is a
nonzero integer, so its sign survives the absolute approximation. The
auxiliary chain gives `s_e^2 <= delta^(2^(T+2)) <= delta^d delta^3`, and
`2^(T+2)-d >= 3`, yielding the required `s_e^2 <= |s_o|/8`.
The designated output and auxiliary gate are distinct. This proves
`thm:reductions-root-circuit`, including all promises used by the tilt.

For `thm:reductions-root-language` at Appendix B:353–430, multiplying by
the common denominator `D` makes every gate an algebraic integer;
the extension degree is at most `3^k`. Every conjugate root is bounded
by `(2L+1)2^L`, including nonreal conjugates. The norm of the nonzero
integral difference `D(xi_o-r)` gives the separation
`|xi_o-r| >= 2^(-2^(6L))`. The Newton cube-root recurrence contracts first
linearly and then quadratically. Its `14L+6` iterations, and the
radicand-error propagation bound `2^(6L+2)`, give error at most `g/8`
without losing radicand positivity. The five shifted rational outputs
correctly distinguish `>`, `>=`, `<`, `<=`, and `=`. All denominators in
the Newton computation are positive.

The upper author's reported missing `lem:models-division` reference is
already repaired: there is no such reference in either reviewed file.
Appendix B:428–430 cites `def:models-circuits`; its actual definition at
Section 01:365–382 gives positive-denominator division and cites the
existing `lem:denominator-clearing` at Section 03:126–136. Adding that
lemma as a direct second citation would be optional, not a proof repair.

### Signed odd-root realization

Appendix B:30–62 normalizes negative boxes by a sign and a common positive
rational scale. Set-valued interval multiplication correctly reverses
negative boxes, and the normalized lower endpoint is at least one. Unary
degrees bound every printed exponent, including negative powers of the
normalization scale, by a polynomial.

The residual chain at Appendix B:445–486 has exactly `N` equations in
`N` variables and exactly one real zero. Its terminal exponent is
`2n_i-1`, so the triangular recursion selects the unique real odd root.
Replacing the first basis vector by the power-curve tangent has determinant
one and leaves the minor with diagonal entries `-1`. Consequently
`|det J| = product_i d_i alpha_i^(d_i-1) >= 1`.
The row norm and Frobenius bounds imply the stated singular-value bound
with `beta=4N A^N` and `nu=beta^{-(N-1)}`. All residual quadratic matrices
have operator norm at most one.

For the local exposing form at Appendix B:488–550, the tridiagonal
matrix is `Delta T_0 Delta` with positive diagonal `Delta >= I`. The
eigenvalue estimate for `T_0` and the inverse lower-bidiagonal difference
matrix give the stated uniform lower bound `h_0`; the upper bound
`8 A^(2N)` also follows. Interlacing diagonal and neighboring terms gives
exactly `(t-alpha)(t^(2n-1)-alpha^(2n-1))` on the power curve. Centering
leaves only the cross term `-u_{i,1} sum a_ije u_{j,e}` to predecessors.
All earlier-coordinate derivatives vanish at the circuit point.

The rescaled coupled form at Appendix B:552–581 has diagonal blocks
`H_i` and an off-diagonal absolute row sum at most
`sqrt(rho) A=h_0/4`. This handles signed coefficients, arbitrary sharing,
and every retained power. Rescaling back gives
`H* >= (3/4) h_0 rho^(k-1) I = (3/2) gamma I`.

The identity at Appendix B:598–619 is an exact representation by rational
quadratics vanishing at the intended zero. The weighted-degree reduction
is valid through degree `2n`; its two nontrivial terminal terms are
`S_i=X_{i,n}^2-b_i X_{i,1}` and
`T_i=X_{i,n-1}X_{i,n}-b_i`. Replacing only the scalar coefficients in this
representation therefore preserves `G(p)=0` exactly. This is stronger
than merely perturbing the exposing quadratic's raw coefficients.

The derivative/coefficient bounds at Appendix B:630–654 give
`||H-H*|| <= gamma/2` and `||grad G(p)|| <= epsilon`, while
`||H|| <= Lambda*+1`. Every hypothesis of the shared assembly lemma is
then satisfied at lines 657–668. Its certificate is computed directly
from the square factors; no gate minimal polynomial is expanded.
All scales, approximation precisions, polynomial coefficients, the
explicit quartic, and the full Gram have polynomial bit length. This
proves all three parts of `thm:reductions-signed-root` and preserves its
coordinates exactly.

The monotone cubic special case at Section 04:384–392 also checks:
`[1,A]` is a valid directly tested box since the radicand upper endpoint
is at most `A^2 <= A^3`.

### Feasibility, fixed cube, and min-sign perturbation

The feasibility corollary uses the unique zero of a nonnegative quartic,
so its feasible set is empty or a singleton. The compiler avoids equality
at the output gate; `p_{o,1} >= kappa` therefore tests the required strict
sign. All power coordinates are in `(0,4)`. The affine map sends the
fixed cube to the stated box and has minimum diagonal entry greater than
six, giving Hessian modulus at least 54. Full-Gram positivity is preserved
by the actual invertible rational congruence of
`lem:models-gram-curvature`, not by just changing Hessian coordinates.
The text correctly distinguishes the cube's interior from the degenerate
zero sublevel set and supplies no unsupported positive gap in the no case.

For `thm:reductions-min-sign` at Section 04:455–502, differentiating
`-u^2 v` gives the displayed sparse rational Hessian Gram. Its Frobenius
bound is `sqrt(12 kappa^2+10)<8`. Multiplying the original full Gram by
`ceil(9/mu)` therefore gives `M_G >= I`, with polynomially many printed
bits. The distinctness of the two coordinates is needed and supplied by
the compiler.

The signal estimates give `|v_0| <= 1/8` and
`u_0^2 <= |v_0|/2`. For positive output, evaluating at `p` gives a strictly
negative value. For negative output, strong convexity bounds the possible
decrease from `p` by half the squared gradient norm and leaves
`G* >= (1/2)u_0^2 |v_0|>0`. Thus the promised nonzero optimal value is
proved on both sides. The text makes no unsupported rationality promise
for the perturbed minimizer and no inverse-polynomial value-gap claim.

### Quaternion compiler and rational optimizer

The identities at Appendix B:692–746 follow from the displayed quaternion
product; rotation sends `e_1` to `e_2` and `e_3` to `e_1` with the sign
needed by the multiplication compiler. The exact commutator identity
retains the product of the vector-part norms. The near-identity estimate
and projection estimate have the stated constants.

The generator invariant at Appendix B:748–781 is valid. Writing `x=g_1`,
the first rotated commutator coordinate lies between `x^2` and `3x^2`;
its scalar part is greater than one half. Projection then gives
`x^2 <= g'_1 <= 6x^2` and transverse norm at most
`48x^4 <= 64(g'_1)^2`. The initial rational generator satisfies the
invariant. Iterating `6g'_1 <= (6g_1)^2` proves the stated strictly
positive doubly small selected coordinate.

Quaternion signal errors at Appendix B:788–848 are absolute and do not
divide by `C`. The bounds `18 Theta^2`, `142 Theta^3`, and
`396 Theta^4` fit within `Theta'=2^20 Theta^4`. Addition is only at a
common order; product changes order by addition. The homogenized leading
coefficients at lines 850–869 are `(4 C_1 C_2,4 D_1 D_2)` for a product
and `(8(C_1 D_2 +/- C_2 D_1),8 D_1 D_2)` for a sum/difference. Therefore
`C=D V` and `D>0` are maintained, including cancellation. The recurrence
`log2 Theta_t=(41*4^t-20)/3` is dominated by the generator depth `2T+2`.
The nonzero output coefficient survives its error. Sharing and repeated
arguments are included in these norm estimates.

Each macro is a fixed finite composition of products and conjugates.
The positive-denominator numerator construction proves the language's
upper bound after checking rational unit generators. No expanded gate
fraction is required.

For realization at Appendix B:903–1003, the Jacobian is block lower
triangular with identity blocks. A repeated-parent product has parent
derivative `-(R_p+L_p)`, and its component quadratic matrices still have
norm at most one. The stated gradient/Frobenius bounds and determinant
one yield the required `nu`.

The exposing identity is correctly ordered for noncommutative
multiplication and holds for repeated parents:

`E_i(p+U)=|U_i|^2-|U_a-p_i conjugate(U_b)|^2`.

The negative term is bounded by four times the norm squared of any one
parent block, including a repeated parent. The geometric weight tail
is `omega_j/15`, so `H* >= (11/15) omega_* I` and `H* <= I`.
The constant and conjugation gates have the displayed centered exposing
forms as well.

Coordinate rounding changes a quaternion vector by at most `h`, not
merely one coordinate by `h`. The Euclidean recurrence
`e_i <= h(3^i-1)` preserves `e_i <= eta/2 <= 1`. Replacing only vectors
that multiply exact residuals preserves the zero. The perturbation
bounds `||ell|| <= 12k eta` and `||H-H*|| <= 8k eta` give the stated
`mu=omega_*/4`, `Lambda=2`, and gradient budget. The assembly is again
an exact application of the shared lemma with `m=n=N`, and the rational
gate list is preserved as the unique optimizer.

This proves `thm:rational-optimizer`, including the supplied `N+1`
rational square factors, known zero minimum, bounded rational point,
and nonzero designated coordinate. Its generator coordinate is below
`2^(-64*4^T)`; a nonzero reduced rational of that magnitude has denominator
greater than `2^(64*4^T)`. Since `N=O(T)`, the expanded coordinate length
is exponential in dimension. The remark does not confuse dimension with
total input length or claim a lower bound for all circuit representations.

### Classification, A1, A4, and scope

The classification proof at Section 04:617–658 applies the actual exact
upper theorem to `h=f-r` or `h=x_j-r`. Replacing `V` by `1-V` reverses
the integer positivity predicate, and every lower construction avoids
the relevant equality. Hence all four strict/weak value and coordinate
relations have the stated many-one lower bounds. Equality receives no
unproved lower bound.

Taylor integration at a stationary point gives real SOS for `f-f*`.
Consequently nonnegativity and real SOS are both exactly `f*>=0` in the
certified class. A positive definite full polynomial Gram forces
`f*>0` because the monomial vector contains one; the converse is the
actual existence part of `thm:interior-gram`. A rational PSD Gram gives
an unweighted rational SOS by rational elimination and the rational
sum-of-squares lemma. The reduction uses only the strict-positive and
strict-negative cases, so rational SOS is proved hard without asserting
an unsupported upper bound at zero minimum.

A1 at Section 04:669–699 uses the exact dense-input contract of
`thm:singleton-field`, its power-coordinate first coordinate, and its
polynomial-time construction. The disjoint sum retains the supplied
curvature bound one, so the promise version of the exact upper theorem
applies even when the combined full Gram is only PSD. Rational roots
and the empty list are covered. The source predicate is not claimed
PosSLP-hard. The one-real-conjugate necessity excludes direct
value-preserving square-root coordinates, and the manuscript explicitly
does not exclude unrelated reductions of Square Root Sum.

A4 at Section 04:723–741 and Appendix B:1008–1031 is also valid. Odd
powers and retained positive powers are convex on their boxes; the
radicand stays positive on the independent predecessor-power boxes.
Root and power upper maps have the stated derivative bounds. The
triangular deficits are nonnegative, and the geometric weighted
inequality is strict unless every deficit vanishes, in which case the
circuit recursion forces the circuit point. The weights have polynomial
bit length. This baseline is not silently promoted to a quartic
unconstrained realization.

The radius bound and the explicit negative-Hessian naive lifting
counterexample are proved. The final scope paragraph correctly excludes
unconditional NP-hardness, ordinary superpolynomial lower bounds,
approximation hardness, equality hardness, and succinct-input dependence.

## Exact literature questions for the designated source agent

No source discovery was done in this review. The root can reuse the
existing vetted report wherever its contract is already sufficient.

- For `EY2010`, identify the exact Lemma 5 version and page and verify:
  the source circuit operations; whether every intermediate value or
  only designated values lie in `(0,1)`; the threshold predicate; whether
  sharing is allowed; rational-constant/denominator encoding; and whether
  its reduction is deterministic polynomial-time many-one.
- For Dawson–Nielsen and König–Lohrey, supply the vetted citation keys
  and locators for near-identity commutator multiplication and shared
  group/matrix-circuit arithmetic. Do not use these sources to imply
  exact sign comparison in the particular fixed rational compact group
  unless the source actually states it.
- Retain the existing Hesse version-1 restriction. The vetted report
  records the later proceedings metadata but does not verify that its
  theorem table or appendix equals the preprint's.

The contribution statement should concern the explicit certified
quartic language and the particular proved compilers, relative to the
sources inspected. The review provides no evidence for first-publication
priority or for the absence of further antecedents.

## Verification record

The proof checks were analytic reconstruction and targeted text inspection.
The inspection commands used `rg`, `nl -ba`, `sed -n`, and `cat` on the
named manuscript and evidence files. No project-wide check, CI status or
CI log was inspected. No compiler or computational experiment was run.

The following checks were run on this review artifact only:

```text
git diff --check -- paper-exact-arithmetic/evidence/reviews/reductions-r1.md
git diff --no-index --check /dev/null paper-exact-arithmetic/evidence/reviews/reductions-r1.md
```

Both produced no whitespace diagnostics. The first returned 0; the
`--no-index` check returned 1 because the new file differs from `/dev/null`,
with no whitespace error output. These are documentation checks, not
mathematical tests or CI results.
