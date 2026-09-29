# Two adjacent positive square coefficients defeat SDP–RLT

Research date: 2026-09-27. Status: exact counterexamples, with an
[independent review](positive-pair-review.md) and a
[separate prior-result audit](positive-pair-prior.md). This is a boundary
result derived from an existing counterexample, not a claimed major
original contribution.

The [stable-positive theorem](stable-positive-submodular-exactness.md)
cannot be extended by allowing a matching among the positive diagonal
vertices. A four-variable submodular quadratic on a path already has a
strict gap for full SDP–RLT when only the two middle square coefficients
are positive. Its continuous two-variable block is jointly convex. A
second exact witness survives every valid linear inequality without
continuous diagonal moments, including all Boolean quadric polytope cuts.
The failure persists with a positive definite middle block and strictly
negative endpoint square coefficients.

## A quadratic with a direct nonnegativity proof

On \([0,1]^4\), let

\[
q(x)=x_2^2+x_3^2-x_1x_2-2x_2x_3-x_3x_4
       +\tfrac34x_1+x_2+\tfrac14x_4.
\tag{1}
\]

Every nonzero mixed coefficient is negative. The interaction graph is the path
\(1-2-3-4\), and the positive diagonal set is \(C=\{2,3\}\).
With the convention \(q=x^TQx+c^Tx\),

\[
Q_{CC}=\begin{pmatrix}1&-1\\-1&1\end{pmatrix}\succeq0.
\]

Put \(u=x_1,s=x_2,t=x_3,v=x_4\). The polynomial is affine in each
endpoint variable \(u,v\), so it is the bilinear interpolation of these
four nonnegative polynomials:

| \((u,v)\) | \(q(u,s,t,v)\) |
|---|---|
| \((0,0)\) | \((s-t)^2+s\) |
| \((1,0)\) | \((s-t)^2+3/4\) |
| \((0,1)\) | \((s-t+1/2)^2\) |
| \((1,1)\) | \((s-t)^2+1-t\) |

Consequently \(q\geq0\) throughout the box. Since \(q(0)=0\), its
minimum is exactly zero. The same conclusion holds if the endpoints
are required to be binary.

## A small rational full SDP–RLT witness

Write the moment matrix as
\(M=\begin{psmallmatrix}1&\mu^T\\\mu&X\end{psmallmatrix}\).
Full SDP–RLT imposes \(M\succeq0\) and

\[
\max(0,\mu_i+\mu_j-1)\leq X_{ij}\leq\min(\mu_i,\mu_j)
\qquad(1\leq i,j\leq4).
\tag{2}
\]

The rational point

\[
M=\frac1{45}
\begin{pmatrix}
45&8&15&30&37\\
8&8&8&8&6\\
15&8&11&15&15\\
30&8&15&26&30\\
37&6&15&30&37
\end{pmatrix}
\tag{3}
\]

satisfies (2). The leading principal minors of its unscaled matrix are
\(45,296,496,56,4\), all positive, so \(M\succ0\). Direct substitution
gives

\[
L_{\mu,X}(q)=-\frac1{60}<0.
\tag{4}
\]

Moreover, \(X_{11}=\mu_1\) and \(X_{44}=\mu_4\). Thus the witness
remains feasible after the usual binary diagonal equalities are imposed
on the endpoints. This rules out exactness of the two-center analogue of
the binary-leaf star moment formulation, even for a convex continuous
block. It also rules out a corresponding forest moment-hull extension:
any representing distribution for the coordinates used by (1) would
have nonnegative expected objective, contradicting (4).

## Even all off-diagonal Boolean cuts are insufficient

Consider the stronger rational point

\[
M=\frac1{400}
\begin{pmatrix}
400&152&165&235&248\\
152&152&144&152&144\\
165&144&144&165&165\\
235&152&165&214&227\\
248&144&165&227&248
\end{pmatrix}.
\tag{5}
\]

The leading principal minors before scaling are
\(400,37696,218664,124416,0\). The leading \(4\times4\) block is
positive definite, and its scalar Schur complement is zero. Hence
\(M\succeq0\). It satisfies (2), including the endpoint binary diagonal
equalities, and

\[
L_{\mu,X}(q)=-\frac1{200}.
\tag{6}
\]

Its means and off-diagonal moments have the following actual binary
distribution:

| Binary point | Probability |
|---|---:|
| \(0000\) | \(144/400\) |
| \(0001\) | \(21/400\) |
| \(0011\) | \(62/400\) |
| \(0111\) | \(21/400\) |
| \(1010\) | \(8/400\) |
| \(1111\) | \(144/400\) |

Therefore \((\mu,(X_{ij})_{i<j})\) belongs to the Boolean quadric
polytope. Every linear cut in these coordinates that is valid for all
box rank-one points is satisfied. This includes every triangle, cycle,
and clique inequality, irrespective of the number of such cuts added.
The distribution does not realize the two middle diagonal moments;
those are exactly the coordinates excluded from this statement.

The same argument permits endpoint diagonal terms in a cut when the
endpoints are binary: their moments equal their means in both (5) and
the displayed binary distribution. Thus strengthening only the Boolean
part of this mixed binary–continuous block cannot recover its hull.

## Linear gap on a single path with positive components of size two

For \(n=4k\), first sum \(k\) disjoint copies of (1). The true minimum
is zero. Take a copy of (5) for each block, and set all cross-block
second moments to products of their means. The resulting global
covariance matrix is block diagonal with PSD blocks, hence its augmented
moment matrix is PSD. The product of the six-atom binary laws realizes
every mean and off-diagonal moment globally. Thus all Boolean quadric
cuts still hold, while the relaxed value is \(-k/200=-n/800\).

