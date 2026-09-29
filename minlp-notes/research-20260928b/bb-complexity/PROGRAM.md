# Program: relaxation-intrinsic complexity of branch-and-bound in MINLP

Selected 2026-09-28 from the scouting wave (see ../scouting/). Sources:
`../scouting/bb-tree-size-convex.md` (integer branching with nonlinear
relaxations, midpoint conflicts) and `../scouting/spatial-bb-theory.md`
(spatial branching, certificate integrals).

## Thesis to establish or refute

The size of any branch-and-bound tree for a MINLP is bounded below by a
quantity determined only by the node relaxation and the geometry of the
near-optimal set: a cover number of that set by "relaxation-admissible"
regions. Simple branching rules attain it up to explicit factors under
regularity. Consequences should explain when branching cannot help and
relaxation strengthening is necessary, and should explain observed
phenomena (the cluster effect, degenerate optimal sets, the sparse
regression phase transition).

## Workstreams (one owner each; separate files)

- `integer-core/`: midpoint-conflict framework for integer (and
  mixed-integer) branching with convex relaxations; random CVP; perspective
  versus pairwise hull; path lemma; tightness for split trees.
- `sparse-regression/`: phase transition of perspective-relaxation B&B in
  random sparse regression; easy side (linear trees above a threshold) and
  hard side (large conflict cliques below a threshold).
- `spatial-constrained/`: certificate-integral theory for spatial B&B with
  constraints (stratified near-optimal sets) and matching upper bounds.
- `spatial-face-exact/`: node complexity for McCormick/multilinear
  relaxations whose gap vanishes on box faces; branching-point placement.
- `branching-competitiveness/`: whether some node-local spatial branching
  rule is within a constant (or polylog) factor of the optimal certificate
  on every instance.

## Standards

- State every theorem with complete hypotheses (node model, what a leaf is,
  pruning rules, tolerance convention, allowed bound tightening).
- Give full proofs, not sketches, for anything labeled Theorem/Lemma.
  Label conjectures and heuristic arguments as such.
- Use targeted computations to test claims; exact arithmetic where cheap.
  Record commands actually run and what each check establishes.
- Novelty: record sources examined; an unsuccessful search does not
  establish novelty. Credit Dey–Dubey–Molinaro (midpoint/cross-polytope
  argument) and Bachoc–Cesari–Gerchinovitz (Lipschitz certificate
  integral) as the closest known mechanisms.
- Do not run project-wide checks or inspect CI. Do not commit.
