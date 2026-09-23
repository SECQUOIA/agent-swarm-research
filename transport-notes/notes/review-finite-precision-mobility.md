# Independent review: mobility placement with a binned offset measurement

Reviewed 2026-09-07 by `review_localization`, following the finite-precision direction proposed by `direction_soft`.

For uniform offset bins of width Δ, the scalar expected design optimum has the order

\[
\Phi(M,\Delta)\asymp M^{-1/5}+M^{-1/4}\Delta^{1/4}
\tag{1}
\]

as M and Δ tend to zero, with constants independent of their relative rates. This review independently derives the lower and upper bounds, including the bins containing or adjoining a fold. The initial sections establish the order result; the appended review also verifies both sharp endpoint constants. No exact coefficient at a finite nonzero crossover ratio is established.

## Measurement and design convention

Take `c` uniform on `[-2,2]` and `k_c(s)=(c+cos s)²` on the circle. Partition the offset interval into consecutive bins of width Δ, permitting shorter end bins. A field `D_b>=0`, with `integral D_b=M`, is selected for each bin b. The actual offset within that bin is unknown when choosing its field. The objective is

\[
\Phi(M,\Delta)=\inf_{\{D_b\}}\frac14\sum_b\int_bJ_c(D_b)\,dc.
\]

The scalar J has the smooth-test variational definition used in the other placement notes. Designs may be arbitrary nonnegative L¹ coefficients. The result also holds for partitions with all interior bin widths uniformly comparable to Δ. A bound only on the maximum bin width is insufficient for the lower bound proportional to Δ^(1/4), since almost all bins could be much narrower.

## Lower bounds: full information and a moving root

Allowing the designer to observe the exact offset can only decrease the objective. The independently verified adaptive theorem therefore gives

\[
\Phi(M,\Delta)\ge c M^{-1/5}.
\tag{2}
\]

For the additional information cost, retain bins inside a fixed compact subset of `(-1,1)`. On each such bin, one of the two roots ranges through an interval of width `w` comparable to Δ. The offset-to-root Jacobian and local quadratic curvature are bounded above and below by positive constants, uniformly over the retained bins.

Use a fixed nonnegative compact smooth bump `f_u(s)=psi((s−u)/ell)`, with its center u moving through a fixed middle fraction of this root interval. Choose

\[
\ell=\kappa(M/w)^{1/4}.
\]

If `M<=c_1w^5`, the supports fit in a fixed enlargement of the root interval. This condition is only needed for the uncertainty-dominated regime. For any competing field in this bin, its local mobility mass is at most M. Writing B(u) for the bump's derivative energy, Fubini gives

\[
\frac1w\int B(u)du\le\frac{CM}{w\ell}.
\]

The potential energy is at most `C ell³`, while the load is proportional to ell. The quotient form of the resolvent and Jensen's inequality for the inverse denominator yield the conditional bound

\[
\mathbb E[J_c(D_b)\mid b]\ge
c\frac{\ell^2}{M/(w\ell)+\ell^3}
\ge cM^{-1/4}w^{1/4}.
\tag{3}
\]

There are order `1/Delta` retained bins, and their total probability stays bounded below. Thus, when `M<=c Delta^5`, summing (3) gives

\[
\Phi(M,\Delta)\ge cM^{-1/4}\Delta^{1/4}.
\]

In the complementary regime this second expression is at most a fixed multiple of the oracle lower bound (2). Combining the two lower bounds, and using that a sum is comparable to the larger term, proves the lower half of (1). This argument uses total mass only and therefore excludes improvements from unresolved microstructure within each bin.

## Upper construction for bins away from folds

Set

\[
W=\Delta+M^{2/7}.
\]

Consider a bin on the side with roots whose distances `t=1−|c|` from the nearest fold satisfy `t>=C W`. Across that bin, t is comparable to a representative value, the root separation is comparable to sqrt(t), and each root moves through a span

\[
w\asymp\Delta/\sqrt t.
\]

Set `ell=(M/t)^(1/5)`. Put half the mobility budget uniformly on a patch covering the entire possible location interval of each root, with an additional margin proportional to ell on both sides. Each patch length is comparable to `w+ell`, and its mobility is comparable to

\[
e=M/(w+\ell).
\]

The patches are disjoint and lie within regions of uniform quadratic comparability because

