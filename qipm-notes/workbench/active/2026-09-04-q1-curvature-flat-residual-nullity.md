# Curvature-flat squared ball slacks still require one nullity per source

Status: Proved; independently hostile-audited throughout  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the stated factorization and barrier scopes

## General orientation-residual theorem

Fix \(s\geq3\), \(b\geq1\).  If \(b\geq2\), choose a PSD order cap
satisfying

\[
                  (\bar R+3)(b-1)<2bs,                   \tag{0}
\]

and for \(b=1\) allow any finite cap.  Put

\[
                         M=(S^{s-1})^b.
\]

For every source \(a\in[b]\), let
\(\tau_a:S^{s-1}\to S^{s-1}\) be topologically conjugate to the antipodal
map and let \(F_a:S^{s-1}\times S^{s-1}\to\mathbb R_+\) be continuous with

\[
                       F_a(u,u)=0,\qquad
                       F_a(u,\tau_a(u))>0.                 \tag{1}
\]

Suppose the labelled cylindrical kernels \(F_a(x_a,v)\) have a finite
real-PSD factorization

\[
 F_a(x_a,v)=\sum_{i=1}^L
       \operatorname {tr}\bigl(A_i(x)B_i^a(v)\bigr),
 \qquad
 A_i(x),B_i^a(v)\in\mathbb S_+^{r_i},\quad r_i\leq\bar R. \tag{2}
\]

Continuity suffices.  At a simultaneous diagonal contact define

\[
                         Z(x)=\sum_i\operatorname {nullity}A_i(x).
                                                                    \tag{3}
\]

Then

\[
                         \boxed{\max_{x\in M}Z(x)\geq b.} \tag{4}
\]

Thus even curvature-flat residuals cannot share fewer than one primal
kernel dimension per source if each residual distinguishes the two sheets
of a projective phase cover.  The uniform-in-\(b\) sufficient cap
\(\bar R\leq2s-3\) follows from (0), but finite \(b\) permits larger
blocks: for example, \(b=2\) permits \(\bar R\leq4s-4\).  The result uses
orientation double-cover monodromy, not a nonzero contact Hessian.

The principal application is the squared ball residual

\[
 K_a(x,v)={1\over2}(1-x_a^Tv)^2,
 \qquad x\in M,\quad v\in S^{s-1}.
\]

with \(\tau_a(u)=-u\).  It has identically zero mixed contact curvature,
but still obeys (4).  The sole \(q=1\) application has
\(\bar R=s\), which satisfies the theorem's cap.

If the selected factors in (2) belong to the closure of a strictly
feasible affine slice, the determinant vanishing-order lemma gives

\[
                         \nu_{\rm std,slice}\geq b.        \tag{5}
\]

This solves the residual subproblem that arose in the formerly unresolved
\(q=1,\ s=R\) product-ball case.  In particular, any factorization that
splits off the canonical saturated projective term

\[
 {1\over2}\bigl(1-(x_a^Tv)^2\bigr)
   =\operatorname {tr}\!\left[(I-x_ax_a^T){vv^T\over2}\right]          \tag{6}
\]

in a separate order-\(s\) block for every source has a simultaneous
contact at which total boundary nullity is at least \(2b\), because (6)
spends \(b\) nullities at every contact and its nonnegative remainder is
exactly \(K_a\).

By itself, this residual theorem does **not** close the unrestricted
\(q=1\) full-slack problem: a factorization need not split into the
canonical terms (6) plus an independently PSD-factorized residual.  The
later, independently audited
[all-field sequential contact-range
theorem](2026-09-04-hermitian-sequential-contact-range-frontier.md) closes
that problem without assuming a positive splitting.  It gives the exact
real standard-slice value \(2b\) for \((B_2^R)^b\), \(R\geq3\), even when
saturated rows or factor labels switch across the contact manifold.

## 1. A fixed-space consequence of too little nullity

Assume for contradiction that

\[
                              Z(x)\leq b-1
                              \qquad(x\in M).              \tag{7}
\]

Place all blocks in the fixed orthogonal direct sum

\[
                   {\cal H}=\bigoplus_{i=1}^L\mathbb R^{r_i},
\]

and write \(A(x)=\bigoplus_iA_i(x)\) and
\(B^a(v)=\bigoplus_iB_i^a(v)\).  Diagonal contact and nonnegativity give

\[
                 A(x)B^a(x_a)=0,\qquad
                 \operatorname {Ran}B^a(x_a)
                         \subseteq\ker A(x).               \tag{8}
\]

