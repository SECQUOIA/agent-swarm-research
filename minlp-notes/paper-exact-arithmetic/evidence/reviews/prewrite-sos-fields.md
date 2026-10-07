# Prewriting audit: SOS fields, descent, denominators, and block certificates

Date: 2026-10-05. This is an internal mathematical audit for the exact-arithmetic manuscript. I read the brief and historical theorem notes, reconstructed the arguments below, and inspected recorded exact certificates. I did not run historical checkers, mathematical scripts, numerical experiments, literature searches, project-wide checks, or CI checks. Computations cited from historical records are not checks performed in this audit.

The field and block results are sound with their stated certificate hypotheses. I found no unresolved internal correctness blocker. The quadratic graph theorem has a useful simplification: its positive centered canonical Hessian Gram translates exactly to the rational canonical Gram at the origin. Its second approximation and coefficient projection can be removed. The pending descent criterion is sound conditional on the universal minimum-SOS-length theorem. Its cyclic applications are finite rank diagnostics, not an all-dimension theorem.

The full interior-Gram height proofs and the geometric/elimination dependencies of the number-field precision theorem belong to other audit assignments. This review checks their interfaces. Primary-source attribution must use the root's vetted literature report. I performed no new source research and make no priority claim.

## 1. Certificate models and common proof lemmas

Use \(I\) for total binary input length, \(n\) for ambient continuous dimension, \(k\) for tower depth, and \(p\) for the minimizer. In the arbitrary-prime result use \(\ell\) for the prime. Polynomial and matrix data are explicitly expanded rationals unless a different output model is stated.

Let \(m_2(X)\) list all monomials of degree at most two, constant first. An SOS over \(E\subseteq\mathbb R\) is a finite sum of squares in \(E[X]\). An \(E\)-valued PSD Gram is a symmetric \(Q\) with entries in \(E\), PSD at its given real embedding, and \(P=m_2^{\mathsf T}Qm_2\). These notions are equivalent over \(\mathbb Q\), but not automatically over arbitrary \(E\): positive LDL weights need not be sums of squares in \(E\). Arbitrary-field necessity needs separate arguments for square factors and PSD matrices.

A full strict Hessian Gram is a supplied rational matrix \(A\succ0\) on \(Z=(v,X\otimes v)\) satisfying \(v^{\mathsf T}\nabla^2P(X)v=Z^{\mathsf T}AZ\). This is stronger than strong convexity or ordinary SOS-convexity. It gives a uniform positive Hessian lower bound, positive definite leading quartic form, and a strict Taylor Gram on centered nonconstant quadratic monomials. It does not give a positive definite full polynomial Gram at a zero.

**Rational squares in polynomial time.** For positive integers \(u,v\), write \(u/v=uv/v^2\), expand \(uv\) in binary, replace \(2^{2j}\) by \((2^j)^2\) and \(2^{2j+1}\) by two copies of that square, and divide the square bases by \(v\). This produces polynomially many rational squares of polynomial bit length. Rational symmetric elimination followed by this conversion gives an unweighted rational SOS from a rational PSD Gram in polynomial bit time. Do not assume a polynomial-time integer four-square algorithm. Four-square existence suffices for qualitative statements.

**Rational eigenvalue margin.** If \(A\succ0\) has dimension \(h\), put
\[
\rho(A)=\frac{\det A}{(\operatorname{tr}A)^{h-1}}.
\]
Each eigenvalue is at most the trace, so \(A\succeq\rho(A)I\). Determinants, trace powers with polynomial exponent, and integer ceilings have polynomial bit complexity for polynomial-dimensional rational matrices of polynomial entry length. A large numerical scale can have a short binary encoding.

**Field-preserving Taylor SOS.** Factor a rational PSD Hessian Gram into rational biform squares. At a stationary zero \(p\in E^n\), substitute \(X=p+tu,v=u\). Each factor becomes \(U(u)+tV(u)\) with coefficients in \(E\), and
\[
\int_0^1(1-t)(U+tV)^2\,dt
=2\left(\frac{U+V/3}{2}\right)^2+\left(\frac V6\right)^2.
\]
Taylor integration gives an actual SOS over \(E\), with no additional field extension. Strong convexity alone does not justify this conclusion.

**Strict Taylor Gram.** Translate a full positive definite Hessian Gram to \(u=X-p\), and choose real \(\mu>0\) below its least eigenvalue. Taylor integration gives an SOS Gram for
\[
P(p+u)-\frac{\mu}{2}\|u\|^2-\frac{\mu}{12}\|u\|^4
\]
when \(P(p)=0,\nabla P(p)=0\). The two positive terms have a positive diagonal Gram on all nonconstant quadratic-or-lower monomials. Adding a positive constant fills the constant coordinate. For a rational polynomial the Gram coefficient equations form a rational affine space; rational points are dense, and the positive definite subset is open. Hence \(P+\eta\) has a rational PD polynomial Gram for every rational \(\eta>0\). This is qualitative, with no bit bound as \(\eta\downarrow0\). More generally, strict positivity plus a full strict rational Hessian Gram gives a rational PD polynomial Gram even if the minimum and minimizer are irrational.

**PSD row restriction.** If \(P=m_2^{\mathsf T}Qm_2\), \(Q\succeq0\), and \(P(p)=0\), then \(Qm_2(p)=0\). Each row represents a quadratic vanishing at \(p\) over the entry field. If these quadratics have coefficient-column basis \(B\), symmetry gives \(Q=BSB^{\mathsf T}\), \(S=CQC^{\mathsf T}\succeq0\), where \(CB=I\). No factorization over the entry field is required.

## 2. Fixed ternary obstruction and dimension boundary

Sources: [ternary construction](../../../research-20260927/ternary-rational-sos-convex-counterexample.md), [fresh review](../../../research-20260927/ternary-rational-sos-convex-counterexample-independent-review.md), [root audit](../../../research-20260927/rational-sos-convex-descent-root-audit.md), and [descent comparison](../../../research-20260927/rational-sos-convex-descent-prior.md).

The theorem uses
\[
\begin{aligned}
r_0&=2-2xy,&r_1&=2x^2-2yz,&r_2&=2y^2-4z,\\
r_3&=2z^2-x,&r_4&=2xz-y,&A_0&=4r_0+5r_1+3r_2+9r_3,
\end{aligned}
\]
and \(F=A_0^2+\sum_{i=0}^3r_i^2-r_4^2\). It has a rational full strict Hessian Gram, \(\nabla^2F\succeq I\), and unique zero \(p=(a^4/2,a,a^2/2)\), \(a=2^{1/5}\). For every real subfield \(E\), an \(E\)-SOS or \(E\)-valued PSD polynomial Gram exists exactly when \(a\in E\).

The explicit convexity certificate is printable without relying on code. At \(c=(3/4,1,1/2)\), write \(q(c+u)=d+b^{\mathsf T}u+u^{\mathsf T}Tu\). The canonical Gram for the Hessian of \(q^2\) on \((v,u\otimes v)\) has blocks
\[
\begin{aligned}
C&=2bb^{\mathsf T}+4dT,\\
D_{i,(k,j)}&=2b_kT_{ij}+4b_iT_{kj},\\
Q&=8\operatorname{vec}(T)\operatorname{vec}(T)^{\mathsf T}+4T\otimes T.
\end{aligned}                                                    \tag{A}
\]
Differentiation proves the identity, including the constant term \(4dT\). Sum these matrices with the displayed signs. The note lists all twelve positive leading principal minors of \(2(M-I)\); formula (A), the center, and those integers form a self-contained Sylvester certificate. A submission must print them, rather than state that a repository checker verifies positivity. The 31-monomial and coefficient-magnitude-448 counts are recorded finite data.

