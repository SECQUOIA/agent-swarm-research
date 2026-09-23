# Independent review: three phase energies and a physical thermal bath

Date: 2026-09-06. Reviewed file: `research/three-phase-physical-bath.md`. The main file was not edited. This review addresses mathematical correctness, including arbitrary total-energy tuning and the absence of an interfacial-tail hypothesis; it does not establish literature novelty.

**Verdict:** the claimed iff condition `c_N/N²→∞` is correct for the stated three-peak local limits and the positive-exponent physical bath. Unequal phase variances and arbitrary non-Gaussian valleys do not invalidate the argument. The necessary concavity and domain steps can be made rigorous without stronger regularity assumptions on the subsystem density. Two scope details should be explicit: assume `c_N>0`, as in the earlier physical-bath note; and for the extension to more than three phases, require their entire span to remain `O(N)`.

## 1. Exact setup and normalizability

Fix `β>0` and `c_N>0`. Define

\[
h_N(E)=\beta E+c_N\log(\mathcal E_N-E)
\]

on `E<mathcal E_N`, and set it to `−∞` outside. For any fixed finite `mathcal E_N` and positive `c_N`, this function has a finite maximum. Indeed, it tends to `−∞` at the upper endpoint and as `E→−∞`, and its unique maximum is at `E=mathcal E_N−c_N/β`. Thus the reweighting of an arbitrary probability density `p_N` has a finite normalizing integral. The integral is positive whenever `p_N` gives positive mass to the feasible domain. Any candidate convergent sequence must have this property, and the constructed sufficient sequence does.

No Gaussian assumption on the full density is used. The only local assumption is the stated `L¹` convergence after each phase is centered and rescaled by `sqrt(N)`, with positive Gaussian limits and weights summing to one.

## 2. Total variation forces feasibility of every fixed phase window

Suppose `TV(p_N,q_N)→0`. Set

\[
b_{i,N}=\frac{\mathcal E_N-E_{i,N}}{\sqrt N}.
\]

For each phase, necessarily `b_{i,N}→+∞`. Otherwise some subsequence has `b_{i,N}≤R` for a fixed real `R`. The canonical probability in the standardized interval `[R+1,R+2]` around that phase tends to

\[
w_i\int_{R+1}^{R+2}\phi_{v_i}(z)\,dz>0,
\]

whereas the bath marginal is identically zero there. This contradicts total-variation convergence.

Consequently every fixed standardized neighborhood of every phase eventually lies strictly inside the feasible domain. In particular, the centers and all finite-difference points used below are feasible. This conclusion allows arbitrary total-energy tuning initially; no large-bath or near-canonical-temperature assumption has been imposed.

## 3. From local likelihood convergence to center values and slopes

Let `Z_N=∫p_N exp(h_N)` and define

\[
f_{i,N}(z)=h_N(E_{i,N}+\sqrt N z)-\log Z_N.
\]

Total-variation convergence is equivalent to

\[
\int p_N(E)\left|e^{h_N(E)-\log Z_N}-1\right|dE\to0.
\tag{R1}
\]

Write `r_{i,N}(z)=sqrt(N)p_N(E_{i,N}+sqrt(N)z)`. On each fixed compact interval `I`, the limiting density `r_i=w_iφ_{v_i}` has a positive lower bound `m_I`. Since `r_{i,N}→r_i` in `L¹(I)`, the set where `r_{i,N}<m_I/2` has Lebesgue measure tending to zero. On its complement, (R1) implies `exp(f_{i,N})→1` in Lebesgue measure. For each `ε>0`, the event `|f_{i,N}|>ε` entails

\[
|e^{f_{i,N}}-1|\ge\min(e^\varepsilon-1,1-e^{-\varepsilon})>0,
\]

so `f_{i,N}→0` in Lebesgue measure on `I` as well.

The following elementary concavity lemma supplies the missing pointwise information. Let smooth concave functions `f_N` converge to zero in measure on `[-2,2]`. Choose `ε_N→0` slowly enough that each of the four intervals

