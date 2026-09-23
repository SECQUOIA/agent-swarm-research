# Exact latent coordinates for additive coagulation: rigidity and minimum dimension

Date: 2026-09-06. Status: independently verified applications of established congruence theory, with additional approximation bounds whose novelty remains unresolved. A deeper [literature audit](../reviews/coarse-graining-literature.md) found a directly applicable theorem of Hofmann–Ruppert (1988). The dimension and rigidity results must not be presented as a new general theory. The elementary proofs are retained for their population-balance interpretation.

## Main findings

An exact smooth coordinate reduction of an additive coagulation equation, valid for every initial population, has parallel affine fibers under a constant-rank assumption. More strongly, among all continuous encoders the minimum number of retained coordinates is the dimension of the global span of collision-kernel gradients. Thus even nonsmooth nonlinear encoders cannot improve on the minimum dimension achieved by a linear projection. A finite-rank collision kernel can still require every physical coordinate.

Adding even very simple component-selective binary fragmentation can increase the required dimension from one to the full number of components. The minimum dimension is then the rank of an explicitly computable invariant-subspace construction. Matching finite-time bounds show that one-coordinate prediction error can nevertheless vanish linearly with the fragmentation rate. These are statements about the dimension of the **particle coordinate**, not finite-dimensional moment closure or finite-dimensional representation of a population distribution.

The event-closure criterion is a version of strong lumpability. The rigidity consequence, dimension characterization, and fragmentation extension follow from established semigroup structure as detailed in the later audit. The combined exact-versus-approximate example and explicit error bounds may remain useful; their publication novelty has not been established.

## 1. Precise scope

Let \(C=(0,\infty)^m\). A particle carries additive component quantities \(x\in C\); aggregation produces \(x+y\). For a symmetric kernel \(K:C\times C\to(0,\infty)\), define the coagulation vector field on finite nonnegative atomic measures by

\[
 Q_K(\mu)=\frac12\iint K(x,y)
 [\delta_{x+y}-\delta_x-\delta_y]\,\mu(dx)\mu(dy).
\tag{1}
\]

An encoder \(h:C\to\mathbb R^d\) is **universally exact** when

\[
 h_\#\mu=h_\#\nu\quad\Longrightarrow\quad
 h_\#Q_K(\mu)=h_\#Q_K(\nu)
\tag{2}
\]

for all such \(\mu,\nu\). This only demands that an autonomous vector field on the observed measure exist; its form is not assumed in advance. Using atomic measures avoids integrability and solution-existence issues. The results concern exact generator closure. For solutions with suitable finite integrals, the resulting weak equation follows by pushforward; global existence, uniqueness, gelation, and post-gelation limits are separate questions.

The strict positivity assumption is substantive. A zero kernel contains no collision information and permits arbitrary encoders. The claims do not rule out accurate approximate reductions, reductions restricted to an invariant manifold or a selected family of initial distributions, density-level autoencoders, memory-dependent models, or finite collections of closed moments. Ordinary particle number is retained because pushforward preserves the total mass of the number measure.

## 2. Event closure from population closure

**Lemma 1.** Condition (2) holds if and only if both of the following are well defined on pairs of encoder values:

\[
 \overline K(h(x),h(y))=K(x,y),\qquad
 H(h(x),h(y))=h(x+y).
\tag{3}
\]

**Proof.** Define the symmetric signed-measure event coefficient

\[
 E(x,y)=K(x,y)[\delta_{h(x+y)}-\delta_{h(x)}-\delta_{h(y)}].
\]

