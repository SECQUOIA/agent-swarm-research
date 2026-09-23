# Independent review of multiphase reservoir geometry

Date: 2026-09-06. Scope: mathematical review of `research/multiphase-reservoir-geometry.md`, including the subsequently added equation (9a). The main file was not edited. Literature priority is being reviewed separately.

**Verdict:** the exact weight invariant, three-phase iff theorem, equal- and unequal-weight optimal total-variation limits, affine invariants, cosphere criterion, full-distribution classification (9a), and upper bound (10) are correct for the stated fixed finite Gaussian mixture with positive fixed weights, distinct fixed phase points, common covariance `N I_d`, and nonnegative scalar reservoir curvature. The proof of the unequal-weight optimal limit requires explicitly ruling out loss of only the central phase and controlling arbitrary temperature shifts; those details are supplied below. No equality extension of (10) is being certified.

## 1. Exact Gaussian integration

Let a component have mean `N e` and covariance `N I_d`. Combining its exponent with `t·E−κ|E|²/2` gives precision `(1+κN)/N`, mean

\[
m_e=\frac{N(e+t)}{1+\kappa N},
\]

and the integration factor

\[
(1+\kappa N)^{-d/2}
\exp\left\{\frac{N|t|^2}{2(1+\kappa N)}
+\frac{Nt\cdot e}{1+\kappa N}
-\frac{\kappa N^2|e|^2}{2(1+\kappa N)}\right\}.
\]

The first two factors outside the phase-dependent linear/quadratic terms are common to every phase and cancel in the normalized weights. Thus equations (2) and (7), including every factor of `N` and `1/2`, are correct. For scalar points −1,0,1, the product of the outer weights divided by the square of the central weight cancels the field and normalization, leaving exactly equation (3).

## 2. A mixture-matching lemma that closes the permutation loophole

Here is a precise argument needed by both the scalar iff theorem and (9a). Let

\[
p_N=\sum_{i=1}^k w_i\mathcal N(Ne_i,NI_d),
\]

with fixed distinct `e_i`, fixed `w_i>0`, and fixed finite `k`. Write transformed component means as

\[
N(s_Ne_i+a_N),\qquad
s_N=(1+\kappa_NN)^{-1}\in(0,1],\qquad
 a_N=s_Nt_N,
\]

and their covariance as `Ns_N I_d`.

Suppose `TV(p_N,q_N)→0`. On the macroscopic variable `E/N`, each transformed component has covariance at most `I_d/N`; hence one such component cannot provide nonvanishing mass to two disjoint small neighborhoods of different target phase points. Every target phase has a fixed positive probability. There are exactly as many transformed components as target neighborhoods, so all transformed components must have nonvanishing weights and must match the target points bijectively. In particular, the transformed centers are bounded, and therefore `a_N` is bounded.

For `k≥2`, extract any subsequence on which `s_N`, `a_N`, and the finite matching permutation converge. Its limiting homothety `e↦se+a` maps the finite phase set onto itself. Comparing the diameter of the image with the original positive diameter gives `s=1`. A finite nonempty set cannot be invariant under a nonzero translation: for example, its arithmetic centroid would move by `a`. Hence `a=0`. The limiting matching is the identity because the `e_i` are distinct. This works on every subsequence, proving

\[
s_N\to1,\qquad a_N\to0,\qquad v_{i,N}\to w_i,
\]

with the original labels, not just after an unknown permutation.

The same separated neighborhoods isolate each matched component in total variation. Their complement has vanishing probability, so after normalizing the restrictions, componentwise Gaussian total variation must tend to zero. Gaussian convergence consequently requires

\[
\sqrt N\big[(s_N-1)e_i+a_N\big]\longrightarrow0
\tag{R1}
\]

for every `i`, as well as `s_N→1`. One can see the mean requirement by projecting onto the normalized mean-difference direction and comparing one-dimensional Gaussian half-space probabilities.

Thus arbitrary common translations, including translations by one phase spacing, do not evade the weight or shape constraints when full-distribution convergence is required.

## 3. Scalar iff theorem and its multivariate extension

For the three scalar phases, the matching lemma gives `v_i/w_i→1`. Taking logarithms in (3) forces `α_N→0`. With `x_N=κ_N N≥0`,

\[
\alpha_N=\frac{Nx_N}{1+x_N}.
\]

This tends to zero iff `κ_N N²=Nx_N→0`: the forward implication first excludes `x_N` bounded away from zero, then uses `1+x_N→1`. This proves necessity without assuming a priori that the reservoir is large or that the field is small.

For sufficiency, `t_N=0` makes the finite collection of weight corrections vanish. The covariance ratio tends to one, and the standardized component mean corrections have magnitudes

\[
\frac{\kappa_NN^{3/2}|e_i|}{1+\kappa_NN}\to0.
\]

Componentwise Gaussian total-variation convergence then implies mixture convergence.

For (9a), subtract (R1) for any two distinct phase points. It follows that

\[
\frac{\kappa_NN^{3/2}}{1+\kappa_NN}|e_i-e_j|\to0.
\]

Since the lemma already gives `κ_NN→0`, this forces `κ_NN^(3/2)→0` for **every** mixture with two or more phases.

If the phase set is cospherical with center `c`, choosing `t_N=κ_NN c` gives `z_N=α_Nc` and restores all component weights exactly. The standardized shift is

\[
\frac{\kappa_NN^{3/2}(c-e_i)}{1+\kappa_NN},
\]

so the universal necessary scale is also sufficient in this case.

If the phase set is not cospherical, an affine dependence `a` exists for which `Σa_i|e_i|²≠0`. The weight invariant (8) together with `v_i/w_i→1` forces `α_N→0`, and hence the stronger condition `κ_NN²→0`. Again `t_N=0` proves sufficiency.

