# Sharp models and an integrability gap for bounded-face row sharing

Status: Proved; targeted literature screen and independent hostile audit completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the stated scopes

## Summary

The bounded-face packing theorem gives the local implication

\[
        \dim F\leq f\quad\Longrightarrow\quad
        \text{one cone block is active on at most }f\text{ source rows}.
                                                               \tag{1}
\]

This note tests its sharpness.  There are two complementary conclusions.

1. For a block that carries whole product-ball slack rows, global linear
   integrability is much stricter than (1): serving \(q\) rows forces
   \(m\geq qs+1\) and \(f\geq1+(q-1)s\).  Both bounds are attained by the
   homogenization cone of \((B_2^s)^q\).  This gives an exact capped theorem
   for row-indivisible grouped factorizations.
2. Linear-in-\(f\) sharing is nevertheless possible for split rows.  A
   natural shared-perspective cone of dimension \(2q+1\) and maximum
   complementary-face dimension \(2q-1\) carries \(q\) independent scalar
   square channels in one globally polynomial block.  Coordinatewise use
   gives a full product-ball factorization.  Thus the \(1/f\) dependence of
   a general incidence theorem cannot be removed, although the optimal
   constant and its dependence on the sphere dimension remain open.
3. The two sharp sharing cones have exact intrinsic barrier parameter
   \(q+1\), not a constant: explicit optimal barriers are given below.
   Consequently, bundling \(q\) channels can collapse the number of cone
   factors by \(q\), but it cannot collapse the ambient IPM iteration
   parameter by the same factor.

Homogeneous PSD blocks also share rows, but their support faces are much
larger: the same scalar construction in \(\mathbb S_+^{q+1}\) has contact
face dimension \(q(q+1)/2\).  This makes precise why PSD column packing is
qualitatively possible but face-dimension inefficient compared with the
shared-perspective cone.

## 1. A sharp one-block theorem for whole rows

Let one proper cone \(K\subset\mathbb R^m\) factor the \(q\) full rows

\[
  1-\langle x_a,z\rangle
     =\langle A(x),B^a(z)\rangle,
 \qquad a\in[q],\quad
 x\in(S^{s-1})^q,\quad z\in S^{s-1}.                       \tag{2}
\]

No regularity beyond continuity is needed for the following lower bounds:

\[
 \boxed{
       m\geq qs+1,
       \qquad
       \max_{0\ne b\in\partial K^*}
          \dim(K\cap b^\perp)\geq1+(q-1)s.}               \tag{3}
\]

### Ordinary functional rank

As \(a,z\) vary, the functions on \((S^{s-1})^q\) on the left side of (2)
span

\[
            \operatorname{span}\{1,x_{a,j}:a\in[q],j\in[s]\}.
                                                               \tag{4}
\]

They contain \(1\) by averaging the rows indexed by \(z\) and \(-z\), and
contain \(x_{a,j}\) by taking the difference of the rows indexed by
\(-e_j\) and \(e_j\).  The \(1+qs\) displayed functions are linearly
independent on the product of spheres.  A bilinear factorization through
\(\mathbb R^m\) has row-function span at most \(m\), proving the first
bound in (3).

### A contact cylinder forces a large face

Fix \(a\) and \(z\), and put

\[
              \mathcal F_{a,z}=K\cap B^a(z)^\perp.         \tag{5}
\]

At every point of the contact cylinder \(x_a=z\), the vector \(A(x)\) lies
in \(\mathcal F_{a,z}\).  On this cylinder the linear functional
\(B^a(-z)/2\) takes the constant value one.  For every \(b\ne a\), the
linear functional

\[
                 \frac{B^b(-e_j)-B^b(e_j)}{2}             \tag{6}
\]

takes the value \(x_{b,j}\).  Therefore a linear image of the span of
\(\mathcal F_{a,z}\) contains

\[
                \{1\}\times(S^{s-1})^{q-1},               \tag{7}
\]

whose linear span has dimension \(1+(q-1)s\).  This proves the second
bound in (3).  It is stronger by \((q-1)\) dimensions than the purely
differential estimate \(1+(q-1)(s-1)\): the full slack rows linearly recover
the radial/constant coordinate of every other ball as well as its tangent
directions.

## 2. The homogenization cone attains both bounds

Define

\[
 \mathcal H_{q,s}
   =\{(t,y_1,\ldots,y_q):t\geq0,\ \|y_a\|_2\leq t
                                      \text{ for all }a\}. \tag{8}
\]

This is the homogenization cone of \((B_2^s)^q\), has dimension \(qs+1\),
and is proper.  The polynomial factor maps

\[
 A(x)=(1,x_1,\ldots,x_q),
 \qquad
 B^a(z)=(1,0,\ldots,-z,\ldots,0)                          \tag{9}
\]

give (2).

Its dual is

\[
 \mathcal H_{q,s}^*
   =\{(\alpha,w_1,\ldots,w_q):
                   \alpha\geq\sum_a\|w_a\|_2\}.          \tag{10}
\]

For a nonzero dual boundary vector, let
\(J=\{a:w_a\ne0\}\).  Equality in the dual pairing fixes
\(y_a=-t w_a/\|w_a\|\) for \(a\in J\), while every other \(y_b\) ranges
over \(tB_2^s\).  Hence its exposed complementary face has dimension

