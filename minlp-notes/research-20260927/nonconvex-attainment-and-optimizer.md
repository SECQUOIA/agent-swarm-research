# Attainment and exact optimizers with few quadratic Hessian directions

Date: 2026-09-28. Status: proof, fresh adversarial review, separate algebra
and inactive-box reviews, and a prior-work audit completed; no gap was found.
Novelty is not established.

An attained optimum has a small algebraic optimizer even when the feasible
set is unbounded. More precisely, a global optimizer of minimum Euclidean
norm has a common algebraic description whose size depends exponentially
on the span of the constraint Hessians, rather than on the ambient dimension.
The proof uses two ordered limits inside an unknown box whose boundary
becomes inactive. The box never enters the algebraic coefficient bounds.
A resulting explicit rational radius permits an exact attainment test using
only rational optimization inputs.

The qualitative fixed-parameter complexity consequences are not presented
as independent new algorithmic mechanisms. Once the previously established
finite-infimum bound is available, classical quadratic-map sampling also
gives an optimizer certificate with a weaker parameter dependence; Section
9 explains that comparison. The sharper bound and minimum-norm selection
are the focus of the proof below.

## 1. Statements

Let

\[
 S=\{x\in\mathbb R^n:Ax\le b,\ Ex=e,\ q_i(x)\le0
                                      \ (1\le i\le m)\}
\]

have rational data, with quadratic polynomials \(q_i\), and let
\(q_0\) be an arbitrary rational quadratic objective. Write

\[
 h=\dim_{\mathbb Q}\operatorname{span}
             \{\nabla^2q_i:1\le i\le m\}.
\]

There are no convexity, boundedness, or constraint-qualification assumptions.
All inequalities are weak. The objective Hessian is excluded from \(h\).
Let \(N\ge2\) be the explicit binary input length, including \(q_0\).

**Minimum-norm optimizer theorem.** Suppose \(q_0\) attains its global
minimum \(\theta\) on nonempty \(S\). There is a global optimizer
\(x^*\) of minimum Euclidean norm for which:

- every coordinate has an integer annihilator of degree and coefficient
  bit length \(N^{O(h+1)}\);
- the common field \(\mathbb Q(x^*)\) has degree
  \(N^{O(h+1)}\);
- the point has a rational univariate representation of total binary
  length \(N^{O(h+1)}\).

The common-field claim is a separate part of the proof; it does not follow
by multiplying the coordinate degree bounds. If the global optimal set is
convex, its minimum-norm point is unique, and the theorem describes that
canonical point.

Consequently an effectively computable radius

\[
 B=2^{N^{O(h+1)}}                                      \tag{1}
\]

contains some optimizer whenever the minimum is attained. For fixed \(h\),
there is an \(\mathrm{FP}^{\mathrm{NP}}\) algorithm which classifies the
problem as infeasible, unbounded below, having an unattained finite infimum,
or having an attained finite minimum. It returns the exact finite value;
in the attained case it also returns an exact algebraic optimizer, which
can be required to have minimum norm.
This is not an algorithm without an oracle or a short certificate of global
optimality.

The degree bounds can be separated from coefficient size. If \(S_0\ge2\)
bounds structural size and \(\tau_0\ge1\) bounds each rational coefficient's
numerator and denominator bit lengths, then an effective absolute constant
\(C\) gives coordinate and common-field degrees at most
\(S_0^{C(h+1)}\), and coordinate annihilator coefficient bits and total
representation length at most
\((\tau_0+1)S_0^{C(h+1)}\), after increasing \(C\). Structural size
counts variables, rows, scalar coefficient positions, and index bit lengths.

## 2. Regularization and an unknown compact box

The global optimal set \(S\cap\{q_0=\theta\}\) is nonempty and closed.
A norm-minimizing sequence can be restricted to a fixed closed ball by
comparison with any one optimizer. Compactness then gives an optimizer
\(\bar x\) of minimum norm. Put \(c=\|\bar x\|\).
Neither \(\bar x\), \(c\), nor \(\theta\) is inserted into the
coefficients of the proof's auxiliary systems.

Use the rational lift from the
[nonconvex certificate note](nonconvex-hessian-span-frontier.md): choose a
basis \(B_1,\ldots,B_h\) for the native Hessian span and write

