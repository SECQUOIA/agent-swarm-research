# Independent review of the continuous-encoder dimension bounds

Date: 2026-09-06. Reviewer: independently assigned `extinction_proof` agent. Scope: Theorem 3 in `research/ideas/coarse-graining.md` and the proposed continuous-encoder version of its distinct-fraction fragmentation example.

## Verdict

Both arguments are correct under the stated hypotheses. Neither needs differentiability of the encoder or continuity of a decoder. The fragmentation argument also does not assume that closure initially identifies the two labeled daughters separately: it uses only the observable **unordered offspring measures**, their positive iterates, and local isolation of one branch. This distinction is essential.

These are mathematical verification conclusions. This review does not establish literature novelty or publication impact.

## Theorem 3: translated probes and topological dimension

The finite-gradient-witness argument is valid.

1. A basis can be selected from the generating collection of gradients because the ambient space is finite dimensional. If there are r witnesses, choose x_0 with every coordinate positive and strictly smaller than the corresponding coordinate of every evaluation point. The finitely many positive translations a_l then put all witnesses at one common point without changing their gradient values.
2. Lemma 1 supplies the additive congruence h(x)=h(x') ⇒ h(x+a)=h(x'+a). Its proof uses no encoder regularity. Kernel closure and the assumed retention of each q_j show that every translated scalar probe has equal values whenever the encodings agree.
3. The resulting map F is C^1, which is enough for the inverse-function theorem. The word “smooth” in the current proof should be read as C^1; no higher regularity has been assumed or used.
4. Restricting F to an r-dimensional affine slice complementary to its derivative kernel gives a local C^1 diffeomorphism into R^r. On the same neighborhood, h must be injective, because equality under h forces equality under F.
5. Invariance of domain proves d≥r for a continuous h. In detail, if d<r, composing the injection into R^d with its coordinate inclusion into R^r gives a continuous injection from an open subset of R^r to R^r. Its image would be open but contained in a proper linear subspace. The r=0 case needs no topological argument.
6. Linear attainment is valid on the convex cone C: vanishing directional derivatives along a common A-fiber imply constancy along every connecting line segment. Kernel symmetry handles the second argument, and addition closes under A. A constant encoder covers r=0.

The global use of gradients is legitimate even though they occur at different particle states: the additive congruence is precisely what makes their translated probes simultaneous observables of one local particle state. No global injectivity, constant rank, smooth encoder, or continuous inverse is being smuggled into the lower bound.

## Fragmentation example: precise continuous-encoder theorem

Let C=(0,∞)^m, s(x)=Σ_i x_i, f(u)=u/(1+u), and

\[
 K(x,y)=1+f(s(x))f(s(y)).
\]

Let R=diag(r_1,…,r_m), where the r_i are pairwise distinct and lie in (0,1). Let a>0 be constant and

\[
 F_R\mu=a\int[\delta_{Rx}+\delta_{(I-R)x}-\delta_x],\mu(dx).
\]

For any continuous encoder h:C→R^d satisfying universal generator closure of Q_K+F_R on finite nonnegative atomic measures, d≥m. The identity encoder attains m. At a=0 the exact minimum is one. Thus the exact dimension jump holds among **all continuous encoders**, not only smooth submersions.

### Step 1: separation of the two mechanisms

If h#μ=h#ν, the same is true after multiplying μ and ν by any c>0. Closure gives a signed-measure polynomial identity