For every \(a\) and \(v\), \(B^a(v)\ne0\).  Otherwise the whole column
\(F_a(x_a,v)\) would vanish, whereas its value at
\(x_a=\tau_a^{-1}(v)\) is positive by (1).

Define the nonempty vector sets

\[
 {\cal S}_a=\bigcup_{v\in S^{s-1}}
                  \bigl(\operatorname {Ran}B^a(v)\setminus\{0\}\bigr)
                  \subset{\cal H}.                        \tag{9}
\]

There is no linearly independent transversal
\(w_a\in{\cal S}_a\), \(a\in[b]\).  Indeed, choose \(v_a\) with
\(w_a\in\operatorname {Ran}B^a(v_a)\) and evaluate at
\(x=(v_1,\ldots,v_b)\).  Equation (8) puts all \(w_a\) in the
at-most-\((b-1)\)-dimensional space \(\ker A(x)\), contradicting their
independence.

The vector-matroid form of Rado's transversal theorem now supplies a
nonempty \(J\subseteq[b]\), with \(j=|J|\), such that

\[
 {\cal V}:=\operatorname {span}\bigcup_{a\in J}{\cal S}_a,
 \qquad m:=\dim{\cal V}\leq j-1.                          \tag{10}
\]

This use of Rado is valid for the infinite sets (9): replace each by a
finite basis of its span.  The usual finite vector-matroid theorem then
has exactly the rank condition in (10).

## 2. The PSD block cap makes the matrix span only linear in \(m\)

Let

\[
 {\cal V}_i=\operatorname {span}_{a\in J,\ v\in S^{s-1}}
                    \operatorname {Ran}B_i^a(v)
       \subseteq\mathbb R^{r_i},
 \qquad m_i=\dim{\cal V}_i.                               \tag{11}
\]

Because every \(B^a(v)\) is block diagonal, its range contains each of its
block-supported range vectors.  Hence

\[
                     {\cal V}=\bigoplus_i{\cal V}_i,
                     \qquad \sum_i m_i=m.                 \tag{12}
\]

Every \(B_i^a(v)\), \(a\in J\), is a symmetric matrix supported on
\({\cal V}_i\).  Therefore all dual columns for the rows in \(J\) lie in
the fixed vector space

\[
                {\cal W}=\bigoplus_i\operatorname {Sym}({\cal V}_i),
\]

whose dimension satisfies

\[
\begin{aligned}
 \dim{\cal W}
   &=\sum_i{m_i(m_i+1)\over2}\\
   &\leq {\bar R+1\over2}\sum_i m_i
    ={\bar R+1\over2}m
    \leq {\bar R+1\over2}(j-1).                          \tag{13}
\end{aligned}
\]

The order cap is decisive in the second line:
\(m_i\leq r_i\leq\bar R\).
Using the unrestricted space \(\operatorname {Sym}({\cal V})\) instead
would lose the block-diagonal structure and give a useless quadratic
bound.

Pairing a fixed matrix space with the primal maps cannot increase linear
dimension.  Consequently (2) and (13) imply

\[
 \dim\operatorname {span}
   \{F_a(x_a,v):a\in J,\ v\in S^{s-1}\}
       \leq {\bar R+1\over2}(j-1).                        \tag{14}
\]

## 3. Orientation monodromy gives enough ordinary rank

Let \(\rho_a\) be the ordinary column rank of \(F_a\).  Choose a basis of
its column space and write the coefficient map as

\[
 F_a(u,v)=\sum_{\ell=1}^{\rho_a}f_{a\ell}(u)c_{a\ell}(v),
 \qquad c_a:S^{s-1}\to\mathbb R^{\rho_a}.                 \tag{15}
\]

The coefficients can be chosen continuously: select
\(\rho_a\) evaluation points at which the basis evaluation matrix is
invertible and recover \(c_a(v)\) from those column values.
Equation (1) implies

\[
                             c_a(v)\ne c_a(\tau_a(v)).
\]

Otherwise the two columns would agree, but evaluation at \(u=v\) gives
\(F_a(v,v)=0<F_a(v,\tau_a(v))\).  Conjugate \(\tau_a\) to the antipodal
map.  Borsuk--Ulam says that every continuous
\(S^{s-1}\to\mathbb R^{s-1}\) has an antipodal collision.  Padding the
codomain if necessary therefore gives

\[
                              \rho_a\geq s.                \tag{16}
\]

