# Submersions from equal-sphere products to spheres

Status: Proved; primary-source-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the rational dimension theorem and joint-map corollary;
the remaining integral existence question is explicitly left open

## Main results

Let

\[
                    E=(S^q)^k,\qquad q\geq2,
\]

and let \(f:E\to S^r\) be a \(C^1\) submersion, with
\(1\leq r<kq\). Then

\[
 \boxed{
 r=q\quad\text{or}\quad
 q=2r-1\ \text{ with }r\text{ even}.}                       \tag{1}
\]

Equivalently, the only rationally possible proper target below \(q\) is

\[
              q\equiv3\pmod4,
              \qquad r={q+1\over2}.                         \tag{2}
\]

Projection realizes \(r=q\).  Composing a projection with a Hopf map
realizes the exceptional pairs

\[
                    (q,r)=(3,2),(7,4),(15,8).               \tag{3}
\]

For \(k=1\), the classical Browder--Adams theorem says that (3) are the
only proper cases.  For \(k>1\), the rational argument does **not** remove
the further candidates

\[
                    (q,r)=(11,6),(19,10),(27,14),\ldots .   \tag{4}
\]

No construction or nonexistence theorem for these product-source cases
was found in the targeted search.  In particular, the sphere-total-space
theorem cannot simply be applied with \((S^q)^k\) as total space.

There is a stronger conclusion for a jointly nonsingular collection.  Let

\[
 f_i:(S^q)^k\longrightarrow S^{r_i},\qquad r_i\geq2,
 \qquad \sum_{i=1}^{\ell}r_i=kq.                            \tag{5}
\]

If the combined differential

\[
       dF=\bigoplus_i df_i,
       \qquad F=(f_1,\ldots,f_\ell),                        \tag{6}
\]

is injective everywhere, then

\[
             \boxed{\ell=k\quad\text{and}\quad r_i=q
                    \text{ for every }i.}                  \tag{7}
\]

Thus Hopf-sized targets and the unresolved candidates (4) cannot occur in
a full-rank saturated collection.  The distinction between an arbitrary
collection and (6) is essential: repeated copies of one projection may
have target dimensions summing to the source dimension while their
differentials have large common kernel.

The covering step is actually more general.  If \(P\) is any compact
connected \(n\)-manifold and maps \(p_i:P\to S^{c_i}\), \(c_i\geq2\),
satisfy \(\sum_i c_i=n\) and \(\bigoplus_i dp_i\) is injective, then

\[
                     P\longrightarrow\prod_i S^{c_i}        \tag{7a}
\]

is a finite covering and, because its target is simply connected, is a
diffeomorphism.  For \(P=S^n\), this immediately forces a single target
of dimension \(n\).  Thus the joint-map proof also gives the strict
saturated-capacity gap for a sphere source without using the individual
Browder classification.

## 1. The rational formal-dimension identity

For a nilpotent rationally elliptic space \(X\), put

\[
                 d_j(X)=\dim_{\mathbb Q}\pi_j(X)\otimes\mathbb Q.
\]

Its formal dimension is

\[
 \operatorname{fdim}X
   =\sum_{j\text{ odd}}j\,d_j(X)
    -\sum_{j\text{ even}}(j-1)d_j(X).                       \tag{8}
\]

This is Theorem 32.6 of Felix--Halperin--Thomas.  Their standard
topological formulation assumes simple connectivity.  For the possible
target \(S^2\), the fiber can have a degree-one generator; the same
formal-dimension identity is the algebraic identity for its finite
nilpotent elliptic Sullivan model, with that generator contributing
weight \(w_1=1\).  Write

\[
 w_j=\begin{cases}
       j,&j\text{ odd},\\
       -(j-1),&j\text{ even}.
     \end{cases}                                             \tag{9}
\]

Set \(w_0=0\); the base is simply connected, so this convention only
records the absent degree-one term when indices are shifted below.