If \(h(x)=h(x')\), condition (2) applied to \(\delta_x,\delta_{x'}\) gives \(E(x,x)=E(x',x')\). Applied to \(\delta_x+\delta_y,\delta_{x'}+\delta_y\), it then gives \(E(x,y)=E(x',y)\). The total mass of \(E(x,y)\) is \(-K(x,y)\), so the kernel agrees. Since it is positive, division and cancellation of the two parent atoms gives \(h(x+y)=h(x'+y)\). Repeat in the other argument. Conversely, substituting (3) into (1) expresses the pushforward using \(h_\#\mu\) alone. ∎

This proof shows why neither state-dependent latent kernels nor stochastic latent offspring rules can circumvent the obstruction while retaining universality: the actual projected event coefficients are fixed by atomic inputs.

## 3. Rigidity of smooth encoder fibers

**Theorem 2.** Suppose \(h\) is \(C^1\), has rank \(d\) at every point, and is universally exact. There is a fixed \((m-d)\)-dimensional linear subspace \(W\subset\mathbb R^m\) such that

\[
 \ker Dh(x)=W\quad\text{for every }x\in C.
\tag{4}
\]

Choose any rank-\(d\) linear map \(A:\mathbb R^m\to\mathbb R^d\) with kernel \(W\). Then

\[
 h=g\circ A\quad\text{on }C,
\tag{5}
\]

where \(g:A(C)\to h(C)\) is a \(C^1\) local diffeomorphism. If every fiber of \(h\) is connected, \(g\) is globally injective and hence a diffeomorphism onto its image.

**Proof.** For \(v\in\ker Dh(x)\), the submersion theorem supplies a \(C^1\) curve \(\gamma\) in the fiber through \(x\), with \(\gamma(0)=x\) and \(\gamma'(0)=v\). For any \(y\in C\), Lemma 1 makes \(h(\gamma(t)+y)\) constant for small \(t\). Thus \(Dh(x+y)v=0\). Equal dimensions give

\[
 \ker Dh(x)=\ker Dh(x+y).
\]

For arbitrary \(x,z\), choose \(u\) with every component larger than the corresponding components of both. Applying the last identity with \(y=u-x\) and \(y=u-z\) proves (4).

Every intersection \((x+W)\cap C\) is convex. Integrating \(Dh\) along line segments proves that \(h\) is constant there and establishes (5). Local linear sections of \(A\) establish that \(g\) is \(C^1\), and the rank condition makes its derivative invertible. A fiber of a local diffeomorphism is discrete. The image under \(A\) of any connected \(h\)-fiber is connected and contained in such a discrete fiber, hence is a singleton. Connected \(h\)-fibers therefore imply injectivity of \(g\). ∎

**Global caveat.** Without connected fibers, global injectivity is false. For example, \(h(x_1,x_2,x_3)=e^{x_1}(\cos x_2,\sin x_2)\) has rank two and satisfies an aggregation law given by complex multiplication, with \(K\equiv1\). Its connected fiber components are parallel lines, but it also identifies periodically separated lines. The minimum-dimension theorem below does not need connected fibers.

## 4. A sharp formula for the minimum latent dimension

Assume additionally that \(K\) is \(C^1\). Let optional \(C^1\) particle observables \(q_1,\ldots,q_s\) be required to factor through \(h\). Define

\[
 V=\operatorname{span}\left(
 \{\nabla_xK(x,y):x,y\in C\}
 \cup\{\nabla q_j(x):x\in C,1\le j\le s\}\right).
\tag{6}
\]

**Theorem 3 (all continuous encoders).** Among continuous universally exact encoders that retain the specified observables, the minimum dimension is exactly

\[
 d_{\min}=\dim V.
\tag{7}
\]

Here dimension zero is allowed and corresponds to retaining particle number alone. If dimensions are required to be positive, replace the minimum by \(\max(1,\dim V)\) when \(m\ge1\).

**Proof of the lower bound.** Write r=dim V. Choose r linearly independent gradient witnesses from (6), with evaluation points z_1,…,z_r. Each witness is the gradient of either K(·,y_l) for a fixed y_l or a retained observable q_j. Choose x_0∈C strictly below every z_l componentwise, and put a_l=z_l−x_0∈C. Define C¹ scalar probes f_l(x)=K(x+a_l,y_l) or q_j(x+a_l), respectively. By construction the map F=(f_1,…,f_r) has derivative of rank r at x_0.

Lemma 1 did not require smoothness or continuity of h. Its additive congruence implies h(x+a_l)=h(x'+a_l) whenever h(x)=h(x'). Consequently every f_l has the same value at x,x' when their encodings agree: each probe factors set-theoretically through h. No continuity of the resulting decoder is assumed or needed.

Choose an r-dimensional affine slice through x_0 complementary to ker DF(x_0). By the inverse-function theorem, F is injective on a neighborhood in that slice. Hence h is also injective there. A continuous injection from an open subset of R^r into R^d requires d≥r. Indeed, if d<r, compose it with the coordinate inclusion R^d→R^r; invariance of domain would make the image open in R^r although it lies in a subspace with empty interior. This contradiction proves the lower bound. The case r=0 is immediate.

**Proof of attainment.** Take the rows of \(A\) to be an orthonormal basis of \(V\). Each segment joining points of a common \(A\)-fiber lies in \(C\), and integrating gradients along it shows that \(K\) factors through \(Ax\) in the first argument. Symmetry gives the second argument. Every \(q_j\) likewise factors through \(A\). Addition satisfies \(A(x+y)=Ax+Ay\), so Lemma 1 proves exactness. ∎

This strengthening was developed by the root agent and independently checked by `closure_direction` and `extinction_proof`. It allows continuous encoders with singular derivatives, varying rank, or no derivative. The smooth fiber-rigidity theorem remains useful for the general fragmentation formula below; Theorem 4b separately removes smoothness for the total-mass example. Continuity is substantive: a discontinuous measurable injection can encode a multicomponent state in one real number without losing information, so Euclidean coordinate count alone would cease to express meaningful dimensional reduction.

**Example 1: a low-rank kernel with no dimension reduction.** On \((0,\infty)^m\), set \(f(x)=\prod_{i=1}^m x_i\) and

\[
 K(x,y)=1+f(x)f(y).
\]

The separated kernel rank is two. Nevertheless, \(\nabla f(x)=f(x)(1/x_1,\ldots,1/x_m)\) spans \(\mathbb R^m\), so \(d_{\min}=m\). Fast low-rank evaluation of pair rates is therefore distinct from exact dimension reduction of particle states. This polynomial example is a generator statement and does not claim global nongelating dynamics. A bounded version replaces \(f\) by \(f/(1+f)\); its gradients are positive scalar multiples of \(\nabla f\), preserving the conclusion and giving \(1<K<2\).

**Example 2: exact total-mass reduction.** If \(K(x,y)=\kappa(c^Tx,c^Ty)\), \(c_i>0\), and the global kernel gradients span \(\operatorname{span}\{c\}\), then one coordinate \(c^Tx\) is optimal for pure coagulation.

## 5. Fragmentation can force hidden composition back into the state

Fix a constant rate \(a>0\) and a diagonal matrix \(R\) with entries in \((0,1)\). Let

\[
 F_R(\mu)=a\int
 [\delta_{Rx}+\delta_{(I-R)x}-\delta_x]\,\mu(dx).
\tag{8}
\]

This represents a component-selective binary split; both daughters remain in \(C\), and every component is conserved in each event. Consider universal closure of \(Q_K+F_R\).

**Theorem 4.** With \(V\) from (6), define

\[
 V_\infty=\operatorname{span}\{(R^T)^k v:v\in V,\ 0\le k\le m-1\}.
\tag{9}
\]

The minimum smooth full-row-rank encoder dimension for the combined equation, retaining the specified observables, is exactly \(\dim V_\infty\).

**Proof.** Scaling both populations in a closure comparison by arbitrary \(c>0\) separates the quadratic term \(c^2Q_K\) and linear term \(cF_R\). Thus both operators close separately, and Theorem 2 provides the fixed subspace \(W\).

For \(w\in W\), the curve \(x+tw\) remains in the same encoder fiber for small \(t\). Fragmentation closure on atomic inputs gives a constant measure

\[
 \delta_{h(R(x+tw))}+\delta_{h((I-R)(x+tw))}.
\]

Each continuous child-encoder curve takes values in the fixed set of at most two atoms of this measure. It is therefore constant. Differentiating the first curve yields \(Rw\in\ker Dh(Rx)=W\). Consequently, \(RW\subset W\), or equivalently \(W^\perp\) is \(R^T\)-invariant. It contains \(V\), so it contains \(V_\infty\). Cayley–Hamilton shows that (9) is the smallest such invariant subspace.

Conversely, let the row space of \(A\) equal \(V_\infty\). Theorem 3's argument closes coagulation and retains the observables. Invariance gives a matrix \(B\) with \(AR=BA\), and then \(A(I-R)=(I-B)A\). Both daughter coordinates are determined by \(Ax\), which proves fragmentation closure. ∎

**Example 3: one coordinate becomes all components.** Set \(c=(1,\ldots,1)^T\) and

\[
 K(x,y)=1+\frac{c^Tx}{1+c^Tx}\frac{c^Ty}{1+c^Ty}.
\]

Pure coagulation has \(d_{\min}=1\). If the split fractions \(r_1,\ldots,r_m\) are all distinct, the vectors \(c,R^Tc,\ldots,(R^T)^{m-1}c\) form a Vandermonde matrix of rank \(m\). Every universally exact smooth encoder for coagulation plus this bounded-rate fragmentation therefore needs all \(m\) coordinates. If there are exactly \(\ell\) distinct split fractions, the optimal dimension is exactly \(\ell\); one may retain total component amount within each equal-fraction group.

The result applies however small the positive fragmentation rate is. At \(a=0\), the exact minimum drops to one. This is a discontinuity of **exact** reducibility; it is not a claim that approximation error remains large as \(a\to0\). Sections 6–7 quantify that distinction.

### The dimension jump also holds for all continuous encoders

**Theorem 4b.** For the bounded total-mass kernel in Example 3 and pairwise distinct split fractions, every continuous universally exact encoder for Q_K+F_R has d≥m. The identity encoder attains this bound. Thus the one-to-m dimension jump does not require differentiability, constant rank, or smooth latent dynamics.

**Proof.** As in Theorem 4, scaling separates closure of Q_K and F_R. Lemma 1 and strict monotonicity of s/(1+s) imply that total size s(x)=1ᵀx is determined by h(x): fix any y and compare K(x,y) when two encodings agree.

Define the positive linear offspring operator T=I+F_R/a, so Tδ_x=δ_Rx+δ_(I−R)x. Fragmentation closure implies that h#Tμ depends only on h#μ for finite nonnegative atomic μ. Because T preserves that class, induction makes h#T^kδ_x depend only on h(x). Since size is determined by the encoding, the following descendant-size multiset is also determined, with the indicated multiplicities:

\[
 \left\{c_{k,j}^Tx\text{ repeated }\binom{k}{j}\text{ times}:
      0\le j\le k\right\},\qquad
 (c_{k,j})_i=r_i^j(1-r_i)^{k-j}.
\]

All measures in this argument are finite atomic, so applying the size decoder requires no unproved measurability assertion.

For each k=1,…,m−1 and j<k, c_k,k−c_k,j is nonzero. Indeed its i-th entry vanishes precisely when r_i=1/2. When m≥2, distinct fractions cannot all equal 1/2. Choose x_0 in the positive cone outside the finitely many proper hyperplanes (c_k,k−c_k,j)ᵀx=0. At x_0, each all-R descendant size c_k,kᵀx_0 is separated from the other generation-k sizes. By continuity, there is a neighborhood U of x_0 on which each such size remains in an isolating interval disjoint from all competing generation-k sizes.

If x,x'∈U have h(x)=h(x'), their descendant-size multisets agree. The isolated atoms therefore agree, giving

\[
 \sum_i r_i^k x_i=\sum_i r_i^k x_i',\qquad k=0,\ldots,m-1.
\]

The k=0 equality is the initial total size. The Vandermonde matrix is invertible, so x=x'. Thus h is a continuous injection on U. Invariance of domain, in the form used in Theorem 3, yields d≥m. When m=1, size alone yields the bound. ∎

The multiset-isolation argument was proposed by `closure_direction`, developed by the root agent, and independently verified by `extinction_proof`; see [the continuous-encoder review](../reviews/coarse-graining-continuous-review.md).

**Stronger attributed corollary.** The later audit establishes that the general formula d_min=dim V_infinity in Theorem 4 also holds for every continuous encoder. Hofmann–Ruppert, *The foliation of semigroups by congruence classes* (1988), Proposition 16, Corollary 19, and Theorem 21 provide a fixed subspace W whose affine slices lie in the fibers globally and equal the local fibers near zero. Applying the finite-support offspring argument near zero gives RW⊂W without differentiating h. Invariance of domain supplies d≥codim W≥dim V_infinity, and the same linear projection attains equality. The [full deduction and exact source assumptions](../reviews/coarse-graining-literature.md) were independently verified. Theorem 4b remains a self-contained proof for the concrete example.

**State-dependent rate extension.** Theorem 4 also holds for a strictly positive \(C^1\) rate \(a(x)\), provided the initial subspace \(V\) also includes every \(\nabla a(x)\). Indeed, the total number change in a fragmentation event is \(a(x)\), so closure first forces equal rates on encoder fibers; dividing by that common positive rate recovers the two-atom argument. The quantitative results below use a constant rate.

## 6. Finite-time accuracy despite discontinuous exact dimension

Write \(s(x)=\mathbf1^Tx\). Suppose
\[
 K(x,y)=\kappa(s(x),s(y)),\qquad
 0<k_-\le\kappa\le k_+,
\]
and \(\kappa\) is separately Lipschitz with constant \(L_\kappa\). Let \(\mu_t\) solve the full vector equation with constant-rate fragmentation (8), and let \(\lambda_t=s_\#\mu_t\). A one-coordinate approximation \(\nu_t\) uses the same coagulation kernel and replaces the two daughter sizes by
\[
 \bar r z,\quad(1-\bar r)z,\qquad \bar r\in(0,1).
\]
Initialize it with \(\nu_0=\lambda_0\). Define
\[
 N_0=\mu_0(C),\quad M_1=\int s(x)\,\mu_0(dx)<\infty,\quad
 \delta=\max_i|r_i-\bar r|,
\]
\[
 N_*=\max(N_0,2a/k_-),\quad
 C_\kappa=\max(3k_+,3L_\kappa+2k_+),\quad
 L=C_\kappa N_*+3a.
\]
Use the bounded-Lipschitz dual norm
\[
 \|\eta\|_{\mathrm{BL}^*}
 =\sup_{\max(\|\phi\|_\infty,\operatorname{Lip}\phi)\le1}
 \left|\int\phi\,d\eta\right|.
\]
The size coordinate and this metric are understood in fixed units, or after nondimensionalization.

**Theorem 5.** The two equations have unique global nonnegative finite-measure solutions with finite first mass moment. They conserve \(M_1\), and for every \(t\ge0\),
\[
 \boxed{\quad
 \|\lambda_t-\nu_t\|_{\mathrm{BL}^*}
 \le 2a\delta M_1\,\frac{e^{Lt}-1}{L}.
 \quad}
\tag{10}
\]
When \(L=0\), the quotient is interpreted as \(t\). The bound is uniform over hidden composition distributions with the given \(N_0,M_1\).

**Proof.** On the Banach space with weighted total variation \(\int(1+s)\,d|\mu|\), bounded \(K\) makes \(Q_K\) locally Lipschitz, and fragmentation is bounded linear. The gain-loss form preserves positivity. The linear functional \(\mu\mapsto\int s\,d\mu\) is bounded on this space and annihilates both event operators exactly, so \(M_1\) is constant. Number satisfies
\[
 N'\le aN-\tfrac12 k_-N^2,
\]
giving \(N(t)\le N_*\). Together these estimates prevent finite-time blowup of the weighted norm and continue the local solution globally. The same proof applies to the scalar approximation.

Coagulation commutes exactly with the total-size projection. For a test function in the BL unit ball, the difference between true and approximate fragmentation births at a parent \(x\) is bounded by
\[
 a\left(
 |r^Tx-\bar r s(x)|+
 |(\mathbf1-r)^Tx-(1-\bar r)s(x)|
 \right)
 \le2a\delta s(x).
\]
Integration gives a residual norm at most \(2a\delta M_1\).

For fixed \(y\), the function
\[
 z\longmapsto\kappa(z,y)
 [\phi(z+y)-\phi(z)-\phi(y)]
\]
has supremum norm at most \(3k_+\) and Lipschitz constant at most \(3L_\kappa+2k_+\). Polarizing the quadratic operator therefore yields
\[
 \|Q_\kappa(\lambda)-Q_\kappa(\nu)\|_{\mathrm{BL}^*}
 \le C_\kappa\frac{N_\lambda+N_\nu}{2}
 \|\lambda-\nu\|_{\mathrm{BL}^*}.
\]
The scalar fragmentation adjoint maps \(\phi\) to
\[
 a[\phi(\bar rz)+\phi((1-\bar r)z)-\phi(z)],
\]
whose supremum norm is at most \(3a\) and Lipschitz constant at most \(2a\). Its operator norm is thus at most \(3a\). Applying these estimates to the integral equation and then Grönwall proves (10). ∎

Choosing \(\bar r=(\min_i r_i+\max_i r_i)/2\) minimizes \(\delta\). The estimate is \(O(a\delta)\) on every fixed time interval, while Theorem 4 may still require all coordinates for each \(a>0\) and every set of distinct fractions. The one-coordinate approximation preserves both the event count and each event's total mass. Formula (10) certifies its distribution error; it does not certify unbounded tail observables from this metric alone.

## 7. A lower bound for every model using only the initial size distribution

The following obstruction needs only a symmetric Borel-measurable kernel with \(k_-\le\kappa\le k_+\); Lipschitz regularity of \(\kappa\) is unnecessary because the proof uses total variation.

Take \(x,x'\in C\) with \(s(x)=s(x')=z\), and set
\[
 D_0=\delta_{r^Tx}+\delta_{z-r^Tx}
       -\delta_{r^Tx'}-\delta_{z-r^Tx'},\qquad
 D=\|D_0\|_{\mathrm{BL}^*}.
\]
If the two unordered daughter-size pairs differ, \(D>0\). Let \(\lambda_t^x,\lambda_t^{x'}\) be the projected solutions from \(\delta_x,\delta_{x'}\). Both observed initial measures equal \(\delta_z\).

**Theorem 6 (uniform small-rate obstruction).** Fix \(a_0,T>0\), and define
\[
 \widehat N=\max(1,2a_0/k_-),\quad
 B=\tfrac32 k_+\widehat N^2+3a_0\widehat N,\quad
 L_Q=3k_+\widehat N,
\]
\[
 C_T=3\widehat N L_Qe^{L_QT}+3B.
\]
For every \(0\le a\le a_0\) and \(0\le t\le T\),
\[
 \|\lambda_t^x-\lambda_t^{x'}-atD_0\|_{\mathrm{BL}^*}
 \le aC_Tt^2.
\tag{11}
\]
Consequently, every deterministic prediction \(\widehat\lambda_t\) that receives only the common initial size distribution and the model parameters satisfies
\[
 \max\left(
 \|\widehat\lambda_t-\lambda_t^x\|_{\mathrm{BL}^*},
 \|\widehat\lambda_t-\lambda_t^{x'}\|_{\mathrm{BL}^*}
 \right)
 \ge \frac a2(Dt-C_Tt^2).
\tag{12}
\]
In particular, for \(t\le\min(T,D/(2C_T))\), its worst-case error is at least \(aDt/4\). This allows an arbitrary predictor, including one with memory; it only assumes that its available initial information is identical in the two experiments.

**Proof.** Every vector solution has number at most \(\widehat N\) and total-variation speed at most \(B\). The scalar coagulation operator is TV-Lipschitz, on this number-bounded set, with constant \(L_Q\). Write fragmentation as \(aF_1\), where \(\|F_1\|_{\mathrm{TV}\to\mathrm{TV}}\le3\), and let \(\Delta_t=\lambda_t^x-\lambda_t^{x'}\). Its integral equation gives
\[
 \|\Delta_t\|_{\mathrm{TV}}
 \le6a\widehat N\,\frac{e^{L_Qt}-1}{L_Q}.
\]
The coagulation contribution to \(\Delta_t\) is therefore bounded by
\[
 L_Q\int_0^t\|\Delta_u\|_{\mathrm{TV}}\,du
 \le3a\widehat N L_Q e^{L_QT}t^2.
\]
Subtracting the initial fragmentation contribution \(atD_0\), the remaining fragmentation contribution has TV norm at most
\[
 3a\int_0^t
 \big(\|\mu_u^x-\delta_x\|_{\mathrm{TV}}
 +\|\mu_u^{x'}-\delta_{x'}\|_{\mathrm{TV}}\big)\,du
 \le3aBt^2.
\]
Since the BL dual norm is at most total variation, these estimates prove (11). The triangle inequality proves (12). ∎

**Explicit two-component witness.** Let \(r=(1/4,3/4)\), \(x=(1,1)\), and \(x'=(1/2,3/2)\). Both parents have total size two. Their daughter pairs are \(\{1,1\}\) and \(\{3/4,5/4\}\). Here \(D=1/2\): coupling each off-center atom to size one gives the upper bound \(1/2\), and \(\phi(z)=\min(|z-1|,1)\) attains it. Thus every predictor based only on initial sizes has an explicit worst-case lower bound \(at/8\) for the stated short-time interval. Together with (10), this gives matching linear dependence on a small positive fragmentation rate, without confusing exact irreducibility with poor approximation.

## 8. Open-literature audit and novelty limits

The comparisons below record the initial search. They are superseded on the main novelty question by the [adversarial semigroup audit](../reviews/coarse-graining-literature.md). That audit inspected [Hofmann–Ruppert (1988)](https://doi.org/10.1007/BF01318680) and [Keimel (1971)](https://doi.org/10.1007/BF02572953), which supply directly applicable affine-congruence results. Absence of the formulas in the initial PBE/ODE search does not establish novelty.

The literature comparison must distinguish a map of individual-particle states from a map of a discretized population vector or a finite set of moments.

- [Li, Rabitz, and Tóth, *A general analysis of exact nonlinear lumping in chemical kinetics* (1994)](https://doi.org/10.1016/0009-2509(94)87006-3) establishes general conditions for nonlinear ODE lumping. Its general fiber-invariance principle predates this note. The full article still needs detailed theorem-by-theorem comparison.
- [Horstmeyer and Atay, *Characterization of exact lumpability for vector fields on smooth manifolds* (2016), full open text](https://arxiv.org/html/1607.01237) was read directly. Proposition 1 states the descended-vector-field criterion; Theorem 4 and Corollaries 5–6 characterize invariance of the tangent kernel; Proposition 10 gives a rank criterion. Their setting is a finite-dimensional smooth vector field, with curved-fiber examples in Section 3. The present argument obtains invariance under **every positive translation** from coagulation events and then forces the tangent kernel to be spatially constant. That specialization and the collision-gradient minimum are absent from the inspected text. This comparison supports a narrower candidate claim than a new general lumpability theory.
- [Ovchinnikov et al., *CLUE: exact maximal reduction of kinetic models by constrained lumping of differential equations* (2021)](https://academic.oup.com/bioinformatics/article/37/12/1732/6126795) computes minimal constrained **linear** lumpings of polynomial ODEs. The invariant-subspace calculation in Theorem 4 is related linear algebra; the proposed new content is why all smooth particle-coordinate encoders must obey it in this coagulation setting.
- [Gupta et al., *Solving High-Dimensional Population Balance Equations via Dynamics-Preserving Autoencoders* (2026)](https://doi.org/10.64898/2026.08.09.743783), [local paper record](../../literature/papers/gupta2026-solving-high-dimensional-population-balance/paper.md), motivates latent particle-coordinate models. Its demonstrated model is a macrophage drift/diffusion model. Our aggregation obstruction does not apply directly to that example and is not a criticism of its reported numerical approximation.
- [Muneer et al., *Exact Method of Moments for multi-dimensional population balance equations* (2023)](https://arxiv.org/abs/2304.10761), [local paper record](../../literature/papers/muneer2023-exact-method-of-moments-for/paper.md), uses characteristic growth without aggregation or breakage and reconstructs a full distribution. That reduction is outside the scope of the present impossibility statements.
- [*A new efficient framework for reduced two-dimensional nonlinear aggregation population balance models*, DOI 10.1016/j.ces.2026.124884](https://www.sciencedirect.com/science/article/pii/S000925092601599X) is a directly adjacent recent source, indexed online in August 2026 with a 2027 volume date. The openly exposed abstract assumes that the aggregation kernel depends on granule volume and time but not tracer volume, and describes two coupled one-dimensional tracer/size balances and a conservative discretization. This is consistent with the projection sufficiency in Theorem 3. The abstract does not state a necessity result against arbitrary nonlinear particle encoders. Full text was not accessible in this audit, so that comparison remains incomplete.
- [Ackleh, Lyons, and Saintier, *A structured coagulation-fragmentation equation in the space of Radon measures: unifying discrete and continuous models* (2021)](https://doi.org/10.1051/m2an/2021061), [open full paper](https://ri.conicet.gov.ar/bitstream/handle/11336/162720/CONICET_Digital_Nro.b062eefd-16e1-49c0-bccc-d8b9a53813fa_A.pdf?isAllowed=y&sequence=2), develops bounded-Lipschitz measure well-posedness and stability for structured coagulation-fragmentation. Its Section 3 supplies relevant prior art for the stability machinery used in (10). Neither the choice of BL metric nor the Grönwall argument is claimed new here; the useful addition is the explicit hidden-composition residual paired with an exact dimension obstruction and a uniform small-rate lower bound.

Searches on 2026-09-06 included “coagulation lumpability”, “coagulation semigroup homomorphism”, “population balance nonlinear lumping”, “multicomponent coagulation reduction”, “coagulation linear projection exact”, and “multicomponent fragmentation dimension reduction”. They located no exact match to Theorems 2–4, but most results used “coagulation” for blood chemistry or Smoluchowski diffusion, making this a limited negative search. More targeted citation-chain work is needed before a publication-level novelty claim.

## 9. Verification and next steps

- [Durable independent proof review](../reviews/coarse-graining-proof.md) records the hypotheses and exact theorem versions reviewed. [Exact-arithmetic verification script](../verification/coarse_graining_atomic.py) checks representative invariant-subspace ranks, the bounded rank-two kernel example, and the two-component BL derivative gap. Run with Python 3; it uses only the standard library. The script was run successfully on 2026-09-06 and returned ranks \(4,2,1\), derivative gap \(1/2\), and short-time lower coefficient \(1/8\).
- Independent reviewer `/root/closure_direction/review_rigidity` verified Lemma 1 and Theorems 2–4, then separately verified Theorems 5–6 and their constants. The reviewer emphasized all positive atomic population masses, the zero-dimensional constant-kernel case, and the distinction between local and global encoder reparametrization; these qualifications are included above. The reviewer also proposed the state-dependent fragmentation-rate extension, which was checked and added.
- The geometric lumpability full text was compared. Obtain and compare the full 1994 nonlinear chemical-lumping article and the recent tracer-reduction paper before claiming publication novelty.
- Search composition-dependent aggregation and multidimensional fragmentation papers for equivalent quotient classifications.
- The finite-time bounds in Sections 6–7 resolve the small-fragmentation continuation at the bounded-kernel level. Improve the long-time constants or extend to physically unbounded kernels only when a clear application justifies the extra analysis.
- Investigate whether positivity only on a connected collision graph suffices for a weaker local rigidity theorem. Do not silently replace strict positivity by nonnegativity.
- Derive constructive compression with an auditable error when the gradient span has small but nonzero singular values. Exact rank alone may be too brittle to guide numerical practice.