\[
 w=(x,y)\in P,\qquad
 F_j(w)=\tfrac12 x^TB_jx-y_j=0\quad(1\le j\le h),      \tag{2}
\]

where \(P\) is a rational polyhedron incorporating all original rows.
The lift has polynomial structural size and coefficient bits linear in
\(\tau_0\) times a polynomial in \(S_0\). Let \(\bar w\) be the
unique lift of \(\bar x\).

For \(\varepsilon>0\), the objective
\(q_0(x)+\varepsilon\|x\|^2\) is coercive **on \(S\)** because
\(q_0(x)\ge\theta\) there. Since \(S\) is nonempty and closed, it
has a global minimizer on \(S\). For every such minimizer \(x_\varepsilon\),
comparison with \(\bar x\) gives

\[
 \theta+\varepsilon\|x_\varepsilon\|^2
 \le q_0(x_\varepsilon)+\varepsilon\|x_\varepsilon\|^2
 \le\theta+\varepsilon c^2.
\]

Thus all these minimizers, for every positive \(\varepsilon\), satisfy
\(\|x_\varepsilon\|\le c\). Their exact lifts have
\(y_j=\tfrac12x_\varepsilon^TB_jx_\varepsilon\), so they lie in one
fixed compact set in the lifted space. Choose an unknown integer \(R\)
strictly larger than the absolute values of all coordinates in that compact
set, and strictly larger than those of \(\bar w\). Its existence is
enough; no encoding bound for \(R\) is assumed or used.

Define

\[
 P_R=P\cap[-R,R]^{n+h},\qquad
 T_R=\{w\in P_R:F_j(w)=0\ (1\le j\le h)\}.            \tag{3}
\]

Every global minimizer of

\[
 q_0(x)+\varepsilon\|x\|^2                            \tag{4}
\]

on the original set has its lift strictly inside this box. Conversely,
every minimizer of (4) on \(T_R\) is a global minimizer on the original
set, since the two optimal values coincide. Every such boxed minimizer
therefore satisfies

\[
 \|x_\varepsilon\|\le c,\qquad
 0\le q_0(x_\varepsilon)-\theta\le\varepsilon c^2.      \tag{5}
\]

In particular, every limit as \(\varepsilon\downarrow0\) is a global
optimizer with norm at most \(c\), hence exactly \(c\). This selection
argument uses the global lower bound \(q_0\ge\theta\) on \(S\), not
convexity or uniqueness. Coercivity outside \(S\) is not asserted.

## 3. Generic perturbations in two formal parameters

Choose integer-coefficient quadratic polynomials \(P_0,P_1,\ldots,P_h\)
in \(w\). For fixed \(\varepsilon>0\) and small \(\eta>0\), consider

\[
 \begin{split}
 \min_{w\in P_R}\quad &
 r_{\varepsilon,\eta}(w)
       =q_0(x)+\varepsilon\|x\|^2+\eta P_0(w),\\
 \text{subject to}\quad &
 |F_j(w)+\eta^2P_j(w)|\le\eta\quad(1\le j\le h).
 \end{split}                                                   \tag{6}
\]

Apply the genericity lemma in Section 4 of the nonconvex certificate note to
the affine charts obtained from active rows of the **original** polyhedron
\(P\). An active subset either defines an empty affine space or has a
rational chart

\[
 w=a+Vu,                                                \tag{7}
\]

with \(V\) of full column rank and coefficient bits
\((\tau_0+1)S_0^{O(1)}\). The box rows are deliberately excluded.
Section 4 proves that they are inactive at the selected points.

For each fixed \(\varepsilon\) and \(\eta\ne0\), restricting the
ambient perturbation coefficients to a positive-dimensional chart is
surjective onto arbitrary objective and selected constraint quadratics in
\(u\). The term \(\varepsilon\|x\|^2\) is a fixed additive term for
this assertion. Every bad-set polynomial therefore remains a nonzero
polynomial in the perturbation coefficients and formal parameters
\((\varepsilon,\eta)\).

For each chart and oriented active subset, choose one nonzero coefficient
in the expansion in both formal parameters. Avoiding the product of these
coefficients ensures that no bad polynomial becomes identically zero after
fixing the perturbations. Its degree is at most
\(2^{\operatorname{poly}(S_0)}\). The finite integer-grid argument gives
one choice of all \(P_j\) with coefficient bits \(S_0^{O(1)}\), independent
of \(\tau_0\), the unknown \(R\), and both parameters.