For different product coordinates, any relation
\(\sum_{a\in J}f_a(x_a)=0\) makes each \(f_a\) constant by varying one
coordinate at a time.  Hence the coordinate column spaces are independent
modulo a relation space of dimension at most \(j-1\), and

\[
 \dim\operatorname {span}
   \{F_a(x_a,v):a\in J,\ v\in S^{s-1}\}
       \geq\sum_{a\in J}\rho_a-(j-1)
       \geq1+j(s-1).                                      \tag{17}
\]

For \(b\geq2\), this contradicts (14), since for every \(1\leq j\leq b\)

\[
 2[1+j(s-1)]-(\bar R+1)(j-1)
   =\bar R+3+j(2s-\bar R-3)>0                             \tag{18}
\]

under (0).  Indeed, the right side is increasing in \(j\) when
\(\bar R\leq2s-3\); otherwise its minimum is at \(j=b\), where positivity
is exactly (0).  For \(b=1\), the nonzero matrix \(B^1(u)\) lies in
\(\ker A(u)\) at every contact, proving (4) without a cap.  This proves the
general nullity theorem.

## 4. Exact ordinary rank of the squared residual

For one source, the column functions are

\[
 K_v(u)={1\over2}-u^Tv+{1\over2}u^T(vv^T)u.
\]

Their odd parts span all \(s\) linear coordinate functions.  Their even
parts span all homogeneous quadratic forms restricted to the sphere:
the matrices \(I+vv^T\), \(v\in S^{s-1}\), span
\(\operatorname {Sym}_s\).  Indeed, a symmetric matrix \(C\) orthogonal
to all of them would satisfy

\[
                    \operatorname {tr}C+v^TCv=0
                    \quad\hbox{for every unit }v,
\]

which first makes \(C\) scalar and then zero.  Linear and quadratic
restrictions have opposite parity and are independent.  Thus the exact
ordinary column rank of (1) for one source is

\[
                           \rho={s(s+3)\over2}.             \tag{19}
\]

The constant function belongs to this column span, because spherical
averaging over \(v\) gives a positive constant.  Column spaces belonging
to different product coordinates are independent modulo the constants.
Indeed, if
\(\sum_{a\in J}f_a(x_a)=0\) on the product, fix every coordinate except
\(x_c\) and vary \(x_c\); then \(f_c\) is constant.  Applying this to every
\(c\) shows that every relation in the quotient by constants is trivial.
Therefore, for the squared kernels,

\[
 \dim\operatorname {span}
   \{K_a(\,\cdot\,,v):a\in J,\ v\in S^{s-1}\}
       =1+j(\rho-1).                                      \tag{20}
\]

There is also an unconditional factor-count corollary.  Taking \(J=[b]\)
in (16), the ordinary rank of the full labelled residual kernel is

\[
 D_{\rm res}=1+b\left({s(s+3)\over2}-1\right).
                                                                    \tag{21}
\]

Every order-\(r_i\) PSD factor contributes at most
\(r_i(r_i+1)/2\) to ordinary rank.  Hence

\[
 \sum_i{r_i(r_i+1)\over2}\geq D_{\rm res}.                \tag{22}
\]

Specializing back to the order-\(s\) cap and writing
\(d_s=s(s+1)/2\) gives

\[
 L_{\rm res}\geq
   \left\lceil{D_{\rm res}\over d_s}\right\rceil
   =b+\left\lceil{b(s-1)+1\over d_s}\right\rceil>b.       \tag{23}
\]

Thus the canonical strategy consisting of \(b\) separate projective
blocks (6) and a separately factorized residual needs at least \(2b+1\)
capped PSD factors.  This is strictly more than the \(2b\) factors in the
grouped Schur construction for the unsplit full slack.

## 5. What this adds to the \(q=1\) frontier

The identity

\[
 1-u^Tv={1\over2}\bigl(1-(u^Tv)^2\bigr)
             +{1\over2}(1-u^Tv)^2                        \tag{24}
\]

shows that a saturated \(\mathbb {RP}^{s-1}\) phase channel can carry the
entire second-order contact metric while leaving a nonnegative
curvature-flat correction.  Theorem (4) shows that this particular
correction is nevertheless globally expensive: under the same order cap,
it needs one exposed primal kernel dimension per source somewhere.

The remaining unrestricted problem is an extraction problem, not a
residual lower-bound problem.  One would have to prove that any global
projective phase component forced by failure of the relative-top-class
argument can be normalized or isolated so that its complementary
nonnegative slack inherits a column-span obstruction of the form above.
Current contact-curvature identities alone do not make individual PSD
summands independent of the other primal source coordinates, so such an
extraction cannot be assumed.

