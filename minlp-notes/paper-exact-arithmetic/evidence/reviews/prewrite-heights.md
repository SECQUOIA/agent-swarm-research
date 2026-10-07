# Prewriting audit: rational heights, moments, and Gram representations

Date: 2026-10-05. Internal proof audit. No literature discovery, external
source verification, computational experiment, or mathematical script rerun
was performed. The conclusions below follow from analytic reconstruction of
the assigned notes and their linked proof dependencies.

## Verdict and exact manuscript decisions

The assigned constructions and height bounds are mathematically sound under
their stated representation and certificate hypotheses. No invalidity
propagates from this audit. The topic can proceed. The principal manuscript
repair is to include the common quantitative realization lemma and its
rational Gram construction, instead of referring readers to repository
notes. A specialized cubic construction below is sufficient for the tiny
root family and avoids importing the entire signed odd-root theorem into a
height proof.

The following decisions are required.

1. Define one total expanded binary input length, denoted by \(L\), counting
   polynomial coefficients, dimensions, and the supplied full Hessian
   matrix. The lower constructions have \(L_k\le Ck^a\) for fixed constants
   \(C,a\). Their bounds are exponential in ambient dimension and
   superpolynomial in \(L_k\). They do **not** establish
   \(2^{\Omega(L_k)}\). For example, the rational-circle optimizer needs
   \(2^k\log_2 5\) denominator bits in dimension \(n=2(k+1)\); the strictly
   feasible witness and interior-Gram families need \(\Omega(k2^k)\) bits
   in dimension \(n=2k\).
2. State the witness result for **every** rational point in the closed
   sublevel set, including its boundary. Strict feasibility proves rational
   points exist. An assertion only about a particular rounded point would
   be weaker than the proved result.
3. State the moment result for the unconstrained real order-two relaxation
   with \(y_0=1\), \(M_2(y)\succeq0\), and all moment indices through
   degree four. The full positive definite Hessian Gram on
   \((v,X\otimes v)\) is essential. Ordinary strong convexity or an
   arbitrary SOS-convex Hessian certificate does not suffice for uniqueness.
4. Restrict the optimal-Gram lower bound to rank
   \(D-1\), where \(D=\binom{n+2}{2}\). Restrict the exposing-matrix claim
   to nonzero PSD matrices orthogonal to **all real feasible Grams at the
   optimal level**. Short lower-rank rational optimal Grams are explicitly
   present. Arbitrary supporting matrices, indefinite affine normals, and
   reductions that deliberately discard real feasible Grams are outside the
   claim.
5. Keep the local Hessian condition-number statement local to the exact
   minimizer. It does not bound curvature on a fixed neighborhood, higher
   derivatives, coefficient conditioning, Gram conditioning, or the
   sensitivity of rational reconstruction.
6. Restrict the interior-Gram height lower bound to rational
   **positive definite** Grams in the ordinary full quadratic monomial
   basis. The same inputs have short singular rational PSD Grams and short
   rational unweighted SOS expressions. An all-PSD lower bound for this
   family is false. An all-PSD lower bound in another family remains a
   separate open question.
7. Describe \(\operatorname{poly}(L)2^{O(n)}\) as an expanded certificate
   **size** upper bound under a supplied full positive definite Hessian
   Gram. The proof uses a strict-open rational sampling theorem. It does
   not yield polynomial-time expanded output in \(L\) alone, and does not
   establish that size bound for arbitrary SOS-interior polynomials.
8. The October 3 construction yields a polynomial-size **shared rational
   circuit** for a Gram, in deterministic polynomial time, with no sign
   oracle. Its exact identity holds for every valid input, and
   \(Q\succ0\) if and only if the attained minimum is positive. It does not
   give ordinary polynomial-time exact validation of circuit identities,
   circuit positive definiteness, or the positive-minimum premise. It also
   does not provide a polynomial-size unweighted rational SOS circuit.
9. Do not use these output lower bounds to assert NP nonmembership or a
   lower bound for finding some exact SOS certificate. Compact algebraic
   or arithmetic-circuit descriptions and the supplied short singular
   certificates are compatible with the results.

There is no ambiguity in the mathematical scope of the assigned audit. The
status of priority and the exact versions of external sampling and warm
start theorems belong to the root's vetted literature report. This audit
read the existing source-review notes and did not independently discover or
verify external sources.

## Sources inspected

The assigned sources were
`research-20260927/strict-convex-quartic-rational-witness-lower-bound.md`,
`rational-convex-quartic-minimizer-height.md`,
`rational-circle-optimal-gram-height.md`,
`rational-circle-minimizer-local-conditioning.md`,
`interior-gram-bit-lower-bound.md`,
`interior-gram-single-exponential-upper.md`,
`research-20261003-arithmetic/reviews/exact-core/general-degree/circuit-interior-gram.md`,
and `research-20261003-arithmetic/document/sections/07-certificates.tex`.

