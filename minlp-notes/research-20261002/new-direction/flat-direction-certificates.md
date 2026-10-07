# Flat optimal directions and diagonal convexification certificates

Date: 2026-10-02. Status: a checked limitation of bounded diagonal shifts,
an explicit way to escape that limitation on the same example, and a
standard-style exact certificate as a positive control. This does not
prove the general unknown-growth FPT theorem for arbitrary optimal sets.
No external search or priority claim is made.

The [proximal exact-recovery theorem](proximal-exact-recovery.md) recovers
an optimizer from a sufficiently accurate point under a supplied valid
growth bound. Its remaining obstacle is an independently valid global
value certificate. Keeping positive-semidefinite quadratic terms exact can
help, but diagonal convexification must also preserve cancellation along
flat optimal directions.

## 1. The certificate model

Write \(F(x)=x^THx/2+b^Tx+c\). Choose a nonnegative diagonal matrix
\(D\) for which \(H+D\succeq0\), keep
\(F(x)+x^TDx/2\) as an exact convex quadratic, and replace each
\(-D_{ii}x_i^2/2\) by its endpoint chord on the selected cell interval
\([\ell_i,u_i]\). The resulting convex lower model \(q_B\) satisfies

\[
 F(x)-q_B(x)
 =\tfrac12\sum_iD_{ii}(x_i-\ell_i)(u_i-x_i)
 \quad(x\in B).
 \tag{1}
\]

This description allows exact global minimization of the convex model
over each cell. A weaker relaxation obtained by splitting its PSD part
among bags cannot remove a gap already present in this stronger model.
The bounds below concern certificates taking the minimum of cell lower
bounds over a covering partition.

## 2. A well-conditioned example with all diagonal entries positive

On \([-1,1]^2\times[0,1]\), consider

\[
 F(x_1,x_2,y)=(x_1-x_2)^2+y(4+x_1+x_2)+y^2.
 \tag{2}
\]

Its optimum is zero, and

\[
 S=\{(t,t,0):-1\le t\le1\},\qquad
 \operatorname{dist}(x,S)^2=(x_1-x_2)^2/2+y^2.
\]

Indeed,

\[
 F(x)-2\operatorname{dist}(x,S)^2
 =y(4+x_1+x_2-y)\ge0.
 \tag{3}
\]

The Hessian is

\[
 H=\begin{pmatrix}2&-2&1\\-2&2&1\\1&1&2\end{pmatrix}.
 \tag{4}
\]

Thus all coordinate curvatures are \(L=2\), growth holds with \(g=2\),
and \(\kappa=1\). The interaction graph is a triangle, so one bag of
size three suffices. The Hessian is indefinite: on the span of
\((1,1,0)/\sqrt2\) and \((0,0,1)\), its matrix is
\(\begin{pmatrix}0&\sqrt2\\\sqrt2&2\end{pmatrix}\).
The nonpositive-diagonal endpoint reduction does not apply to a coordinate
of (2).

## 3. Bounded shifts force refinement along a flat direction

Let \(D=\operatorname{diag}(d_1,d_2,d_3)\ge0\) and assume
\(H+D\succeq0\). Restricting its quadratic form to vectors \((t,t,s)\)
gives the necessary condition

\[
 (d_1+d_2)(2+d_3)\ge4.
 \tag{5}
\]

If \(d_3\le B\), at least one of the two flat-coordinate shifts is
at least \(2/(2+B)\). For a common fixed shift and a product interval
grid, choose any interval of that coordinate of width \(\Delta\), set
both flat coordinates to its midpoint, and set \(y=0\). The point lies
in \(S\), and (1) gives a cell lower bound at most
\(-d_i\Delta^2/8\). Since the exact incumbent is zero, a gap at most
\(\varepsilon\) requires

\[
 \Delta\le2\sqrt{(2+B)\varepsilon}.
 \tag{6}
\]

At least \(\lceil1/\sqrt{(2+B)\varepsilon}\rceil\) intervals are
therefore needed across that flat coordinate's domain \([-1,1]\).

There is also a direct cell-count version when shifts vary by cell but
all satisfy \(d_3\le B\). Let a cell intersect the optimal segment in
an interval of parameter length \(\delta\). Its midpoint has both
flat-coordinate chord products at least \(\delta^2/4\), so (1) and (5)
give

