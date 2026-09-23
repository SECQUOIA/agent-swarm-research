# Independent review: random-offset kinetic barriers

Reviewed 2026-09-06 by `review_localization`.

The moment transition, all displayed leading constants, and the divergence of the squared coefficient of variation in [random-kinetic-barriers.md](random-kinetic-barriers.md) are correct for the stated periodic random-offset scalar model. The estimates below justify exchanging the disorder integral and the small-diffusivity limit. They also supply the uniform intermediate asymptotic needed at the logarithmic threshold, which does not follow from a bounded-parameter fold limit alone.

This establishes mathematical validity within this compact ensemble. The additional uniform bulk estimate and transfer to finite bulk diffusion have since been proved in [review-random-finite-bulk.md](review-random-finite-bulk.md), for nonzero mean velocity and fixed positive bulk diffusivity. No novelty claim or general Gaussian disorder theorem follows.

## Model and constants

Let

\[
H_{D,c}=-D\partial_s^2+(c+\cos s)^2,
\qquad J_D(c)=\langle1,H_{D,c}^{-1}1\rangle,
\qquad c\sim\operatorname{Uniform}[-2,2],
\]

on the circle of length `2π`. Set

\[
C_0=\frac\pi2\frac{\Gamma(1/4)}{\Gamma(3/4)},
\qquad
F(\mu)=\left\langle1,[-\partial_y^2+(y^2-\mu)^2]^{-1}1\right\rangle_{\mathbb R}.
\]

The constant source in F is interpreted in the confining energy dual space. Since its potential grows quartically, weighted Cauchy–Schwarz makes that source bounded. The resolvent and its integrated value are therefore well defined even though the source is not in L² of the line.

For every `q>0`,

\[
\mathbb E J_D^q\sim
\begin{cases}
\displaystyle\frac{2^qC_0^q}{4}
 B\left(\frac12,1-\frac{3q}{4}\right)D^{-q/4},&q<4/3,\\[6pt]
\displaystyle\frac{C_0^{4/3}}{3\,2^{2/3}}D^{-1/3}\log(1/D),&q=4/3,\\[6pt]
\displaystyle2^{q-4/3}D^{1/3-q/2}\int_{\mathbb R}F(\mu)^q\,d\mu,&q>4/3.
\end{cases}
\tag{1}
\]

The middle coefficient equals `2^(1/3) C0^(4/3)/6`, as in the source note.

## 1. Canonical interval estimates

Let `F_R^B(mu)` denote the integrated resolvent of `−partial_y²+(y²−mu)²` on `(-R,R)`, with either Dirichlet or Neumann conditions. For every fixed `theta<1`, there are constants such that, for sufficiently large R and `0<=mu<=theta²R²`,

\[
F_R^B(\mu)\le C(1+\mu)^{-3/4}.
\tag{2}
\]

For `mu<=0`,

\[
F_R^B(\mu)\le C(1+|\mu|)^{-3/2}.
\tag{3}
\]

These bounds hold uniformly under artificial Neumann endpoints. The following variational proof avoids assuming pointwise resolvent tail estimates.

For bounded mu and `R>=R0`, the energy controls

\[
\int_{-R}^R(1+y^4)|f|^2.
\]

To see this, choose a fixed compact core containing all potential zeros; its mass is bounded by derivative energy plus mass on an adjacent interval where the potential is bounded below, using the anchored Poincaré argument from [the earlier localization review](review-localization.md). Outside that core the quartic potential controls the weighted mass. Weighted Cauchy–Schwarz then bounds the source functional uniformly, which bounds the integrated resolvent uniformly. It also gives an integrated source-tail estimate of order `L^(−3/2)` times the square root of the energy outside radius L.

For large positive mu, split the interval around the roots `±sqrt(mu)` into neighborhoods of radius `eta sqrt(mu)`, with a fixed small eta compatible with theta. On either root neighborhood,

\[
(y^2-\mu)^2\ge(2-\eta)^2\mu\,(y\mp\sqrt\mu)^2.
\]

Neumann bracketing and the uniformly bounded Neumann oscillator integral give a contribution `O(mu^(−3/4))` from each neighborhood. The oscillator-scaled half-length is of order `mu^(3/4)`, so the needed uniform interval bound applies. On the remaining pieces, discard derivative energy and use `integral 1/(y²−mu)²`; exclusion of the root neighborhoods makes this `O_eta(mu^(−3/2))`. This proves (2).

For `mu=-nu` with `nu>=1`, potential energy alone gives

