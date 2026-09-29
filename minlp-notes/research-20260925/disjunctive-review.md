# Independent review of path moment claims

Reviewed on 2026-09-25. This is an adversarial check of three proposed claims,
not a claim that the consequences below are new.

All three claims survive, with two important qualifications: the path-three
relaxation uses a **full** moment matrix and RLT constraints on the missing edge;
the path-four obstruction quantifies over a cut family fixed before the objective
is selected. The current version of the first cited paper is v3, not v2.

For a graph \(G=(V,E)\), write

\[
\mathcal M_G=\operatorname{conv}\{((z_i)_i,(z_i^2)_i,
 (z_i z_j)_{ij\in E}):z\in[0,1]^V\}.
\]

Thus “path moment hull” means a projection of the full quadratic moment hull;
it retains every individual square but only the edge products.

## The two-bag witness is correct

For the path \(a-x-b\), prescribe

\[
E x=\tfrac12,\quad E x^2=\tfrac5{16},\quad
E a=E a^2=\tfrac12,\quad E(xa)=\tfrac38,
\]
\[
E b=E b^2=\tfrac45,\qquad E(xb)=\tfrac12.
\]

The first bag has a representing distribution putting probability \(1/2\)
on each of \((x,a)=(1/4,0),(3/4,1)\). The second puts probabilities
\(1/5,4/5\) on \((x,b)=(0,0),(5/8,1)\). Exact rational arithmetic confirms
all the stated moments. Hence the point belongs to the intersection of the
two exact bag hulls with their common first and second moments identified.

Suppose a joint representing distribution existed. Because \(a,b\in[0,1]\),
the equalities \(E a^2=E a\) and \(E b^2=E b\) force \(a,b\in\{0,1\}\)
almost surely. Direct expansion gives

\[
E(x-\tfrac14-\tfrac12a)^2=0,
\qquad E(x-\tfrac58b)^2=0.
\]

Therefore \(x\in\{1/4,3/4\}\) and \(x\in\{0,5/8\}\) almost surely.
The sets are disjoint, a contradiction. The containment is strict.

There is also an exact explanation of how the full SDP detects this point.
The centered covariance data are

\[
\operatorname{Var}(x)=\tfrac1{16},\quad
\operatorname{Cov}(x,a)=\tfrac18,\quad
\operatorname{Cov}(x,b)=\tfrac1{10}.
\]

Both relevant Cauchy–Schwarz inequalities hold with equality. In any PSD
completion, equality forces the centered vectors for \(a\) and \(b\) to
be multiples of that for \(x\). Consequently

\[
E(ab)=\tfrac12\cdot\tfrac45+
\frac{(1/8)(1/10)}{1/16}=\tfrac35.
\]

This violates the missing-edge RLT inequality \(E(ab)\le E(a)=1/2\).
Pairwise moment consistency therefore fails even though a full PSD
completion exists; the missing-edge box constraint matters.

## The path-three exactness corollary is valid

