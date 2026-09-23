# Initial-rate tomography and exact bulk-observation blind spots

Research note, 2026-09-06. Status: algebraically verified candidate results; independent review recorded below. The basic polarization and fixed-concentration gauge are established quadratic-mixture algebra, not a defensible novelty claim. The complete classification of population-balance mechanisms invisible on a conserved-mass preparation shell is the strongest result retained here. Its novelty remains unconfirmed.

## 1. Model and observation

Let \(n_t\) be a finite nonnegative measure on particle masses \(x>0\). Write \(N=\int n\) and \(M=\int x n\). Binary coagulation has symmetric nonnegative kernel \(K(x,y)\). Binary fragmentation has event rate \(S(x)\), and any daughter measure supported in \((0,x)\), with daughter count two and total daughter mass \(x\). The weak equation implies

\[
\dot N=\int S(x)n(dx)-\tfrac12\iint K(x,y)n(dx)n(dy),\qquad \dot M=0. \tag{1}
\]

The identities require a mass-conserving solution and finite displayed integrals. The results below are conditional on these standard forward properties. There is no claim that count data identify the daughter distribution. Source, death, and number-changing boundary fluxes are excluded in Sections 2–3.

## 2. A complete blind class for experiments with fixed initial mass

**Theorem 1 (universal count neutrality at fixed material loading).** Fix \(m>0\). Suppose \(K\) is symmetric and finite pointwise. The following are equivalent:

1. For every finitely supported nonnegative initial measure \(n\) with \(\int x n=m\), the right side of (1) is zero.
2. There is a function \(d\) such that

\[
K(x,y)=x d(y)+y d(x),\qquad S(x)=m d(x). \tag{2}
\]

If the model is physical, \(S\ge0\) forces \(d\ge0\). For every mass-conserving solution of (2) with initial mass \(m\),

\[
N(t)=N(0) \quad\text{for all times of existence}. \tag{3}
\]

Thus observing number, total mass, and mean mass at every time, for every initial size distribution having the same material loading, cannot distinguish this entire class from a static population.

**Proof.** Substitute the monodisperse preparation \(n=(m/x)\delta_x\) into the zero-rate condition. This gives
\(S(x)=mK(x,x)/(2x)\). Define \(d(x)=S(x)/m\). For two distinct masses, use
\(n=\frac{m}{2x}\delta_x+\frac{m}{2y}\delta_y\). Substituting the diagonal identities gives \(K(x,y)=x d(y)+y d(x)\). The diagonal is already covered. Conversely, (2) gives

\[
\dot N=(m-M(t))\int d(x)n_t(dx)=0.
\]

This proves necessity, sufficiency, and the exact-time statement. No inference from an initial derivative to a full trajectory is made without using mass conservation. □

**Corollary 1 (arbitrarily rapid invisible broadening).** Take \(d(x)=\lambda\ge0\), hence \(K(x,y)=\lambda(x+y)\), \(S(x)=\lambda m\), and let each fragmentation split a particle into two equal halves. If the initial second moment is finite, then

\[
M_2(t)=M_2(0)e^{3\lambda m t/2},\qquad N(t)=N(0),\quad M(t)=m. \tag{4}
\]

Indeed coagulation contributes \(2\lambda M M_2\), and equal splitting contributes \(-\lambda m M_2/2\). Consequently no bound on second-moment prediction error in terms only of errors in these three bulk outputs can hold uniformly over this class: the output errors are exactly zero while the second-moment discrepancy can be arbitrarily large. This is an identifiability statement, not a claim of finite-time gelation; (4) is finite at every finite time for fixed \(\lambda\).

The broadening conclusion is robust to the expected daughter law. If the daughter measure has count two, first moment $x$, and support in $(0,x)$, Jensen's inequality and $z^2\le xz$ give $x^2/2\le\int z^2 b_x(dz)\le x^2$. Thus for the same additive kernel and constant fragmentation rate, $3\lambda m M_2/2\le\dot M_2\le2\lambda m M_2$. Equal splitting attains the lower exponent. An actual complementary binary split is not required for this deterministic bound.