For one phase, choose `t_N=κ_NN e_1` to align the mean exactly. Only the covariance changes. Total-variation convergence is equivalent to its ratio `s_N→1`, or `κ_NN→0`. A shift cannot compensate for a nonvanishing Gaussian width difference. All three scales in (9a) and the subsequent single-phase statement therefore pass independent review.

## 4. Uniform lower bound for the unequal three-phase optimum

Assume regime (4): `κ_NN^(3/2)→0` and `κ_NN²→∞`. Then `κ_NN→0`, `α_N→∞`, and `α_N=o(sqrt(N))`. Define three target windows

\[
W_i=\{E:|E-Ne_i|\leq N/8\},\quad e_i=-1,0,1.
\]

Their reference probabilities tend to `w_i`, with exponentially small errors. Fixed-fraction macroscopic windows suffice here because they remain disjoint and contain essentially all of each target Gaussian. They are an alternative to the expanding standardized windows suggested in the main file.

First consider every field with `|t|<1/4`. Since `κ_NN→0`, the transformed center of component `j` stays a distance at least a fixed positive multiple of `N` away from `W_i` whenever `j≠i`, uniformly in these fields. Its standard deviation is at most `sqrt(N)`. Hence

\[
q_{N,t}(W_i)\leq v_i+O(e^{-cN})
\]

uniformly, for some `c>0`. Equation (3) gives

\[
v_+v_-=K e^{-\alpha_N}v_0^2\leq K e^{-\alpha_N},
\qquad K=\frac{w_+w_-}{w_0^2}.
\]

At least one **outer** weight is therefore at most `sqrt(K)e^(−α_N/2)`. Choosing that outer window as a measurable test set yields

\[
\operatorname{TV}(p_N,q_{N,t})
\geq\min(w_-,w_+)-\sqrt K e^{-\alpha_N/2}-O(e^{-cN}).
\tag{R2}
\]

The central phase being the smallest reference weight does not weaken this bound: it is specifically an outer transformed component that must become negligible.

Now consider all fields `t≥1/4`. The log weight ratio of the positive component to the central one is

\[
\log(v_+/v_0)=\log(w_+/w_0)+z_N-\alpha_N/2.
\]

Here `z_N≥N/[4(1+κ_NN)]`, whereas `α_N=o(sqrt(N))`. The positive component therefore has probability `1−O(e^(−cN))`, uniformly in these fields. Its mean is at least `1.25N/(1+κ_NN)`, lying beyond every target window by a fixed multiple of `N` for sufficiently large `N`. Thus the union of all three target windows has `q` probability tending uniformly to zero, and `TV→1` uniformly. The argument for `t≤−1/4` is identical with the negative phase.

Combining the two field ranges proves the desired lower bound uniformly over **all** real `t`, including fields diverging with `N`. This also justifies interchanging the asymptotic claim with the optimization over fields in equations (5)–(6).

For attainment when the negative phase is to be lost, take `t_N=κ_NN/2`, equivalently `z_N=α_N/2`. The limiting weights are

\[
(v_-,v_0,v_+)\to
\left(0,\frac{w_0}{w_0+w_+},\frac{w_+}{w_0+w_+}\right).
\]

Regime (4) makes all component shape changes negligible in total variation. The distance from the original weight vector to this conditional weight vector is `w_-`. The opposite field loses the positive phase and attains distance `w_+`. Together with (R2), this proves equation (6); equation (5) is its equal-weight special case.

No numerical optimization over a bounded field interval is needed to exclude an unobserved better solution at a large field: the preceding proof controls that possibility explicitly.

## 5. Affine invariants and sphere condition

Taking logarithms in (7) gives

\[
\log(v_i/w_i)=z\cdot e_i-\frac\alpha2|e_i|^2-\log Z.
\]

Contracting against any affine dependence eliminates `z` and `log Z`, proving (8). For `α>0`, all weights are restored exactly iff the vector with entries `|e_i|²` belongs to the span of the constant vector and the coordinate vectors. This is precisely (9). Completing the square gives `|e_i−c|²=|c|²+b`, proving the sphere statement. The radius is automatically nonnegative because there is at least one phase point satisfying it.

An affinely independent set of at most `d+1` points admits such a solution by full row rank. A larger set can also satisfy it; the note correctly avoids asserting that phase count alone determines the obstruction.

Minor scope clarification: the anisotropic ellipsoid language presumes a positive-definite effective quadratic metric. A merely positive-semidefinite reservoir curvature can yield a cylindrical or degenerate quadratic level set instead. This does not affect any of the scalar-isotropic theorems, whose hypotheses are explicit.

## 6. Equation (10)

For any fixed finite center `c`, put `z=αc`. Relative log weights differ by `−α(|e_i−c|²−|e_j−c|²)/2`. Since `α→∞`, only the minimizing contact set `F` survives, with conditional reference weights. The associated choice `t_N=κ_NN c` makes all standardized mean shifts vanish under regime (4), while the covariance ratio tends to one. Thus this particular field sequence attains limiting total variation `1−Σ_{i∈F}w_i`.

Optimizing over the finitely many possible contact subsets gives exactly the stated limsup upper bound. Whether unbounded field centers, nested face limits, or partial component displacement can improve the general multivariate optimum is not resolved by this argument. The main file correctly refrains from claiming equality.

## Review status and limits

The results above are exact statements about the specified Gaussian mixture. They do not by themselves transfer to real finite systems with interfacial valleys, non-Gaussian moderate deviations, unequal phase covariance, changing phase locations, or additional thermodynamic fields. The main file states these limits appropriately.

This review supplies independent analytical verification, including arbitrary-field control and the finite-set homothety argument. It does not establish literature novelty, and it does not duplicate the separate numerical quadrature being run by the parent agent.
