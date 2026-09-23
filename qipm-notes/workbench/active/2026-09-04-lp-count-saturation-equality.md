# Equality structure and non-rigidity of count-optimal \(\ell_p\)-ball lifts

Status: Proved; literature-screened; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the arithmetic and local equality theorem; no global rigidity claim

## Results

Fix \(1<p<\infty\), \(N\geq2\), and a block-dimension cap \(d\geq3\).
Put

\[
 n=N-1,\qquad c=d-2,\qquad
 k_*=\left\lceil\frac{n}{c}\right\rceil,\qquad
 \sigma=k_*c-n\in\{0,\ldots,c-1\}.                                \tag{1}
\]

Consider an exact definable proper-cone lift of \(B_p^N\) using exactly
\(k_*\) factors of original dimensions \(m_i\leq d\). After minimal-face
reduction, let \(s_i\leq m_i\) be the factor dimensions. Count optimality
forces all \(k_*\) factors to be non-ray and

\[
 n\leq\sum_{i=1}^{k_*}(s_i-2)\leq k_*c=n+\sigma.                   \tag{2}
\]

Define the capacity excess

\[
 \Delta=\sum_i(s_i-2)-n.                                          \tag{3}
\]

Then

\[
 \boxed{0\leq\Delta\leq\sigma,\qquad
 M:=\sum_i s_i=n+2k_*+\Delta.}                                    \tag{4}
\]

This completely resolves what minimum factor count alone says about
dimensions.

- If \(c\mid n\), then \(\sigma=0\). Every count-optimal lift has
  \(s_i=m_i=d\) for all \(i\), minimum total dimension among capped-block
  lifts, and exact curvature-capacity equality.
- If \(c\nmid n\), count optimality need not imply capacity equality or
  minimum total dimension. Every integer \(\Delta\in\{0,\ldots,\sigma\}\)
  is realized by an exact \(p\)-order-tree lift whose reduced faces are the
  full displayed blocks.

When \(\Delta=0\), equality has a strong but only local consequence. At
every common \(C^2\) regular primal-polar contact in a positively curved
orthant patch, the block curvature matrices form a Parseval fusion
decomposition after whitening by the curvature of \(\partial B_p^N\).
Each block uses its full \(s_i-2\) quotient-curvature capacity. This is a
precise equality theorem, but it does not identify the lifting cones or
force a global norm tree.

## Arithmetic proof

The universal curvature-capacity theorem gives

\[
 n\leq\sum_{i:\,s_i\geq2}(s_i-2)_+.                               \tag{5}
\]

An exact lift using only \(k_*\) total factors cannot contain a ray or
zero-dimensional factor: otherwise it would have fewer than \(k_*\)
non-ray factors, contradicting the already proved count lower bound.
Nor can a reduced factor have dimension two: deleting its zero curvature
capacity would leave at most \((k_*-1)c<n\). Thus every reduced factor has
\(s_i\geq3\), contributes \(s_i-2\), and

\[
 \sum_i(s_i-2)\leq k_*(d-2)=n+\sigma.
\]

This proves (2)--(4). If \(\sigma=0\), equality throughout forces
\(s_i=m_i=d\).

## Every nondivisible slack value is attainable

Choose positive integers \(b_i\leq c\) with

\[
 \sum_{i=1}^{k_*}b_i=n.
\]

The standard chain tree uses one block \(K_{p,b_i+2}\) at node \(i\).
Its \(b_i+1\) actual child entries consist of \(b_i\) new leaves and the
next internal scalar, except at the last node, which has \(b_i+1\) leaves.

For any desired \(\Delta\leq\sigma\), choose integers

\[
 0\leq r_i\leq c-b_i,\qquad \sum_i r_i=\Delta.                     \tag{6}
\]

Such a choice exists because
\(\sum_i(c-b_i)=k_*c-n=\sigma\). Replace node \(i\)'s cone by

\[
 K_{p,b_i+2+r_i}
 =\{(t,u):t\geq\|u\|_p\}                                          \tag{7}
\]

and affinely fix the \(r_i\) added norm coordinates to zero. Recursive
elimination is unchanged, so the projection remains exactly \(B_p^N\).
The block dimension is at most

