# Audit of the discrete and statistical results

Scope: the corrected sparse-regression, stronger-relaxations, binary-least-squares, integer-core and PWE notes, together with their proof reviews and corrected closeouts. This report owns no source note. No literature search, experiment rerun, project-wide verification or CI inspection was performed. The mathematical arguments below are independent proof review and development; archival computations retain their original provenance.

## New complete proof: sign-orbit invariance and square-node inactivity

This development removes the Hu–Lu input from the sharp square-system C1 converse and proves the stronger square-system node-inactivity conjecture in the binary note. It requires an independent fresh proof review before use in the manuscript.

### Sign-orbit identity

Let C have n columns in R^M with n <= M, and let v be independent of C. Assume the joint column law is invariant under independently changing any column sign. Assume C has full column rank almost surely and that v is in general position relative to its column spans, almost surely. Let u^o minimize ||v + C u||^2 over u >= 0, and let S(C,v) = {j : u^o_j > 0}. For a fixed subset S, let E_S(C,v) be any measurable event invariant under every independent column sign change. Then

\[
\Pr\{S(C,v)=S,\ E_S(C,v)\}=2^{-n}\Pr\{E_S(C,v)\}. \tag{SO}
\]

Proof. For fixed C and v, put L_S = span(C_S). The NNLS support is S if and only if the coordinates of -P_{L_S}v in the basis C_S are positive and c_j^T P_{L_S}^{\perp}v > 0 for j outside S. Under independent sign changes of C, the spans stay fixed. Exactly one sign choice on S makes all those coordinates positive, and exactly one choice on the complement makes all the residual inner products positive. General position excludes zero coordinates and zero residual inner products when a complement exists. Thus exactly one of the 2^n sign patterns selects S. Since E_S is invariant, summing the indicator of the intersection over all sign patterns gives the indicator of E_S. Taking expectations and using invariance of the law gives (SO). For the empty or full support, the absent conditions are vacuous. This proves the identity, not just the marginal uniform-support law.

Examples of events allowed in (SO) are bounds on the singular values of C_S and on absolute coordinates of its ordinary least-squares coefficient vector. The identity does not assert independence of every feature of the selected columns: it applies precisely to events invariant under column sign changes.

### An exact finite-dimensional tail bound

Let C = a H with a > 0, H an M by n matrix of independent standard Gaussian entries, n <= M, and let v be independent N(0,c^2 I_M), c > 0. For every t > 0, put

\[
q=\left(1+\frac{a^2t^2}{c^2}\right)^{-1/2}.
\]

Then

\[
\Pr\{\max_j u^o_j>t\}
\le \frac n2\,q^{M-n+1}\left(\frac{1+q}{2}\right)^{n-1}. \tag{NT}
\]

Proof. For each nonempty S of size s, let d^S = -(C_S^T C_S)^{-1} C_S^T v. On the event that NNLS has support S, its positive coordinates equal d^S. The event max_{j in S}|d^S_j| > t is invariant under all column sign changes, since a sign change in S changes only the sign of its corresponding coefficient. Applying (SO) and then a union bound within each S gives

\[
\Pr\{\max_j u^o_j>t\}
\le 2^{-n}\sum_{s=1}^n {n\choose s}
\sum_{j\in S}\Pr\{|d^S_j|>t\}.
\]

For fixed S and j, let P project onto the orthogonal complement of span(H_{S minus j}), and let Q = ||P h_j||^2. Gaussian independence gives Q distributed as chi-square with M-s+1 degrees of freedom. The usual one-coordinate regression identity gives d^S_j = -h_j^T P v/(a Q). Conditional on H_S, this is N(0,c^2/(a^2 Q)). Consequently, using Pr{|Z| > z} <= exp(-z^2/2),

\[
\Pr\{|d^S_j|>t\}
\le \mathbb E\exp\left(-\frac{a^2t^2Q}{2c^2}\right)
=\left(1+\frac{a^2t^2}{c^2}\right)^{-(M-s+1)/2}
=q^{M-s+1}.
\]

Summing the binomial derivative gives

\[
2^{-n}\sum_{s=1}^n {n\choose s}s q^{M-s+1}
=\frac n2 q^{M-n+1}\left(\frac{1+q}{2}\right)^{n-1},
\]

which is (NT). Every fixed Gaussian submatrix has full column rank almost surely. The support size is exactly Bin(n,1/2) by (SO). Thus the support-rank mixture has been summed exactly; no estimate of a data-selected smallest singular value, asymptotic inverse-Wishart claim, or dependence assumption between node events is needed.

### Uniform inactivity at all single-wrong-fixing nodes

Use the binary note's exact model: H is M by N standard Gaussian, A = sqrt(rho/N) H, deterministic planted x* in {-1,1}^N, w independent N(0,I_M), and y=A x*+w. Let beta=M/N >= 1 and rho=theta N with theta>0 fixed. Signed columns b_i=x*_i a_i are independent N(0,theta I_M). At the node fixing x_i=-x*_i, its residual is v_i=w+2b_i, independent of the free columns B_{-i}, and exactly N(0,(1+4theta)I_M). In error coordinates its relaxation is

\[
r_i=\min_{u\in[0,2]^{N-1}}\|v_i+B_{-i}u\|^2.
\]

Apply (NT) with n=N-1, a^2=theta, c^2=1+4theta and t=2. Set

\[
q_\theta=\sqrt{\frac{1+4\theta}{1+8\theta}},\qquad
b_\theta=\frac{1+q_\theta}{2}<1.
\]

For each i, the NNLS minimizer violates an upper bound with probability at most

\[
\frac{N-1}{2}\,q_\theta^{M-N+2}b_\theta^{N-2}.
\]

Therefore the probability that at least one of the N nodes is box-active is at most

\[
\frac{N(N-1)}2\,q_\theta^{M-N+2}b_\theta^{N-2}. \tag{UN}
\]

