Adversarial literature audit: arbitrary constant fragmentation, number sampling, and a finite last coagulation

Date: 2026-09-07. This supplements [the earlier log-size audit](log-size-limit-literature.md) and compares [the arbitrary-rate theorem](../results/general-additive-log-coupling.md) and [the pathwise theorem](../results/pathwise-additive-log-coupling.md) with closer probabilistic sources. It is a bounded literature audit, not an independent certification of those proofs.

No inspected source states the full proposed arbitrary-rate finite logarithmic correction or the finite-last-coagulation conclusion for the specified auxiliary process. Several components have strong prior precedents, and the pure-coagulation endpoint has much less novelty than the general statement. The existence of nonlinear jump representations, size-biased sampling, Doob transforms, and compound Poisson limits should not be presented as discoveries.

The object requiring precise identification is the process with marginals `η_t=n_t/N(t)`, coagulation jump `x→x+U` at rate `λN(t)x`, and fragmentation jump `x→xΘ` at rate `2σ`. Here `U~η_t`, `Θ~B/2`, `b=λm`, and `N(t)=N₀exp((σ−b)t)`. Its proposed path decomposition has a finite nonnegative logarithmic correction `A∞`, even though its expected number of coagulation events through time `t` is `bt`. These are statements about a specified auxiliary process. One-time marginals alone do not determine path properties, and another representation of the same evolving population can have different collision histories.

The closest rigorous primary representation is Madalina Deaconu, Nicolas Fournier, and Etienne Tanré, *A pure jump Markov process associated with Smoluchowski's coagulation equation*, Annals of Probability 30 (2002), 1763–1796, [full author manuscript](https://www-sop.inria.fr/members/Etienne.Tanre/publication/AOP104.pdf). Inspected equations (2.3), (2.6), and (2.16), the stochastic formulation, and Section 6's connection to the Marcus–Lushnikov process. Their probability law is the mass law `Q_t(dx)=x n_t(dx)` with unit total mass. Its generator is

```math
L_t f(x)=\int[f(x+y)-f(x)]\frac{K(x,y)}{y}Q_t(dy).
```

Thus, for the additive kernel, its collision intensity is `λN(t)x+b`. The proposed number process has only `λN(t)x`. This difference is essential. A physical mass tag retains a positive collision-rate contribution `b` at all times, so the finite-last-collision result does not transfer to that tag. The 2002 article already supplies a nonlinear Poisson-driven representation and a rigorous relation to microscopic tagged clusters; those broad claims are established.

There is an additional exact connection that follows by elementary calculation from the generators. It was not located as an explicit assertion in the inspected papers and is recorded here as the reviewer's deduction, not as a sourced theorem. Add fragmentation to the mass-tag generator in its standard size-biased form:

```math
L_t^{\rm mass}f(x)
=\lambda\int(x+y)[f(x+y)-f(x)]n_t(dy)
 +\sigma\int\theta[f(x\theta)-f(x)]B(d\theta).
```

For `h(x)=1/x`, direct integration gives

```math
L_t^{\rm mass}h=(\sigma-b)h.
```

The algebraic Doob transform

```math
L_t^h f=h^{-1}L_t^{\rm mass}(hf)-(\sigma-b)f
```

has coagulation kernel `λx n_t(dy)` and fragmentation kernel `σB(dθ)`: exactly the proposed number process. The inverse-size weight changes the mass law into the number law after normalization. This calculation explains both the missing `b` and the doubled fragmentation rate using standard change-of-measure machinery. Turning the generator identity into a path-space change of measure requires the relevant martingale and integrability argument; that is not supplied by this literature audit. The calculation nevertheless weakens any claim that the auxiliary generator itself represents a major new construction.

