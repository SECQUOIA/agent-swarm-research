# Resolving tied reproductive values in optimal daughter dependence

Date: 2026-09-06. Status: candidate extension, independently verified in [the extension review](../reviews/extinction-extension-review.md). The first-order branching asymptotic and optimal transport principle are established ingredients. Novelty of the explicit second-order selection rule is unresolved.

This note extends [the coupling model](extinction-coupling.md) and [the near-critical analysis](extinction-near-critical.md). It identifies one optimal daughter law near criticality even when some leading reproductive values coincide.

## Assumptions and notation

Let P be a finite irreducible stochastic matrix, 0<b_i<1, and M=2 diag(b)P have Perron root 1. Scale division probabilities to (1+ε)b_i for small ε>0, leaving P fixed. Normalize the positive left and right Perron vectors by uᵀ1=uᵀv=1. For each parent i, C_i ranges over all symmetric couplings with marginals p_i. Define the symmetric bilinear vector map

\[
 B_{C,i}(x,y)=b_i\sum_{j,k}C_{i,jk}x_jy_k,
 \quad H_C=B_C(v,v),\quad D_C=u^TH_C,\quad a_C=D_C^{-1}.
\]

Write s_C(ε)=1−q_C(ε) for survival. The exact equation is

\[
 s_C=(1+\epsilon)Ms_C-(1+\epsilon)B_C(s_C,s_C).
\tag{1}
\]

The uniform first-order result gives s_C=εa_Cv+O(ε²), with the constant independent of C. In particular, all D_C are bounded above and bounded away from zero, and uᵀs_C is bounded above and below by positive multiples of ε.

## Lemma: uniform second-order expansion

Let r_C be the unique solution

\[
 (I-M)r_C=a_Cv-a_C^2H_C,\qquad u^Tr_C=0,
\tag{2}
\]

and put

\[
 c_C=-a_C-2a_Cu^TB_C(v,r_C).
\tag{3}
\]

Then uniformly over all admissible C,

\[
 s_C(\epsilon)=\epsilon a_Cv+
 \epsilon^2(r_C+c_Cv)+O(\epsilon^3).
\tag{4}
\]

### Proof

The right side of (2) has zero u projection since a_C−a_C²D_C=0. The restriction of I−M to u⊥ is invertible: irreducibility makes eigenvalue 1 simple, even if M is periodic. The remaining eigenvalues may lie on the unit circle but differ from 1.

Let t=uᵀs_C and y=s_C−tv. Applying the bounded inverse on u⊥ to (1), and using the uniform first-order expansion, gives

\[
 y=\epsilon^2r_C+O(\epsilon^3).
\]

All remainder bounds are uniform because the transport polytopes are compact, B_C is uniformly bounded, and the inverse is fixed. Projecting (1) onto u and dividing by t>0 yields

\[
 \epsilon=(1+\epsilon)
 \left[D_Ct+2u^TB_C(v,y)+\frac{u^TB_C(y,y)}{t}\right].
\]

The final quotient is O(ε³). Substituting y=ε²r_C+O(ε³) and expanding ε/(1+ε)=ε−ε²+O(ε³) gives

\[
 t=\epsilon a_C+
 \epsilon^2[-a_C-2a_Cu^TB_C(v,r_C)]+O(\epsilon^3),
\]

which proves (4).

## Theorem: a lexicographic transport rule is exactly optimal

For each parent type set

\[
 H_i^*=b_i\min_{C_i}\sum C_{i,jk}v_jv_k,
 \quad D^*=u^TH^*,\quad a^*=(D^*)^{-1}.
\]

Compute r* from

\[
 (I-M)r^*=a^*v-(a^*)^2H^*,\qquad u^Tr^*=0.
\tag{5}
\]

Assume all pairs (v_j,r_j*) are distinct. Order the types lexicographically by these pairs. For each parent, pair the specified daughter marginal with itself in opposite quantile order using this type ordering; call the resulting symmetric coupling C_i*.

There exists ε0>0 such that this one family C* minimizes extinction simultaneously for every initial type and every 0<ε<ε0. Thus the rule is an exact optimization result on a neighborhood, not just an optimization of the leading survival coefficient.

### Proof

For each ε the lower extinction envelope is attained by a stationary coupling. More specifically, its fixed point q− permits choosing an attaining family Cε that pairs types in opposite order of q−, equivalently in opposite order of s+=1−q−. The least-fixed-point argument in the basic coupling theorem establishes attainment.

Uniform first-order expansion ensures that, for all small ε, distinct v values have the same order as s+ values, regardless of the attaining family. Hence the chosen antithetic coupling Cε, sorted by s+, is also an antithetic coupling for the v values, possibly with an arbitrary refinement of equal-v groups. It minimizes every row's v-product cost exactly. This step is stronger than the observation that its leading cost is asymptotically optimal; it puts Cε on the exact first-order optimal face.

