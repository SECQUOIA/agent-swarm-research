# Independent mathematical review of the finite-dimensional PWE discrepancy

Date: 2026-10-05. Scope: the optional PWE discussion in
`AUDIT-DISCRETE.md`, the original sparse-regression notes and reviews, and
the primary source supplied by the literature owner. This is a mathematical
review, not a literature search. No experiment was rerun.

## Verdict and required qualifications

The finite-dimensional counterexample is correct. With fixed integers
`1 <= k < d`, a fixed regression vector having exactly `k` nonzero entries,
fixed positive per-entry noise standard deviation `gamma`, standard Gaussian
design, and ridge `rho = sqrt(n)`, the true support is the unique optimal
support with probability tending to one. Nevertheless, the probability of
value exactness of the interval/perspective relaxation tends to

\[
\bigl[1-2\overline\Phi(w_{\min}/\gamma)\bigr]^{d-k}<1.
\]

This contradicts Theorem 2 on journal page 72 under its printed model and
hypotheses. The contradiction holds for every pair of fixed positive
constants `c0,c1`, even if those constants depend on the fixed instance.

The proof in `AUDIT-DISCRETE.md` is sound in substance. For a submission,
make four details explicit: use one common objective normalization; derive
the certificate with weak inequalities and then exclude ties almost surely;
compute the certificate probability at the fixed true support before
conditioning on optimality; and distinguish support recovery from convex
relaxation exactness. The proof below supplies these details.

The earlier `sparse-easy-review.md` says that an added fixed beta-min/SNR
condition repairs the theorem and suggests a sharp constant `c0 = 2` for
total-energy noise. Those claims should not be carried into the manuscript.
A fixed finite SNR, however large, does not yield a probability tending to
one as `n` grows in fixed dimension. A sharp high-dimensional theorem under
a changed noise normalization is a separate result. The later
`pwe-verification.md` appropriately restricts these proposed repairs.

## Primary source and normalization

I inspected the locally supplied author-hosted, Springer-typeset primary PDF
and its extracted text:

- `/tmp/lit-bb-complexity.wGZhQj/PWE-primary.pdf`;
- `/tmp/lit-bb-complexity.wGZhQj/PWE-primary.txt`.

The literature owner supplied these files. The source is Pilanci,
Wainwright, and El Ghaoui, *Sparse learning via Boolean relaxations*,
*Mathematical Programming*, Series B 151 (2015), 63–87,
DOI `10.1007/s10107-015-0894-1`. I also visually inspected journal pages
65, 71, 72, and 82 from this PDF. Permanent source-package placement is
the literature owner's responsibility.

The relevant primary statements are:

| Location | Statement and consequence |
|---|---|
| Page 65, equation (3) | The objective is `(1/2) norm(y-Xw)^2 + (rho/2) norm(w)^2`, with `card(supp w) <= k`. There is no division of the loss by `n`. |
| Page 71, equations (19) and (20) | The interval objective is `y^T(I + rho^{-1}XD(u)X^T)^{-1}y`, over `0 <= u <= 1`, `sum u <= k`; `M=(I + rho^{-1}X_S X_S^T)^{-1}`. |
| Page 71, Corollary 2, equations (21a) and (21b) | The printed selected-support inequality is strict and the null inequality is weak, with a separating scalar called `lambda`. That scalar is a certificate threshold, not the ridge coefficient `rho`. The direct convex argument below handles the zero-probability boundary. |
| Page 72, Section 3.1 | The design entries are iid `N(0,1)` and the noise entries are iid `N(0,gamma^2)`. The experimental coefficients have absolute magnitudes of order `1/sqrt(k)`. |
| Page 72, Theorem 2 | The stated condition is `n > c0 (gamma^2 + norm(w*_S)^2) log(d) / w_min^2`, the ridge is `rho=sqrt(n)`, and the claimed exactness/integrality probability is at least `1-2 exp(-c1 n)`. |
| Pages 81–85, Appendix 7.1 | The rescaling defined on page 81 uses `1/(rho n)`, whereas the proof of Lemma 2 uses `1/rho`. Page 82 also prints the invalid operator-norm and variance bounds discussed below. |

The theorem and the accompanying model impose no `n <= d` restriction,
no `gamma_n -> 0` condition, and no condition forcing `w_min/gamma` to
diverge. The experimental relation `k=ceil(sqrt(d))` and the chosen range
of sample sizes describe experiments, not additional theorem hypotheses.
In particular, fixed `k` and coefficients exactly `1/sqrt(k)` are allowed.
Independent noise and design give a valid instance of the stated random
model.