After this choice, each bad polynomial \(H(\varepsilon,\eta)\) is
nonzero. The values of \(\varepsilon\) for which it is identically zero
in \(\eta\) form a finite set: they are roots of any one nonzero
coefficient polynomial in \(\varepsilon\). Discard their finite union
over all charts and active subsets. For each remaining positive
\(\varepsilon\), all sufficiently small positive \(\eta\) avoid the
remaining finitely many bad roots. The genericity lemma then makes active
nonlinear gradients independent, the multiplier Hessian invertible, and
the full bordered KKT matrix invertible. The last condition is necessary
even when the first two hold.

There are arbitrarily small admissible positive \(\varepsilon\), each
with an admissible positive \(\eta\)-tail. No uniform smallness threshold
in \(\varepsilon\) is asserted. At most one orientation of a band can
be active, so the active nonlinear count is at most \(h\).

## 4. The box disappears before the algebraic argument

Fix an admissible \(\varepsilon>0\). An exact optimizer of (4) on
\(T_R\) remains feasible in (6) for every sufficiently small positive
\(\eta\). The perturbed feasible set is therefore nonempty and compact,
so its global minimum exists. Every convergent subsequence of perturbed
minimizers as \(\eta\downarrow0\) satisfies (2). Uniform convergence of
the objective on the fixed box, and comparison with an exact optimizer,
show that its limit minimizes (4) on \(T_R\).

By Section 2, all these limits lie strictly inside the box. Consequently
**every** perturbed minimizer is strictly inside the box for every
sufficiently small positive \(\eta\), at this fixed \(\varepsilon\).
Otherwise a sequence of boundary minimizers with \(\eta\downarrow0\)
would have a cluster point on the closed box boundary, contradicting the
previous paragraph. Thus all box rows are eventually inactive.

Choose perturbed minimizers along an admissible \(\eta\)-sequence and a
convergent subsequence. Retain a further subsequence with one constant
active affine chart from the original \(P\) and one constant oriented
nonlinear active subset. This does not change the limit. Choose admissible
\(\varepsilon\downarrow0\). The inner limiting points obey (5) and their
lifts are uniformly bounded. Select a convergent subsequence and, by the
finite pigeonhole principle, one constant chart/subset for all retained
inner sequences. There are therefore parameters
\(\varepsilon_\nu\downarrow0\), and for each \(\nu\) parameters
\(\eta_{\nu,\mu}\downarrow0\), with selected perturbed minimizers obeying

\[
 w_{\nu,\mu}\longrightarrow w_\nu\quad(\mu\to\infty),
 \qquad w_\nu\longrightarrow w^*\quad(\nu\to\infty).   \tag{8}
\]

The first limit is at fixed \(\nu\). The original coordinates \(x^*\)
of \(w^*\) form a global minimum-norm optimizer by (5). All coordinate
outputs use these same nested subsequences and this same point. The initial
perturbed minimizers need not satisfy (5); that estimate is used only after
the inner limit.

If the selected affine chart has dimension zero, every selected point is
its one rational point \(a\), of polynomial coefficient size, and the
claim is immediate. Otherwise let its dimension be \(d>0\). The unknown
radius has now served its entire purpose. It occurs in no selected affine
chart, active quadratic, stationarity equation, or output formula. No
limit in \(R\) or upper bound on its encoding length is needed.

## 5. Eliminate only the active multipliers

At a selected perturbed minimizer, restrict all active polyhedral rows to
(7). The other polyhedral inequalities, including every box row, are strictly
slack locally. Independent active nonlinear gradients therefore give ordinary
KKT stationarity with objective multiplier one. Let \(J\) be the fixed
oriented active subset, of size \(s\le h\), and write its multiplier
Hessian as \(M(\varepsilon,\eta,\lambda)\). It is invertible at every
selected root. Set \(\Delta=\det M\), and let \(p\) be the adjugate
numerator in stationarity, so \(u=p/\Delta\).

Substitution in the \(s\) active quadratic equations and multiplication
by \(\Delta^2\) give

\[
 G_i(\varepsilon,\eta,\lambda)=0\quad(1\le i\le s).    \tag{9}
\]

