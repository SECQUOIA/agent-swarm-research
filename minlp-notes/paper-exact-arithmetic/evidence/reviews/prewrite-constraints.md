The constrained and mixed-integer claims examined here have sound proofs at their stated scopes. I found no blocking mathematical error in the candidate-list, active-gap, constraint-rank, nonlinear-dimension, structured-box, or separable-flow arguments. The unrestricted deterministic polynomial-time PosSLP-oracle problem remains unresolved. Two short analytic additions below make the structured-box proof self-contained: an elementary proof of the comparison-matrix vector condition and a complete parametric proof of the at-most-two-pivots-per-coordinate QP algorithm.

This is an internal proof audit for the manuscript brief, dated 2026-10-05. I read the assigned notes, their upper-bound and candidate-list dependencies, and the relevant existing source-interface reviews. I did not browse, discover literature, download sources, delegate, run experiments, or rerun any mathematical checker. Recorded experimental results are prior evidence; they are not verification performed in this audit. The external algorithms below are accepted only at the precise interfaces recorded in the existing primary-source audits. The manuscript must cite those primary theorems directly rather than cite repository notes as substitutes.

The audit uses L for total explicit binary input length, increased to at least two; n for continuous dimension; t for the number of integer variables when nonlinear dimension k is also present; and r for the rank of continuous constraint normals. Every polynomial has fixed degree and explicit rational coefficients. A supplied positive rational curvature modulus is part of L. A bare modulus gives a promise theorem. A checked rational Gram gives an ordinary certificate-input language only for the explicitly described certificate subclass.

The following scopes can be stated in the paper. The output in the last column is exact but need not be an expanded algebraic coordinate list.

| Assumptions beyond global strong convexity or monotonicity | Valid computation bound | Output and qualification |
| --- | --- | --- |
| Arbitrary rational polyhedron | UP^PosSLP intersect coUP^PosSLP | Fixed-degree observable sign at the unique optimum or VI solution; no deterministic polynomial-time active-set search follows |
| Supplied polynomial-encoding lower bound on every nonzero optimal slack | Polynomial-time many-one reduction to one PosSLP instance per observable relation | Ordinary approximation recovers the full active set first; the slack-gap promise is not verified |
| t integer variables and unrestricted continuous fibers, with rational inequalities on the integer block | 2^{O(t log(t+1))} L^C ordinary candidate construction; the same form with nonadaptive PosSLP queries for exact selection | A finite list containing every optimal integer block; all optimum blocks can then be selected |
| t integer variables and arbitrary mixed rational linear constraints | a(t)L^C ordinary candidate construction | A finite list of feasible integer blocks containing every optimal block; exact constrained-fiber selection remains separate |
| Continuous constraint-normal rank r | Expected (r+1)^{O(r)} L^C with PosSLP | Las Vegas observable decision and polynomial-size affine/unique-zero optimizer representation |
| t integer variables and continuous constraint-normal rank r under arbitrary mixed linear constraints | Expected F(t,r)L^C with PosSLP | An optimal integer block and its continuous unique-zero representation; ties can be retained |
| Nonlinear dimension k | F(k)L^C ordinary deterministic bit time | Exact observable decisions, full active set, and an affine image of a unique stationary point in at most k variables |
| t integer variables and joint nonlinear dimension k, under arbitrary mixed linear constraints | F(k+t)L^C ordinary deterministic bit time | Exact optimum comparison and optimal integer-block selection; the continuous representation has at most k algebraic variables |
| Box and Hessian support contained in a supplied forest, or nonpositive Hessian off-diagonal entries | Polynomial-time Turing reduction to PosSLP | Observable signs and active bounds; arbitrary active-set size and zero multipliers are permitted |
| Network-flow polyhedron and separable globally strongly convex arc polynomials | Polynomial-time Turing reduction to PosSLP | Observable signs, active bounds, and rational-circuit feasible witnesses for strict value inequalities |

Here and below C is an absolute constant; parameter-dependent constants must not be hidden in the exponent of L. The mixed candidate theorem establishes a computable a(t), whereas the more specific 2^{O(t log(t+1))} bound is justified for its unrestricted-fiber predecessor. There is no proof here of the latter sharper parameter function for arbitrary mixed constraints.

The principal sources examined are [the active-gap note](../../../research-20260927/polyhedral-strong-quartic-active-gap.md), [the unrestricted-fiber list](../../../research-20260927/fixed-integer-strong-quartic-fpt.md), [the mixed-constraint list](../../../research-20260927/mixed-linear-strong-quartic-candidate-list.md), [the constraint-rank algorithm](../../../research-20260927/constraint-rank-strong-monotone-oracle.md), [their mixed composition](../../../research-20260927/mixed-quartic-integer-constraint-rank-oracle.md), and the October 3 [nonlinear-dimension theorem](../../../research-20261003-arithmetic/constrained-exact/theorem.md), [Newton transfer](../../../research-20261003-arithmetic/constrained-exact/structural-newton.md), [flow theorem](../../../research-20261003-arithmetic/constrained-exact/network-flow.md), and [remaining boundary](../../../research-20261003-arithmetic/constrained-exact/general-boundary.md).

**Polyhedral optimality supplies the common geometric lemma.** Let P={x:Ax<=b} be nonempty, and let p minimize a differentiable convex f. For each d satisfying a_i^T d<=0 on all rows active at p, p+epsilon d is feasible for sufficiently small positive epsilon. Inactive rows have positive slack and there are finitely many rows. Thus grad f(p)^T d>=0. The polar form of Farkas' lemma gives

\[
 -\nabla f(p)\in\operatorname{cone}\{a_i:a_i^{\mathsf T}p=b_i\}.
\]

The same proof applies to T(p) at a variational-inequality solution. No Slater point, full-dimensional feasible set, or independent equality description is needed. Equalities encoded by opposite inequalities are covered.

Choose a conic representation with minimum positive support. If the used normals are dependent, choose a nonzero dependence d_i, change its sign so that some d_i>0, and subtract theta d_i from the positive coefficients, with theta=min_{d_i>0} lambda_i/d_i. The represented vector is unchanged, all coefficients remain nonnegative, and one disappears. This contradicts minimality. Hence a support of linearly independent active normals exists, of size at most rank(A). A zero represented vector uses the empty support.

