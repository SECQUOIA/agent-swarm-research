# Generic kinetic folds give the same optimized moment threshold

Research note, 2026-09-07. This extends the scalar order theorem in [risk-sensitive-mobility.md](risk-sensitive-mobility.md) beyond the cosine-offset ensemble. The proof identifies sufficient geometric assumptions and does not claim sharp coefficients. The scalar theorem and finite-bulk order corollary have passed [independent review](review-generic-kinetic-folds.md).

## Statement and assumptions

Let Γ be a smooth compact connected one-dimensional wall without boundary, parametrized by arclength s. Let c range over a compact interval I, with probability density p. Set

\[
 k_c(s)=g(s,c)^2,\qquad g\in C^4(\Gamma\times I).
\]

Assume the following.

1. The multiple-zero set `{(s,c):g=g_s=0}` consists of a nonempty finite collection `(s_j,c_j)`. Every c_j is in the interior of I, and every point is a transverse fold:
   \[
   g_{ss}(s_j,c_j)\ne0,\qquad g_c(s_j,c_j)\ne0.
   \]
   All other zeros of g are simple in s. Thus there are no higher spatial degeneracies, zero intervals, or identically zero realizations.
2. For a clean statement, the fold sites s_j are pairwise distinct and the fold parameters c_j are pairwise distinct. Choose disjoint fixed neighborhoods of the sites and parameters. Simultaneous or spatially coincident folds are outside this statement; the proof does not need them to obtain a nonempty class of general families.
3. The density is bounded above on I. In a two-sided neighborhood of every c_j it is bounded below by a strictly positive number. In particular, the side on which the fold produces two roots has positive probability. Continuity and positivity at each fold are sufficient. Positivity on unrelated regular-root parameter intervals is not needed.

Compactness gives a uniform lower bound on `∫Γ k_c`, a finite uniform bound on the number of spatial roots, and a uniform positive lower bound on `|g_s|` at zeros outside retained fold neighborhoods. A parameter derivative g_c may vanish at an ordinary simple root; no motion assumption is imposed on such roots.

For arbitrary `D∈L¹(Γ)`, `D≥0`, define the scalar response by smooth tests,

