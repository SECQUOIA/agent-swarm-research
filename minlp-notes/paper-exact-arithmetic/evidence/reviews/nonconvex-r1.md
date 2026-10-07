# Actual-manuscript review: nonconvex few-Hessian arithmetic

Date: 2026-10-05. Scope: Q13 in `appendices/L-further-arithmetic.tex`,
including the shared nonconvex field bounds used by Q14, and the exact
Appendix J interfaces that these proofs invoke. This is an internal
independent proof review, not external peer review or a novelty audit.

## Result

The actual Q13 manuscript proofs pass independent reconstruction after one
small explicit-interface correction described below. I found no remaining
internal mathematical gap in the reviewed snapshot. This conclusion assumes
the precise established sampling, affine-degree, and algebraic-recognition
contracts identified under source obligations. Their primary-source vetting
belongs to the Luna literature lane; this review did not browse or verify
those sources independently.

The review read the actual statements and proofs rather than treating the
positive source audit as a substitute. It checked the complete prewriting
audit for lost hypotheses. No historical mathematical script, experiment,
CAS, build, project-wide check, or CI status/log inspection was run.

## Reviewed snapshot and inputs

The final manuscript refresh covered L lines 1–632, through the bounded
integer and hardness distinctions. Its shared field lemma was included;
the later cone projection, integer-radius, rational-lift, and mixed-integer
cone algorithm proofs are outside this review's assigned scope.

- `appendices/L-further-arithmetic.tex`, SHA-256
  `02b04f22e1a1b89380a06c55902dcefb37a8d766f1f26f7ed3e6bc322087f0f8`.
- `appendices/J-quadratic-contrast.tex`, SHA-256
  `21361c5eb3eefa2f4decf1ae3c6b3a08755ba1cb59a4d77873a08f341d4aae4a`.

The Q13 prefix, extracted through the following cone-input subsection
heading, has SHA-256
`e71f181114ca6d44eb219b37080c7aa33e59a9876e6adca48a9f05903906b2e9`.
The final refresh also checked the new existing-source Mahler-height
citation and the explicit bounded-mixed-norm constant. The other changes
between the preceding whole-file hash and this one were confined to Q14.

The review also read `evidence/BRIEF.md`, authoring `CONVENTIONS.md`,
`DECISIONS.md`, both integration records, and the full
`evidence/reviews/prewrite-nonconvex-extension.md`. The current literature
report was searched for the relevant Q13 source contracts; it contains no
Q13 entry at this snapshot. Original source notes were not needed to fill
the manuscript arguments and were not used as proof dependencies.

Appendix J interfaces inspected were `lem:qc-heights`,
`eq:qc-minpoly-height`, `lem:qc-ordered-limits`, the full proof of
`lem:qc-elimination`, `thm:qc-kll`, and `lem:qc-sign`. A delegated read-only
review independently reconstructed the inactive-box, quantitative
elimination, and attained common-tuple arguments and reached the same
mathematical conclusion.

## Concrete finding and correction

The first actual draft of `thm:ncq-feasible` invoked component sampling in
chart dimension `d` and printed a `(2d)^{O(h)}` bound without separately
handling a zero-dimensional selected face. A selected face can have
dimension zero even when `h>0`. Its chart is already a bounded-size
rational feasible point, so no sampling theorem is needed.

I reported this to the author and root. The final text now states that
direct case at L:96–98 and invokes sampling only otherwise. This is a
resolved exposition/interface omission, not a change to the theorem.

During review the author also incorporated another reviewer's local
archimedean polynomial-entry factor in the determinant norms, made the
input-field scalar-height estimate explicit, and printed the
integral-scaled primitive-element coefficient estimate. I reread all three
changes at L:289–306 and L:356–380. They are valid and preserve the claimed
bounds. I did not discover or claim ownership of those other corrections.

## Reconstruction of the proof chain

### Model, lift, and feasible witnesses

The model allows arbitrary indefinite rational symmetric constraint
Hessians, arbitrarily many weak quadratic rows, affine inequalities, and
affine equations. Closedness follows from the weak rows and continuous
polynomials. The parameter is the rational span of constraint Hessians;
it excludes the objective Hessian, Hessian rank, and the number of rows.
Every explicitly encoded coefficient is charged to `L`.

