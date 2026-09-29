# Independent review of general strongly convex quartic singletons

Date: 2026-09-28. Scope: the quantitative quartic construction in
[general-strongly-convex-quartic-singleton.md](general-strongly-convex-quartic-singleton.md).
The earlier companion construction and its certified root computation
were checked separately in
[general-algebraic-singleton-review.md](general-algebraic-singleton-review.md).

The complete construction passes this review. No mathematical defect was
found in the final draft. The point requiring care is that
the square of a homogeneous indefinite quadratic need not be convex.
Bounding that negative curvature, instead of discarding it, still leaves
enough positive quartic curvature to prove a uniform positive Hessian
bound. All tolerances have polynomial binary length.

## The consistency equations and their Jacobian

Write $n=d-1$, $p(t)=t^{n+1}+\sum_{i=0}^n c_it^i$, and
$a=(\alpha,\ldots,\alpha^n)$. The rational equations are

\[
 r_j(x)=x_1x_j-x_{j+1}\quad(1\leq j<n),
 \qquad
 r_n(x)=x_1x_n+c_0+\sum_{i=1}^n c_ix_i.
\]

They vanish at $a$. In fact, their real zero set is already $\{a\}$:
the first equations force $x_j=x_1^j$, and the last becomes $p(x_1)=0$.
The quartic argument also proves uniqueness independently through strong
convexity.

Let $\mathcal J$ be their Jacobian at $a$. Set
$w=(1,2\alpha,\ldots,n\alpha^{n-1})^{\mathsf T}$. Differentiating the
identities along $(t,t^2,\ldots,t^n)$ gives

\[
 \mathcal Jw=p'(\alpha)e_n.
\]

Replacing the first column by $\mathcal Jw$ leaves the determinant
unchanged because $w_1=1$. The complementary minor, from the first
$n-1$ rows and last $n-1$ columns, is lower triangular with diagonal
$-1$. Expansion in the new first column therefore gives

\[
 \det\mathcal J=p'(\alpha).
\]

There is no missing sign or factor from the first equation $x_1^2-x_2$.
Since all roots of $p$ are distinct, the Jacobian is invertible.

Use the root radius $R$, separation bound $\sigma$, and
$K=dR^{d-1}$ from the quadratic construction. Each Jacobian entry has
magnitude at most $3R^n$, including the terminal row of a nonmonic input
after division by its leading coefficient. Thus

\[
 \|\mathcal J\|_2\leq\|\mathcal J\|_F\leq V:=3K.
\]

The derivative product gives $|p'(\alpha)|\geq\sigma^n$. Consequently

\[
 \sigma_{\min}(\mathcal J)\geq
 \nu:=\frac{\sigma^n}{V^{n-1}},\qquad
 \mathcal J^{\mathsf T}\mathcal J\succeq\nu^2I.
\]

The reciprocal of $\nu$ has polynomial bit length. It is not necessary
for $\nu$ to have inverse-polynomial numerical magnitude.

After translating by $a$, write
$r_j(a+u)=g_j^{\mathsf T}u+u^{\mathsf T}A_ju$. Here
$\|g_j\|\leq V$ and $\|A_j\|_2\leq1$. The first homogeneous
quadratic is $u_1^2$; the others are products of two coordinates, whose
symmetric coefficient matrices have norm $1/2$. Their possible
indefiniteness must be retained in the Hessian argument.

## A rational exposing approximation

The earlier construction supplies a rational pencil $Q(1,s,t)$ and an
exposing member at $(s,t)=(\alpha,\alpha^2)$. Let its affine restriction
have lower eigenvalue bound $\gamma=1/(2K^4)$. With the earlier bounds
$J_0$ on the inverse real Vandermonde matrix, $M$ on the companion matrix,
and $S$ on $\|Q_1\|+\|Q_2\|$, put

\[
 m=\gamma/2,
 \qquad L=2J_0^2(M+R)^2+1.
\]

The exposing matrix has norm at most $L-1$. Approximating
$(\alpha,\alpha^2)$ within maximum distance $\delta$ changes it by at
most $S\delta$. The resulting rational quadratic $G$ still vanishes
exactly at $a$, because every rational member of the pencil obeys the
polynomial remainder identities.

Write $G(a+u)=\eta^{\mathsf T}u+u^{\mathsf T}Hu$. The bounds

\[
 \delta\leq\frac{\gamma}{2S},\qquad
 \delta\leq\frac{\varepsilon}{2SK}
\]

give $H\succeq mI$, $\|H\|\leq L$, and $\|\eta\|\leq\varepsilon$.
For the last inequality, the exposing matrix annihilates $v(\alpha)$,
while the approximate gradient is twice the affine part of its
perturbation times that vector; $\|v(\alpha)\|\leq K$.
An approximation to $\alpha$ of error at most $\delta/(4R)$ suffices
for both coordinates of $(\alpha,\alpha^2)$, using
$|\widehat\alpha+\alpha|\leq3R$.

