# Independent review: quadratic contact and inertia lower bounds

Date: 2026-09-20. Reviewer: independent source-review agent.
Reviewed modules: `LowerPullback`, `LowerContact`, `LowerVolume`,
`LowerCurvature`, and `LowerNegativeSlice` in
[Formal/QuadraticPrecision](../../../Formal/QuadraticPrecision).
The review also inspected their `SpectralSlice` and parity-contact
dependencies.

Verdict: **PASS** for the actual-lift affine restrictions, quadratic
parity contacts, exact nonsingular contact-volume obstruction, and
original-box negative-inertia logarithmic lower bound. The latter
constructs its negative slice from the original Hessian and box. It has
no assumed slice, factorization, curvature certificate, or finite integer
range in its headline premises.

The initial five-module review did not discharge the separate
principal-slice assembly and algebraic rearrangement giving R3's
determinant constant, or I2's sharper isodiametric constant. The sharp
I2 connection has since passed the additional review below. R3 remains
outside this review's scope. The elementary diameter bound discussed
first is still a valid independent route to the exponent, with a weaker
dimension-dependent constant.

## Lift restriction and compact contacts

`ConvexIntegerLift.pullback` constructs a new carrier by requiring the
parameter input to lie in the chosen convex set and substituting the
affine input map into the original carrier. The original output,
continuous auxiliaries, and integer coordinates retain their roles and
dimensions. Its convexity is proved using the affine combination law,
and the projection equivalence explicitly retains the same integer and
auxiliary witnesses.

The graph, epigraph, and hypograph adapters require only that the affine
image of the new input domain lie in the original one. Each adapter
preserves its full containment and soundness predicates. In particular,
the epigraph/hypograph adapters quantify over every output in the
appropriate unbounded direction. Injectivity is not required for this
general operation; the actual spectral slice later proves injectivity
when claiming its dimension.

The quadratic midpoint calculation cancels both affine terms and gives
`q(x-y)/4`, where `q(v)=v^T M v/2`. The graph contact bound is therefore
`abs(q(x-y))<=4 eps`, and the epigraph bound has the correct opposite
sign, `-q(x-y)<=4 eps`. Both are extracted from actual integer-lift
contacts and passed to compact closures using continuity. Original
contacts may overlap and need not be convex or measurable. The common
lift need not be closed, and signed integer witnesses may be unbounded.

`graph_quadratic_volume_bound` combines the compact cover, finite union
subadditivity, and the previously reviewed indefinite-contact theorem.
It counts at most `2^p` sets and proves exactly

```text
volume D <= 2^p * 2^d * (12 sqrt(d) eps)^(d/2) / sqrt(abs(det M)).
```

The Lean statement uses the corresponding nonnegative `ENNReal.ofReal`
quantity. Its assumptions include `eps>=0`, a symmetric nonsingular
matrix, and compact input domain. There is no positive-definiteness
assumption. The graph theorem still needs the separate original-box
principal restriction and rearrangement to establish R3 in its final
advertised form.

## Elementary curvature bound and its scope

From `mu sum_i v_i^2 <= -v^T M v` with `mu>0`, the epigraph contact
inequality yields
`sum_i (x_i-y_i)^2 <= 8 eps/mu`. The coordinate supremum distance is
then at most `sqrt(8 eps/mu)`. The measure estimate used here is the
coordinate-space bound `volume S <= diameter(S)^d`, not the Euclidean
ball isodiametric inequality. This distinction is mathematically sound:
the implementation first proves the Euclidean sum-of-squares bound and
then deliberately uses the weaker coordinate-distance consequence.

The resulting finite cover gives

```text
volume D <= 2^p * (sqrt(8 eps/mu))^d.
```

For positive real volume and `eps>0`, the logarithm argument proves

```text
(d/2) log2(1/eps) + log2(volume D) - (d/2) log2(8/mu) <= p.
```

The statement is valid uniformly in the tolerance and lift. It does not
silently invoke the missing sharper coefficient
`(mu/2)(volume(D)/omega_d)^(2/d)`.

## Actual negative-inertia slice

