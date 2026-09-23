# Additive standard-barrier frontier for Hermitian PSD lifts of product balls

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the theorem; novelty not established

## Result

Fix \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\), let
\(\delta=\dim_{\mathbb R}\mathbb F\in\{1,2,4\}\), and impose the order
cap \(R\geq2\) on every Hermitian PSD factor.  Put

\[
 c=R-1,\qquad B=\delta c,
 \qquad C=\prod_{a=1}^hB_2^{s_a},
 \qquad p_a=s_a-1.                                      \tag{1}
\]

Suppose a strictly feasible affine lift of \(C\) over a finite product
of \(H_+^{r_i}(\mathbb F)\), \(r_i\leq R\), has globally labelled
\(C^1\) primal and dual factors for every polar-extreme slack row.  Assume
also that each selected primal boundary tuple lies in the closure of the
affine slice on which the standard product log-determinant is restricted.

Define

\[
 \ell_a=\left\lceil{p_a\over B}\right\rceil             \tag{2}
\]

and let \(e_a=1\) precisely in the following cases:

\[
 \begin{array}{c|c}
 \mathbb F& e_a=1\\ \hline
 \mathbb R&B\mid p_a\text{ and }p_a/B\geq2,\\
 \mathbb C\text{ or }\mathbb H
   &B\mid p_a\text{ and }(R,p_a)\ne(2,\delta).
 \end{array}                                             \tag{3}
\]

Then the restricted standard barrier satisfies the additive lower bound

\[
 \boxed{\displaystyle
       \nu_{\rm std,slice}\geq\sum_{a=1}^h(\ell_a+e_a).} \tag{4}
\]

For \(\mathbb F=\mathbb C\) or \(\mathbb H\), the relative-top-class
argument below proves that this is exact:

\[
 \boxed{\displaystyle
 \nu_{\rm std,slice}^{\min}
 =\sum_{a=1}^h
 \begin{cases}
  1,&R=2,\ s_a=\delta+1,\\
  \left\lceil{s_a\over \delta(R-1)}\right\rceil,&\text{otherwise}.
 \end{cases}}                                           \tag{5}
\]

The first line is the direct spin-factor slice
\(H_+^2(\mathbb F)\cong Q_{\delta+2}\).  All other upper bounds in (5)
are attained by grouped Hermitian Schur epigraphs.

The independently audited
[canonical sequential contact-range
theorem](2026-09-04-hermitian-sequential-contact-range-frontier.md)
subsequently closed every real one-projective-channel residue and proved
the same exact formula (5) for
\(\mathbb F=\mathbb R,\mathbb C,\mathbb H\). It constructs one simultaneous
contact at which the aggregate dual range and primal nullity are at least
the right side of (5), without a constant-rank assumption or a persistent
source-to-label assignment. Thus (5) is now the exact all-field additive
frontier under the stated hypotheses. The relative-top-class proof in this
note remains an independent route for the complex and quaternionic cases
and all nonexceptional real residues.

This is a theorem for the restricted **standard product log-determinant**
under global \(C^1\) full-slack selections.  It is not an optimum over
arbitrary coupled barriers and not an iteration lower bound.

## 1. Pointwise private-nullity ledger

At a simultaneous product contact, write

\[
 E_i=\ker X_i(x),\qquad z_i=\dim_{\mathbb F}E_i,
 \qquad U_{ia}=\operatorname {Ran}Y_i^a(x_a),             \tag{8}
\]

and define the private quotient dimension

\[
 d_{ia}=\dim_{\mathbb F}
 {U_{ia}\over U_{ia}\cap\sum_{b\ne a}U_{ib}},
 \qquad D_a=\sum_i d_{ia},\qquad Z=\sum_i z_i.           \tag{9}
\]

Cylindrical complementarity makes the row-\(a\) mixed channel of block
\(i\) factor through a real Hom space of dimension at most

\[
 \delta\,\operatorname {rank}_{\mathbb F}X_i(x)\,d_{ia}
       \leq B d_{ia}.                                    \tag{10}
\]

The row metric has rank \(p_a\), and the private subspaces for distinct
rows are jointly independent in \(E_i\).  Therefore

\[
        D_a\geq\ell_a,
        \qquad \sum_aD_a\leq Z.                          \tag{11}
\]

