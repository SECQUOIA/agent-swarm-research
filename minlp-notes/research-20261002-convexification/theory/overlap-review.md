# Why exact block hulls need separator consistency

Exact hulls of two-variable quadratic graphs do not, in general, give the
exact joint hull when their first and second moments are identified. This
failure occurs on the three-variable path `x -- y -- z`, with all variables
in the same box `[0,1]`. It therefore cannot be ruled out by a tree interaction
graph or by including every quadratic moment inside each block.

The statements below concern exact convex hulls, independently of numerical
separation error. The examples use rational coefficients and admit short
algebraic certificates.

**A graph-only obstruction.** Write

\[
H_{xy}=\operatorname{conv}\{(x,y,x^2,xy,y^2):x,y\in[0,1]\},
\]

and define \(H_{yz}\) analogously. Let \(R\) identify the shared coordinates
\(\mathbb E[y]\) and \(\mathbb E[y^2]\) between these two hulls. Let

\[
H=\operatorname{conv}\{(x,y,z,x^2,y^2,z^2,xy,yz):x,y,z\in[0,1]\}.
\]

Then \(H\subsetneq R\). One point in the difference has coordinates

\[
\begin{array}{c|cccccccc}
 &x&y&z&x^2&y^2&z^2&xy&yz\\\hline
 \bar v&1/2&1/2&4/5&1/2&5/16&4/5&3/8&1/2.
\end{array}
\]

To verify membership in \(R\), use the following representing measures:

- In the left block, put probability \(1/2\) at each of
  \((x,y)=(0,1/4),(1,3/4)\).
- In the right block, put probability \(1/5\) at \((y,z)=(0,0)\) and
  probability \(4/5\) at \((y,z)=(5/8,1)\).

Both have \(\mathbb E[y]=1/2\) and \(\mathbb E[y^2]=5/16\).

No global measure represents \(\bar v\). Its coordinates would force
\(\mathbb E[x(1-x)]=\mathbb E[z(1-z)]=0\), so \(x,z\) would be binary
almost surely. They also force

\[
\mathbb E[(y-1/4-x/2)^2]
=\mathbb E[(y-5z/8)^2]=0.
\]

The first equality requires \(y\in\{1/4,3/4\}\) almost surely; the second
requires \(y\in\{0,5/8\}\). These sets are disjoint.

These affine relations are consequences of the proposed *moment point*;
they are not constraints imposed on the original box. No interval propagation
argument about affine model rows is involved in this example.

**An explicit missing cut and an exact relaxation gap.** On the unit cube,
define

\[
D(x,y,z)=(y-1/4-x/2)^2+(y-5z/8)^2+x(1-x)+z(1-z).
\]

The following inequality is valid and sharp:

\[
D(x,y,z)\ge 1/128.
\tag{1}
\]

For fixed \(y\), the coefficients of \(x^2\) and \(z^2\) in \(D\) are
\(-3/4\) and \(-39/64\), respectively. The minimum over \(x,z\in[0,1]\)
therefore occurs at binary \(x,z\). At those endpoints the last two terms
vanish. For fixed binary \(x,z\), set
\(a=1/4+x/2\), \(b=5z/8\). Then

\[
(y-a)^2+(y-b)^2
=2\left(y-\frac{a+b}{2}\right)^2+\frac{(a-b)^2}{2}.
\]

The midpoint lies in \([0,1]\), and the smallest possible \(|a-b|\) is
\(1/8\), attained at \(x=z=1\). Thus the minimum is \(1/128\), attained
at \((x,y,z)=(1,11/16,1)\).

After expanding, (1) is a linear inequality in the sparse quadratic lift:

\[
2s_y-\tfrac12m_y-c_{xy}-\tfrac54c_{yz}
+\tfrac54m_x-\tfrac34s_x+m_z-\tfrac{39}{64}s_z
\ge-\tfrac7{128},
\tag{2}
\]

where \(m_u,s_u,c_{uv}\) denote the lifted coordinates for \(u,u^2,uv\).
At \(\bar v\), the lifted value of \(D\) is zero, so (2) is violated by
\(1/128\). No \(xz\) coordinate is needed for this cut.

This also gives an optimization example with an exact gap. Decompose

