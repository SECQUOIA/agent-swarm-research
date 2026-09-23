# Continuous separator information: adversarial novelty and significance screen

Date: 2026-09-22. This is a bounded independent review of the proposed separator-feature result, not a claim that the literature search is exhaustive. The candidate uses actual feasible local probability measures and exact local convexification, but matches only finitely many continuous feature expectations on shared continuous states.

**Assessment.** The exact discrepancy identity is established approximation duality; the universal feature-count rate has an elementary packing proof; continuous nodal features and feasible marginal reconstruction already have explicit transport antecedents. Their combination into a sparse MINLP limitation is useful, but presently looks like a corollary and synthesis rather than a substantial new theoretical contribution. A quantitatively sharp repair theorem that preserves hard dynamics, integer decisions, and automaton constraints could be a more meaningful contribution. Its significance depends on the feasible class and cannot be inferred from marginal reconstruction alone.

The proposed identity is

\[
 \sup_{\substack{\mu,\nu\in\mathcal P(K)\\
                 \int\phi_i\,d\mu=\int\phi_i\,d\nu\;(1\le i\le r)}}
 \left|\int f\,d(\mu-\nu)\right|
 =2\inf_{v\in\operatorname{span}(1,\phi_1,\ldots,\phi_r)}
       \|f-v\|_\infty .
\]

For compact metric (K) and continuous functions, Hahn–Banach and the Riesz representation theorem give this directly. A norm-one annihilating signed measure has total mass zero, hence positive and negative parts of mass (1/2). Multiplying both parts by two produces the required probability measures. The elementary upper bound follows by subtracting any (v) in the feature span. Finite-dimensionality makes the span closed. This is mathematically sound but should be introduced as standard duality.

**Strongest direct comparisons examined.**

