# Independent review of fixed-core block optimization

Date: 2026-09-05. Reviewer: independent `benders_review` agent.

Theorem 1, Lemma 2, and Corollaries 3–4 in [the result note](../results/fixed-core-block-polyhedral-optimization.md) are mathematically correct under their stated compactness, bounded-leaf, fixed-dimension, and rational-polynomial assumptions. This approval includes the fixed-number bypass extension after Corollary 4. The proof supports polynomial **bit** complexity and exact algebraic optimizer recovery, not merely a real-arithmetic decision algorithm. Literature novelty is outside this mathematical approval and requires a separate audit.

## 1. Vertex enumeration and degeneracy

For a leaf of dimension at most the fixed constant `d`, the number of candidate row bases is polynomial in its row count. Determinants and adjugate numerators have bounded degree and polynomial coefficient encoding. A candidate is valid precisely when its determinant is nonzero and each residual divided by the determinant is nonpositive. Keeping the determinant sign is necessary; the draft does so.

Every nonempty bounded polyhedron has a vertex with a full-rank set of active row normals, even if its affine dimension is smaller than its ambient dimension. To check this directly, if active normals failed to span at a purported vertex, a nonzero orthogonal direction and a sufficiently small step in both signs would preserve all active inequalities and every inactive inequality. This contradicts extremality. Thus the candidate list detects singleton and lower-dimensional leaves as well as full-dimensional leaves.

Determinants that vanish identically may be discarded. Determinants that vanish only at some core values must remain in the sign family. At those values, invalid bases disappear and another basis of any nonempty bounded leaf remains. There is no hidden generic-position assumption.

## 2. Why the number of simultaneous choices is polynomial

For each candidate, its support score is a rational function whose numerator is linear in the support direction. Each pairwise comparison depends on one polynomial numerator and the two determinant signs. Consequently feasibility, nonemptiness, and the order of valid candidates are constant on a realizable sign condition in the fixed-dimensional space of core variables and support directions.

All realizable sign conditions can be enumerated in polynomial bit time in fixed dimension. The algorithm does not enumerate the Cartesian product of leaf bases. It enumerates polynomially many sign conditions, and for each one scans the polynomially many candidates to select one maximizing basis in each leaf. Ties can be resolved by a fixed index order. Disconnected realizations cause no problem because the relevant information depends only on signs. Zero signs, including the all-zero support direction, must be retained.

This is the substantive compression in the argument. Merely fixing the core and observing an LP would not establish the theorem.

## 3. Denominator clearing and encoding length

On a retained sign condition, all selected determinants `δ_j` are nonzero. Multiplying by `H=∏_j δ_j²` preserves inequality direction. Each term `n_j/δ_j` becomes

\[
n_j\delta_j\prod_{i\ne j}\delta_i^2.
\]

Thus the draft's cleared support inequality is an actual polynomial with no division. Its degree is `O(N)`, not a constant depending only on the structural parameters. This growth does not break polynomial complexity: with a fixed number of variables, the number of monomials of degree `O(N)` is polynomial. Direct dense polynomial multiplication computes the product in polynomial time. Coefficient bit lengths grow at most polynomially under these products and sums, because there are only polynomially many factors of polynomial encoding length.

The same holds when the selected determinant polynomials have repeated factors or when different leaves use the same determinant. Positivity is needed only on the selected sign condition, where all factors are nonzero.

This reasoning uses the fixed degree bound on the original input polynomials. It should not be silently extended to sparse polynomials with exponentially large binary-encoded exponents.

## 4. Support membership and empty leaves

For a fixed core with nonempty leaves, each leaf image under its aggregate-and-objective map is compact convex. Their finite Minkowski sum is compact convex, and membership is equivalent to all support inequalities. The support of the sum equals the sum of leaf supports. Consequently the universal support formula is exactly equivalent to the existence of leaves realizing both the aggregate equations and the specified objective value.

If one leaf is empty, no candidate in that leaf is feasible. Every sign condition containing the given core and any support direction is discarded. The disjunction is false there, so the universal formula rejects the core. No convention about the support function of the empty set is being used.

This exact equivalence relies on convex leaves. Replacing discrete leaves by their support functions would take their convex hulls and lose integrality. The note correctly excludes an unbounded family of local integer decisions.

## 5. Fixed-variable real algebra and exact output

The attainable-value formula has only `r+(k+1)+1` variables. Its length, degrees, and coefficient bit lengths are polynomial after denominator clearing. Fixed-variable quantifier elimination therefore runs in polynomial bit time despite the degree growth.