\[
D=\underbrace{(y-1/4-x/2)^2+x(1-x)}_{D_L(x,y)}
+\underbrace{(y-5z/8)^2+z(1-z)}_{D_R(y,z)}.
\]

Each summand is nonnegative on its block. Consequently minimizing the lifted
objective over \(R\) has value zero, attained at \(\bar v\); minimizing
over the original box has value \(1/128\). Multiplying the objective by a
positive constant scales the gap, so its size in these units is not a bound
on the possible effect of missing separator consistency.

The leaf-square coordinates are not essential. Replacing the two penalties
by \((1/4)x(1-x)\) and \((25/64)z(1-z)\) gives

\[
\widetilde D=2y^2-\tfrac12y-xy-\tfrac54yz
+\tfrac1{16}+\tfrac12x+\tfrac{25}{64}z\ge1/128.
\tag{3}
\]

For fixed \(y\), this polynomial is affine in \(x,z\), so the same endpoint
calculation proves sharpness. The local witness still has objective value
zero. Thus one shared square \(y^2\), together with the two bilinear edge
coordinates, already suffices for this failure of exact gluing.

More generally, let \(a,a+b,c,c+d\in[\ell,u]\), let
\(\delta=\min\{|s-t|:s\in\{a,a+b\},t\in\{c,c+d\}\}\), and take
\(x,z\in[0,1]\), \(y\in[\ell,u]\). Then the quadratic inequality

\[
(y-a-bx)^2+(y-c-dz)^2+b^2x(1-x)+d^2z(1-z)
\ge\delta^2/2
\tag{4}
\]

is valid and sharp. The left side is affine in each leaf variable. Its
minimum therefore occurs at binary leaves; minimizing over \(y\) places
it at the midpoint of a closest pair of endpoints and gives the stated
value. This elementary family gives a cut with a four-case validity check.
Automatic choices of \(a,b,c,d\) and the cost of detecting useful members
remain implementation questions; no novelty or general computational
advantage is claimed for this family here.

**A constrained example that survives separate block interval propagation.**
For a complementary example, define the exact block domains

\[
\begin{aligned}
S_L&=\{(x,y)\in[0,1]^2:x^2=x,\ y^2-y+(3/16)x=0\},\\
S_R&=\{(y,z)\in[0,1]^2:z^2=z,\ y^2-y+(2/9)z=0\}.
\end{aligned}
\]

The left domain consists of
\((0,0),(1,1/4),(1,3/4),(0,1)\). The right domain consists of
\((0,0),(1/3,1),(2/3,1),(1,0)\), with coordinates ordered as \((y,z)\).
Every coordinate projection has interval hull \([0,1]\), so tightening
scalar intervals using either complete block domain leaves all bounds
unchanged, even after repeated passes.

The common feasible set on \((x,y,z)\) consists of
\((0,0,0)\) and \((0,1,0)\): the only shared feasible values of \(y\)
are zero and one. In particular, its convex hull satisfies \(x=z=0\).

Nevertheless, the full quadratic graph hulls of \(S_L,S_R\) contain a common
moment point with

\[
\mathbb E[y]=1/2,\qquad \mathbb E[y^2]=3/8,\qquad
\mathbb E[x]=2/3,\qquad \mathbb E[z]=9/16.
\]

For the left measure, give its two endpoints probability \(1/6\) each and
its two interior points probability \(1/3\) each. For the right measure,
give its two endpoints probability \(7/32\) each and its two interior
points probability \(9/32\) each. The remaining moments are

\[
\mathbb E[x^2]=2/3,\quad \mathbb E[xy]=1/3,\quad
\mathbb E[z^2]=9/16,\quad \mathbb E[yz]=9/32.
\]

The two separator distributions even agree on the cubic moment
\(\mathbb E[y^3]=5/16\), but their fourth moments are \(35/128\) and
\(5/18\).

The qualification about *separate block interval propagation* matters.
Presolve that combines both rows obtains \((3/16)x=(2/9)z\) and can use
the binary equations to deduce \(x=z=0\). The example does not claim to
defeat arbitrary global presolve or branching.

**One extra separator statistic closes the constrained example.** Put
\(q(y)=y(1-y)\). In the left domain \(q\in\{0,3/16\}\), and in the
right domain \(q\in\{0,2/9\}\). Thus their respective exact hulls satisfy