\[
\frac w{\sqrt t}\le C\frac\Delta t,
\qquad
\frac\ell{\sqrt t}=(M/t^{7/2})^{1/5},
\]

and both ratios are small when the fixed C defining the regular-bin region is sufficiently large.

For every offset in the bin, the harmonic width is comparable to `(e/t)^(1/4)`, and

\[
(e/t)^{1/4}\le(M/(t\ell))^{1/4}=\ell.
\]

Thus the root has enough distance to both artificial Neumann endpoints. The uniform interval oscillator estimate bounds the interior response by `Ce^(−1/4)t^(−3/4)`. The exterior reciprocal-potential integral is at most `C/(t ell)+Ct^(−3/2)`, and these terms are bounded by the same response scale. Therefore the common design for that bin satisfies

\[
J_c(D_b)\le C\left[M^{-1/5}t^{-4/5}
+M^{-1/4}\Delta^{1/4}t^{-7/8}\right]
\tag{4}
\]

uniformly over its offsets. Integrating over all regular bins is harmless, since both powers `4/5` and `7/8` are less than one. Their total contribution is bounded by the right side of (1).

## A common construction controls every fold bin

Classify as fold bins all bins intersecting `|1−|c||<=C W`. Since each bin has width at most Δ and `W>=Delta`, their union remains within a fixed multiple of this parameter neighborhood.

For each such bin, use the same simple design at its nearby fold: place all mobility uniformly on an interval of radius `K sqrt(W)`, with K large enough to contain all the possible roots with a fixed relative margin, and put zero mobility elsewhere. Its local diffusivity is

\[
e\asymp M/\sqrt W.
\]

The inequality `W>=M^(2/7)` is equivalent, up to fixed constants, to `W>=e^(1/3)`. The quartic diffusion length therefore fits inside this patch. The exact sine coordinate and the canonical Neumann fold estimates from [the disorder review](review-random-kinetic-barriers.md) give, after integrating the local response over `|t|<=C W`,

\[
\int_{-CW}^{CW}J_{\rm local}(t)dt
\le C e^{-1/4}W^{1/4}
\le CM^{-1/4}W^{3/8}.
\tag{5}
\]

For clarity, the inner parameter layer `|t|<=e^(1/3)` contributes at most `Ce^(−1/6)`. The remaining root side integrates `Ce^(−1/4)t^(−3/4)` to `Ce^(−1/4)W^(1/4)`, which dominates the inner layer because `W>=e^(1/3)`. The no-root side contributes at most `Ce^(−1/6)` as well. The canonical roots stay a fixed relative distance from the patch endpoints, so these bounds are uniform for the truncated Neumann problem, not just for an infinite wall.

Outside the spatial patch, the reciprocal-potential integral is at most `CW^(−3/2)` per offset. The fold parameter interval has length order W, so this adds at most `CW^(−1/2)`. It is no greater than (5), because

\[
\frac{W^{-1/2}}{M^{-1/4}W^{3/8}}
=M^{1/4}W^{-7/8}\le1.
\]

On the no-root side outside all fold bins, any design satisfies `J_c(D)<=integral 1/k_c`. Its total contribution is at most `CW^(−1/2)+C`, also smaller than the target scale.

Finally,

\[
M^{-1/4}W^{3/8}
\le C\left[M^{-1/4}\Delta^{3/8}+M^{-1/7}\right]
\le C\left[M^{-1/4}\Delta^{1/4}+M^{-1/5}\right].
\]

Both fold terms are in fact lower order than this last sum when M and Δ tend to zero. This closes the upper bound in (1), including arbitrary relative rates and any alignment of a fold with the bin grid.

## Domain and interpretation limits

The trial designs have constant positive mobility on their patches and zero mobility outside. Upper bounds use Neumann bracketing, which enlarges the original smooth-test space and does not assume continuity of artificial endpoint traces. The exterior energy has no derivative term, so its contribution is bounded pointwise by the reciprocal potential. For each retained offset all roots lie strictly within a positive-mobility patch. No uncontrolled zero-mobility kinetic root remains outside.

If a closed diffusion form is desired, these piecewise constant coefficients have the natural closure of their smooth-test form. Transitions in the zero-mobility exterior can approximate independent endpoint traces at vanishing cost. The scalar estimates do not require a pointwise differential equation at the jumps.

