# Exponential moment order on a quadratic path

Date: 2026-09-27. Status: candidate contribution, with one completed
[independent adversarial proof review](chebyshev-proof-review.md) and
additional reviews pending. The lower-bound witness, degree accounting,
and perturbed certificate are explicit. Novelty has not been established.
This note concerns a fixed sparse relaxation architecture, not the intrinsic
difficulty of the optimization problems.

## Candidate result

For each integer `m>=1`, put `N=2^m`. Consider variables

\[
 x=u_0=v_0,\quad u_1,\ldots,u_m,\quad v_1,\ldots,v_m\in[-1,1]
\]

and the quadratic equalities

\[
 u_j=2u_{j-1}^2-1,\qquad v_j=2v_{j-1}^2-1\quad(1\le j\le m).
 \tag{1}
\]

Minimize

\[
 F=(u_m-1)^2+(v_m+1)^2. \tag{2}
\]

There are `2m+1` variables and `2m` quadratic equations. All coefficients
belong to a fixed finite set, and the correlative sparsity graph is the path
`u_m,...,u_1,x,v_1,...,v_m`, of treewidth one. The ordinary sparse input has
`O(m log(m+1))` bits when variable indices are binary encoded. Thus a lower
bound `2^{m-1}` is exponential in dimension and superpolynomial in this
ordinary input length; it should not be called exponential in the full
input length without specifying another encoding convention.

Use an order-`r` correlative sparse moment relaxation with one bag for each
adjacent pair in that path, where `r>=1`. Each bag has a normalized linear
functional on its polynomials of total degree at most `2r`; its order-`r`
moment matrix is PSD. Include the box localizers `1-z^2>=0`, and impose
`L(hq)=0` for each equality polynomial `h` in the bag and every polynomial
`q` of degree at most `2r-2`. Identify all singleton moments through degree
`2r` at overlaps. The objective uses its terminal bag functionals. Extra
valid constraints entirely inside each bag are allowed for the lower bound,
because its witness consists of actual feasible local probability measures.

**Theorem 1 (candidate).** The true minimum in (1)--(2) is `2`. The stated
sparse moment relaxation and its sparse SOS dual both have value

\[
 \rho_r=\begin{cases}
 0,&2r<2^m,\\
 2,&2r\ge2^m.
 \end{cases} \tag{3}
\]

In particular, the first exact order is `r=2^{m-1}`. The same lower bound
holds for the stronger relaxation using an arbitrary feasible probability
measure on every edge bag and matching moments through degree `2r` at the
overlaps. Local convexification error is therefore unnecessary for the gap.

The lower bound also covers every width-one tree decomposition of the
original path. Indeed, the graph obtained by making every bag a clique has
treewidth at most one, hence is a forest, and already contains the connected
original path. Adding a nonedge of that path would create a cycle.
Consequently its nonsingleton bags can only be original adjacent pairs;
copies and singleton bags can use the same laws as above. This does not
cover wider decompositions such as (6).

### Proof of the true optimum

Write `T_k` for the first-kind Chebyshev polynomial, characterized by
`T_k(cos theta)=cos(k theta)`. Since `T_2(t)=2t^2-1` and
`T_a(T_b(t))=T_{ab}(t)`, every feasible point satisfies

\[
 u_j=v_j=T_{2^j}(x).
\]

Consequently `F=2T_N(x)^2+2>=2`. Taking
`x=cos(pi/(2N))` gives `T_N(x)=0` and attains `2`.

### Actual-measure witness below the threshold

Define two probability laws on `[-1,1]` by choosing `k` uniformly from
`{0,...,N-1}` and setting

\[
 X_+=\cos(2\pi k/N),\qquad X_-=\cos((2k+1)\pi/N). \tag{4}
\]

