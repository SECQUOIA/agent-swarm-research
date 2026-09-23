# Focused later-literature check: rank-one MOT and logarithmic precision

Date: 2026-09-04. This is a bounded follow-up to [the independent mathematical audit](review-rank-one-mot-precision.md), not an exhaustive priority review.

**Verdict.** No later resolution of the precise constant-rank AMIN precision question was located in this check. The local reduction answers the question negatively in the rational bit model unless P=NP, already for strictly positive rank-one costs and binary uniform marginals. The claim that this is the first answer remains unverified. No change to the mathematical statement or its precision qualifications is indicated by the sources checked below.

## The question is explicit in the published primary source

Altschuler and Boix-Adsera, *Polynomial-time algorithms for multimarginal optimal transport problems with structure*, Mathematical Programming 199 (2023), 1107–1178, Section 7.2, second remark after Theorem 7.4, explicitly asks whether AMIN can improve from polynomial dependence on Cmax/epsilon to polynomial dependence on log(Cmax/epsilon). It notes that such an improvement would enable exact MIN and MOT for that class. Definition 7.2 supplies the cost in low-rank plus sparse factored form; Theorem 7.4 and Corollary 7.5 retain polynomial inverse-accuracy dependence. These passages were checked directly in the [published article](https://link.springer.com/article/10.1007/s10107-022-01868-7).

The [arXiv record](https://arxiv.org/abs/2008.03006) lists its latest revision as v4, 16 July 2022. No later revision or addendum resolving the precision question appeared in that record. This does not rule out a separate later paper.

## The authors' hardness paper does not supply the rank-one conclusion

Altschuler and Boix-Adsera, *Hardness results for Multimarginal Optimal Transport problems*, Discrete Optimization 42 (2021), 100669, Section 4, is explicitly about super-constant rank. Propositions 4.1–4.2 exclude algorithms jointly polynomial in rank and the other input parameters. Lemma 4.3 constructs a clique-encoding tensor by summing one rank-one term per graph edge, with an upper bound n^2 k^2 on the resulting rank. It does not establish hardness at fixed rank. Lemma 4.4 uses the zero-potential MIN oracle for that growing-rank tensor. See the [published primary text](https://www.sciencedirect.com/science/article/pii/S1572528621000487).

Our rank-one tensor's unweighted minimum entry is easy. Its hard oracle is the tilted minimum after subtracting supplied coordinate potentials. This distinction is essential when comparing a claim about the minimum entry of a tensor with the AMIN question actually posed in Section 7.2.

## Nearby later algorithm papers checked

**Strossner and Kressner (2023).** *Low-Rank Tensor Approximations for Solving Multimarginal Optimal Transport Problems*, SIAM Journal on Imaging Sciences 16(1), 169–191, DOI 10.1137/22M1478355. The introduction and Theorems 2–3 analyze approximation of the Gibbs kernel exp(-C/eta), including its effect on entropic and unregularized transport error. Theorem 3 controls the final error through the regularization, kernel approximation, and stopping tolerances. Sections 4–5 exploit graphical tensor networks and approximate their factors. The inspected results do not provide exact fixed-cost-rank MOT or a logarithmic-in-inverse-accuracy AMIN algorithm, nor a hardness resolution of that question. The rank of an approximated Gibbs kernel is a different object from the rank of C. [Open primary paper](https://arxiv.org/pdf/2202.07340); [journal record](https://epubs.siam.org/doi/10.1137/22M1478355).

**Augustino et al. (2026).** *Faster Algorithms for Multimarginal Optimal Transport*, arXiv:2608.09513. Its abstract and Section 1.1 state a classical algorithm with runtime O(m^2 n^m epsilon^(-1) polylog(m,n,epsilon^(-1))) returning an explicit coupling; Sections 4–6 address quantum methods and cost-entry query bounds. Its runtime retains the full tensor dimension n^m and polynomial inverse-accuracy dependence. The rank-one completion in its packing argument describes a coupling correction, not a restriction to rank-one cost tensors. No resolution of the factored constant-rank precision question was found in the inspected statements. This is a scope comparison, not an audit of the new paper's algorithms. [Primary preprint](https://arxiv.org/html/2608.09513v1).

The author's [publication list](https://jasonaltschuler.github.io/) was also checked for an obvious follow-up on this precise question; none was identified. A publication list and search results cannot establish absence of a later resolution.

## Scope of the local answer

The [local theorem](../results/positive-box-single-monomial-hardness.md) supplies C = tensor-product_i (1,1+epsilon a_i), with every cost entry in [1,16/15], rational factors, rank exactly one, and no sparse correction. The prescribed marginals are all (1/2,1/2). Its PARTITION reduction separates the two cases by an inverse-accuracy requirement having polynomial logarithm in the original input length. The separate direct reduction to tilted MIN avoids any precision loss from a generic MOT-to-oracle reduction.

The source's dimension-based entry-bit convention is addressed by the dummy-mode padding already reviewed in [the dedicated audit](review-rank-one-mot-precision.md). Keep the following qualifications: this is a bit-complexity conclusion, not a lower bound for unrestricted unit-cost arithmetic; it is weak NP-hardness, not fixed-additive-accuracy hardness; deterministic algorithms are excluded under P!=NP, while the bounded-error randomized claim uses NP not contained in BPP.

## Search record and recommended wording

Focused searches combined the paper title and authors with constant rank, rank one/rank-one/rank-1, precision, inverse accuracy, logarithmic dependence, exact evaluation, NP-hardness, PARTITION, and product cost. Searches included later years through the check date and followed the pertinent later algorithm leads to primary papers. Generic low-rank transport-plan methods, low-rank Gibbs kernels, and rank-one marginal-completion formulas were kept separate from rank-one factored cost tensors.

Recommended wording: “The reduction gives a negative answer, in the rational bit model unless P=NP, to the precision improvement proposed after Theorem 7.4 of Altschuler and Boix-Adsera. A focused literature check on 2026-09-04 found no later resolution; priority is not established.”
