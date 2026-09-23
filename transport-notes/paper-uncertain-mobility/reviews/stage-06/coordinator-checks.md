# Coordinator checks and development: Stage06

Date: 2026-09-07. Stage05 was accepted before author assignment. Read the complete finite-precision note and its independent review. The sharp finite positive ratio was explicitly open there. The following is an independent derivation for the current stage; the sole author is writing the manuscript proof and will then receive five independent reviews.

## Conditional symmetry and lower localization

Reflection s→2pi−s preserves k_c for every c, so convexity of J permits a symmetric design within each individual bin. No c→−c symmetry of a bin is needed. Each open half-circle then carries mass m=M/2 exactly.

On a compact regular offset set, use bin midpoint c0, curvature a=1−c0², root r0=arccos(−c0), and ell=(m/a)^(1/5). Normalize the pushforward of D ds on a fixed root interval under x=(s−r0)/ell by m. Along a subsequence it converges vaguely to a measure of mass at most one. For c=c0+sqrt(a)ell u, compact tests with amplitude (a ell²)^(-1) give limiting potential (x−u)² and response factor 1/(a ell). Reflection gives two identical local test contributions. The uniform bin parameter becomes u uniform on an interval of width eta=Delta/(sqrt(a)ell)=2^(1/5)(Delta/M^(1/5))a^(-3/10).

For sequences c0→c*, eta→eta*, reparametrize the average by u=eta z, z∈[-1/2,1/2]. Compact-test convergence and Fatou give the integrated local liminf. Stage03 singular-mass removal is potential-independent on each compact support and applies unchanged to (x−u)². If the limiting density has mass below one, add an arbitrary nonnegative integrable density to reach one; monotonicity shows that the original response cannot be smaller than the unit-mass value. Thus loss or singular concentration cannot defeat the lower bound. Strict mass loss, uniqueness, or existence of a local minimizer is unnecessary here.

The resulting conditional coefficient is 2/(a ell) times the local value, namely 2^(6/5) a^(-4/5) M^(-1/5) Fcenter(eta). The lower argument covers arbitrary concentrated and oscillatory bin designs.

## Quadratic positive-background lemma and continuity of Fcenter

For a fixed integrable density d≥b(1+|x|)^(-alpha), 1<alpha<2, compact shifted centers give a positive local floor and a uniformly anchored quadratic energy. Outside a fixed core, the potential controls x²v², so the source tail has bound C L^(-1/2) E[v]^(1/2). Local weighted derivative compactness identifies weak limits.

The whole-line completion step is justified by the unit-interval Sobolev estimate

|v(x)|² ≤ C [|x|^(-2)+|x|^(alpha/2−1)] E[v].

It follows by combining the local L2 bound of order |x|^(-2) and derivative bound of order |x|^alpha. The chosen alpha<2 makes v bounded. A remote cutoff then has added derivative energy at most C R^(-2)||v||_infinity² integral_annulus d→0, while the original energy tails vanish. On compact intervals the floor permits smooth derivative approximation in L2(d dx), integral correction, and primitive convergence. Thus expanding natural-endpoint responses converge to the smooth-test whole-line response, also for bounded source/reaction weights tending locally to one and converging centers. Asymmetric intervals with both endpoints tending to infinity are handled by the same argument. No general finite endpoint traces are assumed for a degenerate profile.

For any unit-mass near-minimizer d, regularize as (d+epsilon rho)/(1+epsilon), with rho a normalized graded tail of the preceding type. This preserves unit mass and the center width, supplies a positive background, and has response at most (1+epsilon) times that of d, by quadratic-form comparison. No unknown continuity in a mass-dilated center width is needed.

Lower semicontinuity of Fcenter under eta_n→eta follows by vague compactness of near-minimizing densities, the joint compact-test liminf in eta and measure, singular removal, and filling any missing mass. Upper semicontinuity follows by fixing a regularized near-minimizer at eta and using continuity of its shifted responses on compact center sets, then sending its approximation error to zero. Shift continuity can be verified directly: the difference of quadratic potentials is controlled by C|u-v|(1+x²), and the fixed-background anchored forms control this weighted L2 norm uniformly on compact center sets. This also handles eta=0 by writing the average on the fixed z interval. It does not assume monotonicity of uniform uncertainty intervals of nonnested lengths.

## Exact-coordinate recovery for regular bins

For one fixed physical root interval contained strictly in (0,pi), use

x=(-cos(s)−c0)/(sqrt(a)ell), ds=ell w(x)dx, w=sqrt(a)/sin(s).