The determinant of block \(i\) vanishes to exact order \(z_i\) on a
segment from the selected boundary point to a strict interior fiber.  The
one-dimensional self-concordant gradient inequality gives

\[
                         \nu_{\rm std,slice}\geq Z.       \tag{12}
\]

Equations (11)--(12) give the baseline \(\nu\geq\sum_a\ell_a\).

## 2. A saturated divisible row has projective phases

Suppose \(B\mid p_a\), write \(p_a=qB\), and assume
\(D_a=q\) at a contact.  Equality holds throughout the row version of
(10).  Every productive private quotient then has dimension one, its
primal factor has rank \(c=R-1\) and nullity one, and its dual contact
factor has rank one.  Exactly \(q\) labels contribute, each with a
rank-\(B\) positive-semidefinite mixed-curvature form; all other row
channels vanish.

For completeness, rank changes do not spoil this statement on closures.
Partition the saturated locus by its finite productive label set \(J\)
and take closures \(K_{a,J}\).  Continuity of the mixed-curvature forms
shows that the nonempty \(K_{a,J}\) are pairwise disjoint.  Along a
closure, a productive dual matrix is a limit of rank-one matrices.  If the
limit were zero, two-sided positivity would make its derivative and mixed
channel zero.  Otherwise its rank is one, and mixed rank \(B\),
complementarity, and the order cap force primal rank \(c\) and nullity
one.

Rank one need not persist off the closure.  Its unique positive eigenvalue
is, however, uniformly separated from zero on the compact projected set.
The corresponding simple top-eigenline therefore extends by a \(C^1\)
spectral projector to a neighborhood and defines a phase

\[
        \phi_i^a:S^{qB}\supset P_{a,J}\longrightarrow
                         \mathbb F P^c.                 \tag{13}
\]

At a rank-one PSD value, the kernel--kernel compression of the derivative
vanishes.  Hence the phase derivative is exactly the off-diagonal support
derivative seen by mixed curvature.  The joint phase

\[
       \Phi_{a,J}:P_{a,J}\longrightarrow(\mathbb F P^c)^q              \tag{14}
\]

is consequently a local diffeomorphism on a neighborhood of the projected
compact closure.

## 3. Exactly which phase maps can cover the source sphere

The neighborhood in (14) is a proper subset of \(S^{qB}\), except in the
cases deliberately omitted from (3).  Indeed, otherwise compactness makes
(14) a finite covering onto the connected target.

For \(\mathbb F=\mathbb R\), if \(q\geq2\), this is impossible.  For
\(c=1\), the target is a \(q\)-torus; for \(c\geq2\), its universal
cover is \((S^c)^q\), which has intermediate cohomology absent from
\(S^{qc}\).  When \(q=1\), the standard double cover
\(S^c\to\mathbb RP^c\) is topologically possible, which is exactly why the
relative-top-class proof does not close the real residue (7).  The
sequential contact-range theorem closes it without trying to exclude this
cover.

For \(\mathbb F=\mathbb C\), \(\mathbb CP^c\) has nonzero
intermediate \(H^2\) when \(c\geq2\), and a product of at least two
copies has intermediate cohomology even when \(c=1\).  Thus only
\(q=c=1\), the identity \(S^2\cong\mathbb CP^1\), survives.  For
\(\mathbb F=\mathbb H\), the same argument in degree four leaves only
\(q=c=1\), \(S^4\cong\mathbb HP^1\).  These two survivors, together
with the real \(R=2,p_a=1\) case, are precisely the direct spin-factor
exceptions in (3).

Let \(u_a\) be the top cohomology class of the source sphere.  Since the
phase neighborhood is proper, \(u_a\) restricts to zero on its pullback
to the full product of source spheres.

## 4. Relative top classes add the missing units simultaneously

Put \(L=\sum_a\ell_a\) and \(E=\{a:e_a=1\}\).  Suppose, contrary to
(4), that \(\nu_{\rm std,slice}<L+|E|\).  At every simultaneous contact,
(11)--(12) give

\[
                         Z\leq L+|E|-1.                \tag{15}
\]

If every row in \(E\) had \(D_a\geq\ell_a+1\), then (11) would give
\(Z\geq L+|E|\).  Hence the saturated-row loci

\[
                    A_a=\{x:D_a(x)=\ell_a\},\qquad a\in E,             \tag{16}
\]

