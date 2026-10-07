# Independent review of the Gaussian NNLS coefficient tail

Core verdict: **verified, with minor statement clarifications**. The sign-orbit identity, finite-dimensional coefficient bound, uniform inactivity of the single-wrong-fixing nodes, and sharp fixed-parameter C1 threshold are correct under the stated Gaussian model. They resolve the square-system all-node inactivity conjecture in the source note and remove the Hu–Lu input from that conclusion. I found no mathematical blocker or counterexample within this scope.

Extension verdict: **verified independently**. The subsequently added exact coefficient density (TD), maximum-coefficient mixture (EM), and sharp root inactivity threshold (RT) are correct. Section 8 records a separate reconstruction and scope check. No part of that extension remains unreviewed here.

The review reconstructs the argument independently. It does not reuse another review, infer correctness from computations, or rely on a literature claim. The only files read for mathematical context were `AGENTS.md`, `BRIEF.md`, the new first section of `AUDIT-DISCRETE.md`, and the relevant portions of the original `certification-thresholds.md`. No source note, audit, or manuscript was edited.

## 1. Statement corrections

These corrections make the statements precise; none changes a Gaussian-model conclusion.

1. **Low severity: make general position explicit.** At `AUDIT-DISCRETE.md:11`, replace “v is in general position relative to its column spans” by the following finite list of nondegeneracy conditions: almost surely, for every nonempty subset S, every coordinate of

   \[
   d^S=-(C_S^T C_S)^{-1}C_S^Tv
   \]

   is nonzero, and for every subset S and every j outside S,

   \[
   c_j^T(I-P_{L_S})v\ne0.
   \]

   Empty lists of conditions are vacuous. This is the meaning used in the proof. Merely requiring v not to belong to the column spans would be insufficient: with M=3, n=2, independently signed columns e1 and e2, and deterministic v=e2+e3, v belongs to none of those spans but the first NNLS coordinate is always zero. Every Gaussian application here satisfies the stronger conditions, as proved below.

2. **Low severity: distinguish the orthant value from the box value.** At lines 93–101, first define

   \[
   \widetilde r_i=\min_{u\ge0}\|v_i+B_{-i}u\|^2
       =\|v_i\|^2(1-Y_i).
   \]

   Then state that `r_i = tilde r_i` simultaneously on the event in (UN) whose probability tends to one. The exact projection law belongs to the orthant problem; it is not an unconditional finite-dimensional law for the box problem. The audit's explanation already has this intended meaning. The concentration statement should specify

   \[
   \Pr\!\left\{\max_i\left|Y_i-\frac{N-1}{2M}\right|>2t\right\}
       \le6N\exp(-Mt^2/64).
   \]

   The factor 2 is part of the mixture conclusion in Lemma 0.2. With `t = sqrt(192 log N/M)`, the right side is `6N^{-2}`, so the stated order is correct.

3. **Low severity: use the exact aspect ratio in the root expansion.** Let `beta_N = M/N` and reserve beta for its limit. The expansion at line 128 is

   \[
   \log\!\left[\frac N2 q^{M-N+1}
         \left(\frac{1+q}{2}\right)^{N-1}\right]
      =\log(N/2)-(2\beta_N-1)\rho+o(1)
   \]

   for `rho = O(log N)` and bounded `beta_N`. Replacing `beta_N` by its limit gives an `o(log N)` remainder under mere convergence, and an `o(1)` remainder if `M = beta N + O(1)`. The sufficient root-inactivity conclusion survives either version. For example, `beta_N = beta + 1/sqrt(log N)` makes the difference from the displayed limit-ratio expansion of order `sqrt(log N)`, so that particular `o(1)` assertion requires the rounding assumption or exact-ratio notation.

One harmless notation improvement: write the coefficient union bound first as `2^{-n} sum_{S nonempty} sum_{j in S} P(|d_j^S|>t)`. Only then group supports by size. The expression at lines 40–41 implicitly uses Gaussian column exchangeability to choose a representative S of each size.

## 2. Deterministic sign action and the invariant-event identity

