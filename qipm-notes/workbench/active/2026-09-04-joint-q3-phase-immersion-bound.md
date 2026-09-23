# Joint \(Q_3\) phases give a sharp codimension-one obstruction

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem; open gap stated explicitly

## Main result

Let

\[
 M=(S^q)^k,\qquad q\geq2,\qquad n=kq,
\]

and consider the normalized contact slack of \(Q_{q+2}^k\),

\[
 \sigma(x,y)=\sum_{\alpha=1}^k
       \bigl(1-\langle x_\alpha,y_\alpha\rangle\bigr),
 \qquad x,y\in M.                                             \tag{1}
\]

Suppose (1) has globally labelled \(C^1\) factors over \(L\)
three-dimensional Lorentz cones:

\[
 \sigma(x,y)=\sum_{j=1}^L\langle A_j(x),B_j(y)\rangle,
 \qquad A_j(x),B_j(y)\in Q_3.                                \tag{2}
\]

Then the local curvature bound gives \(L\geq n\). Global phase
integrability makes this strict:

\[
                              \boxed{L\geq n+1=kq+1.}          \tag{3}
\]

The same conclusion holds for any compact simply connected contact
\(n\)-manifold whose diagonal mixed slack form is nondegenerate. If its
two-point kernel vanishes only on the diagonal and the factors are nowhere
zero, the phase map is in fact an embedding, giving the stronger general
bound by Euclidean embedding dimension.

This improves the local additive lower bound by one block for global
\(C^1\) factor selections. It does **not** prove the conjecturally stronger
separate-block count

\[
                              L\geq k(q+1)=n+k.                \tag{4}
\]

In fact the phase argument factors through the Euclidean immersion
dimension of \(M\), and

\[
                 \operatorname{imm\,dim}\bigl((S^q)^k\bigr)=n+1.           \tag{5}
\]

Thus no argument using only the existence of the joint phase immersion can
improve (3). The gap of \(k-1\) blocks in (4) requires an additional exact
slack-integrability, convexity, or factor-separation invariant.

## 1. Local saturation forces nonzero boundary phases

At a diagonal contact \(y=x\), define

\[
 H_j(x)(u,v)
   =-\langle dA_j(x)u,dB_j(x)v\rangle,
 \qquad u,v\in T_xM.                                         \tag{6}
\]

Mixed differentiation of (1)--(2) gives

\[
 \sum_{j=1}^L H_j(x)(u,v)
   =G_x(u,v)
   :=\sum_{\alpha=1}^k\langle u_\alpha,v_\alpha\rangle.       \tag{7}
\]

Every \(Q_3\) channel has rank at most one. If \(L=n\), rank
subadditivity in (7) forces

\[
                         \operatorname{rank}H_j(x)=1          \tag{8}
\]

for every \(j,x\).

Equation (8) rules out a cone vertex on either side. Indeed, if a \(C^1\)
map into a pointed cone passes through zero, its derivative in every
two-sided tangent direction belongs to the cone and its negative, hence
vanishes. The corresponding channel in (6) would have rank zero.

Consequently, under the putative saturation \(L=n\), every diagonal factor
pair consists of nonzero complementary Lorentz-boundary vectors.

## 2. Exact phase-square formula

Every nonzero vector on \(\partial Q_3\) has a unique representation

\[
                       a(1,p),\qquad a>0,\quad p\in S^1.
\]

Complementarity therefore gives globally \(C^1\) functions

\[
\begin{aligned}
 A_j(x)&=a_j(x)(1,p_j(x)),\\
 B_j(x)&=b_j(x)(1,-p_j(x)),
\end{aligned}
\qquad a_j,b_j>0,\quad p_j:M\to S^1.                          \tag{9}
\]

The same phase occurs on both sides because
\(\langle(1,p),(1,-r)\rangle=1-\langle p,r\rangle\), which
vanishes exactly when \(p=r\).

Since \(q\geq2\), \(M\) is simply connected. Each circle-valued phase has a
global \(C^1\) lift

\[
             p_j=(\cos\theta_j,\sin\theta_j),
 \qquad \theta_j:M\to\mathbb R.                              \tag{10}
\]

Differentiating (9), the amplitude-amplitude and both amplitude-phase
terms vanish because

\[
 \langle(1,p_j),(1,-p_j)\rangle=0,
 \qquad \langle p_j,dp_j\rangle=0.
\]

The remaining term is

\[
 H_j(x)=a_j(x)b_j(x)\,dp_j(x)^*dp_j(x)
       =w_j(x)\,d\theta_j(x)^2,
 \qquad w_j=a_jb_j>0.                                       \tag{11}
\]

Thus (7) becomes the exact weighted sum-of-squares identity

\[
                   G=\sum_{j=1}^L w_j\,d\theta_j^2.          \tag{12}
\]

This calculation needs only first derivatives of the two factor maps.

## 3. The joint phase map is an immersion

Define

\[
                    \Theta=(\theta_1,\ldots,\theta_L):
                    M\longrightarrow\mathbb R^L.             \tag{13}
\]

If \(d\Theta(x)u=0\), then every \(d\theta_j(x)u=0\), so (12) gives
\(G_x(u,u)=0\). Positive definiteness of \(G\) forces \(u=0\).
Therefore \(\Theta\) is a \(C^1\) immersion.

For (1), the zero set is exactly the diagonal. More generally, assume a
kernel in (2) has this property. If \(\Theta(x)=\Theta(y)\), then every
phase agrees at \(x,y\), and (9) makes every Lorentz pairing in (2) zero.
Thus \(\sigma(x,y)=0\), so \(x=y\). Hence \(\Theta\) is injective. A
one-to-one immersion of a compact manifold into Euclidean space is an
embedding.