Every coupling on that face has H_C=H*, D_C=D*, and r_C=r*. By (4), for v_j=v_k,

\[
 s_{C\epsilon,j}-s_{C\epsilon,k}
 =\epsilon^2(r_j^*-r_k^*)+O(\epsilon^3).
\]

The term c_Cv cancels. Uniformity and the distinct-pairs assumption make the sign equal to the sign of r_j*−r_k* for all small ε. Thus the strict ordering of s+ is exactly the specified lexicographic ordering. Its antithetic coupling is C*, independent of ε. Choosing that coupling at q− again gives attainment by the least-fixed-point argument. ∎

## A constructive remainder and interval

Use the constants from the explicit remainder section of [the first-order proof](extinction-near-critical.md), translating its w to this note's u and t to ε. To avoid a collision with a_C, denote its positive lower bound on (uᵀs)/ε by a_lower. Let V=||v||∞ and α=1/D_lo. Define

\[
 K_{y,3}=L\{\|M\|_\infty E+2b_*\alpha VE
                  +b_*E^2\epsilon_0+b_*A^2\},
\]
\[
 K_{t,3}=\frac{1+2\beta V K_{y,3}+\beta K_y^2/a_{\rm lower}}{D_{\rm lo}},
 \qquad K_3=K_{y,3}+VK_{t,3}.
\]

Here ε0 is the probability-valid interval endpoint used to define those constants, before imposing ordering restrictions. These constants give a uniform bound K3 ε³ for the remainder in (4). To check this, put e=s−εa_Cv, ||e||∞≤Eε², in the exact reduced equation. The four cubic remainders come respectively from εMe, the bilinear cross term, B(e,e), and εB(s,s). They give ||y−ε²r_C||∞≤K_y,3 ε³. The projected equation in the lemma and |ε/(1+ε)−ε+ε²|≤ε³ give the displayed K_t,3.

Let δ_v be the minimum positive difference between unequal v values, and δ_r the minimum |r_j*−r_k*| among equal-v pairs. A sufficient interval for the theorem is

\[
 0<\epsilon<\min\{\epsilon_0,
       \delta_v/(2ED_{\rm hi}),\delta_r/(2K_3)\},
\]

omitting a restriction if its set of pairs is empty, and treating a zero error constant as no restriction. The distinct-pairs assumption ensures every required gap is positive. The constants were first derived by the independent reviewer and then checked term by term by the root agent. They are conservative; they do not justify assigning the observed numerical interval to the theorem.

## Concrete three-type example

Take

\[
 P=\begin{pmatrix}.6&.3&.1\\.1&.5&.4\\.2&.3&.5\end{pmatrix},
 \qquad b=(5/11,5/14,2/3).
\]

Then

\[
 u=(11/40,7/20,3/8),\quad v=(8/11,8/11,16/11),
 \quad D^*=56/121.
\]

Exactly r*=(138,−27,−76)/343, and c* for the following policy is −5258/2401. The optimal ordering in zero-based indexing is (1,0,2), resolving the first two equal reproductive values in the opposite order from their original labels. Opposite-quantile pairing then gives

\[
 C_1^*=\begin{pmatrix}.4&.2&0\\.2&0&.1\\0&.1&0\end{pmatrix},\quad
 C_2^*=\begin{pmatrix}0&.1&0\\.1&0&.4\\0&.4&0\end{pmatrix},\quad
 C_3^*=\begin{pmatrix}0&0&.2\\0&0&.3\\.2&.3&0\end{pmatrix}.
\]

The [verification script](../verification/extinction_coupling.py) compares antithetic transport with 120 independently solved linear programs and evaluates both the optimized fixed point and this fixed policy. The [recorded numerical output](../verification/extinction_coupling_results.json) shows agreement below 3×10⁻¹⁴ for ε between .0025 and .04, and second-order approximation errors divided by ε³ between 3.19 and 3.32. This supports the algebra, but it neither proves that .04 is inside the theorem's interval nor certifies floating-point fixed-point error. Near-critical fixed-point iteration is slow and residuals alone are insufficient certificates.

## Limits and open work

The policy requires unrestricted equal-marginal daughter coupling. Additional mechanical constraints can change the optimal transport rule. If two types have both equal v and equal r*, the theorem gives no ordering between them; additional expansion or a structural symmetry argument is needed. The explicit interval above may be much smaller than the true range of optimality.

The basic first-order asymptotic is prior work, as are rearrangement extrema and general branching control. A finite-action polynomial model can also have generic eventual policy stabilization for semialgebraic reasons. The contribution to test against the literature is the explicit Poisson-equation refinement of Perron ordering and its exact optimality, not the mere existence of a stable policy. See [the literature critique](../reviews/extinction-literature.md).