\[
                        1+(q-|J|)s.                        \tag{11}
\]

The maximum is attained at \(|J|=1\), so

\[
       \dim\mathcal H_{q,s}=qs+1,
       \qquad f(\mathcal H_{q,s})=1+(q-1)s.               \tag{12}
\]

Thus (3) is simultaneously sharp.

For comparison, treating \(Q_{s+1}^{\times q}\) as one cone also factors
the rows, but has dimension \(q(s+1)\) and maximum proper exposed-face
dimension \(1+(q-1)(s+1)\).  Sharing the scale coordinate in
\(\mathcal H_{q,s}\) removes exactly \(q-1\) redundant ambient dimensions
and \(q-1\) redundant face dimensions.

### Heterogeneous row dimensions

The construction and all sharp counts extend without an equal-dimension
assumption.  For positive integers \(s_1,\ldots,s_q\), define

\[
 \mathcal H_{\boldsymbol s}
   =\{(t,y_1,\ldots,y_q):t\geq0,\ \|y_a\|_2\leq t,
                         \ y_a\in\mathbb R^{s_a}\}.       \tag{12a}
\]

Then

\[
 \begin{aligned}
 \dim\mathcal H_{\boldsymbol s}
    &=1+\sum_{a=1}^q s_a,\\
 f(\mathcal H_{\boldsymbol s})
    &=1+\sum_{a=1}^q s_a-\min_a s_a.                     \tag{12b}
 \end{aligned}
\]

Indeed, its dual is still
\(\{(\alpha,w):\alpha\geq\sum_a\|w_a\|_2\}\).  If a
nonzero boundary functional has support
\(J=\{a:w_a\ne0\}\), its complementary face has dimension

\[
                   1+\sum_{a\notin J}s_a.                \tag{12c}
\]

The maximum over nonempty \(J\) is obtained by taking a singleton whose
ball dimension is minimal, proving (12b).  The functional-rank and contact-
cylinder proofs also become

\[
       m\geq1+\sum_a s_a,
       \qquad
       f\geq1+\sum_a s_a-\min_a s_a,                    \tag{12d}
\]

so the heterogeneous construction is again simultaneously sharp for a
block carrying all of the indicated whole rows.

This gives an exact, if combinatorial, heterogeneous grouping theorem.
Under a block-dimension cap \(d\) and complementary-face cap \(f\), the
minimum number of row-indivisible blocks is the minimum number of parts in
a partition \(\mathcal G\) of \([k]\) such that every part \(G\) obeys

\[
       \sum_{a\in G}s_a\leq d-1,
       \qquad
       \sum_{a\in G}s_a-\min_{a\in G}s_a\leq f-1.        \tag{12e}
\]

Necessity is (12d) applied to each assigned block; sufficiency uses one
\(\mathcal H_{(s_a)_{a\in G}}\) per part.  Unlike the equal-dimension
closed form (14), optimizing (12e) is strongly NP-hard.  With
\(f=d-1\), its second constraint is redundant and it is exactly bin
packing with item sizes \(s_a\) and capacity \(d-1\); the usual
3-PARTITION restriction proves strong NP-hardness.  Thus heterogeneous
whole-row cone grouping has an exact geometric characterization, but an
optimal compiler cannot in general obtain the grouping by a simple cap
formula.

For every feasible heterogeneous partition with \(g=|\mathcal G|\), the
attaining construction has the exact ledger

\[
        D_{\rm amb}=\sum_{a=1}^k s_a+g,
        \qquad
        \nu_{\rm ambient}=k+g.                            \tag{12f}
\]

The second equality holds against arbitrary coupled self-concordant
barriers on that fixed product of \(\mathcal H\)-cones, by the certificate
argument below.  Hence within the dimension-sharp \(\mathcal H\)-realization,
minimizing the factor count, ambient dimension, and ambient barrier
parameter is the same strongly NP-hard grouping problem; their additive
offsets differ, but their optimizer is identical.  This does not lower-bound
the optimal barrier of a different admissible cone dictionary.

## 3. Exact row-indivisible grouping frontier

Call a factorization **row-indivisible** if every source row is assigned to
one cone block: there is a map \(i:[k]\to[L]\) such that
\(B_j^a\equiv0\) for \(j\ne i(a)\).  The assigned block then carries the
entire row because the terms sum to the full slack.

Suppose every block has dimension at most \(d\) and every nonzero exposed
complementary face has dimension at most \(f\).  Assume \(d\geq s+1\) and
\(f\geq1\), and put

\[
 Q(d,f,s)=\min\left\{
       \left\lfloor\frac{d-1}{s}\right\rfloor,
       1+\left\lfloor\frac{f-1}{s}\right\rfloor
                  \right\}.                               \tag{13}
\]

Then the exact minimum row-indivisible factor count is

\[
 \boxed{
                      L_{\rm row}
                        =\left\lceil\frac{k}{Q(d,f,s)}\right\rceil.}
                                                               \tag{14}
\]

Indeed, if one block is assigned \(q\) rows, (3) gives \(q\leq Q\).
Conversely, partition the sources into groups of size at most \(Q\) and use
one \(\mathcal H_{q,s}\) block for each group.  Equations (9) and (12)
meet both caps and give globally analytic selected factors.  At \(f=1\),
(14) reduces to one strictly convex/ray-exposed block per source.  At larger
\(f\), it gives an exact integrability gap from the local incidence estimate:
a whole-row block can serve only \(1+\lfloor(f-1)/s\rfloor\), not \(f\),
sources.