Nicolas Fournier, Bernard Roynette, and Etienne Tanré, *On long time behavior of some coagulation processes*, Stochastic Processes and their Applications 110 (2004), 1–17, [full author manuscript](https://www-sop.inria.fr/members/Etienne.Tanre/publication/spa.pdf), provides another necessary comparison. Its introduction and model scope concern particles with position and mass, Brownian excitation, and an attractive potential. The announced asymptotic result is that the tagged mass tends to infinity while its position tends to the potential minimum. It does not assert a finite last coagulation for a number-normalized additive model. The opposite mass behavior is not a contradiction, because the sampling law and dynamics differ.

Madalina Deaconu and Etienne Tanré, *Smoluchowski's coagulation equation: probabilistic interpretation of solutions for constant, additive and multiplicative kernels*, Annali della Scuola Normale Superiore di Pisa 29 (2000), 549–579, [full primary article](https://www.numdam.org/item/ASNSP_2000_4_29_3_549_0.pdf), explicitly develops branching-process representations of the additive solution. Inspected the introduction, discrete additive subsection including Proposition 2.4, and the continuous formulation including Proposition 3.2. The discrete construction uses total progeny of a Poisson Galton–Watson process. The article itself identifies these discrete results as known and gives new continuous-kernel connections and renormalization results. Proper number-normalized limits for pure additive coagulation must be compared with this established representation, not advertised as a newly found absence of typical growth.

A particularly transparent formula appears in Jean Bertoin, *Two solvable systems of coagulation equations with limited aggregations*, Annales de l'Institut Henri Poincaré C 26 (2009), 2073–2089, [full primary article](https://www.numdam.org/article/AIHPC_2009__26_6_2073_0.pdf). Inspected the introduction, equation (3), and the description of the limited-aggregation models. Equation (3), credited to Golovin, records the classical monodisperse additive solution

```math
n_t(k)=e^{-t}\operatorname{Borel}(1-e^{-t})(k),\qquad k\ge1.
```

Consequently its number-normalized law tends to the proper critical Borel law, whose arithmetic mean is infinite. Bertoin's own models consume finite numbers of available arms and can converge to terminal populations for that separate reason. Neither the arm mechanism nor its equilibrium conclusion is the proposed constant-fragmentation model.

The pure-coagulation Borel formula has an adversarial consequence for novelty. In the monodisperse discrete setting, an increasing integer-valued auxiliary path with these marginals has a finite terminal value almost surely: the proper limiting distribution precludes divergence to infinity. Each coagulation increases size by at least one, so the path has finitely many coagulations almost surely. This is a deduction from a known solution plus the monotone auxiliary representation, not an assertion located verbatim in the source. Thus the finite-last-collision conclusion at `σ=0` and monodisperse data is already a straightforward consequence of classical formulas. Extending this to arbitrary finite-count, finite-mass continuous initial laws and every `σ≥0` is the more substantial proposed content.

For `σ>0`, the proposed proof has a distinct ingredient absent from those pure-coagulation formulas: the half-moment estimate makes all accumulated upward logarithmic displacement integrable. Once that is known, the remaining path argument is standard. Namely,

```math
\log[\lambda N(t)X_t]
=\log[\lambda N_0X_0]+(\sigma-b)t
  +\sum_{j\le J_t}\log\Theta_j+A_t.
```

Jensen gives `E log Θ≤−log 2` when the expectation is finite; bounded truncations give the corresponding upper asymptotic bound without that assumption. The limiting upper slope is at most `−b−σ(2log 2−1)<0`. An integrable eventual jump intensity gives finitely many accepted coagulation jumps through standard compensator localization. None of these probability steps alone establishes originality. The nonlinear finite-log-correction estimate is what connects them to this model.

The equalities `E C_t=bt` and `C∞<∞` almost surely are compatible: they say that the finite terminal count has infinite expectation and that finite-time counts are not uniformly integrable. Such a distinction is familiar in critical branching and heavy-tailed stopping problems. Its occurrence here is an informative corollary, but should be framed as a model-specific consequence rather than a new probabilistic paradox. After the final coagulation, the auxiliary path follows the fragmentation mechanism exactly. Conditioning on the final-coagulation time can bias its future marks; that random time should not automatically be treated as a stopping time with an independent fresh Poisson future.

The earlier audit remains applicable to pure-fragmentation log-size CLTs, constant-pair versus constant-parent fragmentation terminology, and unrelated reversible partition limits. Additional searches combined Smoluchowski/additive coagulation with nonlinear Markov process, number-normalized distribution, inverse-size transform, Doob transform, tagged particle, last collision, and finite number of jumps. No explicit inverse-size transform or arbitrary-rate finite-last-collision theorem was identified, but failure of keyword searches is weak evidence of absence. The defensible research target is the all-rate quantitative nonlinear logarithmic correction and the resulting pathwise cessation theorem for the specified auxiliary representation, with the classical endpoint and standard representation machinery clearly attributed.
