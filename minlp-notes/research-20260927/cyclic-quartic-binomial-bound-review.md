# Full-text adversarial review of the binomial network degree bound

Date: 2026-09-28.

The full text of [the network degree note](cyclic-quartic-noncirculant-search.md) passes this review. No unresolved mathematical gap was found. The note correctly restricts its result to strongly connected quadratic binomial networks with all vertex equations retained. It does not claim a universal bound for rational SOS quartics.

The reviewer did not develop the general-network extension. The reviewer participated in the preceding interlace-polynomial literature investigation and independently derived the same short odd-count corollary as another agent. This is an independent adversarial review of the network extension and its final text, but not a claim of complete nonparticipation in every ingredient. The [earlier detailed proof audit](quadratic-binomial-network-degree-review.md) records the reconstruction, the boundary correction, and exact finite checks.

## Main proof and corrected boundary

I read every section of the main note and its retained search checker. The full lattice, character, Jacobian, and field-degree arguments agree with the independent reconstruction. In particular:

- The anchored vertex contributes its equation even though $x_0=1$. The gcd of all maximal minors is the relevant index. A single grounded determinant generally gives a different value in the non-Eulerian case.
- Forward propagation from $x_0=1$ excludes every complex root with a zero coordinate. This is valid with loops, repeated neighbors, and arbitrary nonzero rational coefficients.
- Normalization by any real solution preserves the real-root condition, including when some coordinates are negative. The character count uses the whole finite group, not only its largest Smith invariant.
- At every complex root the Jacobian has full column rank. Rational equations preserve all field conjugates, so the joint field degree is bounded by the number of complex roots.
- The non-Eulerian bound $g\leq2^{n-1}$ and oddness imply the stated improvement $g\leq2^{n-1}-1$ for $n\geq2$. The earlier strictness error at $n=1$ is explicitly corrected in the note.
- Euler tours are counted modulo cyclic rotation, with arcs distinguished. The BEST factor is one for two outgoing arcs, so no vertex-count factor is missing. The exact sign in the classical interlace evaluation is stated correctly.

No further correction to the theorem or proof is needed.

## Added weighted energy identity

The stationary vector satisfies

\[
2w_j=\sum_{i:a(i)=j}w_i+\sum_{i:b(i)=j}w_i,
\]

where a repeated neighbor contributes twice. Expanding the proposed right side gives

\[
\frac12\sum_iw_i(Y_{a(i)}-Y_{b(i)})^2
=\frac12\sum_iw_i(Y_{a(i)}^2+Y_{b(i)}^2)
 -\sum_iw_iY_{a(i)}Y_{b(i)}.
\]

Stationarity turns the first sum into $\sum_jw_jY_j^2$, proving the stated identity. If $a(i)=b(i)$, that row contributes zero to the squared-difference side. The expansion still holds; no assumption of distinct neighbors was silently used.

Let $N$ be the undirected multigraph having the edge $\{a(i),b(i)\}$ for every row. Modulo two, row $i$ of the full exponent matrix is $e_{a(i)}+e_{b(i)}$. It is the incidence row of that edge over $\mathbb F_2$; a loop is a zero row. After deleting the anchored column, the incidence matrix has rank $m-1$ exactly when $N$ is connected. Indeed its full kernel consists of vectors constant on each connected component, and the anchored restriction kills that kernel precisely for a single component.

The gcd of the maximal minors of $B$ is odd exactly when at least one such minor is nonzero modulo two. Therefore

\[
g\text{ odd}\quad\Longleftrightarrow\quad
\operatorname{rank}_{\mathbb F_2}B=m-1
\quad\Longleftrightarrow\quad N\text{ connected}.
\]

For the grounded energy, set $u_i=Y_i-1$, so $u_0=0$. Its quadratic form is

\[
\frac12\sum_iw_i(u_{a(i)}-u_{b(i)})^2.
\]

Every $w_i$ is strictly positive. If $N$ is connected, this form vanishes only when all $u_i=0$, proving positive definiteness on the free coordinates. The change from $Y$ to the original variables is invertible because each $p_i\ne0$, even when $p_i<0$. Thus the qualitative exposing-quadratic conclusion is sound. The note appropriately makes no uniform conditioning or coefficient-size claim for arbitrary graphs.

## Additional corollary for a minimum-size binomial exposing system

