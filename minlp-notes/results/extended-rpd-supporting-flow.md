# Supporting flows for polynomial extended RPD relaxations

**Status: mathematical statements independently reviewed; closest-source comparison and practical advantage remain unresolved.** See [the independent review](../notes/research-20260912-ode-theory-independent-review.md) for its scope and the prototype defects found and corrected.

Drafted 12 September 2026 by `algorithm_opportunities`, with the arbitrary-reference supporting-flow construction proposed independently by root. This is a precise result draft, not a verified novelty claim. Source audit and experiment plans are in [the accompanying research note](../notes/research-20260912-second-opportunities.md).

The proposed contribution is to verify a useful globally defined subclass of the extended-McCormick RPD construction in Ye–Scott (2023, 2024, 2025), including empty intermediate endpoint objects, and make rigorous supporting cuts available for it. Convex monotone composition, Metzler comparison, LP partial minimization, and exact penalties are established tools. In particular, the sensitivity result must be compared with Song–Khan (2024), and affine state propagation with Singer–Barton (2006) and Harwood–Barton (2018).

## Assumptions and notation

Let \(P\subset\mathbb R^m\) and \(X=[l,u]\subset\mathbb R^n\) be compact nonempty boxes, and let \(T>0\). Consider

\[
\dot x(t,p)=f(p,x(t,p)),\qquad x(0,p)=x_0(p),\quad t\in[0,T],\ p\in P.
\]

Assume the physical solution exists on this horizon and lies in \(X\). Assume \(f\) is represented by a finite expression graph using constants, addition, and binary multiplication. Thus polynomial mass-action systems with polynomial parameter dependence are included. Compute interval parts of every graph node once from the fixed \(P\times X\); these are finite and do not depend on trial endpoint data. All statements concern exact arithmetic.

Given relaxation endpoints \((c,C)\), define signed endpoints \(v=(c,-C)\in\mathbb R^{2n}\). Empty endpoint objects are allowed: no relation between \(c,C,l,u\) is imposed on the domain of the relaxation vector field. Apply the extended multiplication rule of Ye–Scott (2023), Definitions 13–14, rather than the inequivalent endpoint-minimum version in Definition 15. Treat a square as a binary multiplication; stronger univariate rules require a separate regularity check.

Write \(G^-(p,v)\) for the lower output of this extended arithmetic applied to \(f\), and \(G^+(p,v)\) for the negative of its upper output. The superscript \(+\) here denotes the signed upper channel, not a numerical positive part.

For every physical coordinate \(i\), define two affine maps:

\[
(E_i^-v)_{n+i}=-v_i,\qquad (E_i^+v)_i=-v_{n+i},
\]

and leave all other coordinates unchanged. The first substitutes \(C_i=c_i\), and the second substitutes \(c_i=C_i\).

A refinement \(H_i(p,w)\in\mathbb R^{2n}\), which can differ with \(i\), must have these properties:

1. Every component is convex jointly in \((p,w)\), globally Lipschitz, and nondecreasing in every component of \(w\).
2. If \(z\in X\) satisfies the additional physical constraints used by the refinement and \(w=(a,-b)\le(z,-z)\), then \(H_i(p,w)\le(z,-z)\).

The signed RPD vector field is

\[
F_i(p,v)=G^-_i\bigl(p,H_i(p,E_i^-v)\bigr),\quad
F_{n+i}(p,v)=G^+_i\bigl(p,H_i(p,E_i^+v)\bigr).
\tag{1}
\]

The operations in (1) have the same order as the source construction: substitute, refine, evaluate the RHS. Let \(v_0(p)\) be a finite componentwise convex initial signed relaxation, globally locally Lipschitz, with \(v_0(p)\le(x_0(p),-x_0(p))\) for \(p\in P\). For the finite piecewise-affine conclusion, take \(v_0\) piecewise affine as well. Local Lipschitz continuity of the initial map is sufficient because the parameter is fixed during integration.