Consider a fibration \(H\to E\xrightarrow f B\) of nilpotent spaces in
which \(E,B,H\) are rationally elliptic.  If

\[
 a_j=\operatorname{rank}_{\mathbb Q}
       \bigl(\pi_j(E)\otimes\mathbb Q
             \longrightarrow\pi_j(B)\otimes\mathbb Q\bigr),
\]

exactness of the homotopy sequence gives

\[
 d_j(H)=d_j(E)+d_{j+1}(B)-a_j-a_{j+1}.                      \tag{10}
\]

Substitution in (8), followed by the index change \(m=j+1\), gives

\[
 \operatorname{fdim}H
 =\operatorname{fdim}E
  +\sum_m w_{m-1}d_m(B)
  -\sum_m(w_m+w_{m-1})a_m.                                 \tag{11}
\]

The useful cancellation is

\[
 w_m+w_{m-1}
 =\begin{cases}
    2,&m\text{ odd},\\
    0,&m\text{ even}.
  \end{cases}                                                \tag{12}
\]

Consequently only the ranks of the maps on odd rational homotopy enter
the correction term in (11).

## 2. Proof of the individual-submersion theorem

First suppose \(f\) is smooth.  Since \(E\) is compact, Ehresmann's theorem
makes \(f\) a smooth fiber bundle

\[
                       H\longrightarrow E\longrightarrow S^r.            \tag{13}
\]

The fiber is connected because the base is simply connected and the total
space is connected.  It is a closed orientable manifold of dimension

\[
                         \dim H=kq-r.                       \tag{14}
\]

Orientability also follows directly from
\(TH\oplus f^*TS^r\cong TE|_H\).  The fiber is nilpotent: it is homotopy
equivalent to the homotopy fiber of a map between simply connected
nilpotent spaces.  Its rational homotopy is finite-dimensional by the long
exact sequence, because both a sphere and a finite product of spheres have
finite-dimensional rational homotopy.  Its rational cohomology is finite
because it is a closed manifold.  Hence \(H\) is rationally elliptic, and

\[
                  \operatorname{fdim}H=\dim H=kq-r.         \tag{15}
\]

Also \(\operatorname{fdim}E=kq\).

If \(r\) is odd, \(S^r\) has one rational homotopy generator, in degree
\(r\).  Formula (11) becomes

\[
                  \operatorname{fdim}H
                    =kq-(r-2)-2a_r.                         \tag{16}
\]

Comparison with (15) forces \(a_r=1\).  Thus

\[
          \pi_r((S^q)^k)\otimes\mathbb Q\ne0.               \tag{17}
\]

If \(q\) is odd, the product has rational homotopy only in degree \(q\),
so \(r=q\).  If \(q\) is even, its rational homotopy occurs in degrees
\(q\) and \(2q-1\), but the odd possibility \(r=2q-1\) is excluded by
Euler characteristic:

\[
 2^k=\chi(E)=\chi(S^r)\chi(H)=0.                            \tag{18}
\]

If \(r\) is even, \(S^r\) has rational homotopy generators in degrees
\(r\) and \(2r-1\).  The two base contributions in (11) are

\[
             w_{r-1}+w_{2r-2}
             =(r-1)-(2r-3)=2-r.                             \tag{19}
\]

The rank in even degree \(r\) cancels by (12), whereas the rank in odd
degree \(2r-1\) contributes \(-2a_{2r-1}\).  Thus

\[
        \operatorname{fdim}H=kq+2-r-2a_{2r-1}.              \tag{20}
\]

Comparison with (15) forces \(a_{2r-1}=1\).  If \(q\) is odd, the only
rational homotopy degree of \(E\) is \(q\), giving \(q=2r-1\).  If \(q\)
is even, the only odd rational homotopy degree is \(2q-1\), giving
\(r=q\).  This proves (1) for smooth submersions.

