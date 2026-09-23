# Cut conservation forces large multipliers in signed-copy LPs

Date: 2026-09-02

## Main result

Signed-copy equalities turn central-path slack asymmetry into an ordinary
positive flow demand after a prefix-sign gauge.  Every output cut must carry
the sum of those demands.  For an output set \(S\), this forces

\[
 \|y_{\partial S}\|_\infty
 \ge \frac{2\mu a}{Q^2-a^2}\frac{|S|}{|\partial S|},
 \qquad
 \|y_{\partial S}\|_2
 \ge \frac{2\mu a}{Q^2-a^2}\frac{|S|}{\sqrt{|\partial S|}},
\]

whenever \(|d_v|\ge a>0\) and \(q_v\le Q\) on \(S\).  Thus uniformly
bounded canonical equality multipliers require

\[
                 \mu=O\!\left(\frac{|\partial S|}{|S|}\right).
\]

The path multiplier law
\(\alpha_j=(32/9)\mu\tau_j(P-j)\) is the one-boundary-edge special case.
The graph theorem explains the general tradeoff: a large signed-copy region
can avoid dual accumulation only by providing proportionally many boundary
rows through which its central demand can leave.

The graph structure is not needed for a global obstruction.  For an arbitrary
pair-antisymmetric equality block \(Cd=b_a\), exact centrality and a
pair-symmetric objective imply the exact work identity

\[
 b_a^Ty=\sum_v\frac{2\mu d_v^2}{q_v^2-d_v^2}.
\]

At a pair-symmetric Newton start, its linear analogue is

\[
 r_a^T\Delta y=\Delta d^T
 \operatorname{Diag}\!\left(\frac{s_v^0}{2x_v^0}\right)\Delta d.
\]

Both right sides are positive.  These are paired specializations of standard
KKT virtual-work and Schur-complement energy identities, not new general
optimization identities.  They survive arbitrary invertible, possibly
nonorthogonal, row mixing **within the pair-antisymmetric block**: the
multiplier and the tracked antisymmetric right-hand side transform
contragrediently, leaving their pairing unchanged.  Their norm product cannot
fall below this invariant work.  This does not mean that shrinking the
multiplier must increase the right-hand-side norm relative to its value in
the original representation: when the original vectors are poorly aligned,
a basis change can reduce both norms while preserving their pairing.

Here and below, "positive" means strictly positive when the corresponding
difference vector is nonzero; the work is zero for the zero difference.

There is a stronger resource consequence for a parity amplifier.  If every
one of \(N\) input bits occurs only in its own local signed rows, flipping any
bit reverses \(K\) output vertices, and \(M_{\rm dep}\) is the total number of
input-dependent signed rows, then

\[
 M_{\rm dep}B_{\rm row}\|y\|_\infty
 \ge \frac{2\mu a}{Q^2-a^2}KN,
 \qquad
 M_{\rm dep}B_{\rm row}\|\Delta y\|_\infty
 \ge \rho aKN,
\]

for exact central and pair-symmetric Newton systems, respectively.  Here
\(\rho=\min_v s_v^0/(2x_v^0)\), and \(B_{\rm row}\) is the largest magnitude
used to scale a graph equality row.  Thus
\(M_{\rm dep}=\Theta(N)\), \(K=\Theta(N)\), bounded row scale, and constant local scale force
an \(\Omega(N)\) multiplier.  Dual homogeneity evades this frontier precisely
by making \(\rho=\Theta(1/N)\).

For rows scaled by factors of magnitude at most \(B\), the same parity
frontiers hold with \(B\|y\|_\infty\) and
\(B\|\Delta y\|_\infty\) in place of the multiplier norms.  Thus bounded row
scaling does not evade the result; scaling large enough to remove accumulation
pays the same factor in coefficient magnitude.  The result remains a theorem
for signed-copy rows and their diagonal rescalings, not an invariant lower
bound under arbitrary changes of equality-row basis.

The last qualification applies to the *cut and incidence* bounds.  The global
work identities continue to hold under arbitrary invertible row-basis changes,
but they give a product tradeoff rather than coordinatewise edge-capacity
control.

Finally, bounded-bit direct antisymmetric objective or Newton data cannot
cancel a fixed parity-output cut on every input.  After switching, its average
contribution is its full-parity Fourier coefficient.  If that coefficient
vanishes, some input carries at least the input-average positive
central/Newton demand, and hence any uniform pointwise lower bound on that
demand.  Cancellation on every input therefore needs a direct full-parity
component or a multiplier-mediated/global source.

## 1. Signed-copy model

Let \(G=(V\cup T,E)\) be a directed multigraph.  Vertices in \(V\) carry
nonnegative LP variables \(x_v^+,x_v^-\), and vertices in \(T\) are fixed
terminals used to model anchor rows.  Put

\[
                  d_v=x_v^+-x_v^-,
                  \qquad q_v=x_v^++x_v^-.
\tag{1}
\]

Every oriented edge \(e=(u,v)\) has a sign \(a_e\in\{\pm1\}\) and represents
the equality

\[
                         d_v-a_ed_u=0,
\tag{2}
\]

with multiplier \(y_e\).  If one endpoint is a terminal, orient the edge from
the terminal toward its variable endpoint and move the fixed terminal value
to the right-hand side; the row then has only one variable endpoint.  Parallel
edges are allowed and are counted with multiplicity.

Restrict attention to one graph component, and let \(V\) denote its variable
vertices.  Assume:

1. the point is primal--dual feasible and exactly central,
   \(x_v^\pm s_v^\pm=\mu>0\);
2. \(d_v\ne0\) for every \(v\in V\);
3. the objective is pair-symmetric, \(c_v^+=c_v^-\); and
4. every equality other than (2) has the same coefficient on \(x_v^+\) and
   \(x_v^-\), so its contribution cancels when the two stationarity equations
   are subtracted.

The fourth assumption holds for the cap and reference rows in the parity LP
families.  It is essential: an additional pair-antisymmetric objective or
constraint can inject a source of either sign and cancel the central demand.

Let \(B_a\) be the signed incidence matrix, with row \(e=(u,v)\) containing
\(+1\) in column \(v\) and \(-a_e\) in column \(u\).  Terminal columns are
omitted.  Let \(B\) be the corresponding ordinary oriented incidence matrix,
again restricted to the variable columns.

## 2. Gauge-flow theorem

### Theorem 1 (signed centrality becomes positive divergence)

Define \(\tau_v=\operatorname{sgn}(d_v)\).  On each variable--variable edge,
feasibility of (2) implies

\[
                 a_e=\tau_u\tau_v
\tag{3}
\]

There is a sign gauge of the edge multipliers,
\(z_e=\tau_{h(e)}y_e\), for which

\[
                 B^Tz=g,
 \qquad
 g_v=\frac{2\mu|d_v|}{q_v^2-d_v^2}>0.
\tag{4}
\]

For every \(S\subseteq V\), let \(\partial S\) be the multiset of graph
edges crossing from \(S\) to its complement or to a terminal.  In particular,
a terminal edge is in \(\partial S\) exactly when its unique variable endpoint
lies in \(S\).  When \(\partial S\ne\varnothing\),