Choosing native Hessian basis matrices and rational span coefficients gives
the graph lift `P ∩ Z(F_1,…,F_h)` without dropping an original row.
Cramer's rule gives charts of polynomial structural size and coefficient
bits linear in the original coefficient-bit bound, uniformly over the
finite family of active affine subsets.

`lem:ncq-face` is valid for nonempty unbounded polyhedra, polyhedra with
lineality, and affine spaces. Minimal face dimension excludes algebraic
points from that face's relative boundary. A component meeting the face
then meets it in a nonempty subset that is both relatively open and closed,
so the entire component lies in the face. Sampling that component in its
rational affine chart proves feasibility for all rows. The affine rows are
handled by this lemma; they are not silently added to the quadratic-map
component count.

The one-root sample format converts to the paper's common-field format by
selecting the relevant irreducible factor and inverting the coordinate
denominator modulo that factor. These are polynomial-size dense univariate
operations. The separate `h=0` rational-polyhedron argument and the now
explicit zero-dimensional chart argument cover both boundary cases.
Exact sign checks prove fixed-`h` NP membership. Coordinate annihilators
or the bounded-degree coordinate maps give the stated Cauchy radius.

The connected ellipse calculation at L:130–135 is exact. Its squared norm
is `-3x²+16x−12`; on `x≥5/2` the endpoint values are `37/4` and `9`,
and deleting the inactive affine row exposes norm-square `1`. The warning
correctly concerns global deletion. Using all active affine rows merely as
a local stationarity chart remains valid.

### Genericity and one perturbation tuple

`lem:ncq-generic` has the required independent bordered-matrix condition.
Invertibility of `M` and full row rank of `G` alone would not suffice in
the indefinite setting. At fixed `u`, constants and linear coefficients
independently prescribe constraint values and gradients. The value/rank
incidence dimension gives a proper bad locus, and more than `d` generic
active rows have no common zero.

The KKT incidence is a polynomial graph isomorphic to affine space of the
same dimension as coefficient space. The displayed example makes both
determinants nonzero: the first `s` entries of `M` are `−1/u_i`, the
others are `2`, and the Schur complement is diagonal and nonsingular.
Thus each determinant-zero incidence has smaller dimension, as does its
projected closure. The normalized dependence-vector charts avoid an
exponential minor list. Cumulative degree must include lower-dimensional
components, as the actual proof explicitly says.

Restriction of arbitrary ambient quadratic perturbations to a full-rank
affine chart is surjective. At every fixed nonzero `η`, the factors `η`
and `η²` therefore preserve surjectivity for the objective and each
selected oriented row. Extracting one nonzero formal parameter coefficient
from each exceptional polynomial and taking the finite product gives a
nonzero polynomial in the perturbation coefficients. The integer-grid
argument gives one tuple of polynomial-bit coefficients. It depends on
neither unknown boxes nor numerical parameter precision.

After the tuple is fixed, only finitely many `ε` make an exceptional
polynomial identically zero in `η`. For every remaining fixed `ε`, a
sufficiently small positive `η` tail avoids its finitely many roots. This
tail may depend on `ε`; the manuscript makes no unjustified uniform-tail
or diagonal-limit claim. Only one orientation of a band can be active, so
there are at most `h` nonlinear multipliers and at most `d` of them.
The objective Hessian and regularizing identity matrix affect stationarity
but add no constraint multiplier.

### Elimination, height, and one field

At a selected local minimum, restricting to all active original affine
rows leaves the other affine rows locally strict. Independent nonlinear
gradients give ordinary KKT necessity with objective multiplier one.
Adjugate reconstruction is justified by `Δ≠0`. Differentiating the active
equalities after reconstruction gives
`∂H/∂λ = −Δ² G M⁻¹ Gᵀ`; the bordered determinant makes this Jacobian
nonsingular. No positive definiteness or multiplier boundedness is used.

Coordinates, fixed linear forms, squared norms, and objective values are
rational outputs of the same selected multiplier roots, with denominator
`Δ²`. The multiplier degree is polynomial in structural size. Clearing
the structurally many fixed input denominators once, before determinant
expansion, gives full logarithmic coefficient norm
`(τ₀+1)S₀^{O(1)}`. Formal `ε,η` contribute parameter degree, not
numerical precision. The field-input local-norm argument now explicitly
counts the polynomial number of terms in matrix entries before determinant
expansion; it does not sum heights over expanded monomials.