The substantive analytic dependencies read were
`strict-hessian-moment-arithmetic.md`,
`general-strongly-convex-quartic-singleton.md`,
`sos-convex-quartic-realization.md`,
`signed-odd-root-circuit-quartic.md`, and
`strong-convex-polynomial-posslp-upper.md`. Relevant existing independent
reviews of the assigned constructions, including the strict-open sampling
application and circuit-Gram argument, were also inspected. Recorded finite
checks were treated as supporting diagnostics, not as asymptotic proofs.

## Common quantitative lemma that the manuscript must contain

Let \(p\in\mathbb R^n\). Suppose rational quadratic polynomials
\(G,r_1,\ldots,r_n\) vanish at \(p\), with exact translated forms
\[
 G(p+u)=\ell^{\mathsf T}u+u^{\mathsf T}Hu,\qquad
 r_j(p+u)=b_j^{\mathsf T}u+u^{\mathsf T}T_ju.
\]
Assume positive rational bounds satisfy
\[
 mI\preceq H\preceq MI,\quad \|\ell\|\le\varepsilon,
 \quad \|T_j\|\le1,\quad\|b_j\|\le V,
 \quad\sum_j b_jb_j^{\mathsf T}\succeq\nu^2I,
 \quad\|p\|\le K,
\]
and choose a positive rational square \(\varepsilon=t^2\) with
\[
 \varepsilon\le\min\left\{1,\frac{m^2}{2n},
    \frac{\nu^2m^2}{36n(M+nV)^2}\right\}.
 \tag{A1}
\]
Then
\[
 F=\left(\frac{G}{t\nu}\right)^2+
             \sum_{j=1}^n\left(\frac{r_j}{\nu}\right)^2
 \tag{A2}
\]
is a rational quartic, vanishes at \(p\), has
\(\nabla^2F\succeq(3/2)I\), and has a full positive definite real Hessian
Gram. If the rational data and all these bounds have polynomial bit length,
and \(p\) can be approximated to \(P\) bits in time polynomial in the
original input length and \(P\), an exact rational positive definite full
Hessian Gram of polynomial bit length can be constructed in polynomial time
without expanding \(p\).

Here \(M\) is only a curvature upper bound; it must not be confused with
the total input length \(L\). No condition \(V\ge1\) is required.

### Global convexity

Put \(\Phi=G^2+\varepsilon\sum_jr_j^2\), and split into centered
homogeneous parts of degrees two, three, and four. With \(r=\|u\|\) and
\(B=M+nV\), their Hessians satisfy
\[
 \nabla^2\Phi_2\succeq2\varepsilon\nu^2I,\quad
 \|\nabla^2\Phi_3\|\le12\varepsilon Br,\quad
 \nabla^2\Phi_4\succeq4(m^2-n\varepsilon)r^2I.
\]
The middle estimate follows from
\[
 \nabla^2[2(b^{\mathsf T}u)(u^{\mathsf T}Tu)]
 =4[b(Tu)^{\mathsf T}+(Tu)b^{\mathsf T}+(b^{\mathsf T}u)T].
\]
For the last estimate use
\[
 \nabla^2(u^{\mathsf T}Tu)^2
 =8(Tu)(Tu)^{\mathsf T}+4(u^{\mathsf T}Tu)T.
\]
The second term can be negative when \(T\) is indefinite; keeping its
lower bound \(-4\|T\|^2r^2I\) is essential. Under (A1), completing the
square gives
\[
 2\varepsilon\nu^2-12\varepsilon Br+2m^2r^2
 \ge2\varepsilon\nu^2-18\varepsilon^2B^2/m^2
 \ge\tfrac32\varepsilon\nu^2.
\]
Division by \(\varepsilon\nu^2\) proves the stated bound for \(F\).

### Full Hessian Gram and rational construction

Order \(u\otimes v\) by \((a,b)\), so its coordinate is \(u_av_b\).
For a vector \(b\) and symmetric matrix \(T\), define
\[
 D(b,T)_{i,(a,j)}=2b_aT_{ij}+4b_iT_{aj},
 \qquad\|D(b,T)\|\le6\sqrt n\,\|b\|\|T\|.
\]
For \(\Phi\), the exact centered Hessian Gram is
\[
 \mathcal M=\begin{pmatrix}C&D\\D^{\mathsf T}&Q\end{pmatrix},
\]
where
\[
\begin{aligned}
 C&=2\ell\ell^{\mathsf T}+2\varepsilon\sum_jb_jb_j^{\mathsf T},\\
 D&=D(\ell,H)+\varepsilon\sum_jD(b_j,T_j),\\
 Q&=8\operatorname{vec}H\operatorname{vec}H^{\mathsf T}+4H\otimes H\\
  &\quad+\varepsilon\sum_j
    [8\operatorname{vec}T_j\operatorname{vec}T_j^{\mathsf T}
                          +4T_j\otimes T_j].
\end{aligned}
\]
Substitution proves the exact Hessian identity. Since
\(T_j\otimes T_j\succeq-I\),
\[
 C\succeq2\varepsilon\nu^2I,\quad Q\succeq2m^2I,\quad
 \|D\|\le6\sqrt n\,\varepsilon B.
\]
Its Schur complement is at least
\[
 2\varepsilon\nu^2-18n\varepsilon^2B^2/m^2
 \ge\tfrac32\varepsilon\nu^2>0.
\]
Thus \(\mathcal M\succ0\). Set
\[
 q_0=2m^2,\quad s_0=\tfrac32\varepsilon\nu^2,
 \quad B_D=6n\varepsilon B,
 \quad
 \rho=\frac{\min\{q_0,s_0\}}
            {(2+2(B_D/q_0)^2)(2+K)^2}.
 \tag{A3}
\]
The block-square identity bounds the least eigenvalue of \(\mathcal M\)
below by \(\min\{q_0,s_0\}/(2+2(B_D/q_0)^2)\). Translating to
\((v,X\otimes v)\) uses
\[
 S_p=\begin{pmatrix}I&0\\-p\otimes I&I\end{pmatrix},
 \qquad\|S_p^{-1}\|\le2+K,
\]
so \(\mathcal M_X=S_p^{\mathsf T}\mathcal M S_p\succeq\rho I\).