cover the full product \(M=\prod_aS^{p_a}\).

For each fixed row, partition \(A_a\) by productive label set and use the
disjoint compact closures from Section 2.  Choose disjoint neighborhoods
inside the pullbacks of the proper phase neighborhoods.  Their union
\(U_a\) contains \(A_a\) and satisfies \(u_a|_{U_a}=0\).  The sets
\(U_a\), \(a\in E\), cover \(M\).  Lift each \(u_a\) to relative
cohomology and take their cup product.  It lies in

\[
 H^{\sum_{a\in E}p_a}
       \left(M,\bigcup_{a\in E}U_a;\mathbb R\right)=0,                 \tag{17}
\]

but maps to the nonzero Kunneth product
\(\smile_{a\in E}u_a\) in absolute cohomology.  This contradiction proves
(4).  Notice that source factors outside \(E\) cause no problem: the
relative group in (17) vanishes because the neighborhoods cover all of
\(M\), not because the displayed degree is the dimension of \(M\).

## 5. Matching constructions and scope

For a nonexceptional source, partition its \(s_a\) real coordinates into
\(k_a=\lceil s_a/B\rceil\) groups.  Embed each group isometrically in
\(\mathbb F^c\), introduce one block

\[
       \begin{pmatrix}t_G&w_G^*\\w_G&I_c\end{pmatrix}\succeq0,
       \qquad \sum_Gt_G=1,                              \tag{18}
\]

and repeat independently over the sources.  Schur complementation gives
\(t_G\geq\|w_G\|^2\), so the projection is exactly the product of balls.
The restricted determinant is \(t_G-\|w_G\|^2\); hence the standard
barrier parameter is at most \(\sum_ak_a\).  For
\(R=2,s_a=\delta+1\), use instead the direct trace-one slice of
\(H_+^2(\mathbb F)\), whose restricted parameter is one.  The lower bound
proves exactness in (5).

The private-nullity input is proved and independently audited in
[Private-nullity law for Hermitian PSD lifts of products of
balls](2026-09-04-hermitian-product-ball-private-nullity.md).  The closure,
spectral-projector, and relative-cup argument extends the independently
audited real proof in
[The divisible PSD product-ball gap closes beyond the one-channel
case](2026-09-04-psd-product-ball-divisible-topclass.md).

No claim is made for mixed fields in one formulation, unlabelled or merely
generic selections, arbitrary coupled barriers, infeasible methods, or
iteration complexity. The exact heterogeneous all-field statement is in
[the canonical sequential contact-range
frontier](2026-09-04-hermitian-sequential-contact-range-frontier.md).

## Audit checklist

- Check the factor \(\delta\) in (10) and the equality case over
  \(\mathbb C\) and \(\mathbb H\).
- Check the top-eigenline extension for quaternionic Hermitian matrices.
- Verify every global-cover exception in Section 3.
- Check that the relative cup product still works when source dimensions
  are heterogeneous and only the rows in \(E\) participate.
- Verify the direct \(H_+^2(\mathbb F)\) exception and grouped parameter
  count in (18).

An independent hostile audit passed.  It rederived the
\(\delta c\)-dimensional private channel and every equality condition,
including quaternionic rank-one spectral projectors viewed as real
self-adjoint projectors commuting with right scalar multiplication.  It
checked the complete projective-cover exception list, the heterogeneous
relative cup product when only rows in \(E\) participate, and the direct
and grouped parameter counts.  No mathematical correction was required.
The minimum in (5) is, as stated above, over lifts satisfying the global
\(C^1\) full-slack and boundary-closure hypotheses.

A second hostile audit independently checked the saturated private-row
equality over \(\mathbb C\) and \(\mathbb H\), including the real channel
dimension \(\delta(R-1)\), and reconstructed the local-diffeomorphism
obstruction
\(S^{q\delta(R-1)}\to(\mathbb F P^{R-1})^q\).  It also checked that the
relative top-class cover adds all obstructed divisible rows simultaneously,
not merely one row at a time.  It correctly isolates the real
one-projective-channel residues (7), which its projective topology cannot
exclude.  A later independent hostile audit of the sequential
contact-range theorem verified the compression and additive induction,
closing those residues as stated in (7a) and in the canonical all-field
companion, without strengthening the relative-top-class argument itself.
