# Independent algebra and graphic-representation review

Date: 2026-09-22. Reviewer: `matroid_inventory`, independent of the eight
reviewed implementation modules. This review does not review the author's
own uniform, partition, or boundary modules. It is not a completion verdict
for the whole topic.

## Verdict and scope

No incorrect statement or proof gap was found in the reviewed determinant
support identities, coordinate bounds, graphic-representation bridges, or
nonzero representation scaling.
They discharge P02, the degree/evaluation parts of P03, U03 for finite
labelled graphs including loops and parallel edges, and the M02 auxiliary
assertion that nonzero denominator clearing preserves independence and bases. The explicit interpolation
producer, whole-program execution costs, and final spectral-cover assembly
need their own reviews. An algebraic identity alone does not establish
those algorithmic obligations.

An initial scope issue was resolved during review. The original four
graphic modules handle only finite simple graphs. The added
`GraphicRepresentationMultigraph.lean` supplies the missing labelled
multigraph bridge. Its forest characterization is connected to actual
acyclicity, absence of selected loops and parallel pairs, and walk
reachability. No scope qualification or unresolved finding remains for
that issue.

## Reviewed proofs

`GraphicRepresentation.lean` defines the rational vector with entries
`+1` at one endpoint and `-1` at the other. Walk induction proves reachable
endpoints have their difference vector in the edge span. For the converse,
the component-sum linear functional annihilates every edge vector and
separates endpoints in different components. Thus the span criterion uses
actual graph reachability, rather than defining reachability in algebraic
terms. The converse correctly requires finite vertices.

`GraphicRepresentationForest.lean` chooses the smaller endpoint as the
positive orientation. It proves that the span is unchanged by this choice
and that deleting an actual graph edge deletes exactly its oriented column.
The linear-independence criterion reduces to every edge being a bridge,
then uses Mathlib's actual `SimpleGraph.IsAcyclic`. The separate reorientation
theorem multiplies columns by units and preserves independence. This is
an oriented rational incidence argument, not the incorrect unoriented
zero-one incidence representation over the rationals.

`GraphicRepresentationBasis.lean` proves that independent columns span
the ambient edge space exactly when the selected subgraph is acyclic and
has the same reachability relation as the original graph. It further
identifies maximal forests and, under genuine connectedness, spanning
trees. Empty and disconnected graphs remain covered by the forest
statement; the connected tree conclusion is not asserted without its
premise. Entry values are proved to belong to `{-1,0,1}`.

`GraphicRepresentationFinite.lean` is the essential input bridge. It gives
an actual `Fin`-indexed rational matrix and connects the selected columns
to `ColumnIndependent`, `IsColumnBase`, and the determinant-based `IsBase`
after rank-preserving row reduction. Its `selectedGraph` construction also
starts with an arbitrary finite column set. Consequently
`arbitrary_columns_independent_iff`, `arbitrary_columns_base_iff`, and
`arbitrary_reduced_columns_base_iff` apply to every possible output, rather
than only to a supplied forest witness. The edge-set inverse identity
ensures no selected column is silently lost.

`GraphicRepresentationMultigraph.lean` accepts arbitrary finite endpoint
maps, so loops and parallel edges retain their separate labels. A loop
gives a zero column. The span theorem agrees with actual reachability of
the underlying graph, and the independence criterion deletes one edge
label at a time. The crucial `multigraph_forest_iff` proves that this
criterion is exactly underlying acyclicity together with no selected loop
and no repeated unordered endpoint pair. Thus ordinary parallel-edge
cycles are not lost by converting to a simple graph. The arbitrary-base
and reduced-base theorems add equality with the full graph's reachability,
and connectedness yields a spanning tree. All matrix entries are again
proved to belong to `{-1,0,1}`. This resolves the reported simple-graph
limitation without changing the mathematical source claim.

`DeterminantProfiles.lean` defines the generating polynomial by a matrix
determinant. Its proof expands over ordered column choices and proves the
identity with the factor `q!`; repeated columns contribute zero. This is
the ordered form of Cauchy–Binet. The rational factor is strictly positive,
including `q=0`, so the coefficient positivity theorem has exactly the
required support. It is then connected to actual unordered `IsBase` sets
and their summed profiles. The factorial occurs in the proof identity,
not in a claimed polynomial determinant execution.

The same file's `retainedRepresentation` zeros deleted columns while
retaining all original rows and column identifiers. `retained_isBase_iff`
proves that its bases are precisely original bases contained in the allowed
set. This rules out accepting smaller bases after rank loss. Coefficient
nonnegativity and positivity equivalence use rational arithmetic; no
modular noncancellation rule is assumed. `determinantPolynomial_eval`
proves the actual evaluation identity needed by interpolation, with ordinary
rational matrix products and monomial powers.

