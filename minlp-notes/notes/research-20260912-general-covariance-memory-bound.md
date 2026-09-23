# Finite-memory relative precision bounds from covariance decay

Date: 2026-09-12. Status: independently derived by `dense_exact_review` alongside
the root researcher's derivation. The proof below supplies an explicit extension
of the [noisy Markov bound](research-20260912-noisy-markov-memory.md) to general
block covariances. A further fresh proof review and the root's primary-literature
audit remain necessary. Inverse decay, weighted conjugation, and local conditional
factorizations are established methods; no novelty is claimed for those tools.

**Result.** Exponential decay of off-diagonal covariance blocks and a uniform
positive eigenvalue bound suffice for an explicit relative precision error that
decays exponentially with the calendar window, simultaneously for every selected
subset. Its constants do not depend on the number of candidates or the block
dimension. Diagonal covariance blocks need no upper bound. This gives the same
weighted-trace approximation scheme under broader covariance promises, although
the present constants are much worse than the specialized Markov constants.

## 1. Assumptions and explicit constants

Let \(R\) be a real symmetric positive definite covariance matrix, indexed by
calendar times \(1,\ldots,n\), with a complete \(d\)-dimensional observation
block at each time. Suppose
\[
R\succeq mI,\qquad
\|R_{ts}\|_2\le C\rho^{|t-s|}\quad(t\ne s),
\tag{1}
\]
where \(m>0\), \(C>0\), and \(0<\rho<1\). No bound on \(R_{tt}\) is needed.
For \(C=0\) or \(\rho=0\), the covariance is block diagonal and the local
construction is exact at every window. The proof also works with different
block dimensions at different times.

For a selected subset \(S\) and integer \(L\ge0\), define
\[
H_t=S\cap\{t-L,\ldots,t-1\},\quad
b_t=R_{tH_t}R_{H_tH_t}^{-1},\quad
D_t=R_{tt}-R_{tH_t}R_{H_tH_t}^{-1}R_{H_t t}.
\]
Empty histories have no regression coefficients and \(D_t=R_{tt}\). Let
\(Z_t=Y_t-\sum_{j\in H_t}b_{tj}Y_j\), where the observations here are
centered errors. Write \(A_L\) for this unit block lower triangular residual
map, \(D_L=\operatorname{diag}(D_t)\), and
\[
\mathcal C_L=D_L^{-1/2}A_LR_{SS}A_L^TD_L^{-1/2},\qquad
Q_L=A_L^TD_L^{-1}A_L.
\]
These are genuine local Gaussian conditionals when the errors are Gaussian.
The matrix argument itself only uses covariance and linear regression.

Choose the following rational constants whenever the data in (1) are rational:
\[
\theta=
\frac{4C\rho+m\rho(1-\rho)}{4C\rho+m(1-\rho)}\in(\rho,1),\qquad
B=\frac{2C}{m}\frac{\rho}{\theta-\rho},\qquad
K_{\mathrm{old}}=C\left(1+B\frac{\rho}{\theta-\rho}\right).
\tag{2}
\]
An alternative \(\theta\in(\rho,1)\) is valid if
\[
2C\left(\frac{\rho}{\theta-\rho}-\frac{\rho}{1-\rho}\right)\le m/2.
\tag{3}
\]
The choice in (2) makes (3) an equality. Define
\[
\delta_L=
\frac{2K_{\mathrm{old}}}{m}
\frac{\theta^{L+1}}{1-\theta}
\left[1+B\frac{\theta(1-\theta^L)}{1-\theta}\right]
\le K\theta^{L+1},
\tag{4}
\]
where
\[
K=\frac{2K_{\mathrm{old}}}{m(1-\theta)}
\left(1+B\frac{\theta}{1-\theta}\right).
\tag{5}
\]

**Theorem.** For every subset \(S\),
\[
\|\mathcal C_L-I\|_2\le\delta_L,\qquad
(1-\delta_L)R_{SS}^{-1}\preceq Q_L
\preceq(1+\delta_L)R_{SS}^{-1}.
\tag{6}
\]
The statements are vacuous for an empty subset. If \(L\ge n-1\), the
construction is exact and one can replace \(\delta_L\) by zero. The lower
precision inequality becomes useful when \(\delta_L<1\). The quantities
\(\theta,B,K_{\mathrm{old}}/m,K\), and \(\delta_L\) depend only on
\(C/m\) and \(\rho\), with the common covariance scale cancelled.