The ten quadratic monomials evaluate onto a five-dimensional space; \(1,y,z,yz,x\) give rational multiples of \(1,a,a^2,a^3,a^4\). Thus the five independent \(r_i\) are the full rational vanishing basis. Direct multiplication gives
\[
\Lambda(P)=2[z]P+4[y^2]P,\qquad
\Lambda(r_ir_j)=4\mathbf1_{i=j=4},\qquad \Lambda(F)=-4.
\]
An SOS quartic has factors of degree at most two, since leading real squares cannot cancel. Each factor vanishes at the zero, so the functional excludes rational SOS. It is positive only on this vanishing-space cone, not all real squares.

If \(a\notin E\subseteq\mathbb R\), \(T^5-2\) remains irreducible. A proper monic factor of degree \(1\le r\le4\) has constant term \((-1)^ra^r\zeta_5^j\in E\); its reality forces \(\zeta_5^j=1\). Bézout using \(r,5\) and \(a^5=2\) would put \(a\) in \(E\). The same vanishing basis works over \(E\), excluding SOS. PSD row restriction gives \(\Lambda(F)=4S_{44}\ge0\), separately excluding field-valued PSD Grams. If \(a\in E\), field-preserving Taylor SOS proves sufficiency.

Three is the minimum affine dimension **under the full strict Hessian Gram hypothesis**. In two variables its tensor principal block gives
\[
12F_4(X)=(X\otimes X)^{\mathsf T}C(X\otimes X)>0\quad(X\ne0).
\]
Homogenization is a rational nonnegative ternary quartic with exactly one real projective zero. The imported Scheiderer classification says that any such form which is not rational SOS is a product of four distinct complex lines in general position. A real simple factor would change sign, so the lines form two conjugate pairs. Each pair intersects at a real projective point, and general position makes these points distinct. This contradicts the unique zero. In one variable the minimal polynomial of the zero has its square dividing the quartic and degree at most two; an irrational real quadratic zero would have a second real conjugate zero. The zero is rational and Taylor SOS applies. The root's literature review must confirm the precise classification statement and citation. Do not extend the dimension boundary to weaker convexity hypotheses.

The [four-variable example](../../../research-20260927/rational-sos-convex-descent.md) has a different obstruction. At \((\alpha,\alpha^2,\beta,\beta^2)\), \(\alpha^3=2,\beta^3=5\), its coordinate field has degree nine. If the two real cubic fields coincided, traces of \(\beta,\beta^2\) would force the constant coefficient and the product of the two other rational coefficients to vanish, leaving impossible rational cube equations \(5/2\) or \(5/4\). Its fifteen quadratic evaluations have rank nine; the six vanishing quadratics are the three standard relations in each block. Their products have no \(yz^3\) term, whereas the stationary perturbation does. That example is outside the vanishing-product span; the ternary example lies inside its product span with an indefinite restricted Gram.

Positive constant perturbations have rational interior Grams. Consequently rational SOS lower bounds have supremum zero without attaining it. This is rational certificate nonattainment, not a real SDP gap or real nonattainment.

## 3. Tower field necessity, sufficiency, and individual degree

Sources: [tower theorem](../../../research-20260927/exponential-least-sos-field.md), [individual degree](../../../research-20260927/exponential-sos-individual-coefficient-degree.md), [shared encoding](../../../research-20260927/tower-sos-coefficient-encoding.md), and [signed-root dependency](../../../research-20260927/signed-odd-root-circuit-quartic.md).

For every \(k\ge1\), polynomial bit time constructs a rational quartic \(F_k\) in \(n=3k\) variables, of polynomial total length in \(k\), with a rational full Hessian Gram at least \(I\), and unique zero
\[
p=(a_i,a_i^2,a_i^3)_{i=1}^k,\qquad a_i=2^{1/5^i}.
\]
For every \(E\subseteq\mathbb R\), polynomial SOS or PSD polynomial Grams exist exactly when \(a_k\in E\). The least field is \(\mathbb Q(a_k)\), degree \(5^k\). Every algebraic coefficient list has an individual coefficient of degree at least \(5^k\), so a separately printed dense defining polynomial has at least \(5^k+1\) positions. This is exponential in \(k,n\), and superpolynomial in the polynomially bounded constructed input. It is not asserted to be \(2^{\Omega(I)}\).

The signed-root construction must provide the following exact baseline interface. The equations \(a_1^5=2,a_i^5=a_{i-1}\) pass its exact interval contract with boxes \([1,2]\), no normalization scale. With \(b_1=2,b_i=x_{i-1}\), residuals are
\[
r_{i,1}=x_i^2-y_i,\quad r_{i,2}=x_iy_i-z_i,\quad r_{i,3}=y_iz_i-b_i.
\]
It constructs positive rationals \(t,\nu\), a rational quadratic \(G\) with positive definite homogeneous matrix and \(G(p)=0\), and
\[
F_0=(G/(t\nu))^2+\sum_{i,j}(r_{i,j}/\nu)^2,
\]
with a polynomial-size rational strict full Hessian Gram \(M\). It approximates exposing coefficients within a rational relation span, preserving exact vanishing. It does not expand the degree-\(5^k\) field. The certified nonzero boxes and unary gate degrees are substantive input conditions. The complete baseline proof belongs in the manuscript, not a repository-only dependency.

Set \(R=y_k^2-x_kz_k=X^{\mathsf T}TX\). Here \(\|T\|=1,\|T\|_F^2=3/2\); formula (A) gives a rational Hessian Gram \(B\) of \(R^2\) of norm at most 16. With \(\mu=\rho(M)\), \(\lambda=\lceil17/\mu\rceil\) yields \(\lambda M-B\succeq I\) for \(F_k=\lambda F_0-R^2\). Value and gradient vanish at \(p\), so this proves nonnegativity and unique zero. The scaling has polynomial bit length. Its field proof applies to every larger scale satisfying this curvature margin.

For completeness, let \(a^D=2\), \(D=5^k\), and \(r=[E(a):E]\) for any real subfield. The minimal polynomial divides \(T^D-2\); its real constant term implies \(a^r\in E\). For \(g=\gcd(r,D)\), Bézout gives \(a^g\in E\), and \(T^g-a^g\) gives \(r\le g\le r\). Thus \(r\mid D\), and the minimal polynomial is \(T^r-a^r\). If \(a\notin E\), then \(r\ge5\). The degree of \(a^5\) over \(E\) is at most \(r/5\); adjoining \(a\) over \(E(a^5)\) has degree at most five. The tower identity forces \([E(a):E(a^5)]=5\). This remains valid for transcendental \(E\).

Put \(L=E(a_k^5)\), which contains all earlier tower coordinates. Restrict earlier gates to their coordinates in \(p\). Over \(L\), \(T^5-b\), \(b=a_k^5\), is irreducible, and the last-gate vanishing basis is
\[
q=(x^2-y,xy-z,y^2-xz,yz-b,z^2-bx).
\]
Evaluation of \(1,x,y,z,xz\) proves rank five. The fifteen products are independent: their leading quadratics \(x^2,xy,y^2-xz,yz,z^2\) have products spanning every ternary quartic monomial. The quadratic-space note prints elementary identities for the five less immediate monomials; use them instead of an unexplained determinant.