`DeterminantProfileBounds.lean` bounds the owner-marker degree by `|F|`,
not merely by `q`. Its optional profile bound uses the proved original
base cardinality and `F subset B` to obtain exactly `q-|F|` terms. The
optional-rank-zero theorem proves that the only possible base is `F`.
These statements justify retaining the original output count despite
adding an interpolation coordinate. They also keep the zero-optional-rank
case separate from a strictly positive remainder bound.

`RepresentationScaling.lean` treats arbitrary rectangular rational input,
not just a full-row-rank matrix. Scaling all entries by any nonzero rational
multiplies a size-`q` maximal minor by `c^q`; wrong-cardinality minors remain
zero. Units preserve independence of every selected column family, while
nonzero scalar multiplication preserves matrix rank. Consequently both
`IsBase` and the original-rank `IsColumnBase` are invariant. The result
includes negative scalars and rank zero, so every nonzero common
denominator multiplier is covered without an extra positivity premise.
This closes the auxiliary M02 finding. It does not claim that the selected
producer executes representation clearing: that producer keeps rational
entries and clears each determinant operand matrix separately.

## Targeted verification

The following command passed:

```sh
cd formal
PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1 lake build --wfail \
  Formal.MatroidSpectral.GraphicRepresentation \
  Formal.MatroidSpectral.GraphicRepresentationForest \
  Formal.MatroidSpectral.GraphicRepresentationBasis \
  Formal.MatroidSpectral.GraphicRepresentationFinite \
  Formal.MatroidSpectral.DeterminantProfiles \
  Formal.MatroidSpectral.DeterminantProfileBounds
```

All six source hashes were unchanged before and after the build:

| Module | SHA-256 |
|---|---|
| GraphicRepresentation | `c4e64b6c742c56d6fc5dbc6e2ed22e4e465ac2d5483104d37067f5047ca3be56` |
| GraphicRepresentationForest | `75b1cd5feef45e247afda47de6905eefa304ffd97ac54ed8391ab2e53c0bde86` |
| GraphicRepresentationBasis | `81968f2404500dd21b750934501501df911498ec59a735dd56fc5cde25fc93c5` |
| GraphicRepresentationFinite | `0bfe05a4881db8b10b283208ff0baa33a6164b4f3ce195051e263458d22a587e` |
| DeterminantProfiles | `2612a1e34ead7ba3298320a9574fd37e5e36b6f970a94e14680fad07eb8b3803` |
| DeterminantProfileBounds | `6c5bce7fc169610cd3cdfe3b7c33bab6bfc1ae4cb3e44c1bcbaf0be57a60f30c` |

After resolving the graph-scope issue, the additional targeted command
`lake build --wfail Formal.MatroidSpectral.GraphicRepresentationMultigraph`
also passed with the same environment. Its source hash was unchanged
before and after that build:
`6635ef28b61bfedaf756e1519c3589a62945e05cf70a966723634f35ddc717dd`.

The scaling addendum passed
`lake build --wfail Formal.MatroidSpectral.RepresentationScaling` with the
same environment. Its source hash was unchanged before and after the build:
`5572228da35a3fd235190f3c5df3bb1b58a5cc8784d6153321e67920ae7404d6`.

The final axiom audit and independent kernel replay are separate checks
owned by the integration run. This review neither ran project-wide checks
nor inspected CI.

## Source and manuscript alignment

The primary note and only the matroid subsection and matroid appendix of
the correlated-measurements manuscript were revised to describe the
owner-count producer. They keep the full representation rank `q`, use
full information degree `2qL`, and account for the extra interpolation
coordinate. Cancelling the common forced profile preserves the optional
profile count and the source's original output bound. The note retains
contraction as an equivalent historical cross-check, without claiming a
contraction implementation. The revised proof describes cached Bird
determinants and explicit tensor Lagrange coefficient products.

The manuscript was built successfully in a temporary output directory:

```sh
cd paper-correlated-measurements
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=/tmp/matroid-paper-review-build main.tex
```

The resulting PDF has 67 pages. Its final LaTeX log contains no undefined
references/citations, warnings, or overfull/underfull boxes. Text extraction
confirmed that the owner-count and Lagrange descriptions appear in the
PDF. This is a manuscript check, separate from the Lean build. The checked
version explicitly leaves the assembled Lean verification in progress;
the root integration must update that status only after its final checks.
