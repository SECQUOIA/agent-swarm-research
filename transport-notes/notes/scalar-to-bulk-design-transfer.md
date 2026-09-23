# Transfer of optimized scalar response to finite bulk mixing

Derived and reviewed 2026-09-07 by `review_singular_exchange`. The parent proposed a uniform-background transfer argument; the same-budget refinement below was independently checked by both the parent and `review_localization`.

A vanishing uniform mobility background transfers scalar optimal values, including sharp constants, to the full bulk–surface model. The construction preserves the original budget and observation information. Its sufficient growth condition is only that the scalar optimum dominate a logarithmic moment; regular variation is not required.

## Setting

The wall is a fixed connected closed one-dimensional curve of length `P`, with periodic coordinate, bounding a fixed cross-section. Bulk diffusivity is fixed and positive, `u` belongs to `L2` of the bulk, and affinity `K>0` is constant. The random surface rate satisfies uniformly

\[
0\le k_\omega(s)\le K_0,\qquad
\int_\Gamma k_\omega(s)\,ds\ge\kappa>0.
\tag{1}
\]

Only the rate is random; the bulk geometry, velocity and affinity are fixed. Thus `Z=A+KP`, the mean tracer velocity `V`, and

\[
B=KV^2/Z
\]

are independent of the realization. Assume `V!=0`, so `B>0`.

A policy observes a specified random signal `Y` and selects a nonnegative integrable coefficient `D_Y` with `int D_Y=M` for every observation. The signal may contain no information, the exact realization, a bin label, or a noisy observation. Its law may also vary with the budget. The admissible design class must allow mixing with the uniform coefficient; the unrestricted class used in this repository does.

For fixed `q>0`, define

\[
F_q(M;Y)=\inf_{\text{policies based on }Y}
\mathbb E[J_{k_\omega}(D_Y)^q],
\]

\[
G_q(M;Y)=\inf_{\text{same policies}}
\mathbb E[D_{\rm flow}(D_Y,k_\omega)^q].
\]

The scalar functional uses its smooth-test variational definition, permitting infinite values. For arbitrary designs the full variational lower bound gives `D_flow>=BJ`. For positive-background designs, the finite-response Schur identity gives

\[
D_{\rm flow}=BJ+R,\qquad R\ge0.
\]

By [the general logarithmic bulk lemma](review-risk-sensitive-finite-bulk.md), if `D>=m>0`, then

\[
R\le C[1+\log_+(1/m)]
\tag{2}
\]

in fixed nondimensional units. Its constants are uniform in the rate realization and do not depend on mobility derivatives or its upper bound. The one-dimensional wall and the uniform assumptions in (1) are essential to this application.

## A mixture at the same budget

Take any admissible scalar policy at budget `M`, and choose `0<theta<1`. Define

\[
D_Y^\theta=(1-\theta)D_Y+\theta M/P.
\tag{3}
\]

This policy uses exactly the same observation and has exactly the same budget. It has a deterministic positive floor `theta M/P`.

For a test field `f`, write

\[
Q_{D,k}[f]=\int D|f'|^2+\int kf^2.
\]

The reaction term is included once in the exact identity

\[
Q_{D^\theta,k}
=(1-\theta)Q_{D,k}+\theta Q_{M/P,k}
\ge(1-\theta)Q_{D,k}.
\]

The quotient form of the scalar variational principle therefore yields

\[
\boxed{J_k(D^\theta)\le\frac{J_k(D)}{1-\theta}.}
\tag{4}
\]

This inequality is valid for arbitrary integrable original designs, including degenerate or unbounded coefficients, with the usual extended-value interpretation. The mixed design has a positive background, so the bulk lemma applies to it without needing any estimate for the original design's bulk remainder.

Set

\[
L_\theta(M)=1+\log_+\!\left(\frac P{\theta M}\right).
\]

Combining (2) and (4) gives, realization by realization,

\[
D_{\rm flow}(D_Y^\theta,k_\omega)
\le\frac{B}{1-\theta}J_{k_\omega}(D_Y)+C L_\theta(M).
\tag{5}
\]

## Finite-budget comparison of optimal values

The unrestricted lower bound is

\[
B^qF_q(M;Y)\le G_q(M;Y).
\tag{6}
\]

Choose policies approaching the scalar infimum and apply (5). For `q>=1`, Minkowski's inequality gives

\[
\boxed{G_q(M;Y)^{1/q}
\le\frac B{1-\theta}F_q(M;Y)^{1/q}+C L_\theta(M).}
\tag{7}
\]

For `0<q<1`, subadditivity of the power function gives

\[
\boxed{G_q(M;Y)
\le\left(\frac B{1-\theta}\right)^qF_q(M;Y)
+C^q L_\theta(M)^q.}
\tag{8}
\]

No optimizer needs to exist; the inequalities follow by sending the approximation error of a near-optimal scalar policy to zero. The constants are independent of the observation rule. Additional bounded nonnegative contributions to axial diffusivity can be absorbed into the additive constant.

