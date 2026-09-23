# Near-critical survival and optimal daughter dependence

Date: 2026-09-06. Status: independently verified candidate result; see [the extension review](../reviews/extinction-extension-review.md) and [the literature audit](../reviews/extinction-literature.md). The ordinary near-critical branching expansion is not claimed as new. The candidate contribution is the explicit uniform error certificate and identification of an exact optimal daughter coupling on a specified interval. Publication novelty remains uncertain.

## Setting and normalization

Use the binary offspring model and full symmetric equal-marginal coupling sets from [extinction-coupling.md](extinction-coupling.md). Fix an irreducible matrix

\[
 M_0=2\operatorname{diag}(b^0)P,\qquad \rho(M_0)=1,
 \qquad 0<b_i^0<1.
\]

Here P is row stochastic. Let b_i(t)=(1+t)b_i^0, and choose t_0>0 with (1+t_0)max_i b_i^0<1. Thus the death probabilities remain positive for 0≤t≤t_0. All daughter marginals P remain fixed. Let v,w>0 satisfy

\[
 M_0v=v,\qquad w^TM_0=w^T,\qquad
 \sum_iw_i=1,\qquad w^Tv=1.
\]

For a coupling family C define the symmetric bilinear map

\[
 B_{C,i}(x,y)=b_i^0\sum_{j,k}C_{i,jk}x_jy_k,
 \qquad D_C=w^TB_C(v,v).
\]

Let x_C(t)=1-q_C(t) be eventual survival from each starting type. Its exact equation is

\[
 x_C=(1+t)M_0x_C-(1+t)B_C(x_C,x_C).
 \tag{1}
\]

It is the greatest fixed point in the unit cube of the map on the right. This follows by transforming the least-fixed-point characterization of extinction.

## Theorem 1: expansion uniform over every admissible coupling

There is a finite constant E, determined by M_0 and t_0 and independent of C, such that

\[
 \left\|x_C(t)-\frac{t}{D_C}v\right\|_\infty\leq Et^2,
 \qquad 0<t\leq t_0.
 \tag{2}
\]

If necessary t_0 may be decreased to meet the stated probability constraint. The proof below in fact produces a bound on the entire chosen interval. In particular the assertion also holds for couplings C=C(t) selected separately at each t. Irreducibility is sufficient; aperiodicity is unnecessary.

### Proof

Write H_C,t for the right side of (1). On the unit cube it is monotone: its i-th component is the expected value of b_i(t)(x_J+x_K-x_Jx_K), and this expression is increasing in both coordinates. For small enough η>0, depending on t,

\[
 H_{C,t}(\eta v)-\eta v
 =t\eta v-(1+t)\eta^2B_C(v,v)\geq0.
\]

We may choose ηv≤1 and η>0. Iterating from this subsolution proves that the greatest fixed point x is positive in every coordinate.

Choose, for every ordered pair (i,j), a directed path from i to j with positive entries of P, using the empty path when i=j. Let c>0 be the minimum of the products of b_k^0p_{k\ell} along these finitely many paths, including 1 for empty paths. Then c≤1. Since u+v-uv≥(u+v)/2 for u,v∈[0,1], equation (1) gives

\[
 x_i\geq b_i^0\sum_jp_{ij}x_j.
\]

Following a chosen path proves min_i x_i≥c max_i x_i, uniformly over C and t. With s=w^Tx and \beta=\sum_iw_ib_i^0, this implies

\[
 cs\leq x_i\leq s/c.
 \tag{3}
\]

Multiplying (1) by w^T gives the exact projection identity

\[
 ts=(1+t)w^TB_C(x,x).
 \tag{4}
\]

Consequently

\[
 \frac{tc^2}{(1+t)\beta}\leq s
 \leq\frac{t}{(1+t)\beta c^2}.
 \tag{5}
\]

Thus x=O(t), and s is bounded below by a positive multiple of t, uniformly over the entire coupling set.

Set y=x-sv, so w^Ty=0. Because 1 is a simple eigenvalue of the irreducible matrix M_0, I-M_0 is invertible on the subspace w^Ty=0. Equation (1) implies

\[
 (I-M_0)y=tM_0x-(1+t)B_C(x,x)=O(t^2).
\]

The inverse is fixed, hence y=O(t²) uniformly in C. Substitute x=sv+y into (4):

\[
 ts=(1+t)\{s^2D_C+2s\,w^TB_C(v,y)+w^TB_C(y,y)\}.
\]

The bound s≥constant·t permits division by s. The last two terms after division are O(t²). Moreover

\[
 0<D_{\rm lo}:=\beta(\min_jv_j)^2
 \leq D_C\leq\beta(\max_jv_j)^2=:D_{\rm hi}.
\]

It follows that s=t/D_C+O(t²), uniformly in C, and x=sv+y proves (2).

### Explicit remainder constant

The following constants make the uniformity constructive, although they need not be numerically sharp. All matrix norms below are induced infinity norms. Set