Fix a full-column-rank C and v satisfying the explicit nondegeneracy conditions above. Strict convexity of `||v+Cu||^2` gives a unique NNLS minimizer. Fix a candidate support S. Put

\[
L_S=\operatorname{span}(C_S),\quad
d^S=-(C_S^TC_S)^{-1}C_S^Tv,\quad
z^S=(I-P_{L_S})v.
\]

The point supported on S with coordinates d^S has residual z^S. Its KKT conditions are exactly

\[
d_j^S>0\quad(j\in S),\qquad
c_j^Tz^S\ge0\quad(j\notin S).
\]

The nondegeneracy assumption makes the latter inequalities strict. Necessity follows from the first-order conditions. Sufficiency follows from convexity: the gradient vanishes on S and has nonnegative components off S. Full rank makes this minimizer unique. Thus these conditions characterize support S, without an additional geometric assumption about the selected face.

For a sign vector epsilon, write `C^epsilon = C D_epsilon`. Its S-span and projector are unchanged, its restricted OLS vector is `D_epsilon,S d^S`, and its candidate residual remains z^S. There is exactly one choice

\[
\epsilon_j=\operatorname{sign}(d_j^S)\quad(j\in S),\qquad
\epsilon_j=\operatorname{sign}(c_j^Tz^S)\quad(j\notin S)
\]

that satisfies those KKT conditions. This gives the pointwise identity

\[
\sum_{\epsilon\in\{-1,1\}^n}
    1\{S(CD_\epsilon,v)=S\}=1.
\]

For an event E_S invariant under all these sign changes, multiplication by its indicator gives the stronger pointwise identity

\[
\sum_\epsilon
  1\{S(CD_\epsilon,v)=S,\ E_S(CD_\epsilon,v)\}
      =1\{E_S(C,v)\}.
\]

Independence of v and C, together with column-sign invariance of the law of C, ensures that every pair `(CD_epsilon,v)` has the law of `(C,v)`. Taking expectations therefore proves (SO). It also proves `P(S=S_0)=2^{-n}` for each fixed support S_0, and hence `|S| ~ Bin(n,1/2)`.

This does not condition on the support before invoking a Gaussian regression formula. It transfers the distribution of each sign-invariant event from the unconditional fixed submatrix to the event selecting that submatrix. This distinction is essential and is handled correctly by (SO).

The empty support has only the off-support conditions. The full support has only the positive-coordinate conditions. In the square full-support case the residual is identically zero, but there is no off-support condition to check. Thus the sign count remains one in that case.

For Gaussian C and an independent isotropic Gaussian v of positive variance, all required nondegeneracy conditions hold. Conditional on a full-rank C, each OLS coordinate is a nonzero linear functional of v. For j outside S, full column rank implies `(I-P_{L_S})c_j != 0`, so the off-support inner product is also a nonzero linear functional of v. Each has a continuous, nondegenerate Gaussian law. There are only finitely many such functionals at any fixed dimension, so none is zero almost surely. Every Gaussian submatrix has full rank almost surely because its deficient-rank set has Lebesgue measure zero.

## 3. Fixed-submatrix regression tail and exact mixture sum

Take `C=aH` and `v ~ N(0,c^2 I_M)` independently, with positive a and c. On the event selecting a nonempty S, the positive NNLS coefficients equal d^S. The event

\[
E_S(t)=\{\max_{j\in S}|d_j^S|>t\}
\]

is invariant under every sign change: a sign change within S flips only that coordinate of d^S, and a sign change outside S has no effect. Partitioning by the selected support, applying (SO), and then applying the coordinate union bound gives

\[
\Pr\{\max_j u_j^o>t\}
 =2^{-n}\sum_{S\ne\varnothing}\Pr(E_S(t))
 \le2^{-n}\sum_{S\ne\varnothing}\sum_{j\in S}
       \Pr\{|d_j^S|>t\}.
\]

The first equality is valid because all d^S coordinates are positive on the event selecting S. The absolute-value event coincides there with the positive-coefficient event. The empty support contributes zero.

