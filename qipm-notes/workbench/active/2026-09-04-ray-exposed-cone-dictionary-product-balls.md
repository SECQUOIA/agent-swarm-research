# A sharp full-product-ball frontier for ray-exposed cone dictionaries

Status: Proved; targeted literature screen completed; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the selected-factor theorem; novelty remains subject to specialist review

## Main result

Put

\[
 C=(B_2^s)^k,\qquad M=(S^{s-1})^k,\qquad p=s-1,
 \qquad s\geq3.
\]

Its full extreme slack consists of the rows

\[
 S_a(x,z)=1-\langle x_a,z\rangle,
 \qquad a\in[k],\quad x\in M,\quad z\in S^p.             \tag{1}
\]

For a proper cone \(K\subset\mathbb R^m\), introduce the following
one-sided face condition:

\[
 \tag{ER}
 0\ne b\in\partial K^*,\quad
 F_K(b):=K\cap b^\perp\ne\{0\}
 \quad\Longrightarrow\quad F_K(b)\text{ is a ray}.
\]

Equivalently, every nonzero exposed proper face of \(K\) is an extreme
ray.  A compact base of \(K\) being strictly convex is sufficient.  Requiring
the same property for \(K^*\), or requiring smooth strictly convex primal and
dual bases, is stronger than needed for the orientation of the factorization
used below.  In fact, the factor-relative weakening that (ER) hold only for
the nonzero dual values \(B_i^a(z)\) that occur at contact is enough.

Suppose (1) has globally labelled \(C^1\) factors

\[
 S_a(x,z)=\sum_{i=1}^L\langle A_i(x),B_i^a(z)\rangle,
 \qquad A_i:M\to K_i,\quad B_i^a:S^p\to K_i^*,           \tag{2}
\]

where every \(K_i\) is proper, satisfies (ER), and

\[
 3\leq m_i:=\dim K_i\leq d,
 \qquad r_i:=m_i-2,
 \qquad c:=d-2.                                           \tag{3}
\]

Then the following simultaneous lower bounds hold.

If \(c<p\),

\[
 \boxed{
  L\geq k\left\lceil\frac{s}{c}\right\rceil,
  \qquad \sum_i r_i\geq ks,
  \qquad \sum_i m_i\geq
       k\left(s+2\left\lceil\frac{s}{c}\right\rceil\right).
 }                                                         \tag{4}
\]

If \(c\geq p\),

\[
 \boxed{
  L\geq k,
  \qquad \sum_i r_i\geq kp,
  \qquad \sum_i m_i\geq k(p+2)=k(s+1).
 }                                                         \tag{5}
\]

These bounds are exact when the allowed dictionary contains the Lorentz
cones: grouped Lorentz factors attain (4), and one \(Q_{s+1}\) factor per
source ball attains (5).  Thus (4)--(5) are the exact resource frontier over
the class of all (ER) cones subject to the dimension cap, even though the
lower bound is not specific to Lorentz geometry.

There is a real discontinuity in the integer formula at \(c=p=s-1\).
The tempting expression \(L=k\lceil s/c\rceil\) would give \(2k\), but is
false there: one \(Q_{s+1}\) factor per ball gives \(L=k\).  A uniform way to
write the exact answer is

\[
 h(c)=\begin{cases}
      \lceil s/c\rceil,&c<p,\\
      1,&c\geq p,
     \end{cases}
 \qquad
 \tau(c)=\begin{cases}
      s,&c<p,\\
      p,&c\geq p,
     \end{cases}                                          \tag{6}
\]

and then

\[
 L_{\min}=kh(c),\qquad
 R_{\min}=k\tau(c),\qquad
 D_{\min}=k(\tau(c)+2h(c)).                               \tag{7}
\]

Finally, let \(F\) be any logarithmically homogeneous self-concordant
barrier on the full ambient product \(\prod_iK_i\), including a barrier that
couples different factors.  Its parameter satisfies

\[
                              \nu(F)\geq2L.                 \tag{8}
\]

Consequently the exact minimum ambient barrier parameters over the same
dictionary class are \(2k\lceil s/c\rceil\) in (4) and \(2k\) in (5),
attained by the standard Lorentz product barriers.  This is an ambient-cone
statement, not a lower bound on the parameter of an arbitrary barrier after
affine slicing.

## 1. The universal quotient-rank bound

At every contact point \(z=x_a\), nonnegativity of all terms and vanishing
of their sum imply

\[
                 \langle A_i(x),B_i^a(x_a)\rangle=0.       \tag{9}
\]

