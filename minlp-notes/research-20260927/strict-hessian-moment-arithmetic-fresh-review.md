# Fresh review of moment uniqueness and Gram certificate fields

Date: 2026-09-28. Status: independent full mathematical review completed;
no mathematical defect found in the stated results. The reviewer did not
develop the main construction, its maximal-rank field consequence, or its
facial-reduction consequence before this review.

I read the [main note](strict-hessian-moment-arithmetic.md), the
[first review](strict-hessian-moment-arithmetic-review.md), and the
Taylor lemma in the [descent audit](rational-sos-convex-descent-prior.md).
I reconstructed the proofs below without assuming that the first review
was correct. The source comparison was checked separately. These are
supporting structural consequences, not an independently established
new general theorem about exact SOS relaxations.

## The integrated Gram and its field

Write \(u=x-a\), where \(a\) is the unique minimizer. The rational
positive definite full Hessian Gram implies
\(\nabla^2F(x)\succeq cI\) for a constant \(c>0\). Consequently \(F\)
is coercive, attains its minimum, and has exactly one minimizer.
Its Hessian is nonsingular at that point, so the rational gradient
system has an isolated nonsingular complex zero there. In particular,
the coordinates of \(a\) are algebraic.

The translation of the Hessian Gram is an invertible congruence over
\(K=\mathbb Q(a)\). Choose a real \(\mu>0\) below its smallest
eigenvalue. Substitution \(v=u\), evaluation at \(tu\), and integration
against \(1-t\) give the two strictly positive terms

\[
 \frac{\mu}{2}\sum_i u_i^2+
 \frac{\mu}{12}\left(\sum_i u_i^2\right)^2.
\]

Their Gram is diagonal and positive definite on the complete list
\((u_i,u_iu_j)_{i\le j}\). The residual integral has a positive
semidefinite Gram on this list. Thus the directly integrated Gram is
positive definite. Its entries are in \(K\), because its integrand has
polynomial entries over \(K\) and integration only introduces rational
factors. The auxiliary eigenvalue \(\mu\) is used to prove positivity;
it is not part of the formula for the integrated matrix.

Translation from this list to the full quadratic monomial vector
\(b(x)\) has full row rank and kernel \(\mathbb R b(a)\). Therefore
the resulting Gram \(Q_*\) has precisely that kernel and rank \(N-1\).
Evaluation at \(a\) shows that every positive semidefinite Gram of
\(F-F(a)\) kills \(b(a)\), so this is the largest possible rank.
No square factorization over \(K\) is required for this argument.

## Every optimal moment is determined

The point moments at \(a\) are primal feasible, and \(Q_*\) is dual
feasible at the same value \(F(a)\). This proves both attainment and
equality of the optimal values without a separate duality theorem.

For any optimal moment matrix \(M\),
\(\operatorname{tr}(Q_*M)=0\). Two positive semidefinite matrices
with zero trace product satisfy \(Q_*M=0\): apply the trace to
\(Q_*^{1/2}M Q_*^{1/2}\). Hence the range of \(M\) is contained
in \(\mathbb R b(a)\). Its constant entry is one, so
\(M=b(a)b(a)^{\mathsf T}\). Every moment through degree four occurs
as an entry of this matrix. This establishes uniqueness of the entire
truncated sequence, not only uniqueness of its first moments.

The displayed rank-one moment matrix and \(Q_*\) are strictly
complementary. The Gaussian construction gives primal Slater
feasibility. The matrix
\(Q_*+\varepsilon e_0e_0^{\mathsf T}\), where \(e_0\) is the constant
coordinate vector and \(\varepsilon>0\), is positive definite because
\(e_0^{\mathsf T}b(a)=1\). It represents
\(F-F(a)+\varepsilon\) and gives dual Slater feasibility.
These statements concern the optimization pair; the optimal-level
Gram feasibility problem cannot be strictly feasible in the full cone.

## Maximal rank recovers exactly the optimizer field

If an \(L\)-valued Gram has rank \(N-1\), its kernel is the line
\(\mathbb R b(a)\). Elimination over \(L\), followed by normalization
of its nonzero constant coordinate, gives \(b(a)\in L^N\).
In particular \(K\subseteq L\). Conversely the integrated construction
provides such a Gram over \(K\). This proves the least-field statement
under inclusion, rather than only a degree bound.

