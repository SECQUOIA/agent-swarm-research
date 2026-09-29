# Rational Hessian certificates for algebraic quartic singletons

Date: 2026-09-28. Status: construction and exact Gram identities
independently reviewed. Publication priority is not established.

The [general strongly convex quartic construction](general-strongly-convex-quartic-singleton.md)
can be chosen to be
SOS-convex, with a positive definite rational Gram matrix for its Hessian.
The certificate and the quartic have polynomial bit length. Thus its
irrational zero is not caused by an inability to certify convexity with
rational data.

Here SOS-convex means that the Hessian is a polynomial sum-of-squares
matrix. Equivalently, the polynomial
$y^{\mathsf T}\nabla^2F(x)y$ is a sum of squares in $(x,y)$.
The certificate below uses a Gram matrix on the monomial vector
$(y,x\otimes y)$; it does not claim a positive definite Gram matrix for
$F$ itself. The latter would contradict the prescribed zero.

## The quantitative data used by the construction

Let $p$ be an irreducible rational polynomial of degree $d>1$ with exactly
one real root $\alpha$, let $n=d-1$, and put

\[
 a=(\alpha,\ldots,\alpha^n).
\]

The [effective construction of rational quadratic singletons](general-algebraic-singleton-realization.md)
supplies rational
quadratics $G,r_1,\ldots,r_n$ vanishing at $a$. The $r_j$ are the
companion consistency relations, and $G$ approximates a positive
definite exposing quadratic. Writing $u=x-a$ gives

\[
 G(a+u)=\ell^{\mathsf T}u+u^{\mathsf T}Hu,\qquad
 r_j(a+u)=b_j^{\mathsf T}u+u^{\mathsf T}T_j u.
 \tag{1}
\]

The effective construction supplies positive rational bounds
$m,L,V,\nu,K$ such that

\[
 H\succeq mI,\quad \|H\|_2\leq L,\quad
 \|T_j\|_2\leq1,\quad \|b_j\|_2\leq V,\quad
 \sum_j b_jb_j^{\mathsf T}\succeq\nu^2I,\quad \|a\|_2\leq K.
 \tag{2}
\]

All these bounds and their reciprocals have polynomial bit length in the
dense input for $p$. The gradient $\ell$ can be made smaller than any
positive rational tolerance with polynomially many additional precision
bits. This uses an exact rational linear space of vanishing quadratics:
approximating the exposing coefficients never loses $G(a)=0$.

Choose a positive rational square $\varepsilon=t^2$ with

\[
 \varepsilon\leq
 \min\left\{1,\frac{m^2}{2n},
       \frac{\nu^2m^2}{36n(L+nV)^2}\right\},
 \qquad \|\ell\|_2\leq\varepsilon,
 \tag{3}
\]

and set

\[
 F_0=G^2+\varepsilon\sum_{j=1}^n r_j^2.
 \tag{4}
\]

Choosing $t$ as a sufficiently small dyadic rational makes (3) effective
with polynomial bit length. The extra factor $n$ in the last denominator
is used for the Gram certificate. A bound that proves ordinary convexity
need not by itself prove the certificate below.

## An exact positive definite Hessian Gram matrix

For a symmetric $T$ and vector $b$, the three homogeneous parts of the
Hessian of $(b^{\mathsf T}u+u^{\mathsf T}Tu)^2$ are

\[
 2bb^{\mathsf T},
 \quad
 4(b^{\mathsf T}u)T+4b(Tu)^{\mathsf T}+4(Tu)b^{\mathsf T},
 \quad
 8(Tu)(Tu)^{\mathsf T}+4(u^{\mathsf T}Tu)T.
 \tag{5}
\]

Order the coordinates of $u\otimes y$ by pairs $(k,j)$, so its
$(k,j)$ entry is $u_k y_j$. Define a matrix $D(b,T)$ with $n$ rows
and $n^2$ columns by

\[
 D(b,T)_{i,(k,j)}=2b_kT_{ij}+4b_iT_{kj}.
 \tag{6}
\]

Then twice the cross term $y^{\mathsf T}D(b,T)(u\otimes y)$
is exactly the biform of the middle expression in (5). Moreover,

\[
 \|D(b,T)\|_2\leq\|D(b,T)\|_F
 \leq6\sqrt n\,\|b\|_2\|T\|_2.
 \tag{7}
\]

