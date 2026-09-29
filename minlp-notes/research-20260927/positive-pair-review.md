# Independent review: adjacent positive diagonal vertices

Research date: 2026-09-27. The stated counterexample and its strict
perturbation pass exact independent verification. This is a boundary
example derived from known work, not a claim of a new SDP gap construction.

## True optimum

Write the four variables as \((u,s,t,v)\in[0,1]^4\), and let

\[
q=s^2+t^2-us-2st-tv+\tfrac34u+s+\tfrac14v.
\]

The interaction graph is the path \(u-s-t-v\); all three mixed
coefficients are negative. Precisely the adjacent vertices \(s,t\)
have positive square coefficients. The square coefficients at \(u,v\)
are zero.

For fixed \(s,t\), the objective is affine in the endpoint variables
\(u,v\). The four endpoint restrictions are

\[
\begin{array}{c|c}
(u,v)&q(u,s,t,v)\\\hline
(0,0)&(s-t)^2+s\\
(1,0)&(s-t)^2+3/4\\
(0,1)&(s-t+1/2)^2\\
(1,1)&(s-t)^2+1-t.
\end{array}
\]

Each is nonnegative on the square. The general value is their convex
combination with weights \((1-u)(1-v),u(1-v),(1-u)v,uv\), so
\(q\geq0\) on the full box. Since \(q(0)=0\), the true minimum is zero.

## Rational relaxation witness

Use moment coordinates ordered as \((1,u,s,t,v)\), and put

\[
M=\begin{pmatrix}1&\mu^T\\\mu&X\end{pmatrix}
=\frac1{45}
\begin{pmatrix}
45&8&15&30&37\\
8&8&8&8&6\\
15&8&11&15&15\\
30&8&15&26&30\\
37&6&15&30&37
\end{pmatrix}.
\]

The leading principal minors of the integer matrix are
\(45,296,496,56,4\). Sylvester's criterion therefore proves
\(M\succ0\).

The table gives all full-RLT slacks, multiplied by 45. This includes
diagonal pairs, hence also the box-square upper bounds.

| Pair \(ij\) | \(45X_{ij}\) | \(45(\mu_i-X_{ij})\) | \(45(\mu_j-X_{ij})\) | \(45(1-\mu_i-\mu_j+X_{ij})\) |
|---|---:|---:|---:|---:|
| 11 | 8 | 0 | 0 | 37 |
| 12 | 8 | 0 | 7 | 30 |
| 13 | 8 | 0 | 22 | 15 |
| 14 | 6 | 2 | 31 | 6 |
| 22 | 11 | 4 | 4 | 26 |
| 23 | 15 | 0 | 15 | 15 |
| 24 | 15 | 0 | 22 | 8 |
| 33 | 26 | 4 | 4 | 11 |
| 34 | 30 | 0 | 7 | 8 |
| 44 | 37 | 0 | 0 | 8 |

Every slack is nonnegative. The relaxed objective is

\[
L_M(q)=\frac{11+26-8-30-30+6+15+37/4}{45}
=-\frac1{60}.
\]

Thus full SDP–RLT is not exact. The witness also satisfies the binary
diagonal equalities \(X_{11}=\mu_1\) and \(X_{44}=\mu_4\). Declaring
the outer variables binary does not repair this relaxation.

## Strict signs and a positive definite continuous block

More generally, for \(\eta>0\) and \(0<\tau<3/148\), put

\[
q_{\eta,\tau}
=q+\eta\bigl[u(1-u)+v(1-v)\bigr]+\tau(s^2+t^2).
\]

Every added term is nonnegative on the box, so the true minimum remains
zero. It is now attained only at the origin: a zero forces \(s=t=0\),
after which \(3u/4+v/4\) forces \(u=v=0\).
The outer square coefficients are \(-\eta<0\), and the inner quadratic
coefficient block is

\[
\begin{pmatrix}1+\tau&-1\\-1&1+\tau\end{pmatrix}\succ0,
\]

with eigenvalues \(\tau,2+\tau\). For the same rational moment point,

\[
L_M(q_{\eta,\tau})=-\frac1{60}+\frac{37\tau}{45}<0.
\]

