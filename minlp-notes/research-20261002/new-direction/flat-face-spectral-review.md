# Review of the maximal-optimal-face spectral lemma

Date: 2026-10-02. Scope: an independent mathematical check of a local
structural lemma for box QP. No external search or new subagent was used.

**Verdict.** The lemma is correct when face maximality is taken within
a fixed integer assignment that contains a global optimizer. A sufficiently
small neighborhood then excludes other integer assignments. The upper
spectral bound follows directly from a proper coloring of the sparse
graph; a chordal PSD decomposition is unnecessary.

The result controls one local optimal patch. It does not bound how many
such patches exist, identify a globally optimal face algorithmically,
or certify global optimality without the supplied growth assumption.

## 1. Precise statement

Let `F` be a quadratic with Hessian `H` on a bounded continuous or
mixed-integer product box `X`. Let `S=argmin_X F` be nonempty and assume

```
F(x)-f* >= g dist(x,S)^2,               g>0.                       (1)
```

Suppose `H_ii<=L` for every coordinate, with `L>0`, and the interaction
graph has a supplied tree decomposition of largest bag size `p`.
The decomposition may belong to the supplied factor graph, which can
contain edges that cancel in the summed Hessian; that only gives a
supergraph and does not weaken the argument.

Fix an integer assignment whose continuous slice contains a global
optimizer. Among continuous box faces whose relative interiors contain
such an optimizer, choose `G` maximal by inclusion. Let

```
s in relint(G) intersect S,
J = the free continuous coordinates of G,
A = H_JJ.
```

Then:

- Every sufficiently nearby global optimizer belongs to `G`.
- `A` is positive semidefinite, and
  `S intersect G = (s+ker A) intersect G`, with all fixed coordinates
  understood to remain fixed.
- Every positive eigenvalue of `A` lies in `[2g,pL]`.

Thus, when `A` has nonzero spectrum, its condition number on its range
is at most

```
pL/(2g) <= p kappa/2,          kappa=max(1,L/g).                   (2)
```

If `A=0`, or `J` is empty, there is no positive spectral condition number
to bound. Those cases should be called vacuous rather than assigned a
positive minimum eigenvalue. Rationality is not needed for this local
geometric statement.

## 2. Why maximality gives a local patch in one face

At a point in `relint(G)`, every free coordinate has positive distance
from both of its original bounds. Choose a neighborhood small enough
that these coordinates remain strictly between those bounds. Also make
it too small for a coordinate active at one bound to reach its opposite
bound. Fixed original coordinates can be substituted out first.

Every point in this neighborhood has a smallest containing continuous
box face that contains `G`: original free coordinates stay free, and
original active coordinates may only stay active at the same bound or
become free. If that point is globally optimal, a strict superface
would contradict the maximality used to choose `G`. Hence every nearby
optimizer lies in `G`.

For a mixed box, also choose the neighborhood radius below `1/2`.
Distinct integer assignments have Euclidean distance at least one,
so every nearby optimizer has the fixed integer assignment. The face
argument then applies within that slice. No growth property for a
continuous relaxation of the integer coordinates is being assumed.

Because `s` is a minimum in the relative interior of `G`,

```
grad_J F(s)=0,                    A>=0.
```

For every point `s+d` of that face, exact quadratic expansion gives

```
F(s+d)-f* = d_J^T A d_J/2.                                      (3)
```

A positive semidefinite quadratic vanishes exactly on its kernel.
Equation (3) proves the claimed identity for `S intersect G` on the
whole face. Combined with the preceding neighborhood argument, it also
describes the full global optimal set locally around `s`.

## 3. The lower positive-eigenvalue bound

Let `v` be a unit eigenvector of `A` with positive eigenvalue `lambda`,
extended by zero outside `J`. Take nonzero `t` small enough that
`x=s+tv` lies in `relint(G)`.

Let `epsilon` be a neighborhood radius from Section 2, and additionally
require `2|t|<epsilon`. A nearest optimizer `s'` to `x` exists by
compactness. Since `s` is itself optimal,

```
||s'-s|| <= ||s'-x||+||x-s||
          = dist(x,S)+|t| <= 2|t| < epsilon.
```

Therefore `s'` lies in `G` and `s'-s` lies in `ker A`. The vector `v`
is orthogonal to that kernel, so