For a fixed S of size s and fixed j in S, let P be the projector orthogonal to the span of the other s−1 columns of H_S. Minimizing first over those other unrestricted coefficients reduces OLS to

\[
\min_z\|Pv+aPh_jz\|^2,
\]

so

\[
d_j^S=-\frac{h_j^TPv}{aQ},\qquad Q=\|Ph_j\|^2.
\]

Conditional on the other s−1 columns, P has rank `M-(s-1)=M-s+1`. The vector h_j is independent standard Gaussian, so Q has exactly that chi-square law. Conditional on all H_S, the numerator is centered Gaussian with variance `c^2 Q`, because v remains independent isotropic Gaussian. Thus

\[
d_j^S\mid H_S\sim N\!\left(0,\frac{c^2}{a^2Q}\right).
\]

This conditioning does not assert that the selected support is independent of a Gaussian target, and it does not need the target to be independent of quantities elsewhere in the B&B instance. Independence from this node's free matrix is the hypothesis actually used.

For a standard normal Z and z≥0, `P(|Z|>z) <= exp(-z^2/2)`. The two-sided bound has no missing factor 2. For example, the function `2 exp(z^2/2) Phi(-z)` starts at 1 and decreases, by the elementary Mills inequality. Averaging this bound conditional on H_S gives

\[
\Pr\{|d_j^S|>t\}
 \le\mathbb E\exp\!\left(-\frac{a^2t^2Q}{2c^2}\right)
 =\left(1+\frac{a^2t^2}{c^2}\right)^{-(M-s+1)/2}
 =q^{M-s+1}.
\]

The last equality is the chi-square Laplace transform. It remains valid at `s=M`, where the degrees of freedom are 1. There is no hidden large-degree requirement.

Gaussian column exchangeability makes the bound depend only on s. The remaining sum is

\[
2^{-n}\sum_{s=1}^n {n\choose s}s q^{M-s+1}.
\]

Using `s binom(n,s) = n binom(n-1,s-1)` gives

\[
\begin{aligned}
\sum_{s=1}^n {n\choose s}s q^{M-s+1}
 &=nq^{M-n+1}\sum_{s=1}^n
       {n-1\choose s-1}q^{n-s}\\
 &=nq^{M-n+1}(1+q)^{n-1}.
\end{aligned}
\]

After multiplication by `2^{-n}`, this is exactly (NT). The binomial mixture is summed exactly; the coefficient probability is bounded, not evaluated exactly. The right side can exceed 1, which does not invalidate an upper bound.

The square case `M=n` is covered. Nearly full selected supports have heavy regression tails, but their sign-orbit probability is already included. Replacing the selected matrix by the full square matrix would lose that information; the proof does not make that replacement.

## 4. Scaling, the cutoff 2, and simultaneous node inactivity

For deterministic x*, multiplying column i of A by x*_i preserves the independent Gaussian column law. At `rho=theta N`, the signed columns have covariance `theta I_M`. Error coordinates are exactly

\[
u_j=1-x_j^*x_j,\qquad y-Ax=w+Bu,
\]

so the binary values are 0 and 2, and the box is `[0,2]^N`. A single wrong fixing sets `u_i=2`, leaving residual

\[
v_i=w+2b_i\sim N(0,(1+4\theta)I_M).
\]

The pair `(w,b_i)` is independent of every column of B_-i. Hence v_i is independent of the entire free matrix. Sharing w across nodes does not change this per-node assertion.

Substituting `n=N-1`, `a^2=theta`, `c^2=1+4theta`, and `t=2` into (NT) gives

\[
q_\theta^2=\frac{1+4\theta}{1+8\theta},\qquad
\Pr\{\max_j u_{i,j}^o>2\}
 \le\frac{N-1}{2}q_\theta^{M-N+2}
       \left(\frac{1+q_\theta}{2}\right)^{N-2}.
\]

The exponent is `M-(N-1)+1=M-N+2`. In particular it is 2, rather than 1, for a single-wrong-fixing node of a square N-column system. The single-coordinate regression exponents inside the mixture were `M-s+1`, so these are distinct quantities and both are correct.