One can also make the interaction graph a single path. Add the bridge
terms

\[
\frac1{1000}\sum_{j=1}^{k-1}x_{4j}(1-x_{4j+1}).
\tag{6a}
\]

Each is nonnegative on the box and vanishes at the origin, so the true
minimum stays zero. They connect consecutive four-vertex paths through
their endpoints, and their negative mixed coefficients preserve
submodularity. The set of positive diagonal vertices still induces a
matching. At the same product moment point, each bridge costs at most
\(1/1000\), so the relaxed value is at most

\[
-\frac{k}{200}+\frac{k-1}{1000}
\leq-\frac{k}{250}=-\frac n{1000}.
\]

In the convention \(q=x^TQx+c^Tx\), these connected instances satisfy
\(\max_{ij}|Q_{ij}|\leq1\) and \(\max_i|c_i|\leq1\). This is an
entrywise coefficient normalization, not the induced matrix norm.
The amplification is an elementary consequence of (5), not a separate
new gap mechanism. It shows that the local failure can accumulate even
on a connected path with positive components of size two.

## Strict curvature does not fix the gap

For \(\eta>0\) and \(\delta>0\), define

\[
q_{\eta,\delta}(x)=q(x)
 +\eta\{x_1(1-x_1)+x_4(1-x_4)\}
 +\delta(x_2^2+x_3^2).
\tag{7}
\]

All added terms are nonnegative on the box. Its unique global minimizer
is the origin: equality forces \(x_2=x_3=0\), after which
\(q=3x_1/4+x_4/4\) forces both endpoints to vanish.
The endpoint square coefficients are now \(-\eta\), while the middle
quadratic block has eigenvalues \(\delta\) and \(2+\delta\).

The endpoint perturbation has zero value at both moment witnesses.
At (3), choose \(\eta=1,\delta=1/100\); then

\[
L(q_{1,1/100})=-\frac1{60}+\frac{37}{4500}
             =-\frac{19}{2250}<0.
\]

At (5), choose \(\eta=1,\delta=1/200\); then

\[
L(q_{1,1/200})=-\frac1{200}+\frac{179}{40000}
             =-\frac{21}{40000}<0.
\tag{8}
\]

Thus the stronger obstruction, surviving all the Boolean cuts just
described, has a positive definite middle block, strictly concave
endpoints, and a unique true optimizer. It is not explained by a flat
objective or a singular conditional convex problem.

## What fails in the proposed extension

Partial minimization preserves submodularity here. Indeed, for a
submodular function \(f(x,z)\) on a product of lattices and attained
minima \(g(z)=\min_x f(x,z)\), choose minimizers \(x,x'\) at \(z,z'\).
Submodularity gives

\[
g(z)+g(z')\geq
 f(x\wedge x',z\wedge z')+f(x\vee x',z\vee z')
 \geq g(z\wedge z')+g(z\vee z').
\]

So the eliminated binary value function remains submodular even with
this two-variable continuous block. The missing step is exactness of
the local moment relaxation. Equations (5)–(6) disprove that step even
after the strongest possible Boolean moment inequalities are added.
Submodularity of the eliminated function alone cannot supply the local
SDP lower bound used in the stable-positive proof.

This does not establish that stability is necessary for every individual
instance, or characterize every graph class with uniform exactness.
An isolated two-variable component, for example, has an exact full
SDP–RLT hull. It also proves no optimization hardness: conditional
minimization of a convex continuous block and subsequent submodular
minimization remain available. A more powerful extended formulation
could still be exact.

## Prior work and significance

[Zhang–Wang, arXiv:2609.03617v2](https://arxiv.org/html/2609.03617v2#S3.SS2),
equation (5) and Proposition 2, supply the source family. Set their
\(a=b=1/2\), then replace the two endpoint square terms by their box
secants to obtain (1). Their optimal moment point has zero endpoint
diagonal slack, so its strict gap transfers. Their Proposition 3
already establishes a general obstruction to Boolean cuts with four
positive diagonals; (5) verifies the sharper two-positive pattern here.
The rational witnesses and strict-curvature modifications above are
useful explicit refinements, not an independent foundational example.

[Burer–Natarajan–Willemsen, arXiv:2504.03996v3](https://arxiv.org/html/2504.03996v3#S2.SS2),
Theorem 1, proves upper-RLT SDP exactness for all submodular quadratics
in at most three variables. Thus four variables are minimal for this
kind of submodular SDP gap. This statement is dimension minimality,
not a complete structural classification.

The [separate source audit](positive-pair-prior.md) also checks Tardella's
older tractability result. The useful consequence for the current
research is a precise stopping boundary: allowing interacting positive
pairs requires a genuinely stronger local formulation or a different
argument. The negative result itself does not improve a solver or
establish a new complexity frontier.

## Verification record

The exact command

```text
python research-20260927/check_positive_pair_frontier.py
```

checks all four endpoint identities, all 31 principal minors for each
matrix, every full RLT inequality, both objective values, the binary
mixture, and the strict-curvature perturbations. It passes. An
independent reviewer separately verified the claims; see the linked
review. Neither computation proves a general extension theorem.

A single exploratory CVXPY/CLARABEL solve with all 16 binary mixture
weights and endpoint diagonal equalities gave a value near
\(-0.00547916\) for (1). Its approximate moments suggested the support
used in (5); all final claims use the exact rational certificates.
No project-wide verification, CI inspection, or Lean check was run.