The restricted polynomial is
\[
\lambda(g^2+\nu^{-2}(q_1^2+q_2^2+q_4^2))-q_3^2.
\]
Writing \(g=\sum c_jq_j\), positive definiteness of \(G\)'s homogeneous matrix gives positive \(z^2\)-coefficient, hence \(c_5>0\). The vector \((0,0,c_5,0,-c_3)\) annihilates all positive factors and has Gram value \(-c_5^2\). Product independence makes that indefinite restricted Gram unique. Any \(E\)-SOS restricts to an \(L\)-SOS with vanishing quadratic factors, a contradiction. Any \(E\)-valued PSD Gram restricts by congruence to an \(L\)-valued PSD Gram, and PSD row restriction gives the same contradiction. If \(a_k\in E\), Taylor at \(p\in E^n\) proves sufficiency. Eisenstein gives rational degree \(D\).

**Individual-degree lemma.** Suppose algebraic \(\beta_i\) generate a field containing \(a=2^{1/D}\). Put \(Z=\mathbb Q(\zeta_D)\), \(Z^+=\mathbb Q(\zeta_D+\zeta_D^{-1})\). The latter is totally real. The real-field lemma gives \([Z^+(a):Z^+]=D\), because a smaller degree would put a nontrivial odd root of two, with nonreal conjugates by Eisenstein, in a totally real field. Since \(Z^+(a)\) is real and \(Z/Z^+\) has degree two, \([Z(a):Z]=D\). Its splitting field therefore has an automorphism fixing \(Z\), \(a\mapsto\zeta_Da\), of order \(D\). Let \(T\) be the compositum of the normal closures of \(\mathbb Q(\beta_i)\). Its Galois group embeds in \(\prod_i\mathfrak S_{d_i}\), \(d_i=[\mathbb Q(\beta_i):\mathbb Q]\). Normality gives \(Z(a)\subseteq T\), with surjective restriction. If all \(d_i<D\), every product element has 5-primary order at most \(5^{k-1}\), since no cycle has length divisible by \(5^k\). A lift of the order-\(D\) automorphism is impossible. Hence some \(d_i\ge D\), regardless of the number of coefficients.

The compact upper bound uses the rational Hessian Gram, binary square conversion, and Taylor SOS. Its quadratic factors have coefficients of degree at most two in the coordinates of \(p\). A shared circuit with \(k\) positive fifth-root gates and polynomially many rational arithmetic gates constructs them in polynomial size. The lower bound excludes neither sparse defining polynomials nor radicals, towers, circuits, or transcendental descriptions; \(T^{5^k}-2\) itself is sparse.

## 4. Trace descent and arbitrary primes

If rational \(f\) is SOS over a finite totally real field \(K\), apply normalized trace to its square factors. In a rational basis of \(K\), \(\operatorname{Tr}(z^2)/[K:\mathbb Q]\) is rational positive definite because all embeddings are real. Rational congruence and rational square conversion give a rational SOS. A Galois hypothesis is unnecessary. A subfield of \(\mathbb R\) need not be totally real; \(\mathbb Q(2^{1/5^k})\) has nonreal embeddings. Odd degree alone does not force descent. Also a field-valued Gram PSD only at one embedding need not be PSD at every embedding; one cannot silently apply this square-factor trace argument to such a Gram.

The [arbitrary-prime family](../../../research-20260927/arbitrary-prime-strict-sos-field.md) gives, for every odd prime \(\ell\ge5\), an integer quartic in \(n=(\ell+1)/2\) variables and integer full strict Hessian Gram, polynomial-time constructible in \(\ell\), with \(O(\ell^2)\) polynomial monomials and \(O(\log\ell)\)-bit polynomial and Gram entries. Its unique zero is \((a^s,\ldots,a^{2s})\), \(s=(\ell-1)/2,a=2^{1/\ell}\). Its SOS/PSD-Gram fields are exactly the real fields containing \(a\). Construction time is polynomial in output dimension, not binary \(\log\ell\); field degree grows only linearly with dimension.

The obstruction is \(\Lambda(P)=[x_s]P+[x_0^2]P\). For a vanishing quadratic, irreducibility implies its coefficients satisfy \(v_s+h_{00}=0\), so \(\Lambda(q^2)=v_0^2\). The baseline factors lie in the subspace with \(v_0=0\); the removed \(r=x_1x_s-2x_0\) has \(\Lambda(r^2)=4\). The explicit exposing quadratic, regular residual Jacobian, and rational weight approximations in the note give
\[
N_0=2^{20}n^8,\quad D_0=64(n+1)N_0^2,\quad
F=A^2+(D_0/N_0)^2\sum R_i^2-r^2.
\]
The saved all-prime Schur estimates prove a centered positive Hessian Gram, and Section 5 below proves its direct integer recovery. Prime irreducibility over arbitrary real fields uses the same constant-term/Bézout argument as the ternary example. For PSD necessity, the constant-row relation gives
\[
\Lambda(F)=2Q_{1,x_s}+Q_{x_0,x_0}+2Q_{1,x_0^2}
=Q_{x_0,x_0}\ge0,
\]
a contradiction. Taylor proves sufficiency. I found no missing universal step in the construction or its coefficient bounds. Do not call its linear field-degree growth a superpolynomial output lower bound.

## 5. Exact covariance of canonical Hessian Grams

Formula (A) is covariant under translation. Set \(A_c=c\otimes I\). Direct tensor multiplication gives
\[
\begin{aligned}
A_c^{\mathsf T}Q(T)&=D(2Tc,T),\\
A_c^{\mathsf T}Q(T)A_c&=8(Tc)(Tc)^{\mathsf T}+4(c^{\mathsf T}Tc)T,\\
D(b,T)A_c+A_c^{\mathsf T}D(b,T)^{\mathsf T}
&=4(b^{\mathsf T}c)T+4b(Tc)^{\mathsf T}+4(Tc)b^{\mathsf T}.
\end{aligned}
\]
The congruence for \(u=X-c\) changes the canonical Gram into the same formula with \(b'=b-2Tc,d'=d-b^{\mathsf T}c+c^{\mathsf T}Tc\). Linearity extends this to rational weighted or signed sums of quadratic squares.

Thus a positive canonical Gram proved at an algebraic common zero translates exactly to the canonical Gram computed from the rational factors at center zero. It is rational and PD. Integer factors give integer entries because \(d,b,2T\) are integer. Congruence need not preserve the same numerical matrix margin. This is already used in the arbitrary-prime note, and it shortens the graph theorem in Section 10. It is not a claim about arbitrary Gram parametrizations.

## 6. Rational-function certificates and general multipliers

Sources: [fixed denominator](../../../research-20260927/rational-denominator-certificate-frontier.md), [tower denominator](../../../research-20260927/rational-tower-quadratic-denominator.md), [affine membership](../../../research-20260927/rational-quadratic-perturbation-multipliers.md), and [higher membership](../../../research-20260927/rational-quadratic-multipliers-higher-membership.md).

For the exact ternary \(F\), \(h=1+x^2+y^2+z^2\) gives rational SOS \(hF\). The [saved checker](../../../research-20260927/check_ternary_rational_sos_quadratic_multiplier.py) prints a fifteen-entry cubic vector \(b\) and integer matrix \(N\) with \(b^{\mathsf T}Nb=8hF,N-8I\succ0\); the [fresh review](../../../research-20260927/rational-denominator-certificate-fresh-review.md) records all fifteen positive leading principal minors. Print these finite data in a self-contained appendix. Referring to the checker is insufficient.

