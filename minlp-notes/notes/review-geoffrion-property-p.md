# Independent review: the common-optimizer limitation in Property (P′)

Date: 2026-09-05. Reviewer: independent `benders_review` agent.

Reviewed [the result draft](../results/geoffrion-property-p-conjecture.md), its exact-arithmetic verification script, and Geoffrion's primary statement. Theorem 1, Proposition 2, Corollaries 3–4, and Proposition 5 with its polynomial consequence are mathematically correct under their stated assumptions. This is a verified structural counterexample, with a qualified novelty claim. It is not a refutation of the informal computational Property (P).

## Source and scope audit

The primary source is [Geoffrion (1972), §2.5 and §4.2, printed pp. 251 and 256–257](https://www.anderson.ucla.edu/faculty_pages/art.geoffrion/home/docs/GBD.pdf), also available in the repository's [full text](../literature/papers/geoffrion1972-generalized-benders-decomposition/fulltext.md).

Property (P) describes obtaining whole value functions with essentially the effort of one optimization. Equations (22-1) and (22-2), labeled (P′), instead require a single optimizing continuous point for all complicating-variable values. The conjecture paragraph names (P), then discusses a compactness argument using (P′). The example separates the two conditions in (P′) outside compact domains. Its feasibility value function is the explicit constant 1/2, so it does not disprove the informal computational implication. The source already discusses weakening compactness; the positive compactness substitute in the draft should not be presented as independently new.

## Independent calculation

Write the continuous variables as `(r,a,b,t)`. The set is nonempty, closed, convex, and second-order-cone representable. In particular,

\[
(a+b)t\ge1,\quad a+b,t\ge0
\quad\Longleftrightarrow\quad
\|(2,a+b-t)\|_2\le a+b+t.
\]

The constraints `r²≤a,b` are convex epigraph constraints, and the other domain constraints are linear. The set is unbounded only through the auxiliary coordinate `t`, while all objective and coupling values are bounded.

For either binary choice, maximizing `f+uG` is bounded above by maximizing

\[
u/2+r-ur^2\qquad (0\le r\le1).
\]

For `0≤u≤1/2` the derivative is nonnegative and the maximizing `r` is 1. For `u>1/2`, completing the square gives

\[
u/2+r-ur^2=u/2+1/(4u)-u(r-1/(2u))^2.
\]

The proposed point with `a=b=r²` and `t=1/(2r²)` attains the bound for both binary choices. It is finite for every finite multiplier, including the separately defined case `u=0`. Thus the first condition of (P′) holds with actual attainment.

The separate feasibility maxima are both 1/2. They are attained at `(0,0,1,1)` and `(0,1,0,1)`. A simultaneous maximizer would have `a=b=0`, contradicting `(a+b)t≥1`. Thus the second condition fails despite separate attainment.

For every `u>0`, any common Lagrangian maximizer must have `a=b=r²` and the displayed maximizing `r`. Consequently, for `u>1/2`, every such common maximizer has

\[
t\ge2u^2.
\]

The escape to infinity is therefore unavoidable for all exact common selections, not an artifact of choosing an unnecessarily large auxiliary coordinate.

The strict point `(1/4,1/4,1/4,3)` lies in the ordinary interior of the continuous domain and has strictly positive coupling for both binary choices. Each original fixed-binary subproblem attains value `1/√2`, and multiplier `u=1/√2` gives the same dual value. Thus this example does not depend on primal infeasibility, failure of Slater's condition, a duality gap, or unbounded objective values.

## Verification of the positive statements

Proposition 2 follows from comparison with any fixed competitor `z` and the finite upper bound on `f(·,y)`. That bound is automatic from the first condition at `u=0`. Taking a near-maximizing competitor first, then sending the multiplier to infinity, proves pointwise convergence even without individual feasibility attainment. The explicit `O(1/u)` bound additionally assumes attainment. Uniformity on finite `Y` follows by taking the maximum of finitely many convergence thresholds; uniformity on arbitrary `Y` follows from uniformly bounded displayed constants when maximizing competitors exist.

Corollary 3 is a valid closed-image argument. The joint downward closed image in the example is exactly

\[
(-\infty,1/2]^2\setminus\{(1/2,1/2)\}.
\]

Every point below the missing corner is dominated by a feasible pair of coupling values: choose `r=0`, choose one of `a,b` positive and sufficiently small, set the other to zero, and choose `t` sufficiently large. The individual images are both the closed interval `(-∞,1/2]`. Hence individual image closedness, as used elsewhere in generalized Benders theory, does not imply the joint image closedness needed here. For polyhedral domains with affine coupling functions, the relevant joint image is a polyhedral projection and is closed.

Corollary 4 is valid for arbitrary, even uncountable, `Y`. The compact anchor supplies one convergent subsequence. Pointwise convergence has already been established along the entire sequence for every fixed `y`; upper semicontinuity therefore works for every `y` along that same subsequence. No diagonal argument or countability assumption is needed.

Two editorial clarifications were requested from the author and applied: the opening affine-function description now says affine in continuous variables for each binary choice, and the conclusion applying Corollary 3 to every multiplier retains finiteness of the feasibility suprema for every multiplier.

Proposition 5 is correct: finite simultaneous convergence makes the supremum of the sum equal to the sum of the finite suprema, and attainment of this sum forces every nonnegative coordinate deficit to vanish. Its polynomial consequence uses a precisely applicable known theorem. The [primary abstract of Belousov and Klatte (2002)](https://link.springer.com/article/10.1023/A:1014813701864) states attainment for a convex polynomial bounded below on a nonempty set defined by convex polynomial inequalities. The proposed aggregate negative coupling is a convex polynomial of exactly that kind. The [open primary Theorem 1 of Martínez-Legaz, Noll, and Sosa (2018)](https://arxiv.org/html/1805.03451) also supports the indicated extension to convex sets without flat asymptotes. The draft appropriately separates these known attainment results from the counterexample and distinguishes a convex feasible set from a convex polynomial defining that set.

## Limits of this review

The exact proof is the verification; rational spot checks provide supporting checks of transcription and formulas. This review does not certify literature novelty or publication significance. The construction provides a useful clarification of a compactness boundary, but by itself supplies no new decomposition algorithm or complexity improvement.