This theorem is deliberately restricted to row-indivisible factorizations.
Split-row factorizations can share lower-rank curvature channels more
efficiently, as the next construction shows.

## 4. A face-efficient shared scalar-square cone

For \(q\geq1\), define

\[
 \mathcal P_q=\left\{(t,u,w)\in
       \mathbb R\times\mathbb R^q\times\mathbb R^q:
       t\geq0,\ w_a\geq0,\ t w_a\geq u_a^2\ (a\in[q])
                         \right\}.                         \tag{15}
\]

It is a proper cone of dimension \(2q+1\), obtained by coupling \(q\)
rotated quadratic cones through one scale variable.  Put

\[
 \mathcal A(v)=(1,v_1,\ldots,v_q,v_1^2,\ldots,v_q^2),
 \qquad v\in[-1,1]^q,                                    \tag{16}
\]

and let \(\mathcal B^a(z)\) have coefficients

\[
     \left(\frac{z^2}{2},-z e_a,\frac12e_a\right).        \tag{17}
\]

For every point of \(\mathcal P_q\),

\[
 \left\langle(t,u,w),\mathcal B^a(z)\right\rangle
  =\frac12(tz^2-2zu_a+w_a)\geq0,                          \tag{18}
\]

and equality (16) gives

\[
       \langle\mathcal A(v),\mathcal B^a(z)\rangle
                             =\frac12(v_a-z)^2.             \tag{19}
\]

The dual cone consists of triples \((\alpha,\beta,\gamma)\) with
\(\gamma\geq0\), \(\beta_a=0\) whenever \(\gamma_a=0\), and

\[
                  \alpha\geq
                   \sum_{a:\gamma_a>0}\frac{\beta_a^2}{4\gamma_a}.
                                                               \tag{20}
\]

If \(J=\{a:\gamma_a>0\}\ne\varnothing\) and equality holds in (20),
the exposed face has dimension \(1+2(q-|J|)\).  Strict inequality leaves
only a subface of the recession orthant, of dimension at most \(q-|J|\);
the functional \((1,0,0)\) exposes the full recession face of dimension
\(q\).  It follows that

\[
       \dim\mathcal P_q=2q+1,
       \qquad f(\mathcal P_q)=2q-1.                       \tag{21}
\]

Both numbers are minimal for one block carrying all \(q\) scalar kernels
(19).  Their ordinary functional span is

\[
                     \operatorname{span}\{1,v_a,v_a^2:a\in[q]\},
                                                               \tag{22}
\]

of dimension \(2q+1\).  On a contact cylinder \(v_a=z\), the other scalar
kernel rows recover \(1,v_b,v_b^2\), so its complementary face must have
dimension at least \(1+2(q-1)=2q-1\).  Thus \(\mathcal P_q\) is the exact
minimum-dimension and minimum-face one-block realization of these scalar
square rows.

To factor the full product-ball slack, partition the \(k\) source balls
into groups of size at most \(q\).  For each Euclidean coordinate
\(j\in[s]\) and each source group, use one \(\mathcal P_q\) block with
\(v_a=x_{a,j}\) and scalar dual argument \(z_j\).  Summing (19) gives

\[
             \frac12\sum_{j=1}^s(x_{a,j}-z_j)^2
                        =1-\langle x_a,z\rangle.            \tag{23}
\]

This is a globally polynomial factorization with

\[
   L=s\left\lceil\frac{k}{q}\right\rceil,
   \qquad d=2q+1,
   \qquad f=2q-1                                           \tag{24}
\]

when all groups are full, with smaller last blocks otherwise.  Hence a
single block can share \((f+1)/2\) independent rank-one source channels.
For fixed \(s\), (24) has \(L=O(ks/f)\); the inverse-linear dependence on
face dimension in a general sharing bound is therefore unavoidable up to a
constant depending on \(s\).  Whether arbitrary full-row factorizations can
improve the constant two inherent in \(f(\mathcal P_q)=2q-1\) is open.

## 5. Homogeneous and PSD comparisons

The cone \(\mathcal H_{q,s}\) is generally not homogeneous when \(q>1\),
but homogeneous cones also permit sharing once they have large faces.

For scalar square rows, take \(K=\mathbb S_+^{q+1}\),
\(v(u)=(1,u_1,\ldots,u_q)^T\), and

\[
 A(u)=v(u)v(u)^T,
 \qquad
 B^a(z)=\frac12(e_a-ze_0)(e_a-ze_0)^T.                    \tag{25}
\]

Then \(\operatorname{tr}(A(u)B^a(z))=(u_a-z)^2/2\).  The contact dual has
rank one and nullity \(q\), so it exposes a copy of \(\mathbb S_+^q\) of
dimension

\[
                              \frac{q(q+1)}2.               \tag{26}
\]

The block shares \(q\) scalar rows, but uses a quadratic rather than linear
face budget.  Applying (25) coordinatewise gives another globally
polynomial full product-ball factorization with
\(s\lceil k/q\rceil\) PSD blocks of order at most \(q+1\).

One PSD block can also carry \(q\) whole ball rows.  Let