Define the block-\(a\) mixed channel

\[
 M_i^a(x)(u,v)
 =-\langle D_aA_i(x)[u],DB_i^a(x_a)[v]\rangle,
 \qquad u,v\in T_{x_a}S^p.                                \tag{10}
\]

Mixed differentiation of (2) uses only first derivatives of the factors
and gives

\[
                  \sum_iM_i^a(x)(u,v)=\langle u,v\rangle. \tag{11}
\]

A differentiable map from a manifold into a pointed cone has zero
derivative at every point mapped to the vertex: its derivatives in the two
opposite tangent directions lie in both \(K\) and \(-K\).  Hence a channel
with either contact factor at the vertex is zero.  If one contact factor is
interior, (9) puts the other at the vertex, so that case is also zero.

For a nonzero channel, write \(A=A_i(x)\ne0\) and
\(B=B_i^a(x_a)\ne0\).  The two fixed-variable nonnegative functions have a
minimum at contact, so

\[
 \langle D_aA_i[u],B\rangle=0,
 \qquad
 \langle A,DB_i^a[v]\rangle=0.                            \tag{12}
\]

Thus (10) descends to the bilinear pairing

\[
 \frac{B^\perp}{\mathbb RA}\ \times\
 \frac{A^\perp}{\mathbb RB}\longrightarrow\mathbb R.    \tag{13}
\]

Both quotient spaces have dimension \(m_i-2=r_i\).  Therefore

\[
                         \operatorname{rank}M_i^a\leq r_i.\tag{14}
\]

No smoothness, strict convexity, self-duality, or positive-semidefiniteness
of the individual mixed channel is used in (14).  In particular, unlike the
Lorentz Gram calculation, a general channel need not itself be symmetric or
positive semidefinite.

## 2. Pointwise no-sharing from exposed rays

Call label \(i\) active for source \(a\) at \(x\) when
\(M_i^a(x)\ne0\).  Suppose it is active.  Then both contact factors are
nonzero boundary points.  Fix \(x_a\), and vary all other primal blocks.
The entire resulting cylinder is a zero set of row \(a\).  Termwise
nonnegativity and (ER) give

\[
 A_i(y)\in F_{K_i}(B_i^a(x_a))
       =\mathbb R_+A_i(x)
 \quad\text{whenever }y_a=x_a.                            \tag{15}
\]

Because \(A_i(x)\ne0\), differentiating (15) in a different source
direction \(b\ne a\) makes \(D_bA_i(x)\) radial.  On the other hand, for
fixed \(x\), the nonnegative function
\(z\mapsto\langle A_i(x),B_i^b(z)\rangle\) vanishes at
\(z=x_b\), and hence

\[
                    \langle A_i(x),DB_i^b(x_b)[v]\rangle=0.
\]

It follows that

\[
 M_i^a(x)\ne0\quad\Longrightarrow\quad
 M_i^b(x)=0\quad(b\ne a).                                \tag{16}
\]

This is pointwise no-sharing.  A label may still switch which source it
serves across a vertex region; the proof below is designed to allow exactly
that behavior.

Put

\[
 N_a(x)=\#\{i:M_i^a(x)\ne0\},\qquad
 C_a(x)=\sum_{i:M_i^a(x)\ne0}r_i,
 \qquad R=\sum_ir_i.                                      \tag{17}
\]

Equations (11), (14), and (16) give the pointwise budgets

\[
 N_a(x)\geq\left\lceil\frac p c\right\rceil,
 \quad C_a(x)\geq p,
 \quad \sum_aN_a(x)\leq L,
 \quad \sum_aC_a(x)\leq R.                              \tag{18}
\]

## 3. Phase manifolds without a smooth cone boundary

The saturation argument needs only the topology of normalized cone rays.
Choose \(e_i\in\operatorname{int}K_i\).  The dual base

\[
 \mathcal B_i^*=\{b\in K_i^*:\langle e_i,b\rangle=1\}
\]

is a compact convex body of affine dimension \(m_i-1\), and

\[
 \mathcal J_i^*:=\partial\mathcal B_i^*
                 \cong S^{m_i-2}=S^{r_i}.                 \tag{19}
\]

The homeomorphism can be obtained by radial projection from any interior
point of the base.  No differentiability of \(\mathcal J_i^*\) is assumed.
Whenever \(B_i^a(u)\) is a nonzero boundary point, define its normalized
phase

