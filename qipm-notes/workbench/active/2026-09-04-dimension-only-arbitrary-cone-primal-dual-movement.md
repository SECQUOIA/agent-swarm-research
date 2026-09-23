# Dimension-only movement lower bounds for arbitrary product-cone dictionaries

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the stated primal--dual, bounded-move result

## Main theorem

Let \(C\subset\mathbb R^D\) be a full-dimensional compact convex body and
consider any exact finite-dimensional affine lift of \(C\) over a product
of proper cones. Pass to the minimal operational face and omit zero
factors. Suppose every surviving factor has dimension at most \(d\geq2\).
No smoothness, curvature, symmetry, self-duality, definability, or regular
boundary-factor selection is assumed.

Define, for an integer \(h\geq2\),
\[
 h=a d+b,\qquad 0\leq b<d,\qquad
 \Psi_d(h):=2a+\min\{b,2\}.                              \tag{1}
\]
Then every, possibly coupled, logarithmically homogeneous self-concordant
barrier on the operational product cone has parameter
\[
                  \boxed{\nu\geq\Psi_d(D+1).}             \tag{2}
\]

Consequently, consider a strictly feasible primal--dual conic pair over
this operational cone. Let a trajectory start at an exact central point
of gap \(\Delta_0\), end at any strictly feasible primal--dual point of gap
at most \(\epsilon<\Delta_0\), and contain at most \(m\) chords per round,
each of starting product-Dikin norm at most \(R<1\). For every ambient
LHSC barrier,
\[
 \boxed{
 T\geq
 {\sqrt{\Psi_d(D+1)/2}\,\log(\Delta_0/\epsilon)
  \over m\log(1/(1-R))}.}                                 \tag{3}
\]

For a product of positive-dimensional Euclidean balls
\[
                       C=\prod_{j=1}^k B_2^{s_j},
\]
one has \(D=\sum_j s_j\). Thus every bounded-\(d\) product-cone
formulation, over an otherwise arbitrary cone dictionary, obeys
\[
 T=\Omega_{R,m}\!\left(
       \sqrt{{1+\sum_j s_j\over d}}
       \log{\Delta_0\over\epsilon}\right).                \tag{4}
\]
This is a genuine geometric movement lower bound, not an inference from a
barrier parameter upper bound or from the iteration count of a particular
IPM.

## 1. Ordinary slack rank forces \(D+1\) operational coordinates

Translate \(C\) so that \(0\in\operatorname{int}C\), and write its polar
as \(C^\circ\). Its normalized slack operator is
\[
                         S(x,y)=1-\langle x,y\rangle,
              \qquad x\in C,\quad y\in C^\circ.           \tag{5}
\]
The span of its columns as functions of \(x\) is exactly
\[
                      \operatorname{span}\{1,x_1,\ldots,x_D\}.
                                                                    \tag{6}
\]
Indeed \(y=0\) supplies the constant function, while the full
dimensionality of \(C^\circ\) supplies \(D\) linearly independent linear
parts. These affine functions are independent on the full-dimensional
set \(C\). Hence
\[
                         \operatorname{rank}S=D+1.         \tag{7}
\]

Relative Slater regularity after minimal-face reduction gives the usual
cone factorization
\[
        S(x,y)=\sum_{i=1}^{L}\langle A_i(x),B_i(y)\rangle,
        \qquad A_i(x)\in K_i,\quad B_i(y)\in K_i^*.        \tag{8}
\]
This bilinear factorization passes through the direct-sum vector space of
dimension
\[
                              M=\sum_i m_i,
                  \qquad m_i:=\dim K_i.                   \tag{9}
\]
Ordinary rank cannot increase through that space, so
\[
                              D+1\leq M.                  \tag{10}
\]
This is the only formulation lower bound used below. In particular, it
does not require differentiating a selected boundary factorization.

## 2. Cone coordinates force barrier parameter

Let \(r\) be the number of one-dimensional ray factors and \(q\) the
number of factors of dimension at least two. In each non-ray factor
choose a two-dimensional linear subspace through an interior point. Its
intersection with the factor is a two-dimensional proper cone and is
therefore linearly isomorphic to \(\mathbb R_+^2\). A ray factor is
already \(\mathbb R_+\). The product of these sections is an interior
section isomorphic to
\[
                              \mathbb R_+^{\,r+2q}.        \tag{11}
\]