A multiplier is not a common denominator. From \(hP=\sum f_i^2\),
\[
P=\sum_i(f_i/h)^2+\sum_{i,j}(X_jf_i/h)^2.
\]
The cleared identity is \(h^2P\), not \(hP\). The common denominator has degree two, numerator degrees at most four. Degree two is minimal when \(P\) is not rational polynomial SOS: a nonconstant rational affine denominator \(\ell\) would give \(\ell^2P=\sum u_i^2\). Every \(u_i\) vanishes on the real hyperplane \(\ell=0\), so rational polynomial division gives \(\ell\mid u_i\); cancellation yields a polynomial SOS. This also covers rational identities initially interpreted off their poles.

For the tower, increase the polynomial-bit scale to obtain a polynomial-size certificate with the same \(h\), preserving all field lower bounds. The original \(\lceil17/\mu\rceil\) prescription is not proved to satisfy this extra denominator requirement.

The constructive general interface is as follows. Supply quadratics \(q_i\), \(F_0=\sum q_i^2\), a quadratic \(G=X^{\mathsf T}HX+\ell^{\mathsf T}X+c\) in their constant span with \(H\succ0\), quadratic targets \(R_a\) in the affine span of \(q_i,X_jq_i\), and rational symmetric \(J\). Polynomial time constructs a polynomial-bit integer \(\lambda_*\) and cubic-square rational SOS of \(h(\lambda_*F_0-R^{\mathsf T}JR)\). A supplied larger rational scale counts its own bit length as input. The algorithm does not discover an unspecified positive \(G\).

The full identity is short. Let \(w=(q_i,X_jq_i)\), coordinate vectors \(g,a_a\) represent \(G,R_a\), and columns of \(U\) represent \(X_jG\). Write \(R_a=X^{\mathsf T}T_aX+r_a^{\mathsf T}X+s_a\), \(b_a=XR_a\), and \(v=(w,b_1,\ldots,b_s)\). Define
\[
\begin{aligned}
A&=c\sum_a a_aa_a^{\mathsf T}-\tfrac12\sum_a s_a(ga_a^{\mathsf T}+a_ag^{\mathsf T}),\\
C_a&=(a_a\ell^{\mathsf T}-UT_a-gr_a^{\mathsf T})/2,\qquad \mathcal H=I_s\otimes H.
\end{aligned}
\]
Then \(v^{\mathsf T}\left(\begin{smallmatrix}A&C\\C^{\mathsf T}&\mathcal H\end{smallmatrix}\right)v=0\): its terms per target are \(GR_a^2-GR_a(X^{\mathsf T}T_aX+r_a^{\mathsf T}X+s_a)\). The linear and constant corrections are necessary. Set \(\eta=\rho(H)\), \(B_A=\sum|A_{ij}|\), and
\[
\epsilon=\min\{1,[2(1+B_A)]^{-1},\eta/[4(1+\|C\|_F^2)]\}.
\]
The Gram
\[
Q_\epsilon=\begin{pmatrix}I+\epsilon A&\epsilon C\\
\epsilon C^{\mathsf T}&\epsilon\mathcal H\end{pmatrix}\succ0
\]
represents \(hF_0\). Its top block is at least \(I/2\), Schur complement at least \(\epsilon\eta I/2\). The target Gram is \(D_J=\operatorname{diag}(A_RJA_R^{\mathsf T},J\otimes I_n)\), \(A_R=(a_a)_a\). Choose \(\lambda_*\ge(1+\max_i\sum_j|(D_J)_{ij}|)/\rho(Q_\epsilon)\), so \(\lambda_*Q_\epsilon-D_J\succeq I\). Matrix dimensions and rational entries have polynomial size. Redundant polynomial entries cause no problem: positivity concerns their coefficient matrix. \(J\) can be indefinite; no common zero is required. If a full strict rational Hessian Gram for \(F_0\) is supplied, a separate rational scale dominates a symmetric Hessian Gram of the subtracted quartic and preserves strong SOS-convexity. That optional Hessian certificate must be counted as input.

For the tower \(R=xr_{k,2}-yr_{k,1}\), and \(G\) is a positive rational multiple of the first baseline factor. The field proof's negative direction is independent of the scale, so all field and individual-degree conclusions survive.

The higher-membership theorem assumes \(R_a=\sum_i u_{ai}q_i\), \(\deg u_{ai}\le d\), and gives \(h^d(\lambda_*F_0-R^{\mathsf T}JR)\) rational SOS with factors of degree at most \(d+2\). Complexity is polynomial in explicit coefficient length and \(B=\binom{n+d}{d}\), plus \(n,m,s,d\), not binary \(\log d\). Use \(w=(X^\alpha q_i)_{|\alpha|\le d}\) with positive multinomial diagonal Gram, and new blocks \(b_{a,\alpha}=X^\alpha XR_a\), \(|\alpha|\le d-1\). Each zero identity is the preceding target identity multiplied by \(X^{2\alpha}\). Give a new block level \(|\alpha|+1\). If \(K_0\) is total absolute-entry norm of all identity terms except positive \(H\) blocks, set \(\eta_0=\min(1,\rho(H))\), \(\rho_0=\eta_0/[2(1+K_0)]\), and add level-\(l\) identities with weights \(\rho_0^{2l}\). Congruence by \(\rho_0^{-l}\) leaves positive blocks \(I,H\), while each correction retains an extra power of \(\rho_0\). Its norm is below \(\eta_0/2\); undoing gives \(Q\succeq\eta_0\rho_0^{2d}I/2\). A target Gram is dominated by an explicit rational-bit integer scale. This proves the universal degree and size bounds without repeated determinant growth. The final zero set equals the baseline common zero set because its PD matrix list includes all \(q_i\).

The common denominator is \(h^{\lceil d/2\rceil}\), after multiplying once more by \(h\) for odd \(d\). Denominator degree is \(2\lceil d/2\rceil\), numerator degree at most \(2\lceil d/2\rceil+2\); no minimum-degree claim follows. For \(d=0\), direct Gram domination gives a polynomial SOS. Targets remain quadratic; higher-degree negative squares can defeat nonnegativity at infinity. The saved degree-two membership example with target \(1\) and no common complex zero proves affine membership is a strict restriction, not that multiplier exponent two is necessary.

The broad regular-denominator conclusion is an imported prior-theory corollary: rational nonnegative even-degree \(P\), positive definite leading form, finitely many real zeros, and positive definite Hessian at zeros imply \(h^NP\) rational SOS for some \(N\). The empty zero set is allowed. The saved sphere-ring deduction handles rational descent through the rational vanishing ideal of algebraic sphere zeros, membership in its square from first-order vanishing, an ideal-square order unit, and pure-state positivity: evaluations off the zeros and nonzero PSD tangent forms at zeros. Homogenization and antipodal averaging give the rational radial multiplier. The real-coefficient geometric Hessian theorem alone does not establish rational descent. The root's literature review must confirm the exact general-ring pure-state/order-unit contracts. This qualitative result gives finiteness of each radial order, not a uniform degree or useful bit bound.

## 7. Radial order and adaptive denominators

Sources: [radial theorem](../../../research-20260927/rational-radial-exponent-obstruction.md), [recursive separators](../../../research-20260927/rational-radial-quantitative-separation.md), and [height bound](../../../research-20260927/rational-radial-height-lower-bound.md).

