# Prewriting audit: nonconvex quadratic arithmetic

Date: 2026-10-05. Scope: coverage entry Q13, including algebraic feasibility
witnesses, bounded optimal values, finite infima without attainment,
minimum-norm attained optimizers, and the fixed-span NP and FP^NP interfaces.
This is an independent analytic source audit for Appendix L. It supersedes
the earlier decision to leave Q13 outside the manuscript. No manuscript or
source note was edited. No experiment, historical mathematical script, CAS
calculation, browsing, or literature search was run.

## Finding

I reconstructed the arguments rather than relying on the saved positive
reviews. No invalid theorem or unresolved analytic gap was found in the
final source proofs, subject to the established sampling and effective
algebraic-degree contracts identified below. A separately delegated native
proof reviewer independently checked the finite-infimum argument and
confirmed its ordered-limit and coefficient accounting.

The shorter inactive-box proofs are the clearest route for Appendix L.
They give a complete finite-infimum argument with two small parameters,
then strengthen it to a common-field minimum-norm optimizer when attainment
supplies a uniform primal bound. The general finite-quotient proof already
in Appendix J can be reused by an explicit reference to its mathematical
statement and proof. The new appendix must contain the lift, genericity,
inactive-box argument, nested selection, common-field representation, and
oracle reductions. Repository companion files cannot serve as proof
dependencies in the submitted paper.

The principal obligations are precise rather than repairs to false source
claims:

- The objective Hessian is excluded from the parameter used in the value
  and optimizer bounds. Adding an objective-threshold constraint for a
  feasibility query increases that parameter by at most one.
- A finite infimum need not be attained. Its proof has only a finite
  scalar outer limit; primal points and multipliers may diverge.
- The attained theorem describes at least one minimum-norm optimizer.
  Such a point need not be unique in a nonconvex optimal set. Calling it
  the canonical optimizer is justified only when uniqueness is proved,
  for example when the optimal set is convex.
- Unknown auxiliary radii disappear before the selected KKT coefficients
  are formed. Their numerical magnitude is not an input-height term.
- Every coordinate and linear form in the joint-field proof uses one
  shared nested vector sequence, chart, and oriented active subset.
- The extraction order is the inner generic perturbation first and the
  outer regularization second. A diagonal or unordered infinitesimal
  presentation requires additional justification and is unnecessary here.
- Short algebraic descriptions give exact feasibility verification.
  They do not by themselves certify global optimality or imply an
  ordinary polynomial-time global optimization algorithm.

## Sources read and paper interfaces inspected

The analytic audit read the final versions of
`research-20260927/nonconvex-hessian-span-frontier.md`, its `review.md`
and `adversarial.md` files, `nonconvex-finite-infimum.md` and its review,
`nonconvex-attainment-and-optimizer.md`, its attainment review, and the
nonconvex Hessian-span and attainment prior-audit files. It also checked
the saved algebra and inactive-box reviews where they expose the exact
limit hypotheses. Their recorded computations were not rerun.

The manuscript interfaces inspected were
`appendices/J-quadratic-contrast.tex`, especially
`lem:qc-elimination`, `lem:qc-ordered-limits`,
`eq:qc-minpoly-height`, and `thm:qc-kll`, and the common-field output
contract in `sections/01-models.tex`. `evidence/BRIEF.md` and `macros.tex`
were read for scope and notation.

The source notes contain prior-source reports. This audit did not reopen
external literature. Luna should confirm the contracts listed at the end;
publication priority is not established by this proof review.

## Exact theorem contracts

Use the manuscript's total binary length \(L\), continuous dimension
\(n\), and a local structural parameter \(h\). Consider

\[
 S=\{x\in\mathbb R^n:Ax\le b,\ Ex=e,\ g_i(x)\le0\ (1\le i\le m)\},
 \qquad
 g_i(x)=\tfrac12x^{\mathsf T}Q_ix+a_i^{\mathsf T}x+c_i,
\]

with rational explicitly encoded data and symmetric arbitrary matrices
\(Q_i\). Every rational scalar and matrix entry is counted in \(L\).
Let

\[
 h=\dim_{\mathbb Q}\operatorname{span}\{Q_1,\ldots,Q_m\}.
\]

This is a Hessian-matrix span, not a Hessian rank, common range, number of
rows, or span of complete quadratic polynomials. An arbitrary rational
quadratic objective \(f\) is included in \(L\), but its Hessian is
excluded from \(h\). Weak inequalities and closedness are essential to
the proofs below. There are no convexity, supplied-bound, smoothness, or
constraint-qualification assumptions.

The paper should state the following assertions.

1. If \(S\ne\varnothing\), it contains a point with one common-field
   representation of degree and total length \(L^{O(h+1)}\).
   Consequently exact feasibility belongs to NP for each fixed \(h\).
   A feasible point of magnitude at most \(2^{L^{O(h+1)}}\) exists.