**Manuscript correction, 2026-09-07.** The original paragraph unnecessarily required an eventwise binary split. The expected count and mass constraints suffice, as shown above. Stage 4 of the [manuscript](../../paper-additive-coagulation/main.pdf) also justifies both unbounded moment balances under a locally bounded second moment and improves the entropy-production coefficient below to the sharp value $\log 2$. Its tangent-truncation proof and initial right-derivative sharpness passed five independent manuscript reviews. The original weaker entropy derivation below is retained as development history.

**Corollary 2 (entropy-moment certificate).** For the same additive-kernel family with $\lambda>0$, set $H=\int x\log x\,dn$. Whenever its weak balance is justified, in particular under suitable propagation of the finite $x\log^+x$ moment,

$$
\dot H\ge (1-\log 2)\lambda m^2>0.
$$

To see this, let $h(p)=-p\log p-(1-p)\log(1-p)$. A merger of $x,y$ changes $x\log x$ by $(x+y)h(x/(x+y))$. The elementary inequality $h(p)\ge2p(1-p)$ gives coagulation production at least $\lambda m^2$. Any binary split loses at most $x\log2$, giving fragmentation production at least $-\lambda m^2\log2$. This excludes a stationary state with finite $x\log^+x$ moment and a valid weak entropy balance. It does not exclude stationary laws having infinite logarithmic moment, dust, or mass at infinity. The general inequality was independently derived by the reviewer and checked directly here; a manuscript would still need the truncation argument that justifies this unbounded test function in the chosen solution class.

**Practical implication.** Changing the initial size distribution while keeping total solids or dispersed volume fixed does not resolve this ambiguity, even if this changes number concentration. Diluting the same shape changes total mass and breaks the cancellation. This distinction matters when describing “multiple concentrations” as an identifiability intervention.

## 3. Fixed number and fixed mass: the finite preparation theorem

There is a general algebraic form that includes both count and material-loading constraints. Let \(C\in\mathbb R^{r\times q}\) have full row rank, let \(h\ne0\), and assume the preparation shell
\(\{z\in\mathbb R^q:z>0,\ Cz=h\}\) is nonempty. Let \(K=K^T\) and define \(R(z)=s^Tz-z^TKz/2\).

**Theorem 2.** \(R\) vanishes on this shell if and only if there exists \(A\in\mathbb R^{r\times q}\) such that

\[
K=C^TA+A^TC,\qquad s=A^Th. \tag{5}
\]

In particular, every invisible kernel matrix has rank at most \(2r\). This rank bound concerns the matrix restricted to the selected preparation states; it is not a statement that arbitrary low-rank kernels are invisible.

**Proof.** A quadratic polynomial vanishing on a relatively open affine set vanishes on its entire affine hull. Its quadratic part restricted to \(V=\ker C\) therefore vanishes, and polarization gives \(v^TKw=0\) for all \(v,w\in V\). Decomposing \(\mathbb R^q=V\oplus V^\perp\) shows that a symmetric matrix with zero \(V\)-to-\(V\) block has the form \(C^TA+A^TC\): the mixed block and half of the complementary diagonal block define \(A\). On \(Cz=h\), the residual becomes \((s-A^Th)^Tz\). Its vanishing implies \(s-A^Th=C^T\gamma\), where \(\gamma^Th=0\). Set
\[
B=\frac{h\gamma^T-\gamma h^T}{h^Th}.
\]
Then \(B^T=-B\), \(B^Th=\gamma\). Replacing \(A\) by \(A+BC\) keeps \(K\) unchanged and makes \(A^Th=s\). The converse follows by substitution. □

For \(C\) with rows \(1\) and \(x\), and \(h=(c,m)^T\), the continuous sufficient construction is