\[
 b_i+2+r_i\leq c+2=d,
\]

and its contribution to (3) is \(b_i+r_i\). Hence the total excess is
exactly \(\Delta\).

This padding is not removed by minimal-face reduction. Set the leaf
variables to zero and choose every internal scalar positive, decreasing
rapidly enough from the root toward the leaves that every inequality in
(7) is strict. Zero added norm coordinates do not prevent strict
inequality. The resulting product point is in the interior of every full
\(K_{p,b_i+2+r_i}\), so the minimal factor faces have precisely the
displayed dimensions.

Thus count-optimality alone permits the full interval of total dimensions
in (4), even within the natural irreducible-looking \(p\)-order-cone
dictionary; artificial ray products are unnecessary.

## Local equality theorem

Retain the count-optimal hypothesis above, so there are no ray, zero, or
two-dimensional reduced factors. Assume that the reduced exact lift, not
necessarily a tree, satisfies

\[
 \sum_i(s_i-2)=n.                                                   \tag{8}
\]

At a common \(C^2\) regular contact on a strictly positively curved
orthant patch, let \(A_i(u)\in K_i\) and \(B_i(v)\in K_i^*\) be the
primal and polar slack factors, and put

\[
 H_i=-DA_i(0)^TDB_i(0),\qquad
 \mathcal K=\sum_iH_i.                                             \tag{9}
\]

The exact local cone lemma gives

\[
 H_i\succeq0,\qquad \operatorname{rank}H_i\leq s_i-2.              \tag{10}
\]

The matrix \(\mathcal K\) is a positive multiple of the second fundamental
form in the chosen coordinates, hence \(\mathcal K\succ0\) and has rank
\(n\). Equations (8)--(10) force equality in every rank bound:

\[
 \boxed{\operatorname{rank}H_i=s_i-2\quad\text{for every }i.}      \tag{11}
\]

Moreover, whiten the tangent coordinates and set

\[
 P_i=\mathcal K^{-1/2}H_i\mathcal K^{-1/2}.                        \tag{12}
\]

Then

\[
 \boxed{P_i\succeq0,\qquad \sum_iP_i=I_n,\qquad
 P_i^2=P_i,\qquad P_iP_j=0\ (i\ne j).}                             \tag{13}
\]

Thus the whitened block curvatures are mutually orthogonal projections of
ranks \(s_i-2\). Equivalently,

\[
 H_i\mathcal K^{-1}H_i=H_i,\qquad
 H_i\mathcal K^{-1}H_j=0\quad(i\ne j).                             \tag{14}
\]

### Proof of the projection conclusion

Factor \(P_i=Z_iZ_i^T\), with \(Z_i\) having
\(\operatorname{rank}P_i=s_i-2\) columns, and concatenate the \(Z_i\)'s
into \(Z\). By (8) and (11), \(Z\) is square \(n\times n\). Equation
\(\sum_iP_i=I_n\) says

\[
 ZZ^T=I_n.
\]

Therefore \(Z\) is orthogonal, so its column groups are orthonormal within
each group and mutually orthogonal across groups. This gives (13)--(14).

There is also a factor-level interpretation. Write

\[
 a_i=A_i(0),\quad b_i=B_i(0),\quad
 X_i=DA_i(0),\quad Y_i=DB_i(0).
\]

For \(s_i>2\), equation (11) forces \(a_i,b_i\neq0\). The derivatives
take values in \(b_i^\perp\) and \(a_i^\perp\), respectively. The pairing
descends to the nondegenerate \(s_i-2\)-dimensional quotient pairing

\[
 \frac{b_i^\perp}{\operatorname{span}\{a_i\}}
 \ \times\
 \frac{a_i^\perp}{\operatorname{span}\{b_i\}}.                     \tag{15}
\]

Both quotient spaces in (15) have dimension \(s_i-2\), and their pairing
is nondegenerate. Let

\[
 \bar X_i:\mathbb R^n\to
 b_i^\perp/\operatorname{span}\{a_i\},\qquad
 \bar Y_i:\mathbb R^n\to
 a_i^\perp/\operatorname{span}\{b_i\}
\]