2. If a finite rational box is explicitly supplied and the resulting set
   is nonempty, the minimum of \(f\), and an optimal point, have
   algebraic descriptions of that size, with the box included in the
   encoded input. This follows from the compact proof or from item 3
   and the attained theorem.
3. If \(S\ne\varnothing\) and \(\theta=\inf_S f> -\infty\),
   there is a nonzero \(P\in\mathbb Z[t]\) with
   \(P(\theta)=0\), degree and coefficient bit lengths
   \(L^{O(h+1)}\). No attainment assertion is included.
4. If this infimum is attained, at least one optimizer of least Euclidean
   norm in the original \(x\)-coordinates has a common-field
   representation of degree and total length \(L^{O(h+1)}\).
   Its value belongs to the same field. Its squared norm has a scalar
   annihilator with the same form of bound.
5. For fixed \(h\), an FP^NP algorithm classifies infeasibility,
   unboundedness below, finite nonattainment, and finite attainment. It
   returns the exact finite value. In the attained case it also returns
   an optimizer, and can return one of minimum norm.

For reuse after appending large explicit radii or precise thresholds,
record the coefficient-sensitive form. Let \(S_0\ge2\) bound the
structural size: variables, rows, scalar coefficient positions, and index
bit lengths. Let \(\tau_0\ge1\) bound each rational numerator and
denominator bit length. There is an effective absolute constant \(C\)
such that scalar and joint-field degrees are at most
\(S_0^{C(h+1)}\), and annihilator coefficient bits and common-field
representation length are at most

\[
 (\tau_0+1)S_0^{C(h+1)}.
 \tag{1}
\]

Different occurrences may need a larger common \(C\). This is not a
fixed-parameter running time of the form \(\phi(h)L^{O(1)}\).

## The lift and rational charts

Choose a rational basis \(B_1,\ldots,B_h\) among the native Hessians,
and write \(Q_i=\sum_j\gamma_{ij}B_j\). Rational Gaussian
elimination computes the basis and coefficients. Bounded-order rational
determinants give coefficient bits
\((\tau_0+1)S_0^{O(1)}\). Introduce

\[
 y_j=\tfrac12x^{\mathsf T}B_jx,\qquad
 w=(x,y),\qquad
 F_j(w)=\tfrac12x^{\mathsf T}B_jx-y_j.
\]

The original feasible set is in bijection with

\[
 T=P\cap\{F_1=\cdots=F_h=0\},
 \tag{2}
\]

where \(P\) is the rational polyhedron containing all original affine
rows and all rows
\(\sum_j\gamma_{ij}y_j+a_i^{\mathsf T}x+c_i\le0\).
The lift has polynomial structural size and exactly \(h\) quadratic
equations. No original row is discarded globally.

For any consistent subset of rows of \(P\) made equalities, select
independent normals and solve them to obtain

\[
 w=a+Vu,
 \tag{3}
\]

with \(V\) of full column rank. Cramer's rule bounds these rational
coefficients by \((\tau_0+1)S_0^{O(1)}\) bits, uniformly over all
subsets. The family of charts is finite, with at most
\(2^{S_0^{O(1)}}\) members. Its efficient enumeration is not claimed.
A zero-dimensional chart is one rational point and is handled directly.

## Feasibility: established sampling plus a complete face argument

For feasibility, the paper should use the shorter established route.
The required sampling theorem says that the zero set of an outer
polynomial of degree \(d\) composed with \(h\) quadratic functions in
\(r\) variables has component samples of degree \((dr)^{O(h)}\),
and, for integer input, coefficient bits bounded by the same factor times
input coefficient size. It has no smoothness or compactness requirement.
The applicable source is Grigoriev--Pasechnik, Theorem 1.2, not their
announced optimization theorem.

Here is the whole polyhedral argument, which must appear in the paper.
Among faces \(F\) of \(P\) meeting the variety \(V_0=Z(F_1,\ldots,F_h)\),
choose one of minimum dimension, allowing \(P\) itself. A point in
\(\operatorname{relbd}F\) belongs to a proper face of \(F\), also
a face of \(P\). Minimality therefore gives

\[
 V_0\cap\operatorname{relbd}F=\varnothing.
\]

Choose a connected component \(C\) of
\(V_0\cap\operatorname{aff}F\) meeting \(F\). Its intersection
with \(F\) is nonempty and closed in \(C\). It is also
\(C\cap\operatorname{relint}F\), hence open in \(C\).
Connectedness gives \(C\subseteq F\). The reasoning works for
unbounded faces and lineality; an affine-space face has empty relative
boundary.

Restrict to a rational chart of \(\operatorname{aff}F\) and apply
the sampling theorem with outer polynomial \(\sum_{j=1}^hY_j^2\).
At least one sample meets \(C\), hence is feasible for every original
row. The chart and clearing rational denominators preserve (1). Convert
the sample's coordinate rational functions to coordinate polynomials by
inverting its denominator modulo the root polynomial and isolate the
selected real root. These are polynomial-size univariate operations.
The case \(h=0\) is rational polyhedral feasibility.