There is no submersion to \(S^1\).  Since \((S^q)^k\) is simply connected,
every map to \(S^1\) lifts through \(\mathbb R\to S^1\).  The real-valued
lift has an extremum on the compact source, and the derivative of the
original map therefore fails to be surjective there.

For a \(C^1\) submersion, take a sufficiently close smooth approximation
in the \(C^1\) topology.  With fixed Riemannian metrics, the surjectivity
modulus

\[
             \inf_{\|u\|=1}\|df_x^*u\|
\]

has a positive minimum on compact \(E\), so a close approximation is still
a submersion.  Its image is open and, by compactness, closed in the
connected target, hence it is onto.  The smooth argument therefore proves
the same existence obstruction in the \(C^1\) category.

## 3. What the argument does not classify

When \(q=2r-1\) and \(r\) is even, the rational homotopy fiber has the
right formal dimension.  At the level of Sullivan models, it has the
rational type

\[
                         S^{r-1}\times(S^q)^{k-1}            \tag{21}
\]

when the relevant rational homotopy map has rank one.  Thus rational
homotopy cannot distinguish the three Hopf pairs from (4).

For \(k=1\), Browder's theorem on fiberings with sphere total space,
together with the Hopf-invariant-one theorem, leaves only (3).  That proof
uses the fact that the **entire total space is a sphere**.  It does not
apply to \((S^q)^k\) for \(k>1\).  A proof excluding (4) would need an
integral or prime-local obstruction to a finite manifold homotopy fiber,
or a separate geometric argument.  No such general result was located in
the present search, so (4) must currently be recorded as unresolved, not
as impossible.

## 4. Proof of the jointly nonsingular collection theorem

Under (5)--(6), source and target have the same dimension.  Thus \(F\) is
a local diffeomorphism.  It is proper because its source is compact, so it
is a covering of the connected target.  The target is simply connected
because every \(r_i\geq2\); hence \(F\) is a diffeomorphism.

It remains only to compare rational homotopy.  If \(q\) is odd,
\((S^q)^k\) has rational homotopy of rank \(k\), all in degree \(q\).
Therefore every target sphere is odd-dimensional of dimension \(q\), and
there are exactly \(k\) of them.  If \(q\) is even, the source has rank
\(k\) in degree \(q\) and rank \(k\) in degree \(2q-1\), with no other
rational homotopy.  Each even target sphere contributes one generator in
exactly those two degrees.  This again forces exactly \(k\) targets, all
of dimension \(q\); an odd target would contribute an unmatched odd-degree
generator.  This proves (7).

The same proof works for \(C^1\) maps: a full-rank map between equal-
dimensional \(C^1\) manifolds is a local \(C^1\) diffeomorphism.

Exactly the same local-diffeomorphism and proper-covering argument proves
(7a).  The target is simply connected, so the connected covering has one
sheet.  In the sphere case, a
product of two or more positive-dimensional spheres has rational
cohomology in at least two positive degrees below the top (counting
multiplicity), whereas a sphere does not.  Hence only one target can
occur.

## 5. Consequence for saturated cone curvature channels

Suppose a full mixed-curvature factorization is parametrized by

\[
                         P\cong(S^q)^k,
 \qquad \dim P=kq,                                          \tag{22}
\]

and positive cone blocks have capacities

\[
                         c_i=(\dim K_i-2)_+.
\]

Assume, as in the audited factor-to-submersion theorem, that the cone
factors are globally labelled and \(C^1\), that their normalized boundary
maps are globally defined, and that the quotient derivative of each map
has the same first-slot kernel as its mixed channel.

In the capacity-saturated case \(\sum_i c_i=kq\), the standard quotient-
rank argument produces submersions

\[
                         p_i:P\longrightarrow S^{c_i}.      \tag{23}
\]

A capacity-one block cannot occur: a map from simply connected compact
\(P\) to \(S^1\) lifts to a real-valued function and cannot be a
submersion.  Thus every positive saturated capacity is at least two.

