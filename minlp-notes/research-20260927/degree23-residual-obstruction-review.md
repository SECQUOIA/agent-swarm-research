# Independent review of the small odd residual obstruction

Date: 2026-09-28. Reviewer: `one_parameter_spectrahedral_fields`.
Status: no mathematical defect found in the stated conditional theorem.
The reviewer suggested the earlier reduced-point support argument, but
did not develop the author's Frobenius-quotient proof for nonreduced
residual schemes. This is an independent proof audit of that extension,
not an independent discovery or a priority assessment.

The reviewed source is
[degree23-residual-obstruction.md](degree23-residual-obstruction.md).
Its main theorem says that, in a proper intersection of five quadrics
in projective five-space, every rational residual decomposition with a
reduced component and an odd complementary length at most nine forces
a real residual point into the common quadratic base of the reduced
component. The resulting degree bound 21 for the quartic application
remains conditional on a proper complete intersection and the stated
absence of real common zeros at infinity.

## Reconstruction of the proof

Let the homogeneous coordinate ring of the complete intersection be
`S`, and choose a rational linear form `L` avoiding its finite support.
Then `L` is regular on this one-dimensional Cohen--Macaulay ring.
Dehomogenization at `L=1`, with its degree filtration, has associated
graded algebra `S/(L)`. This is the complete intersection of five
quadrics with Hilbert series `(1+t)^5`. Its Gorenstein socle is in
degree five. A functional on the one-dimensional filtered quotient
`A/F_4 A` therefore induces a nondegenerate multiplication pairing:
for a nonzero element of filtration degree `i`, lift a complementary
graded element of degree `5-i`. Their top product is nonzero.

The disjoint scheme decomposition gives an actual direct product of
finite algebras. Restricting this functional to the residual factor
is nondegenerate, since an element orthogonal to that factor is also
orthogonal to every other factor. For a quadric `q` vanishing on the
other component, the radical of the form `lambda_R(qab)` is exactly
`Ann(q)`. Thus this form descends nondegenerately to
`B=A_R/Ann(q)`; no radical or reduction of the scheme has been taken.

The images of affine linear polynomials form a subspace `V` on which
the pairing is zero, because `q a b` has degree at most four and
vanishes on the other direct factor. Nondegeneracy gives
`dim V <= dim B - dim V`. This dimension inequality is valid for
indefinite bilinear forms and needs no positivity assumption.

The quotient algebra `B` is also a closed subscheme of the original
finite complete intersection. If `v=dim V`, its projective linear
span is `P^(v-1)`, including any linear equations imposed by its
nilpotent structure. The original quadrics restricted to this span
still have finite common base: their common zero scheme is contained
in the original finite intersection. Generic `v-1` combinations
therefore give a proper quadratic complete intersection containing
`Spec B`, of length `2^(v-1)`. The same argument includes scheme
multiplicity. For `v=1`, a closed subscheme of `P^0` has length at
most one. Consequently

```text
2v <= length(B) <= 2^(v-1).
```

For positive length at most nine the only solution is `v=4`,
`length(B)=8`. This is the essential strengthening beyond merely
requiring a residual length of at least eight.

Finally, if the quadrics have no common real residual point, a rational
linear combination can avoid zero at all the finitely many real
residual support points. A finite union of proper real linear
subspaces cannot contain the dense rational coefficient vectors.
This `q` is a unit on each real local factor, so quotienting by its
annihilator leaves those local factors intact. Every local factor
with complex residue field, and every quotient of it, has even real
dimension. One can see this without assuming reducedness from a
composition series whose simple factors are copies of the residue
field. Thus `length(B)` has the same odd parity as the residual
length. This contradicts its forced value eight. In particular,
nonreduced residual components do not create an exception.

## Scope and possible overstatements checked

- The affine chart is used only to construct the finite algebra. The
  theorem concludes a real projective common zero. If that zero is
  at infinity in an application's preferred chart, it does not by
  itself establish a second affine zero. It does rule out the needed
  corank-one positive semidefinite exposing quadric and any strictly
  positive quartic leading form.
- Nonsingularity of the selected five equations at the algebraic
  minimizer extends to all its conjugates, making that orbit a
  reduced direct component of the complete intersection. This is
  where the application's simple-orbit hypothesis is used.
- The argument cannot currently be applied when every choice of five
  combinations retains a positive-dimensional complex base. It
  therefore does not prove the unconditional five-variable degree
  bound 21.
- No general Eisenbud--Green--Harris conjecture or classification of
  quadratic Gorenstein algebras is used. The proof needs the classical
  complete-intersection duality and scheme-theoretic Bezout facts
  identified above. This review does not establish novelty of their
  combination with real parity.

## Targeted verification

Command actually run:

```text
python research-20260927/check_degree23_residual_obstruction.py
```

It passed the explicit nine-point Hilbert function and linkage
arithmetic, the support of its quadratic dependency, the small integer
inequalities, and the sharp nonreduced example of length eight with
four-dimensional isotropic linear image. These are checks of finite
examples and arithmetic, not replacements for the universal
scheme-theoretic proof reconstructed above. No project-wide checks or
CI inspection were performed.