An NP verifier receives just the final represented point, verifies the
root isolation, and determines all original row signs. It does not need
the minimum face, a sampling transcript, or perturbations. The result
should be presented as this explicit corollary of established sampling;
the prior audits do not support a claim of a new sampling method.

## Generic quadratic critical points

The value and minimum-norm proofs require a separate genericity lemma.
Fix \(d>0\) and \(s\le d\). Let \(r,f_1,\ldots,f_s\) be
arbitrary quadratics on \(\mathbb C^d\), with all coefficients free.
Outside a proper algebraic exceptional set:

- common zeros of the \(f_i\) have independent gradients;
- every KKT root has invertible multiplier Hessian
  \(M=\nabla^2r+\sum_i\lambda_i\nabla^2f_i\);
- every KKT root has invertible bordered matrix
  \(\left(\begin{smallmatrix}M&G^{\mathsf T}\\G&0\end{smallmatrix}\right)\),
  where the rows of \(G\) are the active gradients.

For \(s>d\), generic quadratics have no common zero.

These properness statements have a direct proof. At fixed \(u\), the
values and gradients of the quadratics can be chosen independently by
their constant and linear terms. Vanishing values impose \(s\)
conditions, and gradient rank deficiency has codimension \(d-s+1\).
Including the \(d\) coordinates of \(u\) leaves bad-incidence
dimension at most one less than coefficient-space dimension. If \(s>d\),
the value equations alone have that consequence.

For KKT, solve each constraint equation for its constant term and each
stationarity equation for the corresponding linear objective coefficient.
The incidence is the graph of a polynomial map from an affine space of
the same dimension as coefficient space, hence irreducible. Neither
determinant vanishes identically: use

\[
 f_i(u)=u_i^2-1\ (i\le s),\qquad
 r(u)=\sum_{j=1}^du_j^2+\sum_{i=1}^su_i.
\]

At \(u_i=\pm1\) for \(i\le s\), \(u_j=0\) otherwise, and
\(\lambda_i=-1-1/(2u_i)\), the entries of \(M\) are
\(-1/u_i\) in the first \(s\) positions and 2 elsewhere.
The gradients are \(2u_ie_i\), so \(GM^{-1}G^{\mathsf T}\)
is diagonal and invertible. Determinant-zero subvarieties therefore have
codimension at least one; their projected closures are proper.

The bordered condition is separate and necessary. For instance,
\(M=\operatorname{diag}(1,-1)\) is invertible and
\(G=(1,1)\) has full row rank, but
\(GM^{-1}G^{\mathsf T}=0\). Positive-definiteness arguments from
Appendix J cannot be copied into this nonconvex proof.

For a quantitative exceptional set, the incidences have polynomially many
variables and equations of polynomial degree in \(d+s\). Gradient
dependence can be covered by \(s\) charts that normalize one coefficient
of a nonzero dependence vector to one, avoiding an exponential minor list.
Affine Bezout for cumulative degree, linear projection, and a containing
hypersurface bound give one nonzero exceptional polynomial of degree
\(2^{\operatorname{poly}(d+s)}\). Here cumulative degree must include
lower-dimensional irreducible components. No coefficient-height bound
for this exceptional polynomial is needed.

## One short perturbation tuple and its parameter quantifiers

Choose integer quadratic polynomials \(P_0,P_1,\ldots,P_h\) in the
ambient lifted coordinates. The two-parameter family is

\[
 r_{\varepsilon,\eta}(w)
   =f(x)+\varepsilon\|x\|^2+\eta P_0(w),\qquad
 |F_j(w)+\eta^2P_j(w)|\le\eta.
 \tag{4}
\]

Use only charts (3) of the original \(P\), with artificial boxes
excluded. Restriction of arbitrary ambient quadratics to one chart is
surjective onto all quadratics in \(u\): extend affine coordinate
functions from the chart to the ambient space and substitute them into
the desired restricted polynomial. At every fixed \(\varepsilon\)
and \(\eta\ne0\), the factors \(\eta\) and \(\eta^2\)
therefore make the coefficient map in (4) surjective for the objective and
every selected oriented constraint quadratic.

Consequently substitution in every exceptional polynomial yields a
nonzero polynomial in \(\varepsilon,\eta\) and perturbation
coefficients. Take one nonzero coefficient in its formal
\((\varepsilon,\eta)\)-expansion. Multiply these chosen polynomials
over the finite chart and oriented-subset family. The product remains
nonzero and has degree at most \(2^{S_0^{O(1)}}\). A nonzero polynomial
of total degree \(D\) cannot vanish on all of
\(\{0,\ldots,D\}^p\): induction on variables proves this from the
univariate root bound. One successful perturbation tuple thus has
coefficient bits \(S_0^{O(1)}\), independent of \(\tau_0\), both
parameters, and all unknown radii.

