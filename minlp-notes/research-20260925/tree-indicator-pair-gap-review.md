# Independent review of the three-leaf pairwise moment gap

Date: 2026-09-25.

Status: the proposed certificate is correct. The true closed convex hull value
is exactly \(96/17\). The pairwise moment relaxation admits a point with cost
\(359/64\), so its gap is **at least** \(41/1088\). No claim that \(359/64\)
is the optimum of the relaxation has been proved here. This review establishes
the certificate and its scope; it does not establish novelty.

## Setup

Let

\[
Q=\begin{pmatrix}
4&1&1&1\\1&1&0&0\\1&0&1&0\\1&0&0&1
\end{pmatrix},\qquad
E_Q=\{(u,Z,t):t\ge u^TQu,\ u_i(1-Z_i)=0,\ Z\in\{0,1\}^4\}.
\]

The center has index zero. The leaf block is the identity, and its Schur
complement is \(4-3=1\), so \(Q\succ0\). We study the lower hull boundary at

\[
x=(0,-1,1,0),\qquad z=(1,1/4,1/4,1/4).
\]

For center first and second moments, and moments selected by individual leaf
indicators, use

\[
M=\begin{pmatrix}1&x_0\\x_0&v\end{pmatrix},\qquad
M_i=\begin{pmatrix}z_i&s_i\\s_i&r_i\end{pmatrix}.
\]

The pairwise relaxation requires \(0\preceq M_i\preceq M\) and, for every
pair \(i,j\), an overlap matrix \(G_{ij}\) such that all four matrices

\[
G_{ij},\quad M_i-G_{ij},\quad M_j-G_{ij},\quad
M-M_i-M_j+G_{ij}
\]

are positive semidefinite. The cost after exact conditional leaf minimization
is

\[
4v+\sum_{i=1}^3\left[\frac{(x_i+s_i)^2}{z_i}-r_i\right].
\]

## Exact feasibility check

The proposed matrices are

\[
M=\operatorname{diag}(1,27/32),\quad
M_1=\begin{pmatrix}1/4&5/16\\5/16&27/64\end{pmatrix},\quad
M_2=\begin{pmatrix}1/4&-5/16\\-5/16&27/64\end{pmatrix},\quad
M_3=\operatorname{diag}(1/4,45/64),
\]

and

\[
G_{12}=0,\qquad
G_{13}=\frac1{128}\begin{pmatrix}18&26\\26&39\end{pmatrix},\qquad
G_{23}=\frac1{128}\begin{pmatrix}18&-26\\-26&39\end{pmatrix}.
\]

For each symmetric \(2\times2\) matrix, nonnegative diagonal entries and a
nonnegative determinant establish positive semidefiniteness. The following
table gives these three quantities. The signs of off-diagonal entries differ
between leaves 1 and 2 but do not change the entries in the table.

| Matrix | First diagonal entry | Second diagonal entry | Determinant |
|---|---:|---:|---:|
| \(M_i\), \(i=1,2\) | \(1/4\) | \(27/64\) | \(1/128\) |
| \(M-M_i\), \(i=1,2\) | \(3/4\) | \(27/64\) | \(7/32\) |
| \(M_3\) | \(1/4\) | \(45/64\) | \(45/256\) |
| \(M-M_3\) | \(3/4\) | \(9/64\) | \(27/256\) |
| \(G_{12}\) | \(0\) | \(0\) | \(0\) |
| \(M_1-G_{12}\), \(M_2-G_{12}\) | \(1/4\) | \(27/64\) | \(1/128\) |
| \(M-M_1-M_2+G_{12}\) | \(1/2\) | \(0\) | \(0\) |
| \(G_{i3}\), \(i=1,2\) | \(9/64\) | \(39/128\) | \(13/8192\) |
| \(M_i-G_{i3}\), \(i=1,2\) | \(7/64\) | \(15/128\) | \(7/8192\) |
| \(M_3-G_{i3}\), \(i=1,2\) | \(7/64\) | \(51/128\) | \(19/8192\) |
| \(M-M_i-M_3+G_{i3}\), \(i=1,2\) | \(41/64\) | \(3/128\) | \(25/8192\) |

Every nonzero cell matrix in this table has positive mass, meaning positive
top-left entry. Such a PSD matrix is realized by a finite scalar measure with
at most two atoms: for mass \(p\), first moment \(s\), and second moment \(r\),
put mass \(p/2\) at each of
\(s/p\pm\sqrt{r/p-(s/p)^2}\). Zero cells require no atoms. Consequently each
pair of leaf indicators and the center has an actual common finite law with
the prescribed moments. No passage to a closure is needed for pairwise
feasibility of this example.

Substitution in the objective yields

\[
4\frac{27}{32}
+2\left[\frac{(-1+5/16)^2}{1/4}-\frac{27}{64}\right]
-\frac{45}{64}
=\frac{359}{64}.
\]

## A global supporting inequality