## 6. Global row saturation closes \(q=1\)

The orientation theorem gives a quantitative \(q=1\) lower bound under a
natural partial saturation condition, with no separate cylindricity
assumption.  Consider a global
\(C^1\) factorization of the full product-ball slacks with order cap
\(s=R\).  Use the private dimensions \(D_d(x)\) from the divisible-cap
companion.  Let \(J\subseteq[b]\), \(j=|J|\), and suppose

\[
                         D_d(x)=1
             \qquad\text{for every }d\in J,\ x\in M.      \tag{25}
\]

Then

\[
                       \boxed{\nu_{\rm std,slice}\geq b+j.}             \tag{26}
\]

In particular, if every row is globally saturated, then
\(\nu_{\rm std,slice}\geq2b\).  The grouped Schur lift attains \(2b\), so
the all-row case is exact.

To prove it, fix \(d\in J\).  Equality in its rank--private-dimension chain
gives exactly one active order-\(s\), primal-nullity-one label at every
contact.  The exact-active-label sets form a clopen partition of the
connected manifold \(M\), so one label \(i_d\) persists globally.  Write

\[
 Y_{i_d}^d(u)=\lambda_d(u)q_d(u)q_d(u)^T,\qquad
 \ker X_{i_d}(x)=\mathbb Rq_d(x_d),                       \tag{27}
\]

locally choosing a unit representative \(q_d\), with \(\lambda_d>0\).
The full mixed-curvature identity is

\[
 \langle h,k\rangle
   =2\lambda_d(u)
      \left\langle dq_d(u)k,\,
        X_{i_d}(x)\,dq_d(u)h\right\rangle                 \tag{28}
\]

for \(h,k\in T_uS^{s-1}\).  Hence \(dq_d\) is an isomorphism onto
\(q_d(u)^\perp\), and (28) uniquely determines
\(X_{i_d}(x)|_{q_d(u)^\perp}\) from \(u\).  Together with
\(X_{i_d}(x)q_d(u)=0\), this determines the whole symmetric matrix.
Therefore \(X_{i_d}(x)\) depends only on \(x_d\): cylindricity is forced by
global saturation.  The projective phase

\[
 L_d(u)=[q_d(u)]:S^{s-1}\longrightarrow\mathbb {RP}^{s-1}
\]

is a local diffeomorphism, hence the universal double cover.

The labels \(i_d\) are distinct and have no cross-row dual terms.  Indeed,
for \(e\ne d\), diagonal complementarity requires

\[
 \operatorname {Ran}Y_{i_e}^d(x_d)
       \subseteq L_e(x_e)
\]

for every independently variable \(x_e\).  Surjectivity of \(L_e\) makes
the intersection of these lines zero, so \(Y_{i_e}^d\equiv0\).  The same
independent-variable argument prevents one label from serving two
persistent phase covers.

Remove the \(j\) labels \(i_d\), \(d\in J\).  Positivity of every PSD
summand and the
cylindricity forced by (28) give labelled cylindrical residuals

\[
 F_d(u,v)=1-u^Tv-
   \operatorname {tr}\bigl(X_{i_d}(u)Y_{i_d}^d(v)\bigr)
   \geq0.                                                 \tag{29}
\]

Let \(\tau_d\) be the deck involution of \(L_d\); it is conjugate to the
antipodal map.  Equation (27) gives

\[
 F_d(u,u)=0,\qquad
 F_d(u,\tau_d(u))=1-u^T\tau_d(u)>0.                       \tag{30}
\]

For a row \(e\notin J\), all removed labels have zero cross-row dual terms,
so its remaining kernel is still the original full slack
\(1-x_e^Tv\).  This vanishes on the diagonal and is positive at the
antipode.  Thus all \(b\) remaining labelled kernels—orientation
residuals for \(d\in J\) and full slacks for \(e\notin J\)—satisfy the
general orientation theorem.  It gives a simultaneous contact at which
the remaining labels have total primal nullity at least \(b\).  The
persistent labels in (27) contribute another \(j\) at every contact,
proving (26).