For the rational rank bound, let
\[
 r=\dim_{\mathbb Q}\operatorname{span}_{\mathbb Q}
       \{a^\alpha:|\alpha|\le2\}.
\]
The rational linear map from \(\mathbb Q^N\) to this span, sending
a coefficient vector to its value at \(a\), has rank \(r\).
Every row of a rational Gram belongs to its kernel. Its row rank,
and hence its real matrix rank, is at most \(N-r\). This gives a
second proof of the bound without choosing basis coordinates.

There is no assertion that the upper bound is attainable, that a
rational optimal Gram exists, or that a Gram over \(K\) has an
unweighted square factorization over \(K\). All three distinctions
are necessary.

## The exposing matrix and rational facial reduction

The presence of \(Q_*\), with exactly a one-dimensional kernel,
determines the minimal real PSD face of the entire optimal Gram set:
\[
 \mathcal F_a=\{Q\succeq0:Qb(a)=0\}.
\]
If a positive semidefinite \(Z\) has zero trace product with every
optimal Gram, it has zero trace product with \(Q_*\). Thus
\(\operatorname{range}Z\subseteq\mathbb R b(a)\), which forces
\(Z=c\,b(a)b(a)^{\mathsf T}\), with \(c\ge0\). If \(c>0\), the
ratios of its first row to its constant entry recover all coordinates
of \(a\). Every such exposing matrix therefore has coefficient field
containing \(K\), and \(c=1\) attains that field.

The matrix \(b(a)b(a)^{\mathsf T}\) is an admissible facial-reduction
certificate, not merely an arbitrary exposing matrix. If
\(\mathcal A\) maps a symmetric matrix to the polynomial coefficients
of \(b^{\mathsf T}Qb\), then
\[
 \mathcal A^*(y^a)=b(a)b(a)^{\mathsf T},\qquad
 \langle y^a,\operatorname{coef}(F-F(a))\rangle=0.
\]
It performs one real reduction to \(\mathcal F_a\), where \(Q_*\)
is relatively strictly feasible. There is no reduction of length zero,
because all feasible Grams are singular. The real singularity degree
is exactly one.

When \(a\) is irrational, there is no nonzero rational positive
semidefinite exposing matrix preserving all real feasible Grams.
This is stronger than merely failing to find a rational multiplier
for a particular representation of the affine equations. It does not
exclude rational restrictions that preserve only rational candidates.
Such restrictions can discard \(Q_*\).

There is one useful data distinction. The original optimization
programs have rational data for every rational \(F\), but their
optimal-level affine Gram equations have rational right-hand side
only if \(F(a)\in\mathbb Q\). If \(F(a)\notin\mathbb Q\), a rational
optimal Gram is already impossible by the constant coefficient.
The cited cyclic and descent examples have minimum zero, so they
realize the facial-reduction obstruction even when the optimal-level
Gram equations are rational.

## What the full Hessian assumption does and does not mean

I checked the main counterexample
\(F(x,y)=x^2+y^2+y^4\) directly. Its Hessian is
\(\operatorname{diag}(2,2+12y^2)\). With quadratic basis
\((1,x,y,x^2,xy,y^2)\), the matrix
\(\operatorname{diag}(1,0,0,t,0,0)\), for any \(t\ge0\), is a
consistent feasible moment matrix of objective zero. Thus strong
convexity and SOS-convexity alone do not give the claimed moment
uniqueness.

The full positive definite Hessian Gram is a sufficient condition,
not a necessary characterization of uniqueness. For example
\[
 \widehat F(x,y)=x^2+y^2+x^4+y^4
\]
has no such full Hessian Gram: the coefficient of \(x^2v_y^2\) in
its Hessian biform is zero, whereas a positive definite full Gram
would make the corresponding diagonal entry strictly positive.
Nevertheless \(\widehat F\) has a positive definite Gram on
\((x,y,x^2,xy,y^2)\): take \(I_2\) on the linear coordinates and
\[
 \begin{pmatrix}
 1&0&-1/2\\
 0&1&0\\
 -1/2&0&1
 \end{pmatrix}
\]
on the quadratic coordinates. The latter eigenvalues are
\(1/2,1,3/2\), and its polynomial is \(x^4+y^4\).
The same complementarity proof gives unique optimal moments.
The main note's wording that the hypothesis is material is correct;
it should not be strengthened to necessity.

