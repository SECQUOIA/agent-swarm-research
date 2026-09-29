# Independent adversarial review of the quantitative Hölder bound

Date: 2026-09-27. Status: no unresolved mathematical gap found after one
required clarification to the multiplier system. This review supports the
candidate theorem in [the quantitative proof](hessian-span-holder-height-review.md).
It does not establish publication priority or replace the proofs of its
algebraic-witness and compressed-elimination dependencies.

## Claim checked

For a nonempty rational convex quadratic feasible set

\[
 F=\{x\in P:q_i(x)\le0\},\qquad
 h=\dim\operatorname{span}\{\nabla^2q_i\},
\]

where the rational polyhedron \(P\) contains an explicit coordinate box
in its description, the claim is

\[
 \operatorname{dist}(x,F)\le C\max(0,q_1(x),\ldots,q_m(x))^{2^{-h}}
 \quad(x\in P),
 \qquad \log_2\max(1,C)\le N^{O((h+1)^2)}.
\]

Here \(N\) is the total explicit binary input length, all Hessians are
positive semidefinite, and no strict-feasibility condition is assumed.
The same encoding conclusion holds on the input box when the residual
also includes the affine rows. The asserted constant is a uniform
effective upper bound, rather than a practically calibrated constant or
a constructed repair map.

I first checked the proposed arithmetic mechanism independently, then
read the saved quantitative proof and its
[terminal-margin audit](algebraic-slater-margin-review.md).

## A necessary active-row restriction

The multiplier system must explicitly impose

\[
 \lambda_i=0\qquad\text{whenever }q_i(x^*)<0.
\]

Equivalently, its native multiplier variables can be indexed only by
quadratic rows active at the fixed feasible point \(x^*\). Restricting
only the polyhedral normal multipliers to active rows is insufficient.
The proof needs both stationarity and \(g(x^*)=0\) for
\(g=\sum_i\lambda_iq_i\).

For a concrete failure, take \(P=[-1,1]^2\),
\(q_1(x,y)=y^2\), \(q_2(x,y)=x^2-1\), and \(x^*=0\).
Both rows are curved, the feasible set is \([-1,1]\times\{0\}\),
and there is no common strict point. The unrestricted normalized
stationarity system admits \(\lambda_1=0,\lambda_2=1\), since
both gradients vanish at zero. This choice has \(g(x^*)=-1\).
Its Hessian equation forces \(x=0\), discarding feasible points;
at the feasible point \((1,0)\), it also has
\(g(1,0)-g(0,0)=1>v(1,0)=0\). The correct choice
\(\lambda_1=1\) is available. Thus this is a repairable omission
in the system, not a counterexample to the theorem. The author supplied
this stronger two-dimensional version after I reported a one-dimensional
example of the missing activity condition; I independently checked it.

The author's surrounding explanation already intended this active-row
restriction. The saved correction now defines the active set \(I_q\),
indexes every native multiplier sum by that set, fixes unlisted native
multipliers to zero, and derives \(g(x^*)=0\) and \(g\ge0\)
for the newly chosen basic solution. I independently reread this correction
and found that it resolves the issue.

## Field and height checks

