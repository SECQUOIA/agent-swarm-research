# Second independent review: fixed core with small polyhedral blocks

Date: 2026-09-05. Verdict: **PASS** for Theorem 1 and both pooling
corollaries under their stated assumptions. No substantive proof defect was
found. The unresolved literature discrepancy about two-pool hardness and the
novelty of the general theorem remain separate questions.

Reviewed: [fixed-core block theorem](../results/fixed-core-block-polyhedral-optimization.md),
Sections 1–7 as present on 2026-09-05, including preprocessing pools without
incoming arcs, the joint optimum-pair formula, and the fixed-bypass extension.
This reviewer read the full construction and checked its complexity and
reformulations independently before exchanging conclusions with the first
reviewer. This is a mathematical and source audit; no independent
implementation of quantifier elimination was built.

## 1. Local vertex enumeration is complete

Explicit finite leaf boxes make each nonempty leaf polytope bounded. Every
such polytope has an extreme point even when its dimension is below its
ambient dimension. At an extreme point the active row normals span the
ambient space: otherwise moving a sufficiently small distance in both
directions orthogonal to the active normals preserves every inequality.
Consequently some full-size active row subset has nonzero determinant.

The Cramer candidate therefore exists at every nonempty leaf. Candidates
with zero determinant at a particular parameter value are correctly rejected,
and different bases cover degeneracy. The test `e/delta<=0` is correct for
both signs of the determinant. Identically zero determinants can be removed
globally. No full-dimensionality or nondegeneracy hypothesis is missing.

## 2. The support formula has polynomial size

Let `L` denote the original bit length and `q=r+k+1` the dimension of the
joint parameter/support-direction space. Both `q` and the local dimension
are fixed. There are at most polynomially many local bases, feasibility
tests, and within-leaf score comparisons. Including both determinant signs
and cross-multiplied score numerators is necessary and sufficient to order
the rational scores, including negative denominators and ties.

The number of realizable sign vectors in this fixed-dimensional space is
polynomial in the number of polynomials. The construction enumerates these
realizable vectors, not all formal ternary sign assignments. Every such
vector fixes all valid bases and a tie-broken maximizing basis in every
leaf. This remains true on disconnected realizations because all decisions
depend only on the signs. Thus a Cartesian product of local basis choices
is never enumerated.

For a retained sign vector, every selected determinant is nonzero, and
`H=product(delta_j^2)` is strictly positive. The numerator in (4) obeys the
exact identity

```
F/H = lambda^T w - sum_j n_j/delta_j.
```

This verifies the denominator handling without assuming positive determinants.
The identity is asserted only on the corresponding sign realization, where
division is valid. Values of the cleared polynomial on its excluded
determinant-zero boundary cannot create spurious feasibility.

The degree of each cleared polynomial is `O(N)` for fixed structural
parameters. This growth is harmless here: a polynomial of degree `t` in
`q+1` fixed variables has at most `binomial(t+q+1,q+1)` monomials. Products
of `N` input-derived factors have polynomial coefficient bit length as
well; multiplication adds coefficient heights, and collecting terms adds
only the logarithm of the number of contributions. Hence explicit dense
expansion of every cleared polynomial and the complete disjunction are
polynomial in `L`. Treating the expanded degree as constant would be wrong,
but the draft explicitly avoids that mistake.

## 3. Support membership and quantifier order are exact

For fixed core `x`, nonempty leaf polytopes have compact convex images
`W_j(x)P_j(x)`, and their Minkowski sum is compact convex. Membership is
equivalent to all support inequalities. Linear support optimization over a
leaf is attained at an enumerated vertex. Appending the objective as the
last image coordinate therefore expresses attainment of an exact objective
value, not merely a bound on the optimum.

If a leaf is empty, all sign conditions realized at that `x` are discarded,
so the universally quantified formula is false. Otherwise the disjunction
expresses precisely the support inequality at every direction. The direction
zero is included and causes no difficulty. The proof correctly preserves
`exists x, forall lambda`; swapping these quantifiers would be invalid.

The number of quantified and free variables in the membership formula is
fixed. Duplicating it in the joint minimum formula only doubles a fixed
count. Formula length, degrees, and coefficient sizes are polynomial, so
fixed-dimensional real quantifier elimination applies even after the degree
growth caused by clearing denominators.

