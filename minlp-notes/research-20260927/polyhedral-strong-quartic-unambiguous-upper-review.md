# Independent review of the unambiguous constrained upper bound

Date: 2026-09-28. Reviewer: `posslp_proof_adversary`, with fresh
narrow reviews requested from `gls_circuit_objective_audit` and
`up_mask_narrow_audit`.

Reviewed manuscript:
[Unambiguous certificates for exact strongly convex quartic optimization](polyhedral-strong-quartic-unambiguous-upper.md).
Frozen SHA256:
`c173045b8871a92a96b5cb293b358d5fd7b4eff32ad8772f7dc63a142634613d`.

**Verdict: pass, subject to three minor presentation repairs.** The
primary reviewer and two fresh narrow reviewers found no substantive
mathematical defect. Close the display after equation (4), change
`qquad` to `\qquad` in equation (9), and explicitly make invalid Gram
certificates reject in the original language and accept in its
complement before applying empty-polyhedron conventions. The last
repair makes the intended branch precedence unambiguous.

The reviewer did not contribute to this construction. Previous reviews
covered the companion unconstrained observable theorem and the earlier
constrained active-support and supplied-slack-gap results. Those are
explicit dependencies here, not newly inferred consequences of the
complexity of representing algebraic numbers.

## 1. What the theorem claims

The result concerns explicit rational degree-at-most-four objectives,
arbitrary explicit rational polyhedra, and a supplied valid positive
global curvature bound. On that promise, each exact value or minimizer
coordinate comparison has an unambiguous polynomial-time verifier with
a PosSLP oracle, and so does its complement. A polynomial-time checked
full positive definite Hessian Gram gives ordinary languages instead.

The proof neither identifies the active set deterministically nor gives
a single PosSLP instance for the constrained problem. It supplies a
unique certificate, followed by a deterministic polynomial number of
oracle queries. These distinctions are stated correctly in the note.

## 2. The rational LP arithmetic model

I read the local primary text of Grötschel, Lovász, and Schrijver,
[*Geometric Algorithms and Combinatorial Optimization* (1988)](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf),
Section 1.3, Theorem 6.2.13 and its proof, and printed pages 189--191
containing the arithmetic model and Theorem 6.6.3. I also inspected the
rendered page 168 to disambiguate the normalized rounding formula.
The browser could not load the 37 MB PDF; the author-hosted PDF was
already available locally and was the primary text examined.

Theorem 6.6.3 provides an arithmetic-operation bound polynomial in the
explicit constraint matrix encoding, independent of the objective and
right-hand-side lengths. It supplies an optimal vertex when one exists.
The bounded nonempty polytope in Lemma 1 satisfies that existence
condition even if its affine dimension is smaller than the ambient
dimension.

The source's division convention deserves explicit attention. Its
default model allows rational division and conversion to an integer
when integrality is already known. It does not include an unrestricted
floor or divisibility oracle. Some algorithms elsewhere in the book
use a stronger convention; that alone would not justify this circuit
simulation. Here the relevant Frank--Tardos step rounds a normalized
vector whose coordinates lie in a known bounded interval. Its integer
rounding can be performed with polynomially many comparisons. The
subsequent number-theoretic computation receives explicitly bounded
integer data. Thus the relevant LP construction has no hidden need to
read exponentially many objective bits, perform unrestricted integer
division, or expand a circuit value.

Independently of expanded rational sizes, each arithmetic operation can
append a constant number of shared numerator/denominator gates.
For a quotient of two represented rationals, the note's formula gives
denominator `D1 * N2^2`, which is positive when the actual divisor is
nonzero. Comparisons therefore reduce to signs of integer circuits;
equality may use two sign queries. Known-integral values can remain
rational circuits, since the simulation does not need their expanded
integer representation. Binary encodings of the initial explicit
constants give polynomial-size circuits built from the PosSLP constants.

The separate vertex recovery step is sound. At a vertex, all active
constraint normals span the ambient space. Otherwise a nonzero common
null vector permits a short feasible segment in both directions:
inactive constraints have positive slack and there are finitely many
of them. This proof also covers lower-dimensional polytopes. Exact
queries identify all active rows of the circuit output. A deterministic
rank calculation selects an invertible explicit subsystem, whose
unique solution has polynomial-bit rational coordinates by determinant
bounds. The recovery does not expand any circuit integer.

## 3. Uniform separation and the approximate objective

For the tangent-direction polytope, every vertex is determined by an
invertible subsystem of explicit rational inequalities. Clearing their
denominators and applying Cramer's rule gives a uniform polynomial bound
on every vertex's coordinate encoding. This is a bound over all
vertices, not an enumeration algorithm.

For each such vertex `v`, the polynomial `h_v(Y) = v^T C(Y)` has degree
at most three and polynomial total coefficient encoding. Products and
sums of the printed rational coefficients preserve this bound; possible
cancellation only makes the final encoding shorter. A computable
polynomial bound `M` on the combined encodings of `g`, the supplied
curvature, and every `h_v` can therefore be selected before any vertex
is known.

The companion singleton real-projection argument, with its effective
monotone polynomial `a`, gives the same nonzero gap
`gamma = 2^(-2^(a(M)+1))` for every vertex value. It does not require a
finite complex critical locus. Padding the Newton construction to `M`
also gives one ordinary rational starting point and one shared Newton
circuit with error at most `gamma/8` in every `h_v`. This works because
the derivative bound depends on the coefficient encoding bound, while
the starting point and Newton steps depend only on `g`, the curvature,
and the padded bound. There is no hidden collection of vertex-specific
starting points or circuits.

