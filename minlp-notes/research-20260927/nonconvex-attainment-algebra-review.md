# Independent review of the ordered-limit optimizer argument

Date: 2026-09-28.

This review concerns the algebra and limits in the proposed attained-optimizer
extension of [the finite-infimum proof](nonconvex-finite-infimum.md). It also
checks the common-field and rational univariate representation arguments in
[the nonconvex certificate proof](nonconvex-hessian-span-frontier.md),
Sections 6--7. It does not independently establish the underlying generic
KKT incidence bounds or make a novelty claim.

**Conclusion.** I found no gap in this extension, provided the proof explicitly
selects one nested vector tree and then one chart and active subset throughout
that tree. The coefficient extractions are, in order, the lowest power of
\(\eta\), the lowest power of \(\varepsilon\), and the highest power of
\(R\). These operations preserve the multiplier-based degree and coefficient
norm bounds. Exceptional specializations do not invalidate the extraction
identities.

## 1. The precise limit hypothesis

Fix finitely many rational outputs \(b_j/a\) of one polynomial root system
in \(s\) multiplier variables. Suppose there is a nested family with

\[
 R_\nu\longrightarrow+\infty,\qquad
 \varepsilon_{\nu,\mu}\longrightarrow0^+,
 \qquad \eta_{\nu,\mu,\kappa}\longrightarrow0^+,
\]

where the second limit is taken separately for each fixed \(\nu\), and
the third separately for each fixed \((\nu,\mu)\). At every leaf the
root Jacobian is nonsingular and \(a\ne0\). Require vector limits

\[
 w_{\nu,\mu,\kappa}\longrightarrow w_{\nu,\mu},
 \qquad w_{\nu,\mu}\longrightarrow w_\nu,
 \qquad w_\nu\longrightarrow w^*.
\]

No uniform rate between the three levels is needed. The same tree and
vectors must be used for every rational linear combination of the outputs.
Selecting unrelated coordinate limits would not justify a common-field bound.

A single chart and active subset can be retained in this tree. First pass to
a subsequence at each innermost level. At each middle level, retain one of
the finitely many labels on an infinite subsequence. Finally retain a label
on an infinite outer subsequence. Subsequences preserve all vector limits.

## 2. Why attainment supplies bounded outer vectors

Write \(S\) for the original closed feasible set in the original variable
\(x\), and suppose \(q_0\) attains its finite minimum \(\theta\).
The closed set \(\{x\in S:q_0(x)=\theta\}\) has a point \(x^*\)
of minimum Euclidean norm. Its existence follows by intersecting this set
with the closed norm ball of any one optimizer and using compactness.

For every sufficiently large box in lifted coordinates, the lift of \(x^*\)
belongs to that box. After taking \(\eta\to0\), any selected cluster
of perturbed minimizers minimizes

\[
 q_0(x)+\varepsilon\|x\|^2
\]

on the exact feasible set inside this box. The compact-box argument proving
this statement is the same as the inner-limit argument of the finite-infimum
proof: original feasible points satisfy the perturbed bands for sufficiently
small \(\eta\), and the perturbed objective converges uniformly on the
fixed box. Comparison with \(x^*\) gives

\[
 \theta+\varepsilon\|x\|^2
 \le q_0(x)+\varepsilon\|x\|^2
 \le \theta+\varepsilon\|x^*\|^2.
\]

Thus these inner limiting points satisfy \(\|x\|\le\|x^*\|\).
As \(\varepsilon\to0\), every cluster is an original optimizer of
minimum norm. Since every lifted coordinate is a fixed quadratic function
of \(x\), the whole lifted vector is bounded independently of the box.
An outer vector cluster therefore exists and is an original optimizer.

This argument requires attainment. A finite unattained infimum does not
supply a feasible comparison point with objective exactly \(\theta\).
It also uses ordered limits; it does not justify an arbitrary diagonal
choice of \(\eta,\varepsilon,R\).

## 3. Exceptional parameters and coefficient extraction

After choosing the generic integer perturbation, let a bad-set polynomial be
\(b(R,\varepsilon,\eta)\ne0\). Select a nonzero coefficient when it
is expanded in \(\varepsilon,\eta\). Its real roots exclude only
finitely many radii. At each retained radius, select a nonzero coefficient
in \(\eta\); its roots exclude finitely many values of
\(\varepsilon\). At each retained pair \((R,\varepsilon)\), the
remaining nonzero polynomial in \(\eta\) has only finitely many roots.
Applying this argument to the finitely many bad polynomials leaves sequences
at all three levels. Thresholds may depend on previously fixed parameters.

For the elimination itself, work over the coefficient ring
\(\mathbb Z[R,\varepsilon,\eta]\). The deformation, finite quotient,
and determinant of the finite-infimum proof work over this ring without
change. Removing the lowest \(\zeta\) and then lowest \(\delta\)
coefficient yields a nonzero polynomial

\[
 Q(R,\varepsilon,\eta,t)
\]