For an independent support I, the free-coordinate chart x=xbar+Zy is obtained by solving pivot coordinates in terms of the remaining original coordinates. Z contains an identity row block, so Z^T Z>=I. Its rational coefficients have polynomial bit length by determinant bounds. Therefore

\[
 \nabla^2 f(x)\succeq\mu I
 \quad\Longrightarrow\quad
 \nabla^2(f(\bar x+Zy))\succeq\mu I,
\]

and, for a globally mu-strongly monotone map T,

\[
 U(y)=Z^{\mathsf T}T(\bar x+Zy)
\]

is globally mu-strongly monotone. The support selects the actual optimizer or VI solution as the unique zero of the restricted equations. The chart needs no curvature-conditioning promise. A rank-n chart is a rational point and should bypass zero-map calls entirely.

Existence for a nonpotential strongly monotone T on an unbounded polyhedron also has a complete elementary proof. Fix x0 in P and R>||T(x0)||/mu. On K=P intersect the closed radius-R ball centered at x0, a fixed point of x -> projection_K(x-T(x)) exists by Brouwer and solves the VI on K. It cannot lie on the artificial sphere, because strong monotonicity gives

\[
 T(p)^{\mathsf T}(p-x_0)
 \ge\mu R^2-\|T(x_0)\|R>0,
\]

whereas the VI tested at x0 gives the opposite weak inequality. A short segment toward any point of P now extends the VI from K to all of P. Summing the VI inequalities for two candidate solutions contradicts strong monotonicity unless they coincide. This supplies every subset solution needed later.

**The general upper bound and supplied active gap are distinct results.** The [active-support verifier](../../../research-20260927/polyhedral-strong-quartic-posslp-upper.md) guesses an independent active support I and checks primal slacks, nonnegative multipliers

\[
 \Lambda_I(y)=-(A_IA_I^{\mathsf T})^{-1}
                 A_I\nabla f(\bar x+Zy),
\]

and stationarity at the unconstrained minimizer of the restricted polynomial. All tested expressions are explicit polynomials of degree at most four and polynomial encoding length. The unconstrained observable theorem applies. These checks prove global constrained optimality, and some support passes. Testing a requested relation or its complement proves NP^PosSLP intersect coNP^PosSLP. Enumerating supports is not polynomial time when dimension varies.

The [unambiguous refinement](../../../research-20260927/polyhedral-strong-quartic-unambiguous-upper.md) uses a fixed-length full active-mask guess, so it can have only one accepting mask. Its important additional step is a deterministic normal-cone check, rather than a guessed multiplier support. For a proposed mask S, set

\[
 Q_S=\{v:A_Sv\le0,\ -1\le v_j\le1\}.
\]

It checks min_{v in Q_S} grad f(p_S)^T v>=0. To implement this, use the uniform polynomial coordinate-size bound for every rational vertex v of Q_S. Every observable v^T grad f(xbar+Zy) then has uniformly polynomial encoding length. The existing singleton gap and Newton construction approximate all these vertex costs to a common gamma/8 using one rational circuit point. Solve the rational LP with that circuit objective, recover its chosen vertex as printed rational coordinates from n independent active equations, and ask the true explicit vertex-observable sign. If any true vertex cost is negative, it is at most -gamma and its approximate cost is at most -7gamma/8; a true nonnegative vertex has approximate cost at least -gamma/8. Thus the approximate-cost optimal vertex detects exactly the existence of a negative true cost. No LP with an unhandled algebraic objective is used.

This depends on the precise GLS arithmetic LP interface recorded in the existing note: polynomially many elementary arithmetic operations and comparisons in the explicit constraint-matrix encoding, independently of objective and right-hand-side encoding lengths. The recorded inspection also covers its bounded rounding steps. The proof cannot replace this by a generic polynomial-bit LP claim for expanded circuit coefficients. For the manuscript, state this as a cited algorithmic lemma, explain the circuit simulation, and include vertex recovery. A lower-dimensional bounded polytope still has n independent active normals at every vertex; otherwise it admits a short feasible segment through the vertex in both directions.

The normal-cone check and exact zero/positive slack mask prove UP^PosSLP intersect coUP^PosSLP. The same reasoning permits any supplied explicit degree-four observable, although the original quartic statement emphasizes value and coordinate comparison. In the verified-certificate language, reject an invalid certificate before feasibility and handle that rejection deterministically in the complement. For bare curvature data, retain the promise formulation. The [VI extension](../../../research-20260927/polyhedral-strong-monotone-vi-upper.md) replaces grad f by T and uses its corresponding unconstrained zero theorem; the geometric and cost-transfer arguments are unchanged.

For the active-gap refinement, supply delta>0 such that every slack at p is zero or at least delta, and let sigma=max(1,max_i ||a_i||_1). Request an exactly feasible rational approximation of objective error

\[
 \varepsilon=\min\{1,\mu\delta^2/(128\sigma^2)\}.
\]

Constrained first-order optimality must be retained:

\[
 f(\widehat p)-f(p)
 \ge\nabla f(p)^{\mathsf T}(\widehat p-p)
       +\frac\mu2\|\widehat p-p\|^2
 \ge\frac\mu2\|\widehat p-p\|^2.
\]

It follows that ||phat-p||<=delta/(8 sigma), so row-slack errors are at most delta/8. The rows with approximate slack below delta/2 are exactly all active rows. Restriction to their row space now gives one unconstrained observable instance, hence one many-one PosSLP instance for each requested relation. A chosen row basis need not itself have nonnegative multipliers; stationarity on its affine space is all that is needed after identifying the entire mask. The claim remains conditional on the supplied gap, and a general algebraic separation estimate does not provide a polynomial-bit delta.

**The candidate-list theorem has a valid fixed-oracle proof.** The required external integer-feasibility algorithm must satisfy this exact interface: for a fixed closed convex S contained in [-R,R]^t, queried only at integer points, accept membership or return a rational inequality valid on S and strictly violated by the query. Empty targets, singleton targets, and deficient dimension are allowed. The complexity is

\[
 2^{O(t\log(t+1))}
 \operatorname{poly}\bigl(t,1+\langle R\rangle,
     \Phi(c_0t(1+\langle R\rangle))\bigr),
\]