Indeed the two tensors in (6) have Frobenius norms
$2\|b\|_2\|T\|_F$ and $4\|b\|_2\|T\|_F$.

Using the same pair order for $\operatorname{vec}T$, put

\[
 \begin{aligned}
 C&=2\ell\ell^{\mathsf T}+2\varepsilon\sum_jb_jb_j^{\mathsf T},\\
 D&=D(\ell,H)+\varepsilon\sum_jD(b_j,T_j),\\
 Q&=8\operatorname{vec}H(\operatorname{vec}H)^{\mathsf T}+4H\otimes H\\
  &\quad+\varepsilon\sum_j\left[
      8\operatorname{vec}T_j(\operatorname{vec}T_j)^{\mathsf T}
                           +4T_j\otimes T_j\right],\\
 M&=\begin{pmatrix}C&D\\D^{\mathsf T}&Q\end{pmatrix}.
 \end{aligned}
 \tag{8}
\]

Direct substitution into (5) proves the polynomial identity

\[
 y^{\mathsf T}\nabla^2F_0(a+u)y
  =\begin{pmatrix}y\\u\otimes y\end{pmatrix}^{\mathsf T}
      M\begin{pmatrix}y\\u\otimes y\end{pmatrix}.
 \tag{9}
\]

The matrices $T_j$ can be indefinite. Their tensor products satisfy
$T_j\otimes T_j\succeq-\|T_j\|_2^2I$, which is the negative term
that must be retained. Equations (2), (3), and (7) give

\[
 C\succeq2\varepsilon\nu^2I,\quad
 Q\succeq(4m^2-4\varepsilon n)I\succeq2m^2I,
 \quad
 \|D\|_2\leq6\sqrt n\,\varepsilon(L+nV).
 \tag{10}
\]

Consequently,

\[
 \begin{aligned}
 C-DQ^{-1}D^{\mathsf T}
 &\succeq\left[2\varepsilon\nu^2-
     \frac{18n\varepsilon^2(L+nV)^2}{m^2}\right]I\\
 &\succeq\tfrac32\varepsilon\nu^2I\succ0.
 \end{aligned}
 \tag{11}
\]

The Schur complement proves $M\succ0$. This is a Gram-matrix proof of
SOS-convexity, stronger than checking that the Hessian biform is
nonnegative only on vectors of the special form $(y,u\otimes y)$.

## Making the certificate rational

The entries of $M$ contain the algebraic point $a$. The Hessian of the
original polynomial $F_0$ has rational coefficients. We now use this
rational affine space to obtain an exact rational certificate, rather
than asserting that an algebraic Gram factor is already rational.

Let

\[
 S_a=\begin{pmatrix}I&0\\-a\otimes I&I\end{pmatrix},
 \qquad M_x=S_a^{\mathsf T}MS_a.
 \tag{12}
\]

Then $M_x\succ0$ and (9) becomes

\[
 y^{\mathsf T}\nabla^2F_0(x)y
 =(y,x\otimes y)^{\mathsf T}M_x(y,x\otimes y).
 \tag{13}
\]

For an explicit lower bound, set

\[
 q=2m^2,\quad s=\tfrac32\varepsilon\nu^2,
 \quad B_D=6n\varepsilon(L+nV),
 \quad
 \mu=\frac{\min\{s,q\}}
      {(2+2(B_D/q)^2)(2+K)^2}>0.
 \tag{14}
\]

Completing the block square in (8), using (11) and
$\|Q^{-1}D^{\mathsf T}\|_2\leq B_D/q$, gives
$\lambda_{\min}(M)\geq\min\{s,q\}/(2+2(B_D/q)^2)$.
Also $\|S_a^{-1}\|_2\leq2+K$. Thus $M_x\succeq\mu I$.
The rational number $\mu$ has polynomial bit length.

Write $z=(y,x\otimes y)$ and let $N=n+n^2$. For each distinct
monomial $\gamma$ appearing as a product $z_i z_j$, let $E_\gamma$
be the symmetric zero-one matrix with

\[
 (E_\gamma)_{ij}=1\quad\Longleftrightarrow\quad z_i z_j=\gamma.
\]

Each ordered matrix entry belongs to exactly one such matrix.
Therefore the $E_\gamma$ have pairwise disjoint supports, are
Frobenius-orthogonal, and
$1\leq\|E_\gamma\|_F^2\leq N^2$. Off-diagonal entries are counted
twice, exactly as they are in $z^{\mathsf T}Az$.
If $c_\gamma$ is the rational coefficient of $\gamma$ in the Hessian
biform, the exact affine projection onto all its coefficient equations is