## Exact transfer theorem

Suppose along the budgets and observation rules under consideration that the scalar optimum is finite and

\[
\frac{F_q(M;Y)}{[1+\log(1/M)]^q}\longrightarrow\infty.
\tag{9}
\]

Choose, for example, `theta=M` when `0<M<1/2`. The floor is then `M^2/P`, and `L_theta(M)=O(log(1/M))`. Equations (6)–(8) prove

\[
\boxed{G_q(M;Y)\sim B^qF_q(M;Y).}
\tag{10}
\]

A divergent regularly varying power law satisfies (9), as do all polynomial moment orders proved in this repository. The theorem also applies when the observation rule changes with `M`, since the mixture compares scalar and full values at the identical budget and identical information. It does not require comparing observation rules or optimal values at different budgets.

Thus an established scalar sharp constant transfers with the factor `B^q`. If only scalar order bounds are established, (10) transfers those orders and identifies the ratio of the two optimal values; it does not create a previously unknown scalar leading constant.

## Uniformity over all observation rules in the cosine model

For `k_c=(c+cos s)^2` with `c` uniform on `[-2,2]`, the growth condition holds uniformly over every observation rule, including perfect information.

A direct lower bound avoids any information-specific theorem. On a fixed positive-probability set of offsets with a root, choose one root `r` and a smooth nonnegative bump `f(s)=psi((s-r)/ell)`, with `ell=M^(1/5)`. The cosine Lipschitz bound gives `k_c(s)<=C(s-r)^2` on its support, while every budget-`M` coefficient satisfies

\[
\int D|f'|^2\le CM/\ell^2,\quad
\int k_cf^2\le C\ell^3,\quad
\int f\asymp\ell.
\]

The scalar quotient therefore gives `J_c(D)>=cM^(-1/5)`, uniformly on that offset set and for every design. Raising to the positive power and averaging yields

\[
F_q(M;Y)\ge c_qM^{-q/5}
\tag{11}
\]

for every observation rule. The uniform design makes these optimal values finite. The constants in the bulk lemma are also uniform because `k_c<=9` and `int k_c>=P/2`.

With `theta=M`, the comparison consequently has the uniform quantitative form

\[
1\le\frac{G_q(M;Y)}{B^qF_q(M;Y)}
\le
\begin{cases}
1+C_qM^{q/5}[\log(1/M)]^q,&0<q<1,\\
1+C_qM^{1/5}\log(1/M),&q\ge1,
\end{cases}
\tag{12}
\]

for sufficiently small budgets, with fixed `B>0`. The harmless `O(M)` mixture error is absorbed into these bounds. Uniformity here refers to the observation structure; it does not assert a uniform bulk correction for all unmixed candidate designs.

## Consequences for existing research records

The sharp blind and adaptive scalar constants in [robust-mobility-design.md](robust-mobility-design.md) transfer directly by (10). Their explicit-design bulk estimates remain useful stronger statements about those particular trials, but are not needed to prove leading optimal-value transfer.

The positive moment orders and the critical `8/5` threshold in [risk-sensitive-mobility.md](risk-sensitive-mobility.md) also transfer. For compact generic rate families satisfying (1), the same theorem applies whenever their scalar optimal values satisfy (9), including the polynomial orders under study for generic folds.

For the finite-precision policy in [finite-precision-mobility.md](finite-precision-mobility.md), (12) is uniform in the bin width, even if it varies with the budget. Writing its scalar mean optimum as `Phi(M,Delta)` and its full-bulk counterpart as `Phi_bulk`,

\[
\Phi_{\rm bulk}(M,\Delta)\sim B\Phi(M,\Delta)
\]

uniformly over the observation partitions covered by that model. Hence the independently reviewed two-parameter order

\[
\Phi(M,\Delta)\asymp M^{-1/5}+M^{-1/4}\Delta^{1/4}
\]

and the reviewed sharp fine- and coarse-resolution endpoint constants transfer unchanged apart from `B`. No claim about the still-unproved interior scalar crossover is added by this argument.

## Scope and review status

The policy class must remain admissible under (3). This is automatic for the current unrestricted nonnegative fixed-budget fields. Additional constraints that exclude a uniform positive background or the mixture need separate treatment. A fixed zero mean velocity, loss of a uniform positive integral of the rate, higher-dimensional walls, or bulk diffusivity tending to zero also falls outside the stated theorem.

The transfer concerns optimized values. It does not prove convergence of original optimizing profiles, a uniform remainder for arbitrary designs, or realizability of the limiting designs under fabrication constraints. The uniform background can carry a vanishing fraction of the budget while regularizing the transverse problem.

The mixture inequality and same-information argument were independently checked by `review_localization` and the parent. They follow from standard order properties of positive quadratic forms and elementary moment inequalities. No novelty claim is made for those general tools or for this transfer corollary.
