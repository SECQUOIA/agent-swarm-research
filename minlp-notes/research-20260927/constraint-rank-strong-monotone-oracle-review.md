# Independent review of the constraint-rank oracle algorithm

Date: 2026-09-28. Reviewer: `posslp_proof_adversary`.

Reviewed manuscript:
[A constraint-rank algorithm for exact strongly monotone polynomial equilibria](constraint-rank-strong-monotone-oracle.md).
Frozen SHA256:
`d4eda2875ac0b6eaa96791f93d20201b31f71256a17db2cf58b06881096a1eea`.

**Verdict: pass, with minor presentation clarifications requested.**
No substantive mathematical defect was found. A genuinely fresh
reviewer, `rank_violator_source_fresh`, independently checked the
primary sampling theorem, all primitive argument sizes, and the
binary random-sampling implementation. That review also passed.
Neither reviewer contributed to this construction.

Requested clarifications are:

- Repair the bare `quad` in equation (5).
- Cite Definition 19 for combinatorial dimension, alongside
  Definitions 6--7 for violator spaces and bases.
- Distinguish the first stage's potentially larger samples from the
  second stage's `6 r^2`-copy samples. Neither is a large first argument
  to the exact violation primitive.
- State that the successful-update bound applies separately to each
  invocation of the second stage and to nonterminal reweightings.
- Make explicit that sampled duplicate copies are identified with
  their original row indices before the exhaustive basis subroutine.

The last clarification makes the implementation match the primitive's
set-of-row-indices interface. Multiplicity affects sampling probability,
not the polyhedron or its variational-inequality solution.

## 1. Scope and dependencies

The claimed expected running time is
`(r+1)^(O(r)) poly(N)` with a PosSLP oracle, where `r` is the rank
of all constraint normals. Oracle instances and the returned affine
chart have polynomial encoding length in `N`, with an exponent
independent of `r`. This is an oracle algorithm with expected runtime,
not a single-query reduction or an ordinary algorithm omitting PosSLP.

The supplied global strong-monotonicity modulus is a promise, unless
established by the separately checked Jacobian Gram format. The
existence and affine-restriction facts and the exact polynomial-
observable zero theorem are previously reviewed dependencies. The
primitive here does not use the more elaborate circuit-objective LP
normal-cone test from the unambiguous theorem.

## 2. Feasibility, locality, and every-basis rank

Once the full rational system is checked feasible, every row subset
defines a nonempty polyhedron. Global strong monotonicity therefore
gives a unique VI solution for every subset, including the empty
subset. This precheck excludes any hidden infeasible-subsystem basis
case and permits the stated rank bound without an additive dimension
term.

For `F` contained in `G`, absence of violations from `G` at `p_F`
means `p_F` is feasible for `P_G`. The inequality it satisfies on
`P_F` remains true on its subset `P_G`. Uniqueness then gives
`p_F = p_G`, which proves locality of the violation map. The argument
does not compare objective values or assume that the map is a
gradient. Consistency follows from feasibility. Identical inequalities
with different input row indices cause no change to either argument.

At a subset solution, the polyhedral normal-cone condition represents
`-T(p_G)` by active normals with nonnegative coefficients. A minimal
positive support is linearly independent: a nonzero dependence can
be signed to have a positive coefficient, and subtracting the largest
allowed multiple removes one support member while preserving
nonnegativity. The resulting support has at most `rank(A)` rows.
If `T(p_G)=0`, the empty support suffices.

The sign in the sufficiency argument is correct. For a point feasible
for those support inequalities, each active-normal displacement has
nonpositive pairing; negating their nonnegative combination gives a
nonnegative pairing with `T(p_G)`. Thus the support alone determines
the same VI solution, and hence the same violation set.

Existence of one small determining subset for each `G` would not by
itself be a complete argument about every basis. The manuscript makes
the necessary further step: apply the support construction to an
arbitrary inclusion-minimal basis itself. The obtained equivalent
subset must be the whole basis. Every basis consequently has at most
`r` rows, and in fact its normals are independent.

## 3. Exact small-subproblem implementation

The primitive must handle every row subset of size at most `r`, not
only subsets already known to be bases. Exhaustive enumeration of
its at most `2^r` support candidates meets that requirement.

For each independent support, rational elimination produces a chart
with an identity free-coordinate block. Its matrix satisfies
`Z^T Z >= I`, so `Z^T T(bar_x + Z y)` has the same valid global
monotonicity lower bound. It is an explicit cubic map with polynomial
coefficient encoding. Its unique zero and each required fixed-degree
observable fall within the reviewed zero theorem.

The multiplier formula uses the inverse of the positive definite
matrix `A_I A_I^T`, which exists for the chosen independent rows.
Its entries have polynomial bit length. The multipliers and the
stationarity residual remain explicit cubic polynomials after chart
substitution. Feasibility tests are affine. Thus every scalar test
uses a polynomial-length PosSLP query, and the number of scalar tests
per candidate is polynomial in the input length. No high-degree
elimination polynomial or expanded algebraic coordinate is produced.