\[
 v(x)=(1,x_1,\ldots,x_q)^T\in\mathbb R^{1+qs},
 \quad A(x)=v(x)v(x)^T,
\]

and set

\[
 B^a(z)=\frac12\sum_{j=1}^s
      (e_{a,j}-z_je_0)(e_{a,j}-z_je_0)^T.                 \tag{27}
\]

Then \(\operatorname{tr}(A(x)B^a(z))=1-x_a^Tz\).  At contact,
\(B^a(z)\) has rank \(s\), nullity \(1+(q-1)s\), and hence exposes a PSD
face of dimension

\[
                   \binom{2+(q-1)s}{2}.                  \tag{28}
\]

This is the support-Grassmannian version of the face packing mechanism, but
it is far less face-efficient than the optimal homogenization cone (12).
Likewise, the homogeneous product cone \(Q_{s+1}^{\times q}\) is less
efficient than \(\mathcal H_{q,s}\) by exactly \(q-1\) dimensions.

These comparisons do not prove that no irreducible homogeneous cone can
improve on the displayed PSD construction.  They show only that the most
direct homogeneous packings do not attain the information-theoretic
whole-row face minimum (3).

## 6. Exact barriers: sharing factors does not share the IPM parameter

Write \(\nu_{\rm opt}(K)\) for the infimum of the parameters of
logarithmically homogeneous self-concordant barriers (LHSCBs) on a proper
cone \(K\).  Both nonhomogeneous sharp models above have the same exact
answer:

\[
 \boxed{\nu_{\rm opt}(\mathcal H_{q,s})
       =\nu_{\rm opt}(\mathcal P_q)=q+1.}                 \tag{29}
\]

### The product-ball homogenization cone

An optimal barrier for \(\mathcal H_{q,s}\) is

\[
 F_{\mathcal H}(t,y)
   =-\sum_{a=1}^q\log\bigl(t^2-\|y_a\|_2^2\bigr)
       +(q-1)\log t.                                     \tag{30}
\]

This formula is a linear restriction of Nesterov--Nemirovskii's classical
\((r+1)\)-barrier
\((r-1)\log t-\log\det(t^2I_r-WW^T)\) for the spectral-norm cone
\(t\geq\sigma_{\max}(W)\).  Take \(r=q\) and put each row vector \(y_a\)
in a private block of \(s\) columns of \(W\).  Then
\(WW^T=\operatorname{Diag}(\|y_1\|^2,\ldots,\|y_q\|^2)\), so the cone and
barrier restrict exactly to \(\mathcal H_{q,s}\) and (30).  The following
calculation is therefore an independent direct verification, not a new
barrier construction.

The positive \(\log t\) correction is essential: it reduces the
logarithmic-homogeneity degree of the obvious sum of \(q\) Lorentz
barriers from \(2q\) to \(q+1\).  It is not legitimate to infer
self-concordance merely by subtracting barriers, so here is a direct
verification.

Put \(n=q+1\).  On the section \(t=1\), the normalized function associated
with (30) is

\[
 f(y)=-\frac1n\sum_{a=1}^q\log(1-\|y_a\|_2^2).            \tag{31}
\]

For a point \(y\) and direction \(h\), define the two nonnegative inverse
line-to-boundary distances

\[
 \begin{aligned}
 r_a^-&=\frac{\sqrt{\langle y_a,h_a\rangle^2
       +(1-\|y_a\|^2)\|h_a\|^2}+\langle y_a,h_a\rangle}
      {1-\|y_a\|^2},\\
 r_a^+&=\frac{\sqrt{\langle y_a,h_a\rangle^2
       +(1-\|y_a\|^2)\|h_a\|^2}-\langle y_a,h_a\rangle}
      {1-\|y_a\|^2}.
 \end{aligned}                                           \tag{32}
\]

They factor the directional quadratic
\(1-\|y_a+\lambda h_a\|^2\), and direct differentiation gives

\[
 \begin{aligned}
 Df[h]&=\frac1n\sum_a(r_a^- -r_a^+),\\
 D^2f[h,h]&=\frac1n\sum_a((r_a^-)^2+(r_a^+)^2),\\
 D^3f[h,h,h]&=\frac2n\sum_a((r_a^-)^3-(r_a^+)^3).
 \end{aligned}                                           \tag{33}
\]

These are exactly the three scalar formulas in Hildebrand's proof of the
optimal barrier for the \(\ell_\infty\)-epigraph cone.  His auxiliary
inequality is stated for arbitrary nonnegative pairs \((r_a^-,r_a^+)\),
so it applies unchanged to (32); it does not use that a ball block is
one-dimensional.  Moreover

\[
                       r_a^-r_a^+
          =\frac{\|h_a\|^2}{1-\|y_a\|^2},                \tag{34}
\]

which makes the projective Hessian strictly positive for every nonzero
\(h\).  Hildebrand's conic/projective equivalence therefore turns (33)
into positive Hessian and the ordinary self-concordance inequality for
(30).  Boundary blow-up and \((q+1)\)-logarithmic homogeneity are immediate,
so (30) is a \((q+1)\)-LHSCB.

For the matching lower bound, fix one unit vector \(e\in\mathbb R^s\) and
restrict to \(y_a=\xi_a e\).  The resulting linear section is

