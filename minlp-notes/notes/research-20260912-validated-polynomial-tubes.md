# Validated polynomial ODE tubes for shrinking MINLP parameter boxes

**Status: established construction, with a proof tailored to the research prototype; [independently reviewed](research-20260912-polynomial-tube-independent-review.md) with no mathematical defect found.** The reviewer also checked the two explicit counterexamples below and supplied the fixed-grid example. This is a correctness and convergence safeguard for [extended RPD supporting flows](../results/extended-rpd-supporting-flow.md), not a proposed new interval ODE method. The implementation is [polynomial_tubes.py](../code/research_20260912/polynomial_tubes.py).

A fixed broad state box can leave a nonzero McCormick state gap even at a singleton parameter box. Reducing only the parameter domain therefore does not establish convergence of that relaxation. The construction below supplies verified state boxes on time slabs. Their widths vanish when both the initial/parameter uncertainty and the time step vanish, provided accumulated arithmetic rounding also vanishes. Retaining the resulting interval objective bound alongside affine cuts gives a simple safeguard that does not depend on the quality of support selection.

An exact example makes this obstruction explicit. Take \(\dot x=-x^2\), \(x(0)=1\), with fixed state interval \([0,1]\) and no uncertain parameter. Evaluate the square as binary multiplication. The lower and upper square relaxations at a scalar input \(a\in[0,1]\) are \(\max(0,2a-1)\) and \(a\). The standard lower/upper differential substitutions therefore give

\[
\dot c=-c,\qquad \dot C=-\max(0,2C-1),\qquad c(0)=C(0)=1.
\]

Thus \(c(t)=e^{-t}\), \(C(t)=(1+e^{-2t})/2\), whereas \(x(t)=1/(1+t)\). At \(t=1\), the relaxation encloses \(1/2\) by approximately \([0.367879,0.567668]\). Even exact integration and infinitely frequent supporting-flow updates only recover this nonzero fixed-box gap. The example concerns the binary-multiplication implementation; a specialized unary-square relaxation changes its equations and is not covered by this calculation.

## 1. Model and interval arithmetic

Consider

\[
\dot x=f(p,x),\qquad x(0)=x_0(p),\qquad p\in P\subseteq\bar P,
\]

where \(f\) is a fixed polynomial expression graph, \(\bar P\) is compact, and the initial state is affine in \(p\) in the prototype. Let \(f^I(P,B)\) be its natural interval evaluation with exact rational arithmetic or outward rounding. The essential enclosure property is

\[
f(p,x)\in f^I(P,B)\quad(p\in P,\ x\in B).
\tag{1}
\]

Only physically admissible parameters need be covered if some points of \(P\) violate separately enforced model constraints. Every physical box or invariant used below must hold for all such admissible trajectories. The interval operations themselves may discard dependence between parameters and states; this weakens bounds but preserves (1).

For a box \(B\), write \(w(B)=\max_i(\overline B_i-\underline B_i)\). All box additions and scalar products below are interval operations. In particular, \([0,h]V\) encloses \(\tau v\) for every \(0\le\tau\le h\) and \(v\in V\).

## 2. A strict inclusion certificate for one slab

**Proposition 1.** Suppose a box \(Y\) contains every admissible state at time \(t_j\). Let \(h>0\), and let a finite box \(B\) satisfy the coordinatewise strict inclusion

\[
Y+[0,h]f^I(P,B)\subset\operatorname{int}B.
\tag{2}
\]

Then every admissible solution exists throughout \([t_j,t_j+h]\) and remains in \(B\). Let \(C\subseteq B\) be any sound contraction of this established slab enclosure. Then

\[
x(t_j+h,p)\in Y+h f^I(P,C).
\tag{3}
\]

Consequently one may contract the right-hand side of (3), round it outward, and intersect it with \(C\), in any order that retains every possible endpoint.

**Proof.** Fix a parameter and an enclosed initial state. A polynomial vector field is locally Lipschitz, so a unique local solution exists. Suppose its first boundary contact with \(B\) occurs at \(0<\tau\le h\), measured from \(t_j\). Before contact, (1) gives

