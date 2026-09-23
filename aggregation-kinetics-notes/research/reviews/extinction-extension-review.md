# Independent review of near-critical extinction extensions

Date: 2026-09-06. Reviewed [extinction-near-critical.md](../results/extinction-near-critical.md) and [extinction-perron-ties.md](../results/extinction-perron-ties.md) as present during this review. The reviewer did not author either theorem note and did not edit them.

**Verdict:** both proofs are correct under their stated finite-type, irreducibility, fixed-marginal, binary-offspring, and division-scaling assumptions. I found no substantive error in the explicit quadratic remainder constant, uniform cubic expansion, or exact optimizer argument. The tie example also passes independent exact arithmetic checks. Correctness does not establish novelty or likely publication impact.

## First note: uniform expansion and constants

The survival map sends the unit cube to itself: each daughter-pair term x_j+x_k−x_jx_k lies in [0,1]. It is monotone on that cube. A sufficiently small positive multiple of v is a subsolution for every positive parameter, so the greatest fixed point is strictly positive. This justifies all subsequent divisions by the positive projected amplitude.

Irreducibility of M_0 and positivity of b_i^0 give the required paths in P. The estimate x_i≥b_i^0∑_jp_ijx_j is valid because the exact survival term is at least half the sum of the two daughter survival coordinates. Following each chosen path gives min x≥c max x. Since w is a probability vector, the stated weaker estimates cs≤x_i≤s/c are correct for s=wᵀx.

The exact projection is ts=(1+t)wᵀB_C(x,x). The preceding bounds give βc²s²≤wᵀB_C(x,x)≤βs²/c², which yields equation (5) with its displayed factors of (1+t). The upper bound ||x||∞≤At with A=1/(βc³) and lower bound s≥at with a=c²/((1+t_0)β) both follow.

The reduced inverse is well defined. For an irreducible matrix with Perron root 1, that eigenvalue is algebraically simple. Other peripheral eigenvalues in a periodic matrix cause no obstruction to inversion of I−M_0 on w⊥. The operator in the displayed definition of L represents that inverse followed by projection. Applying it to the exact equation gives the stated K_y.

The projected remainder satisfies

\[
 \left|t-(1+t)D_Cs\right|
 \leq (1+t_0)\beta
 \left[2\|v\|_\infty K_y+
 \frac{K_y^2t_0}{a}\right]t^2.
\]

The final term is correct: ||y||²/s≤K_y²t³/a, which is at most K_y²t_0t²/a. Writing the left side as a residual R gives

\[
 s-\frac{t}{D_C}
 =-\frac{R+t^2}{(1+t)D_C}
\]

with the sign of R depending on its definition; in either convention the magnitude is bounded by (K_p+1)t²/D_lo. Consequently the displayed E is valid on the entire chosen probability interval. These constants may be very conservative but they are finite and independent of C. The m=1 formulas remain valid with L=K_y=K_p=0.

The first-order extrema follow from rearrangement and the uniform estimate even when the exact optimizing policy depends on t. The sandwich argument is sound. For distinct v coordinates, the lower bound tδ/D_hi−2Et² has the correct direction and denominator. The strict interval in Theorem 3 makes the ordering argument valid. Evaluating the fixed antithetic law at the attained lower extinction envelope and using leastness then proves exact optimality, without requiring uniqueness of a fixed point or a policy.

## Second note: expansion and tied ordering

Let ε be the parameter, t=uᵀs_C, and y=s_C−tv. The uniform first-order expansion inserted into the reduced equation gives

\[
 (I-M)y=\epsilon^2(a_Cv-a_C^2H_C)+O(\epsilon^3).
\]

Its leading right side has zero u projection, so equation (2) is solvable with the stated normalization and y=ε²r_C+O(ε³) uniformly. This argument only uses bounded bilinear coefficients and the fixed inverse; no differentiation of an ε-dependent optimizer is required.

The exact divided projection is

\[
 D_Ct=\frac{\epsilon}{1+\epsilon}
 -2u^TB_C(v,y)-\frac{u^TB_C(y,y)}{t}.
\]

Here ||y||=O(ε²) and t is bounded below by a positive multiple of ε, so the quotient is O(ε³). Expansion therefore gives exactly c_C=−a_C−2a_CuᵀB_C(v,r_C). In particular the factor a_C and the sign in equation (3) are correct.

The exact optimizer proof handles a subtle point correctly. A generic sequence of nearly minimizing D_C values need not lie on the first-order optimal face. Instead the proof chooses an exact antithetic optimizer at each attained extinction-envelope vector. For small ε its order refines the order of v. Its pushforward onto the scalar v values is consequently countermonotonic, so each row attains H_i* exactly. The choice within tied v groups does not change that row objective. Hence H_C=H*, D_C=D*, and r_C=r* for these selected optimizers.

