# Reduced-Hessian audit and globally conditioned plateau variant

This note independently audits
`2026-09-02-exact-central-plateau-newton-direction.md`.  The original
common-\(\mu\) theorem, its \(O(\log N)\) public-outlier count, and its public
plateau deflation are correct.  Two refinements are possible:

1. a public diagonal congruence makes the original endpoint Hessian exactly a
   scalar identity, while retaining the centered start and exact Newton endpoint;
2. a different public objective makes the **raw orthonormal** reduced Hessian
   globally \(<91/81\)-conditioned and retains an exact one-step Newton theorem,
   but the public start is no longer coordinatewise centered.

The final section proves that this loss is necessary within the separable
four-variable-node ansatz.

## 1. Audit of centrality, strict complementarity, and the Newton secant

Use the notation of the source note.  At node \(i\), the endpoint pair values are

\[
 L_i=\frac{9H_i}{8},\qquad S_i=\frac{H_i}{8},
\]

and \(h_i=H_i,t_i=3H_i/4\).  The objective pair weight is
\(1+w_i\), where \(w_i=7/(36H_i)\), and \(\mu_1=1/16\).

The objective reweighting preserves strict complementarity.  At the optimum,
choose the cap multiplier \(\gamma=\mathbf1\), the reference multiplier by
\(B_g^T\beta=3\mathbf1\), and the signed-difference multiplier by

\[
 B_{ga}^T\alpha=(w_i\tau_i)_i.
\]

Then

\[
 s_{u,i}=w_i(1-\tau_i),\qquad
 s_{v,i}=w_i(1+\tau_i),qquad s_h=s_t=0.
\]

Thus the zero member of every pair has slack \(2w_i>0\).  The original
positive-column basis still proves primal and dual nondegeneracy.

The reduced stationarity equation is

\[
 \frac{w_i}{\mu_1}
 =\frac1{2H_i+z_i}+\frac1{z_i}-\frac1{H_i-z_i}.
\]

At \(z_i=H_i/4\), both sides equal \(28/(9H_i)\).  Hence the endpoint uses one
common complementarity parameter, rather than hidden node-dependent parameters.

The four cross terms in the source note all equal \(25/54\), and the public
start products all equal \(\mu_0=25/81\).  Therefore

\[
 S^0\Delta x+X^0\Delta s
 =\left(\frac{25}{54}-2\frac{25}{81}\right)\mathbf1
 =\left(\frac{25}{162}-\frac{25}{81}\right)\mathbf1,
\]

which is precisely the standard equation with target
\(\widehat\mu=25/162\).  Endpoint primal and dual feasibility supply the other
Newton equations.  Full row rank and positivity of \(X^0,S^0\) make the Schur
complement positive definite, so the correction is unique.

The displayed direction norm and decoder constants also check:

\[
 \left(\frac7{24}\right)^2+left(\frac{17}{24}\right)^2
 +\left(\frac7{27}\right)^2+left(\frac7{36}\right)^2
 =\frac{16139}{23328},
\]

and the squared selected-versus-unselected pair difference is \(5H_i^2/12\).

## 2. The outliers and deflation are genuinely public

For the public orthonormal null columns

\[
 W_i=\sqrt{\frac23}
 \left(\frac12e_{u_i}+\frac12e_{v_i}-e_{t_i}\right),
\]

the endpoint reduced Hessian is exactly

\[
 \Lambda=\frac{182}{243}\operatorname{diag}(H_i^{-2}).       \tag{1}
\]

Heights satisfy \(H_i<H\) only for \(i=0,\ldots,T-1\).  There are therefore
exactly \(T=O(\log N)\) nonplateau eigenmodes, not only \(O(\log N)\) distinct
eigenvalues.  The prefix projector

\[
 \Pi_{<T}=\sum_{i<T}|W_i\rangle\langle W_i|
\]

is an input-independent sparse coordinate operation.  Its complementary
restriction is

\[
 (I-\Pi_{<T})\Lambda(I-\Pi_{<T})
 =\frac{182}{243H^2}(I-\Pi_{<T}),                            \tag{2}
\]

so plateau deflation leaves an exact scalar block of dimension
\(P-T=17N+1-O(\log N)\).

This is a matrix statement.  It does not by itself prepare an input-dependent
right-hand side, solve for the affine feasibility correction, or load the answer
into original coordinates.  If an algorithm is given a reduced right-hand-side
oracle, applying the public projector is free only under the corresponding
access-model assumption.  The original-variable state lower bound continues to
charge all hidden loading and recovery through raw coefficient access.

There is an even simpler public exact preconditioner.  Let

\[
 D_H=\operatorname{diag}(H_i).
\]

Then

\[
 D_H\Lambda D_H=\frac{182}{243}I.                           \tag{3}
\]

