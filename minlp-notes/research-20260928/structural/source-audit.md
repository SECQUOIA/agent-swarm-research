# Source and significance audit for exact feasible repair

Date: 2026-09-28. This is a bounded primary-source screen, not proof of
priority. It accompanies [the repair theorem](repair-probe.md).

The useful candidate is an exact transfer principle: on a tree of compact
local feasible sets, the best uniform deterministic Hölder repair constant
is also the best constant for repairing local probability laws in summed
Wasserstein distance. Local sets may include integer decisions and hard
constraints. The theorem does not calculate the constant, produce an
efficient global repair map, or solve local nonconvex optimization.

Its contribution, if externally new, is the equality of optimal constants
and exponents for these two repair problems. Gluing, marginal extension,
metric error bounds, and transport-based reconstruction are established
tools. The short proof and strong prior ingredients make this a focused
theorem, not currently a sufficient basis for a major MINLP advance.

## Primary results examined

**Vorob'ev (1962), *Consistent Families of Measures and Their Extensions*.**
The [open original paper](https://www.panix.com/~jays/vorob.pdf) proves that
its regularity condition on the coordinate complex is necessary and
sufficient for every consistent family of finite marginals to extend to a
joint law. This is the classical acyclic marginal-extension background.
The introduction already gives the three-binary-variable example with
two equal pairs and one unequal pair, each pair having fair marginals.
Thus neither acyclic gluing nor this cyclic obstruction is new. The local
note additionally computes the obstruction's repair distance and compares
it with the deterministic error-bound constant. The source was inspected
directly, including its introduction and final theorem/proof discussion;
a [local copy](sources/vorobev1962.pdf) and extracted text are retained.

**Haasler, Ringh, Chen, and Karlsson (2021), *Multimarginal Optimal
Transport with a Tree-Structured Cost and the Schrödinger Bridge
Problem*.** The introduction explicitly states that unregularized
transport with a tree-decomposable cost has an equivalent coupled
pairwise transport formulation. Section 3 develops the tree-cost
framework and algorithms for its entropy-regularized version. The
[local full-text transcription](../../literature/papers/haasler2021-multimarginal-optimal-transport-with-a/fulltext.md)
was inspected, especially the introduction and Sections 2--3; the
[primary manuscript](https://arxiv.org/abs/2004.06909) identifies the
paper. This directly precedes the edge-coupling identity behind the
new note. Optimizing the marginal laws as well gives the deterministic
penalty identity as a straightforward consequence. The candidate's
defensible narrower content is the sharp comparison with deterministic
hard-support repair, not a new tree-transport equivalence.

**Neufeld and Xiang, *Numerical method for feasible and approximately
optimal solutions of multi-marginal optimal transport beyond discrete
measures*, v7, 12 June 2026.** The
[author manuscript](https://personal.ntu.edu.sg/ariel.neufeld/MMOT.pdf)
was downloaded and its version checked. Definition 2.8 and Lemma 2.9
construct a joint-law reassembly using optimal marginal transports.
Theorem 2.11 gives objective error controlled by marginal Wasserstein
distances; its globally Lipschitz special case is especially close.
This reconstruction enforces prescribed marginals. It does not generally
preserve an arbitrary nonlinear hard support set. The local theorem takes
that support set seriously through a deterministic repair error bound,
and proves equality of its best constant with the corresponding law
constant. This distinction is narrower than claiming a new general
transport-reassembly method. The theorem statement and definitions were
read in the [retained v7 PDF](sources/neufeld-xiang.pdf).

**Alfonsi, Coyaud, Ehrlacher, and Lombardi, *Approximation of Optimal
Transport problems with marginal moments constraints*.** The
[open manuscript](https://arxiv.org/pdf/1905.05663), Proposition 5.1,
bounds the Lipschitz transport-objective error from cell-moment matching
by a constant times inverse grid resolution. Proposition 5.2 bounds
Wasserstein distances under these moment constraints. Remark 5.2 extends
the argument to higher-dimensional, multiple marginals. Hence passing
from finite separator features to Wasserstein error, or then to a
Lipschitz objective bound, is established background. The local result
addresses the additional hard-support repair step and its sharp
constant. The cited statements were read in the
[retained PDF](sources/alfonsi2019.pdf).

**Hoffman (1952), *On Approximate Solutions of Systems of Linear
Inequalities*.** The main theorem bounds distance to a nonempty
polyhedron by linear-inequality violation, with a finite constant for
the fixed coefficient matrix. The repository's
[original-source transcription](../../literature/papers/hoffman1952-on-approximate-solutions-of-systems/fulltext.md)
was read. Applying this theorem separately to feasible pieces of a
compact finite union of polyhedra supplies the standard linear error
bound used by the repair corollary. Infeasible compact pieces require a
separate positive minimum-residual argument; they cannot be silently
included in a Hoffman bound for an empty system.

**Kruger (2015), *Error Bounds and Hölder Metric Subregularity*.** The
[primary abstract](https://arxiv.org/abs/1411.6414) identifies the relevant
general error-bound framework. Only the abstract was inspected here;
no theorem-level dominance or originality conclusion is drawn from it.
A full comparison with this literature and measure-space metric
regularity remains needed.

**Ye (2012), *The exact penalty principle*.** The
[publisher's primary extract](https://www.sciencedirect.com/science/article/abs/pii/S0362546X11001556)
and the search-accessible introduction of the
[author manuscript](https://web.uvic.ca/~janeye/hosted/papers/ExactPenaltyFinal.pdf)
were inspected. The latter states Clarke's distance-penalty result:
a Lipschitz objective admits an exact distance penalty at its Lipschitz
constant, and a strictly larger penalty excludes other minimizers when
the feasible set is closed. The paper connects general residual
penalties with global and local error bounds. Thus the companion
[separator-penalty note](penalty-messages.md) cannot claim the
error-bound/exact-penalty mechanism as new. Its additional formulation
combines this mechanism with tree transport and bounded separator
potentials. A full source comparison for that precise combination is
unfinished. Direct browser fetches of the publisher page and author
PDF failed; the available primary search extracts supplied the stated
comparison, not a full-paper inspection.

**Fan, Park, and Xu (2023), *Quantifying Distributional Model Risk in
Marginal Problems via Optimal Transport*.** The
[primary abstract](https://arxiv.org/abs/2307.00779) treats marginal
Wasserstein ambiguity, strong duality, attainment, and continuity of
distributional model risk. It is adjacent literature, but only the
abstract was inspected. It does not suffice to rule out an equivalent
sharp error-bound lifting statement deeper in the paper or its
references.

## Earlier local results and rejected directions

The [September 22 control note](../../notes/research-20260922-moment-control.md)
already repairs exact local transition laws by replaying actions when
action availability is independent of state. Its transport argument and
its [novelty review](../../notes/research-20260922-separator-novelty.md)
explicitly characterize that argument as a synthesis of established
methods. The present theorem handles arbitrary hard support sets by
identifying exactly which additional deterministic repair estimate is
required. It does not make such an estimate automatic.

The [September 27 equality note](../../research-20260927/equality-frontier.md)
already contains exponentially poor polynomial error exponents on sparse
quadratic systems. The terminal-constraint example in the new repair
note adds a uniformly contractive forward-dynamics interpretation.
It must not be presented as the first exponential error-exponent example
or as a lower bound for an exactly matched moment hierarchy.

A guard-margin proposal was screened out as a main contribution. It
would glue local trajectories, replay actions, estimate the probability
of crossing a guard from transport error and guard-margin mass, and
discard unsafe samples. The key transport-budget/unsafe-set-distance
mechanism is already explicit in Chen, Kuhn, and Wiesemann,
[*Data-Driven Chance Constrained Programs over Wasserstein Balls*](https://optimization-online.org/wp-content/uploads/2018/06/6671-1.pdf),
Section 2.1 and Theorem 2. Their empirical formulation uses distances to
the unsafe set and a fractional-knapsack interpretation. The searched
primary extract and theorem discussion were inspected; this branch did
not complete a separate theorem or novelty claim.

Search phrases included `approximate marginal consistency Wasserstein
junction tree error bound`, `Wasserstein metric subregularity marginal
constraints probability measures error bound`, `marginal gluing Hölder
error bound`, `Vorobev Consistent families measures extensions`, and
`Wasserstein distance to the unsafe set chance constraints`. Failed
searches are not evidence that the candidate is original.

## Targeted computational check

The command actually run was:

```text
python3 research-20260928/structural/check_repair_transfer.py
```

It enumerates deterministic tuples using exact rational arithmetic and
solves finite law-repair LPs with SciPy 1.18.0/HiGHS. For the three-bag
binary path in the script, the exact deterministic constant is 2.
All 300 seeded random-law checks satisfy the proposed bound, and a
Dirac law attains 2. The attaining tuple is
`((0,0),(0,1),(0,0))`, with residual 1 and repair distance 2.

After adding the penalty/message consequences, the same command was
rerun. It additionally verifies 80 exact rational comparisons between
the constructive dual messages and enumeration of every deterministic
tuple, and checks the sharp penalty threshold below, at, and above 2.
These new checks justify the rerun; the earlier 300 random-law checks
were not independently duplicated for additional confidence.

For the classical binary triangle, exact enumeration gives deterministic
constant 1, while the LP gives separator residual 0 and law-repair
distance 1. The latter value also has the elementary proof in the note.
The floating-point LP calculations do not certify arbitrary real
instances, measurable selections, optimal constants in the compact
setting, or novelty. They test the stated finite formulations and a
specific regression boundary. No project-wide verification or CI
inspection was run.

The [independent proof-review record](repair-proof-review.md) specifies
which arguments were reviewed before and after the written notes. The
parent structural investigator then reread the final main proof, the
terminal example, and the new constructive message proof. No substantive
proof correction was needed. A clarification now explicitly restricts
the low-moment terminal propagation observation to actual local measures.

A targeted inline Python check of these Markdown files also passed
relative-link existence, math-delimiter balance, and trailing-whitespace
checks. This checks document hygiene only. The files were new and
untracked during this work; `git diff --check` alone would not inspect
their contents and is not relied on for that verification.

## Assessment and next question

The proved transfer would allow a solver designer to reuse deterministic
feasibility error bounds without paying an additional universal
probabilistic constant. It also prevents attributing difficult repair to
moment information when it is already present for a single deterministic
tuple. Practical value requires a useful, computable deterministic
constant and an implementable repair map for an important model class.

The strongest next question is therefore concrete: find a nonlinear
network or hybrid-control class with hard terminal constraints and a
repair constant controlled by meaningful physical or combinatorial
parameters. A theorem that merely assumes a favorable global constant
has not solved that problem.
