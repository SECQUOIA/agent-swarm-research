# Sequential compression gives the exact Hermitian contact-range frontier

Status: Proved; fixed-field and mixed-dictionary theorems independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

Fix \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\), put
\(\delta=\dim_{\mathbb R}\mathbb F\), and fix a Hermitian PSD order cap
\(R\geq2\).  Define

\[
 B=\delta(R-1),\qquad
 \kappa_{\mathbb F,R}(s)=
 \begin{cases}
  1,&R=2,\ s=\delta+1,\\
  \left\lceil s/B\right\rceil,&\text{otherwise}.
 \end{cases}                                                \tag{1}
\]

Let

\[
                         C=\prod_{a=1}^hB_2^{s_a},
                         \qquad s_a\geq2,                   \tag{2}
\]

and suppose its full extreme-row slack family has a finite globally
bi-\(C^1\) factorization

\[
 1-x_a^Tz=\sum_{i=1}^L
       \operatorname {Re}\operatorname {tr}
          \bigl(X_i(x)Y_i^a(z)\bigr),
 \quad X_i,Y_i^a\in H_+^{r_i}(\mathbb F),\quad r_i\leq R.  \tag{3}
\]

Then there is a simultaneous contact
\(u=(u_1,\ldots,u_h)\) such that, for every choice of positive weights
\(\lambda_a\),

\[
 \boxed{
 \sum_i\operatorname {rank}_{\mathbb F}
       \left(\sum_a\lambda_aY_i^a(u_a)\right)
 \geq\sum_{a=1}^h\kappa_{\mathbb F,R}(s_a).}              \tag{4}
\]

This is an additive exposed-dual-rank theorem.  It holds without a
constant-rank assumption, without a persistent source-to-label assignment,
and without an affine-lift or Slater hypothesis.

If the row factors are genuine affine-slice dual certificates, the
exposed-rank Dikin theorem turns (4) into a path-independent standard
log-determinant distance coefficient at least

\[
              \sqrt{\sum_a\kappa_{\mathbb F,R}(s_a)}
                    \quad\text{in front of }\log(1/\epsilon),          \tag{5}
\]

for the support objective selected by \(u\).  The exact finite spectral
scale is the reference-minor constant in that theorem.

At the same contact,

\[
 \sum_i\operatorname {nullity}_{\mathbb F}X_i(u)
       \geq\sum_a\kappa_{\mathbb F,R}(s_a).               \tag{6}
\]

Consequently, if the selected boundary tuple belongs to the closure of a
strictly feasible affine slice carrying the restricted standard product
log-determinant, then

\[
 \boxed{\nu_{\rm std,slice}\geq
       \sum_a\kappa_{\mathbb F,R}(s_a).}                  \tag{7}
\]

Grouped Hermitian Schur epigraphs attain (7), with the direct trace-one
rank-two spin slice used in the exceptional first line of (1).  Hence (7)
is the exact additive standard-slice frontier.  For
\(\mathbb F=\mathbb R\), it closes the former one-projective-channel gap;
for \(\mathbb C,\mathbb H\), it gives a shorter proof of the known exact
frontier and strengthens it to the exposed-rank movement statement (4).

## 1. The sharp one-ball contact-range lemma

The induction rests on a factorization theorem that is useful in its own
right.

> **Lemma 1.**  Suppose
> \[
>  1-u^Tv=\sum_i\operatorname {Re}\operatorname {tr}
>                 \bigl(A_i(u)B_i(v)\bigr),
> \quad A_i,B_i:S^{s-1}\to H_+^{n_i}(\mathbb F),
> \quad n_i\leq R,                                      \tag{8}
> \]
> is globally bi-\(C^1\).  Then some \(v\in S^{s-1}\) satisfies
> \[
>             \sum_i\operatorname {rank}_{\mathbb F}B_i(v)
>                         \geq\kappa_{\mathbb F,R}(s).    \tag{9}
> \]

Put \(p=s-1\) and
\(Q(v)=\sum_i\operatorname {rank}_{\mathbb F}B_i(v)\).
At diagonal contact, PSD complementarity and the real mixed-channel rank
bound give