This tends to zero exponentially for every fixed theta>0 and every M>=N. No independence between the N nodes is asserted or used. On the complementary event all node NNLS minimizers belong to [0,2]^{N-1}, so every node bound equals its orthant-relaxation value. Equality at an upper bound does not obstruct this conclusion; Gaussian continuous laws also make such equality a null event.

### Sharp C1, including all-node failure for square systems

Assume beta=M/N converges to a fixed beta>=1; rounding M to an integer is harmless. The Gaussian-cone projection law in the binary note, Theorem 1.3 and Lemma 0.2, gives

\[
r_i=\|v_i\|^2(1-Y_i),\qquad
\max_i\left|Y_i-\frac{N-1}{2M}\right|
=O_{\mathbb P}\!\left(\sqrt{\frac{\log N}{N}}\right).
\]

Here the equality holds simultaneously by (UN). For the concentration, Lemma 0.2 gives failure at most 6 exp(-M t^2/64) per node; choose t=sqrt(192 log N/M) and union bound over N nodes, for total failure at most 6N^{-2}. The projection law is used separately at each node because v_i is independent of its free columns.

Also W=||w||^2=beta N+o_P(N), all ||b_i||^2=theta beta N+o_P(N), and max_i|b_i^T w|=O_P(sqrt(N log N)). The last statement follows by conditioning on w; the signed column inner products are independent centered Gaussians with variance theta W. Gaussian norm tails and a union bound give the simultaneous column-norm statement. Hence, uniformly over i,

\[
\|v_i\|^2=W+4b_i^T w+4\|b_i\|^2
=\beta N(1+4\theta)+o_{\mathbb P}(N),
\]

and therefore

\[
\max_i\left|\frac{r_i-W}{N}-\left(2\theta(2\beta-1)-\frac12\right)\right|
\xrightarrow{\mathbb P}0. \tag{C1}
\]

The elementary ML achievability theorem in the binary note, Theorem 2.2(a), gives OPT=W with probability tending to one, since rho beta=theta beta N greatly exceeds log N. Put theta_c=1/[4(2beta-1)]. For fixed epsilon in (0,1), if theta >= (1+epsilon)theta_c, all single-wrong-fixing bounds are at least OPT+epsilon N/4 with probability tending to one. If theta <= (1-epsilon)theta_c, all are at most OPT-epsilon N/4 with probability tending to one. The upper side gives a unique planted optimum and the path lemma's at most 2N+1 nodes, with the optimal incumbent available at off-path nodes or strict C1 plus best-bound search. The lower side proves the all-node failure statement for beta=1 that the source note labels Conjecture 3.3, with no Hu–Lu input.

### Root inactivity without a box-decoder theorem

At the root take n=N, a^2=rho/N, c^2=1 and t=2 in (NT). With q=(1+4rho/N)^{-1/2},

\[
\Pr\{\max_j u^o_j>2\}
\le\frac N2 q^{M-N+1}\left(\frac{1+q}{2}\right)^{N-1}. \tag{RI}
\]

For rho=(1+epsilon)log N/(2beta-1) and fixed beta>=1, the logarithm of the right side is log(N/2)-(2beta-1)rho+o(1), so it tends to zero. For larger rho, root NNLS coefficients shrink exactly as rho^{-1/2} on the same H,w, so inactivity persists. This proves the source note's Hu–Lu-based sufficient root-inactivity bound directly, for square and tall systems, without its extra technical regime assumptions. It concerns equality of box and orthant values, not correctness of rounding and not root exactness at a vertex.

### Optional exact mixture and sharp root inactivity threshold

The sign-orbit identity also gives an exact coefficient distribution. Retain the Gaussian assumptions of (NT). For any nonempty fixed support S of size s, put nu=M-s+1. The ordinary least-squares vector d^S has density

\[
f_s(d)=\left(\frac ac\right)^s
\frac{\Gamma((M+1)/2)}{\pi^{s/2}\Gamma((M-s+1)/2)}
\left(1+\frac{a^2}{c^2}\|d\|^2\right)^{-(M+1)/2},
\qquad d\in\mathbb R^s. \tag{TD}
\]

Equivalently, d^S has the same distribution as (c/a)Z_s/sqrt(Q), where Z_s is a standard Gaussian vector in R^s and Q is an independent chi-square variable with nu degrees of freedom. This is a distributional representation; it does not identify these auxiliary variables with the selected design's singular values.

Here is a derivation that does not require an inverse-Wishart formula. Conditional on H_S, d^S is centered Gaussian with covariance (c^2/a^2)(H_S^T H_S)^{-1}, so its conditional density is

\[
\left(\frac ac\right)^s(2\pi)^{-s/2}
\det(H_S^TH_S)^{1/2}
\exp\!\left(-\frac{a^2}{2c^2}d^TH_S^TH_Sd\right).
\]

Multiply by the standard Gaussian density of the M by s matrix H_S and integrate over that matrix. For fixed d let T=I_s+(a^2/c^2)dd^T. Substitute H_S=G T^{-1/2}. The Jacobian on the M rows contributes det(T)^{-M/2}, and the determinant in the conditional density contributes det(T)^{-1/2}. The remaining integral is independent of d, so the density is proportional to det(T)^{-(M+1)/2}=(1+(a^2/c^2)||d||^2)^{-(M+1)/2}. Independently, integrating the joint density of Z_s and Q after the substitution Z_s=(a/c)sqrt(Q)d gives the density

\[
\frac{(a/c)^s}{2^{(\nu+s)/2}\pi^{s/2}\Gamma(\nu/2)}
\int_0^\infty q^{(\nu+s)/2-1}
\exp\!\left[-\frac q2\left(1+\frac{a^2}{c^2}\|d\|^2\right)\right]dq.
\]

The gamma integral and nu+s=M+1 give exactly (TD). Both densities integrate to one, so their proportionality constants agree. All integrals are finite: the Gaussian matrix integral contains only the square root of a Gram determinant.

For any Borel set D in [0,infinity)^s, the event {|d^S| in D} is invariant under column sign changes. Equation (SO), divided by P{support=S}=2^{-n}, therefore gives

