# Audit of the constant-relative scalar parity-chain LP

Status: Independent audit PASS with scope qualifications  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Audited result

Let \(\sigma_1,\ldots,\sigma_N\in\{-1,1\}\), set
\(H=\prod_{m=1}^N\sigma_m\), and consider

\[
\begin{aligned}
 \max\quad&\alpha+2w,\\
 \text{s.t.}\quad&-1\leq\alpha\leq1,\\
 &r_0=\alpha,\qquad r_m=\sigma_mr_{m-1}\quad(m\in[N]),\\
 &w=r_N.
\end{aligned}                                                     \tag{1}
\]

The equalities give \(w=H\alpha\), so the eliminated LP is

\[
             \max_{-1\leq\alpha\leq1}(1+2H)\alpha.
\]

Consequently

\[
 \boxed{\operatorname{OPT}=
 \begin{cases}3,&H=1,\\1,&H=-1,\end{cases}}
 \qquad
 \alpha^*=\begin{cases}1,&H=1,\\-1,&H=-1,\end{cases}
 \qquad w^*=1.                                             \tag{2}
\]

A two-sided relative value estimate
\[
             |\widehat v-\operatorname{OPT}|
                 \leq\delta\,\operatorname{OPT}
\]
determines \(H\) for every fixed \(\delta<1/2\). The two permitted
intervals become \([1-\delta,1+\delta]\) and
\([3(1-\delta),3(1+\delta)]\), which are disjoint exactly when
\(\delta<1/2\). Thus \(\delta=1/4\), for example, gives a
\(\Theta(N)\) bounded-error quantum query lower bound and a matching
\(O(N)\) upper bound.

Other approximation contracts have different sharp thresholds:

- a returned feasible objective value satisfying
  \(v\geq(1-\delta)\operatorname{OPT}\) determines parity from the value
  alone when \(\delta<2/3\);
- a returned feasible \(\alpha\) with the same guarantee determines parity
  from \(\operatorname{sign}\alpha\) for every \(\delta<1\);
- no claim should use the endpoint \(\delta=1/2\) for a two-sided value
  estimate, because the two intervals meet at \(3/2\).

The lower bound is ordinary parity hardness. A \(q\)-query LP-value
algorithm would give a \(q\)-query algorithm for \(H\); bounded-error
quantum parity has query complexity \(\Theta(N)\).

## Barrier and fixed central scale

After equality elimination, the restricted standard box barrier is

\[
                         F(\alpha)=-\log(1-\alpha^2).       \tag{3}
\]

It has exact self-concordance parameter one. Indeed,

\[
 F'(\alpha)={2\alpha\over1-\alpha^2},\qquad
 F''(\alpha)={2(1+\alpha^2)\over(1-\alpha^2)^2},
\]

and

\[
 F'''(\alpha)={4\alpha(3+\alpha^2)\over(1-\alpha^2)^3},\qquad
 {F'''(\alpha)^2\over4F''(\alpha)^3}
 ={\alpha^2(3+\alpha^2)^2\over2(1+\alpha^2)^3}\leq1.
\]

The last inequality follows from
\(2(1+x)^3-x(3+x)^2=(1-x)^2(x+2)\geq0\) for
\(x=\alpha^2\in[0,1)\). Moreover,

