# Strong convexity does not remove the rational cost of block SOS certificates

Date: 2026-09-28. Status: construction and certificate-size consequences
passed a [fresh independent review](strongly-sos-convex-block-splitting-review.md),
after correcting the extension lemma's supplied-certificate scope.
Publication priority remains unestablished.

The [quartic block-splitting construction](rational-block-sos-splitting-obstruction.md)
produces rational nonnegative quartics \(f(x)\) and \(g(w)\) in
disjoint variables such that \(f+g\) is a sum of rational polynomial
squares, but no such representation uses squares confined to individual
blocks. This note makes both blocks strongly SOS-convex. It also
preserves the separation between short unrestricted rational
certificates and exponentially long rational block certificates after
a strictly positive perturbation.

The conclusion concerns a prescribed sparsity restriction. The
unrestricted rational SOS certificates remain short. The polynomial
Hessians have explicit rational SOS certificates and a uniform positive
lower bound. Their positive semidefinite Grams on the full joint Hessian basis are
singular: an additively separable polynomial has no curvature coupling
between independent variable blocks.

## 1. Adding affine zero coordinates to a quartic realization

We first record an elementary extension used only with fixed dimensions
below. It also gives a general construction with polynomial bit length.

**Lemma.** Let \(r\ge1\), and let
\(B_0\in\mathbb Q[u_1,\ldots,u_r]\) be a rational
quartic with a supplied rational SOS certificate and a rational
positive definite Hessian Gram \(A_0\)
on \((a,u\otimes a)\). Suppose \(B_0^{-1}(0)=\{p\}\). For every
integer \(s\ge1\), a positive rational \(\epsilon\) can be chosen
with polynomial bit length so that
\[
 B(u,v)=B_0(u)+\epsilon\|v\|^2
                 (1+\|u\|^2+\|v\|^2),\qquad v\in\mathbb R^s,
 \tag{1}
\]
is a rational SOS, has zero set \(\{(p,0)\}\), and has a positive
definite rational Hessian Gram on the full basis
\((a,b,(u,v)\otimes(a,b))\).

Here polynomial bit length is measured in the expanded input
\(B_0,A_0\), the supplied rational SOS certificate, and the
dimensions. Unweighted rational squares can be
obtained with polynomial output length by expanding positive rational
weights into rational squares.

**Proof.** Put \(h=r+r^2\) and
\[
 \rho=\frac{\det A_0}{(\operatorname{tr}A_0)^{h-1}}>0,
 \qquad
 0<\epsilon\le\min\{1,\rho/(16rs)\}.
 \tag{2}
\]
The eigenvalue product bound gives \(A_0\succeq\rho I\). The
added polynomial in (1) is a positive rational combination of the
squares \(v_i^2\), \((u_jv_i)^2\), and \((v_jv_i)^2\). This
proves the SOS claim and, together with \(B_0\ge0\), the zero set.

For directions \((a,b)\), its Hessian biform is
\[
 \begin{aligned}
 &2\epsilon\|b\|^2+2\epsilon\|v\|^2\|a\|^2
 +8\epsilon(u^{\mathsf T}a)(v^{\mathsf T}b)
 +2\epsilon\|u\|^2\|b\|^2\\
 &\hspace{25mm}
 +8\epsilon(v^{\mathsf T}b)^2
 +4\epsilon\|v\|^2\|b\|^2.
 \end{aligned}
 \tag{3}
\]
Order the full Hessian basis as the old block
\((a,u\otimes a)\), followed by
\[
             (b,u\otimes b,v\otimes a,v\otimes b).
\]
The new diagonal block \(D\) is block diagonal, with blocks
\[
 2\epsilon I_s,\quad 2\epsilon I_{rs},\quad
 2\epsilon I_{sr},\quad
 4\epsilon I_{s^2}+8\epsilon e_se_s^{\mathsf T},
 \tag{4}
\]
where \(e_s=\operatorname{vec}I_s\). Thus
\(D\succeq2\epsilon I\). The only old-new cross block \(C\)
is \(4\epsilon e_re_s^{\mathsf T}\) between
\(u\otimes a\) and \(v\otimes b\). Its squared norm is
\(16\epsilon^2rs\). Consequently
\[
 D-C^{\mathsf T}A_0^{-1}C
 \succeq
 \left(2\epsilon-\frac{16\epsilon^2rs}{\rho}\right)I
 \succeq\epsilon I.
 \tag{5}
\]
The Schur complement proves positive definiteness of the rational
full Hessian Gram. Determinants, traces, and this fixed number of
matrix operations have polynomial bit length.

A positive rational weight \(a/b\) can be expressed as the sum of
polynomially many rational squares using the binary expansion of
\(ab\) and the denominator \(b\). No integer factorization
algorithm is needed. This proves the output assertion. \(\square\)