be the maps induced by \(X_i,Y_i\). Since \(H_i\) factors through
\(\bar X_i,\bar Y_i\), its rank \(s_i-2\) forces both induced maps to be
surjective. No block can hide unused local curvature capacity when (8)
holds.

## What equality does not prove

Equation (13) is a tangent-space statement at each regular contact. It is
only a second-order statement. It does not identify a cone from its local
complementarity pairing, make the subspaces in (13) constant as the contact
moves, or supply the integrability needed to reconstruct a global tree.
Accordingly, no claim is made that an arbitrary equality lift is a norm
tree or even uses \(p\)-order cones.

The padding construction is a concrete obstruction to deriving such
rigidity from *count* saturation when \(\sigma>0\): it preserves the
minimum count while changing every requested capacity excess and total
dimension in (4), and the added directions remain in the full minimal face.

Even when \(\sigma=0\), syntax-level tree uniqueness would not be an
invariant statement without specifying an equivalence relation on lifts.
Affine equations may be recombined, product factors permuted and linearly
isomorphic copies substituted without changing the represented body. A
global classification would need hypotheses beyond local rank equality,
for example a fixed cone dictionary and a reduced incidence model.

## Barrier consequences and boundary

For a fixed dictionary in which every factor is a \(p\)-order cone of
original dimension between \(3\) and \(d\), the companion
[product-premium theorem](2026-09-04-pcone-product-barrier-premium.md)
already gives, for every possibly coupled ambient LHSC barrier,

\[
 \nu\geq k_*h(p)>2k_*\qquad(p\ne2).                                \tag{16}
\]

This conclusion does not require count saturation; the curvature theorem
forces at least \(k_*\) \(p\)-order blocks.

For arbitrary cone dictionaries, neither (11) nor (13) implies the
Hildebrand cross-ratio witness underlying \(h(p)\). Those equations contain
only the second jet at complementary contacts, whereas the barrier premium
uses global projective boundary data. Thus no \(p\)-dependent ambient
barrier premium is claimed from count saturation alone. The arbitrary-
dictionary problem outside the minimum-total-space regime remains open.

The only unconditional strict premium proved by these workbench arguments
is the minimum-space case: if the entire lifting cone has dimension \(N+1\),
minimum-dimensional lift rigidity identifies it with \(K_{p,N+1}\), and
the product-premium note gives \(\nu\geq h(p)>2\) for \(p\ne2\).

## Literature boundary

The upper norm-tree construction is classical; see Krokhmal and Soberanis,
[*A unified approach for modeling risk preferences in portfolio
optimization*](https://doi.org/10.1016/j.ejor.2009.03.053), Proposition 1,
and Blanco and Martínez-Antón,
[*On Minimal Extended Representations of Generalized Power
Cones*](https://doi.org/10.1137/23M1617205).

The product barrier premium and its Hildebrand source are recorded in the
companion note. A targeted search found no equality-case theorem for the
universal dimension-minus-two curvature inequality, no Parseval fusion
conclusion for saturated cone lifts, and no global classification of
count-optimal \(B_p^N\) lifts over arbitrary tame cone dictionaries. The
local projection theorem and the exact slack interval (4) therefore appear
new, subject to specialist review.

## Audit checklist

- Check that count optimality rules out ray and zero factors when the total
  factor count is exactly \(k_*\).
- Check realization of every integer \(\Delta\in[0,\sigma]\), including
  simultaneous strict feasibility of all padded blocks.
- Check that rank equality and positive semidefiniteness imply the
  orthogonal-projection identities (13), not merely direct-sum ranges.
- Check the quotient-pairing statement (15), especially the locations of
  \(\operatorname{span}\{a_i\}\) and \(\operatorname{span}\{b_i\}\).
- Keep the local theorem separate from any global tree or arbitrary-
  dictionary barrier-rigidity claim.

The independent audit verified the ray/face arithmetic, every-\(\Delta\)
padding construction, simultaneous strict feasibility, Parseval projection
identities, and quotient-pairing argument. It required the explicit
retention of the no-low-dimensional-factor hypothesis and the
dimension-\(3,\ldots,d\) restriction in the barrier paragraph, now included
above. It found no mathematical error or direct literature collision.
