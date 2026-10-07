# Independent mathematical review: stable nonlinear dynamics

Reviewed the manuscript `sections/dynamics.tex`, together with its actual
`sections/model.tex` and `sections/regridding.tex` dependencies. This report
does not rely on the original notes to establish validity. No computational
experiments, literature discovery, or knowledge-base operations were run.

## Verdict

The exact-real dynamics theorem and its example are mathematically sound as
written. No major mathematical repair is needed. The finite-precision section
was not present at this review stage and must receive a separate review once
its author declares it stable. One interface condition is essential there:
the derivative bound on the state coordinates must hold at arbitrary ambient
reset centers, whereas Assumption 7.1 in the dynamics section requires it
only at feasible centers. The adjoint lemma already states the stronger
pointwise hypothesis explicitly.

Minor editorial clarification: the theorem could initialize the incumbent
with `UB = F(y_{-1})` explicitly before its first stage. Its present meaning is
clear from the preceding algorithm, and the proof uses only inclusion of the
current repaired point.

## Checks

1. **Affine strips.** A two-dimensional input rectangle has midpoint radius
   at most `sqrt(2) w_B / 2`. The gradient-Lipschitz Taylor remainder is
   therefore at most `H w_B^2 / 4`. The strip's own deviation has the same
   bound. Their sum gives `|q_t(z)| <= (H/2) w_B^2`. The map invariance
   assumption is needed for repair, not for this graph-containment argument.
   Both ingredients use the full input rectangle. For `H=0` the graph is
   affine on the rectangle and the strip can be lower-dimensional; the stated
   compact-convex-domain oracle handles this case.

2. **Flags and certificate validity.** An own cell is flagged only after
   every incident leaf is unusable or its strip/own-cell intersection is
   empty. A true feasible subtree assignment cannot induce such a flag:
   its local point lies in its leaf strip, and its actual child separator
   value belongs to an intersecting unflagged child cell by induction. The
   minimum over all unflagged touching cells is a valid affine minorant for
   the true value selected at that separator. Therefore no true trajectory
   is lost. This also proves that the root has a finite configuration.
   Unfolding selects independent finite child minima exactly as in the
   box-domain dynamic program. Empty-domain calls are correctly retained
   in the work bound.

3. **Forward repair.** Invariance guarantees that every state constructed
   from the retained initial state and controls stays in its specified
   interval. The recurrence `|e_{t+1}| <= a |e_t| + |q_t(x)|`, followed by
   the Euclidean operator norm of the causal convolution with geometric
   kernel, proves `||R(x)-x|| <= ||q(x)||/(1-a)`. This bound is independent
   of the horizon. State restrictions or a terminal target would break
   this repair; the text expressly excludes them.

4. **Adjoints at infeasible centers.** The backward equation gives
   `d_j + mu_{j-1} - A_j mu_j = 0` for every dependent state, and the
   terminal equation gives `d_T + mu_{T-1}=0`. Neither equation uses
   `q(c)=0`. The initial state and controls do not move in repair, so the
   adjusted gradient annihilates every repair displacement. The geometric
   multiplier bound `|mu_t| <= G/(1-a)` is valid. The Hessian/gradient
   Lipschitz contribution of `mu_t q_t` is at most `|mu_t| H`, giving
   `overline M = M+UH`. The state `sigma_t` occurs only in bag `t`
   within that bag's descendant subtree, so its adjusted subtree slope is
   exactly the displayed `partial_sigma_t a_t - mu_t A_t`.

5. **Exact error identity.** Applying the telescope to the adjusted
   gradients, replacing the consistent point by its repair, and using
   `q_t(y)=0` gives
   `Phi = F(y) + sum T_t - sum err_t - sum mu_t q_t(z^t)`.
   The final multiplier-residual term cannot be dropped; the manuscript
   retains and bounds it by `UKQ`. It keeps the convex lower models of the
   original bag cost rather than making an unsupported claim that the
   multiplier-adjusted function has the same convex model.