The following proof works directly on \(E_Q\), including its points with
inactive center. It therefore avoids any subtlety about intersections of a
closed hull with the face \(z_0=1\).

Set \(c=48/17\) and \(h=(0,-c,c,0)\). For an active support \(T\), completing
the square gives

\[
u^TQu\ge 2h^Tu-h_T^TQ_T^{-1}h_T.
\tag{1}
\]

The empty support has conjugate term zero. Suppose first that the center is
active, write \(Z_i\in\{0,1\}\) for the leaf indicators, and put
\(k=Z_1+Z_2+Z_3\). Block inversion gives

\[
\frac{h_T^TQ_T^{-1}h_T}{c^2}
=Z_1+Z_2+\frac{(Z_1-Z_2)^2}{4-k}.
\tag{2}
\]

For every binary leaf pattern,

\[
Z_1+Z_2+\frac{(Z_1-Z_2)^2}{4-k}
\le\frac43(Z_1+Z_2)+\frac16Z_3.
\tag{3}
\]

Here is a complete case proof. If \(Z_1=Z_2=0\), the left side is zero.
If exactly one of \(Z_1,Z_2\) is one, the two sides are equal: both are
\(4/3\) when \(Z_3=0\), and \(3/2\) when \(Z_3=1\). If
\(Z_1=Z_2=1\), the left side is 2 and the right side is at least \(8/3\).
If the center is inactive, the active leaf matrix is the identity, so the
left side of (2) instead equals \(Z_1+Z_2\), which still satisfies (3).

Combining (1)--(3), the affine inequality

\[
t\ge 2c(-u_1+u_2)
-c^2\left[\frac43(Z_1+Z_2)+\frac16Z_3\right]
\tag{4}
\]

is valid on \(E_Q\). It remains valid on its closed convex hull by continuity.
At the prescribed \((x,z)\), its right side is

\[
4c-\frac{17}{24}c^2=\frac{96}{17}.
\tag{5}
\]

## Exact attainment

For every atom below, the center indicator is one, and the leaf indicators
are exactly the listed support. Set the atom's epigraph coordinate to its
quadratic cost.

| Leaf support | Probability | Continuous point \(u\) | Quadratic cost |
|---|---:|---|---:|
| \(\varnothing\) | \(1/2\) | \((0,0,0,0)\) | \(0\) |
| \(\{1\}\) | \(1/8\) | \((16,-64,0,0)/17\) | \(3072/289\) |
| \(\{2\}\) | \(1/8\) | \((-16,0,64,0)/17\) | \(3072/289\) |
| \(\{1,3\}\) | \(1/8\) | \((24,-72,0,-24)/17\) | \(3456/289\) |
| \(\{2,3\}\) | \(1/8\) | \((-24,0,72,24)/17\) | \(3456/289\) |

These probabilities sum to one. Their mean continuous point is
\((0,-1,1,0)\), their mean indicator vector is
\((1,1/4,1/4,1/4)\), and their mean cost is \(96/17\). Thus the bound (5)
is attained in the ordinary convex hull, proving that the closed hull value
is exactly \(96/17\).

Each listed point is also obtained by restricting
\(u_T=Q_T^{-1}h_T\) to its support and embedding by zeros, so equality holds
in the square completion. Every used leaf pattern has equality in (3).
This independently explains why the mixture attains the supporting cut.

## Conclusions and limits

The feasible pairwise point violates the globally valid cut (4), with exact
discrepancy

\[
\frac{96}{17}-\frac{359}{64}=\frac{41}{1088}>0.
\]

Therefore pairwise compatibility of the center's first two moments with leaf
indicators is insufficient for an exact formulation even after projection
to the original indicator epigraph. Its failure on these auxiliary moments
is not merely an artifact of retaining unnecessary moment information.
If all three leaves admitted one common law with these moments, conditional
leaf minimizers would give an original epigraph convex combination with cost
\(359/64\), contradicting (4).

This result concerns the specified moment relaxation. It does not preclude
a different compact formulation, establish computational hardness, or show
that every bounded-order compatibility hierarchy has a projected gap. It
also does not show that \(359/64\) is the pairwise relaxation's optimum.
The cut (4) separates this point; its availability does not imply that the
entire exact hull has a compact inequality description. No independent
literature search was part of this certificate review.

## Targeted verification performed

One inline `python` command using SymPy was run. With exact rational
arithmetic it checked both diagonal entries and the determinant of every
individual and pair-cell matrix; computed the objective \(359/64\);
enumerated all eight binary patterns to check (3); formed the active
principal inverses for all five attaining atoms; and checked their means,
indicator marginals, cost \(96/17\), and discrepancy \(41/1088\).

These checks independently verify the displayed finite algebra. The
square-completion argument proves the lower bound for every original
feasible point, and continuity extends it to the closed hull. The finite
mixture proves attainment. No project-wide tests or CI inspection were
performed, and no Lean verification was performed.