A union bound over the N indices gives exactly (UN). For fixed positive theta, `b_theta=(1+q_theta)/2<1`, and for every `M>=N`, `q_theta^{M-N+2}<=1`. Thus (UN) is at most a constant times `N^2 b_theta^N`, which decreases exponentially. Independence of node events is unnecessary.

The orthant feasible set contains the box. If its unique minimizer has all coefficients at most 2, it lies in the box and the two minimum values agree. Conversely, if the values agree, a box minimizer also minimizes the orthant problem; strict convexity forces it to be the NNLS minimizer. Therefore the exact value-equality cutoff is `max u^o <= 2`, not `<2` and not a decoder cutoff at 1.

Equality at 2 does not prevent value equality. It is also a null event here: for each fixed S and coordinate j, d_j^S has a continuous law at any nonzero value; taking a finite union over supports and coordinates proves the assertion for the NNLS solution. Thus “upper bounds inactive” can be interpreted strictly without changing any probability statement.

The source conjecture's normalized pure-noise variable U is also covered. With n=N−1, `C=H/sqrt(n)`, standard Gaussian target, and `t=k sqrt(N)` for any fixed k>0,

\[
q_N=(1+k^2N/n)^{-1/2}\longrightarrow(1+k^2)^{-1/2}<1.
\]

For the source's M=N observations, (NT) bounds the tail by

\[
\frac n2 q_N^2\left(\frac{1+q_N}{2}\right)^{n-1},
\]

which is exponentially small and therefore `o(1/N)`. The node cutoff in the source reduction is exactly

\[
U\le2\sqrt{\frac{\theta(N-1)}{1+4\theta}},
\]

consistent with the direct `t=2` substitution. No normalization discrepancy remains.

## 5. Independent reconstruction of the projection law and C1 limit

The projection law can itself be derived using (SO). For a fixed S, both squared norms

\[
X_S=\|P_{L_S}v_i\|^2,\qquad
Z_S=\|(I-P_{L_S})v_i\|^2
\]

are invariant under all column signs. Conditional on the free matrix, their laws are independent chi-squares with s and M−s degrees of freedom, multiplied by `c_theta^2=1+4theta`. Those laws depend only on the dimensions. Applying (SO) to every Borel event of `(X_S,Z_S)` shows that the same joint law holds conditional on selecting S. Thus the selected support size is `Bin(N-1,1/2)` and

\[
Y_i=\frac{X_S}{X_S+Z_S}\ \bigg|\ |S|=s
       \sim\operatorname{Beta}(s/2,(M-s)/2).
\]

At s=0 or s=M, this means the point mass at 0 or 1. For the single-fixing problems n=N−1≤M−1, the s=M case cannot arise. This argument proves the per-node law directly and does not assume independence between nodes or condition on simultaneous inactivity.

Lemma 0.2's mixture bound applies to each such Y_i. For large N, `t=sqrt(192 log N/M)` lies in `[0,1]`. A union bound gives

\[
\Pr\!\left\{\max_i\left|Y_i-\frac{N-1}{2M}\right|>2t\right\}
 \le6N^{-2}.
\]

Separately, let `beta_N=M/N -> beta>=1`. The chi-square norm tails imply

\[
W=M+O_{\mathbb P}(\sqrt{N\log N}),\qquad
\max_i\big|\|b_i\|^2-\theta M\big|
      =O_{\mathbb P}(\sqrt{N\log N}).
\]

Conditional on w, the variables `b_i^T w` are independent centered Gaussians with variance `theta W`. On the event W=O(N), the Gaussian tail and a union bound show

\[
\max_i|b_i^Tw|=O_{\mathbb P}(\sqrt{N\log N}).
\]

The fact that these quantities are not independent of the corresponding Y_i is irrelevant: all concentration events are intersected using union bounds. Consequently,

\[
\max_i\left|\|v_i\|^2-(1+4\theta)M\right|
      =O_{\mathbb P}(\sqrt{N\log N}).
\]

Intersect these events with the inactivity event from (UN). On this intersection,