The order crossover occurs at `Delta` comparable to `M^(1/5)` for regular root locations. More locally, with curvature a and root uncertainty width proportional to `Delta/sqrt(a)`, comparison to the known-defect design width `(M/a)^(1/5)` gives `Delta` comparable to `M^(1/5)a^(3/10)`. The global order theorem does not give a universal sharp crossover function or coefficient.

The task is explicitly a binned measurement of c followed by design, with budget M available for every bin. Random measurement noise, unequal precision varying over the offset range, a total budget shared among all bin-specific coatings, and online learning during transport are different problems.

## Additional review: sharp fine- and coarse-resolution limits

The two endpoint equivalents added in [finite-precision-mobility.md](finite-precision-mobility.md) are also correct. They require more than the order bounds above; the following local certificates and constructions provide the additional justification.

For equal-width bins, with both M and Δ tending to zero,

\[
\frac{\Delta}{M^{1/5}}\longrightarrow0
\quad\Longrightarrow\quad
\Phi(M,\Delta)\sim
\frac{2^{6/5}C_*}{4}B(1/2,1/5)M^{-1/5},
\tag{8}
\]

and

\[
\frac{\Delta}{M^{1/5}}\longrightarrow\infty
\quad\Longrightarrow\quad
\Phi(M,\Delta)\sim
2^{-3/4}C_0B(1/2,1/8)M^{-1/4}\Delta^{1/4}.
\tag{9}
\]

### Canonical uncertain-center endpoints

For a unit-mass coefficient on the real line and an uncertain center uniform on an interval of length eta, let F(eta) be the optimized averaged inverse for the potential `(y−u)²`, as defined in the source note.

For large eta, take the mobility equal to `1/(eta+2)` on the possible-center interval padded by one unit at both ends, and zero outside. Its oscillator length is of order `eta^(−1/4)`, much smaller than the padding. Uniform Neumann oscillator localization therefore gives an interior response `C0 eta^(1/4)[1+o(1)]` for every center. The exterior reciprocal-potential integral is at most two, uniformly. This proves the sharp upper bound.

For a sharp lower bound over every unit-mass design, choose any fixed compact smooth psi and the translated fields

\[
h_u(y)=\eta^{1/2}\psi((y-u)/\eta^{-1/4}).
\]

Their averaged source-minus-potential expression is exactly `eta^(1/4)(2I_psi−V_psi)`. Their averaged squared derivative is at most `eta^(1/4)T_psi` at every spatial point: averaging centers over the finite interval can only truncate the nonnegative derivative kernel. The mass budget therefore gives the lower bound `eta^(1/4)(2I_psi−V_psi−T_psi)`. Taking the oscillator variational supremum proves

\[
F(\eta)\sim C_0\eta^{1/4}.
\tag{10}
\]

This proof does not assume an optimal coefficient is uniform, or that arbitrary competitors are regular.

At eta tending to zero, exact knowledge of the center gives `F(eta)>=C_*`. For the reverse bound, approximate the known-center optimal coefficient by a normalized compact smooth coefficient which dominates `(1−epsilon)` times that optimum and is positive on a fixed neighborhood of all possible small center shifts. Such coefficients can have mass exactly one and response tending to C_* as epsilon tends to zero. On their fixed positive-mobility patch, the shifted-potential forms and their source inverses vary continuously for small shifts. Outside the patch the reciprocal-potential tail also varies continuously, since the centers remain a positive distance from its boundary. First send eta to zero for a fixed approximate coefficient, then epsilon to zero. Hence `F(eta)->C_*`.

### Fine bins: recovering the oracle coefficient

The lower bound in (8) follows directly from the oracle optimum. For the upper bound, retain offsets in a fixed compact subset of `(-1,1)`. In each bin freeze the curvature at a representative offset and place two scaled copies of a fixed smooth approximation to the exact adaptive profile, with half the budget each. The center uncertainty divided by the adaptive design length is proportional to

\[
\Delta M^{-1/5}a^{-3/10},
\]

and tends to zero uniformly on this retained region. The preceding continuous-dependence argument, quadratic potential comparison, and the uniform local Taylor remainder therefore give the sharp adaptive coefficient on the retained bins. The approximate profile can be chosen arbitrarily close to optimal before taking the small-budget limit.