For fixed rational \(G,r_j\), \(H,T_j\) are constant, \(\ell,b_j\) are
affine in the formal center, and entries of \(\mathcal M_X\) have degree
at most two in that center. Let \(B_0\ge1\) bound each entry's absolute
coefficient sum, and \(d=n+n^2\). On a box of radius \(K+1\), each
partial derivative is bounded by \(2(K+1)B_0\). Coordinate error
\(\delta\) therefore gives Frobenius error at most
\(2dn(K+1)B_0\delta\). Choosing this below \(\rho/4\) requires only
polynomially many center bits whenever (A3) and the other data have
polynomial bit length. This accounts for bit complexity, rather than
merely counting rational operations.

To restore the exact rational coefficient equations, let \(E_\gamma\)
have entry one exactly where a product of Hessian basis monomials equals
\(\gamma\). These symmetric matrices have disjoint supports and are
Frobenius-orthogonal; off-diagonal entries are counted twice. If
\(c_\gamma\) are the exact rational Hessian coefficients, use
\[
 \mathcal P(T)=T+\sum_\gamma E_\gamma
     \frac{c_\gamma-\langle E_\gamma,T\rangle_F}
          {\|E_\gamma\|_F^2}.
 \tag{A4}
\]
This is orthogonal affine projection, fixes \(\mathcal M_X\), and is
nonexpansive. Hence \(\|T-\mathcal M_X\|_F<\rho/4\) implies
\(\mathcal P(T)\succeq3\rho I/4\) with the exact rational identity.
Scaling by \(1/(\varepsilon\nu^2)\) gives the Hessian Gram for (A2).
The construction uses polynomially many rational entries and polynomial
bit length. An exact rational LDL factorization validates the final
expanded certificate.

## Rational-circle optimizer and local conditioning

Set \(z_0=(3+4\mathrm i)/5\) and \(z_j=z_{j-1}^2\). In
\(n=2(k+1)\) variables define
\[
\begin{aligned}
 r_0&=x_0-3/5,&s_0&=y_0-4/5,\\
 r_j&=x_j-x_{j-1}^2+y_{j-1}^2,&
 s_j&=y_j-2x_{j-1}y_{j-1},\\
 q_j&=x_j^2+y_j^2-1.
\end{aligned}
\]
Their unique common zero is
\(p=(a_j,b_j)_{j=0}^k\), where \(z_j=a_j+\mathrm ib_j\). Every
coordinate has magnitude at most one. Write
\((3+4\mathrm i)^m=A_m+\mathrm iB_m\). Idempotence of
\(3+4\mathrm i\) modulo five gives
\(A_m\equiv3\), \(B_m\equiv4\pmod5\) for every positive integer
\(m\). Both terminal fractions therefore have reduced denominator
exactly \(5^{2^k}\).

For
\[
 E_0=r_0^2+s_0^2,\qquad
 E_j=q_j-2a_jr_j-2b_js_j-2q_{j-1},
\]
the full gradient at \(p\) vanishes. The centered predecessor block of
\(E_j\) is
\[
 2\begin{pmatrix}a_j-1&b_j\\b_j&-a_j-1\end{pmatrix},
\]
with eigenvalues zero and minus four, and its current block is \(I\).
Weights \(8^{-j}\) give a centered quadratic matrix between
\(8^{-k}I\) and \(I\). Replacing only the coefficients multiplying
\(r_j,s_j\) by rational approximations preserves value zero at \(p\)
exactly. Coordinate errors at most \(\eta\) give leading-matrix error
at most \(4\eta\) and gradient error at most \(4kV\eta\), where
\(V=4n\). Use
\[
 \eta\le\min\{1,8^{-k}/8,\varepsilon/[4(k+1)V]\}.
\]
Then the common lemma applies with \(m=8^{-k}/2\), \(M=2\), and
\(\nu=V^{-(n-1)}\): the residual Jacobian is block lower triangular
with identity diagonal blocks, determinant one, and Frobenius norm at
most \(V\).

