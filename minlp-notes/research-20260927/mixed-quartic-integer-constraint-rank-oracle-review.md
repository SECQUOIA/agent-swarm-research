# Independent review of the mixed-integer and constraint-rank composition

Date: 2026-09-28. Reviewer: `posslp_proof_adversary`.

Reviewed manuscript:
[Exact mixed-integer quartic optimization with few integer variables and low continuous constraint rank](mixed-quartic-integer-constraint-rank-oracle.md).
Frozen SHA256:
`73634fa1738881d462284594b2ce6c37a58e0080571f446ff5399ae18960cf67`.

**Verdict: pass.** No mathematical or parameter-accounting defect was
found. A separate genuinely fresh reviewer, `mixed_composition_fresh`,
independently checked the same composition and also passed it. That
reviewer obtained a further fresh check of output size, ties, and
degenerate cases. None of these reviewers contributed to this
composition.

This review accepts two independently reviewed dependencies at their
precise stated interfaces:

- [Mixed-linear candidate lists](mixed-linear-strong-quartic-candidate-list.md),
  final main SHA256
  `9c4a69a9527d498c8ca79ad8bb781fd26aedc311735a01c3e02174187ec7f448`;
  its [fresh proof and source review](mixed-linear-strong-quartic-candidate-list-review.md)
  is closed at that hash.
- [The constraint-rank oracle algorithm](constraint-rank-strong-monotone-oracle.md),
  final main SHA256
  `457a1cab90441d2a2528221875ed1e6e816f208d93d7ca0e91e219aa346e86c3`;
  its [independent review](constraint-rank-strong-monotone-oracle-review.md)
  is closed at that hash.

I read the candidate-list statement, initialization and dimension-zero
handling, its full final review, and the constraint-rank interface.
This report checks their composition. It does not claim another full
audit of the candidate-list proof or of the primary algorithms used
inside either dependency.

## 1. Feasible fibers and input lengths

The first dependency provides the needed strong guarantee: every
listed integer block is feasible, and every global optimal integer
block appears. It provides ordinary deterministic fixed-parameter
time and total printed output length, not merely a bound on list
cardinality. This distinction is necessary because the coordinates
of a candidate can have parameter-dependent bit length.

Fixing the integer block leaves the principal continuous Hessian
block of the original Hessian. It is bounded below by the same
positive `mu` on all real continuous coordinates. Each feasible
fiber therefore has a coercive strongly convex objective on a closed
nonempty polyhedron, so its minimum is attained and unique. Neither
boundedness nor a nonempty ambient interior is needed.

Let `Q = a(k) L^C1 + L` as in the manuscript. At degree at most four,
each monomial substitution uses a bounded number of products of
candidate coordinates. Summing the polynomially many resulting
rational terms and forming `c-Az` has polynomial bit cost in `Q`.
The exponent does not depend on the integer dimension or constraint
rank. Gradients and fixed-degree affine substitutions used internally
preserve that form of bound.

The candidate count is bounded by total output length after the
explicit zero-integer-variable convention. Removing duplicates and
sorting numerically in lexicographic order use polynomial time in
that output length. Sorting binary encodings for duplicate detection
need not be confused with the numeric ordering used for tie selection.

## 2. Exact comparison of two fiber minima

On independent variable blocks, the sum of two fiber objectives has
block-diagonal Hessian with the same lower bound `mu`. The feasible
set is their Cartesian product, so its unique minimizer is the pair
of the two individual minimizers. The difference of the two
objectives evaluated there is exactly the difference of their
minimum values.

The product constraint matrix is block diagonal with two copies of
`B`, and thus has rank exactly `2 rank(B)`. This remains true when
the rank is zero. Adding product inequalities introduces no other
normal directions. All product coefficients have polynomial encoding
length in `Q`, and the total variable dimension is still polynomial
in the explicit original length.

The difference observable need not be convex. The constraint-rank
theorem permits any explicit rational polynomial observable of degree
at most four, so this is within its reviewed interface. There is no
comparison of independently expanded algebraic numbers and no implicit
extension to arbitrary algebraic circuit observables.

The internal product need not have a full positive definite Hessian
Gram in the original certificate basis. The checked input certificate
already proves the global curvature inequality; its principal blocks
and their sum inherit a supplied valid modulus. The promise version
of the internal theorem is enough. The manuscript states this point
correctly rather than assuming Gram closure under a separable sum.

## 3. Selection, ties, and implicit output

A scan replaces its incumbent only when the next fiber value is
strictly smaller. Exact oracle answers make every such decision
correct. Keeping the incumbent on equality chooses the first
minimizer in the fixed lexicographic list order. Because every global
optimal block occurs in the list, this is the lexicographically
smallest optimal integer block in the entire original problem.
Feasibility and coercivity ensure that the optimal set is nonempty
and compact; its integer-block projection is consequently finite.

