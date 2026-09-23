# A feedback-variable gap bound, sharp for one deleted variable

Date: 2026-09-04. Status: full proof independently audited; no unresolved mathematical issue identified. Novelty is provisional.

## Theorem

Let

    p(x)=Σ_(e∈E) a_e ∏_(i∈e) x_i,       a_e≥0,

on a finite box with nonnegative lower bounds. Affine terms can be discarded because they have zero gap. The incidence graph has variable nodes i, factor nodes e, and an edge ie when i∈e. Suppose a set F of f variable nodes can be deleted to make this graph a forest. Then at every x,

    tbtgap_p(x) ≤ 2^f chgap_p(x).                          (1)

There is no restriction on monomial degree, number of variables, or number of factors.

For f=0 the two gaps coincide, with ratio one wherever positive, recovering the known exactness of standard linearization for Berge-acyclic hypergraphs. For f=1 the constant two is sharp as a supremum, even with unit coefficients and incidence treewidth exactly two.

The proof below first establishes a coupling statement that applies to arbitrary nonnegative local functions on binary variables, then applies it to unit-box deficiencies and to the original monomials on nonnegative boxes.

## A universal law on the feedback variables and each remaining variable

Fix the prescribed Bernoulli means x. Let U be uniform on (0,1), and independently choose an orientation η∈{+,-}^F uniformly. For j∈F define

    X_j=1[U≤x_j]        if η_j=+,
    X_j=1[U>1−x_j]      if η_j=-.

For every i∉F define X_i=1[U≤x_i]. Denote the resulting joint law by Q, its F-marginal by Q_F, and its (F,i)-marginal by Q_i. Every coordinate has its prescribed mean.

For s∈{0,1}^F and b∈{0,1}, let

    m(s,b;i)=min({x_j : j∈F,s_j=1},
                 {1−x_j : j∈F,s_j=0},
                 {x_i if b=1, 1−x_i if b=0}).

Empty portions of this list contribute no entries. Then

    Q_i(s,b) ≥ 2^−f m(s,b;i).                             (2)

To see this when b=1, select the unique orientation that makes the required state of every feedback variable occur on an interval starting at zero: use η_j=+ for s_j=1 and η_j=- for s_j=0. The common intersection with X_i=1 has length m(s,1;i). For b=0 use the opposite orientation; all required events then occupy intervals ending at one, whose intersection has length m(s,0;i). The chosen orientation has probability 2^−f.

Every distribution P on F∪{i} with the prescribed singleton means satisfies P(s,b)≤m(s,b;i). Therefore Q_i dominates 2^−f P entrywise, simultaneously for every i∉F and every such P.

The analogous domination holds for Q_F: every prescribed-mean law P_F satisfies

    Q_F(s)≥2^−f P_F(s).                                   (3)

This follows by the same endpoint-interval argument, or by summing the pair domination when an outside variable exists. When F is empty there is a single feedback state of probability one.

## Repairing local laws without changing their singleton means

