# A shared finite bath can preserve both subsystem laws while imposing one bit of phase correlation

Date: 2026-09-07. Status: mathematical derivation and independent review complete; see [the review](verification/shared-bath-review.md). A bounded [prior-art audit](verification/shared-bath-prior-art.md) is complete; priority remains provisional. The mechanisms are derived for the physical power-law reservoir, not a Gaussian bath surrogate. No microscopic interfacial-tail assumption is needed for the phase-selection theorem below.

## 1. Two independent copies produce three total-energy phases

Let `P_N` be the canonical law of one system at inverse temperature `β>0`. Give it two disjoint phase events `A_-,N,A_+,N` exhausting its probability space, with

\[
w_{i,N}=P_N(A_{i,N})\to w_i>0,\quad w_-+w_+=1.
\]

Let their energy centers satisfy `Δ_N=E_+,N−E_-,N`, `Δ_N/N→ell>0`. Initially assume only that

\[
(E-E_{i,N})/\sqrt N\mid A_{i,N}
\]

is tight. Neither a conditional Gaussian limit nor a local density approximation is required for the conclusions stated below.

Take two identical independent copies with canonical product law `P_N⊗P_N`, physical total energy `T=E^(1)+E^(2)`, and phase labels `(S_1,S_2)`. The three total-energy centers are

\[
2E_{-,N},\qquad M_N=E_{-,N}+E_{+,N},\qquad 2E_{+,N}.
\]

Their limiting probabilities are `w_-²,2w_-w_+,w_+²`. The central peak contains two different assignments, `(-,+)` and `(+,-)`, with equal probability even when the canonical one-copy weights are unequal.

The subsystem size variable N counts **one copy**; the combined subsystem has size `2N`. Fixed factors of two do not change any bath-growth exponent.

## 2. Exact physical bath centered at the mixed phase

Couple the pair additively to a reservoir with density of states `U_B^c 1_{U_B>0}`, with `c=c_N>0`. Set the total energy of the isolated composite to

\[
\boxed{\mathcal E_N=M_N+c_N/\beta.}
\tag{1}
\]

After dividing the unnormalized likelihood by its value at `T=M_N`, the bath weight is

\[
W_N(T)=\exp[\beta(T-M_N)]
\left(1-\frac{\beta(T-M_N)}{c_N}\right)^{c_N}
\mathbf1_{T<M_N+c_N/\beta}.
\tag{2}
\]

The formula means zero outside its feasible domain. On that domain set `x=β(T−M_N)/c_N`; then

\[
\log W_N=c_N[x+\log(1-x)]\le0,
\]

with equality precisely at the mixed center. In particular,

\[
0\le W_N\le1
\tag{3}
\]

globally, including arbitrarily rare energy tails. Let `Z_N=E_{P_N⊗P_N}W_N`, and let `Q_N` be the normalized reweighted joint law.

## 3. Shared-bath phase selection theorem

Assume

\[
\boxed{N\ll c_N\ll N^2.}
\tag{4}
\]

Let `O_N={S_1≠S_2}` be the opposite-phase event. Then

\[
\boxed{\operatorname{TV}\bigl(Q_N,(P_N\otimes P_N)(\cdot\mid O_N)\bigr)\to0.}
\tag{5}
\]

**Proof.** On either opposite-phase assignment, `T−M_N=O_P(sqrt(N))`. The exact expansion

\[
x+\log(1-x)=-x^2/2+O(|x|^3)
\]

and `N/c_N→0` imply `log W_N→0` in conditional probability. On equal-phase assignments,

\[
T-M_N=\pm\Delta_N+O_P(\sqrt N).
\]

Since `c_N/N→∞`, these typical energies are feasible and `x→0`. Since `N²/c_N→∞`, their log weights instead tend to `−∞`, with leading term `−β²Δ_N²/(2c_N)`.

Therefore `W_N−1_{O_N}→0` in canonical probability. The global bound (3) upgrades this to `L¹(P_N⊗P_N)` convergence. In particular,

\[
Z_N\to p_O:=2w_-w_+>0.
\]

Normalizing the two likelihoods proves (5). The proof never reweights an uncontrolled rare tail upward: its likelihood is at most one. ∎

Thus, throughout a broad range of bath sizes, the bath selects one low-energy and one high-energy subsystem. It does not need to identify which copy occupies which phase.