vanishing at every selected rational output. The nonsingular-root branch
and determinant factor argument applies separately at each parameter leaf.
If specialization makes an extracted coefficient identically zero, the
required vanishing identity still holds.

Write

\[
 Q=\eta^a Q_0(R,\varepsilon,t)+O(\eta^{a+1}),
 \qquad Q_0\ne0.
\]

Divide the leaf identity by \(\eta^a\), and take the inner limit with
\(R,\varepsilon\) fixed. This gives the identity for \(Q_0\) at
every inner vector output. Repeat using the lowest \(\varepsilon\)
power in \(Q_0\), obtaining a nonzero \(V(R,t)\) vanishing at the
middle limits. Finally write

\[
 V(R,t)=R^b P(t)+\sum_{j<b}R^jP_j(t),\qquad P\ne0.
\]

Divide by \(R^b\) and use convergence of the outer scalar output. Then
\(P(t^*)=0\). Polynomial evaluations in bounded convergent scalar outputs
are bounded, so the lower powers vanish after division. Every coefficient
extraction preserves the degree in \(t\) and cannot increase the
coefficient norm. No exclusion is needed merely because an elimination
coefficient has a zero specialization.

## 4. Common field and representation size

If all eliminated polynomials and outputs have multiplier degree at most
\(a\), the determinant bound is \(L=(a+1)^s\). Applying the argument
to the coordinates first shows that \(E=\mathbb Q(w^*)\) is a finite
extension of \(\mathbb Q\). Every rational linear combination of
\(w^*\) is another output along the same root tree, with the same degree
bound \(L\). Its coefficient norm may grow with the combination
coefficients, but its multiplier degree does not.

The primitive element theorem for this separable extension supplies one
rational linear combination generating \(E\). Its degree is at most
\(L\), hence \([E:\mathbb Q]\le L\). No multiplication of the
individual coordinate degrees is involved.

For a representation size bound, choose the combination coefficients from
\(\{0,\ldots,L(L-1)/2\}\). A product of the proper hyperplanes where
two embeddings agree has degree at most \(L(L-1)/2\); the elementary
grid argument yields a primitive combination within this range. The output
coefficient norm logarithm increases by at most
\(O(\log m+\log L)\), where \(m\) is the number of coordinates.
The same elimination bound therefore bounds the primitive element's
annihilator height. Minimal-polynomial factor bounds preserve polynomial
dependence on the degree and height bounds.

The trace-matrix argument in the nonconvex certificate proof then applies
unchanged. Scaling each coordinate and the primitive element by its minimal
polynomial's leading coefficient gives algebraic integers. Traces give an
integer linear system in the power basis. Separability makes its matrix
nonsingular; Cauchy's root bound and Cramer's rule bound the rational
coordinate coefficients. A rational isolating interval of polynomial bit
length identifies the intended real embedding. This establishes a common
rational univariate representation with the claimed degree and height scale.

## 5. Verification scope

This was a direct algebraic review of the displayed arguments and their
dependencies. No computation or formal proof assistant was used: neither
would replace the ordered-limit and common-field reasoning needed here.
The local checks run for this review file were a check of its final newline,
control characters, trailing whitespace, and local Markdown links, followed
by scoped `git diff --check`. No project-wide or CI verification was run.

## 6. Update after the two-limit simplification, 2026-09-28

I read Sections 2--6 of the revised
[attainment and optimizer proof](nonconvex-attainment-and-optimizer.md), and
also checked its common-field argument in Section 7. The triple-limit
argument reviewed above remains valid, but the revised proof does not need
it.

The simplification is sound. Comparison with a minimum-norm optimizer bounds
every exact minimizer of \(q_0+\varepsilon\|x\|^2\), for every
\(\varepsilon>0\), in one fixed compact set after lifting. Choose an unknown
box strictly containing that compact set. At each fixed admissible
\(\varepsilon\), every cluster of perturbed minimizers as \(\eta\to0\)
is an exact regularized minimizer and therefore lies strictly inside the
box. A contrary sequence of boundary minimizers would have a boundary
cluster by compactness. Thus every perturbed minimizer is eventually
strictly inside the box at that fixed \(\varepsilon\).

Consequently, the selected active affine charts come entirely from the
original polyhedron. The unknown radius appears in none of their
coefficients, the KKT equations, or the rational outputs. It requires no
encoding bound and no outer limit. Its sole role is to supply compactness
before the algebraic argument.

The revised common-field proof uses one shared nested vector tree, with
\(\eta\to0\) first and \(\varepsilon\to0\) second. Extracting the lowest
\(\eta\) coefficient and then the lowest \(\varepsilon\) coefficient
preserves the same degree and coefficient norm estimates. Exceptional
\(\varepsilon\) values are explicitly excluded in Section 3 of the main
proof. The primitive-element and trace-matrix arguments in Section 4 of
this review apply unchanged. I found no gap in the revised argument.

After this update, I reran this file's final-newline, control-character,
trailing-whitespace, and local-link checks and its scoped
`git diff --check`. All passed. No project-wide or CI checks were run.
