# Novelty screen for the positive multilinear marginal-floor gap

Date: 2026-09-04. Bounded independent primary-literature screen. Mathematical review of the candidate theorem is separate.

## Assessment

No exact antecedent was found for [the candidate marginal-floor theorem](../results/positive-multilinear-marginal-floor-gap.md): the worst pointwise term-by-term/hull gap ratio over positive multilinear polynomials with all unit-cube coordinates at least `delta` is asymptotic to

`ln(1/delta)/ln ln(1/delta)`, with leading constant one.

The closest verified bounded-marginal correlation-gap theorem gives a reciprocal-linear bound `O(1/delta)` when applied separately to the deficiencies. Ordinary independence cannot achieve the candidate asymptotic, even on one bilinear deficiency. The proposed content is a common correlated law that preserves every original mean and captures a much larger fraction of each local optimum simultaneously, followed by a matching lower family. Its interpretation as a degree-independent interior bound for the original relaxation appears substantively different from the inspected prior statements. This is provisional novelty evidence, not a certification of priority.

The statement restricts evaluation points, while retaining the full original unit cube as the envelope domain. It does not replace that domain by `[delta,1]^n`. The lower construction also fits `[delta,1-delta]^n` for small delta, so the sharp order persists when evaluation points avoid both sets of faces.

## The three different expected values

For a monomial `e`, choose a smallest-mean anchor `a(e)` and define the binary set function

`g_e(X)=X_(a(e))-product_(i in e) X_i`.

It is nonnegative and submodular. For fixed means `x`, let `g_e^+(x)` be its largest expectation under any law with those means. Then

`g_e^+(x)=min{x_(a(e)), sum_(i in e\{a(e)}) (1-x_i)}`.

For positive coefficients `c_e`, put

`A(x)=sum_e c_e g_e^+(x)`,

`H(x)=(sum_e c_e g_e)^+(x)`,

`F(x)=E_independent[sum_e c_e g_e(X)]`.

The local ratio is `A/H`; ordinary correlation-gap literature compares `H/F`. The numerator `A` allows different optimal laws for different factors, whereas `H` requires one common law. Applying a uniform correlation-gap theorem to every factor can bound `A/F`, and hence `A/H`, but that route can lose much more than necessary.

This is also the coverage-baseline issue: the relevant comparison is excess coverage above a fixed concave-envelope baseline. A multiplicative bound on total coverage does not preserve that excess automatically.

## Exact bounded-marginal prior theorem and its implication