For bins outside the retained region use the order-level trial construction already reviewed above. After multiplication by `M^(1/5)`, its regular-root envelope is

\[
C t^{-4/5}
+C(\Delta/M^{1/5})^{1/4}t^{-7/8}.
\]

Both singular powers are integrable, the second prefactor tends to zero, and the fold-bin bound is lower order. One may thus shrink the omitted fold neighborhoods after taking the joint limit. This proves the matching upper constant in (8), rather than merely the adaptive order.

### Coarse bins: the paired-root coefficient

On a fixed regular offset region, write `a=1−c²`. Each bin's root span is

\[
w=\Delta/\sqrt a\,[1+o(1)]
\]

uniformly. Use frozen local curvature a and reference diffusivity `e=M/(2w)`. The harmonic length is `ell=(e/a)^(1/4)`, and `ell/w` tends to zero uniformly because `Delta/M^(1/5)` tends to infinity.

A sharp lower bound need not assume that a competitor divides its mass evenly. Use two harmonic test fields centered at the actual paired roots, each with amplitude `(ea)^(−1/2)` and shape psi at scale ell. Let `z=e^(−1/4)a^(−3/4)`. Their averaged source-minus-potential expression is

\[
2z(2I_\psi-V_\psi)[1+o(1)].
\]

The conditional root density is `(1+o(1))/w`, uniformly in the bin. The averaged squared derivative has the global upper bound

\[
(1+o(1))\frac{T_\psi}{w}e^{-5/4}a^{-3/4}.
\]

The two spatial root neighborhoods are disjoint. Integration against any competing mobility with total mass M costs at most `2zT_psi[1+o(1)]`, since `M/w=2e`. The bin edges only truncate the derivative kernel and cannot increase the bound. Taking the oscillator variational supremum therefore proves the conditional lower coefficient `2zC0`. This is an unrestricted lower bound for the original bin problem.

For the matching upper bound, put half the budget uniformly on each possible-root arc and pad it by a length p satisfying `ell<<p<<w`. The added mass fraction tends to zero; the artificial boundaries lie many harmonic lengths from every possible root; and the exterior reciprocal-potential contribution, at most `C/(ap)`, is negligible relative to `1/(a ell)`. Potential curvature and the offset-to-root Jacobian vary by `o(1)` uniformly on compact regular offset regions. Thus the conditional equivalent is

\[
2^{5/4}C_0a^{-7/8}M^{-1/4}\Delta^{1/4}.
\]

Multiplication by the disorder density 1/4 and integration in c gives

\[
\frac{2^{5/4}C_0}{4}\int_{-1}^1(1-c^2)^{-7/8}dc
=2^{-3/4}C_0B(1/2,1/8),
\]

confirming the coefficient in (9). The regular-bin estimate (4), normalized by the coarse scale, controls the omitted folds: its adaptive term has prefactor `(M^(1/5)/Delta)^(1/4)` tending to zero, while `t^(−7/8)` is integrable. Here `W` is comparable to Delta, and the fold-bin bound divided by the coarse scale is `O(Delta^(1/8))`, tending to zero. The compact-region Riemann sums therefore extend to the entire ensemble.

The proposed finite, nonzero-ratio crossover expressed through F still requires a separate optimization-localization theorem. The verified endpoint constants and order bounds do not prove that interior crossover formula.


## Final integration: finite-bulk optimal values

The separate [scalar-to-bulk transfer theorem](scalar-to-bulk-design-transfer.md), independently checked by this reviewer and the parent, now extends the reviewed scalar results. For fixed smooth bulk geometry, fixed positive bulk diffusivity, `u∈L²`, constant affinity, and `B=KV²/Z>0`, the full-bulk first-moment optimum satisfies `Φ_bulk/(BΦ)=1+O(M^{1/5}log(1/M))`, uniformly over the bin observations. The cosine family supplies the required uniform rate bound and positive integral. The same-budget mixture with a vanishing uniform background remains admissible in the unrestricted policy class.

Thus both sharp endpoint constants and the uniform order law are also verified for full-bulk optimized flow dispersion after multiplication by `B`. This adds no claim about the interior crossover, original profile convergence, or a uniform remainder for arbitrary unmixed designs. See the transfer note for the exact assumptions and proof.