\[
\mathcal L\big((u^o_j)_{j\in S}\mid S(C,v)=S\big)
=\mathcal L(|d^S|).
\]

Thus the positive coordinates conditional on a specified active support are the absolute values of the unconditional vector in (TD). In particular, an exact synthetic representation of max_j u^o_j is: sample K distributed as Bin(n,1/2); conditional on K=s>=1 sample independent Q distributed as chi-square with M-s+1 degrees of freedom and Z_s standard Gaussian; return (c/a)max_{j<=s}|Z_j|/sqrt(Q). Return zero when K=0. No independence across different branch-and-bound nodes follows from this representation. The resulting exact cumulative distribution function, for t>=0, is

\[
\Pr\{\max_j u^o_j\le t\}
=2^{-n}\sum_{s=0}^n{n\choose s}
\mathbb E_{Q\sim\chi^2_{M-s+1}}
\left[1-2\overline\Phi\!\left(\frac{at\sqrt Q}{c}\right)\right]^s,
\tag{EM}
\]

where the s=0 summand is one and overline(Phi) denotes the standard Gaussian upper-tail function. In particular, the atom at zero is exactly 2^{-n}.

For the sharp root threshold, let M_N>=N be integers with beta_N=M_N/N tending to a fixed beta>=1. Let H_N be M_N by N with independent standard Gaussian entries, w_N independent N(0,I_{M_N}), and A_N=sqrt(rho_N/N)H_N for an arbitrary deterministic sequence rho_N>0. The planted signs may be deterministic: sign absorption leaves the same Gaussian law. Define u_N^o(rho) as the unique minimizer of ||w_N+sqrt(rho/N)H_N u||^2 over u>=0, and define the random threshold

\[
\rho_{\mathrm{box},N}=\frac14\left(\max_j u_{N,j}^o(1)\right)^2.
\]

Then

\[
\frac{\rho_{\mathrm{box},N}}{\log N/(2\beta_N-1)}
\xrightarrow{\mathbb P}1. \tag{RT}
\]

Proof. At rho=1, the exact mixture has a^2=1/N and c^2=1. Conditional on K distributed as Bin(N,1/2), it gives

\[
\left(\max_j u_{N,j}^o(1)\right)^2
\ \stackrel{d}{=}\ \frac{N}{Q}\max_{j\le K}|Z_j|^2,
\qquad Q\mid K\sim\chi^2_{M_N-K+1},
\]

with conditional independence of Q and the Gaussian vector. Binomial concentration gives K/N tending to 1/2. On N/4<=K<=3N/4 the conditional degrees of freedom are at least N/4, so chi-square concentration, uniformly in K on this event, gives Q/N-(beta_N-1/2) tending to zero in probability. Finally max_{j<=K}|Z_j|^2/(2 log N) tends to one in probability. For completeness, for each fixed delta in (0,1) the upper Gaussian-tail union bound is at most 2N^{-delta} at squared level 2(1+delta)log N. For the lower bound, the elementary Gaussian-tail lower estimate gives

\[
\Pr\{|Z|>\sqrt{2(1-\delta)\log N}\}
\ge c_\delta\,N^{-(1-\delta)}/\sqrt{\log N}
\]

for all sufficiently large N. Conditional on K>=N/4, independence of the Gaussian coordinates bounds the probability that all are below this level by exp(-c_delta N^delta/(4 sqrt(log N))), which tends to zero. The excluded binomial event also has probability tending to zero. Combining these limits proves (RT).

Full column rank makes the objective strictly convex. Therefore the minimum over [0,2]^N equals the minimum over the nonnegative orthant if and only if its unique orthant minimizer lies in [0,2]^N. For a fixed H_N,w_N and rho>0, substituting sqrt(rho)u gives the exact identity u_N^o(rho)=rho^{-1/2}u_N^o(1). Consequently root equality with the orthant relaxation holds if and only if rho>=rho_box,N. For every fixed epsilon in (0,1), (RT) implies:

- If rho_N>=(1+epsilon)log N/(2beta_N-1) eventually, the root upper bounds are inactive with probability tending to one.
- If 0<rho_N<=(1-epsilon)log N/(2beta_N-1) eventually, the root upper bounds are active and its value strictly exceeds the orthant value with probability tending to one.

These are thresholds for equality of root box and orthant values. They do not claim correct rounding, recovery of the planted vector, an integral root optimum, or root exactness. The result holds for square systems as well as tall systems, uses unit-variance noise, and uses rho exactly as normalized by A_N=sqrt(rho_N/N)H_N. Noise with variance sigma^2 is reduced to these hypotheses by dividing the residual by sigma, so the effective parameter in this normalization is rho_N/sigma^2.

## Scope corrections required in the manuscript