\[
\begin{aligned}
\frac{r_i-W}{N}
 &=\frac{\|v_i\|^2}{N}(1-Y_i)-\frac WN\\
 &=\beta(1+4\theta)\left(1-\frac1{2\beta}\right)-\beta
       +o_{\mathbb P}(1)\\
 &=2\theta(2\beta-1)-\frac12+o_{\mathbb P}(1),
\end{aligned}
\]

with the error uniform in i. The event omitted from this calculation has probability tending to zero. This proves (C1) as convergence in probability of the displayed maximum, including beta=1.

There is an equivalent direct proof that further checks the calculation. The invariant-event argument above gives the exact orthant residual law

\[
\widetilde r_i/c_\theta^2\ \bigg|\ |S|=s\sim\chi^2_{M-s},
\qquad |S|\sim\operatorname{Bin}(N-1,1/2).
\]

Binomial and chi-square tails, followed by a union bound over i, yield

\[
\max_i\left|\widetilde r_i-
  (1+4\theta)\left(M-\frac{N-1}{2}\right)\right|
       =O_{\mathbb P}(\sqrt{N\log N}).
\]

On inactivity, r_i equals this orthant residual. Subtracting `W=M+O_P(sqrt(N log N))` gives

\[
r_i-W
 =N\left[2\theta(2\beta_N-1)-\frac12\right]
       +\frac{1+4\theta}{2}
       +O_{\mathbb P}(\sqrt{N\log N})
\]

uniformly in i. This confirms both the threshold constant and the finite N−1 correction.

## 6. ML recovery, the two sides of C1, and the tree consequence

At fixed positive theta, the required assertion `OPT=W` does not need a box-decoder theorem. It follows from the elementary vertex union bound, which can be checked directly at linear SNR. For a nonempty flipped set T of size k, the random vector `2 sum_{j in T} b_j` is Gaussian with covariance `4 theta k I_M`, independently of w. A coordinatewise Gaussian integration at exponential parameter 1/4 gives

\[
\Pr\{f(x^T)\le W\}\le(1+\theta k)^{-M/2}.
\]

To sum this bound, choose a small constant delta in `(0,1/2)` with

\[
\delta\log(e/\delta)<\tfrac14\log(1+\theta).
\]

For `1<=k<=delta N`, the bound `binom(N,k)<=exp(N delta log(e/delta))` and `M>=N` bound each term by `exp[-N log(1+theta)/4]`. For `k>delta N`, the whole contribution is at most

\[
2^N(1+\theta\delta N)^{-M/2},
\]

which tends to zero faster than exponentially in N. Hence no nonplanted vertex has value at most W with probability tending to one. This independently proves unique ML recovery in exactly the regime used here.

Set `theta_c=1/[4(2 beta-1)]`. The limiting node gap is

\[
2\theta(2\beta-1)-\tfrac12
      =\tfrac12(\theta/\theta_c-1).
\]

If fixed `theta >= (1+epsilon)theta_c`, the limit is at least epsilon/2. Uniform convergence then gives `r_i>=OPT+epsilon N/4` for all i with probability tending to one. If fixed `theta <= (1-epsilon)theta_c`, the limit is at most −epsilon/2, giving `r_i<=OPT-epsilon N/4` for all i with probability tending to one. The loss from epsilon/2 to epsilon/4 leaves a strict margin for all random errors and aspect-ratio rounding.

On the upper side, any off-path variable-branching node relative to x* has a wrong fixing i and has a feasible relaxation set contained in that single-wrong-fixing node. Its bound is therefore strictly above OPT. With the incumbent OPT available when those nodes are checked, only the path to x* can branch. At most N binary branchings generate at most `2N+1` nodes. For best-bound search, while the planted optimum is not yet reached there is an active node on its path with bound at most OPT, so an off-path node with bound strictly above OPT cannot be expanded first. The same node bound follows once the optimum is found. This checks the necessary search/incumbent qualification.

On the lower side, all N single-wrong-fixing nodes fail C1 at the unique optimum x*. This resolves the source's square-system all-node failure claim. It does not by itself prove a superlinear or exponential tree lower bound: failure of a sufficient condition for a short tree is not such a lower bound.