Equivalently, the public sparse nonorthonormal basis \(\widetilde W=WD_H\) has
an exactly scalar endpoint reduced Hessian.  This retains the common-\(\mu_1\)
central point, exactly centered public start, one-step endpoint, and direction
state lower bound.

Equation (3) must be described as congruence preconditioning, not as condition
one in an orthonormal basis.  Here

\[
 \kappa(D_H)=H=\Theta(\sqrt N).
\]

Block-encoding normalization, postselection, or recovery into the orthonormal or
original-variable state can inherit that dynamic range.  Thus (3) does not make
the end-to-end task free.  It does show that the direction-output lower bound
survives even when the endpoint reduced Hessian has an exact public condition-one
preconditioner.

The Hessian in (1)--(3) is the reduced primal-barrier Hessian at the **endpoint**.
The hard direction is generated by the infeasible-start KKT system at
\((x^0,s^0)\) and contains an affine feasibility correction; it is not a vector in
\(\ker A\).  The theorem therefore does not assert condition one for that
particular KKT or normal matrix.

## 3. A globally conditioned orthonormal formulation

There is a shortest formulation in the pure coefficient-query model.  Return to
the **original** gain--plateau objective, whose feasible-line slope is one.  For
any prescribed \(0<\mu\le1/16\), let the public central scalar \(z_i(\mu)\) be
the unique root

\[
 \frac1\mu=\frac1{2H_i+z_i}+\frac1{z_i}-\frac1{H_i-z_i}.
                                                               \tag{4a}
\]

Put

\[
 L_i=H_i+\frac{z_i}{2},\qquad S_i=\frac{z_i}{2},
 \qquad t_i=H_i-z_i.
\]

Use the public start

\[
 u_i^0=v_i^0=S_i,qquad
 s_{u,i}^0=s_{v,i}^0=\frac{\mu}{L_i},
\]

and put \(h,t\) and their slacks already at their central endpoint values.  With
\(y^0=0\) and complementarity target \(\widehat\mu=\mu\), exactly the calculation
in (9) below shows that one full Newton step reaches the genuine global central
point.  Its primal direction again has one hidden selected coordinate \(H_i\) per
node.  The original gain--plateau estimates give

\[
 \kappa(W^T\nabla^2F_\mu W)<\frac76
 \qquad(0<\mu\le1/16)
\]

on the **whole** orthonormal reduced space.  Thus the original objective already
provides the strongest conditioning statement if arbitrary public algebraic
central scalars are free.  The start is positive but not coordinatewise centered.
Its exact preparation also requires access to the public roots (4a), which a gate
complexity model must charge.

The following alternative has a closed rational endpoint and
\(O(\log N)\)-bit public data.  It is useful when exact finite descriptions are
preferred.

Keep the constraints but set

\[
 \mu_*:=\frac1{16},\qquad z_*:=\frac14,
\]

at every node.  Replace the inverse-height objective weights by

\[
 \widehat w_i
 :=\mu_*\left(
 \frac1{2H_i+z_*}+\frac1{z_*}-\frac1{H_i-z_*}
 \right).                                                   \tag{4}
\]

Use pair coefficients \(1+\widehat w_i\) and retain unit coefficients on
\(h_i,t_i\).  The bracket is positive for every \(H_i\ge1\): it is at least
\(4-1/(H_i-1/4)\ge8/3\).  Therefore the unique optimum and the strict regularity
proof remain unchanged.  These public weights are exact rationals with
\(O(\log N)\)-bit descriptions.

The genuine common-\(\mu_*\) central point is, up to the hidden pair swap,

\[
 L_i=H_i+\frac18,qquad S_i=\frac18,qquad
 h_i=H_i,qquad t_i=H_i-\frac14.                           \tag{5}
\]

Equation (4) is exactly its reduced stationarity equation.  In the public
orthonormal null basis, the reduced eigenvalues are

\[
 \widehat\lambda_i
 =\frac{2\mu_*}{3}\left[
 (2H_i+1/4)^{-2}+16+(H_i-1/4)^{-2}
 \right].                                                  \tag{6}
\]

The two height-dependent terms decrease on \(H_i\ge1\), so

\[
 \frac23<\widehat\lambda_i\le
 \frac23\frac{91}{81},
 \qquad
 \kappa(\widehat\Lambda)<\frac{91}{81}<\frac76.           \tag{7}
\]

Thus the complete orthonormal reduced Hessian is uniformly conditioned without
deflation or nonunitary congruence.

### A public one-step Newton start

Set

\[
 u_i^0=v_i^0=S_i=\frac18,qquad
 s_{u,i}^0=s_{v,i}^0=\frac{\mu_*}{L_i}.                    \tag{8}
\]

