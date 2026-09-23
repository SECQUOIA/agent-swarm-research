# Adversarial review of the planar message construction

Date: 2026-09-22. Reviewer: a fresh independent agent.

## Verdict

I found no substantive mathematical gap in the deterministic construction in
[the algorithm note](research-20260922-planar-message-algorithm.md), or in its
stated conditional high-probability consequence. The result is an exact,
output-sensitive algorithm in fixed dimension. It does not establish
polynomial expected work for a prescribed perturbed instance or a smoothed
Turing algorithm with continuous noise. The note correctly separates those
claims.

Two assumptions should be explicit in the statement:

- The quadratic matrix is symmetric. This is the usual convention for this
  model; row diagonal dominance alone does not imply positive definiteness
  for an arbitrary nonsymmetric matrix.
- Fix the decomposition before drawing the penalty perturbations, or choose
  it from the sparsity graph alone. The first-moment argument applies to each
  fixed message. It does not justify choosing a decomposition adaptively
  from the sampled penalties.

These clarify the intended setting rather than repair a counterexample to
the construction under that setting. The analytic planar-region theorem was
read for its assumptions and conclusion; its curvature proof was not fully
re-audited in this review. Its two existing independent reviews remain
separate evidence.

## Objective ownership and modes

The bags containing a vertex form a connected subtree. The bags containing
both endpoints of an edge also form a connected subtree, as an intersection
of two connected subtrees of a tree. Every original objective term therefore
has a unique highest containing bag. An internal vertex of a rooted subtree
cannot have a neighbor outside that subtree except through its separator.
Every term involving an internal vertex belongs to the subtree; every term
involving only separator vertices belongs above it. This proves the required
ownership statement, including linear and indicator costs.

For a fixed boundary mode, an active indicator permits a zero continuous
coordinate. Treating it this way is essential when penalties are negative or
when an optimum has zero coordinates. The separate modes in the note handle
this correctly. No positivity assumption on indicator penalties is needed.

Child interiors are disjoint and have no mutual edges. Once bag indicators
are fixed, any choice of child support representatives yields a consistent
complete support. Adding their unrestricted quadratic value functions and
the assigned local costs is exactly partial elimination of this support.
The Hessian on the bag variables still to be forgotten is positive definite,
although the complete bag polynomial need not be convex in separator
variables: it is the relevant Schur complement of a positive definite
principal submatrix. This distinction is correctly respected by the proof.

## Why full-dimensional samples suffice

The strongest apparent failure mode is a conditional optimizer lying at the
intersection of several child switching curves, possibly on a box boundary.
It does not invalidate coverage.

After identically zero restricted comparisons are discarded, full-dimensional
cells are dense in the active bag box. Given the conditional optimal bag
point, take a convergent sequence in those cells. Finitely many child tuples
occur, so one tuple occurs along a subsequence. Continuity makes every member
of this tuple attain its child envelope value at the target point. Its summed
polynomial therefore attains the true conditional optimum there.

The sample sequence may change the parent boundary coordinates. This is
harmless: it discovers a full polynomial, which is subsequently evaluated
at the specified parent boundary. Unrestricted minimization over forgotten
bag coordinates can only lower its value. Conversely, the candidate is the
value of a feasible complete support at that same boundary, so it cannot be
below the true message. The two inequalities give equality.

The same argument justifies deleting polynomials that never strictly win
after identical polynomials are merged. A finite family of distinct
polynomials has a dense set of points with a unique minimizer. Continuity
then covers all lower-dimensional and boundary points. This argument would
fail for interval- or cell-restricted pieces; retaining full support
polynomials is material, not merely a storage choice.

## Complexity and probability transfer