with absolute polynomial degree, including answer-output length in Phi. Queries under lattice parametrizations return to the original integer coordinates before the supplied oracle is evaluated. The existing [integer-query audit](../../../research-20260927/integer-query-convex-oracle-prior.md) records this for the cited Ari--Hildebrand, Hildebrand--Goess, and Basu results. The manuscript should explicitly state the interface and cite the inspected versions. A theorem requiring separation of the whole continuous sublevel would not be sufficient.

For initial mixed-linear feasibility, the existing notes use Del Pia's fixed-integer-dimension convex quadratic algorithm with constant objective zero. It supplies an attained feasible rational witness or an infeasibility answer in a(t)L^C time. This is a feasibility import, not exact nonlinear optimization. For the unrestricted-fiber integer-polyhedron case, Hildebrand--Koeppe's linear specialization gives the sharper 2^{O(t log(t+1))} preprocessing bound recorded in its source audit. In either case, the witness encoding is charged to preprocessing time.

If x0 is a feasible witness, let C0=f(x0), F0=f(0), a0=grad f(0), and

\[
 A_0=\|a_0\|_1+|C_0-F_0|+1,
 \qquad R=2+\lceil2A_0/\mu\rceil.
\]

For rho=||x||>=R, global strong convexity gives

\[
 f(x)-C_0\ge
    \rho(\mu\rho/2-\|a_0\|_1)-|C_0-F_0|>0.
\]

Coercivity and closedness give attainment, and every optimizer lies inside that radius. Fixed degree bounds the encoding of R polynomially in the input and witness encoding. Truncate only the integer block for the mixed theorem. Continuous fibers retain all original inequalities.

At a feasible integer query z, suppose the routine computes rational q with the following inequality for every distinct feasible integer w:

\[
 g(w)-g(z)\ge q^{\mathsf T}(w-z)
                    +\frac\mu4\|w-z\|^2.                 \tag{C1}
\]

Then q=0 proves z is the unique globally optimal integer block. Otherwise

\[
 q^{\mathsf T}(x-z)\le-\mu/4                          \tag{C2}
\]

strictly excludes z and retains every other feasible integer point no worse than z, including tied optima. A cut need not retain every better nonintegral point.

Initialize the candidate list with the initial feasible integer block. Run the deterministic integer-feasibility algorithm; reject infeasible-fiber or outside-box queries by domain cuts, and record each other query before returning (C2). Stop early if q=0. All oracle routines and tie choices depend only on the fixed data and query, not on a changing incumbent.

To prove termination first, use the fixed target S=empty. Every returned inequality is valid there and strictly excludes its query. Complete a possible q=0 answer by x_1<=z_1-1 for this proof only; the actual list algorithm stops at that query. The run is therefore a prefix of a valid empty-target execution, and the cited bound proves its termination and total output size. This argument does not assume an optimum has already been found.

To prove that every optimal block w is present, suppose w is omitted after a non-early run. Define a total oracle for the fixed singleton {w}: accept exactly at w, and use the same canonical domain and gradient/residual cuts elsewhere. Domain cuts retain w. At every other feasible query z, (C1) and g(w)<=g(z) make (C2) valid at w. A zero q at a different query would make that query the unique optimum, which is impossible. Hardcoding w adds only O(t(1+<R>)) bits and a cheap equality check. Since w was never queried, the actual transcript is identical to this valid singleton execution, which would falsely return emptiness. Hence no optimal block is omitted. The zero-q early stop already records the unique optimum. Dispatch t=0 separately after feasibility, returning the singleton empty integer vector; no positive-dimensional feasibility theorem is invoked then.

The proof really gives all optimum blocks, not just one. There are at most 2^t of them: two different blocks of the same coordinatewise parity have a feasible integer midpoint, and averaging their continuous optimizers preserves mixed linear constraints. Joint strict convexity makes that midpoint strictly better. The example sum_i(z_i-1/2)^2+||y||^2 attains the bound.

Uniform answer sizes are essential. Every cut must be computed from the original polynomial and original integer query. Substitution of a degree-four polynomial, rational LP, derivative bounds, and rational feasible approximations cost a fixed polynomial in L, <R>, and query length. This is why the algorithm is FPT rather than a recursion with a parameter-dependent input-length exponent. The older vertex-enumeration recursion establishes a valid fixed-dimension polynomial result, but its L^{O(t)}-type intermediate counts should not be reused to justify an FPT claim.

**Unrestricted fibers implement (C1) by a coarse gradient.** For f(z,y) globally mu-strongly convex, y(z) is uniquely defined and smooth by the implicit function theorem for grad_y f=0. Partial minimization is globally mu-strongly convex and

\[
 \nabla g(z)=\nabla_z f(z,y(z)).
\]

If ||q-grad g(z)||<=mu/4, strong convexity and ||w-z||>=1 give

\[
 g(w)-g(z)\ge q^{\mathsf T}(w-z)
    +\frac\mu2\|w-z\|^2-\frac\mu4\|w-z\|
 \ge q^{\mathsf T}(w-z)+\frac\mu4\|w-z\|^2.
\]

A polynomially accurate rational fiber minimizer produces that q. With m=t+n, C=max(1,sum |f_alpha|), integer box R, set

\[
 D_0=4mC(1+R)^3,\quad
 S_0=1+R+D_0/\mu,\quad
 K_0=1+12mCS_0^2.
\]

Strong monotonicity gives ||y(z)||<=D0/mu from the gradient at y=0; K0 bounds the cross-Hessian on its unit neighborhood. Put tau=mu/(4t), eta=min(1,tau/K0). An actual rational approximate minimizer of objective error at most min(1,mu eta^2/2) has distance at most eta, so every integer-gradient component error is at most tau and its Euclidean error is at most sqrt(t)tau<=mu/4. This uses only ordinary precision of polynomial encoding length. If n=0, evaluate the gradient exactly. If t=0, use the dispatch above.

After this list is known, exact selection over unrestricted fibers can use a nonadaptive batch. For candidates z,w, minimize f(z,y)+f(w,y') and evaluate f(z,y)-f(w,y') at its unique minimizer. This observable equals the fiber-value difference, even if either value is irrational. All pairwise comparisons and rational threshold comparisons reduce independently to PosSLP by the unconstrained theorem; s^2 queries for a list of size s retain every minimum block. A tournament uses s-1 adaptive comparisons if only one block is requested. Neither statement assumes closure of PosSLP under arbitrary Boolean combinations or a single many-one reduction for the complete mixed problem.

