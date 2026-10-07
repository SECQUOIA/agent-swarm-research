# Adaptive OBBT: related work and contribution boundaries

Literature audit: 2026-10-03. This report supplements the earlier
[OBBT literature review](../../research-20260922/iterated-obbt/literature.md)
and its [cluster analysis](../../research-20260922/iterated-obbt/literature-cluster.md).
The source ledger below records what was inspected in this pass. Search
coverage is targeted, not exhaustive; absence from these sources does not
establish novelty.

**Selective OBBT, learned variable selection, incumbent-aware dual reuse,
and adaptive solver scheduling are established research topics.** A useful
follow-up must distinguish a certificate about a specified tightening
procedure from a prediction about total solving time.

## What already exists

Gleixner et al.'s filtering, LP ordering, and Lagrangian variable bounds are
required baselines.
[Primary manuscript](https://optimization-online.org/wp-content/uploads/2016/03/5356.pdf).

Current SCIP implements filtering, budgets, and generalized variable bounds.
Its separate generalized-bound propagator reacts to incumbent improvements.
Therefore, detecting a new incumbent and reevaluating a dual inequality are
not missing capabilities. See the pinned source entries in the
[ledger](source-ledger.md#software).

Cengil et al. (2025) dynamically select OBBT variables at each iteration using
learned rankings for AC optimal power flow. This rules out a broad claim that
adaptive or learned selective OBBT is new. Their experiments address
relaxation strengthening, not complete generic MINLP solving.
[Primary article](https://link.springer.com/article/10.1007/s10589-025-00715-7).

Gómez-Casares et al. study conic OBBT, dual-information propagation, and learned
configuration selection in polynomial optimization. Their instance-level
selection is an additional baseline for a learned start/skip policy.
[Versioned manuscript](https://arxiv.org/html/2403.02823v2).

The cost-quality tradeoff also has recent application-specific treatments.
Badilla et al. compare activation-bound methods for ReLU networks; Pineda and
Morales select which integrality restrictions to retain in tightening
subproblems. González-Díaz et al. show that explicitly storing redundant
lifted-variable bounds can improve or worsen solver performance. These
results support measuring the complete solve, including tightening cost.
[ReLU study](https://arxiv.org/html/2312.16699v2),
[topology study](https://arxiv.org/html/2507.16496v1),
[RLT study](https://arxiv.org/html/2509.18731v1).

## Mathematical attribution

The following ingredients should be presented as established mathematics or
elementary consequences, with self-contained proofs of their use here:

| Ingredient | Prior foundation | What must still be supplied for OBBT |
|---|---|---|
| A nested fixed box survives monotone tightening | Order theory and fixed-point reasoning; Tarski; earlier OBBT and FBBT analyses | Feasible endpoint witnesses for the relaxation rebuilt on that box; explicit validity under cutoff and domain changes |
| A residual and a uniform contraction majorant bound the remaining displacement | Banach/Perov contraction principles and a geometric-series sum | A verified majorant over every parameter state the iteration can visit; measured ratios alone are insufficient |
| LP optima vary affinely within a valid basis region | Multiparametric LP analysis | Exact region membership, primal/dual validity, and coverage across active-set changes |
| Dual solutions yield reusable bounds | LP duality and Lagrangian variable bounds | Row scope, cutoff dependence, and numerical validation appropriate to the chosen relaxation |
| A cap limits optional computation | Elementary accounting | A separate argument or empirical measurement for complete solving time |

Sources: [Tarski](https://people.csail.mit.edu/carroll/probSem/Documents/Tarski.pdf),
[Belotti et al.](https://optimization-online.org/wp-content/uploads/2012/01/3325.pdf),
[Jachymski and Klima](https://www.math.ubbcluj.ro/~nodeacj/download.php?f=162-ja-kl-1396-final.pdf),
[Borrelli et al.](https://cse.lab.imtlucca.it/~bemporad/publications/papers/jota-mplp.pdf).

The fixed-matrix, affine-right-hand-side LP model is a material restriction.
Rebuilding McCormick inequalities generally changes their coefficients, so
ordinary right-hand-side sensitivity does not certify the complete rebuilt
OBBT map. A proof must either keep that restriction or validate the additional
coefficient dependence.

Ordinary primal filtering proves that one direction cannot improve beyond its
witness in the current relaxation. Extending that statement to every future
round requires an invariant box or another verified persistence argument.
GBMW2017 Remark 5 also shows why zero tightening need not mean zero value:
the call can still generate a useful dual inequality.
The contribution assessed here is this OBBT-specific construction and its
checked scope, not a new order or contraction theorem.

## Promising extensions and their limits

**Predict candidate boxes, then verify them.** Anderson acceleration is an
established fixed-point method. Its unconstrained mixing coefficients do not
supply a domain-reduction proof. A candidate generated by acceleration may
be useful as input to an independent certificate checker; accepting it as a
new feasible domain requires a different, sound reduction proof.
[Walker and Ni](https://users.wpi.edu/~walker/Papers/Walker-Ni,SINUM,V49,1715-1735.pdf).

**Choose among different solver computations.** Existing SCIP studies use
bandits for several expensive algorithmic components and jointly schedule
diving and large-neighborhood heuristics. A new generic scheduler needs a
specific objective, cost accounting, and evidence beyond these precedents.
[Hendel et al.](https://optimization-online.org/wp-content/uploads/2018/07/6725.pdf),
[Chmiela et al.](https://arxiv.org/pdf/2304.03755).

**Separate computation selection from ordinary bandit rewards.** Hay et al.
formalize the value of further computation and explicit stopping decisions.
Their results concern a specified probabilistic decision model; importing
them into OBBT requires a model of how computations affect subsequent search.
[Primary manuscript](https://arxiv.org/pdf/1207.5879).

## Defensible contribution statement

This project develops checkable conditions for the remaining benefit of a
specified OBBT procedure, the validity of cached information after solver
events, and the cost of the implemented policy. These conditions use classical
duality, parametric LP analysis, and fixed-point arguments. They do not certify
that optional tightening is the fastest use of solver time. Computational
claims must come from the accompanying experiments and their stated test set,
solver version, resource limits, and accounting rules.

The review does not establish that the research area is exhausted. In
particular, the sources inspected do not supply a universal rule that chooses
optimally between tightening, cutting, branching, and incumbent search in
arbitrary MINLP instances. Nor does this review prove that such a rule is
impossible under every useful restricted model.