\[
K(x,y)=a(x)+a(y)+x d(y)+y d(x),\quad S(x)=c a(x)+m d(x). \tag{6}
\]

Equation (1) becomes
\(\dot N=(c-N)\int a\,dn+(m-M)\int d\,dn\). Thus, when \(N(0)=c\) and \(M(0)=m\), count stays constant. Nonnegative \(a,d\) ensure physical rates. Bounded \(a,d\) give bounded fragmentation rates and at-most-linear coagulation kernels. The finite preparation theorem proves completeness on any selected grid with an interior feasible composition; it does not by itself establish a continuum representation theorem for two simultaneous constraints.

## 4. Fixed-concentration gauge and its removal

Allow a count source \(J\), and replace \(S\) by the net single-particle number production rate \(b\). Preparing \(n_0=cp\), where \(p\) is a probability measure, gives the initial rate

\[
r(c,p)=J+c\int b\,dp-\frac{c^2}{2}\iint K\,dp\,dp. \tag{7}
\]

For known \(J\), two symmetric models agree at every composition \(p\) at one fixed \(c\) if and only if their differences satisfy

\[
\Delta K(x,y)=a(x)+a(y),\qquad \Delta b(x)=c a(x). \tag{8}
\]

Monodisperse and equal-bidisperse preparations prove this directly. Two distinct positive concentrations, using the same composition family and unchanged rates, remove (8). With unknown \(J\), two concentrations \(c_1,c_2\) leave the one-dimensional algebraic gauge

\[
\Delta J=\delta,\quad
\Delta b=-\delta(c_1^{-1}+c_2^{-1}),\quad
\Delta K=-2\delta/(c_1c_2). \tag{9}
\]

A third concentration removes it. Physical nonnegativity can restrict or collapse the allowable interval in (9); nonuniqueness within the positive model class should not be asserted unconditionally at boundary points. Antisymmetric kernels are always invisible to (7), which is why symmetry is an explicit assumption.

For concentrations \(c\) and \(2c\), the particularly simple reconstruction is

\[
K(x,y)=\frac{r(c,\delta_x)+r(c,\delta_y)-r(2c,(\delta_x+\delta_y)/2)-J}{c^2}, \tag{10}
\]
\[
b(x)=\frac{4r(c,\delta_x)-r(2c,\delta_x)-3J}{2c}. \tag{11}
\]

At \(q\) selected masses, this requires \(q\) monodisperse rates at \(c\) and \(q(q+1)/2\) equal-mixture rates at \(2c\), counting repeated masses. The total equals the number of unknown parameters \(q+q(q+1)/2\), and is minimal among scalar initial-rate measurements on an unrestricted open parameter set: the measurement map is linear in those parameters and fewer scalar equations cannot be injective. Unknown \(J\) needs one additional measurement, since for any reference mass

\[
J=3r(c,\delta_x)-3r(2c,\delta_x)+r(3c,\delta_x).
\]

This is a measurement-count bound, not an optimality theorem for noise, cost, finite-time data, or nonlinear trajectory observations.

## 5. Noise and short-time limits

With exact \(J\), if each rate in (10) has absolute error at most \(\varepsilon\), then \(|\widehat K-K|\le3\varepsilon/c^2\). Formula (11) gives \(|\widehat b-b|\le5\varepsilon/(2c)\).

Suppose a measured count at time \(t\) has deterministic error at most \(\eta\), the initial count is exact, and each of the three trajectories needed for (10) satisfies \(|N''(s)|\le B\) for \(0\le s\le t\). Replacing rates by \([N(t)-N(0)]/t\) gives

\[
|\widehat K-K|\le \frac{3}{c^2}\left(\frac{\eta}{t}+\frac{Bt}{2}\right). \tag{12}
\]

The minimizing time is \(t=\sqrt{2\eta/B}\), when this lies in the assumed validity interval. The bound becomes \(3\sqrt{2B\eta}/c^2\). If the initial count is noisy too, replace \(\eta\) by the error bound on the count difference. A uniform \(B\) is an assumption, and may increase with concentration. Therefore (12) does not justify taking concentration arbitrarily large. Finite-width seeds recover kernel averages, and localization bias must be bounded separately using a regularity assumption on \(K\).