Historically, this theorem isolated the only escape route left by the
residual method.  Each globally
saturated row costs one unit beyond the universal \(b\)-nullity floor.
Any \(\nu_{\rm std,slice}<2b\) factorization must have some row and some
contact with \(D_d(x)\geq2\); under the global upper assumption
\(Z(x)\leq2b-1\), at least one other row is saturated at each point.
Thus any putative counterexample to that intermediate method had to switch
which rows or labels carried the saturated projective channel.
Cross-coordinate variation of a globally persistent active spectrum was
not an escape, because (28) rules it out.  The canonical sequential
contact-range theorem cited above subsequently rules out switching as
well.

## Scope and novelty boundary

The general lower bound is a finite-dimensional factorization statement.
It uses only positivity, diagonal contact, the order cap, Rado's theorem,
and Borsuk--Ulam; it does not require differentiability.  The sharper
factor-count statement uses the exact ordinary rank of the squared kernel.
The barrier corollary additionally requires selected boundary factors in
the closure of a Slater affine slice.

A targeted search found the ingredients separately—ordinary-rank lower
bounds for PSD rank, Rado's independent-transversal theorem, classical
Borsuk--Ulam, and coincidence theorems for products of spheres—but did not
locate a PSD-factorization theorem combining them, the product residual
bound (4), or the extraction bound (26).  The precise results appear new,
subject to specialist review.  Relevant background includes
[general PSD-rank lower bounds](https://arxiv.org/abs/1407.4308),
[support-based PSD-rank bounds](https://arxiv.org/abs/1203.3961), and
[Borsuk--Ulam coincidence results for products of
spheres](https://doi.org/10.1016/j.topol.2015.12.063).

## Audit checklist

- Check the infinite-set reduction in the vector-matroid transversal step.
- Verify that \({\cal V}=\bigoplus_i{\cal V}_i\), rather than merely
  embedding into that direct sum.
- Verify the Borsuk--Ulam column-rank bound for every involution conjugate
  to antipodal.
- Recompute the exact squared-kernel column rank on the sphere, including
  the constant/quadratic relation.
- Verify that coordinate-column spaces intersect only in constants and
  hence have dimension \(1+j(\rho-1)\).
- Check the block-cap inequality in (13), arithmetic in (18), and the
  ordinary-rank factor-count corollary (21)--(23).
- Do not promote the canonical-split corollary itself to the unrestricted
  \(q=1\) theorem; that closure is supplied by the separate sequential
  contact-range theorem.
- Check the clopen persistence, curvature reconstruction, cross-row
  vanishing, and deck-separation arguments in (25)--(30).

## Independent hostile audits

Two independent hostile audits rederived the Rado step, including its
infinite-set reduction, and verified the exact block-direct-sum identity
\({\cal V}=\bigoplus_i{\cal V}_i\).  They checked that symmetry and range
support put every dual matrix in \(\operatorname {Sym}({\cal V}_i)\), so
the order cap makes the available matrix dimension linear in \(m\).

Both audits independently recomputed the one-source rank
\(s(s+3)/2\), the direct-sum-modulo-constants product rank, and the final
arithmetic.  One audit requested that the coordinate-independence argument
be written explicitly rather than inferred from pairwise intersections,
and that the canonical-split conclusion say “at some simultaneous
contact.”  Both repairs are incorporated above.  No mathematical gap
remained.

A third independent hostile audit checked the global-saturation extraction
in Section 6.  It rederived the factor two and cancellation of scale
derivatives in (28), verified that the invertible phase differential and
kernel equation determine the complete primal matrix, and checked
cross-row dual vanishing.  It also independently verified the deck-
involution Borsuk--Ulam bound, Rado/block-span step, and
quotient-by-constants arithmetic.  The audit found no gap and confirmed
that the hypothesis \(D_d\equiv1\) is not being inferred from a barrier
bound.  A follow-up audit checked the subset extension: after removing the
\(j\) persistent labels, the other \(b-j\) rows retain their full slacks,
so the residual theorem charges \(b\) remaining nullities without double
counting the \(j\) removed ones.  This confirms (26).
The same follow-up checked the finite-\(b\) cap extension (0): the affine
gap in (18) is minimized at \(j=b\) exactly when
\(\bar R>2s-3\), and its positivity there is precisely (0).

The same auditor checked the finite-\(b\) cap sharpening (0).  It verified
that the contradiction gap is affine in the deficient-set size \(j\), with
minimum \(2s\) at \(j=1\) for nonnegative slope and
\(2bs-(b-1)(\bar R+3)\) at \(j=b\) otherwise.  Hence (0) is exactly the
strict condition supplied by this proof; the \(b=1\) cap-free case and the
\(b=2\) threshold \(\bar R\leq4s-4\) also check.