**Mixed constraints implement (C1) by a primal-dual residual without Slater.** Consider Az+By<=c and a feasible query z. Rational LP returns either a short feasible fiber point ybar or a rational Farkas vector alpha>=0 with B^T alpha=0 and alpha^T(c-Az)<0. In the infeasible case, alpha^T A w<=alpha^T c is a projection-valid strict separator. Do not construct an explicit inequality description of the projection.

In a feasible fiber, let yhat be any rational feasible point and lambda>=0 any rational vector. Define

\[
 \begin{aligned}
 s&=c-Az-B\widehat y\ge0,\\
 r_y&=\nabla_y f(z,\widehat y)+B^{\mathsf T}\lambda,\\
 E&=\lambda^{\mathsf T}s+\frac{\|r_y\|^2}{2\mu},\\
 q&=\nabla_z f(z,\widehat y)+A^{\mathsf T}\lambda.
 \end{aligned}
\]

For another feasible (w,v), put dz=w-z and dy=v-yhat. Feasibility gives lambda^T(A dz+B dy)<=lambda^T s. Joint strong convexity therefore gives

\[
 f(w,v)\ge f(z,\widehat y)+q^{\mathsf T}d_z
     +r_y^{\mathsf T}d_y-\lambda^{\mathsf T}s
     +\frac\mu2(\|d_z\|^2+\|d_y\|^2).
\]

Complete the square in dy, minimize over v, and use f(z,yhat)>=g(z). The result is

\[
 g(w)-g(z)\ge q^{\mathsf T}(w-z)
                          +\frac\mu2\|w-z\|^2-E.
\]

If E<=mu/4, the integer-distance bound gives (C1), since mu||w-z||^2/2-mu/4>=mu||w-z||^2/4. This argument uses neither differentiability of g nor a finite extension of g outside its projected domain.

To construct E<=mu/4 ordinarily, write h(y)=f(z,y) and let p minimize h on its fiber. From ybar compute

\[
 A_z=\|\nabla h(0)\|_1+|h(\bar y)-h(0)|+1,
 \qquad Y=2+\lceil2A_z/\mu\rceil.
\]

Then ||p||<Y. With m=t+n and the original coefficient bound C, set S=2+R+Y, G=1+4mCS^3, and K=1+12mCS^2. G bounds ||grad h(p)|| and K bounds the Hessian operator norm throughout its unit neighborhood. Request an exactly feasible rational yhat with objective error at most min(1,mu delta^2/2), where

\[
 \delta=\min\{1,\mu/[16(G+1)],\mu/(4K)\}.
\]

Constrained first-order optimality gives ||yhat-p||<=delta. Polyhedral normal-cone optimality supplies some real lambda_*>=0 satisfying stationarity and complementarity at p. It need not be rational, bounded, or unique. The decisive identity is

\[
 0\le\lambda_*^{\mathsf T}s
    =\nabla h(p)^{\mathsf T}(\widehat y-p)
    \le G\delta.
\]

Also ||grad h(yhat)+B^T lambda_*||<=K delta. Thus the rational convex quadratic

\[
 \mathcal E(\lambda)=s^{\mathsf T}\lambda
      +\frac{\|\nabla h(\widehat y)+B^{\mathsf T}\lambda\|^2}{2\mu}
      \quad(\lambda\ge0)
\]

has infimum at most mu/16+mu/32=3mu/32. It attains a minimum: its image cone {(B^T lambda,s^T lambda):lambda>=0} is a closed polyhedral cone with second coordinate nonnegative, and a sublevel of t+||grad h(yhat)+u||^2/(2mu) in these image coordinates is compact. A minimizer in the image lifts to a nonnegative lambda. The multiplier set itself need not have bounded sublevels.

An ordinary rational convex approximation of this quadratic to error at most min(1,mu/8) returns a feasible rational lambdahat with E<=7mu/32<mu/4. The two convex calls have explicit rational data of polynomial length in the original query and fixed data. Their required accuracy has polynomial printed encoding. This proves the mixed answer-size bound independently of ||lambda_*||. If n=0, direct integer-gradient evaluation suffices. No active-set recognition, multiplier lower bound, or strict-feasibility point enters the construction.

Every invocation of the ordinary approximation result in these proofs must have the exact-feasibility contract used in the existing source audits: it returns a rational point in the original rational polyhedron, while only objective accuracy is relaxed. A point violating constraints by a tiny amount would invalidate both the distance estimate and the slack/multiplier identity. The manuscript should name the global-convexity, finite attained minimum, unbounded-polyhedron, and deficient-dimensional provisions explicitly. Cap all requested errors by one as above; this is a harmless precision repair where older notes leave the cap implicit.

**Constraint rank controls a genuine violator space.** Precheck the full polyhedron by rational LP. Then every row subset G is feasible and has a unique VI solution p_G. With row-index ground set H define V(G)={i:a_i^T p_G>b_i}. Consistency is immediate. If F is contained in G and G has no violations at p_F, p_F is feasible for P_G and its VI inequality on P_F remains valid on P_G. Uniqueness implies p_F=p_G, proving locality. No scalar potential or ordering by objective values is required.

The independent active support at p_G has size at most r=rank(A) and determines the same VI solution using only those support inequalities. Hence it determines the same violator set. To bound every minimal basis B, apply that support argument to B itself. A subset I of B of size at most r has V(I)=V(B); minimality forces I=B. Merely proving that some small support exists in the full instance would not establish Clarkson's combinatorial-dimension bound. The full-feasibility precheck is also necessary to exclude an infeasibility-basis case. When r=0, feasibility makes every zero-normal row automatic and the problem is unconstrained.

For a required violation test with first argument G of size at most r, enumerate all independent subsets I of G, at most 2^r. Form the free-coordinate chart and U_I(y)=Z^T T(xbar+Zy). At its unique real zero, test all G inequalities, nonnegativity of

\[
 \Lambda_I(y)=-(A_IA_I^{\mathsf T})^{-1}A_IT(\bar x+Zy),
\]

