# Fields and certificate review, round 2

This round independently reviews the restored rational radial-finiteness
proof in Appendix H and the changed field/certificate statements responding
to round 1. The independent development note is background rather than a
verdict. The BSS contracts are the source contracts supplied by the root
and the authorized Luna source review; I did not browse or conduct source
research. A delegated reviewer independently checked antipodal averaging,
homogeneous padding, dehomogenization, and the certified-quartic hypotheses.

The root confirmed author completion on 2026-10-05. I refreshed the actual
four manuscript files, read the author report, checked the additional final
changes, and recorded the final hashes below. Appendix H's hash matches the
author report exactly. The hashes for Sections 08–09 and Appendix G include
the root's final corrections described below.

## Final disposition

All seven findings below have been repaired in the final manuscript and
independently rechecked. The findings remain as the record of the review;
their original line numbers refer to the earlier text. No mathematical
blocker or unresolved finding remains in the four reviewed files. The
radial-finiteness argument is complete under the supplied, vetted BSS
contracts; it establishes rational squares rather than relying on a
real-coefficient existence theorem.

- R2-1: Appendix H lines 408–417 requires a positive order unit in the cone,
  positive integer bounds with both signs, and the precise preordering and
  pseudomodule hypotheses.
- R2-2: Appendix H lines 420–442 states the integer-multiple conclusions,
  splits Corollary 4.12 at `psi(u^2)`, and explains rational SOS rescaling.
  Lines 514–526 also prove the needed order-unit case directly.
- R2-3: Section 08 lines 502–507 includes the binary length of the supplied
  scale and restricts the input-relative lower bound to short scales.
- R2-4: Appendix H lines 467–477 gives the derivation argument explicitly.
- R2-5: Section 09 lines 238–239 makes the exponent depend on the quartic.
- R2-6: Section 08 lines 35–39 gives the prime-family bit bound per
  polynomial coefficient and per Hessian-Gram entry.
- R2-7: Section 09 lines 192–200 and Appendix G lines 254–263 explicitly
  charge the supplied prime-family scale's binary length and transfer only
  the monomial count and mathematical conclusions of the prime theorem.

The completed supplied literature report now records the exact BSS
general-ring contracts and locators. This closes the documentation of the
source interfaces used in the reconstruction below. Shared Appendix E also
now says `g_hatp(w_*)=f(p)=0`, without claiming that this exposing quadratic
has a unique zero.

The final additional changes are sound. Section 08's descent summary now
requires minimum zero and positive definite Hessian, matching the theorem's
value and stationarity hypotheses, and explicitly requires a degree-four
baseline. Section 09's real separation discussion now applies to the actual
certified blocks, whose real SOS representations follow from Taylor
integration. The constant term `g_0` in Appendix G matches the shared
canonical Gram formula and no longer clashes with the realization margin.
The block-height construction explicitly identifies `F_k^circ` and
`A_k^circ` with Section 07's `F_k` and `A_k`; its affine term is `x_k-1`, so
the direction-coordinate selector used in Appendix H is correct.

After author completion, the root corrected the conditional cyclic descent
paragraph in Section 08 lines 753–757. The final sentence now requires
“minimum zero at that cyclic point and a positive definite Hessian there.”
I re-read this final wording and refreshed the Section 08 hash. It explicitly
states the value and stationarity hypotheses needed by the descent theorem.
The `J_4=W` application remains conditional for the specified `n>=4`, and
the finite rank diagnostics remain outside the proofs. At this stage no
other theorem or proof changed; the other three reviewed files were
unchanged.

The later narrow review checked the prime-scale transfer in Section 09 and
Appendix G. For `B=f_ell+r^2`, both the coefficient vector and its canonical
Hessian Gram have integer entries bounded by a polynomial in `ell`, and
`f_ell^(lambda)=lambda B-r^2` scales them affinely. Thus the support remains
`O(ell^2)`, while rational coefficient and Gram-entry lengths are
`O(log ell+bits(lambda))`; for integer `c>=1`, this is
`O(log ell+log c)`. The new explicit runtime charges the scale's input
length. The Gram is
`Gamma_f+(lambda-1)Gamma_B>=I`, value and gradient at the same point remain
zero, and the obstruction functional remains `-4`. Therefore conclusions
(b)–(d), including both least-field certificate types, transfer unchanged.
The affine membership scalars used to compute `c_ell` already have
`O(log ell)` bits, so the multiplier theorem computes that threshold in
time polynomial in `ell`. Both final passages are correct. I refreshed
only the changed Section 09 and Appendix G hashes for this review; Section
08 and Appendix H are unchanged.

