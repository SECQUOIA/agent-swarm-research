# Stage 1 independent review: readability and full mathematical check

I read all current manuscript `.tex` files, `references.bib`, `README.md`, and `development/COVERAGE.md`. I also inspected the Makefile, built a separate copy in `/tmp/stage1-readability-k3k9fkha`, read the resulting PDF text, and visually inspected an appendix page. I did not read other review reports or change the manuscript. This review concerns the model, fractional moments, and well-posedness appendix; the intentionally unwritten introduction and later sections are not deficiencies.

The principal mathematics appears sound. I found no major issue. The manuscript carefully separates existence under a finite second moment from estimates requiring only finite count and conserved mass. The explanation of expected daughters versus eventwise binary splitting is especially useful for population-balance readers. The interpretation of number and mass sampling, the distinction between finite-time conservation and long-time boundary limits, and the limits of instantaneous sharpness are sufficiently explicit.

## Issues requiring correction

### RDB-01 — Minor: define the perturbed weak equation and quantify the fractional order

**Location:** `sections/fractional-moments.tex:219–235`, Proposition 2.7, especially “finite-count weak solution” and equation (2.13).

**Reason:** Definition 1.2 refers to equation (1.4), which has the specific additive kernel and a size-independent selection rate. Proposition 2.7 changes both coefficients but does not explicitly say how that definition changes. Its displayed estimate also uses $p$ without explicitly restricting it to $0<p<1$. The intended interpretation is recoverable from the proof, but the proposition should specify its own mathematical framework. In particular, readers should not need to infer which factors in the weak balance are replaced or whether local boundedness of count is retained.

**Fix:** State that $K_t(x,y)$ and $S_t(x)$ are jointly measurable, and use Definition 1.2 with $\lambda(s)(x+y)$ replaced by $K_s(x,y)$ and $\sigma(s)\mathcal F_s f(x)$ replaced by $S_s(x)\mathcal F_s f(x)$. Retain the local count bound and conserved mass. Introduce the estimate with “For every $p\in(0,1)$.” No additional second-moment assumption is needed.

### RDB-02 — Minor: make the local loss bound an explicit hypothesis of the comparison setup

**Location:** `appendices/wellposedness.tex:28–48` and `66–81`, preceding Lemma A.1.

**Reason:** The general setup assumes that $\int_0^T a_s(x)\,ds$ is finite for each $x$, then says that an integrable bound uniform on each bounded size interval holds “in the application.” The given justification of (A.3), however, directly uses this stronger local uniform bound when restricting to $x\le R$. Pointwise time integrability alone does not supply it: a finite measurable function of $x$ can be unbounded on a bounded size interval. The actual additive loss rate satisfies the stronger condition, so this does not undermine the existence or uniqueness theorem, but the stated general setting and the proof should match.

**Fix:** Include the bound $\sup_{0<x\le R}a_s(x)\le h_{R,T}(s)$, with $h_{R,T}\in L^1(0,T)$, as a hypothesis of the comparison setup. That is the simplest correction and covers every use in this manuscript. Alternatively, give a different localization argument that proves (A.3) under the broader stated hypotheses.

### RDB-03 — Minor: qualify the differential count balance as holding almost everywhere

**Location:** `sections/model.tex:114–118`, equation (1.8).

**Reason:** The rates are only measurable and locally integrable. Consequently $N$ is locally absolutely continuous, and its differential equation holds almost everywhere; it need not have a derivative at every time. For example, a rate with a jump can produce a kink in $N$. Equation (2.3) correctly includes the almost-everywhere qualification for the fractional moment, so the count statement should use the same precision.

**Fix:** Write that $N$ is locally absolutely continuous and that the first equality in (1.8) holds for almost every $t$. The explicit exponential formula holds for every $t\ge0$.

### RDB-04 — Minor: identify the norm in the well-posedness theorem

**Location:** `sections/model.tex:77–78`, Theorem 1.3.

**Reason:** “Continuous in the norm (1.5)” points to an equation defining two norms, $\|\cdot\|_w$ and $\|\cdot\|_{\mathrm{var}}$. Weighted-variation continuity is the stronger conclusion needed to understand the approximation argument. The prose following the theorem resolves the ambiguity, but the theorem itself should be unambiguous.

**Fix:** Replace the phrase with “continuous in the weighted-variation norm $\|\cdot\|_w$.”

## Mathematical verification

- The pair inequality proof has the correct normalization and equality case. The monotonicity of $R(u)$, together with the endpoint conditions, supports the claimed derivative sign changes.
- The bounded fractional tests have the necessary subadditivity and daughter sign. The bound by $xy^p+yx^p$ gives time-integrable domination using only count and mass; no hidden $M_{p+1}$ hypothesis is required.
- The normalization gives exactly $-a_p b-a_{1-p}\sigma$. Monodisperse initial data with equal splitting establish the stated instantaneous sharpness, including each rate separately. The overlap identity uses the declared probability total-variation convention correctly.
- The critical exponents, fixed-window bounds, weak boundary limits, and the limits $\kappa_p/p\to\log2$ and $\kappa_p/(1-p)\to\log2$ are consistent. The moving-window conclusion does not claim the endpoint speed. The perturbed nonstationarity threshold is correctly presented as sufficient.
- In the appendix, polarization and the positive comparison operator retain the required direct-loss cancellation. The majorant balance justifies the comparison inequality without differentiating total variation. The stability coefficient requires only locally bounded second moments.
- The bounded coagulation construction preserves mass and yields the stated second- and third-moment bounds. The cutoff forcing is $O(r^{-1})$ in weighted variation under the third-moment bound. The final initial-data approximation removes the third-moment assumption through stability. Passage to bounded Borel tests is compatible with merely measurable daughters. The argument does not silently use convergence of the second moments.

## Build, references, and optional exposition

The clean isolated `make` completed successfully and produced a ten-page PDF. The final LaTeX log contains no undefined citations or references and no overfull or underfull box warnings. The inspected PDF page had readable equations and cross-references. The initial-pass unresolved-reference messages disappeared after the prescribed build sequence. No numerical reproduction is required for the current stage.

The bibliographic metadata and the limited contextual claims are consistent with the primary sources: [Cepeda's paper](https://arxiv.org/abs/1301.1934) and [Deaconu, Fournier, and Tanré's paper](https://www-sop.inria.fr/members/Etienne.Tanre/publication/AOP104.pdf). Neither citation substitutes for a missing step in the current self-contained argument.

As an optional exposition improvement, define $\langle f,\mu\rangle=\int f\,d\mu$ at first use and say explicitly that a measurable measure curve means that $t\mapsto n_t(A)$ is measurable for each Borel set $A$. A short sentence explaining that the factor $1/2$ counts unordered coagulation pairs would also help readers coming from engineering population balances. These are audience aids, not additional mathematical objections.

**Major issue count: 0. Recommendation: accept Stage 1 after the four minor corrections above.**
