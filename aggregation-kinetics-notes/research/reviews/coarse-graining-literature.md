# Adversarial literature audit: continuous particle encoders

Date: 2026-09-06. Reviewer: closure_direction. Scope: Theorem 3 and Theorem 4b of [the coarse-graining note](../ideas/coarse-graining.md), including their claims over **all continuous encoders**. This audit concerns novelty; earlier independent reviews concern correctness.

## Finding

The underlying affine structure of continuous additive quotients is established mathematics. A directly applicable theorem of Hofmann and Ruppert (1988) implies the minimum-dimension result after the population-balance event-closure lemma and a short argument. Its assumptions explicitly allow an open positive cone, exclude any need for a differentiable encoder, and only require closed congruence classes.

The same theorem also gives the invariant-subspace fragmentation formula for **all continuous encoders**, extending the smooth version in the note. Therefore the one-to-\(m\) jump in Theorem 4b is a short application of established semigroup structure and a Vandermonde calculation. I did not find a publication stating these population-balance formulas or the particular rate-dependent approximation bounds. That narrower absence does not justify presenting the quotient geometry or the general method as new.

Recommended status: retain the results as useful population-balance corollaries with elementary proofs and explicit attribution. Treat the proposed standalone novelty of the affine rigidity and dimension lower bounds as substantially weakened. The rate-dependent exact-versus-approximate distinction is a separate candidate contribution; this audit has not established its novelty.

## 1. Decisive primary source: congruence foliations

K. H. Hofmann and W. A. F. Ruppert, *The foliation of semigroups by congruence classes*, Monatshefte für Mathematik **106** (1988), 179–204, DOI [10.1007/BF01318680](https://doi.org/10.1007/BF01318680). [Full PDF inspected](https://link.springer.com/content/pdf/10.1007/BF01318680.pdf); [EuDML archive record](https://eudml.org/doc/178400).

**Inspected:** introduction pp. 179–181; Lemma 12; Proposition 16 pp. 191–192; Corollaries 18–19 p. 193; Lemma 20 pp. 194–195; Theorem 21 and proof pp. 196–198; Theorem 24 pp. 199–200.

**Assumptions and usable conclusions.** Theorem 21 takes a finite-dimensional Lie group \(G\), an open subsemigroup \(S\) with identity in its closure, and a congruence with closed classes. An ideal in its Lie algebra describes the classes locally near the identity. Proposition 16 and Corollary 19 give inclusion of connected subgroup-coset intersections in entire congruence classes. Theorem 24 supplies a local factorization; it warns that the resulting continuous bijection need not be open. No global quotient-manifold assumption is available or needed here.

The publisher landing page labels the article subscription content, but the linked PDF was publicly retrievable without credentials and was read at the stated sections. The archive also lists access to the full article.

### Application to our setting

Set \(G=(\mathbb R^m,+)\), \(S=C=(0,\infty)^m\), and
\[
x\sim x' \quad\Longleftrightarrow\quad h(x)=h(x').
\]
Lemma 1 in the note makes this an additive congruence. Continuity of \(h:C\to\mathbb R^d\) makes each class closed in \(C\). The identity \(0\) belongs to \(\overline C\). Thus every source hypothesis holds.

In this additive group, the ideal is a linear subspace \(W\), and its analytic subgroup is \(W\) itself, which is closed. The intersections \((x+W)\cap C\) are convex. Specializing the cited results gives:

1. For every \(x\in C\), \(h\) is constant on \((x+W)\cap C\).
2. In a neighborhood of zero, each point has a local affine product chart whose fibers are precisely the local \(W\)-slices. In particular, \(h\) is injective on a sufficiently small transverse slice of dimension \(m-\dim W\).

These statements allow extra disconnected identifications away from zero. They do not assert that all global fibers equal individual affine slices.

### Direct deduction of Theorem 3

Since \(K(\cdot,y)\) and retained \(q_j\) are constant on \(h\)-fibers, conclusion 1 gives
\[
W\subseteq\bigcap_{x,y}\ker D_xK(x,y)
       \cap\bigcap_{x,j}\ker Dq_j(x)=V^\perp.
\]
Conclusion 2 and invariance of domain give
\[
d\ge m-\dim W\ge \dim V.
\]
The projection onto \(V\) is exact by the elementary attainment proof already in the note. Thus
\[
d_{\min}=\dim V
\]
is a direct population-balance corollary. No encoder derivative, decoder continuity, properness, connected-fiber assumption, or extension of \(h\) to zero is needed.

The note's translated-gradient proof remains useful: it gives an elementary argument for this specific conclusion without invoking the general foliation theorem. It is an alternative proof of a consequence of prior theory, rather than evidence that the consequence could not have been obtained before.