At a selected root, their multiplier Jacobian is
\(-\Delta^2 L M^{-1}L^T\), where \(L\) is the active-gradient matrix.
It is nonsingular by the Schur complement of the full bordered KKT matrix.
No positive-definiteness condition is needed here.

Every coordinate of \(w=a+Vp/\Delta\), and every rational linear
combination of those coordinates, is a rational output \(B/A\) of this
same system, with \(A\ne0\) at the selected roots. The squared norm
\(\|x\|^2\) is also such an output. After clearing constant rational
denominators, these expressions belong to
\(\mathbb Z[\varepsilon,\eta,\lambda]\). For coordinates and the squared
norm, their degree in the multipliers is \(a=O(d+1)\), their degree in
both parameters is \(S_0^{O(1)}\), and the logarithm of their coefficient
norm is \((\tau_0+1)S_0^{O(1)}\). The same degree bound holds for every
fixed rational linear combination; its coefficient size may depend on that
combination. No numerical \(\log R\), \(\log(1/\varepsilon)\), or
\(\log(1/\eta)\) enters these formal coefficient bounds.

## 6. Two ordered coefficient extractions

The [finite-quotient lemma](explicit-span-separation.md) applies unchanged
over the coefficient ring \(\mathbb Z[\varepsilon,\eta]\). Suppose the
equations and output in (9) have multiplier degree at most \(a\ge1\) and
coefficient norm at most \(2^\tau\). Set

\[
 D=a+1,\quad L_0=D^s,\quad T=a(s+1),\quad
 K=L_0[\tau(T+1)+2+\lceil\log_2L_0\rceil].             \tag{10}
\]

The deformation \(G_i+\delta\lambda_i^D\) gives a quotient of dimension
\(L_0\). The multiplication determinant, followed by extraction of its
lowest \(\zeta\) and then lowest \(\delta\) coefficients, gives a
nonzero polynomial

\[
 Q(\varepsilon,\eta,t)\in\mathbb Z[\varepsilon,\eta,t] \tag{11}
\]

vanishing at every selected rational output. Its degree in \(t\) is at
most \(L_0\), and \(\|Q\|_1\le2^K\). The selected-root nonsingularity
and nonvanishing denominator are exactly the conditions required by that
lemma's implicit-function and factor arguments. Possible vanishing of an
extracted coefficient after specialization is allowed: its relation then
holds identically at that specialization. The coefficient norm is taken
in all formal variables, so adjoining the second parameter does not change
the estimate.

Let \(\eta^r V(\varepsilon,t)\) be the lowest nonzero \(\eta\)-term in
(11). At fixed \(\nu\), divide the output relation by \(\eta^r\) and
take the inner limit in (8), giving \(V(\varepsilon_\nu,v_\nu)=0\).
Let \(\varepsilon^j P(t)\) be the lowest nonzero \(\varepsilon\)-term
in \(V\). Divide by \(\varepsilon^j\) and take the finite outer output
limit, giving \(P(v^*)=0\). Since both extracted coefficient polynomials
are nonzero by definition and extraction cannot increase coefficient norm
or output degree,

\[
 \deg P\le(a+1)^s,\qquad \log_2\|P\|_1\le K.          \tag{12}
\]

This is applied separately to coordinates and linear forms, always using
the same roots and nested point limits (8). It yields coordinate annihilators
with degree \(S_0^{O(h+1)}\) and coefficient bits
\((\tau_0+1)S_0^{O(h+1)}\). The same bound applies to the minimum squared
norm \(\rho=\|x^*\|^2\). No interchange or diagonal limit is used.

## 7. A common field, a short representation, and a radius

The coordinates of \(w^*\) are algebraic by (12), so they generate a
finite extension of \(\mathbb Q\). Every rational linear combination of
them has degree at most the same \(L_0\), independently of the sizes of
its rational coefficients. The primitive element theorem supplies such a
linear combination generating the entire field. Therefore

\[
 [\mathbb Q(w^*):\mathbb Q]\le L_0=S_0^{O(h+1)}.        \tag{13}
\]