1. **Sparse converses concern the planted support.** The source proves a root bound strictly below f(S*) and forced-in bounds strictly below f(S*). This establishes failure of global root exactness and C1 only when S* is optimal. Below the recovery regime it does not exclude exactness at a different optimal support. Call these planted-support certification thresholds, or retain the optimality condition in every converse. In the window 2-gamma < alpha < 2, the positive C1 theorem itself proves S* uniquely optimal, so the unconditional separation there is sound.
2. **A C1 upper bound needs an incumbent or node-order hypothesis.** The path proof requires OPT available when off-path nodes are examined. Strict C1 also works with best-bound search without an initial incumbent. Arbitrary depth-first search without an incumbent is not covered. Failure of C1 by itself is not a lower bound on tree size: the removal half alone gives a 2k+1-node sparse certificate.
3. **Root exactness is not literally impossible in binary least squares.** Exactness at the planted point has probability exactly 2^{-N}; global root exactness is bounded above by the displayed exponentially small bound. Replace phrases such as "never exact" by a probability statement. Correct rounding of the box solution is a different event.
4. **The matching binary complexity law needs its range stated carefully.** The proved lower bound is c_beta(N/rho)log rho - log(8N). It supports Theta((N/rho)log rho) for rho tending to infinity with rho=o(N), and exp(Theta(N)) for each fixed rho>=rho_0. It does not give that matching law throughout the larger source range rho<=c'_beta N: at beta=1, c'_1 is about 1.4e-4 while c_1 is about 1.8e-5, so the subtractive log(8N) can dominate at rho=c'_1 N. A smaller linear range also works, for example rho<=min(c'_beta,c_beta/8)N for all sufficiently large N. At arbitrary rho=theta N retain the polynomial upper bound and the stated, possibly vacuous polynomial lower bound.
5. **The local-hull hard theorem uses helpers that survive zero fixings.** Its convex-piece leaf bound uses the projected root-lifted L_2 function. It does not cover deletion of columns fixed to zero. The easy threshold theorem does cover such implementations because its upper comparisons are used only at the root and forced-in nodes, where no column is fixed to zero. Bounded coefficient models and big-M formulations also remove the unbounded recession mechanism and are outside the local-hull theorem.
6. **Cuts and tightening are different operations.** Cuts in the integer variables valid for every node integer point preserve the leaf lower bound. Incumbent reductions can remove feasible integer points, so they preserve only the augmented count: class number <= leaves + certified removals. For binaries this yields nodes >= class number/(N+1). For general integer variables, one pass gives /(2n+1); repeated passes require counting bound changes, with no dimension-only factor proved.
7. **CVP exponents at vanishing tolerance must retain that limit.** The rates 0.2075 and 0.2925 with o(1) loss follow when eps/GH^2 tends to zero. For fixed positive relative tolerance the source gives losses O(delta), with eps<=delta GH^2. Taking delta to zero while retaining a fixed positive eps/GH^2 is invalid. The Haar model and the uniform torus target are essential; Gaussian-basis lattices are not covered.
8. **No unconditional computational hardness follows from the sparse relaxation obstruction.** The obstruction applies to the specified convex lifts and node conventions. The low-degree detection conjecture, reductions to recovery, and transfer from binary signals to arbitrary signs are separate assumptions. They do not prove a universal polynomial-time recovery barrier at alpha=2 for fixed gamma>0. Variable branching counts also exclude the time spent solving node relaxations, probes, and generating cuts.
9. **Square SDP threshold N^3 is empirical.** The inspected note's data and heuristic cannot distinguish N^3 from N^2 times logarithmic factors. Tall-system SDP exactness at O(log N) is proved; its sufficient constant is not the sharp SDP constant. The uniform eigenvalue-shift threshold has a proved converse above the ML threshold.

Two small proof details should be repaired even though their statements are correct. In binary Theorem 2.2(c), bound the small-support sum by the binomial expression (1+exp(-0.148 beta rho))^N, rather than the looser exp(N exp(-0.148 beta rho)); only the former proves the displayed log(1+...) bound. In part (b), handle c>2 separately by ML achievability, which makes W-OPT zero with probability tending to one; the written bound involving an added log N does not imply a negative-power bound by itself. For c<=2 choose the truncation parameter small enough and absorb log N into N^delta.

The end of the integer note's asymmetric-gadget discussion says that incumbent tightening still requires 2^k leaves. That wording conflicts with its correctly stated earlier node bound. Retain 2^k leaves without incumbent reductions and 2^k/(2k+1) nodes with such reductions.

## Complete proof replacing the pairwise-hull hard-side sketch

This completes stronger-relaxations Corollary 4.6. Assume p tends to infinity, k tends to infinity, k/n tends to zero, lambda/n tends to zero, and x_p=(2/n)log binomial(p,k) tends to x in (0,x_0), where x_0 is the positive root of exp(-x)(1+2x)=1. In pure noise y is independent of X and nonzero almost surely. In the planted case use the same model as the sparse hard theorem, with ||beta*||^2/sigma^2 tending to kappa_s < exp(-x)(1+2x)-1.

First, log(p/k) tends to infinity and k log(p/k)=(x/2+o(1))n, by the elementary binomial bounds. Thus log(p/k)=o(n), log k=o(n), and log p=o(n). Writing t=p/k and a=n/k, t grows exponentially in a, whereas a tends to infinity, so p/n=t/a tends to infinity.

There is an event of probability tending to one on which all of the following hold simultaneously:

- lambda_min(XX^T)=p(1-o(1)), by the Gaussian smallest-singular-value bound with deviation sqrt(2 log p).
- max_j||x_j||^2=n(1+o(1)), by chi-square concentration with deviation parameter 3 log p and a union bound; here log p=o(n).
- max_{|U|<=2k}||X_U||^2=O(n). To prove this, pad U to size h=2k. For each h-subset the Gaussian largest-singular-value bound with deviation sqrt(4h log(ep/h)) fails with probability at most exp(-2h log(ep/h)). A union bound over at most exp(h log(ep/h)) subsets has failure at most exp(-h log(ep/h)), which tends to zero. The resulting bound (sqrt n+sqrt h+sqrt(4h log(ep/h)))^2 is O(n).

For every such U, take the helper set H_U=[p] minus U and W_U=X_{H_U}X_{H_U}^T. On this event,

\[
\lambda_{\min}(W_U)
\ge \lambda_{\min}(XX^T)-\|X_U\|^2=p(1-o(1)),
\]

uniformly in U. Consequently the deterministic completion lemma's quantities satisfy

\[
\vartheta_U=\|X_U^TW_U^{-1}X_U\|=O(n/p),\qquad
\max_{m\in H_U}x_m^TW_U^{-1}x_m=O(n/p).
\]

Use the pairwise weighted completion in stronger-relaxations Lemma 4.1(ii), with its slack parameter chosen as sqrt(n/p). Its objective inflation is bounded uniformly by a deterministic quantity e_p=O(sqrt(n/p)) tending to zero. This is a simultaneous deterministic consequence of the design event, so the data dependence of the top-correlated set, the code, U and its covariance causes no independence problem.

Take the sparse hard proof's family C' of k-subsets with pairwise differences at least ceil(mu k). For S,T in C', let z=(1_S+1_T)/2 and U=S union T. The two-point support mixture with marginals z gives the covariance required in the completion lemma for any beta supported on U. Because z takes only values 0, 1/2 and 1,