The statement is a sharp first-order threshold for fixed theta separated from theta_c by a fixed multiplicative margin. No conclusion is proved at equality or inside a shrinking critical window.

## 7. Root inactivity and its precise scope

For the root, `n=N`, `a^2=rho/N`, `c^2=1`, and the cutoff is again t=2. Direct substitution into (NT) gives (RI) with exponent `M-N+1`. This exponent is 1 in a square root problem, unlike the exponent 2 in its single-wrong-fixing problems.

For `rho=O(log N)` and bounded `beta_N=M/N`, elementary Taylor expansions give

\[
\log q=-2\rho/N+O(\rho^2/N^2),\qquad
\log\frac{1+q}{2}=-\rho/N+O(\rho^2/N^2).
\]

Therefore

\[
\log(\text{RI right side})
 =\log(N/2)-(2\beta_N-1)\rho
       +O(\rho/N+\rho^2/N).
\]

At `rho=(1+epsilon)log N/(2 beta-1)` with `beta_N -> beta>=1`, this is

\[
-\epsilon\log N-\log2+o(\log N)\longrightarrow-\infty.
\]

Thus the violation probability tends to zero for both square and tall systems. If `M=beta N+O(1)`, the remainder in the audit's stated expansion is indeed o(1).

For a fixed realization of the signed H and w, set `z=sqrt(rho)u` in the orthant problem. Its objective becomes `||w+(H/sqrt(N))z||^2`, independent of rho. Uniqueness gives exactly `u^o(rho)=u^o(1)/sqrt(rho)`. The maximum coefficient is nonincreasing in rho, so the sufficient inactivity result extends to every larger rho by this coupling. The same conclusion could also be seen directly from the monotonic right side of (RI).

This finite-tail sufficient bound proves equality of box and orthant minimum values. By itself it does not prove a necessary threshold for inactivity, a guarantee that the box solution rounds to x*, or a claim that the root minimizer is a vertex. The new extension reviewed below supplies the matching necessary threshold for inactivity. The argument assumes `M>=N` and the independent Gaussian model; it does not establish a result for underdetermined matrices, sign-biased columns, a data-dependent planted vector, or a target correlated with this node's free columns.

## 8. Separate review of the exact mixture and sharp root threshold

This section reviews the extension saved at `AUDIT-DISCRETE.md:130` through line 207 after the original core review was complete. I derived the coefficient representation independently before reading that extension, then compared each formula, its normalization, and the asymptotic proof. **All extension claims are verified.** The genericity clarification in Section 1 still applies to the abstract sign-orbit lemma; the extension's Gaussian assumptions satisfy it automatically. No additional correction is needed in (TD), (EM), or (RT).

### Fixed-support density, normalization, and a common denominator

For a fixed support of size s≥1, conditional on H_S,

\[
d^S\mid H_S\sim N\!\left(0,
  \frac{c^2}{a^2}(H_S^TH_S)^{-1}\right).
\]

Multiplying this normal density by the Gaussian matrix density leaves a matrix integral proportional to

\[
\int_{\mathbb R^{M\times s}}
\det(H^TH)^{1/2}
\exp\!\left[-\tfrac12\operatorname{tr}
  \left(H^TH\left(I_s+\frac{a^2}{c^2}dd^T\right)\right)\right]\,dH.
\]

Put `T=I_s+(a^2/c^2)dd^T` and substitute `H=GT^{-1/2}`. Applying the right-side linear map to each of the M rows gives the Jacobian `det(T)^{-M/2}`. The Gram determinant factor gives another `det(T)^{-1/2}`. The exponential becomes `exp(-tr(G^TG)/2)`. Hence the entire d dependence is

\[
\det(T)^{-(M+1)/2}
   =\left(1+\frac{a^2}{c^2}\|d\|^2\right)^{-(M+1)/2}.
\]

The matrix integral is finite: by Hadamard's inequality the square root of the Gram determinant is bounded by the product of the s column norms, and Gaussian norms have all finite moments. This remains true for M=s.