For integers \(t>0\), \(f_t(X)=t^{-2}F(tX)\) stays strongly SOS-convex with a full strict rational Hessian Gram, unique zero \(p/t\), and \(\nabla^2f_t(p/t)=\nabla^2F(p)\). Its input length is \(I(t)=\Theta(1+\log t)\); \([X_1^4]f_t=104t^2\) proves the lower bound. Adaptive \(h_t=1+t^2\|X\|^2\) gives \(h_tf_t=(b(tX)/t)^{\mathsf T}(N/8)(b(tX)/t)\), hence a degree-two denominator and rational certificate of size \(O(I)\).

For every fixed \(N\), \(h^Nf_t\) fails rational SOS for all sufficiently large integers \(t\). The correct cone is \(C_d=\{\sum q_j^2:q_j\in V_d\}\), \(V_d=I_d(p)\otimes_{\mathbb Q}\mathbb R\), not all real polynomials vanishing at \(p\). It is closed: integrate a basis-vector outer product over a ball to get \(T\succ0\); convergence of polynomial images bounds \(\operatorname{tr}(QT)\), hence PSD \(Q\)'s trace and norm, so a convergent subsequence exists. Arbitrary PSD linear images need not be closed. If \(F\in C_d\), degree cancellation forces factors to degree at most two, and rational kernel restriction gives \(V_d\cap\mathbb R[X]_{\le2}=V_2\). Then \(\Lambda(F)=-4\) contradicts positivity. Now \((1+t^{-2}\|x\|^2)^NF\to F\), and any rational SOS factors at its zero lie in \(I_{N+2}(p)\). The same proof excludes a fixed finite menu of rational multipliers with positive values at zero.

The quantitative separator is explicit. Use representatives \((1,y,z,yz,x)\). For \(m=x^iy^jz^k\), let \(e=4i+j+2k,r=e\bmod5\), \(c_m=2^{\lfloor e/5\rfloor-i-k+\mathbf1_{r\ge2}}\). Then \(q_m=m-c_m\rho_r\) is a nested basis of \(I_d\). The base functional is \(\lambda_2=\Lambda+E/28450\), \(E(P)=\sum_{u\in\{0,1,2\}^3}P(u)\); grid unisolvence makes it strictly positive on nonzero \(V_2\)-squares, and recorded exact evaluation gives \(\lambda_2(F)=-85351/28450\).

At degree \(d\), extend the old functional by zero in degrees \(2d-1,2d\), obtaining Gram blocks \(A,B,C\) with \(A\succ0\). The top-degree grid functional \(M_d(P)=\sum_{u\in\{0,\ldots,d\}^3}P_{2d}(u)\) affects only the new homogeneous block, with integer PD Gram \(D\). Set \(S=C-B^{\mathsf T}A^{-1}B\), \(m_d=\max_i\sum_j|S_{ij}|\), \(\beta_d=\rho(D)\), \(T_d=\lceil(m_d+1)/\beta_d\rceil\). Adding \(T_dM_d\) gives Schur complement at least \(I\), preserves the negative value on \(F\), and preserves a common denominator dividing 28450. This induction, not the historical first-step computation, proves all degrees.

With \(A_N=\sum_{j=1}^N|\binom Nj\lambda_{N+2}(\|X\|^{2j}F)|\), the threshold
\[
\tau_N=\left\lceil\sqrt{\max\{1,2(A_N+1)/(85351/28450)\}}\right\rceil
\]
excludes order \(N\) for all integers \(t\ge\tau_N\). The saved denominator/adjugate analysis gives \(b_2=17\),
\[
b_d\le64d^3b_{d-1}\le17\cdot64^{d-2}(d!/2)^3,\qquad
\tau_N\le2^{34\cdot64^N((N+2)!/2)^3}
\le2^{2^{10(N+2)\log_2(N+3)}}.
\]
For \(u=\log_2\log_2t\ge1024\), choose \(N=\lfloor u/(40\log_2u)\rfloor\). Then \(\tau_N\le t\). Upward closure of radial SOS excludes all smaller orders too. Thus the finite least order satisfies
\[
\nu(t)=\Omega\!\left(\frac{\log\log t}{\log\log\log t}\right)
=\Omega\!\left(\frac{\log I}{\log\log I}\right).
\]
The quantifier is every sufficiently large integer \(t\); no monotonicity of actual orders is assumed. The height recurrence and inversion are coherent. Do not extend \(I=\Theta(\log t)\) to arbitrary rational parameters. These are rational hierarchy order lower bounds; all family members are real SOS at order zero. They are neither unrestricted rational certificate-length bounds nor optimization-time bounds.

## 8. Rational quartic block lift

Source: [block theorem](../../../research-20260927/rational-block-sos-splitting-obstruction.md).

Supply rational quartic \(f\), promised minimum zero, and a full strict rational Hessian Gram \(A\); the minimizer need not be supplied. Put \(\rho=\rho(A),\mu=\rho/2\), introduce \(r_{ij}=y_iy_j-z_{ij}\), and replace a fixed quadratic pair in each cubic monomial of \(\nabla f(y)\) by \(z_{ij}\). The resulting quadratic \(a(y,z)\) satisfies \(\nabla f-a=E(y)r\), with homogeneous linear \(E\). Define
\[
g(y,z)=\frac{\|a(y,z)\|^2}{2\mu}-f(y)+\lambda\|r(y,z)\|^2.
\]
Polynomial bit time constructs \(\lambda,g\), and a polynomial-size rational SOS of \(f(x)+g(y,z)\) with quadratic factors. Also \(g\ge0\) and \(g(p,(p_ip_j))=0\). No convexity of \(g\) is asserted here.

With \(d=x-y,w=(d,y\otimes d,d\otimes d)\), the Taylor remainder Gram is
\[
M=\begin{pmatrix}
A_{00}/2&A_{01}/2&A_{01}/6\\
A_{10}/2&A_{11}/2&A_{11}/6\\
A_{10}/6&A_{11}/6&A_{11}/12
\end{pmatrix}.
\]
It dominates \(\rho[\tfrac12I_n\oplus(\left(\begin{smallmatrix}1/2&1/6\\1/6&1/12\end{smallmatrix}\right)\otimes I_{n^2})]\). The scalar block determinant is \(1/72\), so \(N=M-\mu\operatorname{diag}(I_n,0,0)/2\succ0\). Take rational \(D\) with \(e^{\mathsf T}d=r^{\mathsf T}Dw\), \(\delta=\rho(N)\), \(\lambda=\lceil1+\|D\|_F^2/(4\delta)\rceil\). Then \(K=\left(\begin{smallmatrix}N&D^{\mathsf T}/2\\D/2&\lambda I\end{smallmatrix}\right)\succ0\), and
\[
f(x)+g(y,z)=(w,r)^{\mathsf T}K(w,r)+\frac\mu2\|d+a/\mu\|^2.
\]
Expansion uses \(e+a=\nabla f\); this checks the important error sign. At the graph zero \(a=r=0\). Substituting \(x=p\) in the joint SOS proves \(g\ge0\). All determinant and coefficient operations have polynomial bit bounds.

Apply the lift to \(f_k\). The joint polynomial is short rational SOS, but separated SOS or separated PSD polynomial Grams over \(E\) exist exactly when \(a_k\in E\). Grouping separate certificates gives \(f_k+c=S_x,g_k-c=S_{y,z}\), \(c\in E\). Evaluation at the two zero minima forces \(c=0\), so the first block invokes the tower field theorem. Conversely, if \(a_k\in E\), specialize the joint rational SOS at \(x=p_k\in E^{3k}\) for \(g_k\), and use Taylor SOS for \(f_k\). PSD necessity uses the separate Gram field theorem, without a factorization assumption. Total variables are \(\Theta(k^2)\), hence individual coefficient degree \(5^{\Theta(\sqrt n)}\), not \(5^{\Theta(n)}\).

