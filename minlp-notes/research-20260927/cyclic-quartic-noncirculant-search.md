# The cyclic degree is optimal within strongly connected quadratic binomial networks

Date: 2026-09-28. Status: proof and full text independently reviewed.
The graph bound below is a short
consequence of classical interlace-polynomial identities. No separate
priority claim is made for that consequence or the lattice translation.

The [cyclic quartic construction](cyclic-quartic-exponential-degree.md)
uses a system of $n+1$ quadratic binomials to create its unique zero.
Permuting that system, or allowing a general strongly connected graph
with two outgoing arcs per vertex, cannot increase its field degree.
This closes one natural attempt to strengthen the construction. It
does not bound the degree of arbitrary rational SOS quartics.

**Theorem.** Let $n\geq2$, $m=n+1$, and let $D$ be a strongly
connected directed multigraph on vertices $0,\ldots,n$, with exactly
two outgoing arcs at each vertex. Loops and repeated arcs are allowed.
Write their endpoints as $a(i),b(i)$. Fix $x_0=1$, choose
$c_i\in\mathbb Q\setminus\{0\}$, and impose all $m$ equations

\[
 q_i(x)=x_i^2-c_i x_{a(i)}x_{b(i)}=0
 \qquad(0\leq i<m).                              \tag{1}
\]

If the common real zero set is a singleton $\{p\}$, then $p$ is
algebraic and

\[
 [\mathbb Q(p):\mathbb Q]
 \leq\frac{2^{n+1}-(-1)^{n+1}}3.                 \tag{2}
\]

The bound is attained for every $n\geq2$ by the cyclic construction.
If $D$ is not Eulerian, the stronger bound
$[\mathbb Q(p):\mathbb Q]\leq2^{n-1}-1$ holds.
Neither positive coordinates nor positive $c_i$ are needed for this
upper bound.

The assumption that every vertex contributes its equation, including
vertex zero, matters. One grounded determinant alone generally gives
the wrong arithmetic degree for a non-Eulerian graph.

## The full lattice index counts complex roots

Let $A$ be the adjacency matrix, counting arc multiplicities, and put
$L=2I-A$. Let $B$ be the $m\times n$ integer matrix obtained by
deleting column zero from $L$. Its rows are the exponent differences
of (1). Denote by $\tau_i>0$ the number of arborescences directed
toward root $i$, with parallel arcs distinguished, and set

\[
 g=\gcd(\tau_0,\ldots,\tau_n).
\]

The directed matrix-tree theorem identifies $\tau_i$ with the
principal cofactor of $L$. Strong connectivity gives rank $m-1$,
right kernel spanned by the all-ones vector, and adjugate
$\mathbf1\tau^{\mathsf T}$. Thus the signed maximal minor of $B$
obtained by deleting row $i$ is, up to its determinant sign,
$\tau_i$. The Smith normal form gives

\[
 [\mathbb Z^n:\operatorname{row}_{\mathbb Z}(B)]=g.            \tag{3}
\]

Every complex solution of (1) has nonzero coordinates. Indeed
$x_0=1$; if $x_i\ne0$, its equation and $c_i\ne0$ force both
outgoing neighbors to be nonzero. Reachability from zero then covers
every vertex.

Normalize by the given real solution: $x_i=p_i y_i$, with $y_0=1$.
Equation (1) becomes

\[
 y_i^2=y_{a(i)}y_{b(i)}.
\]

The normalized complex solutions are exactly the characters of the
finite group

\[
 \Gamma=\mathbb Z^n/\operatorname{row}_{\mathbb Z}(B)
\]

into $\mathbb C^\times$. There are $g$ such characters. If
$e$ is the exponent of $\Gamma$, then $e$ times each standard
basis vector belongs to the row lattice. Applying that integer
combination of the original equations shows $p_j^e\in\mathbb Q$.
Consequently every coordinate is algebraic. Every embedding of
$\mathbb Q(p)$ into $\mathbb C$ gives a distinct common zero of
the rational equations, so