\[
\begin{aligned}
 \sum_{e\in\partial S}|y_e|&\ge G_S,\\
 \|y_{\partial S}\|_\infty&\ge\frac{G_S}{|\partial S|},\\
 \|y_{\partial S}\|_2&\ge\frac{G_S}{\sqrt{|\partial S|}},
 \qquad
 G_S:=\sum_{v\in S}\frac{2\mu|d_v|}{q_v^2-d_v^2}.
\end{aligned}
\tag{5}
\]

If \(S\ne\varnothing\) and \(\partial S=\varnothing\), (5) says that no such
positive central point exists.  Thus every nonzero signed-copy component with
symmetric local data must ultimately connect to an anchor or another
antisymmetric source.

**Proof.**  Subtract the \(x_v^-\) stationarity equation from the
\(x_v^+\) equation.  Pair symmetry cancels every term except the signed graph
rows and the two slacks:

\[
                2(B_a^Ty)_v+s_v^+-s_v^-=0.
\tag{6}
\]

Centrality and (1) give

\[
 \frac{s_v^--s_v^+}{2}
 =\frac\mu2\left(\frac1{x_v^-}-\frac1{x_v^+}\right)
 =\frac{2\mu d_v}{q_v^2-d_v^2}.
\tag{7}
\]

Let \(R=\operatorname{Diag}(\tau_v)\) on vertices and
\(T_E=\operatorname{Diag}(\tau_{h(e)})\) on edges.  On variable--variable
edges, (3) gives the switching identity

\[
                        B_aR=T_EB.
\tag{8}
\]

On a terminal edge, both incidence matrices
have the single restricted coefficient \(+1\) at its variable head, so (8)
holds there as well.

Equations (6)--(8), multiplied by \(R\), yield (4) with \(z=T_Ey\).
In particular, \(|z_e|=|y_e|\).

Sum (4) over \(v\in S\).  Every internal edge cancels in the ordinary
incidence matrix, leaving a signed sum over \(\partial S\):

\[
 G_S
 =\left|\sum_{e\in\partial S}\epsilon_{S,e}z_e\right|
 \le\sum_{e\in\partial S}|y_e|,
 \qquad \epsilon_{S,e}\in\{\pm1\}.
\tag{9}
\]

The maximum-norm bound follows by dividing by \(|\partial S|\), and the
Euclidean bound follows from Cauchy--Schwarz. \(\square\)

The nonzero feasible \(d\) also proves that the signed graph is balanced on
the component: (3) switches every edge sign to positive.  The theorem does
not need balance as a separate promise.

### Corollary 2 (row-scaling-invariant physical force)

Allow each graph equality to be written as

\[
                     r_e(d_v-a_ed_u)=0,
 \qquad r_e\ne0,
\tag{R1}
\]

where the row scales are fixed and public, and put
\(B_{\rm row}:=\max_e|r_e|\).  Define the physical edge force

\[
                              f_e=r_ey_e.
\tag{R2}
\]

Then Theorem 1 holds verbatim with \(f\) in place of \(y\).  In particular,

\[
 \sum_{e\in\partial S}|r_ey_e|\ge G_S.
\tag{R3}
\]

If \(\|y_{\partial S}\|_\infty\le Y\), this implies the scale-aware capacity
bound

\[
               B_{\rm row}Y|\partial S|\ge G_S.
\tag{R4}
\]

The same statements hold for a Newton direction after replacing
\(f_e\) by \(r_e\Delta y_e\) and \(G_S\) by
\(\sum_{v\in S}g_v^{\rm N}\).

**Proof.**  The weighted graph block is
\(\operatorname{Diag}(r)B_a\), so its stationarity contribution is
\(B_a^T\operatorname{Diag}(r)y=B_a^Tf\).  Every switching and cut step in
Theorem 1 therefore applies to \(f\).  Finally,
\(|f_e|\le B_{\rm row}Y\) gives (R4). \(\square\)

Thus arbitrary row scaling does not remove the conservation law.  It can make
the coordinate multipliers small only by increasing coefficient magnitude.
The invariant object is the stationarity contribution \(r_ey_e\), called the
physical force here; the canonical unit-row case has \(B_{\rm row}=1\).
The scale may be negative: its sign is already included in \(f_e\), and no
positivity assumption on \(r_e\) is used.
Because \(B_{\rm row}=\max_e|r_e|\), a scaled graph row contains an entry of
magnitude \(B_{\rm row}\), and the normalization of any exact block encoding
of that matrix is at least \(B_{\rm row}\).  Zero row scales are excluded because they delete
the signed-copy equality rather than rescale it.  If scales themselves depend
on hidden input bits, those extra dependent coefficient positions must also
be counted in the oracle resource.

## 3. Isoperimetric multiplier law

### Corollary 3 (volume-to-boundary tradeoff)

Suppose on \(S\) that

\[
                         |d_v|\ge a>0,
                  \qquad q_v\le Q.
\tag{10}
\]

Then necessarily \(Q>a\), and

\[
 G_S\ge\frac{2\mu a}{Q^2-a^2}|S|,
\tag{11}
\]

and hence

\[
\boxed{
 \|y_{\partial S}\|_\infty
 \ge\frac{2\mu a}{Q^2-a^2}\frac{|S|}{|\partial S|},
 \qquad
 \|y_{\partial S}\|_2
 \ge\frac{2\mu a}{Q^2-a^2}\frac{|S|}{\sqrt{|\partial S|}}.}
\tag{12}
\]

In particular, if all canonical boundary multipliers have magnitude at most
\(Y\), then

\[
                 \mu\le
 \frac{Y(Q^2-a^2)}{2a}\frac{|\partial S|}{|S|}.
\tag{13}
\]

**Proof.**  Positivity gives \(q_v>|d_v|\), and
therefore \(Q>a\).  Moreover,
\(q_v^2-d_v^2\le Q^2-a^2\).  Substitute this in (4)--(5). \(\square\)

Thus the relevant graph parameter is the edge expansion of the copied output
region.  A path suffix of length \(L\) has one boundary edge and forces a
multiplier of order \(\mu L\).  More generally, avoiding accumulation at
fixed \(\mu,a,Q,Y\) requires \(|\partial S|=\Omega(|S|)\).

### 3.1 A graph-free central work identity

The global multiplier obstruction does not require incidence rows.  Let
\(C\in\mathbb R^{m_a\times |V|}\) be an arbitrary pair-antisymmetric equality
block, meaning that its contribution to the primal equalities is

\[
                         Cd=b_a,
\tag{C1}
\]

and its coefficients in the \(x^+\) and \(x^-\) columns are \(C\) and
\(-C\), respectively.  Other equality rows may be present, provided their
two columns are identical.  Let \(y_a\) denote the multipliers of \(C\).

### Theorem 4 (exact central work)

At every primal--dual feasible central point with a pair-symmetric objective,