Compactness of the core together with global leaf boxes bounds the complete
feasible set. Polynomial non-strict leaf inequalities and linking equations
make it closed. Thus feasibility implies an attained minimum. The theorem
does not need an explicit rational core box to conclude attainment or apply
quantifier elimination. Its separate slack construction appropriately asks
for explicit bounds when aggregate inequalities are converted to equations.

## 4. Exact optimizer recovery does not hide a field-degree explosion

The joint algebraic sample contains only the fixed number of coordinates
`(x*,v*)`. A rational univariate sample represents them as rational functions
of one algebraic number of polynomial degree and encoding length. Evaluating
the original bounded-degree coefficient polynomials preserves polynomial
descriptions in this same field.

The residual system in all leaves is an ordinary continuous LP over that
ordered algebraic field. Its variables may be numerous, but its coefficients
do not generate a product of unrelated algebraic extensions. A nonempty
bounded polyhedron over the field has a vertex obtained by field arithmetic,
so no new algebraic roots are needed for the leaf coordinates. The cited
algebraic LP algorithm supplies polynomial bit-time recovery. This justifies
both the optimizer and output-length claims; describing only an algebraic
optimum value would not by itself have justified them.

The reviewer checked Basu, Pollack, and Roy's
[primary quantifier-elimination paper](https://www.math.purdue.edu/~sbasu/jacm95.ps),
Theorem 1.3.1 and the bit-complexity statement preceding it, plus Sections
3.1.3 and 3.2. These give the required fixed-dimensional bounds, univariate
sampling, and realizable-sign enumeration. The reviewer also checked
[Adler and Beling's primary paper](https://adler.ieor.berkeley.edu/ilans_pubs/lp_algebraic_stoc_1992.pdf):
its runtime explicitly depends polynomially on the degree of a common
extension containing the LP coefficients, as required here.

## 5. Pooling corollaries

With fixed input and pool counts, source fractions form a fixed core. Each
output has only a fixed number of pool flows and bypass flows, regardless
of the number of quality rows. Input capacities, pool capacities, and inlet
arc capacities use a fixed number of aggregate rows. The inlet arc cost is
correctly distributed as a coefficient of every outflow from that pool.

For positive throughput, source fractions are the actual inlet fractions;
conversely they reconstruct inlet flows and each pool's quality vector.
Inactive pools may use any supported simplex point. The preprocessing of
pools without incoming arcs is necessary and present. Missing arcs and
positive lower flow requirements are respected. Arbitrarily many bypass
arcs are compatible with these output blocks because the number of inputs
is fixed.

With fixed pool and quality counts and no bypasses, pool qualities form the
fixed core. Each input block and each output block has at most one flow per
pool. There are only the fixed number of mass balances, quality balances,
and pool capacity rows. Equations (11) are exactly the concentration
formulation after using pool mass balance. Attributewise minimum/maximum
input-quality bounds contain every positive-throughput pool quality; zero
throughput contributes nothing and can use any value in these intervals.
The no-input case is separately processed. Thus this second encoding is
also exact.

A fixed number of bypass variables can be placed in the core. Their input,
output, quality, and objective contributions then become polynomial
right-hand-side or core-objective terms. Unrestricted bypass variables can
couple an unbounded number of leaf blocks and are correctly excluded from
this second corollary.

## 6. Scope and remaining limitations

The theorem needs continuous convex polyhedral leaves of fixed dimension
and a fixed number of aggregate rows. Fixed nonlinear core dimension alone
does not justify it. Discrete leaves would destroy the exact support
membership argument; one aggregate equation with binary leaves already
encodes subset sum. The draft explicitly excludes this extension. Its
bounded number of design binaries in the core is valid because these are
fixed-dimensional polynomial equations.

No claim about general large-domain integer core variables, arbitrary leaf
dimensions, fixed-parameter tractability, or practical runtime follows from
this proof. All these boundaries are appropriately stated. The literature
conflict noted in the draft requires resolution before claiming a specific
published open problem has been settled, but it does not reveal a flaw in
either explicitly stated pooling reformulation or the general proof.
