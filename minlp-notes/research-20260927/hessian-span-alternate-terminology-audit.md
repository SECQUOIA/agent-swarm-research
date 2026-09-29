# Hessian-span research: an audit under alternative terminology

Date: 2026-09-27. Status: independent literature and reduction audit. This
note narrows the possible contribution; it does not establish publication
priority or replace a proof review.

The strongest defensible addition in the current package is the passage from
many convex quadratic rows to an algebraic value bound controlled by the
linear span of their **native Hessian matrices**. Algebraic algorithms for
few quadratic forms, exact algorithms for small semidefinite descriptions,
algebraic separation followed by decision-query bisection, and compact
polyhedral approximations are established precedents. The inspected results
do not directly give the present parameterization. The missing ingredient
in the direct comparisons is the active affine restriction used in
[the value proof](hessian-span-reduction.md).

The comparison concerns rational convex quadratic inequalities with arbitrary
affine terms and affine side constraints, unrestricted ambient dimension,
and

\[
 h=\dim_{\mathbb Q}\operatorname{span}\{Q_1,\ldots,Q_m\}.
\]

In [the mixed-integer result](mixed-integer-span-frontier.md), the parameter
instead counts the continuous blocks \(Q_{i,xx}\), and the full Hessians
must still be positive semidefinite. Neither theorem assumes Slater or
genericity. Exact decision and preservation of integer assignments are
different from producing an exactly feasible rational continuous point.

## Few quadratic forms and low-dimensional quadratic maps

