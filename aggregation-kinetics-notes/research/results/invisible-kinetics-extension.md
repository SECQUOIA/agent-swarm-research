# Exponential separation of number and mass under invisible kinetics

Developed 2026-09-06; independently reviewed by `review_gauge`. This extends [the inverse-design note](../ideas/inverse-design.md). Status: proved conditional on the stated mass-conserving weak solution class; novelty remains under review. The result removes the extra logarithmic or second-moment assumptions from the earlier nonstationarity argument.

## 1. Model and main theorem

Let $n_t$ be a nonnegative measure on $(0,\infty)$ with finite initial number $N>0$ and mass $m>0$. Coagulation has kernel

$$K(x,y)=\lambda(x+y),\qquad \lambda>0.$$

Fragmentation has constant per-particle selection rate $S=\lambda m$. Its daughter measure $b_x$ may depend on parent size, and satisfies

$$b_x((0,x))=2,\qquad \int_{(0,x)}z\,b_x(dz)=x.$$

An actual random split into two positive fragments satisfies these assumptions. The theorem only needs the displayed expected daughter count and mass identities. There is no source, death, growth, or boundary loss.

Assume $n_t$ is a global mass-conserving weak solution with locally finite count, for which the standard weak balance holds for bounded continuous tests, including the bounded truncations used below. This note proves the estimates for such solutions; it does not supply a new existence theorem. The coefficients are at most linear for coagulation and bounded for fragmentation, which is the standard non-gelling finite-time regime.

For a test $f$, write

$$
\frac{d}{dt}\int f\,dn_t
=\frac{\lambda}{2}\iint(x+y)[f(x+y)-f(x)-f(y)]\,dn_t(x)dn_t(y)
+\lambda m\int\left[\int f(z)b_x(dz)-f(x)\right]dn_t(x).
\tag{1}
$$

**Theorem 1.** Number remains $N$, and the half moment satisfies

$$
M_{1/2}(t):=\int\sqrt{x}\,dn_t(x)
\le M_{1/2}(0)e^{-\kappa\lambda m t},\qquad
\kappa=3-2\sqrt2>0.
\tag{2}
$$

The constant $\kappa$ is the largest possible coefficient in an estimate of this form that holds for all admissible initial measures and daughter laws: monodisperse initial data and equal splitting attain the corresponding differential inequality at time zero.

The theorem implies all of the following:

1. There is no stationary nonzero measure on $(0,\infty)$ with finite number and finite positive mass for this model.
2. For every $\varepsilon,R>0$,

$$
n_t([\varepsilon,\infty))
\le\frac{M_{1/2}(0)}{\sqrt\varepsilon}e^{-\kappa\lambda mt},
\qquad
\int_{(0,R]}x\,dn_t(x)
\le\sqrt R M_{1/2}(0)e^{-\kappa\lambda mt}.
\tag{3}
$$

3. As measures on $[0,\infty)$, $n_t$ converges weakly to $N\delta_0$. Meanwhile the mass probability measures $x n_t(dx)/m$ leave every bounded size interval. Their weak limit on the one-point compactification $[0,\infty]$ is $\delta_\infty$.

These are long-time conclusions. They do not assert finite-time shattering or gelation. At each finite time the assumptions preserve all number and mass. The apparent paradox disappears because the small population of very large particles carries nearly all the mass, while nearly all particles have very small mass.

## 2. Proof of Theorem 1

The count equation is

$$N'(t)=-\lambda M_1(t)N(t)+\lambda m N(t)=0.$$

Cauchy–Schwarz gives $M_{1/2}(t)\le\sqrt{Nm}$, so the test used below requires no moment beyond number and mass.

### Sharp pair inequality

For all $x,y>0$,

$$
(2-\sqrt2)(x\sqrt y+y\sqrt x)
\le(x+y)[\sqrt x+\sqrt y-\sqrt{x+y}]
\le x\sqrt y+y\sqrt x.
\tag{4}
$$

To prove it, set $a=\sqrt x$, $b=\sqrt y$, and
$t=\sqrt{a^2+b^2}/(a+b)\in[1/\sqrt2,1)$. Rationalization gives the ratio of the middle expression to $ab(a+b)$ as

$$\frac{2t^2}{1+t}.$$