\[
 q_i^a(u)=\frac{B_i^a(u)}{\langle e_i,B_i^a(u)\rangle}
                         \in\mathcal J_i^*.                \tag{20}
\]

Fix a source \(a\), a label set \(J\), and a compact set
\(E\subset M\) on which exactly \(J\) is active for \(a\) and

\[
                         \sum_{i\in J}r_i=p.               \tag{21}
\]

Every projected contact \(u=x_a\in\pi_a(E)\) has a neighborhood on which
all phases (20) are defined.  Indeed, keep the other primal coordinates
fixed.  Activity keeps \(A_i\) nonzero nearby, continuity keeps \(B_i^a\)
nonzero, and complementarity then forces \(B_i^a\) to remain on the dual
boundary.

On a common neighborhood \(P\) of the compact projection \(\pi_a(E)\),
consider

\[
 Q_J=(q_i^a)_{i\in J}:P\longrightarrow
                    \prod_{i\in J}\mathcal J_i^*.         \tag{22}
\]

This map is an immersion near the projected compact set.  To see the
logical order precisely, take \(u\in\pi_a(E)\), choose \(x\in E\) with
\(x_a=u\), and suppose \(DQ_J(u)[v]=0\).  Then every
\(DB_i^a(u)[v]\) is radial modulo normalization.  Equations (12) and (10)
give

\[
                  M_i^a(x)(w,v)=0
                  \qquad(w\in T_uS^p,\ i\in J).
\]

Labels outside \(J\) are inactive at this chosen \(x\).  Equation (11)
therefore gives \(\langle w,v\rangle=0\) for every \(w\), and hence
\(v=0\).  Thus \(DQ_J\) has full rank on \(\pi_a(E)\).  Full rank is open,
and compactness lets one shrink to a common neighborhood \(P\) on which
\(Q_J\) is an immersion.

Although the target boundaries in (22) may initially be nonsmooth, this is
enough.  The constant-rank theorem makes (22) a local embedding in the
ambient Euclidean product.  Its target is a topological \(p\)-manifold by
(19) and (21).  Invariance of domain therefore makes every embedded image
relatively open in the target: (22) is a local homeomorphism.

If every \(r_i<p\), then \(P\) cannot be all of \(S^p\).  Otherwise the
compact local homeomorphism (22) would be a finite covering onto the
connected product of spheres.  If some \(r_i=1\), that product has infinite
fundamental group, whose universal cover is noncompact, whereas \(S^p\) is
simply connected and compact.  If all \(r_i\geq2\), the target is simply
connected, so the covering would be a homeomorphism; this is impossible
because a product of at least two positive-dimensional spheres has nonzero
intermediate integral cohomology and \(S^p\) does not.  Consequently

\[
 P\subsetneq S^p,
 \qquad H^p(P;\mathbb Z)=0.                               \tag{23}
\]

The latter assertion holds componentwise for every proper open subset of a
connected closed oriented \(p\)-manifold.

## 4. The relative top-class argument

Assume first \(c<p\) and, contrary to the capacity bound in (4),

\[
                              R\leq k(p+1)-1.               \tag{24}
\]

The pointwise budgets (18) imply that the closed sets

\[
                         E_a=\{x:C_a(x)=p\}                \tag{25}
\]

cover \(M\).  Closedness follows because each active locus is open and
\(C_a\geq p\).  Partition \(E_a\) by its exact active-label set.  The
pieces form a finite clopen partition of \(E_a\): existing active labels
persist locally, while a new one would raise the capacity above \(p\).

On every such compact piece, (21) holds and every \(r_i\leq c<p\), so
Section 3 supplies a proper phase neighborhood.  The pieces are disjoint
compact subsets of the metrizable manifold \(M\), so choose pairwise
disjoint open neighborhoods of them, each contained in the pullback of its
phase neighborhood, and call their union \(U_a\).  If
\(u_a\in H^p(M;\mathbb Z)\) is the pullback of the top class of the
\(a\)-th sphere, (23) gives

\[
                             u_a|_{U_a}=0.                  \tag{26}
\]

The \(U_a\)'s cover \(M\).  Lifting each \(u_a\) to
\(H^p(M,U_a;\mathbb Z)\) and taking the relative cup product gives

\[
                u_1\smile\cdots\smile u_k=0.              \tag{27}
\]

This contradicts the Künneth theorem for \((S^p)^k\).  Hence
\(R\geq k(p+1)=ks\).

For the factor count, (18) already gives

\[
 L\geq k\left\lceil\frac pc\right\rceil
      =k\left\lceil\frac{p+1}{c}\right\rceil
\]

