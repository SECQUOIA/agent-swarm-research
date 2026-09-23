# Shared conventions

These conventions follow the [scope map](../notes/potential-flow-complexity-map.md), [paper-readiness record](../notes/potential-flow-paper-readiness.md), and the result files assigned in [coverage.md](coverage.md). They fix notation for both papers. Paper A's preliminaries implement these definitions.

## Model and objectives

Use a finite connected loopless graph $G=(V,E)$ with an arbitrary orientation of each edge. Write $n=|V|$ and $m=|E|$. An edge $e=(u,v)$ has tail $u$ and head $v$. Its incidence column in $A$ is $+1$ at $u$ and $-1$ at $v$. Some sources call this matrix $B$; both papers use $A$. “Arc” refers to an oriented edge, and a signed flow may run against that orientation. Parallel edges are allowed, and a pair of parallel edges forms a cycle of length two. State when simplicity is required; the universal graph characterizations use connected simple graphs.

Nominations (balanced loads) are $b\in\mathbb R^V$, with positive entries for injections and negative entries for withdrawals. Conservation is $Ax=b$, and balance is $\mathbf1^\top b=0$. A balanced nomination box is $\mathcal B=\{b:\ell\le b\le u,\ \mathbf1^\top b=0\}$. Bounds are finite rationals in algorithmic statements. They may be shifted and need not contain zero. State nonemptiness or detect it. A fixed-dimensional affine family is $b=b^0+Mz$ on a compact parameter polytope $P$ given by an explicit list of rational linear equalities and inequalities.

Potentials are $\pi\in\mathbb R^V$ and flows are $x\in\mathbb R^E$. The passive equations are $A^\top\pi=(g_e(x_e))_{e\in E}$. Edge laws are continuous, strictly increasing, and zero at zero within each stated model. The symmetric quadratic law is $\pi_u-\pi_v=\beta_e x_e|x_e|$, with $\beta_e>0$. The asymmetric variant uses $g_e(x)=\beta_e^+x^2$ for $x\ge0$ and $g_e(x)=-\beta_e^-x^2$ for $x\le0$, with separate positive coefficients. Reversing an edge reverses its flow and swaps the positive and negative coefficients. Symmetry must not be assumed for a constructed envelope law.

Potentials are gauge invariant: adding one constant to all potentials preserves the state equations. Fix a reference vertex $v_0$ and set $\pi_{v_0}=0$ when a normalized vector is needed. A weighted potential objective is $c^\top\pi$ with rational $c$ and $\mathbf1^\top c=0$. Its support size is $p=|\{v:c_v\ne0\}|$. A weighted flow objective is $d^\top x$; it is a different objective class.

MPD means maximum potential difference for a prescribed ordered terminal pair $(s,t)$: maximize $\pi_s-\pi_t$ over the stated scenario domain. Do not silently optimize over the choice of terminals. The single-source/sink SRS equivalence uses those same terminals as the only source and sink. General balanced-box cactus approximation permits many nonzero nominations.

Primitive energy is $\mathcal E(x)=\sum_e\int_0^{x_e}g_e(t)\,dt$. Under symmetric quadratic laws it is $\sum_e\beta_e|x_e|^3/3$. Constitutive dissipation is $D=\sum_e\beta_e|x_e|^3=b^\top\pi$ at a physical state. Preserve the factor of three. Dissipation need not mean literal compressor power, and the sum of arc flows is not delivered throughput.

## Graph parameters

A cactus is a graph in which distinct simple cycles share at most one vertex. Its blocks are bridges or simple cycles. Cacti have block rank at most one, with equality only when a cycle is present. Series-parallel means no $K_4$ minor; an arbitrary pair of terminals need not define a two-terminal series-parallel decomposition.

A block is a maximal biconnected subgraph, with bridges treated as rank-zero blocks. Blocks have edges; the connected one-vertex graph has no blocks. For a connected block $C$, its cycle rank is $r(C)=|E(C)|-|V(C)|+1$. Block rank is $r_{\max}=\max_C r(C)$, with value zero when there are no cyclic blocks. Total (global) cycle rank is $r=m-n+1$ for a connected graph, or $m-n+k$ for $k$ components. Fixing block rank permits arbitrarily many cycles overall. A fixed-rank polynomial whose exponent depends on that rank is not automatically a fixed-parameter tractable algorithm.

## Uncertainty and quantifiers

Unless a section explicitly replaces them, resistance intervals are independent: $\mathcal R=\prod_e[L_e,U_e]$ with rational $0<L_e\le U_e<\infty$. Singleton intervals are allowed. Nomination and resistance choices form a product apart from nomination balance. Finite uncertainty means explicitly listed nonempty positive rational sets. Replacing finite choices by interval hulls needs an objective-specific justification.

