# Independent review: indefinite contact volume

Date: 2026-09-20. Reviewer: independent source-review agent.
Reviewed modules:
[ContactVolume.lean](../../../Formal/QuadraticPrecision/ContactVolume.lean)
and
[ContactNondegenerate.lean](../../../Formal/QuadraticPrecision/ContactNondegenerate.lean).

Verdict: **PASS** for R1 with the explicit qualification `delta >= 0`.
The final theorem proves the source's exact constant from compactness,
symmetry, nonzero determinant, and the actual pairwise contact inequality.
It does not assume that the contact has full dimension or comes with a
nondegenerate simplex or an enclosing parallelepiped.

## Geometric and algebraic argument

The nondegeneracy module proves that nonzero volume forces the linear
span of the translated contact to be the whole space: a proper real
subspace has zero Lebesgue measure. A basis selected from this spanning
set supplies `d` actual contact points whose differences from the chosen
origin have nonzero determinant. This argument handles arbitrary contact
sets and does not require their measurability. Compactness is used later
to attain the maximal determinant.

The implementation fixes any origin `o` in the nonempty contact and
maximizes over the remaining `d` vertices. This is sufficient: the
preceding span argument supplies a nondegenerate choice for this same
origin. Varying all `d+1` vertices simultaneously, as in the source's
presentation, is not necessary. The determinant is continuous on the
compact finite Cartesian product of contacts, so an actual maximum is
attained. Replacing one selected vertex by any other contact point is a
permitted competitor. The column-replacement identity and the positive
absolute determinant give the required inverse-coordinate bound
`abs(z_j) <= 1`. Thus the contact is contained in the actual translated
linear image of `[-1,1]^d`.

`contact_polarization` uses symmetry to prove
`x^T M y = q(x)+q(y)-q(x-y)` for `q(x)=x^T M x/2`.
It applies this to differences from the origin, and uses the three
pairwise contact inequalities, obtaining the uniform Gram-entry bound
`3 delta`. The proof need not retain the sharper diagonal-only bound
`2 delta`, because the claimed final constant uses `3 delta` throughout.

The imported, previously established Hadamard theorem bounds the absolute
determinant by the product of Euclidean column norms, including dimension
zero. Each Gram column has norm at most `sqrt(d) * (3 delta)`, so the
determinant is at most `(3 sqrt(d) delta)^d`. The algebraic identity
`abs(det(A^T M A)) = abs(det A)^2 abs(det M)` is proved directly with
determinant multiplicativity and transpose invariance. Taking square
roots is valid because `delta >= 0` and `abs(det M) > 0`, and yields
the exact simplex determinant bound

```text
abs(det A) <= (3 sqrt(d) delta)^(d/2) / sqrt(abs(det M)).
```

Lebesgue measure transformation under the linear map and translation
proves that the enclosing parallelepiped has volume
`2^d abs(det A)`. Monotonicity then gives precisely the R1 right-hand
side. The theorem is expressed using `ENNReal.ofReal`, as appropriate
for Lean's measure type; all quantities on the real right-hand side
are nonnegative, so this truncation does not weaken the asserted bound.

## Boundary cases and source qualification

The proof immediately disposes of volume-zero contacts, covering empty
sets and contacts of lower affine dimension. Nonzero volume itself
supplies nonemptiness and a nondegenerate simplex; these are not added
premises. At `delta=0` and `d>0`, the right-hand side is zero and the
theorem forces zero volume. At `d=0`, the empty determinant and real
zeroth power are one, so the conclusion is `volume S <= 1`, the correct
statement in zero-dimensional space. Both latter specializations were
also checked as direct clients of the final theorem.

The explicit nonnegative-tolerance hypothesis should appear in the source
lemma too. Without it, take the empty contact, `d=2`, the identity matrix,
and `delta=-1`: the pairwise condition is vacuous but the displayed real
volume upper bound is negative. For nonempty contacts the pairwise
condition already implies `delta >= 0` by taking identical points.
Every intended precision application uses `delta=4 eps >= 0`, so the
qualification does not change those results. This source correction was
reported to the parent agent; no source manuscript or proof module was
edited by this review.

## Targeted checks actually run

From `formal/`, with `PATH="$HOME/.elan/bin:$PATH"` and
`LEAN_NUM_THREADS=1`:

```text
lake build --wfail Formal.QuadraticPrecision.ContactVolume Formal.QuadraticPrecision.ContactNondegenerate
lake env lean /tmp/Topic20ContactVolumeReview.lean
```

Both commands passed. The temporary client file checked the dimension-zero
and zero-tolerance specializations and printed axioms for
`exists_nondegenerate_contacts`, `exists_max_contactMatrix`,
`contactMatrix_enclosure`, `contact_polarization`,
`contact_simplex_det_bound`, and `contact_volume_bound`. Every list was
exactly `[propext, Classical.choice, Quot.sound]`.

Reviewed SHA-256 hashes:

- `ContactVolume.lean`: `44e2635bb1657fc950a59062bf4f55c94cb9e6e2a7523253e68f6aae09164dfb`
- `ContactNondegenerate.lean`: `d8c490dd169934449c49830751e1ffd1afadb44a6793ee452a2f8a2938075761`

No proof source was changed, and no project-wide verification or CI
inspection was performed.