For encoding size, choose a primitive integer linear combination with
coefficients in \(\{0,\ldots,L_0(L_0-1)/2\}\). The elementary
embedding-hyperplane argument in Section 7 of the nonconvex certificate
note proves this bound. Applying (12) to this bounded-coefficient combination
gives a primitive generator of coefficient height
\((\tau_0+1)S_0^{O(h+1)}\). The trace-matrix construction in that same
section expresses every coordinate as a rational polynomial in the
generator with this same form of bound. Root separation gives an isolating
interval of this size. Factoring annihilators, clearing algebraic-integer
scales, and solving the trace equations only multiply height bounds by
polynomials in the algebraic degree. The dependence on \(\tau_0+1\)
therefore remains linear.

The resulting representation uses one squarefree integer polynomial, a
rational interval isolating its intended real root, and rational coordinate
polynomials. Its total length is
\((\tau_0+1)S_0^{O(h+1)}\). The common field for the original \(x^*\)
is a subfield and obeys the same degree bound.

If \(H=(\tau_0+1)S_0^{C(h+1)}\) bounds coordinate annihilator coefficient
bits, Cauchy's root bound gives \(|x_i^*|<2^{H+2}\). Thus
\(B=2^{H+2}\) is a computable radius containing an optimizer whenever one
exists. It does not claim that all optimizers lie in the box, or that any
optimizer exists when the finite infimum is unattained.

Appending this box adds only affine rows. Its coefficient bits are
\((\tau_0+1)S_0^{O(h+1)}\), while structural size stays polynomial in
\(S_0\). Applying the coefficient-sensitive bounds again preserves the
form \((\tau_0+1)S_0^{O(h+1)}\); treating the enlarged total input length
as the new structural size would give an unnecessary quadratic exponent
in \(h\).

## 8. Exact attainment and optimizer recovery with an NP oracle

First use the [finite-infimum algorithm](nonconvex-finite-infimum.md) to
classify infeasibility and unboundedness, and otherwise obtain the exact
finite infimum \(\theta\) as its integer minimal polynomial \(f_\theta\)
and rational isolating interval \((a,b)\). Root isolation can ensure that
neither endpoint is a root.

Construct the radius \(B\) above and consider \(S_B=S\cap[-B,B]^n\).
If this set is empty, the infimum is unattained, since any attained optimum
would have a representative inside the box. Otherwise compute its exact
minimum \(\theta_B\) with the same algorithm. The set \(S_B\) is compact,
so

\[
 \theta\text{ is attained on }S
       \quad\Longleftrightarrow\quad \theta_B=\theta. \tag{14}
\]

The forward implication is the radius theorem; the reverse implication is
compact attainment in \(S_B\). Equality of two represented real algebraic
numbers can be decided in polynomial time by polynomial gcd and root
isolation. Every optimization oracle input here remains rational.

For a general NP oracle, attainment has an even simpler test. Let \(L\)
be the proved polynomial bound, for fixed \(h\), on an attained optimizer's
representation length. Use the following
polynomial-time certificate verifier: parse a common univariate
representation of a real point \(x\); verify its isolating interval and all
original feasibility inequalities; compute the algebraic element
\(\gamma=q_0(x)\) in that representation; and check

\[
 f_\theta(\gamma)=0,\qquad a<\gamma<b.                \tag{15}
\]

All these tests are exact univariate arithmetic and sign determination.
Condition (15) is equivalent to \(q_0(x)=\theta\). It does not require a
compositum with a separately represented \(\theta\). The verifier also
checks \(x\in[-B,B]^n\) if the box is included in the desired certificate.
No global optimality assertion is verified from the point alone: the exact
value \(\theta\) is already known from the optimization algorithm.

One NP query asks whether this verifier has any accepting certificate of
length at most \(L\). The optimizer bound makes the answer yes exactly
when \(\theta\) is attained. Thus recomputing a boxed minimum is useful
when restricted to rational optimization oracles, but unnecessary for the
general \(\mathrm{FP}^{\mathrm{NP}}\) claim.

In the attained case, there is such an accepting certificate. Pad a
self-delimiting encoding to a fixed polynomial length. The language asking
whether an input prefix can be extended to an accepting certificate is in
NP. Query this language for each next bit, taking zero whenever a valid
extension exists and one otherwise. After polynomially many queries, the
complete accepting certificate is an exact optimizer. This standard search
reduction does not require that a chosen geometric coordinate selection
be unique, and it need not return the minimum-norm optimizer used to prove
the radius bound.