\[
 \boxed{
 b_a^Ty_a
 =\sum_{v\in V}\frac{2\mu d_v^2}{q_v^2-d_v^2}\ge0.}
\tag{C2}
\]
The inequality is strict if and only if \(d\ne0\).

Consequently, if \(|d_v|\ge a>0\) and \(q_v\le Q\) on at least \(L\)
coordinates, then

\[
 \|y_a\|_\infty
 \ge \frac{2\mu a^2L}{(Q^2-a^2)\|b_a\|_1},
 \qquad
 \|y_a\|_2
 \ge \frac{2\mu a^2L}{(Q^2-a^2)\|b_a\|_2}.
\tag{C3}
\]

The corresponding inequality is interpreted as impossibility when the
denominator is zero.  In particular, a homogeneous pair-antisymmetric block
\(Cd=0\) cannot support a nonzero exactly central difference vector under
pair-symmetric local data unless some additional antisymmetric source is
present.

**Proof.**  Subtracting the two stationarity equations gives

\[
 2C^Ty_a+s^+-s^-=0,
 \qquad
 (C^Ty_a)_v=\frac{2\mu d_v}{q_v^2-d_v^2}.
\tag{C4}
\]

Take the inner product with \(d\) and use \(Cd=b_a\).  This proves (C2).
Every summand is nonnegative because \(q_v>|d_v|\), and it is positive
exactly when \(d_v\ne0\).  The margin assumptions
lower-bound the right side by
\(2\mu a^2L/(Q^2-a^2)\); Hölder's inequality proves (C3). \(\square\)

