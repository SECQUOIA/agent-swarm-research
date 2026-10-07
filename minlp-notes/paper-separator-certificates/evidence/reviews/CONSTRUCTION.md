# Independent mathematical review: constructive and inexact regridding

Reviewed the current manuscript proofs in `sections/regridding.tex` and `sections/inexact.tex`, with the model section and canonical regridding and inexact notes as context. The arguments below were checked from the manuscript, rather than accepted merely because they match the source. Arithmetic implementation review will be added after that section is reported ready by the root author.

## Verdict

No mathematical repair is required in the reviewed sections. The shell construction, touching-incidence upper bounds and enumeration, aggregate copy estimates on arbitrary trees, error constants, base cases and contraction, selected-residual identity, slope and gradient perturbations, certified stopping, and budgeted unknown-parameter search are valid under the stated assumptions. The draft correctly separates oracle-call accounting from internal numerical work and distinguishes fixed-sufficient-ratio size bounds from the output of parameter search.

No literature research, knowledge-base operations, computational experiments, project-wide checks, or CI inspections were performed.

## Regridding construction

### Shell coverage and grading

The grid side at level $\ell\ge1$ is $g_\ell=\theta 2^{\ell-1}h$, and the inner cube boundary aligns because $1/\theta$ is an integer. A cube not contained in the inner cube has its interior entirely outside that cube, so the infimum sup-distance of the entire closed cube is at least $2^{\ell-1}h$. Therefore its width is at most $\theta$ times that distance. The level-zero width is $h$. Clipping can only reduce the width and increase the set-to-center distance.

Removing empty-interior clipped pieces preserves every boundary point when the original box is nondegenerate. Approximate the point by interior points avoiding all grid hyperplanes, use the finite family to select one repeated containing piece, and pass to its closed limit. This argument is valid also for a center on a boundary or at a vertex. The separately defined zero-dimensional cell is consistent with all later counts. Removing original fixed coordinates before this operation is essential and is done explicitly.

### Arbitrary-tree drift

For one occurrence-tree edge and coordinate, joining child and parent copies through a point of the closed separator-cell/parent-box intersection gives

\[
|z_i^t-z_i^{\pi(t)}|\le b_{\pi(t)}+d_t.
\]

No assumption that the parent copy belongs to the chosen child cell is made. On an occurrence path each parent width and cell width appears once. The path-incidence matrix therefore has squared Frobenius norm $2\sum_t\operatorname{depth}(t)$; the depth sum is at most $m_i(m_i-1)/2$. Summing over coordinates counts each bag width at most $|V_t|$ times and each cell width at most $|S_t|$ times. This independently gives $E\le k(k-1)pQ=C_0Q$ without a tree-degree factor.

### Grading absorption

For every coordinate, the number of containing separators is exactly one less than the number of containing bags. Copy errors vanish on $V_t\setminus S_t$, because such a coordinate first appears at $t$. Thus the bag-plus-separator sum of squared center differences is bounded by $(2k-1)R^2$, while the corresponding copy-error sum is exactly $2E$. These facts imply

\[
Q\le6Nh^2+3(2k-1)\theta^2R^2+6\theta^2E.
\]

The condition $12C_0\theta^2\le1$ permits absorption and yields $Q\le12Nh^2+12k\theta^2R^2$. When $k=1$, every separator is empty and $E=0$, so no zero denominator or unproved limiting argument is needed.

### Current-center remainder and constants

Taylor expansion at the consistent bag point followed by the Lipschitz gradient comparison with the current center gives

\[
|T_t|\le M\|x_{V_t}-c_{V_t}\|\|z^t-x_{V_t}\|+\frac M2\|z^t-x_{V_t}\|^2.
\]

The model errors are nonnegative and at most $Ab_t^2/4$. Therefore

\[
|F(x)-\Phi|\le M\sqrt{kC_0}R\sqrt Q+B_0Q.
\]

After grading, Young's inequality with coefficient $\eta/2$ pays the mixed term with $6kC_0M^2Nh^2/\eta$. The other two displayed restrictions on $\theta$ each pay at most $\eta R^2/4$. This verifies $C=12B_0+6kC_0M^2/\eta$ and the full error estimate. The cancellation is algebraic at an arbitrary box center; a boundary optimum introduces no missing first-order term.

### Contraction and its base case

Lower-certificate validity and quadratic growth give

\[
ge_j\le\frac g{20}\,2(e_j+e_{j-1})+CNh_j^2,
\qquad
e_j\le e_{j-1}/9+10CNh_j^2/(9g).
\]

For later stages, $h_{j-1}=2h_j$ and $B\ge2C/g$ give the asserted invariant. At stage zero, $e_{-1}\le ns_0^2\le pNh_0^2\le BNh_0^2$, hence $e_0\le2BNh_0^2/3$. The looser stage-zero center-distance bound with coefficient four is valid. The certified gap follows from $(gB/2+C)Nh_j^2\le gBNh_j^2$. No upper-growth estimate or monotonicity of lower bounds is used.

### Touching incidences and enumeration