No large fraction is expanded to make the approximations. Iterated
complex squaring with dyadic coordinate rounding of error at most \(h\)
obeys \(e_j\le3e_{j-1}+2h\) when \(e_{j-1}\le1\); hence
\(e_j\le h(3^j-1)\). Taking \(h\le\eta/(2\cdot3^k)\) proves
the required error bound inductively. The number of bits is polynomial
in \(k+\log(1/\eta)\). The common lemma then gives both the short
rational SOS and the small rational full Hessian certificate. Optional
integer-square scaling normalizes that Hessian Gram to at least identity
without changing \(p\) or its denominators.

For the local-conditioning version put
\(R_j=2^{-j}\), \(p_j=R_j(\Re z_j,\Im z_j)\), and
\(c_j=2^{j-2}\). Replace the gate map by
\(\Phi_j(x,y)=c_j(x^2-y^2,2xy)\), and use circle equations
\(q_j=x_j^2+y_j^2-R_j^2\). The derivative at the exact predecessor
is orthogonal because \(2c_jR_{j-1}=1\). Thus the residual Jacobian
is \(J=I-T\), with \(\|T\|\le1\) and \(T^{k+1}=0\), giving
\[
 \|J\|\le2,\qquad\|J^{-1}\|\le k+1.
\]
Use
\[
 E_j=q_j-2a_jr_j-2b_js_j-\tfrac12q_{j-1}
\]
and weights \(k+1-j\). Its predecessor block has eigenvalues zero
and minus one. Each nonterminal weighted block has eigenvalues
\(k+1-j\) and one; the last is \(I\). The resulting exact exposing
quadratic has leading matrix between \(I\) and \((k+1)I\).

Let \(C=\max\{1,2^{k-2}\}\), and divide every residual by \(C\).
The common lemma then permits
\(V=2/C\), \(\nu=1/[C(k+1)]\), \(m=1/2\), and \(M=k+2\).
Approximation of the coefficients with
\[
 \eta\le\min\{1,[8C(k+1)]^{-1},
                        \varepsilon/[8(k+1)^2]\}
\]
preserves the exact zero and supplies the required margins. For its
output quartic,
\[
 \nabla^2F(p)=\frac{2\ell\ell^{\mathsf T}}{\varepsilon\nu^2}
                              +2(k+1)^2J^{\mathsf T}J.
\]
The first term has norm at most \(2\varepsilon/\nu^2<1\), by (A1);
the second lies between \(2I\) and \(8(k+1)^2I\). Therefore
\[
 2I\preceq\nabla^2F(p)\preceq[8(k+1)^2+1]I,
 \qquad\kappa_2(\nabla^2F(p))\le4(k+1)^2+\tfrac12.
\]
Meanwhile \(\|p\|^2=\sum_{j=0}^k4^{-j}<4/3\), and scaling by
powers of two cannot cancel the terminal denominator's power of five.
These prove the local claim without a global smoothness claim. Scaling
the full Hessian Gram to identity changes the displayed absolute Hessian
bounds but preserves their eigenvalue ratio.

## A self-contained cubic realization for the tiny-root family

This is an optional replacement for the broader signed-root dependency in
the two height proofs. It is an analytic derivation, not an experiment.
Put
\[
 M_*=1000^{k+3},\quad \delta_0=M_*^{-1},\quad
 \delta_i=(1+3\delta_{i-1}^2)^{1/3}-1,\quad
 \xi_i=1+\delta_i.
\]
Since \((1+t)^3\ge1+3t\),
\(0<\delta_i\le\delta_{i-1}^2\), so
\(\delta_k\le M_*^{-2^k}\). Use widths
\(w_i=1000^i/M_*\) and boxes \([1-w_i,1+w_i]\).
Signed interval evaluation of
\(3\xi_{i-1}^2-6\xi_{i-1}+4\) differs from one by at most
\(12w_{i-1}+3w_{i-1}^2\le13w_{i-1}\). The factor-1000 increase
in widths makes this interval lie inside the cubes of the next box.
The first constant radicand \(1+3/M_*^2\) also satisfies that promise.

Take the fixed rational
\(\kappa=1/(1-w_k)=10^9/(10^9-1)<2\), and normalize
\(\alpha_i=\kappa\xi_i\). All normalized boxes lie in \([1,2]\).
Use \(n=2k\) variables \((x_i,y_i)\) and rational affine radicands
\[
 b_1=\kappa^3(1+3/M_*^2),\qquad
 b_i=3\kappa y_{i-1}-6\kappa^2x_{i-1}+4\kappa^3\quad(i>1).
\]
The residuals
\[
 r_i=x_i^2-y_i,\qquad s_i=x_iy_i-b_i
\]
have unique common real zero
\(p=(\alpha_i,\alpha_i^2)_{i=1}^k\). Their quadratic parts have norm
at most one. The block lower triangular Jacobian has local determinant
\(3\alpha_i^2\ge3\), so its determinant has magnitude at least one.
Individual gradient norms and its Frobenius norm are bounded by
\(V=64n\), hence \(\nu=V^{-(n-1)}\) is a valid lower singular-value
bound. Coordinates of \(p\) lie in \((0,4)\), so \(K=4n\) suffices.