To recover a minimum-norm optimizer, let \(\rho\) be the least squared
norm among global optimizers. Section 6 gives degree and coefficient bounds
of the same form for \(\rho\). Consider the NP query asking for an accepting
certificate of length at most the universal minimum-norm representation
bound, with the additional rational test \(\|x\|^2\le t\). For the already
computed valid \(\theta\), this query is yes exactly when \(t\ge\rho\):
no global optimizer has a smaller norm, while one minimum-norm optimizer
has the bounded certificate independently of \(t\).

Bisection on \([0,nB^2]\), followed by the same algebraic-recognition
algorithm used for \(\theta\), recovers \(\rho\) exactly. The endpoints
bound \(\rho\); an infeasible lower endpoint is not required for the
interval-containment invariant. Finally perform certificate prefix search
with both equalities \(q_0(x)=\theta\) and \(\|x\|^2=\rho\), testing each
via its minimal polynomial and isolating interval in the candidate point's
representation. This returns a minimum-norm optimizer. In a convex optimal
set it returns the unique such point.

All deterministic operations and query lengths are polynomial for fixed
\(h\). The same bounds, with the coefficient-sensitive accounting from
Section 7, prevent repeated radius and value calls from creating a quadratic
exponent in the structural parameter. The statement is membership in
\(\mathrm{FP}^{\mathrm{NP}}\), not a practical bound on NP-oracle work.

## 9. Prior work and what this proof adds

The primitive-element theorem, polynomial sign verification, certificate
prefix search, and the use of a radius to test attainment are established
tools. The proof above relies on the previously reviewed finite-quotient
and genericity arguments. Its additional step is the minimum-norm selection
in (5), removal of the inactive unknown box, and ordered extraction first
in \(\eta\) and then in \(\varepsilon\). These limits are not interchanged.

There is a shorter route to a weaker optimizer certificate after the finite
value \(\theta\) has been encoded. Lift \(q_0(x)\) as an additional
quadratic coordinate \(z\), impose the affine interval \(a\le z\le b\),
and require \(f_\theta(z)=0\), together with the original lift equations.
Write this as the zero set of a polynomial composed with \(h+2\) quadratic
or affine functions: the \(h\) native equations, the equation
\(q_0(x)-z\), and \(z\) itself. Its outer polynomial is the sum of the
squares of the equation outputs and \(f_\theta(z)^2\). The interval's
endpoints are not roots, so its weak inequalities still select exactly
\(\theta\).