A closed interval whose length does not exceed a regular grid's spacing meets at most three of that grid's closed intervals, even when endpoints coincide. This remains true for distinct grid anchors. For each pair of shell levels, charge pairs to the finer bag grid, or to finer separator cells and the private-coordinate bag fibers. The respective bounds are both at most $3^{q'}m^d$. Clipping cannot add an intersection between previously disjoint cubes. Central grids are regular with at most two positions, so the same bound applies despite their side length differing from the first annular grid.

The stated enumeration avoids a dense all-pairs scan: enumerate a finer grid position, calculate the at most three coarse positions per separator coordinate, enumerate private fibers if needed, and filter shell membership and clipping. Its candidate count is the same bound as the incidence count, with $O(p)$ coordinate work per candidate.

There is one local program per nonroot own-cell incidence and one per root leaf. Parent-child incidences determine separate child minima, without a product over children. The root count is covered by its allocated share of $N3^qm^p(j+1)^2$. Summing $j+1$ and $(j+1)^2$ verifies all final-box, created-box, and local-call counts. The additional affine-child aggregation cost is covered because $\sum_t|\operatorname{ch}(t)||\mathcal L_t|\le(N-1)m^p(j+1)$.

### Unknown-parameter search

With $W\ge\max\{2,2^{\mu_*}\}$, the round $R=\lceil\log_2W\rceil$ includes the sufficient grading index and allows its full run. Restarting finite runs without a separate stage cap introduces no completeness problem because each counted operation is budgeted and each oracle call terminates. The sum of all trial budgets is at most $2R2^R=O(W\log W)$.

The first successful trial need not be the sufficient one. Its returned gap remains valid solely by certification, and the text correctly refrains from substituting sufficient-run parameters into that trial's final-box estimate. Counting box emission gives at most $2^R=O(W)$ returned boxes. This is a distinct assertion from the sharper fixed-sufficient-ratio bound.

## Inexact construction

### Validity and residual identity

Every reported local lower bound satisfies $q(v)\ge\ell\ge\widehat\beta$ throughout its domain. Choosing the smallest compatible child intercept gives the required child inequality. Thus approximate slopes and nonmaximal certified intercepts preserve validity.

Along the selected backtracked configuration, each selected nonroot local lower bound equals its incoming table intercept, and its parent's selected child constant equals the same number. Summing local objectives and subtracting selected lower bounds cancels every such inherited constant exactly, yielding

\[
\widehat\Phi-\mathrm{LB}=\sum_t(q_t(z^t)-\ell_t),
\qquad 0\le q_t(z^t)-\ell_t\le\delta_{t,j}.
\]

Exactly one selected residual is paid per bag. No term for all solved pairs belongs in this sum. Constants inherited from child messages may be removed from the objective for the numerical solve and added back exactly as the text suggests.

### Perturbation estimates

For each parent bag, the sum of child-separator dimensions is at most $(k-1)|V_t|$, since a coordinate can belong to no more than $k-1$ additional child bags. The edge-difference estimate therefore gives $H\le C_1Q$ with $C_1=2p\max\{k-1,1\}$. Cauchy--Schwarz and grading give two terms: $\sqrt{12C_1}\zeta Nh_j^2$ and $\sqrt{12kC_1}\zeta\theta\sqrt N h_jR$. Young's inequality with allowance $\eta R^2/4$ yields precisely the displayed $K_s$.

The bag-gradient-to-slope map has one incidence for every ancestor occurrence edge. Its squared Frobenius norm is the occurrence-depth sum, at most $G=k(k-1)/2$. Summing the operator bounds by coordinate gives $\nu^2\le G\sum_t\|e_t\|^2$. The stated vector and componentwise error conditions then follow. For $k=1$, actual slope and edge differences are zero; no gradient approximation is needed for these estimates.

### Contraction, evaluation, and search

The exact error and slope perturbation allowances total $\eta+\eta/4=g/16$. Adding selected residuals gives the local-to-global error bound before upper evaluation. Quadratic growth gives the contraction factor $1/7$. With $B_{\mathrm{in}}\ge8K/(3g)$, the later-stage induction closes and the stage-zero estimate improves to $4B_{\mathrm{in}}/7$. The actual certified gap is at most $(5gB_{\mathrm{in}}/8+K)Nh_j^2\le gB_{\mathrm{in}}Nh_j^2$. The upper evaluator's allowance is correctly included in $K$ without altering certificate validity.

The inexact parameter search uses fixed positive approximation budgets and requires all certified calls to terminate. Requests do not need the unknown growth or model constants. It gives the same honest work/output distinction as exact search. The absence of a stage cap is useful: a sufficient run is determined only by its actual finite counted work.

### Rational reconstruction

The intersection of rational bag and own-cell boxes is a rational box, possibly a face. Exact endpoint comparison detects emptiness and fixes every singleton coordinate. On the remaining relative box, rational clipping of a coordinatewise approximation to a feasible point cannot increase its error. Thus the returned point is exactly feasible and within Euclidean distance $\sqrt p\tau$ of that point. A supplied Lipschitz bound gives the objective transport allowance $K_q\tau$, which fits the second half of the local gap budget.

The argument properly separates feasibility from objective certification and does not claim that mere continuity supplies an efficient procedure. Positive tolerance admits rational points by density, but zero tolerance need not: the strictly convex polynomial example on $[1,2]$ has unique irrational minimizer $\sqrt2$ and correctly demonstrates this limitation.

## Integration notes

These are reminders rather than defects in the reviewed text:

- Retain all touching intersections in numerical implementations, including face-only local tasks.
- Model generation, bag term counts and oracle internal work must remain in the later arithmetic accounting.
- The parameter-search bound requires charging output emission, comparisons, arithmetic, construction and enumeration. An oracle-call-only budget would not bound final box output.
- Never replace the newly backtracked next center with the best retained incumbent without a fresh proof; the current manuscript makes the correct choice.
- Unknown soundness parameters needed to construct a lower model cannot be treated like unknown parameters needed only in the convergence proof. The rational polynomial implementation must certify its model curvature bound.

## Arithmetic implementation

Pending the author notification requested by the root. No conclusion on that section is asserted here.
