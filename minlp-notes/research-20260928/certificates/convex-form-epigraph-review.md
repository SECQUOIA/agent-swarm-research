# Independent check of the convex-form epigraph argument

Date: 2026-09-28. Status: independent algebraic review of
[the complete main note](convex-form-epigraph.md). The broad
nonrepresentability statement in the inspected slides cannot be used
as written; the argument below gives an incompatible consequence of
the standard compact positive-curvature representation theorem.

## 1. Exact statements inspected

Printed slide 13 of
[the locally retained Scheiderer slides](sources/scheiderer-slides.pdf)
states that the epigraph of every convex form that is not SOS is not a
spectrahedral shadow. The display defines the ordinary epigraph
\(\{(t,x):t\geq f(x)\}\), without an evident qualification on the
lift. Printed slide 11 also states the compact positive-curvature
second-order-cone representation theorem.

[Scheiderer, *Smooth hyperbolicity cones are second-order cone representable*](https://arxiv.org/abs/2509.17121),
Theorem 1.2, says that every compact convex semialgebraic set with
Nash-smooth boundary and strictly positive curvature has a lift by
positive semidefinite blocks of size at most two. The discussion there
credits Helton and Nie for the earlier spectrahedral-shadow conclusion
under ordinary smoothness and positive curvature. The current
[locally retained PDF](sources/scheiderer-smooth-soc.pdf) correctly
includes a constant matrix in its affine lifted LMI. The arXiv v1 HTML
rendering inspected during this review omits that constant in the
display of Theorem 1.2; Section 3.1 of the same rendering includes it.
The argument below uses the correct affine form.

This review does not independently prove the compact representation
theorem. It checks the proposed deduction from its stated conclusion,
including the potential difficulty at homogenization parameter zero.

## 2. Homogenizing a lift of a compact convex set

Suppose a nonempty bounded convex set \(K\subseteq\mathbb R^n\)
has the exact representation
\[
K=\{x:\exists y,\ A_0+A(x)+B(y)\succeq0\},               \tag{1}
\]
where \(A\) and \(B\) are linear matrix maps. Then
\[
\widehat K=\{(u,x):u\geq0,\ \exists y,
                         uA_0+A(x)+B(y)\succeq0\}        \tag{2}
\]
equals
\[
\{(u,x):u>0,\ x/u\in K\}\ \cup\ \{(0,0)\}.             \tag{3}
\]

For \(u>0\), divide the matrix inequality by \(u\). If \(u=0\)
and \(A(x)+B(y)\succeq0\), take any feasible lift
\((z,w)\) from (1). For every \(s\geq0\),
\[
A_0+A(z+s x)+B(w+s y)
  =A_0+A(z)+B(w)+s(A(x)+B(y))\succeq0.
\]
Hence \(z+s x\in K\) for every \(s\geq0\), and boundedness
forces \(x=0\). Conversely, \((u,x,y)=(0,0,0)\) is feasible.
No boundedness of the auxiliary lift variables is needed.

The construction preserves the maximum PSD block size, except for the
additional one-by-one inequality \(u\geq0\). Thus a second-order
cone lift of \(K\) gives one for \(\widehat K\).

## 3. From a homogeneous sublevel set to the polynomial epigraph

Let \(f\) be a positive definite convex form of even degree \(m\),
and let \(K=\{x:f(x)\leq1\}\). It is compact, convex, and has
the origin in its interior. Positive homogeneity gives
\[
\widehat K=\{(u,x):u\geq f(x)^{1/m}\}.                    \tag{4}
\]
At \(u=0\), positive definiteness is essential: (4) then forces
\(x=0\), in agreement with (3).

If \(\widehat K\) has a second-order cone lift and the epigraph
of \(u\mapsto u^m\) on \(u\geq0\) has one, then so does
\[
\{(t,x):\exists u\geq0,\ (u,x)\in\widehat K,
                                            t\geq u^m\}
                         =\{(t,x):t\geq f(x)\}.          \tag{5}
\]
The inequality direction is correct: \(u\geq f(x)^{1/m}\)
implies \(u^m\geq f(x)\), and conversely one may choose
\(u=f(x)^{1/m}\).

Only the quartic case is needed to contradict the slide statement.
For \(m=4\), the power epigraph has the explicit two-block lift
\[
\begin{pmatrix}z&u\\u&1\end{pmatrix}\succeq0,
\qquad
\begin{pmatrix}t&z\\z&1\end{pmatrix}\succeq0.             \tag{6}
\]
These inequalities say \(z\geq u^2\) and \(t\geq z^2\).
They imply \(t\geq u^4\), and the converse chooses \(z=u^2\).
No general power-cone representation theorem is needed here.

The main note also states the deduction for all even degrees. For
completeness, any integer power \(m\geq2\) has the required finite
SOC lift. Take a power of two \(N\geq m\) and a binary geometric
mean tree with \(N\) nonnegative leaves: one copy of \(t\),
\(N-m\) copies of \(u\), and \(m-1\) copies of one. At every
internal node impose \(z^2\leq ab\) with \(z\geq0\), using
the two-by-two PSD block with diagonal \((a,b)\) and off-diagonal
\(z\). Require the root to be at least \(u\geq0\). The tree
is feasible exactly when
\(u^N\leq t u^{N-m}\), with \(t\geq0\) from the leaf
condition. For \(u>0\), this is \(u^m\leq t\). For
\(u=0\), both the power epigraph and the tree permit every
\(t\geq0\). Choosing each internal node as the corresponding
geometric mean proves sufficiency. This checks the general-degree
claim independently of an unstated power-cone reference.

## 4. A convex non-SOS quartic can have all required curvature

Let \(p\) be any convex quartic form that is not SOS, whose existence
is established independently in the literature cited by the slides.
The SOS cone in the finite-dimensional quartic coefficient space is
closed. Therefore, for all sufficiently small \(\epsilon>0\),
\[
f(x)=p(x)+\epsilon\|x\|^4                                \tag{7}
\]
still is not SOS. Convex forms of positive even degree are
nonnegative: evenness and convexity give
\(p(0)\leq(p(x)+p(-x))/2=p(x)\), and \(p(0)=0\).
Thus \(f\) is positive definite.

For \(x\ne0\),
\[
\nabla^2\|x\|^4=8xx^{\mathsf T}+4\|x\|^2I\succ0.
\]
Since \(\nabla^2p(x)\succeq0\), the Hessian of \(f\) is
positive definite away from the origin. On \(f=1\), Euler's
identity gives \(x^{\mathsf T}\nabla f(x)=4\), so the gradient
does not vanish. The defining function \(1-f\) has negative
definite Hessian on every nonzero tangent direction. Hence
\(\partial K\) is a smooth algebraic boundary with strictly
positive curvature, satisfying the hypotheses of the compact
representation theorem.

That theorem and (2)--(6) imply that the epigraph of the non-SOS
quartic (7) is second-order cone representable, and therefore is a
spectrahedral shadow. The older shadow conclusion for the compact
body would already imply that its epigraph is a shadow, so the
conflict is not specific to the newer second-order-cone strengthening.

## 5. Independent check of the explicit rational perturbation

The lead researcher supplied the proposed explicit choice
\[
f(X)=q^{\mathbb O}_{17}(X)+\frac1{1016}\|X\|_F^4,
\qquad X\in\mathbb R^{16\times17}.
\]
I independently read Proposition 4.9 and the proof of Theorem 4.11 in
[Saunderson's retained primary manuscript](sources/saunderson-2021.pdf).
The three evaluation points there have squared Frobenius norms
\(1,16,16\), hence fourth powers \(1,256,256\). Their
\(q^{\mathbb O}_{17}\)-values are \(1/4,64,128\).

Reconstructing the displayed three-by-eight matrix directly from the
primary text gives
\[
M=\begin{pmatrix}
1/272&1/272&14/272&1/17&1/17&14/17&0&0\\
16/17&16/17&0&18/17&18/17&140&56&56\\
16/17&0&0&1/17&9&126&36&84
\end{pmatrix}.
\]
For \(w=(252,3,-2)\), exact rational multiplication yields
\[
wM=(127/68,15/4,441/34,304/17,0,6384/17,96,0)\geq0,
\]
whereas
\[
w(1/4,64,128)^{\mathsf T}=-1,\qquad
w(1,256,256)^{\mathsf T}=508.
\]
Therefore the perturbed evaluations have separating value
\(-1+508/1016=-1/2\), strictly negative.

The matrix characterizes invariant SOS quartics, rather than all
quartics. This restriction causes no gap: both
\(q^{\mathbb O}_{17}\) and \(\|X\|_F^4\) are invariant under
the compact orthogonal group action used in Proposition 4.9, so their
sum is invariant. That proposition applies if the sum has any SOS
representation. The separating vector therefore excludes an
unrestricted SOS representation of this particular invariant sum.
Convexity of \(q^{\mathbb O}_{17}\) is supplied by Saunderson's
Theorem 1.2; the added positive radial term gives the strict curvature
used above. The representation-theoretic proof behind Proposition
4.9 was not rederived in this review.

I ran the targeted command `python3 -` with an inline script using
only Python `fractions.Fraction`. It checked all eight entries of
\(wM\), their nonnegativity, the values \(-1\) and \(508\), and
the perturbed gap \(-1/2\). It passed. This finite computation
checks the displayed witness arithmetic, not convexity or the conic
representation theorem.

## 6. Assessment and limits

The inspected universal statement about non-SOS convex forms is
incompatible with the compact positive-curvature representation
theorem and the elementary deductions above. I found no missing
inequality direction, recession point, or curvature hypothesis that
repairs the incompatibility. A missing qualification or an error in
the slide statement remains possible. It should not be cited as a
valid universal nonrepresentability theorem without a corrected
source or explanation.

This deduction asserts existence of real conic lifts. It supplies no
bound on their number of blocks, no polynomial-time construction,
and no rationality guarantee for their coefficients. It also does
not establish that every convex form has a conic lift: the strict
curvature assumption can fail without the perturbation in (7), and
limits of lifts of unbounded size do not preserve a finite lift.

Verification in this review consists of direct matrix and polynomial
algebra, the targeted exact witness calculation above, and inspection
of the primary-source statements. No Lean verification, project-wide
check, or CI inspection was performed. No message was sent to the
source author.