In particular, \(\eta=1,\tau=1/100\) gives the exact value
\(-19/2250\). Hence the failure persists with strictly negative outer
square coefficients, a unique true minimizer, and a positive definite
continuous block. It is not caused by the zero outer square coefficients
or by singularity of the continuous block.

## A witness surviving all BQP valid cuts

The proposing agent subsequently supplied a second rational witness,
which also passes independent exact verification:

\[
\widetilde M=\frac1{400}
\begin{pmatrix}
400&152&165&235&248\\
152&152&144&152&144\\
165&144&144&165&165\\
235&152&165&214&227\\
248&144&165&227&248
\end{pmatrix}.
\]

The integer matrix has leading minors
\(400,37696,218664,124416,0\). Its leading \(4\times4\) block is positive
definite and its final scalar Schur complement is zero, proving PSD.
All full-RLT inequalities hold. Again,
\(\widetilde X_{11}=\widetilde\mu_1\) and
\(\widetilde X_{44}=\widetilde\mu_4\).

Consider the probability distribution on binary vectors ordered as
\((u,s,t,v)\):

| Atom | Probability |
|---|---:|
| 0000 | 144/400 |
| 0001 | 21/400 |
| 0011 | 62/400 |
| 0111 | 21/400 |
| 1010 | 8/400 |
| 1111 | 144/400 |

It reproduces every mean and every off-diagonal entry of
\(\widetilde M\). Thus their projection belongs to the Boolean quadric
polytope (BQP). Every affine cut in the means and off-diagonal moments
that is valid for unit-box rank-one points holds at this witness.
Nevertheless,

\[
L_{\widetilde M}(q)=-\frac1{200}<0.
\]

The conclusion survives the strict perturbation above. With
\(\eta=1,\tau=1/200\), the same witness has value

\[
-\frac1{200}+\frac1{200}\frac{144+214}{400}
=-\frac{21}{40000}<0.
\]

Hence adding all BQP valid cuts cannot restore exactness, even with
strictly negative outer square coefficients and a positive definite
inner block. The distribution represents the projected moments only:
its inner diagonal moments are \(\widetilde\mu_2,\widetilde\mu_3\),
not \(\widetilde X_{22},\widetilde X_{33}\). It therefore does not
represent the entire matrix, as the negative objective already proves.
Cuts involving continuous diagonal moments are not covered by this
argument.

## Relation to the existing example and exact relaxation value