For the selected integer block there is only one continuous fiber
minimizer. The final single-fiber call returns a polynomial-size
rational chart and an explicit strongly monotone cubic map having a
unique real zero. The representation denotes that minimizer exactly.
Different successful random executions may return different charts,
but all represent the same point. The theorem does not claim short
expanded coordinates or a canonical chart.

The output-size bound need not contain an extra function of the rank.
Each chart is obtained by polynomial-size rational linear algebra on
one subset of the printed fiber rows, and its cubic map has polynomial
encoding length in the fiber input. Rank affects the number of
primitive calls, not the length of this one output. Combining that
bound with `Q` gives the stated `F0(k) L^C0` output length.

The chosen optimum's objective or any supplied fixed-degree
observable can be compared by the single-fiber theorem or through
the returned chart. A general observable at that selected optimizer
is not a claim about all tied integer-block optima; the manuscript
correctly makes this distinction.

## 4. Expected fixed-parameter running time

Each comparison uses continuous constraint rank `2r` and a uniformly
bounded input encoding. Its conditional expected runtime, after any
earlier computation history, is therefore bounded by
`(2r+1)^O(r) Q^C4`. There are at most `Q` comparisons and final
recovery calls up to a constant adjustment. Using fresh random bits
for each call permits the same expectation bound regardless of the
previous random running times or returned charts. Linearity of
expectation gives the claimed sum. The decisions and chosen integer
block are exact and independent of sampling outcomes.

To make the parameter accounting explicit, put
`d = max(C1,1)`. Since `L >= 2`,

```text
Q <= (a(k)+1) L^d.
```

Consequently `Q^(C4+1)` is at most
`(a(k)+1)^(C4+1) L^(d(C4+1))`. The exponent on `L` is an
absolute constant, and all parameter-dependent factors can be
absorbed into a computable `F(k,r)`. A computable bound depending
only on `k+r` follows by taking the finite maximum over pairs with
that sum. No parameter-dependent exponent of the original input
length is hidden in the composition.

Each call is always correct and has finite expected running time,
hence terminates almost surely. There are finitely many calls.
The composition is therefore Las Vegas with the stated expected
bound, rather than only a bounded-error algorithm. Each individual
PosSLP query has polynomial length in its enlarged fiber input,
although that input itself may have fixed-parameter length in the
original instance.

## 5. Degenerate and invalid inputs

When `k=0`, the first dependency returns the singleton empty block
after feasibility checking; no pairwise scan is needed. When `n=0`,
every feasible fiber is a rational constant problem, `rank(B)=0`,
and comparison and output use rational arithmetic directly. These
conventions include the case where both dimensions vanish.

If mixed-integer infeasibility is reported, there is no call to a
fiber oracle. The optional `+infinity` convention gives the correct
truth values for all finite-threshold predicates in that case.
For feasible instances, the mixed-integer feasible set is closed;
joint strong convexity gives coercivity and attainment, so no
unbounded-below or unattained-infimum case is omitted.

In the checked-certificate format, invalid certificates reject before
any feasibility or empty-value branch. In the bare-modulus format,
the algorithmic theorem is only a promise statement. The two
interfaces use these conventions consistently.

## 6. Verification and final reconciliation

The verification here consists of the dependency-interface read,
independent symbolic reasoning above, and frozen-hash checks. No new
computational test was needed for this elementary composition; a
small test of a product Hessian or scan would add little confidence
in the actual fixed-parameter and representation claims. The more
substantive exact checks and source audits remain recorded in the
dependency reviews. No Lean check, project-wide verification, or
CI inspection was performed.

The result is an exact parameterized oracle consequence. It supplies
neither an ordinary algorithm eliminating PosSLP nor a deterministic
algorithm, and it makes no numerical speedup claim. Its attribution
to the two main dependencies and the elementary product comparison
is appropriately limited. Publication priority is not established
by this review.

The fresh composition reviewer checked both dependency hashes and
statements, substitution size, curvature, product rank, nonconvex
observable permission, lexicographic ties, conditional expected time,
output length, and all listed degenerate cases. Its separate fresh
edge reviewer also passed output size, ties, and dimension-zero
handling. These independent reports support the reconstruction above.

Only administrative reconciliation is needed: replace the provisional
status now that both dependencies and this composition have passed.
Explicitly repeating that a zero-dimensional output chart means a
rational point would improve clarity but does not repair a correctness
gap; that convention is already supplied by the dependency interface.

Targeted whitespace checking passed:

```text
git diff --check -- research-20260927/mixed-quartic-integer-constraint-rank-oracle-review.md
```

Final reconciliation: the amended main has SHA256
`5f3d84209c3b730d7c2ff01a02de96717c1851c417cbfa88add13f5972d14364`.
The reviewer confirmed this hash and inspected the closed dependency
status, review links, theorem wording, explicit zero-dimensional
rational-point output convention, and verification disclosures.
They agree with this review. No mathematical construction or parameter
bound changed. The targeted review-file `git diff --check` passed
after this addition. The review is closed with a pass at this final
hash; no further work in this direction is proposed.