\[
             \{(t,\xi):t\geq|\xi_a|\ \text{for all }a\}, \tag{35}
\]

the \((q+1)\)-dimensional \(\ell_\infty\)-epigraph cone.  Restriction
preserves the LHSCB parameter, and the sharp polyhedral-vertex lower bound
gives \(\nu\geq q+1\).  This also shows why the parameter in (30) is
independent of the ball dimension \(s\).

The same section supplies a parameter-sharp Nesterov recession
certificate, which will be useful for products.  Fix
\(0<\epsilon<\min\{1,2/q\}\) and put

\[
 x_0=(1,(1-\epsilon)e,\ldots,(1-\epsilon)e)\in
       \operatorname{int}\mathcal H_{q,s}.               \tag{35a}
\]

Let \(p_0\) have scale one and every ball component equal to \(e\).  For
\(i\in[q]\), let \(p_i\) have scale one, ball component \(-e\) in position
\(i\), and \(e\) in every other position.  All \(p_i\) lie in
\(\mathcal H_{q,s}\), hence in its recession cone.  Choose

\[
 \begin{aligned}
 a_0&=1-q\epsilon/2,& b_0&=1-\epsilon/2,\\
 a_i&=b_i=\epsilon/2 &&(i\in[q]).
 \end{aligned}                                           \tag{35b}
\]

Directly, the joint subtraction is the cone vertex,

\[
                  x_0-a_0p_0-\sum_{i=1}^q a_ip_i=0.       \tag{35c}
\]

For \(i\geq1\), the \(i\)-th ball of \(x_0-b_ip_i\) has
norm and scale both \(1-\epsilon/2\), while every other ball has norm
\(|1-3\epsilon/2|\leq1-\epsilon/2\).  For \(i=0\), every ball of
\(x_0-b_0p_0\) has norm and scale both \(\epsilon/2\).  Thus every
individual subtraction is feasible and noninterior.  The certificate value is

\[
 q+\frac{1-q\epsilon/2}{1-\epsilon/2}
       \ \longrightarrow\ q+1.                           \tag{35d}
\]

Nesterov's recession-certificate lower bound therefore recovers
\(\nu\geq q+1\), but now in a form that tensorizes: placing local
certificate directions in separate direct summands gives a certificate
on a product whose value is the sum of the local values.

Nothing in this barrier argument requires equal vector dimensions.  On
\(\mathcal H_{\boldsymbol s}\), the same formula

\[
 -\sum_{a=1}^q\log(t^2-\|y_a\|_2^2)+(q-1)\log t          \tag{35e}
\]

is a \((q+1)\)-LHSCB: the proof (31)--(34) uses only one nonnegative
inverse-distance pair for each ball block.  Choosing an arbitrary unit
vector in each \(\mathbb R^{s_a}\) gives both the scalar
\(\ell_\infty\)-section and the certificate (35a)--(35d).  Consequently

\[
                   \nu_{\rm opt}(\mathcal H_{\boldsymbol s})=q+1. \tag{35f}
\]

For any partition of heterogeneous source balls into \(g\) groups, with
\(k\) rows in total, certificate tensorization gives exact coupled ambient
parameter \(k+g\).  Fixing each group scale to one restricts (35e) to the
ordinary heterogeneous product-ball barrier, whose exact affine parameter
is \(k\); its value, derivatives, Dikin geometry, and reduced Newton system
are independent of the grouping.

### The shared-perspective cone

For the dual variables in (20), introduce the sparse arrow matrix

\[
 M(\alpha,\beta,\gamma)=
 \begin{pmatrix}
  \alpha&\beta^T/2\\[2pt]
  \beta/2&\operatorname{Diag}(\gamma)
 \end{pmatrix}.                                          \tag{36}
\]

Then \(\mathcal P_q^*=\{(\alpha,\beta,\gamma):M\succeq0\}\).
The restriction \(-\log\det M\) of the order-\(q+1\) PSD barrier is a
\((q+1)\)-LHSCB on \(\mathcal P_q^*\).  LHSCB Legendre duality transfers
the same parameter to \(\mathcal P_q\); carrying out the scalar
maximizations gives, up to an additive constant, the explicit primal
barrier

\[
 F_{\mathcal P}(t,u,w)
    =-\sum_{a=1}^q\log(tw_a-u_a^2)+(q-1)\log t.           \tag{37}
\]

Equivalently, \(\mathcal P_q\) is the PSD-completable partial-matrix cone
of a star graph.  Classical chordal maximum-determinant completion gives

\[
             \det X_{\max\det}
       =\frac{\prod_a(tw_a-u_a^2)}{t^{q-1}},
\]

whose negative logarithm is (37).  Thus the formula and its
\((q+1)\)-upper bound are also classical sparse-matrix-barrier
specializations; the contribution here is their use and sharp accounting
in the shared-perspective slack model.

Conversely, the linear section \(u=0\) of \(\mathcal P_q\) is the
orthant \(\mathbb R_+^{q+1}\) in coordinates \((t,w)\).  The optimal
orthant lower bound is \(q+1\), proving the second equality in (29).

### Exact ambient costs for the grouped constructions

Partition the \(k\) source rows into \(g=\lceil k/q\rceil\) groups of
sizes \(q_1,\ldots,q_g\), so \(\sum_\ell q_\ell=k\).  The sum of the
optimal block barriers (30) for the row-indivisible construction has
parameter