A passing candidate has nonnegative multipliers, the active equations,
full subproblem feasibility, and exact stationarity. These conditions
prove its VI inequality directly, with the same sign orientation as
the support argument. Hence it is the unique `p_G`. The support
existence argument proves that at least one candidate passes, so a
fixed enumeration order yields a deterministic exact primitive.

Dependent or redundant input rows are allowed; only a candidate
support is required to be independent. Zero normals cannot enter a
nonempty independent support. A rank-full support gives a rational
point and still receives the multiplier and feasibility tests.
At rank zero the feasible polyhedron is all of space, and the
unconstrained zero theorem supplies the answer directly. These cases
also cover ambient dimension zero with rational constant observables.

## 4. Sampling source and binary costs

Both reviewers directly read Gärtner, Matoušek, Rüst, and Škovroň,
[Violator Spaces: Structure and Algorithms](https://arxiv.org/pdf/cs/0606087v3),
Definitions 6--7 and 19, Primitive 22, and Sections 4.2--4.5 including
Theorem 27. The stated expected primitive bound applies using the
known upper bound `r`. Every primitive's first argument is a returned
basis or an enumerated candidate of size at most `r`, possibly with
one member removed. Larger samples are processed through these calls.

The weighted implementation has no expanded-multiset requirement.
For one second-stage invocation on `q` original rows and `t`
successful nonterminal updates, a fixed basis gives

```text
2^(t/r) <= weight(basis) <= weight(all) <= q exp(t/(3r)).
```

Hence `t < 3r ln(q)` and total weight is less than `q^2`.
If the basis is empty, no nonterminal update occurs. Unsuccessful
iterations do not increase any weight. Prefix-sum draws with temporary
decrements sample labeled copies without replacement; duplicate row
indices can then be identified. All counts have polynomial bit length.
Uniform integer rejection sampling uses expected constant trials.
The terminal empty-violation iteration adds only constant overhead.

Thus polynomial overhead per iteration, combined with the reviewed
primitive bound, gives the asserted expected bit time. Long unlucky
runs do not increase numerical encoding lengths.

## 5. Output and significance

The returned basis has no violations in the full row set. Its VI
solution is therefore feasible for the full polyhedron, and its
inequality on the larger basis polyhedron remains valid on the full
one. Uniqueness identifies it with the desired solution. Running the
small-subproblem routine again produces a valid polynomial-size chart
and explicit cubic zero map. The final observable after substitution
has degree at most four and polynomial coefficient encoding.

The exponential support factor is absorbed by the parameter function;
the input-length exponent stays independent of rank. This improves
the parameter dependence over enumerating `m^O(r)` supports while
leaving the PosSLP oracle material, even at rank zero. The distinction
between all-subproblem basis dimension and the final active-support
size is correctly emphasized. A small final support alone does not
supply the theorem's dimension bound.

No deterministic algorithm or numerical speedup is established.
The sampling framework, conic support argument, and uniqueness
principle are not claimed as new. This review verifies the stated
oracle consequence, not publication priority for it.

## 6. Targeted verification and final reconciliation

The author checker was read and rerun:

```text
python research-20260927/check_constraint_rank_violator.py
```

It passed 128 exact affine VI subproblems in three ambient variables,
702 locality implications, and all 11 inclusion-minimal bases of the
two resulting violation maps. The examples have constraint rank one
and two, with redundant and zero rows and nonsymmetric strongly
monotone maps. The check also verifies solution recovery for every
equivalent determining basis. It checks every minimal basis in these
finite examples, rather than only finding one small support.

These computations do not implement Clarkson sampling, prove its
expected runtime, or verify the general cubic zero reduction. Those
claims rely on the source audit, the proof reconstruction, and the
explicitly reviewed dependencies. No Lean verification, project-wide
checks, or CI inspection was performed.

An additional fresh proof-review thread was requested but could not
be started because the thread limit had been reached. The primary
review above is independent of the construction, and the successful
fresh source reviewer separately checked the every-basis implication
as well as the algorithmic source and bit model.

Targeted whitespace checking passed:

```text
git diff --check -- research-20260927/constraint-rank-strong-monotone-oracle-review.md
```

Final reconciliation: the amended manuscript has SHA256
`457a1cab90441d2a2528221875ed1e6e816f208d93d7ca0e91e219aa346e86c3`.
I checked the corrected equation (5), Definition 19 citation, the
different sampling-stage sizes, the per-invocation nonterminal update
bound, and explicit duplicate-copy identification before the basis
subroutine. The status and exact-check disclosures agree with this
review. The mathematical construction is unchanged. The review is
closed with a pass at this final hash.
