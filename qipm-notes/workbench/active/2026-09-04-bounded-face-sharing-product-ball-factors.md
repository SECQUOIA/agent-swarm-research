# Bounded complementary faces interpolate between no-sharing and packed cone blocks

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the stated selected-factor theorem

## Main theorem

Let

\[
 M=(S^p)^k,\qquad p=s-1\geq2,
\]

and factor the full extreme slack of \((B_2^s)^k\) as

\[
 1-\langle x_a,z\rangle
   =\sum_{i=1}^L\langle A_i(x),B_i^a(z)\rangle,
 \qquad a\in[k],\quad x\in M,\quad z\in S^p,             \tag{1}
\]

where \(A_i:M\to K_i\), \(B_i^a:S^p\to K_i^*\) are
globally \(C^1\) and \(K_i\subset\mathbb R^{m_i}\) is proper.  Assume
\(m_i\geq3\), and put

\[
 r_i=m_i-2,
 \qquad
 f_i=\max_{0\ne b\in\partial K_i^*}
          \dim\bigl(K_i\cap b^\perp\bigr),
 \qquad \bar f_i=\min(f_i,k).                             \tag{2}
\]

Zero exposed faces are omitted from the maximum; every face that occurs in
an active contact channel is nonzero.  Let

\[
       F=\sum_i\bar f_i,
 \qquad G=\sum_i\bar f_i r_i,
 \qquad R=\sum_ir_i.                                      \tag{3}
\]

At every contact point define

\[
 M_i^a(x)(u,v)
   =-\langle D_aA_i(x)[u],DB_i^a(x_a)[v]\rangle,
 \qquad t_i^a(x)=\operatorname{rank}M_i^a(x),             \tag{4}
\]

and let \(I_i(x)=\{a:t_i^a(x)>0\}\).  Then every individual cone block
obeys the sharp local packing inequalities

\[
 \boxed{
  \sum_{a\in I_i(x)}t_i^a(x)\leq m_i-1,
  \qquad
  1+\sum_{b\in I_i(x)\setminus\{a\}}t_i^b(x)
       \leq \dim\bigl(K_i\cap B_i^a(x_a)^\perp\bigr)
       \quad(a\in I_i(x)).}                               \tag{5}
\]

In particular,

\[
                         |I_i(x)|\leq\bar f_i.             \tag{6}
\]

Thus a face of dimension \(f\) can serve at most \(f\) source rows at the
same point.  The ray-exposed case \(f=1\) is exactly pointwise no-sharing.

Suppose also that \(m_i\leq d\) and put \(c=d-2\).  Define

\[
 h(c)=\begin{cases}
       \lceil s/c\rceil,&c<p,\\
       1,&c\geq p,
      \end{cases}
 \qquad
 \tau(c)=\begin{cases}
       s,&c<p,\\
       p,&c\geq p.
      \end{cases}                                         \tag{7}
\]

Then the global face budgets satisfy

\[
 \boxed{
         F\geq kh(c),\qquad
         G\geq k\tau(c),\qquad
         R+L\geq kp.}                                     \tag{8}
\]

The first two inequalities include the same relative-top-cohomology
increment that makes the ray-exposed frontier exact; they are not merely
pointwise incidence counts.

If every nonzero exposed complementary face has dimension at most \(f\),
then (8) gives

\[
 \boxed{
 L\geq L_0:=\left\lceil\frac{kh(c)}{f}\right\rceil,
 \qquad
 R\geq R_0:=\left\lceil\frac{k\tau(c)}{f}\right\rceil,
 \qquad R+L\geq kp.}                                     \tag{9}
\]

Since \(r_i\geq1\), one also has \(R\geq L\), and therefore the ambient
scalar dimension \(D=R+2L\) and every ambient logarithmically homogeneous
self-concordant barrier parameter satisfy

\[
 D\geq2L_0+\max\{R_0,kp-L_0,L_0\},
 \qquad \nu_{\rm ambient}\geq2L_0.                       \tag{10}
\]

For \(f=1\), (9) recovers the exact ray-exposed count and capacity frontiers
and (10), together with \(D=R+2L\), recovers their exact dimension and
ambient barrier bounds.  For \(f>1\), these are interpolation lower bounds,
not generally exact: face incidence controls how many rows can share a
block, but does not classify which abstract packing patterns are integrable
by one global cone factor.

There is also a useful face--capacity tradeoff not visible in (9).  If
\(q_i=|I_i(x)|\geq2\) and \(T_i=\sum_at_i^a(x)\), summing the second
inequality in (5) gives