The author subsequently added the section "A normal form for the minimal binomial exposing strategy." I read the inserted section in full after independently checking its proposed argument. Let $m\geq2$, let $p=(1,p_1,\ldots,p_{m-1})$ have no zero coordinate, and let $m$ rational homogeneous quadratic binomials vanish at $p$. Suppose a real linear combination of them has a positive semidefinite symmetric matrix with kernel exactly $\operatorname{span}(p)$. This system reduces to the network class above. The following independent check found no mathematical gap in that corollary.

Write the exposing form as $Q(X)=X^{\mathsf T}MX$. Every diagonal entry of $M$ is positive: for a positive semidefinite matrix, $M_{ii}=0$ implies $Me_i=0$, contradicting $\ker M=\operatorname{span}(p)$ because $p$ has no zero coordinate and $m\geq2$.

Each summand $\lambda_jq_j$ can contribute a positive square coefficient to at most one coordinate. If its two monomials were both positive square terms, its value at $p$ would be strictly positive, contradicting $q_j(p)=0$. Every positive diagonal of $Q$ must receive some positive square contribution. Covering $m$ positive diagonals with $m$ binomials therefore forces every summand to have exactly one positive square coefficient, with a different assigned coordinate for every summand. In particular all $\lambda_j$ and all binomials are nonzero. The argument also proves that fewer than $m$ binomials cannot satisfy these assumptions.

After permuting and rationally rescaling the equations, each has the form

\[
q_i(X)=X_i^2-c_iX_{a(i)}X_{b(i)},\qquad c_i\in\mathbb Q^\times.
\]

Identical monomials must first be combined. The case $a(i)=b(i)=i$ would then be a zero or one-term equation and is excluded by the positive-diagonal argument and $q_i(p)=0$. Repeated neighbors at another vertex, or one neighbor equal to $i$, are allowed. Negative coordinates or coefficients cause no problem.

On substituting $X_i=p_iY_i$, each weighted summand becomes

\[
h_i(Y_i^2-Y_{a(i)}Y_{b(i)}),\qquad h_i>0.
\]

The diagonal change of variables preserves positive semidefiniteness and turns the kernel into $\operatorname{span}(\boldsymbol1)$. Vanishing gradient at $\boldsymbol1$ gives $2h=A^{\mathsf T}h$. Assign weight $h_i$ to each outgoing arc of $i$. This is a strictly positive circulation. Summing flow balance over any source strongly connected component shows that it has zero total outgoing weight. Thus it has no outgoing arcs. Removing it and repeating proves that there are no arcs between distinct strongly connected components.

All neighbor pairs consequently lie inside their components. The weighted energy identity shows that the indicator of each component lies in the kernel of the normalized exposing matrix. Corank one therefore forces a single component: the network is strongly connected.

The first inserted prose called these component vectors constant vectors in the kernel of $Q$ without specifying the change of coordinates. I requested a notation correction: they are component indicators for the normalized form, and are multiplied coordinatewise by $p$ for the original form. The author made that distinction explicit, and I reread the corrected sentence. This was a clarification of the represented vectors, not a change to the argument.

Finally, every common real zero of the binomials has $Q(X)=0$, hence lies in $\operatorname{span}(p)$. After anchoring $X_0=1$, the common real zero set is exactly $\{p\}$. Thus uniqueness need not be imposed separately for this corollary; it follows from the exposing assumption. The network degree bound applies. This verifies the implication but makes no independent novelty claim for it.

## Verification and limits

The preceding audit independently enumerated every strongly connected two-outgoing-arc multigraph on one through four labeled vertices, including loops and repeated arcs. The retained command

```sh
python research-20260927/check_quadratic_binomial_network_degree_review.py
```

passed. Its exact integer checks and output counts are documented in the earlier audit. Those checks preceded the request to avoid repeating the author's enumeration; the author's permutation search was not rerun. I read `check_permuted_cycle_degree_search.py` and found its reported scope consistent with the code. The author's reported run through ten vertices remains author-run verification, not an independently repeated run.

The new weighted identity and incidence-rank equivalence were checked algebraically above. No additional computation was needed. No project-wide verification, CI inspection, or Lean formalization was performed.

A targeted `python -` structural check passed for the two review documents and the retained review checker: five local Markdown links resolved, display and code delimiters balanced, and no trailing whitespace or control characters were found.

The exact maximum in this network class is a useful restriction on future constructions. Its key ingredients are established theory, and the source note appropriately declines a separate novelty claim for the interlace corollary or lattice translation. The theorem leaves open improvements using more general quadratic equations or other representations of singleton convex sets.