A rational invertible affine change of the point variables preserves
all these conclusions. It gives an invertible rational change of the
full Hessian basis, since both the direction vector and every product
of a point coordinate with a direction coordinate transform linearly.
Positive definiteness is therefore preserved by congruence.

## 2. A fixed strongly SOS-convex block counterexample

Let \(a=2^{1/5}\) and use the one-gate quartic \(f=f_1\) from
[the reviewed least-field construction](exponential-least-sos-field.md).
It is a rational quartic in three variables, is strongly SOS-convex
with a supplied full positive definite rational Hessian Gram, and has
unique zero
\[
                  p=(a,a^2,a^3).
 \tag{6}
\]
It has no rational polynomial SOS representation.

Apply the quartic lifting construction to \(f\), with one variable
\(z_{ij}\) for each \(1\le i\le j\le3\). Write
\[
 w=(y_1,y_2,y_3,z_{11},z_{12},z_{13},z_{22},z_{23},z_{33}).
\]
The resulting rational quartic \(g_0(w)\) satisfies
\[
 g_0\ge0,\qquad g_0(w_0)=0,
 \qquad f(x)+g_0(w)\text{ is a rational SOS},
 \tag{7}
\]
where
\[
 w_0=(a,a^2,a^3,a^2,a^3,a^4,a^4,2,2a).
 \tag{8}
\]
No convexity of \(g_0\) is used.

The [general power-basis realization](general-strongly-convex-quartic-singleton.md),
with its [reviewed rational Hessian certificate](sos-convex-quartic-realization.md),
applied to \(T^5-2\), supplies a rational SOS quartic \(B_0\) in
four variables. Its unique zero is \((a,a^2,a^3,a^4)\), and its
full rational Hessian Gram is positive definite.

Consider the rational invertible affine map from \(w\) to
\((u,v)\in\mathbb R^4\times\mathbb R^5\) given by
\[
 \begin{aligned}
 u&=(y_1,y_2,y_3,z_{13}),\\
 v&=(z_{11}-y_2,\ z_{12}-y_3,\ z_{22}-z_{13},\
                  z_{23}-2,\ z_{33}-2y_1).
 \end{aligned}
 \tag{9}
\]
It sends \(w_0\) to \((a,a^2,a^3,a^4,0)\).
Applying the lemma and transforming back gives a rational SOS quartic
\(B(w)\), with unique zero \(w_0\), whose full Hessian Gram
\(A_B\) is rational positive definite.

Every rational quartic has a rational symmetric Hessian Gram on the
full basis: its Hessian biform has degree two in the direction and
degree at most two in the point variables, so every monomial is a
product of two entries of that basis. Let \(C\) be any such Gram
for \(g_0\), put \(q=9+9^2\), and define
\[
 \beta=\frac{\det A_B}{(\operatorname{tr}A_B)^{q-1}}>0,
 \qquad U=\sum_{i,j}|C_{ij}|,
 \qquad T=\left\lceil\frac{U+1}{\beta}\right\rceil.
 \tag{10}
\]
Since \(\|C\|_2\le U\),
\[
                      C+T A_B\succeq I.
 \tag{11}
\]
Thus
\[
                         g=g_0+TB
 \tag{12}
\]
is a strongly SOS-convex rational quartic with unique zero \(w_0\).
The uniqueness follows also from \(g_0\ge0\), \(B\ge0\), and
the unique zero of \(B\). All data in this section have fixed
dimension and fixed finite rational encoding.

Adding \(TB\) to the certificate in (7) proves that \(f+g\)
is a rational SOS. Suppose instead that it had a rational SOS with
each square depending only on \(x\) or only on \(w\). Grouping
the squares gives
\[
             f(x)+g(w)=S_x(x)+S_w(w),
\]
where \(S_x,S_w\) are rational SOS. Independence of the variables
forces \(S_x=f+t\), \(S_w=g-t\) for a rational constant \(t\).
Evaluation at the two zeros gives \(t\ge0\) and \(t\le0\).
Hence \(t=0\), contradicting the absence of a rational SOS for
\(f\).

This obstruction is about rational coefficients. A real block SOS
exists: \(f\) is a real SOS, and restricting the joint rational
certificate to \(x=p\) makes \(g\) a real SOS. The old real
zero-minimum block-splitting observation therefore remains valid.

## 3. Strict positivity and exponentially long sparse certificates

Let \(h_k(t)\) be the reviewed family from
[the interior Gram lower bound](interior-gram-bit-lower-bound.md),
in \(2k\) new variables. It has polynomial-size rational quartic
input and a polynomial-size rational SOS. It also has a full
positive definite rational Hessian Gram, and
\[
 0< m_k:=\min h_k
 <4M_k^{-2^{k+1}},\qquad M_k=1000^{k+3}.
 \tag{13}
\]
Use the two prescribed blocks \(x\) and \((w,t)\), and put
\[
                   P_k(x,w,t)=f(x)+g(w)+h_k(t).
 \tag{14}
\]
This is a strictly positive strongly SOS-convex rational quartic in
\(12+2k\) variables. Its expanded input, unrestricted rational SOS,
and rational SOS Hessian certificate have polynomial total bit length
in \(k\). The minimum is exactly \(m_k\).

