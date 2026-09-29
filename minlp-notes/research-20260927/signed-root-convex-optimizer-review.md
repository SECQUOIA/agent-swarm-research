# Independent review of the convex optimizer baseline

Date: 2026-09-28. Status: passed with no correction required.

I independently read the full
[certified-root optimizer baseline](signed-root-convex-optimizer-baseline.md).
I did not develop its weighted-objective argument. The proof is correct,
including signed affine dependencies, independently boxed power variables,
finite rational weights, and the distinction between a unique optimizer
and a feasible singleton. No computation is needed for the short universal
inequality, and none was used to replace its proof.

On the normalized positive boxes, every power function $X_i^e$ and
$X_i^{d_i}$ is convex. Each constraint subtracts only a linear variable
or an affine radicand, so its sublevel is convex on that domain. This
does not assert global convexity of an odd power on the entire real
line. The boxes make the feasible set compact, and the exact circuit
point proves nonemptiness.

The supplied radicand certificate uses the independent intervals for
each retained predecessor power. It therefore remains valid when the
optimization power variables differ from the actual powers, provided
they stay in those same boxes. After orienting power variables by a
minus sign, each variable has a triangular upper bound $y_t\leq
g_t(y_{<t})$. Its boundary value is always inside its own box. The
recursive all-boundary point is feasible and is exactly the required
normalized circuit and powers.

For completeness, set $D=1+C$ and let
$S_t=\sum_{j\leq t}|e_j|$, with $S_0=0$. From the stated slack
recursion,

\[
 S_t\leq D S_{t-1}+\delta_t,
 \qquad
 S_{t-1}\leq\sum_{j<t}D^{t-j-1}\delta_j.
\]

It follows that the coefficient of $\delta_j$ in the lower bound
on the weighted objective difference is

\[
 W_j-C\sum_{t>j}W_tD^{t-j-1}.
\]

For $B=2(C+1)$ and $W_t=B^{N-t}$, the ratio of the subtracted
term to $W_j$ is at most

\[
 C\sum_{h\geq1}B^{-h}D^{h-1}
 =\frac{C}{B-D}=\frac{C}{C+1}.
\]

Thus the objective gap is at least
$(C+1)^{-1}\sum_jW_j\delta_j$. If any slack is positive,
the objective is strictly smaller. If all slacks vanish, triangular
recursion forces equality with the circuit point. This proves uniqueness
without requiring monotonicity of the gates in their predecessors.

The choice $C=NA^N$ bounds each relevant coordinate derivative on
the normalized boxes: the radicands stay at least one, root derivatives
are at most one, and retained power derivatives are at most
$eA^{e-1}$. The mean-value bound on the convex predecessor boxes gives
the required Lipschitz estimate. Since $\log C$ has polynomial size,
so do all rational weights $B^{N-t}$. The model has polynomial size in
the supplied circuit and interval encoding with unary degrees.

The scope comparison is accurate. This gives a compact convex program
with a unique optimizer and potentially nonconstant polynomial degrees.
It does not give the quartic construction's unique feasible point,
uniform global curvature, or rational Hessian certificate. Neither
representation by itself proves polynomial-time exact optimization,
an arithmetic-comparison hardness result, or novelty.

No project-wide verification, CI inspection, or Lean checking was run.