After this tuple is fixed, every exceptional polynomial in
\((\varepsilon,\eta)\) is nonzero. Only finitely many
\(\varepsilon\) make it identically zero in \(\eta\), since
they are roots of any one nonzero coefficient polynomial. Exclude their
finite union. At every remaining fixed positive \(\varepsilon\),
there is a sufficiently small positive \(\eta\)-tail on which all
genericity conclusions hold. The tail can depend on \(\varepsilon\).
No simultaneous uniform tail is claimed.

Only one orientation of each band can be active because its width is
\(2\eta>0\). Thus at most \(h\) nonlinear multipliers occur, and
the genericity lemma additionally makes their number at most the chart
dimension. This count explains why the objective Hessian adds no parameter
cost: it appears in stationarity but creates no active multiplier.

## KKT elimination and the Appendix J interface

At a box-interior perturbed minimizer, make every active row of the original
polyhedron an equality and use its chart (3). Inactive affine rows remain
strict locally. Independent active nonlinear gradients give ordinary KKT
necessity with objective multiplier one. The KKT assertion is local; no
global minimization claim follows after deleting inactive rows.

Fix the chart and oriented active subset of size \(s\le h\).
Stationarity is \(Mu+\mu=0\). Put

\[
 \Delta=\det M,\qquad p=-\operatorname{adj}(M)\mu,
 \qquad u=p/\Delta.
\]

Multiply each reconstructed active equality by \(\Delta^2\) to
obtain \(G_i(\varepsilon,\eta,\lambda)=0\). At a selected root,

\[
 \frac{\partial G}{\partial\lambda}
       =-\Delta^2GM^{-1}G^{\mathsf T},
 \tag{5}
\]

where the \(G\) on the right denotes the active-gradient matrix.
The notation should be separated in the paper to avoid confusing this
matrix with the eliminated polynomials. Formula (5) follows by
differentiating stationarity to get
\(\partial u/\partial\lambda_i=-M^{-1}\nabla f_i(u)\);
terms differentiating \(\Delta^2\) vanish at an active equality.
The Schur complement of the bordered matrix proves that this multiplier
Jacobian is nonsingular. Neither multipliers nor primal variables need to
stay bounded for this assertion.

Coordinates, fixed rational linear forms, the squared original-coordinate
norm, and the perturbed objective are rational outputs of the same roots.
Use common denominator \(A=\Delta^2\), multiplying coordinate
numerators by \(\Delta\) as needed. Clear only fixed rational
denominators. All eliminated equations and output numerator/denominator
polynomials have multiplier degree \(a=O(d+1)\), polynomial parameter
degree, and logarithmic full coefficient norm
\((\tau_0+1)S_0^{O(1)}\).

One denominator clears the structurally many input coefficients before
determinant expansion. Later denominators divide a structurally bounded
power of it. Multiplying separately over all expanded monomial
coefficients would obscure or lose the linear dependence on \(\tau_0\).
Adjugate expansions may have exponentially many monomials, but their
logarithmic coefficient norm is polynomial in structural size and linear
in input coefficient bits. Parameter values stay formal; no numerical
\(\log(1/\varepsilon)\) or \(\log(1/\eta)\) is charged.

`lem:qc-elimination` in Appendix J is exactly the needed interface over
\(K=\mathbb Q\), after renaming its inner parameter \(\delta\)
to \(\eta\). Its proof only uses nonsingular multiplier roots,
nonvanishing output denominator, and finite ordered scalar output limits;
it uses no convexity or bounded-multiplier assumption. It accepts either
coordinate outputs or just a value output.

For clarity, its quantitative kernel is as follows. For integer formal
polynomials with full coefficient norm at most \(2^\tau\), let

\[
 z=(a+1)^s,\qquad T=a(s+1),\qquad
 K=z[\tau(T+1)+2+\lceil\log_2z\rceil].
 \tag{6}
\]

Deform by \(G_i+\beta\lambda_i^{a+1}\). Its pairwise coprime
leading monomials give a quotient basis of \(z\) monomials. Reducing
multiplication by an output numerator and denominator needs at most
\(T\) substitutions per branch. Clearing \(\beta^T\) gives
matrix entries of norm at most \(2^{\tau(T+1)}\). The determinant

\[
 \det(t\beta^TM_A-\beta^TM_B-\zeta\beta^TI_z)
\]

is nonzero, has degree in \(t\) at most \(z\), and norm at most
\(2^K\). Extract its lowest nonzero \(\zeta\)-coefficient and
then lowest nonzero \(\beta\)-coefficient. The selected-root implicit
branch and the multiplication-eigenvalue factor ensure vanishing at every
selected output. This removes components where both output numerator and
denominator vanish. A specialization can make the extracted coefficient
identically zero; the required relation is then vacuous there and remains
valid. The formal extracted polynomial is nonzero.