[Zhang and Wang, Proposition 2](https://arxiv.org/html/2609.03617v2#S3.SS2),
give a path example with \(a=b=1/2\), objective
\(f=q-\tfrac14[u(1-u)+v(1-v)]\), and exact SDP value
\(\nu=\sqrt3-7/4\). Their optimal moments have binary outer diagonals.
Replacing the two outer positive quadratic terms by their secants
therefore preserves their relaxed value and gives the present objective.
The rational witness above results from their moment formula after
replacing \(2-\sqrt3\) by \(4/15\). This derivation establishes the
provenance; no priority claim is made for the resulting boundary example.

The exact optimum \(\nu\), although not needed for the counterexample,
also passes a separate check. Let \(\gamma=2-\sqrt3>0\), and define

\[
\ell_1=-\gamma+u+(\gamma-2)s+t,
\qquad \ell_2=s+(\gamma-2)t+v.
\]

Direct expansion gives

\[
\begin{aligned}
q-\nu={}&\tfrac14(\ell_1^2+\ell_2^2)
 +\tfrac\gamma2u(1-s)+\tfrac12u(1-t)
 +\gamma s(1-t)\\
&+\tfrac12s(1-v)+\tfrac\gamma2t(1-v)
 +\tfrac14\bigl[u(1-u)+v(1-v)\bigr].
\end{aligned}
\]

PSD and upper RLT imply that the expectation of every term on the right
is nonnegative. This gives the lower bound \(\nu\) even for the weaker
relaxation using only upper RLT. Equality is attained by

\[
\mu=\left(\tfrac{2\gamma}3,\tfrac13,\tfrac23,
1-\tfrac{2\gamma}3\right),\qquad
X=\begin{pmatrix}
2\gamma/3&2\gamma/3&2\gamma/3&2(1-3\gamma)/3\\
2\gamma/3&(1-\gamma)/3&1/3&1/3\\
2\gamma/3&1/3&(2-\gamma)/3&2/3\\
2(1-3\gamma)/3&1/3&2/3&1-2\gamma/3
\end{pmatrix}.
\]

For completeness, the leading \(3\times3\) block of its augmented moment
matrix has leading minors
\(1,(10\sqrt3-16)/9,(14-8\sqrt3)/27\), all strictly positive.
The Schur complement of that block is the zero \(2\times2\) matrix.
This proves PSD. Direct substitution verifies full RLT and objective
\(\nu\). Both full SDP–RLT and its upper-RLT version therefore have the
exact value \(\sqrt3-7/4\) for the unperturbed objective.

## Scope of the conclusion

The proposed direct-sum consequence is also valid. Take \(k\) disjoint
copies of the unperturbed objective, so \(n=4k\). The true minimum is
zero, while a relaxation witness has value \(-k/200=-n/800\), even
with all BQP cuts. To see feasibility, let \((\mu^{(j)},X^{(j)})\)
be the second witness in block \(j\). Its covariance
\(C^{(j)}=X^{(j)}-\mu^{(j)}\mu^{(j)T}\) is PSD. Stack the block means
into \(\mu\), and use

\[
X=\operatorname{diag}(C^{(1)},\ldots,C^{(k)})+\mu\mu^T.
\]

The augmented moment matrix is PSD by its Schur complement. The product
of the block binary distributions represents every mean and
off-diagonal moment, including cross-block products. All diagonal RLT
bounds are inherited from the blocks. The positive square vertices
induce a matching, and the full interaction graph is a forest of paths.
Under the entrywise maximum convention, both \(Q\) in
\(q=x^TQx+c^Tx\) and \(c\) have norm at most one. Thus the normalized
additive gap grows at least as \(n/800\) on this restricted pattern.
This elementary amplification follows the existing source's direct-sum
strategy; it is not a separate novelty claim. The strict perturbation
would require rescaling to meet the same normalization.

The same obstruction can be made connected. Number the variables by
their path order within successive blocks, and add

\[
\frac1{1000}\sum_{j=1}^{k-1}x_{4j}(1-x_{4j+1}).
\]

These terms are nonnegative on the box and vanish at the origin, so the
true optimum stays zero. They join the components into one path,
preserve submodularity and the positive-vertex matching, and leave the
entrywise normalization intact. Each new term costs at most \(1/1000\)
at the same product moment point. Therefore its objective is at most
\(-k/200+(k-1)/1000\leq-k/250=-n/1000\). In fact its expected
unscaled interface product is
\((248/400)(1-152/400)=961/2500\). No new moment construction is needed.

The [stable positive diagonal theorem](stable-positive-submodular-exactness.md)
cannot be extended to permit even one interacting positive pair in
general, including on forests. Positive definiteness of the continuous
block does not suffice to make that extension valid.

This does not say stability is necessary for exactness of every
individual objective. It does not imply hardness for the class with two
positive square coefficients, failure of higher-order relaxations, or
failure after arbitrary cuts involving continuous diagonal moments.
The rational witnesses only prove upper bounds on the relaxation optima;
the separate primal and dual certificates establish the exact value
for the unperturbed case with upper RLT or full RLT, without additional
BQP cuts.

## Verification record

The independent check used exact SymPy arithmetic, not a floating-point
SDP solution. The targeted command

```text
python research-20260927/check_positive_pair_review.py
```

passes the endpoint polynomial identities, rational principal minors,
all RLT inequalities, the rational objective values, the six-atom BQP
representation, the strict continuous-block eigenvalues, and the algebraic primal and dual
certificates for the exact unperturbed SDP optimum. Earlier inline
SymPy calculations checked the same identities and all 31 principal
minors of the algebraic moment point. These checks establish the stated
finite examples; the global true-bound argument is the symbolic proof
above. No project-wide checks, CI inspection, or Lean verification were
performed.
