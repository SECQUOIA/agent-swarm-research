# Independent review of the constrained strongly monotone extension

Date: 2026-09-28. Status: pass; no substantive defect found.

Reviewed manuscript:
[Exact observables of strongly monotone cubic variational inequalities](polyhedral-strong-monotone-vi-upper.md).
Frozen SHA256:
`c58c1e4ddd156f9cf2b8820258f1b63197bca2f4c07d713092120abcdf28e232`.

The primary reviewer, `posslp_proof_adversary`, did not contribute to
this extension. The genuinely fresh reviewer `vi_extension_fresh_audit`
separately checked existence, affine restriction, the active-mask
argument, and input degeneracies. That reviewer also obtained a further
independent check of existence and dimension-zero handling. All found
no substantive gap in the specified scope.

This is a scoped review of the extension. The reviewed dependencies are
the [unambiguous constrained quartic argument](polyhedral-strong-quartic-unambiguous-upper-review.md)
at final main hash
`2a230e2e92dd25f12b92b052f5d2b65bfe658fae6230b1fd46b1b582557a9791`
and the [strongly monotone zero theorem](strong-monotone-cubic-posslp-upper-independent-review.md)
at final main hash
`a3322129b57f590a9121aaf2d8fd80e29a457bc64747235fa7c582c7cc17c058`.
I read the latter theorem and its proof review to check the precise
interface. This report does not claim a new full source audit of its
ellipsoid warm start or repeat the completed GLS LP source review.

## 1. Existence on an unbounded or lower-dimensional polyhedron

For any point `x0` in the nonempty polyhedron, the intersection with a
closed ball centered at `x0` is nonempty, compact, and convex. Euclidean
projection onto this set is continuous. Brouwer's theorem applies in
the affine hull; a singleton is an immediate special case. Its fixed
point satisfies the variational inequality on the truncated set by
the projection characterization.

If that point were on the artificial sphere of radius
`R > ||T(x0)|| / mu`, strong monotonicity would give
`T(p) dot (p-x0) > 0`. The inequality tested at `x0` gives the
opposite weak sign. The point therefore lies strictly inside the ball.
For each point of the original polyhedron, a sufficiently short
positive segment from `p` toward that point remains inside the ball
and the polyhedron. Dividing the variational inequality on that
segment by its positive parameter proves the inequality for the full
unbounded set. No uniform segment length over all points is required.

For two solutions, testing their inequalities at one another gives
`(T(p)-T(q)) dot (p-q) <= 0`, while strong monotonicity bounds this
quantity below by `mu ||p-q||^2`. Thus the solution is unique. The
argument needs neither a scalar potential nor a polyhedron with
nonempty ambient interior.

## 2. Affine restriction and the monotone-zero interface

A row basis of the guessed active normals has consistent basis
equations and a rational free-coordinate chart with polynomial-bit
coefficients. Its identity block gives `Z^T Z >= I`. For the map
`U(y) = Z^T T(bar_x + Z y)`, the strong-monotonicity pairing is exactly
the pairing for `T` on the two chart points. It is therefore at least
`mu ||Z(y-z)||^2 >= mu ||y-z||^2` for all real chart coordinates.
This is global strong monotonicity, not just monotonicity on the
feasible part of the chart.

Substitution into an explicit fixed-degree polynomial preserves
polynomial total encoding length. The zero theorem applies to `U`
with the same supplied modulus. A new full positive definite Gram
for the restricted map is not needed: the original certificate, when
that format is used, has already established the global inequality.
Rank equal to the ambient dimension gives a rational point and uses
rational arithmetic and the required direction LP instead.

The normal-test observable for a rational vertex `v` is
`v^T T(bar_x + Z y)`, an explicit polynomial of degree at most three.
The desired final observable remains explicit and degree at most four.
The determinant bound for vertices of the boxed tangent polytope gives
a common polynomial encoding bound `M` for every normal-test
observable. This is exactly the interface required by the zero
theorem; no circuit-defined algebraic observable is introduced.

I checked the changed constants rather than importing the quartic
constants silently. The monotone theorem uses `B = 2^(30M)` and an
effective monotone polynomial `a` with `a(M) >= 60M+10`. Its common
warm start and `a(M)+2` Newton steps give, for every vertex observable,
error at most

```text
2^(31M+1 - 12*2^a(M)) <= gamma/8,
gamma = 2^(-2^(a(M)+1)).
```

The same rational Newton point works for all vertices. As in the
reviewed quartic argument, a negative true value has approximate value
at most `-7 gamma/8`, while a nonnegative one has approximate value
at least `-gamma/8`. A circuit-objective LP therefore selects a vertex
of negative true value exactly when some negative value exists; the
last explicit observable query checks its true sign. The LP source,
positive-denominator circuit simulation, and printed-vertex recovery
are unchanged dependencies.