Finally extract the lowest \(\eta\)-coefficient and take the inner
limit at fixed \(\varepsilon\), then the lowest
\(\varepsilon\)-coefficient and take the finite outer output limit.
Each extraction takes a subvector of coefficients, so output degree and
coefficient norm do not increase. The resulting nonzero annihilator has
degree at most \(z\) and coefficient bits at most \(K\), giving
(1). The argument includes \(s=0\), with \(z=1\).

## Compact bounded values

For the explicitly bounded problem, append polynomial-bit bounds for each
lifted \(y_j\), obtained by estimating its quadratic form on the given
\(x\)-box. This makes the lifted polyhedron compact. Use objective
\(f+\eta P_0\) and the bands of (4), without needing norm
regularization. An original optimizer remains in the bands for all
sufficiently small \(\eta\). Every primal cluster is feasible, and
uniform convergence of the objective plus comparison with the original
optimizer makes it a global optimizer. Fix a chart and active subset on
one convergent subsequence, apply the elimination interface to coordinates,
linear forms, and objective, and use the common-field proof below. The
box's encoded bits are part of the input in this bounded theorem.

The proof covers \(h=0\). An indefinite quadratic objective over a
rational polytope may be NP-hard despite admitting a short optimum
description; existence of a short description does not discover it.

## Finite infima: remove the auxiliary box before forming coefficients

Assume only \(S\ne\varnothing\) and finite \(\theta=\inf_Sf\).
For each \(\varepsilon>0\), put

\[
 f_\varepsilon(x)=f(x)+\varepsilon\|x\|^2,
 \qquad v_\varepsilon=\min_S f_\varepsilon.
\]

Because \(f_\varepsilon\ge\theta+\varepsilon\|x\|^2\)
on the closed set \(S\), a sublevel below the value at any fixed feasible
anchor is nonempty and compact. Thus the regularized minimum exists.
For a fixed feasible \(\bar x\), every exact regularized optimizer
satisfies

\[
 \|x\|^2\le\|\bar x\|^2+
             \frac{f(\bar x)-\theta}{\varepsilon}.
 \tag{7}
\]

This bounds all regularized optimizers and all their quadratic lifts for
each fixed \(\varepsilon\). Choose an unknown finite integer radius
\(R_\varepsilon\) strictly enclosing all of them. This radius need
not have bounded encoded length or a uniform bound as
\(\varepsilon\downarrow0\). Also

\[
 \theta\le v_\varepsilon
       \le f(x)+\varepsilon\|x\|^2\qquad(x\in S).
\]

Take the upper limit in \(\varepsilon\) for each fixed feasible
\(x\), then the infimum over \(x\), to obtain
\(v_\varepsilon\to\theta\). This proves convergence without
assuming a primal limit or attainment.

At one admissible fixed \(\varepsilon\), minimize (4) inside
\(P\cap[-R_\varepsilon,R_\varepsilon]^{n+h}\). An exact
regularized optimizer remains feasible in its bands eventually. The
perturbed problem is therefore nonempty and compact. Every cluster of
perturbed optimizers as \(\eta\downarrow0\) satisfies \(F_j=0\).
Uniform objective convergence on this fixed box and comparison with an
exact regularized optimizer show that the cluster's
\(f_\varepsilon\)-value is \(v_\varepsilon\). It is therefore
an original global regularized optimizer and lies strictly inside the box.

If arbitrarily small \(\eta\) allowed a boundary optimizer, compactness
would give a boundary cluster, contradicting strict interiority. Thus all
perturbed optimizers are box-interior for a sufficiently small
\(\eta\)-tail at this fixed \(\varepsilon\). This establishes
eventual inactivity before deriving KKT equations. The box supplies
compactness only; none of its rows occurs in (3), (5), or any selected
coefficient polynomial.

For each admissible \(\varepsilon_\nu\downarrow0\), first retain
an inner \(\eta\)-sequence with one constant original-row chart and
oriented active subset. A second finite pigeonhole selection makes that
label constant on an infinite outer subsequence. These choices come from
a fixed finite family independent of the radii. Use the perturbed objective
itself as output: its inner limit is \(v_{\varepsilon_\nu}\), and
its outer limit is \(\theta\). The Appendix J elimination interface
therefore proves the finite-infimum bound.

If the selected chart has dimension zero, it is one fixed rational point
\(a\). Its inner value is
\(f(a_x)+\varepsilon\|a_x\|^2\), and its outer limit is the
rational \(f(a_x)\). No multiplier elimination is needed.

The saved alternate radius-parameter proof is also valid: charts have
the form \(a+bR+Vu\), the inner perturbation coefficient is extracted
first, and the highest remaining \(R\)-coefficient second. Appendix L
need not reproduce both routes. A positive-infinitesimal-radius shortcut
should not replace the proved inactive-box argument without its own formal
coefficient and ordering proof.