\[
 \min_B q_B\le-\frac{\delta^2}{2(2+B)}.
\]

Every cell in an \(\varepsilon\)-certificate must therefore have
\(\delta\le\sqrt{2(2+B)\varepsilon}\). Covering the optimal segment
requires at least \(\sqrt2/\sqrt{(2+B)\varepsilon}\) cells. This
argument concerns the minimum of the cell bounds; it does not exclude
combining overlapping models by stronger operations.

The restriction on shift size is essential. These are not lower bounds
for optimization, arbitrary convexification, or all certificates.

## 4. Unbounded, cell-dependent shifts escape the example

For a slab \(y\in[a,a+w]\), \(0<w\le1\), keep the two flat intervals
equal to \([-1,1]\), and use

\[
 D(w)=\operatorname{diag}(w,w,2/w-2).
 \tag{7}
\]

This is a nonnegative shift, and \(H+D(w)\) is PSD. For a vector
\((u_1,u_2,v)\), its quadratic form is

\[
 (2+w/2)(u_1-u_2)^2
       +(w/2)(u_1+u_2+2v/w)^2.
 \tag{8}
\]

The total chord error on the slab is at most

\[
 w+\tfrac18(2/w-2)w^2\le5w/4.
 \tag{9}
\]

Since (2) satisfies \(F\ge2y\), its convex lower model has value at least
\(2a-5w/4\). For \(0<\varepsilon\le1\), choose a dyadic first width
\(w_0\le4\varepsilon/5\),
within a factor of two of that threshold. The first slab \([0,w_0]\)
has lower bound at least \(-\varepsilon\). Subsequent doubling slabs
\([a,2a]\) use \(w=a\) and have lower bound at least \(3a/4\).
Clip the last slab at one; its width is no larger than its lower endpoint,
so the same nonnegative bound applies.

There are only \(O(1+\log(1/\varepsilon))\) slabs, with no refinement
along either flat coordinate. The largest shift is \(O(1/\varepsilon)\),
but its rational encoding length is only \(O(1+\log(1/\varepsilon))\).
Consequently a norm bound on convexification shifts cannot be imposed
without losing a potentially useful mechanism.

This example also has simpler certificates. Its derivative in \(y\) is
at least two throughout the box, so monotonicity fixes \(y=0\). Equally,

\[
 F=(x_1-x_2)^2+y^2+2y+y(x_1+1)+y(x_2+1)
 \tag{10}
\]

is an exact sum of terms nonnegative on the box. Thus (2) is a diagnostic
for the certificate representation, not a difficult optimization instance.
Aspect-ratio-dependent shifts and products of boundary slacks are possible
ways to preserve flat directions; no general FPT count for either is
proved here.

## 5. A standard diagonal certificate as a positive control

For a rational continuous-box KKT point \(s\), define

\[
 d_i=\begin{cases}
 0,&\ell_i<s_i<u_i,\\
 2\partial_iF(s)/(u_i-\ell_i),&s_i=\ell_i,\\
 -2\partial_iF(s)/(u_i-\ell_i),&s_i=u_i.
 \end{cases}
 \tag{11}
\]

Fixed coordinates have been substituted out. KKT signs make \(d_i\ge0\).
If \(H+D\succeq0\), then the exact identity

\[
 F(x)-F(s)=\tfrac12(x-s)^T(H+D)(x-s)
       +\tfrac12\sum_i d_i(x_i-\ell_i)(u_i-x_i)
 \tag{12}
\]

certifies global optimality. All quantities are rational, and rational
PSD testing suffices; no growth constant is trusted. This is a diagonal
Lagrangian certificate, not a new general exactness principle. The shift
in (11) is maximal among nonnegative diagonal shifts leaving nonnegative
residual boundary slopes. If any such smaller shift makes the Hessian PSD,
(11) does too.

If this certificate holds at one optimum \(s\), the same \(D\) is the
maximal shift at every optimum \(t\). In (12), every nonnegative term
must vanish. Hence \((H+D)(t-s)=0\), and coordinates with \(d_i>0\)
are endpoints at \(t\). Also
\(\nabla F(t)=\nabla F(s)-D(t-s)\), giving exactly (11) at \(t\).
An exact-recovery routine need not select a particular component to pass
this verifier on the certified class. This observation does not establish
its completeness for arbitrary QPs.