## 9. Strongly SOS-convex blocks and rational height cost

Sources: [fixed-field padding](../../../research-20260927/strongly-sos-convex-block-splitting-obstruction.md) and [graph extension](../../../research-20260927/quadratic-graph-quartic-realization.md).

The padding input must include a **supplied rational SOS of the baseline**, in addition to its strict Hessian Gram. For \(B_0\ge0\) in \(r\ge1\) variables, unique zero \(p\), and \(s\ge1\) new coordinates,
\[
B(u,v)=B_0(u)+\epsilon\|v\|^2(1+\|u\|^2+\|v\|^2)
\]
works with \(\epsilon\le\min(1,\rho(A_0)/(16rs))\). Polynomial output length counts the expanded baseline and its supplied SOS. The new Hessian diagonal blocks are \(2\epsilon I_s,2\epsilon I_{rs},2\epsilon I_{sr},4\epsilon I_{s^2}+8\epsilon\operatorname{vec}(I_s)\operatorname{vec}(I_s)^{\mathsf T}\). The old-new cross block has norm squared \(16\epsilon^2rs\); its Schur subtraction leaves margin at least \(\epsilon I\). Its unique zero is \((p,0)\), and an invertible rational affine map preserves the full strict Gram. Without a supplied baseline SOS the output-length claim is unjustified.

For the fixed quintic graph, a four-coordinate rational SOS power-basis realization of \((a,a^2,a^3,a^4)\) and five padded affine coordinates give a rational SOS \(B\) on the nine lifted variables, at the same graph zero, with full strict Gram \(A_B\). A rational symmetric Hessian Gram \(C\) of \(g_0\) is dominated by taking \(T\ge(1+\sum|C_{ij}|)/\rho(A_B)\). Then \(g=g_0+TB\) is strongly SOS-convex; the joint rational SOS and zero-shift obstruction survive. This fixed-field argument is independent of the growing-field graph theorem.

For the positive family import the interior-Gram lower-bound quartic \(h_k\) in \(2k\) variables, with short rational SOS and full strict Hessian Gram, whose attained minimum satisfies
\[
0<m_k<4M_k^{-2^{k+1}},\qquad M_k=1000^{k+3}.
\]
Then \(P_k=f(x)+g(w)+h_k(t)\) is short rational strongly SOS-convex in \(12+2k\) variables. Fix blocks \(x\) and \((w,t)\). Rational separated certificates exist: choose rational \(0<c<m_k\), rational \(q\) near \(p\), and rational \(s\) with \(f(q)<s<m_k-c\). Specialize the joint certificate to get \(g+f(q)\), add \(s-f(q)\), and use the strict Taylor lemma for \(f+c\) and \(h_k-c-s\). This gives existence with no short-bit promise.

Every separated rational certificate has \(0<c\le m_k\); \(c=0\) would certify \(f\). For reduced \(c=a/b\), \(\log_2b>2^{k+1}\log_2M_k-2\). The Gram model is **two separately stored local PSD Grams, each with its own constant monomial**. The first matrix satisfies \(Q_{00}=f(0)+c\); with fixed denominator \(b_0\) of \(f(0)\), \(\operatorname{den}(c)\le b_0\operatorname{den}(Q_{00})\). Hence one entry needs \(\Omega(k2^k)\) denominator bits, without requiring PD. For unweighted separated SOS, \(c=\sum_j u_j(0)^2-f(0)\), whose denominator divides \(b_0\prod_j\operatorname{den}(u_j(0))^2\); total coefficient denominator length is \(\Omega(k2^k)\).

A single joint matrix with one shared constant coordinate can hide its allocation. Do not state this bound for that storage convention without extra extraction data. The unrestricted joint SOS stays short and rational. The bound is exponential in the constructed dimension and superpolynomial in its polynomially bounded input length, not claimed exponential in every input bit. Positive weights, if permitted, must be counted as data or converted to the specified unweighted format.

## 10. Quadratic graph realization: shorter proof interface

The graph theorem is sound. From rational quartic \(f\), promised minimum zero, and a supplied full strict rational Hessian Gram, polynomial bit time constructs rational SOS quartic \(B(y,z)\), full strict rational Hessian Gram, and unique zero \(w_*=(p,(p_ip_j)_{i\le j})\), without expanding \(p\). There are \(N=n+n(n+1)/2\) variables. The algorithm uses the promise; it does not decide it.

Let \(\rho=\rho(A),U=\operatorname{tr}A,P=1+\|\nabla f(0)\|_1/\rho\), so \(\|p\|\le P\). The imported bit-model convex approximation theorem on \([-P-1,P+1]^n\), with objective tolerance \(\min(1,\rho\eta^2/2)\), returns rational \(q\) with \(\|q-p\|\le\eta\) in time polynomial in input and \(\log(1/\eta)\). Its exact source contract must be vetted; it is not an exact oracle.

Put \(d=y-q,s_{ij}=z_{ij}-q_iy_j-q_jy_i+q_iq_j\), and let \(C\) duplicate symmetric coordinates into the ordered tensor. Define
\[
G_q=f(q)+\nabla f(q)^{\mathsf T}d+
\int_0^1(1-t)(d,q\otimes d+tCs)^{\mathsf T}A(d,q\otimes d+tCs)\,dt.
\]
It is rational quadratic. Graph restriction is exactly \(f(y)\), so \(G_q(w_*)=0\) for every rational \(q\). Uniform bounds for \(\|q-p\|\le1\) are
\[
J=4(P+2),\quad m_0=\rho/(48J^2),\quad
L_0=10U(P+2)^2J^2,\quad K=2P^2,
\]
with \(m_0I\preceq H_q\preceq L_0I\), \(\|w_*\|\le K\). The scalar integration block has determinant \(1/72\), trace \(7/12\), and eigenvalue at least \(1/42>1/48\); the affine chart and inverse have norms at most \(J\). A coefficient-sum derivative majorant for the fixed-degree polynomial \(\Phi(q,t)=\nabla G_q(t,(t_it_j))\) gives a polynomial-bit rational \(D_\Phi\) with \(\|\nabla G_q(w_*)\|\le D_\Phi\|q-p\|\), since \(\Phi(p,p)=0\).

Residuals \(R=(a,r)\) from the gradient lift have unique zero \(w_*\) and \(|\det J_R(w_*)|=\det\nabla^2f(p)\ge\rho^n\), by the triangular change \((y,z)\mapsto(y,r)\). The saved coefficient bounds give normalization \(\widetilde R=R/C_0\), gradients \(b_j\), quadratic matrices \(T_j\), and polynomial-bit \(V,\nu>0\) with \(\|T_j\|\le1,\|b_j\|\le V,\sum b_jb_j^{\mathsf T}\succeq\nu^2I\). Choose a positive rational square
\[
\epsilon\le\min\{1,m_0^2/(2N),\nu^2m_0^2/[36N(L_0+NV)^2]\}
\]
and approximate \(q\) to error \(\min(1,\epsilon/D_\Phi)\). Then \(B_*=G_q^2+\epsilon\sum\widetilde R_j^2\) has short rational SOS and unique zero \(w_*\).