Chekuri and Livanos, *On submodular prophet inequalities and correlation gap*, Theorem 1, gives `F_f(y)>=(1-max_i y_i)(1-1/e)f^+(y)` for every nonnegative submodular function. They also give near-matching examples as the largest marginal approaches one. Theorem 2 obtains other guarantees by selecting a smaller marginal vector; that change is unavailable in the present problem. [Primary published author manuscript, Theorems 1 and 2](https://chekuri.cs.illinois.edu/papers/submod-prophet-inequality-tcs.pdf).

Here is the exact reduction of their Theorem 1 to a weaker local bound. Complement all coordinates: `Y=1-X`, with means `y=1-x`, and define `h_e(Y)=g_e(1-Y)`. Complementation preserves submodularity and nonnegativity. If every `x_i>=delta`, then `max_i y_i<=1-delta`. Consequently

`E_independent g_e(X) >= delta(1-1/e) g_e^+(x)`.

Sum over the positive coefficients and use `H>=F`. This proves the already available consequence

`A/H <= 1/[delta(1-1/e)]`.

The same weak estimate follows directly from the elementary product bound. If the anchor mean is `u>=delta` and the nonanchor failure sum is `S`, then

`E_independent g_e >= u(1-exp(-S))`

`>= (1-1/e) u min(1,S) >= delta(1-1/e) min(u,S)`.

Thus mere finiteness for fixed delta is not a new claim. The candidate contribution is the sharp sublogarithmic growth in `1/delta`, including its leading constant.

### Independence has the wrong order even for one term

For `0<delta<=1/2`, take the bilinear monomial `X_1 X_2` with means `(delta,1-delta)`. The deficiency is `X_1(1-X_2)`. Its local and global optimum are both `delta`: set `X_1=1-X_2`. Independence gives only `delta^2`.

Therefore `A/H=1` but `H/F=1/delta`. This example lies in `[delta,1-delta]^2`. Any proof relying solely on independence to capture every term's individual deficiency necessarily permits a factor at least `1/delta`. It cannot yield the candidate `ln(1/delta)/ln ln(1/delta)` guarantee. This is a distinction between the mathematical quantities, not a claim that the general correlation-gap theorem could not inspire a different coupling.

## Directed hypergraph terminology

Each deficiency is the cut indicator of a directed hyperedge with singleton tail `{a(e)}` and head `e\{a(e)}`: the tail lies in the selected set and at least one head lies outside. Khanna, Putterman, and Sudan, *Almost-Tight Bounds on Preserving Cuts in Classes of Submodular Hypergraphs*, explicitly define this directed-hypergraph cut convention and study sparsification and sketching of cut values. Their Theorems 1 and 2 concern preserving individual cuts through a transformation or a smaller hypergraph. [Primary ICALP 2024 manuscript](https://www.cis.upenn.edu/~sanjeev/papers/icalp24_submodular_hypergraph.pdf).

Preserving every deterministic cut also preserves expectations under any specified law. However, it does not repair separately chosen local laws into one global law or compare the sum of local concave closures with the global closure. Those are the additional requirements here. The minimum-mean choice of each anchor also imposes structure not shared by arbitrary directed-hypergraph objectives at arbitrary prescribed marginals. Searches in directed-hypercut and submodular-dependence terminology did not locate the candidate marginal-floor theorem.

## Other close-looking sources

Luedtke, Namazifar, and Linderoth, *Some Results on the Strength of Relaxations of Multilinear Functions*, state the uniform positive-coefficient gap conjecture in Conjecture 1 of the linked author manuscript. The manuscript compares the same envelope-gap quantities and is the direct MINLP context. Its numerical discussion samples points in a unit cube, but the inspected statements do not provide the candidate marginal-floor dependence. The present theorem supplies a sharp parameter-dependent replacement for the unrestricted constant conjecture, alongside the separately developed counterexample. [Primary author manuscript, Section 4 and Conjecture 1](https://jlinderoth.github.io/papers/Luedtke-Namazifar-Linderoth-12-TR.pdf).

Costa, *A proof for multilinear error bounds*, Theorems 1 and 2, bounds absolute errors for a single monomial relative to its hull. This concerns a different quantity from the loss due to separately convexifying several overlapping monomials. A single monomial has termwise/hull ratio one wherever its gap is positive. [Primary manuscript](https://optimization-online.org/wp-content/uploads/2024/01/multilinear_gap.pdf).

Staib, Wilder, and Jegelka, *Distributionally Robust Submodular Maximization*, has simultaneous approximation and same-marginal distributions in its discussion, but Section 2 assumes monotone submodular functions. The deficiencies here are generally nonmonotone. Its robust optimization statements are therefore not a direct application to these functions. [Primary paper and supplement](https://proceedings.mlr.press/v89/staib19a/staib19a-supp.pdf).

## The proposed density mechanism

The candidate uses a normalized density proportional to `1/(t+tau)`, with a regularization scale below delta. Low-coordinate successes share one threshold. High-coordinate conditional failures begin at `min{1,p h(t)}` and are increased to restore their exact original means. Conditional independence then supplies a simultaneous union estimate. When clipping occurs, the affected union is certain; otherwise the usual exponential product inequality applies.

Clipping, completion to a prescribed mean, threshold coupling, conditional independence, and the exponential union estimate are elementary mechanisms. This screen did not locate their specific assembly into the claimed simultaneous local-deficiency bound or a prior sharp marginal-floor theorem. The lower example is inherited from the local dyadic construction, so the new parameterization and density upper bound should be distinguished from a claim that the lower combinatorial family was newly invented in this step.

Search coverage included marginal boundedness and interiority in correlation gaps, nonmonotone submodular dependence, prescribed-marginal directed hypergraph cuts, sums of concave closures, simultaneous submodular approximation, and multilinear envelope errors. Broad searches sometimes returned unrelated uses of “marginal” or “gap”; those misses carry little weight. A publication should retain the exact comparisons above and broaden citation tracking beyond this bounded screen.
