# Prior-art audit for exact SOCP feasibility at fixed Hessian span

Date: 2026-09-27; updated 2026-09-28. This is an independent source and consequence audit, not a
proof review of the candidate
[nonconvex Hessian-span theorem](nonconvex-hessian-span-frontier.md).

The most important finding is a limitation on novelty: **all rational SOC
systems with Hessian span at most one have exact polynomial-time feasibility
and polynomial rational lifts preserving boxed integer projections as
consequences of older results.** The one-cone case has a particularly short
reduction to classical exact convex QP. Explicit reductions appear below.
This audit did not locate sources stating these corollaries verbatim, so
the reductions are identified as inferences, not attributed as named theorems.

For an arbitrary fixed number of SOC constraints, the inspected direct
cone-complexity theorem retains an exponential bound. The search did not
identify a stronger theorem covering arbitrary affine rows and unbounded cone
dimensions. That is an unresolved literature comparison, not evidence of
priority. Moreover, the feasible-witness and radius bound already follows
from Grigoriev–Pasechnik through an elementary minimum-face argument.
The remaining candidate contribution is the bounded-value/positive-gap
precision bound at larger fixed Hessian span and its conic decision and
integer-projection consequences.

## Parameter and comparison class

The candidate input consists of rational affine rows and constraints

\[
 \|A_iw+b_i\|_2\le c_i^Tw+d_i.
\]

The squared polynomial is
\(q_i(w)=\|A_iw+b_i\|_2^2-(c_i^Tw+d_i)^2\). Its Hessian need not be
positive semidefinite. The sign row \(c_i^Tw+d_i\ge0\) is essential.
The parameter is the rational linear-span dimension of these Hessian
matrices, or their continuous-variable blocks when \(w=(z,x)\) and the
integer vector \(z\) is boxed. It is not matrix rank, range-span dimension,
cone dimension, or the number of components of a full quadratic map.

With \(k\) native SOC constraints, \(h\le k\). Thus the proposed result
includes fixed cone count and allows the native cone count to grow at fixed
\(h\). This is a strict relaxation of the *native input parameter*. It
does not establish that such an input has no alternative formulation with
fewer cones. Repeated constraints, for example, are not evidence of a
representational separation.

## Direct cone-complexity results

Blanco, Magron, and Martínez-Antón, *On the complexity of p-order cone
programs*, Journal of Complexity 91 (2025), 101979, define a single-cone
problem with \(m\) affine inequalities and cone dimension \(n+1\).
Their Theorem 4.3 gives

\[
 m\min\{m,n\}^{O(\min\{m,n\})}
\]

arithmetic operations on
\(\tau\min\{m,n\}^{O(\min\{m,n\})}\)-bit numbers. For \(d\)
independent cone blocks, Theorem 5.2 gives

\[
 m[\min\{m,n\}+d]^{O(\min\{n+d,md^2\})},
\]