## Theorem 1: global structure and validity

The field \(F\) in (1) is globally Lipschitz, jointly componentwise convex in \((p,v)\), and cooperative: \(F_j\) is nondecreasing in \(v_k\) for every \(k\ne j\). If every \(H_i\) is finite piecewise affine, then \(F\) is finite piecewise affine. Its ODE has a unique solution \(v(t,p)\) on every finite horizon. For \(p\in P\),

\[
v(t,p)\le (x(t,p),-x(t,p)),
\]

and every component of \(v(t,\cdot)\) is convex. Thus \((v_{1:n},-v_{n+1:2n})\) gives convex lower and concave upper physical state bounds.

**Proof.** For fixed interval data, the signed cut operation is \((a,b)\mapsto(\max(l,a),\max(-u,b))\). Extended addition is a nonnegative linear combination of signed inputs after these cuts. In multiplication, the sign-dependent selector in equation (29) of Ye–Scott (2023) selects the appropriate signed input using the sign of a fixed interval coefficient. After negating the upper channel, equations (34)–(35) are maxima of affine functions having nonnegative signed-input coefficients. Consequently the signed arithmetic is convex, isotone, finite piecewise affine, and globally Lipschitz in its signed endpoint arguments. Substituting exact parameter channels \((p,-p)\) is affine, so joint convexity in \(p\) remains; monotonicity is required only in the state endpoint channels.

The convex monotone composition rule gives the same convexity and isotonicity before the \(E_i^\pm\) substitution. That substitution is affine. Its only negative coefficient is in the state coordinate whose differential equation is being formed; it introduces no negative dependence on any other state coordinate. Thus \(F\) is convex and cooperative. Finite compositions of globally Lipschitz maps are globally Lipschitz. Finite compositions of piecewise-affine maps have finitely many affine pieces. Existence and uniqueness on every finite horizon follow from global Lipschitz continuity and the resulting linear-growth bound.

Let \(z(t,p)=(x(t,p),-x(t,p))\). Each equality substitution leaves \(z\) unchanged. Refinement bound preservation and validity of extended arithmetic at inputs enclosing the physical state imply \(F(p,z(t,p))\le\dot z(t,p)\). Since \(v_0(p)\le z(0,p)\) and \(F\) is cooperative, ordinary cooperative comparison gives \(v(t,p)\le z(t,p)\).

For convexity fix \(p_1,p_2\) and \(\lambda\in[0,1]\), put \(p_\lambda=\lambda p_1+(1-\lambda)p_2\), and set \(y(t)=\lambda v(t,p_1)+(1-\lambda)v(t,p_2)\). Joint convexity gives \(\dot y\ge F(p_\lambda,y)\), and convexity of \(v_0\) gives \(y(0)\ge v_0(p_\lambda)\). Comparison proves \(y(t)\ge v(t,p_\lambda)\). ∎

The same proof works with deterministic time dependence if all Lipschitz/growth bounds are uniform and coefficients meet the usual measurable-in-time assumptions. That extension is not needed for the autonomous fixed-box prototype.

## Theorem 2: sensitivity equations produce genuine supports

Fix \(p_0\), and at almost every \(t\) choose bounded measurable joint subgradients

\[
(a_j(t),b_j(t))\in\partial F_j(p_0,v(t,p_0)),\qquad j=1,\dots,2n.
\]

Stack these as rows of \(A(t)\in\mathbb R^{2n\times m}\) and \(B(t)\in\mathbb R^{2n\times2n}\). Let \(S_0\) contain global supporting rows of the initial signed state at \(p_0\). Then the unique absolutely continuous solution of

\[
\dot S=A+BS,\qquad S(0)=S_0
\tag{2}
\]

satisfies

\[
v(t,p)\ge v(t,p_0)+S(t)(p-p_0),\qquad p\in P.
\tag{3}
\]