Equations (13) and (19) omit the factor `1/2` from equation (3). The proof
below uses the same doubled normalization for the integer and relaxation
objectives. This harmless common
scaling changes neither minimizers nor exactness; it is not the source of
the counterexample. In manuscript notation the unnormalized ridge
`lambda` equals PWE's `rho`. If the loss and objective are divided by `n`,
the corresponding ridge coefficient becomes `rho/n = n^{-1/2}`. Keeping
`sqrt(n)` as the ridge after dividing only the loss by `n` would define a
different problem.

## A complete counterexample theorem

Fix `1 <= k < d`, a subset `S` of size `k`, and `w* in R^d` with support
exactly `S`. Write

\[
w_{\min}=\min_{i\in S}|w_i^*|>0.
\]

For every `n`, let `X` be an `n` by `d` matrix with independent standard
Gaussian entries, let `epsilon ~ N(0,gamma^2 I_n)` be independent of `X`,
where `gamma>0` is fixed, and set

\[
y=Xw^*+\epsilon,\qquad \rho_n=\sqrt n.
\]

For `T subseteq [d]` define

\[
F_n(T)=\min_{b\in\mathbb R^{|T|}}
 \{\|y-X_Tb\|^2+\rho_n\|b\|^2\},
\quad
P_n=\min_{|T|\leq k}F_n(T).
\]

For `K={u in [0,1]^d: sum u <= k}`, define

\[
G_n(u)=y^\top\left(I_n+\rho_n^{-1}XD(u)X^\top\right)^{-1}y,
\qquad R_n=\min_{u\in K}G_n(u).
\]

Then the probability that `S` uniquely minimizes `F_n(T)` over `|T|<=k`
tends to one, and

\[
\lim_{n\to\infty}\Pr\{R_n=P_n\}
=\bigl[1-2\overline\Phi(w_{\min}/\gamma)\bigr]^{d-k}.
\tag{PWE-FD}
\]

Here `Phi_bar(t)=Pr{Z>t}` for `Z ~ N(0,1)`.

### 1. The true support becomes the unique optimum

Finite-dimensional laws of large numbers give

\[
\frac{X^\top X}{n}\xrightarrow{\Pr}I_d,
\quad \frac{X^\top\epsilon}{n}\xrightarrow{\Pr}0,
\quad \frac{\|\epsilon\|^2}{n}\xrightarrow{\Pr}\gamma^2.
\]

Consequently `||y||^2/n -> ||w*||^2+gamma^2` and
`X_T^T y/n -> w*_T`. For every nonempty `T`, the ridge value satisfies

\[
\frac{F_n(T)}{n}
=\frac{\|y\|^2}{n}
-\left(\frac{X_T^\top y}{n}\right)^\top
 \left(\frac{X_T^\top X_T}{n}+\frac{\rho_n}{n}I\right)^{-1}
 \left(\frac{X_T^\top y}{n}\right)
\xrightarrow{\Pr}
\gamma^2+\|w^*_{S\setminus T}\|^2.
\tag{1}
\]

The formula for the empty set has a zero subtraction term and the same
limit. There are finitely many sets of size at most `k`, so the convergence
holds simultaneously over this family. Every `T != S` in the family
misses an element of `S`; its limiting gap from `S` is at least
`w_min^2`. Thus

\[
\Pr(U_n)\longrightarrow 1,
\quad
U_n=\{F_n(T)>F_n(S)\text{ for every }T\ne S,\ |T|\leq k\}.
\tag{2}
\]

Each restricted ridge fit has a unique coefficient vector because its
Hessian is positive definite. On `U_n`, the fit on `S` has no zero
coefficient, since otherwise a proper subset of `S` would have the same
value. Hence it also uniquely solves the cardinality-constrained problem.
This argument does not infer uniqueness of a nonconvex cardinality problem
from strong convexity alone.

### 2. Ridge coefficients, covariance, and the selected threshold

Write `C_n=X_S^T X_S`, `A_n=C_n+rho_n I_k`, and

\[
\widehat w_S=A_n^{-1}X_S^\top y,
\qquad
M_n=(I_n+\rho_n^{-1}X_SX_S^\top)^{-1},
\qquad r_n=M_ny=y-X_S\widehat w_S.
\]

