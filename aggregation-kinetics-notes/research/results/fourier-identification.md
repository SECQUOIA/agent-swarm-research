# Asymptotic identification of fragmentation despite additive coagulation

Date: 2026-09-07. Status: candidate extension with [independent full proof review](../reviews/fourier-identification-proof.md) complete. Transform-ratio identification is established in fragmentation inverse problems. The proposed contribution here is an exponentially vanishing error from nonlinear additive coagulation, valid without logarithmic moments, together with a precise structural identifiability statement. The [focused literature audit](../reviews/fourier-identification-literature.md) examines that narrow claim.

## 1. Setting and observed data

Use [the constant-rate additive model](general-additive-log-coupling.md): K(x,y)=λ(x+y), λ>0, selection rate σ≥0, and parent-independent daughter fraction measure B on (0,1), with total count two and first moment one. Assume a global mass-conserving weak solution with finite count N_0>0 and mass m>0. A reviewed [existence construction](additive-model-wellposedness.md) covers finite initial second moment. The estimates below themselves require only finite count and mass.

Let η_t=n_t/N(t) and nondimensionalize sizes with one fixed reference size. The observed normalized log-size characteristic function is

\[
 \phi_t(k)=\int e^{ik\log x}\eta_t(dx),\qquad k\in\mathbb R.
\]

Define

\[
 b=\lambda m,\quad \omega=(3-2\sqrt2)(b+\sigma),\quad
 a_0=\frac{\lambda M_{1/2}(0)^2}{N_0},\quad
 \psi(k)=\sigma\int_{(0,1)}(\theta^{ik}-1)B(d\theta).
\tag{1}
\]

The function ψ is the characteristic exponent of the pure-fragmentation log process, whose jump measure is ν=σ(log)_#B on (−∞,0). Here ν has total mass 2σ. No initial or daughter logarithmic moment is assumed. Characteristic functions and ψ are nevertheless continuous on the real line.

The identifiability conclusion uses ideal exact observations of η_t for arbitrarily late times, and additionally the count growth and mass to recover λ. It is not a finite-data statistical consistency or stability theorem.

## 2. An exponentially accurate Fourier factorization

The normalized bounded-test equation gives, for every real k,

\[
 \partial_t\phi_t(k)=\psi(k)\phi_t(k)+r_t(k),
\]
\[
 r_t(k)=\frac{\lambda}{N(t)}\iint x
 \left[e^{ik\log(x+y)}-e^{ik\log x}\right]n_t(dx)n_t(dy).
\tag{2}
\]

The identity is understood in its absolutely continuous, time-integrated form. Since |e^(ikz)−e^(ikw)|≤|k||z−w| and log(1+y/x)≤sqrt(y/x), the Hellinger-affinity estimate proves

\[
 |r_t(k)|\le |k|\frac{\lambda M_{1/2}(t)^2}{N(t)}
 \le |k|a_0e^{-\omega t}.
\tag{3}
\]

For any real k with δ(k)=ω+Re ψ(k)>0, define

\[
 C(k)=\phi_0(k)+\int_0^\infty e^{-s\psi(k)}r_s(k)ds.
\tag{4}
\]

The integral converges absolutely. Variation of constants gives

\[
 \boxed{\quad
 \left|\phi_t(k)-e^{t\psi(k)}C(k)\right|
 \le D(k)e^{-\omega t},\qquad
 D(k)=\frac{|k|a_0}{\delta(k)}.\quad}
\tag{5}
\]

In particular

\[
 e^{-t\psi(k)}\phi_t(k)=C(k)+\varepsilon_t(k),
 \qquad |\varepsilon_t(k)|\le D(k)e^{-\delta(k)t}.
\tag{6}
\]

There is an interval I containing zero on which δ is bounded below by a positive constant, C is continuous, and |C| is bounded below by a positive constant. Indeed ψ(0)=0 and ψ is continuous. On a sufficiently small compact interval, (6) gives uniform convergence of the continuous functions e^(−tψ)φ_t to C. Thus C is continuous and C(0)=1; shrinking the interval gives nonvanishing.

