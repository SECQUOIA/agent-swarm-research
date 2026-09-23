# Positive multilinear gap investigation

Date: 2026-09-04. This note records the route to `results/positive-multilinear-gap.md` and directions that remain open. Claims labeled conjectural or heuristic are not theorems.

## Main outcome

The dimension-independent positive-coefficient multilinear gap conjecture of Luedtke–Namazifar–Linderoth is false. A sparse dyadic construction has unit coefficients, O(n) monomials, O(n log n) variable occurrences, and an exactly computed gap ratio asymptotic to ln n/ln ln n. Two independent audits checked the proof and exact formula. Consult the result file and review notes for the full statement, proofs, limitations, and source review.

The discovery began with a dense symmetric multiscale-anchor construction. The root agent replaced the symmetric hyperedges with disjoint blocks at each level, removing the large monomial count and nonunit coefficients. Nested dyadic partitions then permit simultaneous saturation of every block-hit bound by bit-reversal failure sets, which yields an exact hull formula.

## Useful reformulations

For f(x)=Σ_e a_e∏_{i∈e}x_i, a_e>0, on the unit box, let u_e=min_{i∈e}x_i and choose an anchor r(e) attaining that minimum. For any binary random vector X with E X=x,

\[
u_e-E\prod_{i\in e}X_i
=E\left[X_{r(e)}1\{X_j=0\text{ for some }j\in e\setminus\{r(e)\}\}\right].
\]

Consequently the true hull gap is the maximum expected total of these nonnegative anchored failure indicators. The term-by-term gap of a monomial is

\[
\min\left\{u_e,\sum_{j\in e\setminus\{r(e)\}}(1-x_j)\right\}.
\]

Equivalently, put y=1−x and define the coverage function F(S)=Σ_e a_e 1[S∩e≠∅]. Then

\[
\operatorname{chgap}(x)=F^+(y)-\widehat F(y),\qquad
\operatorname{tbtgap}(x)=\sum_ea_e\left[\min\{1,\sum_{i\in e}y_i\}-\max_{i\in e}y_i\right],
\]

where F^+ is the concave closure and F̂ is the Lovász extension. Thus the disproved conjecture is an additive-strengthening variant of a coverage correlation-gap question; a usual multiplicative correlation-gap bound does not survive subtraction of F̂.

## A stronger numerical search and why it was insufficient

`code/multilinear_ratio/universal_coupling.py` optimizes all positive monomial coefficients simultaneously at a fixed x. Its LP finds the largest γ for which a single distribution λ over binary vertices with mean x satisfies

\[
\min_{i\in e}x_i-E_\lambda\prod_{i\in e}X_i
\ge\gamma\operatorname{tbtgap}_e(x)
\]

for every degree-at-least-two subset e. Finite minimax duality makes 1/γ the worst coefficient-weighted ratio at that point. The dual multipliers provide a worst polynomial. The script searches all monomials, not just a preselected random family.

Two hundred point samples per dimension for n=3,...,9 did not yield a ratio above two. The largest n=9 value was about 1.87179. This stronger search still missed the mechanism because many variables, highly unequal marginals, and multiple coordinated scales are needed. It is evidence about those samples, not a bound.

A factor-two universal-coupling conjecture was therefore considered and rejected by the later multiscale construction. Independent Bernoulli rounding also fails as a universal constant-factor proof: a term with one very small coordinate and many coordinates near one can have an independent-rounding gap arbitrarily smaller than its term-by-term gap.

## Earlier family worth preserving

The pre-existing star-plus-leaf-monomial family is

\[
f_m(x)=x_0\sum_{i=1}^m x_i+\prod_{i=1}^m x_i,
\qquad x_0=1/m,\quad x_i=1-1/m.
\]

Its tbt gap is 2−1/m and its hull gap is one. One certificate for the convex envelope is

\[
f_m(v)\ge \sum_{i=1}^mv_i-(m-1)+(m-1)v_0
\]

for all binary vertices: if v_0=0 and not all leaves are one, the right side is nonpositive; if v_0=0 and all leaves are one, the monomial gives one. If v_0=1, the right side equals the leaf sum and is bounded by f_m(v). This lower bound has expectation 1−1/m. It is attained by the coupling with all leaves one and x_0=0 with probability1−1/m, and all leaves zero and x_0=1 with probability1/m. The concave envelope is 2−1/m, so the hull gap is one. This family approaches two and suggested an incorrect universal upper bound before the multiscale idea was found.

## Continuation and subsequent resolution

- **Subsequently resolved with completed written audits:** dyadic conditional-failure couplings give an O(log d) upper bound (`results/positive-multilinear-degree-upper-bound.md`). A harmonic coupling improves it to O(log d/log log d). An optimized mixture and threshold refinement gives leading constant one, matching the exact lower construction. The [sharp result](../results/positive-multilinear-sharp-degree-growth.md) links both independent audits and root review. The same asymptotic applies to worst-case dimension n.
- Determine exact finite-degree or finite-dimension worst ratios and sharper lower-order asymptotics. The new harmonic upper bound rules out a larger leading growth order.
- The exact hull proof only needs equal block partitions for the logarithmic upper estimate; nested dyadic structure supplies attainment. Study nonnested partitions and whether they increase the ratio for the same dimensions and degrees.
- The [marginal-floor theorem](../results/positive-multilinear-marginal-floor-gap.md) subsequently established sharp asymptotic growth when coordinates stay away from zero, also with a matching two-sided interior construction. Exact finite-parameter values remain open.
- Investigate whether recognized multilinear-polytope inequalities already close this sparse counterexample, and how many are needed. The ratio concerns the base term-by-term relaxation; it does not by itself measure the complexity of closing its gap.