Put the \(h_i,t_i\) primal and slack coordinates already at their endpoint
values in (5), take \(s^1=\mu_*/x^1\), and set \(y^0=0\).  This start is public,
strictly positive, and primal-dual infeasible.  Use the standard complementarity
target \(\widehat\mu=\mu_*\).

For the pair coordinate selected by \(\tau_i\),

\[
 \Delta x=L_i-S_i=H_i,qquad \Delta s=0.
\]

For the unselected coordinate,

\[
 \Delta x=0,qquad
 \Delta s=\frac{\mu_*}{S_i}-\frac{\mu_*}{L_i}.
\]

Both obey

\[
 S^0\Delta x+X^0\Delta s
 =\mu_*\left(1-\frac{S_i}{L_i}\right)
 =\widehat\mu-X^0S^0.                                    \tag{9}
\]

For \(h,t\), both sides are zero.  Endpoint feasibility and the same Schur
argument prove that a full standard Newton step lands exactly at (5).

The primal direction contains one coordinate of magnitude \(H_i\), selected by
\(\tau_i\), at every node, and no other nonzero coordinate.  Hence

\[
 \|\Delta x\|^2=\sum_iH_i^2,
\]

and the output plateau carries probability

\[
 \frac{16NH^2}{\sum_iH_i^2}>
 \frac{16}{53/3}=\frac{48}{53}.                            \tag{10}
\]

A fixed plus/minus pair measurement recovers parity with constant bias, even
after constant trace error.  The local coefficient-oracle simulation and the
quantum parity lower bound therefore give \(\Omega(N)=\Omega(P)\) queries for the
normalized exact primal direction state.  Trace distance \(1/10\) is more than
sufficient.

The price is explicit: the pair products at the start are

\[
 x_{u,i}^0s_{u,i}^0=x_{v,i}^0s_{v,i}^0
 =\mu_*\frac{S_i}{L_i},
\]

which vary with height, while the \(h,t\) products equal \(\mu_*\).  The start is
not coordinatewise centered.

## 4. A sharp incompatibility inside the local ansatz

The lost centered-start property is necessary within this four-variable node
gadget.  Let a hidden-swappable endpoint pair have values \(L_i>S_i>0\) at common
parameter \(\mu_1\).  Suppose the public start is coordinatewise centered at one
common \(\mu_0\).  Write its public pair values as \(a_i,b_i\), with slacks
\(\mu_0/a_i,\mu_0/b_i\).

For one full Newton correction with a common complementarity target to work for
both hidden orientations, the cross terms for \(L_i\) and \(S_i\) must agree.  For
the first coordinate,

\[
 \frac{\mu_0L_i}{a_i}+\frac{a_i\mu_1}{L_i}
 =\frac{\mu_0S_i}{a_i}+\frac{a_i\mu_1}{S_i}.
\]

Because \(L_i\ne S_i\), this forces

\[
 a_i^2=\frac{\mu_0L_iS_i}{\mu_1}.                         \tag{11}
\]

The same argument gives \(b_i=a_i\).  The common cross term is

\[
 C_i=\sqrt{\mu_0\mu_1}\,
 \frac{L_i+S_i}{\sqrt{L_iS_i}}.                            \tag{12}
\]

One global Newton target makes \(C_i\) independent of \(i\), so the aspect ratio
\(L_i/S_i\) is constant across all hidden-swappable nodes.  Since
\(L_i-S_i=H_i\), both values must be proportional to \(H_i\).  The standard
log-barrier Hessian in the local orthonormal null direction then scales as
\(H_i^{-2}\), yielding condition ratio \(H^2=\Theta(N)\).

Consequently, within this separable ansatz one cannot simultaneously have:

1. a public start with one common coordinatewise complementarity parameter;
2. one full standard Newton correction to a hidden-swappable common-\(\mu\)
   central endpoint;
3. an \(O(1)\)-conditioned endpoint Hessian in an orthonormal null basis.

The source theorem keeps the first two properties and admits public deflation or
the exact congruence (3).  The variant (4)--(10) keeps the latter two properties
and a public positive start, but not a centered start.  This is not an
impossibility theorem for augmented gadgets, weighted barriers, or other LP
families.

## Verdict

The original theorem's common-\(\mu\) algebra, exact direction, Hessian spectrum,
\(O(\log N)\) outlier count, and input-independent plateau deflation are sound.
The outlier statement is stronger than dimension counting alone: the exact
projector and all exceptional eigenvalues are public.  However, it concerns the
endpoint reduced Hessian, not the infeasible-start KKT matrix that generates the
hard direction.

Equation (3) gives a whole-space condition-one preconditioned formulation while
retaining every original hypothesis, subject to honest scaling and recovery
costs.  If condition in the orthonormal coordinates is required, equations
(4)--(10) give an exact globally central, globally \(<91/81\)-conditioned
one-step direction theorem; its public start is positive but not centered.