## 3. Soundness, completeness, and a unique accepting mask

The exact slack test enforces both feasibility and the full active
mask. Every displacement toward a feasible point satisfies the guessed
active homogeneous inequalities and can be scaled into the tangent
box. Passing the direction test therefore proves the variational
inequality. Uniqueness identifies the constructed point with the
actual solution.

At the actual solution, every direction satisfying the active
homogeneous inequalities gives a sufficiently short feasible segment:
there are finitely many inactive rows, all with positive slack.
The variational inequality on those segments and Farkas' lemma give
`-T(p)` in the cone of active normals. Hence `T(p)` lies in their row
span, and `Z^T T(p) = 0`. The reviewed zero theorem identifies this
chart point with the unique zero of the restricted map. The full true
mask consequently passes every test.

Any passing mask must describe the active rows of that same point, so
the optimality certificate is unique. Redundant normals, zero rows,
zero multipliers, and inconsistent extra guessed equations do not
break this argument. The last case is rejected by the exact slack
test. A rank-full chart must still pass the tangent test; the note
correctly retains it. An arbitrary rational vertex is not automatically
a variational-inequality solution.

The predicate in this extension explicitly includes nonemptiness.
Thus an empty polyhedron rejects in the original language and accepts
in its complement. Invalid checked Gram certificates receive those
same outcomes before the empty-set branch. Ambient dimension zero
reduces to rational feasibility and a constant observable. The rank
zero/full-rank convention and the inherited deterministic handling
suffice; there is no call to a positive-dimensional zero construction
in that case. All later choices are deterministic, so appending a
predicate or its complement preserves unambiguity.

## 4. Targeted verification

I wrote and ran the separate exact check:

```text
python research-20260927/check_polyhedral_monotone_vi_review.py
```

It passed symbolic checks of a three-dimensional radial cubic plus a
nonzero skew linear map, a two-dimensional affine restriction whose
Jacobian still has a nonzero skew part, a full active mask with
redundant and zero rows, and the rejection of an incorrect rational
feasible point. The rejection uses a boxed tangent direction with
exact pairing `-283/19200`, which checks the sign orientation.
The polynomial derivative identities explicitly verify that this
example and its restriction are strongly monotone and nonpotential.

The fresh narrow reviewer separately reports an inline exact SymPy
check of 191 masks and 42 tangent vertices across nine affine,
nonsymmetric strongly monotone examples, including unbounded,
lower-dimensional, singleton, redundant, inconsistent-guess, and
dimension-zero cases. That command was run by the narrow reviewer,
not by the primary reviewer.

These finite checks do not establish general existence, the algebraic
gap, the LP arithmetic bound, or the complexity theorem. They support
the proof reconstruction and exercise the new nonpotential scope.
No PosSLP implementation, Lean verification, project-wide tests, or
CI inspection was performed. Publication priority is not established
by this review, and the manuscript correctly treats the existence
argument as classical and the new result as a scope extension.

Targeted whitespace checking passed for this review and its checker:

```text
git diff --check -- research-20260927/polyhedral-strong-monotone-vi-upper-review.md research-20260927/check_polyhedral_monotone_vi_review.py
```

## 5. Final reconciliation

The amended main has SHA256
`85afe45372dadb8d374903eb3d58c0643e340f89b2ea68cb49718c38b840a6cc`.
Its status, dependency closure, and verification disclosures were
inspected and agree with this review. The theorem and proof are
unchanged apart from removing the provisional dependency caveat.

The added two-dimensional example was independently checked by an
inline `python -` command using SymPy. For the displayed translated
radial cubic plus the matrix with rows `(1,2)` and `(-2,1)`, exact
expansion verified the quadratic derivative pairing, the skew
Jacobian difference `4`, the map value `(-1,0)` at `(0,1)`, and the
restricted equation `(y-1)+(y-1)^3`. On `x <= 0, y >= 0`, the
claimed variational-inequality pairing is indeed `-x >= 0`. The
example is correct and does not change the theorem's scope.

The final hash was confirmed with `sha256sum`, and the targeted
review/checker `git diff --check` passed. The review is closed with
a pass at this final hash.

## 6. Limited terminology check

After closing the proof review, I ran the following web searches:

- `"variational inequality" "violator" space`
- `"strongly monotone" "Clarkson"`
- `"variational inequalities" "LP-type"`

The returned results did not identify a matching primary theorem.
Several used Clarkson's name for uniform convexity of Banach spaces,
which is unrelated to the randomized constraint algorithms. Those
results were not used as mathematical evidence. These three searches
are too narrow to establish publication priority or exclude an
equivalent formulation.
