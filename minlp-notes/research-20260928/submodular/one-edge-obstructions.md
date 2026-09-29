# Two failed exact-solution shortcuts for one positive quadratic pair

Date: 2026-09-28. Status: exact counterexamples, not a complexity classification.
The general exact complexity question remains open in this investigation.
The first example has a signed-tree interaction graph and belongs to the
established sign-switchable tractable class. A small exact perturbation below
gives the same obstructions outside that class. Neither example establishes
a difficult instance family.

Consider

\[
\min\{x^TQx-2b^Tx+c^Tz:0\le x_i\le2z_i,\ z\in\{0,1\}^4\},
\]

with

\[
Q=\begin{pmatrix}
2&1&-1&0\\
1&2&0&-1\\
-1&0&2&0\\
0&-1&0&2
\end{pmatrix},\qquad
b=(3,3,0,0)^T,\qquad c=(0,0,3/5,3/5)^T.
\]

The only positive off-diagonal pair is \(\{1,2\}\). The lower-right
block is \(2I\); its Schur complement is
\(\left(\begin{smallmatrix}3/2&1\\1&3/2\end{smallmatrix}\right)\),
whose eigenvalues are \(1/2\) and \(5/2\). Thus \(Q\succ0\).

## Fixing both endpoint indicators does not restore submodularity

Fix \(z_1=z_2=1\). For \(T\subseteq\{3,4\}\), define \(v(T)\)
as the minimum of the continuous quadratic when exactly the optional
indicators in \(T\) are one. Direct solution of the four strictly convex
problems gives:

| \(T\) | Optimal \(x\) | \(v(T)\) | \(v(T)+(3/5)\lvert T\rvert\) |
|---|---|---|---|
| \(\varnothing\) | \((1,1,0,0)\) | \(-6\) | \(-6\) |
| \(\{3\}\) | \((3/2,3/4,3/4,0)\) | \(-27/4\) | \(-123/20\) |
| \(\{4\}\) | \((3/4,3/2,0,3/4)\) | \(-27/4\) | \(-123/20\) |
| \(\{3,4\}\) | \((6/5,6/5,3/5,3/5)\) | \(-36/5\) | \(-6\) |

Every listed coordinate is in its required box. The submodular inequality
would require

\[
v(\{3\})+v(\{4\})\ge v(\varnothing)+v(\{3,4\}),
\]

but \(-27/2<-66/5\). Modular activation costs do not change this violation.
Thus branching on the indicators at the exceptional pair does not justify
calling the resulting support value function submodular.

This is also the global optimum of the original instance. If neither
endpoint is available, the best value is zero. If only endpoint 1 is
available, coordinate 4 optimally vanishes, while activating coordinate 3
gives \(x_1=2,x_3=1\) and value \(-6+3/5=-27/5\); leaving coordinate
3 inactive gives \(-9/2\). The case with only endpoint 2 is symmetric.
These are all greater than \(-123/20\). Because \(Q\succ0\), the table
contains exactly the two optimal continuous solutions, with ratios
\(x_2/x_1=1/2\) and \(2\).

## The scalar majorant envelope need not be unimodal

For \(r>0\), the standard weighted-square majorant is

\[
Q_r=Q+
\begin{pmatrix}
r&-1&0&0\\
-1&1/r&0&0\\
0&0&0&0\\
0&0&0&0
\end{pmatrix}.
\]

Write \(U(r)\) for the indicator optimum with \(Q_r\) replacing \(Q\).
The added quadratic is
\((\sqrt r\,x_1-x_2/\sqrt r)^2\), so
\(U(r)\ge-123/20\) for every \(r>0\). At \(r=1/2\) the added term
vanishes at the first singleton optimum above; at \(r=2\) it vanishes
at the other one. Therefore

\[
U(1/2)=U(2)=-123/20.
\]

At \(r=1\), the objective separates into identical two-coordinate
problems on \((x_1,x_3)\) and \((x_2,x_4)\). In each problem, leaving
the optional leaf inactive gives \(x_{\rm endpoint}=1\) and value
\(-3\). Activating it gives
\(x_{\rm endpoint}=6/5,x_{\rm leaf}=3/5\), continuous value
\(-18/5\), and total value \(-3\). Turning off the endpoint cannot
improve these values. Hence

\[
U(1)=-6>-123/20.
\]

The strict inequality between two equal global minima disproves
quasiconvexity and the usual single-valley notion of unimodality. It rules
out a proof of exact optimization based only on those properties of this
scalar envelope. It does not rule out another polynomial exact algorithm,
and it supplies no NP-hardness result.

## The same obstructions outside the sign-switchable class

Replace \(Q_{34}=Q_{43}=0\) by \(-\eta\), where \(\eta=1/10\),
and leave all other data unchanged. Write \(Q^{\eta}\) for this matrix.
The negative path \(1,3,4,2\) now joins the endpoints of the sole positive
edge. Consequently no diagonal sign switching makes all off-diagonal
entries nonpositive: the negative path requires equal endpoint signs,
whereas the positive edge requires opposite signs.

Positive definiteness follows directly from