\[
 \mathcal P(T)=T+\sum_\gamma E_\gamma
        \frac{c_\gamma-\langle E_\gamma,T\rangle_F}
             {\|E_\gamma\|_F^2}.
 \tag{15}
\]

Compute a rational symmetric approximation $T$ to $M_x$ with
$\|T-M_x\|_F<\mu/4$ and set $\widehat M=\mathcal P(T)$.
The affine projection fixes $M_x$ and is nonexpansive, so

\[
 \|\widehat M-M_x\|_F<\mu/4,
 \qquad \widehat M\succeq3\mu I/4\succ0.
 \tag{16}
\]

Equation (15) gives the exact polynomial identity (13) with the rational
matrix $\widehat M$. There are polynomially many entries. All matrices
in (8) and (12) are polynomial expressions in the rational input data
and powers of $\alpha$, with polynomial degree and polynomial coefficient
bit length. The root bound and the positive gap (14) therefore require
only polynomially many precision bits. Certified real-root approximation
and exact rational arithmetic compute $T$ and (15) in polynomial bit
time. No exact semidefinite-feasibility oracle is used.

A rational positive definite Gram matrix is an exact rational
certificate: fraction-free elimination, or an exact rational $LDL^{\mathsf T}$
factorization, verifies positivity. It also gives a weighted rational
sum of squares. Positive rational weights can be expanded into a
polynomial number of rational squares using a binary expansion of their
numerator times denominator, so no field extension is necessary.

## Consequence and limits

The construction has $F_0(a)=0$, is a rational sum of squares, and is
strongly convex. Hence its zero set is exactly $\{a\}$.
The usual scaling

\[
 F=\frac{F_0}{\varepsilon\nu^2}
   =\left(\frac{G}{t\nu}\right)^2+
                      \sum_j\left(\frac{r_j}{\nu}\right)^2
 \tag{17}
\]

preserves rational SOS structure and the rational positive definite
Hessian Gram certificate. The choice (3) is stricter than the ordinary
strong-convexity bound in the companion construction, so that proof
gives $\nabla^2F\succeq(3/2)I$. The degree is exactly four, since $H\succ0$ makes the leading
quartic part nonzero.

Thus every real algebraic number with exactly one real conjugate can be
realized as a coordinate of the unique zero of a rational SOS-convex,
globally strongly convex quartic. For a rational prescribed coordinate
$\alpha$, the univariate polynomial $(x-\alpha)^2+(x-\alpha)^4$
gives the same conclusion directly. The converse follows from the
[real-embedding argument for rational convex singletons](few-quadratic-unbounded-degree.md);
convexity certification does not weaken that restriction.
This extends the [explicit bivariate quartic](convex-quartic-irrational-zero.md),
which retains a smaller hand-checkable certificate.

This result does not imply hardness of exact decision. It shows that
allowing a rational Hessian certificate does not restore rational
feasible points or bound their algebraic degree by a constant. Approximate
optimization remains a separate question.

## Prior comparison and verification

Positive definite Hessian Gram matrices and Schur-complement proofs of
SOS-convex regularization are established techniques.
[Ahmadi, Chaudhry, and Zhang, Lemmas 2--3 and Theorem 3](https://arxiv.org/html/2311.06374v2)
give particularly close prior results. The arithmetic distinction here
is preserving a prescribed irrational zero while retaining rational
coefficients, fixed degree four, and polynomial bit bounds. Centering an
ordinary regularizer at that irrational point would not retain rational
coefficients. The [scoped primary-source audit](general-quartic-realization-prior.md)
compares this and other relevant results and does not establish
publication priority.

The [fresh independent review](sos-convex-quartic-realization-review.md)
verified the Gram identity, every Schur and conditioning bound, the
affine coefficient projection, and polynomial-time rational certificate
construction. It also gives an explicit derivative bound for certified
approximation of the algebraic Gram entries. Its exact symbolic checks
covered the block-Gram identity, affine shift, coefficient projection,
and rational-weight expansion into rational squares. They passed.
Those checks support the identities; the general matrix inequalities
and bit bounds are proved above and in the review. No Lean proof or
project-wide verification is claimed.

An author-side targeted `python - <<'PY'` check of this note's local
links, display delimiters, trailing whitespace, and final newline also
passed. No CI inspection was performed.