This factorization includes a generally nontrivial amplitude C(k) determined by the initial distribution and accumulated nonlinear interactions. It does not assert that C is a characteristic function or an independent random shift. Its role is to cancel between observation times.

## 3. Late-time ratios identify the fragmentation exponent

Fix an observation lag h>0. For k in a sufficiently small interval I, the denominator φ_t(k) is nonzero for all sufficiently large t, and

\[
 \boxed{\quad
 \frac{\phi_{t+h}(k)}{\phi_t(k)}\longrightarrow e^{h\psi(k)}.
 \quad}
\tag{7}
\]

For t such that D(k)e^(−δ(k)t)≤|C(k)|/2, direct division of (6) gives

\[
 \left|\frac{\phi_{t+h}(k)}{\phi_t(k)}-e^{h\psi(k)}\right|
 \le \frac{2D(k)}{|C(k)|}
       e^{h\operatorname{Re}\psi(k)}
       (1+e^{-\delta(k)h})e^{-\delta(k)t}.
\tag{8}
\]

Convergence is uniform on a sufficiently small compact interval around zero, using uniform bounds on δ, D, and |C|. At k=0 the ratio is exactly one.

The phase ambiguity in taking a logarithm is removed locally by continuity: choose I small enough that |h Im ψ(k)|<π and e^(hψ(k)) stays near one. The continuous logarithm equal to zero at k=0, equivalently the principal logarithm on a suitably small interval, then gives

\[
 \psi(k)=\frac1h\log\left[
 \lim_{t\to\infty}\frac{\phi_{t+h}(k)}{\phi_t(k)}\right],\qquad k\in I.
\tag{9}
\]

A fixed change in the reference size multiplies both characteristic functions by the same phase and cancels in the ratio. An unknown initial distribution also cancels through C. Neither cancellation removes measurement error.

## 4. Why local frequencies determine all daughter fractions

**One-sided uniqueness lemma.** Let ν_1,ν_2 be finite measures on (−∞,0). If

\[
 \int(e^{iky}-1)\nu_1(dy)
 =\int(e^{iky}-1)\nu_2(dy)
\]

on a nonempty open real interval, then ν_1=ν_2.

**Proof.** Write Δ=ν_1−ν_2 and μ=Δ−Δ(ℝ)δ_0. This is a finite signed measure on (−∞,0], and its Fourier transform vanishes on the given interval. The transform

\[
 f(z)=\int e^{izy}\mu(dy)
\]

is holomorphic for Im z<0 and continuous up to the real boundary. Finiteness of μ gives boundary continuity. Holomorphy follows by differentiating on compact subsets of the lower half-plane; exponential damping controls every power of |y| there, without moments of μ. The boundary values are zero on the interval. Schwarz reflection across a smaller segment extends f holomorphically, with zero values on that segment, so the identity theorem gives f=0 throughout the lower half-plane. Boundary continuity and Fourier uniqueness imply μ=0. Restricting to (−∞,0) then gives Δ=0. ∎

Therefore (9) determines the entire finite jump measure ν. If σ>0, it determines

\[
 \sigma=\tfrac12\nu(({-\infty},0)),\qquad
 B=\sigma^{-1}(\exp)_\#\nu.
\tag{10}
\]

If σ=0, the data identify that zero rate, but cannot identify an unused daughter law. The exclusion of a jump at zero matters: an atom at log θ=0 is invisible in e^(iky)−1. Our model assumes strictly smaller positive daughters.

**Qualification, 2026-09-07.** Strict reduction is not necessary for algebraic identification when both daughter count and mass are known. If one hypothetically allows B on (0,1] with total count two and first moment one, the local exponent identifies the visible measure ν_-=σ(log)_#(B restricted to (0,1)) by the same one-sided lemma. The bounded integral and count constraint give

