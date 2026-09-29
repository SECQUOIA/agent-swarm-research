# Publication-readiness review: component elimination and treewidth

Reviewed 25 September 2026. Scope: the mathematical claims and primary-source
attribution in [treewidth-elimination-review.md](treewidth-elimination-review.md).
This is an independent review of an existing result, not an extension to a
new research direction.

**Verdict.** The five-vertex counterexample, the replacement decomposition,
and the padded family are correct. The note is suitable as a supporting
correction with its existing limitations. One material source-version
qualification was required and has been incorporated: the August revision
of the polynomial-optimization preprint changed which result relies on the
false graph bound.

## Proof audit

1. For `K_{2,3}`, bags `{a,b,u}`, `{a,b,v}`, `{a,b,w}` in a path form a
   width-two decomposition. A cycle supplies a `K_3` minor. Eliminating
   `a` produces `K_4`; hence the claimed maximum bound fails exactly as
   stated, with a singleton eliminated component.
2. Replacing every component occurrence by its entire retained boundary
   covers every torso edge. For each retained vertex, its new occurrence
   set is its original connected subtree together with connected
   component-occurrence subtrees, each meeting that original subtree.
   Running intersection follows. The cardinality estimate gives
   `(kappa+1) max(1,Delta)-1`, including empty boundaries. A supplied
   decomposition must be charged its own width; the note does so.
3. Eliminating the original vertices of a one-subdivision of `K_k` gives
   `L(K_k)`. The displayed input decomposition and the `K_k` minor show
   input width `k-1`. Harvey–Wood's exact output-width formula agrees
   with the note. The separate weighted-centroid proof of the weaker
   quadratic lower bound is valid: the occurrence path for an edge `ij`
   crosses the centroid unless both labels are in one component, and
   each component has at most half the labels.
4. A retained pendant path of `2^k` vertices preserves both relevant
   treewidths and all eliminated boundaries. Thus the separate
   logarithmic hypotheses hold while residual width is quadratic in
   `log n`. The padding is explicitly disclosed. The resulting lower
   bound concerns full bag-assignment tables, not arbitrary convex
   extended formulations or every possible optimization algorithm.

No gap was found in these arguments. The product dependence is shown
necessary along the comparable-parameter family, not for every pair of
parameter values. The replacement construction is a classical mechanism;
the note makes no graph-theoretic novelty claim.

## Primary sources and version correction

The following primary sources were opened and checked on the review date.

- Khajavirad, [arXiv:2601.18545v2](https://arxiv.org/html/2601.18545v2#S5),
  dated 12 February 2026: Lemmas 7–8 contain the false graph bound;
  Theorem 6 uses it to infer logarithmic residual width. The arXiv
  submission history still lists v2 as the latest version.
- Khajavirad, [Lehigh report 26T-007](https://engineering.lehigh.edu/sites/engineering.lehigh.edu/files/_DEPARTMENTS/ise/pdf/tech-papers/26/26T_007.pdf),
  dated 27 April 2026: printed pages 5–7 contain Lemmas 3–4 and their
  use in the proof of Theorem 1. This remains an older version, even
  though the URL is still publicly available.
- Khajavirad, [arXiv:2604.25033v2](https://arxiv.org/html/2604.25033v2),
  dated 19 August 2026: Theorem 1 now assumes the residual torso has
  logarithmic treewidth. The false Lemmas 3–4 remain in Section 2.3,
  where they support Corollary 1. The same current version is linked
  from the author's publication page and the updated Optimization
  Online entry. Our singleton-component family has zero component
  nonconvexity parameter, so it refutes the width implication used for
  that corollary. It does not undermine the current Theorem 1 through
  this graph issue. The rest of that theorem is outside this audit.
- Harvey and Wood, [*Treewidth of the Line Graph of a Complete Graph*](https://users.monash.edu.au/~davidwo/papers/HarveyWood-JGT14.pdf),
  Theorem 1: its odd/even formulas equal
  `floor((k-1)^2/4)+k-2` as used in the note.

The higher-degree portion of the August preprint also invokes the disputed
graph lemma. This review does not assert a complete verdict on its
higher-degree theorem: that requires checking the separate hypergraph
claims and algorithmic assumptions. It is unnecessary for the correction
established here.

The precise defensible statement is therefore that the cited lemmas are
false and the specified proof steps fail. A claim that the associated
optimization conclusions themselves are false would exceed the evidence.
The revision's use of a direct residual-width assumption also means that
this assumption must not be presented as new here.

The supporting-work coordinator independently reread the August version's
Theorem 1, Corollary 1, Lemmas 3–4, and Section 2.3 from arXiv HTML and
confirmed this source-version correction. This second check establishes
agreement on the attribution and logical dependency, not a review of the
remaining algorithmic claims.

## Reproducibility and remaining limits

The mathematical verification command run in this review was:

```text
python research-20260925/check_treewidth_elimination.py
```

It passed, reporting `2 -> 3` for `K_{2,3}`, `2 -> 2` for the subdivision
of `K_3`, `3 -> 4` for the subdivision of `K_4`, and the torso/line-graph
identity for `k=3,...,8`. The code was read as well as executed: its
elimination-order recurrence is exact on the tested finite graphs, and
its pruning only removes branches that cannot improve the current best
width. The infinite-family and general upper-bound conclusions rest on
the proofs above. No project-wide checks, CI inspection, or Lean build
were performed.

The targeted formatting check
`git diff --check -- research-20260925/treewidth-elimination-review.md research-20260925/publication-treewidth-review.md`
also passed.

This supporting correction is mathematically complete within its stated
scope. Before a public claim of priority, the literature and current
source versions should be checked again; this review is not a certificate
that no equivalent correction exists. No communication to source authors
has been sent.