One integration note was sent for a file outside this review: the
introduction at lines 435–440 described the descent conclusion using a
“nondegenerate zero.” A convex polynomial can cross zero with nonzero
gradient: at `p=0`, take `G=x^4+x^2` and `F=x^4+x^2+x`. The relation space is
`span_Q{x,x^2}`, of dimension two, and its products span the stationary
quartics. Both Hessians are `12x^2+2>0`, but `F` is negative just to the left
of zero, so it cannot be SOS. The introduction should use the corrected Section 08 wording,
“minimum zero at the point and positive definite Hessian there.” This was
sent to the root; it is not a gap in the stated descent theorem. Bibliography
integration is also owned by the root and the authorized literature agents.

## Final snapshot

SHA-256, recorded after author completion and the final root correction on
2026-10-05:

```text
e2d740662a25da2d08bbccc6349411e417219f18e8b339891a0975e94f541b81  sections/08-fields.tex
d54888338ae9d221dfe9f0176fa9f2078a40e67c57686345a1147a09916afb34  sections/09-certificates.tex
0c4ddf55ba158ccd8c3857002eaea8805d15373d183f46b785777d50117cfeb1  appendices/G-fields.tex
37ca5a03d9cbb382b9ffe327ab6894e3b43664f9a2c9e405527a37fa47f1a7c5  appendices/H-certificates.tex
```

## Findings

### R2-1. The order-unit definition needs positivity

**Severity: false literal abstract definition; local repair.**

Appendix H lines 413–414 defines an order unit using an arbitrary integer
`N` and requires only `u in I`. Require `u in M intersect I` and a positive
integer `N` in the bounding condition, or state the standard equivalent
definition with both signs. With the current wording, take `A=Q`,
`M=Q_{>=0}`, `I=Q`, and `u=-1`: for each `b`, a sufficiently negative
integer `N` gives `Nu-b in M`. Thus the text calls `-1` an order unit,
although no nonnegative additive state can normalize it to one. The
positivity condition in imported result (IV) would then be vacuous and
would incorrectly imply `m(-1) in M`. The actual proof uses
`u=sum b_i^2`, so this is a defect in the abstract interface, not in that
constructed order unit.

### R2-2. Specialize the multiplicative pure-state contract correctly

**Severity: imported-contract scope error; local repair.**

Appendix H lines 419–430 states Corollary 4.12 for every archimedean
quadratic module `M`. The supplied exact contract uses an archimedean
semiring or preordering `S` and an `S`-pseudomodule `C` in the ideal. In the
actual sphere ring, `M=Sigma A^2` is a preordering and
`C=M intersect I` is closed under multiplication by `M`. Say this
explicitly and specialize (III) to this case, or give the complete
semiring/preordering hypothesis in the imported statement. Both normalized
Corollary 4.12 alternatives give the multiplicative relation used by the
proof. The text does not need to introduce a false dichotomy in the
normalized value of the state on `u`.

At lines 422–423, source Theorem 6.2 has an integer-multiple conclusion.
The direct conclusion printed here is valid over a ring containing `Q`,
because a positive rational is SOS and rescales the cone. For a precise
imported contract, print `mf in M` first and derive `f in M` using the
rational scaling already explained at lines 436–437.

### R2-3. The individual-degree discussion still ignores arbitrary scale length

**Severity: encoding overstatement; local repair.**