- Han, Jiao, and Weissman, *Local moment matching: A unified methodology for symmetric functional estimation and distribution estimation under Wasserstein distance*, COLT 2018, [Lemma 25, equation (24)](https://proceedings.mlr.press/v75/han18b/han18b.pdf). The lemma explicitly identifies the maximum expectation separation of two probability measures with matching polynomial moments as twice best uniform polynomial approximation error. The same discussion uses an absolute-value witness. Arbitrary continuous features replace the polynomial space by another finite-dimensional subspace; this extension follows from the same functional analysis. The proposed identity and its absolute-value specialization therefore cannot be advertised as newly discovered dualities.

- Alfonsi, Coyaud, Ehrlacher, and Lombardi, *Approximation of Optimal Transport problems with marginal moments constraints*, Math. Comp. 90 (2021), 689–737, [open manuscript](https://arxiv.org/pdf/1905.05663). Proposition 5.1 obtains an (O(1/N)) Lipschitz-cost gap with cell-indicator moments; Remark 5.2 extends it to (d)-dimensional marginals with (MN^d) moments and explicitly locates the dimension curse in (d), rather than the number (M) of marginals. Section 5.2 gives faster rates under additional regularity or cost structure. Example 5.1 shows that matching piecewise-affine moments does not force (O(N^{-2})) Wasserstein proximity for arbitrary nonsmooth measures. This rules out presenting the feature-count upper rate or the distinction between marginal dimension and number of blocks as new.

- Neufeld and Xiang, *Numerical method for feasible and approximately optimal solutions of multi-marginal optimal transport beyond discrete measures*, [arXiv:2203.01633v7](https://arxiv.org/pdf/2203.01633v7), dated 12 June 2026. Theorem 2.11 gives feasible reassembly and, for globally Lipschitz cost, an objective error bounded by the Lipschitz constant times the sum of marginal (W_1) discrepancies. Proposition 3.7 constructs continuous piecewise-affine simplicial nodal functions, proves their partition-of-unity property, and bounds the (W_1) diameter of every moment class by twice the mesh size. Proposition 3.9 gives explicit feature counts with exponent equal to each marginal's dimension. These are particularly close antecedents. The theorem reconstructs prescribed marginals; it does not assert that reconstruction preserves an arbitrary hard support relation such as a deterministic dynamic equation. The downloaded unversioned PDF was v7; the web HTML initially returned v4, so theorem numbers here refer to v7.

- Lasserre, *Convergent SDP-relaxations in polynomial optimization with sparsity*, SIAM J. Optim. 17 (2006), 822–843, [open manuscript](https://optimization-online.org/wp-content/uploads/2006/04/1367.pdf). Its compact polynomial setting, running-intersection condition, sparse moment hierarchy, and convergence theorem are the basic sparse-optimization antecedent. The candidate's exact local-measure model isolates information loss at separators from positivity-certificate error. That is a useful conceptual distinction, but asymptotic consistency of sparse moments is established background. A lower bound in the stronger exact-measure relaxation can transfer to an SDP relaxation only after checking the actual shared variables, degree convention, and all extra overlap constraints.

- Bienstock and Muñoz, *LP formulations for polynomial optimization problems*, SIAM J. Optim. 28 (2018), 1121–1150, [open manuscript](https://arxiv.org/pdf/1501.00288); local full text `literature/papers/bienstock2018-lp-formulations-for-polynomial-optimization/fulltext.md`. Theorem 4 gives an LP of size (O((2\pi/\epsilon)^{\omega+1}n\log(\pi/\epsilon))), with coefficient-scaled constraint tolerance and objective tolerance, for bounded mixed-integer polynomial optimization of degree at most \(\pi\) and treewidth \(\omega\). The candidate counts separator features, assumes exact local optimization, and could preserve feasibility only under extra repair assumptions. It is therefore not a stronger complexity theorem for the same general class. Appendix A already examines limits on numerical tolerance guarantees.

- de Farias and Van Roy, *The Linear Programming Approach to Approximate Dynamic Programming*, Operations Research 51 (2003), 850–865, [publisher record and abstract](https://doi.org/10.1287/opre.51.6.850.24925). Restricting value functions to a linear span and bounding approximation through basis quality is established approximate dynamic programming. Only the abstract was inspected in this screen, so no exact constant or theorem-level dominance claim is made. Any proposed upper bound expressed solely through best approximation of Bellman value functions needs a full comparison with this literature before a novelty claim.

- Bernstein, *Sur la meilleure approximation de \(|x|\) par des polynomes de degrés donnés*, Acta Mathematica 37 (1914), 1–57, [original scan](https://www.math.auckland.ac.nz/hat/fpapers/acta37.pdf). The original introduction explicitly announces two-sided degree-dependent bounds for absolute-value approximation; the (\Theta(k^{-1})\) phenomenon is classical. The present screen read the search-extracted introduction, while a direct browser fetch timed out. An independently accessible full scan should be retained before relying on a precise historical constant. No such constant is needed for the proposed rate.

Additional local checks: the introductions of `literature/papers/faenza2022-new-limits-of-treewidth-based/fulltext.md` and `literature/papers/haasler2021-multimarginal-optimal-transport-with-a/fulltext.md` were inspected. The former treats extension-complexity and tractability limits tied to treewidth; the latter treats tree-structured multi-marginal transport and entropy regularization. Neither inspected introduction establishes an equivalent constrained dynamic repair theorem. This limited inspection does not exclude overlap deeper in those works or their references.

**Independent mathematical screen of the lower bound.** No width theorem is actually needed to obtain the stated exponent. Given (r) arbitrary features, choose (r+2) points (z_j) at pairwise distance at least \(\delta\). The vectors

\[
 (1,\phi_1(z_j),\ldots,\phi_r(z_j))\in\mathbb R^{r+1}
\]

are linearly dependent. A nonzero dependence (a) has \(\sum_j a_j=0\), so both signs occur. Normalizing the positive and negative coefficients gives disjointly supported probability measures with equal feature expectations. Every transport from one support to the other travels at least \(\delta\), so (W_1\ge\delta). More explicitly, (f(x)=\operatorname{dist}(x,\operatorname{supp}\nu)) is one-Lipschitz, zero on the negative support, and at least \(\delta\) on the positive support. On a cube with the infinity norm, (f) is continuous piecewise linear and hence admits a finite mixed-integer linear description. A grid supplies \(\delta=\Omega_d((r+2)^{-1/d})\). This demonstrates a useful information obstruction but also explains why the exponent alone is unlikely to support a major originality claim.

The construction establishes

\[
 \forall\Phi\text{ of size }r\quad\exists f\in\mathrm{Lip}_1(K)
 \quad \text{gap}(\Phi,f)\ge c_d(r+2)^{-1/d}.
\]

It does not establish the same claim when \(\Phi\) may be chosen after seeing (f). For the reset instance \(\min\{-f(u)+f(x):x=u\}\), one feature equal to (f) removes the objective gap. Thus a lower bound for arbitrary feature design is necessarily universal over a class of objectives, or requires restrictions on how features are obtained. An individual fixed absolute-value example is valuable specifically for polynomial-feature hierarchies, not arbitrary features.

Other scope conditions that affect significance:

1. A compact subset of \(\mathbb R^d\) need not have the packing geometry of a cube. Ambient dimension alone does not imply \(\Omega(\epsilon^{-d})\). State a cube, nonempty interior with fixed scale, or an explicit packing assumption. Finite sets, lower-dimensional manifolds, and thin reachable sets can be much easier.
2. The piecewise-linear witness can require a number of pieces growing with (r). This is a legitimate class lower bound, but not a fixed-size MINLP family unless its encoding complexity is analyzed separately. The two-mode absolute-value construction avoids that issue only in the polynomial-feature specialization.
3. The reset example's true optimum is obvious. It demonstrates weakness of a specified relaxation architecture, not optimization hardness, extension complexity, or an unconditional limit on solvers. Presolve can remove the artificial cancellation by substitution.
4. Exact local feasible-measure optimization is a strong oracle. Counting coupling features does not bound total formulation size, arithmetic complexity, or local oracle cost.
5. “Two modes, degree at most two” is representation sensitive. If graph auxiliaries or mode variables become shared separator variables, low-order matching may already transmit the missing absolute-value observable. The decomposition and overlaps must be fixed as part of the result.
6. For dynamic repair, replaying the same control at a nearby state preserves feasibility only if admissible control sets and guards permit it. A state-independent automaton constraint is compatible with replay; state-dependent guards or exact terminal equalities generally are not. Contraction bounds propagated distances, not logical feasibility. These restrictions should appear in the theorem, not only in limitations.

The most promising next theorem would identify a meaningful constrained dynamic class in which every feasible local-measure relaxation point can be converted into an exactly feasible integer trajectory with a computable cost loss, while exploiting more than universal state discretization. Examples of additional structure worth testing are state-dependent feasible-control correspondences with a quantitative repair property, reachability-aware separator features, or low-complexity value functions that support adaptive coupling. These are proposed research directions, not established consequences of the current candidate.

This screen used targeted `rg`/`sed` reads of the named local files, primary-source web searches and opens, and `pdftotext -layout` on the downloaded Neufeld–Xiang PDF. It ran no project-wide checks, inspected no CI, and performed no numerical proof verification. The packing argument and scope counterexamples were reconstructed independently. Positive findings concern the sources and arguments described here; search failures are not evidence of novelty.