`negativeInertia hH` counts the indices of strictly negative eigenvalues
of the actual Hermitian matrix. Repeated eigenvalues are counted with
their multiplicities, and zero eigenvalues are excluded. The embedding
extends coordinates by zero on other spectral indices and applies the
actual eigenvector unitary. Applying the inverse spectral coordinates
recovers the original parameters, proving injectivity.

A strictly positive lower bound on the finitely many absolute negative
eigenvalues gives coercivity of the embedded quadratic. The finite-family
lemma includes the empty family; in that case its arbitrary positive
modulus multiplies an empty sum. No assertion of a nonexistent negative
direction is made.

The box radius is explicitly obtained from the original positive side
widths and the rows of the embedding matrix. This requires
`l_i<u_i` for every original coordinate. Translation to the midpoint
of the original box and a sufficiently small positive parameter box
give the actual affine slice. The theorem supplies its injectivity,
domain inclusion, exact restricted quadratic coefficients, and coercivity
bound. The restricted Hessian is the actual matrix `T^T H T`.

Reindexing the negative spectral indices by
`Fin (negativeInertia hH)` preserves sums of squares. Hence
`exists_negative_quadratic_slice` gives precisely that many independent
parameter directions, rather than an arbitrary supplied dimension.
`epigraph_negative_inertia_lower` applies the proved lift pullback to
this constructed slice. The radius and curvature modulus are chosen
before quantifying over tolerance or integer count; its additive
constant is independent of both. No additional hypothesis about an
epigraph upper bound is introduced.

Zero negative inertia is included. Its parameter space is
zero-dimensional, the parameter-box volume is one, and the lower
inequality reduces to `0<=p`. This does not itself prove existence of
zero-integer epigraph formulations or the hypograph inertia headline;
those are separate assembly obligations.

## Targeted checks actually run

From `formal/`, with `PATH="$HOME/.elan/bin:$PATH"` and
`LEAN_NUM_THREADS=1`:

```text
lake build --wfail Formal.QuadraticPrecision.LowerNegativeSlice
lake env lean /tmp/Topic20LowerBoundsReview.lean
```

Both commands passed. The module's import closure includes all five
reviewed files. The temporary audit printed axioms for the three
`Has*Lift.pullback` adapters, `graph_quadratic_parity_cover`,
`epigraph_quadratic_parity_cover`, `graph_quadratic_volume_bound`,
`epigraph_negative_volume_bound`, `epigraph_negative_log_bound`,
`exists_negative_quadratic_slice`, and
`epigraph_negative_inertia_lower`. All ten lists were exactly
`[propext, Classical.choice, Quot.sound]`.

Reviewed SHA-256 hashes:

- `LowerPullback.lean`: `fb4f700a68885bee7d2fd5d5af8429376aa56b9889c2ac20c31d2d590fb75db5`
- `LowerContact.lean`: `eec0ca833e82166b71435d80ec6bab0e2fada95e52dbd20a2205b42063ff2dce`
- `LowerVolume.lean`: `0e34915786a7fb68015d4af7810b65a48cdeeb17e4998ad18a1e026b7a9abd70`
- `LowerCurvature.lean`: `318cb3c117d433802c180c32c0603b83a35647d8190dad5b447460b57c339032`
- `LowerNegativeSlice.lean`: `c6e03196e7850f55ffe39fecdf3a453361bdebcce6203f0230f600d89d971950`
- `SpectralSlice.lean`: `f8708a6d46cd1a381ac6a6a06949f0e5cfc72865f7ccdd5c4fbb77a429b24838`

No proof source was changed, and no project-wide verification or CI
inspection was performed.

## Additional review: exact isodiametric constant and original-box application

The completed `LowerEuclidean.lean` and `LowerIsodiametric.lean`
modules were subsequently reviewed after the author confirmed they were
stable. Verdict: **PASS**, including the exact constant in I2 and the
wrapper deriving it for actual original-Hessian epigraph lifts.
The new general geometric foundation is independently reviewed in
[isodiametric.md](isodiametric.md).

