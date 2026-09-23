# Independent review of TU integrality and simultaneous cardinality laws

Reviewed 2026-09-20 against the TU slab and simultaneous-attainment part of
W03 in [CLAIMS.md](../CLAIMS.md). The reviewer did not author or modify
`StructuralCardinalityTU.lean` or `StructuralTreewidthTU.lean`. The reviewer
did author the separate signing-criterion proof in `StructuralCamion.lean`;
this report does not independently review that proof.

**Result: the reviewed modules prove TU slab integrality and construct one
law attaining the interpolated count value on every scope simultaneously.
No mathematical or statement-scope defect was found.** Their structural
input remains an explicitly assumed TU matrix. These statements alone do
not prove that treewidth two supplies a TU partition or the final gap bound.

## Proof and statement audit

1. `exists_symmetric_perturbation` uses the finiteness of the row set to
   choose a common positive perturbation radius. Tight rows stay fixed and
   each nontight inequality has strict slack. Both signs of the perturbation
   are proved feasible; the direction need not be nonzero.
2. `extreme_kernel_eq_zero` puts the original point at the midpoint of
   those two feasible points. Extremality and the positive step length
   force the direction to vanish. `extreme_active_injective` therefore
   proves full column rank of the actual active-row matrix, rather than
   assuming a basis of active constraints.
3. `extreme_integral` applies the integer-system descent theorem to those
   active rows and their integer right-hand sides. The dependency in
   `StructuralTreewidthTU.lean` selects independent rows over the reals,
   obtains a nonsingular square integer TU minor, and uses its adjugate and
   determinant square equal to one. Integer descent is proved; no generic
   polyhedral-integrality axiom is introduced.
4. `convexHull_binaryPoints_eq` proves an exact convex-hull equality. The
   feasible polyhedron is closed and contained in the compact cube. Its
   extreme points are integral and hence binary. The finite binary set has
   a closed convex hull, so the closure in the extreme-point hull theorem
   can be removed. The result is not merely a closure or approximation
   assertion.
5. `exists_binaryLaw` converts that hull membership into a law on feasible
   binary vertices, then maps it into the full ambient vertex type. It
   preserves every coordinate mean and proves feasibility of every atom
   with nonzero weight. The hull membership comes from the given feasible
   point; it is not an additional assumption in the final theorem.
6. `mem_scopeBox_iff` checks the exact signs and bounds of
   `[A; I; -A; -I]`. `exists_scopeBoxLaw` proves simultaneous preservation
   of both integer bounds on every row. Row duplication and sign changes,
   and the added cube rows, use proved TU closure lemmas.
7. `exists_adjacent_scopeLaw` applies those slabs to the integer scope
   incidence matrix with bounds `floor(meanSum)` and `floor(meanSum)+1`.
   Nonnegative means follow from cube membership, so the natural-number
   floor is appropriate. Counts on binary atoms are proved to equal the
   corresponding matrix row sums.
8. `expect_cardinality_of_adjacent` replaces each count-table value on the
   supported two-point interval by its affine interpolation. Zero-weight
   atoms are handled separately. The prescribed means determine the mean
   count, yielding `cardinalityLower` exactly. No sign, monotonicity, or
   convexity assumption on the table enters this identity.
9. `exists_cardinality_scopeLaw` selects one law before universally
   quantifying over both the scope index and the table. Thus all scope
   equalities hold under the same law, even for overlapping scopes and
   different tables. Convexity is needed separately to identify these
   interpolated values as lower envelope endpoints.

## Boundary cases and limits

The statements impose no nonemptiness or strict-interiority assumptions.
Empty coordinate types, empty row classes, empty scopes, repeated scopes,
redundant constraints, and coordinates absent from all scopes are covered.
The means remain prescribed on the entire ambient coordinate space.

The hull equality covers an empty feasible set; construction of a law
requires the supplied feasible point. Integer lower and upper bounds need
not be nonnegative or strictly ordered: feasibility supplies the necessary
compatibility. The matrix itself may have negative entries; only the scope
specialization restricts it to zero and one.

At an integer mean the interpolation coefficient of the upper count is
zero. In particular, at the maximum count the artificial table value one
past the scope size cannot affect the expectation. Signed and decreasing
tables are allowed. These observations concern the displayed theorem
statements and their proofs, not additional separately executed examples.

The proof constructs laws noncomputably using finite-dimensional convexity.
It does not establish a decomposition algorithm, termination bound, or
bit-complexity bound. It also does not discharge the graph-to-TU premise,
the mixture of the two class laws, or the final aggregate envelope argument.

## Targeted verification

The following commands were run from `formal/` and passed:

```sh
PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1 lake build Formal.MultilinearGap.StructuralCardinalityTU
PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1 lake env lean /tmp/topic19-tu-integrality-review.lean
```

The temporary review file printed the axioms of `extreme_integral`,
`convexHull_binaryPoints_eq`, `exists_binaryLaw`, `exists_scopeBoxLaw`,
`exists_adjacent_scopeLaw`, `expect_cardinality_of_adjacent`, and
`exists_cardinality_scopeLaw`. All seven depended only on `propext`,
`Classical.choice`, and `Quot.sound`; none depended on `sorryAx`. It also
checked the elaborated type of the final theorem, confirming that it
requires only `[Finite R]` for rows and quantifies over tables after selecting
the law. No project-wide verification or CI inspection was performed.

Reviewed SHA-256 values:

```text
5624c38423f8749e0eee463e2973826041cdaff243d7bd78246ca10434588b83  StructuralCardinalityTU.lean
4ee87e04f90192fbc4f031e7a64d4729472290bf37bf32d03efe5e5f55ee9f14  StructuralTreewidthTU.lean
```