Thus each row is an actual convex subgradient, even if (2) does not compute a classical or directional derivative of the state solution.

**Proof.** If \(k\ne j\), monotonicity of \(F_j\) in \(v_k\) and its subgradient inequality evaluated at \(v-te_k\), \(t>0\), imply \((b_j)_k\ge0\). Thus \(B(t)\) is Metzler. For fixed \(p\), define \(w=v(t,p)-v(t,p_0)-S(t)(p-p_0)\). Joint convexity gives \(\dot w\ge Bw\) almost everywhere; the initial support gives \(w(0)\ge0\). Nonnegativity of the transition matrix of the bounded measurable Metzler linear system yields \(w(t)\ge0\), proving (3). ∎

Bounded measurable selections exist in the finite piecewise-affine case: choose, for example, the first active affine piece in a fixed finite enumeration. A large implicit representation need not be enumerated to implement a valid selection. Convex monotone composition permits valid subgradient propagation through its elemental operations. Generic AD through a nonconvex rearrangement is not covered. The theorem needs no strict interval-interiority, transversal switching, or differentiability hypothesis.

## Theorem 3: arbitrary-reference supporting flows

Let bounded measurable affine supports satisfy, for all \((p,v)\),

\[
F(p,v)\ge d(t)+A(t)p+B(t)v,
\tag{4}
\]

where \(B(t)\) is Metzler. Let \(\ell_0(p)\le v_0(p)\) be affine in \(p\), and solve

\[
\dot\ell(t,p)=d(t)+A(t)p+B(t)\ell(t,p),\qquad\ell(0,p)=\ell_0(p).
\tag{5}
\]

Then \(\ell(t,\cdot)\) is affine and \(\ell(t,p)\le v(t,p)\) for all \(t,p\).

**Proof.** With \(w=v-\ell\), equations (4)–(5) give \(\dot w\ge Bw\) and \(w(0)\ge0\). Apply Metzler comparison. ∎

A joint affine support of \(F_j\) chosen at any \((\hat p,\hat v)\) has the required nonnegative off-diagonal coefficients. Different rows may use different reference points. The reference states need not solve the relaxation ODE or describe consistent enclosures. A numerical reference path therefore affects strength, not mathematical validity of the supports. For autonomous \(F\), any chosen support remains valid over an entire time slab. Holding coefficients constant on each slab reduces (5) to propagation by matrix exponentials.

Numerical certification still matters. If an affine coefficient row \((q,r)\) of the exact final solution is replaced by \((\hat q,\hat r)\), and certified error bounds give \(|\hat q-q|\le\epsilon_q\), \(|\hat r-r|\le\epsilon_r\), then

\[
\hat q^Tp+\hat r-\epsilon_r-\epsilon_q^T\max(|p^L|,|p^U|)
\]

is a valid final lower affine bound on \(P\). This corrects coefficient errors after they have been certified; ordinary floating-point matrix exponentials alone do not provide those error bounds. Changing support slopes before integration must likewise retain (4), not just apply an unrelated final rounding shift.

### Nominal-point recovery estimate

Suppose one selects at \((p_0,\hat v(t))\) a true supporting affine row of \(F\). In a common compact neighborhood, let \(L\) bound both the Lipschitz constant of \(F(p_0,\cdot)\) and the selected state-gradient matrix norm. Then the support deficit evaluated at \(v(t,p_0)\) has norm at most \(2L\|v(t,p_0)-\hat v(t)\|\). If \(\|B(t)\|\le K\), variation of constants bounds the final gap by the propagated initial gap plus

\[
2L\int_0^t e^{K(t-s)}\|v(s,p_0)-\hat v(s)\|\,ds.
\tag{6}
\]

This estimate needs an actual reference-error bound to become numerical. It does not require one for validity in Theorem 3.

