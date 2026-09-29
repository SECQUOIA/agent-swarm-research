# Analytic reductions for the four-variable star question

Research date: 2026-09-25. Status: partial sufficient conditions and explicit
limits of a proposed proof route. The unrestricted four-variable star case
remains unresolved here. None of the sufficient conditions below is claimed
to be new.

The question concerns minimization of

\[
q(t,y)=a t^2+b t+c+
\sum_{i=1}^{m}\bigl(d_i y_i^2+(e_i+f_i t)y_i\bigr)
\]

on \([0,1]^{m+1}\), using the full moment matrix
\(Y=\left(\begin{smallmatrix}1&\mu^T\\\mu&X\end{smallmatrix}\right)\succeq0\)
and every McCormick inequality, including diagonal upper bounds
\(X_{ii}\leq\mu_i\). The unresolved case is \(m=3\). A documented
[five-variable counterexample](star-hull-proof-exploration.md) has \(m=4\).

## The binary-center face is exact in every dimension

**Lemma.** On the face \(X_{tt}=\mu_t\), the projection of SDP–RLT onto
the first moments, individual squares, and center–leaf products equals
the moment hull of points with a binary center. There is no restriction
on the number of leaves.

**Proof.** Write \(p=\mu_t=X_{tt}\). If \(0<p<1\), set

\[
u_i=\frac{X_{ti}}p,
\qquad
v_i=\frac{\mu_i-X_{ti}}{1-p}.
\]

The center–leaf McCormick inequalities give \(u_i,v_i\in[0,1]\).
The PSD principal submatrix indexed by \((1,t,y_i)\) gives

\[
w_i:=p u_i^2+(1-p)v_i^2\ \leq\ X_{ii}\ \leq\mu_i.
\]

This follows either by its Schur complement or by nonnegativity of the
second moment of the residual from regressing \(y_i\) on the binary center.

Construct a random center \(T\sim\operatorname{Bernoulli}(p)\). If
\(\mu_i>w_i\), put

\[
\theta_i=\frac{X_{ii}-w_i}{\mu_i-w_i}\in[0,1].
\]

Conditional on \(T=1\), mix a deterministic leaf equal to \(u_i\) with a
Bernoulli variable of mean \(u_i\), giving the Bernoulli component weight
\(\theta_i\). Conditional on \(T=0\), use the same mixture with mean
\(v_i\). The conditional means are unchanged, while the unconditional
second moment is \(w_i+\theta_i(\mu_i-w_i)=X_{ii}\). If \(\mu_i=w_i\),
then \(X_{ii}=w_i\), and deterministic conditional leaves suffice.
Choose the leaves independently conditional on \(T\).

The resulting finitely supported distribution preserves every retained
moment. If \(p=0\) or \(p=1\), the center is deterministic and McCormick
forces \(X_{ti}=0\) or \(X_{ti}=\mu_i\), respectively. The same construction
reduces to mixing a deterministic leaf at \(\mu_i\) with a Bernoulli leaf
of that mean, since \(\mu_i^2\leq X_{ii}\leq\mu_i\). The reverse hull
inclusion follows because actual moments satisfy the relaxation.
\(\square\)

The proof only needs center–leaf McCormick constraints, diagonal upper
bounds, and the PSD matrices indexed by the constant, center, and one leaf.
It does not reconstruct the unused leaf–leaf moments, which do not occur
in the objective. This observation does not establish equality of the
full moment hull.

**Corollary.** If the center coefficient \(a\leq0\), SDP–RLT is exact for
the star, with arbitrary leaf curvatures and arbitrary linear and
interaction coefficients. If \(a>0\), an optimal relaxed pair satisfies

\[
0\leq q^*-q^*_{\rm SDP}
\leq a(\mu_t-X_{tt})\leq\frac a4.
\]

Indeed, increase \(X_{tt}\) to \(\mu_t\). This adds a nonnegative diagonal
matrix to \(Y\) and preserves every McCormick inequality. The lemma
provides an actual distribution whose objective differs from the original
relaxed objective by exactly \(a(\mu_t-X_{tt})\). Some point in the
distribution is no worse than its mean objective. For \(a\leq0\), this
proves exactness. For \(a>0\), use
\(0\leq\mu_t-X_{tt}\leq\mu_t-\mu_t^2\leq1/4\).

The same point-dependent rounding statement holds for every feasible
relaxed pair. For a center interval of width \(U-L\), the uniform bound
is \(\max\{a,0\}(U-L)^2/4\), with \(a\) the original center square
coefficient. This is a structural limitation on possible gaps, not a
claim that the bound is sharp or that it resolves the four-variable case.