\[
 c^2[h_\#Q_K\mu-h_\#Q_K\nu]
 +c[h_\#F_R\mu-h_\#F_R\nu]=0.
\]

Two distinct positive values of c already force both coefficients to vanish. Thus coagulation and fragmentation close separately. This uses arbitrary positive atomic population weights, as allowed by the definition.

### Step 2: total size is retained

By Lemma 1, h(x)=h(x') implies K(x,y)=K(x',y) for a fixed y∈C. Since f(s(y))>0 and f is strictly increasing, s(x)=s(x'). Thus size factors set-theoretically through h. This conclusion does not require it to be an explicitly requested observable.

### Step 3: the positive offspring operator descends and can be iterated

Define

\[
 T\mu=\int[\delta_{Rx}+\delta_{(I-R)x}],\mu(dx)
       =a^{-1}F_R\mu+\mu.
\]

Separate fragmentation closure implies

\[
 h_\#\mu=h_\#\nu\quad\Longrightarrow\quad
 h_\#T\mu=h_\#T\nu.
\]

Unlike F_R, T is positive and maps finite nonnegative atomic measures to finite nonnegative atomic measures. Therefore the same implication applies again with Tμ,Tν, and induction proves

\[
 h(x)=h(x')\quad\Longrightarrow\quad
 h_\#T^k\delta_x=h_\#T^k\delta_{x'}
 \quad\text{for every integer }k\geq0.
\]

This is the point where directly iterating the signed fragmentation generator would have required extra justification. Iterating T avoids that issue completely.

Applying the size labeling to these finite atomic measures is legitimate without a measurable global decoder: every encoder atom has one well-defined size label, and equality of finite atomic measures preserves the total coefficient at each label. Hence

\[
 s_\#T^k\delta_x=s_\#T^k\delta_{x'}.
 \tag{1}
\]

Because R and I−R commute, the left side is exactly

\[
 \sum_{j=0}^k {k\choose j}\,
 \delta_{\ell_{k,j}(x)},\qquad
 \ell_{k,j}(x)=\sum_i r_i^j(1-r_i)^{k-j}x_i.
 \tag{2}
\]

Equation (2) is a measure identity with binomial multiplicities, not a claim that the branch labels themselves are observable.

### Step 4: local isolation identifies the all-R branch

For each k=1,…,m−1 and j=0,…,k−1, the equality

\[
 \ell_{k,k}(x)=\ell_{k,j}(x)
\]

defines a proper linear hyperplane, provided at least one r_i differs from 1/2. Indeed its i-th coefficient is

\[
 r_i^j\{r_i^{k-j}-(1-r_i)^{k-j}\},
\]

which vanishes precisely when r_i=1/2. For m≥2, pairwise distinct fractions ensure the required nonzero coefficient. A finite union of proper hyperplanes cannot cover the open cone, so choose x_0 outside all of them.

For each k choose a small interval around \ell_{k,k}(x_0) that excludes every \ell_{k,j}(x_0), j<k. Continuity of the finitely many linear forms supplies one open neighborhood U⊂C of x_0 such that, for each x∈U, the measure in (2) has exactly one unit atom in the selected interval, namely its all-R atom. Every other branch remains outside. Possible coincidences between the other branches are irrelevant.

If x,x'∈U and h(x)=h(x'), equality (1) identifies these isolated unit atoms, giving

\[
 \sum_i r_i^kx_i=\sum_i r_i^kx'_i,
 \qquad k=1,\ldots,m-1.
\]

The equation for k=0 is s(x)=s(x'). The Vandermonde matrix (r_i^k)_{0≤k≤m−1,1≤i≤m} is invertible because the fractions are distinct. Therefore x=x'. The continuous h is injective on U, and invariance of domain gives d≥m. When m=1, size retention alone gives local and global injectivity, so no hyperplane or offspring-iterate argument is needed.

## Boundaries and suggested edits

- The proof establishes the all-continuous result for this size-dependent kernel and diagonal split example. It should not silently replace the smooth hypothesis in the general invariant-subspace Theorem 4; that broader strengthening needs its own proof.
- Complementary fractions, such as r_1=1/4 and r_2=3/4, are allowed. They can cause branch-label ambiguity at special states, but the generic local argument removes those states. No assumption excluding r_i+r_j=1 is needed.
- One fraction may equal 1/2. All fractions equal to 1/2 would defeat the hyperplane claim, but are compatible with pairwise distinctness only when m=1, already handled separately.
- The cone being open and full dimensional is used both to choose a generic positive x_0 and to apply invariance of domain. A restriction to a lower-dimensional family of compositions would be a different problem.
- The rate must be positive for the T=a^{-1}F_R+I argument. Nothing here asserts dimension m at a=0.
- Replace the obsolete sentence after Theorem 3 saying that fragmentation hypotheses have not been relaxed once this example is added. The general Theorem 4 remains smooth, while its flagship example now has a stronger continuous-encoder lower bound.
- Replace “smooth scalar probes” by “C^1 scalar probes” in Theorem 3 to match the exact assumptions.

## Addendum: direct consequence of Hofmann–Ruppert (1988)

Date: 2026-09-06. Additional independent reviewer: `/root/closure_direction/review_rigidity`. This addendum supersedes the earlier caution that the general fragmentation theorem lacks a proof for continuous encoders. It also substantially downgrades the novelty assessment of the general dimension formulas.

I inspected the local full text `/tmp/hofmann1988.txt`, Proposition 16 on page 191, Corollary 19 on page 193, and Theorem 21 on page 196 of K. H. Hofmann and W. A. F. Ruppert, [*The Foliation of Semigroups by Congruence Classes*, Monatshefte für Mathematik 106 (1988), 179–204](https://eudml.org/doc/178400). I also inspected the PDF image of page 196 to resolve an OCR ambiguity: the hypothesis is that the group identity lies in the **closure** of the open semigroup. It need not lie in the semigroup itself.

### Applicability and the fixed subspace

Take the finite-dimensional Lie group (G=(\mathbb R^m,+)), the open subsemigroup (S=C=(0,\infty)^m), and the relation (x\sim y\) defined by equality of a continuous encoder (h:C\to\mathbb R^d). The identity (0) lies in (\overline C). Event closure from Lemma 1 makes this relation an additive semigroup congruence. Every class is closed relative to (C), since it is a level set of the continuous map (h). These are the required hypotheses; smoothness, constant rank, and connected encoder fibers are unnecessary.

The ideal in the 1988 theorem is a linear subspace (W\subseteq\mathbb R^m). In this additive group its analytic subgroup is exactly (W), which is closed and has its ordinary vector-space topology. Proposition 16, or directly Corollary 19, gives

\[
(x+W)\cap C\subseteq h^{-1}(h(x))
\quad\text{for every }x\in C,
\tag{A1}
\]

because every affine slice ((x+W)\cap C) is convex and hence connected. There is therefore no issue involving a nonclosed immersed subgroup or its intrinsic topology.

Theorem 21 supplies a neighborhood (U) of zero and, near every (u\in U\cap C), a product chart in which the full congruence classes are exactly local affine (W)-slices. In the additive setting its chart is simply ((X,Y)\mapsto u+X+Y), with (X) in a complement (E) of (W) and (Y\in W). In particular, (h) is injective on the local transversal (u+A_u\subset u+E). Invariance of domain implies

\[
d\ge\dim E=m-\dim W.
\tag{A2}
\]

For completeness, if (d<\dim E), compose this continuous injection with the coordinate inclusion (\mathbb R^d\hookrightarrow E). Invariance of domain would make its image open in (E), although that image lies in a proper linear subspace. The zero-dimensional case is immediate.

### General continuous-encoder minimum for coagulation

Suppose (K) and the required particle observables are (C^1), as in the gradient-span formula. By (A1), kernel closure, and observable retention, their directional derivatives along every (w\in W) vanish at every particle state. Thus the global span (V) of their gradients satisfies (V\subseteq W^\perp). Combining this with (A2) yields

\[
d\ge\dim W^\perp\ge\dim V.
\]

The existing linear projection with row space (V) attains dimension (\dim V). Consequently the minimum dimension is (\dim V) among **all continuous encoders**, not only smooth full-row-rank ones. The global inclusion (A1), rather than only local structure near zero, is what allows gradients at arbitrary states to enter this argument.

### General continuous-encoder minimum with diagonal fragmentation

Let (a>0) and (R=\operatorname{diag}(r_i)), (0<r_i<1). Scaling arbitrary positive atomic population weights separates coagulation and fragmentation closure. We use the same (W) supplied by the coagulation congruence above.

Fix any (w\in W). Choose a sufficiently small positive (x) so that (x,Rx\in U\cap C). Such a choice exists because (R) is continuous linear, maps (C) into (C), and fixes zero. For all sufficiently small positive and negative (t), (A1) implies (h(x+tw)=h(x)). Fragmentation closure fixes the measure

\[
\delta_{h(Rx+tRw)}+
\delta_{h((I-R)x+t(I-R)w)}.
\]

Each continuous child-encoder path is confined to the fixed support of this measure, a set of at most two points, so it is constant. This remains true when daughter atoms coincide or labels could otherwise be exchanged.

Shrink the interval in (t) so that (Rx+tRw) stays in the Theorem 21 chart centered at (Rx). In that chart, the class of (Rx) is precisely an affine (W)-slice. Hence (tRw\in W) for all sufficiently small (t), and therefore (Rw\in W). No differentiation of (h) is used. Thus

\[
RW\subseteq W,
\qquad R^TW^\perp\subseteq W^\perp.
\]

It follows that (V_\infty=\operatorname{span}\{(R^T)^kv:v\in V,\ 0\le k<m\}\subseteq W^\perp). Equation (A2) gives (d\ge\dim V_\infty), and the existing invariant-row-space projection attains this dimension. The general fragmentation formula therefore also holds among all continuous encoders. The distinct-fraction total-size example follows immediately.

The strictly positive state-dependent (C^1) rate extension follows by including its global gradient span in (V): total number identifies the rate on fibers before division recovers the fixed offspring measure.

### Limits and novelty correction

The 1988 theorem gives local affine-class equality near zero and global affine-slice inclusion. It does **not** by itself say that arbitrary continuous-encoder fibers are globally nothing more than affine slices. For example, additive congruences may acquire extra identifications away from zero. That distinction does not affect the lower bounds above.

The application needs strictly positive coagulation rates to recover the additive congruence from population closure, and a positive fragmentation rate to recover its offspring measure. It does not justify the same conclusion for a zero coagulation kernel or at fragmentation rate zero. The open positive cone and its convex affine slices are also used explicitly.

No missing hypothesis or topological obstruction was found. The previous direct proofs remain correct and useful as elementary proofs tailored to this population balance problem. However, the rigidity and dimension conclusions are short consequences of a much older structural theorem. They should be presented as an application or corollary of Hofmann–Ruppert, with further work required to establish any distinct publication contribution. This discovery does not by itself identify prior versions of the explicit finite-time error bounds or their small-rate lower bound.