\[
 p\leq\sum_i\delta\,\operatorname {rank}_{\mathbb F}A_i(v)
                         \operatorname {rank}_{\mathbb F}B_i(v)
   \leq BQ(v).                                           \tag{10}
\]

Thus \(Q(v)\geq\lceil p/B\rceil\).  If \(B\nmid p\), then
\(\lceil p/B\rceil=\lceil s/B\rceil\), so (9) follows.  It remains to
consider

\[
                         p=qB,\qquad q\geq1.              \tag{11}
\]

Assume \(Q(v)\leq q\) for every \(v\).  Equation (10) makes
\(Q(v)=q\) everywhere.  Each individual dual rank is lower
semicontinuous, and their finite sum is constant on the connected sphere,
so every rank is constant.  For a nonzero block, equality in

\[
\begin{split}
 qB
 &\leq\sum_i\delta\,p_iq_i\\
 &\leq\sum_i\delta\,(R-q_i)q_i
 \leq\delta(R-1)\sum_iq_i=qB                         \tag{12}
\end{split}
\]

forces

\[
              q_i=1,\qquad n_i=R,\qquad p_i=R-1,          \tag{13}
\]

and full real mixed rank \(B\).  A zero-rank dual factor vanishes
identically.  The \(q\) rank-one dual support maps therefore assemble into
a same-dimensional local diffeomorphism

\[
        S^{q\delta(R-1)}
             \longrightarrow\bigl(\mathbb F P^{R-1}\bigr)^q.          \tag{14}
\]

Compactness makes (14) a finite covering.  If \(q>1\), this is impossible:
for \((\mathbb F,R)=(\mathbb R,2)\) the target is a torus with noncompact
universal cover; in every other real case its universal cover is a product
of at least two spheres; and complex or quaternionic projective products
have nonzero intermediate cohomology.

If \(q=1\), complex and quaternionic projective space has a sphere
universal cover only at \(R=2\), giving respectively
\(\mathbb CP^1=S^2\) and \(\mathbb HP^1=S^4\).  For
\(\mathbb F=\mathbb R\), the universal sphere cover of
\(\mathbb RP^{R-1}\) is topologically possible for every \(R\), but the
independently audited even-quadratic full-slack theorem excludes the sole
order-\(R\) factor when \(R\geq3\).  The only survivors are therefore

\[
                         q=1,\qquad R=2,\qquad s=\delta+1.             \tag{15}
\]

They are genuine: \(H_+^2(\mathbb F)\) is the spin factor
\(Q_{\delta+2}\), and its trace-one slice gives the direct ball
factorization with one dual contact-range dimension.  Outside (15), the
integer \(Q(v)\) is at least \(q+1=\lceil s/B\rceil\) somewhere.  This
proves Lemma 1.

## 2. Sequential compression

Choose the contacts \(u_1,\ldots,u_h\) successively.  After choosing the
first \(a-1\), put

\[
 W_i^{a-1}=\sum_{d<a}\operatorname {Ran}_{\mathbb F}Y_i^d(u_d),
 \qquad
 P_i^{a-1}=P_{(W_i^{a-1})^\perp}.                         \tag{16}
\]

Fix arbitrary values of the future primal coordinates and vary only
\(x_a=u\).  Every earlier row \(d<a\) remains at diagonal contact, so
termwise nonnegativity gives

\[
                   W_i^{a-1}\subseteq\ker X_i(x)
                \quad\text{for every value of }u.         \tag{17}
\]

The spaces in (16) are \(\mathbb F\)-linear.  Restricting to their
orthogonal complements gives Hermitian PSD maps

\[
\begin{split}
 A_i^{(a)}(u)&=X_i(x)|_{(W_i^{a-1})^\perp},\\
 B_i^{(a)}(v)&=
   \left(P_i^{a-1}Y_i^a(v)P_i^{a-1}\right)
                        |_{(W_i^{a-1})^\perp}.            \tag{18}
\end{split}
\]

They are globally bi-\(C^1\), have orders at most \(R\), and factor the
exact one-ball slack.  Indeed, (17) gives \(X_i=P_iX_iP_i\), so cyclicity
of the real trace yields