\[
                       \sum_{\ell=1}^g(q_\ell+1)=k+g.     \tag{38}
\]

The exact optimum on the ambient product, even over barriers that couple
different factors, is

\[
       \boxed{\nu_{\rm opt}\!\left(\prod_{\ell=1}^g
                      \mathcal H_{q_\ell,s}\right)=k+g.} \tag{38a}
\]

With arbitrary factorwise ball dimensions the same statement is

\[
 \nu_{\rm opt}\!\left(\prod_{\ell=1}^g
       \mathcal H_{q_\ell,s_\ell}\right)
 =\sum_{\ell=1}^g(q_\ell+1).
\]

More generally, each factor may contain unequal internal dimensions as in
\(\mathcal H_{\boldsymbol s}\); only its number of ball blocks enters the
sum.

Indeed, apply the certificate (35a)--(35d) independently in each direct
factor.  Recession-certificate tensorization and then
\(\epsilon\downarrow0\) give the lower bound
\(\sum_\ell(q_\ell+1)=k+g\); the sum barrier (30) gives the matching upper
bound.  Nesterov's certificate theorem applies to every standard
self-concordant barrier, not only to logarithmically homogeneous or
separable barriers.  Thus (38a) is also the optimum in that larger barrier
class, under the same parameter convention.

This certificate is needed.  A tempting shortcut is to restrict to the
scalar product cone and choose a boundary ray supported in only one group.
The active facet normals there have rank \(k+g-1\), but every vanished
group lies on all of its \(2q_\ell\) facets, whose normals are dependent.
The sharp active-facet theorem requires a local representation by exactly
the stated number of independent facets; rank alone does not meet its
hypotheses.  Therefore that shortcut does not prove (38a).

The certificate argument is stronger than restricting a product to either a
common-scale \(\ell_\infty\)-epigraph section or an orthant section, which
would give only \(k+1\) or \(2g\), respectively.  In particular,
factorwise optimality alone is not being used as an additivity theorem;
the explicit parameter-sharp certificates are what prove additivity.
Relative to the \(2k\) parameter of \(k\) separate Lorentz factors, whole-row
grouping therefore improves the exact ambient parameter only to \(k+g\).
Even maximal grouping \(g=1\) saves asymptotically a factor two in
\(\nu\), or \(\sqrt2\) in a standard \(O(\sqrt\nu\log(1/\epsilon))\)
iteration bound, despite collapsing the factor count from \(k\) to one.

There is an exact and stronger statement on the affine formulation that
the slack factorization actually uses.  Fix every group scale
\(t_\ell=1\).  The sum of (30) then restricts to

\[
             \Phi(y)=-\sum_{a=1}^k\log(1-\|y_a\|^2),     \tag{38b}
\]

the ordinary product-ball barrier, with exact affine SCB parameter \(k\).
The upper bound is the product rule.  For the lower bound, restrict every
ball to one scalar diameter; the resulting cube has a vertex with \(k\)
linearly independent active facets, so the standard vertex lower bound is
\(k\).  Formula (38b), including its block-diagonal Hessian and Newton
equations, is completely independent of the grouping
\((q_1,\ldots,q_g)\).  Hence bundling whole rows changes the cone
description but gives no barrier-iteration or reduced-Newton-system
improvement on this fixed-scale slice.  This exact slice statement is
separate from the ambient conic bounds (38a).

The statement is literal at the oracle level.  After eliminating the
fixed scales, the value, gradient, Hessian, Hessian-vector products, Dikin
metric, and KKT/Newton equations obtained from one cone
\(\mathcal H_{k,s}\), from any intermediate grouping, or from \(k\)
separate Lorentz cones are the same maps for (38b), up to coordinate
relabeling.  Thus a reduced classical or quantum oracle for one grouping
can be matched exactly for every other grouping.  Any remaining cost
difference must come from the chosen ambient representation or its data
access implementation, not from the reduced barrier geometry.

There is also a genuine bounded-move lower bound, not just a parameter
comparison.  Choose unit vectors \(c_a\) and maximize
\(\ell(y)=\sum_ac_a^Ty_a\), whose optimum is \(k\).  Start at the analytic
center \(y=0\).  If each counted outer round contains at most \(m\) chords,
each chord stays in the product-ball interior and has starting-point Dikin
norm at most a fixed \(R<1\), then reaching
\(k-\ell(y)\leq\epsilon\) requires

\[
 T\ \geq\
 \frac{\left[\sqrt{k}\log\!\left(k/(2\epsilon)\right)\right]_+}
      {m\log(1/(1-R))}.                                  \tag{38c}
\]

This is the \(h=1\) specialization of the independently audited
[path-independent small-step theorem](2026-09-04-grouped-ball-short-step-iteration-lower-bound.md).
It allows arbitrary classical or quantum computation between the bounded
Dikin moves and does not require later iterates to remain near the central
path.  Hence even the one-factor representation \(\mathcal H_{k,s}\)
retains
\(\Omega(\sqrt{k}\log(k/\epsilon))\) moves in this model.  This is not a
query or runtime lower bound for unrestricted QIPMs, and it does not cover
methods that take unbounded local-norm moves.

For completeness, the exact central path is also grouping-independent:

