# Harmonic-analysis novelty audit of the McCormick gap bound

Date: 2026-09-04. Scope: a bounded search through graph-supported Walsh polynomials,
Sidon constants, unconditional constants, sparse Rademacher chaos, and related graph
sparsity terminology. This is a novelty audit, not a claim that all relevant literature
has been exhausted.

A late Schur-multiplier search changed the assessment: the square-root
maximum-induced-density order follows from Davidson–Donsig (2007), using
Grothendieck duality and polarization. The precise transfer is in
[`mccormick-hereditary-density-characterization.md`](../results/mccormick-hereditary-density-characterization.md),
last section, and has passed independent review. Earlier unsuccessful Sidon
searches are retained below as an audit trail; they do not support a novelty
claim for the graph-norm order. A related 2024 paper contains a displayed
sparse-support proposition that cannot be used as stated; an explicit
counterexample is recorded below for independent review.

## Exact translation of the optimization problem

For a finite graph G and real edge coefficients a, set

```
f_a(s) = sum_{ij in E(G)} a_ij s_i s_j,       s in {-1,1}^{V(G)},
L(a) = sum_{ij in E(G)} |a_ij|,
R(a) = (max f_a - min f_a)/2.
```

The real Sidon constant of its degree-two character system is

```
S(G) = sup_{a != 0} L(a) / ||f_a||_infinity.
```

Since the uniform mean of f_a is zero,

```
||f_a||_infinity / 2 <= R(a) <= ||f_a||_infinity.
```

Consequently the worst signed-cut-range constant C(G)=sup_a L(a)/R(a)
satisfies S(G)<=C(G)<=2S(G). Allowing zero coefficients makes both constants
monotone under taking subgraphs. Under the induced-subgraph formula in the
McCormick result, the worst-over-coefficients McCormick gap constant is C(G).
Thus a sqrt(density) theorem is also a graph-supported Walsh Sidon theorem.
This connection should be stated in any paper, and the analytic lemmas should
not be represented as discoveries specific to MINLP.

For bipartite G the range of f_a is symmetric: reversing all vertex signs on
one part negates f_a. Therefore R(a)=||f_a||_infinity and C(G)=S(G) exactly.

## Primary literature inspected