Every rational block SOS gives a rational constant \(c\) with
\[
 S_x=f+c,\qquad S_{w,t}=g+h_k-c.
 \tag{15}
\]
Nonnegativity and the zero of \(f\) imply \(c\ge0\). Equality
would make \(f\) a rational SOS, so \(c>0\). Evaluating the other
block at \(w_0\) and a minimizer of \(h_k\) gives \(c\le m_k\).
In particular
\[
                       0<c<4M_k^{-2^{k+1}}.
 \tag{16}
\]

This is a nonvacuous certificate-size statement. Choose rational
\(0<c<m_k\). Both \(f+c\) and \(h_k-c\) are strictly positive
quartics with full positive definite rational Hessian Grams, so the
reviewed Taylor construction supplies rational polynomial SOS
certificates for them. To handle \(g\), choose a rational \(s>0\)
with \(c+s<m_k\), and a rational \(q\) near \(p\) with
\(f(q)<s\). Restricting the joint rational certificate for \(f+g\)
to \(x=q\) proves \(g+f(q)\) is a rational SOS. Hence \(g+s\)
is a rational SOS. Adding it to a rational SOS for \(h_k-c-s\)
gives the second block in (15).

For a direct denominator bound, a block Gram certificate here means
a pair of separately stored local PSD Grams, one for each block,
each using its own constant monomial. Write \(f(0)=a_0/b_0\) in lowest
terms with \(b_0\ge1\). A rational PSD Gram \(Q_x\) for the
first block on the usual monomial vector beginning with \(1\)
satisfies
\[
                      (Q_x)_{00}=f(0)+c.
\]
If its reduced denominator is \(d\), then the reduced denominator
of \(c\) is at most \(b_0d\). A positive rational has numerator
at least one, so (16) implies
\[
 \log_2 d>
          2^{k+1}\log_2 M_k-2-\log_2 b_0.
 \tag{17}
\]
Thus every rational PSD block Gram has an individual entry with
\(\Omega(k2^k)\) denominator bits. Positive definiteness is not
required. Every explicit unweighted block SOS has exponential total
coefficient bit length as well: if \(a_j\) are the constant
coefficients of its \(x\)-block square factors, then
\((Q_x)_{00}=\sum_j a_j^2\), whose denominator divides the product
of their squared denominators.

The unrestricted rational SOS stays polynomial-size. This is therefore
a cost of enforcing exact rational block certificates, not an
unrestricted rational SOS output lower bound.

## 4. Scope and prior comparison

The arithmetic obstruction uses the rational failure of SOS descent,
the quartic gradient lift, and the previously reviewed tiny-minimum
family. The elementary extension (1) adds strong SOS-convexity without
changing the zero or the block obstruction. It is not claimed as a
new general convexification principle without further literature work.

The [separate prior audit](rational-block-sos-splitting-prior.md)
compares real block decomposition and sparse SOS results. The distinction
between real and rational coefficients is essential: reducing the SDP
to independent real blocks can preserve existence while losing all
rational points, or greatly increasing the length of rational points.
No novelty conclusion follows merely from an unsuccessful search.

For MINLP certification, the possible implication is that a sparsity
restriction can be harmless for real feasibility and costly for exact
rational proof output, even with certified strong convexity. A practical
solver rule for deciding when to merge certificate blocks remains to
be developed. No running-time lower bound for optimization is proved.

The exponential-field variant of the base lifting theorem is not
upgraded here to polynomial-size strongly SOS-convex second blocks.
This note uses one fixed degree-five field. A dense power-basis
realization for degree \(5^k\) would itself have exponential size,
so it cannot justify that stronger claim.
The subsequently [reviewed quadratic graph construction](quadratic-graph-quartic-realization.md)
supplies a different polynomial-size proof of the growing-field
strong-convexity extension. The fixed-field proof above remains
independent of that additional theorem.

## Verification status

The proof above passed a fresh independent audit of the extension,
the affine map, and the sparse denominator bound. The reviewer required
the baseline SOS certificate to be supplied and counted in the padding
lemma's input. That correction, the explicit positive-dimension
hypothesis, and the two-local-Gram convention were independently
rechecked. The concrete fixed-field application already supplied the
required baseline certificate.

The reviewer retained
[an exact targeted checker](check_strongly_sos_convex_block_splitting_review.py)
and ran it successfully. It checks the padding Hessian identity in
several dimensions, exact positive LDL pivots, the affine inverse,
the quintic graph point, and the translated Hessian chain rule. Those
finite checks support the identities; the general inequalities and
encoding claims are justified by the proof and independent review.
The root independently read and reconstructed the full argument.
No floating-point experiment or Lean formalization was used, and no
project-wide verification or CI inspection was performed.