The ridge normal equations imply the exact identity

\[
X_S^\top r_n=\rho_n\widehat w_S.
\tag{3}
\]

Conditional on `X_S`, the mean and covariance of the coefficients are

\[
\mu_n=A_n^{-1}C_nw_S^*,
\qquad
V_n=\gamma^2 A_n^{-1}C_nA_n^{-1}.
\tag{4}
\]

Since `C_n/n -> I_k` and `rho_n/n -> 0`,

\[
\mu_n\xrightarrow{\Pr}w_S^*,\qquad
nV_n\xrightarrow{\Pr}\gamma^2 I_k,
\qquad
\widehat w_S\xrightarrow{\Pr}w_S^*.
\tag{5}
\]

For completeness, the root-`n` limiting law, including the ridge bias, is

\[
\sqrt n(\widehat w_S-w_S^*)
\ \Rightarrow\ N(-w_S^*,\gamma^2 I_k).
\tag{6}
\]

Indeed, `sqrt(n)(mu_n-w*_S)=-sqrt(n)rho_n A_n^{-1}w*_S -> -w*_S`,
and conditional characteristic functions for the centered Gaussian term
converge to those of `N(0,gamma^2 I_k)` by (4) and (5).

If `a_j=x_j^T r_n` and `m_n=min_{i in S}|a_i|`, equation (3) gives

\[
\frac{m_n}{\sqrt n}
=\min_{i\in S}|\widehat w_i|
\xrightarrow{\Pr}w_{\min}.
\tag{7}
\]

### 3. The residual retains per-entry noise energy

Let `Q_n` be the orthogonal projector onto `range(X_S)`. For `n>=k`, its
rank is `k` almost surely. The signal part of the residual is

\[
q_n=M_n X_Sw_S^*
=\rho_n X_S A_n^{-1}w_S^*,
\quad
\|q_n\|^2
=\rho_n^2 (w_S^*)^\top A_n^{-1}C_nA_n^{-1}w_S^*
\xrightarrow{\Pr}\|w_S^*\|^2.
\tag{8}
\]

The matrix `M_n-I_n` vanishes on the perpendicular complement of the
column space and has operator norm at most one. Independence and
isotropy of the noise give
`||Q_n epsilon||^2/gamma^2 ~ chi_square(k)`, conditionally on `X_S`.
Therefore

\[
\|r_n-\epsilon\|
\leq\|q_n\|+\|(M_n-I_n)\epsilon\|
\leq\|q_n\|+\|Q_n\epsilon\|=O_{\Pr}(1).
\]

Together with `||epsilon||=O_Pr(sqrt(n))`, this yields

\[
\frac{\|r_n\|^2}{n}\xrightarrow{\Pr}\gamma^2,
\qquad
\frac{m_n}{\|r_n\|}\xrightarrow{\Pr}\frac{w_{\min}}\gamma.
\tag{9}
\]

### 4. Exact certificate and conditional probability

The representation

\[
G_n(u)=\max_{v\in\mathbb R^n}
 \left\{2y^\top v-\|v\|^2
       -\rho_n^{-1}\sum_j u_j(x_j^\top v)^2\right\}
\]

shows convexity in `u`. The defining matrix is positive definite, so the
function is differentiable, with

\[
\partial_jG_n(1_S)=-\frac{a_j^2}{\rho_n},
\qquad G_n(1_S)=F_n(S).
\tag{10}
\]

The point `1_S` minimizes `G_n` over `K` if and only if it maximizes the
linear form `sum_j a_j^2 u_j` over `K`. All its weights are nonnegative
and `|S|=k`; this is equivalent to

\[
\max_{j\notin S}|a_j|\leq\min_{i\in S}|a_i|=m_n.
\tag{11}
\]

This also follows directly from the supporting hyperplane in (10). If a
null index has a larger absolute correlation than a selected index, the
feasible direction `-e_i+e_j` has strictly negative directional derivative,
giving a strictly smaller relaxation value. Thus (11) is exactly the event
`E_n={R_n=F_n(S)}`, without assuming that `S` is already optimal.

Let `H_n=sigma(X_S,epsilon)`. Conditional on `H_n`, the null columns are
independent standard Gaussian vectors, while `r_n` and `m_n` are fixed.
Since `M_n` is invertible and the noise has a density, `||r_n||>0` almost
surely. Hence