## 4. Joint and marginal accuracy differ sharply

Because conditioning a probability law on an event of probability `p` has total-variation distance `1−p` from the original law, (5) gives

\[
\boxed{\operatorname{TV}(Q_N,P_N\otimes P_N)
\to w_-^2+w_+^2.}
\tag{6}
\]

For identical independent copies, the exact one-copy marginal of the opposite-phase-conditioned law is

\[
\frac12P_N(\cdot\mid A_{-,N})+
\frac12P_N(\cdot\mid A_{+,N}).
\tag{7}
\]

The two conditional laws have disjoint supports by their definitions. Hence either physical subsystem marginal satisfies

\[
\boxed{\operatorname{TV}(Q_N^{(i)},P_N)
\to|w_--1/2|.}
\tag{8}
\]

If the reference phase weights are balanced, both complete subsystem marginals converge to their canonical laws, whereas the joint law stays a distance `1/2` from the canonical product. For example, in the plain short-range large-q Potts model, or the Potts-plus-kinetic benchmarks, with positive nondegenerate order-sqrt(N) phase fluctuations, `c_N=N^(5/4)` works here despite growing more slowly than the `N^(3/2)` necessary bath scale for reproducing an isolated subsystem law with a single physical bath. This isolated-subsystem comparison uses the positive-variance hypotheses; tightness alone would also allow two exact atomic energy phases, whose relative weights can be balanced without that fluctuation-scale obstruction. The second subsystem supplies an additional fluctuating energy store, and the missing independence appears as phase anticorrelation.

This statement concerns complete subsystem equilibrium distributions. It does not claim that their dynamics become independent or canonical.

## 5. The mutual information tends to exactly one bit

Total-variation convergence alone would not justify a claim about continuous-state entropy. The physical weight supplies the stronger bounds needed here.

Define `h_N=log W_N`, with `h_N=−∞` when `W_N=0`, and use the convention `0 log0=0`. Since

\[
0\le -W_N\log W_N\le1/e,
\]

and `W_N log W_N→0` in canonical probability on every phase assignment, bounded convergence gives

\[
\mathbb E_{Q_N}h_N
=Z_N^{-1}\mathbb E_{P_N\otimes P_N}(W_N\log W_N)\to0.
\]

It follows that

\[
D(Q_N\|P_N\otimes P_N)
=\mathbb E_{Q_N}h_N-\log Z_N
\to-\log(2w_-w_+).
\tag{9}
\]

Each marginal likelihood ratio has the uniform bound

\[
r_{i,N}=\frac{dQ_N^{(i)}}{dP_N}\le1/Z_N.
\]

Equation (5) gives its `L¹(P_N)` convergence to the opposite-phase-conditioned marginal ratio, equal to `1/(2w_{-,N})` on the minus phase and `1/(2w_{+,N})` on the plus phase. All these ratios are eventually uniformly bounded. Uniform continuity of `r log r` on a compact interval containing them therefore gives

\[
D(Q_N^{(i)}\|P_N)
\to-\log2-\tfrac12\log(w_-w_+).
\tag{10}
\]

All relative entropies are finite. The relative-entropy chain rule yields

\[
\boxed{I_{Q_N}(X_1;X_2)
=D(Q_N\|P_N\otimes P_N)-\sum_iD(Q_N^{(i)}\|P_N)
\to\log2.}
\tag{11}
\]

This is one bit, regardless of the original positive phase weights. No finite differential-entropy hypothesis is needed. The asymptotic phase labels are individually uniform and perfectly anticorrelated; equation (11) also shows that no additional finite amount of within-phase dependence survives in mutual information.

## 6. A full microscopic three-phase bath-size iff theorem

The original phase-concentration assumptions already imply

\[
\boxed{\exists\mathcal E_N:\operatorname{TV}(Q_{N,\mathcal E_N},P_N\otimes P_N)\to0
\quad\Longleftrightarrow\quad c_N/N^2\to\infty.}
\tag{12}
\]

In fact, this statement needs only the macroscopic two-atom energy limit of each copy, with positive weights and distinct energies; Gaussian limits, kinetic smoothing, and fluctuation-scale tightness are unnecessary for (12).

