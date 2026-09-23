# Independent mathematical review of the nucleation scouting note

Date: 2026-09-06. Reviewer: independent subagent. Scope: equations (1)–(4), network sharpness, and physical normalization in `scouting-nucleation.md`. This review verifies mathematics; it does not establish literature novelty.

## Verdict

Equations (1)–(4) are correct under the stated assumptions of a fixed reversible divergence-form generator, fixed boundaries, and sufficient existence and differentiability. The sharp network examples are correct. The careful distinction between capacity rate, equilibrium event frequency, and a rate normalized by the last-visited basin is necessary and is handled correctly.

One minor literal correction is needed: the interval width vanishes exactly for constant Q only when the perturbation parameter is nonzero. At λ = 0 the width vanishes for every Q.

## Independent derivation

Write K = wD, C = E(q,q), and let V be the space of admissible variations vanishing on A and B. The minimizer obeys E(q,v) = 0 for every v in V.

1. The old potential q₀ is admissible after changing K₀ to e^{λQ}K₀, and its new energy is C₀ Eν₀[e^{λQ}]. This proves the upper bound in (1).
2. The old current j₀ = K₀∇q₀/C₀ has the required divergence, outer-boundary condition, and total flux. Its new resistance is Eν₀[e^{−λQ}]/C₀. Thomson minimization gives the lower bound in (1), with the stated inequality direction.
3. Since Z_A(λ)/Z_A(0) = E_A,₀[e^{λQ}], division gives (2) without approximation. The same argument holds with the full partition integral for event frequency.
4. Differentiating stationarity gives E(h,v) = −∫Q∇q·K∇v, where h = ∂λq. The envelope derivative is C′ = ∫Q∇q·K∇q. A second derivative gives C″ = ∫Q²∇q·K∇q − 2E(h,h). Therefore (log C)″ = Varν(Q) − 2E(h,h)/C, establishing (4).
5. Let m = EνQ. Since E(q,h) = 0, E(h,h) = −∫(Q−m)∇q·K∇h. Cauchy–Schwarz gives E(h,h) ≤ C Varν(Q), including the E(h,h) = 0 case. This proves both inequalities in (3). Applying the scalar result to every linear combination of field observables gives the claimed matrix order; no separate matrix differentiation assumption beyond existence of the Hessian is needed.

The finite-field proof also independently implies the curvature sandwich by applying the same reference-state bound at any λ and expanding in a new increment. The two proofs agree on the factor of two in (4).

## Sharpness and exact continuum equality conditions

For a parallel network, C = Σc_e and ν_e = c_e/C. For a chain, C = 1/(Σ1/c_e), the potential drop on edge e is C/c_e, and ν_e = C/c_e. Thus the arithmetic and harmonic bounds are attained, respectively, with the claimed signs of curvature. Given any strictly positive probability vector p_e, setting parallel conductances proportional to p_e and series resistances proportional to p_e realizes the same reference dissipation distribution. Overall scales can also match C₀. Consequently even the complete law of Q under ν₀ and the reference capacity do not determine the response.

Exact continuum examples need not be limited to thin-channel limits. Two useful sufficient conditions can be established directly.

**Upper equality.** If q₀ remains harmonic for Kλ, it remains the Dirichlet minimizer and the upper finite-field bound is exact. For differentiable Q and nonzero λ, a sufficient condition is

\[
\nabla Q\cdot D\nabla q_0=0.
\]

In a rectangle with absorbing left and right sides, reflecting horizontal sides, D = I, and w₀ depending only on the transverse coordinate y, q₀ = x/L. Any Q(y) satisfies the condition. It gives exact positive-variance upper saturation in a connected continuum domain. This example uses a piecewise smooth boundary; a circular annulus with absorbing inner and outer circles, radial w₀, and Q depending smoothly on angle gives a smooth-boundary example.

**Lower equality.** Suppose Q = F(q₀), with the integrals below finite. The pushforward of ν₀ under q₀ is uniform on [0,1]. Indeed, testing stationarity with G(q₀) − G(0) − [G(1)−G(0)]q₀ gives

\[
\mathbb E_{\nu_0}G'(q_0)=G(1)-G(0).
\]

Define Hλ(t) = ∫₀ᵗ e^{−λF(s)}ds and Iλ = Hλ(1). Then

\[
q_\lambda=H_\lambda(q_0)/I_\lambda,
\qquad
K_\lambda\nabla q_\lambda=K_0\nabla q_0/I_\lambda,
\qquad
\frac{C_\lambda}{C_0}=\frac1{I_\lambda}
=\frac1{\mathbb E_{\nu_0}e^{-\lambda Q}}.
\]

The current is divergence free and the boundary values are correct, so this is the exact new committor. This proves lower saturation in a connected smooth continuum domain, for example a radial annulus with Q = F(q₀). The uniform-pushforward identity also makes the baseline dissipation law easy to construct explicitly.