and T(xbar+Zy)+A_I^T Lambda_I(y)=0. Every scalar observable is explicit of degree at most three and polynomial coefficient length. The zero theorem implements these tests with polynomial-size PosSLP instances. Some support passes; every passing support proves the VI and hence gives p_G. Then test a_j^T p_G>b_j. This is a deterministic primitive of cost 2^r L^{C0}. It handles non-basis G, redundant rows, empty support, and rank-full rational charts. It does not require the unambiguous verifier's circuit-objective LP.

The external violator-space sampling theorem supplies expected O(rm+r^{O(r)}) such tests. The existing primary-source audit checks an important detail: first arguments are returned bases or candidate subsets of size at most r, including one-element deletions. Larger sampled sets are processed using these small tests; they are not passed directly to the expensive primitive. Binary multiplicities in the weighted stage have polynomial size, because each stage has only O(r log m) successful nonterminal weight doublings. Sample labeled copies by prefix sums and bounded-length uniform integer draws, then identify duplicate copies before the exhaustive subset routine. Random-bit and rational overhead is polynomial per sampled operation. This converts the theorem's expected primitive count to expected bit time. The final no-violations check guarantees correctness, so the algorithm is Las Vegas.

The output chart and cubic zero map are polynomial-size in one explicit fiber input, independently of how many random samples were taken. The rank is the rank of all normals, not the size of the final active support. A full-dimensional box normally has rank n. The rank theorem neither proves deterministic FPT nor removes PosSLP, which is already material at rank zero.

For the mixed composition, each candidate z has nonempty fiber P_z={y:By<=c-Az} and objective f_z(y)=f(z,y) with Hessian at least mu I. If the candidate output has total encoding Q=a(t)L^{C1}+L, every substituted fiber and each pairwise product has encoding polynomial in Q with an absolute exponent. On a product fiber, minimize f_z(y)+f_w(y') and observe f_z(y)-f_w(y'); its constraint-normal rank is exactly 2rank(B). Thus each pair comparison has expected cost (2r+1)^{O(r)}Q^{C2}. At most Q comparisons and final recovery calls give expected F(t,r)L^C. Conditional expectations are uniformly bounded for every possible previous history; fresh random bits make the composition Las Vegas. A fixed lexicographic scan that replaces only on strict improvement chooses the lexicographically first global optimal integer block. Compare all candidates with that block afterward to return every tied block if desired. This additional linear number of exact comparisons preserves the bound.

Do not assume that a full positive definite Hessian Gram is closed under fiber substitution or separable product formation. A checked original certificate already proves the global curvature promise; each derived internal instance can use that inherited promise. The selected continuous optimum is represented by a rational chart and a unique-zero polynomial map, not by rational arithmetic circuits for its generally irrational coordinates.

**Nonlinear dimension gives ordinary FPT exact comparison without searching faces.** Write f=q+r_3+r_4, where q has degree at most two and r_j is homogeneous of degree j. Form the coefficient matrix of the vector gradient of r_3+r_4, with rows indexed by monomials of degree two and three. Its kernel is K={v:D_v(r_3+r_4)=0}, and its rank is k. Rational elimination gives a row basis U with kernel K and a right inverse V. Integrating the zero directional derivative along lines in K proves

\[
 r_3(x)+r_4(x)=g(Ux),\qquad g(t)=r_3(Vt)+r_4(Vt).
\]

This construction has polynomial encoding length and time at fixed degree. Translation preserves K: the new quartic part is r_4 and the new cubic part is r_3+D_a r_4. Once D_v r_4=0, D_v D_a r_4=0, so the cubic condition is still D_v r_3=0. This verifies both inclusions, rather than asserting translation invariance from terminology alone.

For the proof only, take the full active set S at p and its affine space E={x:A_Sx=b_S}. Polyhedral optimality makes p stationary on E; global strong convexity makes it the unique unconstrained minimizer there. Parameterize E by x=xbar+Zy and choose a rational decomposition y=Tt+Ww with W spanning ker(UZ). Put s=rank(UZ)<=k. Every term of degree at least three is independent of w, so

\[
 f(\bar x+ZTt+ZWw)
 =\tfrac12w^{\mathsf T}Hw+w^{\mathsf T}(Jt+a)+\psi(t).
\]

H is a constant rational positive definite matrix, by global curvature and injectivity of ZW. Eliminating w=-H^{-1}(Jt+a) gives a rational affine map x=u+Dt. Its image under U has linear part UZT of rank s, so D has full column rank. Consequently

\[
 \phi(t)=f(u+Dt),\quad \eta(t)=h(u+Dt),\quad
 \nabla^2\phi(t)\succeq\mu D^{\mathsf T}D\succ0,
 \qquad p=u+Dt_*\text{ with }\nabla\phi(t_*)=0.
\]

All rational data and fixed-degree coefficients have bit length bounded by one effective polynomial T(L) with an absolute exponent, uniformly over every independent input-row subset. This uses a fixed number of matrix nullspaces, inverses, and degree-four substitutions, not a sequence of L^{O(k)} expansions. Empty blocks are omitted. In particular, s=0 yields a polynomial-bit rational optimizer. If the returned representation needs a supplied reduced curvature modulus, use

\[
 \nu=\mu\,\frac{\det(D^{\mathsf T}D)}
                  {\operatorname{tr}(D^{\mathsf T}D)^{s-1}}>0
\]

for s>0. Its encoding is polynomial. Do not automatically reuse mu after arbitrary elimination coordinates; the reduced Hessian bound is mu D^T D.

For alpha=h(p), the existential formula grad phi(t)=0 and z=eta(t) has exactly one real z-value. It has at most k quantified variables, at most k+1 polynomials of degree at most four, and integer coefficients of bit length at most T(L) after denominator clearing. The cited one-block real-quantifier-elimination theorem bounds output coefficient bit lengths linearly in T(L), multiplied by a function G(k). This linear dependence is the decisive FPT fact. A bound T(L)^{O(k)} would not suffice. The existing source review explicitly checked this clause.