The proof and its boundary cases received an independent delegated
adversarial check. The construction was then checked directly here.
No numerical calculation is needed. These observations are plausibly
standard consequences of convexification with a binary separator; their
novelty has not been established. Related decomposition theory appears
in [Khajavirad, Lemma 4, arXiv:2601.18545v1](https://arxiv.org/html/2601.18545v1),
where overlaps are required to have no positive loop; that result does
not resolve a positive-curvature center.

## A valid book-graph route when leaf bounds can be released

Here \(T_{m+2}\) denotes the book graph with two adjacent hubs and \(m\)
otherwise independent leaves, each adjacent to both hubs. The corrected
SPN-graph theorem establishes that \(T_5\) is SPN: every copositive
symmetric matrix supported on this graph is the sum of a PSD matrix and an
entrywise nonnegative matrix. See Shaked-Monderer's
[corrigendum](https://arxiv.org/abs/1712.05115), rather than the superseded
claim that all book graphs are SPN.

**Proposition.** Let \(m\leq3\). Suppose independent leaf complementations
can be chosen so that replacing all leaf domains \([0,1]\) by
\([0,\infty)\), while retaining \(t\in[0,1]\), does not change the true
minimum. Then full SDP–RLT is exact.

**Proof.** Leaf complementation preserves the star support, PSD, and full
McCormick system. Work in the chosen coordinates and write the common
minimum as \(v\). Homogenize \(q-v\) with two nonnegative hub variables
\(r,s\):

\[
h(r,s,y)=(r+s)^2
\left[q\left(\frac{s}{r+s},\frac{y}{r+s}\right)-v\right].
\]

For \(r+s>0\), the assumed bound release implies \(h\geq0\) on the
nonnegative orthant. Continuity gives this also when \(r=s=0\).
The coefficient matrix of \(h\) is supported on \(T_{m+2}\). Thus it has
an SPN decomposition. For \(m<3\), pad the matrix by isolated zero rows
and columns and apply the \(T_5\) result.

Substitute \(r=1-t\) and \(s=t\). The PSD part is a sum of squares of
affine functions of the original variables; its moment evaluation is
nonnegative. Every product in the entrywise nonnegative part is a product
of two entries of \((1-t,t,y_1,\ldots,y_m)\). Its moment evaluation is
nonnegative by PSD for squares and by McCormick for distinct factors,
including \(t(1-t)\). Therefore every SDP–RLT point has objective at least
\(v\). \(\square\)

A transparent sufficient condition for bound release is available when
every \(d_i>0\). Define the affine unconstrained leaf minimizer

\[
g_i(t)=-\frac{e_i+f_i t}{2d_i}.
\]

For each leaf, require either
\(\max_{t\in[0,1]}g_i(t)\leq1\) or
\(\min_{t\in[0,1]}g_i(t)\geq0\). In the first case keep the leaf as it is;
its minimizer over \([0,\infty)\) is \(\max\{0,g_i(t)\}\leq1\).
In the second case complement the leaf; its new unconstrained minimizer
is \(1-g_i(t)\leq1\), and the same argument applies. Consequently no
released leaf bound changes any fixed-center minimum. The condition means
that an individual unconstrained leaf response does not cross both ends
of the unit interval as the center varies.

This is a sufficient condition only. It excludes some simple objectives
whose SDP–RLT relaxation is exact.

## Why the bound-release bridge does not settle the question

Book-graph support alone does not make the homogenized matrix copositive.
For example, \(x^2-3x+2\geq0\) on \([0,1]\), but its value at
\(x=3/2\) is negative. Box nonnegativity and orthant nonnegativity are
different hypotheses.

Even optimizing the leaf orientation does not always justify releasing
leaf bounds. Consider the two-variable star

\[
q(t,y)=t^2+y^2-4ty+t+y
=(t-y)^2+t(1-y)+y(1-t).
\]

It is nonnegative on the unit square, has minimum zero at \((0,0)\) and
\((1,1)\), and has an immediate SDP–RLT certificate from the displayed
identity. Its unconstrained response is \(g(t)=2t-1/2\). If the upper bound
on \(y\) is removed, then \(q(1,3/2)=-1/4\). If \(y\) is complemented
before its upper bound is removed, the released domain in the original
coordinate is \(( -\infty,1]\), and
\(q(0,-1/2)=-1/4\). Thus neither orientation preserves the minimum.
Complementing the center simply swaps these two cases.

One possible stronger bridge would subtract a suitable nonnegative
combination of McCormick products before applying book-graph copositivity.
Such a bridge has not been proved. Corrections involving leaf–leaf
products generally destroy the book sparsity, so unrestricted SDP–RLT
duality does not by itself provide it.

Likewise, replacing the PSD moment matrix by a completely positive
completion on the \(T_5\) entries preserves nonnegative variables but does
not force the factors to satisfy their upper bounds. Adding vectors for
both \(y_i\) and \(1-y_i\) changes the relevant graph: the prescribed
center–leaf blocks become three copies of \(K_4\) sharing a hub edge.
The theorem for \(T_5\) cannot be applied directly to that graph.

## Remaining scope and literature check

These reductions leave a positive-curvature center with leaf bounds that
cannot be released. They do not prove that a nonpositive leaf coefficient
alone implies exactness, even though its square may be replaced in the
objective by a linear term plus a nonnegative diagonal RLT product.
Conditioning on a binary leaf would require second moments of the other
variables conditional on that leaf, which first-order moments do not
directly provide.

The current
[Burer–Natarajan–Willemsen paper, arXiv:2504.03996v3](https://arxiv.org/html/2504.03996v3)
proves submodular exactness in dimensions at most three; a star can be made
submodular by leaf complementations. This settles at most two leaves.
The explicit four-variable obstruction in
[Zhang–Wang, arXiv:2609.03617v1](https://arxiv.org/html/2609.03617v1)
has path support, as already examined in
[the repository review](disjunctive-review.md). It does not resolve the
four-variable star. The relevant corrected SPN result and the
five-variable star obstruction are compared in
[the star construction](star-hull-proof-exploration.md).

No additional random search was used in this investigation. Existing
negative random probes remain weak evidence; neither those probes nor
the absence of a located star theorem establishes exactness or novelty.

At batch completion, the separate directed search artifacts
`four_star_countersearch.py` and `four_star_countersearch_results.json`
record five search classes with 6,000 trials each and status
`no_candidate`. Saved near-zero numerical discrepancies do not certify
strict gaps; tighter solves can change their sign. The root inspected
these saved statuses but did not rerun the searches or independently
certify every trial. The exact four-variable question remains unresolved.
