# Finite invariant refinement and supporting cuts for dynamic MINLP

Research note, 12 September 2026. Author: research subagent `algorithm_opportunities`.

This note develops one opportunity after the initial scout. The strongest current direction is a rigorous cut construction for the recently proposed extended-McCormick RPD state relaxations, followed by coupled invariant refinement. The generic convex-analysis and comparison arguments below are established tools, not novelty claims. A contribution would need to establish their applicability to the particular extended RPD construction, close a documented source gap, and provide useful software and comparative results. Independent review and the closest full-text source comparisons remain necessary.

## 1. The source gap and its limits

Ye and Scott, *Tightening state relaxations for global dynamic optimization using dynamic cuts*, J. Global Optim. 92:21–54 (2025), DOI [10.1007/s10898-025-01466-9](https://doi.org/10.1007/s10898-025-01466-9), provides the relevant framework. The full paper is available locally at `literature/papers/ye2025-tightening-state-relaxations-for-global/original.pdf`.

- Theorem 4 gives valid convex and concave state bounds from an RPD system if the composed vector field meets the stated local Lipschitz condition.
- Remark 3, printed pp. 32–33, states that regularity of the extended McCormick rules has not been analyzed in detail; local Lipschitz continuity is assumed reasonable. This is distinct from the older generalized McCormick rules, for which a Lipschitz result is cited.
- Algorithm 1, printed p. 34, refines bounds by sequential rearrangements of affine invariant rows. For fixed matrices and interval bounds, this refinement is already a finite composition of affine maps and max/min operations. Giving it a finite extension alone would not be new.
- Remark 7, printed pp. 43–44, explains that its preliminary global dynamic optimization implementation uses custom sensitivity equations and new subgradient rules that have not been rigorously justified. The proposed rigorous development would follow Song and Khan's 2024 work.

The closest sensitivity source is Song and Khan, *Computing subgradients of convex relaxations for solutions of parametric ordinary differential equations*, Optim. Methods Softw. 39(6):1309–1351 (2024), DOI [10.1080/10556788.2024.2346641](https://doi.org/10.1080/10556788.2024.2346641). Its [institutional abstract](https://experts.mcmaster.ca/scholarly-works/3434889) explicitly assumes state relaxations remain strictly within interval bounds. Its [MIT-licensed implementation](https://github.com/kamilkhanlab/convex-ode-subgradients) implements generalized-McCormick and optimization-based state relaxations. The exact theorem hypotheses still need full-text inspection; do not claim that the comparison argument below is a new general sensitivity theorem.

Ye and Scott's extended rules are in J. Global Optim. 87:57–95 (2023), DOI [10.1007/s10898-023-01315-7](https://doi.org/10.1007/s10898-023-01315-7), available locally. Definitions 13–14, equations (29)–(35), give the sign-selected multiplication rule needed on empty inputs. The alternative rule using `min(alpha*cv, alpha*cc)` is not equivalent on empty inputs and can destroy convexity. This distinction must survive implementation.

## 2. Concrete model class

Consider a parametric ODE

\[
\dot x=f(p,x),\qquad x(0,p)=x_0(p),\qquad p\in P,
\]

with a valid compact state box \(X=[l,u]\) throughout a finite horizon. Initially restrict \(f\) to polynomial expression trees implemented using constants, addition, and binary multiplication. In particular, implement a square as multiplication, not a separate univariate square envelope. Parameters may include rate coefficients, feeds, and fixed-schedule operating decisions. Discrete choices can select a kinetic model or catalyst, with this construction used inside each applicable disjunct or branch.

All interval parts of the expression tree are computed from fixed \(P\) and \(X\); these interval parts do not depend on the trial convex/concave endpoint values. They may be conservative. This restriction is important: arbitrary adaptive interval updates are not covered by the proof.

Let

\[
v=(c,-C)\in\mathbb R^{2n}
\]

be the signed state relaxation vector. This sign change turns both improved lower bounds and improved upper bounds into componentwise increases. A signed endpoint input need not describe a nonempty enclosure.

### Lemma 1: structure of the polynomial extended arithmetic

For fixed valid interval parts, the signed output of an extended-McCormick polynomial expression is a finite convex piecewise-affine function of the signed input endpoints. Each output is nondecreasing in every signed input endpoint. It is therefore globally Lipschitz and has bounded subgradients.

**Proof.** The cut operation sends \((a,b)=(c,-C)\) to \((\max(l,a),\max(-u,b))\), which has these properties. Addition and multiplication by a constant use nonnegative linear combinations of the appropriate signed components. For multiplication, equation (29) selects a component according to the sign of a fixed interval coefficient. After applying the sign change to the upper output, equations (34)–(35) are maxima of affine functions whose coefficients on signed inputs are nonnegative. Composition preserves convexity when the outer map is nondecreasing, preserves monotonicity, and remains piecewise affine with finitely many pieces. A finite convex piecewise-affine function on the whole finite-dimensional space is globally Lipschitz. ∎

This proves a useful restricted form of the regularity requested in Ye–Scott Remark 3. It does not establish regularity of every univariate extended rule, and it does not establish global existence if a different primitive introduces superlinear growth outside its physical interval.

## 3. Refinement operators and the RPD substitution

In signed coordinates write a refinement as

\[
H(p,v)=(c',-C').
\]

Require each component of \(H\) to be convex jointly in \((p,v)\), nondecreasing in every component of \(v\), globally Lipschitz, and bound preserving for the physical states. Fixed finite sweeps of the affine row refinement in Ye–Scott satisfy the first three properties. Bound preservation is their existing theorem.

For the lower-state equation for coordinate \(i\), define the affine substitution \(E_i^-\) on signed endpoints by replacing \(v_{n+i}\) with \(-v_i\); leave every other component unchanged. For the upper-state equation, whose signed output coordinate is \(n+i\), define \(E_i^+\) by replacing \(v_i\) with \(-v_{n+i}\). These are precisely the two own-coordinate equality substitutions in the RPD construction.

The base signed arithmetic is convex and isotone in endpoint inputs. Compose it with \(H\) and then with the appropriate \(E_i^\pm\), keeping the order of the source construction: first substitute, then refine, then evaluate the RHS. The resulting signed vector field is denoted \(F(p,v)\).

### Lemma 2: convex and cooperative signed RPD field

Under these assumptions, each \(F_i\) is jointly convex in \((p,v)\), globally Lipschitz, and nondecreasing in \(v_j\) whenever \(j\ne i\). For the polynomial and finite piecewise-affine refinement class, \(F\) is finite piecewise affine. Consequently the signed RPD ODE has a unique solution on every finite horizon for every finite initial state.

**Proof.** Before the equality substitution, all component functions are convex and isotone in signed endpoint arguments, by the monotone convex composition rule. The substitution is affine, so it preserves joint convexity. It can introduce a negative dependence only on the coordinate whose differential equation is being computed. Every other surviving endpoint dependence remains nonnegative; the overwritten opposing coordinate disappears. Lipschitz continuity follows by finite composition. A globally Lipschitz vector field has at most linear growth, so its unique local solution extends to every finite horizon. ∎

Every joint subgradient \((a_i,b_i)\in\partial F_i(p,v)\) satisfies \((b_i)_j\ge0\) for \(j\ne i\). To see this, compare the global subgradient inequality at \(v-te_j\), \(t>0\), with monotonicity in coordinate \(j\). Thus a matrix formed from these rows is Metzler (all off-diagonal entries are nonnegative).

**Self-coordinate implementation caveat.** Ye–Scott Remark 6 recommends leaving the own-coordinate pair unchanged to suppress an observed unstable numerical mode. Skipping only Algorithm 1 lines 9–10 when \(k=i\) is not enough to enforce that identity globally: initial clipping in lines 2–3 still changes the own pair. For example, with \(X_i=[0,1]\), an RPD lower substitution supplying \((c_i,C_i)=(-1,-1)\) is changed by clipping to \((0,-1)\). A literal self-excluding implementation must skip own-coordinate initial clipping as well, or state an interiority assumption. Leaving a coordinate unchanged preserves bound preservation and the convex/isotone properties. This observation does not show the source's numerical implementation is wrong on its tested trajectories. Also, self-exclusion alone is not a general stability theorem.

## 4. A supporting sensitivity theorem

The following elementary comparison result is the central proof route. It is an application of established convex and cooperative ODE theory. Its proposed contribution is a verified application to the globally defined extended RPD field above.

### Proposition 3: global supporting rows

Let \(F\) be jointly componentwise convex and cooperative as in Lemma 2. Suppose \(v_0(p)\) is componentwise convex, and let \(v(t,p)\) solve \(\dot v=F(p,v)\), \(v(0,p)=v_0(p)\). Fix \(p_0\). At almost every time choose measurable joint subgradients

\[
(a_i(t),b_i(t))\in\partial F_i(p_0,v(t,p_0)),
\]

and stack them into \(A(t),B(t)\). Assume these selected coefficients are bounded on the horizon. This is automatic for finite piecewise-affine \(F\), provided a measurable selection is used. Let \(S_0\) contain a valid subgradient row of each \(v_{0,i}\) at \(p_0\), and solve

\[
\dot S=A+BS,\qquad S(0)=S_0.
\]

Then, for every \(p\in P\),

\[
v(t,p)\ge v(t,p_0)+S(t)(p-p_0).
\]

In particular, every row of \(S(t)\) is a valid global convex subgradient of the corresponding signed state relaxation at \(p_0\).

**Proof.** Set \(w(t)=v(t,p)-v(t,p_0)-S(t)(p-p_0)\). Convexity gives \(\dot w\ge B(t)w\) almost everywhere, and the initial support gives \(w(0)\ge0\). The transition matrix of the bounded measurable Metzler system \(\dot z=B(t)z\) is nonnegative. Variation of constants yields \(w(t)\ge0\). ∎

This proof uses no differentiability of the state solution, no transversal switching condition, and no strict inclusion between interval and relaxation endpoints. It does require true joint subgradients of \(F_i\). Arbitrary automatic differentiation through a representation with nonconvex intermediate functions is not justified. For the convex/isotone composition above, valid elementary subgradients can instead be propagated using the convex monotone chain rule; the affine own-coordinate substitution is applied explicitly. Finite max-affine tie choices are admissible.

The convexity of \(v(t,\cdot)\), if desired independently of the source RPD theorem, follows by applying cooperative comparison to the convex combination of the trajectories at two parameter points. The combination is a supersolution at the convexly combined parameter.

## 5. Coupled affine-invariant refinement with finite empty-input values

Suppose physical states obey \(Az+Bp=b\) in addition to \(z\in X\). For \(s\in\{-1,1\}\) and coordinate \(k\), define

\[
h_{k,s}(p,c,C)=\min_{z\in X}\left\{s z_k+\rho\left[\sum_j(c_j-z_j)_++\sum_j(z_j-C_j)_++\|Az+Bp-b\|_1\right]\right\},\quad\rho\ge0.
\]

This is an LP after introducing slacks. It is finite on **all** endpoint and parameter inputs, including inconsistent endpoint pairs and inconsistent invariant rows. Hard bound closure would be infeasible on some RPD inputs and cannot be substituted directly.

Set a lower endpoint to \(\max(c_k,l_k,h_{k,+})\), and a signed upper endpoint to \(\max(-C_k,-u_k,h_{k,-})\). Leave the own-coordinate pair unchanged if using the source's self-excluding variant.

### Proposition 4: properties of the penalized refinement

For fixed \(A,B,b,X,\rho\), both signed outputs are finite convex piecewise-affine functions of \((p,c,-C)\), nondecreasing in signed endpoints, and globally Lipschitz. They preserve bounds for every physical state satisfying the supplied endpoints and affine invariants.

**Proof.** The objective is jointly convex in the minimization variable and the supplied data, and the fixed box \(X\) is convex and compact. Partial minimization proves convexity and finiteness. Increasing a signed endpoint cannot decrease the objective at any \(z\), proving monotonicity after minimization. Comparing objectives at a common minimizer gives

\[
|\Delta h|\le \rho\big(\|\Delta c\|_1+\|\Delta C\|_1+\|B\Delta p\|_1\big).
\]

The polyhedral epigraph gives piecewise affinity. A physical feasible \(z\) has zero penalty, so \(h_{k,+}\le z_k\) and \(h_{k,-}\le-z_k\). Taking maxima with existing valid signed bounds preserves validity. ∎

The pointwise Jensen-consistency condition in Ye–Scott Definition 9 follows from the same joint convexity and endpoint monotonicity: first use the supplied Jensen inequality on endpoint values, then joint convexity. This matters because their condition is stated at arbitrary individual Jensen triples, not only for globally convex endpoint functions.

### Dual supports and cheap fixed bundles

Introduce \(\alpha,\beta\in[0,\rho]^n\), \(q\in[-\rho,\rho]^m\), and \(d=s e_k-\alpha+\beta+A^Tq\). Strong minimax duality gives

\[
h_{k,s}=\max_{\alpha,\beta,q}\left\{\alpha^Tc-\beta^TC+q^T(Bp-b)+\sum_j\min(l_jd_j,u_jd_j)\right\}.
\]

For fixed dual multipliers the displayed expression is affine in \((p,c,-C)\), with nonnegative signed endpoint coefficients. Every feasible multiplier tuple therefore supplies a globally valid affine support. An optimal tuple supplies a true joint subgradient: parameter gradient \(B^Tq\), endpoint gradients \(\alpha,\beta\). A finite fixed bundle of such supports produces a cheaper, weaker refinement with the same structural guarantees. Freeze the bundle during an integration; choosing or dropping pieces adaptively based on the current parameter without accounting for that selection need not preserve convexity.

On feasible input enclosures, a sufficiently large fixed \(\rho\) gives exact coordinate bounds of the coupled hard LP. One proof uses a uniform Hoffman error-bound constant for the fixed constraint matrix: distance to the hard feasible polyhedron is at most a constant times the summed residual. Since \(z_k\) is 1-Lipschitz in the 1-norm, any larger penalty coefficient gives equality of the penalized and hard optimum. This is ordinary LP exact-penalty theory; it is not a proposed new theorem. A large coefficient may worsen stiffness, and practical penalty choice must be measured.

Increasing \(\rho\) strengthens every signed refinement component. Cooperative comparison consequently strengthens the integrated signed RPD solution. For a fair no-loss extension of the source implementation, take the componentwise maximum of the signed source row-refinement map and the signed penalized map. This remains convex/isotone and pointwise dominates the source map even on empty inputs. Lemma 2 and cooperative comparison then guarantee integrated dominance over the same source RPD implementation. Without this maximum, exactness only on feasible inputs does not establish dominance during empty RPD calls.

### A bounded example where coupled closure helps

Take \(z\in[0,1]^4\) with

\[
z_1+z_2+z_3+z_4=1,\qquad z_1+2z_2+3z_3+4z_4=5/2.
\]

Row propagation of these original rows reaches the bounds \(z\le(1,1,5/6,5/8)\), with zero lower bounds. Coupled LP closure instead gives \(z\le(1/2,3/4,3/4,1/2)\), each attained by a feasible two-variable support. Even replacing the rows by reduced row echelon form gives only \(z\le(1,1,3/4,1/2)\) under repeated individual-row bound propagation. Thus the improvement is not limited to an unfortunate original row scaling or a single sweep. This example is a mathematical test of coupled propagation, not a substantive chemical case study.

## 6. Affine cuts from an arbitrary reference trajectory

Root proposed the following extension. It avoids using an inaccurate nonlinear reference trajectory as if it were exact.

Suppose global affine supports have been selected so that

\[
F(p,v)\ge d(t)+A(t)p+B(t)v,
\]

with measurable bounded coefficients and Metzler \(B\). Let \(\ell(0,p)\) be an affine global lower support of \(v_0(p)\), and integrate

\[
\dot\ell=d+A p+B\ell.
\]

Then \(v(t,p)\ge\ell(t,p)\) for every parameter, by exactly the comparison proof above. Supports may be chosen at any supplied reference states; those reference states need not lie on the true relaxation trajectory or even form a feasible endpoint enclosure. For autonomous finite piecewise-affine \(F\), a selected affine support is valid at all times, so one can freeze supports on time slabs and propagate the linear system by matrix exponentials.

This is a continuous-time validity theorem. Floating-point matrix exponentials are not automatically certified. A useful implementation should enclose their coefficient errors and subtract the resulting worst-case affine evaluation error over \(P\), or use another validated linear integration method. The nonlinear reference integration only selects supports and thus need not itself be validated for cut validity.

An elementary convergence estimate makes the selection error explicit. At a fixed \(p_0\), suppose the support is chosen at \(\hat v(t)\), the field and selected gradients have a common Lipschitz bound \(L\), and \(\|\hat v(t)-v(t,p_0)\|\le\delta(t)\). The support deficit evaluated at the true trajectory is at most \(2L\delta(t)\). Therefore the final support gap is at most the propagated initial gap plus

\[
2L\int_0^t e^{K(t-s)}\delta(s)\,ds,
\]

where \(K\) bounds the matrix norm of \(B\). Freezing a near-trajectory support over slabs of maximum length \(h\) adds an \(O(h)\) reference-state error if the true trajectory has bounded speed. This is a recovery statement at the chosen parameter point, not uniform exactness of one affine cut on the whole parameter box.

**Strong prior-art caution.** Singer and Barton, *Bounding the Solutions of Parameter Dependent Nonlinear Ordinary Differential Equations*, SIAM J. Sci. Comput. 27:2167–2182 (2006), DOI [10.1137/040604388](https://doi.org/10.1137/040604388), already construct affine state relaxations. Harwood and Barton, *Affine relaxations for the solutions of constrained parametric ordinary differential equations*, OCAM 39:427–448 (2018), DOI [10.1002/oca.2323](https://doi.org/10.1002/oca.2323), incorporate interval bounds and state constraints using auxiliary optimization problems. Their full theorems must be compared before calling the arbitrary-reference linear-system construction new. It may chiefly be a useful way to implement and certify the new extended/invariant-refined RPD field.

## 7. Decisive prototype and rejection criteria

First implement only the finite polynomial arithmetic and row refinement, and independently verify support validity on empty endpoint cases, endpoint contact, tied max branches, and the source's simple decay example. Compare true global supports against finite-difference approximations at nonsmooth points; finite differences are diagnostic, not a correctness oracle. Verify the coupled LP example above with exact rational arithmetic or independently solved LPs.

For a useful energy-process prototype, consider an isothermal batch or fixed-schedule reactor with water-gas shift and methanation:

\[
\mathrm{CO+H_2O\rightleftharpoons CO_2+H_2},\qquad
\mathrm{CO+3H_2\rightleftharpoons CH_4+H_2O}.
\]

Polynomial mass-action rates fit the proved class. Carbon, oxygen, and hydrogen inventories give coupled affine invariants. Feed allocation supplies continuous decisions; a small catalyst menu supplies discrete kinetic choices. Initial experiments should use explicitly labeled stylized rate data, then move to a cited process model if the algorithmic advantage survives. Arrhenius temperature dependence is not covered by the binary-polynomial proof unless rate coefficients are lifted as decisions with their nonlinear linking equations handled in the master model, or the corresponding univariate extension is separately proved.

Measure source row refinement, row refinement after row reduction, combined penalty refinement, and a small fixed dual bundle using the **same** valid state tube and base polynomial McCormick expressions. Report state relaxation gap, final objective lower bound, support-generation time, LP calls, and branch-and-bound effort. Include Song–Khan optimization-based relaxation as a strong competitor once its full formulation is read. Check the cost of large penalties and whether coupled refinement remains useful after standard conservation-variable elimination. Compare validated direct affine propagation against ordinary sensitivity propagation with an explicit numerical error allowance.

Reject a major novelty claim if the global convex/cooperative extended-RPD verification is already in Ye–Scott 2024/2025 or Song–Khan 2024, or if the affine cut method is merely the established Singer/Harwood method without a new useful capability. Reject coupled LP as a major practical direction if eliminating dependent states or improving invariant rows removes most gains, or if LP overhead outweighs gap reduction. Preserve the regularity proof and the self-clipping implementation caveat even in that case.

## 8. Source queue and verification status

### Later prior-art findings

The fresh reviewer pointed out that local Lipschitz continuity on a fixed interval fiber already follows from finite convexity in Ye–Scott (2023) Definitions 5–9. The polynomial structure proof contributes the stronger global Lipschitz and finite-affine properties, but its local conclusion should not be advertised as a major result.

Harwood–Barton (2018) was inspected through its [author-upload text](https://www.researchgate.net/publication/318145908_Affine_relaxations_for_the_solutions_of_constrained_parametric_ordinary_differential_equations). Its Theorem 1 already covers time-dependent polyhedral enclosures satisfying facet differential inequalities. Proposition 7 propagates a physical reference trajectory, pseudo-sensitivities, interval bounds, and affine offsets. Table 1 also compares cuts formed by linearizing McCormick state relaxations. Our abstract affine-flow validity result is therefore a specialization of established theory, not a new general enclosure principle.

Zhang and Khan's [FOCAPO-CPC 2023 paper](https://skoge.folk.ntnu.no/prost/proceedings/focapo-cpc-2023/Oral%20Talks/100_Oral.pdf), physical p. 2, says Khan's 2018 subtangent method covers differentiable or convex RHS fields, but did not cover the then-superior Scott–Barton and Song–Khan formulations. Physical p. 3 imposes strict ordering of interval and relaxation bounds, then summarizes the affine forward subgradient system in equation (5); p. 4 gives the adjoint form. Thus globally convex signed extended RPD may make an older sensitivity theorem applicable. The 2024 exact theorem remains unread until a lawful full text is supplied or retrieved.

The most plausible remaining contribution is an auditable implementation that compiles global affine pieces of the empty-input refined RPD field, propagates them with certified linear arithmetic, and optionally strengthens them with coupled invariant certificates. In (8) of the dedicated result draft, approximate LP dual multipliers can be rationally rounded and clamped to their simple boxes, after which an exact recomputation of the dual intercept gives a valid support regardless of LP optimality. The `min` operations in that intercept must be computed exactly or bounded downward.

### Possible direct RHS variant, not yet assessed

Instead of solving separate coordinate-bound LPs before evaluating a RHS, one could minimize a standard joint convex RHS relaxation \(f_i^{cv}(p,z)\) over \(z\in X\), plus

\[
\rho\left[|z_i-c_i|+\sum_{j\ne i}(c_j-z_j)_++(z_j-C_j)_++\|Az+Bp-b\|_1\right].
\]

The negative upper channel uses \(-f_i^{cc}\) and \(|z_i-C_i|\). Partial minimization gives a finite convex field with nonnegative off-diagonal signed-state dependence. At a physical contact point the true state is a zero-penalty candidate, giving the differential bound needed for comparison. For a piecewise-affine RHS relaxation this is one LP per signed differential equation. It retains correlations in the RHS rather than reducing them to independent coordinate bounds. This is very close to Song–Khan's optimization-based relaxation with a finite penalty extension and invariants; it is only an implementation candidate pending source comparison.

All missing sources were sent to the shared `/root/literature` agent. No literature knowledge-base files were modified by this scout. The queue includes Song–Khan 2022 optimization-based ODE relaxations (DOI 10.1007/s10107-021-01654-x), Song–Khan 2024 sensitivities, Ye–Scott 2024 modified RPD (DOI 10.1007/s10898-024-01381-5), Song–Barton 2024 optimal-value derivatives (DOI 10.1007/s10898-023-01359-9), Khan–Barton 2014 nonsmooth ODE derivatives (DOI 10.1007/s10957-014-0539-1), Song–Khan 2025 comparison inequalities, and the Singer/Harwood affine methods. Their reports and unresolved full-text requests belong in the eventual user report.

The proofs in this note have been checked by the author and discussed independently with root, but have not yet received a fresh independent formal review. No publishable novelty or computational performance result is claimed here.