Repeated values are retained with their multiplicities. For every integer
`0<=a<N`, the two laws have the same moment of degree `a`. To see this,
expand `cos(theta)^a=2^{-a}(e^{i theta}+e^{-i theta})^a`.
Every nonconstant Fourier frequency has absolute value at most `a<N`, and
its average over either shifted `N`-point angular grid is zero. Both
averages are therefore zero for odd `a`, and
`2^{-a} binom(a,a/2)` for even `a`.

These are classical quadrature laws. With `q=N/2`, the minus law is the
`q`-node Chebyshev--Gauss rule, and the plus law is the `q+1`-node
Chebyshev--Gauss--Lobatto rule, both normalized for the arcsine probability
measure `dx/(pi sqrt(1-x^2))`. The latter has endpoint weights `1/(2q)`
and interior weights `1/q`. Their degree-`N-1` exactness is the familiar
quadrature mechanism behind the witness; it is not a new moment-matching
construction. See [NIST DLMF, Section 3.5(v)](https://dlmf.nist.gov/3.5.v)
for the Gauss--Chebyshev formula and Shen and Tang,
[*Spectral and High-Order Methods with Applications*](https://www.math.purdue.edu/~shen7/sp_intro12/book.pdf)
(2006), equations (1.3.9) and (1.3.11), for both sets of nodes and weights.

For each bag on the `u` chain use the joint law of
`(T_{2^{j-1}}(X_+),T_{2^j}(X_+))`; on the `v` chain use the same construction
with `X_-`. Every law is supported on its exact bounded quadratic relation.
Within either chain all overlap marginals agree completely. At the central
overlap they agree through degree `2r` whenever `2r<N`. Thus these laws
give a feasible point even for exact local-measure convexification.

Equation (4) gives `T_N(X_+)=1` and `T_N(X_-)=-1` almost surely, so its
objective is zero. The sparse moment relaxation cannot give a value below
zero, because each objective summand is the square of a linear polynomial
inside one terminal bag. Its value is therefore exactly zero.

### Exactness at the threshold

In an edge bag with variables `(a,b)` and equality `h=b-T_2(a)`, every
univariate polynomial `p` of degree `s` satisfies

\[
 p(b)-p(T_2(a))=h(a,b)q(a,b),\qquad \deg q\le2s-2. \tag{5}
\]

For the constant case the difference is zero. For each monomial `b^k`,
the usual difference-of-powers identity gives quotient degree at most
`2k-2`; linearity proves (5). If `2s<=2r`, the stated equality truncation
therefore gives `L(p(b))=L(p(T_2(a)))`.

Apply this identity successively to `p=T_{2^{m-j}}` on the edge ending at
level `j`, for `j=m,...,1`. The largest polynomial degree before
substitution is `N/2`, and the largest degree afterward is `N`.
The overlap identification permits passing each singleton expectation to
the preceding edge. When `2r>=N`, both terminal means equal the same
central expectation `L(T_N(x))`. Thus

\[
 L(F)=2+L(u_m^2)+L(v_m^2)+2\{L(v_m)-L(u_m)\}\ge2.
\]

The true optimizer gives a feasible Dirac moment point of value `2`, proving
exactness. This upper-bound argument needs only PSD and the displayed
equality moments; it does not require local representing measures.

There is also an explicit dual certificate, avoiding any reliance on strong
duality. Set `P_j=T_{2^{m-j}}` and, for either chain `w`, let

\[
 h_j^w=w_j-T_2(w_{j-1}),\qquad
 Q_j^w=\frac{P_j(w_j)-P_j(T_2(w_{j-1}))}{w_j-T_2(w_{j-1})}.
\]

The quotient is a polynomial by (5). Telescoping gives
`w_m-T_N(x)=sum_j h_j^w Q_j^w`, and hence

\[
 F-2=u_m^2+v_m^2+
       2\sum_{j=1}^m(h_j^vQ_j^v-h_j^uQ_j^u). \tag{5a}
\]

Every summand lies in one edge bag and has degree at most `N`. It is an
allowed SOS-plus-equality-ideal certificate at `2r>=N`. Below that threshold
the objective itself is a sparse SOS certificate of the lower bound zero,
and the local-measure witness gives the matching upper bound. Thus both
primal and dual values in (3) are attained.

**Infeasibility variant.** Replace the objective by the two endpoint
equalities `u_m=1` and `v_m=-1`. The bounded quadratic path system is
infeasible, but its edge-bag sparse moment relaxation is feasible exactly
at the integer orders `1<=r<2^{m-1}`. The same local laws satisfy both new
equalities pointwise below the threshold. At or above it, propagation forces
the two terminal means equal, contradicting their prescribed values.
Thus the obstruction also concerns certifying infeasibility. For `m=1`
the below-threshold range is empty.

## A constant-width repair

The path decomposition is not the only useful sparse decomposition. Use
the bag `C_1={x,u_1,v_1}`, followed, for each `j=2,...,m`, by

\[
 B_j=\{u_{j-1},v_{j-1},u_j\},\qquad
 C_j=\{v_{j-1},u_j,v_j\}. \tag{6}
\]

These bags, in the displayed order, form a path decomposition of width
two. Every original edge is covered, and every variable occurs in
consecutive bags. Match the full paired overlap moments through degree four
and use order `r=2`.

**Proposition 2 (candidate).** This width-two order-two moment relaxation
has value `2` for every `m`.

**Proof.** A PSD order-two moment matrix defines a positive semidefinite
bilinear form `L(pq)` on polynomials of degree at most two. Thus, if
`L(p^2)=L(q^2)=0`, then `L((p+q)^2)=L((p-q)^2)=0`, by Cauchy--Schwarz.

The two first equations imply that `u_1-T_2(x)` and `v_1-T_2(x)` have
zero square expectation in `C_1`: each square is its equality polynomial
multiplied by an allowed polynomial of degree two. The bilinear-form fact
gives `L((u_1-v_1)^2)=0`.

Inductively suppose that the preceding paired overlap has
`L((u_{j-1}-v_{j-1})^2)=0`. In `B_j`, write
`a=u_{j-1}`, `b=v_{j-1}`, `c=u_j`, `d=a-b`, and `s=a+b`.
The identity

\[
 4d^2-d^2s^2
 =2d^2(1-a^2)+2d^2(1-b^2)+d^4 \tag{7}
\]

is nonnegative under degree-four box localizers and PSD. Since `ds` has
degree two, PSD also gives `L(d^2s^2)>=0`. Therefore
`0<=L(d^2s^2)<=4L(d^2)=0`. It follows that
`L((T_2(a)-T_2(b))^2)=4L(d^2s^2)=0`.

The equality `c-T_2(a)=0` gives `L((c-T_2(a))^2)=0`. The bilinear-form
fact now yields

\[
 L((c-T_2(b))^2)=0. \tag{8}
\]

This degree-four polynomial involves only the paired separator `{b,c}`,
so (8) transfers to `C_j`. In `C_j`, the second chain equality gives
`L((v_j-T_2(b))^2)=0`. Subtracting the two zero-square polynomials gives
`L((u_j-v_j)^2)=0`, completing the induction. PSD with the constant
polynomial gives `L(u_m-v_m)=0`. The objective is therefore at least two,
as in Theorem 1, and a true optimizer attains two. This proves the
proposition.

The degree-four argument uses the explicit quadratic bounds `1-z^2>=0`.
If only linear bounds are included, adding these valid quadratic bounds
is part of this formulation claim. They are not silently assumed to be
available in every alternative hierarchy convention.

## A distinct perturbed chain retains a constant gap

The exact equalities between the two unperturbed trajectories are not
necessary for a large relaxation gap. Change only the first `v` equation to

\[
 v_1=(1-\delta)T_2(x),\qquad \delta=4^{-m}, \tag{9a}
\]

and keep all other equations and the objective unchanged. The two chains
now compute different functions. The altered map still sends `[-1,1]`
into itself. Only one coefficient has changed, and its binary encoding
has `O(m)` bits, so the full ordinary sparse encoding remains
`O(m log(m+1))`.

**Proposition 4 (perturbed separation).** The true minimum and the
width-two order-two moment lower bound are both at least `49/32`.
A rational sparse SOS certificate of degree four and polynomial encoding
size proves that lower bound.
For every integer order with `2r<2^m`, the edge-bag moment relaxation has
value at most `1/16`. Its gap from the true value is therefore at least
`47/32`. No exact threshold or exact optimum is asserted for the perturbed
instance.

**Proof of the true bound and weak edge relaxation.** The first trajectory
difference has magnitude at most `delta`. Since `T_2` is four-Lipschitz on
`[-1,1]`, all true trajectories satisfy

\[
 |u_m-v_m|\le4^{m-1}\delta=1/4. \tag{9b}
\]

For real numbers `u,v` and `d=u-v`,

\[
 (u-1)^2+(v+1)^2
   =2+u^2+v^2-2d
   \ge 2+\tfrac12d^2-2d.
\]

The last expression is decreasing for `d<=2`, so `|d|<=1/4` gives
the bound `2+(1/4)^2/2-2/4=49/32`.

For the weak relaxation use exactly the original two central laws (4),
but push the second through the altered chain. They still match all
central moments of degree below `N`, and all bag laws satisfy their own
equations and boxes. The first terminal state is exactly one. The second
differs by at most `1/4` from its unperturbed value minus one, by the same
Lipschitz estimate. Thus its objective is at most `1/16`.

**Proof of the width-two bound.** Let `L` denote the appropriate bag
functional. In the first bag the two equality polynomials imply the linear
relation `v_1-(1-delta)u_1=0` in all required moment products. Consequently

\[
 L((u_1-v_1)^2)=\delta^2L(u_1^2)\le\delta^2. \tag{9c}
\]

For a later pair of bags, keep the notation of the proof of Proposition 2.
Allowed equality multiples yield the exact identities in expectation

\[
\begin{split}
 L_{B_j}((c-T_2(b))^2)&=4L_{B_j}(d^2s^2),\\
 L_{C_j}((u_j-v_j)^2)&=L_{C_j}((c-T_2(b))^2).
\end{split} \tag{9d}
\]

For the first, subtract `4d^2s^2` from `(c-T_2(b))^2`; the difference
is `(c-T_2(a))[(c-T_2(a))+4ds]`. For the second, subtract the two
squares; the difference is a multiple of `v_j-T_2(b)` with multiplier
degree at most two. Both equality products have degree at most four.
Overlap consistency identifies the middle polynomial in (9d). Identity
(7) therefore gives

\[
 L((u_j-v_j)^2)\le16L((u_{j-1}-v_{j-1})^2).
\]

Together with (9c), the terminal bound is `L((u_m-v_m)^2)<=1/16`.
Write `t=L(u_m-v_m)`. PSD gives `|t|<=1/4` and
`L(u_m^2)+L(v_m^2)>=L((u_m-v_m)^2)/2>=t^2/2`. Expanding the objective
as before proves `L(F)>=49/32`. This completes the proof.

For completeness, the promised finite dual certificate is explicit. Put
`d_j=u_j-v_j` and `g=v_1-(1-delta)u_1`. The base identity is

\[
 \delta^2-d_1^2
 =\delta^2(1-u_1^2)+g(2\delta u_1-g). \tag{9e}
\]

Here `g` is a constant linear combination of the two first equality
polynomials, so its second term belongs to their truncated equality ideal.
For `j>=2`, set `a=u_{j-1}`, `b=v_{j-1}`, `c=u_j`, `e=v_j`,
`h=c-T_2(a)`, `k=e-T_2(b)`, and

\[
 R_B=h[h+4(a-b)(a+b)],\qquad
 R_C=k[k-2(c-T_2(b))].
\]

The local identities used in (9d) give

\[
 16d_{j-1}^2-d_j^2
 =8d_{j-1}^2(1-a^2)+8d_{j-1}^2(1-b^2)
   +4d_{j-1}^4-R_B-R_C. \tag{9f}
\]

The terms before `R_B,R_C` are valid degree-four local SOS or box
certificates in `B_j`; the two remaining terms are degree-four equality
multiples in `B_j,C_j`, respectively. Multiply (9e) by `16^{m-1}`, and
multiply each identity (9f) by `16^{m-j}` before summing. Their left sides
telescope to `1/16-d_m^2`. Finally use

\[
 F-\frac{49}{32}
 =\frac12(u_m+v_m)^2+4(d_m-\tfrac14)^2
    +\frac72(\tfrac1{16}-d_m^2). \tag{9g}
\]

This is an actual degree-four sparse SOS-plus-equality certificate. There
are `O(m)` displayed local terms, and every coefficient has `O(m)` bits;
the total ordinary encoding is polynomial. No strong-duality or attainment
assumption is used to certify this perturbed lower bound.

The perturbation scale is inverse exponential in chain length. Proposition
4 demonstrates persistence under a specified rational perturbation with
short encoding; it does not establish robustness to fixed-scale noise or
poorly known coefficients. A solver can also propagate the elementary
Lipschitz discrepancy bound directly. Therefore the perturbed example
continues to establish a relaxation-architecture separation, not a hard
optimization family.

## Meaning and limitations

The candidate is a sharply quantified separation between two decompositions
of the same fixed-degree bounded problem: minimizing graph width alone can
force exponential moment order, whereas modestly wider bags retain enough
correlation for a constant order proof. It could motivate decomposition
selection or propagation of synchronization relations in polynomial MINLP
relaxations. No algorithm for detecting the best extra correlations, no
runtime improvement on difficult instances, and no broad tractability result
are established.

The example is deliberately easy as an optimization problem. Repeated
symbolic substitution proves `u_j=v_j`, after which the objective lower
bound is immediate. A solver that identifies duplicate deterministic
computations removes the obstruction. The result therefore does not bound
arbitrary sparse SDP lifts, adaptive reformulations, dense moment methods,
or presolve. It contains no integer variables; continuous polynomial
optimization is a subclass of MINLP, but adding a disconnected binary would
not strengthen the claim.

The state map has derivative up to four and exponential compositional
sensitivity. The family does not show the same phenomenon for uniformly
contracting dynamics. Its possible importance is the exact hierarchy-order
and decomposition tradeoff, not an assertion that every sparse model is hard.

The individual local relations are uniformly regular. For

\[
 K=\{(a,b)\in[-1,1]^2:b=T_2(a)\},\qquad h(a,b)=b-T_2(a),
\]

the explicit repair `(a,b) -> (a,T_2(a))` remains inside the box, because
`T_2([-1,1])=[-1,1]`. Therefore

\[
 \operatorname{dist}_2((a,b),K)\le |h(a,b)|
 \quad\text{for every }(a,b)\in[-1,1]^2. \tag{9}
\]

With the equality encoded as the two inequalities `h>=0` and `-h>=0`,
the largest constraint violation is `|h|`. Thus the local error-bound
exponent and constant are both one, independently of chain length. Also
`||grad h||_2>=1` on the box. The lower bound does not arise from worsening
degree, coefficients, domains, or this local metric regularity. Global
compatibility and propagation remain distinct from local regularity.

**Corollary 3 (unavoidable instance dependence).** Fix any exponent
`alpha>0`. If a convergence guarantee for this edge-bag hierarchy takes the
form `2-rho_r<=C_m r^(-alpha)` for every integer `r>=1`, then, for `m>=2`,

\[
 C_m\ge2(2^{m-1}-1)^{\alpha}. \tag{10}
\]

This follows by taking the last order below the threshold in Theorem 1.
In particular no prefactor polynomial in `m` can make a fixed positive
convergence-rate exponent uniform over this family, despite (9) and all
the uniform local numerical bounds. This directly qualifies how
clique-size-dependent asymptotic exponents may be interpreted; it does not
contradict rates whose constants depend exponentially on the instance.

### Matching standard local normalization hypotheses

Some quantitative sparse Putinar results require a unit-ball certificate
in every bag and an error bound on the entire ambient unit cube, rather
than only the natural box in (9). These conditions can also hold uniformly
here. Rescale every state by one half. The local relation becomes

\[
 \widehat K=\{(a,b)\in[-1/2,1/2]^2:
       \widehat h(a,b)=b-4a^2+1/2=0\}. \tag{11}
\]

Use the four inequalities
`g_a=(1/4-a^2)/9`, `g_b=(1/4-b^2)/9`,
`g_+=widehat h/9`, `g_-=-widehat h/9`.
Their absolute values on the ambient cube `[-1,1]^2` are at most `1/2`.
The local Archimedean identity is

\[
 1-a^2-b^2=9g_a+9g_b+1/2. \tag{12}
\]

For the ambient error bound, let
`R=max(0,a^2-1/4,b^2-1/4,|widehat h(a,b)|)`.
Clip `a` to `a'` in `[-1/2,1/2]`, and set `b'=4(a')^2-1/2`.
Then `(a',b')` belongs to `widehat K` and
`|a-a'|<=max(0,a^2-1/4)<=R`.
The polynomial `4a^2-1/2` has Lipschitz constant eight on `[-1,1]`,
so `|b-b'|<=|widehat h(a,b)|+8|a-a'|<=9R`. Consequently

\[
 \operatorname{dist}_2((a,b),\widehat K)
 \le10R=90\max\{0,-g_a,-g_b,-g_+,-g_-\}. \tag{13}
\]

This gives uniform local exponent one, uniform constant ninety, and a
degree-two local unit-ball certificate. The numbers of local constraints,
their degrees, and their coefficients are uniformly bounded. The objective
becomes `(2u_m-1)^2+(2v_m+1)^2`, still with only two terms and uniform
norm and Lipschitz bounds. Invertible coordinate scaling preserves the
moment orders and values proved above. Thus this normalized family
satisfies these local hypotheses of the quantitative sparse Putinar
framework; their presence does not remove the necessary instance-size
dependence in (10).

## Prior-art comparison

The repository's
[earlier separator review](../notes/research-20260922-separator-novelty.md)
already identifies finite-feature approximation duality, Wasserstein
moment matching, and generic feature-count lower bounds as established
theory. This construction uses their familiar moment-matching mechanism.
The proposed additional statement is an exact exponential threshold for a
native fixed-coefficient quadratic path, with a constant-width repair.

- Balada Gaggioli, Henrion and Korda, *Composition and tensor train structure
  in polynomial optimization*, 19 April 2026,
  [arXiv:2604.17563v1](https://arxiv.org/abs/2604.17563v1): this is the closest
  current framework examined. Sections 2.1.1, 2.1.4 and 4 were read from
  the retained primary PDF. They introduce intermediate states, explicitly
  discuss growth of propagated monomial features under repeated squaring,
  and study the tradeoff between state dimension and polynomial degree.
  Their equation (21) uses the same full equality-ideal truncation as this
  note. Theorem 4.1 gives convergence, while Section 4.2 counts SDP size as
  linear in chain length **for fixed state dimension and relaxation order**.
  These statements do not supply a uniform order sufficient for a given
  accuracy. Theorem 1 here would complement that framework with an exact
  order requirement for a fixed-width quadratic family. The proposed
  distinction is the explicit matching lower/upper threshold and the
  width-one versus width-two comparison; state lifting and the general
  degree/width tradeoff are already established ideas.
- Fawzi, Saunderson and Parrilo, *Equivariant semidefinite lifts of regular
  polygons*, Mathematics of Operations Research 42(2), 472--494,
  [primary manuscript](https://arxiv.org/abs/1409.4379): the abstract and
  Theorems 1 and 7, inspected in the independent review, establish exact
  SOS order `ceil(N/4)` for a regular
  `N`-gon and an equivariant PSD lift of size `2n-1` for `N=2^n`. This is
  a strong conceptual precedent for exponential separation between standard
  polynomial degree and a structured lift. Our variables and two
  decompositions differ, and no equivalence has been established. A claim
  that exponential degree-versus-lift separation itself is new would be
  incorrect. The targeted theorem comparison does not rule out a deeper
  reformulation relating these constructions.
- Lasserre, *Convergent SDP-relaxations in polynomial optimization with
  sparsity*, SIAM J. Optim. 17 (2006), 822--843,
  [open manuscript](https://optimization-online.org/wp-content/uploads/2006/04/1367.pdf):
  Theorem 3.6 and its measure-gluing proof were inspected in the independent
  review. The running-intersection sparse hierarchy and asymptotic
  convergence are established background; the inspected theorem does not
  give this family's finite-order threshold.
- Korda, Magron and Rios-Zertuche, *Convergence rates for sums-of-squares
  hierarchies with correlative sparsity*, Mathematical Programming 209
  (2025), 435--473,
  [primary full text](https://link.springer.com/article/10.1007/s10107-024-02071-6),
  [arXiv](https://arxiv.org/abs/2303.14824): the full-text summary and Theorems
  6 and 8 were inspected on 2026-09-27. Their rate exponents depend on clique
  sizes, while constants contain instance information and regularity
  parameters. In particular, Theorem 8 allows its constants to depend on
  the full constraint list and collection of bags. The present family
  changes these with `m`, so the exact threshold is consistent with that
  theorem. No contradiction to their fixed-instance asymptotic rate is
  claimed. The primary PDF and text are retained in `structure-sources/`.
- Han, Jiao and Weissman, *Local moment matching*, COLT 2018,
  [primary paper](https://proceedings.mlr.press/v75/han18b/han18b.pdf), Lemma
  25: matching moments and best uniform polynomial approximation are dual.
  The angular-grid witness here is elementary Fourier quadrature, not a
  new moment-duality theorem.
- Bienstock and Munoz, *LP formulations for polynomial optimization
  problems*, SIAM J. Optim. 28 (2018), 1121--1150,
  [primary manuscript](https://arxiv.org/pdf/1501.00288): bounded-treewidth
  formulations with coefficient-scaled feasibility tolerances do not
  promise exact preservation of the hard quadratic dynamics used here.
  Precise theorem-level comparison remains to be completed.

Targeted searches for sparse moment exponential degree lower bounds,
Chebyshev path constructions, and correlative sparsity convergence located
these relevant sources but have not established originality. An unsuccessful
search is not evidence that no equivalent construction exists.

## Verification record

The [independent review](chebyshev-proof-review.md) confirms Theorem 1 and
Propositions 2 and 4. It found the explicit dual certificates and sharpened
an initial width-three repair to the width-two construction above. Further
independent review of the contribution and source comparison is pending.

The targeted command
`python3 research-20260927/check_structure_frontier.py` passed. Its exact
rational Fourier averages checked 254 central matched moments, seven first
different moments, 598 local equality moments, and 160 internal overlap
moments. Symbolic arithmetic checked 32 Chebyshev quotient degree bounds
and eight identities used by the width-two repair and perturbed certificate.
Seven perturbed witness objectives were evaluated exactly and satisfied
the stated upper bound. These are finite reconstructions of proof
ingredients, not a computational proof for all `m`, a numerical SDP
experiment, or Lean verification.

The independent reviewer additionally ran
`python3 research-20260927/check_chebyshev_review.py`, checking six identities,
the width-two running-intersection property, and weighted telescoping for
`m=1,...,20`. That command and its result belong to the reviewer, rather
than this note's author's own run. No project-wide checks or CI inspection
were run for this investigation.