The exposing quadratic
\[
 E_i=y_i^2-b_ix_i-\alpha_i s_i+\alpha_i^2r_i
 \tag{C1}
\]
has zero value and full gradient at \(p\). To check its complete
centered form, let
\[
 P_\alpha=(x-\alpha,y-\alpha x)
       \begin{pmatrix}\alpha^2&\alpha/2\\\alpha/2&1\end{pmatrix}
       (x-\alpha,y-\alpha x)^{\mathsf T}.
\]
Expansion gives
\(E_i=P_{\alpha_i}+(\alpha_i-x_i)(b_i-\alpha_i^3)\).
Its local centered block is
\[
 H_i=\begin{pmatrix}\alpha_i^2&-\alpha_i/2\\-\alpha_i/2&1\end{pmatrix},
 \qquad (3/20)I\preceq H_i\preceq5I,
\]
because \(\det H_i=3\alpha_i^2/4\ge3/4\) and
\(\operatorname{tr}H_i\le5\). Its only cross term is
\(-u_{i,x}[b_i(p+u)-b_i(p)]\).

Let \(h_0=3/20\), \(A_0=64\),
\(\sigma=(h_0/(2nA_0))^2\), and weights
\(\omega_i=\sigma^{i-1}\). After scaling block \(i\) by
\(\sqrt{\omega_i}\), each cross entry has magnitude at most
\(A_0\sqrt\sigma/2\); every row has at most \(n\) such entries.
The cross operator norm is therefore at most \(h_0/4\). The weighted
sum of (C1) has leading matrix at least
\(\gamma I\), with \(\gamma=h_0\sigma^{k-1}/2\), and at most
\(WI\), where \(W=5+nA_0\) is a safe bound.

Replace \(\alpha_i\) in (C1) by rational \(\widehat\alpha_i\), and
\(\alpha_i^2\) by \(\widehat\alpha_i^2\). Exact residual vanishing
preserves value zero at \(p\). If the root error is at most
\(\theta\le1\), then \(|\widehat\alpha_i^2-\alpha_i^2|\le5\theta\).
Since \(\|b_i\|_1<64\), one gate's coefficient error is at most
\(76\theta\), and the weighted sum's at most \(76k\theta\).
The leading-matrix error is no larger, and its gradient error at \(p\)
is at most \(608k\theta\). Thus
\[
 \theta\le\min\{1,\gamma/(2048k),\varepsilon/(2048k)\}
\]
gives the common lemma's bounds with \(m=\gamma/2\), \(M=W+1\).
All inverse-margin logarithms are \(O(k\log k)\).

Certified root approximation also has polynomial bit cost. On normalized
boxes in \([1,2]\), predecessor squares amplify interval width by at
most four, and the affine radicand amplifies root width by at most
\(24+6\cdot4=48\). Cubic root has derivative at most one there.
Rational outward endpoint rounding therefore gives widths
\(D_i\le48D_{i-1}+2\eta\), with the first gate treated directly.
Taking \(\eta\le\theta/(4k49^k)\), and bisecting each increasing
cubic with exact rational comparisons, supplies all roots to error
\(\theta\) in time polynomial in \(k+\log(1/\theta)\). Intersecting
with the supplied boxes maintains the derivative domain. The common lemma
now constructs a polynomial-size rational quartic \(F\) with unique zero
\(p\), \(n+1\) short rational quadratic square factors, and a small
rational full positive definite Hessian Gram. This is all that the next
two height proofs need.

## Every rational feasible point is long

Let \(A\succ0\) be the polynomial-size rational Hessian Gram of the
cubic realization, \(h=n+n^2\), and
\[
 \mu=\det A/(\operatorname{tr}A)^{h-1},\quad
 \lambda=\lceil3/\mu\rceil,\quad
 u(X)=X_{k,1}-\kappa,\quad G=\lambda F-u^2.
\]
The determinant-to-trace inequality gives \(A\succeq\mu I\).
The Hessian Gram of \(G\) is \(\lambda A-2ee^{\mathsf T}\succeq I\),
where \(e\) selects the corresponding constant Hessian direction.
Determinants, the trace power, and the ceiling have polynomial bit cost
on this polynomial-size rational matrix.

At \(p\), put \(u_*=\kappa\delta_k>0\). Then
\(G(p)=-u_*^2<0\) and \(\|\nabla G(p)\|=2u_*\). Strong convexity
makes the zero sublevel set compact; continuity makes it have nonempty
interior. For **every** feasible \(X\), with \(r=\|X-p\|\),
\[
 0\ge G(X)\ge-u_*^2-2u_*r+r^2/2,
 \qquad r\le(2+\sqrt6)u_*<5\kappa M_*^{-2^k}.
 \tag{W1}
\]
All feasible coordinates are bounded by fixed constants. No claim that
\(p\) minimizes \(G\) is used.