\[
x(t_j+\tau,p)=x(t_j,p)+\int_0^\tau f(p,x(t_j+s,p))\,ds
\in Y+\tau f^I(P,B)
\subseteq Y+[0,h]f^I(P,B).
\]

This is strictly inside \(B\), a contradiction. A finite maximal existence time before the end of the slab is also impossible: the solution remains in a compact subset of \(B\), its derivative is bounded there, and the standard continuation theorem extends it. The same integral argument with the now established enclosure \(C\) proves (3). ∎

The proof does not require a separate check of \(h\|D_xf\|<1\). Strict inclusion plus local existence, uniqueness, and continuation is enough. A non-strict inclusion with an explicit contraction condition gives another classical route, but is not the prototype's certificate.

The contraction \(C\) need not itself satisfy (2). For example, imposing nonnegativity after validation may put a physical trajectory on a face of \(C\). Requiring strict inclusion again would needlessly reject such tubes. The proof uses strict inclusion only for the raw box \(B\).

Equation (3) is an integrated slope enclosure, not an unverified Euler step. Replacing \(f^I(P,C)\) with \(f^I(P,Y)\) and omitting a remainder is generally invalid: for \(\dot x=x\), \(x(0)=1\), the value \(1+h\) does not enclose \(e^h\).

## 3. Sound physical and invariant contraction

For a closed mass-action system \(\dot x=S r(p,x)\), assume nonnegative rate constants and ordinary mass-action monomials. The vector field is quasipositive: when \(x_i=0\) and the other concentrations are nonnegative, consumption terms for species \(i\) vanish. Hence the nonnegative orthant is invariant. If

\[
w>0,\qquad w^T S=0,
\]

then \(w^Tx(t,p)=w^Tx_0(p)\). An upper bound \(M\) on this initial total gives the invariant compact box

\[
K_i=[0,M/w_i].
\tag{4}
\]

These facts establish global existence for admissible initial states. They also justify intersecting verified tubes and endpoints with \(K\). Extra affine invariants \(Ax=b+Dp\) can be propagated by sound interval row updates or a joint linear program. Every finite number of sound row sweeps is valid; reaching a fixed point is unnecessary for certification.

For the prototype's water-gas-shift/methanation species order \((\mathrm{CO},\mathrm{H_2O},\mathrm{CO_2},\mathrm{H_2},\mathrm{CH_4})\), the reaction columns are \((-1,-1,1,1,0)^T\) and \((-1,1,0,-3,1)^T\). The positive vector \((28,18,44,2,16)^T\) annihilates both columns. This is one convenient conserved mass vector; the tighter element-balance rows remain useful for contraction.

An unsuccessful finite tube search is a failure to validate the chosen time step. It is not evidence of physical infeasibility. Likewise, the prototype reports empty contraction as an error requiring inspection of the metadata; it does not silently turn that event into a global optimization exclusion.

## 4. The prototype's inflation rule and small-step success

Starting from \(Y_j\subseteq K\), the implementation computes \(V_j=f^I(P,Y_j)\) and tries the raw box

\[
B_j=Y_j+\prod_i[-r_{j,i},r_{j,i}],\qquad
r_{j,i}=h_j\big((1+\alpha)\operatorname{mag}(V_{j,i})+\mu\big),
\tag{5}
\]

with \(\alpha\ge0\) and a fixed positive **rate margin** \(\mu>0\). Failed attempts double the radii of coordinates whose strict inclusion failed, up to a stated cap. Every returned slab has separately passed (2); (5) alone is never accepted as a certificate.

The factor \(h_j\) applies to the margin too. Thus a fixed positive rate margin introduces \(O(h_j)\) padding, not a fixed state-width floor. It also permits strict inclusion in a coordinate whose derivative is identically zero.

For completeness, the first attempt succeeds uniformly for sufficiently small \(h_j\) on a fixed compact model domain. Indeed, natural interval polynomial evaluation is uniformly continuous in box endpoints on compact sets. The seed magnitudes are uniformly bounded for \(P\subseteq\bar P\), \(Y_j\subseteq K\). Therefore \(B_j\) approaches \(Y_j\) uniformly as \(h_j\to0\), and

