# Literature audit: box quadratic moment hulls

**Scope.** This is a source-level comparison of the claims in the current
box-hulls manuscript with the primary works and versions identified below. It
records theorem statements and their limits; it is not a blanket priority
claim. The completed source batches and KB check are recorded in
[`literature/runs/2026-10-06-box-hulls-literature-luna/run.md`](../../literature/runs/2026-10-06-box-hulls-literature-luna/run.md).
The BoxQP dataset record is now present as `BurerBoxQPInstances2019` in the
paper bibliography, with no publication year asserted.

## Main comparison and claim boundaries

### Exact low-dimensional box hulls are prior work

Anstreicher and Burer study the lifted quadratic moment hull
`conv{[1;x][1 x^T] : x in P}`. For a box, their Theorem 6 gives the
positive-semidefinite moment matrix plus box-RLT description exactly in
dimension two; it is not a general exactness theorem for three-variable
boxes. Their Theorem 7 constructs an exact representation for triangulated
polytopes through dimension three by combining the simplex representations
of the triangulation. A three-cube can be triangulated into six tetrahedra,
so an exact three-variable box-hull lift was already known, albeit with a
larger construction. The manuscript correctly disclaims a first exact
three-variable hull and uses the triangulated lift as a reference point.
[[anstreicher2010-computable-representations-for-convex-hulls]] p.7
[[anstreicher2010-computable-representations-for-convex-hulls]] p.9

For the small blocks, Maxfield and Minc prove that every positive-semidefinite,
entrywise nonnegative matrix of order at most four has a factorization
`X'X=A` with `X` entrywise nonnegative; their paper gives an order-five
counterexample. This is the order-four identity `CP = DNN`. The dual identity
`COP = PSD + N` follows by cone duality. The theorem was checked against the
original Cambridge PDF; its extracted KB text contains only DOI watermarks,
so the retained extraction is not the reading basis. [[maxfield1962-on-the-matrix-equation-x]] p.2-3

Anstreicher and Burer–Dong also prevent a broader historical reading of the
new representability result. Burer and Dong give exact cone separation for
the homogenized three- and four-dimensional box cones and a hierarchy of
tractable relaxations. Exact separation is a different property from having
a finite semidefinite lift; the manuscript's obstruction addresses the
latter and does not rule out exact separation or other exact optimization
procedures. [[burer2013-separation-and-relaxation-for-cones]] p.24
[[burer2013-separation-and-relaxation-for-cones]] p.27

### The rational witness is specific to two named relaxation systems

Khajavirad's arXiv version 2, equation (17), is the disjoint-support sparse
SDP system compared in the paper. On the selected three positive-loop
variables it gives 27 localizing matrices. The manuscript's rational moment
functional is feasible for those displayed blocks and separates a
nonnegative quadratic. This establishes a gap for that specified system; it
does not exclude other sparse SOS systems, other degree conventions, or all
possible semidefinite formulations. [[khajavirad2026-tight-semidefinite-programming-relaxations-for]] p.9

Anstreicher and Puges's arXiv version 1 gives extended triangle inequalities
and switched second-order-cone formulations. Equations (14)–(16) and
Lemmas 4–5 describe the trilinear RLT and SOC implications. The manuscript
checks its rational witness against all coordinate complements and
permutations in the named SOC system. The resulting separation is therefore
from that formulation, not from every SOC or conic relaxation.
[[anstreicher2025-extended-triangle-inequalities-for-nonconvex]] p.12-13

Burer, Natarajan, and Willemsen's current arXiv version 3, Theorem 1, proves
objective-value tightness for their SDP relaxation on every submodular
continuous box quadratic in dimensions at most three. The data allow
arbitrary diagonal and linear terms; submodularity requires nonpositive
off-diagonal quadratic coefficients. This is not equality of the full
moment hull. Cube symmetries transfer the result to the three-variable
mixed-coefficient sign classes whose coefficient product is nonpositive.
The manuscript's positive-product class is outside that theorem's scope.
[[burer2025-on-the-semidefinite-representability-of]] p.9-13

### The extreme-ray comparison uses Hildebrand as a criterion, not as the classification