\[
             {F'(\alpha)^2\over F''(\alpha)}
                  ={2\alpha^2\over1+\alpha^2}\longrightarrow1.
\]

Thus the ambient two-ray orthant barrier has restricted parameter
\(\boxed{\nu_{\rm slice}=1}\).

At public central multiplier \(\eta>0\), stationarity is

\[
           {\alpha\over1-\alpha^2}={\eta(1+2H)\over2}.
\]

With

\[
 \rho(z)={\sqrt{1+4z^2}-1\over2z},\qquad \rho(-z)=-\rho(z),
\]

the exact center is

\[
            \alpha_H(\eta)=\rho\!\left({\eta(1+2H)\over2}\right).
                                                               \tag{4}
\]

At any fixed \(\eta>0\), its sign is the parity. For example, at
\(\eta=1\),

\[
 \alpha_+=\rho(3/2)>0,\qquad \alpha_-=-\rho(1/2)<0,
\]

with a constant gap. The central objective values
\[
        3\rho(3/2)\quad\text{and}\quad \rho(1/2)
\]
are also positive and separated by a constant relative gap. Hence a
fixed-scale central scalar, not only the exact optimum, is
\(\Theta(N)\)-query hard.

This is not iteration hardness. The restricted problem is one-dimensional
with \(\nu=1\); once \(H\) is known, every center is given by (4). The
construction proves hard data propagation through sparse equalities, not
an \(\Omega(N)\) lower bound on the number of IPM rounds.

## Analytic-center Newton and full-KKT state

There is a useful state-output strengthening at the analytic center.
Order the \(d=N+3\) primal variables as

\[
                     x=(\alpha,r_0,r_1,\ldots,r_N,w).
\]

Let \(A_\sigma x=0\) denote the \(d-1=N+2\) chain equalities. At
\(x=0\), the barrier Hessian in ambient coordinates is
\[
                         D=2e_0e_0^T.
\]
The literal unscaled augmented KKT system for the first Newton direction is

\[
 \begin{pmatrix}D&A_\sigma^T\\A_\sigma&0\end{pmatrix}
 \begin{pmatrix}\Delta x\\y\end{pmatrix}
 =\begin{pmatrix}c\\0\end{pmatrix},
 \qquad c=e_0+2e_{d-1}.                                  \tag{5}
\]

Let
\[
 v=(1,1,\sigma_1,\sigma_1\sigma_2,\ldots,H,H).
\]
Diagonal sign changes on primal variables and equality rows transform
\(A_\sigma\) into the ordinary incidence matrix \(B\) of a path, transform
\(v\) into the all-ones vector, and transform the objective endpoints into
\(1\) and \(2H\). These transformations are orthogonal and preserve all
singular values and register norms.

In the transformed gauge, (5) has the exact solution

\[
       \Delta z=t_H{\bf1}_d,\qquad
       y=2H{\bf1}_{d-1},\qquad
       t_H={1+2H\over2}
          =\begin{cases}3/2,&H=1,\\-1/2,&H=-1.\end{cases} \tag{6}
\]

Thus the scalar Newton coordinate already computes parity. More strongly,
the normalized **full** KKT solution state has primal-register probability

\[
 P_H={d\,t_H^2\over d\,t_H^2+4(d-1)}.                    \tag{7}
\]

For \(N\geq1\), \(P_+\) and \(P_-\) differ by a fixed positive constant.
Measuring the primal-versus-dual register a constant number of times
therefore determines parity. Preparing the literal normalized state in
(5) to a sufficiently small fixed trace or Euclidean error requires
\(\Omega(N)\) sign queries, and reading all signs gives the matching upper
bound.

This state claim is representation-specific. It applies to the unscaled
full augmented KKT state in (5). It does not automatically apply after a
preconditioner or arbitrary block rescaling.

It also does not apply to the normalized primal direction alone. That
direction is \(t_Hv\); its scalar sign is a physically irrelevant global
phase, while the designated endpoint coordinates have only
\(O(N^{-1/2})\) amplitude. A constant-error primal-only state can therefore
lose the scalar parity information. Likewise, a classical scalar, a full
classical vector, a normalized state, and an expectation-value oracle are
distinct output contracts.

## Equality and KKT conditioning

The nonzero singular values of the \(d-1\) by \(d\) path incidence matrix
are

\[
                  2\sin{k\pi\over2d},\qquad k=1,\ldots,d-1.
\]

Hence
\[
             \kappa_2(A_\sigma)
                =\cot{\pi\over2d}=\Theta(N).              \tag{8}
\]

The analytic-center KKT matrix in (5) also has
\[
                         \boxed{\kappa_2(K_\sigma)=\Theta(N).}        \tag{9}
\]

For completeness, its norm is \(O(1)\). A lower bound on the inverse norm
comes from a unit primal right-hand side proportional to \({\bf1}_d\):
the nullspace component of the solution has norm \(\Omega(d)\).
Conversely, solving \(Bx=g\) by prefix sums and \(B^Ty=f-2x_0e_0\) by
tail sums bounds every solution by \(O(d)\|(f,g)\|\). This proves (9).
The same scaling holds at any fixed \(\eta\), since the only changed
Hessian entry remains bounded above and below by positive constants.

The \(\Theta(N)\) condition number is a property of the natural sparse
equality/KKT representation, not intrinsic one-dimensional curvature.
Eliminating the equalities gives a scalar Hessian with condition number
one, but forming its reduced objective coefficient \(1+2H\) requires
computing parity. Thus the example saturates a condition-number-scale
query obstruction for the literal KKT system without implying that every
formulation or preconditioning has condition \(\Theta(N)\).

A crucial access caveat is that the analytic-center matrix (5) has public
Hessian \(D\). At a nonzero exact center, the scalar Hessian itself depends
on \(H\); granting it as a direct entry oracle could leak the answer.
Therefore the clean KKT query statement is (5), not an oracle that is
magically supplied at the unknown nonzero center.

## Sparse and SQ oracle simulation

Every equality row has two nonzeros and at most one hidden sign. Every
column has constant incidence. The support pattern and all squared
magnitudes and norms are public. Consequently:

- a sparse location query needs no hidden query;
- a sparse value or entry query uses at most one sign query;
- squared-coordinate sampling and row/column norms are public; and
- a canonical normalized row or column state is prepared with at most one
  coherent sign query to insert its phase.

The same accounting applies to the analytic-center KKT matrix (5), because
\(D\) and the right-hand side are public and \(A_\sigma,A_\sigma^T\) retain
constant row and column sparsity. Hence a \(q\)-query algorithm under this
canonical full-SQ interface gives an \(O(q)\)-query parity algorithm.

As usual, an arbitrary unitary completion of a state-preparation oracle is
not permitted to encode extra information off its specified preparation
subspace. The reduction is for the canonical entry/sampling/state
interfaces just described.

## Relation to existing notes and literature

The concurrently developed local
[boxed parity-chain note](2026-09-04-boxed-parity-chain-readout-separation.md)
now subsumes the basic LP, value, restricted-barrier, fixed-center,
sparse-oracle, and conditioning statements. It removes the redundant
variables \(\alpha\) and \(w\), using only
\((r_0,\ldots,r_N)\); this changes dimensions by two but no asymptotic or
geometric conclusion. The exact analytic-center solution (6) and the
parity-dependent full-KKT register mass (7) are the useful additional audit
calculations here and can be folded into that note.

The local
[single-scalar central-path parity note](2026-09-04-single-scalar-central-path-parity-saturation.md)
already contains the core carrier mechanism. Setting its transition count
to one and its block length to \(N\) gives a \(\nu=1\) sparse LP whose
optimizer and fixed central coordinate carry parity. The present chain is
simpler: it removes the duplicated carrier and puts the public coefficient
\(2w\) directly in the objective, so the **optimal value itself** is
constant-relatively separated. Equations (5)--(7), especially the
primal-versus-dual mass separation of the normalized full KKT state, are
a distinct useful strengthening.

The parity query lower bound is classical; it follows from the polynomial
method of Beals et al. Optimization-value embeddings of Boolean
composition are also prior art. In particular,
[Apers--Gribling](https://arxiv.org/abs/2311.03215) prove quantum LP-value
query lower bounds by embedding a composed Boolean function, although not
this parity chain. The full-KKT state result is also consistent with the
general \(\Omega(\kappa)\)-scale sparse-QLS lower-bound landscape; the
closest current source is
[Mori--Kikuchi--Benedetti--Rosenkranz](https://arxiv.org/abs/2601.16697),
whose hard family uses a parity clock. Therefore this elementary parity LP
should not be presented as a new quantum lower-bound technique, as the
first LP optimal-value query lower bound, or as the first
condition-number-scale QLS obstruction.

The defensible contribution is the minimal conjunction of constant row and
column sparsity, canonical SQ simulation, constant-relative positive
optimal values, restricted parameter one, fixed-scale Newton/central
separation, and the explicit state-output and conditioning audit. A
targeted specialist literature check would still be required before
claiming that this exact conjunction is new.

## Audit verdict

The proposed theorem is correct with the following qualifications.

1. State the two-sided relative threshold as any fixed
   \(\delta<1/2\), not \(\delta\leq1/2\).
2. Keep feasible-value and feasible-solution thresholds separate from
   two-sided value estimation.
3. Attribute \(\nu=1\) to the equality-restricted barrier; the ambient
   two-slack orthant parameter is two.
4. State the full-KKT normalized-state result only for the literal
   unscaled analytic-center system. Do not transfer it automatically to
   primal-only, preconditioned, or differently normalized states.
5. The equality and natural KKT condition numbers are \(\Theta(N)\), but
   the equality-eliminated scalar problem has condition one.
6. Do not claim iteration hardness. The lower bound is endpoint,
   fixed-central-scalar, or one-shot KKT/output hardness on a static input.