## 2. Weighted conjugation and regression localization

First consider any principal block matrix \(R_{HH}\), with \(H\) an arbitrary
subset of calendar times. Let \(W\) be block diagonal, with scalar positive
weights satisfying
\[
|W_i/W_j-1|\le\theta^{-|i-j|}-1.
\]
Weights \(W_i=\theta^{-|i-j_0|}\), or \(W_i=\theta^{-(t-i)}\) on a history
strictly preceding \(t\), have this property in both orientations.
Diagonal blocks of
\(E=W^{-1}R_{HH}W-R_{HH}\) vanish. Every row and every column of the scalar
matrix of block operator norms therefore has sum at most
\[
2C\sum_{h\ge1}\rho^h(\theta^{-h}-1)
=2C\left(\frac{\rho}{\theta-\rho}-\frac{\rho}{1-\rho}\right)
\le m/2.
\tag{7}
\]
There is at most one calendar block at each positive distance on each side;
deleting candidates only reduces this bound. The block Schur estimate gives
\(\|E\|_2\le m/2\): apply the scalar matrix of block norms to the vector of
component norms and use its row and column sums. This argument introduces no
factor depending on \(d\).

Every principal covariance satisfies \(R_{HH}\succeq mI\). A Neumann-series
inverse estimate hence yields
\[
\|(W^{-1}R_{HH}W)^{-1}\|_2\le2/m.
\tag{8}
\]
This step does not require an upper eigenvalue bound on \(R_{HH}\). In
particular, choose weights centered at block \(i\). Row \(i\), column \(j\)
of the conjugated inverse is \((R_{HH}^{-1})_{ij}\theta^{-|i-j|}\).
Equation (8) therefore proves the usual localized inverse estimate
\(\|(R_{HH}^{-1})_{ij}\|_2\le(2/m)\theta^{|i-j|}\).

For the regression bound it is cleaner to use the whole weighted row rather
than sum this inverse-block estimate. On \(H_t\), take
\(W_j=\theta^{-(t-j)}I\). Then
\[
b_tW=(R_{tH_t}W)(W^{-1}R_{H_tH_t}W)^{-1}.
\]
The horizontal row operator has norm at most the sum of its block norms, so
\[
\|R_{tH_t}W\|_2
\le C\sum_{r\ge1}(\rho/\theta)^r
=C\frac{\rho}{\theta-\rho}.
\]
Equation (8) proves
\[
\|b_{tj}\|_2\le B\theta^{t-j},\qquad j\in H_t.
\tag{9}
\]
This is a bound for the true local regression on \(H_t\), not a truncation
of full-history regression coefficients. Naively convolving individual
inverse-block bounds is a different proof and does not immediately give the
constant \(B\) in (2).

## 3. Old covariances and overlapping histories

If \(j<t-L\), every \(u\in H_t\) satisfies \(u>j\). Thus (1) and (9) give
\[
\begin{aligned}
\|\operatorname{Cov}(Z_t,Y_j)\|_2
&\le C\rho^{t-j}
 +BC\sum_{u\in H_t}\theta^{t-u}\rho^{u-j}\\
&\le C\theta^{t-j}
 \left[1+B\sum_{r\ge1}(\rho/\theta)^r\right]
 =K_{\mathrm{old}}\theta^{t-j}.
\end{aligned}
\tag{10}
\]
For \(j\in H_t\), the covariance is exactly zero by regression orthogonality.