Formula (A), centered at \(w_*\), gives
\[
C\succeq2\epsilon\nu^2I,\quad Q\succeq2m_0^2I,\quad
\|D\|\le6\sqrt N\epsilon(L_0+NV),\quad
C-DQ^{-1}D^{\mathsf T}\succeq\tfrac32\epsilon\nu^2I.
\]
The negative tensors \(T_j\otimes T_j\) are retained; individual squared quadratics are not assumed convex. The Schur subtraction is at most \(18N\epsilon^2(L_0+NV)^2/m_0^2\le\epsilon\nu^2/2\). A rational lower margin after translation is
\[
\gamma=\frac{\min\{(3/2)\epsilon\nu^2,2m_0^2\}}
{(2+2[B_D/(2m_0^2)]^2)(2+K)^2},\qquad
B_D=6N\epsilon(L_0+NV).
\]
Section 5 shows that the translated matrix is exactly the canonical Gram computed from the rational factors at center zero. It is rational, directly computable, and at least \(\gamma I\). There is a simpler normalization that preserves the square count. Write \(\epsilon=t_0^2\), and set
\[
B=\frac{B_*}{\epsilon\nu^2}
=\left(\frac{G_q}{t_0\nu}\right)^2+
\sum_{j=1}^{N}\left(\frac{\widetilde R_j}{\nu}\right)^2.
\]
Completing the centered Gram block square gives the directional bound \(\nabla^2B_*\succeq(3/2)\epsilon\nu^2 I\), so \(\nabla^2B\succeq(3/2)I\). This is a bound for the evaluated Hessian, not the least eigenvalue of its full Gram. The direct rational full Gram stays PD by congruence, and the certificate has exactly \(N+1\) rational quadratic factors. The independently audited minimum-SOS-length theorem makes this number minimal even over \(\mathbb R\). If a full matrix margin of \(I\), rather than a Hessian margin, is desired, scaling by \(2/\gamma\) and binary rational-square conversion gives that additional certificate. The saved second center approximation and coefficient projection are sound but unnecessary.

Apply \(B_k\) at the growing-field block lift's graph zero, add a polynomial-bit multiple to dominate the second block's symmetric Hessian Gram, and obtain two strongly SOS-convex blocks. The joint rational SOS and least separated field remain unchanged. Dimension is \(\Theta(k^2)\), coefficient-degree bound \(5^{\Theta(\sqrt N)}\).

Every **PSD** Gram on the full joint Hessian basis of an additive disjoint-block polynomial is singular. A coordinate \(X_jv_i\) belonging to different point and direction blocks has zero coefficient on \(X_j^2v_i^2\); this monomial comes only from its diagonal entry. A PSD zero diagonal forces a zero row. Short rational Hessian SOS still follows by adding local certificates, consistently with global strong convexity. Do not say every symmetric Gram is singular: the closing scope review gives a nonsingular indefinite counterexample.

## 11. Auxiliary certificates and tower relation spaces

Sources: [auxiliary identity](../../../research-20260927/tower-rational-auxiliary-certificate.md), [quadratic space](../../../research-20260927/tower-quadratic-vanishing-space.md), and [stationary space](../../../research-20260927/tower-quartic-stationary-space.md).

For the signed-square tower \(F=\sum w_jq_j^2\), let \(M\) be its **final** rational Hessian Gram, \(u=X-Y,A=(u,Y\otimes u),B=(0,u\otimes u)\). The rational SOS
\[
s(X,Y)=\tfrac12(A+B/3)^{\mathsf T}M(A+B/3)+\tfrac1{36}B^{\mathsf T}MB
=F(X)-F(Y)-\nabla F(Y)^{\mathsf T}(X-Y)
\]
gives \(F(X)=s(X,Y)+\sum H_jq_j(Y)\), where \(H_j=w_j(q_j(Y)+2\nabla q_j(Y)^{\mathsf T}(X-Y))\). Certificate degree is four and total size polynomial. The auxiliary equations have a real solution by odd-root recursion. Existence is essential; an identity modulo inconsistent equations does not prove nonnegativity. \(G,R\) are redundant: \(R_i=-y_ir_{i,1}+x_ir_{i,2}\), \(S_i=-z_ir_{i,2}+x_ir_{i,3}\), and the exposing \(G\) is a constant rational combination of these and chain residuals. Removing the two redundant equations leaves certificate degree at most five. This is a standard equality-ideal proof format.

The full rational quadratic vanishing basis has exactly five relations per gate:
\[
x_i^2-y_i,\quad x_iy_i-z_i,\quad y_i^2-x_iz_i,\quad
y_iz_i-b_i,\quad z_i^2-b_ix_i.
\]
Eliminate distinct pivots \(x_i^2,x_iy_i,y_i^2,y_iz_i,z_i^2\). Remaining monomials are \(1\), four per gate \(x_i,y_i,z_i,x_iz_i\), and nine cross products per gate pair. Their evaluations have distinct base-five exponent patterns below \(5^k\); Eisenstein gives independence and \(\dim I_2=5k\). This correctly handles the first-gate wrap and later three-monomial collision. One must not assume every evaluation collision class has size two.

All unordered pair products are independent. Induct on gates: last-gate degree four kills local-local coefficients using the fifteen leading products; degree two kills earlier relations coupled to last-gate leading quadratics; earlier product independence finishes. Scalar extension to \(\mathbb R\) preserves coefficient rank.

For rational quartics with this supplied zero, rational SOS recognition is product-span membership and one PSD test of the unique order-\(5k\) rational matrix. A rational full-basis PSD Gram is unique too, by row restriction and a rational left inverse. Coefficient matching, PSD elimination, and binary conversion run in polynomial time. Zero validation collects evaluations with exponent residues modulo \(5^k\), using \(O(k)\)-bit exponents, not a dense field. This does not recognize real SOS or discover an unknown tower zero.

The universal stationary theorem is \(J_{3,k}=0,J_{4,k}=\{q^{\mathsf T}Aq:A\in\operatorname{Sym}_{5k}(\mathbb Q)\}\). Its local cubic first-jet map at \((a,a^2,a^3)\), over \(L\) with irreducible \(T^5-b\), has five residue blocks with determinants \(5,5b,-5b,-5b,-5b\), hence is invertible. Gate induction specializes away last-gate cubics, uses affine independence to kill high-degree coefficients, and first derivatives to force remaining coefficients stationary. For quartics remove fifteen last-gate leading products first. In the remaining quadratic part, earlier stationarity forces the sum of \(y_k^2,x_kz_k\) coefficients to vanish; it is therefore a combination of five leading relations times earlier \(I_2\). Remove those cross products and use the cubic and earlier quartic inductions. This is a complete uniform proof, not finite rank evidence. Ambient stationarity is required; a constrained optimum need not satisfy it.

## 12. Pending convex descent criterion

Source: [criterion](../../../research-20260927/convex-quartic-descent-criterion.md). Its historical fresh-review status was pending. I reconstructed its proof; another audit owns the imported universal minimum-SOS-length theorem.

Assume \(\dim_{\mathbb Q}I_2(p)=n+1,J_4(p)=W(p)\), and a rational SOS polynomial \(G\) of degree exactly four is globally convex, \(G(p)=0,\nabla^2G(p)\succ0\). Then every rational globally convex polynomial \(F\) of degree exactly four with zero value/gradient and positive definite Hessian at \(p\) has a PD rational Gram in any rational basis of \(I_2(p)\), hence is rational SOS.