\[
[-2,-3/2],\quad[-1,-1/2],\quad[1/2,1],\quad[3/2,2]
\]

contains a point `a_N,b_N,c_N,d_N`, respectively, with `|f_N|≤ε_N`. Such choices exist because convergence in measure makes the bad set smaller than the length of each interval.

Concavity bounds the central derivative by the outer secants:

\[
\frac{f_N(d_N)-f_N(c_N)}{d_N-c_N}
\le f_N'(0)\le
\frac{f_N(b_N)-f_N(a_N)}{b_N-a_N}.
\]

Every denominator is at least `1/2`; hence `|f_N'(0)|≤4ε_N`.

The chord between `b_N` and `c_N` gives `f_N(0)≥−ε_N`. For the upper bound, the tangent at `b_N` and the left secant give

\[
f_N(0)\le f_N(b_N)-b_N f_N'(b_N)
\le\varepsilon_N+4\varepsilon_N|b_N|
\le5\varepsilon_N.
\]

Thus both `f_N(0)→0` and `f_N'(0)→0`. Bracketing a larger compact interval with the same construction also yields local uniform convergence if desired, but the center-value and derivative conclusions alone suffice for this theorem.

Apply the lemma separately at all three phase centers. Since `f_{i,N}'(0)=sqrt(N)h_N'(E_{i,N})`, it proves precisely

\[
h_N(E_{i,N})-\log Z_N\to0,
\qquad \sqrt N h_N'(E_{i,N})\to0.
\tag{R2}
\]

The argument needs neither pointwise convergence of `p_N` nor an everywhere-positive finite-`N` subsystem density. Positivity of the limiting local density and local `L¹` convergence are enough.

## 4. Necessity for an arbitrary total-energy sequence

Introduce endpoint bath inverse temperatures

\[
\beta_{i,N}=\frac{c_N}{\mathcal E_N-E_{i,N}}.
\]

Equation (R2), together with `h_N'=β−β_{i,N}` at the center, gives

\[
\beta_{i,N}=\beta+o(N^{-1/2}).
\]

Subtract the reciprocals at phases 1 and 3:

\[
\frac{E_{3,N}-E_{1,N}}{c_N}
=\frac1{\beta_{1,N}}-\frac1{\beta_{3,N}}
=o(N^{-1/2}).
\]

Since the endpoint gap is asymptotic to `(l_1+l_2)N>0`, this first yields `c_N/N^(3/2)→∞`.

More directly, monotonicity of the bath inverse temperature in `E` sandwiches its value throughout the entire phase interval between the two endpoint values. Therefore

\[
-h_N''(E)=\frac{c_N}{(\mathcal E_N-E)^2}
=\frac{\beta^2}{c_N}[1+o(1)]
\tag{R3}
\]

uniformly between the outer phase centers. There is no uncontrolled Taylor expansion across the gap.

For a concave function with `−h''≥m_N` on `[a,b]`, applying concavity to `h(E)+(m_N/2)E²` proves

\[
h(x)-\frac{b-x}{b-a}h(a)-\frac{x-a}{b-a}h(b)
\ge\frac{m_N}{2}(x-a)(b-x).
\]

Use `a=E_1`, `x=E_2`, `b=E_3`, and the lower curvature bound in (R3). The left side tends to zero by (R2), since the three coefficients sum to zero and thus cancel `log Z_N`. The right side is

\[
\frac{\beta^2[1+o(1)]}{2c_N}
(E_2-E_1)(E_3-E_2)
\sim\frac{\beta^2l_1l_2N^2}{2c_N}.
\]

It follows that `N²/c_N→0`. This proof includes all total-energy sequences for which the marginal is defined; translating the bath working point cannot remove the concave chord gap.

## 5. Sufficiency and why the valley needs no envelope

Let `Δ_N=E_{3,N}−E_{1,N}` and choose

\[
\mathcal E_N=E_{1,N}+
\frac{\Delta_N}{1-\exp(-\beta\Delta_N/c_N)}.
\tag{R4}
\]