Independently, take a standard Gaussian Z in dimension s and an independent `Q~chi^2_nu`, with `nu=M-s+1>=1`. For `D=(c/a)Z/sqrt(Q)`, changing variables in the Gaussian density conditional on Q and then integrating Q gives

\[
\begin{aligned}
p_D(d)
&=\left(\frac ac\right)^s
 \frac{1}{(2\pi)^{s/2}2^{\nu/2}\Gamma(\nu/2)}
 \int_0^\infty q^{(s+\nu)/2-1}
     e^{-q(1+(a^2/c^2)\|d\|^2)/2}\,dq\\
&=\left(\frac ac\right)^s
 \frac{\Gamma((s+\nu)/2)}{\pi^{s/2}\Gamma(\nu/2)}
 \left(1+\frac{a^2}{c^2}\|d\|^2\right)^{-(s+\nu)/2}.
\end{aligned}
\]

Since `s+nu=M+1`, this is precisely (TD), including its gamma constant. It is a normalized density. The original matrix-integral density has the same shape and is also normalized, so the two constants agree.

This proof establishes a **joint** representation of all coefficients with one common Q. Applying a separate one-coordinate Student law to each coordinate and assuming the denominators independent would be wrong. The extension uses the joint law correctly. The auxiliary Q is not a claim about an actual selected singular value or a coupling between different nodes.

### Transfer to positive NNLS coordinates and the exact CDF

For any Borel event of the absolute vector `|d^S|`, (SO) says

\[
\Pr\{S(C,v)=S,\ |d^S|\in D\}
     =2^{-n}\Pr\{|d^S|\in D\}.
\]

On the selected support, d^S is positive and equals the NNLS coordinate vector. Dividing by the nonzero probability `2^{-n}` proves that the selected positive vector conditional on that specified support has exactly the law of `|d^S|`. This verifies lines 153–158 of the extension. It does not assert that the signed OLS vector itself is unaffected by conditioning on positivity.

Every support has probability `2^{-n}`; its size is therefore `K~Bin(n,1/2)`. Conditional on size K=s, the maximum positive coordinate has the law

\[
\frac ca\frac{\max_{j\le s}|Z_j|}{\sqrt Q},
\qquad Q\sim\chi^2_{M-s+1},
\]

with independent Gaussian coordinates and conditional independence of Q and those coordinates. At K=0, the NNLS maximum is zero. Conditional on Q and positive s, the Gaussian maximum CDF is

\[
\left[1-2\overline\Phi\!\left(\frac{at\sqrt Q}{c}\right)\right]^s.
\]

Mixing over K gives exactly (EM). At t=0, every positive-s term vanishes, leaving the atom `2^{-n}`. The zero-size summand is explicitly defined as one, so the apparent `0^0` at t=0 does not cause an ambiguity.

The Gaussian target, its independence from H, and the full-rank condition M≥n are all necessary hypotheses of this particular derivation. No independence among B&B node maxima follows from the synthetic one-node representation.

### Extreme-value scale and the random root cutoff

At rho=1 for the root, `a^2=1/N`, `c^2=1`, and n=N. The mixture gives

\[
U_N^2:=\left(\max_j u_{N,j}^o(1)\right)^2
 \stackrel d=\frac NQ\max_{j\le K}|Z_j|^2,
\quad K\sim\operatorname{Bin}(N,1/2),
\quad Q\mid K\sim\chi^2_{M_N-K+1}.
\]

The K=0 case is interpreted as U_N=0; its probability tends to zero. Binomial concentration gives K/N→1/2. On `N/4<=K<=3N/4`, the degrees of freedom of Q lie between positive constants times N for bounded `beta_N=M_N/N`, and are at least N/4. Conditional chi-square concentration is therefore uniform on this event. Explicitly,

\[
\frac QN-\left(\beta_N-\frac12\right)
 =\frac{Q-(M_N-K+1)}N
      -\left(\frac KN-\frac12\right)+\frac1N
 \xrightarrow{\mathbb P}0.
\]