A quantifier-free description of a singleton must contain a nonzero polynomial vanishing at alpha: otherwise every sign would be locally constant. For alpha!=0, remove any factor z^e from such a polynomial. Its integer constant term is nonzero and has magnitude at least one. If degree is D0, coefficient magnitude at most H0, and |alpha|<1, its root equation gives 1<=D0 H0 |alpha|. Thus an effective uniform bound is

\[
 \alpha\ne0\quad\Longrightarrow\quad
       |\alpha|\ge\gamma=2^{-N},\qquad N=G(k)T(L),
\]

after enlarging fixed majorants. The unknown active set is used only to prove this bound; the algorithm neither guesses it nor executes quantifier elimination.

Obtain an ordinary polynomial-bit rational feasible x0 and a polynomial-bit radius R containing p by the coercive inequality. On the radius-(R+1) ball bound ||grad h|| by B>=1 of polynomial encoding length. Request an exactly feasible approximation with error at most min(1,mu delta^2/2), where delta=min(1,gamma/(8B)). Then ||xhat-p||<=delta and |h(xhat)-h(p)|<=gamma/8. Exact rational evaluation returns zero if |h(xhat)|<gamma/2 and otherwise its sign. A true zero has observed magnitude at most gamma/8; a nonzero value has magnitude at least 7gamma/8 and retains its sign. Crucially, the algorithm prints N accuracy bits. This costs F(k)L^C and is affordable under that bound; it is not a polynomial-time claim in log N.

Applying this decision routine to every slack recovers S in the same FPT form. Only then carry out the affine/quadratic elimination above to print the exact optimizer representation. Neither constraint rank nor active-set cardinality is a parameter. The optional bound F(k)=(k+2)^{O(k)} is consistent with the recorded one-block theorem, but a computable F(k) is sufficient for the main theorem and avoids unnecessary reliance on an optimized parameter bound.

For mixed variables, use the ordinary mixed candidate list first. In a fixed integer fiber, g(U_z z+U_y y) has higher-degree terms depending only on U_y y, so nonlinear dimension is at most the joint k; the same mu bounds the continuous principal Hessian. A product of two fibers has nonlinear dimension at most 2k. The theorem above therefore compares their minima ordinarily, including ties. If a fiber encoding is at most a(t)L^{C0}, the cost F(2k)[a(t)L^{C0}]^C still has an absolute input-length exponent. Summing over the list and enlarging parameter functions gives deterministic ordinary FPT in k+t. Global joint strong convexity is essential; fiber-only curvature would not justify the imported integer list.

A full positive definite Hessian Gram is too restrictive to serve as the default certificate for this theorem. In a direction from K, the objective's Hessian has no polynomial growth in that direction, whereas positive definiteness on a full tensor basis would force such growth. The note correctly offers instead a rational positive semidefinite Gram for v^T(H_f(x)-mu I)v. Coefficient identity and rational semidefinite checking certify curvature, but the paper must not claim that every globally strongly convex quartic admits that SOS certificate.

**Exact constrained Newton refinement needs an arithmetic QP interface.** On a bounded rational polyhedron P with a supplied rational containing box, define

\[
 N(x)=\arg\min_{y\in P}
   \left\{\nabla f(x)^{\mathsf T}(y-x)
        +\tfrac12(y-x)^{\mathsf T}H_f(x)(y-x)\right\}.
\]

Let M bound the Hessian Lipschitz constant on the containing box and K=max(1,M/(2mu)). The first-order inequalities at y=N(x) and p, with d=y-p, give

\[
 d^{\mathsf T}H_f(x)d
 \le[\nabla f(p)-\nabla f(x)-H_f(x)(p-x)]^{\mathsf T}d.
\]

Taylor's integral remainder is at most M||x-p||^2/2, so

\[
 \|N(x)-p\|\le K\|x-p\|^2.
\]

This proof holds on any convex feasible polyhedron and does not need identical active sets, strict complementarity, or a slack/multiplier gap. An exactly feasible ordinary warm start of objective error min(1,mu/(8K^2)) gives ||x0-p||<=1/(2K). Every exact Taylor-QP solution remains feasible, and induction gives

\[
 \|x_j-p\|\le K^{-1}2^{-2^j}.
\]

The computational hypothesis is stronger than polynomial bit time for explicitly expanded QP data. Each Taylor QP must be solved in polynomially many additions, subtractions, multiplications, divisions by known nonzero values, and numerical comparisons, independently of the expanded bit lengths of its circuit Hessian and cost. Polynomial dependence on the logarithms of supplied numerical bounds is also sufficient if those logarithms are polynomial in L; polynomial dependence on the numerical bounds themselves is insufficient. A QP theorem retaining Hessian-encoding dependence does not supply this interface.

Maintain shared numerator/positive-denominator integer circuits. In particular,

\[
 (N_1/D_1)/(N_2/D_2)
       =N_1D_2N_2/(D_1N_2^2)
       \quad(N_2\ne0)
\]

keeps the denominator positive. Each arithmetic operation adds constantly many shared gates, and each comparison becomes a constant number of PosSLP tests. Only the actual branch path is constructed; there is no expansion of the decision tree or circuit integers.

The original printed constrained instance gives a singleton KKT projection z=h(p), with fixed-degree conditions, polynomially many variables, and polynomial coefficient bit length. Thus nonzero h(p) has a gap gamma=2^{-2^{a(L)+1}} for an effective polynomial a. Enlarge a to dominate a polynomial bound on log_2 ||grad h|| over the box. O(a(L)) Newton iterations make observable error below gamma/8. Repeated squaring represents gamma by a polynomial-size rational circuit. For an approximation v=h(x_j), the strict PosSLP expressions

\[
 v-\gamma/2,\qquad v+\gamma/2,
       \qquad\gamma^2/4-v^2
\]

decide respectively h(p)>0, h(p)>=0, and h(p)=0. Negation covers the remaining relations. The separation bound concerns the original input, not expanded iterates. The generally irrational p is not a rational-circuit value; only feasible rational approximations are. Testing slack observables supplies the full active mask and hence an implicit exact stationary description on the active affine space.

**The structured-box QP has a short complete proof.** The following derivation strengthens self-containedness; it does not change the published scope or claim novelty for the source algorithm. Let H be rational symmetric positive definite and B its comparison matrix, with B_ii=H_ii and B_ij=-|H_ij| for i!=j. Assume B is positive definite. An SPD matrix with nonpositive off-diagonal entries has nonnegative inverse. To prove this directly, solve Bu=b>=0 and write u=u_+-u_- with disjoint nonnegative parts. If u_- is nonzero, then