with the corresponding coefficient-bit bound. Here \(n\) is the total
dimension of the norm-vector blocks. Neither bound becomes polynomial
merely by fixing \(d\) while \(m,n\) grow. Affine SOC maps can be
converted to independent cone blocks by adding linking equations, counted
among the affine rows. These are valid upper bounds, not hardness results
or a claim that better algorithms are impossible. The elementary one-cone
reduction below demonstrates why their exponential single-cone bound cannot
support a one-cone novelty claim.
[Inspected primary version, §§4.1 and 5, arXiv v2](https://arxiv.org/html/2501.09828v2),
[publication](https://doi.org/10.1016/j.jco.2025.101979).

## One cone reduces to exact convex QP

The established ingredient is polynomial-time exact solution of rational
convex quadratic programming over a rational polyhedron. The classical
source is Kozlov, Tarasov, and Khachiyan, *The polynomial solvability of
convex quadratic programming*, USSR Computational Mathematics and
Mathematical Physics 20(5) (1980), 223–228.
The original Russian article, p. 1320, explicitly defines exact solution
as deciding linear feasibility and boundedness, then finding the exact
rational optimal value and an optimizer. It states polynomial Turing
complexity in binary input length. Pages 1321 and 1323 give the rational
size bounds and optimizer-recovery step, respectively.
[Inspected primary full text](https://www.mathnet.ru/php/getFT.phtml?jrnid=zvmmf&option_lang=eng&paperid=5189&what=fullt),
[English publication](https://doi.org/10.1016/0041-5553(80)90098-1).

Here is our explicit corollary. Write the instance as

\[
 Dw\le e,\qquad \|Aw+b\|_2\le c^Tw+d.
\]

First use LP to check the zero-right-hand-side branch

\[
 Dw\le e,\qquad Aw+b=0,\qquad c^Tw+d=0.
\]

On the other branch put
\(s=1/(c^Tw+d)>0\) and \(y=sw\). The problem becomes

\[
 (y,s)\in R:=\{(y,s):Dy\le es,\ c^Ty+ds=1,\ s\ge0\},
 \qquad \|Ay+bs\|_2^2\le1,\qquad s>0. \tag{1}
\]

The substitution and its inverse \(w=y/s\) are exact. Check by LP
whether \(R\) has a point with \(s>0\). If not, this branch is empty.
Otherwise solve the rational convex QP

\[
 \mu=\min_{(y,s)\in R}\|Ay+bs\|_2^2.
\]

The minimum is attained: the linear image
\(V=\{Ay+bs:(y,s)\in R\}\) is a nonempty closed polyhedron, and the
Euclidean norm attains its minimum on \(V\). The exact QP algorithm
provides a rational minimizer of polynomial encoding length.

- If \(\mu>1\), (1) is infeasible.
- If \(\mu<1\), interpolate the minimizer with the previously found
  point having \(s>0\). A sufficiently small positive interpolation
  weight keeps the squared norm below one and makes \(s>0\).
- If \(\mu=1\), all minimizers have the same image
  \(v^*=Ay^*+bs^*\), by strict convexity of the squared norm on \(V\).
  Thus the minimizer set is exactly
  \(R\cap\{Ay+bs=v^*\}\). A final LP tests whether this set contains
  a point with \(s>0\).

A strict-positivity LP test can maximize a variable \(r\) subject to
\(0\le r\le1\) and \(r\le s\), and compare its optimum with zero.
All programs have rational coefficients of polynomial encoding length.
No boundedness or strict-feasibility assumption on the original instance
is used. This proves the one-cone exact decision consequence without the
candidate Hessian-span theorem or a cone approximation.

This reduction does not extend by applying a separate normalization to
each cone: the shared original variables create nonlinear coupling between
the independently normalized systems. It also does not preserve integer
coordinates, so its direct use is continuous feasibility only.

## Existing rational certificates also cover one-cone integer projections

Del Pia, Dey, and Molinaro, *Mixed-integer Quadratic Programming is in NP*,
Theorem 1, give a polynomial-size witness for a nonempty system with one
quadratic inequality and arbitrary affine rows, with specified integer
variables. Section 2.2, Theorem 3, records the Vavasis result that an
attained continuous QP has a polynomial-size rational optimizer. These
theorems do not require the quadratic to be convex. Their witness result
does not by itself give a polynomial-time discovery algorithm.
[Primary manuscript](https://arxiv.org/pdf/1407.4798).

Kocuk, *Rational polyhedral outer-approximations of the second-order cone*,
Discrete Optimization 40 (2021), 100643, §§3.3 and 5, supplies rational
lifted cone approximations with polynomial encoding in dimension and
\(\log(1/\epsilon)\). Proposition 7 preserves the integer points of
intersections of balls with integral centers and radii; Section 5 also
discusses ellipsoid data. That proposition does not cover arbitrary
existential continuous fibers. The source's approximation construction and
its coefficient-bound edge cases are audited separately in
[the rational-lift note](socp-rational-lift-source.md).
[Primary manuscript](https://optimization-online.org/wp-content/uploads/2019/12/7501.pdf).

Nevertheless, a short combination of these older results already proves
the candidate's *one-cone*, boxed-integer projection consequence. This is
our inference, not a claim about the wording of Kocuk's Proposition 7:

1. Fix an allowed integer vector \(z\). Squaring the single cone and
   retaining its sign row leaves one quadratic inequality in \(x\)
   plus affine rows. The rational-witness theorem gives a feasible point
   in a polynomial-bit box whenever the fiber is nonempty.
2. Since \(z\) belongs to an explicitly encoded box, substituting any
   such \(z\) gives coefficient lengths bounded uniformly by a
   polynomial in the original input length. Hence the continuous witness
   box can be chosen uniformly for all these fibers.
3. In an infeasible fiber whose affine rows and witness box are nonempty,
   the minimum of the squared cone residual is a positive rational
   number with polynomial encoding length, by the QP result. It therefore
   exceeds a uniform inverse-exponential threshold.
4. On the joint box the cone right-hand side is at most a
   polynomial-bit bound \(M\). A rational cone outer approximation of
   relative error \(\epsilon\le1\) allows squared residual at most
   \(3\epsilon M^2\). Choose this below the uniform threshold.

The resulting rational linear lift has the same feasible integer vectors
\(z\), uses only continuous auxiliary variables, and has polynomial
size. Empty affine fibers remain empty because their rows are unchanged.
Consequently, neither one-cone polynomial decision nor one-cone boxed
integer-projection preservation should be advertised as the central new
result. The same conclusion extends to every span-one SOC system, as follows.

## The whole Hessian-span-one case follows from older bounds

This section gives checked consequences of the sources, rather than claims
that those sources state an explicit span-one SOCP theorem. All cone sign
rows remain present. Zero full Hessians give affine squared rows and may be
imposed exactly.

**One sign of proportionality.** Suppose every nonzero squared Hessian is
\(a_iH\), with \(a_i>0\). Choose a rational quadratic form \(Q\) with
Hessian \(H\), and write \(q_i/a_i=Q+\ell_i\), with \(\ell_i\)
affine. Introducing \(t\ge\ell_i\) replaces all these inequalities by
the single inequality \(Q+t\le0\). The Vavasis witness bound therefore
gives a polynomial-bit feasible-point radius. After boxing the original
variables and bounding \(t\) using the affine functions, the minimum of
\(Q+t\) over this polyhedron is rational with polynomial encoding length.
An infeasible system has an inverse-exponential positive minimum. Applying
the native SOC outer lifts below that gap decides feasibility by LP.
The epigraph lift itself need not be convex, so the projective one-cone
algorithm above is not being applied to that lifted quadratic inequality.

The same argument gives uniform bounds over boxed integer fibers. A small
extra step handles native SOC rows whose **continuous Hessian block** is
zero: after fixing \(z\), their squared residuals are affine in \(x\),
but the conic outer lift satisfies them only approximately. If those affine
rows and the retained box are inconsistent, rational LP has an
inverse-exponential positive violation gap. Otherwise a Hoffman bound
moves an approximately feasible point into their polyhedron by at most
\(2^{\operatorname{poly}(N)}\) times its residual. On the box,
\(Q+\max_i\ell_i\) has Lipschitz constant
\(2^{\operatorname{poly}(N)}\), so a correspondingly smaller cone
tolerance still lies below the positive QP gap. These estimates are uniform
because every allowed \(z\) has polynomial encoding length.

For completeness, the rational size of the Hoffman constant follows from
the usual projection proof. If \(v\) is the nearest point in a nonempty
polyhedron \(Bx\le b\) to \(u\), an independent active row set \(I\)
and \(\lambda\ge0\) satisfy
\(u-v=B_I^T\lambda\). Therefore
\(\|u-v\|^2\le\delta\|\lambda\|_1\), where \(\delta\) bounds
positive row residuals. The formula
\(\lambda=(B_IB_I^T)^{-1}B_I(u-v)\) and rational determinant bounds
give \(\|\lambda\|_1\le2^{\operatorname{poly}(N)}\|u-v\|\).
This proves the required distance bound, including singular full matrices.
[Hoffman, original theorem](https://upload.wikimedia.org/wikipedia/commons/0/07/On_approximate_solutions_of_systems_of_linear_inequalities_%28IA_jresv49n4p263%29.pdf).

**Both signs of proportionality.** Every native SOC Hessian has at most
one negative eigenvalue, since it is twice \(A^TA-cc^T\). Thus if both
\(H\) and \(-H\) occur up to positive scaling, \(H\) has at most one
positive and one negative eigenvalue: \(\operatorname{rank}H\le2\).
The same statement holds for continuous blocks. A rational invertible
change of coordinates gives \(x=T(y,v)\), with at most two coordinates
in \(y\), so every squared residual is quadratic in \(y\) and affine
in \(v\). After fixing any boxed integer vector, all coefficient lengths
remain uniformly polynomial.

Collect the rows as \(Bv\le b(y)\), where \(b\) has degree at most
two. Farkas elimination describes their projection by
\(\lambda^Tb(y)\ge0\) for the extreme rays of
\(\{\lambda\ge0:B^T\lambda=0\}\). Each ray has a minimal
support of size at most \(\operatorname{rank}(B)+1\) and rational
determinant coefficients of polynomial bit length. There are at most
\(2^m\) such supports for \(m\) rows. Thus the projection has at most
exponentially many degree-two inequalities, each with polynomial-bit
coefficients, in at most two variables. This representation is used only
to prove size bounds; the algorithm does not enumerate it.

Basu and Roy's Theorem 4 bounds a radius meeting every connected component
of a semialgebraic set. At fixed degree and dimension, its logarithm is
\(O(\tau+\log s)\), where \(\tau\) is coefficient bit length and
\(s\) the number of polynomials. It therefore supplies a polynomial-bit
bound on some feasible \(y\) even for this exponential description.
A minimum-norm feasible \(v\) has the form
\(B_I^T(B_IB_I^T)^{-1}b_I(y)\) for independent active rows, so its
magnitude is bounded by \(2^{\operatorname{poly}(N)}\) as well.
[Basu–Roy, primary Theorem 4](https://www.math.purdue.edu/~sbasu/MEGA-submitted-07-11-09.pdf).

For the gap, impose this witness box on \(x\), retain the original
affine/sign rows, and form the compact violation epigraph
\(0\le\tau\le U,\ q_i(x)\le\tau\), choosing an elementary
polynomial-bit \(U\) above all squared residuals on the box. If the
retained affine system is empty, its LP rows already reject the lift.
Otherwise eliminate \(v\) again. The projected epigraph is compact and
has dimension at most three, degree two, exponentially many rows, and
polynomial-bit coefficients. Its minimum \(\tau\), if positive,
occurs on a compact connected component.

Jeronimo, Perrucci, and Tsigaridas, Theorem 1, gives a nonzero-value bound
whose logarithm, at fixed dimension and degree, is
\(O(\log H+\log m)\), with \(H\) the coefficient magnitude and
\(m\) the number of defining polynomials. Its displayed bound uses
\(\widetilde H=\max\{H,2n+2m\}\). Hence the positive violation is
at least \(2^{-\operatorname{poly}(N)}\) despite the exponential row
count. No regularity assumption is required.
[Jeronimo–Perrucci–Tsigaridas, primary Theorem 1](https://arxiv.org/pdf/1112.0544).

The rational native cone lifts then give exact LP decision and, uniformly
over boxed integer vectors, a polynomial rational MILP with the same
integer projection and no new integer variables. This argument handles
zero continuous Hessian blocks automatically. The case \(h=0\) is affine
after fixing the integer variables; LP witness and value bounds give the
same uniform precision conclusion. Thus the proposed general fixed-span
result must be compared against this entire \(h\le1\) baseline.

This argument uses SOC inertia and does not settle arbitrary nonconvex
span-one systems or their arbitrary quadratic objectives. It also does not
give rational witnesses in every span-one SOC system: the rational cones
\(\|(x,1/2)\|\le3/2\) and \(\|(1,1)\|\le x\) force
\(x=\sqrt2\).

## Fixed cone count, few quadratics, and degeneracy

Grigoriev and Pasechnik, *Polynomial-time computing over quadratic maps I:
sampling in real algebraic sets*, Computational Complexity 14 (2005),
20–52, Theorem 1.2, samples every connected component of a variety defined
through a fixed-component quadratic map, with degree and coefficient-bit
bounds polynomial for fixed component count. Arbitrarily many affine
inequalities are not automatically free inputs to their algorithm.
However, the feasible-witness conclusion follows from their theorem by a
short face argument; the earlier parameter comparison alone was incomplete.
[Primary manuscript](https://arxiv.org/pdf/cs/0403008v3).

Write the Hessian-basis lift as \(P\cap V\), where \(P\) is rational
polyhedral and \(V\) is defined by \(h\) quadratic equations. Choose
a face \(F\) of minimum dimension meeting \(V\). Its relative boundary
does not meet \(V\). If a connected component \(C\) of
\(V\cap\operatorname{aff}F\) meets \(F\), then \(C\cap F\) is
nonempty, closed in \(C\), and open in \(C\). Hence \(C\subseteq F\).
A polynomial-bit rational chart of \(\operatorname{aff}F\) and the
Grigoriev–Pasechnik theorem give a short algebraic sample in that component,
and therefore a feasible witness in \(P\). Root bounds give the small
radius. Neither smoothness nor boundedness is needed. Finding the right
face is unnecessary for this existence argument and can be hard.

The [independent nonconvex prior audit](nonconvex-hessian-span-prior-audit.md)
gives the full reduction and representation details. This establishes
mathematical subsumption by older sampling machinery plus an elementary
lemma, without asserting that the resulting Hessian-span corollary was
previously published. The face argument does not by itself bound optimal
values: a component meeting a constrained optimizer can leave its face
through feasible points with larger objective values. Bounded-value and
positive-gap claims therefore retain a separate proof and priority burden.

Nie and Ranestad, *Algebraic Degree of Polynomial Optimization*, SIAM
Journal on Optimization 20 (2009), 485–502, give the generic QCQP degree
\(2^k\binom nk\) for \(k\) active quadratics, with a related upper
bound under a zero-dimensional KKT hypothesis. Eliminating active affine
equations first explains why a fixed quadratic count has polynomial
algebraic degree. This is substantial precedent; it does not supply the
candidate's uniform coefficient-height and radius statements in all
singular cases. The distinction is degree versus effective binary size,
and regular KKT systems versus arbitrary degeneracy.
[Primary manuscript, Theorem 2.2 and Corollary 2.5](https://arxiv.org/pdf/0802.1233).

One-negative-eigenvalue quadratic optimization is not the same problem as
a single SOC branch. A general indefinite quadratic sublevel need not be
one convex SOC set. Conversely, polynomial-size algebraic witnesses do
not imply easy discovery for nonconvex systems: on \([0,1]^n\), the
single inequality \(\sum_i x_i(1-x_i)\le0\) forces Boolean variables,
and rational affine clause rows encode 3SAT. This elementary example has
Hessian span one. It is compatible with a small-witness theorem and with
the convex SOC decision consequence.

## Exact duals and facial reduction do not settle Turing complexity

Hu, *An Exact Dual for Second-Order Cone Programming Using Only
Lorentz-Cone Constraints*, arXiv:2609.06757, gives an exact SOC dual and an
SOC infeasibility alternative without Slater assumptions. Theorem 3.5 and
Corollary 3.7 give polynomial formulation size, including rational
coefficient encoding. The paper expressly distinguishes this from
polynomial-time exact solution or short rational certificates. Moreover,
the tangent lift uses \(1+\binom n2\) generator maps per
\(L_n\) block, with cone copies for those maps. Thus a fixed number of
original cones of growing dimension does not stay a fixed cone count in
this exact-dual construction.
[Primary manuscript, equations (5), (10), (12)–(13)](https://arxiv.org/pdf/2609.06757).

Lourenço, Muramatsu, and Tsuchiya, *Facial Reduction and Partial
Polyhedrality*, SIAM Journal on Optimization 28(3) (2018), 2304–2326,
Theorem 10, bound reducing steps by one plus the sum of distances to
polyhedrality. For \(r\) Lorentz factors and any polyhedral factor this
is at most \(r+1\). This controls sequence length, not encoding length
or the cost of obtaining the reducing directions.
[Primary manuscript](https://arxiv.org/pdf/1512.02549).

Their *Weak Infeasibility in Second Order Cone Programming*, §5, formulates
reducing-direction searches as further SOCPs.
[Primary manuscript](https://arxiv.org/pdf/1509.05168).
Their *Solving SDP Completely with an Interior Point Oracle*, §§1.2–1.3
and Algorithm 4/Theorem 25, assumes exact optimal outputs from auxiliary
interior-point oracles; its general-cone extension does not remove that
assumption. Neither observation implements a bit-polynomial exact oracle.
[Primary manuscript](https://arxiv.org/pdf/1507.08065).

Naldi and Sinn, *Conic Programming: Infeasibility Certificates and
Projective Geometry*, Theorem 3.4 and the discussion after Remark 3.5,
place the nice-cone certificates in
\(\mathrm{NP}_{\mathbb R}\cap\mathrm{coNP}_{\mathbb R}\), in the
Blum–Shub–Smale real-arithmetic model. This is not Turing-model polynomial
time or a polynomial binary certificate bound.
[Primary manuscript](https://arxiv.org/pdf/1810.11792).

## Recommended positioning and verification limits

The safe positioning is:

> Existing quadratic-map sampling and a minimum-face argument provide
> small feasible witnesses and radii at fixed native Hessian span. A
> bounded-value/positive-gap precision bound yields exact polynomial-time
> SOCP feasibility and polynomial rational MILP lifts preserving boxed
> integer projections. Existing cone lifts are an ingredient. The entire
> span-zero and span-one cases already follow from older quantitative
> results by the reductions above. The inspected general cone-complexity
> and exact-duality results do not establish the full fixed-span conclusion.

Do not describe fixed cone count as an established open problem based on
this audit. Do not infer priority from the 2025 paper's nonpolynomial
upper bound. A claim that the fixed-span theorem is new needs a positive
comparison of assumptions and conclusions, including its degeneracy and
height arguments, rather than a search-absence statement.

Searches covered exact/Turing SOCP feasibility, fixed cone count, Lorentz
and symmetric-cone rank, fixed quadratic counts with affine rows, rational
solutions, one negative eigenvalue, Charnes–Cooper normalization, exact
duals, facial reduction, and weak infeasibility. Primary-source theorem
statements were inspected through arXiv/publisher pages and by a delegated
independent source audit. The newly found one-cone reduction was checked
independently in both the projective-QP and witness/gap forms. The
minimum-face consequence and both span-one sign cases were independently
checked, including the exponential Farkas projection's coefficient bounds
and the logarithmic dependence on its number of inequalities.

Targeted local work used `rg`, `sed`, and `cat` to inspect `AGENTS.md`,
the named local source notes, and the Bienstock–Del Pia–Hildebrand full
text; `git diff --no-index --check /dev/null
research-20260927/socp-hessian-span-prior.md` reported no whitespace errors
(the no-index exit status 1 records that the files differ).
No repository-wide checks,
CI inspection, numerical solver runs, or tests of the main candidate
theorem were performed. Literature reading and the elementary corollaries
do not certify publication priority or the general candidate proof.