\[
F_R^B(-\nu)\le\int_{\mathbb R}\frac{dy}{(y^2+\nu)^2}
=\frac\pi2\nu^{-3/2}.
\]

Together with the bounded-parameter estimate, this proves (3).

The same arguments on the real line show

\[
F(\mu)\sim A\mu^{-3/4}\quad(\mu\to+\infty),
\qquad A=C_0/\sqrt2,
\tag{4}
\]

\[
F(-\nu)\sim\frac\pi2\nu^{-3/2}\quad(\nu\to+\infty).
\tag{5}
\]

For (4), sandwich the potential near either root between quadratic potentials with curvatures `(2±eta)²mu`; use expanding Dirichlet and Neumann oscillator intervals; then send eta to zero. Each root contributes `C0(4mu)^(−3/4)`, so the sum has coefficient `C0/sqrt(2)`. For (5), the upper bound was just proved. Inserting the reciprocal potential `f=(y²+nu)^−2` as an energy test gives the same upper value minus `integral |f'|²=O(nu^(−9/2))`, which is a smaller error.

The positive asymptotic is also uniform in expanding intervals:

\[
\sup_{R:\,\mu\le\theta^2R^2}
\left|\frac{F_R^B(\mu)}{A\mu^{-3/4}}-1\right|\longrightarrow0
\quad(\mu\to+\infty),
\tag{6}
\]

for fixed theta<1 and sufficiently large R. In the preceding root-neighborhood proof, all local intervals fit uniformly, the oscillator lengths tend to infinity uniformly, and the complementary `O_eta(mu^(−3/2))` term is relatively negligible. This is the estimate that controls the logarithmic moment.

Finally, `F_R^B(mu)->F(mu)` uniformly on bounded parameter sets as R tends to infinity. For Dirichlet intervals this follows from energy-density and exhaustion. For Neumann intervals, the common energy bound, local weak compactness, and the `L^(−3/2)` source-tail estimate give the upper limit; the Dirichlet inclusion gives the lower limit. The reasoning is the quartic counterpart of the earlier independent quadratic proof. Continuity in bounded mu follows from convergence of the potential forms; the change in potential is bounded by a constant times `|delta mu|(1+y²)`, which the same energy controls.

## 2. Exact fold coordinate and global envelopes

Consider c near +1, put `t=1-c`, and center the wall coordinate at `s=π`. Then

\[
c+\cos s=-t+1-\cos x.
\]

Use the exact local coordinate

\[
z=2\sin(x/2),\qquad dx=w(z)dz,
\qquad w(z)=(1-z^2/4)^{-1/2}.
\]

The local potential becomes exactly `(z²/2−t)²`. On any sufficiently small fixed neighborhood, `1<=w<=w_*`, and the variational energy and source become

\[
\int\left[\frac D{w}|f_z|^2+w(z^2/2-t)^2f^2\right]dz,
\qquad\int wf\,dz.
\]

For nonnegative f, comparison of these expressions brackets the physical local integral between `w_*^(−1)` times its canonical Dirichlet integral and `w_*³` times its canonical Neumann integral. Using nonnegative tests causes no loss because the source is nonnegative and absolute value does not increase energy. The remaining wall contributes O(1), uniformly for t in a small fixed neighborhood of zero. The factor `w_*` tends to one as the neighborhood shrinks. The fold at c=−1 is identical by symmetry.

Set

\[
\ell=(4D)^{1/6},\qquad
\mu=\frac{t}{(D/2)^{1/3}},\qquad z=\ell y.
\]

The canonical integrated resolvent scales exactly as

\[
2D^{-1/2}F_R^B(\mu),\qquad R=r/\ell.
\tag{7}
\]

Choose the t-neighborhood sufficiently small relative to r² so that positive mu satisfies the root-containment condition in (2) and (6). The interval bounds imply

\[
J_D(c)\le C\begin{cases}
D^{-1/2}(1+t/D^{1/3})^{-3/4},&t\ge0,\\
D^{-1/2}(1+|t|/D^{1/3})^{-3/2},&t<0.
\end{cases}
\tag{8}
\]

The additive bounded exterior term can be absorbed into these bounds on the fixed parameter neighborhood. Away from both folds, ordinary quadratic localization gives the uniform inside bound `CD^(−1/4)`, and potential positivity gives the uniform outside bound C.

The same coordinate comparison, interval convergence at bounded mu, and shrinking-neighborhood limit give

\[
J_D(c)\sim2D^{-1/2}F(\mu)
\tag{9}
\]