\[
 0\le b^{\mathsf T}u_-
    =u_-^{\mathsf T}Bu_+-u_-^{\mathsf T}Bu_-<0,
\]

because the first term is nonpositive and the second is strictly positive. This contradiction shows u>=0. In particular d=B^{-1}1>=0, and every coordinate is strictly positive: if d_i=0, (Bd)_i<=0 contradicts (Bd)_i=1.

Set v=(H+B)d/2. Since Bd=1,

\[
 v_i=H_{ii}d_i+\sum_{j\ne i,\ H_{ij}<0}H_{ij}d_j
     =1+\sum_{j\ne i,\ H_{ij}>0}H_{ij}d_j\ge1.         \tag{B1}
\]

For each nonempty principal set S, the Jacobi map

\[
 (\mathcal J u)_i=
       [v_i-\sum_{j\in S\setminus\{i\}}H_{ij}u_j]/H_{ii}
       \quad(i\in S)
\]

sends [0,d_S] into itself. Its smallest numerator on that box is

\[
 v_i-\sum_{j\in S\setminus\{i\},\ H_{ij}>0}H_{ij}d_j
       =1+\sum_{j\notin S,\ H_{ij}>0}H_{ij}d_j>0,
\]

and its largest numerator is

\[
 v_i-\sum_{j\in S\setminus\{i\},\ H_{ij}<0}H_{ij}d_j
       =H_{ii}d_i+\sum_{j\notin S,\ H_{ij}<0}H_{ij}d_j
       \le H_{ii}d_i.
\]

Also Bd=1 gives

\[
 \sum_{j\ne i}|H_{ij}|d_j=H_{ii}d_i-1<H_{ii}d_i.
\]

Therefore J is a contraction in the d-weighted infinity norm. Its unique fixed point is H_SS^{-1}v_S and belongs to [0,d_S]. This proves the required principal-system condition without appealing to an unproved comparison-matrix lemma. Iteration is used only in this existence proof; the algorithm obtains d and principal-system solutions by rational linear algebra.

For an SPD Hessian with nonpositive off-diagonal entries, simply use v=1. For forest support, root each tree and assign a sign s_j=-sign(H_ij)s_i on every nonzero edge; zero edges can be omitted. The diagonal sign matrix S satisfies B=SHS, so B is positive definite. This also shows that eliminating fixed box coordinates preserves the condition. The comparison-matrix-positive-definite promise itself gives the broader valid box subclass even with cycles.

Here is a complete parametric proof of the at-most-2n QP bound, following the established Pang--Han algorithm. Translate the finite box to 0<=x<=u, with u_i>0 after substituting fixed coordinates. Suppose v>0 and H_SS^{-1}v_S>=0 for every nonempty S. Consider the family

\[
 \min_{0\le x\le u}\ \tfrac12x^{\mathsf T}Hx+(c+\lambda v)^{\mathsf T}x,
       \qquad\lambda\ge0.
\]

Initially x=0 is optimal for lambda0=max(0,max_i(-c_i/v_i)). Track a partition into lower coordinates L, free coordinates F, and upper coordinates U. With x_L=0 and x_U=u_U, define

\[
 a_F=H_{FF}^{-1}(c_F+H_{FU}u_U),\qquad
 b_F=H_{FF}^{-1}v_F,
 \qquad x_F(\lambda)=-a_F-\lambda b_F.
\]

For i outside F, define

\[
 a_i=c_i+H_{iU}u_U-H_{iF}a_F,\qquad
 b_i=v_i-H_{iF}b_F.
\]

Then its gradient is a_i+lambda b_i. Admissibility gives b_F>=0. It also gives b_i>=0 for every i outside F: in the principal system on F union {i}, the i-th solution coordinate is b_i divided by the positive Schur complement of H_FF. This identity includes F empty. Consequently, while lambda decreases, every free coordinate weakly increases, every lower gradient weakly decreases, and every upper gradient weakly decreases. A coordinate already fixed at its upper bound can retain the required nonpositive gradient.

Assume the current point satisfies the box KKT conditions at the current lambda. The next possible events are a lower gradient reaching zero, at lambda=-a_i/b_i for i in L with b_i>0, or a free coordinate reaching its upper bound, at lambda=-(u_i+a_i)/b_i for i in F with b_i>0. Choose the largest of these values and zero. All positive next-event values are at most the current lambda by the current KKT conditions. Zero slopes cannot create an event; their inequalities remain valid. Until the next event, free lower feasibility, free upper feasibility, and all lower and upper KKT signs remain valid.

If the next lambda is positive, move one deterministically selected event coordinate from L to F or from F to U. At that event its value is respectively zero or u_i, and recomputing the free system gives the same current point. Thus KKT conditions persist, even at tied events; process ties one coordinate at a time. The new principal systems remain nonsingular. A coordinate moves only L -> F -> U, so there are at most 2n pivots. If the next lambda is zero, the current affine formulas at zero give a feasible point with all box KKT signs for the original objective. Strong convexity makes it the unique minimizer. With fresh Gaussian elimination at every pivot, the arithmetic-operation count is O(n^4), plus polynomially many sign and ratio comparisons. Ratio denominators are explicitly positive. This proof includes degeneracy and does not require strict inequalities in the principal-system condition.

At each Newton point the comparison matrix, d, v, principal systems, and threshold ratios can therefore be computed from shared rational circuits using polynomially many PosSLP tests. No expanded coefficient height enters the operation count. Forest, Z-matrix, and SPD-comparison-matrix box promises consequently meet the transfer theorem. They do not establish PosSLP-hardness for those structural subclasses; no such hardness was supplied in the examined notes.

**Separable network flows meet the transfer through a different arithmetic algorithm.** For incidence matrix A and rational balances/capacities, P={x:Ax=b,l<=x<=u}. With f=sum_e f_e(x_e), every Taylor model has diagonal positive Hessian and arc cost