The scalar \(b_a^Ty_a\) is invariant under every invertible equality-row
change of basis within this block.  Indeed, if \(C'=UC\) and \(b_a'=Ub_a\),
then the corresponding multiplier is \(y_a'=U^{-T}y_a\), so

\[
                         (b_a')^Ty_a'=b_a^Ty_a.
\tag{C5}
\]

No row independence or multiplier uniqueness is needed: (C2) holds for every
multiplier satisfying stationarity, even when \(C\) is rank deficient or has
redundant rows.  Appending zero-right-hand-side redundant rows does not alter
the work identity, although it can change the coordinate norm of a chosen
multiplier and weaken a representation-dependent bound.

Equation (C5) gives
\(\|b_a'\|_2\|y_a'\|_2\ge b_a^Ty_a\) and
\(\|b_a'\|_1\|y_a'\|_\infty\ge b_a^Ty_a\).  Thus row mixing cannot make
either norm product smaller than the positive work.  This statement tracks
the pair-antisymmetric source \(b_a\).  If these rows are mixed with
pair-symmetric rows, the full transformed LP right-hand side is generally not
the work vector; the antisymmetric component must be transformed and tracked
separately.  The cut theorem is stronger when incidence structure is available:
it localizes this global work to individual output boundaries rather than only
bounding a residual--multiplier product.

### 3.2 Two-input central comparison with a common public source

The one-input positivity theorem assumes pair-symmetric local data.  A
two-input statement survives a pair-antisymmetric source, provided the
source is the **same numerical vector** in the original pair coordinates on
both inputs.

Consider two feasible exact central points \(p\in\{+,-\}\) on a common graph
topology.  Their edge signs and central parameters may differ.  Include
public nonzero row scales \(r_e\), put \(f_e^p=r_ey_e^p\), and suppose their
subtracted stationarity equations have the form
\[
 (B_{a^p}^Tf^p)_v
 =h_v+\frac{2\mu_p d_v^p}{(q_v^p)^2-(d_v^p)^2},
 \qquad p\in\{+,-\},
\tag{C6}
\]
for one common vector \(h\).  Let \(S\subseteq V\), and assume
\[
 d_v^+>0,\qquad d_v^-<0\qquad(v\in S).
\tag{C7}
\]
More generally, the same proof applies after one common sign gauge, whenever
the two signs are opposite pointwise on \(S\).  Define
\[
 g_v^p=\frac{2\mu_p|d_v^p|}
                  {(q_v^p)^2-(d_v^p)^2}>0.
\]
Then
\[
 \boxed{
 \sum_{e\in\partial S}(|f_e^+|+|f_e^-|)
 \ge \sum_{v\in S}(g_v^++g_v^-).}
\tag{C8}
\]
In particular, if \(\mu_p\ge\mu_0>0\),
\(|d_v^p|\ge a>0\), and \(q_v^p\le Q\) on \(S\) for both inputs, then
\[
 \sum_{e\in\partial S}(|f_e^+|+|f_e^-|)
 \ge \frac{4\mu_0a}{Q^2-a^2}|S|.
\tag{C9}
\]
If also \(|r_e|\le B\), this implies
\[
 \max_{p\in\{+,-\}}\|y_{\partial S}^p\|_\infty
 \ge \frac{2\mu_0a}{Q^2-a^2}
       \frac{|S|}{B|\partial S|}.
\tag{C10}
\]

**Proof.**  Switch each input using
\(R_p=\operatorname{Diag}(\operatorname{sgn}d_v^p)\).  Equation (C6)
becomes
\[
 B^Tz^p=R_ph+g^p,
 \qquad z_e^p=\operatorname{sgn}(d_{h(e)}^p)f_e^p.
\]
On \(S\), (C7) gives \(R_-h=-R_+h\).  Add the two equations and sum their
vertex coordinates over \(S\).  Each internal ordinary-incidence term
cancels, the common source cancels pointwise, and the triangle inequality on
the remaining boundary terms proves (C8).  The margin assumptions imply
\(g_v^p\ge2\mu_0a/(Q^2-a^2)\), proving (C9).  Finally, the left side of
(C9) is at most
\(2B|\partial S|\max_p\|y_{\partial S}^p\|_\infty\), which proves (C10).
\(\square\)

A fixed pair-asymmetric objective contributes such a common \(h\).  Public
pair-antisymmetric constraint coefficients do **not** suffice by themselves:
their multiplier contribution may differ between inputs.  They are covered
only when that resulting contribution is promised to be the same vector
\(h\), or when its difference is separately bounded.

## 4. Exact recovery of the parity-path law

For the constant-ratio central endpoint in
[2026-09-02-dual-homogeneity-bounded-full-kkt-lower-bound.md](2026-09-02-dual-homogeneity-bounded-full-kkt-lower-bound.md),

\[
                         q_v=\frac54,
                  \qquad |d_v|=1.
\tag{14}
\]

The exact demand in (4) is therefore

\[
                         g_v=\frac{32}{9}\mu.
\tag{15}
\]

Take \(S=\{j,j+1,\ldots,P-1\}\) on the path.  Its only boundary row is the
anchor row when \(j=0\), and the transition into node \(j\) otherwise.  Thus
(9) is an equality and gives

\[
              |\alpha_j|=\frac{32}{9}\mu(P-j),
 \qquad
              \alpha_j=\frac{32}{9}\mu\tau_j(P-j).
\tag{16}
\]

Summing over all path rows also gives

\[
 \|\alpha\|_2
 =\frac{32}{9}\mu
   \left(\sum_{\ell=1}^P\ell^2\right)^{1/2}
 =\Theta(\mu P^{3/2}).
\tag{17}
\]

At \(\mu=1/16\), (16) is
\(\alpha_j=(2/9)\tau_j(P-j)\).  Scaling to
\(\mu=1/(16P)\) makes every \(\alpha_j\) bounded and its total squared mass
\(\Theta(P)\), exactly as in the bounded full-KKT theorem.

## 5. Newton-direction cut conservation

The same conservation law holds at a pair-symmetric Newton start and does not
require the full step to land on a central point.  Write a general primal--dual
Newton system as

\[
 A\Delta x=r_p,\qquad
 A^T\Delta y+\Delta s=r_d,\qquad
 S^0\Delta x+X^0\Delta s=r_c.
\tag{18}
\]

Assume at every signed-copy vertex that

\[
 x_v^{0,+}=x_v^{0,-}=\xi_v>0,
 \qquad
 s_v^{0,+}=s_v^{0,-}=\zeta_v>0,
\tag{19}
\]

that \(r_{d,v}^+=r_{d,v}^-\) and
\(r_{c,v}^+=r_{c,v}^-\), and that all nongraph equality columns are
pair-symmetric.  Finally, suppose the graph rows of the primal Newton equation
are homogeneous away from terminal anchors, so

\[
          \Delta d_v=a_e\Delta d_u,
 \qquad \Delta d_v:=\Delta x_v^+-\Delta x_v^-.
\tag{20}
\]

This is exactly what happens at a public pair-symmetric start: its initial
difference is zero, and every nonanchor signed-copy equality has zero primal
residual.

### Theorem 5 (Newton sources obey the same cut law)

Suppose \(\Delta d_v\ne0\) on the component and put
\(\eta_v=\operatorname{sgn}(\Delta d_v)\).  There is an edge gauge
\(z_e=\eta_{h(e)}\Delta y_e\) such that

\[
 B^Tz=g^{\rm N},
 \qquad
 g_v^{\rm N}=\frac{\zeta_v}{2\xi_v}|\Delta d_v|>0.
\tag{21}
\]

Consequently, for every nonempty boundary \(\partial S\),

\[
\begin{aligned}
 \|\Delta y_{\partial S}\|_\infty
 &\ge \frac{\sum_{v\in S}g_v^{\rm N}}{|\partial S|},\\
 \|\Delta y_{\partial S}\|_2
 &\ge \frac{\sum_{v\in S}g_v^{\rm N}}{\sqrt{|\partial S|}}.
\end{aligned}
\tag{22}
\]

In particular, if \(\zeta_v/\xi_v\ge r>0\) and
\(|\Delta d_v|\ge a>0\) on \(S\), then

\[
 \|\Delta y_{\partial S}\|_\infty
 \ge\frac{ra}{2}\frac{|S|}{|\partial S|},
 \qquad
 \|\Delta y_{\partial S}\|_2
 \ge\frac{ra}{2}\frac{|S|}{\sqrt{|\partial S|}}.
\tag{23}
\]

**Proof.**  Subtract the two dual equations in (18).  Pair symmetry gives

\[
            2B_a^T\Delta y+\Delta s^+-\Delta s^-=0.
\]

Subtracting the two complementarity equations gives

\[
 \zeta_v\Delta d_v
 +\xi_v(\Delta s_v^+-\Delta s_v^-)=0.
\]

Elimination yields

\[
                 (B_a^T\Delta y)_v
                 =\frac{\zeta_v}{2\xi_v}\Delta d_v.
\tag{24}
\]

Equation (20) implies \(a_e=\eta_u\eta_v\).  Apply the switching identity
(8) with \(\eta\) in place of \(\tau\), and sum (21) over \(S\) exactly as
in (9).  This proves (21)--(23). \(\square\)

For the all-ones public start in the unit-height full-KKT path,
\(\xi_v=\zeta_v=1\) and \(\Delta d_v=\tau_v\).  A suffix of length \(L\)
has one boundary row, so Theorem 5 gives the exact recurrence

\[
                         \Delta y_{\partial S}
                         =\frac{L}{2}\tau_{\partial S}.
\tag{25}
\]

For the bounded secant start,
\(\xi_v=5/6\), \(\zeta_v=10/27\), and hence
\(\zeta_v/(2\xi_v)=2/9\).  The same calculation gives
\(\alpha_j=(2/9)\tau_j(P-j)\).  Scaling all dual data by \(\lambda\)
scales \(\zeta\), the Newton multiplier, and the source in (21) by
\(\lambda\), while leaving \(\Delta d\) unchanged.

Thus multiplier growth in public-start copy amplifiers is already forced by
the linearized Newton equations.  Exact landing on a feasible central point
is useful for identifying a particular direction, but is not the cause of
the accumulation.

### 5.1 A quadratic work identity beyond incidence graphs

There is a complementary formulation that does not require the
pair-antisymmetric rows to be an incidence matrix.  Let that entire block be
an arbitrary matrix \(C_\sigma\), let \(r_a\) be its primal Newton right-hand
side, and let \(\alpha\) be its multiplier correction.  Under the same
pair-symmetric start and right-hand-side assumptions as (19), subtracting the
pair equations exactly as above gives

\[
 C_\sigma\Delta d=r_a,
 \qquad
 C_\sigma^T\alpha=D\Delta d,
 \qquad
 D=\operatorname{Diag}\!\left(\frac{\zeta_v}{2\xi_v}\right).
\tag{W1}
\]

Taking inner products yields the exact Newton work identity

\[
 \boxed{\qquad
       r_a^T\alpha=\Delta d^TD\Delta d.
       \qquad}
\tag{W2}
\]

Consequently, if \(D\succeq\rho I\) and
\(|\Delta d_v|\ge a\) on \(L\) coordinates, then

\[
 \|\alpha\|_\infty
 \ge\frac{\rho a^2L}{\|r_a\|_1},
 \qquad
 \|\alpha\|_2
 \ge\frac{\rho a^2L}{\|r_a\|_2}.
\tag{W3}
\]
As in (C3), a zero denominator with nonzero \(\Delta d\) is an impossibility
statement.  Under an arbitrary invertible row change
\(C_\sigma'=UC_\sigma\), the corresponding quantities transform as
\[
 r_a'=Ur_a,\qquad \alpha'=U^{-T}\alpha,\qquad
 (r_a')^T\alpha'=r_a^T\alpha.
\tag{W4}
\]
Thus (W2), unlike a coordinate multiplier norm, is row-basis invariant.
Equations (W3) are the associated dual-norm product bounds in the chosen row
basis.

This proof uses neither acyclicity nor independence of the rows.  Thus adding
zero-right-hand-side redundant constraints, parallel copy rows, cycles, or a
bounded-degree branching network does not remove multiplier growth when the
antisymmetric Newton residual has bounded norm.

For the bounded secant start,

\[
 D=\frac29I,\qquad \Delta d_v=\tau_v,
 \qquad r_a=e_0.
\]

Equation (W2) gives the root multiplier \(\alpha_0=2P/9\) directly.  After
dual scaling by \(\lambda\), it gives
\(D=(2\lambda/9)I\), so bounded complete directions force
\(\lambda=O(1/P)\).  This proves the inverse-scale price in
`2026-09-02-dual-homogeneity-bounded-full-kkt-lower-bound.md` without a path
or backward-substitution assumption.

The assumptions identify the genuine escape routes.  A construction must
make the start ratio \(\zeta/\xi\) vanish, shrink the hard difference
amplitude, use an antisymmetric residual whose norm grows with the number of
copies, inject additional pair-antisymmetric objective or constraint sources,
or leave the signed-copy model.  The first option is precisely the known
\(1/P\) dual scale.  The second loses constant state mass unless another
amplification is introduced.  The remaining options require separate
local-input accounting; Section 6 supplies that accounting for canonical
one-bit-local signed-copy rows.

### 5.2 Public antisymmetric sources do not cure a small output cut

Pair symmetry is needed for the one-instance positive-demand theorem, but a
two-input comparison handles arbitrary **public** pair-antisymmetric objective
or Newton sources on a copy region.  Let \(S\) have boundary
\(\partial S\) in the common graph topology.  Use the same public start and
Newton right-hand sides on two instances, denoted \(+\) and \(-\).  Before
switching, elimination of the slack differences has the form

\[
             (B_{a^p}^Tf^p)_v=h_v+D_v\Delta d_v^p,
             \qquad p\in\{+,-\},
\tag{T1}
\]

where \(h\) is the same public pair-antisymmetric source in the original
variable coordinates, \(f_e^p=r_e\Delta y_e^p\), and \(D_v>0\) is common to
the two instances.  Equality of \(h\) as a numerical vector is the operative
assumption.  Merely making the coefficients of another antisymmetric
constraint public does not ensure it, because that constraint's multiplier
correction may depend on the input.  Suppose

\[
 \Delta d_v^+\ge a,\qquad \Delta d_v^-\le-a,\qquad
 D_v\ge\rho>0\qquad(v\in S).
\tag{T2}
\]

Let \(R_p=\operatorname{Diag}(\eta_v^p)\), where
\(\eta_v^p=\operatorname{sgn}(\Delta d_v^p)\), and switch each instance as in
Theorem 5.  On \(S\), (T2) gives \(R_-=-R_+\).  The two switched equations are

\[
 B^Tz^p=R_ph+D|\Delta d^p|.
\]

Add them and sum over \(S\).  The two gauged public sources cancel because
\(R_-h=-R_+h\) on \(S\), while every internal incidence contribution cancels
under the cut sum.  Only boundary forces remain, and therefore

\[
 \sum_{e\in\partial S}
       (|f_e^+|+|f_e^-|)
 \ge2\rho a|S|.
\tag{T3}
\]

If \(|r_e|\le B\), this implies

\[
 \boxed{
 \max_{p\in\{+,-\}}\|\Delta y_{\partial S}^p\|_\infty
 \ge\frac{\rho a|S|}{B|\partial S|}.}
\tag{T4}
\]

Thus a bounded-degree tree or branching copy network behind one parity seed
still has an \(\Omega(|S|)\) multiplier on at least one parity class, even if
public asymmetric objective terms are added to cancel the flow on the other
class.  Escaping this comparison requires \(\Omega(|S|)\) independent
boundary channels, an input-dependent antisymmetric source, a growing row
scale, or a vanishing start ratio/output margin.

## 6. Input-incidence frontier for parity copy amplifiers

Consider a family on one fixed graph topology indexed by
\(\sigma\in\{\pm1\}^N\).  Every signed edge label is either public or depends
on at most one input bit.  Terminal values and labels, nongraph
data, terminal Newton residuals, and nonzero row scales \(r_e\) are public and
fixed.  The nongraph objective, constraint, and Newton data obey the
pair-symmetry hypotheses of Theorems 1 and 5.  Put
\(B_{\rm row}:=\max_e|r_e|\).  Let
\(M_j\) be the number of signed graph rows whose edge label changes when only
\(\sigma_j\) is flipped, and put

\[
                       M_{\rm dep}=\sum_{j=1}^NM_j.
\tag{26}
\]

Under one-bit locality, each nonpublic signed row is counted for exactly one
bit.  If instead \(M_j\) counts raw LP constraint-matrix positions, the pair
expansion of one internal edge sign contains two such positions, so
\(|\partial S_j|\le M_j\); all lower bounds below remain valid with that
larger count.  An explicitly stored KKT matrix may duplicate those positions
in its transpose block.  Counting every such copy only increases \(M_j\) and
therefore preserves the inequalities.

Fix a base input \(\sigma\) and let \(\sigma^{(j)}\) flip only bit \(j\).
Assume that the base instance and every single-flip instance have feasible
exact central points on the same component, with nonzero \(d_v\) throughout.
Let \(\mu\) denote the complementarity of the base central point.  Define

\[
 S_j=\{v:\tau_v(\sigma^{(j)})=-\tau_v(\sigma)\}.
\tag{27}
\]

For an internal edge \(e=(u,v)\), feasibility gives

\[
 \frac{a_e(\sigma^{(j)})}{a_e(\sigma)}
 =\frac{\tau_u(\sigma^{(j)})\tau_v(\sigma^{(j)})}
        {\tau_u(\sigma)\tau_v(\sigma)}.
\tag{28}
\]

The right side is negative exactly when one endpoint is in \(S_j\).  Public
terminal signs play the role of a fixed outside vertex.  Therefore

\[
                         |\partial S_j|=M_j
\tag{29}
\]

when rows are counted, and \(|\partial S_j|\le M_j\) when coefficient
positions are counted.

Assume there is a fixed output set \(O\) of \(K\) vertices whose orientation
flips whenever any one input bit is flipped.  Thus \(O\subseteq S_j\) for
every \(j\).  Suppose the base central point obeys
\(|d_v|\ge a\), \(q_v\le Q\) on \(O\), and put
\(Y=\|y(\sigma)\|_\infty\).  Theorem 1 and Corollary 2 applied to \(S_j\)
give

\[
        M_jB_{\rm row}Y\ge\frac{2\mu a}{Q^2-a^2}K.
\tag{30}
\]

Summing over every input bit proves the resource frontier

\[
\boxed{
       M_{\rm dep}B_{\rm row}Y
       \ge\frac{2\mu a}{Q^2-a^2}KN.}
\tag{31}
\]

The same proof applies to Newton directions provided the base and every
single-flip system satisfy the hypotheses of Theorem 5, with nonzero
\(\Delta d_v\) throughout.  Define \(S_j\) using
\(\eta_v=\operatorname{sgn}(\Delta d_v)\) for the two inputs.  Assume every
output direction flips and the base direction obeys
\(|\Delta d_v|\ge a\) on \(O\).  For its pair-symmetric start, put

\[
             \rho:=\min_{v\in O}\frac{s_v^0}{2x_v^0}>0.
\tag{32}
\]

Theorem 5 and Corollary 2 then give

\[
\boxed{
       M_{\rm dep}B_{\rm row}\|\Delta y(\sigma)\|_\infty
       \ge \rho aKN.}
\tag{33}
\]

These statements use only the multiplier vector for the single fixed base
input; its different flip sets impose \(N\) simultaneous cut-capacity
requirements.  Uniform bounds over the family are therefore more than
sufficient.

If \(M_{\rm dep}=O(N)\), \(K=\Omega(N)\), \(B_{\rm row}=O(1)\), and
\(a,Q\) are constants, (31)
says that constant central multipliers require \(\mu=O(1/N)\).  Under the
same size assumptions, (33) says that constant Newton multipliers require
\(\rho=O(1/N)\).  At the unscaled bounded secant start,
\(\rho=2/9\), so \(\|\Delta y\|_\infty=\Omega(N)\).  Scaling all dual data by
\(\lambda=1/P=\Theta(1/N)\) changes this to
\(\rho=2\lambda/9=\Theta(1/N)\), exactly matching the bounded full-direction
construction.

The frontier assumes that every output orientation changes under every input
flip, as it does when the output stores parity.  Other Boolean output
functions give a bound summed only over sensitive input bits.

### 6.1 Diagonal row scaling pays coefficient magnitude

Replace an edge row by

\[
                       r_e(d_v-a_ed_u)=0,
 \qquad 0<|r_e|\le B.
\tag{34}
\]

The quantity that enters pair stationarity is not the coordinate multiplier
itself but the row force

\[
                              f_e=r_ey_e
 \quad\text{or}\quad
                              \Delta f_e=r_e\Delta y_e.
\tag{35}
\]

After this substitution, every switching and cut identity above is unchanged.
On a boundary with at most \(M_j\) rows,

\[
 \sum_{e\in\partial S_j}|f_e|
 \le B M_j\|y\|_\infty,
 \qquad
 \sum_{e\in\partial S_j}|\Delta f_e|
 \le B M_j\|\Delta y\|_\infty.
\tag{36}
\]

Therefore (31) and (33) strengthen to

\[
 \boxed{
 M_{\rm dep}B\|y\|_\infty
 \ge\frac{2\mu a}{Q^2-a^2}KN,
 \qquad
 M_{\rm dep}B\|\Delta y\|_\infty
 \ge\rho aKN.}
\tag{37}
\]

Thus a linear-incidence parity amplifier with constant local primal/slack
scale cannot make every complete-direction coordinate bounded using bounded
row rescaling.  Quantitatively, when
\(M_{\rm dep}=\Theta(N)\) and \(K=\Theta(N)\), it must satisfy
\[
                  B\|\Delta y\|_\infty=\Omega(\rho N).
\]
Thus constant \(\rho\) and bounded \(B\) force
\(\|\Delta y\|_\infty=\Omega(N)\), while constant \(\rho\) and bounded
\(\|\Delta y\|_\infty\) force \(B=\Omega(N)\).  Intermediate tradeoffs,
such as both factors growing as \(\sqrt N\), are also possible.  Keeping both
factors bounded instead requires \(\rho=O(1/N)\), exactly the inverse dual
scale in the bounded full-KKT construction.

More explicitly, take \(P=\Theta(N)\), \(K=\Theta(P)\),
\(M_{\rm dep}=O(P)\), \(B=O(1)\), and assume both the public primal start and
public slack start are bounded above and below by positive constants.  Then
\(\rho=\Theta(1)\).  If the output difference direction has constant margin
\(a=\Theta(1)\), (37) forces

\[
                         \|\Delta y\|_\infty=\Omega(P).
\tag{38}
\]

Hence no LP in this signed-copy class simultaneously has linear input
incidence, bounded coefficient magnitude, constant primal/slack scale, a
constant output margin on a linear parity plateau, and a coordinatewise
bounded complete Newton direction.  Branching, redundant copy rows, and
bounded diagonal row scaling are already included in this conclusion.

The force statement also permits input-dependent \(r_e\), with two changes
to the accounting.  Define \(M_j\) to count every graph row whose label or
scale changes under the \(j\)-th flip (or count all changed coefficient
positions), and let \(B\) be the worst-case scale magnitude over all inputs.
Every edge in \(\partial S_j\) must still have a changed label, so
\(|\partial S_j|\le M_j\), and the proof of (37) is unchanged.  The row must
remain nonzero.  A sign hidden in \(r_e\) is handled directly by the signed
force \(f_e=r_ey_e\); it does not alter the feasible copy relation and cannot
remove (37).  A scale depending on many bits must be charged once for every
sensitive coefficient--bit incidence.  This is combinatorial incidence
accounting, not by itself a quantum query lower bound: a nonlocal coefficient
oracle may reveal a global predicate in one call.  Arbitrary sparse row
mixing is not a diagonal rescaling and is outside this corollary; it may
introduce new pair-antisymmetric sources or nonlocal coefficient dependencies
that require their own access accounting.

## 7. Fourier obstruction to local direct cancellation

The pair-symmetry hypotheses can be weakened for a worst-case theorem.
Suppose prescribed antisymmetric data adds a direct source
\(h_v(\sigma)\) to central stationarity.  In the weighted-row notation of
Section 6.1, this means

\[
 (B_a^Tf)_v
 =\frac{2\mu d_v}{q_v^2-d_v^2}+h_v(\sigma),
 \qquad f_e=r_ey_e.
\tag{F1}
\]

For example, if all other rows are pair-symmetric, an asymmetric objective
contributes \(h_v=(c_v^+-c_v^-)/2\).  After switching by
\(\eta_v=\operatorname{sgn}(d_v)\), the ordinary divergence is

\[
 (B^Tz)_v
 =g_v+\eta_v(\sigma)h_v(\sigma),
 \qquad
 g_v=\frac{2\mu|d_v|}{q_v^2-d_v^2}>0.
\tag{F2}
\]

Let \(O\) be one fixed output region of \(K\) vertices, with the same graph
boundary \(\partial O\) for every input, and compare central points at one
common complementarity \(\mu\).  Assume

\[
 \eta_v(\sigma)=\kappa_v\chi_{[N]}(\sigma),
 \qquad \kappa_v\in\{\pm1\},
 \qquad \chi_{[N]}(\sigma)=\prod_{j=1}^N\sigma_j
\tag{F3}
\]

on \(O\).  Use the uniform Fourier convention

\[
 \widehat h_v([N])
 =2^{-N}\sum_\sigma\chi_{[N]}(\sigma)h_v(\sigma).
\tag{F4}
\]
All hypotheses in this section are imposed on the full input cube
\(\{\pm1\}^N\), not merely on one base input and its single-bit neighbors;
otherwise the average in (F4) is unavailable.
The directed topology and vertex set \(O\) are fixed.  Input-dependent edge
signs and nonzero diagonal row scales are allowed as elsewhere in this note,
because switching produces one common ordinary incidence matrix and the
physical force absorbs the row scale.  A relative edge gain of magnitude
different from one is not a diagonal row scale: internal terms then need not
cancel under the fixed cut sum.  Such gains require a separate,
input-independent positive gauge, or lie outside Theorem 6.

### Theorem 6 (local direct sources cannot cancel every parity instance)

Suppose \(|d_v|\ge a\), \(q_v\le Q\) on \(O\) for every input, and define

\[
                 \varepsilon_O
 =\frac1K\sum_{v\in O}|\widehat h_v([N])|.
\tag{F5}
\]

There exists an input \(\sigma^*\) for which the physical boundary force
satisfies

\[
 \sum_{e\in\partial O}|r_ey_e(\sigma^*)|
 \ge K\left(\frac{2\mu a}{Q^2-a^2}-\varepsilon_O\right).
\tag{F6}
\]

The bound is informative when the parenthesis is positive.  In particular,
if every \(h_v\) has zero full-parity Fourier coefficient, then

\[
 B_{\rm row}|\partial O|\,
 \|y(\sigma^*)\|_\infty
 \ge\frac{2\mu a}{Q^2-a^2}K.
\tag{F7}
\]

**Proof.**  Put

\[
 H(\sigma)=\sum_{v\in O}\eta_v(\sigma)h_v(\sigma).
\]

Equations (F3)--(F4) give

\[
 \mathbb E_\sigma H(\sigma)
 =\sum_{v\in O}\kappa_v\widehat h_v([N])
 \ge-K\varepsilon_O.
\tag{F8}
\]

Some \(\sigma^*\) has \(H(\sigma^*)\) at least its average.  The positive
central demand on \(O\) is at least
\(2\mu aK/(Q^2-a^2)\).  Summing (F2) over \(O\), cancelling internal edges,
and applying the triangle inequality proves (F6).  Equation (F7) follows from
\(|r_e|\le B_{\rm row}\). \(\square\)

There is an exact Newton analogue.  Retain the homogeneous primal signed-copy
equations (20) for every input, so that switching by
\(\operatorname{sgn}(\Delta d)\) remains valid.  At the pair-symmetric start
(19), whose positive scales \(\xi_v(\sigma),\zeta_v(\sigma)\) may vary with
the input, allow the two Newton right-hand sides to be asymmetric and set

\[
 h_v^{\rm N}(\sigma)
 =\frac{r_{d,v}^+-r_{d,v}^-}{2}
  -\frac{r_{c,v}^+-r_{c,v}^-}{2\xi_v(\sigma)}.
\tag{F9}
\]

The subtraction used in (24) now gives

\[
 (B_a^T\Delta f)_v
 =\frac{\zeta_v(\sigma)}{2\xi_v(\sigma)}\Delta d_v
  +h_v^{\rm N}(\sigma),
 \qquad \Delta f_e=r_e\Delta y_e.
\tag{F10}
\]

Assume on the fixed output region that
\(\operatorname{sgn}(\Delta d_v)=\kappa_v\chi_{[N]}\),
\(|\Delta d_v|\ge a\), and
\(\zeta_v(\sigma)/(2\xi_v(\sigma))\ge\rho\).  Define

\[
 \varepsilon_O^{\rm N}
 =\frac1K\sum_{v\in O}|\widehat h_v^{\rm N}([N])|.
\]

The same averaging proof gives an input \(\sigma^*\) such that

\[
 \sum_{e\in\partial O}|r_e\Delta y_e(\sigma^*)|
 \ge K(\rho a-\varepsilon_O^{\rm N}).
\tag{F11}
\]

If all full-parity coefficients vanish, then

\[
 B_{\rm row}|\partial O|\,
 \|\Delta y(\sigma^*)\|_\infty
 \ge\rho aK.
\tag{F12}
\]

A function depending on a strict subset of the \(N\) input bits has zero
full-parity Fourier coefficient.  So does every function of Fourier degree
less than \(N\).  Therefore a direct objective coefficient or a direct Newton
right-hand-side entry that is a bounded-bit junta cannot cancel the positive
parity-oriented demand on every input.  This is the coefficient-locality
interpretation of Theorem 6.  For the Newton interpretation, the start
coordinates \(\xi_v\) and the raw right-hand-side data must themselves be
public/input-independent, or the zero-full-parity property of the combined
source \(h_v^{\rm N}\) must be checked directly.

The normalization qualification is substantive.  Even constant raw Newton
right-hand-side differences can acquire full parity through (F9): if
\(1/\xi_v(\sigma)=A+B\chi_{[N]}(\sigma)\), where \(A>|B|>0\), and
\(r_{d,v}^+-r_{d,v}^-=A(r_{c,v}^+-r_{c,v}^-)\) is constant, then
\(h_v^{\rm N}\) is a pure full-parity term.  By contrast, the positive factor
\(\zeta_v/(2\xi_v)\) in (F10) may vary arbitrarily with the input without
affecting the proof, provided its stated uniform lower bound \(\rho\) holds.

The Fourier boundary is tight.  If \(g_v=g_0\) is constant, the direct source
\[
 h_v(\sigma)=-\kappa_v\chi_{[N]}(\sigma)g_0
\]
makes \(g_v+\eta_vh_v=0\) identically on \(O\).  Its full-parity coefficient
is \(-\kappa_vg_0\), exactly the component excluded by (F7).

The word **direct** is essential.  An additional pair-antisymmetric constraint
contributes its coefficient times an unknown equality multiplier.  That
multiplier can depend on all input bits even if the row coefficients are
one-bit-local, so the resulting effective \(h_v\) need not have zero
full-parity coefficient.  Likewise, input-dependent preprocessing or a
recovery oracle may explicitly manufacture a parity source.  The theorem
applies to prescribed objective/RHS data, or to any broader source for which
the Fourier condition is separately proved; it does not infer the condition
for multiplier-mediated sources.

The use of one fixed \(O\) is also essential to the simple averaging proof.
If the output cut itself depends on \(\sigma\), its indicator can carry full
parity and invalidate (F8).  The parity plateaus above have a fixed topology
and satisfy this requirement.

## 8. Repeated incidences and what the theorem does not prove

The cut counts equality rows, not distinct hidden input bits.  Parallel rows
or many boundary edges carrying the same hidden sign increase
\(|\partial S|\) and can divide the required flow among more multipliers.
This is a real escape from the multiplier bound, not a flaw in (12).  It has
three consequences for oracle lower-bound constructions:

1. A bounded-degree graph cannot give a large region many boundary channels
   without spending proportionally many vertices or external incidences.
2. Reusing one input bit on many coefficient entries may keep Boolean query
   complexity small while increasing LP size.  Any size-versus-query theorem
   must separately bound the number of coefficient locations controlled by
   one bit.
3. An edge sign equal to a long prefix product makes the graph description
   locally convenient but moves the hard computation into coefficient-oracle
   preparation.  Such a global-sign oracle cannot be supplied for free in a
   raw input-query reduction.
4. Replacing the plateau path by a bounded-degree fanout tree does not help:
   the whole descendant region is separated from its parity seed by only
   constantly many rows, so Theorem 5 still forces linear flow at that cut.
5. Giving the region \(K\) independent boundary channels can keep individual
   forces bounded, but a one-bit-local parity construction must then carry
   every sensitive input across those channels.  Section 6 charges the
   resulting \(M_{\rm dep}=\Omega(KN)\) incidences.  Duplicating \(K\) full
   parity chains is the simplest example; its raw parity lower bound is only
   \(\Omega(N)\), not \(\Omega(P)\), when \(P=\Omega(KN)\).
6. Public antisymmetric sources can cancel the demand for one parity
   orientation, but Section 5.2 shows that they cannot cancel both sides of a
   small output cut.  Input-dependent antisymmetric sources are a genuine
   escape only if their coefficient-loading cost is omitted.

The conservation theorem itself is algebraic.  It is not, without those
additional locality assumptions, a quantum query lower bound.  Multiplier
coordinates alone do not survive row scaling: multiplying one equality row
by \(r_e\) divides its multiplier by \(r_e\).  Section 6.1 shows that the
row force \(r_ey_e\) is invariant and that a bound on coefficient magnitude
restores a multiplier lower bound.  Arbitrary changes of row basis remain
outside the theorem.

## 9. Novelty calibration

The following ingredients are **not** novelty claims.

- The balance criterion and switching a balanced signed graph to an
  all-positive graph go back at least to Harary,
  [*On the notion of balance of a signed graph*](https://doi.org/10.1307/mmj/1028989917).
  Zaslavsky's
  [*Matrices in the Theory of Signed Simple Graphs*](https://arxiv.org/abs/1303.3083)
  is a modern source for signed incidence matrices and switching.
- Once the graph has been switched, summing \(B^Tz=g\) over a vertex set to
  obtain net cut flux equal to total demand is the standard incidence-flow
  conservation identity.  The ensuing \(\ell_\infty\), \(\ell_2\), and
  volume-to-boundary inequalities are immediate norm bounds.
- Replacing a constraint by \(r_e\) times that constraint changes its
  multiplier inversely.  Thus \(r_ey_e\) is the invariant contribution to
  stationarity.  Corollary 2 records this standard multiplier covariance in
  the notation needed here; “physical force” is only a descriptive name.
- The usual KKT and primal--dual Newton systems already identify multipliers
  with constraint-normal forces and reduce Newton equations to Schur
  complements; see Chapters 10--11 of Boyd--Vandenberghe,
  [*Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf).
  Equation (C2) is the resulting virtual-work pairing after choosing the
  pair-antisymmetric displacement and inserting \(x_i s_i=\mu\).  It is not
  the ordinary total primal--dual gap \(x^Ts=n\mu\), although it is derived
  from the same KKT equations.  Equivalently, its right side is
  \(\mu d^T\nabla_d[-\sum_v\log(q_v^2-d_v^2)]\), the radial derivative of
  the paired logarithmic barrier at fixed \(q\).  Equation (W2) is the
  standard quadratic energy identity for the condensed system
  \(C_\sigma D^{-1}C_\sigma^T\).  The invariance of
  \(b_a^Ty_a\) under
  \((C,b_a,y_a)\mapsto(UC,Ub_a,U^{-T}y_a)\), and of
  \(r_a^T\alpha\) under
  \((C_\sigma,r_a,\alpha)\mapsto
  (UC_\sigma,Ur_a,U^{-T}\alpha)\), is elementary dual-pairing covariance.
  None of these facts alone is a novelty claim.

Electrical-flow interpretations of graph-optimization Newton systems are
also established.  Mądry's
[*Navigating Central Path with Electrical Flows*](https://arxiv.org/abs/1307.2205)
uses electrical flows to navigate an interior-point central path for flow and
matching problems.  It does not give a lower bound on equality multipliers
from a signed-copy cut.

There is also established IPM literature on multiplier growth.  In
particular, Haeser--Hinder--Ye,
[*On the behavior of Lagrange multipliers in convex and non-convex infeasible
interior point methods*](https://arxiv.org/abs/1707.07327),
prove general asymptotic boundedness or divergence results depending on the
relative rates at which primal infeasibility and complementarity are reduced.
That work is an important conceptual precedent for a residual--multiplier
tradeoff.  It does not give the finite-instance signed-copy formula (C2), the
quadratic Newton identity (W2) as a gadget obstruction, a cut-local
volume-to-boundary estimate, or the coefficient-incidence product of
Section 6.

The nearest quantum LP lower bounds found in the targeted search are
Apers--Gribling,
[*Quantum speedups for linear programming via interior point methods*](https://arxiv.org/abs/2311.03215),
Section 8, especially Theorems 8.1 and 8.4.  They prove row-query lower
bounds for spectral approximation and for recovering an LP optimum value.
They do not study the
size of central-point or Newton equality multipliers, diagonal row scaling,
or simultaneous cut demands imposed by different input-bit flips.  Earlier
QLS-based QIPMs such as Kerenidis--Prakash,
[*A Quantum Interior Point Method for LPs and SDPs*](https://arxiv.org/abs/1808.09266),
and Mohammadisiahroudi--Fakhimi--Terlaky,
[*Efficient use of quantum linear system algorithms in inexact infeasible
IPMs for linear optimization*](https://arxiv.org/abs/2307.14445),
are algorithmic upper-bound analyses.  The 2026 benchmarking lower bounds of
Binkowski,
[*Practical lower bounds for hybrid quantum interior point methods in linear
programming*](https://arxiv.org/abs/2604.24362),
lower-bound estimated runtime for specified hybrid pipelines on benchmark
instances, rather than proving an oracle lower bound or a multiplier
conservation theorem.

A targeted open-literature search through 2 September 2026 found no exact
precedent for the **conjunction** in Section 6: every sensitive bit defines a
flip cut containing a common \(K\)-vertex output region; the multiplier for
one fixed base instance must satisfy all \(N\) cut demands; and summing the
separate coefficient incidences yields
\[
 M_{\rm dep}B_{\rm row}\|y\|_\infty
 =\Omega(\mu KN),\qquad
 M_{\rm dep}B_{\rm row}\|\Delta y\|_\infty
 =\Omega(\rho KN)
\]
under the stated margin and locality hypotheses.  The paired KKT subtraction
that produces \(2\mu|d|/(q^2-d^2)\), and its Newton counterpart, are short
algebraic observations.  The graph-free consequences (C3) and (W3) are also
direct Hölder bounds on standard work/energy pairings.  The defensible
candidate contribution is the use of these identities as a no-go criterion
for signed-copy amplifiers, and especially their conjunction with the
many-neighbor incidence accounting to obtain the Section 6 gadget-design
frontier.  The search found no source making that cross-instance use, but
absence from a targeted search is evidence, not proof of priority, so the
claim should remain “apparently new” rather than “the first.”

The search also found no use of full-parity Fourier orthogonality to show that
bounded-bit direct objective or Newton sources cannot cancel a switched
positive-demand cut on every input.  The Fourier averaging step itself is
elementary.  The candidate contribution in Theorem 6 is its conjunction with
the central/Newton cut conservation law, including the explicit separation
between direct prescribed sources and multiplier-mediated sources.