The actual two-parameter `lem:qc-elimination` applies exactly. Its
deformation has a finite quotient because the leading monomials are
pairwise coprime. Multiplication matrices provide the output relation.
The lowest `ζ` coefficient removes components with simultaneously zero
numerator and denominator; the selected regular root continues under the
`β` deformation. Extracting the lowest `β` coefficient gives a relation
at every selected root. Intermediate specialization to the zero polynomial
is allowed. The ordered-limit lemma then extracts the lowest `η`
coefficient before the lowest `ε` coefficient. Every extraction selects a
subvector of coefficients, so the local norms cannot increase.

With `s≤h` and `a₀=S₀^{O(1)}`, the degree and height budget is
`S₀^{O(h+1)}` with coefficient bits
`(τ₀+1)S₀^{O(h+1)}`. Over the rationals, affine height also bounds the
primitive integer coefficient vector after common-denominator clearing.
The one-parameter use with a dummy inner parameter is a valid special case
of this exact interface.

`lem:ncq-common-field` first applies the uniform degree relation to a
primitive linear form of the same limiting tuple, proving the joint-field
degree rather than multiplying coordinate degrees. The small
integer-combination grid separates all embeddings of the absolute field.
Integral scaling and conjugate bounds give its minimal-polynomial height.
The trace-pairing matrix on the primitive power basis is nonsingular by
separability; its integer entries and right-hand side have the printed
bit bounds. Cramer's rule supplies short rational coordinate maps.
Root separation supplies a short isolator. These steps multiply by
polynomials in degree and structural size and preserve linear dependence
on `τ₀+1` in the rational case.

The field small-point lemma's norm-square objective is uniformly coercive
for small `η`; comparison with a fixed original feasible lift gives a
uniform primal bound. Its supplied-box objective proof is compact and
counts the supplied rows in the input. Both select one common tuple before
applying scalar or linear-form elimination. The nonzero-value gap follows
by removing zero powers and applying Cauchy's bound to the reciprocal
annihilator. These shared arithmetic arguments are valid for indefinite
squared-cone rows; they do not assume their Hessians are PSD.

### Finite infimum and attained optimizer

The use of `f+ε‖x‖²` is confined to the nonempty finite-bounded-below case.
It is coercive on the closed feasible set because it is bounded below by
`θ+ε‖x‖²`. The anchor inequality bounds all exact regularized minimizers
and their lifts for each fixed `ε`. The comparison inequality proves
`v_ε→θ` without assuming attainment or a primal outer limit.

For each admissible fixed `ε`, an unknown integer box strictly encloses
all exact regularized minimizers. Every inner cluster of compact perturbed
global minimizers is an original global regularized minimizer. A boundary
sequence would have a boundary cluster, contradicting strict enclosure.
Therefore all artificial box rows become inactive before any selected
chart or KKT coefficient is formed. No hidden `log R_ε` term remains.

The finite chart/support family is independent of the boxes. Inner
pigeonhole selection and then outer selection give one label. The
perturbed objective itself has inner limit `v_ε` and outer limit `θ`,
so the scalar J elimination lemma applies even if primal points and
multipliers escape. The zero-dimensional selected chart case is directly
rational.

If attainment holds, comparison with a least-norm optimizer bounds every
exact regularized optimizer by that norm. One unknown box suffices. The
inner and outer selections then converge to one tuple whose original
coordinates attain `θ` and have least norm. All coordinate and linear-form
outputs use this same tuple. The value lies in its field by rational
evaluation. No uniqueness is claimed for a nonconvex minimum-norm set.
The `x²=1` and `xy≥1` examples correctly distinguish nonuniqueness and
finite nonattainment.

### NP-oracle output and bounded integer slices

Adding an objective threshold increases constraint-Hessian span by at most
one. Fixed-`h` feasibility witnesses therefore give NP threshold queries.
The finite-value annihilator bound supplies an effective `M`; on a
nonempty domain, feasibility of `f≤−M−1` is equivalent to unboundedness
below. Bisection preserves containment of an unattained infimum even at
an exact midpoint. Its polynomial-bit precision and the minimal-polynomial
height bound match `thm:qc-kll`. Refinement identifies the selected root.