At a bag, pairwise comparisons within child dictionaries produce at most a
quadratic number of input polynomials in their combined size. A
sign-invariant decomposition in at most three variables has polynomial
construction cost for fixed dimension and degree. Selecting one tuple per
full-dimensional cell yields polynomially many candidates. Pruning them
takes place in at most two variables and also has polynomial cost. Summing
these local bounds gives one fixed polynomial in the number of bags and the
sum of final dictionary sizes. There is no hidden product over all children.

The rational coefficient claim also holds. Every stored coefficient is a
Schur-complement coefficient of a support of the original rational instance.
Determinant bounds give polynomial encoding length. CAD sample coordinates
serve only to choose support representatives; they never become stored
quadratic coefficients. A polynomial number of rational arithmetic steps
per candidate and exact algebraic sign comparisons therefore have polynomial
bit cost in the original input length and dictionary size. This statement
does not assign finite encodings to continuously sampled real penalties.

For a fixed decomposition, each two-dimensional boundary mode satisfies the
planar theorem with its internal support bits and the stated uniform
gradient bound. Boundary penalties are absent by ownership. One-dimensional
modes obey the scalar estimate, and zero-dimensional modes need one value.
Summing expectations requires no independence between messages. Markov's
inequality gives the stated bound polynomial in inverse failure probability.
It does not imply logarithmic dependence on that parameter.

The redraw argument is also valid in the declared exact algebraic model.
The deterministic polynomial work cap is a bound on actual construction
work, not merely on the final output size. Independent trials succeed with
probability at least one half, so capped work has a geometric expectation.
The accepted noise is biased, as the note states. The original-objective
certificate is deterministic for every accepted perturbation and therefore
survives this bias. Neither conclusion gives a finite-bit implementation
without a separate discretization argument.

## Targeted verification

I ran one inline `python3`/SymPy exact check, using rational arithmetic. The
test has a central bag `{0,1,2}`, parent separator `{0,1}`, and five one-vertex
child interiors attached respectively to separators `{0,2}`, `{1,2}`,
`{0,1}`, `{0,2}`, and `{1,2}`. Diagonal coefficients are `2`, every graph-edge
coefficient is `1/10`, linear coefficients are `(i-3)/7`, and indicator
penalties are `((i mod 3)-1)/11` for vertex indices `0,...,7`.

Across all eight central-bag indicator modes and all 32 child support choices,
the script compared direct elimination of the complete internal support with
child elimination followed by elimination of active bag vertex `2`. It
checked all quadratic, linear, and constant coefficients exactly, and checked
positivity of every nonempty final pivot.

Result: **256 exact identities passed**. This verifies a representative
ownership and elimination calculation, including negative penalties and
separator dimensions zero through two. It does not implement CAD, verify
the probability theorem, or prove the general coverage argument. No Lean or
project-wide verification was run.

## Sources checked and novelty limits

I opened the full primary-source PDF of Arnon, Collins, and McCallum,
[*Cylindrical Algebraic Decomposition I: The Basic Algorithm*](https://www.lacl.fr/pvanier/cours/2015-2016/lm/articles/Cylindrical%20Algebraic%20Decomposition%20I-%20The%20Basic%20Algorithm.pdf).
Its introduction explicitly states polynomial computing time when the number
of variables is fixed. Its construction specification provides exact sample
points and signs of all input polynomials on each cell. These are the
classical algorithmic ingredients needed here.

I also opened Basu, Pollack, and Roy's
[sign-condition component bound](https://www.math.purdue.edu/~sbasu/combinatorica_final.pdf).
The algorithm does not need its sharp exponent. A bound on realizable sign
components should not be conflated with the number of cells in a particular
CAD; the older fixed-dimensional CAD result already supplies the sufficient
polynomial construction guarantee.

This review supports correctness of the transfer, not priority. The
simultaneous arrangement step is a standard fixed-dimensional method. The
potential research contribution lies in its combination with full support
elimination and the penalty-only planar expectation bound. A broader audit
of parametric dynamic programming and bounded-treewidth quadratic
optimization remains necessary before a publication-level novelty claim.
