# Positive multilinear gaps and incidence structure

Date: 2026-09-04.

The investigation now establishes [sharp asymptotic incidence growth](../results/positive-multilinear-incidence-sharp-growth.md): the worst ratios under treewidth k, degeneracy k, and maximum orientation outdegree k are each asymptotic to k, with leading constant one. Both the upper and lower proofs passed independent full written audits.

## Audited result and unresolved target

The main result developed in this investigation is [the feedback-variable gap bound](../results/positive-multilinear-feedback-gap.md):

    tbtgap≤2^f chgap

when deleting f variable nodes from the original incidence graph leaves a forest. The theorem is independent of monomial degree and extends to the original monomials on finite nonnegative boxes.

The constant two is sharp when f=1. The unit-coefficient family

    p_n(a,x)=a Σ_i x_i+∏_i x_i

at a=1/n and x_i=1−1/n has tbtgap=2−1/n and chgap=1. Its incidence graph has treewidth exactly two and becomes a tree after deleting a.

The complete proof, all boundary cases, the nonnegative-box extension, and the example passed [independent audit](review-multilinear-feedback-gap.md). A separate exact-arithmetic program checked the universal-law domination for all 780 prescribed-mean vectors in its rational grid with f=0,...,3.

The feedback theorem alone does not settle bounded incidence treewidth, because a bounded-width graph can require arbitrarily many feedback vertices. A subsequent [incidence-orientation theorem](../results/positive-multilinear-incidence-sparsity-gap.md) now resolves existence of such a bound: variable outdegree at most r and factor outdegree at most s imply ratio at most r+s+2/(1−e^−1). It passed independent audit. In particular incidence treewidth two gives a universal upper bound below 7.165, and the subsequent [exact treewidth-two theorem](../results/positive-multilinear-treewidth-two-exact.md) improves this to the sharp constant two.

## Mechanism

The proof repairs all local distributions while preserving singleton means. It builds one universal law Q on feedback variables and each outside variable using 2^f orientations of threshold intervals. Each such pair marginal dominates every admissible local pair distribution after scaling by 2^−f. Nonnegative residual measures then give every factor the same feedback-plus-single-variable marginals. Conditioning on the feedback state permits exact forest gluing.

The domination costs one global factor, not one factor per tree depth. The proof applies to arbitrary nonnegative local payoff functions. Positive multilinear gaps fit because they can be represented by nonnegative local deficiencies. For nonnegative boxes, a local affine majorant supplies the deficiency without replacing factors by expanded hyperedges.

For arbitrary nonnegative local payoffs, the factor 2^f is sharp: use all cell indicators of f feedback bits and one outside bit at means 1/2. Their local maxima sum to 2^f, while their total is identically one. Private variables fixed at one can make all factor scopes distinct. This obstruction applies to the general domination lemma; it does not establish the same lower bound for positive monomials.

## Why a simple forest-cover argument fails

Partitioning factors into q incidence forests would immediately give a q bound by mixing exact forest couplings. But incidence treewidth does not bound the required q. The incidence graph K_(2,m) has treewidth two, whereas any pair of its factor nodes and the two variable nodes forms a cycle, requiring m colors in such a partition. Distinct monomials can realize this obstruction by adding a private variable to each factor.

Thus a forest-cover proof cannot establish a bound depending only on incidence width. This is a limitation of that proof strategy, not a counterexample to a width-dependent gap bound.

## Primary literature and novelty scope