Section 08 lines 498–501 says the input `f_{k,lambda}` and its Hessian
certificate have length polynomial in `k`, and therefore the forced dense
output is superpolynomial in input length. The theorem permits arbitrary
supplied rational `lambda`. Restrict this explanatory conclusion to
`lambda=lambda_k` or scales of polynomial bit length in `k`. The
coefficient-degree lower bound is valid for every scale; the
superpolynomial-in-input interpretation needs the short-scale condition.
The compact-certificate theorem now correctly uses `L_lambda`.

### R2-4. Complete the short algebraicity step if self-containment is intended

**Severity: minor proof presentation issue; no mathematical error.**

Appendix H lines 479–482 correctly infer algebraic coordinates from a
nonsingular rational gradient system, but invoke the unnamed fact that an
isolated complex zero of such a system is algebraic. The independent
development supplies a short direct proof that would make this step
self-contained. If `K=Q(z)` had positive transcendence degree, a nonzero
derivation of a transcendence basis extends through the finite separable
extension `K`. Differentiating `gradient f(z)=0` gives
`Hessian f(z) Dz=0`; invertibility forces `Dz=0`, contradicting that the
coordinates generate `K`.

### R2-5. Avoid suggesting a uniform radial multiplier

**Severity: minor wording issue.**

Section 09 lines 236–237 says that “a fixed radial multiplier always works
for these quartics.” The proposition correctly allows its exponent to
depend on the polynomial. Say that some power of `omega` works for each
quartic. A single exponent for the entire scaling family is excluded by the
next radial theorem.

### R2-6. State the prime family's size bound entrywise in the summary

**Severity: minor encoding wording issue; no theorem error.**

Section 08 lines 35–38 says that the full Hessian Gram is “of
`O(log ell)` bits.” Read literally as total matrix size, this contradicts
the growing matrix order. The precise theorem at lines 207–208 correctly
states that polynomial coefficients and Hessian-Gram entries have
`O(log ell)` bits. Use that entrywise wording in the introductory summary.

### R2-7. Do not transfer the prime theorem's fixed-scale input bound

**Severity: encoding overstatement; resolved by the root.**

The earlier prime-scale corollary and supporting remark transferred “all
conclusions” of the prime theorem except its entrywise bit bound. This also
transferred construction time polynomial in `ell`, although the supplied
scale can have arbitrarily many bits. For example, reading integer
`c=2^(2^ell)` already requires more than polynomial time in `ell` in the
explicit binary input model. The rational-scale remark also needed to
distinguish rational output from integrality when the scale is integer.

The final Section 09 lines 192–200 and Appendix G lines 254–263 transfer
the monomial count in (a) and conclusions (b)–(d), explicitly charge the
scale's binary length, and state the resulting entrywise bit bounds. The
direct affine-scaling check is recorded in the final disposition above.
The mathematical field and multiplier claims are unchanged.

## Independent reconstruction of radial finiteness

The rational double-vanishing argument is correct. A rational linear
coordinate change can put a primitive generator of `Q(s)` in the first
coordinate. The minimal polynomial of that coordinate and the remaining
coordinate graph equations generate the rational maximal ideal. Their
gradients are independent over the residue field. Writing a rational
polynomial in those generators and differentiating shows that zero value
and gradient force its coefficients into the same maximal ideal, hence
give membership in its square. This establishes exact rational membership;
it does not infer it from real SOS factors.

The rational sphere ring is archimedean. Sums of squares form a
preordering, the coordinate bounds are explicit SOS identities, and the
subring argument extends them to every polynomial class. Rational scaling
is available because every positive rational is a sum of rational squares.
The positive definite leading form excludes sphere zeros on the equator.
All remaining zeros are the finite antipodal lifts of the affine zeros.

Using each distinct rational evaluation ideal once is correct even when
several real zeros have the same ideal. Different maximal ideals and their
squares are comaximal. The rational homogeneous polynomial has zero ambient
gradient at every real sphere zero, so the double-vanishing argument puts
it into every squared maximal ideal and thus into `J^2`. Every real
embedding of a residue field is accounted for: its image is another
sphere zero of the same rational polynomial. No total-real-field
assumption is used.

