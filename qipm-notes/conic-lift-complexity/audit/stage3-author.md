# Stage 3 author report

## Scope and files

Added `sections/06-restricted-barriers.tex` and integrated the independently
written `sections/07-concrete-barriers.tex`. Updated `main.tex` and bibliography.
The manuscript now distinguishes the least parameter of the specified standard
restriction from the infimum over all self-concordant barriers on a fixed lifted
domain. No existing paper or workbench source was edited.

Two bounded independent tasks ran alongside authorship: the concrete formulation
section, and a mathematical check of the fixed-generic-label reduction. These
are distinct from the five formal Stage 3 reviews, now complete; all five found
no major issue. The accepted minor corrections are recorded in
`stage3-assessment.md` and `stage3-corrections.md`.
Their reports are `stage3-concrete.md` and `stage3-rigidity-check.md`.

## Results independently reconstructed

- Exact gradient quotient on the effective affine slice; Jordan determinant
  boundary order at every tuple; derivative-level two-parameter recession bound.
  The latter is extended to all EJAs using the Jordan Schur determinant formula,
  rather than associative matrix manipulations.
- Selection-free generic lower bound, grouped exact standard parameter,
  off-divisible exact optimum, and exact globally smooth product optimum.
- Critical one-channel full-certificate-fiber rigidity for every EJA dictionary,
  including Albert, and sequential product certificate rank / parameter 2b.
- Factor-count-independent compact face-codimension bound with explicit
  homogenizing-height argument; wide-cap Hermitian and Lorentz exact frontiers.
- Full-certificate range-collapse codimension and compact incidence reduction.
  A new checked refinement establishes one fixed generic active-label pattern
  when B>=2. The independent proof is in the rigidity-check report.
- Rotated perspective counterexample: minimum primal fiber nullity q, maximum
  certificate rank q at every support, exact restricted parameter 2q-1; separate
  heterogeneous products preserve the exact distinctions.
- Exact standard norm-tree root-incidence formula and combinatorial cap optimum;
  intrinsic lower L and logarithmically homogeneous cone lower L+1.
- Exact arbitrary-barrier grouped and column-packed parameters, via interior
  box sections and rigorously bounded-fiber partial minimization respectively.
  Column packing is formulated over R/C/H and heterogeneous nonzero column
  subspaces. Intrinsic parameter differs from ambient cone rank and factor count.

## Corrections to source claims and proof scope

1. One-channel lower bound must assume hypothetical parameter <2, not merely
   <=1. Integer boundary orders then justify rank-one fibers. The result is an
   optimum over lifts, not the parameter of every lift whenever a spin factor
   is present.
2. An O(1) barrier-value expansion alone does not establish a recession gradient
   parameter bound. The paper proves scaled first and second derivative limits.
3. The full certificate-fiber minimum at the north pole of the rotated example
   is one, whereas the maximum is q. Minimum primal nullity is q everywhere.
4. No arbitrary-barrier lower bound is inferred merely from simultaneous
   determinant multiplicity. The repeated-block ball example disproves this.
5. Compact convex fibers do not automatically globalize projective channels.
   Explicit density-matrix and simplex-fiber examples identify the failure.
6. The incidence space has the cohomology of the support sphere, but this does
   not extend a generic kernel-line map across collapsed channels and does not
   supply a degree theorem. No unproved no-fold lemma is used.
7. We do not assert exact intrinsic norm-tree optimality. The proved interval
   is [L, standard root-incidence parameter]. The concrete author supplies an
   exact rational counterexample to a proposed logarithmic correction.

## Remaining mathematical boundary

The generic fixed-label refinement was genuinely investigated independently.
It is proved, but it does not resolve collapse of a fixed pattern over the
exceptional range-collapse set. For bounded narrow-cap divisible lifts,
q>=B+2 and s=qB+1, the manuscript states the rigorous interval [q,q+1].
Neither an exact unrestricted frontier nor the absence of fixed-pattern collapse
is claimed. This is a remaining classification problem, not an assumption or
missing step in any asserted theorem. All currently proved nondivisible,
one-channel, unbounded, wide-cap, and globally smooth cases are complete.

## Per-source dispositions

- arbitrary-affine-psd-ball-barrier-cap: general boundary/recession bounds,
  grouped upper, and precise unresolved range; the escaping-disk example is
  explicitly included as Example escaping-disk, with Slater and exactness checks.
- arbitrary-factor-q2-lorentz-barrier-rigidity: proved as Lorentz wide-cap theorem.
- arbitrary-factor-wide-cap-hermitian-barrier-rigidity: full proof, including
  homogenization and projective-product contradiction.
- boundary-ray-multiplicity-barrier: subsumed by all-EJA boundary-order lemma;
  repeated-block counterexample records its arbitrary-barrier limitation.
- bounded-divisible-hermitian-seam-incidence-reduction: full convex incidence
  and generic-fiber facts retained; unproved degree extension rejected; new
  fixed-label refinement narrows the permitted mechanism.