\[
\mathbb E[q^2]=(3/16)\mathbb E[q],\qquad
\mathbb E[q^2]=(2/9)\mathbb E[q].
\]

The quadratic separator moments already identify \(\mathbb E[q]\).
If an extended formulation also identifies \(\mathbb E[q^2]\), the two
equalities force \(\mathbb E[q]=0\). Since \(q\ge0\) on \([0,1]\),
both measures must then concentrate on \(y\in\{0,1\}\), and their local
rows force \(x=z=0\). Matching \(\mathbb E[y]\) now matches the entire
separator distribution. The resulting projected hull is exact.

This suggests enriching a separator with a function that distinguishes
incompatible local distributions. It does not establish an automatic rule
for finding that function or a general runtime advantage. Adding the shared
variable alone is also insufficient: each block must enforce a valid
relationship between that variable and its original graph.

**What makes tree gluing exact.** Suppose blocks form a finite tree and satisfy the
running-intersection property: the blocks containing any particular variable
form a connected subtree. Let each block hull point have a representing
probability measure on that block's compact feasible domain. If the measures
agree on the *entire marginal distribution* on every shared separator, they
have a global representing measure supported on all the block domains.

To see this, root the tree. Retain the root measure. For each child, condition
its measure on its separator with its parent, and attach the remaining child
variables using that conditional distribution. Equal separator marginals
ensure that the resulting distribution has the correct child marginal.
The running-intersection property ensures that variables newly attached at
that step do not conflict with variables elsewhere in the existing tree.
Induction constructs the joint measure. Conditional probability kernels
exist here because compact Euclidean domains with their Borel sets are
standard Borel spaces. For finitely supported measures the construction is
just conditional probability and finite summation.

Agreement of finitely many moments implies this hypothesis only when those
moments determine the relevant separator distribution. Examples include:

- A binary separator with a shared mean: its probability of one is its mean.
- A scalar separator known to lie in a common finite set of \(k\) distinct
  points, with shared moments of orders zero through \(k-1\). The Vandermonde
  system uniquely determines all \(k\) atom probabilities.
- A finite vector separator when the blocks explicitly share its full table
  of atom probabilities.

Coordinate means do not generally determine a multi-variable binary
separator's joint distribution. Likewise, a continuous scalar separator's
first and second moments do not determine its distribution, as the examples
show.

The graph-only obstruction does not contradict the exactness of McCormick
inequalities for a *pure bilinear* graph on a forest. In that setting there
are no squared-variable graph coordinates, and the variable box here is
\([0,1]^n\). For an edge with means
\(m_i,m_j\) and product coordinate \(w_{ij}\), its McCormick inequalities
are precisely the nonnegativity conditions for binary pair probabilities

\[
p_{11}=w_{ij},\quad p_{10}=m_i-w_{ij},\quad
p_{01}=m_j-w_{ij},\quad p_{00}=1-m_i-m_j+w_{ij}.
\]

Adjacent edge measures have the same binary marginal at their shared
vertex, determined by that vertex's mean. Gluing these measures on the
forest gives a global measure with all required edge products. This proves
exactness in this special case. Prescribed squared-variable coordinates
can prevent the choice of binary marginals, which is why the argument does
not apply to the quadratic graph hull above.

**Implication for the small-block program.** Exact local convexification is
a valid strengthening, but tree structure and pairwise moment agreement do
not justify an exact global-hull claim. An implementation can retain small
blocks, add selected cuts involving several adjacent blocks, or enrich
separator statistics. Each choice needs its own separation-cost and solver
benefit evidence. Inequality (2) is a concrete regression case for detecting
the missing strength of quadratic pair hulls.

**Targeted verification.** A standalone Python calculation using
`python -` with a `fractions.Fraction` checker supplied on standard input
checked every displayed witness moment, the four binary
endpoint cases in (1), the attained minimum \(1/128\), and the violation of
the expanded lifted cut. The command returned exit status zero and printed
`Exact Fraction checks passed: both hull witnesses, separator moments through degree four, and sharp cut gap 1/128.`
A second `python -` exact arithmetic check verified the reduced certificate
(3), its attained minimum, and its value at the local witness; it returned
exit status zero and printed
`Reduced certificate checks passed: only y squared is needed.`
This was an exact arithmetic check of the examples;
no project-wide checks or CI checks were run for this note.