For each fixed delta in `(0,1)`, a Gaussian tail union bound at the squared level `2(1+delta)log N` is at most `2N^{-delta}`, uniformly in K≤N. An elementary lower-tail estimate at the squared level `2(1-delta)log N` gives the single-coordinate probability at least

\[
c_\delta\,\frac{N^{-(1-\delta)}}{\sqrt{\log N}}.
\]

For example, this estimate follows by integrating the normal density over the interval `[z,z+1/z]` for z≥1; the density on that interval is at least a constant times `exp(-z^2/2)`. Conditional on `K>=N/4`, independence of the Gaussian coordinates then bounds the probability of no exceedance by

\[
\exp\!\left[-\frac{c_\delta N^\delta}{4\sqrt{\log N}}\right].
\]

Thus `max_{j<=K}|Z_j|^2/(2 log N)→1` in probability. No refined extreme-value theorem is needed, and random K does not alter the first-order scale.

For `rho_box,N=U_N^2/4`, the ratio in (RT) is

\[
\frac{\rho_{\mathrm{box},N}}{\log N/(2\beta_N-1)}
 =\frac{\beta_N-1/2}{Q/N}\,
   \frac{\max_{j\le K}|Z_j|^2}{2\log N}
 \xrightarrow{\mathbb P}1.
\]

The denominator stays away from zero in probability because `beta_N>=1`. This verifies both the limiting ratio and its normalization. The use of the exact ratio beta_N in (RT) avoids the root-expansion precision issue from Section 1.

For each fixed realization of H_N and w_N and every positive rho, strict convexity and the scaling substitution give `u_N^o(rho)=rho^{-1/2}u_N^o(1)`. Section 4's cutoff argument therefore proves the pathwise equivalence

\[
\text{box minimum = orthant minimum}
  \quad\Longleftrightarrow\quad
  \rho\ge\rho_{\mathrm{box},N}.
\]

If a deterministic positive rho_N is eventually at least `(1+epsilon)log N/(2beta_N-1)`, (RT) places it above the random cutoff with probability tending to one. If it is eventually at most `(1-epsilon)log N/(2beta_N-1)`, (RT) places it strictly below the cutoff with probability tending to one. The orthant minimizer then lies outside the box. A box minimum equal to the orthant minimum would also be an orthant minimizer and contradict uniqueness; hence the value inequality below the threshold is strict. Equality at the cutoff still belongs to the equality event, as the extension states.

This works for arbitrary deterministic positive sequences rho_N, including sequences much smaller or larger than log N. Positive rho is essential for strict convexity and the scaling argument; the extension explicitly excludes rho=0. At rho=0, all feasible vectors have the same objective, so extending the converse to that isolated value would be false.

The threshold concerns root equality with the orthant relaxation. It does not imply planted recovery, rounding correctness, a vertex optimum, or equality with the integer optimum. No conclusion is given at the critical first-order ratio 1. For independent noise of variance sigma^2 with sigma>0, dividing the residual by sigma gives the stated effective SNR `rho_N/sigma^2`; this normalization is correct.

## 9. Verification record

Verification consisted of the independent KKT and sign-action reconstruction, Gaussian regression conditioning, chi-square degree count and Laplace transform, binomial sum, exact error-coordinate scaling, both projection-law derivations, vertex union bound, threshold algebra, root Taylor expansion, and the separate coefficient-density, exact-mixture, and random-root-threshold proofs above.

Actual local commands were document reads and scoped searches: `cat AGENTS.md`, `cat paper-bb-complexity/evidence/BRIEF.md`, `sed`/`nl` reads of the first section of `AUDIT-DISCRETE.md` and its added lines 130–207, `cat` followed by targeted `rg` and `sed` reads of `certification-thresholds.md`, a scoped `rg --files` search for additional `AGENTS.md` or an existing owned review file, and `tail` to inspect the owned report. No code, numerical experiment, project-wide verification, or CI check was run. No literature research or delegation was performed.

Only `paper-bb-complexity/evidence/REVIEW-NNLS-R1.md` was written.