\[
              (q_i-1)T_i\leq q_i(f_i-1),
              \qquad T_i\leq2(f_i-1).                    \tag{10a}
\]

Consequently a block can attain the one-unit aggregate bonus
\(T_i=r_i+1\) allowed by the first inequality in (5) only if
\(r_i\leq2f_i-3\).  If

\[
             B=\#\{i:r_i\leq2f_i-3\},
\]

then

\[
                              kp\leq R+B.                  \tag{10b}
\]

In the uniform regime \(r_i\leq c\), \(f_i\leq f\), and
\(2(f-1)\leq c\), every block has \(T_i\leq c\), whether it serves one row
or several.  Hence

\[
                  L\geq\left\lceil\frac{kp}{c}\right\rceil. \tag{10c}
\]

This can be stronger than the raw incidence bound in (9) when faces are
small relative to cone dimension.

## 1. Cross-contact annihilation

Termwise nonnegativity and contact give

\[
              \langle A_i(x),B_i^a(x_a)\rangle=0.         \tag{11}
\]

Fix \(a\), fix \(u=x_a\), and let all other primal coordinates vary.  For
every such \(x\), the nonnegative function

\[
                 z\longmapsto\langle A_i(x),B_i^a(z)\rangle
\]

has value zero and hence a critical point at \(z=u\).  Thus

\[
                 \langle A_i(x),DB_i^a(u)[v]\rangle=0     \tag{12}
\]

for every \(x\) on that cylinder.  Differentiating (12) in a different
source direction \(b\ne a\) is legitimate under only \(C^1\) regularity and
gives the individual cross-contact identity

\[
 \boxed{
   \langle D_bA_i(x)[w],DB_i^a(x_a)[v]\rangle=0
   \qquad(b\ne a).}                                      \tag{13}
\]

No cancellation between cone blocks is involved.  This identity is the
linear-algebraic source of the packing theorem.

As in the universal contact-rank lemma, a derivative at a pointed-cone
vertex is zero.  At a nonvertex contact, first derivatives also satisfy

\[
 \langle D_aA_i[u],B_i^a\rangle=0,
 \qquad \langle A_i,DB_i^a[v]\rangle=0,                  \tag{14}
\]

so the mixed pairing factors through two \((m_i-2)\)-dimensional ray
quotients.  Hence

\[
                           t_i^a(x)\leq r_i.               \tag{15}
\]

Mixed differentiation of (1) gives

\[
                    \sum_iM_i^a(x)=g_{S^p,x_a},           \tag{16}
\]

and rank subadditivity implies

\[
                     \sum_it_i^a(x)\geq p.                \tag{17}
\]

## 2. Direct-sum proof of face packing

Fix \(i,x\), suppress these indices, and assume at least one source is
active.  Then \(A=A_i(x)\ne0\).  Write

\[
 X_a=D_aA_i(x):T_{x_a}S^p\to\mathbb R^{m_i},
 \qquad
 (\Lambda_av)(w)=\langle v,DB_i^a(x_a)[w]\rangle.         \tag{18}
\]

The rank of \(\Lambda_aX_a\) is \(t_a=t_i^a(x)\).  Choose a subspace

\[
 E_a\subseteq\operatorname{im}X_a,
 \qquad \dim E_a=t_a,                                    \tag{19}
\]

on which \(\Lambda_a\) is injective.  Equations (12)--(13) say

\[
                    \Lambda_aA=0,
 \qquad \Lambda_aE_b=0\quad(b\ne a).                    \tag{20}
\]

Consequently

\[
                  \mathbb RA\oplus
                     \bigoplus_{a\in I_i(x)}E_a           \tag{21}
\]

is a direct sum.  Indeed, apply \(\Lambda_a\) to a putative linear
dependence; all terms except the one in \(E_a\) vanish, and injectivity
forces that term to vanish.  Doing this for every active \(a\) leaves only
a multiple of the nonzero vector \(A\).  Taking dimensions in (21) proves
the first inequality in (5).

For an active source \(a\), put

\[
             \mathcal F_a=K_i\cap B_i^a(x_a)^\perp.       \tag{22}
\]

This is a nonzero exposed face containing \(A\).  If \(b\ne a\), varying
only \(x_b\) stays on the zero cylinder of row \(a\), so the entire curve
\(A_i(x)\) remains in \(\mathcal F_a\).  Therefore

\[
                       E_b\subseteq\operatorname{span}\mathcal F_a
                       \qquad(b\ne a).                    \tag{23}
\]

The direct subspace