The metric is uniformly bounded above and below on a compact regular offset set and converges locally to one. At c=c0+sqrt(a)ell u the kinetic potential is exactly a ell²(x−u)². Choosing D(s)=a ell⁴ w(x)d(x) makes the derivative energy canonical; source and reaction retain metric w. The physical mass is m integral w²d over an expanding interval, tending to m for fixed integrable d. Reflect the field on the other half, and multiply the full field by a factor tending to one to restore the exact total budget. This normalization changes every response by uniformly comparable factors tending to one.

The weighted natural-endpoint lemma gives local recovery uniformly for compact centers. Outside the two fixed root intervals the potential is uniformly positive for these bins, so its reciprocal contribution is O(1). All possible roots remain in the retained intervals. Thus a fixed regularized near-minimizer at a limiting eta provides the matching conditional upper bound for every convergent sequence of regular bin midpoints and finite eta. A subsequence contradiction then gives the uniform conditional equivalent on compact regular offset sets. Finite bins require only finitely many near-minimizer choices, not a measurable selection over a continuum of designs.

## Global integration and endpoint separation

For Delta/M^(1/5)→tau<infinity, the uniform regular-bin equivalent and continuity of Fcenter give Riemann sums with integrand

(2^(6/5)/4) a^(-4/5) Fcenter(2^(1/5)tau a^(-3/10)).

The local order Fcenter(eta)≤C(1+eta^(1/4)) makes this integrand bounded by C[a^(-4/5)+tau^(1/4)a^(-7/8)], integrable at both folds. The earlier constructive regular-bin bound has exactly these two powers, permitting the omitted fixed fold neighborhoods to shrink after the limit.

The union of fold bins has parameter width O(W), W=Delta+M^(2/7), and a common patch gives integrated cost at most C M^(-1/4)W^(3/8). Relative to M^(-1/5)+M^(-1/4)Delta^(1/4), this is bounded by quantities tending to zero: C[M^(2/35)+Delta^(1/8)]. This is uniform in the relative rate, and the rootless exterior is absorbed in the same estimate. Thus folds cannot add a missing contribution to the finite-ratio coefficient.

The finite-ratio localization theorem does not itself justify sending eta to infinity jointly with the budget. The sharp coarse endpoint still requires its separate uniform harmonic moving-root lower certificate and padded-arc recovery, as in the source review. That proof gives conditional coefficient 2^(5/4)C0 a^(-7/8) M^(-1/4)Delta^(1/4), and global coefficient 2^(-3/4)C0 B(1/2,1/8). Matching endpoint values of the finite-tau integral are a consistency check after both theorems are proved, not a substitute for either proof.

## Source audit and numerical constants

Read the complete authored section06 before freeze. The additional attainment claim for the local uncertain-center problem is justified: vague compactness and Fatou give a relaxed minimizer of mass at most one; singular removal and adding missing absolutely continuous mass give an admissible unit-mass minimizer with no larger cost. Strict decrease with mass is unnecessary. Re-read the singular-removal construction in section03; it uses common compact support, derivative flattening, an integral correction, and uniformly converging primitives, so the change from quartic to shifted quadratic potential is valid.

An independent 60-digit mpmath evaluation is saved in `coordinator-sanity-checks.json`. It gives Kobs = 22.4046282307491383 and Kcoarse = 25.7238273887632910. This is an arithmetic check, not a numerical proof of the crossover.

Primary contextual sources opened on 2026-09-07: Yüksel and Linder, https://arxiv.org/abs/1009.3824 (v2, 2012; full PDF introduction and setup inspected), and Saldi, Yüksel and Linder, https://arxiv.org/abs/1511.04657 (v2, 2016; abstract and metadata inspected). General optimization of observation channels and asymptotic optimality of quantized policies are established frameworks. No claim is made here that their general theorems directly cover this singular unbounded-cost design problem, and no framework-level novelty should be asserted in the synthesis.

Additional openly indexed searches on 2026-09-07 used the query strings `"optimal" "diffusivity" "uncertain" "location" transport design`, `"mobility" "quantization" "optimal" transport surface reaction`, `"optimal reinforcement" "uncertain" "location" reaction diffusion`, and `"finite precision" "surface diffusion" optimization`. Returned leads mainly concerned inverse estimation, communications, quantum transport, or reinforcement learning, and did not identify a direct counterpart of the present conditional singular-design theorem. This negative keyword search is limited evidence, not proof of novelty.

Frozen Stage06 was independently force-built with latexmk -g: 45 pages, no final log warnings, undefined references or overfull/underfull boxes. Explicit scans of authored source/text found no control-byte or trailing-whitespace issues; all manifest hashes remained unchanged. Sample PDF page39 was visually inspected.