The available bath energies at the two endpoints have ratio `exp(−βΔ_N/c_N)`. Consequently their bath-log-weight difference exactly cancels the canonical factor `βΔ_N`, and `h_N(E_1)=h_N(E_3)`.

Subtract this common value and denote the resulting extended log-weight by `g_N`. If `c_N/N²→∞`, then `Δ_N/c_N→0`, and uniformly between the endpoints and in every fixed standardized phase neighborhood,

\[
\mathcal E_N-E=\frac{c_N}{\beta}[1+o(1)],
\qquad -g_N''(E)=O(c_N^{-1}).
\]

All such neighborhoods are feasible for large `N`. The usual interpolation bound gives

\[
0\le g_N(E)\le\frac{K}{2c_N}
(E-E_1)(E_3-E)\le\frac{K\Delta_N^2}{8c_N}=o(1)
\]

throughout the entire phase interval. Its endpoint slopes have absolute values at most `KΔ_N/c_N`. Therefore on the parts of the extreme phase neighborhoods lying outside that interval,

\[
|g_N(E_i+\sqrt N z)|
\le C_R\left(\frac{\Delta_N\sqrt N}{c_N}
+\frac{N}{c_N}\right)=o(1),\quad |z|\le R.
\]

The middle phase neighborhood is eventually inside the interval. Thus `g_N→0` uniformly on every fixed standardized neighborhood of all three phases.

Globally, concavity with two zero endpoints gives `g_N≤0` outside the endpoint interval, including the convention `g_N=−∞` on infeasible energies. Consequently

\[
\sup_E e^{g_N(E)}\le e^{o(1)}.
\tag{R5}
\]

This is the decisive protection against anomalous valley or exterior tails: no portion of the canonical measure is multiplied by a diverging factor.

For fixed `R`, let `A_{N,R}` be the union of the three standardized phase windows. On this union, `|exp(g_N)−1|→0` uniformly. On the complement it is bounded by `1+o(1)` using (R5). The local limits and the sum of the weights imply

\[
\lim_{R\to\infty}\limsup_{N\to\infty}p_N(A_{N,R}^c)=0.
\]

Splitting the integral across these two regions yields

\[
\int p_N|e^{g_N}-1|\to0.
\]

Hence `Z_N^*=∫p_Ne^{g_N}→1`, and

\[
\int p_N\left|\frac{e^{g_N}}{Z_N^*}-1\right|
\le\frac{\int p_N|e^{g_N}-1|+|Z_N^*-1|}{Z_N^*}\to0.
\]

This proves the total-variation conclusion without any interfacial, droplet, moderate-deviation, or global Gaussian hypothesis.

## 6. Scope refinements and limits

- **Positive bath exponent.** State `c_N>0` explicitly. It is the natural positive surface-entropy heat-capacity case and guarantees the concavity used throughout. The earlier two-phase physical-bath note already imposes it.
- **Additional phases.** For finitely many positive-weight peaks, the same sufficiency proof balances the two outermost peaks and requires their span to be `O(N)`. Necessity follows from any three peaks with adjacent separations proportional to `N`. A clean statement assumes all phase centers have finite limiting energy densities, with at least three distinct ones. Merely retaining a valid triple while adding a positive-weight peak at distance `N²` would not retain the `N²` bath threshold.
- **Fixed positive local masses matter.** A third phase with weight tending to zero does not supply the nonvanishing local-density argument and need not impose the same obstruction.
- **Three energies, not three labels.** Distinct order-parameter phases at the same energy do not supply the two positive scalar energy gaps needed by the chord inequality.
- **Physical conclusions remain scoped.** The theorem concerns the full energy probability law under a specific reservoir density of states. It does not identify a kinetic rate, certify microscopic local limits for a particular material, or allow extra tunable conjugate fields.

The proof is robust to unequal local variances and even to replacing the Gaussian local limits by other strictly positive local limiting densities with total limiting mass one, provided the same `sqrt(N)` fluctuation scale and local `L¹` convergence are retained. That is a logical extension of the proof, not needed for the current claim and not independently literature-audited here.