\[
 J_c(D)=\sup_{f\in C^\infty(\Gamma)}
 \left\{2\int_\Gamma f-\int_\Gamma[D|f'|^2+k_cf^2]\right\}\in[0,\infty].
\]

Use fixed nondimensional units for the asymptotic powers and logarithms. A single D is chosen before observing c. For each fixed q>0, let

\[
 \Phi_q(M)=\inf_{D\ge0,\ \int D=M}\int_I J_c(D)^q p(c)\,dc.
\]

**Theorem (scalar order bounds).** Under assumptions 1–3, as M tends to zero,

\[
 \boxed{\Phi_q(M)\asymp
 \begin{cases}
 M^{-q/4},&0<q<8/5,\\
 M^{-2/5}[\log(1/M)]^{7/5},&q=8/5,\\
 M^{(2-3q)/7},&q>8/5.
 \end{cases}}
 \tag{1}
\]

The comparison constants can depend on the family, wall, density and fixed q, but not on M or on an admissible competitor. Hence the threshold 8/5 and critical logarithm follow from transverse fold geometry and the shared mobility budget, rather than the exact cosine profile or equal paired-root weights. These are unrooted moments; taking the qth root divides all powers by q.

The response definition makes the lower bounds valid even when an irregular coefficient has not been assigned a diffusion generator. Every upper-bound design used below is bounded and strictly positive for fixed M, so its ordinary periodic H¹ energy form is unambiguous. A finite-bulk order extension follows from the general positive-background lemma, as stated below.

## Local geometry needed in the proof

Near a fold, the parameter-dependent Morse lemma gives a smooth spatial coordinate x, with Jacobian bounded above and below, in which

\[
 g(s,c)=h(c)+\sigma x(s,c)^2,\qquad \sigma\in\{-1,1\},
 \quad h(c_j)=0,\quad h'(c_j)\ne0.
 \tag{2}
\]

The critical-point center moves by `O(|c−c_j|)` from s_j. Absorb fixed constants and signs into a signed parameter t comparable to c−c_j. On the root side, the two roots have distance comparable to `r=√|t|` from s_j, separation comparable to r, and slopes `|g_s|` comparable to r. On neighborhoods of either root u of radius a sufficiently small fixed multiple of r,

\[
 c_1r^2(s-u)^2\le k_c(s)\le c_2r^2(s-u)^2.
 \tag{3}
\]

The root branch can also be parametrized by its arclength position u: implicit differentiation with respect to c gives `c=C(u)`, with `|C'(u)|` comparable to `|u−s_j|`. The probability of roots in an interval of length comparable to r at distance r from the site is therefore comparable to r². The density hypothesis is used here.

On the rootless side, the local potential is comparable to `(t+(s−s_j)^2)^2` after a bounded coordinate change; its reciprocal integral is `O(|t|^(−3/2))`. Away from the fold neighborhoods, ordinary quadratic-zero comparisons and fixed positive-potential regions cover the wall with uniformly bounded multiplicity. This follows from the compact zero set and assumption 1.

## Lower bounds independent of the mobility shape

The amplitude-optimized variational formula is

\[
 J_c(D)=\sup_{f:\int f\ne0}
 \frac{(\int f)^2}{\int[D|f'|^2+k_cf^2]}.
 \tag{4}
\]

Fix one fold and one of its moving root branches. Use local arclength with fold site zero. For root positions u in `[r,3r/2]`, take a fixed spatial enlargement of this interval and let m denote the actual mobility mass there. Suppose `0<m≤c_*r^7`. For a fixed smooth nonnegative compact bump ψ and sufficiently small fixed κ, set

\[
 \ell=\kappa(m/r^3)^{1/4},\qquad f_u(s)=\psi((s-u)/\ell).
\]

The condition on m ensures that all bump supports lie inside the enlargement and inside the root neighborhood where (3) holds. The source integral is proportional to ℓ, and reaction energy is at most `Cr²ℓ³`. If

\[
 B(u)=\ell^{-2}\int D(s)|\psi'((s-u)/\ell)|^2ds,
\]

Fubini gives the moving-root average bound

\[
 \frac1r\int_r^{3r/2}B(u)du\le\frac{Cm}{r\ell}.
\]

Since the parameter density in u is bounded below by a positive constant times r, Jensen's inequality for `(x+b)^(−q)` and (4) imply

\[
 \boxed{\mathbb E[J_c(D)^q;\ u\in[r,3r/2]]
 \ge c_q r^{2-5q/4}m^{-q/4}.}
 \tag{5}
\]

This uses only total local mass. No continuity, minimum feature size, or pointwise lower bound on D is required. If m=0, shrinking bumps show an infinite response for almost every retained root position.

For q<8/5, fix one small r independent of M. Its local mass is at most M; (5) gives the lower bound `c_qM^(−q/4)`.

For q=8/5, choose geometric radii r_n tending to zero, with disjoint spatial enlargements and disjoint parameter images under C. Retain radii above a large constant times `M^(1/7)`. There are N comparable to `log(1/M)` such shells, and each satisfies the small-mass condition since `m_n≤M`. Summing (5), then using `Σm_n≤M`, yields

\[
 \mathbb E J_c(D)^{8/5}\ge c\sum_{n=1}^N m_n^{-2/5}
 \ge c N^{7/5}M^{-2/5}.
 \tag{6}
\]

For q>8/5, set `R=M^(1/7)` and place a single fixed-shape bump of width R at the fold. On `|c−c_j|≤cR²`, Taylor's theorem gives `k_c≤CR⁴` on its support. The quotient is at least

\[
 c\frac{R^2}{M/R^2+R^5}=cR^{-3}.
\]

This parameter window has probability at least a constant times R², giving `c_qM^((2−3q)/7)`. Other zeros of the same realization cannot weaken any of these lower tests.

## Graded designs and a uniform upper bound

Let ρ(s) be arclength distance to the finite set of known fold sites. Choose

\[
 \alpha=\max\left\{0,\frac{6q-4}{q+4}\right\},\qquad
 D_M(s)=A(\rho(s)+R)^{-\alpha},\qquad
 A=\frac{M}{\int_\Gamma(\rho+R)^{-\alpha}}.
 \tag{7}
\]

Set

\[
 R=\begin{cases}
 M^{1/(6+\alpha)},&q<8/5,\\
 [M/\log(1/M)]^{1/7},&q=8/5,\\
 M^{1/7},&q>8/5.
 \end{cases}
 \tag{8}
\]

Then

\[
 A\asymp\begin{cases}M,&\alpha<1,\\
 M/\log(1/M),&\alpha=1,\\
 MR^{\alpha-1},&\alpha>1,
 \end{cases}
 \qquad A\asymp R^{\alpha+6}.
 \tag{9}
\]

The choice α=0 for q≤2/3 is deliberate. A generic ordinary root could remain fixed at a fold site belonging to a different parameter value; a negative grading exponent would unnecessarily suppress mobility there. Taking α nonnegative ensures `D_M≥cA` everywhere, while retaining all orders in (1). The claim is about order-optimal trials, not sharp shapes.

Near a given fold on its root side, for `r=√|t|≥CR`, a root neighborhood of width proportional to r has mobility comparable to `Ar^(−α)` and potential comparable to `r²(s-u)²`. Neumann bracketing and a uniform interval harmonic-oscillator estimate give its response at most

\[
 C A^{-1/4}r^{-3/2+\alpha/4}.
 \tag{10}
\]

The oscillator length is small compared with r because `A≍R^(α+6)` and r≥CR. The remainder of the local fold neighborhood contributes at most `Cr^(−3)` by reciprocal-potential integration. That contribution is bounded by (10), since their ratio is at most a constant times `(R/r)^((α+6)/4)`.

For `|t|≤CR²`, bracket an interval of radius KR around s_j, with K sufficiently large. There `D_M≍R⁶`. Rescaling space by R gives a uniformly elliptic derivative coefficient and a compact family of quartic potentials with operator scale R⁴. The corresponding Neumann forms are uniformly coercive: a zero-energy field would have to be constant and annihilated by a nonzero quadratic-square potential. Compactness then excludes eigenvalues tending to zero. The integrated inverse response is at most `CR^(−3)`. The complementary local reciprocal-potential integral has the same bound.

On the rootless side with `|t|≥CR²`, the local fold contribution is at most `C|t|^(−3/2)` by (2). All other ordinary roots together contribute at most `CA^(−1/4)` because `D_M≥cA`, their slopes are uniformly nonzero, and their number is bounded. Fixed positive-potential regions contribute only a constant. These regular contributions must be retained if a realization has ordinary roots in addition to the unfolding fold.

For a fixed q>0, a finite sum of nonnegative responses raised to q is at most a constant depending on q and the number of pieces times the sum of their qth powers. Distinct fold parameter neighborhoods therefore allow the above estimates to be integrated separately. The root-side integral that controls the transition is

\[
 C A^{-q/4}\int_R^{r_*}
 r^{1-3q/2+\alpha q/4}dr.
 \tag{11}
\]

For q>2/3, write

\[
 e=2-3q/2+\alpha q/4=\frac{8-5q}{q+4}.
\]

If q<8/5, e>0, so (11) is at most `CM^(−q/4)`. For q≤2/3, α=0 and e=2−3q/2>0, yielding the same bound. The fold-window and rootless-side terms are smaller or bounded; a possible rootless logarithm at q=2/3 is also smaller.

At q=8/5, α=1 and e=0. Equation (11) is `CA^(−2/5)log(1/R)`, which equals the critical order in (1). The central window contributes only `CR^(−14/5)`, one logarithmic factor smaller.

For q>8/5, e<0 and the lower endpoint controls (11). Equations (9) and (11) give `CA^(−q/4)R^e≍R^(2−3q)`. The central and rootless terms have at most that order. The regular contribution `A^(−q/4)` is smaller because e<0. This proves all matching upper bounds.

## Finite transverse bulk diffusion preserves these orders

The general lemma in [review-risk-sensitive-finite-bulk.md](review-risk-sensitive-finite-bulk.md) applies without the cosine structure. For a fixed one-dimensional wall, it states that

\[
 0\le k\le K_0,\quad\int k\ge\kappa>0,\quad D\ge m>0
 \quad\Longrightarrow\quad
 0\le R(D,k)\le C[1+\log(1/m)]
 \tag{12}
\]

in the exact finite-response decomposition `D_flow=BJ+R`, in fixed units with m≤1. Here the bulk domain and positive transverse bulk diffusivity are fixed, affinity K>0 is constant, `Z=A_bulk+KP`, `V=∫u/Z`, and `B=KV²/Z`. The velocity is in L², and the domain has the usual H¹-to-H¹/² trace bound. The logarithm contains a fixed reference mobility if dimensional units are retained. The constants depend on the fixed bulk data and `K_0,κ`, but not on mobility derivatives.

The present compact kinetic family has the required uniform bounds. For (7), α≥0 gives `m_M≍A`, so `log(1/m_M)=O_q(log(1/M))`. Thus the graded designs satisfy (12) uniformly in c. If V≠0, define the optimized full-bulk moment over admissible energy-form designs, allowing an infinite response,

\[
 \widetilde\Phi_q(M)=\inf_{\int D=M}\mathbb E[D_{\rm flow}(D,c)^q].
\]

The smooth-test lower bound `D_flow≥BJ` applies even when a competing coefficient lacks a finite surface inverse. It yields the same lower orders as (1). On the explicit positive designs, the Schur identity and (12) give

\[
 \mathbb E D_{\rm flow}^q\le C_q\left[
 B^q\mathbb E J_c(D_M)^q+(1+\log(1/M))^q\right].
\]

Every scalar scale in (1) diverges as a negative power of M, so the added logarithmic term is smaller. Consequently **the three orders in (1) also hold for \(\widetilde\Phi_q\)** at fixed nonzero V and fixed positive bulk diffusivity. A fixed molecular contribution or the isotropic axial surface term `(K/Z)M` does not change the orders.

The subsequently reviewed [same-budget transfer theorem](scalar-to-bulk-design-transfer.md) strengthens the comparison to

\[
 \widetilde\Phi_q(M)\sim B^q\Phi_q(M).
\]

Indeed, mix an arbitrary near-optimal scalar coefficient with a vanishing uniform background, `D^θ=(1−θ)D+θM/P`. This keeps its budget and information, gives `J(D^θ)≤J(D)/(1−θ)`, and makes the bulk remainder logarithmic. Every scalar order in (1) dominates that logarithmic moment. This identifies the ratio of full and scalar optimal values, but supplies no unknown generic scalar coefficient.

This transfer does not assert a bounded or convergent bulk remainder, a sharp generic scalar moment coefficient, or uniformity as bulk diffusivity vanishes. At V=0, B=0 and the singular lower bound disappears. The Fourier estimate behind (12) uses the one-dimensional wall; it should not be transferred to a higher-dimensional surface without a separate argument.

## Scope, failure modes, and interpretation

Only one positively sampled interior fold is needed for all lower bounds; the graded trial protects every possible fold site for the upper bound. The result tolerates asymmetry, unequal root slopes, extra regular roots, and roots that move nonmonotonically away from folds. Those features affect constants. Equal paired-root weights and ensemble symmetries are unnecessary at the level of orders and cannot be assumed when seeking a generic sharp coefficient.

The fold and sampling assumptions matter. If there are no folds, the threshold need not occur. A parameter law supported only on the rootless side removes the moving-root shell lower bound. A density vanishing or diverging at the fold changes the scale probabilities. Higher-order spatial degeneracies, a failure of g_c≠0, or realizations whose entire reaction profile approaches zero require different estimates. The statement also assumes the designer knows the fixed fold sites; uncertainty in those sites is a different information structure.

The admissible class has no pointwise upper mobility cap, prescribed positive background, or fixed spatial resolution. Such constraints can alter the small-budget laws. The theorem establishes matching orders and explicit achieving designs, not exact finite-budget optimizers, sharp coefficients, or convergence of every optimizing sequence. The full-bulk extension concerns fixed positive bulk diffusivity and nonzero mean drift; its correction estimate is deliberately only logarithmic.

The general ingredients are established: the Morse normal form, variational compliance, fixed-budget reinforcement, and rare-degeneracy moment selection. Prior-art boundaries are documented in [risk-sensitive-prior-art.md](risk-sensitive-prior-art.md), including [Buttazzo, Oudet and Velichkov](https://arxiv.org/abs/1506.00141) for reinforcement and [Berry, Keating and Schomerus](https://doi.org/10.1098/rspa.2000.0580) for bifurcation-dominated moments. The candidate transport contribution is that spatial mobility design changes the generic quadratic-fold moment threshold to 8/5, with a budget-sharing logarithm of power 7/5. This is an extension of the repository theorem, not a claim that its general mathematical ingredients are new.