Consider selected \(s<t\), with \(h=t-s\). The residual pair is
\[
\operatorname{Cov}(Z_t,Z_s)
=\operatorname{Cov}(Z_t,Y_s)
-\sum_{j\in H_s}\operatorname{Cov}(Z_t,Y_j)b_{sj}^T.
\tag{11}
\]
When \(h>L\), all terms in (11) concern old observations, yielding
\[
\|\operatorname{Cov}(Z_t,Z_s)\|_2
\le K_{\mathrm{old}}\theta^h
\left[1+B\sum_{d=1}^{L}\theta^{2d}\right].
\tag{12}
\]
When \(1\le h\le L\), the direct term vanishes. Terms with
\(j\ge t-L\) also vanish; the remaining terms have
\(L+1-h\le d=s-j\le L\). Consequently,
\[
\|\operatorname{Cov}(Z_t,Z_s)\|_2
\le\frac{K_{\mathrm{old}}B}{1-\theta^2}
\theta^{2L+2-h}(1-\theta^{2h}).
\tag{13}
\]
This retains the overlapping-history cross terms. Recent residuals need not be
uncorrelated merely because their observation times are within the window.

Every local conditional covariance satisfies \(D_t\succeq mI\). One direct
proof is the Schur-complement variational formula: for a fixed vector \(v\),
\(v^TD_tv\) is the minimum of the quadratic form of \(R_{\{t\}\cup H_t}\)
over vectors whose \(t\)-block is \(v\). That minimum is at least
\(m\|v\|_2^2\).

Block normalization therefore multiplies the off-diagonal bounds by at most
\(1/m\). Sum (12) for \(h>L\) and (13) for \(1\le h\le L\), then account
for both sides of a row. The finite geometric sums give exactly (4). The scalar
matrix of normalized block operator norms is symmetric, has zero diagonal,
and has row sums at most \(\delta_L\). The same block Schur estimate proves
the first inequality in (6).

Finally set \(T=D_L^{-1/2}A_LR_{SS}^{1/2}\). The matrices
\(TT^T=\mathcal C_L\) and \(T^TT=R_{SS}^{1/2}Q_LR_{SS}^{1/2}\) have the
same eigenvalues. Congruence gives the precision sandwich in (6). This proves
the theorem.

## 4. Supplied rational block metrics