## Attained minima: one minimum-norm tuple and one common field

Now suppose the finite value \(\theta\) is attained. The optimal set
is nonempty and closed. Its intersection with the closed norm ball of one
optimizer is compact, so it has an optimizer \(\bar x\) of minimum
norm \(c=\|\bar x\|\). Comparison with \(\bar x\) gives, for
every exact regularized optimizer,

\[
 \theta+\varepsilon\|x_\varepsilon\|^2
 \le f(x_\varepsilon)+\varepsilon\|x_\varepsilon\|^2
 \le\theta+\varepsilon c^2.
\]

Consequently

\[
 \|x_\varepsilon\|\le c,
 \qquad 0\le f(x_\varepsilon)-\theta\le\varepsilon c^2.
 \tag{8}
\]

All exact regularized lifts lie in one fixed compact set. Choose one
unknown integer box strictly enclosing that set. The preceding inactive-box
argument works at every admissible fixed \(\varepsilon\), with this
one box, and still removes all its rows before coefficient formation.

Select inner convergent perturbed primal sequences and outer convergent
regularized limits, while retaining one chart and oriented subset:

\[
 w_{\nu,\mu}\to w_\nu\quad(\mu\to\infty),
 \qquad w_\nu\to w^*\quad(\nu\to\infty).
 \tag{9}
\]

The first limit is at fixed \(\varepsilon_\nu\). Inequality (8)
holds for the inner limiting points, not necessarily the perturbed leaves.
It shows that \(x^*\) is a global optimizer and has norm at most
\(c\), hence exactly the minimum norm. All coordinate outputs and
linear forms must use this same tuple tree (9).

Apply elimination to each coordinate of \(w^*\), its squared original
norm, and every fixed rational linear form in its coordinates. All forms
have degree at most the same \(z=(a+1)^s\), independently of the
sizes of their rational coefficients. Coordinates are therefore algebraic,
and the field \(E=\mathbb Q(w^*)\) is finite and separable. A
primitive element can be chosen as a rational linear combination of these
coordinates. Its degree is at most \(z\), so

\[
 [E:\mathbb Q]\le z.
\]

This step bounds the joint field. Multiplying separate coordinate-degree
bounds would not prove the theorem. Since \(f\) has rational
coefficients, \(\theta=f(x^*)\) lies in this same field. The original
coordinate field is a subfield and obeys the same bound.

For a short representation, let \(D\ge[E:\mathbb Q]\). For every
pair of distinct embeddings of \(E\), equality of their values on an
integer linear combination imposes a proper linear hyperplane on its
coefficients. The product over pairs has degree at most
\(D(D-1)/2\). The grid argument therefore finds a primitive element
\(\alpha=\sum_jt_jw_j^*\) with all
\(0\le t_j\le D(D-1)/2\). Applying the same output elimination to
this bounded-coefficient combination bounds its annihilator height by
(1). The elementary integer-factor bound in
`eq:qc-minpoly-height` gives the same form of bound for its primitive
irreducible minimal polynomial and the coordinate minimal polynomials.

Here is the complete power-basis height argument. Scale \(\alpha\)
and a coordinate \(\beta\) by the leading coefficients of their
minimal polynomials, obtaining algebraic integers \(A\) and \(B\).
If their coefficient bits are bounded by \(H\), Cauchy's bound gives
conjugate magnitudes of \(A,B\) at most \(2^{O(H+1)}\).
Writing \(d=[E:\mathbb Q]\) and
\(B=\sum_{r=0}^{d-1}c_rA^r\), take traces after multiplication by
\(A^s\), \(0\le s<d\). The resulting matrix has entries
\(\operatorname{Tr}(A^{r+s})\); the right-hand side has entries
\(\operatorname{Tr}(BA^s)\). They are integers of
\(O(d(H+1)+\log d)\) bits. Separability makes the trace form
nonsingular on this basis. Cramer's rule bounds all rational \(c_r\)
by \(O(d^2(H+1)+d\log d)\) bits. Scaling back gives rational
polynomials in \(\alpha\) for every coordinate with polynomial size
in \(d,H\), preserving linear dependence on the original coefficient
bit bound.

Root separation supplies a rational interval isolating the intended real
root with polynomial bit length in \(d,H\). Thus the common-field
representation has total length (1). It can use the manuscript's primitive
irreducible generator polynomial. The source notes' weaker squarefree-root
format also suffices for verification, but the stronger format exists and
matches Appendix J.

Cauchy's bound on the coordinate annihilators gives an effective explicit
radius \(B_0=2^{H+2}\) containing at least one optimizer whenever
attainment holds. It does not contain every optimizer. Appending this
radius adds only affine rows; structural size stays polynomial in
\(S_0\), while the new coefficient bits satisfy (1). Applying the
coefficient-sensitive bound again preserves the form (1), rather than
introducing a needless quadratic exponent in \(h\).