\[
(a_j)_{j\notin S}\mid H_n
\sim N(0,\|r_n\|^2 I_{d-k}),
\]

and

\[
\Pr(E_n\mid H_n)
=\left[1-2\overline\Phi\left(\frac{m_n}{\|r_n\|}\right)\right]^{d-k}.
\tag{12}
\]

Any equality between a null absolute correlation and the selected threshold
has conditional probability zero. Therefore the strict selected-support
form of PWE's displayed certificate and the weak form (11) give the same
probability in this model. No deterministic claim about boundary cases is
needed.

The unstandardized null correlations share a random variance; they should
not be called unconditionally independent. Their standardized vector
`(a_j/||r_n||)_{j notin S}` has the same `N(0,I_{d-k})` conditional law
for every `H_n`, so it is exactly independent of `H_n`. In particular,
the null correlation vector divided by `sqrt(n)` converges to
`N(0,gamma^2 I_{d-k})`. It is also asymptotically independent of the
coefficient fluctuation in (6). Equation (12) needs only conditional
independence and avoids any stronger independence assumption.

The right side of (12) is bounded by one and converges in probability to
the constant in (PWE-FD), by (9) and continuity. A bounded random variable
converging in probability to a constant also converges in mean. Taking
expectations therefore proves

\[
\Pr(E_n)\longrightarrow
\bigl[1-2\overline\Phi(w_{\min}/\gamma)\bigr]^{d-k}.
\tag{13}
\]

### 5. Global exactness and the published assertion

Always `R_n <= P_n <= F_n(S)`. Thus `E_n` implies global exactness, and
on `U_n` global exactness implies `E_n`. It follows that

\[
0\leq\Pr\{R_n=P_n\}-\Pr(E_n)\leq\Pr(U_n^c)\longrightarrow0.
\tag{14}
\]

This proves (PWE-FD). It also explains why one must not first condition the
null Gaussian calculation on the event that `S` is optimal: that event
depends on the null columns. Equation (14) supplies the required transfer.

For fixed `d,k,w*,gamma`, the right side of the sample-size condition of
PWE Theorem 2 is a finite constant. The condition therefore holds for all
sufficiently large `n`, for every fixed `c0>0`. The claimed lower bound
`1-2 exp(-c1 n)` tends to one for every fixed `c1>0`, whereas (PWE-FD) is
strictly less than one. An integral relaxation optimum would imply value
exactness, so the integrality assertion is contradicted as well.

A minimal concrete choice is `d=2`, `k=1`, `w*=(1,0)`, and `gamma=1`.
The nonzero magnitude equals `1/sqrt(k)`, the sample-size condition is
`n > 2 c0 log(2)`, and the limiting exactness probability is
`1-2 Phi_bar(1)`, about `0.683`. The manuscript does not need numerical
experiments or the larger archived example to establish the contradiction.

## Reconciliation and the appendix diagnosis

No fixed beta-min/SNR assumption reconciles the printed exponential
probability bound. For fixed `d`, even a condition
`w_min^2/gamma^2 >= C log(d)` permits a finite fixed ratio; (PWE-FD) then
still gives a fixed positive failure probability. A model with shrinking
per-entry noise, growing coefficient-to-noise ratio, or a different ridge
scaling can behave differently, but none is imposed by the printed theorem.

For example, replacing the noise by iid `N(0,gamma^2/n)` changes the model.
In the same fixed-dimensional setting, (8) still holds, the perpendicular
noise energy tends to `gamma^2`, and the remaining noise in the selected
column space is negligible. The signal and perpendicular noise are
orthogonal. Consequently `||r_n||^2 -> ||w*_S||^2+gamma^2`, while
`m_n/sqrt(n) -> w_min`. The certificate ratio diverges and the exactness
probability tends to one. This is a fixed-dimensional statement about a
different model. It does not establish a sharp sample-size constant or
the published high-dimensional probability bound under that model.

The primary appendix also confirms the normalization problem identified
by the previous verifier:

1. Page 81 defines `U_j=x_j^T M y/(rho n)` and decomposes it into
   `A_j+B_j`. For the signal part on `S`,
   `A_S=n^{-1}(C_n+rho I)^{-1}C_n w*_S`, so
   `n A_S -> w*_S`. With this definition, the event in Lemma 2 (34a),
   `min_S |A_j| < w_min/4`, has probability tending to one, whereas its
   proposed bound tends to zero in this fixed instance.