Moreover their combined differential is injective.  Indeed, if
\(v\in\bigcap_i\ker dp_i\), then the quotient derivative of every channel
annihilates \(v\), so every mixed channel \(M_i(v,\cdot)\) vanishes.  Their
sum is the nondegenerate full mixed pairing, forcing \(v=0\).  Since
\(\sum_i c_i=\dim P\), the combined derivative is an isomorphism.

Section 4 now gives the exact saturated profile

\[
        \boxed{\text{there are exactly }k\text{ positive blocks and }
               c_i=q\text{ for every one of them}.}         \tag{24}
\]

This conclusion is stronger than applying the individual obstruction (1)
block by block.  It excludes even genuine Hopf-sized channels because the
joint map would otherwise be a forbidden covering between unequal products
of spheres.  It applies only when the curvature argument supplies globally
labelled sphere maps and the common-kernel implication above; a numerical
identity \(\sum_i c_i=kq\) by itself is not enough.

## 6. Arithmetic for a collection without joint rank

If one knows only that each \(f_i\) is a submersion and
\(\sum_i r_i=kq\), then (1) gives the following weaker statement.

- If \(q\not\equiv3\pmod4\), every \(r_i=q\), so there are \(k\) maps.
- If \(q\equiv3\pmod4\), write \(a\) for the number of targets of
  dimension \(q\) and \(b\) for the number of targets of dimension
  \((q+1)/2\).  Necessarily

  \[
                    aq+b{q+1\over2}=kq.                     \tag{25}
  \]

  Existence of the smaller targets is known from Hopf maps only for
  \(q=3,7,15\).  For the remaining \(q\), (25) is only a necessary
  arithmetic condition.

In particular, if the collection has exactly \(k\) members, their average
dimension is \(q\) and each has dimension at most \(q\), so every target
already has dimension \(q\), without a joint-rank assumption.

## 7. Literature boundary

The ingredients used above are classical:

- C. Ehresmann,
  [*Les connexions infinitesimales dans un espace fibre differentiable*](https://www.numdam.org/item/SB_1948-1951__1__153_0/),
  gives the proper-submersion theorem.
- Y. Felix, S. Halperin, and J.-C. Thomas,
  *Rational Homotopy Theory*, Graduate Texts in Mathematics 205,
  Springer (2001), Theorem 32.6, gives (8).  An accessible statement
  is also recorded in
  [Kathryn Hess's rational-homotopy notes](https://homepages.math.uic.edu/~bshipley/Hess.Chicago.pdf).
- W. Browder,
  [*Fiberings of spheres and H-spaces which are rational homology spheres*](https://doi.org/10.1090/S0002-9904-1962-10747-2),
  Bulletin of the AMS 68 (1962), 202--203, treats the case in which the
  total space itself is a sphere.
- J. F. Adams,
  [*On the non-existence of elements of Hopf invariant one*](https://doi.org/10.2307/1970147),
  Annals of Mathematics 72 (1960), 20--104, is the primary source for the
  exceptional Hopf dimensions.

A targeted search found these sphere-total-space and rational-homotopy
results, but no theorem classifying submersions
\((S^q)^k\to S^r\) for \(k>1\).  The formal-dimension calculation leading
to (1) is elementary once (8) is invoked and may be implicit in the
literature.  The cone-curvature use of the jointly nonsingular conclusion
(24) appears new, subject to specialist review.

## Audit record

An independent hostile audit checked the elliptic formal-dimension
identity, the homotopy long-exact-sequence rank algebra, fiber
connectedness, orientability, nilpotence and ellipticity, both parity
branches of the dimension restriction, \(C^1\) smoothing, the proper
local-diffeomorphism argument, and the conditional cone common-kernel
application. It found no mathematical defect after the regularity
hypotheses and the surjectivity modulus were made explicit.
