# Literature comparison for spatial branch-and-bound strengthening

Search date: 2026-09-05. Scope: continuous spatial branch-and-bound lower
bounds, SDP/RLT strengthening, higher-order SOS, and fractional cardinality.
This is a bounded search, not proof of novelty or priority. In particular,
**exponential spatial branch-and-bound lower bounds already exist**; no
claim of being the first such result is appropriate.

## Close sources

- [Florian Jarre (2018), Best case exponential running time of a
  branch-and-bound algorithm using an optimal semidefinite relaxation](https://optimization-online.org/wp-content/uploads/2018/07/6729.pdf).
  Read in full. The model fixes binary variables to zero or one and uses a
  standard max-cut SDP after transforming weighted binary knapsack. It does
  not analyze arbitrary real coordinate split points or full nodewise RLT.
  It is a close conceptual predecessor to the SDP–RLT result.
- [Stefano Coniglio (ICLR 2026), Solving the 2-norm k-hyperplane clustering
  problem via multi-norm formulations](https://openreview.net/pdf?id=VJAqqtVXfD).
  The initial PDF read exposed the abstract and formulation sections; a
  search result exposed Section 4.3 including its midpoint-branching
  assumption. Later PDF accesses returned a browser challenge, so the
  appendix proof has not been fully inspected in this search. The supported
  distinction is that its lower-bound claim concerns obtaining a nonzero
  bound under midpoint branching on symmetric domains, whereas our theorem
  concerns arbitrary split points and a fixed objective gap with the stated
  node relaxation. An earlier submission was public in September 2024.
- [Gérard Cornuéjols and Yatharth Dubey (2025), Branch-and-Bound versus
  Lift-and-Project Relaxations in Combinatorial Optimization](https://link.springer.com/article/10.1007/s10107-025-02248-7).
  Read the model description, knapsack discussion, and Sections 4–5.
  The paper compares binary branch-and-bound formulations and hierarchy
  strength. It does not give the combined continuous spatial-box/higher-SOS
  oracle lower bound developed here.
- [Aaron Potechin (2019), Sum of Squares Lower Bounds from Symmetry and a
  Good Story](https://drops.dagstuhl.de/storage/00lipics/lipics-vol124-itcs2019/LIPIcs.ITCS.2019.61/LIPIcs.ITCS.2019.61.pdf).
  Read the knapsack theorem, definitions, moment construction, and
  specialization of its general machinery to knapsack. Fractional-cardinality
  moments and their SOS positivity are classical Grigoriev ingredients.
  The incidence-Gram matrix basis used in our elementary positivity proof
  is likewise a standard Johnson-scheme construction.

## Potentially new combined statements

The strongest current claims are specific combinations of features:

1. A fixed-gap cover lower bound for arbitrary real spatial boxes using full
   nodewise SDP–RLT and all linear-equality products.
2. A quantitative spatial-cover-size/order tradeoff for the full truncated
   box preordering, including moment matrices, all localizers, all RLT
   products up to the stated degree, and all equality products.
3. Survival of this obstruction after distinct small linear-objective
   perturbations make the optimizer unique and remove permutation symmetry.

The new argument uses existing fractional-cardinality moment ideas inside
arbitrary real boxes and combines them with an endpoint-exclusion witness
count. No source found in this search states that combination. This is the
scope of the tentative novelty assessment; the individual ingredients and
general phenomenon are not claimed as new.

## Searches and limitations

Queries included combinations of “spatial branch-and-bound”, “exponential
lower bound”, “semidefinite”, “RLT”, “sum-of-squares”, “knapsack”, “arbitrary
continuous”, and “unique”. Primary sources above were preferred. Search
results also found newer algorithmic papers using SOS/spatial branching,
but their abstracts did not expose a matching combined lower-bound theorem.
No exhaustive citation-network review or complete publication-level priority
assessment has yet been performed.


## Concrete known cut that defeats the obstruction

The [clique-cut scope note](spatial-bb-known-clique-cut.md) gives the
classical Boolean-quadric inequality
`2 sum_(i<j) X_ij-2k sum_i x_i+k(k+1)>=0` and its primary-source formula.
It is valid on the continuous unit-box graph by multiaffinity. With the
linearized demand equality, it gives the exact penalty bound `1/4` at the
root. One such cut per block closes the relative-gap direct product.
These known cuts materially limit any impact claim: the results separate
specified hierarchy/spatial certificate systems from available global
quadratic cuts; they do not establish inherent hardness of these instances.