For the first coordinate \(\alpha=\kappa\xi_1\),
\[
 \alpha^3=A_*/B_*,\quad
 A_*=M_*(M_*^2+3),\quad B_*=(M_*-1000^k)^3<M_*^3.
\]
The integer \(M_*^2\) is a cube, and \(M_*^2+3\) lies before the
next cube, so \(\alpha\) is irrational. If a feasible first coordinate
is the reduced rational \(a/b\), then
\(B_*a^3-A_*b^3\) is a nonzero integer. Both arguments of the
difference of cubes have absolute value below three. Therefore
\[
 b^{-3}\le|B_*(a/b)^3-A_*|
 \le27B_*|a/b-\alpha|
 <270M_*^{3-2^k}.
\]
It follows that
\[
 \log_2b>
 \frac{(2^k-3)(k+3)\log_2 1000-\log_2 270}{3}.
\]
This holds for every rational feasible point and all \(k\ge1\);
the asymptotic \(\Omega(k2^k)\) statement begins when \(k\) is large.
Open-set density guarantees rational points exist. A quantitative Slater
radius was never promised and must not be inferred from strict feasibility.

## Moment uniqueness, maximal rank, and the exposing matrix

Let a rational quartic \(f\) have a full positive definite rational
Hessian Gram on \((v,X\otimes v)\), unique minimizer \(p\), and minimum
\(m=f(p)\). Put \(D=\binom{n+2}{2}\), let \(z_2\) be the ordinary
full quadratic monomial vector with constant first, and \(e=z_2(p)\).
Taylor integration at \(p\) constructs a PSD Gram \(Q_*\) of \(f-m\)
with rank \(D-1\) and kernel \(\mathbb Re\). Indeed, translation
preserves strict positivity of the Hessian Gram; for any sufficiently
small real \(\tau>0\), its Taylor integral dominates
\(\tau\|X-p\|^2/2+\tau\|X-p\|^4/12\). Those terms have positive
Gram coefficients on all centered nonconstant monomials. Integration
itself introduces only rational constants, so \(Q_*\) has entries in
\(\mathbb Q(p)\), and is rational when \(p\) is rational. Every PSD
Gram of \(f-m\) annihilates \(e\), because it evaluates to zero at
\(p\); hence this rank is maximal.

Use precisely the moment relaxation
\[
 \min L_y(f),\qquad y_0=1,\quad M_2(y)\succeq0,
 \quad M_2(y)_{\alpha,\beta}=y_{\alpha+\beta}
 \quad(|\alpha|,|\beta|\le2).
\]
The point sequence \(y_\alpha=p^\alpha\) and \(Q_*\) certify value
\(m\). Every optimal \(y\) satisfies
\(\operatorname{tr}(Q_*M_2(y))=0\). For PSD matrices, zero trace
pairing implies orthogonality of their ranges; equivalently the
Frobenius norm of the product of their square roots is zero. Thus
\(\operatorname{range}M_2(y)\subseteq\mathbb Re\). The constant
normalization forces \(M_2(y)=ee^{\mathsf T}\). Every monomial of
degree at most four is a product of two monomials of degree at most two,
so this determines the entire moment sequence uniquely.

Gaussian moments give primal Slater feasibility. Adding a positive
constant to the centered Gram fills the constant coordinate and gives
dual Slater feasibility at a suboptimal level. The pair
\((ee^{\mathsf T},Q_*)\) is strictly complementary over the reals. The
optimal-level Gram problem itself has smallest face
\(\{Q\succeq0:Qe=0\}\), with \(Q_*\) in its relative interior.
Every nonzero PSD matrix \(Z\) orthogonal to all those feasible Grams
must, by pairing with \(Q_*\), have range in \(\mathbb Re\), so
\(Z=c ee^{\mathsf T}\), \(c>0\). Evaluation at \(p\) is a linear
combination of the Gram coefficient equations and exposes this face.
One real facial-reduction step suffices; the real singularity degree is
exactly one. These statements are about real feasibility, not a search
that keeps only rational Gram candidates.

The full Hessian hypothesis cannot be weakened without another argument.
For \(f(x,y)=x^2+y^2+y^4\), all moments except \(y_{00}=1\) and an
arbitrary nonnegative \(y_{40}\) may vanish. These are PSD feasible
optimal moment sequences of value zero, so the moment optimum is not
unique despite strong convexity and SOS-convexity.