Set C=2^f. For each factor e, suppose P_e is any distribution on F∪e having all prescribed singleton means. Let I_e=e\F. We construct a law P'_e on the same variables such that

    P'_e ≥ P_e/C entrywise,
    (P'_e)_(F,i)=Q_i for every i∈I_e,
    (P'_e)_F=Q_F.                                        (4)

For each feedback state s define

    h_s=Q_F(s)−(P_e)_F(s)/C.

By (3), h_s≥0. For i∈I_e and b∈{0,1}, define

    r_(i,s,b)=Q_i(s,b)−(P_e)_(F,i)(s,b)/C.

These residual masses are nonnegative by (2), and their sum over b is h_s. When h_s>0, put residual mass h_s at feedback state s and choose all outside coordinates in I_e independently with conditional probabilities r_(i,s,b)/h_s. When h_s=0, place no residual mass there; all corresponding r-values then vanish. This defines a nonnegative residual measure R_e of total mass 1−1/C. For I_e empty, simply give state s residual mass h_s.

Now put P'_e=P_e/C+R_e. Its total mass is one, and the prescribed marginal identities and entrywise domination in (4) follow directly.

## Conditional gluing on the forest

Condition on a feedback state s with Q_F(s)>0. The factor laws P'_e conditioned on s give distributions on I_e with the same singleton marginal

    Pr(X_i=b | X_F=s)=Q_i(s,b)/Q_F(s)

wherever the variable i occurs. The incidence graph on these outside variables and factors is a forest by assumption.

These conditional factor laws can therefore be glued into one joint law on all outside variables. A direct construction roots each nontrivial incidence-tree component at a factor, samples its local law, and traverses the tree. Each new factor shares exactly one already sampled variable with the preceding part. Sample its other variables using its conditional law given that shared variable. Zero-probability shared-variable values are never encountered, so their conditional laws can be assigned arbitrarily. Isolated variables may be sampled with their required conditional means, and factors with I_e empty add no outside variables.

This construction preserves every conditional factor law. Mixing over s with probabilities Q_F(s) yields a global law P' whose marginal on F∪e is P'_e for every factor. Consequently, for every collection of nonnegative local functions g_e on e,

    E_(P') g_e ≥ E_(P_e) g_e/C for every e.                (5)

This is a simultaneous guarantee. No loss is multiplied along a path in the forest.

The factor 2^f is sharp for this general class of nonnegative local payoffs. Give the f feedback variables and one outside variable X means 1/2. For every state (s,b)∈{0,1}^(f+1), introduce the local payoff 1[(X_F,X)=(s,b)]. Each payoff has local maximum expectation 1/2, so the sum of local maxima is 2^f. Their sum is identically one under every global law. Deleting F leaves a star incidence graph. If distinct genuine factor scopes are required, multiply each payoff by a different private binary variable of mean one; this preserves the calculation and the forest property. These cell indicators involve zero literals and are not positive-coefficient monomials, so this example does not establish sharpness of (1) for general f.

## Applying the coupling to multilinear gaps

For each e choose an anchor k_e minimizing x_i over i∈e, and define the nonnegative binary deficiency

    g_e(X_e)=X_(k_e)−∏_(i∈e)X_i.

The largest expectation of this deficiency under prescribed singleton means equals the individual monomial's term-by-term gap T_e. Choose a maximizing local law on e and extend it to F∪e by giving any missing feedback coordinates independent Bernoulli values with their prescribed means. This gives the laws P_e used above.

The global law P' preserves every coordinate mean, and (5) gives E g_e≥T_e/C simultaneously. Positive monomials have a simultaneously attainable concave envelope, so

    chgap_p(x)=max_(P: E X=x) Σ_e a_e E_P g_e
              ≥Σ_e a_e T_e/C=tbtgap_p(x)/C.

This proves (1).

## Finite nonnegative boxes without changing the incidence structure

Delete fixed coordinates first; their nonnegative values only rescale coefficients or make terms vanish, and deleting their incidence edges cannot create cycles. Rescale each remaining coordinate to a unit variable Y_i with prescribed mean ξ_i. An original monomial becomes a local function

    φ_e(Y_e)=∏_(i∈e) [l_i+(u_i−l_i)Y_i]
             =Σ_(A⊆e) c_A ∏_(i∈A)Y_i,       c_A≥0.

For each nonempty A choose k_A minimizing ξ_i over i∈A and define the affine function

    ℓ_e(Y_e)=c_empty+Σ_(nonempty A⊆e) c_A Y_(k_A).

Pointwise on binary vertices, ℓ_e≥φ_e. Every prescribed-mean law has Eℓ_e=c_empty+Σ_A c_A min_(i∈A) ξ_i. Comonotone Bernoulli coordinates attain this value for Eφ_e, so it equals the concave-envelope value U_e of the original monomial at the original point.

Therefore g_e=ℓ_e−φ_e is a nonnegative function on the same original factor scope e. Its largest local expected value is U_e−vex φ_e, which is exactly the original monomial's term-by-term gap. Apply (5) to these functions. The concave envelope of the complete positive polynomial is Σ_e a_e U_e, again by simultaneous comonotone attainment, and the desired bound follows.

The expansion is used only to exhibit a local affine majorant. It does not replace the original factor by new hyperedges. Such a replacement could introduce incidence cycles and would not justify the structural conclusion.

## Sharpness when f=1

For each integer n≥2, consider

    p_n(a,x)=a Σ_(i=1)^n x_i+∏_(i=1)^n x_i,
    a=1/n,       x_i=1−1/n.

All coefficients equal one. Each bilinear term has gap 1/n, while the degree-n term has gap (n−1)/n. Hence

    tbtgap=2−1/n.                                        (6)

Under an arbitrary binary coupling with these means, write A for the anchor and R for the number of failed x-variables. Then E A=1/n and E R=1. The total deficiency is

    E[A R]+Pr(R≥1)−1/n.

Pointwise,

    A R+1[R≥1]≤R+A.

Taking expectations shows chgap≤1. Equality is attained by choosing exactly one failed leaf uniformly at random, and choosing A independently with probability 1/n. Therefore

    chgap=1,       tbtgap/chgap=2−1/n→2.                  (7)

Deleting the variable node a leaves a tree: the factor for ∏x_i is its center, and each leaf variable x_i is joined to its bilinear factor. The full incidence graph has treewidth two. An explicit decomposition has bags {a,e_0,x_i}, connected in a path, and leaf bags {a,x_i,e_i} attached to the corresponding path bag. Here e_0 is the degree-n factor and e_i is the factor ax_i. All bags have size three. The graph contains a cycle for n≥2, so its treewidth is not one.

Thus the worst gap ratio over incidence graphs made into forests by deleting at most one variable is exactly two as a supremum. This also proves a lower bound of two for unrestricted incidence-treewidth-two families; it does not prove an upper bound for every incidence-treewidth-two graph.

## Scope and prior art

The f=0 case is classical: Del Pia and Khajavirad characterize exact standard linearization by Berge-acyclicity. Their result concerns the full multilinear polytope. [Open primary article](https://par.nsf.gov/servlets/purl/10081429).

Conditioning on a feedback vertex set to obtain a forest is also a standard inference method. The point requiring verification here is preservation of the original singleton means while repairing all local laws with one uniform loss factor. Exact inference or an extended formulation alone does not give the displayed pointwise relaxation-gap ratio.

The proposed new statements are the feedback-variable gap bound and its sharp one-variable specialization. No novelty claim is made for forest gluing, the conditioning framework, or bounded-treewidth tractability. A dedicated bounded literature screen is in [the incidence investigation](../notes/multilinear-incidence-width-investigation.md).

The general dependence on f is not proved sharp. Bounded feedback-variable number is stronger than bounded incidence treewidth, and (1) does not settle the latter parameter.

The full written proof, nonnegative-box extension, sharp feedback-one example, and generic-payoff observation passed [independent review](../notes/review-multilinear-feedback-gap.md). An independent exact-arithmetic check of the universal law appears in [the audit script](../code/audit-multilinear-feedback-law.py).

## Lean verification

[Topic 19](../formal/topics/19-structural-multilinear/COVERAGE.md) formalizes the
feedback-variable bound on original finite nonnegative boxes, including fixed
coordinates and zero coefficients. The input is acyclicity of the actual
incidence graph after deleting the specified variables. The proof constructs
the universal law, repaired local laws, forest elimination order and global
coupling; none of these is an additional assumption of the gap theorem.

The unit-coefficient flower has its stated exact gaps, an attaining law, minimum
feedback size one and incidence treewidth exactly two. Its ratios converge to
two. For general nonnegative local payoffs, the cell-indicator example proves
the loss `2^f` sharp for every `f`, including the variant with distinct scopes
and private mean-one variables. This does not prove general-`f` sharpness for
positive monomials.

The [verification record](../formal/topics/19-structural-multilinear/VERIFICATION.md)
identifies the checks and reviewed source snapshots. Separate optimization or
separation algorithms and their bit complexity are outside this package.