\[
                  \mathbb RA\oplus
                  \bigoplus_{b\ne a}E_b
                  \subseteq\operatorname{span}\mathcal F_a
\]

has dimension \(1+\sum_{b\ne a}t_b\), proving the second inequality in
(5).  Since every active rank is at least one, (6) follows immediately.

## 3. Global incidence, capacity, and rank ledgers

Let

\[
 N_a(x)=\#\{i:t_i^a(x)>0\},
 \qquad
 C_a(x)=\sum_{i:t_i^a(x)>0}r_i.                           \tag{24}
\]

Equations (15)--(17) imply

\[
 N_a(x)\geq\left\lceil\frac pc\right\rceil,
 \qquad C_a(x)\geq p.                                    \tag{25}
\]

Counting block--source incidences and using (6) gives

\[
                 \sum_aN_a(x)=\sum_i|I_i(x)|\leq F,       \tag{26}
\]

while capacity-weighted incidence gives

\[
                 \sum_aC_a(x)
                 =\sum_i|I_i(x)|r_i\leq G.                \tag{27}
\]

Finally, summing the first inequality in (5) over blocks and using (17)
gives the face-independent rank-packing ledger

\[
 kp\leq\sum_{a,i}t_i^a(x)
       \leq\sum_i(m_i-1)=R+L,                             \tag{28}
\]

which is the third assertion of (8).

For completeness, if \(q_i=|I_i(x)|\geq2\), summing the second inequality
in (5) over its \(q_i\) active rows gives

\[
 q_i+(q_i-1)T_i\leq q_if_i.
\]

This proves (10a).  Together with \(T_i\leq r_i+1\), it gives
\(T_i\leq r_i\) whenever \(r_i\geq2f_i-2\); a single-row block also obeys
\(T_i\leq r_i\).  Summation proves (10b), and the uniform specialization
proves (10c).

When \(c\geq p\), equations (25)--(27) immediately give
\(F\geq k\) and \(G\geq kp\).  It remains to prove the strict increments
for \(c<p\).

## 4. The top-class increment survives bounded sharing

First consider capacity.  Suppose, contrary to (8), that

\[
                            G\leq k(p+1)-1.                \tag{29}
\]

Equations (25) and (27) imply that at every point at least one source has
\(C_a(x)=p\).  Thus the closed sets

\[
                         Z_a=\{x:C_a(x)=p\}                \tag{30}
\]

cover \(M\).  Partition each \(Z_a\) into its finitely many clopen
exact-active-label strata.  On such a stratum with label set \(J\),

\[
                             \sum_{i\in J}r_i=p.           \tag{31}
\]

Normalize the nonzero dual contact factors into the boundaries of compact
dual cone bases.  Those boundaries are topological spheres \(S^{r_i}\).
Exactly as in the arbitrary-cone phase lemma, (16) and (31) make the product
phase map

\[
                 P\longrightarrow\prod_{i\in J}S^{r_i}   \tag{32}
\]

a local homeomorphism on a neighborhood \(P\) of the projected compact
stratum.  Since every \(r_i\leq c<p\), this neighborhood is proper: if it
were all of \(S^p\), (32) would be a finite covering, ruled out by the
fundamental group when some \(r_i=1\), and by intermediate cohomology when
all \(r_i\geq2\).

The top class of the \(a\)-th sphere therefore vanishes on a neighborhood
of \(Z_a\).  These neighborhoods cover \(M\), so their relative cup product
would make the nonzero class

\[
        u_1\smile\cdots\smile u_k
           \in H^{kp}((S^p)^k;\mathbb Z)                  \tag{33}
\]

vanish.  This contradiction proves \(G\geq k(p+1)=ks\).

For count, if \(c\nmid p\), then

\[
             \left\lceil\frac pc\right\rceil
              =\left\lceil\frac{p+1}{c}\right\rceil=h(c),
\]

so (25)--(26) already give \(F\geq kh(c)\).  If \(p=tc\), suppose
\(F\leq k(t+1)-1\).  At every point some source then has exactly \(t\)
active labels.  Its exact-label strata have \(t\) capacities at most \(c\),
while (16) has rank \(p=tc\); hence every capacity is \(c\) and (31) again
holds.  Repeating (30)--(33) proves

\[
                             F\geq k(t+1)=kh(c).            \tag{34}
\]