unless \(c\mid p\).  In the remaining case write \(p=tc\).  If
\(L\leq k(t+1)-1\), the closed loci on which source \(a\) has exactly
\(t\) active labels cover \(M\).  On each exact-label stratum, the rank
\(p\) identity (11) forces all \(t\) capacities to equal \(c\), so (21)
holds and the same relative top-class contradiction applies.  Therefore

\[
                        L\geq k(t+1)
                         =k\left\lceil\frac{s}{c}\right\rceil. \tag{28}
\]

Since \(\sum_i m_i=R+2L\), (4) follows.  When \(c\geq p\), the direct
pointwise inequalities (18) give (5); no strict topological increment is
available or needed.

### Heterogeneous product balls

The same statement is exact for \(C=\prod_{a=1}^kB_2^{s_a}\), with
\(p_a=s_a-1\geq2\).  Define

\[
 h_a=\begin{cases}
  \lceil s_a/c\rceil,&c<p_a,\\
  1,&c\geq p_a,
 \end{cases}
 \qquad
 \tau_a=\begin{cases}
  s_a,&c<p_a,\\
  p_a,&c\geq p_a.
 \end{cases}                                               \tag{28a}
\]

Then the exact frontier over the capped (ER) dictionary class is

\[
 \boxed{
 L_{\min}=\sum_ah_a,\qquad
 R_{\min}=\sum_a\tau_a,\qquad
 D_{\min}=\sum_a(\tau_a+2h_a),\qquad
 \nu_{\min}=2\sum_ah_a.}                                  \tag{28b}
\]

For capacity, let \(I=\{a:c<p_a\}\).  If
\(R<\sum_ap_a+|I|\), then at every point at least one source in \(I\)
has active capacity exactly \(p_a\).  Those closed saturation loci cover
the full product, and the preceding phase and relative-cup proof, now using
only \(\prod_{a\in I}u_a\), gives a contradiction.  For count, the only
sources where the pointwise ceiling is one below \(h_a\) are
\(J=\{a:c<p_a,\ c\mid p_a\}\).  If \(L<\sum_ah_a\), the exact-baseline
loci for sources in \(J\) cover the product, and the same proof using
\(\prod_{a\in J}u_a\) gives a contradiction.  Both cohomology products are
nonzero by Künneth.  Separate direct or grouped Lorentz constructions attain
all four quantities in (28b).

## 5. Sharpness and the ambient barrier bound

For \(c<p\), split the \(s\) Euclidean coordinates of each source into
\(h=\lceil s/c\rceil\) nonempty groups \(G\), each of size at most \(c\).
For \(w\in\mathbb R^{|G|}\), set

\[
 \mathcal A(w)=\left(\frac{1+\|w\|^2}{2},
                     \frac{1-\|w\|^2}{2},w\right),\qquad
 \mathcal B(w)=\left(\frac{1+\|w\|^2}{2},
                    -\frac{1-\|w\|^2}{2},-w\right).       \tag{29}
\]

These vectors lie in \(Q_{|G|+2}\) and satisfy

\[
                  \langle\mathcal A(u),\mathcal B(v)\rangle
                         =\frac12\|u-v\|^2.                \tag{30}
\]

Using separate grouped factors for each source and summing (30) gives
\(1-x_a^Tz\).  The construction has \(L=kh\), total capacity \(ks\), and
ambient dimension \(k(s+2h)\).  For \(c\geq p\), use one direct Lorentz
factor

\[
                  A_a(x)=(1,x_a),\qquad B_a^a(z)=(1,-z)   \tag{31}
\]

per source and zero dual factors on the other rows.

To prove (8), choose for each \(K_i\) a two-dimensional linear subspace
\(V_i\) meeting \(\operatorname{int}K_i\).  The section
\(K_i\cap V_i\) is a two-dimensional proper cone, hence linearly isomorphic
to \(\mathbb R_+^2\).  Restricting \(F\) to
\(V=\prod_iV_i\) preserves logarithmic homogeneity and self-concordance and
produces a barrier on

\[
             \left(\prod_iK_i\right)\cap V
                   \cong\mathbb R_+^{2L}.                  \tag{32}
\]

The optimal self-concordance parameter of the \(2L\)-orthant is \(2L\),
which proves (8).  The standard barrier of each Lorentz factor has parameter
two, proving sharpness for the constructions.

## 6. Why the face hypothesis is essential