For coordinates sharing v_j=v_k, the leading term and c_Cv term cancel. The difference is ε²(r_j*−r_k*)+O(ε³) with a uniform error. The distinct-pairs condition gives a positive minimum gap among each finite set of tied pairs. This proves the claimed strict lexicographic order and supplies the same fixed antithetic coupling for every sufficiently small ε. The final least-fixed-point attainment argument is valid. No unsupported exchange of optimization and asymptotic expansion is needed.

## Constructive cubic remainder derived during review

The qualitative uniform cubic remainder can also be bounded using the first note's constants. This is a supplementary reviewer calculation, not a required correction. The author or another reviewer should check it before adopting it as a theorem statement.

Use the first note's β,b_*,A,L,E,K_y,D_lo,D_hi and interval endpoint t_0. Rename its positive projected-amplitude lower constant as a_lo to distinguish it from a_C. Put V=||v||∞ and α=1/D_lo. Define

\[
 K_{y,3}=L\left[
 \|M\|_\infty E+2b_*\alpha VE+
 b_*E^2t_0+b_*A^2\right].
\]

Writing e=s_C−εa_Cv with ||e||≤Eε² in the exact reduced equation bounds its remainder by the four terms inside the brackets, respectively from εMe, the bilinear cross term, B_C(e,e), and εB_C(s_C,s_C). Thus

\[
 \|y-\epsilon^2r_C\|_\infty\leq K_{y,3}\epsilon^3.
\]

The divided projection and identity ε/(1+ε)=ε−ε²+ε³/(1+ε) then give

\[
 K_{t,3}=\frac{1+2\beta V K_{y,3}+\beta K_y^2/a_{\rm lo}}{D_{\rm lo}},
 \qquad K_3=K_{y,3}+VK_{t,3},
\]

\[
 \|s_C-\epsilon a_Cv-\epsilon^2(r_C+c_Cv)\|_\infty
 \leq K_3\epsilon^3.
\]

Let δ_v be the minimum gap between unequal v coordinates, when such pairs exist, and δ_r the minimum |r_j*−r_k*| over pairs with equal v, when such pairs exist. Under the theorem's distinct-pairs condition, these gaps are positive whenever defined. A sufficient strict interval for its ordering argument is

\[
 0<\epsilon<\min\left\{
 t_0,\frac{\delta_v}{2ED_{\rm hi}},\frac{\delta_r}{2K_3}
 \right\},
\]

omitting an empty-pair restriction or a restriction with zero error constant. This bound can be extremely small; it is a certificate, not a prediction of the actual policy-switching threshold.

## Independent exact example check

Using a separately written SymPy calculation with rational arithmetic, I checked Mv=v, uᵀM=uᵀ, both Perron normalizations, symmetry and row marginals of all three displayed coupling matrices, and equations (2)–(3). The exact values are

\[
 H^*=\left(\frac{384}{1331},\frac{288}{847},\frac{256}{363}\right),
 \quad D^*=\frac{56}{121},
 \quad r^*=\frac1{343}(138,-27,-76),
\]

\[
 c_{C^*}=-\frac{5258}{2401},\qquad
 r^*+c_{C^*}v=\frac1{2401}(-2858,-4013,-8180).
\]

The first tied-coordinate difference is 165/343>0, so the displayed zero-based ordering (1,0,2) is correct. This exact check supports the example and coefficient algebra. I did not treat the existing floating-point fixed-point comparisons as rigorous extinction certificates; the source note already states that limitation correctly.

## Novelty assessment, separate from proof approval

The basic first-order asymptotic, antithetic transport, BMDP stationary attainment, and abstract eventual policy stabilization are not credible standalone novelty claims. The sources and reduction are recorded in [the literature critique](extinction-literature.md), including [Athreya's multitype asymptotic paper](https://link.springer.com/article/10.1007/BF00160373), [Eshel's earlier result](https://link.springer.com/article/10.1007/BF00277746), and the [BMDP accepted manuscript](https://www.pure.ed.ac.uk/ws/portalfiles/portal/68952841/Polynomial_Time_Algorithms_for.pdf).

The explicit tied-order theorem is not supplied by those sources as inspected. Its distinctive part is that the rowwise minimum H* fixes a common transverse second-order correction r* across the relevant first-order optimal face, which in turn resolves the exact transport policy. A generic second-order branching expansion does not itself identify this policy. Generic semialgebraic policy stabilization likewise does not provide the explicit Poisson-equation ordering.

Additional targeted searches combined branching extinction with second-order expansion, multitype survival with higher-order terms, branching with lexicographic optimality, and reproductive value with Poisson equation. They produced no directly matching primary theorem. This supports describing the result as a plausible unreported explicit consequence with a verified proof. It does **not** justify claiming an established absence of prior work, a major new general theory, or high citation impact. The formula uses familiar perturbation and transport tools, and a reviewer may reasonably regard it as a useful specialized corollary. A concrete population-balance application or substantially sharper usable certificates would strengthen its case.