Hildebrand's arXiv version 4, Definition 2.1 and Lemma 4.3, applies to a
copositive matrix `A` and every nonzero real vector `w`, without a sign or
support condition: `A` is irreducible with respect to `ww^T` exactly when
some nonzero nonnegative zero `u` of `A` has `w^T u != 0`. Equivalently,
there is an `epsilon > 0` for which `A - epsilon ww^T` remains copositive
exactly when `w` annihilates every such zero. The choice of `epsilon` may
depend on `(A,w)`; no uniform bound is asserted. Theorem 4.5 separately
characterizes irreducibility with respect to the PSD cone by spanning of the
minimal zeros. See the supplied original-source
[Hildebrand receipt](hildebrand-source-receipt.md) and
[[hildebrand2014-minimal-zeros-of-copositive-matrices]] p.2
[[hildebrand2014-minimal-zeros-of-copositive-matrices]] p.8.

Those criteria are prior art. The manuscript's facet-zero reduction,
explicit cube-edge contact graph argument, and resulting classification
are its own proof. Its stated classification is limited to extreme rays
with positive square coefficients and positive values at all cube vertices;
vertex-zero rays remain outside the classification. No broader
classification of all extreme rays is supported by Hildebrand's result.

### The field-preservation theorem is general; the box and graph transfers are manuscript work

Bodirsky, Kummer, and Thom's published JEMS article supplies the general
real-closed-field machinery: Lemma 2.3 characterizes maps preserving
size-`k` LMI formulas; Theorem 2.13 supplies the positive-definite-function
to `k`-positive-map step; Remark 3.2 gives denominator clearing; Example 3.4
uses the Horn polynomial; Theorem 3.7 gives strict separation of a
non-SOS rational-exponent polynomial by a functional positive on every
nonzero square; and Remark 3.17 gives the closed-cone/dual-shadow
equivalence. Their copositive-cone application is to the orthant. The
constant-monomial box embedding, lexicographic evaluation, and transfers to
the stated box, simple-vertex, and sparse-graph hulls are the manuscript's
applications, not the source's theorems.
[[bodirsky2026-spectrahedral-shadows-and-completely-positive]] p.4
[[bodirsky2026-spectrahedral-shadows-and-completely-positive]] p.7
[[bodirsky2026-spectrahedral-shadows-and-completely-positive]] p.9
[[bodirsky2026-spectrahedral-shadows-and-completely-positive]] p.11
[[bodirsky2026-spectrahedral-shadows-and-completely-positive]] p.14

Nishijima's arXiv version 3, Theorem 3.2, proves that the copositive and
completely positive cones associated with any symmetric cone of rank at
least five are not spectrahedral shadows. This is a nearby extension of the
cone-level nonrepresentability landscape, not a theorem about box moment
hulls or the manuscript's box embedding. It should be presented as adjacent
context, not as a direct predecessor to the box-hull threshold.
[[nishijima2026-copositive-and-completely-positive-cones]] p.11

The resulting defensible representability statement is the manuscript's
specific finite-lift threshold for the full and positive-loop box moment
hulls, together with its stated simple-vertex and sparse-graph transfers.
The source audit does not broaden this to every cone or every sparse graph.

## Benchmark, software, and classical construction citations

The official BoxQP repository README defines the data as instances of
maximizing `0.5 x'Qx + c'x` over the unit box and identifies its Basic,
Extended, and Extended2 subsets with the listed source papers. The
repository itself is undated; the key suffix in `BurerBoxQPInstances2019`
must not be presented as a publication year. The new BibTeX entry is an
undated online dataset record. [[burer0000-boxqp-instances]] p.1

Goulart and Chen describe Clarabel as a primal-dual interior-point solver
for conic programs with quadratic objectives. Their comparisons are tied to
the specific benchmark sets, settings, and time limits in the paper; they do
not establish general solver dominance. The manuscript's exact Clarabel
version is a separate release citation. [[goulart2024-clarabel-an-interior-point-solver]] p.1
[[goulart2024-clarabel-an-interior-point-solver]] p.13-14

O'Donoghue, Chu, Parikh, and Boyd describe SCS as a first-order ADMM method
on a homogeneous self-dual embedding, designed for large problems at
modest accuracy; they note that high accuracy can require substantially
more iterations. Its method paper and the SCS 3.3.1 release record are
distinct sources. [[donoghue2016-conic-optimization-via-operator-splitting]] p.1-2
[[donoghue2016-conic-optimization-via-operator-splitting]] p.17-21

For classical construction names, the read McCormick source supports the
factorable underestimators, while Sherali–Tuncbilek directly applies RLT to
bounded continuous polynomial programs. These are the better attributions
for the paper's box inequalities and continuous RLT discussion. Sherali–Adams
is a zero-one RLT hierarchy and should be cited only for that discrete
hierarchy, not as the sole source of continuous box-product inequalities.
The Shor 1987 item can support bibliographic attribution to the named
condition, but its primary text was not retrieved; do not attach a theorem
number, page locator, or more detailed claim to it. A versioned Gurobi
reference is not recommended: the paper reports archived incumbent data,
not a version-specific solver claim.