\[
\operatorname{mag}(f_i^I(P,B_j))
<\operatorname{mag}(V_{j,i})+\mu
\le r_{j,i}/h_j
\]

for all sufficiently small steps. This strict magnitude bound implies (2). One can obtain an explicit step threshold from endpoint Lipschitz constants, but the prototype checks (2) directly. A fixed inflation cap may fail at practical coarse steps even though sufficiently small steps succeed.

## 5. Width convergence, including rounding

Natural interval evaluation of a fixed polynomial graph on bounded boxes has finite constants \(L_x,L_p\ge0\) such that

\[
w(f^I(P,C))\le L_x w(C)+L_p w(P),
\qquad P\subseteq\bar P,\ C\subseteq K.
\tag{6}
\]

This follows by induction from interval addition and

\[
w(UV)\le\operatorname{mag}(U)w(V)+\operatorname{mag}(V)w(U).
\]

The constants in (6) concern the actual interval expression, not just the derivative of the simplified real function. For example, the expression \(x-x\) has zero real derivative but natural interval width \(2w(X)\). Using a zero width constant inferred from that derivative would be wrong.

Let \(W_j=w(Y_j)\), \(h_{\max}=\max_jh_j\), and \(\sum_jh_j=T\). Suppose the successful raw boxes satisfy

\[
w(B_j)\le W_j+\nu h_j
\tag{7}
\]

for one finite \(\nu\). Rule (5), bounded seed magnitudes, and a fixed number of possible doublings imply (7). Sound contraction gives \(w(C_j)\le w(B_j)\). If outward arithmetic rounding in the endpoint calculation adds at most \(\delta_j\) to its maximum component width, then (3) and (6) imply

\[
W_{j+1}\le(1+L_xh_j)W_j+L_ph_jw(P)+L_x\nu h_j^2+\delta_j.
\tag{8}
\]

Iterating and using \(1+a\le e^a\) yields

\[
W_N\le e^{L_xT}
\left[W_0+L_pT w(P)+L_x\nu T h_{\max}+\sum_j\delta_j\right].
\tag{9}
\]

The same argument bounds every intermediate endpoint, and (7) bounds each entire slab. Thus, for fixed finite \(T\), all enclosure widths vanish when

\[
W_0\to0,\quad w(P)\to0,\quad h_{\max}\to0,\quad
\sum_j\delta_j\to0.
\tag{10}
\]

For affine \(x_0(p)\), \(W_0=O(w(P))\). If \(\sum_j\delta_j=O(h_{\max})\), the bound is \(O(w(P)+h_{\max})\). Correlation loss can make the exponential constant poor, so this is an asymptotic guarantee, not a claim of competitive long-horizon enclosure quality.

The current implementation uses exact rational interval operations and optionally rounds endpoint coordinates outward to a grid of spacing \(g=1/d\). This adds at most \(2g\) per coordinate per step. On a uniform mesh, the bound on accumulated rounding is \(2Tg/h\). Accordingly:

- A fixed denominator is valid but does not justify the vanishing-step convergence claim.
- \(g=o(h)\), equivalently \(hd\to\infty\), is sufficient for the rounding contribution to vanish.
- \(g=O(h^2)\) retains the first-order bound.
- `grid_denominator=None` removes this rounding term, with potentially severe rational-denominator growth.

This is a real obstruction, not just a limitation of estimate (9). The independent `polynomial_tube_review` agent supplied the exact example \(\dot x=1/3\), \(x(0)=0\), physical box \([0,1]\) on \([0,1]\), \(\alpha=0\), \(\mu=1/3\), and grid denominator \(d=1\). With \(N\ge2\) uniform steps, the code returns

\[
Y_j=[0,2j/(3N)],\qquad j=0,\ldots,N.
\]