## Prior comparison and significance

I read the primary passages of
[Lasserre, arXiv:0806.3784v3](https://arxiv.org/pdf/0806.3784):
Theorem 2.6 gives the functional Jensen inequality, and Theorem 3.3
gives exactness, attainment, and extraction from first moments in
SOS-convex optimization under its assumptions. The current argument
uses the stronger Gram hypothesis to determine all moments and the
complete optimal Gram kernel. It should not be described as a new
general exactness theorem.

I also read
[Laplagne, arXiv:1810.04215v1](https://arxiv.org/pdf/1810.04215),
Sections 3.1--3.2 and Proposition 3.4. Real zeros supply Gram
kernel vectors; rational Grams must additionally annihilate their
algebraic conjugates, and field traces produce rational relations.
The rational rank bound is a dimension consequence of this established
mechanism. Appendix A.3 explicitly separates real SOS testing from
the trace restrictions for rational candidates. Thus the distinction
between the two feasibility questions is established prior as well.

[Chua--Plaumann--Sinn--Vinzant, arXiv:1608.00234v3](https://arxiv.org/pdf/1608.00234),
Lemma 1.6 and Remark 1.7, support the rational Gram/SOS equivalence
and the caveat about general number fields. The claim about Gram
entries is the appropriate one.

I checked the introduction and Theorem 1.1 of
[Kolmogorov--Naldi--Zapata, arXiv:2405.13625v3](https://arxiv.org/pdf/2405.13625).
Their algebraic certification method already allows irrational
feasible points and uses a nearby maximum-rank point. The note
identifies the exact field that such a point must contain in the
present examples; it does not introduce algebraic SDP certification.

A separate primary-source subreview found two additional close
comparisons, whose passages I then inspected.
[Dostert--de Laat--Moustrou, Sections 3.2--3.4](https://optimization-online.org/wp-content/uploads/2020/01/7553.pdf)
base exact rounding on recovering kernel bases over the chosen field
and explicitly discuss the rational-kernel requirement and extension
to quadratic fields.
[Bhardwaj, Section 4](https://link.springer.com/article/10.1007/s10957-023-02258-5)
already warns that irrational zeros can obstruct the facial-reduction
and rationalization methods considered there. This is close qualitative
prior, not the exact exposing-ray field statement. Its wording about
irrational zeros should not be read as excluding the rational-candidate
restrictions that Laplagne describes.

The conjunction is useful: strict rational convexity, exact moment
relaxation, unique rank-one primal optimum, both Slater conditions,
real strict complementarity, and real singularity degree one can
coexist with mandatory nontrivial fields for maximum-rank Grams and
exposing matrices. The cyclic family transfers its exponentially
large optimizer field to those objects. These are precise consequences
of the separately verified family, not an additional complexity
lower bound or a proof that compact algebraic representations fail.
The contribution of this note is explanatory and structural. Priority
for the full conjunction remains unestablished.

Searches included combinations of “facial reduction,” “rational
exposing vector,” “irrational,” “maximal rank Gram,” “field,” and
“SOS-convex unique moment.” An unsuccessful search is not evidence
that no equivalent formulation exists.

## Verification limits

This review used exact Taylor identities, linear algebra, field
arguments, and the two explicit moment/Gram checks above. No numerical
SDP experiment, repeated construction checker, or Lean proof was run.
The exponential-degree examples and the non-rational-SOS construction
were used only through their already reviewed statements; their
large construction checks were not repeated here. No project-wide
test or CI inspection was performed.

Targeted checks run: an inline Python check passed for this file's
three local links, paired math delimiters, trailing whitespace, and
final newline. The scoped command

    git diff --check -- research-20260927/strict-hessian-moment-arithmetic-fresh-review.md

also completed without output; because this is a newly created file,
the Python content checks provide the actual untracked-file coverage.