For supports sampled at \((p_0,\ell(t_j,p_0))\) and held on slabs, the following complete bound was independently supplied by `ode_theory_review`. Let \(L\) bound the Lipschitz constant of \(F(p_0,\cdot)\), \(K\) bound \(\|B_j\|\), \(M\) bound \(\|\dot v(t,p_0)\|\), and let \(C=L+K\). Use a compatible induced matrix/vector norm. If every slab length \(h_j\le h\) and \(E_0=\|v_0(p_0)-\ell_0(p_0)\|\), then

\[
\|v(t,p_0)-\ell(t,p_0)\|
\le e^{(K+C)t}\left(E_0+\frac{CM}{2}t h\right),\qquad 0\le t\le T.
\tag{9}
\]

Indeed, write \(E_j=\|v(t_j,p_0)-\ell(t_j,p_0)\|\). Equality of the selected support with \(F\) at \(\ell(t_j,p_0)\), the Lipschitz bound, and \(\|v(t_j+\tau,p_0)-v(t_j,p_0)\|\le M\tau\) bound the support deficit by \(C(E_j+M\tau)\). Variation of constants gives

\[
E_{j+1}\le e^{Kh_j}\left((1+Ch_j)E_j+\frac{CM}{2}h_j^2\right).
\]

Use \(1+Ch_j\le e^{Ch_j}\), iterate, and use \(\sum_j h_j^2\le h\sum_jh_j\); the same argument handles a partial final slab. In the finite piecewise-affine case \(L,K\) are global, and the true trajectory has bounded speed on a finite horizon. Hence no additional compact-region assumption about the generated lower reference trajectory is needed. With zero initial gap, (9) gives first-order recovery at the nominal parameter, uniformly in time. This is an elementary consistency bound, not a novelty claim, and Theorem 3 does not depend on it.

## Proposition 4: a finite coupled-invariant refinement

Let physical states satisfy \(Az+Bp=b\), and let \(\rho\ge0\) be fixed. For \(s\in\{-1,1\}\), set

\[
h_{k,s}(p,c,C)=\min_{z\in X}\{s z_k+\rho R(z;p,c,C)\},
\]

\[
R=\sum_j(c_j-z_j)_++\sum_j(z_j-C_j)_++\|Az+Bp-b\|_1.
\tag{7}
\]

Set lower and signed upper outputs respectively to \(\max(c_k,l_k,h_{k,1})\) and \(\max(-C_k,-u_k,h_{k,-1})\). This map satisfies the refinement assumptions of Theorem 1, remains finite at every inconsistent input, and is finite piecewise affine.

**Proof.** Compactness of \(X\) gives finiteness. Joint convexity of the objective and partial minimization give convexity in \((p,c,-C)\). Its objective is nondecreasing in each signed endpoint for every fixed \(z\), proving isotonicity. Comparing objectives at an optimum yields

\[
|\Delta h_{k,s}|\le\rho(\|\Delta c\|_1+\|\Delta C\|_1+\|B\Delta p\|_1).
\]

The epigraph is a projection of a polyhedron, so a finite piecewise-affine representation exists. Any physical \(z\) enclosed by the input endpoints has zero penalty; hence \(h_{k,1}\le z_k\) and \(h_{k,-1}\le-z_k\). The remaining maxima are existing valid signed bounds. ∎

For implementation define \(\alpha,\beta\in[0,\rho]^n\), \(q\in[-\rho,\rho]^r\), and \(a=s e_k-\alpha+\beta+A^Tq\). The dual is

\[
h_{k,s}=\max_{\alpha,\beta,q}\left[\alpha^Tc-\beta^TC+q^T(Bp-b)+\sum_j\min(l_ja_j,u_ja_j)\right].
\tag{8}
\]

Equation (8) follows by writing each positive part and absolute value as a bounded support function and applying minimax to the two compact convex variable domains. Fixed feasible multipliers give affine global supports with signed-endpoint slopes \((\alpha,\beta)\ge0\). Optimal multipliers give a joint subgradient. A fixed finite bundle of feasible tuples gives a weaker refinement retaining all assumptions.