[Burer–Natarajan v2, Theorem 1](https://arxiv.org/html/2504.03996v2)
proves exactness for \(n\le3\) of

\[
\min\{Q\mathbin\bullet X+c^Tm:
Y=\begin{pmatrix}1&m^T\\m&X\end{pmatrix}\succeq0,
\ X_{ij}\le m_i\quad\forall i,j\},
\]

when every off-diagonal entry of \(Q\) is nonpositive. Its hypotheses impose
no sign condition on diagonal entries or linear coefficients.

Let \(R_3\) be full PSD plus all four RLT inequalities, including diagonal
upper inequalities:

\[
0\le X_{ij},\quad m_i+m_j-1\le X_{ij},\quad
X_{ij}\le m_i,\quad X_{ij}\le m_j.
\]

For every linear functional on the path coordinates, its value on rank-one
points is a quadratic with only the edges \(ax\) and \(xb\). Choose signs
\(s_i\in\{-1,1\}\), recursively along this path, such that each nonzero
edge coefficient times \(s_i s_j\) is negative. The substitution
\(z_i=d_i+s_i w_i\), where \(d_i=0\) for \(s_i=1\) and \(d_i=1\) for
\(s_i=-1\), complements selected box coordinates and makes the objective
submodular. It creates only linear and constant terms besides the same
quadratic edges. In particular, arbitrary diagonal coefficients cause no
problem.

This substitution maps \(Y\) by the invertible congruence

\[
Y\longmapsto TYT^T,\qquad
T=\begin{pmatrix}1&0\\d&\operatorname{Diag}(s)\end{pmatrix}.
\]

It preserves PSD and permutes the four linearizations of products of
\(z_i,1-z_i,z_j,1-z_j\). Thus it preserves the full RLT system. The
submodular exactness theorem applies to the weaker upper-RLT relaxation;
inserting the valid lower RLT inequalities preserves exactness by a
sandwich argument. Transforming back gives equality of the true and
relaxed minimum for every linear functional on the path coordinates.

Finally, \(R_3\) is compact: PSD and \(X_{ii}\le m_i\) imply
\(m_i^2\le X_{ii}\le m_i\), hence \(0\le m_i\le1\), and PSD bounds
every \(X_{ij}\). Both its path projection and \(\mathcal M_{P_3}\) are
compact convex sets. Equality of all linear minima, or finite-dimensional
strict separation, proves

\[
\pi_{P_3}(R_3)=\mathcal M_{P_3}.
\]

This does not assert that edge-only PSD and edge-only RLT suffice. The
preceding witness disproves that stronger assertion. It also does not
assert equality of the full three-variable moment hull and \(R_3\).

The [current v3](https://arxiv.org/html/2504.03996v3) adds Rick Willemsen as
an author and adds “Pricing” to the title. It retains the low-dimensional
theorem and gives a four-variable counterexample. The all-dimensional
exactness conjecture in v2 is therefore superseded.

## The finite-cut obstruction retains path-four sparsity

[Zhang–Wang v1](https://arxiv.org/html/2609.03617v1), equation (5), has
\(Q\) supported on \(12,23,34\). In their finite-cut argument, equation
(10) changes only \(Q_{44}\), and Lemma 2 changes only \(c_3,c_4\).
Thus Theorem 2's construction remains supported on that path. Its
quantifiers are

\[
\text{for every fixed finite family of box-valid linear cuts,}
\quad\text{there exists a path-supported submodular objective with a gap.}
\]

A single fixed objective cannot defeat every possible valid cut: its
optimal-value inequality is itself one such cut. The theorem concerns
one basic lifted PSD matrix plus finitely many linear inequalities, not
arbitrary SDP extensions, higher-degree moments, or adaptive algorithms.

An independent exact-arithmetic check verified both published rational
certificates. All 31 principal minors of each \(5\times5\) moment matrix
are nonnegative. For Appendix A, the six weights sum to one, reproduce
the first and off-diagonal moments, and give objective \(-1/100\);
the diagonal upper RLT constraints also hold. For Appendix B, its three
conic atoms reproduce \(\Psi\) exactly, and at \(\eta=1/100\) its
objective minus the true optimum is \(-173/28800<-1/200\).

The source's quantitative lower bound was read but not independently
reproved here. The qualitative obstruction follows from its checked
certificate, the stated perturbation, and the finite-zero-set argument.

## Significance and verification limits

The pairwise witness is a useful warning against gluing continuous
distributions by finitely many moments. The path-three equality is a
short consequence of existing submodular SDP exactness, rather than a
substantial independent contribution. The path-four observation is a
sparsity consequence of an existing construction. These results justify
rejecting universal tree exactness for this relaxation; they do not
justify rejecting all useful tree algorithms or all stronger sparse
relaxations.

The exact checks are reproducible with
`python research-20260925/verify_disjunctive_review.py`. They check the
stated rational identities and certificate feasibility. They do not
certify the cited papers' full proofs, literature novelty, or practical
solver improvements. That targeted command passed on 2026-09-25.
A separate reviewer independently checked the path-three complement and
separation argument, conditional on the cited theorem's hypotheses; those
hypotheses were checked directly against Theorem 1. No project-wide
checks or CI inspection were run.