The attainment verifier evaluates the recognized value polynomial and
isolator inequalities in the candidate point's own field. These conditions
identify the already computed exact value without a compositum. The
uniform attained-witness bound makes the bounded-certificate question an
NP language, and prefix search recovers an optimizer with polynomially
many queries. The least-norm query has a short least-norm witness
independent of the queried threshold; it answers yes exactly for
thresholds at least `ρ`. Bisection of `[0,nB₀²]` is valid when `ρ=0`.
Exact scalar equality and another prefix search return a least-norm point.
All deterministic work and query lengths are polynomial for fixed `h`.

Finite integer bounds make every guessed assignment polynomial length.
Total-degree-two substitution preserves the continuous Hessian span and
gives uniform coefficient bounds. Finitely many slices reduce the finite
value and status arguments to their continuous counterparts. A least mixed
norm comes from one optimal slice, with the integer squared norm added as
a rational constant. This proves the stated bounded-integer extension,
even with varying integer dimension. It makes no claim about arbitrary
unbounded integer variables.

The single-row Boolean feasibility reduction and known-zero attainment
reduction are correct with bounded coefficients and `h=1`. In the latter,
`x_i=1/2`, `y=n/(4t)` is feasible for every positive `t`, and `t=0`
forces a satisfying Boolean assignment. The manuscript correctly separates
short feasible/output descriptions from global-optimality certificates
and ordinary polynomial-time global optimization.

## Exact primary-source obligations

These are source-contract checks, not unresolved internal derivations.
They must be closed in the literature lane before final readiness is
claimed.

1. **Grigoriev–Pasechnik, Theorem 1.2:** component sampling for a degree-2
   outer polynomial of an `h`-component quadratic map, allowing degenerate
   and unbounded zero sets, with the stated univariate degree and integer
   coefficient/output-bit bounds. Verify the common-denominator/root format
   and the applicable bit-size convention. Arbitrarily many affine rows are
   accommodated by the manuscript's proved face lemma, not imported as free
   quadratic-map components.
2. **Krick–Pardo–Sombra Section 1.2.1 and Heintz Lemma 2/Proposition 3:**
   confirm the exact locators for cumulative affine degree including all
   irreducible components, the needed Bézout bound, linear-projection degree
   monotonicity, and a containing hypersurface of at most that degree. The
   proof only needs a `2^{poly(d+s)}` degree estimate, with no height bound
   for the exceptional polynomial.
3. **Kannan–Lenstra–Lovász:** verify the certified bit-model recognition
   contract already printed as `thm:qc-kll`, including the approximation
   precision and polynomial bit time in degree and coefficient-bit bound.
   An arithmetic-operation statement alone is insufficient.
4. **Attribution/comparison:** the feasible-witness theorem is explicitly a
   polyhedral corollary of established sampling. The finite-infimum,
   coefficient-sensitive common-field, and minimum-norm output interfaces
   are the additions whose precise comparison remains a literature task.
   The manuscript explicitly excludes GP's announced optimization
   Theorem 1.5 as a proof dependency. No lack-of-search-hit novelty claim is
   made. Any comparison with existing attainment hardness should credit the
   established result and describe the single-Hessian restriction as the
   refinement proved here.

Khachiyan–Porkolab and the other cone integer-radius contracts concern the
later Q14 proof and remain with that review and the Luna source lane; this
Q13 pass neither verifies nor clears them.

## Verification record

Targeted commands actually run were scoped `rg`/`rg --files`, `wc -l`,
`cat`, line-numbered `sed` reads of L and the reused J interfaces, and
`sha256sum` of L and J. These provided text inspection and snapshot
identification; they were not computational theorem tests. The review-file
check `git diff --check --
paper-exact-arithmetic/evidence/reviews/nonconvex-r1.md` passed. The direct
untracked-file check `git diff --no-index --check /dev/null
paper-exact-arithmetic/evidence/reviews/nonconvex-r1.md` emitted no whitespace
diagnostic; its exit status was 1 because the new file differs from
`/dev/null`. No manuscript source was edited by this reviewer. Only this
assigned evidence file was written.
