# Review of the signing criterion and cycle-to-TU bridge

Reviewed 2026-09-20. The reviewer did not author `StructuralCamion.lean` or
`StructuralCycleTU.lean`. The reviewer supplied the integer parity helpers in
`StructuralGHParity.lean`; those helpers are not independently reviewed by
this report.

**No mathematical or statement-scope defect found. The Ghouila-Houri
sufficiency theorem and the cycle-to-signing bridge are complete, including
the right-factor incidence wrapper. They have no hidden TU or polyhedral
integrality premise.**

`ColumnSigning A` quantifies over every natural number `k` and every injective
selection `Fin k → n` of columns. The selected signs are actual integers equal
to `1` or `-1`, and every row sum must lie in the range `{-1,0,1}`. It does not
merely sign the complete column set, and it does not assume determinant bounds.
The column version is appropriate because transpose converts the usual row
version without changing total unimodularity.

`ColumnSigning.submatrix` permits arbitrary row restriction and injective
column restriction. Composing an arbitrary finite injective selection with
the column restriction yields exactly the selection needed in the original
condition. Thus every square submatrix used by mathlib's TU definition
inherits the signing condition. Repeated rows are not needed for the TU
definition; repeated columns would force zero determinant anyway.

`ColumnSigning.support` enumerates the nonzero support of an arbitrary finite
vector, applies the signing condition to that injective enumeration, and
extends the signs by zero outside the support. It proves both the pointwise
support conditions and all matrix-product row sums. This step does not assume
that the supplied vector was already sign-valued.

The determinant induction in `ColumnSigning.det` handles the zero-dimensional
matrix separately. For a nonzero determinant, one adjugate column is nonzero
because multiplication by the original matrix gives the determinant times a
coordinate vector. Each adjugate entry is zero or a unit by induction on the
proper cofactor submatrix, including the cofactor sign. Signing its support
preserves the vector modulo two. The signed matrix product is sign-valued and
zero modulo two away from the distinguished row, so those entries are zero.
Multiplying by the adjugate then yields `det(A) * v_j = w_0 * u_j`. Choosing a
nonzero support coordinate gives `v_j = ±1`, and both right-hand factors are
zero or units. Consequently the determinant is zero or a unit. No division,
field extension, or unproved minimal-counterexample theorem is used.

`ColumnSigning.totallyUnimodular` applies that determinant theorem to every
injectively selected square submatrix. Neither the ambient row nor column
type needs a finiteness instance: every determinant concerns a finite square
selection.

The core graph-to-signing proof in `StructuralCycleTU.lean` assumes zero-one
integer entries and even row-vertex count on every simple support cycle. The
quantifier covers all simple cycles, not merely induced cycles. The latter
weaker balanced-matrix condition would not by itself justify arbitrary
integer slab integrality.

`transpose_columnSigning` selects an arbitrary finite set of distinct original
rows, indexes it by `Fin k`, and forms the support sets for every original
column. The map back to the original support graph is injective, so all
simple cycles retain the parity hypothesis. The proof pairs each column's
selected neighbors, leaving at most one unpaired neighbor. A simple cycle of
the pair graph lifts to an actual incidence trail: the edge-origin lemma
prevents repeated incidence edges even when column vertices repeat. The
closed-trail parity theorem then makes every pair-graph cycle even. A proper
Boolean coloring supplies opposite signs on each pair, so all column sums
are zero or a unit. The zero-one entry hypothesis identifies these support
sums with the matrix sums. This constructs the signing of every finite row
selection, hence `ColumnSigning A.transpose`; transpose preserves TU.

The criterion concludes TU without assuming a good coloring, a TU partition,
signing existence, an integral polyhedron, or a law. The graph cycle parity
premise remains explicit and must be supplied by the separate structural
coloring argument.

The final wrapper `totallyUnimodular_of_even_factor_cycles` explicitly swaps
the two incidence sides by an injective `Sum.swap` graph homomorphism. Mapping
a simple cycle through that map preserves simplicity, and pulling back the
right-factor marking gives exactly the row marking used by the generic
criterion. No factor/variable convention is silently exchanged.

The proper-coloring dependency `StructuralEvenCycleColoring.lean` was also
reviewed. It derives ordinary walk-length parity from even simple cycles by
removing either simple cycles or two-edge returns, then colors each connected
component by distance parity from a chosen root. Its assertion for arbitrary
closed walks concerns edge length, for which a backtrack contributes two;
it does not extend factor-vertex parity to arbitrary closed walks. This is
consistent with the stronger trail hypothesis used by the incidence lift.

Targeted compilation of `StructuralCamion` passed without warnings, as
reported by its author. The reviewer independently ran
`PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake env lean /tmp/topic19-signing-audit.lean`,
importing the completed module and checking the criterion's type and axioms.
It passed; the only axioms were `propext`, `Classical.choice`, and `Quot.sound`.
The review also checked the final proof source and the definition of
`Matrix.IsTotallyUnimodular` in the installed mathlib.
The reviewer independently ran
`PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake env lean /tmp/topic19-cycle-tu-audit.lean`,
importing the completed cycle criterion, checking its final wrapper type,
and printing the axioms of both final TU theorems. It passed; both use only
`propext`, `Classical.choice`, and `Quot.sound`. The module author also reported
a warning-free targeted `lake build Formal.MultilinearGap.StructuralCycleTU`.
No project-wide verification or CI inspection was performed.
