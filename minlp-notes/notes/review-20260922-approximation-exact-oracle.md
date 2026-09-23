# Independent review: additive oracles and exact smoothed optimization

Date: 2026-09-22. Reviewer: `review_approximation_exact_oracle`.

Reviewed source: [Additive approximation and exact smoothed optimization with deterministic offsets](research-20260922-approximation-exact-smoothing.md).

**Verdict.** The conversion, the fixed-treewidth indicator-QP oracle, and the finite-grid expected bit-complexity argument are correct under the stated assumptions. I found no substantive mathematical correction. The general statement should explicitly assume a nonempty feasible set, or specify that an empty root-oracle response returns infeasibility before defining an incumbent. This convention is automatic for the indicator application. The result is useful as a comparison and a concrete corollary of an established conversion strategy; it should not be presented as the invention of exact expected-time smoothed conversion.

## 1. Approximate enumeration and its certificate

The first-difference partition is valid for arbitrary feasible sets, not just the whole binary cube. For a cell with some bits fixed and an extracted support `z`, order the remaining coordinates. Assign every other feasible support to its first coordinate that differs from `z`. The resulting cells are disjoint and their union is exactly the original cell minus `z`. Some cells can be empty; the assumed restricted oracle recognizes them.

For each nonempty cell `p`, the bound `L_p=V_p-epsilon` is a genuine lower bound on its true restricted optimum. A computed candidate remains a feasible global incumbent after its original cell is removed. Thus retaining the best value over **all** candidates ever computed is correct, including candidates that were never extracted. Previously extracted supports also remain covered by this incumbent comparison. If every remaining lower bound is at least the incumbent, none of the remaining supports can improve it, and no removed support can improve it either.

The key near-optimality claim does not presume that the approximate candidates are extracted in exact objective order. Consider the selected cell while the certificate has failed:

- If at least one global optimizer remains in the partition, its cell has lower bound at most the global optimum. Selecting the minimum lower bound gives the same inequality for the selected cell.
- If all global optimizers have been extracted, the incumbent already equals the global optimum. Failure of the certificate gives a selected lower bound strictly below it.

In both cases the extracted candidate has value at most `v+epsilon`. Distinctness follows from the partition invariant. Therefore reaching the extraction budget `k` implies that the original instance has at least `k` distinct epsilon-near-optimal supports. The restrictions are chosen adaptively, but this implication is pointwise for each full noise vector. No probabilistic conditioning on the adaptive search history is used.

The `1+kn` oracle-call count is valid. Implementing the cell list and selecting its minimum also costs polynomial time: there are at most `1+kn` cells, and `k=2^(r-1)+1` is a fixed constant when the approximation exponent is fixed. A linear scan is sufficient; no special data structure is needed for the complexity conclusion.

## 2. Higher-gap dependency and the precision loop

I independently rechecked the affine-rank argument rather than assuming the earlier review settles its use here. An affine space of dimension `r-1` has an injective projection onto `r-1` coordinate positions and therefore contains at most `2^(r-1)` binary vectors. More near-optimal supports provide `r+1` affinely independent supports and a nonsingular projected difference matrix on `r` coordinates.

After conditioning on the other coordinates, the minimum offset in each selected pattern class is deterministic. Each represented class has its minimum within epsilon of the global optimum. Differences from one reference class therefore lie in `[-epsilon,epsilon]`, independently of which support attains the class minimum. The nonsingular integer difference matrix has determinant of absolute value at least one. The volume and bounded joint-density argument consequently applies to arbitrary deterministic offsets. Taking a union over coordinate sets and ordered pattern lists gives the displayed coarse constant. There is no union over all supports hidden in that constant.

Reaching precision stage `j` implies failure at stage `j-1`; it does not require independence between stages. Multiplying this probability by a deterministic upper bound on the stage cost and summing is sufficient. With stage cost proportional to `2^(aj)` and failure probability proportional to `2^(-r(j-1))`, the series converges when `r>a`. This proves finite expected total work and hence almost-sure termination. The separate enumeration convention for `n<r` avoids applying the rank bound outside its range.

For arbitrary real noise this is an arithmetic-oracle statement. It is not a Turing algorithm for arbitrary real numbers. The source makes that distinction, and the rational finite-grid construction addresses the bit model separately.

## 3. Restricted fixed-treewidth approximation oracle

All fixed-bit restrictions preserve the supportwise stationarity argument. A bit fixed to one still permits the corresponding continuous coordinate to equal zero. A bit fixed to zero forces it to zero. On any chosen support, strict symmetric diagonal dominance and positive diagonal imply positive definiteness, so the continuous conditional optimum exists uniquely.

At its largest coordinate, stationarity gives

\[
 X\le C/(2d)+\rho X,
\]

and therefore `X<=M`. This uses no graph degree bound. The symmetric row-sum estimate gives `||Q||_2<=D(1+rho)=H`.

The rounding argument is especially important: the first-order term vanishes because rounding is confined to the chosen support. It would generally fail for a grid scheme that activated formerly inactive continuous coordinates without changing the support. Here inactive coordinates remain zero, while active coordinates are rounded within the box. An even number of grid subdivisions includes zero and gives coordinate error at most `M/B`. Thus the exact conditional minimizer has a feasible grid representative with objective increase at most `HnM^2/B^2`.

The finite-domain tree-decomposition dynamic program is valid with state cardinality `B+2`. Assigning each unary and edge cost to one containing bag avoids double counting. A child table can first be minimized over its separator states, then added to each compatible parent-bag state. The resulting operation count is polynomial in the number of bags times `(B+2)^(w+1)`, without multiplying the state counts of a parent and child. Fixed-bit restrictions only delete local states, so the same oracle applies to every cell in the partition procedure.