As a positive example with all Hessian diagonals positive, take

\[
 F(x,y,t)=(x-y+t/2)^2+\tfrac18t(1-t),\qquad (x,y,t)\in[0,1]^3.
\]

Its optimum set consists of the two segments
\(\{(v,v,0):0\le v\le1\}\) and
\(\{(v,v+1/2,1):0\le v\le1/2\}\). Its Hessian is indefinite with
diagonal \((2,2,1/4)\), but (11) gives
\(D=\operatorname{diag}(0,0,1/4)\) at every optimum, and
\(H+D=2(1,-1,1/2)(1,-1,1/2)^T\). Writing \(r=x-y+t/2\), projection
to the lower endpoint segment when \(t\le1/2\) gives squared distance
at most \(r^2+5t^2/4\). For \(t\ge1/2\), the upper segment gives
at most \(2r^2+3(1-t)^2/2\). These inequalities imply
\(\operatorname{dist}(x,S)^2\le12F(x)\), so
\(L=2\), \(g=1/12\), and \(\kappa=24\) suffice.

Certificate (12) fails at every optimizer of (2): the two flat-coordinate
gradients vanish, so their
shifts are zero, contradicting (5). The box-product certificate (10)
handles precisely the cross terms that this diagonal certificate misses.

## 6. A local spectral bound on a maximal optimal box face

There is one useful connection between growth, width, and exact PSD
patches. It concerns an ordinary rational mixed-box quadratic with growth
\(F-f^*\ge g\operatorname{dist}(x,S)^2\); no mode-dependent collection
of different quadratics is included in this statement.

Fix an integer assignment occurring at a global optimizer. Among faces
of its continuous box whose relative interiors contain a global optimizer,
choose a face \(G\) maximal by inclusion. This means a face containing
an optimizer in its relative interior, **not** a face wholly contained in
\(S\). Choose \(s\in S\cap\operatorname{relint}G\), let \(J\) be
the coordinates free in \(G\), and put \(A=H_{JJ}\).

**Lemma.** The free Hessian is PSD, and

\[
 2g\,P_{(\ker A)^\perp}\preceq A
       \preceq p\operatorname{diag}(A)\preceq pL I.
 \tag{13}
\]

Here \(P_{(\ker A)^\perp}\) is the orthogonal projector onto the
nonzero-curvature directions, \(L\) bounds the original summed diagonal
curvature, and the interaction graph has a supplied decomposition with
bag size at most \(p\). Thus, if a positive eigenvalue exists, the ratio
of largest to smallest positive eigenvalues is at most
\(pL/(2g)\le p\kappa/2\). Null directions incur no curvature error.

*Proof.* Free first-order and second-order optimality at \(s\) give
\(\nabla_JF(s)=0\) and \(A\succeq0\). In a sufficiently small
neighborhood of \(s\), every coordinate in \(J\) remains strictly
between its original bounds. A nearby point therefore belongs to the
relative interior of \(G\) or a strict superface. A nearby optimizer in
a strict superface would contradict the choice of \(G\). Other integer
assignments are at Euclidean distance at least one and can be excluded by
taking a smaller neighborhood. Consequently every nearby optimizer lies
in the same face and integer slice.

Two stationary points in \(G\) differ by a vector in \(\ker A\).
Conversely, every sufficiently small displacement from \(s\) in that
kernel remains feasible and keeps the objective equal to \(f^*\), by
the exact quadratic expansion. Thus locally the optimal set is precisely
the affine space \(s+\ker A\), with the other coordinates fixed.
For a free direction \(v\) and sufficiently small \(t\), its nearest
optimizer also lies in this neighborhood, and

\[
 F(s+tv)-f^*=\tfrac12t^2v^TAv,\qquad
 \operatorname{dist}(s+tv,S)^2
       =t^2\|P_{(\ker A)^\perp}v\|^2.
\]

Applying growth proves the first inequality in (13).

For the upper bound, the induced interaction graph has a proper coloring
with at most \(p\) colors. Write \(v=\sum_c v_c\), with each \(v_c\)
supported on one color class. Positive semidefiniteness gives