## 2. Stronger consequence for fragmentation

This subsection is our deduction from the preceding source, not a theorem stated there.

Let the note's assumptions hold with constant fragmentation rate \(a>0\) and
\[
R=\operatorname{diag}(r_1,\ldots,r_m),\qquad 0<r_i<1.
\]
Define
\[
V_\infty=\operatorname{span}\{(R^\top)^k v:
                         v\in V,\ 0\le k<m\}.
\]
Then the formula
\[
\boxed{d_{\min}=\dim V_\infty}
\]
holds among **all continuous universally exact encoders** for coagulation plus binary fragmentation, not only smooth constant-rank ones.

**Proof of the additional lower bound.** Scaling the atomic population separates the quadratic coagulation and linear fragmentation fields. Hence the congruence and its subspace \(W\) above still apply. Closure of fragmentation implies that, on every \(h\)-fiber,
\[
\delta_{h(Rx)}+\delta_{h((I-R)x)}
\]
is constant. Fix \(w\in W\). Choose \(x\in C\) sufficiently close to zero that both \(x\) and \(Rx\) lie in the neighborhood of the foliation theorem. For all sufficiently small real \(t\), conclusion 1 gives \(h(x+tw)=h(x)\). The continuous path \(t\mapsto h(Rx+tRw)\) lies in the fixed finite support
\[
\{h(Rx),h((I-R)x)\};
\]
it is therefore constant. Take \(t\) smaller if needed so that \(Rx+tRw\) stays in a single local affine product chart at \(Rx\). Conclusion 2 forces \(tRw\in W\), so \(RW\subseteq W\).

We already have \(W\subseteq V^\perp\). Iteration yields \(W\subseteq V_\infty^\perp\), and the transverse-slice bound gives \(d\ge\dim V_\infty\). Conversely, choose \(A\) with row space \(V_\infty\). Its kernel is invariant under \(R\) and \(I-R\), so both offspring coordinates factor through \(Ax\); \(K\) and the retained observables also factor through \(Ax\). This proves attainment. Cayley–Hamilton justifies stopping the span at \(m-1\).

This proof does not label the observed daughters globally. The finite-support argument is valid even if their encodings coincide. It also avoids assuming the latent addition law is continuous.

For the total-size kernel in Theorem 4b, \(V=\operatorname{span}\{\mathbf1\}\). Distinct \(r_i\) make \(\mathbf1,R^\top\mathbf1,\ldots,(R^\top)^{m-1}\mathbf1\) independent. Thus \(d_{\min}=m\) whenever \(a>0\), while \(d_{\min}=1\) at \(a=0\). The general prior foliation theorem therefore supplies a shorter route to the specific all-continuous jump.

**Verification:** reviewer review_rigidity independently inspected the source and verified this implication on 2026-09-06. Its detailed addendum is in [the continuous-encoder review](coarse-graining-continuous-review.md). It found no missing hypotheses or topological defect.

## 3. Earlier cone theorem