This proves (8).  The uniform-face bounds (9) follow from
\(F\leq fL\), \(G\leq fR\).  The dimension formula (10) minimizes
\(D=R+2L\) subject to \(L\geq L_0\),
\(R\geq\max(R_0,kp-L,L)\); the objective is nondecreasing in \(L\), so its
minimum occurs at \(L=L_0\).  The barrier bound follows by restricting any
coupled ambient barrier to a product of two-dimensional cone sections,
which is a \(2L\)-orthant.

## 5. PSD interpretation

For \(K_i=\mathbb S_+^q\), a contact dual matrix \(B_i^a\) of nullity
\(h_{ia}\) exposes

\[
 \mathcal F_{ia}
   =\{X\succeq0:\operatorname{range}X\subseteq\ker B_i^a\}
   \cong\mathbb S_+^{h_{ia}},
 \qquad
 \dim\mathcal F_{ia}=\binom{h_{ia}+1}{2}.                 \tag{35}
\]

The local packing theorem becomes

\[
 1+\sum_{b\ne a}t_i^b(x)
       \leq\binom{h_{ia}+1}{2},
 \qquad
 \sum_at_i^a(x)\leq\binom{q+1}{2}-1.                    \tag{36}
\]

Thus PSD cross-source sharing is literally column/support-face packing:
all rank-detecting directions used by the other source balls, together with
the contact ray, must fit into the symmetric matrices supported on
\(\ker B_i^a\).  This explains why PSD blocks can share source rows whereas
strictly convex cones cannot.  It is compatible with, but does not replace,
the sharper one-row PSD mixed-curvature capacity
\(\lfloor q^2/4\rfloor\); combining (36) with that capacity can strengthen
instance-specific ledgers when the contact nullities are known.

## 6. Limits and counterexamples

The face bounds are necessary, not sufficient.  Abstract subspaces can
satisfy (5) without integrating to global cone-valued factors.  Hence no
matching construction is claimed for \(f>1\).

The dependence on \(f\) cannot be removed.  Regard
\(Q_{s+1}^{\times k}\) as one cone and set

\[
 A(x)=((1,x_1),\ldots,(1,x_k)),
\]

with \(B^a(z)\) supported only in Lorentz block \(a\).  This represents all
rows with one cone block.  The face exposed by \(B^a(z)\) contains the full
other \(k-1\) Lorentz factors, providing exactly the high-dimensional face
in which cross-source derivatives are packed.

Nor can one replace face dimension by the number of extreme rays of a face:
nonpolyhedral faces may have infinitely many extreme rays but only finitely
many tangent dimensions, and the proof uses the latter.

## Scope and novelty screen

The theorem concerns globally labelled \(C^1\) selected factors of the full
extreme slack.  It does not automatically apply to an arbitrary cone lift
without a global regular selection, and it does not concern only one fixed
weighted contact kernel.  The full cylindrical contact sets are used in
(12)--(13) and (23).

Gouveia--Parrilo--Thomas established the general cone-factorization
correspondence in [*Lifts of Convex Sets and Cone
Factorizations*](https://arxiv.org/abs/1111.3164).  Saunderson's
[*Limitations on the Expressive Power of Convex Cones Without Long Chains
of Faces*](https://arxiv.org/abs/1902.06401) uses face-chain length and
neighborliness to obstruct product-cone lifts.  Fawzi's
[*On Representing the Positive Semidefinite Cone Using the Second-Order
Cone*](https://arxiv.org/abs/1610.04901) uses finite slack sparsity and
second-order-cone coverings.  These works do not appear to contain the
pointwise differential inequalities (5), the face-incidence budgets (8),
or their relative-top-class strengthening.

A targeted search for combinations of cone factorization, complementary
face dimension, smooth/strictly convex cones, and product-cone sharing found
no matching theorem.  The potentially new result is the direct-sum
cross-contact packing lemma (5) and its conversion into global topological
resource ledgers.  Priority remains subject to specialist review.

## Independent audit

An independent hostile audit checked:

1. whether differentiating the cylinderwise criticality identity (12) is
   valid with only \(C^1\) factor maps;
2. the construction and simultaneous directness of the \(E_a\)'s;
3. the extra radial dimension in every face inequality;
4. all double-counting identities in (26)--(28);
5. that the phase/top-class proof uses no hidden ray-exposed hypothesis;
6. the integer transition at \(c=p\) and the divisible case \(c\mid p\);
7. the minimization giving (10); and
8. the PSD nullity specialization.

It confirmed that \(C^1\) regularity suffices for cross-contact
annihilation, that the rank-detecting subspaces and the extra radial
dimension give (5), and that all incidence, topology, cap arithmetic,
dimension minimization, PSD, and coupled-barrier statements are correct as
scoped.  No substantive correction was required.