Choose a minimum-dimensional face of the resulting rational polyhedron
meeting that zero set. The connected-component argument from the
[feasibility prior audit](nonconvex-hessian-span-prior-audit.md) places a
whole component inside that face. Grigoriev--Pasechnik's
[Theorem 1.2](https://arxiv.org/pdf/cs/0403008v3) then samples an optimizer.
Its stated dependence on the degree of the outer polynomial directly gives
bounds of the form \(N^{O((h+1)^2)}\), already enough for the qualitative
fixed-\(h\) complexity consequences after the finite-value theorem.
This route does not select a global minimum-norm optimizer.

The same source's arithmetic theorem over the ordered coefficient field
\(\mathbb Q(\theta)\) already gives an optimizer with absolute field degree
\(N^{O(h+1)}\): impose \(q_0=\theta\), use the same face argument, and
multiply the degree over that field by \([\mathbb Q(\theta):\mathbb Q]\).
Its stated bit bound is specifically for integer coefficients, so the sharp
number-field height extension requires separate justification. Thus an
arbitrary optimizer's degree bound alone is also not a new contribution.
The [completed prior audit](nonconvex-attainment-prior-audit.md) records
these distinctions and the remaining coefficient-height obligation.

Grigoriev--Pasechnik's Theorem 1.5 announces exact optimization and attainment
classification on quadratic-map zero sets, but defers its proof to a
continuation. A current primary comparison is Kamminga--Rudolph,
[*The Pure-State Consistency of Local Density Matrices Problem*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.83/LIPIcs.ITCS.2026.83.pdf),
ITCS 2026, Section 1.1.4 and Theorem 1.15. Their proved optimization theorem
assumes a bounded quadratic-map zero set and returns approximations to the
value and an optimizer; they explicitly report that GP's announced
unbounded optimization proof was unavailable to their knowledge. This is
stronger evidence than an unsuccessful search, but it does not prove that
no equivalent result exists. Their small quadratic-map dimension does not
permit arbitrary affine rows at no parameter cost.

For a convex optimal set, uniqueness turns the encoding theorem into a
bound on its canonical minimum-norm point. This is useful for exact recovery
from deterministic convex decision oracles. Such recovery, including any
SOCP specialization, needs its own oracle and arithmetic analysis; it is
not asserted by the NP search argument alone.

## 10. Attainment remains hard with one nonlinear constraint

A direct reduction gives strong NP-hardness even when \(h=1\), there is
only one quadratic inequality, the objective is linear, and the finite
infimum is supplied as the known number zero. This is a parameter refinement
of the established hardness phenomenon, not a priority claim.

Given a 3SAT instance, introduce \(x\in[0,1]^n\) and \(t,y\ge0\). For
each clause impose its affine literal-sum inequality \(L_C(x)\ge1\).
Minimize \(t\) subject also to the single quadratic inequality

\[
 \sum_{i=1}^n x_i(1-x_i)-ty\le0.                       \tag{16}
\]

For every \(t>0\), the choice \(x_i=1/2\), \(y=n/(4t)\) is feasible:
each three-literal sum is \(3/2\), and (16) holds with equality. Hence
every constructed problem is feasible with infimum zero. At \(t=0\),
every term \(x_i(1-x_i)\) is nonnegative, so (16) forces every \(x_i\)
to be Boolean. The clause rows then express satisfiability. Conversely a
satisfying Boolean assignment with \(t=y=0\) attains the infimum.

All coefficient magnitudes are bounded by an absolute constant, and the
single native Hessian is nonzero, so its span is exactly one. This proves
strong NP-hardness on the promised known-zero subclass. That subclass is
also in NP: append \(t\le0\) and use the fixed-span feasibility certificate.
No exact-value oracle is needed for this promised comparison.

Ahmadi--Zhang's
[*On the Complexity of Testing Attainment of the Optimal Value in Nonlinear
Optimization*](https://optimization-online.org/wp-content/uploads/2018/03/6536.pdf),
Theorem 2.2, already proves strong NP-hardness for a linear objective with
quadratic constraints, using a different reduction with many quadratic
rows. The reduction above isolates the one-quadratic-row boundary. The
prior audit records the source comparison and independent checks.

## 11. Verification status and limitations

The completed [fresh adversarial review](nonconvex-attainment-review.md)
checks genericity, the norm selection, common-field bounds, coefficient
size, the attainment and minimum-norm recovery reductions, and the hardness
example. Its [separate algebra review](nonconvex-attainment-algebra-review.md)
checks the ordered coefficient extractions and common-field argument. A
fresh additional reviewer independently attacked the inactive unknown-box
step. Two agents working on the SOCP application independently reread the
replacement proof. The [prior audit](nonconvex-attainment-prior-audit.md)
records primary sources and the distinction between established consequences
and the sharper argument. Positive reviews are evidence, not a guarantee.

The original draft used a third, outer box-radius limit. The valid algebra
for that route is recorded in the separate algebra review, but the simpler
inactive-box proof above makes it unnecessary. The finite-infimum note's
separate leading-radius extraction lemma remains valid independently.

The reviewer ran exact SymPy checks of attained and unattained hyperbola
examples and independently checked the one-quadratic SAT reduction. These
checks test the examples and do not establish the general theorem. The
author ran targeted formatting and local-link checks for this note, plus
`git diff --check -- research-20260927/nonconvex-attainment-and-optimizer.md`.
No Lean formalization, project-wide checks, or CI inspection was performed.

The theorem assumes attainment only for its optimizer bound; it does not
infer attainment from finite infimum. For example, the closed quadratic
system \(xy\ge1\), \(x\ge0\), has unattained infimum zero for objective
\(x\). Nor does the theorem imply rational optimizers: \(x^2=2\), written
as two weak inequalities with Hessian span one, has only irrational feasible
points. Unbounded integer variables are outside the theorem.

No computational speedup or global-optimality certificate is established.
The bounds identify exact information that exists and what a decision oracle
can recover. Useful solver implementations would still need tractable ways
to exploit the small Hessian span and avoid the generic worst-case constants.