\[
 [\mathbb Q(p):\mathbb Q]\leq g.                            \tag{4}
\]

The real normalized solutions are precisely
$\operatorname{Hom}(\Gamma,\{1,-1\})$, because a real number
of finite multiplicative order is $1$ or $-1$. A finite abelian
group has no nontrivial homomorphism to $\{1,-1\}$ exactly when
its order is odd. Thus, conditional on the existence of one real
solution, uniqueness is equivalent to

\[
 g\text{ is odd}.                                           \tag{5}
\]

All complex roots are nonsingular as an overdetermined system: at a
root $z$, the Jacobian equals
$\operatorname{diag}(z_i^2)B\operatorname{diag}(z_1^{-1},\ldots,z_n^{-1})$,
which has column rank $n$. No multiplicity is hidden in the root count.
The lattice-character interpretation is standard binomial-ideal theory;
the [binomial prior comparison](cyclic-quadratic-toric-prior.md) records
its relationship to Eisenbud--Sturmfels and directed toppling ideals.
The elementary argument here is included to specify the exact index
and the role of all $m$ equations.

## Non-Eulerian graphs have a smaller index

The vector $\tau$ lies in the left kernel of $L$. Hence
$w_i=\tau_i/g$ form a primitive positive integer stationary vector.
It is the all-ones vector exactly when every indegree is two, which
is the Eulerian case.

At each nonroot vertex, an arborescence chooses one of the two outgoing
arcs. Some of the $2^n$ choices contain cycles or loops and are
invalid, but every valid arborescence is among them. Therefore

\[
 \tau_i\leq2^n\qquad(0\leq i<m).                           \tag{6}
\]

If the graph is non-Eulerian, at least one primitive integer $w_i$
is at least two. It follows that $g\leq2^{n-1}$. By (5), $g$ is
odd, so for $n\geq2$,

\[
 [\mathbb Q(p):\mathbb Q]\leq g\leq2^{n-1}-1
   <\frac{2^{n+1}-(-1)^{n+1}}3.                              \tag{7}
\]

At $n=1$, the strict comparison fails: both the weak bound
$2^{n-1}$ and the right side of (2) equal one. For example,
$A=\left(\begin{smallmatrix}1&1\\2&0\end{smallmatrix}\right)$
is strongly connected and non-Eulerian, with rooted cofactors $(2,1)$
and $g=1$. This boundary case is outside the stated range and does
not affect the weak degree bound.

## The Eulerian bound follows from classical interlace identities

In the Eulerian case all rooted cofactors equal $g$. The BEST theorem
identifies this common value with the number of Euler tours modulo
cyclic rotation; the usual factor
$\prod_v(\operatorname{outdeg}(v)-1)!$ is one. Equivalently fix
one distinguished first arc, rather than multiplying by the number
of possible starting positions. The interlace graph $H$ of any Euler
tour has $m$ vertices and satisfies $q_H(1)=g$, where $q_H$ is
the one-variable interlace polynomial.

The needed classical facts are:

- $q_H(x)=\sum_{j\geq1}\alpha_jx^j$ has nonnegative integer
  coefficients and no constant term for a nonempty graph.
- $q_H(2)=2^m$.
- If $r=\operatorname{rank}_{\mathbb F_2}(I+A_H)$, then
  $q_H(-1)=(-1)^r2^{m-r}$.