1. Ron C. Blei, *Sidon partitions and p-Sidon sets*, Pacific J. Math. 65(2),
   307–313 (1976), [open original paper](https://msp.org/pjm/1976/65-2/pjm-v65-n2-p03-p.pdf).
   The opening discussion explicitly attributes the mixed row-norm inequality
   for bilinear forms to Littlewood (1930). Lemma 1.4 recasts it through Sidon
   partitions. Corollary 2.2 treats products of dissociated characters through
   a decoupling argument. These establish the classical nature of the row-norm
   and decoupling ingredients. No degeneracy, arboricity, or hereditary edge
   density theorem appears in this paper.

2. Ron Blei, *Measurements of interdependence*, 2010,
   [author-hosted manuscript](https://www.cs.columbia.edu/~blei/papers/Blei2010.pdf).
   Section 2 defines combinatorial dimension by counts in Cartesian boxes;
   Section 4 relates it to Sidon exponents of subsystems of Walsh chaos.
   This is a strong conceptual antecedent for measuring support sparsity.
   The manuscript concerns asymptotic exponents rather than the finite
   graph-parameter constant sought here. It points to Blei's 1984
   *Combinatorial dimension and certain norms in harmonic analysis* and his
   2001 monograph as further priorities. Those full texts were not exhaustively
   checked in this pass.

3. Andreas Defant, Daniel Galicer, Martín Mansilla, Mieczysław Mastyło,
   Santiago Muro, *Asymptotic insights for projection, Gordon–Lewis and Sidon
   constants in Boolean cube function spaces*,
   [arXiv:2302.00233v2](https://arxiv.org/html/2302.00233v2), 24 May 2024.
   Theorem 5.2 bounds a homogeneous support's Sidon constant through a
   coordinate projection norm and the projection constant of its one-step
   reduced support. For edge supports the reduced support is the set of
   nonisolated vertices, so this does not directly give a density bound.
   Proposition 5.10 claims a stronger support-size bound under a size
   condition; see the counterexample below. The arXiv record lists v2 as
   the latest version checked. Definitions and the disputed formula were
   compared in HTML, math alttext, and the
   [PDF copy](https://ri.conicet.gov.ar/bitstream/handle/11336/257790/CONICET_Digital_Nro.ad85c82b-29b4-42ef-b8cf-cad2db078c4c_B.pdf?sequence=2).

4. Sergey V. Astashkin, *The Rademacher system in function spaces*,
   [author-hosted survey](https://astashkin.ssau.ru/papers/70engl.pdf).
   The discussion following Corollary 6.5 connects Rademacher chaos,
   decoupling, and p-Sidon systems; it records classical quantitative
   nonsidonicity of the full quadratic system. This again prevents treating
   the dense-system order sqrt(n) or decoupling itself as new.
   The separate Astashkin–Lykov paper *Sparse Rademacher chaos in symmetric
   spaces* (2016/2017), DOI 10.1090/spmj/1436, remains a full-text follow-up
   priority: search results confused its metadata with an older paper, so
   this audit does not claim to have verified its complete theorem list.

The combinations Sidon/Walsh/Rademacher with graph, degeneracy, arboricity,
maximum degree, density, and sparse were searched. Many hits concerned
additive-combinatorial Sidon sets, which are a different notion and do not
settle this question. Searches involving signed cuts and arboricity also
produced no exact match. A search failure is not evidence of nonexistence.

## A counterexample to the displayed sparse-support proposition

Status: complete elementary argument checked by the author of this audit;
independent review requested. This concerns Proposition 5.10 as displayed in
arXiv:2302.00233v2, not a claim about every version or the other results.

For polynomial degree two its asserted upper bound specializes to

```
Sid(B_S^N) <= K sqrt(|S|/N),  provided |S| >= N/2,
```

with one absolute K. The following connected support disproves such a bound.

Take q=2^k>=4 and a Sylvester Hadamard matrix H of order q, so H H^T=q I.
Start with a complete bipartite graph with q vertices in each part. Attach
q^2-2q new leaves to the first vertex of one part. The resulting graph is
connected, has N=q^2 vertices and m=2q^2-2q edges, and uses every vertex.
Its edge characters form S.

Assign coefficient H_ij to each core edge and epsilon=q^{-3} to each leaf
edge. Every coefficient is nonzero. The associated polynomial is

```
f(x,y,z) = x^T H y + epsilon x_1 sum_l z_l.
```

For all sign vectors, Cauchy–Schwarz and H^T H=qI give

```
|x^T H y| <= ||x||_2 ||H y||_2 = sqrt(q) q = q^(3/2).
```

There are fewer than q^2 leaves. Hence

```
||f||_infinity <= q^(3/2) + 1/q,
L(f) >= q^2,
Sid(B_S^N) >= q^2 / (q^(3/2) + 1/q) -> infinity.
```

Yet m/N<2 and m>=N/2, so the asserted upper bound is at most K sqrt(2),
a contradiction. Connectedness, nonisolated vertices, and nonzero coefficients
therefore cannot repair the displayed proposition.

The displayed proof also contains an exponent inconsistency: applying the
Bohnenblust–Hille inequality and Hölder gives the support-size factor
m^((d-1)/(2d))=sqrt(m)/m^(1/(2d)); the proof instead writes
sqrt(m)/m^(1/d). This observation identifies a possible source of the issue,
but the counterexample is sufficient and does not rely on diagnosing the proof.
Do not use the proposition as an existing valid density theorem.

## Implications for the research direction

- A theorem C(G)<=4 sqrt(rho(G)), where rho(G)=max_{U nonempty}
  |E(G[U])|/|U|, would also give S(G)<=4 sqrt(rho(G)). The proof should be
  framed as an explicit weighted graph refinement of classical Sidon and
  signed-discrepancy estimates, followed by a McCormick consequence.
- A matching lower bound for every graph follows from a standard random-sign
  argument on a densest induced subgraph, not only from complete-graph
  examples. For an n-vertex m-edge subgraph, independent random edge signs
  satisfy, for fixed s, P(|f(s)|>t)<=2 exp(-t^2/(2m)). A union bound over 2^n
  sign vectors yields a signing with ||f||_infinity<=sqrt(2m(n+2)log 2).
  Therefore C(G)>=S(G)>=sqrt(m/[2(n+2)log 2]); choosing the densest subgraph
  gives an absolute-constant multiple of sqrt(rho(G)). This is a useful
  graph-by-graph characterization, though its lower-bound ingredient is
  classical and no novelty is claimed for that argument.
- Forest edge characters are independent, and finite unions of independent
  character sets are classical Sidon sets. Thus qualitative boundedness for
  bounded arboricity should not be claimed as new. The quantitative square
  root dependence and the direct relaxation interpretation are the points
  requiring further novelty investigation.

## Late audit update: Schur-bounded patterns

The decisive additional terminology is **Schur-bounded patterns**, including
row/column decompositions and hereditary rectangle density. See the explicit
transfer in the linked characterization note. This is stronger prior-art
evidence than the unsuccessful Sidon/degeneracy searches above. The raw
square-root density order must be treated as a consequence of existing theory.