\[
 \sigma=\int_{(-\infty,0)}(1-e^y)\nu_-(dy),\qquad
 z:=\sigma B(\{1\})=2\sigma-\nu_-(\mathbb R).
\]

For σ>0, these determine B=σ^(-1)[(exp)_#ν_-+zδ_1], including the atom invisible to the exponent alone. This qualification does not extend the forward solution framework used in this note.

The known mass identity supplies a second expression, interpreted through the unique analytic continuation:

\[
 \psi(-i)=\sigma\int(\theta-1)B(d\theta)=-\sigma.
\tag{11}
\]

This is an identity for the identified exponent, not a prescription for evaluating noisy real-frequency observations at a complex argument.

Finally, from the observed unnormalized count growth

\[
 r_N=\frac{\log N(t+h)-\log N(t)}h=\sigma-\lambda m,
\]

and known conserved mass m, the coagulation coefficient is

\[
 \lambda=\frac{\sigma-r_N}{m}.
\tag{12}
\]

In the count-neutral case r_N=0 this separates the common activity level from the stationary bulk count. The additional mass and count information in (12) must not be inferred from normalized characteristic functions alone.

## 5. What the theorem does and does not establish

The result gives structural identifiability of both kinetic rates and the expected daughter fraction measure from ideal late-time size-distribution traces, count growth, and mass. It does not identify daughter-pair dependence beyond the expected daughter measure; the population balance never contains that additional information.

Transform methods and ratio inversion are established in fragmentation research. The claim being investigated is that nonlinear additive coagulation contributes an exponentially small ratio error on a nonempty low-frequency interval, even though total expected coagulation activity persists. The proof uses the integrable nonlinear log-displacement estimate, not a claim that the full population stops coagulating.

Equation (8) bounds deterministic model bias. At fixed nonzero k, |φ_t(k)| may decrease exponentially, so measurement errors are amplified by division. The uniqueness argument then uses analytic continuation from an interval and supplies no stability estimate. Arbitrarily late observation is therefore not asserted to improve practical reconstruction. A finite-sample method would need a noise model, a choice of observation window and frequencies, and regularization assumptions. Those are outside this theorem.

Independent proof and literature reports are maintained separately. The pure-fragmentation endpoint of (7) is already immediate from its established transform solution; it is not a new result here.

## 6. Closest precedents and relevance

[Garnier (2024), Section 2.2](https://arxiv.org/html/2405.10588v1), explicitly cancels an unknown factor by taking characteristic-function quotients at two times and uses a distinguished logarithm for decompounding. The cancellation in (7) is the same algebra. Here the factor arises asymptotically from nonlinear coagulation, may not be a characteristic function, and comes with the proved error (8).

The exact pure-fragmentation transform evolution is already given in [Doumic and Escobedo (2016), Equations (12)–(14)](https://arxiv.org/pdf/1510.03588). Mellin inversion from asymptotic and short-time population distributions appears in [Doumic, Escobedo, and Tournus (2018)](https://www.numdam.org/item/10.1016/j.anihpc.2018.03.004.pdf) and [their 2024 article](https://www.numdam.org/item/10.5802/ahl.207.pdf). The latter traces inverse breakage research to Ramkrishna's work. His population-balance text also treats recovery of breakage and aggregation rates from dynamic distributions. The relevance here is a rigorous recovery statement while both mechanisms remain active, rather than a new inverse-problem motivation.

Actual coagulation–fragmentation daughter-law estimation from time-dependent histograms is studied by [Mirzaev, Byrne, and Bortz (2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5352987/). Their consistency framework assumes identifiability; this note supplies a specific structural result and quantitative asymptotic factorization for the additive model. The literature audit records further comparisons and the limits of the search.

An independently checked [sampling-error application](fourier-sampling-tradeoff.md) gives a finite-time certificate under an explicit independent-sampling model. It concerns a fixed Fourier ratio, not stable recovery of the whole daughter measure.