This is increasing in $t$. Its minimum is $2-\sqrt2$, attained at $a=b$, and its supremum is $1$. Therefore coagulation's contribution to the half-moment derivative is at most

$$-\lambda(2-\sqrt2)mM_{1/2}(t).$$

For fragmentation, Cauchy–Schwarz against $b_x$ gives

$$\int\sqrt z\,b_x(dz)\le\sqrt{2x},$$

so its contribution is at most $\lambda m(\sqrt2-1)M_{1/2}(t)$. Adding these bounds gives

$$M_{1/2}'\le-\kappa\lambda mM_{1/2}.$$

Gronwall's inequality proves (2). Both inequalities become equalities for an initially monodisperse population undergoing equal splitting. A larger uniform decay coefficient would already fail at time zero.

### Justification of the unbounded test

Use $f_R(x)=\min\{\sqrt x,R\}$ in the time-integrated weak equation. It is increasing, concave, subadditive, and bounded. Its coagulation loss obeys

$$
0\le f_R(x)+f_R(y)-f_R(x+y)\le\min\{\sqrt x,\sqrt y\}.
$$

Consequently its product with $\lambda(x+y)$ is bounded by
$\lambda(x\sqrt y+y\sqrt x)$, whose double integral is $2\lambda mM_{1/2}\le2\lambda m\sqrt{Nm}$.

Also $0\le\int f_R\,db_x-f_R(x)\le\sqrt{2x}$. The lower bound follows from the fact that $f_R(z)/z$ is nonincreasing and $z<x$, together with daughter-mass conservation. The upper bound follows from $f_R\le\sqrt{\cdot}$. These provide integrable bounds uniform in $R$ on every finite time interval. Dominated convergence passes the integrated identity to $f(x)=\sqrt x$. It also establishes absolute continuity of $M_{1/2}$ and justifies the differential inequality almost everywhere.

If a stationary measure existed, this identity and (2) would give $M_{1/2}=0$, contradicting positive mass. The estimates (3) follow from $\sqrt x\ge\sqrt\varepsilon$ on $[\varepsilon,\infty)$ and $x\le\sqrt R\sqrt x$ on $(0,R]$. The weak convergence statements follow by splitting bounded continuous tests at $\varepsilon$ or $R$. □

## 3. Two observed moments rule out universally hidden physical kinetics

Fix a material loading $m>0$. Consider arbitrary nonnegative symmetric coagulation kernel $K$ and nonnegative fragmentation selection rate $S$, with expected daughter count two and conserved daughter mass. Suppose that for **every finitely supported initial population of mass $m$**, both the count derivative and the half-moment derivative vanish.

**Theorem 2.** Then $K=0$ and $S=0$ pointwise. The same conclusion follows if the second-moment derivative replaces the half-moment derivative.

**Proof.** Universal count neutrality gives, by the classification in the [earlier note](../ideas/inverse-design.md),

$$K(x,y)=x d(y)+y d(x),\qquad S(x)=m d(x),\qquad d\ge0.$$

For the monodisperse preparation $n_0=(m/x)\delta_x$, the calculation leading to (2) gives

$$M_{1/2}'(0)\le-\kappa\frac{m^2d(x)}{\sqrt x}.$$

Thus vanishing of that derivative forces $d(x)=0$ for every $x$.

Alternatively, for the second moment, coagulation contributes $2m^2xd(x)$. Cauchy–Schwarz gives $\int z^2 b_x(dz)\ge x^2/2$, so fragmentation contributes at least $-m^2xd(x)/2$. Hence

$$M_2'(0)\ge\tfrac32m^2xd(x),$$

which gives the same conclusion. All these monodisperse preparations have finite second moment. □

This theorem concerns universal tests over all shapes with fixed mass and varying initial count. Fixing both count and mass allows only one monodisperse size, so the proof does not establish the same conclusion under that stronger preparation restriction. It also does not say that two moments identify arbitrary rates from one passive trajectory. It rules out the universal hidden class through feasible repeated preparations.

## 4. Interpretation and limitations

The count, mass, and mean-size traces of Theorem 1 are exactly constant, for every initial shape at material loading $m$. Nevertheless the population separates toward both ends of the size axis at a uniform exponential rate. A count-based experiment can therefore mistake continued irreversible redistribution for equilibrium. A half-moment measurement provides a finite, monotone certificate even when second moments or logarithmic moments are unavailable.