Within-cycle resistance polytopes may correlate edges of one cycle while different cycle polytopes remain independent. One global polytope can correlate different cycles and requires separate results. Independent affine coefficient boxes, fixed laws, and asymmetric laws are separate representations; preserve each result's hypotheses. Dense polynomial encoding includes numerical degree and piece count in the input size. Do not transfer those bounds to sparse binary exponents. Fixed breakpoints, uniform strict increase, and promised objective convexity must be stated where used.

Robust validation asks whether every admissible parameter/nomination scenario's passive state satisfies the tested bounds. Existential design asks whether some admissible scenario satisfies them or optimizes an objective. In unfiltered validation, first evaluate all passive scenarios and then compare their extrema to capacities. Using capacities or potential bounds to filter the scenario domain changes the problem. Signed capacities $\underline{x}_e \le x_e \le \overline{x}_e$ include absolute capacities as a special case. A strict violation, a weak threshold, and its robust complement retain their exact inequalities and equality cases.

## Arithmetic and output

Use the Turing bit model. Rational data are binary encoded; running time includes arithmetic bit costs and output length. Let $N$ denote total input bit length and $\epsilon>0$ the additive tolerance. “Polynomial additive” means polynomial in $N$ and the requested accuracy bits $\max\{0,\log_2(1/\epsilon)\}$. For arbitrary rational tolerance input, count its encoding too. Larger tolerances can be replaced by one. This is stronger precision dependence than polynomial in $1/\epsilon$.

Exact threshold comparison decides the stated inequality against a rational threshold, including equality. Additive intervals alone do not decide it when the threshold meets the optimum. Square-Root-Sum (SRS) asks, for binary-encoded positive integers $a_1,\ldots,a_k,K$, whether $\sum_i\sqrt{a_i}\le K$. Handle trivial zero cases explicitly if allowed. Etessami and Yannakakis (2010), [On the Complexity of Nash Equilibria and Other Fixed Points](../literature/papers/etessami2010-on-the-complexity-of-nash/paper.md), Section 1, state the PSPACE upper bound and the open questions of polynomial-time decidability and membership in NP. They also report the stronger counting-hierarchy bound of Allender et al. The [local SRS result](../results/potential-flow-cactus-square-root-sum.md) records only the open status, including the absence of known NP-hardness; it is not the source for these upper bounds. An SRS lower bound is an arithmetic barrier, not an NP-hardness or additive-approximation claim.

The class $\exists\mathbb R$ consists of decision problems reducible in polynomial time to feasibility of finite polynomial equalities and inequalities over real variables with rational (equivalently integer) coefficients. Membership or completeness must be justified for the actual model. AC power feasibility uses different injection equations and supplies no automatic hardness conclusion for passive flow.

An exact real-algebraic output uses a defining polynomial and rational isolating interval, or an equivalent standard algebraic encoding, with the claimed encoding length. Rational input scenarios can have irrational physical states. An exact rational optimizing resistance profile does not imply a rational objective value or polynomial exact comparison of a sum of independent algebraic block values. Retain separate local quadratic encodings when that is the output contract. Capacity-filtered varying-load domains can require algebraic feasible parameters; a supplied slack recovery guarantee is compared with the tightened optimum unless an additional optimum-margin assumption is given.

## Shared LaTeX macros

Both `macros.tex` files define the same names. Use ordinary $A,b,x,\pi,c,d$ for the model variables so source notation does not require a second alias system.

| Macro | Meaning |
| --- | --- |
| `\R`, `\Q`, `\Z`, `\N` | Real, rational, integer, and natural numbers |
| `\one` | All-ones vector |
| `\eps` | Additive tolerance |
| `\MPD`, `\SRS` | Problem names |
| `\ETR` | The class $\exists\mathbb R$ |
| `\NP`, `\coNP`, `\PSPACE` | Complexity classes |
| `\OPT` | Optimum value |
| `\Vmax` | Rational absolute bound $V_{\max}$ on terminal potential differences |
| `\supp` | Support operator |
| `\sgn` | Sign operator |
| `\rank` | Matrix rank operator |
| `\blockrank` | Maximum block cycle rank $r_{\max}$ |
| `\totalrank` | Total cycle rank $r$ |
| `\nomset`, `\resset` | Nomination and resistance domains |
| `\energy` | Primitive energy $\mathcal E$ |
| `\abs{...}`, `\norm{...}` | Absolute value and norm delimiters |
| `algorithm` environment | Definition-style Algorithm environment sharing the theorem counter |

Theorem, lemma, proposition, corollary, definition, example, remark, problem, assumption, and algorithm share one counter, reset by section. Each paper defines its own macros file with the identical shared definitions. Section labels use `sec:a-...` or `sec:b-...` to remain distinct across papers.

Algorithms use enumerated steps inside the definition-style `algorithm` theorem environment. No algorithm or algpseudocode package is loaded. Both macros files restore plain theorem style after defining the remark environment so later additions do not inherit remark style.