Restriction of a coupled \(\nu\)-LHSC barrier to this section preserves
self-concordance, logarithmic homogeneity with the same coefficient, and
barrier blow-up at every relative-boundary point. Since the sharp LHSC
parameter of an orthant is its dimension,
\[
                              \nu\geq r+2q.                \tag{12}
\]
On the other hand, the dimension cap and (10) give
\[
                              D+1\leq r+dq.                \tag{13}
\]

It remains only to solve this two-variable integer packing problem. Put
\(h=D+1=ad+b\), \(0\leq b<d\). Using \(a\) full non-ray blocks costs
\(2a\); a residual capacity of one costs one ray, while a residual capacity
of at least two costs one further non-ray block. Conversely no factor of
barrier charge one carries more than one coordinate and no factor of
charge two carries more than \(d\). Therefore
\[
 \min\{r+2q:r,q\in\mathbb Z_+,\ r+dq\geq h\}
       =2a+\min\{b,2\}=\Psi_d(h),                         \tag{14}
\]
which proves (2).

The formula retains the small integer residues that the asymptotic bound
loses. In particular,
\[
                 \Psi_d(h)\geq {2h\over d},
                                                                    \tag{15}
\]
because \(\min\{b,2\}\geq2b/d\); exact multiples satisfy
\(\Psi_d(h)=2h/d\).

## 3. Primal--dual movement consequence

For an arbitrary \(\nu\)-LHSC barrier \(F\) and its conjugate \(F_*\), put
\[
                         \widehat F(x,s)=F(x)+F_*(s).      \tag{16}
\]
The Nesterov--Todd endpoint-set theorem gives, from an exact central point
of gap \(\Delta_0\),
\[
 \operatorname{dist}_{\widehat F}
 \bigl(z(\Delta_0),\{z:\operatorname{gap}(z)\leq\epsilon\}\bigr)
 \geq\sqrt{\nu/2}\log(\Delta_0/\epsilon).                 \tag{17}
\]
Each chord of starting local norm at most \(R<1\) has Riemannian length at
most \(\log(1/(1-R))\). Combining (2) and (17) proves (3).

Intermediate chords may leave the affine primal--dual equations; the
endpoint must be a strictly feasible primal--dual gap certificate. The
argument allows arbitrary computation, quantum or classical, between
chords. It does not lower-bound oracle queries, long steps, a primal-only
trajectory, a normalized state output, or a scalar objective estimate.

## 4. Relation to the sharper curvature theorem

For one body with a positively curved smooth boundary point and definable
cone factors, the differential curvature theorem strengthens the factor
capacity from \(m_i\) to \(m_i-2\). It gives
\[
 \nu\geq2\left\lceil{D-1\over d-2}\right\rceil,           \tag{18}
\]
which is usually sharper than (2). The present theorem has three
compensating advantages:

1. it needs no regularity or definability assumptions;
2. it applies to every full-dimensional compact convex body; and
3. it sees the full dimension \(\sum_j s_j\) of a product of balls, whose
   boundary is not strictly positively curved as a product.

For fixed \(d\), both results have the same square-root order on a single
high-dimensional ball. On a product body, (4) supplies the direct
arbitrary-dictionary dependence on every source dimension.

## 5. Provenance and novelty boundary

This section records a targeted, non-exhaustive primary-source screen
through 2026-09-04. It is not a novelty opinion.