\[
 \tfrac12 f_e''(x_e)y_e^2+
       [f_e'(x_e)-f_e''(x_e)x_e]y_e.
\]

The existing [flow source review](../../../research-20261003-arithmetic/constrained-exact/network-flow-review.md) records the required exact strongly polynomial quadratic-flow theorem of Vegh: elementary rational arithmetic and comparisons, coefficient-encoding-independent operation count, and capacity normalization permitting zero-cost auxiliary arcs. Quadratic derivative evaluations, rational linear systems, and the source's parametric search use no extra root or rounding oracle. It is this arithmetic interface, not a polynomial expanded bit-length bound, that lets a Taylor solve return rational circuits.

The source's high artificial linear costs can be chosen without inspecting circuit integer lengths. After the finite-capacity gadget reduction, all original gadget flows lie in printed finite intervals. Bound every quadratic derivative there by a rational circuit C>=1, for example by summing absolute endpoint derivatives and adding one. Let N be the number of gadget nodes. At an original optimum the derivative residual graph has no negative cycle. Add a temporary source with zero-cost arcs and choose shortest-path potentials pi; a shortest simple path has at most N-1 arcs, so -(N-1)C<=pi_i<=0. Add a new node with zero potential and artificial arcs in both directions of cost M=NC+1. Every artificial reduced cost is strictly positive. The original optimum extended by zero artificial flow satisfies all convex-flow KKT conditions in the augmented graph. Convexity then forces zero artificial flow at every augmented optimum: any positive artificial flow gives a strictly positive first-order contribution. Thus the reduction preserves the optimizer and uses only polynomially many circuit operations. The unknown optimum and potentials are used to prove that M works, not computed by the normalization routine.

The graph, rank, active bounds, parallel arcs, balance redundancy, and zero multipliers impose no additional parameter restriction. A fixed-degree explicit observable may couple many arcs; only the objective must be separable for the Taylor-flow solver. Disjoint union of two flow instances compares optimal values by the sum objective and difference observable. Global curvature of a quartic arc cost is checkable from its quadratic second derivative: for a nonconstant quadratic a t^2+b t+c, nonnegativity on the line requires a>0 and 4ac-b^2>=0; a constant needs c>=0, and a nonconstant linear polynomial is invalid. Apply this to f_e''-mu. This is a rational polynomial-time certificate check specific to the univariate case.

If f(p)<rho, the final approximation for h=f-rho can be chosen with exactly feasible rational-circuit x satisfying f(x)<rho. Its circuit has polynomial size and is computable with PosSLP, even when its expanded rational coordinates are large. Equality attained only at an irrational optimum gives no rational exact optimizer witness. The flow theorem is a Turing reduction because the QP execution branches depend on oracle answers.

**Infinite endpoints are correctly removed by an inactive finite truncation.** For a nonempty rational box, clip zero to its finite endpoints to obtain a polynomial-bit feasible q. For a nonempty flow polyhedron, ordinary rational LP supplies a polynomial-bit feasible flow q even if some endpoints are infinite. Coercivity supplies p and f(p)<=f(q). Strong convexity gives

\[
 0\ge f(p)-f(q)
   \ge-\|\nabla f(q)\|\|p-q\|
          +\frac\mu2\|p-q\|^2,
 \qquad\|p-q\|\le2\|\nabla f(q)\|/\mu.
\]

Set R=1+2||grad f(q)||_1/mu and intersect each original interval with [q_i-R,q_i+R]. The new endpoints have polynomial encoding length, preserve the box or flow structure, and retain p strictly inside every added bound. Thus original active labels are unchanged. This uses global strong convexity, not a curvature promise only on a finite initial region. The same finite-truncation reasoning could be applied to any transfer setting whose exact QP interface survives intersection with the added box; the structured results explicitly do survive it.

**The unrestricted boundary must remain explicit.** The convergence estimate above does not solve arbitrary circuit-Hessian QPs. Generic convex-QP polynomial bit complexity charges expanded input coefficients, which may be exponentially long after Newton refinement. The recorded Granot--Skorin-Kapov scope removes linear-cost and right-hand-side encoding dependence but retains Hessian-encoding dependence. It therefore cannot be imported as the missing general subroutine. The circuit-objective LP used for the unambiguous verifier also does not solve a QP with a varying circuit Hessian.

Likewise, ordinary weak optimization with accuracy polynomial in log(1/epsilon) is exponential when epsilon=2^{-2^{a(L)}}. Encoding epsilon as a circuit does not shorten its iteration count. A squared-hinge penalty already fails a naive explicit-coefficient reduction in one dimension: minimizing (x+1)^2/2+(lambda/2)max(0,-x)^2 over the line gives p_lambda=-1/(1+lambda), while the constrained minimizer for x>=0 is zero. Distance gamma requires lambda>=gamma^{-1}-1. Printing lambda at a general singleton gap can require exponentially many bits, and the hinge is not a polynomial. A short circuit coefficient does not automatically satisfy the unconstrained theorem's explicit-polynomial and polynomial-bit warm-start interface. These examples invalidate those proof routes; they are not lower bounds separating the general problem from P^PosSLP.

The manuscript can therefore make each positive result above a proved theorem while retaining the unrestricted deterministic question as a stated open boundary. It should not infer a deterministic algorithm from UP intersect coUP, from a small final active support, from a bit-polynomial QP theorem, or from the ordinary candidate list alone.

Concrete amendments for the author are limited. Include the exact-feasible-point contract, use min(1,epsilon) uniformly in approximation calls, distinguish the sharper unrestricted candidate parameter function from the general mixed a(t), include the every-basis argument in the violator proof, charge total candidate encoding rather than only count, and carry rank 2r or nonlinear dimension 2k through pairwise products. In the nonlinear output, supply a reduced curvature modulus if one is subsequently needed. The two direct box-QP derivations above can replace a bare appeal to the source's admissible-vector assertion and can supply a full proof of the pivot bound. Preserve the distinction between implicit algebraic optimizers and rational-circuit feasible iterates, and between nonadaptive batches, adaptive Turing reductions, and single many-one instances.

Verification in this audit consists of source-note reads and analytic reconstruction. The only new executable check was an inline `python - <<'PY'` document-check script scoped to this report. It passed all 14 local links, trailing whitespace, final newline, display-math delimiter counts, and control characters. No mathematical experiment, prior checker rerun, project-wide verification, or CI inspection was performed.