Indeed, each raw radius is \(2/(3N)\). The exact endpoint image is \([1/(3N),(2j+1)/(3N)]\) at step \(j\) starting from \(Y_j\); outward rounding gives \([0,1]\), and intersection with the validated tube gives \(Y_{j+1}\). Hence the final box is always \([0,2/3]\), despite the true endpoint being \(1/3\). The reviewer checked \(N=2,3,10,40,100\) with exact rational execution. Without endpoint grid rounding, every returned endpoint is the exact singleton \(j/(3N)\).

Retaining nonzero initial uncertainty that is not represented by shrinking parameters also prevents (10). Such uncertainty must either be partitioned too or treated as a different robust optimization problem.

## 6. Connection to certified affine supporting flows

Let \(X_j=C_j\) be the validated physical box on slab \(j\), and compile its signed extended RPD field \(F_j\) using fixed interval data from this box. The physical signed state \(z=(x,-x)\) satisfies

\[
\dot z(t,p)\ge F_j(p,z(t,p))
\ge d_j+A_jp+B_jz(t,p),
\tag{11}
\]

where the second inequality is a globally valid affine support and \(B_j\) is Metzler. Starting the affine system at a certified lower affine bound from the previous slab gives

\[
\dot\ell=d_j+A_jp+B_j\ell,\qquad \ell(t,p)\le z(t,p)
\]

by cooperative comparison. The same proof works across the known slab switches. The old affine lower bound or the support-selection reference need not lie inside \(X_j\); global finite extended arithmetic on empty endpoint inputs is what permits that situation. Only the physical trajectory must lie in the validated box. Certified matrix-exponential propagation and its final downward rounding correction remain necessary.

This argument establishes validity of adaptive slab interval data without integrating one global nonlinear relaxation field. It does not prove that every arbitrary support-selection policy recovers the tight interval bounds. For a simple objective-bound safeguard, retain both the affine bound and a natural interval objective bound computed from the validated endpoint box, then take the stronger lower bound. For a continuous objective with a convergent interval extension, (10) makes the latter width vanish. This supplies a value-consistency ingredient for parameter branch and bound; it does not by itself prove finite termination, feasible incumbent certification, or a complete mixed-integer algorithm.

Known changes of control or reaction regime can be placed on slab boundaries and treated separately. Unknown switching times, state-dependent events, non-polynomial primitives without certified interval evaluation, and unbounded state domains are outside this prototype's proof.

## 7. Established methods and comparison requirements

The coarse interval Picard enclosure followed by a tighter endpoint calculation is classical. Immler explicitly uses this two-stage structure in the open primary article [*A Verified ODE Solver and the Lorenz Attractor*](https://pmc.ncbi.nlm.nih.gov/articles/PMC6044317/), section “Single Step”; the tighter method there uses Runge–Kutta and affine arithmetic. The present interval slope endpoint is deliberately simpler and lower order. It should be compared with stronger validated solvers when enclosure tightness or long-horizon cost matters.

Relevant primary literature queued for the local knowledge base includes Lin and Stadtherr, [*Validated solutions of initial value problems for parametric ODEs*](https://doi.org/10.1016/j.apnum.2006.10.006), Applied Numerical Mathematics 57 (2007), 1145–1162; Nedialkov, Jackson, and Corliss, [*Validated solutions of initial value problems for ordinary differential equations*](https://doi.org/10.1016/S0096-3003(98)10083-8), Applied Mathematics and Computation 105 (1999), 21–68; and Scott and Barton, [*Tight, efficient bounds on solutions of chemical kinetics models*](https://doi.org/10.1016/j.compchemeng.2009.11.021), Computers & Chemical Engineering 34 (2010), 717–731. Their full formulations have not been inspected for this note. No new-priority claim depends on them being unavailable.

The immediate comparative experiment should vary parameter width and time step independently, using the same physical model and objective for all methods. Record interval-only bounds, fixed-box affine-flow bounds, slab-box affine-flow bounds, certificate cost, and arithmetic precision. Include singleton parameters to expose a fixed-state-box floor. A numerical trajectory lying inside a tube is only a diagnostic; the rational inclusion checks and the proof above are the certificate.