uniformly when mu ranges over any fixed compact subset of the real line. This verifies the fold prefactor and the parameter scale, including the side where no zero is present.

## 3. Averaging below and above the threshold

For `|c|<1` fixed, the independently proved quadratic theorem gives

\[
D^{1/4}J_D(c)\longrightarrow2C_0(1-c^2)^{-3/4}.
\]

For `|c|>1` fixed, the same normalized quantity tends to zero. On the inside of a fold, (8) bounds its qth power by `C t^(−3q/4)`. On the outside it gives the same integrable majorant because

\[
\frac{D^{1/4}}{(|t|+D^{1/3})^{3/2}}
\le C|t|^{-3/4}.
\]

For q<4/3, dominated convergence is therefore valid over the full parameter interval. The remaining integral is

\[
\frac14(2C_0)^q\int_{-1}^1(1-c^2)^{-3q/4}\,dc
=\frac{2^qC_0^q}{4}B\left(\frac12,1-\frac{3q}{4}\right),
\]

proving the first line of (1).

For q>4/3, rescale each fold using `dc=(D/2)^(1/3)dmu`. The envelope (8), after division by the fold amplitude, is bounded by `C(1+mu)^(−3/4)` on the inside and `C(1+|mu|)^(−3/2)` on the outside. Its qth power is integrable precisely when q>4/3. Dominated convergence applies on expanding parameter intervals. Away from the folds the inside contribution is `O(D^(−q/4))`, negligible relative to `D^(1/3−q/2)` because q>4/3; the outside contribution is bounded.

There are two folds, and the disorder density is 1/4. Their total prefactor is

\[
\frac24\,2^q\,2^{-1/3}=2^{q-4/3},
\]

which proves the third line of (1).

## 4. The logarithmic threshold

At q=4/3, the positive-mu envelope is only marginally nonintegrable. The bounded-mu fold limit alone does not identify the coefficient of the logarithm. Use the uniform interval matching (6) instead.

Fix a small physical fold neighborhood and its associated positive parameter interval `0<t<t0`. Its canonical upper endpoint is `mu_max=t0(D/2)^(−1/3)`. From (2), (3), and (6),

\[
\int_{-\mu_{\max}}^{\mu_{\max}}
F_R^B(\mu)^{4/3}\,d\mu
\sim A^{4/3}\log\mu_{\max}
\sim\frac{A^{4/3}}3\log(1/D).
\tag{10}
\]

The bounded and negative-mu parts are uniformly integrable; on the positive tail, (6) gives the coefficient uniformly up to mu_max. Physical metric factors bracket this result between factors tending to one as the fixed coordinate neighborhood shrinks. The contribution outside the fixed fold neighborhoods is `O(D^(−1/3))`, which is smaller than the logarithmic term. Combining the two folds and the density gives no additional factor at q=4/3, since `2^(q−4/3)=1`. The coefficient is therefore

\[
\frac{A^{4/3}}3=\frac{C_0^{4/3}}{3\,2^{2/3}},
\]

as claimed. No uncontrolled extension of the bounded-parameter fold approximation is used.

## Consequences and other checks

At q=1, the beta and gamma identities reduce the mean coefficient to `C0²/sqrt(pi)`. At q=2,

\[
\mathbb E J_D^2\sim2^{2/3}D^{-2/3}\int F^2.
\]

The squared mean is only order `D^(−1/2)`, and is therefore negligible in the variance. In particular,

\[
\frac{\operatorname{Var}J_D}{(\mathbb EJ_D)^2}
\sim\frac{\pi\,2^{2/3}\int F^2}{C_0^4}D^{-1/6}.
\]

The Gaussian marked-zero identities in the source note also check algebraically: marked Kac–Rice weights the ordinary Gaussian slope density by its absolute value, giving the Rayleigh magnitude density and the mark-tail exponent 4/3. These are established zero-statistics consequences. The sinusoidal Gaussian amplitude-collapse counterexample is valid: the constant variational test gives `J_D>=2L/R²`, and the Rayleigh amplitude distribution has an infinite inverse-square moment, while its inverse-three-halves moment is finite. Thus the counterexample correctly prevents an unjustified general Gaussian mean theorem.

This review proves asymptotic equivalents, not rates of convergence. In particular, the apparently slow numerical convergence of the mean is not evidence against its coefficient, but a claimed specific next-order rate would require a separate expansion. The disorder moments concern differences among walls. They do not establish a long-wall stable limit or a temporal anomalous-diffusion law for individual particles.