6. **Copy error and repair error.** The original incidence estimate gives
   `E_x <= C_0 Q`, independently of strip membership. Each residual has
   Lipschitz constant `sqrt(1+a^2+b^2)`. Since `b_t <= s_0`, the strip
   residual contributes `K s_0 sqrt(Q)` to the stacked residual norm.
   This establishes `||y-x|| <= rho sqrt(Q)` and then
   `E_y <= (sqrt(C_0)+sqrt(k) rho)^2 Q = DQ`. The `K s_0` term is
   needed even for one bag. Using the uniform bound `k=2` for `T=1`
   merely overestimates; it causes no degeneracy.

7. **Grading absorption.** For bags and own separator cells, the squared
   center differences sum to at most `(2k-1)||y-c||^2`; the associated
   copy differences sum to at most `2E_y`. The latter is an upper bound,
   not an equality, because repair can change a private top-bag state.
   The text correctly makes this distinction. Thus
   `Q <= 6Nh^2 + 3(2k-1) theta^2 r^2 + 6 theta^2 E_y`.
   The first grading condition allows absorption of at most `Q/2` and
   yields `Q <= 12Nh^2 + 12k theta^2 r^2`. Young's inequality contributes
   exactly `eta r^2/2 + 6kD overline M^2 Nh^2/eta`; the remaining two
   grading conditions supply the other `eta/2`. The constants match.

8. **Growth and contraction.** Growth is imposed on the true feasible
   set and applies to `y_j=R(x_j)`. Combined with the valid lower bound,
   it gives `e_j <= e_{j-1}/9 + 10C Nh_j^2/(9g)`. The stage-zero
   diameter estimate is valid because `n=2T+1 <= 3T=pN`. The induction
   condition `B >= 2C/g` is sufficient since
   `4B/9 + 10C/(9g) <= B`. The gap estimate uses the current feasible
   point even if the retained incumbent is older. No stationarity,
   lower-bound monotonicity, or feasibility of an arbitrary lemma center
   is used.

9. **Counts.** Each graph strip changes the local domain but not the
   bag/own-cell or parent-leaf/child-cell geometric incidence list.
   Hence the exact bound is
   `N 3^q m^p (J+1)(J+2)(2J+3)/6`, with `p=3`, `q=1` for `T>=2`,
   and `q=0` for `T=1`. There is no product over child choices. There
   are at most three local variables and affine constraints, although the
   objective remains a supplied continuous convex function in this
   exact-real result. The claimed polynomial finite-bit implementation
   must replace that objective by its explicit affine realization.

10. **Analytic example.** The state-only part of the map is increasing on
    `[-1,1]` and has image `[-1/8,3/8]`, so adding `u/2` gives precisely
    `[-5/8,7/8]`. Its state derivative lies in `[0,1/2]`, its control
    derivative is `1/2`, and its input Hessian norm is `1/4`. Each bag's
    cost Hessian has norm at most `2`, including bag zero's additional
    initial-state square. The state objective derivative bound is `G=2`.
    The lower bound `u^2-u^4/4 >= 3u^2/4` gives full-box growth with
    `g=3/4` and the unique zero minimizer. Subtracting
    `(u-l)(r-u)/2` adds one to the cost second derivative, so the model
    is convex with second derivative `3-3u^2 >=0` and error at most
    `(r-l)^2/8`, corresponding to `A=1/2`. Varying only the final
    control gives reduced curvature `5/2-3v^2`, which is strictly
    negative at `15/16`. All stated example constants are correct and
    horizon-independent.

## Outstanding follow-up

Review the stable `dynamics-bit.tex` for the ambient derivative promise,
rational Taylor models, constant-dimensional LP certificates, reset-center
contraction constants, finite-bit adjoint evaluation, compressed trajectory
representation, contraction-based enclosures, and total bit complexity.