The required length theorem states that a globally convex degree-exactly-four polynomial with a zero and PD Hessian there needs at least \(n+1\) real quadratic squares. Therefore a PSD baseline matrix on the \(n+1\)-dimensional vanishing basis is PD. If a rational symmetric matrix \(S\) representing \(F\in W\) were not PD, the segment from the baseline to \(S\) reaches a first singular PSD point of rank at most \(n\). Its polynomial remains convex, has PD Hessian at \(p\), and degree four: the nonzero nonnegative leading forms cannot cancel in a convex combination. Its at-most-\(n\) real squares contradict the length theorem. Moving along a nonzero product-map kernel direction gives the same contradiction, proving injectivity and uniqueness. Product independence is not an initial assumption.

The conditional universal criterion is sound. Its cyclic applications are only the recorded exact dimensions \(n=2\) and \(n=4,\ldots,16\). Dimension three has five vanishing quadratics and fails the dimension hypothesis. No all-dimension cyclic collision/rank theorem is proved. Keep the table explicitly finite, or omit its applications from the theorem package. A submission retaining those applications should supply exact rank certificates; a historical script's existence is not a self-contained proof. No rerun was authorized or performed here.

## 13. Optimal moment, maximal-rank Gram, and exposing fields

Source: [strict-Hessian moment arithmetic](../../../research-20260927/strict-hessian-moment-arithmetic.md). This is distinct from the all-rank SOS field theorem.

For rational quartic \(f\) with a full strict rational Hessian Gram, put \(m=f(p),K=\mathbb Q(p),e=m_2(p)\), \(M=\binom{n+2}{2}\). Strict Taylor integration yields a \(K\)-valued PSD Gram of \(f-m\) of rank \(M-1\), kernel \(\mathbb Re\). Its entries lie directly in \(K\); the auxiliary real margin used to prove rank is not inserted into the construction. Every PSD Gram annihilates \(e\), so this rank is maximal.

The order-two moment optimum is unique and equals evaluation at \(p\): the zero trace product with the maximal-rank Gram forces the moment range into \(\mathbb Re\); its constant normalization gives \(ee^{\mathsf T}\). Every degree-at-most-four monomial occurs in the moment matrix. The real primal and dual programs attain, have Slater points, and have a strictly complementary optimum, despite irrational optimal certificates.

An \(E\)-valued maximal-rank Gram exists exactly when \(K\subseteq E\): normalize its one-dimensional kernel over \(E\) to recover every coordinate of \(p\); Taylor proves sufficiency. If \(r=\dim_{\mathbb Q}\operatorname{span}\{p^\alpha:|\alpha|\le2\}\), rational optimal Grams have rank at most \(M-r\), since their rows annihilate each rational coefficient vector in a rational basis expansion of \(e\).

For rational optimal-level SDP data assume \(m\in\mathbb Q\). Its smallest real PSD face is \(\{Q\succeq0:Qe=0\}\). Every nonzero PSD matrix annihilating all feasible Grams is \(c\,ee^{\mathsf T}\), \(c>0\), since a rank-\(M-1\) feasible Gram is in that face's relative interior. Ratios of its entries recover \(p\), so the least exposing field is \(K\). No nonzero rational exposing step exists for irrational \(p\), although one real step suffices. This preserves **all real feasible matrices**; it does not prohibit a method intentionally restricting to rational candidates and conjugate relations. Ordinary strong SOS-convexity alone does not imply moment uniqueness.

## 14. Number-field precision refinement

Source: [number-field precision](../../../research-20260927/algebraic-coefficient-span-precision.md). Its geometric reduction, ordered-limit elimination, and Hölder assembly are imported interfaces, not SOS descent statements.

At a fixed real embedding of a number field \(K\), degree \(D\), convex quadratic input with attained finite optimum, native constraint-Hessian span \(h\), explicit scalar/count bound \(S\ge2\), and coefficient Weil heights at most \(B\ge1\) satisfies
\[
[K(\theta):K]\le(2n+1)^{\min(h,n)},\quad
h_{\rm W}(\theta)\le(B+1)S^{c(h+1)},\quad
\theta\ne0\Rightarrow|\log|\theta||\le D(B+1)S^{c(h+1)}.
\]
The dense rational minimal-polynomial degree is at most \(D(2n+1)^{\min(h,n)}\), with coefficient-bit bound \(D(B+1)S^{O(h+1)}\). Minimum-norm optimizer coordinates and their joint extension have the same relative degree bound. Convexity is required only at the selected embedding; the objective Hessian is excluded from \(h\). This is an existence and encoding bound, not an implemented number-field algorithm.

The arithmetic step passes reconstruction. Joint local norms in a quotient of size \(L_0=(a+1)^s\) bound cleared multiplication matrices by \(C_v^{T+1}\), \(T=a(s+1)\). Determinant expansion gives \(L_0!3^{L_0}C_v^{L_0(T+1)}\) at archimedean places, \(C_v^{L_0(T+1)}\) elsewhere. Ordered coefficient extraction selects subvectors and cannot increase norms. The resulting annihilator has degree at most \(L_0\), height \(W\le L_0(T+1)E+\log(L_0!)+L_0\log3\). The nonsingularity/nonzero-denominator ordered-limit contract must be supplied by the elimination proof; local height bounds do not repair a failure of that contract.

The product formula and Cauchy estimate give \(h_{\rm W}(\theta)\le W+\log2\). Ratios of annihilator coefficients have height at most \(W\); at the selected embedding \(|\log|\gamma||\le D h(\gamma)\), \(\gamma\in K^*\). Cauchy applied to the annihilator and its reversal after removing zero-root powers gives \(|\log|\theta||\le DW+\log2\), without an extra extension-degree factor. Fixed-count affine-chart linear algebra preserves a polynomial \(S\), linear \(B+1\) height budget. It must include regularizer Hessian \(2V^{\mathsf T}V\), vector \(2V^{\mathsf T}x_0\), and constants \(2,1/2\), as corrected historically. The final Hölder constant bound depends on the separate geometric/common-field audit.

## 15. Manuscript decisions and verification limits

The universal field, individual-degree, denominator, block-existence, separated-height, auxiliary, relation-space, graph, and strict-Hessian moment statements can be used with their precise models and supplied-certificate assumptions. Use canonical covariance to shorten graph and root-realization Gram recovery where its hypotheses match. Keep minimum-zero promises explicit. Arbitrary-field PSD necessity must not assume field-valued square factorization.

The root's vetted literature report must confirm the ternary-quartic classification, general-ring pure-state/order-unit contracts, and rational approximate-minimization bit-model theorem. No unresolved internal analytic gap remains after treating these as precise imported results. The minimum-SOS-length theorem and interior-Gram tiny-minimum family need reconciliation with their owning audits before promoting dependent claims.

The all-dimension cyclic application of the descent criterion is unproved; keep its diagnostics finite. The unrestricted all-PSD rational certificate-size question remains open. Neither separated-Gram nor interior-Gram lower bounds resolve it. These results concern exact certificate formats and expanded output, not optimization-time lower bounds, NP-hardness, or practical speedups.

Checks performed here: targeted cat, sed, rg, and wc source reads; inspection of the retained explicit multiplier matrix and recorded positivity minors; analytic reconstruction of the field, multiplier, radial, block, covariance, graph, moment, and height steps above. Only document-integrity and scoped whitespace checks are run after writing. No historical experimental command is counted as rerun; no CI result is asserted.

The targeted document commands actually run were an inline Python command reading only this review and checking its final newline, whitespace, control characters, paired math delimiters, and all relative Markdown links, and the command below. The inline check passed all 28 links and all text checks. The diff check returned no diagnostics; the file is untracked, so the inline check supplies its direct whitespace validation.

~~~text
git diff --check -- paper-exact-arithmetic/evidence/reviews/prewrite-sos-fields.md
~~~