For the rational-circle family, put \(H_k=2^k\log_2 5\). If a
maximal-rank rational optimal Gram has all reduced numerators and
denominators bounded by \(2^B\), partition it as
\[
 Q=\begin{pmatrix}q_{00}&c^{\mathsf T}\\c&A\end{pmatrix},
 \qquad e=(1,w)^{\mathsf T}.
\]
The principal block \(A\) is positive definite: a null vector
\((0,u)\) would belong to \(\mathbb Re\) and therefore be zero.
Then \(Aw=-c\). Clear the \(D\) denominators in each row using
their product. Integer entries are bounded by \(2^{(D+1)B}\), and
\[
 0<|\det A'|\le(D-1)!\,2^{(D^2-1)B}.
\]
Cramer's rule says each reduced denominator of \(w\) divides
\(|\det A'|\), including a terminal denominator \(5^{2^k}\). Hence
\[
 B\ge\frac{H_k-\log_2((D-1)!)}{D^2-1}
   =\Omega(2^k/n^4).
\]
The total matrix-length bound can omit this polynomial divisor: sum
row denominator lengths and the largest numerator length in each row,
then apply the determinant expansion. Symmetric upper-triangle encoding
changes that total bound only by a constant factor.

For any nonzero rational exposing matrix,
\(p_i=Z_{0i}/Z_{00}\). Two entries of height at most \(B\) give a
quotient with denominator at most \(2^{2B}\); thus \(B\ge H_k/2\),
regardless of positive rational rescaling. The unique normalized moment
matrix has a constant-versus-linear entry equal to \(p_i\), whose
denominator is exactly \(5^{2^k}\). The supplied \(n+1\) short square
factors give an optimal Gram of rank at most \(n+1<D-1\); this explicitly
precludes extending the bound to every optimal Gram. The scaled local
family has the same consequences using denominator divisibility by
\(5^{2^k}\).

## Strictly positive inputs and long interior Grams

For the cubic realization use \(f_k=\lambda F+u^2\), with the same
\(\lambda,u\) as above. Its Hessian Gram is at least \(3I\).
Since \(F\ge0\) has unique zero \(p\) and \(u(p)>0\), \(f_k>0\)
everywhere. Coercivity ensures an attained positive minimum, and
\[
 0<f_k(p)=\kappa^2\delta_k^2<4M_*^{-2^{k+1}}.
 \tag{G1}
\]
The short \(n+1\) square factors of \(F\), together with \(u\), give
a rational PSD Gram of rank at most \(n+2<D\). A positive integer weight
\(\lambda\) is converted to polynomially many rational squares by
binary expansion, so the unweighted short SOS claim is valid too.

For any quartic with full Hessian Gram \(A\succeq\mu I\) and positive
minimum, continuity gives a rational center \(a\) with
\[
 c=f(a)-\|\nabla f(a)\|^2/(2\mu)>0.
 \tag{G2}
\]
The exact Taylor formula in the next section constructs a positive
definite rational Gram, so the lower bound is nonvacuous.

Let \(B\) be the matrix of second moments of \(z_2\) under uniform
measure on \([-1,1]^n\). A quadratic with coefficients
\((a_0,b_i,c_i,d_{ij})\) has squared integral
\[
 (a_0+\tfrac13\sum_i c_i)^2+\tfrac13\sum_i b_i^2
       +\tfrac4{45}\sum_i c_i^2+\tfrac19\sum_{i<j}d_{ij}^2.
\]
Writing \(a'=a_0+\sum_i c_i/3\), use
\(a_0^2\le2(a')^2+(2n/9)\sum_i c_i^2\) to obtain
\(B\succeq I/[15(n+1)]\). Every PSD Gram of \(f_k\) therefore has
\[
 \|Q\|\le\operatorname{tr}Q\le15(n+1)\|f_k\|_1\le T_+,
 \qquad T_+=\max\{1,15(n+1)\|f_k\|_1\}.
 \tag{G3}
\]
This bound holds uniformly over the entire Gram spectrahedron.

For \(Q\succ0\), the constant entry of \(z_2(p)\) is one, so
\(\lambda_{\min}(Q)\le f_k(p)\). From (G1) and (G3),
\[
 0<\det Q<4M_*^{-2^{k+1}}T_+^{D-1}.
\]
If the reduced upper-triangular entry denominators are \(b_{ij}\),
\(\prod_{i\le j}b_{ij}^2\) clears each determinant term: any symmetric
entry can occur at most twice in a permutation product. The cleared
positive determinant is an integer at least one. Consequently
\[
 \sum_{i\le j}\log_2b_{ij}>
 2^k\log_2M_*-1-\frac{D-1}{2}\log_2T_+.
\]
The subtracted term is polynomial in \(k\), while the leading term is
\(\Theta(k2^k)\). For singular PSD Grams, the determinant is zero and
the positive-integer argument fails. This is exactly why the theorem
concerns strict interior certificates.

## Expanded upper bound and compact circuit construction

Let \(A\succ0\) be the supplied full rational Hessian Gram,
\(h=n+n^2\), and
\(\mu=\det A/(\operatorname{tr}A)^{h-1}\). The polynomial
\[
 H(X)=f(X)-\|\nabla f(X)\|^2/(2\mu)
\]
has degree at most six and polynomial coefficient bit length after
positive denominator clearing. If \(\min f>0\), then \(H(p)>0\).
The strict-open rational sampling theorem used by the source note gives
a rational \(a\) in \(\{H>0\}\), with coordinate numerator and
denominator bit length \(\operatorname{poly}(L)6^{O(n)}\). Only an open
strict inequality is used; no equality or rationality of \(p\) is needed.
This specific strict-open height theorem, rather than an algebraic
sampling or coordinate-magnitude theorem, must be cited from the vetted
primary-source report.

For an arbitrary rational center \(a\), let \(d=X-a\),
\(b=\nabla f(a)\), \(c=H(a)\), and
\(\bar A=A-\mu\operatorname{diag}(I_n,0)\). Then
\(\bar A\succeq\mu\operatorname{diag}(0,I_{n^2})\). Define
\[
 U=(d,a\otimes d)=C_Uz_2,\quad
 V=(0,d\otimes d)=C_Vz_2,\quad
 d+b/\mu=C_{\rm aff}z_2.
\]
Taylor integration gives the exact ordinary Gram
\[
\begin{aligned}
 Q={}&\tfrac12(C_U+C_V/3)^{\mathsf T}\bar A(C_U+C_V/3)
            +\tfrac1{36}C_V^{\mathsf T}\bar A C_V\\
    &+\tfrac\mu2C_{\rm aff}^{\mathsf T}C_{\rm aff}
            +c e_0e_0^{\mathsf T}.
 \tag{T1}
\end{aligned}
\]
The scalar integration identity is
\[
 \int_0^1(1-t)(U+tV)^{\mathsf T}\bar A(U+tV)\,dt
 =\tfrac12(U+V/3)^{\mathsf T}\bar A(U+V/3)
                         +\tfrac1{36}V^{\mathsf T}\bar A V.
\]
The remaining linear and quadratic terms complete to
\(\mu\|d+b/\mu\|^2/2+c\). Thus \(f=z_2^{\mathsf T}Qz_2\)
for every center, without approximation of the polynomial identity.
When \(c>0\), the second term controls all \(d_id_j\), the third
controls all \(d_i+b_i/\mu\), and the last controls the constant.
These span the full quadratic polynomial space; hence \(Q\succ0\).

If the center coordinates have bit bound \(B\), (T1) has total length
\(\operatorname{poly}(L,n,B)\). These are fixed-degree expressions in
the center with polynomially many terms; polynomial operation count alone
would not justify this bit bound. Substituting the strict-open sample
bound gives \(\operatorname{poly}(L)2^{O(n)}\). Exact rational LDL
factorization gives rational polynomial factors with positive rational
weights. For \(a/b>0\), expand \(ab\) in binary and divide by \(b^2\):
an even binary power is one rational square, and an odd one is two equal
rational squares. The number and total size of unweighted factors are a
polynomial in the Gram length, hence retain the stated upper-bound form.
No factoring or four-square algorithm is hidden here.

For the circuit theorem, use the existing constructive Newton upper
reduction with objective \(f\) and observable \(H\), stopped before
its final PosSLP query. Its input length includes the polynomial-size
derived \(\mu\) and explicit degree-six observable. It constructs an
exact rational-circuit center \(a\) with
\[
 |H(a)-H(p)|\le g/8,
 \qquad H(p)\ne0\Longrightarrow|H(p)|\ge g.
\]
Thus \(\min f>0\) implies \(c>0\), without testing that sign. Newton
Hessians remain positive definite, so every rational division is defined,
including when the minimum is zero or negative. Appending (T1) with
shared references to \(a\) adds polynomially many gates. It always
represents \(f\) exactly. Conversely, a positive definite Gram on a
basis containing one implies
\(f(X)\ge\lambda_{\min}(Q)\|z_2(X)\|^2
\ge\lambda_{\min}(Q)>0\), so its attained minimum is positive.
Therefore the exact equivalence in report section 07 is correct.

This compact construction depends on the separately audited effective
algebraic separation bound and polynomial-bit warm start of the Newton
upper reduction. The journal proof may refer to an earlier theorem in
the same manuscript, but must not rely on a repository link for these
steps. Constructing a short circuit is not expanding its output. Validating
positive definiteness of the constructed circuit Gram is linked by this
equivalence to exact minimum comparison. The proof does not assert an
ordinary polynomial-time verification procedure or an unweighted SOS
circuit factorization. In particular, the binary-weight expansion above
is polynomial in **expanded weight length**, which can be exponential
for a short circuit weight.

## Verification and remaining work

The review used scoped `cat`, `sed`, and `rg` source reads plus analytic
derivations. A document-only `python -` check of this file verified its final
newline, whitespace, control characters, and matching display and inline
math delimiters; it passed. `git diff --check --
paper-exact-arithmetic/evidence/reviews/prewrite-heights.md` also exited
successfully; the document-only check covers the new file independently of
whether Git tracks it. No project-wide verification, CI inspection,
experiment, symbolic computation, or mathematical script rerun occurred.
Existing recorded diagnostics were read only.

The root must integrate the quantitative lemma or equivalent complete
proof, preserve all output and relaxation contracts above, and use the
vetted literature report to settle citation versions and primary-source
comparisons. No unresolved main mathematical claim was found in this
assigned height scope. The all-PSD frontier must stay explicitly separate;
the supplied families demonstrate why it is not a consequence of these
interior or maximal-rank bounds.
