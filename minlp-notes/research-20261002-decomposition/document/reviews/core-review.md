# Independent review of the core algorithm

Date: 2026-10-02.

Scope: `document/main.tex`, from the model through the exact quadratic
theorem and explicit-polynomial corollary. The pending extensions and
computational sections were not reviewed. This review compared the synthesis
with `research-20261002/new-direction/pruned-coordinate-grid.md`,
`research-20261002/new-direction/polynomial-pruned-grid-extension.md`, and
`research-20261002/geometric-dp/exact-box-qp.md`.

## Status

The mathematical core passes this review. No substantive gap was found in
the interpolation certificate, filtering history, contraction and state
counts, capped unknown-growth search, rational arithmetic, or exact-output
argument. Two small specification amendments should be included so that the
algorithm and polynomial bit-complexity statement are fully explicit.

1. **Specify the initial rational center.** Start each trial at the original
   lower endpoint vector, with its evaluated feasible upper bound. The
   contraction argument correctly permits any feasible center, but the bit
   proof needs its initial center to have a denominator dividing the selected
   common denominator. An unrestricted externally supplied center need not
   satisfy that requirement. Choosing the lower endpoints supplies the
   missing base case without changing any proof or bound.
2. **Charge alternate curvature verification to the input.** The polynomial
   subsection permits a sharper checked curvature bound. Include the
   accepted rational bound and any alternative certificate in the input
   length, and require that certificate to have polynomial verification
   cost. The explicit interval-arithmetic construction already has that
   property. The source polynomial theorem states these obligations
   explicitly; merely saying “checked” does not bound a checker's work.

These amendments were sent directly to the document author. They are
clarifications of the algorithm and complexity model, rather than changes
to the main mathematical result.

## Mathematical findings

- The curvature condition is imposed on the sum of factors throughout the
  full continuous hull. This retains the hypothesis needed for sequential
  mean-preserving rounding, including fractional points between integer
  labels. Ignoring integer unit intervals is valid because they have no
  feasible interior points.
- The conditional interpolation inequality supports both interval filtering
  and preservation of the feasible incumbent. The document retains the full
  filtering history and uses the first exclusion of each removed point.
  This correctly certifies the original box, rather than only the final
  restricted box.
- The two directed tree passes use sums of incoming messages and exclusions,
  not a product over children. Running intersection justifies the component
  separation. The stated table-operation bound does not introduce a hidden
  variable-occurrence parameter.
- The contraction coefficient `1/15`, the choice
  `B0 = max(1, 4L/(11g))`, the gap constant `7/8`, and the retained-witness
  constant `22/15` are consistent. The radius five is conservative. The
  additive one for integer domains is retained, as required for unit
  intervals that survive through only one qualifying endpoint.
- The integer step bound with `H = max(h, 1)` is valid. For `h < 1`, split
  at `theta*t = 2`; for `h >= 1`, use the elementary floor bound. Together
  with localization, it gives a state count independent of stage number.
- The search aborts before allocating tables if a coordinate grid exceeds
  the cap. This is essential to bounding unsuccessful earlier trials. The
  logarithm-power absorption leaves an ordinary input-size exponent
  independent of bag size.
- Once its initial center is specified as above, the common-denominator
  induction is valid: clipping inherits endpoints, recentering inherits a
  grid label, and the geometric offsets introduce only bounded additional
  powers of two. The denominator does not multiply over refinement stages.
  Message values are sums and selections on a common denominator.
- The rational-height proof correctly fixes an integer assignment only as
  an existence argument. A singular free continuous Hessian yields a flat
  direction and a smaller optimal face. It does not require enumerating
  integer assignments. The isolated-optimizer version follows from the
  same local argument.
- Uniqueness implies qualitative global quadratic growth for a quadratic
  on a compact mixed box. The proof correctly applies first-order
  optimality only after the integer assignment has stabilized.
- Exact reconstruction isolates the optimal value using the height bound,
  reconstructs coordinates only within disjoint denominator-bounded
  windows, and verifies feasibility, integrality, and exact objective
  equality. The threshold `g/(32 R^4)` puts the incumbent strictly inside
  the radius `1/(4 R^2)`. Doubling the requested precision preserves the
  stated fixed-parameter bit bound. No discrete gap between arbitrary
  continuous feasible values is assumed.
- The polynomial corollary keeps fixed numerical degree, explicit
  monomial-list encoding, full-hull curvature verification, and the
  quadratic-growth hypothesis. Its integer exactness argument uses the
  original coefficient denominator. It does not incorrectly extend
  rational-QP reconstruction or uniqueness-implies-growth to continuous
  polynomial objectives.

## Targeted verification actually run

Read-only comparisons used `sed -n` and `cat` on the four documents named
above. A targeted inline Python command, invoked as
`python3 - <<'PY'`, used `fractions.Fraction` to check:

- 75 admissible curvature-ratio and mesh-parameter combinations for the
  contraction induction and localization constants;
- 352 continuous and integer grids inside the proved retained radii;
- 23,770 exact adjacent-mesh inequalities on those grids;
- 30 common-denominator checks over a seven-stage rational-grid sequence
  with clipping, recentering, and inherited endpoints;
- the squared exact-reconstruction distance threshold.

The command printed:

```text
{'constant_cases': 75, 'state_count_cases': 352,
 'mesh_node_checks': 23770, 'common_denominator_node_checks': 30,
 'result': 'all assertions passed'}
```

These finite checks support the independent proof review; they do not prove
the universal statements or benchmark the complete solver. No project-wide
verification, CI status, or CI logs were inspected. The manuscript was not
modified by this reviewer.