1. **One common field is essential.** The bound on
   \(K=\mathbb Q(x_1^*,\ldots,x_n^*)\) in
   [the witness note, Section 5](algebraic-witness-recovery.md#5-a-common-field-degree-bound)
   follows from a uniform algebraic-degree bound for every rational linear
   form in the coordinates, followed by the primitive element theorem.
   It is not inferred from separate coordinate degree bounds. This avoids
   a potentially exponential compositum degree.

2. **Affine preprocessing does not repeatedly enlarge heights.** When a
   row becomes affine on the current affine hull, use
   \(q_i(x^*)+\nabla q_i(x^*)^T(x-x^*)\) in the original
   coordinates. Its coefficients are fixed expressions in the original
   rational data and the one point \(x^*\). Up to \(m\) such
   replacements therefore do not create \(m\) rounds of determinant
   growth. All coefficients remain in \(K\).

3. **A bounded-height exposing multiplier exists in that field.** With
   the active native rows fixed, the normalized stationarity system is a
   nonempty linear system over \(K\) in nonnegative variables.
   Equality normals can be represented by opposite inequality rows. A
   feasible vector of minimal positive support has linearly independent
   supported columns; otherwise a dependence can remove one supported
   entry while preserving nonnegativity. Cramer's rule thus provides a
   solution over \(K\) using a square subsystem of order at most
   \(n+1\). Real feasibility does not require an extension field here.

4. **Determinants require a place-by-place estimate.** The bound
   \(H(\det M)\le r^3B+\log(r!)\) for entries of absolute
   logarithmic height at most \(B\) is valid and sufficient. At each
   place, bound the determinant by \(r!\) times the \(r\)-th
   power of the largest entry at archimedean places, and omit the
   factorial at non-archimedean places. Summing the local maxima is
   bounded by the sum of entry heights. Applying the elementary
   two-term height inequality separately to all \(r!\) terms would
   give an unnecessarily exponential and unusable estimate.

5. **At most \(h\) height-growth rounds occur.** With normalization
   \(\sum_i\lambda_i=1\), positive semidefiniteness and nonzero
   restricted Hessians imply that the exposing Hessian has nonzero
   restriction. Its minimizer face kills this member of the current
   Hessian span. Hence there are at most \(h\) curved reductions.
   A recurrence \(B_{j+1}\le N^c(B_j+B_*+1)\), with fixed
   \(c\), preserves \(N^{O(h+1)}\) height throughout.

6. **No normal-closure degree is hidden in coordinate conversion.** For
   a primitive \(\alpha\), the conjugate Vandermonde system
   expresses each \(\beta\in K\) as
   \(\sum_{r<D}c_r\alpha^r\). Its determinant ratios lie in
   \(\mathbb Q\). Absolute heights are invariant under the ambient
   number field, so bounding these ratios in a normal closure does not
   introduce that closure's degree. The resulting rational coefficient
   bit lengths are polynomial in \(D\), \(H(\alpha)\), and
   \(H(\beta)\).

The minimum-norm witness theorem is a substantive dependency. I checked
the specific common-field argument used here, but did not rerun its
algebraic-recognition algorithm or claim a new independent verification of
that algorithm.

## Hoffman and terminal-margin checks

The active-row proof of the Hoffman bound works for the possibly
irrational polyhedral rows. For a projection \(p\) and an independent
active row matrix \(M_J\), write
\(x-p=M_J^T\nu\), \(\nu\ge0\). If
\(r=\|(Mx-d)_+\|_\infty\), then

\[
 \|x-p\|^2\le\sqrt n\,\|\nu\|r,
 \qquad \|x-p\|\ge\sigma_{\min}(M_J)\|\nu\|.
\]

A nonsingular column minor and the adjugate formula therefore bound the
Hoffman constant. The inequalities
\(e^{-D H(a)}\le|a|\le e^{D H(a)}\) for nonzero \(a\in K\)
control every needed determinant and its inverse at the intended real
embedding. There is no need to count or enumerate the possible minors.

At the terminal face, minimize \(\max_i q_i(x)\) over the remaining
compact polyhedron. If rows remain, strict feasibility makes this optimum
negative. Epigraph introduction adds no Hessian dimension. The active
affine restriction and compressed KKT argument use linear algebra over
\(K\), and their bounded-size determinants have controlled height.
All field coefficients can be encoded using one primitive-root variable,
its minimal polynomial, and a rational isolating interval. That variable
can be put in the existing existential block. It neither introduces one
variable per coefficient nor changes the intended embedding.

I checked that the resulting formula has one free value coordinate and
quantifier blocks of sizes \(1\) and at most \(h+4\). Its degrees
and coefficient bit lengths are \(N^{O(h+1)}\). The
coefficient-sensitive block elimination bound therefore gives the claimed
\(N^{O((h+1)^2)}\) degree and height for the terminal margin. The
reciprocal Cauchy bound then controls its positive inverse. Direct
elimination in all original variables would not prove this parameter
bound.

Every intermediate projection remains in the original compact polyhedron.
The quadratic Lipschitz constants are thus controlled on one fixed box.
Affine repair steps multiply constants; each curved step changes the
residual power by a square root. For \(0\le\delta\le1\), the bound
\(v_j\le K_j\delta^{2^{-r}}\) remains usable even when
\(v_j>1\): both \(\sqrt{v_j}\) and \(v_j\) are bounded by
\((\sqrt{K_j}+K_j)\delta^{2^{-(r+1)}}\). Consequently there is
no hidden assumption that every intermediate residual is at most one.
The total number of steps is polynomial in \(N\), so multiplying
their constants preserves the stated logarithmic bound.

## Sources checked and limitations

I independently inspected [Basu's 2011 survey, Theorem 2.16, printed
p. 12](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf), including
its integer coefficient bit-size conclusion. I also inspected
[Silverman's 2024 Arizona Winter School notes, Definitions 4.4–4.5 and
Proposition 4.6, printed pp. 13–14](https://swc-math.github.io/aws/2024/2024SilvermanNotes.pdf).
These support the elimination and absolute-height ingredients, respectively;
they do not state the optimization theorem reviewed here.

The review found no counterexample to the quantitative theorem. It found
the explicit active-native-row restriction above necessary for the written
proof. No numerical computation or Lean formalization was used to certify
the universal statement. No project-wide checks or CI inspection were run.
Publication priority, practical calibration of constants, and efficient
construction of the facial-reduction sequence remain outside this review.
