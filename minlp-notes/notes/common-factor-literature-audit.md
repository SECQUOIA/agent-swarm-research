# Literature audit for the common-factor results

Date: 2026-09-04. This is a targeted open-literature comparison, not proof of novelty.

## Fixed number of linking rows

The [algorithm result](../results/common-factor-fixed-linking-optimization.md) documents the close prior method in Punnen, Sripratak, and Karapetyan (2015), section 3.2, Lemma 1. Its basis enumeration and perturbation are established. Only the moving-matrix/product-bound and integer-scalar extension remains a possible contribution.

## Classical foundations of the full anchored hull

Müller and Scarsini, *Stochastic Order Relations and Lattices of Probability Measures*, SIAM Journal on Optimization 16(4), 1024–1043 (2006), Theorem 3.3 (open preprint page 6), states that fixed-mean probability distributions form a lattice under convex order and that the least upper bound is obtained by taking the pointwise maximum of their integrated survival functions. These are precisely call functions. [Primary preprint](https://www1.mat.uniroma1.it/ricerca/convegni/2005/MeStoFin2005/scarsini.pdf). The theorem and proof were visible in the search engine's primary-PDF extraction; direct web fetching timed out. The authors also cite older work on this lattice structure. Our use of a maximum call function must therefore be attributed to classical theory.

Koshevoy and Mosler, *Lift Zonoids, Random Convex Hulls and the Variability of Random Vectors*, Bernoulli 4(3), 377–399 (1998), Theorem 2.1 (printed page 380) gives the zonoid support function through a positive-part integral. Lemma 3.1 (printed page 383) describes the univariate lift zonoid through threshold and integrated-quantile points. [Open author PDF](https://wisotypo3.uni-koeln.de/sites/statistik/pdf_publikationen/1998_KoshevoyM98.pdf). The set of feasible leaf pairs `(E[Y],E[XY])`, with `0<=Y<=1`, is this classical lift zonoid. Our threshold selection argument is an elementary specialization, not a new probability theorem.

The proposed contribution in [the full hull note](../results/common-factor-reciprocal-anchor-full-hull.md) is the application to the complete graph of one reciprocal anchor and arbitrarily many common-factor products, with a complete original-space inequality description, rational separation by an upper envelope of `2n+2` lines, and constructive recovery of a common representing distribution. The probability foundations make the argument short. They also mean that claims of a new general convex-order method would be unjustified.

## Adjacent nonlinear convexification work

Tawarmalani, *Inclusion Certificates and Simultaneous Convexification of Functions* (manuscript dated September 5, 2010), develops general simultaneous convexification and discusses mixed bilinear/fractional examples. [Primary Optimization Online manuscript](https://optimization-online.org/wp-content/uploads/2010/09/2722.pdf). Its general convex-extension machinery is adjacent. Targeted searches within the manuscript did not locate the reciprocal-anchor block, call-function representation, or convex-order argument. This is not a theorem-by-theorem non-overlap proof.

Hyun-Ju Oh, Margaret Wiecek, and Boshi Yang, *Convexification of a Class of Bilinearly Constrained Sets Sharing a Common Variable*, appears in [SIAM Optimization 2026 abstracts](https://www.siam.org/media/r0be0xtr/op26_abstracts_v3.pdf). The abstract announces extreme-point/facet characterization and separation for box domains with common-variable bilinear inequalities. No full paper was found. This is a direct reason not to claim novelty for unrestricted common-variable convexification generally; comparison with that full paper remains important for the anchored application too.

## Search coverage and remaining risk

Queries included combinations of “bilinear,” “convexification,” “convex hull,” “reciprocal,” “common variable,” “convex order,” “lift zonoid,” “call function,” “stop-loss,” “univariate,” “quadratic,” and “multiple binary,” plus fixed-rank/parametric LP queries for the algorithm theorem. Primary matches above were examined at the relevant statements. No exact previously published anchored-star hull application was identified.

The current result should be described as **mathematically verified, with explicit classical foundations and no exact application match found in this targeted search**. It should not yet be described as certainly new or publishable. Broader citation chaining through nonlinear mixing sets, perspective formulations, and low-dimensional moment hulls may find an equivalent formulation.
