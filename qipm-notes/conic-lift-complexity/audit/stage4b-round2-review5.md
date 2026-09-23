# Stage 4B, second independent review 5

I read all of `09a-whole-rows.tex` through `09e-spectral-chordal.tex`,
the root assessment and correction audit, and the relevant universal
contact and joint-cover dependencies. I did not consult other reviewers'
reports or edit the manuscript.

**Finding: no major or minor issues identified.** The substantive
correction is valid, and its consequences have been propagated correctly.

## The revised sharing arguments

In Theorem `thm:face-sharing-local` and Proposition
`prop:spectral-contact`, an active row has nonzero primal and dual contact
factors. Pairing with its fixed dual factor has a local minimum zero on
the entire primal source manifold. Thus this factor annihilates every
primal derivative, including derivatives associated with other rows.
The rank-detecting subspaces for distinct active rows, together with the
primal ray, form a direct sum by the cross-contact identities. They lie
in this one common hyperplane. Its dimension is `m_i-1`, proving the
corrected total bound `sum_a t_i^a <= m_i-2`. The argument uses only
first derivatives and does not require equal primal/polar manifold
dimensions or symmetric spectral mixed forms. The complementary-face
inequalities and active-row incidence bounds are compatible with this
stronger total bound.

For Theorem `thm:face-sharing-global`, summing the labelled dual maps
produces a genuine cone-valued C1 factorization of the joint kernel on
two copies of the product of spheres. The contact map is the identity
and the mixed pairing is nondegenerate. At `R=kp`, all hypotheses of
Theorem `thm:general-joint-cover` hold. Its product-sphere conclusion
forces capacities equal to `p`, so the strict cap excludes equality.
The resulting integer lower bound `R>=kp+1` is valid. Zero-capacity
factors do not change this application. I also checked the compact
active-piece argument for the independently retained incidence and
face-weighted capacity budgets.

The stated `R_*` combines the capacity premium and the face-weighted
capacity budget. The stated `L_*` combines the incidence bound and
`R<=cL`. Hence `D>=R_*+2L_*` follows without assuming that the two
resource lower bounds are simultaneously attainable. The arbitrary
ambient-barrier lower bound follows by restriction to product wedge
sections. The specialization to face cap one recovers the exact
ray-exposed frontier. The integer dimension-cap conventions are now
explicit in 09b, 09d, and 09e.

## Spectral and completion checks

I independently computed the contact pairing at `X=(I_r,0)` and
`Z=e_1e_1^*`. The skew-Hermitian first-column channels contribute
`delta(r-1)`, the rectangular tail contributes `delta(c-r)`, and the
imaginary diagonal contributes `delta-1`. This gives `delta c-1`,
including the quaternionic phase directions and the zero-rank real
scalar case. Summing the corrected block totals proves the unweighted
capacity inequality in `eq:spectral-summed-budgets`. Both ceilings in
the displayed factor-count consequence follow from the stated budgets.

For whole spectral rows, equality in spectral/nuclear duality leaves a
complementary `(r-h)` by `(c-h)` contraction. This verifies both the
rank-one contact codimension and the maximum exposed-face formula.
The grouped spectral barrier is the restriction of the classical
block-diagonal spectral-cone barrier. Its logarithmic degree is
`R_G+1`, and its fixed-scale restriction is the displayed sum of
log determinants.

The arbitrary-barrier lower certificate is sound: all directions of the
diagonal infinity-norm cone are recession directions, all coefficients
are positive under the specified epsilon bound, their weighted sum is
the interior point, and each backward endpoint is on the boundary.
Its limiting bound is `R_G+1`. Taking the certificate in the product
also handles coupled competing barriers. For the slice, the diagonal
gradient norm computation gives parameter at most `R`, and the cube
section proves the matching lower bound.

The completion cone is closed by bounded diagonals and the PSD entry
bound. Its signed Legendre barrier is the negative log determinant of
the maximum-determinant completion, up to a constant. The orthant
section supplies the sharp graph-order lower bound for arbitrary
barriers. The clique/separator identity, block-star coordinate counts,
identity-block slice, and rank-one full-row certificate all check out.
The reduced gradient and Hessian formulas are correct over both stated
fields. Claims about identical reduced Newton systems keep the same
coordinates and affine data, and do not identify ambient KKT systems.

## Other sections

I found no issue in the whole-row function-rank/face-rank bounds,
minimum-dimensional rigidity, normalized-base bound, or recession-level
normalization criterion in 09a. The last criterion correctly retains
its uniform minimum-height condition; the escaping-fiber example
prevents an automatic normalization claim.

The balance-slice extremality criterion, paths connecting the one- and
two-block primitive configurations, and orthant/simplex lower sections
in 09c are consistent. The trace-hyperplane gradient norm proves the
claimed restricted parameter, including the Albert case. The comparison
of matched cone dimensions is explicitly between different bodies.

The local and global norm-ball counts, all count-optimal capacity
excesses, half-cone counterexample, Young certificates, planar power-cone
exception, and generalized-power curvature calculation in 09d have
the needed hypotheses. The integer caps remove the issue recorded in
the assessment. The representation-class qualifications in its
literature comparison avoid an unsupported scalar priority claim.

## Primary-source verification

I checked Nesterov's recession bound as reproduced in Fawzi--Saunderson,
Theorem 3.9, against the actual hypothesis and conclusion used here:
<https://arxiv.org/html/2205.04581v3>.

I checked the signed Legendre transform, inverse-completion stationarity,
and maximum-determinant relationship in Andersen--Dahl--Vandenberghe,
Section 1.2, equations (3)--(6):
<https://arxiv.org/pdf/1203.2742>.

I also accessed the primary Coey--Kapelevich--Vielma formulation paper:
<https://arxiv.org/pdf/2005.01136>.

No additional corrections are requested by this review.
