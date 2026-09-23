# Mobility design when the kinetic defect location is unknown

Research note, 2026-09-07. Derived by `review_optimal_placement` following a direction proposed by the parent. The proof below includes unrestricted mobility fields that depend on the budget and can oscillate on arbitrarily short scales. The scalar theorems have passed [independent review](review-robust-mobility-design.md). The mathematical framework of expected compliance optimization is established; the potentially new claim is the singular transport law and the quantitative value of knowing the kinetic defect locations.

## Model and sharp optimum

On the circle `0≤s<2π`, let

\[
 k_c(s)=(c+\cos s)^2,\qquad c\sim\operatorname{Uniform}[-2,2],
\]

\[
 J_c(D)=\sup_f\left\{2\int f-\int[D(s)|f'|^2+k_c(s)f^2]\right\},
 \qquad D\ge0,\quad\int D=M.
\]

The supremum is over smooth periodic fields, with the natural energy completion when appropriate. An infinite value is permitted for some admissible designs. A design made before `c` is observed must use the same deterministic field `D` for the whole ensemble. Define

\[
 \Phi(M)=\inf_{D:\,\int D=M}\mathbb E_cJ_c(D).
\]

Set

\[
 C_0=\frac\pi2\frac{\Gamma(1/4)}{\Gamma(3/4)},\qquad
 w(s)=\frac14|\sin s|^{-1/2},\qquad
 Z_w=\int_0^{2\pi}w(s)^{4/5}ds
 =4^{-4/5}\,2B(3/10,1/2).
\]

Then the sharp asymptotic is

\[
 \boxed{\Phi(M)\sim C_0Z_w^{5/4}M^{-1/4}.}
 \tag{1}
\]

An asymptotically optimal design is

\[
 \boxed{D_M(s)=M d_*(s),\qquad
 d_*(s)=\frac{|\sin s|^{-2/5}}{2B(3/10,1/2)}.}
 \tag{2}
\]

The endpoint singularities are integrable. Their pointwise values at `s=0,π` can be assigned arbitrarily without changing the coefficient. The design has a strictly positive lower bound proportional to `M`, is smooth away from those two points, and defines a natural weighted diffusion form. If only bounded smooth coefficients are allowed, smooth bounded approximations to `d_*` achieve the same asymptotic infimum by a diagonal choice. A fixed numerical upper bound or fixed fabrication length is a different constraint.

Crucially, the lower bound for (1) ranges over all admissible `D`, including budget-dependent narrow spikes, vanishing regions, and arbitrarily rapid oscillations. Formula (1) is stronger than minimizing an approximation valid only for fixed smooth shapes.

## Fixed shapes and the upper bound

For each fixed `|c|<1`, the two simple zeros have curvature `a=1−c²`. For a positive shape `d` smooth at those zeros, the local quadratic theorem gives

\[
 M^{1/4}J_c(Md)\longrightarrow
 C_0\sum_{c+\cos r=0}d(r)^{-1/4}|\sin r|^{-3/2}.
 \tag{3}
\]

There are no zeros when `|c|>1`, and the scaled value then tends to zero. To average (3), change variables from `c` to the root position `r`: on each root branch, `dc=|sin r|dr`. Including the ensemble density `1/4` yields

\[
 \mathbb E J_c(Md)\sim
 C_0 M^{-1/4}\int w(r)d(r)^{-1/4}dr.
 \tag{4}
\]

This change of variables is the elementary marked-zero/Kac–Rice calculation for this one-parameter ensemble.

The exchange of limit and expectation in (4) is justified when `d` has a positive lower bound `b`. Form ordering gives `J_c(Md)≤J_c(Mb)`. The uniform constant-mobility fold bounds in [the independent random-barrier review](review-random-kinetic-barriers.md) imply an integrable majorant for `M^{1/4}J_c(Mb)`, proportional near `c=±1` to `|1−|c||^{−3/4}`. Therefore dominated convergence applies. This includes `d_*`, despite its integrable singularities: for almost every `c`, its zeros lie in neighborhoods where `d_*` is smooth, and potential-energy bounds control the rest of the wall without requiring `d_*` to be bounded there.

Hölder's inequality gives

\[
 \int w d^{-1/4}\ge\left(\int w^{4/5}\right)^{5/4}
 \quad\text{when}\quad\int d=1,
\]

with equality at (2). Thus (4) proves the upper bound in (1). On its own this calculation would not exclude better budget-dependent microstructure; that is the role of the next argument.

## A dual lower bound uniform over every mobility placement

The proof uses an ensemble of localized test fields. It does not exchange an infimum and a supremum.

Fix a compact interval of offsets strictly inside `(-1,1)`. Let `E` be the corresponding two closed arcs of root positions, so `|sin r|` is bounded away from zero on a neighborhood of `E`. Write

\[
 \rho(r)=\frac14|\sin r|,\qquad
 a(r)=\sin^2r,\qquad
 w(r)=\rho(r)a(r)^{-3/4},
\]

\[
 Z_E=\int_Ew^{4/5},\qquad
 d_E(r)=w(r)^{4/5}/Z_E.
\]

Use the displayed smooth positive formula for `d_E` on a slightly larger neighborhood of the arcs. Its values elsewhere play no role. It is a reference width parameter for the test fields; it need not be an admissible global design.

Choose any fixed real `ψ∈C_c^∞(R)` and define

\[
 I_\psi=\int\psi,\qquad
 V_\psi=\int y^2\psi(y)^2dy,\qquad
 T_\psi=\int|\psi'(y)|^2dy.
\]

For each retained offset and each of its two roots `r`, set

\[
 \ell_r=\left(\frac{M d_E(r)}{a(r)}\right)^{1/4},\qquad
 h_{M,r}(s)=\frac1{\sqrt{M d_E(r)a(r)}}
 \psi\left(\frac{s-r}{\ell_r}\right).
\]

Let `h_{M,c}` be the sum of the two root fields. Set it to zero for offsets outside the retained interval. For sufficiently small `M` the two supports are disjoint and contained in the chosen regular neighborhoods.

The averaged non-gradient part of the dual functional is

\[
 A_M:=\mathbb E_c\left[2\int h_{M,c}-\int k_c h_{M,c}^2\right]
 =M^{-1/4}Z_E^{5/4}(2I_\psi-V_\psi)+o(M^{-1/4}).
 \tag{5}
\]

Indeed, `k_c(s)=a(r)(s−r)²+O(|s−r|³)` uniformly on the retained root arcs. Both the source and quadratic potential integrals scale as `M^{−1/4}d_E(r)^{−1/4}a(r)^{−3/4}`. Multiplying by the root density `ρ(r)` and integrating yields `∫_E w d_E^{−1/4}=Z_E^{5/4}`. The cubic Taylor error is relatively `O(M^{1/4})` for fixed arcs and test function.

The averaged squared derivative satisfies the uniform bound

\[
 G_M(s):=\mathbb E_c|\partial_sh_{M,c}(s)|^2
 \le M^{-5/4}Z_E^{5/4}[T_\psi+o(1)]
 \quad\text{for every }s.
 \tag{6}
\]

Here uniformity in `s` is essential. To see it directly, write

\[
 G_M(s)=M^{-3/2}\int_E\rho(r)d_E(r)^{-3/2}a(r)^{-1/2}
 \left|\psi'\left(\frac{s-r}{\ell_r}\right)\right|^2dr.
\]

When this integrand is nonzero, `|s−r|=O(M^{1/4})`. All coefficient functions and their derivatives are bounded on a fixed neighborhood of `E`. The map `y=(s−r)/ℓ_r` is monotone on the contributing interval, and its Jacobian is `|dr/dy|=ℓ_r[1+O(M^{1/4})]`, uniformly in `s`. Replacing the smooth coefficients by their values at `s` incurs the same relative error. The leading coefficient becomes

\[
 M^{-5/4}\rho(s)d_E(s)^{-5/4}a(s)^{-3/4}
 =M^{-5/4}w(s)d_E(s)^{-5/4}
 =M^{-5/4}Z_E^{5/4}.
\]

At the endpoints of the retained arcs the transformed integration set can be truncated, which only decreases the integral of the nonnegative `|ψ′|²`. Outside an `O(M^{1/4})` neighborhood of the arcs, `G_M=0`. This proves (6) globally, including the arc edges.

For any admissible coefficient, including a coefficient chosen differently at each `M`, the variational formula now gives

\[
 \mathbb E J_c(D)\ge A_M-\int DG_M
 \ge A_M-M\|G_M\|_\infty.
\]

Consequently

\[
 \liminf_{M\downarrow0}M^{1/4}\Phi(M)
 \ge Z_E^{5/4}(2I_\psi-V_\psi-T_\psi).
 \tag{7}
\]

The harmonic-oscillator variational identity is

\[
 \sup_{\psi\in C_c^\infty}
 \left(2\int\psi-\int[|\psi'|^2+y^2\psi^2]\right)=C_0.
\]

Take this supremum in (7), then expand the retained offset interval to `(-1,1)`. Monotone convergence gives `Z_E→Z_w`, proving the sharp lower bound in (1). No regularity or length-scale assumption on the actual design entered the argument.

## The quantitative value of observing the defect locations

Define the adaptive value

\[
 \Psi(M)=\mathbb E_c\left[\inf_{D:\,\int D=M}J_c(D)\right].
\]

This assumes the offset, and therefore both defect locations, is known before choosing the design. It is a different decision problem from `Φ`. For fixed `|c|<1`, the two-zero allocation theorem gives

\[
 \inf_DJ_c(D)\sim C_*2^{6/5}(1-c^2)^{-4/5}M^{-1/5},
 \qquad C_*=12(3/80)^{1/5}.
\]

The adaptive ensemble equivalent is

\[
 \boxed{\Psi(M)\sim
 \frac{C_*2^{6/5}}4B(1/2,1/5)M^{-1/5}.}
 \tag{8}
\]

The endpoint singularity of the sample coefficient is integrable, but that fact alone does not justify (8). The following uniform trial bounds supply the missing control.

Near either fold put `t=1−|c|`, positive on the side with two zeros, and write `j_M(c)=inf_DJ_c(D)`. For fixed small `t_0` there are constants such that

\[
 j_M(c)\le C\begin{cases}
 M^{-1/5}t^{-4/5},&t\ge L M^{2/7},\\
 M^{-3/7},&|t|\le L M^{2/7},\\
 |t|^{-3/2},&t\le-L M^{2/7},
 \end{cases}
 \tag{9}
\]

where `L` is fixed sufficiently large.

For the first bound, each root lies a distance comparable to `√t` from the fold center and has quadratic curvature comparable to `t`. Place half the budget in the explicit quadratic design around each root, using a lower comparison curvature `a_−=c_1t`. Its width is of order `(M/t)^{1/5}`, which fits within a fixed small multiple of `√t` when `t≥L M^{2/7}`. Potential comparison bounds the interior response by `C/(tR)`. Outside the two supports, the reciprocal-potential integral is bounded by `C/(tR)+Ct^{-3/2}`. The last term is smaller than the first in this regime, giving the stated bound.

For the middle bound, put constant mobility of order `M^{6/7}` on an interval of radius `L_1M^{1/7}` around the fold center, and put zero mobility outside. Choose the fixed constant `L_1` large enough that all nearby roots for `|t|≤L M^{2/7}` lie strictly inside the interval. The exact fold coordinate `z=2sin(x/2)` changes the potential to `(z²/2−t)²`, with metric factors uniformly approaching one. Rescaling `z=M^{1/7}y` produces a local operator of order `M^{4/7}` on a fixed interval, with parameter `t/M^{2/7}` in a compact set. Its natural-endpoint inverse integral is uniformly bounded: the derivative coefficient is uniformly positive, and none of these fixed-interval potentials is identically zero. The physical integrated response is therefore at most `CM^{-3/7}`. The outside reciprocal-potential integral has the same bound because the support contains the roots with a fixed scaled margin.

For the last bound there are no zeros. Any placement satisfies `J_c(D)≤∫1/k_c`, and that reciprocal integral is `O(|t|^{-3/2})` near the fold. An arbitrary design with the required budget is sufficient.

In all three regimes, (9) implies the common integrable domination

\[
 M^{1/5}j_M(c)\le C|t|^{-4/5}\qquad(t\ne0).
\]

Away from the folds the bounds are uniform. Dominated convergence proves (8), including the contribution from offsets with no zeros. The parameter layer of width `M^{2/7}` contributes only `O(M^{-1/7})` to the unnormalized adaptive mean, which is smaller than its leading `M^{-1/5}` term.

The resulting constants are

| Design information | Leading expected response |
|---|---:|
| Uniform mobility, chosen before observing `c` | `19.2932034452 M^(−1/4)` |
| Optimal placement before observing `c` | `18.3860636501 M^(−1/4)` |
| Placement after observing `c` | `22.4046282307 M^(−1/5)` |

Thus the optimal predetermined spatial shape improves the uniform leading constant by about 4.7%, while learning the defect locations changes the budget exponent. Quantitatively,

\[
 \frac{\Psi(M)}{\Phi(M)}\sim1.2185657929\,M^{1/20}\longrightarrow0.
\]

This is a small-budget asymptotic in the dimensionless model. The power `1/20` makes convergence slow; the statement does not by itself demonstrate a large gain at a particular experimental budget.

## Interpretation, provenance, and open checks

The blind-design optimum retains the uniform-mobility exponent because the defect can occur throughout the wall. The nonuniform optimal shape concentrates more mobility near the extrema of `cos s`, where the two kinetic zeros approach each other and their slopes become small. The derivative-density certificate is what excludes hidden improvements from arbitrarily narrow or rapidly varying allocations.

Fixed-budget conductivity design, compliance minimization, and saturated-gradient duality are established. [Buttazzo, Oudet and Velichkov, *A free boundary problem arising in PDE optimization*](https://arxiv.org/pdf/1506.00141) provides a close reinforcement precedent, as detailed in [the placement prior-art audit](optimal-mobility-placement-prior-art.md). Design under uncertainty also predates this calculation: [*Robust topology optimization: Minimization of expected and variance of compliance*](https://researchportal.bath.ac.uk/en/publications/robust-topology-optimization-minimization-of-expected-and-variance/) studies expected compliance under uncertain loads, while [Jouve, Allaire and de Gournay, *Shape and topology optimization of the robust compliance via the level set method*](https://www.numdam.org/item/COCV_2008__14_1_43_0/) studies worst-case compliance. Those general decision frameworks are not claimed as new.

The prospective contribution here is a sharp small-budget expected resolvent optimum for a random reaction field, proved over unrestricted mobility placements, together with the change of asymptotic exponent when the random defect locations are known before design. The Hölder allocation by itself is elementary. The [targeted overlap search](robust-design-prior-art.md) found established stochastic conductivity design, but no exact match to these singular transport laws. Its access and scope limits remain relevant to any novelty claim.

This note develops the scalar surface functional. The first-moment finite-transverse-bulk extension is established separately in [review-robust-finite-bulk.md](review-robust-finite-bulk.md), using uniform control of selected designs. A later [general transfer theorem](scalar-to-bulk-design-transfer.md) preserves optimal values and sharp constants by adding a vanishing uniform share of mobility. [Higher disorder moments](risk-sensitive-mobility.md) and [finite-precision observations](finite-precision-mobility.md) are developed in separate notes. Minimax objectives and a fixed mobility cap are outside the present results.

## Independent review and finite-budget qualification

The separate reviewer independently verified both expectation theorems, the uniform derivative-density lower bound including arc edges, and the adaptive fold bounds. Its report is [review-robust-mobility-design.md](review-robust-mobility-design.md). The lower certificate also applies to a finite-measure relaxation of the mobility budget because its averaged derivative bound is pointwise.

Finite-budget calculations reveal a useful limitation. The explicit asymptotic blind shape (2) can perform worse than uniform mobility before the small-budget regime is sufficiently developed:

| `M` | Asymptotic blind shape / uniform response | Adaptive explicit trial / blind response |
|---:|---:|---:|
| `10⁻³` | `1.03364` | `0.826` |
| `10⁻⁶` | `0.99844` | `0.594` |
| `10⁻⁹` | `0.97908` | `0.430` |

Thus its eventual 4.70% prefactor improvement is not a guaranteed finite-budget gain. The asymptotic profile is not asserted to be the exact finite-budget optimizer. At `M=10⁻⁹`, the scaled blind response was about `18.016` against the limit `18.386`, while the uniform value was about `18.401` against `19.293`; differing corrections explain the slow crossover. The parent's refined calculation used 32,768 wall cells and 60-point parameter quadrature and was stable to about `10⁻⁴` relative. The reproducible calculations are in [check_robust_design.py](../scripts/check_robust_design.py), with outputs in [robust-design-checks.json](../results/robust-design-checks.json). These numerical values support convergence and document a practical limitation; they do not prove exact finite-budget optimality of either explicit design.