These equality constructions are mathematical consequences, not independently searched novelty claims.

## Interpretation and limitations

- For the given generator, normalized stationary density is w/Z, so normalized reactive flux is C/Z. Dividing by equilibrium probability Z_A/Z produces C/Z_A. No missing factor of two appears when the diffusion generator and Dirichlet form use the stated convention.
- C/Z_A is not generically an inverse MFPT from the equilibrium distribution conditioned on A. The note correctly avoids that claim. Extending q as zero on A and one on B is understood when integrating w(1−q) over the full state space.
- Adding a constant to Q changes the unnormalized capacity and unnormalized basin partition integral by the same factor; both physical ratios are invariant. Equations (2) and the curvature bounds respect this check.
- Finite exponential moments alone should not be read as establishing well-posedness of the perturbed diffusion or existence of its minimizing current. The opening regularity and variational assumptions must continue to apply at every parameter value used. For bounded Q with an initially well-posed uniformly elliptic bounded-domain problem this issue is straightforward; unbounded state spaces require explicit hypotheses.
- The claimed O(λ⁴) symmetric cumulant remainder requires corresponding regularity around zero. Finite exponential moments on an open interval containing zero are a simple sufficient condition.
- Conductance scores in jump models encode kinetics as well as equilibrium changes. The note correctly refuses to identify an arbitrary Q_e with a thermodynamic particle number.
- The interval certifies exact reference potentials and currents. A fitted dissipation distribution does not by itself certify either endpoint, and finite-sample moment estimates require a separate uncertainty analysis.

No substantive mathematical error was found in the audited results.

## Follow-up audit: equations (5)–(6)

The subsequent committor-coordinate upper bound (5) and harmonic-flow path lower bound (6) are also correct. These are specializations of established variational arguments, not independently established novelty claims.

For (5), the uniform pushforward proved above gives the new energy of g(q₀) as C₀∫₀¹mλ(u)g′(u)²du. Weighted Cauchy–Schwarz, with ∫₀¹g′(u)du = 1, minimizes this energy at g′ proportional to 1/mλ. The comparison with Eν₀[e^{λQ}] is the harmonic–arithmetic mean inequality. The proposed exact transformed committor for Q = F(q₀) agrees with the independent construction in this review.

For (6), a small specification is useful when A contains several vertices: choose the initial vertex in A with probability equal to its total outgoing unit flow. Then choose each outgoing edge in proportion to its flow, omitting zero-flow edges. Strict increase of q₀ on all sampled edges makes the finite flow graph acyclic. Conservation gives edge visitation probability φ_e and ensures arrival in B.

There is also a short direct proof of the stated Berman–Konsowa specialization. For every boundary-admissible potential f, telescoping along any sampled path gives ΣγΔf_e = 1. Hence Cauchy–Schwarz yields

\[
\frac{C_0}{S_\gamma(\lambda)}
=\frac{1}{\sum_{e\in\gamma}\phi_e/c_{\lambda,e}}
\leq\sum_{e\in\gamma}
\frac{c_{\lambda,e}(\Delta f_e)^2}{\phi_e}.
\]

Averaging over paths turns the right side into the perturbed energy summed over positive-reference-flow edges. That sum is at most the full perturbed energy, since omitted edges have nonnegative energy. Minimizing over f proves the first inequality in (6). Furthermore EγSγ = Σeφ_eΔq₀,e e^{−λQ_e} = Eν₀[e^{−λQ}], so Jensen proves the second inequality. Edges with zero reference flow cause no division problem because they are never sampled; their possible activation under perturbation does not invalidate the bound.

For a chain, there is one path and (6) is the exact harmonic formula. For parallel edges, each path has one edge, φ_e = ν_e, and Δq₀,e = 1; (6) becomes the exact arithmetic formula.

Two further second-order consequences follow algebraically if derivatives exist. They are recorded as deductions, without a novelty claim:

- In the diffusion setting, let a(u) = Eν₀[Q | q₀ = u]. Expanding the logarithm of the optimized upper bound gives (log C)″ at zero ≤ Varν₀(Q) − 2 Var_{u∼Uniform[0,1]} a(u). This strengthens the original upper curvature bound whenever the conditional mean varies along the committor.
- In the finite-network setting, let Aγ = ΣγΔq₀,e Q_e. Expanding the logarithm of the path lower bound gives (log C)″ at zero ≥ 2 Varγ(Aγ) − Varν₀(Q). This strengthens the original lower curvature bound whenever path-averaged scores differ. It recovers the exact positive curvature for parallel edges and the exact negative curvature for a chain.

These two refinements refer to their respective diffusion and finite-network settings; combining them into a single theorem would require establishing both constructions in the same setting.