The optimum grid support gives a continuous conditional value no larger than its grid value. Exact conditional minimization therefore preserves the epsilon guarantee. Formula (8) evaluates this value and recovers a feasible rational continuous vector by solving a rational positive-definite principal system. Its encoding length is polynomial in the rational input length; this is not an assumption about floating-point conditioning.

For fixed structural magnitude bounds and fixed width, `B=O(1+sqrt(n/epsilon))`, up to the stated constants, gives the claimed inverse-accuracy exponent. Taking a larger fixed exponent to absorb logarithmic bit factors is legitimate. Dependence on the numerical magnitude and diagonal-dominance margin is essential; the proof does not establish polynomial dependence on their encoding lengths alone.

## 4. Finite-grid cutoff, ties, and expected bit complexity

The finite-grid higher-gap estimate survives exact ties. Entries of the selected difference matrix belong to `{-1,0,1}`. Cofactors have magnitude at most `(r-1)!`, and the inverse has that same entrywise bound because the nonzero integer determinant has magnitude at least one. The inverse image of the difference box is contained in a coordinate box of side length `2r! epsilon`.

For `N_g` equally spaced points in `[-sigma,sigma]`, the probability of any interval of length `ell` is at most

\[
 \frac{(N_g-1)\ell}{2\sigma N_g}+\frac1{N_g}
 \le \phi\ell+\frac1{N_g}.
\]

Conditioning on the other coordinates and taking the coordinate-box product proves the stated bound. This product argument would not follow from a density bound, since the finite-grid distribution has none; the source uses the interval estimate correctly.

Let `t=min(1,sigma)`. The first index with `2^-J<=t/N_g` satisfies

\[
 2^J<2N_g/t.
\]

Consequently the atomic contribution to expected stage work is bounded by a constant times

\[
 N_g^{-r}2^{aJ}
 \le 2^a N_g^{a-r}\max(1,\sigma^{-a}).
\]

Polynomial factors in the input length and in `J` can be kept outside this finite sum, or absorbed into a slightly larger fixed accuracy exponent. The continuous contribution is the convergent series already checked above. At the final stage, `phi epsilon_J<=1/(2N_g)`, so failure has probability at most a constant depending on `r` times `n^r N_g^-r`. With `N_g=2^n`, even an exhaustive `2^n`-support fallback has polynomial expected cost. These calculations need `r>a`, not any unmentioned independence between fallback and the earlier stages.

The algorithm is correct on every grid-noise realization, including those with many tied optimizers. The expectation concerns its runtime only. Endpoint grid coordinates have denominator `N_g-1`, whose encoding uses `O(n)` bits; sampling a uniform grid index requires exactly `n` independent bits. Intermediate precision exponents satisfy `J=O(n+log^+(1/sigma))`. Including the rational encoding of `sigma` in the input size, all exact arithmetic has polynomial bit cost per operation. The bound is polynomial in `1/sigma`, not in `log(1/sigma)` alone.

This use of an exponentially fine grid and a rare exhaustive fallback is mathematically sound. It offers no evidence that the fallback-based method is preferable in a solver implementation.

## 5. Priority and significance

I reopened [Röglin and Teng, FOCS 2009](https://www.roeglin.org/publications/FOCS09.pdf), especially Sections 6.1–6.2 and the appendix. Lemma 6.1 already gives a higher-winner-gap estimate at the same support-count threshold. Theorem 6.2 already proves an expected-polynomial smoothed conversion for binary linear optimization from a randomized pseudopolynomial algorithm. Their proof also refines coefficient precision and compares a growing computation cost with a decaying higher-gap probability. Finite precision is discussed there as well.

The present note gives a transparent offset argument, a directly certified additive-oracle interface, and a concrete fixed-treewidth indicator-QP specialization. Those are useful contributions to the local research program. They do not justify claiming that nonlinear eliminated support costs prevent the classical conversion strategy, or that expected runtime itself distinguishes the complete-message result from prior conversion theory. The note's restrained comparison is appropriate. A full novelty audit of this exact offset formulation and the indicator corollary remains open; this review did not independently re-audit every cited paper.

## 6. Targeted verification and remaining limits

I ran an exact rational adversarial partition check with:

```text
python3 /tmp/check_approximation_exact_partition.py
```

The temporary checker enumerated all ternary-valued objective tables on the full binary cubes of dimensions one and two, and 600 seeded tables on arbitrary nonempty subsets in dimensions three through five. For each it used three exact rational accuracies and three extraction budgets. The mock oracle deliberately returned the **worst** allowed epsilon-approximate objective value in its cell. At every step the checker verified disjoint coverage of precisely the unextracted feasible supports. It also checked each extracted candidate's global near-optimality, every optimality certificate against exhaustive minimization, and every budget failure against the true near-optimal support count.

All **6,210 runs** passed: **16,290 extractions**, **3,358 certificates**, and **2,852 budget failures**. These finite checks challenge the partition implementation and the invariant, including ties and empty child cells. They do not prove the probabilistic bounds, asymptotic runtime, or tree-decomposition oracle; those were checked by the mathematical derivations above. The checker is a temporary review aid, not a repository implementation of the proposed optimization algorithm.

No Lean proof, project-wide checks, or CI inspection were performed. I did not edit the reviewed source. Beyond the empty-domain convention, I found no correction required for the stated conclusions.