## Citation-key and source-status ledger

The following citations are supported by a readable primary source in the
KB unless marked otherwise. `references.bib` contains the BoxQP key and the
verified solver and classical suggestions; the manuscript's TeX was not
changed in this audit.

| Use | Bibliography key | Source and status |
|---|---|---|
| Exact box and triangulated-polytope hulls | `AnstreicherBurer2010` | Read; Theorems 6–7, as scoped above. |
| Cone separation and recursive relaxations | `BurerDong2013` | Read; exact separation is distinct from finite SDP representability. |
| Named sparse SDP system | `Khajavirad2026SparseBoxQP` | Read arXiv v2; equation (17), limited to that system. |
| Named ETRI/SOC system | `AnstreicherPuges2025ETRI` | Read arXiv v1; equations (14)–(16), Lemmas 4–5. |
| Submodular SDP exactness | `BurerNatarajanWillemsen2025` | Read arXiv v3; Theorem 1 is objective-value tightness for the stated class. |
| Rank-one subtraction and minimal-zero criterion | `Hildebrand2014MinimalZeros` | Read arXiv v4; published metadata verified; version-of-record text not separately read. Receipt linked above. |
| Field-preservation and orthant obstruction | `BodirskyKummerThom2024` | Read final JEMS article; online 2024, volume year 2026. |
| Symmetric-cone nonrepresentability | `Nishijima2026` | Read arXiv v3; adjacent cone result. |
| Order-four CP=DNN identity | `MaxfieldMinc1962` | Original read; extracted text unusable, so theorem checked against the downloaded original PDF. |
| Order-four historical parallel | `Diananda1962` | Metadata and publisher extract only; full text unavailable. Maxfield–Minc independently supports the needed order-four identity. |
| BoxQP benchmark collection | `BurerBoxQPInstances2019` | Official README read; undated dataset, key suffix is not a year. |
| Clarabel method | `GoulartChen2024` | Read arXiv v1; not a version record. |
| Clarabel 0.11.1 | `ClarabelSoftware2025` | Official release HTML checked; KB package remains unread because `lit.py get` rejected the HTML body. |
| SCS method | `ODonoghueEtAl2016` | Read final journal-form author PDF. |
| SCS 3.3.1 | `SCSSoftware2026` | Official release HTML checked; KB package remains unread because `lit.py get` rejected the HTML body. |
| Factorable underestimators | `McCormick1976` | Existing readable KB source. |
| Continuous polynomial RLT | `SheraliTuncbilek1992` | Existing readable KB source; recommended for continuous box-RLT attribution. |
| Zero-one RLT hierarchy | `SheraliAdams1990` | Existing readable KB source; scope is zero-one programming. |
| Shor condition | `Shor1987QuadraticOptimization` | Bibliographic identity only; no accessible primary full text or theorem locator. |

### Remaining access limits

Full-text access limits remain for Diananda's 1962 article (publisher
metadata/extract only) and Shor's 1987 article (bibliographic identity
checked, but no lawful open text located). The official version pages for
Clarabel 0.11.1 and SCS 3.3.1 were inspected, but their KB packages remain
unread because their HTML bodies were rejected by `lit.py get`. The
Clarabel and SCS method papers are readable and do not substitute for those
release records. Maxfield–Minc is a read source despite its failed text
extraction: the original PDF was read directly. No theorem or page claim in
this audit depends on an unread source.

## Novelty recommendation

Keep the manuscript's current narrow formulations: (i) the specific valid
three-variable inequality family and its order-five exact semidefinite
enforcement; (ii) the rational witness against Khajavirad's displayed
disjoint-support system and the specified switched Anstreicher–Puges SOC
system; (iii) the extreme-ray classification only for positive square
coefficients with no zero at a cube vertex; and (iv) the finite-lift
obstruction and constructions for the exact box and sparse-graph classes
proved in the paper. Preserve the explicit acknowledgement of the known
three-variable hull. BKT, Nishijima, and Hildebrand supply external tools or
criteria; the manuscript's box/graph transfer, facet and contact analysis,
and exact named-system separator are the asserted contributions. Treat
priority wording as “to the best of our knowledge” within this bounded
source comparison, not as exhaustive publication clearance.