The theorem also applies after a supplied block diagonal change of metric,
without computing irrational square roots. Let each \(V_t\succ0\) be rational,
put \(V=\operatorname{diag}(V_t)\), and suppose
\[
R\succeq mV,\qquad
\begin{pmatrix}
C\rho^{|t-s|}V_t&R_{ts}\\
R_{st}&C\rho^{|t-s|}V_s
\end{pmatrix}\succeq0\quad(t\ne s).
\tag{14}
\]
After the conceptual whitening \(R'=V^{-1/2}RV^{-1/2}\), these are exactly
\(R'\succeq mI\) and
\(\|V_t^{-1/2}R_{ts}V_s^{-1/2}\|_2\le C\rho^{|t-s|}\). They can be checked
through rational positive-semidefinite tests in the original coordinates.

Compute all local regressions, conditional covariances, and information
increments directly with the original rational \(R\) and sensitivities.
They transform covariantly under whitening, so the precision sandwich returns
to the original coordinates by congruence. Even the normalized residual norm
is unchanged: the two normalized residual maps differ by a block orthogonal
matrix, since each transformed covariance is
\(D'_t=V_t^{-1/2}D_tV_t^{-1/2}\). No square roots enter an implementation.
The matrices \(V_t\) may have unbounded Euclidean condition numbers.

## 5. Fixed partial observations of a latent state

One concrete extension beyond the earlier Kalman gain proof is
\[
X_t=A_tX_{t-1}+w_t,\qquad Y_t=H_tX_t+v_t,
\]
with the usual independent centered initial state, process innovations, and
observation noises. Suppose
\[
\|A_t\|_2\le\rho<1,\quad
\operatorname{Cov}(X_t)\preceq\overline P I,\quad
\|H_t\|_2\le\overline H,\quad
\operatorname{Cov}(v_t)\succeq mI.
\]
The latent-state dimension and the observed-packet dimension may differ.
The observation covariance satisfies \(R\succeq mI\), and, for \(t>s\),
\[
R_{ts}=H_tA_t\cdots A_{s+1}\operatorname{Cov}(X_s)H_s^T,
\qquad\|R_{ts}\|_2\le\overline H^2\overline P\rho^{t-s}.
\]
Thus the theorem applies with \(C=\overline H^2\overline P\). Neither a
contractive Kalman update nor full observation of the latent state is needed.
No upper bound on the observation-noise covariance is needed either.

The selection still acquires a complete, fixed observation packet \(Y_t\).
This does not permit independently selecting its coordinates: that different
combinatorial problem retains the hardness boundary documented in the
[full-block approximation note](research-20260912-full-block-design-fptas.md).

## 6. Inherited weighted-trace approximation scheme

Fix a rational \(0<\rho<1\) and a rational upper bound on \(C/m\).
The positive rational constants \(m,C\), rational accuracy
\(0<\epsilon<1\), and, when used, rational block metrics are supplied.
Let the rational covariance,
sensitivities \(F_t\in\mathbb Q^{d\times p}\), trace weight \(W\succeq0\),
and prior \(J_0\succeq0\) be explicitly encoded input. Both \(d\) and \(p\)
may grow with the input. The covariance promises may be (1) or their supplied
rational-metric form (14). Select exactly \(k\) complete blocks, optionally
with fixed mandatory or forbidden times, and maximize
\[
I(S)=\operatorname{tr}\{W[J_0+F_S^TR_{SS}^{-1}F_S]\}.
\tag{15}
\]
Assume the feasible family is nonempty; cardinality consistency with mandatory
and forbidden times is elementary to check.

The [previous full-block FPTAS proof](research-20260912-full-block-design-fptas.md)
applies with the new constants. For the supplied accuracy, put
\(\eta=\epsilon/2\), and select the first \(L\ge0\) satisfying
\(K\theta^{L+1}\le\eta\), capped at \(n-1\). Return immediately for an
empty candidate set or \(k=0\). At the cap, use exact full-history conditioning.
Rational powers and comparisons suffice to choose \(L\).

Each choose arc in the calendar-mask/count graph contributes the nonnegative
rational weight
\[
w(t,H)=\operatorname{tr}\{W G_{t,H}^TD_{t,H}^{-1}G_{t,H}\},\qquad
G_{t,H}=F_t-R_{tH}R_{HH}^{-1}F_H.
\]
An exact longest-path dynamic program maximizes their sum, with the fixed prior
added once. The precision sandwich implies
\((1-\eta)I(S)\le I_L(S)\le(1+\eta)I(S)\) for every schedule. Therefore the
returned schedule satisfies
\[
I(\widehat S)\ge\frac{1-\eta}{1+\eta}\max I(S)
\ge(1-\epsilon)\max I(S).
\tag{16}
\]
This remains valid when the optimum is zero.

Let \(a_0=\log2/\log(1/\theta)\). Minimality of the history length gives
\[
2^L\le\max\{1,(K/\eta)^{a_0}\}.
\]
There are \(O(n(k+1)2^L)\) graph states and arcs. Each local calculation
involves at most \(d(L+1)\) covariance coordinates. Exact rational solves,
trace calculations, path additions, and comparisons have polynomial bit
complexity in the explicit input length and \(1/\epsilon\). No state count
contains a factor exponential in \(d\) or \(p\). The supplied promises are
also polynomially checkable using rational PSD tests.

This is an FPTAS for fixed \(\rho\) and fixed \(C/m\), with polynomial degree
depending on those constants. It is not a uniform FPTAS when those conditioning
or decay parameters vary without a fixed bound. The statement covers weighted
trace of information, not trace of inverse information, multi-parameter logdet,
arbitrary side constraints, or covariance-parameter Fisher terms. The relative
precision theorem itself remains usable for D-optimal upper certificates as in
the earlier memory note; exact dynamic programming of a scalar additive objective
is what supplies the approximation scheme here.

## 7. Practical limits and verification status

The broad assumptions have a substantial cost in this proof. At
\(m=C=1\), \(\rho=0.4\), formula (2) gives
\(\theta=46/55\approx0.83636\), \(B=11/6\), and
\(K_{\mathrm{old}}=193/72\). The accuracy exponent is about 3.88, compared
with about 0.756 for the specialized Markov rate \(0.4\). The generic bound
is therefore a broader capability, not an improvement to the present Markov
benchmark calculations. The constants are not claimed optimal.

For these constants, the first windows satisfying the finite bound (4) are:

| Target relative precision error | Calendar window | Maximum masks per stage |
|---:|---:|---:|
| 0.05 | 49 | \(2^{49}\) |
| 0.01 | 58 | \(2^{58}\) |
| 0.001 | 71 | \(2^{71}\) |

These are large-horizon state-count estimates, not measured solve times. A short
horizon instead permits the exact full-history cap. This proof alone does not
provide a practical large-instance method at those constants.

A numerical spot-check used nine rationally specified non-Markov covariances
with seven times, block dimensions 2, 3, and 5, and diagonal scales 0, 1, and
1,000. Here \(m=1,C=1/2,\rho=2/5\). Each off-diagonal block was
\(C\rho^{|t-s|}E/d\), with integer entries of \(E\) in \(\{-1,0,1\}\).
The diagonal blocks were \((5/3)I+\text{scale}\,G^TG\), with entries of \(G\)
in \(\{-2,-1,0,1,2\}\). The Frobenius bound \(\|E/d\|_2\le1\) and block
diagonal dominance establish (1) for the underlying rational matrices. Values
were generated in time order, drawing the diagonal first and then lower blocks
in increasing earlier-time order, with NumPy generator seed 78192.

Floating-point evaluation of all 127 nonempty subsets and windows 0 through 6
passed 8,001 spectral checks. It also checked the regression and old-covariance
bounds. The maximum observed ratios to their respective bounds were about
0.02415 for the normalized residual norm, 0.11339 for a regression block, and
0.22806 for an old covariance block. Full-history residuals were identity to
the numerical tolerance. This is supplementary numerical evidence, not a proof
or a sharpness result. No implementation files were changed for this probe.

The root researcher is auditing primary inverse-decay and FSAI literature,
including Benzi--Tuma, Benzi--Boito--Razouk, Pilipovic--Prangoski--Zigic, and
Ajanki--Erdos--Kruger. Those sources were routed to the sole literature agent
by the root. This derivation does not assert that the general covariance theorem
or its ingredients are absent from earlier work. It identifies a precise
dimension-independent operator statement and the optimization corollary to
compare against that literature.

## 8. Two priority reductions

`design_opportunities` pointed out the following elementary reductions, which
were independently checked during this derivation. They narrow what should be
claimed as a new theoretical distinction.

First, a class-uniform full-calendar local-conditional theorem transfers to
arbitrary subsets by adding independent dummy blocks at deleted times. Keep all
original calendar indices. The covariance of the selected blocks is \(R_{SS}\),
the dummy covariance is \(mI\), and all cross covariances involving dummies are
zero. The padded matrix remains bounded below by \(mI\) and satisfies the same
off-diagonal decay promise. Conditioning on a dummy changes no selected local
regression. After a permutation, the normalized residual covariance is
\(\mathcal C_L(S)\oplus I\). Therefore uniformity over every subset is immediate
from a suitably class-uniform full-calendar theorem; it should not by itself
be presented as a novel approximation result.

Second, unbounded original diagonal blocks can be normalized before applying
older bounded-spectrum estimates. Put \(D=\operatorname{blockdiag}(R_{tt})\),
\(E=R-D\), and \(b=2C\rho/(1-\rho)\). The block Schur bound gives
\(\|E\|_2\le b\), and \(D\succeq mI\). Hence
\[
D\preceq R+bI\preceq(1+b/m)R,
\qquad R\preceq D+bI\preceq(1+b/m)D.
\]
The diagonally normalized covariance consequently satisfies
\[
\frac{m}{m+b}I\preceq D^{-1/2}RD^{-1/2}
\preceq(1+b/m)I,
\]
and its off-diagonal blocks obey the decay bound
\((C/m)\rho^{|t-s|}\). The normalization is a proof device; all local information
calculations remain rational in the original coordinates. Thus removing an upper
bound on the original diagonal is not, by itself, a barrier to applying older
bounded-condition-number theory. The block-operator norm constants and the
optimization consequence still require their own precise priority comparison.