If a negative true vertex value exists, one approximate value is at
most `-7 gamma/8`. Every true nonnegative vertex value has approximate
value at least `-gamma/8`. Hence every optimal vertex for the approximate
rational objective has negative true value in that case. If no negative
true value exists, every chosen vertex has nonnegative true value.
This reasoning handles ties and the case where all true vertex values
are zero. The final query uses the explicit cubic polynomial for the
recovered rational vertex; it does not apply the observable theorem to
an arbitrary circuit function at the algebraic minimizer.

The finite gap and Newton construction are used only to construct a
sufficiently accurate rational LP objective. The proof correctly keeps
the final exact algebraic sign check separate.

## 4. Full active masks and unambiguity

For any guessed mask, a deterministic row basis gives consistent basis
equations because independent rows define a surjective linear map.
The remaining equations may be inconsistent, but the exact full-mask
test rejects them. The free-coordinate chart has an identity block, so
`Z^T Z >= I`; the restricted objective retains the supplied curvature.
For full row rank the restriction is a rational point, handled without
a positive-dimensional Newton construction.

The exact mask test enforces zero slack on every selected row and
strictly positive slack on every unselected row. It therefore handles
redundancy and zero normals without an extra convention: a zero row
with zero right-hand side must be selected, a zero row with positive
right-hand side must be unselected, and a negative right-hand side is
already an empty-polyhedron case.

For a passing primal point, every feasible displacement satisfies the
selected homogeneous inequalities. Scaling puts any such displacement
inside the bounded direction polytope, without changing the sign of
its gradient pairing. The gradient test thus implies first-order
optimality, and strong convexity identifies the point with the unique
global constrained minimizer.

Conversely, at the true minimizer, polyhedral normal-cone optimality
puts the gradient in the row span of all active normals. Every direction
in the affine restriction's nullspace has zero gradient pairing, so
the true point is the unique minimizer of that restriction. The full
active mask consequently passes. This does not require nonnegative
multipliers on the deterministically selected row basis, Slater's
condition, strict complementarity, or a positive slack margin.

Any passing mask must now describe the active rows of the same unique
point, so exactly one mask passes optimality verification. Guessing
exactly one bit per input row gives one computation for that mask.
All basis selection, rational LP choices, and oracle queries can be
made deterministic; no multiplier support is guessed.

The final predicate and its logical complement select the accepting
side without creating additional certificates. Empty polyhedra,
zero-dimensional ambient problems, and malformed or invalid checked
Gram certificates are handled deterministically before branching.
For the ordinary languages the complement must accept invalid
certificates on its deterministic branch, and certificate validity
must be checked before assigning an empty-set truth value. This is
consistent with the theorem's stated language convention, but should
be explicit in the algorithm paragraph. For the bare-curvature
formulation the statement is only on the promised inputs. These
distinctions preserve the asserted unambiguity.

## 5. Verification and limits

The author checker was read and rerun with:

```text
python research-20260927/check_polyhedral_unambiguous_upper.py
```

It passed 168 masks across six rational quadratic examples, 17 vertex
recoveries, and 1466 approximate-objective optimal-vertex sign checks,
including ties. These exact finite checks cover useful degenerate
cases. They do not implement PosSLP or the GLS LP algorithm and do not
prove the uniform algebraic bound or the all-input unambiguity claim.
Those are supported by the proof reconstruction above. No Lean check,
project-wide verification, or CI inspection was performed.

The claim is a complexity refinement built from substantial existing
tools and the companion theorem. No practical speedup follows merely
from this membership result. This review does not certify publication
priority; the manuscript appropriately leaves priority unestablished.
The separate literature search should remain distinguishable from a
proof that no equivalent result exists.

## 6. Additional narrow reviews and final reconciliation

`up_mask_narrow_audit` independently read Sections 3--4 at the frozen
hash. It found no counterexample or missing polynomial input-size
bound. It checked the common Newton error bound, lower-dimensional
and full-rank restrictions, inconsistent dependent rows, zero normals,
and complement predicates. It requested the explicit invalid-input
branch precedence recorded above.

`gls_circuit_objective_audit` independently examined the GLS arithmetic
model and the relevant construction in Sections 5.3, 6.2, 6.5, and 6.6,
including a visual check of page 168. It confirmed that the potentially
large circuit-dependent residuals require only rational arithmetic and
comparison. The number-theoretic and ordinary LP subroutines receive
small explicit data after bounded rounding. It also independently
checked active-row vertex recovery. It found no source/model defect.

The primary reviewer checked both reports against the manuscript and
the source excerpts. These are independent supporting reviews, not a
substitute for the reconstruction in this file.

Targeted whitespace check passed:

```text
git diff --check -- research-20260927/polyhedral-strong-quartic-unambiguous-upper-review.md
```

Final reconciliation: the amended manuscript has SHA256
`2a230e2e92dd25f12b92b052f5d2b65bfe658fae6230b1fd46b1b582557a9791`.
The reviewer confirmed the repaired display delimiters, `\qquad`, and
the explicit certificate-validity branch before the empty-polyhedron
convention. The other additions are status, review/search links, and
the finite-check disclosure. They do not change the mathematical
construction. The review is closed with a pass at this final hash.