\[
 y_a(\tau)=r(\tau)c_a,qquad
 r(\tau)=\frac{\tau}{\sqrt{1+\tau^2}+1},qquad
 k-\ell(y(\tau))=k(1-r(\tau)).                           \tag{38d}
\]

Thus the same central path, local metric, and lower bound survive the
maximal factor-count collapse from \(k\) cones to one.

For the coordinatewise \(\mathcal P\)-construction, there are \(s\)
copies of this grouping.  The product barrier parameter is exactly

\[
                           \nu=s(k+g).                    \tag{39}
\]

Optimality follows by taking \(u=0\) in every block, which produces an
orthant section of dimension \(s(k+g)\).  Thus sharing reduces the number
of \(\mathcal P\)-blocks to \(sg\), but its best possible ambient barrier
parameter remains \(\Theta(sk)\).  Relative to \(2sk\) separate rotated
quadratic cones it saves at most a factor approaching two in \(\nu\), or
\(\sqrt2\) in the usual \(O(\sqrt\nu\log(1/\epsilon))\) iteration term,
not the factor \(q\) suggested by the block count.  This statement concerns
iteration complexity; the cost of evaluating and solving with the bundled
barrier Hessian is a separate issue.

## Scope, novelty screen, and open problem

The exact theorem (14) applies to the explicitly defined row-indivisible
class.  The constructions (23), (25), and (27) are unrestricted valid
factorizations, but no exact unrestricted factor-count claim is made for
\(f>1\).  Equations (29)--(39) settle both intrinsic single-block
parameters, the fixed-scale affine parameter, and the exact ambient
parameters of both the \(\mathcal H\)- and \(\mathcal P\)-product
constructions.  Face-efficient representation and barrier-efficient
representation need not coincide for other dictionaries.