Here is the direct necessity argument suggested and independently checked by `capacity_review`. TV convergence makes the normalized log likelihood tend to zero in probability. Select three good total-energy points `t_1<t_2<t_3`, one near each of the three total-energy peaks, with gaps proportional to N. They are feasible and their normalized log likelihood values tend to zero. Set

\[
\theta=\frac{t_2-t_1}{t_3-t_1},\qquad
r=\log\frac{\mathcal E_N-t_1}{\mathcal E_N-t_3}>0.
\]

The endpoint log-weight difference gives `c_N r=β(t_3−t_1)+o(1)=Θ(N)`. The exact concavity gap at the middle point is

\[
c_N\left\{\log[(1-\theta)e^r+\theta]-(1-\theta)r\right\}\to0.
\]

Since θ stays bounded away from zero and one, the expression in braces is bounded below by `C min(r²,r)`. For `0≤r≤1`, this follows from the positive uniformly bounded-below second derivative; for `r≥1`, convexity makes its ratio to r no smaller than its value at one. The gap is consequently at least a constant times `min(N²/c_N,N)`. Its vanishing forces `c_N≫N²`, with no preliminary large-bath or local-slope assumption.

For sufficiency, use the maximum-centered bath (1). The canonical total energy obeys `T−M_N=O_P(N)`. If `c_N≫N²`, equation (2) tends to one in probability, and `0≤W_N≤1` upgrades this to L1 convergence. Normalization proves TV convergence. Rare valleys and tails never need an envelope.