This controls both the homogeneous quadratic part and the linear term
after translation. Positive definiteness of $H$ alone would not be
sufficient to prove convexity of $G^2$.

## Global Hessian estimate

Set $D=L+nV$, and choose a positive square dyadic rational
$\varepsilon$ satisfying

\[
 \varepsilon\leq
 \min\left\{1,\frac{m^2}{2n},
                 \frac{\nu^2m^2}{36D^2}\right\}.
\]

Consider the untranslated rational sum of squares

\[
 F_0=G^2+\varepsilon\sum_{j=1}^n r_j^2.
\]

At $a+u$, its homogeneous quadratic part has Hessian at least
$2\varepsilon\nu^2I$. For any symmetric $T$ and vector $b$,

\[
 \nabla^2\bigl[2(b^{\mathsf T}u)(u^{\mathsf T}Tu)\bigr]
 =4\bigl[(b^{\mathsf T}u)T+
             b(Tu)^{\mathsf T}+(Tu)b^{\mathsf T}\bigr].
\]

Its norm is at most $12\|b\|\|T\|\|u\|$. The cubic Hessian
therefore has norm at most $12\varepsilon D\|u\|$.

For the homogeneous quartic terms, the exact identity is

\[
 \nabla^2(u^{\mathsf T}Tu)^2
 =8(Tu)(Tu)^{\mathsf T}+4(u^{\mathsf T}Tu)T.
\]

It gives a lower bound $4m^2\|u\|^2I$ for $T=H$, and a lower
bound $-4\|u\|^2I$ for each $T=A_j$. Thus the total quartic Hessian
is at least

\[
 4(m^2-\varepsilon n)\|u\|^2I
 \succeq2m^2\|u\|^2I.
\]

Putting $t=\|u\|$ and completing the scalar square proves

\[
 \begin{aligned}
 \nabla^2F_0(a+u)
 &\succeq
   [2m^2t^2-12\varepsilon Dt+2\varepsilon\nu^2]I\\
 &\succeq
   \left[2\varepsilon\nu^2-
            \frac{18\varepsilon^2D^2}{m^2}\right]I
 \succeq\tfrac32\varepsilon\nu^2I.
 \end{aligned}
\]

This proves a bound on all of $\mathbb R^n$, with no bounded-domain
assumption. The negative curvature from the indefinite squares is fully
included.

Since $\varepsilon$ is a rational square and $\nu$ is positive rational,
the normalized polynomial

\[
 F=\frac{F_0}{\varepsilon\nu^2}
   =\left(\frac{G}{\sqrt\varepsilon\,\nu}\right)^2
           +\sum_{j=1}^n\left(\frac{r_j}{\nu}\right)^2
\]

is a sum of squares of rational quadratics and satisfies
$\nabla^2F\succeq\tfrac32I\succeq I$. It vanishes at $a$, so this
point is its unique zero and minimizer. Its degree is exactly four:
the positive-definite homogeneous quadratic part of $G$ has a nonzero
square, and the other squared leading terms cannot cancel it.

All scale choices have polynomial bit length in $d,H$; in particular
$\log(1/\nu)$ is polynomial by the explicit separation estimate.
Choosing a square dyadic $\varepsilon$ below the displayed minimum adds
only a constant factor to its required logarithmic precision. The root
refinement, rational operations, normalization, and expansion into
$O(n^4)$ quartic coefficients therefore take polynomial time and preserve
polynomial output length. For arbitrary rational input, primitive
normalization must still be charged to the original input length.

The assertion that $F$ is a sum of squares concerns $F$ itself. This
Hessian argument alone does not assert that its Hessian has a rational
polynomial matrix factorization, a separate property usually called
SOS-convexity.

## Targeted verification

An inline `python - <<'PY'` command using SymPy checked the homogeneous
quartic Hessian identity for a generic symmetric matrix in three
variables, the cubic Hessian identity for a generic vector and symmetric
matrix in three variables, and the canonical Jacobian determinant
identity with symbolic polynomial coefficients in degrees three, four,
and five. The even-degree check concerns the algebraic identity only;
the realization theorem still assumes exactly one real root and hence
odd degree. All checks passed.

The same command checked the regression that $(xy)^2$ has an indefinite
Hessian at $(1,1)$: its determinant is $-12$. This rules out the incorrect
shortcut of treating every squared consistency quadratic as convex.
The global matrix bound follows from the proof above, not from sampled
Hessians. A separate inline `python - <<'PY'` command checked this review's
local links, display delimiters, final newline, whitespace, and control
characters; it passed. No project-wide verification or CI inspection was
performed.