The slack-factorization step is classical. Gouveia, Parrilo, and Thomas,
“Lifts of Convex Sets and Cone Factorizations,” *Mathematics of Operations
Research* 38 (2013), Theorem 2.4
([arXiv](https://arxiv.org/abs/1111.3164),
[publisher](https://doi.org/10.1287/moor.1120.0575)), prove the equivalence
between a proper \(K\)-lift and a \(K\)-factorization of the slack operator.
The use here first replaces a non-Slater lift by its minimal operational
face and then applies the proper-lift direction relative to that face. The
ordinary affine rank \(D+1\), and the implication \(D+1\leq\sum_i m_i\),
are elementary consequences of that factorization; they are not proposed
as new lift lower bounds.

The barrier ingredients are also classical. Restriction of a barrier to a
linear section is standard barrier calculus. Sharpness of the orthant
parameter is a basic case of the lower-bound theory for logarithmically
homogeneous self-concordant barriers; see, for example, Güler and Tunçel,
“Characterization of the Barrier Parameter of Homogeneous Convex Cones,”
*Mathematical Programming* 81 (1998), 55--76, and Hildebrand, “A Lower
Bound on the Barrier Parameter of Barriers for Convex Cones,”
*Mathematical Programming* 142 (2013)
([open manuscript](https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf),
[publisher](https://doi.org/10.1007/s10107-012-0576-1)). The present proof
uses one orthant section of the whole product, so it remains valid for a
barrier that couples the product factors; it is not an appeal to an
unproved additivity rule for optimal parameters.

The movement conversion is an extraction from Nesterov and Todd, “On the
Riemannian Geometry Defined by Self-Concordant Barriers and Interior-Point
Methods,” *Foundations of Computational Mathematics* 2 (2002)
([author manuscript](https://people.orie.cornell.edu/miketodd/NTRiemann.pdf),
[publisher](https://doi.org/10.1007/s102080010032)). Definition 3.1,
Lemma 3.2, and Corollary 3.2 give the exact bounded-Dikin-chord length
conversion. Theorem 5.1(c) and the primal--dual product geometry behind
Theorem 5.2 give the endpoint-set/gap estimate used in (17). Thus neither
the denominator in (3) nor the \(\sqrt{\nu/2}\) Riemannian ingredient is
claimed as new.

The closest formulation lower bounds found have different scopes.
Fawzi and Parrilo, “Exponential Lower Bounds on Fixed-Size PSD Rank and
Semidefinite Extension Complexity”
([arXiv](https://arxiv.org/abs/1311.2571)), prove strong block-count lower
bounds for particular polytopes lifted over products of fixed-size PSD
cones. Saunderson, “Limitations on the Expressive Power of Convex Cones
Without Long Chains of Faces”
([arXiv](https://arxiv.org/abs/1902.06401)), obstructs product lifts whose
factor cones have short face chains when the source cone satisfies a
neighborliness hypothesis. These are much stronger for their hard
families, but neither states a universal dimension-only lower bound for
every full-dimensional compact body, converts an orthant-section charge
into an LHSC parameter, or derives bounded-Dikin primal--dual movement.
Conversely, Lee and Yue, “Universal Barrier is \(n\)-Self-Concordant”
([arXiv](https://arxiv.org/abs/1809.03011)), is a sharp dimension-dependent
*upper* bound for arbitrary convex domains, not a lift or movement lower
bound.

No primary source was located in this targeted screen that explicitly
combines slack rank \(D+1\), a cap \(m_i\leq d\), the orthant-section lower
bound \(\nu\geq r+2q\), the exact integer envelope
\(\Psi_d(D+1)\), and Nesterov--Todd distance to obtain (3), including the
product-body corollary (4). The conservative label is therefore:

> Apparently unlocated exact synthesis of classical ingredients; modest
> standalone novelty, with the main useful feature being its uniformity
> over arbitrary compact full-dimensional bodies, arbitrary proper-cone
> dictionaries under a block-dimension cap, and coupled LHSC barriers.

This negative search does not establish priority. In particular, (2) is
a lower bound for barriers on the **operational product cone**, not for an
arbitrary barrier written directly on the projected body or lift slice;
(3) needs the stated primal--dual endpoint/gap contract and bounded local
chords; and the theorem does not lower-bound oracle queries or algorithms
that take unrestricted long moves.

## 6. Independent hostile audit

The audit verified the ordinary slack-rank argument after arbitrary
minimal-operational-face reduction, including free variables, nonexposed
faces, zero factors, and surviving rays. It checked that every surviving
non-ray proper factor has a two-dimensional linear section meeting its
relative interior, that retaining all ray coordinates makes the product
section an interior orthant section, and that restriction of a coupled
LHSC barrier preserves self-concordance, logarithmic homogeneity with the
same coefficient, and boundary blow-up.

The integer minimization was checked separately for \(d=2\), zero and
one-coordinate residues, and all larger residues:
\[
 \min\{r+2q:r+dq\geq h,\ r,q\in\mathbb Z_+\}
 =2\lfloor h/d\rfloor+\min\{h\bmod d,2\}.
\]
Finally, the audit verified the exact Nesterov--Todd factor
\(\sqrt{\nu/2}\), the bounded-chord denominator in (3), and the fact that
no differentiable or definable factor selection is used. No mathematical
correction was required.