For `I=J^2` and `u=sum b_i^2`, the imported order-unit theorem has its
required actual hypotheses. Off the zero set, the multiplicative
pure-state identity and normalization give
`phi(H)=H(x)/u(x)>0`. At a zero, multiplication by the evaluation kernel
annihilates the state, so it induces a linear functional on the residue
module.

The local identification of this module with tangent quadratic forms is
valid. Both `J^2/(m J^2)` and `m^2/m^3` are killed by `m`, so localization
does not change them; all other maximal ideals become units. First-order
vanishing identifies `m/m^2` with the `n`-dimensional sphere cotangent
space. Its pair-products span the second quotient. The tangent Hessian map
is surjective because the differentials span the cotangent space, and the
dimension bound makes it bijective after extension through the specified
real residue embedding.

Positivity of the induced dual form follows from squares of elements of
`J`. Their cotangent classes fill the residue-field vector space, whose
real image is dense since the field contains `Q`. Normalization at
`sum b_i^2` makes the PSD dual form nonzero. The degree-two tangent form of
`H` is positive definite: the affine chart has an invertible derivative on
the sphere tangent space, the original Hessian is positive definite, and
the value and gradient vanish. Its pairing with the nonzero PSD dual is
strictly positive. The state is therefore positive at `H` in every case.

BSS Theorem 2.5 then gives an integer multiple of `H` in the rational
sphere SOS cone. Rational SOS scaling removes that integer. The result is
a rational polynomial identity modulo the sphere equation, not merely a
real SOS identity.

Antipodal averaging gives `sum (even_part^2+odd_part^2)` with no missing
scalar. An even padding degree `D` bounds all factor degrees; odd terms
then have degree at most `D-1`. Powers of `q` homogenize the two parities
to degrees `D` and `D-1`. The identity
`q^(D-e) H=sum E_i^2+sum (y_j O_i)^2` is homogeneous of degree `2D`
and agrees on the sphere, so homogeneity makes it an exact polynomial
identity everywhere. Setting `y_0=1` yields a rational radial SOS with
nonnegative exponent `D-e`. The empty-zero branch reaches the same
homogenization step through strict positivity.

The hypothesis inheritance for certified quartics is correct: minimum zero
gives nonnegativity and a unique real zero; strong convexity gives a
nondegenerate Hessian; the full PD Hessian Gram's tensor block gives a
positive definite quartic leading form. The radial lower-bound proof does
not use finiteness, but the restored theorem proves each individual order
finite.

## Round-1 responses checked

The multiplier proof now uses the actual normalized tower factors
`G_k/(t nu)` and `r_{i,j}/nu`, with the matching affine membership
coefficients. The prime-family membership likewise includes its rational
scaling. This resolves the normalization issue F-R5.

The compact-certificate theorem and its proof use `L_lambda` and resolve
F-R1. The individual-degree discussion now also includes arbitrary scale
length, resolving R2-3. Private Taylor/regularization references remain
removed.

The restored three-variable minimality corollary uses the shared bivariate
descent lemma. Under the supplied Scheiderer classification, its proof is
sound: four distinct complex lines with no triple intersection and no real
line factor form two conjugate pairs, producing two distinct real
projective zeros. The positive definite leading form and unique affine
zero of a certified bivariate quartic permit only one real projective zero.
The univariate proof correctly excludes a quadratic irrational zero by its
second real conjugate. Thus the dropped result F-R6 is restored.

Nonnegativity is explicit in the restored radial proposition; the
counterexample `x^2-1` is retained to explain the hypothesis. The rational
source gap F-R2 is addressed by the new full argument, subject to the
contract corrections R2-1 and R2-2, which have now been made and rechecked.
The finite cyclic stationary-space
diagnostics are still not a uniform theorem.

## Verification limits

Only targeted text inspection with `rg`, `sed`, `nl`, and `cat`, file
metadata inspection with `stat`, and the four-file `sha256sum` were
performed. I edited only this review report in round 2.
No mathematical scripts, experiments, browsing, compilation, project-wide
verification, or CI inspection was performed. The repaired local
interface/encoding corrections have been rechecked; no obstruction was found in the
restored rational ideal, tangent, pure-state, or homogenization mechanism.
