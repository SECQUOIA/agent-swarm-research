# Independent audit of two auxiliary multilinear lemmas

Date: 2026-09-04. Reviewer: `fbbt`. Scope: only the canonical-pair forest lemma and identical-factor-neighborhood compression lemma, including their stated extensions, in [the investigation note](multilinear-treewidth-two-investigation.md). Neither is a dependency of the canonical exact treewidth-two theorem.

**Verdict: both written lemmas and proofs pass. No correction or counterexample was found within their stated scope.** This is a mathematical audit, not a novelty assessment.

## Canonical pair laws on a forest

For prescribed binary means p and q, every pair law is determined by t=Pr(1,1), where max(0,p+q−1)≤t≤min(p,q). The four cells are t, p−t, q−t, and 1−p−q+t. Each is affine in t, so its value at the midpoint is the midpoint of its minimum and maximum feasible values. Since the minimum is nonnegative, twice that midpoint is at least every feasible cell value. Thus 2Q−P is entrywise nonnegative for any feasible pair law P. Its total mass is 2−1=1 and its singleton means are 2p−p=p and 2q−q=q.

A target union probability min(1,sum p_i) is attainable. For example, place consecutive half-open intervals of lengths p_i on a circle of circumference one. Their union has the required measure: they are disjoint before the total length reaches one, and cover the circle once it reaches one. Add all nontarget variables with their prescribed means. This supplies the proof's starting law P, including empty and singleton targets.

The residual edge laws have consistent singleton marginals and therefore glue on each forest component by sampling a root and then each child conditionally on its parent. A parent state of probability zero forces both corresponding edge cells to be zero, so arbitrary conditional choices on that state cannot alter the resulting marginals. Different components can be sampled independently. Consequently M=(P+R)/2 has exactly the canonical edge laws. Every residual law has target union at least max p_i, proving the stated improved half bound. For an arbitrary nonnegative function g on a finite binary target, choose a maximizing singleton-feasible law P; the same construction and E_R g≥0 give the stated half-of-maximum extension. The constructed law may depend on the target or g; no simultaneous guarantee for all targets is asserted.

The triangle warning is also exact. At fair means the canonical pair law is uniform over its four outcomes. Subtracting the perfectly correlated pair law from twice this uniform law leaves perfect anticorrelation. Three binary variables cannot be pairwise anticorrelated. This invalidates that residual extension on a cycle, without disproving the separate positive-multilinear statement.

## Compression of an identical-neighborhood block

Let B be nonempty and let w=max(0,sum_B x_i−|B|+1). In any original endpoint law, V=product_B X_i has mean q≥w. If q>0, retain V's ones with an independent probability w/q to obtain W≤V of mean w; if q=0 then w=0 and take W=0. The reduced objective is nondecreasing in W because its coefficients and all outside endpoint products are nonnegative. This proves reduced minimum ≤ original minimum without changing outside means.

Conversely, a local law on B attaining product mean w exists by the sharp one-monomial Fréchet bound (equivalently, maximize the union of its failure events). Condition that local law on its product and attach it to any reduced law through W. The resulting original means are correct, the product equals W almost surely, and every objective term is unchanged because it contains all of B or none of B. This proves the reverse inequality, including w=0 and w=1. Null conditioning states cause no problem.

For any incident scope B∪C, direct substitution proves equality of the two local lower-envelope expressions in the note. If sum_B x_i−|B|+1<0, both expressions are zero since sum_C x_i≤|C|. The upper-envelope comparison follows from w≤min_B x_i. For empty C, the reduced term is affine W and the same comparison holds. Common-threshold coupling simultaneously attains all upper envelopes of positive monomials, so summing these comparisons gives a single nonnegative difference Δ and the exact identities T_original=T_reduced+Δ and H_original=H_reduced+Δ.

The ratio transfer is most directly written without division: if T_reduced≤C H_reduced with C≥1, then T_original≤C H_original because Δ≤CΔ. Thus zero gaps do not require a division convention. Coefficients may be zero, and coincident reduced monomials may be combined by adding their coefficients. The proof is restricted to the unit-cube endpoint formulation, nonnegative coefficients, and blocks that appear in every incident term in their entirety. It makes no claim for signed coefficients, partial block incidences, or arbitrary local payoff functions.

The review checked the complete finite-law arguments algebraically. No numerical search or test is needed to establish these two elementary statements.