The observation model assumes dilution preserves the kernel and linear rates. Surface chemistry, depletion, hydrodynamics, or collision-induced fragmentation can violate this. Binary collision-induced breakup is also quadratic and cannot be separated from coagulation merely by concentration scaling.

## 6. Literature and novelty audit

The local topic reviews [03](../../literature/topics/03-inverse-identifiability-observability-control.md) and [07](../../literature/topics/07-prioritized-open-questions.md) motivate mechanism separation and explicit nullspaces. They do not, by themselves, establish novelty.

- Classical quadratic mixture models already contain the finite-dimensional algebra of (8), including the removal of pure quadratic terms on the simplex. An openly accessible primary treatment is [General Blending Models for Data From Mixture Experiments](https://pmc.ncbi.nlm.nih.gov/articles/PMC4673519/). Consequently Sections 4–5 should be presented as a PBE application or supporting lemma, not as a new inverse-problem theory.
- Direct early-time aggregation-rate measurements are established, including doublet-formation methods for monodisperse colloids. See [Characterization of colloidal polymer particles through stability ratio measurements](https://www.sciencedirect.com/science/article/pii/S0032386104011668). The paper also explicitly discusses dilution changing surface chemistry. This blocks a novelty claim for initial-rate concentration separation alone.
- Constant-count, evolving-distribution coagulation–fragmentation examples are also established. The primary records are [Patil and Andrews, 1998](https://doi.org/10.1016/S0009-2509(97)00314-X), [Lage's 2002 correction](https://doi.org/10.1016/S0009-2509(02)00369-X), and [McCoy and Madras, 2003](https://doi.org/10.1016/S0009-2509(03)00159-3). The publisher records and an open modern account were inspected; the McCoy–Madras introduction explicitly distinguishes the earlier constant-count case. The older constant-kernel, linear-fragmentation examples exploit fixed mass as well as number. They prevent treating mere existence of hidden constant-count dynamics as new.
- [Tiong, Ahamed, and Ho, PBE-SPOT](https://arxiv.org/abs/2502.09010) reports confounding among mixed mechanisms under its data/library choices. Its open repository full text was searched for identifiability and sum aggregation. This was not an exhaustive comparison of the supplementary examples.
- Targeted open searches on 2026-09-06 used “coagulation identifiability concentration,” “population balance identifiability kernel experiments,” “coalescence breakage constant number of particles,” and quadratic mixture models. No directly matching statement of Theorem 1's complete fixed-mass-shell classification or Theorem 2's PBE interpretation was located in this bounded search. This is a search result, not proof that the theorems are unpublished.

**Assessment.** The exact classification and the experimental distinction between fixed material loading and same-shape dilution are useful, rigorous findings. Their proofs are short consequences of quadratic algebra and moment conservation. Impact is likely modest unless they become part of a larger observation-design theorem or experimentally validated inverse method. Do not prioritize this as a standalone high-impact publication without a substantially deeper novelty review.

## 7. Independent verification and next useful work

An independent subagent, `review_gauge`, checked symmetry requirements, (8)–(11), the sharp scalar-measurement count, positivity caveats, and the exact-time fixed-number construction. It also warned that constraining mass creates additional gauges, which motivated Theorems 1–2. The same reviewer independently confirmed the general-shell theorem, supplied the explicit skew matrix used in its proof, and independently derived the additive-kernel exponential-broadening example. The proofs in this note have also been checked by the developing agent.

Useful next work is to classify what one extra distribution-sensitive observable removes from the blind class, with realistic preparation and noise constraints. A second moment distinguishes the explicit example (4), but does not identify an arbitrary function \(d\) without more experiments. It would be incorrect to infer unrestricted mechanism recovery from that one example.
