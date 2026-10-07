# Exact indicator optimization after random screening

Date: 2026-10-02. Status: a proved candidate theorem with an independent
check of the percolation argument; external priority assessment is pending.
This is a restricted positive result, not a resolution of the broader
high-disorder problem described below.

The useful question is whether numerical data can make exact sparse
indicator optimization easy on graphs of arbitrarily large treewidth. A
simple answer is available when independent positive penalties leave a
sufficiently sparse set of coordinates that could possibly be active. Safe
screening followed by exact component optimization then has polynomial
expected bit complexity. Every potentially active continuous variable is
retained, so the decomposition does not overlook coupling through variables
whose indicators are already known to be active.

The mathematics combines a coordinate-deletion bound with standard site
percolation and branching-process generating functions. It should not be
presented as a major new general optimization principle. The potentially
useful contribution is the resulting exact solver regime and its explicit
noise-versus-response threshold. No claim of novelty is currently justified.

## Model and deterministic screening

Let Q be a rational symmetric positive-definite matrix, b a rational vector,
and let the rational penalties lambda_i be independent random
variables. Their support is finite, and the total encoding length of Q,b
and every penalty realization is bounded by the input parameter L. Minimize

    F(x,z) = x^T Q x - 2 b^T x + sum_i lambda_i z_i,
    x_i(1-z_i)=0,  z_i in {0,1}.

Let G have edge ij whenever Q_ij is nonzero. Suppose deterministic rational
numbers r_i satisfy

    |(Q_SS^{-1} b_S)_i| <= r_i   for every S containing i.

Set M_i=Q_ii r_i^2 and retain R={i:lambda_i<=M_i}. This strict deletion
rule preserves every optimal support, including threshold ties.

**Screening lemma.** Every globally optimal pair has z_i=0 whenever
lambda_i>M_i.

Fix an optimal support S and its unique conditional continuous optimizer x.
For i in S, stationarity gives (Qx)_i=b_i. Replacing x_i by zero and z_i
by zero, without changing anything else, increases the objective by

    Q_ii x_i^2 - lambda_i.

It cannot decrease the optimum. Thus lambda_i<=Q_ii x_i^2<=M_i. This
proof allows an active coordinate to equal zero and allows zero penalties.

The restricted matrix Q_RR has no entries between distinct connected
components of G[R]. Solve each component independently by enumerating its
supports, solving its principal linear systems exactly, and comparing the
rational values

    sum_{i in S} lambda_i - b_S^T Q_SS^{-1} b_S.

Their union is a global optimum. This is exact for every penalty realization.
It is not a method that first eliminates known-active continuous variables.

## Computing useful screening bounds

Suppose the comparison matrix A has A_ii=Q_ii and
A_ij=-|Q_ij| for i!=j, and A is a nonsingular M-matrix. Then

    r=A^{-1}|b|

is a valid nonnegative rational bound. Indeed, for a principal support S,

    A_SS |x_S| <= |b_S|,
    A_SS r_S >= |b_S|.

Multiplication by the nonnegative inverse A_SS^{-1} proves |x_S|<=r_S.
This includes strictly diagonally dominant Q. If

    Q_ii - sum_{j!=i}|Q_ij| >= delta > 0,
    |b_i| <= B,

one may simply take r_i=B/delta. With Q_ii<=H, the common threshold is
M=H B^2/delta^2. Computing this common bound only needs the sparse rows;
using the tighter comparison inverse has a separate polynomial setup cost.

The screening lemma itself permits negative penalties. The useful
probability condition below then requires that their total probability is
small enough, since every negative-penalty coordinate is retained.

There is also a general positive-definite bound. Put y=Q^{-1}b and
T=b^TQ^{-1}b. Every principal-support optimizer satisfies
x^TQx=b^Tx, hence

    (x-y/2)^T Q (x-y/2)=T/4,
    |x_i| <= (|y_i| + sqrt(T (Q^{-1})_ii))/2.

Any rational upper bound on the last expression is admissible. The simpler
rational threshold M_i=Q_ii (Q^{-1})_ii T also follows from
x^TQx=b^Tx<=sqrt(T x^TQx) and coordinate Cauchy--Schwarz. This removes
diagonal dominance from the theorem, but it often yields thresholds growing
with n. Diagonal dominance supplies a dimension-independent threshold when
the local coefficients are bounded.

## Expected complexity on arbitrary bounded-degree graphs

Write p_i=Pr(lambda_i<=M_i). The retained vertices are independent. Let the
maximum degree of G be Delta>=2, and assume p_i<=p.

For Delta=2, assume p<1/2. For Delta>=3 put d=Delta-1 and assume

    p < 1/d,
    2p(1-p)^(d-1) < (d-1)^(d-1)/d^d.                 (1)

The strict inequality is convenient because it supplies a constant a>2
with finite component-size a-moment. For fixed Delta and p satisfying (1),
there is a constant K(Delta,p,a) such that for every vertex v,

    E[a^{|C(v)|} | v retained] <= K,

where C(v) is its retained component. No treewidth bound is assumed.

To see this, explore a component breadth first. The root has at most Delta
potential children. Every other discovered vertex has at most d fresh
neighbors; each is retained independently with probability at most p.
Coupling to independent extra trials gives stochastic domination by a tree
whose non-root offspring law is Bin(d,p). If H(s) is its descendant total
progeny generating function, then

    H(s)=s(1-p+pH(s))^d.

For d>=2, the largest s for which a finite solution exists is

    s_c=(d-1)^(d-1)/(p d^d(1-p)^(d-1)).