\[
 a=\frac{c^2}{(1+t_0)\beta},\quad
 A=\frac1{\beta c^3},\quad b_* =\max_i b_i^0,
 \quad
 L=\left\|(I-M_0+vw^T)^{-1}(I-vw^T)\right\|_\infty,
\]

\[
 K_y=L\{\|M_0\|_\infty A+(1+t_0)b_*A^2\},
\]

\[
 K_p=(1+t_0)\beta\{2\|v\|_\infty K_y+K_y^2t_0/a\},
 \qquad
 E=K_y+\|v\|_\infty\frac{K_p+1}{D_{\rm lo}}.
\]

Indeed (5) gives s≥at and \|x\|∞≤At; the reduced inverse gives \|y\|∞≤K_yt². Dividing (4) by s yields |t−(1+t)D_Cs|≤K_pt². Therefore |s−t/D_C|≤(K_p+1)t²/D_lo, as claimed. For m=1, the reduced inverse is zero and the same formulas remain meaningful.

## Theorem 2: sharp first-order dependence bounds

Let Q_i^v be the quantile function of v_J with J distributed as p_i. Then

\[
 D_{\min}=\sum_iw_ib_i^0\int_0^1Q_i^v(u)Q_i^v(1-u)\,du,
 \qquad
 D_{\max}=\sum_iw_ib_i^0\sum_jp_{ij}v_j^2.
\]

The minimum is attained by pairing opposite quantiles of the daughters' Perron reproductive values. The maximum is attained by identical sister types. If q^- and q^+ are the sharp extinction envelopes, then

\[
 1-q^-(t)=\frac{t}{D_{\min}}v+O(t^2),\qquad
 1-q^+(t)=\frac{t}{D_{\max}}v+O(t^2).
\]

The remainders are uniform. For the first formula, apply (2) to the stationary optimizer guaranteed by the lower-envelope theorem and to a fixed D-minimizing coupling, then sandwich componentwise. The second follows directly from the diagonal optimizer. Thus the leading ratio of maximal to minimal survival is D_max/D_min, the same for every initial type.

This is transport of reproductive values, not necessarily transport of the measured size, phenotype label, or growth rate. An applied interpretation requires knowing how the mean offspring matrix assigns reproductive value to those measurements.

## Theorem 3: a fixed coupling is exactly optimal near criticality

Suppose the components of v are pairwise distinct, and let C^anti be the symmetric antithetic type coupling obtained by sorting types by v_j, separately using each row marginal p_i. Then there exists t_*>0 such that

\[
 q_{C^{\rm anti}}(t)=q^-(t),\qquad 0<t<t_*.
\]

Thus this one family of couplings minimizes the exact eventual extinction probability simultaneously for every starting type and every sufficiently small positive distance from criticality.

### Proof

For m≥2, put \delta=\min_{j\ne k}|v_j-v_k|>0. By (2), every admissible C satisfies, whenever v_j>v_k,

\[
 x_{C,j}(t)-x_{C,k}(t)
 \geq t\delta/D_{\rm hi}-2Et^2.
\]

Hence for 0<t<t_*:=min{t_0,\delta/(2ED_hi)} every survival vector has the strict order of v, and every extinction vector has its reverse order. If E=0, omit the second restriction. The case m=1 is immediate.

In particular q^-(t), which is attained by a stationary admissible family, has the reverse order of v. The antithetic coupling C^anti minimizes every row's transport objective evaluated at q^-(t): the rearrangement minimizer depends only on the order of the scalar values and the fixed marginal masses, and reversing the full order leaves the symmetric antithetic matrix unchanged. Therefore

\[
 F_{C^{\rm anti}}(q^-(t))=q^-(t).
\]

The least-fixed-point property gives q_Canti≤q^-, and the universal lower bound gives the reverse inequality. This proves exact optimality. The theorem asserts existence of an optimal family, not uniqueness of the type-level coupling.

## Boundaries and open checks

- Equal Perron values do not invalidate Theorems 1–2. They prevent the first-order proof of exact order stability; higher-order terms can decide ordering within a tie.
- If v is constant, the first-order survival coefficient is independent of daughter dependence. Under the present normalization v=1, criticality then forces b_i^0=1/2 for every i. In fact total population size is then the same one-type binary process for all couplings, so extinction is exactly independent of C for every admissible t.
- The scaling b_i(t)=(1+t)b_i^0 is an explicit model assumption, not a consequence of arbitrary perturbations of the mean matrix. More general perturbations require a different coefficient and additional notation.
- First-order expansions of nearly critical multitype branching survival are classical. This derivation establishes correctness and uniformity for the present problem; it does not establish novelty. The exact fixed-coupling stability conclusion and its broader impact require targeted literature review.
- Eventwise conservation constraints generally change the optimizing transport problem and can remove the order-only characterization needed by Theorem 3. The uniform expansion itself still applies to restricted nonempty coupling sets with these same marginals.