\[
 v^TAv=\left\|\sum_c A^{1/2}v_c\right\|^2
 \le p\sum_c v_c^TAv_c
 =p\sum_i A_{ii}v_i^2.
\]

The equality on the right uses the absence of edges within each color
class. Therefore \(A\preceq p\operatorname{diag}(A)\), and the
diagonal upper bound finishes (13). The matrix square root is only a
proof device; no irrational computation is needed. \(\square\)

Maximality is essential even for a convex quadratic. Let
\(F=(\eta x-z_1+z_2)^2\) on
\([-1,1]\times[0,1]^2\), with \(0<\eta<1\). Keeping \(x\) fixed,
one can adjust \(z_1-z_2\) to \(\eta x\) by a feasible move of length
at most \(|\eta x-z_1+z_2|\): distribute the required change between
increasing one coordinate and decreasing the other. The available total
slack suffices because the target difference lies in \([-1,1]\).
Hence \(F\ge\operatorname{dist}(x,S)^2\), so \(g=1\) and \(L=2\)
are valid. The face \(z_1=z_2=0\) contains the optimizer \(x=0\) in
its relative interior, but its free Hessian is only \(2\eta^2\).
The face is not maximal: the full box has interior optimizers. A face
obtained by snapping a nearby point can therefore require further
maximalization before (13) applies.

This lemma supports keeping the free-face PSD energy and its kernel exact:
the nonzero local curvature has conditioning controlled by \(p\) and
\(\kappa\), without a coordinate-projection count or an added shift-norm
parameter. It is an analysis statement about a suitable optimal face;
it neither identifies that face nor certifies its global optimality.

Maximality cannot be dropped. As the
[independent review](flat-face-spectral-review.md) shows,
`F=(eps*x-z1+z2)^2` on `[-1,1] times [0,1]^2` has valid `g=1`,
`L=2`, and `kappa=2` for every `0<eps<1`. The nonmaximal face
`z1=z2=0` contains an optimizer in its relative interior but has free
Hessian `[2eps^2]`. Its positive eigenvalue tends to zero at fixed
conditioning. A face returned by snapping a nearby point is therefore
not automatically a face to which (13) applies.

The missing global step is a bound on how many such patches, and how much
separator information, suffice to cover the original problem. A bag has
only \(3^p\) continuous endpoint/interior status patterns, but that pattern
does not determine a subtree's stationary equations, Schur complement,
linear term, or conditional value function. Different active choices in
the subtree can produce different separator data while the bag's status
pattern stays unchanged. Global growth toward \(S\) does not itself give
a conditional-growth or representation bound for all those subproblems.

Accordingly, the current route supplies a controlled local PSD component
and independently checkable special-class certificates. To obtain the
general unknown-growth FPT certificate, it still needs a construction
showing that globally sufficient separator potentials and boundary-product
patches have bounded representation size and can be found within the
claimed parameters. Counting local active signatures alone does not
supply that construction.

## Verification record

An independent reviewer checked (2)--(6), including the exact growth
constant and the fixed-shift interval count. It also checked (11)--(12)
and the positive example's optimal segments and growth bound. The
cell-dependent count and explicit slab escape are direct derivations
given above. An inline `python3 - <<'PY'` command using exact fractions
passed 125 growth checks, 56 PSD principal-minor checks, 216 shifted-square
identities, 2,625 slab-model inequalities, and 125 checks of the positive
example's distance bound. These are targeted formula checks, not a solver
implementation or a performance claim.

The separate [spectral review](flat-face-spectral-review.md) checks
Section 6's maximal-face argument, mixed slices, positive and zero spectra,
coloring proof, and counterexample when maximality is omitted.

The commands `git diff --check -- research-20261002/new-direction/flat-direction-certificates.md`
and a second inline Python check of whitespace, math delimiters, and the
local link passed. No external search, knowledge-base access, project-wide
verification, or CI inspection was performed.

The spectral lemma in Section 6 was subsequently added with a direct
proof. A fresh independent reviewer confirmed its maximal-face definition,
local-optimal-set argument, fixed-integer-slice qualification, and spectral
bounds, and supplied the coloring proof of the upper bound. It does not
rely on the sampled formula checks above, and no new global certificate
theorem is asserted.