\[
\pi(z,\beta)\le\|\beta\|^2,
\]

so the root-lifted pairwise-hull value satisfies

\[
L_2(z)\le\|y-X_U\beta\|^2+(2+e_p)\lambda\|\beta\|^2.
\]

Put c_j=x_j^T(y/||y||), s_U=||c_U||^2, and beta=t c_U. Optimizing over t gives

\[
L_2(z)\le\|y\|^2\left[
1-\frac{s_U}{s_U+\|X_U^{\perp}c_U\|^2/s_U+(2+e_p)\lambda}
\right].
\]

This is exactly the sparse hard proof's midpoint upper bound with 2lambda replaced by (2+e_p)lambda. The new penalty is o(n). The code proof already gives, simultaneously over pairs, s_U >= (1+mu)(1-theta)xn(1+o(1)) and ||X_U^perp c_U||^2/s_U <= nB(1+o(1)), where B=1+2sqrt(c'x)+2c'x and the parameters obey

\[
\frac{(1+\mu)(1-\theta)x}{B}>e^x-1,
\qquad 0<c'<(1-\mu)\theta.
\]

The strict inequality leaves a positive margin. The same OPT lower bound, which concerns the integer problem and is unaffected by lifting, now gives L_2(z)<OPT-eta||y||^2 for a smaller fixed eta>0 in pure noise. In the planted case replace the margin scale by n sigma^2 and choose parameters close enough to mu=1, theta=0, c'=0 to use kappa_s < exp(-x)(1+2x)-1. Thus every pair in C' conflicts and |C'| >= exp(c'k log(p/k)) = binomial(p,k)^{c'+o(1)}. The convex-piece leaf bound and the binary certified-removal node bound follow from the framework.

This is a complete asymptotic proof with all new uniformity and dependency steps stated. It requires projected root-lifted leaf bounds: after deleting helpers fixed to zero the constructed B need not exist, so the argument makes no claim about that alternative.

## Safe theorem spine and exact source map

Abbreviations below are exact paths relative to the repository root:

- IC: `research-20260928b/bb-complexity/integer-core/relaxation-intrinsic-bounds.md`.
- PT: `research-20260928b/bb-complexity/sparse-regression/phase-transition.md`.
- SR: `research-20260928b/bb-complexity/sparse-regression/stronger-relaxations/thresholds.md`.
- BL: `research-20260928b/bb-complexity/binary-least-squares/certification-thresholds.md`.
- PV: `research-20260928b/reviews/pwe-verification.md`.

| Manuscript claim | Safe hypotheses and conclusion | Source statement and proof |
|---|---|---|
| Class number lower bound | Fixed convex projected relaxation phi and required integer set P; every covering certificate has at least kappa_tau(P) leaves | IC Definition 1.4, line 261; Theorem 1.6 and complete proof, line 292 |
| Exact semantic certificate size | Finite class number; arbitrary convex pieces, including hemispaces when needed; kappa leaves and 2kappa-1 nodes for a binary tree | IC Lemma 1.7a, line 309; Theorem 1.7, line 335, proof line 381; corrected kappa=1 convention included |
| Solver-operation accounting | Integer-space cuts valid for all node integer points preserve leaf bound; certified incumbent removals preserve leaves-plus-removals count | IC Theorem 1.8, line 431, proof line 480; exact recheck in `reviews/integer-core-recheck.md`, Sections 1 and 4 |
| Class versus syntax separation | Pure ILP class number <= rows+1; compact MILP can have 2^n classes; quadratic Jeroslow instance has kappa=2 but exponential variable trees | IC Proposition 2.1, line 574; Example 2.1a before line 664; Proposition 2.4, line 841 |
| Split versus class separation | Piecewise-linear projected objective from the clique-coloring system; use the cited split-tree theorem with its exact external hypotheses | IC Theorem 2.3, line 739, proof line 776; not a claim for one convex quadratic |
| Lattice-free interpretation | Finite convex phi on R^n, tau<=integer infimum; kappa equals the minimum number of facets of a lattice-free polyhedron enclosing {phi<tau} | IC Theorem 2.2, line 666, proof line 685; uses maximal lattice-free polyhedron theorem as a named standard input |
| Haar-CVP leaf lower bound | Haar unimodular lattice, uniform torus target; fixed delta in (0,0.1), eps<=delta GH^2; at least ((3/2)(1-delta)^2-delta)^{n/2}/[2(n+1)] leaves with displayed high probability | IC unfolding and moments, lines 1024 and 1045; Theorem 3.5, line 1151, proof line 1163 |
| Haar-CVP clique versus class | At vanishing relative tolerance: clique lower rate log_2(4/3)/2, clique upper rate 0.261241, class lower rate log_2(3/2)/2 and upper rate 1/2 | IC Theorem 3.4, line 1083; Proposition 3.6, line 1208; clique upper needs the explicit Kabatiansky–Levenshtein exponent from primary-source accounting |
| Curvature gadget | Orthogonal two-feature blocks with budget k; eps below the positive block midpoint deficit; 2^k conflicts, while exact block epigraph hull is root-exact | IC Lemma 4.2, line 1552; Theorems 4.3 and 4.4, lines 1585 and 1644; full algebraic proofs provided |
| C1 path theorem | Known OPT incumbent at off-path nodes, or strict C1 and best-bound search; at most 2p+1 nodes for binaries | PT Lemma 1.2, line 224; general integer form IC Lemma 5.1, line 1721 |
| Sparse root certification | Gaussian X, entries +/-b on fixed S*, fixed b,sigma>0; log^6 p<=n<=p, k<=C_0n/log p, sqrt n<=lambda<=n/log^2 p; threshold tau_lambda^2=(2+/-epsilon)log p at S* | PT Theorem 3.1, line 440; residual/coefficient lemmas lines 664 and 682; proofs in Sections 3.3 and 3.4, lines 700 and 826 |
| Sparse C1 certification | Same regime; threshold tau_lambda^2=(2+/-epsilon)log(p lambda/n); converse also k>=5000/epsilon^2, and interpret relative to S* | PT Theorem 3.2, line 450; saturated witness Proposition 2.3, line 355; primal Lemma 2.5, line 389; complete asymptotic proof lines 700 and 826 |
| Sparse linear/inexact window | k=p^{gamma+o(1)}, n=alpha k log p, fixed 0<gamma<1 and 2-gamma<alpha<2; suitable deterministic ridge; unique planted optimum, inexact root, linear variable trees with path qualifications | PT Corollary 3.3, line 482; sample-size proof at end of Section 3.4 |
| Fixed-ridge obstruction | lambda=sqrt n with fixed per-entry b/sigma; tau_lambda<=b/sigma, so planted certification eventually fails | PT Corollary 3.4, line 498; do not infer failure from small experiments with k=5 |
| Sparse hard conflict packing | k tends to infinity, k/n and lambda/n tend to zero, x=(2/n)log binomial(p,k) in (0,x_0); pure noise or total SNR below exp(-x)(1+2x)-1 | PT Theorems 4.3 and 4.4, lines 1027 and 1052; complete packing, conditional Gaussian and union-bound proof at line 1080 |
| Local hull thresholds unchanged | Above sparse easy regime plus r n log p=o(p); valid node relaxation >=perspective everywhere and <=L_r at root and forced-in nodes; converse k>=20000/epsilon^2 | SR Lemma 4.1, line 303; Lemma 4.2, line 350; Corollary 4.3, line 376; Theorem 4.4, line 393, proof line 408 |
| Pairwise-hull hard conflicts | Sparse hard hypotheses, projected root-lifted L_2 bounds and surviving helpers | SR Corollary 4.6, line 486, with the complete replacement proof in this report |
| Richer moment lift prices variance | Full moment PSD on (1,z,beta), complementarity, product cones, and McCormick constraints; penalty at least (lambda+lambda_min(X_A^TX_A))pi on A=supp z | SR Definition 5.0, line 516; Proposition 5.1, line 540, complete Gram proof line 548; no threshold claimed for this lift |
| PWE counterexample | Fixed d>k, fixed nonzero coefficients and sigma>0, n tends to infinity, ridge sqrt n; global exactness probability tends to [1-2 Phi_bar(b_min/sigma)]^{d-k}<1 | PT Remark 3.5, line 525; PV Section 3 has the self-contained finite-d proof; elementary proof expanded below |
| Binary root sign condition | M>=N, any rho>0; planted box exactness probability 2^{-N}; global exactness exponentially small in the stated SNR range | BL Proposition 1.1, line 277; Theorem 1.2, line 301, complete proof line 313 |
| Gaussian cone law | n<=M, full-rank Gaussian columns and independent residual; uniform support law and Beta/chi-square mixtures | BL Theorem 1.3, line 355, proof line 374; sign-orbit event extension and exact coefficient tail are new in this report |
| Binary ML threshold | Fixed beta>=1 and rho beta=(2+/-epsilon)log N; unique planted optimum above, one-bit improvement below with rho beta bounded below | BL Theorem 2.2, line 555, proof line 573; small proof repairs described above |
| Binary sharp C1 | Fixed beta>=1 and rho=theta N, threshold theta_c=1/[4(2beta-1)]; all nodes pass above and all fail below | BL Theorem 3.1, line 671; use (SO), (NT), (UN), (C1) from this report to replace Hu–Lu and the square conjecture |
| Static binary upper bound | Data-independent fixed branching order, rho tends to infinity, rho beta<=N, incumbent OPT<=UB<=W; log nodes <=(1+o(1))N log rho/[4(2beta-1)rho]+log(eN)+O(1) | BL Theorem 4.1, line 873, proof line 900; correct hockey-stick count included after closing audit |
| Binary class lower bound | rho_0<=rho<=c'_beta N, 0<=eps<=rho; every convex-piece box certificate has log leaves >=c_beta(N/rho)log rho-log(8N) | BL entropy Lemma 4.2, line 980; Theorem 4.3, line 1011, full proof line 1059; improved range interpretation above |
| Midpoint blindness | rho beta>(8+epsilon)log N: midpoint graph has no edges, while class number stays superpolynomial for rho=o(N); at rho beta=c log N, 0<c<8, log clique=N^{1-c/8+o(1)} | BL Theorem 2.3, line 631; Theorem 5.1, line 1192, proofs line 1204 and 1274 |
| Tall relaxation separation | Fixed beta>1; SDP and eigenvalue shift root-exact when rho>(1+epsilon)2beta log N/(sqrt beta-1)^4; box certificates still superpolynomial | BL Proposition 6.1, line 1304; Theorem 6.2, line 1342; Proposition 6.3, line 1360, proof line 1371; this is sufficient for SDP, sharp for the uniform shift above ML threshold |

## Normalizations and probabilistic dependencies

### Sparse regression

The model is X_ij~N(0,1), y=X beta*+sigma w, w~N(0,I_n), and the objective has no division by n: ||y-X beta||^2+lambda||beta||^2. A factor 1/2 on both objective terms is immaterial. Dividing the loss by n without correspondingly changing the ridge is not immaterial. The decisive quantities are

\[
b_\lambda=\frac{bn}{n+\lambda},\quad
\omega_\lambda^2=n\sigma^2+\frac{k b^2\lambda^2n}{(n+\lambda)^2},\quad
\tau_\lambda=\frac{\lambda b_\lambda}{\omega_\lambda}.
\]

In fact tau_lambda^2<n/k holds exactly for sigma>0: with A=(lambda b_lambda)^2, omega_lambda^2=n sigma^2+k A/n. The source's asymptotic version is valid but weaker. Suitable ridges of order sqrt(n log p), with constants adjusted to the distance above threshold, achieve the sample-size constants. Keeping lambda=sqrt n at fixed per-entry SNR instead keeps tau bounded. With per-entry variance gamma^2/n and lambda=sqrt n, tau_lambda^2=(1+o(1))n/(k+gamma^2/b^2); the root theorem extends to this normalization when its other hypotheses hold, including gamma^2=O(k b^2). For fixed gamma, its contribution is lower-order near the theorem's high-dimensional threshold.

Conditional on X_{S*},w, the null correlations x_j^T r are independent N(0,||r||^2). The selected violating set is measurable in these correlations; the orthogonal column components remain independent after conditioning on all correlations. This is why the sparse saturation proof may apply singular-value bounds to the selected columns after projecting away the true column space and r. Correlations on unselected columns are controlled only after conditioning on the selected perpendicular components and the witness they determine. The stronger-hull easy converse keeps a disjoint helper half independent of each candidate construction. The stronger-hull hard proof above instead uses a simultaneous deterministic event over every small support, so it needs no helper-half independence.

In the low-SNR hard model, use null features disjoint from S*. Conditional on X_{S*},w they are fresh Gaussian columns independent of y. For an arbitrary support T, the residual-producing vector X_{S* minus T} beta*+sigma w is independent of X_T. These are different conditional statements and neither assumes all support residuals independent. The OPT lower bound uses a union bound over supports, while the clique cross-term bound conditions on all scalar correlations and uses the still-independent perpendicular Gaussian components. The greedy code must be fixed as a measurable function of the correlation-selected index set before revealing those components.

### Binary least squares

A=sqrt(rho/N)H, per-entry noise variance one, M=beta N, and ||a_i||^2 is about rho beta. In the common alternative convention H/sqrt N with noise variance 1/rho, multiplying the entire objective by rho yields this model. The ML constant is rho beta=2log N; the midpoint constant is rho beta=8log N; C1 is rho=N/[4(2beta-1)]. These constants refer to three different events. The box decoder threshold from Hu–Lu concerns signs of a fractional solution and is not an integrality threshold. The new inactivity proof does not establish or require that decoder theorem.

For any fixed node, its residual w+2B_Wr 1 is independent of the free columns. A branching order chosen from the data does not preserve the fixed-node distribution without a further argument. The static-tree upper proof uses one fixed order and a union bound over its possible nodes; it must not be presented as an adaptive upper bound. The class lower proof uses a descent set chosen only from scalar Gaussian projections onto w, then controls the operator norm of its independent perpendicular matrix once, for all barycenters. It does not condition on the unknown optimum. Its allowance for W-OPT is crucial below the ML threshold.

### Random CVP

The lattice has Haar probability distribution on SL_n(R)/SL_n(Z); the target is uniform on the quotient torus conditional on the lattice. A change of lattice basis maps convex pieces bijectively, so the bounds are invariant under arbitrary unimodular basis reduction. In Euclidean coordinates the projected relaxation is ||Bx-t||^2. GH is the radius of the unit-volume ball, with GH^2~n/(2pi e). Unfolding in the random target and Siegel's mean theorem give E N_A=vol A and Var N_A=vol A under the joint law. No Poisson independence or higher Rogers moment is needed. The per-class cap bound needs the separate shortest-vector event. The clique packing does not.

## PWE discrepancy: self-contained manuscript proof

Let d>k be fixed, S fixed, and beta* have exactly k nonzero entries. Let X be n by d standard Gaussian, w independent standard Gaussian, y=X beta*+sigma w with fixed sigma>0, and lambda=sqrt n. Write f_n(T)=min_b||y-X_T b||^2+sqrt n||b||^2.

By finite-dimensional laws of large numbers, X^TX/n tends in probability to I_d, X^Tw/n tends to zero and ||w||^2/n tends to one. For every T of size at most k, f_n(T)/n tends to sigma^2+||beta*_{S minus T}||^2. The family of such T is finite, so the convergence is simultaneous. Every T distinct from S misses at least one nonzero coefficient, hence S is the unique optimal support with probability tending to one.

The ridge coefficients on S converge to beta*_S. Its residual is r=(I+X_SX_S^T/lambda)^{-1}y, and X_S^T r=lambda beta^S. Thus min_{j in S}|x_j^Tr|/sqrt n tends to b_min=min_{j in S}|beta*_j|. The squared norm of the signal part of r is O_P(1), since X_S^TX_S/n tends to I and lambda=sqrt n. The noise contribution differs from sigma w only on a fixed k-dimensional subspace, so ||r||^2/n tends to sigma^2; the cross term is negligible by Cauchy–Schwarz. Conditional on X_S,w, the d-k null correlations are independent N(0,||r||^2). The deterministic exactness characterization therefore gives

\[
\Pr\{R=f_n(S)\}
=\mathbb E\left[
\left(1-2\overline\Phi\left(\frac{\min_{j\in S}|x_j^Tr|}{\|r\|}\right)\right)^{d-k}
\right]
\longrightarrow
\left(1-2\overline\Phi(b_{\min}/\sigma)\right)^{d-k}<1.
\]

Changing from exactness at S to global exactness changes the probability by at most Pr{S is not the unique optimal support}, which tends to zero. The published sample-size inequality holds eventually for every fixed c_0, whereas its claimed probability 1-2exp(-c_1 n) tends to one for every fixed c_1>0. Thus the stated theorem is false under per-entry noise. This proof does not use the high-dimensional assumption n<=p and does not rely on a failed proof alone. The appendix normalization defects identify the source of the error, but are unnecessary to the counterexample. Total-energy noise is a different model; do not claim that the counterexample contradicts that model or that the entire published algorithm is invalid.

## Existing empirical evidence and its limits

| Evidence family | Stored provenance | What can be said |
|---|---|---|
| Sparse easy thresholds | PT Section 6, data and code under `sparse-regression/`; exact replacements in `data/c1_redecided.jsonl`; `sparse-easy-review.md`, `sparse-recheck.md`, `closing-audit-b.md` | C1 can hold with an inexact root at modest sizes. Every reported easy experiment violates log^6 p<=n<=p. These are finite-size observations, not validation of first-order sharp constants. |
| Fixed ridge seed 1007 | PT Section 6.3; `reviews/sparse-recheck/` and `reviews/closing-audit-b/` | At p=3200, k=5, four forced-in nodes fail, at null ranks 1,5,6,50. About 60% of the budget price is recovered for every forced-in null. Correct mechanism: many violators plus the individual fit, not one unusually strong null alone. The theorem's converse needs much larger k and n. |
| Sparse hard cliques and trees | PT Sections 6.4–6.6; sparse hard review's independent small enumerations | Fast-growing exact or greedy certified cliques illustrate the mechanism. The asymptotic proof's finite conditions are vacuous at practical dimensions. A greedy clique is a lower bound, not an exact clique number. |
| Stronger sparse relaxations | SR Section 7, `stronger-relaxations/data/`; first review and recheck | Moderate p/n yields real finite-size improvement; it disappears as p/n grows for the specified lifts. Some stored objective values exceed OPT by small floating errors; use the corrected certificate decisions and their reported tolerance. The p=3200 feasible constructions certify inexactness in four of six runs; they do not estimate an asymptotic transition. |
| PWE counterexample | PV Section 4, `reviews/pwe-verify/` | Analytic limit is (1-2 Phi_bar(2))^45=0.1230. Full-support enumeration confirms thirteen inexact roots among sixteen archived instances. Monte Carlo estimates are supporting observations; the last 0.153 estimate is above the limiting value and has an interval containing it. |
| Binary cone/C1/tree data | BL Section 7 and `binary-least-squares/data/`; mimo easy/hard reviews and recheck | Finite-size transitions and tree counts are useful evidence; at N=800 the observed square C1 scale is about 0.4N, above the asymptotic N/4. The proved class lower bound is numerically vacuous below roughly 1.7e7 in the quoted regimes, and its exponent is 10^4–10^5 times smaller than the upper exponent. |
| Binary sphere-decoder comparison | BL Section 7.3 and `reviews/mimo-recheck/sd_*` | Box branching has fewer nodes on the same instances, but sphere-decoder nodes are cheaper; the archived Python timing favors sphere decoding at N=64. Do not infer practical speedup from node count alone. The extrapolated e^80 or e^1900 counts are heuristic. |
| Binary SDP | BL Section 7.5 and mimo reviews | Tall systems show root certification at logarithmic SNR. Square observations suggest a much larger threshold but establish no N^3 theorem or polynomial SDP-based B&B theorem. |
| CVP | IC Section 3.7, `cvp_bounds.jsonl`, `cvp_bounds_big.jsonl`, `cvp_summary.log`; integer-core review | Goldstein–Mayer instances approximate the Haar family through a separate large-prime limit; fixed primes and n<=32 do not sample the asymptotic theorem exactly. Gaussian-basis experiments are a different distribution. Counts truncated by enumeration radii are conservative; clique calculations become greedy above the stated size limit. Deterministic nonviolations check the code, not the asymptotic law. |
| Curvature gadgets | IC Section 4, `check_perspective_gadget.py` and stored log | Exact rational arithmetic confirms finite gadgets and dual hull certificates. The theorem is proved algebraically for all k; finite enumeration is corroboration. The asymmetric hypotheses must scale with k if a family with unique optima is asserted. |

The corrected closeout is `research-20260928b/closing-research-results.md`, whose Limits section appropriately emphasizes finite-size vacuity, model-specific solver operations, and provisional novelty. Use the corrected theorem statements and proof reviews rather than the early summaries or scouts. Relevant reviews inspected: sparse easy and hard reviews, sparse recheck, PWE verification, stronger-relaxations review and recheck, mimo easy and hard reviews and recheck, integer-core review and recheck, and closing audits A and B. Their unresolved source-attribution matters should be passed to the single literature owner, not inferred from their unsuccessful searches.

## Optional completion: a unique-optimum gadget family for every k

The asymmetric theorem itself is complete, but its archived exact instances stop at k=6. A uniform rational family can be obtained without asserting extrapolation of those checks. Fix lambda=1, u=(1,0), v=(3/5,4/5). The unperturbed response y=u+v has positive midpoint deficit delta_0=32/225 and a strict global diminishing-returns margin. For block j=1,...,k take

\[
s_j=1+\eta j/k,\qquad e_j=\eta j/k^3,\qquad
y_j=s_j(u+v)+e_j u,
\]

with one sufficiently small rational eta>0 independent of k. All responses lie in a fixed compact neighborhood of y, so by continuity the global diminishing-returns gap stays strictly positive and the midpoint deficits are at least delta_0/2, uniformly over k and j. Since u and v have unit length, their singleton ridge values differ by

\[
g_{01,j}-g_{10,j}
=\frac{(u^Ty_j)^2-(v^Ty_j)^2}{2}>0,
\]

because u^Ty_j-v^Ty_j=(1-3/5)e_j>0 and both inner products are positive. The same compact neighborhood gives Delta_j<=C e_j with an absolute C, hence sum_j Delta_j<=C eta(k+1)/(2k^2)<=C eta. Choose eta small enough that C eta<delta_0/4. For every eps<delta_0/4 the asymmetric theorem's H1 and H2 hold for every k. It gives a unique optimum, a 2^k conflict clique and an exact pairwise-hull root. Coefficients are rational with polynomial denominators, so the instance encoding remains polynomial in k. Distinct scales remove block-permutation symmetry; the positive singleton gaps remove feature-swapping symmetry. The substantive statement is unique optimum and the proved conflict/hull separation, not a claim excluding every possible abstract symmetry or dominance argument.

## Verification performed for this audit

Only targeted source reads and mathematical proof reconstruction were performed. The commands used were `cat`, `sed -n`, `wc -l`, and `rg` on the assigned notes, their reviews, AGENTS.md and the manuscript brief; `apply_patch` wrote only this report. No numerical or symbolic experiment was rerun. No project-wide check or CI query was made. The new sign-orbit/NNLS results and pairwise-hull completion should receive the independent proof review requested by root before manuscript integration. Existing computational outcomes above are reported as archived evidence, not as newly verified runs.