2. Pages 83–85 instead analyze the signal rescaled by `1/rho`.
   That signal does converge to `w*_S`. With this scaling, however, the
   null noise term has conditional-on-design variance
   `gamma^2 ||M x_j||^2/rho^2`, which tends to `gamma^2` for a fixed null
   column. To see this last limit, `M-I` is supported on a fixed-rank
   subspace, `||Q_n x_j||^2=O_Pr(1)` by independence, and
   `||x_j||^2/n -> 1`; hence `||M x_j||^2/n -> 1`.
   Thus the exponential-in-`n` vanishing-noise bound of Lemma 1 (33)
   cannot hold with this rescaling at a fixed positive threshold.
3. Page 82 prints `sigma_max(M) <= rho^{-1}`. For `n>k`, `M` has
   eigenvalue one on the perpendicular complement of `range(X_S)`;
   its operator norm is exactly one. The valid bound is `||M||<=1`.
   The same page prints a variance bound `4 gamma^2/rho^2` for
   `x_j^T M epsilon/rho` on `||x_j||<=2 sqrt(n)`. Conditional on the
   entire design, the bound obtained from that event is
   `4 n gamma^2/rho^2=4 gamma^2`, not the displayed bound.

These appendix defects support the diagnosis, but the independent proof of
(PWE-FD) is what establishes failure of the theorem's conclusion. Avoid
claims about the validity of the whole algorithm, other theorems, later
papers, or the existence of an erratum; those questions are outside this
mathematical review.

## Recommended submission wording

Use the theorem above with its complete proof, followed by a narrow
comparison such as:

> Under the per-entry Gaussian noise model and ridge scaling stated in
> Pilanci, Wainwright, and El Ghaoui, Section 3.1 and Theorem 2 (p. 72),
> the displayed sample-size condition alone does not imply their claimed
> probability of exactness. For fixed dimension and sparsity, that condition
> holds eventually, whereas the limiting exactness probability is
> `[1-2 Phi_bar(w_min/gamma)]^(d-k)<1`, even though the optimal support
> equals the true support with probability tending to one. A shrinking-noise
> normalization gives a different statement.

If the appendix diagnosis is retained, give the exact page and equation
locators above and the corrected conditional variance. It is supplementary
to the counterexample. The contribution is the explicit limitation of the
printed Gaussian exactness claim, together with the support/certificate
distinction; do not claim that the underlying Boolean reformulation or
perspective relaxation is invalid.

## Targeted verification performed

I reconstructed the proof and covariance formulas without rerunning
experiments or querying CI. The read-only targeted commands included:

```text
cat AGENTS.md
cat paper-bb-complexity/evidence/BRIEF.md
sed -n '355,379p' paper-bb-complexity/evidence/AUDIT-DISCRETE.md
cat research-20260928b/reviews/pwe-verification.md
sed -n '515,572p' research-20260928b/bb-complexity/sparse-regression/phase-transition.md
rg -n -C 10 'PWE|Pilanci|fixed.ridge|Remark 3.5|Corollary 3.4' research-20260928b/bb-complexity/sparse-regression/stronger-relaxations/thresholds.md
sed -n '506,625p' /tmp/lit-bb-complexity.wGZhQj/PWE-primary.txt
sed -n '1201,1346p' /tmp/lit-bb-complexity.wGZhQj/PWE-primary.txt
pdftoppm -f 10 -l 10 -singlefile -scale-to 1800 -png /tmp/lit-bb-complexity.wGZhQj/PWE-primary.pdf /tmp/PWE-review-p72
pdftoppm -f 3 -l 3 -singlefile -scale-to 1400 -png /tmp/lit-bb-complexity.wGZhQj/PWE-primary.pdf /tmp/PWE-review-p65
pdftoppm -f 9 -l 9 -singlefile -scale-to 1400 -png /tmp/lit-bb-complexity.wGZhQj/PWE-primary.pdf /tmp/PWE-review-p71
pdftoppm -f 20 -l 20 -singlefile -scale-to 1600 -png /tmp/lit-bb-complexity.wGZhQj/PWE-primary.pdf /tmp/PWE-review-p82
```

Additional `rg`/`sed` reads located the supplied files and checked their
local context. `view_image` inspected the four rendered source pages.
`apply_patch` wrote only this repository review file. No web search,
download, literature API, experiment, CI query, or project-wide check was
performed.