Combining the signed map in (7) componentwise by maximum with the source row-refinement map preserves the assumptions and pointwise dominates the source map, including on empty inputs. Since the base arithmetic is isotone, its field dominates the source field. Cooperative comparison then proves no weaker integrated signed relaxations with a common initial condition and common base interval data. The same argument proves monotone improvement with increasing fixed \(\rho\).

Do not replace (7) by a hard feasible-set LP on arbitrary RPD inputs. Infeasibility of that LP can occur after the required equality substitution even for a physical feasible parameter. The finite extension is essential. Do not select \(\rho\) as an arbitrary function of the trial parameter; joint convexity would no longer follow.

### Self-exclusion convention

To leave the own-coordinate pair unchanged, replace both of its output components by the corresponding inputs and skip their initial clipping too. Identity components satisfy all assumptions. This is stronger than merely skipping the invariant-row update, as initial clipping can otherwise change an empty own-coordinate pair. Self-exclusion is optional for the theorems above and is not asserted to guarantee numerical stability.

## Scope of the proposed advance

Theorem 1 verifies the global structure of a useful concrete class. Its **local** Lipschitz implication is modest: as the independent reviewer observed, Ye–Scott (2023) Definitions 5–9 already imply that the signed extended maps are finite convex functions on the whole fixed-interval coherence fiber, so local Lipschitz continuity follows from elementary convex analysis. The polynomial restriction adds global Lipschitz continuity, linear growth, and finite affine support structure. Do not present the local regularity corollary as a major independent advance.

Theorem 2 provides a route to justify the state-relaxation subgradients whose validity is left open in Ye–Scott (2025) Remark 7. Proposition 4 adds coupled row information while retaining a finite globally regular RHS, and offers bounded dual multipliers for support computation. Theorem 3 is potentially a reliable implementation route because approximate nonlinear trajectories only select exact global supports; certification reduces to affine linear propagation.

Harwood–Barton (2018), Theorem 1, already gives general time-varying polyhedral enclosures under facet differential inequalities; our affine-flow comparison is a specialization applied to the signed relaxation field. Their Proposition 7 propagates physical reference trajectories, pseudo-sensitivity matrices, interval bounds, and affine offsets. Their numerical comparison also includes affine cuts obtained by linearizing McCormick state relaxations. Thus neither affine state bounds nor supporting linear propagation should be claimed as newly invented here. The remaining candidate is the concrete global empty-input compilation and certification of refined RPD, possibly strengthened by the coupled finite dual refinement.

None of these statements establishes priority over unread source theorems. The completed independent proof review supports the scoped mathematical claims; the exact Song–Khan (2024) theorem comparison and fair reactor benchmarks remain necessary.

## State-box convergence safeguard

The fixed-interval theory above does not imply convergence to the physical trajectory when only the parameter box shrinks. A singleton-parameter example, \(\dot x=-x^2\), \(x(0)=1\), with binary multiplication on the fixed state interval \([0,1]\), retains the exact lower/upper relaxation trajectories \(e^{-t}\) and \((1+e^{-2t})/2\), while the physical trajectory is \(1/(1+t)\).

[The validated polynomial tube note](../notes/research-20260912-validated-polynomial-tubes.md) supplies the needed separate construction. A strict interval Picard inclusion validates each physical slab; sound invariant contraction and an integrated interval slope enclose its endpoint. On compact mass-action domains, widths vanish with parameter width and time step if accumulated rounding vanishes. Its proof also permits globally valid affine supports to use different validated interval data on successive slabs, comparing each affine system directly with the physical signed state. Keeping the convergent interval objective bound alongside affine cuts avoids making branch-and-bound value consistency depend on an arbitrary support-selection policy. This tube construction is established interval ODE methodology, not an additional novelty claim.