No compact \(n\)-manifold immerses in \(\mathbb R^n\). Such an immersion
would be a local diffeomorphism, hence have open image; compactness would
also make its image compact and closed, which is impossible in connected
\(\mathbb R^n\). Consequently \(L\geq n+1\), contradicting \(L=n\) and
proving (3).

More generally, whenever all factors in (2) are nowhere zero on the contact
diagonal, (9)--(13) directly give

\[
                         L\geq\operatorname{imm\,dim}(M).     \tag{14}
\]

If in addition the kernel vanishes only on the diagonal, the injectivity
argument strengthens (14) to

\[
                         L\geq\operatorname{emb\,dim}(M).    \tag{14a}
\]

For the lower bound (3), nowhere-vanishing need not be assumed: it is forced
by the only excluded case \(L=n\).

## 4. Why the immersion obstruction stops after one extra block

Every finite product of positive-dimensional spheres embeds in Euclidean
space with codimension one. Here is a direct induction.

The map

\[
                \mathbb R\times S^d\longrightarrow
                \mathbb R^{d+1}\setminus\{0\},
 \qquad (t,u)\longmapsto e^t u                              \tag{15}
\]

is a diffeomorphism. Hence, for every \(a\geq1\),

\[
 \mathbb R^a\times S^d
   =\mathbb R^{a-1}\times(\mathbb R\times S^d)
   \hookrightarrow\mathbb R^{a+d}.                           \tag{16}
\]

Starting with
\(\mathbb R\times S^{q_1}\times\cdots\times S^{q_k}\) and applying
(16) one factor at a time gives an embedding into
\(\mathbb R^{1+\sum_iq_i}\). Restricting the initial real coordinate to
zero yields

\[
        S^{q_1}\times\cdots\times S^{q_k}
        \hookrightarrow\mathbb R^{1+\sum_iq_i}.               \tag{17}
\]

Together with the no-immersion-in-equal-dimension argument, (17) proves
(5). This is stronger than merely observing that the product is stably
parallelizable.

For one source block, \(k=1\), (3) matches the coordinate-square
\(Q_3^{q+1}\) factorization. For \(k>1\), separate coordinate-square lifts
use \(n+k\) factors, while topology currently gives only

\[
                              n+1\leq L\leq n+k.              \tag{18}
\]

The lower endpoint of (18) is only a factorization lower bound, not a known
construction.

For full ambient products \(Q_3^L\), the corresponding barrier and ambient
dimension consequences are

\[
                              \nu\geq2(n+1),\qquad
                              M_{\rm amb}\geq3(n+1),           \tag{19}
\]

under the same global-selection hypotheses. Separate smooth lifts attain
\(\nu=2(n+k)\) and \(M_{\rm amb}=3(n+k)\).

## 5. Safe sphere-target submersion constraints

The normalized-boundary argument for a capacity-saturated cone block turns
it into a \(C^1\) submersion

\[
                              (S^q)^k\longrightarrow S^r.     \tag{20}
\]

A complete classification of (20) was not found and is not claimed.
Several rigorous constraints and counterweights are immediate:

1. If \(q\geq2\), then \(r=1\) is impossible. The domain is simply
   connected, so a map to \(S^1\) lifts to a real-valued function and has a
   critical point.
2. If \(q\) is even, \(r\) cannot be odd. Ehresmann makes (20) a fiber
   bundle, and Euler-characteristic multiplicativity would give
   \[
       2^k=\chi((S^q)^k)=\chi(F)\chi(S^r)=0.
   \]
3. If \(k>1\), \(r=n\) is impossible. A same-dimensional submersion is a
   covering of the simply connected sphere and would make \((S^q)^k\)
   diffeomorphic to \(S^n\), contrary to its cohomology.
4. The value \(r=q\) always occurs by coordinate projection.
5. Further targets occur by composing a coordinate projection with a Hopf
   submersion:
   \[
       (q,r)=(3,2),(7,4),(15,8).
   \]

Accordingly, one must not infer that every submersion is a coordinate or
Hopf projection without a separate classification theorem. In particular,
these facts alone do not characterize all saturated rank multisets
\(\{r_i\}\) with \(\sum_i r_i=kq\).

## Literature boundary

Hirsch's foundational immersion theorem classifies immersions by tangent
bundle monomorphisms:

- M. W. Hirsch,
  [*Immersions of Manifolds*](https://doi.org/10.2307/1993453),
  Transactions of the AMS 93 (1959), 242--276.

The codimension-one product-sphere embedding used here is elementary and
is proved explicitly in (15)--(17), so the result does not depend on an
unstated cancellation theorem. Ehresmann's proper-submersion theorem
supplies the bundle step in item 2 above.

A targeted search found the standard cone-factorization framework,
classical sphere and product-sphere immersion theory, and the recent work
of Aubrun--La Piana--Muller-Hermes on factorization of positive maps through
Lorentz cones. It found no source deriving the weighted phase immersion
(12)--(14) from globally smooth \(Q_3\) slack factors or applying the exact
codimension-one immersion dimension as a sharp limitation on smooth
small-cone lower bounds. Apparent novelty remains subject to specialist
review.

## Audit record

An independent hostile audit checked the cone-vertex derivative argument,
the sign and weights in the phase-square identity, the need for globally
liftable circle phases, and the exact codimension-one immersion dimension
of a product of spheres. It also supplied the sharp counterexample at
\(q=1\): coordinate phases on a torus need not lift to real functions, so
the hypothesis \(q\geq2\) is essential. A follow-up audit verified the
embedding upgrade for a common-domain kernel whose zero set is exactly the
diagonal, including the identification of primal and dual phases by
diagonal complementarity.