The first two follow from Theorem 12 and Remark 17 of
[Arratia--Bollobás--Sorkin](https://arxiv.org/pdf/math/0209045);
their Theorem 9 supplies the Euler-tour interpretation. The last
identity is Theorem 1 of
[Balister--Bollobás--Cutler--Pebody](https://www.memphis.edu/msci/people/pbalistr/interlace.pdf).
Both primary papers were inspected directly. The
[source audit](permuted-cycle-interlace-prior.md) records the precise
conventions and related prior results. Loops and distinguished
parallel arcs in the directed graph are permitted; its interlace
graph is simple.

Because $q_H(1)=g$ is odd, $q_H(-1)$ is odd too. The third identity
forces $r=m$ and $q_H(-1)=(-1)^m$. For every $j\geq1$,
$2^j-(-1)^j\geq3$. Nonnegative coefficients now give

\[
 3g\leq\sum_{j\geq1}\alpha_j\bigl(2^j-(-1)^j\bigr)
      =q_H(2)-q_H(-1)=2^m-(-1)^m.                            \tag{8}
\]

Equations (4), (7), and (8) prove (2). Equality in the interlace
inequality is equivalent to $\deg q_H\leq2$. No graph-theoretic
classification of that equality case is needed or claimed here.

## Why this covers the weighted energy extension

The primitive positive stationary vector $w$ gives, in normalized
coordinates,

\[
 \sum_i w_i(Y_i^2-Y_{a(i)}Y_{b(i)})
 =\frac12\sum_iw_i(Y_{a(i)}-Y_{b(i)})^2.                    \tag{9}
\]

Stationarity is exactly the equality of the diagonal coefficients
on the two sides. The undirected multigraph with edges
$\{a(i),b(i)\}$ is connected precisely when $g$ is odd: modulo
two, $B$ is its incidence matrix with the anchored column deleted,
and this matrix has full column rank exactly when the graph is
connected. Full rank modulo two is equivalent to the index (3)
being odd.

Thus the unique-real-root case has a positive definite grounded
quadratic energy, including nonuniform weights. Its real coefficients
can support the same qualitative exposing-quadratic strategy used
in the cyclic quartic construction. Equation (2) shows that changing
this graph or these weights cannot improve the arithmetic degree
within the stated binomial class. No uniform coefficient-size or
conditioning bound for all these alternative graphs is asserted.

## A normal form for the minimal binomial exposing strategy

The network assumption also follows from a natural exposing hypothesis.
Let $m=n+1$ rational homogeneous quadratic binomials
$r_0,\ldots,r_n$ in $X_0,\ldots,X_n$ vanish at
$p=(1,p_1,\ldots,p_n)$, where every coordinate is nonzero.
Suppose a real combination

\[
 Q(X)=\sum_{j=0}^n\lambda_jr_j(X)
\]

is positive semidefinite and its kernel is exactly $\mathbb Rp$.
Then, after permuting and rationally rescaling the equations, they
have the form (1) for a strongly connected two-out graph. In
particular their anchored zero has field degree at most (2).

To prove this, every diagonal entry of $Q$ is strictly positive.
A zero diagonal entry of a positive semidefinite matrix would put
the corresponding coordinate vector in its kernel, which is
impossible because $p$ has all coordinates nonzero and $m\geq2$.
Each nonzero binomial summand $\lambda_jr_j$ can contribute a
positive coefficient to at most one square monomial $X_i^2$.
If both its monomials were squares with positive coefficients, it
could not vanish at $p$.

The $m$ positive diagonal entries must therefore be covered by the
$m$ summands one each. Every multiplier is nonzero, and each summand
has one distinct positive square monomial. Identical monomials are
combined first; an identically zero polynomial or a single nonzero
monomial could not supply a missing positive diagonal while vanishing
at $p$. After assigning its unique positive square to vertex $i$,
the original rational equation can be rescaled to
$X_i^2-c_iX_{a(i)}X_{b(i)}=0$ with $c_i\in\mathbb Q^\times$.

Normalize $X_i=p_iY_i$. The contribution of its $i$th row to $Q$
is $h_i(Y_i^2-Y_{a(i)}Y_{b(i)})$ with $h_i>0$.
The kernel condition at the all-ones vector gives
$2h=A^{\mathsf T}h$. A directed graph with such a strictly positive
stationary vector has no arcs between distinct strongly connected
components. For example, a source component has no incoming flow;
summing stationarity over it forces its outgoing flow to vanish,
and positivity excludes any outgoing arc. Remove this component
and repeat. Each resulting component contributes its independent
indicator vector to the kernel of the normalized form
$Q(p_0Y_0,\ldots,p_nY_n)$, by the energy identity (9).
In the original coordinates these vectors are multiplied coordinatewise
by $p$. Corank one consequently forces a single component.

Finally, the exposing hypothesis itself ensures anchored real
uniqueness: if all $r_j$ vanish, then $Q=0$, so $X\in\mathbb Rp$;
$X_0=1$ then forces $X=p$. This proves every hypothesis needed for
the network degree bound. The diagonal-cover argument also shows
that fewer than $m$ quadratic binomials cannot span such an exposing
form at a point with all coordinates nonzero. This is a statement
about binomial equations and the stated exposing form, not a lower
bound for general polynomial SOS representations.

## Exact permutation search and its limits

The initial search kept the neighbor pairs as a Hamiltonian cycle
and assigned diagonal squares through an arbitrary permutation $p$:

\[
 Y_{p(i)}^2-Y_iY_{i+1},\qquad
 p(i)\notin\{i,i+1\},\qquad i\pmod m.
\]

Its exponent matrix is $2P-I-S$. Left permutation by $P^{-1}$
gives a two-in/two-out Laplacian. Modulo two the original matrix is
$I+S$, whose grounded cofactor is odd. Hence (8) proves the
all-dimension bound for this search class. The cyclic assignment
$p(i)=i+2$ attains it.

The [retained exact checker](check_permuted_cycle_degree_search.py)
exhaustively considered every admissible permutation for
$m=3,\ldots,10$:

| Vertices $m$ | Admissible permutations | Maximum cofactor |
| --- | ---: | ---: |
| 3 | 1 | 3 |
| 4 | 2 | 5 |
| 5 | 13 | 11 |
| 6 | 80 | 21 |
| 7 | 579 | 43 |
| 8 | 4,738 | 85 |
| 9 | 43,387 | 171 |
| 10 | 439,792 | 341 |

Every maximum equals $(2^m-(-1)^m)/3$, and a maximizing cyclic
witness has Smith invariants $1,\ldots,1,g$. Cofactor and largest
Smith invariant are not interchangeable in general. For instance,
at $m=6$, $p=(2,0,1,5,3,4)$ gives invariants $(1,1,1,3,3)$:
the group has order nine but is not cyclic. The degree upper bound
uses group order and does not assume cyclicity. The main construction
proves equality of field degree by its separate Eisenstein argument.

The targeted command

```text
python research-20260927/check_permuted_cycle_degree_search.py --max-size 10
```

passed the permutation search and Smith checks. Exact Bareiss
determinants were compared with SymPy determinants for every
permutation through $m=6$. After adding the general-network check,
a targeted `python - <<'PY'` invocation of its new function enumerated
every strongly connected two-out multigraph at $m=3,4$, including
loops and repeated arcs. There were respectively 65 and 2,325 such
graphs, of which 42 and 1,296 had odd lattice index. Their maximum
odd indices were three and five. It checked the primitive stationary
bound, Eulerian distinction, cofactor choice bound, and odd-index
degree bound. These finite checks do not prove (2); the proofs above
do. No project-wide verification or CI inspection was run.

The [full-text adversarial review](cyclic-quartic-binomial-bound-review.md)
found no unresolved gap, including in the weighted energy and minimal
binomial normal-form arguments. Its
[detailed reconstruction](quadratic-binomial-network-degree-review.md)
also independently checked all strongly connected two-out multigraphs
through four vertices. The reviewer contributed to the interlace
literature investigation but did not develop the non-Eulerian extension
or the exposing normal form; that distinction is recorded explicitly.
The $n=1$ strictness issue was found before this theorem was stated and
is preserved above as a boundary warning.

## Research consequence

The cyclic construction attains the exact maximum degree in this
strongly connected quadratic binomial network class. To exceed it,
the residual-system approach must leave at least one defining feature
of that class, for example by using genuine sums of several monomials
in its rational quadratic equations. This is a restriction on the
construction method, not a universal upper bound for strongly convex
quartics, rational SOS representations, or singleton convex sets.