## Exact verification and value recovery

For a common-field represented point, substitute the coordinate polynomials
into each rational original row and reduce modulo the generator polynomial.
Exact signs at its isolated real root are computed by Sturm or subresultant
arithmetic in polynomial time in the input and representation lengths.
Root isolation and polynomial squarefreeness or irreducibility are also
polynomial-time verifiable. Thus the witness bound proves NP membership
for fixed \(h\).

For rational \(t\), feasibility with \(f(x)\le t\) is in NP by
the same theorem, with Hessian span at most \(h+1\). First query the
original feasibility. If nonempty, use the finite-value annihilator bound
to compute \(M=2^{H+2}\) such that every finite infimum of this input
satisfies \(|\theta|<M\). Then

\[
 \inf_S f=-\infty
 \quad\Longleftrightarrow\quad
 \exists x\in S:\ f(x)\le-M-1.
\]

The forward implication is the definition of unboundedness below; the
reverse contradicts the proved finite-value bound. This is a status test,
not a construction of a recession ray.

In the finite case, bisection starts with \(a=-M-1\), \(b=M+1\).
The lower threshold is infeasible and the upper one feasible. Threshold
queries retain a closed interval containing \(\theta\). If a queried
midpoint equals an unattained infimum, the answer is no and moving the
lower endpoint to that midpoint still preserves containment. No
attainment assumption enters bisection.

The degree and minimal-polynomial coefficient bounds and certified
approximations meet `thm:qc-kll`. Its precision is polynomial in degree
and coefficient bit bound, and it recovers the primitive minimal
polynomial in polynomial bit time. Further approximation below a
discriminant root-separation bound identifies the correct real root and
gives an isolating interval with endpoints that are not roots. Every
threshold has polynomial length for fixed \(h\), even at the recognition
precision. This proves FP^NP finite-value and status computation.

## Attainment and minimum-norm output with the oracle

After recovering the actual finite value, let its minimal polynomial be
\(P_\theta\) and its isolating interval be \((a,b)\), with
nonroot endpoints. A polynomial-time verifier accepts a common-field point
certificate exactly when it satisfies all original rows and, writing
\(\gamma=f(x)\) in that point's own representation,

\[
 P_\theta(\gamma)=0,\qquad a<\gamma<b.
 \tag{10}
\]

This tests equality to the selected real value without constructing a
compositum of separately represented fields. Condition (10) alone does
not establish global optimality; the preceding value algorithm has
already produced the correct \(\theta\).

Fix the proved polynomial certificate bound for this original instance.
One NP query asks whether this verifier has an accepting certificate within
that bound. The answer is yes exactly when the infimum is attained.
Completeness comes from the attained optimizer theorem; soundness comes
from exact feasibility and (10). Standard prefix search on a padded
self-delimiting bounded-length encoding recovers an accepting optimizer
with polynomially many NP queries. Each prefix-extension language is in
NP because the verifier is polynomial time.

Alternatively, all optimization queries can remain rational: append
\([-B_0,B_0]^n\), test its feasibility, and compute its compact minimum
\(\theta_{B_0}\). The original infimum is attained exactly when that
set is nonempty and \(\theta_{B_0}=\theta\). Empty boxed feasibility
must be treated as nonattainment, not as original infeasibility.

To recover a minimum-norm optimizer, let
\(\rho=\min\{\|x\|^2:x\in S,f(x)=\theta\}\). Its
annihilator has bounds (1). After attainment is established, ask for a
certificate within the universal minimum-norm witness bound satisfying
(10) and \(\|x\|^2\le t\). This NP query answers yes exactly when
\(t\ge\rho\): no optimizer has lower norm, and one minimum-norm
optimizer has a short certificate independent of \(t\). Bisect on
\([0,nB_0^2]\) and recognize \(\rho\) exactly by `thm:qc-kll`.
This bisection needs interval containment, not an infeasible lower endpoint
when \(\rho=0\). Prefix search with both exact scalar equalities then
returns a minimum-norm optimizer. Equality to \(\rho\) uses its
minimal polynomial and isolating interval inside the candidate point's
field, just as in (10).

The distinction between a short output and a certificate of optimality
must stay visible. The point certifies feasibility. Its optimality in this
algorithm follows from the separately computed value; no short standalone
global-optimality certificate is established.

## Bounded integer slices and hardness boundaries

The finite-infimum source also gives a bounded-integer extension. For
total-degree-two rational mixed-integer input with explicit integer bounds,
let \(h\) be the span dimension of the continuous Hessian blocks.
Every integer assignment has polynomial bit length. Substitution yields
continuous slices with the same span bound and uniform polynomial
coefficient-size bounds. Feasibility with a rational objective threshold
is in NP by guessing the integer assignment and its continuous algebraic
witness. There are finitely many assignments. If one feasible slice is
unbounded below, the mixed problem is unbounded below; otherwise a finite
mixed infimum equals one of the finitely many slice infima. The uniform
scalar bound therefore gives the same FP^NP classification and exact
finite-value algorithm. No claim about unbounded integer variables follows.