The primary source was independently read: [Basu, Pollack, and Roy (1996), *On the Combinatorial and Algebraic Complexity of Quantifier Elimination*](https://www.math.purdue.edu/~sbasu/jacm95.ps). Theorem 1.3.1 and the preceding definition of well-behaved algorithms give the required quantifier-elimination and integer bit-size bounds. Sections 3.1.3 and 3.2 provide algebraic sample points and enumeration of all realizable sign conditions. Their samples use rational univariate representations with polynomial degree and coefficient size when dimension is fixed. The author-hosted PostScript was downloaded and converted locally for inspection.

The full original feasible set is closed and bounded because the core is compact, the leaf boxes are finite, and all displayed constraints are continuous non-strict polynomial constraints. Its objective is continuous. The attainable-value set is therefore compact, and any finite optimum is attained. A univariate formula permits exact root isolation and minimum extraction.

A particularly explicit optimizer-recovery route is to define `F(x,v)` as core membership together with the universal support formula and use

\[
F(x,v)\ \wedge\ \neg\exists x',v'\,[v'<v\ \wedge\ F(x',v')].
\]

After renaming its bound variables, this is still a formula with a fixed total number of variables. Quantifier elimination and algebraic sampling return an optimal core and value in one rational univariate representation. Equivalently, separately sampling the fixed number of coordinates yields a common field of polynomial degree, because the product of a fixed number of polynomial degrees is polynomial.

At that optimal core, recovering all leaves is a polynomial-size feasible LP over the common real-algebraic field. The [primary Adler–Beling (1992) paper](https://adler.ieor.berkeley.edu/ilans_pubs/lp_algebraic_stoc_1992.pdf) explicitly gives polynomial complexity in LP dimension, coefficient encoding, and the degree of a common extension containing the coefficients. These parameters are all polynomial here. The common-field requirement is essential: separate polynomial-size descriptions of an unbounded number of unrelated algebraic coefficients would not suffice.

The [1994 journal version](https://adler.ieor.berkeley.edu/ilans_pubs/lp_algebraic_1994.pdf), §5, Remark 1, printed p.455, confirms this bit-complexity conclusion for polynomial-plus-isolating-interval encodings. Both versions outline the Turing implementation using finite-precision ellipsoids and exact algebraic separation, and refer the full implementation details elsewhere. The result note is relying on their stated algorithmic conclusion, not claiming to supply a new algebraic LP algorithm.

The output can therefore be represented exactly by a common algebraic generator with a specified real embedding and polynomial-size rational coordinate representations. No claim that the optimizer is rational, or that its algebraic degree is bounded by the fixed structural parameters alone, is justified or required.

## 6. Fixed-input, fixed-pool standard pooling

The pooling encoding is exact. The source fractions form a compact core of dimension at most `mp`. Each output leaf has at most `m+p` flows. Quality constraints have coefficients affine in the fractions, and additional qualities only add local rows. Input capacities, pool capacities, and input-to-pool arc capacities contribute a fixed number of aggregate rows. Input-to-pool costs are correctly distributed over pool-to-output flows through the same fractions.

Positive-throughput pools recover their fractions by dividing input flow by pool throughput. Inactive pools admit arbitrary normalized fractions on their incoming arcs. A pool with no incoming arcs must be removed or handled separately, because forcing all its fractions to zero while requiring their sum to be one would incorrectly exclude the feasible zero-flow state. This issue was raised during review and the draft now explicitly preprocesses these pools, checking conflicting lower bounds.

Upper and lower aggregate inequalities can be converted to equations using bounded slacks. For pooling the required bounds follow from simplex bounds and rational flow boxes with polynomial-size arithmetic. The general theorem does not assume that arbitrary compact-core coordinate bounds are already available: its separate inequality extension appropriately requires explicit bounds or supplied slack bounds.

The result covers bypass arcs in this fixed-input encoding. It does not cover an arbitrary number of output binary decisions or generalized pool-to-pool topology merely by implication.

## 7. Fixed-pool, fixed-quality pooling without bypasses

Corollary 4 also has an exact encoding in the theorem. Fixing the pool count `p` and quality count `K` keeps the concentration core dimension `pK` fixed. The input leaf for each source contains at most `p` inlet flows, with all source and inlet-arc bounds local. The output leaf for each destination contains at most `p` outflows, with destination throughput, outlet-arc, and quality bounds local. Pool mass and quality equations contribute only `p+pK` aggregate rows. Pool throughput bounds contribute another fixed number.

The displayed quality equation

\[
\sum_i C_{ia}x_{i\ell}-q_{\ell a}\sum_jv_{\ell j}=0
\]

is linear in all leaf variables for a fixed concentration core. Together with mass balance, it exactly enforces the weighted input quality at every active pool. At inactive pools it becomes `0=0`; assigning their quality inside the global input min/max box is harmless. Those bounds contain the weighted quality of every active pool, even when some inputs cannot reach it. An input-free instance has all flows zero and is correctly processed separately.

A fixed number of bypass flows can be put into the core. They change the affected input and output leaf right-hand sides and add a core objective term; all such changes are polynomial. Their finite flow boxes preserve compactness, and the total core dimension remains fixed. An arbitrary number of bypass flows does not fit this argument because it either makes the core unbounded in dimension or directly links the input and output leaf families.

The pending source-conflict warning concerning a 2014 two-pool hardness abstract is properly separated from the proof. This review verifies the explicit mathematical reduction under its no-bypass assumptions; it does not assert that the conflicting literature statement has been resolved or that the corollary is a confirmed new resolution of a published open problem.

## 8. Review limits

This is a proof audit rather than a computational implementation of the real-algebraic algorithm. Numerical experiments would not verify the asymptotic complexity claim. The cited primary algorithmic theorems, exact formula construction, and encoding bounds supply the relevant verification.

The supplied `code/fixed_core_blocks/check.py` was rerun successfully: 1,971 exact rational support and denominator checks, auxiliary LP comparisons, and degeneracy checks passed. These support the formulas and edge cases; they do not implement the quantifier-elimination complexity proof.

The theorem may have a large parameter-dependent exponent. Neither practical efficiency, strong polynomiality, nor fixed-parameter tractability follows. The independent literature audit must determine how much of this general construction and its pooling consequences is new.