- coupled-barrier-grouped-ball-slice: intrinsic grouped theorem and box section.
- extra-factor-bounded-lorentz-kernel-collapse: subsumed by arbitrary-factor
  wide-cap theorem, which is strictly stronger in the quotient-two range.
- fiberwise-nullity-selection-free-rigidity: **partially incorporated; mandatory
  Stage 4A coverage remains.** The singleton/continuity argument and a single-ball
  fixed-field constant-nullity consequence follow the wide-cap theorem. They do
  not subsume the heterogeneous product theorem for all symmetric cones under
  a dimension cap, or its every-boundary-tuple contact-accessibility corollary.
  Both are explicitly routed to Stage 4A, retaining compactness of the full
  preimage of the simultaneous extreme stratum and hypotheses at every tuple.
- h3r-local-pencil-obstruction: Example local-real-three-pencil now explicitly
  gives the local rank-two pencil, determinant and north-pole rank drop. Only
  the local-to-global shortcut is invalidated. The source's obsolete claim that
  the global PSD3 exception remains open is rejected: Proposition
  no-real-three-saturation already excludes it using finite affine gluing.
- hermitian-product-ball-standard-additive-frontier: standard parameter corollary
  of Stage 2 sequential smooth rank theorem, with matching constructions.
- hermitian-psd-standard-slice-barrier-frontier: same dictionary-cap synthesis.
- norm-tree-reduced-barrier-parameter: root-incidence exact formula, cap optimizer,
  intrinsic polyhedral-section bounds and correction counterexample in Section07.
- one-block-psd-packing-coupled-barrier: exact intrinsic packing theorem, generalized
  to R/C/H and heterogeneous column subspaces, with full projection hypotheses.
- product-ball-standard-slice-barrier-frontier: smooth product parameter sum.
- psd-nullity-restricted-barrier: subsumed by Jordan boundary-order lemma and
  Hermitian smooth frontier; no selection assumption silently removed.
- qgt1-hermitian-fiber-topology-obstructions: density-matrix and simplex examples.
- rotated-lorentz-fiberwise-nullity-counterexample: explicit complete example,
  certificate fibers, exact parameter and heterogeneous extension. Its
  objective-specific metric calculation is routed to Stage 5 if needed there.
- selection-free-exposed-rank-premium-counterexample: Stage 1 exact rank frontier
  plus Section06 rotated example distinguishing barrier from certificate ranks.
- selection-free-hermitian-one-channel-rigidity: subsumed by all-EJA theorem.
- selection-free-hermitian-standard-barrier-cap: full general/recession/collapse
  argument; new fixed-label refinement; open range explicitly stated.
- selection-free-lorentz-standard-barrier-cap: corresponding spin specialization.
- selection-free-psd2-nullity-seam-obstruction: proposed fiberwise premium rejected
  by rotated perspective; no false extra nullity in every completion claimed.
- selection-free-symmetric-cone-one-channel-rigidity: full corrected theorem and
  sequential product proof, including exceptional Albert case.
- symmetric-cone-standard-slice-barrier-frontier: smooth dimension-cap corollary
  permits all symmetric cone families, using maximal B=d-2.
- two-lorentz-factor-compact-ball-barrier-rigidity: subsumed by arbitrary-factor
  wide-cap proof; generic convex-fiber shortcut excluded by explicit examples.
- affine-psd-sequential-compression-without-selections (deferred Stage2): critical
  real result subsumed by all-EJA one-channel sequential theorem.

## Literature and prior manuscript overlap

The Jordan recession proof uses Gowda--Sznajder 2010 (existing verified source).
Vietoris--Begle is classical, not new here. Original Begle paper metadata verified
from the scanned primary paper at
https://webhomes.maths.ed.ac.uk/~v1ranick/papers/begle1.pdf
(Annals 51(3), 1950, 534--543, DOI10.2307/1969366). The standard compact-space
acyclic-fiber theorem is also explicitly stated in Section4 of McLennan's primary
paper https://arxiv.org/html/1909.11347, inspected online.
The concrete author checked the original NN active-facet bound and Chares
partial-minimization source; see their report for exact locators/bib entries.
Norm-tree root calculations, grouped/packed constructions, and some movement
connections already occur in `central-path-cost/`. Their self-contained reuse
must not be advertised as new repository developments. Section 7 now cites
the anonymous unpublished companion manuscript and states this relationship
explicitly, without inventing authors or a publication date. The current additions
concern optimization across formulations, selection-free rigidity, and the
precise parameter separations, not an invented new norm-tree construction.

## Final validation

`conda run -n qipm --live-stream make` completes successfully. Integrated PDF:
36 pages. Final `main.log` has no undefined references/citations, warnings,
or overfull/underfull boxes. Build transcript: `audit/stage3-build.log`.
The concrete author additionally checked the cap optimizer against exhaustive
small recursive trees and checked the self-concordance counterexample using
exact rational arithmetic; see `stage3-concrete.md`.

Post-review validation is recorded in `stage3-corrections.md`; the earlier
36-page build above is the original author snapshot.