The elementary hardness distinctions belong beside the oracle statements.
On \([0,1]^n\), one concave row
\(\sum_i x_i(1-x_i)\le0\) forces every variable to be Boolean.
Adding the affine 3SAT clause inequalities proves strong NP-hardness of
feasibility at \(h=1\), while the witness theorem gives NP membership.
Algebraic witnesses are sometimes necessary: \(x^2=2\), written as
two opposite weak quadratic inequalities, has span one and no rational
feasible point.

Attainment is strongly NP-hard even for one quadratic row, a linear
objective, and promised known finite infimum zero. For a 3SAT instance,
take \(x\in[0,1]^n\), \(t,y\ge0\), the affine clause rows,
and

\[
 \sum_i x_i(1-x_i)-ty\le0,
 \qquad \min t.
\]

For every \(t>0\), choose \(x_i=1/2\) and \(y=n/(4t)\).
Every three-literal clause sum is \(3/2\), so the instance is feasible
and has infimum zero. At \(t=0\), the nonnegative summands force a
Boolean satisfying assignment. Conversely, such an assignment with
\(t=y=0\) attains zero. The single Hessian is nonzero and all
coefficients have bounded magnitude. The promised subclass is in NP by
appending \(t\le0\) and using fixed-span feasibility. This is a
parameter refinement of established attainment hardness, not a priority
claim.

For a direct nonattainment example, \(xy\ge1\), \(x\ge0\), with
objective \(x\), is closed, has one indefinite Hessian direction, and
has finite unattained infimum zero. Finite infimum cannot be replaced by
attainment in any theorem statement.

## Primary-source contracts for Luna and contribution framing

The proof review does not establish novelty. Route any additional primary
source requests through the root. The final literature report should
confirm these precise contracts and qualifications:

1. Grigoriev--Pasechnik Theorem 1.2 gives component sampling for a
   fixed-component quadratic map, including degree and integer
   coefficient-bit bounds. Arbitrarily many affine rows are accommodated
   here by the proved minimum-face lemma, not by silently treating them
   as free map components.
2. Grigoriev--Pasechnik Theorem 1.5 is an announced optimization statement
   whose proof is deferred. The source notes report Kamminga--Rudolph,
   ITCS 2026, Theorem 1.15 and surrounding text, as a current comparison:
   bounded-map approximation is proved and the earlier unbounded
   optimization proof is reported unavailable to their knowledge. Neither
   statement settles absence of an equivalent theorem elsewhere.
3. Cumulative affine degree obeys the stated Bezout and linear-projection
   bounds, and a proper image component lies in a hypersurface of degree
   at most its degree. The source notes name Krick--Pardo--Sombra and
   Heintz, with the latter facts used in Ovchinnikov--Pogudin--Vo. The
   degree must include all irreducible components, not only those of
   maximal dimension.
4. Kannan--Lenstra--Lovasz Theorem 1.19 gives the certified recognition
   bit-model contract already stated as `thm:qc-kll` in Appendix J. An
   arithmetic-operation claim alone is insufficient.
5. The closest finite-infimum comparison reported in the source audit is
   El Hilany--Tsigaridas, whose stated generic semialgebraic class has
   regularity hypotheses and ambient-dimension-dependent bounds. The
   Appendix L statement allows degenerate inputs and arbitrarily many
   rows, with dependence on native Hessian span.
6. Ahmadi--Zhang Theorem 2.2 is the reported established strong attainment
   hardness result; the elementary reduction above isolates one quadratic
   row. Del Pia--Dey--Molinaro gives rational witnesses for one quadratic
   inequality with affine rows, including unbounded integer domains;
   it should not be conflated with algebraic witnesses for many rows of
   span one.

Once the finite value is encoded, established sampling plus a rational
optimizer-variety construction already gives some optimizer with the
weaker bound \(L^{O((h+1)^2)}\), hence the qualitative fixed-\(h\)
attainment and output interfaces. Sampling over \(\mathbb Q(\theta)\)
also gives the sharper degree for some optimizer, but the stated integer
bit bound does not automatically give the needed number-field height
extension. The direct inactive-box proof supplies the coefficient-sensitive
\(L^{O(h+1)}\) common-field representation and a minimum-norm
selection without that unproved transfer. These are the precise distinctions
the contribution statement should retain.

## Verification record

Verification was analytic source reading and proof reconstruction. The
targeted commands actually run were `python -` with assertions for this
file's final newline, control characters, trailing whitespace, and paired
display/inline math delimiters, and
`git diff --check -- paper-exact-arithmetic/evidence/reviews/prewrite-nonconvex-extension.md`.
Both passed. The direct text check also covers an untracked new file.
No project-wide verification or CI status/log inspection was performed.