This gives an actual microscopic short-range example: take two independent plain nearest-neighbor two-dimensional periodic large-q Potts systems. No kinetic variables are required. Their macroscopic two-atom energy law follows from the audited Borgs–Kotecký–Miracle-Solé partition theorem at real shifts of order `1/N`; see [the source audit](short-range-potts-route.md#8-closed-necessity-gate-precise-source-audit-and-corollary) and [the primary theorem](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/Finite-Size-Scaling-for-Potts-Models.pdf). Equation (12) therefore applies to the combined microscopic law. The unresolved inward-tail sufficiency estimate for an **isolated** short-range copy is not needed here. Macroscopic energy separation alone suffices for (12).

For the shared-bath anticorrelation theorem (5), the stronger order-sqrt(N) conditional tightness is still needed to obtain the smaller lower scale `c_N≫N`. It follows from the independently verified weak-CLT route for the plain short-range Potts model. Moreover, the conditional-independence variance bound in [section 3.1 of the source route](short-range-potts-route.md#31-positive-spin-phase-variances-from-conditional-independence) proves that both spin-phase Gaussian limits have positive variance. Thus the isolated-copy necessary scale `c_N≫N^(3/2)` also holds without kinetic variables. Kinetic energy is useful for a continuous benchmark, but neither it nor positivity of the within-phase variance is required by theorem (5). The mean-field benchmark retains its kinetic sector: the local independent-set bound used for the finite-range model does not apply there.

The already verified mean-field three-state Potts benchmark is another microscopic example. These constructions realize three total-energy peaks using two ordinary first-order systems; they do not assert a new single-material triple point.

## 7. Balancing the canonical weights by a finite-size temperature change

The large-q periodic Potts model at its infinite-volume transition has ordered/disordered weights `q/(q+1)` and `1/(q+1)`, so (8) does not vanish there. A canonical finite-size temperature adjustment produces the balanced benchmark.

More generally, when the phase partition asymptotics permit a real temperature displacement `δ/N`, the phase-weight ratio changes by the factor `exp(δ ell)`, with `ell=u_+−u_->0`. Thus a balanced sequence is

\[
\boxed{\beta_N=\beta_c-
\frac{\log(w_-/w_+)}{N\ell}+o(N^{-1}).}
\tag{13}
\]

For the short-range periodic Potts model this is `β_N=βc−log(q)/(Nell)+o(N^(−1))`. The sign is negative: warming reduces the excess probability of the lower-energy ordered phase. The audited real-temperature theorem justifies this adjustment and the corresponding weak phase limits. No kinetic sector is needed. If one is optionally included, its canonical law uses the same `β_N`. The shift is O(1/N), and bounded spin energy makes the corresponding canonical likelihood uniformly bounded. Within either phase its centered likelihood converges to a constant, so the conditional weak spin CLTs and their positive variances persist under this balancing shift.

Use this canonical reference for both copies and replace β in (1)–(2) by β_N. Since `β_N→βc>0`, every estimate in sections 2–6 remains valid. Both subsystem marginals then converge to their respective balanced canonical laws in regime (4), while joint TV tends to `1/2` and mutual information tends to `log2`.

One may tune an exact finite-N equal-weight temperature when it exists; only asymptotic balance is needed here. The reference temperature and physical bath must be changed consistently. It would be incorrect to claim marginal convergence to the original unbalanced βc canonical law after making this adjustment.

## 8. Fixed numbers of copies and selected phase counts

For any fixed integer `m≥2`, take m identical independent copies and let `K` count the copies in their plus phase. Center the shared bath maximum at `(m−k)E_-,N+kE_+,N`, for fixed `0≤k≤m`. The same bounded-weight proof in regime (4) gives

\[
Q_N\longrightarrow P_N^{\otimes m}(\cdot\mid K=k)
\quad\text{in total variation}.
\]

Each marginal has plus-phase probability `f=k/m`. Its TV distance from the canonical marginal tends to `|w_+−f|`; the joint distance tends to

\[
1-p_k,\qquad p_k=\binom mk w_+^k w_-^{m-k}.
\]

The same bounded-likelihood entropy proof gives joint relative entropy to the canonical product tending to `−log p_k`. Subtracting the m marginal relative entropies yields total correlation

\[
\boxed{D\left(Q_N\middle\|\bigotimes_{i=1}^m Q_N^{(i)}\right)
\to m H(k/m)-\log\binom mk,}
\]

where `H(f)=−f log f−(1−f)log(1−f)` with the usual endpoint convention. The limit is independent of the original positive phase weights. When `w_+=k/m`, all complete subsystem marginals converge to their canonical laws and the total-correlation limit equals `−log p_k`. The two-copy, one-plus case reduces to one bit.

This is a fixed-m statement. Taking m to infinity would require uniform phase, tail, and normalization estimates and is not claimed.

## 9. Deterministic numerical check

`verification/check_shared_bath_correlations.py` evaluates the **exact power-law bath** for a two-Gaussian one-copy benchmark with means `±N/2`, variance N in each phase, `β=1`, and `c_N=N^(5/4)`. It is a formula check, not Potts enumeration or a Gaussian approximation used in the proofs. Independent Gauss–Hermite rules with 96 and 160 points per Gaussian component gave the following 160-point values:

| N | Canonical minus weight | Joint TV | Marginal TV | TV to opposite-phase conditioning | Mutual information (nats) |
| --- | --- | --- | --- | --- | --- |
| 100 | 0.5 | 0.5148 | 0.0522 | 0.1177 | 0.72251 |
| 10,000 | 0.5 | 0.5004 | 0.0212 | 0.0442 | 0.69730 |
| 1,000,000 | 0.5 | 0.5000 | 0.0073 | 0.0149 | 0.69362 |
| 100 | 0.7 | 0.5889 | 0.2012 | 0.1177 | 0.72211 |
| 10,000 | 0.7 | 0.5801 | 0.2000 | 0.0442 | 0.69730 |
| 1,000,000 | 0.7 | 0.5800 | 0.2000 | 0.0149 | 0.69362 |

The respective predicted limits are joint TV `0.5` or `0.58`, marginal TV `0` or `0.2`, conditioned TV `0`, and mutual information `log2=0.693147…`. Across all ten computed cases, changing quadrature order altered TV values by at most `4.8×10^-4`; the mutual-information difference was below `5×10^-16`. Absolute-value kinks make the TV integrals converge less rapidly than the smooth entropy integrals. No interval-arithmetic enclosure is claimed.

The Gaussian components in this benchmark have exponentially small overlap. Latent component labels were used to compute the diagnostic distance to opposite-phase conditioning; this differs from an energy-threshold phase label by an exponentially small probability at the reported N. Joint and marginal TV and mutual information use the actual energy likelihood and do not require observing the latent labels.

Run `python research/verification/check_shared_bath_correlations.py --order 160`. The retained numerical output is `verification/shared-bath-correlations-results.json`.

## 10. Scope, review, and next checks


The copies exchange energy through one common passive reservoir and have no direct interaction. Additivity, fixed positive phase weights, order-N separation, and order-sqrt(N) conditional tightness are the key hypotheses for phase selection. Rare valleys may be arbitrarily irregular because the chosen bath weight never exceeds its mixed-phase value.

For nonidentical copies, mixed assignments need not have the same total energy or equal reference weights, so the exact one-bit and one-half statements require modification. The selected assignments must be degenerate on the reservoir's discrimination scale. No claim about arbitrary nonidentical systems is made here.

The thermodynamic capacity convention is the surface-entropy capacity `C_B/k_B=c_N` of the exact power-law bath. The result is about full equilibrium laws, their correlations, and their information; no nucleation or switching-rate theorem follows from it.

Independent reviewer `capacity_review` approved the phase-selection theorem, joint and marginal TV limits, entropy convergence, balanced-temperature sign, fixed-m extension, and generalized macroscopic-support necessity proof in [the written review](verification/shared-bath-review.md). The isolated-subsystem comparison was narrowed to positive nondegenerate phase fluctuations following that review. A separate literature audit remains necessary before any novelty or publication claim.

## 11. Centered bath at linear capacity: residual fluctuation correlations

This appendix completes the boundary case `c_N/N→γ∈(0,∞)` for the same centered calibration (1). It assumes positive Gaussian conditional weak limits, strengthening the tightness hypothesis used in section 2:

\[
Z_{i,N}:=\frac{E-E_{i,N}}{\sqrt N}\ \bigg|\ A_{i,N}
\Rightarrow\mathcal N(0,v_i),\qquad v_-,v_+>0.
\tag{18}
\]

The copies are independent and identical under the canonical reference, the two phase probabilities tend to `w_-,w_+>0`, and their energy gap divided by N tends to `ell>0`. The inverse temperature may be fixed or satisfy `β_N→β>0`. Set

\[
a=\frac{\beta^2}{\gamma},\quad V=v_-+v_+,\quad
A_\gamma=(1+aV)^{-1/2},\quad p_O=2w_-w_+.
\]

All conclusions below concern this centered total-energy choice. They do not assert an impossibility theorem for arbitrary total-energy tuning at linear capacity.

### 11.1. Phase selection and the Gaussian fluctuation tilt

On an opposite-phase assignment, the exact weight (2), as a function of the standardized energies, converges uniformly on compact sets to

\[
W_\gamma(z_-,z_+)=
\exp\left[-\frac a2(z_-+z_+)^2\right].
\tag{19}
\]

On either same-phase assignment, the weight tends to zero uniformly on compact standardized windows. Indeed, `T−M_N=±ell N+o(N)` there, while `c_N/N→γ`; the physical log weight is bounded above by a negative constant times N, or the configuration lies beyond the bath cutoff. If the upper same-phase center approaches that cutoff, the bound `x+log(1−x)≤−x²/2` for `0≤x<1` still forces decay. The lower same-phase center has a finite negative limiting x and the same strict decay.

Conditional weak convergence, tightness, and `0≤W_N≤1` therefore give

\[
\mathbb E_{P_N^{\otimes2}}W_N\longrightarrow p_OA_\gamma.
\tag{20}
\]

The two opposite-phase assignments each acquire probability `1/2`; same-phase assignments disappear. Within either opposite assignment, order the standardized coordinates by phase (minus, plus). They converge weakly to a centered Gaussian with covariance

\[
\boxed{\Sigma_\gamma
=D-\frac{a}{1+aV}\,vv^{\mathsf T},\qquad
D=\operatorname{diag}(v_-,v_+),\quad
v=(v_-,v_+)^{\mathsf T}.}
\tag{21}
\]

This follows by adding `a 11ᵀ` to the precision matrix `D⁻¹`. In particular,

\[
u_i=\frac{v_i(1+av_j)}{1+aV}
=v_i\left(1-\frac{av_i}{1+aV}\right),\quad j\ne i,
\qquad
\rho_\gamma^2=\frac{a^2v_-v_+}{(1+av_-)(1+av_+)}.
\tag{22}
\]

Here `u_i` denotes the limiting marginal variance conditional on phase i; it is strictly between zero and `v_i`.

These conclusions do not assume that microscopic phase laws converge in TV to Gaussian laws. More precisely, replace the exact weight by `1_O W_γ(Z_-,Z_+)`, retaining the original conditional microscopic laws and then normalizing. The resulting reference-dependent approximation converges to `Q_N` in full TV: the unnormalized weights converge in L1 by compact convergence, tightness, and boundedness. Gaussian laws enter only when evaluating limiting integrals of the standardized energies.

### 11.2. Exact limiting error of each complete subsystem marginal

Let `φ_v` denote the centered normal density of variance v. Integrating (19) over the other phase gives

\[
g_i(z)=\frac{1}{\sqrt{1+av_j}}
\exp\left[-\frac{az^2}{2(1+av_j)}\right],
\qquad
\frac{g_i(z)}{A_\gamma}=\frac{\phi_{u_i}(z)}{\phi_{v_i}(z)}.
\tag{23}
\]

The limiting marginal likelihood on phase i is therefore `g_i(z)/(2w_iA_γ)`. The exact marginal likelihood is bounded by the reciprocal of the normalizer in (20). Integrating the exact kernel over the other subsystem gives uniform convergence to this expression on compact phase windows; outside those windows, tightness and the uniform likelihood bound control the error. Consequently the TV distance of either **complete microscopic subsystem marginal** has the exact limit

\[
\boxed{\lim_N\operatorname{TV}(Q_{1,N},P_N)
=\frac12\sum_{i\in\{-,+\}}
\int_{\mathbb R}\left|
\frac12\phi_{u_i}(z)-w_i\phi_{v_i}(z)
\right|\,dz.}
\tag{24}
\]

For balanced canonical weights, this becomes

\[
\frac12\sum_i\operatorname{TV}
\bigl(\mathcal N(0,u_i),\mathcal N(0,v_i)\bigr)>0.
\tag{25}
\]

An explicit expression uses the standard normal distribution function Φ. With

\[
x_i=\sqrt{\frac{u_iv_i\log(v_i/u_i)}{v_i-u_i}},
\]

the balanced limit (25) is `Σ_i[Φ(x_i/√u_i)−Φ(x_i/√v_i)]`. Thus the centered linear-capacity bath leaves a positive full-marginal error even after balancing phase probabilities. This differs from the vanishing marginal error proved in section 3 for `N≪c_N≪N²`.

### 11.3. Mutual information, including the fluctuation contribution

Entropy convergence needs a separate argument; weak or TV convergence alone is insufficient. Write `h_N=log W_N` on the feasible set and use the convention `W_N log W_N=0` when `W_N=0`. The function `x log x` is continuous and bounded on `[0,1]`. The compact convergence and tightness argument above therefore also gives convergence of `E[W_N log W_N]`. Under the Gaussian tilt, the sum of the two standardized energies has variance `V/(1+aV)`. It follows that

\[
\lim_N D(Q_N\Vert P_N^{\otimes2})
=-\log p_O+\frac12\log(1+aV)
-\frac{aV}{2(1+aV)}.
\tag{26}
\]

The exact marginal likelihoods are uniformly bounded, by (20). Their compact convergence from section 11.2 and continuity of `r log r` on the resulting bounded interval give

\[
\lim_N D(Q_{1,N}\Vert P_N)
=\frac12\sum_i\log\frac1{2w_i}
+\frac12\sum_i
D\bigl(\mathcal N(0,u_i)\Vert\mathcal N(0,v_i)\bigr).
\tag{27}
\]

The same holds for the second marginal. All these finite-N relative entropies are finite: both joint and marginal likelihoods are bounded. The relative-entropy chain rule, (26), and (27) now prove

\[
\boxed{\lim_N I_{Q_N}(\omega_1;\omega_2)
=\log2-\frac12\log(1-\rho_\gamma^2)
=\log2+\frac12\log
\frac{(1+av_-)(1+av_+)}{1+aV}.}
\tag{28}
\]

The first term is the phase anticorrelation already found above; the strictly positive second term is the information in correlated energy fluctuations within opposite phases. Original canonical phase weights cancel from (28). No finiteness or convergence of microscopic differential entropies is assumed.

For the plain short-range large-q Potts model, the positive conditional weak limits required in (18) were established in `short-range-potts-route.md`, including after the finite-size balancing adjustment. Thus this boundary calculation applies to that microscopic model as well as to the Gaussian benchmark. Independent reviewer `capacity_review` re-derived and approved equations (18)–(28), including the cutoff case, full-marginal TV limit, and entropy convergence; see [the review](verification/shared-bath-review.md). No further proof gap remains in this centered linear-capacity appendix under its stated hypotheses. Literature priority is a separate question.