1. Del Pia and Khajavirad, *The Multilinear Polytope for Acyclic Hypergraphs* (2018), explicitly characterize standard-linearization exactness for Berge-acyclic hypergraphs. Incidence-forest exactness is therefore prior art. The work also treats broader acyclicity classes with stronger inequalities. [Open primary article](https://par.nsf.gov/servlets/purl/10081429). Direct browser retrieval timed out in this session; the primary indexed abstract and the later authors' paper below corroborate the relevant statement.

2. Del Pia and Khajavirad, *Beyond hypergraph acyclicity: limits of tractability for pseudo-Boolean optimization*, technical report dated October 30, 2024, PDF p.4 (printed p.3), reviews polynomial solvability under bounded incidence treewidth and distinguishes it from primal/intersection treewidth. Its theorem on printed p.5 concerns extended formulations controlled by primal treewidth. These statements should not be interchanged. [Open author manuscript](https://engineering.lehigh.edu/sites/engineering.lehigh.edu/files/_DEPARTMENTS/ise/pdf/tech-papers/24/24T_016.pdf).

3. *Factorized binary polynomial optimization* (2025), Section 5, lists bounded incidence treewidth as a known tractable class and defines primal and incidence graphs separately. The cited underlying work is Capelli, Del Pia, and Di Gregorio, *A knowledge compilation take on binary polynomial optimization*. Tractability does not by itself imply the pointwise ratio for the original term-by-term relaxation. [Open primary article](https://link.springer.com/article/10.1007/s10107-025-02274-5).

4. Pletscher and Ong, *Part & Clamp: Efficient Structured Output Learning* (2012), uses feedback-vertex conditioning to obtain forest inference problems. This establishes the standard status of the conditioning framework. The present proof's additional issue is a simultaneous guarantee at fixed original singleton marginals. [Open conference paper](https://proceedings.mlr.press/v22/pletscher12a/pletscher12a.pdf).

5. Del Pia and Walter, *Simple odd β-cycle inequalities for binary polynomial optimization* (2024), reviews exact descriptions for various hypergraph classes using flower and cycle inequalities. The sharp example above has a direct valid inequality behind its hull value; no claim is made that this inequality introduces a new cutting-plane family. The proposed novelty is the quantitative feedback-variable statement and its sharp specialization. [Open primary article](https://link.springer.com/article/10.1007/s10107-023-01992-y).

Searches combining positive multilinear gaps, feedback vertex sets, local marginal relaxations, incidence treewidth, and integrality gaps did not identify the displayed quantitative theorem. This is a bounded screen, not a proof of novelty. Further search through inference and fixed-marginal optimization terminology remains useful.

## Questions retained for later work

- Is the exponential dependence on f necessary for positive multilinear deficiencies, or merely for the universal domination proof?
- Resolved: every incidence-treewidth-two instance satisfies tbtgap≤2 chgap, and two is sharp. The next question is whether the exact treewidth-k constant equals k for all k.
- Incidence degeneracy k has the audited upper bound k+O(ln k/ln ln k), using an outdegree-k orientation and the sharp degree theorem. Its sharp leading-order dependence is now known to be k; the next question is the lower-order difference.
- Can tree decompositions be used without multiplying a loss at every separator?

The unresolved statements above are research questions. The sharp feedback-one example alone did not prove the width-two upper bound; the later two-TU-block graph partition now supplies that proof.

## Why varying the radix settled the leading order

With L levels and radix b, the nested-block lower construction has exact tbtgap L and hull gap 1+(L−1)/b whenever b≥L. Its incidence treewidth is exactly L. Sending b to infinity while holding L fixed makes the ratio tend to L, giving a lower bound k for the treewidth-k supremum.

For orientation and degeneracy, deepest bilinear factors can be removed or oriented first. This reduces the parameter to L−1 when L≥3, giving the stronger fixed-k lower bound k+1. In both cases the upper certificate k+o(k) proves leading constant one.

The tempting exact bound ratio≤incidence degeneracy is false. At L=3 and b=5 the ratio is 15/7>2, while degeneracy and maximum orientation outdegree are at most two. The graph has treewidth three, so it does not contradict the later exact treewidth-two factor-two theorem.

This use of a large radix does not contradict the earlier degree-investigation barrier. The number of levels determines incidence structure, whereas degree grows with the radix. The same modification can be ineffective for a degree refinement and decisive for an incidence refinement.

The intermediate hard-term parameter is also exact: if every term has one low anchor and every high variable appears in at most r terms, with unrestricted low-anchor frequency, its worst ratio is exactly r. This is distinct from ordinary all-variable frequency, for which the deepest anchor has exponentially larger frequency.