Without (ER), even the factor-count conclusion is false when \(k\geq2\).
For a cap-respecting example take \(d=k(s+1)\) and let

\[
                          K=Q_{s+1}^{\times k}
\]

but regard this Cartesian product as one proper cone of dimension
\(k(s+1)\).  Define

\[
 A(x)=((1,x_1),\ldots,(1,x_k)),
\]

and let \(B^a(z)\) have \((1,-z)\) in block \(a\) and zero in every other
block.  Then

\[
                          \langle A(x),B^a(z)\rangle
                                  =1-x_a^Tz,                \tag{33}
\]

so all rows are represented with \(L=1\), rather than \(L\geq k\).  The
complementary face exposed by \(B^a(z)\) contains arbitrary vectors in the
other \(k-1\) Lorentz blocks and is far from a ray.  This example isolates
the precise sharing mechanism excluded by (ER).

Strict convexity of the primal base is sufficient even if the boundary is
nonsmooth.  Smoothness alone is not sufficient for the proof: smooth convex
bodies can contain flat boundary patches, whose supporting functionals
expose positive-dimensional faces.  Requiring both the primal and dual
bases to be smooth and strictly convex is safe but redundant.  Also, if
one-dimensional ray factors are admitted, the assertion \(\nu\geq2L\) must
be changed because a ray has optimal barrier parameter one; assumptions
(3) deliberately exclude that edge case.

## Scope and literature screen

This is a theorem about globally labelled \(C^1\) selected factors of the
full extreme slack.  A cone lift implies an abstract cone factorization, but
does not automatically supply selections with this global regularity.  The
result therefore does not apply to an arbitrary nonsmooth lift without an
additional selection theorem.  It also does not apply to one fixed weighted
contact kernel: the full cylindrical zero sets in (15) are essential.

Gouveia, Parrilo, and Thomas established the lift--cone-factorization
correspondence in [*Lifts of Convex Sets and Cone
Factorizations*](https://arxiv.org/abs/1111.3164).  Saunderson's
[*Limitations on the Expressive Power of Convex Cones Without Long Chains
of Faces*](https://arxiv.org/abs/1902.06401) gives different obstructions to
product-cone lifts through neighborliness and face-chain length, including
applications to smooth cones.  Fawzi's
[*On Representing the Positive Semidefinite Cone Using the Second-Order
Cone*](https://arxiv.org/abs/1610.04901) proves a different
nonrepresentability theorem via growing finite slack submatrices.  Standard
orthant barrier optimality is due to Nesterov and Nemirovskii; a modern
discussion of barrier parameters and universal barriers is Lee and Yue,
[*Universal Barrier Is \(n\)-Self-Concordant*](https://arxiv.org/abs/1809.03011).

A targeted search over these sources and combinations of "strictly convex
cone," "smooth cone," "cone factorization," and "product cone lift" found
no result deriving the exact finite dimension-capped frontier (4)--(8) from
global \(C^1\) contact topology.  The apparently new ingredient is the
combination of pointwise exposed-ray no-sharing with the relative top-class
cover argument.  Priority is not certified and remains subject to a
specialist literature review.

## Internal hostile audit

The following possible failure modes were checked explicitly.

1. **Individual channels need not be PSD.**  The proof uses only the rank
   inequality (14), rank subadditivity, and nondegeneracy of the sum (11).
2. **Vertices cause no hidden phase singularity.**  Derivatives at cone
   vertices vanish, and phase maps are introduced only on open neighborhoods
   of compact saturated strata where both contact factors remain nonzero.
3. **The cone boundary need not be smooth.**  The normalized boundary is a
   topological sphere.  Ambient \(C^1\) immersion plus invariance of domain,
   rather than a preassigned smooth boundary atlas, supplies the local
   homeomorphism used by the covering argument.
4. **Labels may switch globally.**  No channelwise continuation is used.
   Exact-active-label strata are clopen only inside the closed saturation
   locus; the relative cup product handles switching between strata.
5. **The divisible count case is separate.**  The topological increment is
   needed only when \(c\mid p\).  The boundary case \(c=p\) belongs to the
   large-cap regime and is an explicit counterexample to the naive uniform
   ceiling formula.
6. **The barrier claim allows coupling.**  It is obtained by restricting the
   entire coupled barrier to one product orthant section, not by assuming
   additivity across factors.
7. **The structural assumption is oriented.**  Only exposed faces of the
   common-primal cone \(K_i\) need be rays.  If primal and dual factor roles
   are reversed, the corresponding property must instead be imposed on
   \(K_i^*\).