The general lift/factorization correspondence is due to
Gouveia--Parrilo--Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://arxiv.org/abs/1111.3164).  General properties of
homogenization cones are discussed by Bauschke--Bendit--Wang,
[*The Homogenization Cone: Polar Cone and
Projection*](https://arxiv.org/abs/2206.02694).  Saunderson's
[*Limitations on the Expressive Power of Convex Cones Without Long Chains
of Faces*](https://arxiv.org/abs/1902.06401) studies a different
neighborliness/face-chain obstruction.
The conic/projective derivative criterion and the nonnegative-pair
inequality used in (31)--(34), as well as the sharp
\(\ell_\infty\)-epigraph lower bound, are from Hildebrand,
[*A Lower Bound on the Barrier Parameter of Barriers for Convex
Cones*](https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf).
More importantly, (30) is the private-column-block restriction of the
spectral-norm-cone barrier in Nesterov--Nemirovskii,
[*Interior-Point Polynomial Algorithms in Convex
Programming*](https://doi.org/10.1137/1.9781611970791.ch5), Section 5.4.6;
Güler's [*Barrier Functions in Interior Point
Methods*](https://doi.org/10.1287/moor.21.4.860) contains its scalar
\(s=1\) case.  Therefore neither (30), its self-concordance, nor its
\(q+1\) upper bound is a new construction.  The scalar-section lower bound
combines with that classical upper bound to prove the exact parameter for
the block restriction.

Likewise, (37) is the star-graph specialization of classical chordal
maximum-determinant completion: see Grone--Johnson--Sá--Wolkowicz,
[*Positive Definite Completions of Partial Hermitian
Matrices*](https://doi.org/10.1016/0024-3795(84)90207-6), and
Barrett--Johnson--Lundquist,
[*Determinantal Formulae for Matrix Completions Associated with Chordal
Graphs*](https://doi.org/10.1016/0024-3795(89)90706-4).  Andersen--Dahl--
Vandenberghe,
[*Logarithmic Barriers for Sparse Matrix
Cones*](https://arxiv.org/abs/1203.2742), develops the corresponding
conjugate barrier on the PSD-completable cone.  The \(u=0\) orthant
section supplies the matching lower bound.  The exact parameters in (29)
are useful syntheses for these sharing models, but the underlying barriers
must not be claimed as new.

Standard restriction, product, PSD log-determinant, and LHSCB
Legendre-duality rules are used for (36)--(39).  The recession-certificate
theorem used in (35a)--(35d) is due to Nesterov and is reproduced as
Theorem 3.9 by
[Fawzi--Saunderson](https://doi.org/10.1137/22M1500216); the direct-sum
tensorization used for
(38a) is recorded with proof in
[the exact product-barrier note](2026-09-04-exponential-product-exact-barrier-parameter.md).

A targeted search found no source stating the simultaneous one-block
dimension/face lower bound (3), the exact row-indivisible frontier (14), its
heterogeneous partition form (12e), or the face-optimal shared-perspective
factorization (15)--(24).  The strong NP-hardness in (12e) is the standard
3-PARTITION reduction to bin packing; the new content is only its exact
identification with heterogeneous whole-row cone grouping.  The search
also found no explicit statement of the certificate (35a)--(35d), the
exact coupled product law (38a), or the use of the two classical barriers
in this joint factor/face/parameter frontier.  The recession-certificate
theorem and its direct-product use are published techniques: Theorem 3.9
of Fawzi--Saunderson states the Nesterov bound, and placing its data in
separate direct summands gives (38a) immediately.  The spectral-norm-cone
literature supplies the factorwise upper bounds; sparse PSD-completion
barriers concern a different completion cone and do not improve this
fixed ambient product.  Thus (38a) is an exact derived corollary with low
standalone novelty.  The plausible contribution is its use in the joint
factor/face/parameter frontier and the fixed-product-versus-projected-cone
distinction, not a new barrier or lower-bound method.  Priority remains
subject to specialist review.

The main open problem is now sharply delimited: determine whether a general
globally \(C^1\), split-row factorization under \((d,f)\) caps can beat the
coordinatewise shared-perspective count (24), or strengthen the local
packing theorem so that (24) is optimal up to its unavoidable single-ball
topological increment.  A second question is whether other face-efficient
sharing cones can achieve a smaller barrier parameter than the exact
\(q+1\) cost forced in both natural sharp models here.

## Audit checklist (completed)

The independent audit checked:

1. ordinary functional rank and the contact-cylinder linear recovery in
   (3);
2. the dual and every exposed face dimension of \(\mathcal H_{q,s}\), and
   the heterogeneous formulas and grouping reduction (12a)--(12f);
3. the exact integer caps in (13)--(14), including a smaller last group;
4. properness, dual characterization, and maximum face dimension of
   \(\mathcal P_q\);
5. minimality of \(\mathcal P_q\) for the scalar kernel family;
6. the sphere restriction and full-slack identity (23);
7. both PSD rank/nullity calculations; and
8. the intrinsic, affine-slice, and ambient barrier claims (29)--(39),
   including the projective derivative criterion, Legendre dual, and
   parameter-sharp recession certificate.

## Independent hostile audit

The audit rederived the \(1+qs\) row-function span and the
\(1+(q-1)s\) contact-cylinder face span.  It checked the dual of
\(\mathcal H_{q,s}\), including every nonzero boundary-support pattern,
and confirmed the exact maximum face dimension \(1+(q-1)s\), the integer
caps in (13), and the smaller last group.  For heterogeneous dimensions it
also checked the support-\(J\) face dimension
\(1+\sum_{a\notin J}s_a\), its maximum
\(1+\sum_as_a-\min_as_a\), the matching functional/contact lower bounds,
the exact partition constraints (12e), and the bin-packing/3-PARTITION
reduction when \(f=d-1\).

For \(\mathcal P_q\), the audit verified convexity, closedness, pointedness,
full dimension, the dual formula (20), and both kinds of dual boundary:
equality in (20) gives face dimension \(1+2(q-|J|)\), while strict
inequality can expose only a recession-orthant face of dimension at most
\(q-|J|\).  Thus the maximum is exactly \(2q-1\), including the case
\(q=1\).  The scalar functional-span and contact-cylinder arguments prove
the claimed simultaneous dimension and face minimality.  The sphere
identity (23), the smaller final source group, and both PSD rank/nullity
computations also check.  No mathematical correction was required.

The barrier extension was separately hostile-audited from the derivative
identities rather than by analogy.  On the section \(t=1\), differentiating
each vector-ball quadratic gives exactly (33), and the quantities in (32)
are nonnegative with product (34).  Hildebrand's auxiliary inequality is
quantified over arbitrary nonnegative scalar pairs, so substituting one
pair per vector block is valid; the positive product for every nonzero
direction also supplies the strict projective-Hessian condition.  The
conic/projective equivalence therefore proves ordinary self-concordance of
(30).  Its logarithmic sign is correct:

\[
 -\sum_a\log\!\left(\lambda^2
   (t^2-\|y_a\|^2)\right)+(q-1)\log(\lambda t)
 =F_{\mathcal H}(t,y)-(q+1)\log\lambda .
\]

For \(\mathcal P_q\), the arrow-matrix map is injective and its PSD
condition is exactly (20).  Maximizing
\(\log\det M-\langle(t,u,w),(\alpha,\beta,\gamma)\rangle\)
first in the Schur complement, then in \(\beta_a\), and then in
\(\gamma_a\), gives

\[
 -\sum_a\log(tw_a-u_a^2)+(q-1)\log t
\]

up to an additive constant, so (37) has the correct normalization and
sign.  The fixed-direction section (35) and the \(u=0\) section of
\(\mathcal P_q\) give respectively the sharp
\(\ell_\infty\)-epigraph and orthant lower bounds.  For the stronger product
claim, the later certificate audit checked that (35c) is exactly zero,
that every individual subtraction in (35b) is on the boundary, and that
the value (35d) tends to \(q+1\).  Direct-sum tensorization therefore proves
(38a) even for coupled barriers; blockwise optimality by itself would not
have sufficed.  The fixed-scale cube restriction in (38b) and the orthant
product section for (39) were also checked.  Direct
numerical derivative checks for \(1\le q\le6\) were consistent with
\(|D^3F[h,h,h]|\le2(D^2F[h,h])^{3/2}\); these checks are supplementary,
not part of the proof.

The final reduced-oracle and iteration corollary was checked against the
separately audited bounded-move theorem.  Equation (38c) is exactly its
\(h=1\), \(L=k\), analytic-center specialization, and (38d) follows from
\(2r/(1-r^2)=\tau\).  The audit confirmed that all reduced derivative and
KKT maps are identical after fixing the shared scales, and that the stated
scope excludes unbounded moves and unrestricted query/runtime lower bounds.