\[
 1-u^Tv=\sum_i\operatorname {Re}\operatorname {tr}
                  \bigl(A_i^{(a)}(u)B_i^{(a)}(v)\bigr).   \tag{19}
\]

Lemma 1 supplies \(u_a\) such that

\[
        \sum_i\operatorname {rank}_{\mathbb F}B_i^{(a)}(u_a)
                    \geq\kappa_{\mathbb F,R}(s_a).        \tag{20}
\]

Update

\[
             W_i^a=W_i^{a-1}
                   +\operatorname {Ran}_{\mathbb F}Y_i^a(u_a).        \tag{21}
\]

For Hermitian PSD \(Y=CC^*\) and the orthogonal projection
\(P=P_{W^\perp}\),

\[
\begin{split}
 \operatorname {rank}_{\mathbb F}(PYP)
 &=\operatorname {rank}_{\mathbb F}(PC)\\
 &=\dim_{\mathbb F}(W+\operatorname {Ran}_{\mathbb F}Y)
                         -\dim_{\mathbb F}W.              \tag{22}
\end{split}
\]

Thus (20) is exactly the new range dimension added at step \(a\).
Telescoping gives

\[
                         \sum_i\dim_{\mathbb F}W_i^h
                 \geq\sum_a\kappa_{\mathbb F,R}(s_a).     \tag{23}
\]

Changing future coordinates never invalidates an earlier range inclusion:
the cylindrical identity (17) held for all their values.  At the final
simultaneous contact, every row is diagonal, so
\(W_i^h\subseteq\ker X_i(u)\).  This proves (6).

For positive weights, PSD range additivity gives

\[
 \operatorname {Ran}_{\mathbb F}
      \left(\sum_a\lambda_aY_i^a(u_a)\right)=W_i^h.        \tag{24}
\]

Equations (23)--(24) prove the exposed-rank statement (4).

## 3. Barrier consequences and attainment

If the weighted row factors in (24) are genuine affine-slice dual
certificates, their sum exposes the simultaneous support objective.
The path-independent exposed-rank theorem applied with (4) gives (5).
This conclusion permits arbitrary feasible lifted paths and does not
require a central-path neighborhood.

If the selected primal tuple lies in the closure of one relative-Slater
affine slice, the determinant of block \(i\) vanishes along an
interior-point segment to exact order
\(\operatorname {nullity}_{\mathbb F}X_i(u)\).  The one-dimensional
barrier-gradient inequality and (6) give (7).

For attainment, partition the \(s_a\) real coordinates of each source
into groups of size at most \(B=\delta(R-1)\).  Embed every group
real-isometrically in \(\mathbb F^{R-1}\) and use the Schur block

\[
                 \begin{pmatrix}t_G&w_G^*\\w_G&I_{R-1}\end{pmatrix}
                    \succeq0,\qquad \sum_{G\ {\rm in\ row}\ a}t_G=1.
                                                               \tag{25}
\]

The restricted determinant is \(t_G-\|w_G\|^2\), so the standard barrier
has exact parameter one per group.  This uses
\(\lceil s_a/B\rceil\) blocks for row \(a\).  In the exceptional case
\(R=2,s_a=\delta+1\), use instead the direct trace-one slice of
\(H_+^2(\mathbb F)\), with exact restricted parameter one.  Summing over
sources attains the right side of (7).  Each Schur group has a rank-one
dual contact factor, as does the direct spin slice, so the same
constructions attain equality in the factorization bound (4).

## 4. Mixed Hermitian dictionaries

The argument is not limited to one field.  Let an allowed dictionary
\(\mathcal D\) contain real, complex, or quaternionic Hermitian PSD block
types, and put

\[
 K=\max_{(\mathbb F_i,R_i)\in\mathcal D}
       \delta_i(R_i-1),\qquad
       \delta_i=\dim_{\mathbb R}\mathbb F_i.              \tag{26}
\]

Assume every lift factor has one of these types, with order no larger than
the corresponding \(R_i\).  Define