`Input d` has the coordinate supremum norm, whereas the sharp diameter
inequality needs the Euclidean norm. The implementation does not identify
these two metrics. It transports each compact contact through
`WithLp.toLp 2` into `EuclideanSpace ℝ (Fin d)`, proves compactness by
continuity, and uses `PiLp.volume_preserving_toLp` to prove equality of
the actual image volume with the original coordinate Lebesgue volume.
That Mathlib theorem relates the canonical coordinate and Euclidean
normalizations; there is no unspecified determinant or scale factor.

The distance proof returns to the sum-of-squares estimate
`sum_i (x_i-y_i)^2<=8 eps/mu`. The Euclidean distance is the square
root of that sum, so it is bounded by `sqrt(8 eps/mu)`. It does not use
the weaker supremum-norm diameter estimate from `LowerCurvature` in
place of an L2 estimate.

`unitBallVolume d` is the real volume of the actual Euclidean closed
unit ball. It is proved finite and strictly positive. The isodiametric
theorem gives each contact the bound

```text
omega_d * (sqrt(8 eps/mu)/2)^d.
```

Finite parity coverage therefore bounds the original domain's volume by
`2^p` times this quantity. The half-diameter radius is retained exactly.
The conversions between `ENNReal` and real integrals/volumes require
and prove the relevant finiteness and nonnegativity conditions.

For compact domains of nonzero volume, `d>0`, and `eps>=0`, the sharp
cover first proves `eps>0` from the existence of an actual epigraph
lift. At `eps=0`, its right-hand side is zero, contradicting positive
domain volume. Thus the subsequent logarithm argument does not silently
discard the zero-tolerance case. The generic theorem still quantifies
over all nonnegative tolerances, with exact lifts ruled out by its
premises.

The scalar rearrangement correctly proves

```text
eps >= (mu/2) * (volume(D)/omega_d)^(2/d) * 2^(-2p/d).
```

In detail, the radius factor simplifies to
`(2 eps/mu)^(d/2)`. The logarithmic inequality has additive constant
`(d/2) log2((mu/2)(volume(D)/omega_d)^(2/d))`, and the verified
positive-base exponential conversion yields precisely the displayed
coefficient and exponent. All divisions by dimension occur under
`d>0`; all logarithms used in the rearrangement have positive arguments.

`epigraph_negative_inertia_sharp_lower` then invokes the previously
reviewed actual negative-slice construction. Its hypotheses are the real
symmetric original Hessian, nondegenerate original box, and positive
actual negative inertia `k`. It supplies positive `rho` and `mu` before
quantifying over tolerance, count, or lift, pulls each actual original
epigraph lift back to the constructed slice, and proves the slice volume
is exactly `(2 rho)^k`. The resulting original-box bound is

```text
eps >= (mu/2) * ((2 rho)^k/omega_k)^(2/k) * 2^(-2p/k).
```

The slice, parameter dimension, coercivity, and volume are all constructed
or proved; none is an additional headline premise. Empty contacts are
allowed in the parity cover. The domain's positive volume follows from
`rho>0`. The zero-negative-inertia case remains covered by the separate
trivial lower and convex epigraph constructions, rather than an invalid
division by `k=0` in this sharp formula.

Additional targeted commands, from `formal/` with the same environment:

```text
lake build --wfail Formal.QuadraticPrecision.LowerIsodiametric
lake env lean /tmp/Topic20SharpLowerReview.lean
```

Both passed. The temporary audit checked the zero-error impossibility
as a client and printed axioms for `euclidean_image_volume`,
`negative_contact_euclidean_distance`, `curvature_volume_log_lower`,
`negative_contact_volume_sharp`, `epigraph_negative_volume_sharp`,
`epigraph_negative_error_pos`, `epigraph_strong_curvature_error_lower`,
and `epigraph_negative_inertia_sharp_lower`. All eight lists were exactly
`[propext, Classical.choice, Quot.sound]`. An initial temporary client
used the wrong namespace for `dotProduct`; correcting that client
required no source change.

Additional reviewed SHA-256 hashes:

- `LowerEuclidean.lean`: `df81e6bd163e93ec614c591c811dba84b7aae6d74dc2e94758283b8570fe392c`
- `LowerIsodiametric.lean`: `41fecbe7e32db4ddc96bcc52b6111824512c89af9660d6eafa2900c56df8e112`

No proof source was changed by this additional review, and no
project-wide verification or CI inspection was performed.