This follows by maximizing h/(1-p+ph)^d over h>=1. Condition (1) gives
s_c>2; choose 2<a<s_c. The root generating function is bounded by
a(1-p+pH(a))^Delta. For d=1, H(s)=s(1-p)/(1-sp), so any
2<a<1/p works. The cases p=0 and Delta<=1 are immediate.

**Theorem.** Under these hypotheses, the screening/component algorithm
returns an exact rational global optimizer for every realization, with
polynomial expected bit complexity. If each support linear solve takes at
most P(L) k^c bit operations on a component of size k, the expected total
component work is at most K' n P(L), where K' depends on Delta,p,c and the
strict margin in (1). The deterministic cost of computing r and reading the
input is added separately.

For the proof, support enumeration costs at most P(L) k^c 2^k per
component. Since a>2, k^c 2^k<=K'' a^k uniformly in k. Charging each
component to each of its vertices only increases this bound; summing the
uniform exponential moments over vertices proves the estimate. Rational
linear algebra has polynomial bit cost, and the rational output lengths
are polynomial in the input encoding length.

The threshold is stronger than ordinary subcritical percolation p<1/d.
That weaker condition controls component sizes with high probability, but
does not by itself control the expectation of exponentially expensive
component enumeration. For Delta=3 the sufficient strict threshold is

    p < (1-1/sqrt(2))/2 = 0.1464466094... .

The corresponding values for Delta=4 and 5 are approximately 0.0893164
and 0.0643883. The percolation review gives endpoint details and an example
showing why this moment distinction is real. These thresholds are not
lower bounds on the complexity of the optimization problem: an improved
component solver could work outside this regime.

## A graph-specific expected-work certificate

The maximum-degree threshold can be replaced by a certificate using the
actual probabilities p_i and graph. This permits heterogeneous probabilities
and unbounded degrees.

For this certificate, let p_i be known rational upper bounds on the
retention probabilities; use their exact values when rational. Fix rational
a>2 independently of the input size. For every directed edge v->u, supply a rational H_vu>=a
satisfying

    H_vu >= a product_{w in N(v), w!=u} (1-p_w+p_w H_wv).       (2)

Define

    K_v = a product_{w in N(v)} (1-p_w+p_w H_wv).

Then E[a^{|C(v)|} | v retained]<=K_v. To prove this, unfold the graph
into a rooted tree of nonbacktracking walks. Each occurrence of a vertex w
other than the root receives its own independent Bernoulli(p_w) retention
trial. Breadth-first exploration of a real component is dominated by this
tree: a fresh neighbor receives its first trial, and already examined
neighbors only remove possible branches. Truncated tree generating
functions start at a and obey the products in (2); induction bounds each
directed branch by H_vu. Monotone convergence proves the claim, including
when the unfolded tree is infinite.

Consequently the expected component work is at most

    C_{a,c} P(L) sum_v p_v K_v,

using k^c 2^k<=C_{a,c}a^k and charging each component to its retained
vertices. Thus (2), together with a polynomial bound on sum_v p_v K_v,
is a directly checkable expected-polynomial-work certificate. Merely finding
finite H values does not establish a polynomial bound if these products
are exponentially large. Exact verification uses rational products; the
cost of obtaining the certificate is separate.

There is a convenient convex search problem for a certificate. Put
y_vu=log H_vu. The inequalities become

    log a + sum_{w in N(v), w!=u}
        log(1-p_w+p_w exp(y_wv)) - y_vu <= 0,
    y_vu >= log a.

Each left side is convex. A numerical solution is only a candidate;
rational H values must pass (2) exactly before claiming the bound. No
claim is made that these inequalities are necessary or that a small
certificate can always be found. The homogeneous branching-process
calculation is a special case.

## A finite-grid perturbation corollary

Let baseline penalties be arbitrary nonnegative rationals and independently
add noise uniform on the N equally spaced rational points in [0,sigma],
including both endpoints, where N>=2 and sigma is positive rational. Then

    p_i <= min(1, M_i/sigma + 1/N).

Consequently the theorem applies whenever the right-hand side is at most a
fixed p satisfying (1). Under the uniform diagonal-dominance assumptions,
it is enough that

    H B^2/(delta^2 sigma) + 1/N <= p.

The noise need not break ties, and its atom size does not enter an isolation
lemma. The algorithm solves the realized instance exactly even with ties.
Unlike the repository's fixed-treewidth smoothed theorem, this result
requires noise or baseline penalties large enough relative to the possible
activation benefit. It therefore is a high-positive-penalty regime, not a
small-noise theorem for arbitrary baselines.

## Limits and the unresolved stronger direction

The screening and percolation argument has no control when many indicators
are certainly active. Treating only undecided indicators as a percolating
graph is invalid: a certainly active center can couple every undecided leaf
after its continuous variable is eliminated. The present algorithm avoids
that error by keeping all potentially active coordinates in R.

A stronger, unresolved question is whether weak numerical coupling and
random penalties centered around activation thresholds give expected
polynomial exact optimization even when a positive fraction of variables
are certainly active. Inverse decay alone is insufficient for the simple
component argument: any nonzero connection can matter at an arbitrarily
small optimality gap. A proof would need a quantitative interaction between
decay and random decision margins, accounting for continuous mediators.

The present theorem establishes a new candidate tractable regime to compare
with the literature. It does not yet meet the ambition of a substantial new
algorithm for general weakly coupled sparse MINLP. If priority assessment
finds an equivalent random-screening result, this should remain a short
supporting lemma rather than become a separate research topic.