\[
 \kappa_{\mathcal D}(s)=
 \begin{cases}
  1,&s=K+1\text{ and }\mathcal D\text{ contains }
       H_+^2(\mathbb F)\text{ with }\dim_{\mathbb R}\mathbb F=K,\\
  \lceil s/K\rceil,&\text{otherwise}.
 \end{cases}                                               \tag{27}
\]

Then the simultaneous-contact conclusions (4) and (6) remain valid with
\(\sum_a\kappa_{\mathcal D}(s_a)\) on the right.

Indeed, the one-ball local bound is
\[
                         s-1\leq KQ.                       \tag{28}
\]
Only the divisible case can miss \(\lceil s/K\rceil\).  Equality makes
every active dual rank one and every active block attain
\(\delta_i(R_i-1)=K\).  The joint rank-one support map is a
same-dimensional covering from the source sphere to a product of the
corresponding real, complex, or quaternionic projective spaces.  With at
least two factors, fundamental groups or intermediate cohomology exclude
the covering.  With one factor, complex and quaternionic projective spaces
are spheres only at order two, while the real higher-order case is
excluded by the even-quadratic sole-factor theorem.  The sole surviving
case is exactly the direct spin exception in (27).

Sequential compression is performed separately in each block over its own
field.  Quaternionic, complex, and real range increments are all counted
in their native ranks and then added as integers, so no cross-field vector
space is required.  If arbitrary repetitions of a type attaining \(K\)
are allowed, grouped Schur blocks of that type attain
\(\lceil s_a/K\rceil\) for every nonexceptional source, and the direct
rank-two block attains the exceptional value.  Thus

\[
        \nu_{\rm std,slice}^{\min}
             =\sum_a\kappa_{\mathcal D}(s_a)              \tag{29}
\]

for the mixed dictionary under the same global-selection and affine-slice
hypotheses.  The corresponding aggregate exposed-rank lower bound is again
the stronger bare factorization statement.

## 5. Scope and novelty boundary

The factorization theorem (4) needs finite globally labelled bi-\(C^1\)
Hermitian PSD factors and the order cap.  The Dikin consequence additionally
requires genuine affine-slice dual certificates.  The standard-barrier
consequence additionally requires a common relative-Slater slice and
boundary closure.  No claim is made for unlabelled lifts, arbitrary custom
barriers, infeasible methods, or unrestricted quantum query complexity.

The one-ball projective obstruction and grouped constructions are
independently audited in
[The exact Hermitian PSD standard-slice barrier frontier for a Euclidean
ball](2026-09-04-hermitian-psd-standard-slice-barrier-frontier.md).
The sequential quotient idea first appeared in the real one-channel
closure
[Sequential range compression closes the real PSD one-channel
residue](2026-09-04-q1-sequential-range-compression-closure.md).

### Primary-source screen through 2026-09-04