The theorem gives upper bounds on the time at which a prescribed fraction has left an observation window. For example, whenever the logarithm is positive, all but $\delta N$ particles are below $\varepsilon$ after

$$t\ge\frac1{\kappa\lambda m}\log\frac{M_{1/2}(0)}{\delta N\sqrt\varepsilon}.$$

A finite lower or upper particle-size cutoff changes the mathematical problem. A numerical method that retains both number and mass on a fixed bounded interval cannot reproduce (2) indefinitely, because those constraints impose a positive lower bound on $M_{1/2}$. This is a useful long-time numerical diagnostic, not evidence that the continuous model loses mass at a finite time.

## 5. Literature check and novelty status

The starting ideas—moment balances, quadratic polarization, and special constant-count solutions—are established. This note's candidate contribution is the sharp, daughter-law-independent half-moment decay and its full finite-number/finite-mass nonstationarity and two-boundary consequences.

The title “Additive Coagulation and Constant Fragmentation” appears in the authorized publisher-preview table of contents of Banasiak, Lamb, and Laurençot, *Analytic Methods for Coagulation-Fragmentation Models*, Volume II, §10.3.3.1. The title alone does not identify the fragmentation convention. An openly accessible primary source, [Laurençot (2019), Equation (1.8) and its discussion](https://www.numdam.org/item/10.1016/j.anihpc.2019.06.003.pdf), records stationary solutions for $K=k_0+k_1(x+y)$, **selection rate $a(x)=A_0x$**, and daughter density $2/y$. It cites Dubovskii and Stewart (1996), “Trend to equilibrium for the coagulation-fragmentation equation.” That selection rate differs from the constant per-particle rate used here. The existence result therefore does not contradict Theorem 1.

The main text of that book section was not used as an openly accessible source. No conclusion about its full coverage is justified from its title. Searches on 2026-09-06 included “additive coagulation constant fragmentation,” “additive coagulation constant fragmentation rate,” “coagulation constant selection,” “additive fragmentation nonexistence stationary,” and “coagulation fragmentation square root moment.” No exact match for (2)–(3) was located. This bounded search does not establish novelty, and the broader homogeneous coagulation–fragmentation and weak convergence literature still needs checking.

## 6. Independent review

The subagent `review_gauge` independently checked the sharp pair inequality, the decay coefficient, the integrability bound, the absence of a finite-count/finite-mass stationary state, both limits in (3), and Theorem 2's half-moment rigidity. It explicitly warned against confusing a fixed-mass preparation class with one that also fixes count. The developing agent checked the second-moment alternative and supplied the bounded-truncation argument above. No numerical simulation is needed to verify these algebraic inequalities; a solver benchmark could be useful as a separate application.

## 7. The full family of fractional moments

**Theorem 3.** Under Theorem 1's assumptions, every $0<p<1$ satisfies

$$
M_p(t)\le M_p(0)e^{-\kappa_p\lambda mt},\qquad
\kappa_p=3-2^p-2^{1-p}>0.
\tag{5}
$$

For each fixed $p$, the coefficient is sharp for a uniform estimate with prefactor one. The largest such coefficient over the fractional moments occurs uniquely at $p=1/2$. This is a comparison of uniform exponential rates, not a claim that the half moment is optimal for every noisy observation or threshold-estimation problem.

The key algebraic inequality is

$$
(x+y)[x^p+y^p-(x+y)^p]
\ge(2-2^p)(xy^p+yx^p),\qquad x,y>0.
\tag{6}
$$

Its constant is sharp at $x=y$. This is a power inequality used as a proof tool; no novelty claim is made for the inequality itself.

**Proof of (6).** Set $u=x/(x+y)$, $v=1-u$, and $A=2^p-1\in(0,1)$. Inequality (6) is equivalent to $f(u)\ge1$, where

$$f(u)=A(u^p+v^p)+(1-A)(u^{p+1}+v^{p+1}).$$

By symmetry it suffices to consider $0<u<1/2$. The function has $f(0)=f(1/2)=1$, $f'(0+)=+\infty$, and $f'(1/2)=0$. The sign of $f''$ is the sign of

$$
(1-A)(p+1)-A(1-p)R(u),\qquad
R(u)=\frac{u^{p-2}+v^{p-2}}{u^{p-1}+v^{p-1}}
=\frac{u^{2-p}+v^{2-p}}{uv(u^{1-p}+v^{1-p})}.
$$

On $(0,1/2)$ the numerator in the final ratio strictly decreases. Both positive denominator factors strictly increase, so $R$ strictly decreases. Hence $f''$ changes sign at most once, from negative to positive. It must make that change: otherwise $f'$ decreases from $+\infty$ to zero, contradicting $f(0)=f(1/2)$. Its increasing final branch approaches zero from below; its decreasing initial branch therefore crosses zero exactly once. Thus $f$ first increases and then decreases back to $1$, and $f(u)>1$ for $0<u<1/2$. Equality for positive $x,y$ holds exactly at $x=y$. □

**Proof of (5).** By Hölder's inequality, $M_p\le N^{1-p}m^p$. Applying (6) in the coagulation balance gives a contribution at most $-\lambda(2-2^p)mM_p$. Concavity against the daughter measure gives $\int z^p b_x(dz)\le2^{1-p}x^p$. The fragmentation contribution is therefore at most $\lambda m(2^{1-p}-1)M_p$. Their sum is (5)'s differential inequality. The bounded truncation $\min\{x^p,R\}$ justifies the balance: its coagulation increment is dominated after multiplication by $K$ by $\lambda(xy^p+yx^p)$, and its fragmentation increment by $2^{1-p}x^p$ before multiplication by $S$.

Monodisperse initial data and equal splitting give equality in the derivative bound at time zero. Finally $2^p+2^{1-p}\ge2\sqrt2$, with equality only at $p=1/2$, proves the optimization statement. Positivity of $\kappa_p$ follows from strict convexity of $2^p+2^{1-p}$ and its common endpoint value $3$. □

**Corollary 3 (moving observation windows).** Fix $\varepsilon_0,R_0>0$ and $0<v<\lambda m\log2$. Then both

$$n_t([\varepsilon_0 e^{-vt},\infty))\longrightarrow0,
\qquad
\int_{(0,R_0e^{vt}]}x\,dn_t(x)\longrightarrow0$$

at exponential rates. Indeed, for any $p\in(0,1)$,

$$
n_t([\varepsilon_0 e^{-vt},\infty))
\le\varepsilon_0^{-p}M_p(0)e^{-[\kappa_p\lambda m-pv]t},
$$
$$
\int_{(0,R_0e^{vt}]}x\,dn_t(x)
\le R_0^{1-p}M_p(0)e^{-[\kappa_p\lambda m-(1-p)v]t}.
$$

The limits $\kappa_p/p\to\log2$ as $p\downarrow0$ and $\kappa_p/(1-p)\to\log2$ as $p\uparrow1$ permit a suitable exponent in each bound. The two bounds generally use different values of $p$. These guaranteed velocities do not establish a matching asymptotic front speed, and the endpoint $v=\lambda m\log2$ is not covered.

The initial proof of (6) used a binomial-series argument; the independent reviewer checked it and supplied the shorter calculus proof recorded here, which the developing agent then checked. The durable [independent review](../reviews/invisible-kinetics-independent-review.md) records the detailed verification and scope limits.

## 8. A nonstationarity criterion stable under changes to the rates

The fractional-moment calculation is useful beyond the exactly count-neutral model. Suppose

$$a(x+y)\le K(x,y)\le A(x+y),\qquad 0\le S(x)\le\sigma,$$

for constants $0<a\le A<\infty$, with the same daughter-count and daughter-mass assumptions. For a mass-conserving weak solution of mass $m$,

$$
M_p'(t)\le-\gamma_p M_p(t),\qquad
\gamma_p=am(2-2^p)-\sigma(2^{1-p}-1)
=(2^{1-p}-1)(am\,2^p-\sigma).
$$

If $\sigma<2am$, some $p<1$ sufficiently close to one has $\gamma_p>0$. Consequently there is no stationary state of mass $m$ with finite particle count. This is a sufficient condition; no assertion of sharpness of the threshold or existence above it is made.

The proof repeats the two contributions in Theorem 3. The upper bound on $K$ and the count estimate $N(t)\le N(0)e^{\sigma t}$ provide local integrability for the truncation argument. Count need not remain constant in this extension. The independent reviewer checked this calculation. Its novelty has not been established; it should initially be treated as a supporting moment criterion.