[Grigoriev and Pasechnik, *Polynomial-time computing over quadratic maps I:
sampling in real algebraic sets*](https://arxiv.org/pdf/cs/0403008v3),
Theorem 1.2, constructs real-univariate samples for
\(p(Q_1(x),\ldots,Q_k(x))=0\), with degree and integer coefficient-bit
bounds polynomial for fixed \(k\). No convexity is required. Theorem 1.5
also announces optimization with the same complexity, but its proof is
deferred. The present audit relies on the proved sampling theorem, rather
than assuming that the deferred proof has been located.

The parameter \(k\) counts complete quadratic-map components. A basis of
native Hessians is insufficient to represent all complete polynomials:
independent affine terms can add up to \(n+1\) directions. For example,
the polynomials

\[
 q_i(x)=\|x\|^2+2x_i-1,\qquad i=1,\ldots,n,
\]

have \(h=1\), while their complete coefficient vectors are linearly
independent. Thus the substitution \(k=h\) in the sampling theorem is
invalid before the active affine reduction. This calculation is part of the
present audit, not a claim made in the source.

The proof's active-system step has a precise role. At a chosen optimizer,
active quadratic rows have value zero. Subtracting their Hessian-basis
combinations gives affine equations that also vanish there. After imposing
those equations, the complete restricted quadratic polynomials span at
most \(h\) dimensions. Convexity ensures that deleting inactive rows has
not changed the minimum. The existing few-quadratic value lemma can then
be used. This is a concise alternative interpretation of the proposed
contribution, even though the main manuscript supplies its own regularized
KKT proof.

[Bienstock, Del Pia and Hildebrand, *Complexity, Exactness, and Rationality in
Polynomial Optimization*](https://arxiv.org/abs/2011.08347), Introduction,
explicitly warns that the cited Barvinok and Bienstock fixed-count results
do not automatically cover arbitrarily many linear inequalities and two
quadratic inequalities. Its local full text was independently inspected at
[the repository copy](../literature/papers/bienstock2023-complexity-exactness-and-rationality-in/fulltext.md).
This warning supports the parameter distinction; it is not itself a proof
that the proposed convex specialization is new. The local
[few-quadratic audit](few-quadratic-value-bound-evidence.md) covers
Kamminga–Rudolph and the precise quantitative elimination dependency.

## Small SDP descriptions and matrix pencils

[Porkolab and Khachiyan, *On the Complexity of Semidefinite Programs*,
DIMACS TR 96-18](https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/1996/96-18.html)
states exact feasibility of \(m\) scalar inequalities over
\(\mathbb S_+^r\) in
\(m r^{O(\min\{m,r^2\})}\) arithmetic operations on
\(\ell r^{O(\min\{m,r^2\})}\)-bit numbers. It also gives a feasible
solution magnitude bound. The primary report abstract was inspected;
this audit did not retrieve its FTP PostScript proof.

[Henrion, Naldi and Safey El Din, *Exact algorithms for linear matrix
inequalities*](https://perso.lip6.fr/Mohab.Safey/Articles/HNS_siopt16.pdf),
Theorem 3, gives an exact algebraic feasibility algorithm under explicit
smoothness, radicality and dimension assumptions on incidence varieties.
Its arithmetic complexity is polynomial when the pencil's variable count
or matrix size is fixed. Absence of interior points is allowed; the stated
genericity assumptions must still be retained.

These parameters do not become fixed merely because \(h\) is fixed.
In the example \(q_i(x)=\|x\|^2+2x_i-1\), the augmented symmetric
coefficient matrices

\[
 B_i=\begin{pmatrix}I_n&e_i\\e_i^T&-1\end{pmatrix}
\]

are linearly independent: their last columns already force every coefficient
of a zero linear combination to vanish. A standard exact convex lift uses
\(Y=\left(\begin{smallmatrix}X&x\\x^T&1\end{smallmatrix}\right)
\succeq0\) and retains the scalar affine and quadratic rows. Its matrix
size, scalar constraint count and complete coefficient span can all grow.
Exactness of that lift follows from
\(X-xx^T\succeq0\) and \(Q_i\succeq0\); exactness does not supply
the missing fixed parameter.

Likewise, low rank of a pencil is not implied by low dimension of its
coefficient span: \(\eta I_n\) has one coefficient matrix and can have
rank \(n\). These observations rule out the immediate parameter
substitutions. They do not rule out a more sophisticated reduction to an
older SDP theorem.

## Simultaneous diagonalization and hidden convexity

[Jiang and Li, *Simultaneous Diagonalization of Matrices and Its Applications
in Quadratically Constrained Quadratic Programming*](https://rjjiang.github.io/papers/SIOPT_SD.pdf),
Section 4, gives LP reductions under simultaneous diagonalization by
congruence. For nonhomogeneous polynomials the relevant hypothesis involves
the augmented matrices and the additional homogenizing normalization
matrix. A bound on native Hessian span does not impose that hypothesis.
This primary-source comparison was checked by a fresh subreview.

Even simultaneous diagonalization of the native Hessians would not solve
the exact precision question for arbitrary many independent diagonal forms:
the square-root-sum construction in
[the earlier audit](hessian-span-prior.md) already has diagonal Hessians.
Conversely, fixed matrix span does not imply simultaneous diagonalization.
For example \(I_2\), \(e_1e_1^T\), and
\((1,1)(1,1)^T\) span a three-dimensional space and cannot all be
diagonalized by congruence. Normalizing the positive definite first matrix
would give an orthogonal simultaneous diagonalization of the other two,
which is impossible because they do not commute.

[Jeyakumar and Li, *Trust-region problems with linear inequality constraints:
exact SDP relaxation, global optimality and robust optimization*](https://archive.ymsc.tsinghua.edu.cn/pacm_download/351/11861-Jeyakumar-Li2014_Article_Trust-regionProblemsWithLinear.pdf),
Section 6, considers uniform convex quadratic constraints
\(\|Bx\|^2+b_i^Tx-\beta_i\), along with a ball and a possibly
nonconvex objective. Proposition 6.1 imposes an eigenvalue/kernel dimension
condition and proves convexity of an augmented joint range. This is relevant
shared-Hessian prior, but it neither states the present arbitrary fixed-span
class nor provides its uniform coefficient-height bound. The theorem's
exact relaxation conclusion should not be conflated with exact finite-bit
feasibility.

The family
\(Q(t)=\left(\begin{smallmatrix}1&t\\t&t^2\end{smallmatrix}\right)
\otimes I_r\), discussed in
[the package assessment](hessian-package-assessment.md), gives a stronger
distinction from bounded PSD-generator lifts than a diagonal moment curve.
For distinct \(t\), its ranges intersect only at zero. Every PSD summand
used positively to represent \(Q(t)\) must have its range inside that
range. Hence \(m\) such matrices require at least \(m\) nonzero PSD
generators, although their matrix span has dimension at most three. A claim based
only on extreme rays of the cone of the *input* matrices would be weaker:
external PSD generators can compress some such cones.

## Error bounds and singularity

[Wang and Pang, *Global error bounds for convex quadratic inequality
systems*](https://doi.org/10.1080/02331939408844003), Optimization 31 (1994),
1–12, gives a global error bound without a constraint qualification. The
primary abstract describes a residual exponent \(2^{-d}\), where \(d\)
is a degree of singularity bounded by the number of constraints. This audit
obtained the abstract, not the original full proof. Definitions and the
statement are also reproduced in
[Jiang and Li's trust-region error-bound paper](https://rjjiang.github.io/papers/EBKLTRS_mor.pdf),
Definitions 3.1–3.4 and Lemma 3.5; that reproduction is secondary evidence
for the 1994 theorem.

The inspected statements are not uniform encoding bounds for the error-bound
constant. Moreover, they assume a nonempty feasible set, whereas exact
decision needs a positive lower bound on the minimum violation of an
infeasible boxed system. Neither gap is closed merely by knowing a Hölder
exponent. This distinction leaves room for the present value-height result.
Whether a refined singularity analysis yields a simpler proof of that result
remains a reasonable question, not a settled non-equivalence claim.

## Classical algebraic separation and a simpler radius consequence

[Chandrasekaran and Tamir, *Optimization problems with algebraic solutions:
quadratic fractional programs and ratio games*](https://www.tau.ac.il/~atamir/opt_84.pdf),
Mathematical Programming 30 (1984), 326–339, already uses a bounded degree
and coefficient-height class of algebraic values, separation of its distinct
members, and decision-query bisection to isolate an optimum. Pages 326–328
were inspected visually from the scanned author copy, saved
[here](sources-span-alternate/chandrasekaran-tamir-1984.pdf).
Thus algebraic separation followed by exact threshold search is classical;
the relevant addition must be the new input-dependent bound and the class
to which it applies.

There is also a direct route from the proved GP sampling theorem to the
[removal of explicit continuous bounds](unbounded-hessian-span.md).
This is an inference made in this audit:

1. Minimize \(\|x\|^2\) over a nonempty, closed convex quadratic
   system. A closest point \(x^*\) exists by coercivity.
2. Perform the active deletion and affine restriction from the candidate
   proof. The reduced convex problem still has minimum norm
   \(\|x^*\|\). Parameterize its rational affine space as
   \(x=x_0+Vu\), with polynomial-bit rational coefficients. Impose
   equality for a basis of at most \(h\) active quadratic polynomials.
3. The resulting real algebraic set contains \(x^*\), and every point
   of it belongs to the reduced convex system. Apply GP in the free
   coordinates, with \(p(Y)=\sum_jY_j^2\). A sample from that set
   therefore gives an upper bound on \(\|x^*\|\), even if the sample
   violates some of the deleted original rows.
4. GP's polynomial degree and height for fixed \(h\), followed by an
   elementary coordinate root bound and the rational affine map back to
   \(x\), makes this upper bound \(2^{L^{O(h+1)}}\).

If the restricted affine space has dimension zero, its rational point has
polynomial encoding directly. If no nonzero quadratic remains, choose the
zero free-coordinate vector. These cases do not require the sampling theorem.

For the last step, a real-univariate coordinate is a quotient
\(g_j(\alpha)/g_0(\alpha)\). GP's definition (1.1) explicitly requires
its root polynomial \(f\) and denominator \(g_0\) to be coprime.
Consequently \(\operatorname{Res}_T(f(T),Zg_0(T)-g_j(T))\) is a
nonzero polynomial annihilating that coordinate. Determinant and Cauchy
bounds give the claimed magnitude bound with polynomial overhead. The
coprimality condition matters: a weaker unnormalized representation could
have irrelevant common roots that make this resultant identically zero.
The sample need not be an original feasible point, and this argument must
not be advertised as a feasible-point recovery algorithm.

This radius argument shows that the extension uses the same active affine
restriction plus a proved old sampling theorem. It is a useful consequence,
but should not be counted as a second independent algebraic discovery.

## Scope and conclusion

Queries covered few quadratic forms, quadratic-map output dimension,
linearly dependent Hessians, uniform quadratic systems, simultaneous
diagonalization, matrix pencils, fixed-size SDP, degree of singularity,
small solutions, and algebraic optimization. Existing audits cover the
strong one-row result of Del Pia, generic algebraic degree of
Nie–Ranestad, fixed-dimensional semialgebraic integer optimization, and
Kocuk's exact preservation of integer points by rational approximations.
Those comparisons should remain in the package.

No direct subsumption of the native-Hessian-span theorem was identified.
This is a bounded search outcome, not proof of novelty. The contribution
should be stated narrowly: an active affine restriction gives uniform
algebraic precision controlled by Hessian matrix span, which permits exact
continuous decision and exact preservation of integer fibers under an
established compact polyhedral approximation. Claims of a new general
few-quadratic algorithm, a new algebraic-separation mechanism, or a new
general integer-preserving approximation principle would overstate the
evidence.

Targeted verification: primary theorem/abstract inspection as specified
above; independent mathematical checks of the parameter examples and radius
reduction; a fresh subagent check of the SDP, simultaneous-diagonalization
and quadratic-image comparisons; and a separate fresh review of the
noncompact radius deduction and quotient-coordinate bounds. The latter
review prompted more precise affine-parameterization wording, with no
substantive gap found. A targeted Python check of this file's local links,
control characters, trailing whitespace and final newline passed. No
numerical tests, project-wide checks, CI inspection, or Lean verification
were used for this literature audit.