The PSD lift/factorization framework is classical; see Gouveia, Parrilo,
and Thomas, “Lifts of Convex Sets and Cone Factorizations”
([arXiv](https://arxiv.org/abs/1111.3164),
[publisher](https://doi.org/10.1287/moor.1120.0575)). More importantly,
the **compression mechanism has a close published antecedent**. Theorem
2.10 of Fawzi, Gouveia, Parrilo, Robinson, and Thomas, “Positive
Semidefinite Rank,” *Mathematical Programming* 153 (2015)
([arXiv](https://arxiv.org/abs/1407.4095),
[publisher](https://doi.org/10.1007/s10107-015-0922-1)), proves

\[
 \operatorname{rank}_{\rm psd}
 \begin{pmatrix}P&0\\Q&S\end{pmatrix}
 \geq \operatorname{rank}_{\rm psd}(P)+
      \operatorname{rank}_{\rm psd}(S).
\]

Its proof spans the ranges of the column factors paired with the zero
block, puts the corresponding row factors in the orthogonal complement,
and compresses the two diagonal subproblems to complementary subspaces.
This is the same linear-algebraic motif as (16)--(23). Orthogonal range
compression and telescoping additivity should therefore not be presented
as a new general PSD-factorization technique.

The local theorem is nevertheless not an instance of that matrix result.
Theorem 2.10 concerns a finite block-triangular nonnegative matrix, one
real PSD cone of variable order, and the minimum ambient factorization
size. Here no block-triangular slack matrix is supplied: the proof chooses
one contact on each smooth ball sphere, preserves the full cylindrical
slack identity under later choices, reapplies a sharp one-ball contact
lemma after every compression, and concludes the rank of **one positive
weighted sum of dual contact certificates** in each member of a capped
product of cones. This quantity is not ordinary PSD rank. The published
compression proof extends algebraically to complex or quaternionic
Hermitian matrices, but the exact constants and exception list in (1) do
not appear there.

Other nearby formulation measures answer different questions:

- Fawzi--Parrilo's fixed-size block-PSD lower bounds
  ([arXiv](https://arxiv.org/abs/1311.2571)) count how many fixed real PSD
  blocks are needed for particular hard polytopes. They do not select a
  simultaneous smooth contact or lower-bound the rank of a summed exposing
  certificate.
- Fawzi's SOC nonrepresentability theorem
  ([publisher](https://doi.org/10.1007/s10107-018-1233-0)) decomposes SOC
  product factorizations into summands and uses zero-pattern
  combinatorics. It gives no field-uniform ball contact-range frontier.
- Semidefinite extension degree, as developed by Averkov and used by
  Scheiderer
  ([arXiv](https://arxiv.org/abs/2004.04196),
  [publisher](https://doi.org/10.1137/20M133717X)), minimizes the largest
  real PSD block while allowing arbitrarily many blocks. It deliberately
  forgets precisely the additive block/rank charge measured by (4) and
  (7).
- Kummer, “Two Results on the Size of Spectrahedral Descriptions”
  ([arXiv](https://arxiv.org/abs/1506.07699),
  [publisher](https://doi.org/10.1137/15M1030789)), proves matrix-order
  lower bounds for a **direct real spectrahedral description** of a ball
  or other quadratic body. It does not treat projected products,
  Hermitian fields, contact ranges, or restricted barrier parameters.

Fawzi and Safey El Din, “A Lower Bound on the Positive Semidefinite Rank
of Convex Bodies”
([arXiv](https://arxiv.org/abs/1705.06996),
[publisher](https://doi.org/10.1137/17M1142570)), lower-bound the order of
a real PSD lift through the algebraic degree of the polar boundary. A ball
has a quadratic boundary, so this general algebraic-degree method does not
yield the additive capped-block frontier here. Soh and Varvitsiotis,
“Multiplicative Updates for Symmetric-Cone Factorizations”
([publisher](https://doi.org/10.1007/s10107-023-02015-6)), develop
algorithms for finite-matrix factorizations over arbitrary symmetric
cones, while Brown, Pashkovich, and Tunçel
([arXiv](https://arxiv.org/abs/2501.03025)) study normalization of cone
factorizations and consequences for extension complexity. Neither source
was found to contain a smooth ball-slack contact-capacity or
standard-slice theorem.

Complex PSD rank is established terminology in the 2015 PSD-rank paper
and later work such as Bogart, Gouveia, and Torres, “Complex PSD-Minimal
Polytopes in Dimensions Two and Three”
([arXiv](https://arxiv.org/abs/2110.08158),
[publisher](https://doi.org/10.1142/S0219498824500257)). Those sources
study minimum Hermitian matrix order for polytopal lifts. Quaternionic
Hermitian PSD cones are, of course, classical symmetric cones; what was
not located is a quaternionic **PSD-rank/lift invariant** developed in
parallel with complex PSD rank, or any source with the all-field
smooth-ball capacity \(\delta(R-1)\), projective exception list, and
additive simultaneous-contact conclusion in (4).

On the barrier side, the standard Jordan log-determinant and its optimal
parameter on the **full** Hermitian PSD cone are classical; see Cardoso
and Vieira, “On the Optimal Parameter of a Self-Concordant Barrier over a
Symmetric Cone”
([open manuscript](https://optimization-online.org/wp-content/uploads/2003/11/774.pdf),
[publisher](https://doi.org/10.1016/j.ejor.2004.11.027)). The
ball barrier \(-\log(1-\lVert x\rVert^2)\), whose gradient parameter is
one under the convention used here, is also classical. Affine restriction
of log-determinant and the factorwise additive upper bound are standard
barrier calculus. These facts do not determine the smallest gradient parameter of
the standard product log-determinant **after an arbitrary lifted
affine-slice restriction**. No primary source was located with the exact
frontier (7), including the real/complex/quaternionic constants and the
three order-two spin exceptions.

The conservative novelty label is therefore:

> The range-compression motif is published prior art. Apparently
> unlocated are the sharp field-uniform one-ball contact lemma, its
> sequential use to select a simultaneous product-ball contact with the
> additive weighted exposed-rank guarantee (4), and the consequent exact
> all-field standard-slice frontier (7). These are candidate derived
> theorems under strong global bi-\(C^1\)/labelling and slice hypotheses,
> not unconditional PSD-rank or semidefinite-extension lower bounds.

This was a targeted, non-exhaustive primary-source screen, not a priority
opinion. Separate expert review is warranted in quaternionic convex
optimization and in the topology of smooth PSD factorizations.

## Hostile-audit checklist (completed)

1. Recheck the ceiling arithmetic and the complete exception list in
   Lemma 1.
2. Verify equality in (12), including complex/quaternionic real channel
   dimensions and rank-changing labels.
3. Check every topology case in (14), and exact applicability of the real
   even-quadratic theorem.
4. Verify \(\mathbb F\)-linear compression, real-trace cyclicity, and
   (22) for singular quaternionic PSD matrices.
5. Check telescoping, final weighted range equality, and the distinction
   between factorization, Dikin, and standard-slice scopes.
6. Verify the grouped Schur and direct-spin attainment counts.

## Independent hostile audit

The audit rederived the one-ball lower bound and checked the ceiling
arithmetic in every residue class. When the local bound is saturated,
lower semicontinuity of the finitely many labelled dual ranks and constancy
of their sum make every rank locally constant. Equality in all mixed-channel
bounds then forces \(q\) order-\(R\), complementary-rank
\((R-1,1)\) blocks and a same-dimensional projective-space covering.
The product-cover obstructions and the complete direct exceptions
\(R=2,\ s=\delta+1\) were checked separately over
\(\mathbb R,\mathbb C,\mathbb H\), including applicability of the real
even-quadratic full-slack obstruction.

The audit also verified that each accumulated \(W_i^a\) is an
\(\mathbb F\)-linear subspace, real-trace cyclicity preserves the exact
compressed slack identity, and for singular quaternionic PSD matrices
\(Y=CC^*\),
\[
 \operatorname{rank}_{\mathbb H}(PYP)
 =\operatorname{rank}_{\mathbb H}(PC)
 =\dim_{\mathbb H}(W+\operatorname{Ran}_{\mathbb H}Y)-\dim_{\mathbb H}W.
\]
Thus the rank increments telescope exactly. Positive weighted PSD sums
have kernel equal to the intersection of the individual kernels, so their
range is precisely \(W_i^h\); the contact selected by the induction works
for every positive weight vector.

Finally, the audit checked the scope separation: (4) is a bare
factorization theorem, (5) additionally needs genuine affine-slice dual
certificates, and (7) additionally needs closure of one relative-Slater
slice. The grouped Schur blocks and the direct trace-one rank-two spin
slices attain the stated standard-barrier values. No mathematical
correction was required.

The mixed-dictionary extension (26)--(29) passed a further hostile audit.
Equality in the local bound forces every productive label to have dual
rank one, full allowed order, and capacity
\(\delta_i(R_i-1)=K\). The resulting mixed product of projective spaces
has no sphere finite cover when more than one label is active. With one
label, the only surviving cases are precisely the order-two
\(\mathbb R,\mathbb C,\mathbb H\) spin factors in (27); the real
higher-order possibility is excluded by the same even-quadratic
full-slack theorem. Blockwise compression and rank increments remain in
each block's native field, so they sum without any cross-field
identification. The exact upper formula (29) is correctly conditional on
the dictionary allowing arbitrary repetitions of a type attaining \(K\).
No correction was required.