```
||x-s'||^2 = t^2+||s'-s||^2 >= t^2.
```

Equality is attained by `s'=s`. Consequently `dist(x,S)=|t|`, and
(1), (3) yield `lambda t^2/2>=g t^2`. Hence `lambda>=2g`.

This nearest-point argument is the needed justification for using growth
toward the full set `S`, rather than growth toward just `S intersect G`.

## 4. The upper bound needs only graph coloring

The sparsity graph of the principal submatrix `A` has treewidth at
most `p-1`, and therefore admits a proper coloring with at most `p`
colors. One can obtain this from a leaf-bag elimination order and greedy
coloring. Restricting the supplied decomposition to `J` does not
increase bag size.

For an arbitrary vector `v`, write `v=sum_c v_c`, where `v_c` is
supported on color class `c`. Positive semidefiniteness gives

```
v^T A v
 = ||sum_c A^(1/2) v_c||^2
 <= p sum_c ||A^(1/2) v_c||^2
 = p sum_c v_c^T A v_c
 = p sum_i A_ii v_i^2.                                          (4)
```

The last equality uses that each color class is independent: its
off-diagonal entries of `A` are zero. Thus in Loewner order

```
0 <= A <= p diag(A) <= p L I.                                   (5)
```

In particular, every eigenvalue is at most `pL`. This proof also works
with any known proper coloring bound, whether or not it comes from
treewidth. Zero diagonal entries cause no difficulty.

The proposed alternative proof by chordal PSD decomposition is valid:
rank-one PSD terms supported on filled bags of size at most `p`
satisfy the same termwise inequality, and their diagonals sum to
`diag(A)`. Equation (4) avoids needing that decomposition or handling
singular elimination pivots explicitly.

## 5. Maximality is essential

The lower spectral bound can fail for a nonmaximal face, even when its
relative interior contains an optimizer. The failure can be arbitrarily
large at fixed conditioning. For rational `0<epsilon<1`, consider

```
F(x,y,z)=(epsilon x-y+z)^2,
X=[-1,1] times [0,1] times [0,1].
```

Its optimal set is `S={epsilon x=y-z}` intersected with this box,
and `g=1` is valid globally. Put `r=epsilon x-y+z` and keep `x`
fixed. If `r>=0`, increase `y` and decrease `z` by nonnegative amounts
whose sum is `r`. The available total movement is sufficient because

```
1-y+z >= r,               since epsilon x<=1.
```

For `r<=0`, decrease `y` and increase `z` by total amount `-r`;
the available capacity `y+1-z` is at least `-r` because
`epsilon x>=-1`. In either case the resulting point lies in `S`.
Its squared displacement is at most the square of the total movement,
namely `r^2`. Thus `F>=dist(.,S)^2` everywhere. The curvature bound
is `L=2`, so `kappa=2` is independent of `epsilon`.

Now choose `s=(0,0,0)` and the nonmaximal face
`G={y=z=0, -1<=x<=1}`. The point `s` lies in `relint(G)`, and its
free Hessian is `[2 epsilon^2]`. Its positive eigenvalue tends to zero
while `g=1`, `L=2` and the bag size remain fixed. Nearby optimizers leave
`G` in both directions of the free `x` coordinate. A strict superface, including
the full box, contains optimizers in its relative interior, so the
maximality hypothesis correctly excludes this example.

In particular, a smaller face obtained by snapping an approximate point
to nearby bounds cannot silently replace the maximal face in the
spectral argument. Exact recovery on that smaller face may still work,
but the lower bound `2g` need not hold there.

## 6. What the lemma does not establish

The proof supplies spectral control for one maximal optimal face. It
does not give a width-preserving quotient of its kernel: the
[flat-quotient example](flat-quotient-obstruction.md) shows that this
can create a complete constraint graph even with constant conditioning.

Nor does it bound the number, adjacency, or geometry of different
maximal optimal faces. It assumes a globally optimal face has been
chosen, so it does not supply the missing algorithmic global certificate.
These limits matter when using the lemma as a local ingredient in an
unknown-growth algorithm.

This review checked the proof algebraically. A targeted inline
`python3 - <<'PY'` check verified the local Markdown link and balanced
code fences. No executable numerical test, project-wide verification,
CI inspection, or external search was performed for the spectral claims.