Klaus Keimel, *Congruence relations on cone semigroups*, Semigroup Forum **3** (1971), 130–147, DOI [10.1007/BF02572953](https://doi.org/10.1007/BF02572953). [Full PDF inspected](https://link.springer.com/content/pdf/10.1007/BF02572953.pdf); [author publication list](https://www2.mathematik.tu-darmstadt.de/~logik/keimel/publications.html); [EuDML record](https://eudml.org/doc/133855).

**Inspected:** definitions and Theorem 1.4 pp. 131–133; following generalization remark p. 133.

Theorem 1.4 concerns a closed cone in a finite-dimensional real vector space and a closed congruence relation. It gives a greatest subspace \(L\) whose affine-coset equivalence is contained in the congruence, with equality locally near zero. The following remark extends the results to subsemigroups for which zero is a limit of interior points. This is already very close to our exact domain. Hofmann–Ruppert is the cleaner citation because its open-semigroup hypothesis and weaker closed-class assumption are stated explicitly.

The 1988 reference list gives volume 2 for Keimel, whereas his own publication list and EuDML give volume 3; use volume 3. Its introduction also cites a different theorem number than the clearly numbered Theorem 1.4 in the inspected PDF. Cite the inspected statement by its actual number.

## 4. Observability and topological latent-dimension antecedents

**Bronisław Jakubczyk (1980).** *Existence and uniqueness of nonlinear realizations*, Astérisque **75–76**, 141–147. [Open full paper](https://www.numdam.org/item/AST_1980__75-76__141_0.pdf).

Inspected Sections 3–8, especially the experiment-map rank in Section 4, realization definition in Section 5, Theorem 2, and necessity in Section 7. Theorem 2 identifies minimal smooth realization dimension with a rank defined using families of input-output experiments, under analytic hypotheses or sufficiently smooth hypotheses with a symmetry condition. Section 8 identifies histories when every future experiment agrees. This is a clear antecedent of the translated-witness/observable-rank argument. It is not by itself our theorem: the realization and dynamics there are smooth and satisfy control-system assumptions, while our reduced encoder is merely continuous and has no prescribed reduced dynamics.

**Edward Wagstaff et al. (2019).** *On the Limitations of Representing Functions on Sets*, Proceedings of Machine Learning Research **97**, 6487–6494. [Paper and supplement](https://proceedings.mlr.press/v97/wagstaff19a.html).

Inspected main-paper Section 4, Theorem 4.1 and Lemma 4.2. Their continuous sum-decomposition problem uses an embedding of individual elements followed by summation and decoding. A suitable target forces the aggregated embedding to be injective, and topology forces latent dimension at least the allowed set size. Thus the strategy “observable discrimination implies continuous injection, which forces dimension” is established in the learned-representation literature. The paper does not supply a coagulation-kernel gradient formula or selective-fragmentation analysis.

**Argyris et al.** *Minimization of Dynamical Systems over Monoids*, [arXiv:2206.15169](https://arxiv.org/html/2206.15169).

Inspected Sections III–V, Definition 3 and Theorems 1–3. These reductions partition a finite set of state variables and aggregate each block using a prescribed monoid operation. The work characterizes descent and computes coarsest admissible partitions. It is relevant algebraic reduction theory but does not optimize arbitrary continuous encoders on an open Euclidean particle-state cone.

**Lawson and Madison (1971).** *On congruences and cones*, Mathematische Zeitschrift **120**, 18–24. [Full paper](https://link.springer.com/content/pdf/10.1007/BF01109714.pdf).

Inspected Sections 2–3, Corollary 2.4, Proposition 2.5, and Theorem 3.2. This addresses quotient topology of semigroups and embedding locally compact cones in topological vector spaces. The scalar structure and quotient assumptions differ from an arbitrary latent encoder. It is background, not the decisive direct implication supplied by Hofmann–Ruppert.

## 5. Population-balance comparison inspected in this audit

Deesha Wadhwa et al., *A new efficient framework for reduced two-dimensional nonlinear aggregation population balance models*, Chemical Engineering Science **338**, 124884; DOI [10.1016/j.ces.2026.124884](https://doi.org/10.1016/j.ces.2026.124884). The issue date is February 2027; an online record and primary-source preview were accessible on 2026-09-06.

**Inspected:** publisher abstract, introduction with displayed two-dimensional PBE, and preview of the new-formulation section. The kernel depends on granule volume and time but is independent of tracer volume. Integrating over tracer gives the number density; a tracer-weighted integral gives a second coupled scalar balance. The principal advertised contribution is a conservative discretization.

This confirms that exact reduction under a kernel independence assumption is established PBE practice. It is distinct from a universal impossibility theorem over every continuous particle encoder: a number distribution plus a tracer-weighted measure is a different observation map. The accessible preview does not contain our dimension classification or a fragmentation jump. The complete article was not obtained, so it cannot be ruled out as a source of additional relevant statements.

## 6. Search coverage and remaining claim

The targeted search used combinations of “cone semigroup congruence,” “closed congruence foliation,” “continuous quotient dimension,” “minimal realization observable rank,” “population balance exact reduction,” and coagulation/fragmentation with “lumping” and “congruence.” References in the primary semigroup papers led to the decisive older results. This is a bounded adversarial audit, not an exhaustive review of every non-English source or inaccessible article.

The following attribution is justified by what was inspected:

| Claim in the note | Assessment after this audit |
|---|---|
| Universal atomic closure implies an additive congruence and kernel factorization | Elementary PBE form of established exact-lumping logic. |
| Continuous congruences have affine fibers locally near zero | Established by Keimel and Hofmann–Ruppert. |
| \(d_{\min}=\dim V\) among all continuous particle encoders | Direct specialized corollary; no exact PBE statement located. |
| Linear selective splitting forces an invariant hidden subspace | Short deduction from established congruence geometry and finite-support offspring closure. |
| General all-continuous \(d_{\min}=\dim V_\infty\) | Useful stronger corollary developed during this audit; independently verified. |
| One-to-\(m\) exact dimension jump for arbitrarily weak selective splitting | Explicit physical example of the preceding corollary; no exact prior example located. |
| Matching \(O(a)\) finite-time upper and lower prediction bounds | Not settled by this audit; requires its own approximation/perturbation comparison. |

The strongest defensible presentation combines the exact corollaries with a useful approximation question or an application that requires them. Novelty should not rest on describing the same established congruence structure in population-balance or autoencoder terminology.