\[
x^TQ^{\eta}x=(x_1+x_2)^2+(x_1-x_3)^2+(x_2-x_4)^2
 +\eta(x_3-x_4)^2+(1-\eta)(x_3^2+x_4^2).
\]

This sum is positive for every nonzero \(x\), since \(0<\eta<1\).
The first three conditional solutions in the table remain unchanged.
With both leaves active, the unique solution is

\[
x=(57/47,57/47,30/47,30/47),\qquad
v(\{3,4\})=-342/47,
\]

so its value including activation costs is \(-1428/235\). The conditional
submodular inequality still fails, because
\(-27/2<-6-342/47=-624/47\).

The two singleton solutions remain the exact global optima, of value
\(-123/20<-1428/235\). To exclude endpoint-inactive cases without an
exhaustive table, suppose endpoint 2 is zero. Dropping all nonnegativity,
upper bounds, and activation penalties on the other three coordinates gives
the valid lower bound

\[
-\frac{9}{2-2/(4-\eta^2)}=-3591/598>-123/20.
\]

The case with endpoint 1 zero is symmetric; if both are zero the objective
is nonnegative. These bounds leave no additional global minimizer.

Let \(U^{\eta}(r)\) be the perturbed scalar majorant envelope. Exactness of
the majorant at the singleton solutions again gives
\(U^{\eta}(1/2)=U^{\eta}(2)=-123/20\). At \(r=1\), the endpoint-active
conditional values including penalties are \(-6,-6,-6,-1428/235\).
The last solution is symmetric, so the added square vanishes and the
optimizer is the same both-leaf point displayed above. Endpoint-inactive
solutions have the stronger lower bound from the preceding paragraph,
since majorization can only increase their objective. Thus

\[
U^{\eta}(1)=-1428/235>-123/20.
\]

Both proof shortcuts therefore fail even when the known sign-switching
criterion does not apply. This is still only a four-variable counterexample.

## Why the first hub-elimination hardness attempt did not work

Eliminating a two-coordinate block
\(H=\left(\begin{smallmatrix}a&\beta\\\beta&d\end{smallmatrix}\right)\succ0\)
with \(\beta>0\) can create positive effective interactions between leaves
attached with negative coefficients to opposite endpoints, since
\((H^{-1})_{12}<0\). However, it also creates unavoidable negative
interactions among leaves attached to the same endpoint. Adding further
nonpositive original coefficients cannot cancel those negative interactions.
An argument claiming an arbitrary bipartite quadratic objective from this
construction must account for them. No valid such reduction was obtained.

For independent leaves, a further obstacle is that each leaf's activation
decision, after fixing the two hub values, is determined by a constant-size
piecewise-quadratic comparison. This suggests an arrangement algorithm in
two dimensions. No full bit-complexity theorem is claimed here, because
upper-bound faces, algebraic boundary handling, and degenerate cells would
need a separate treatment. General attractive interactions among leaves
invalidate that independent-leaf argument.

## Verification and relation to prior work

The counterexample addresses the exact question recorded in
[the preceding majorant note](../../research-20260927/free-frontier.md).
The majorant identity itself is established weighted AM–GM. The computations
above do not claim a new optimization method or a publication-level advance.
For the unperturbed example, switching the signs of coordinates 2 and 4 makes all
off-diagonal entries nonpositive. The accompanying indicator orders can also
be reversed, as covered by Han and Gómez's established sign-switching
extension. See [the literature audit](near-stieltjes-literature-audit.md).

The targeted command

```sh
python research-20260928/submodular/check_one_edge_obstructions.py
```

uses exact rational arithmetic and exhaustive nonnegative support-face
enumeration from the existing small-instance checker. For each of the two
instances, it verifies the four conditional values, the full optimum, and
the three majorant optimum values. It also verifies the exact rational
endpoint-inactive lower bound for the perturbed instance.
All returned optima satisfy the upper bound 2, so the unconstrained-above
minimum certificates also prove the stated box-constrained optima.
The general claims are justified by the formulas, not by finite testing.
No project-wide verification or CI inspection was used; no Lean proof was
attempted.

Additional primary sources examined while exploring hardness were
[Liu, Atamtürk, Gómez and Küçükyavuz, *Polyhedral analysis of quadratic
optimization problems with Stieltjes matrices and indicators*](https://link.springer.com/article/10.1007/s10107-025-02272-7),
especially the hardness of optimizing a lifted inverse-matrix entry, and
[Brumelle, Granot and Liu, *Ordered optimal solutions and parametric minimum
cut problems*](https://doi.org/10.1016/j.disopt.2005.03.002).
The first concerns a different lifted objective; its hardness does not
establish hardness of the present indicator quadratic. The second concerns
ordered parametric cut families under specific capacity changes; those
conditions have not been shown to apply to the majorant envelope here.
An unsuccessful search for an equivalent counterexample or a complexity
classification is not evidence of novelty.

The [independent review](obstruction-independent-review.md) recomputed all
finite-box support optima for both matrices and all three ratio values. It
found no substantive error and retains the limited significance assessment.
