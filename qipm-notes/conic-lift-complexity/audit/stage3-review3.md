# Stage 3 independent review 3

Scope: Sections 6 and 7, with particular attention to the norm-tree parameter,
cap combinatorics, intrinsic polyhedral sections, compact-base lemma, and
rotated perspective counterexample. I reconstructed the calculations rather
than treating the workbench or author reports as proof.

## Assessment

**No major issue found.** The root-incidence formula, its capped optimum, the
intrinsic tree lower bounds, and the exact rotated-slice parameter are supported
by complete arguments. Two valid minor corrections are listed below. They do
not change the theorems or require a new mathematical development.

## Required minor corrections

1. **Section 6, Example `ex:rotated-nullity`, full certificate characterization:**
   add `A_G >= 0` explicitly to the displayed conditions. At `eta=1`, the stated
   conditions `gamma=0`, `sum A_G=1`, and `4 A_G gamma >= ||c_G||^2=0` do not
   prevent negative `A_G`; such a block is outside the Lorentz cone. The prose
   subsequently gives the correct simplex, but the preceding assertion that
   coefficient matching makes the displayed conditions necessary and sufficient
   is incomplete as written. Adding nonnegativity makes the characterization
   correct also at the north pole. For `eta<1`, it is already implied by the
   determinant inequality.

2. **Section 6, final density-matrix example:** replace “fills the primitive
   projective line with rank-two matrices” by a precise description such as
   “contains all primitive rays in `U`, normalized to trace one, and their
   rank-two mixtures.” The trace-one PSD set is the convex hull of the primitive
   projective line, not a projective line consisting of rank-two matrices. The
   intended obstruction at the scalar center is correct.

## Independent mathematical checks

### Tree root restriction

Homogeneity gives the restricted squared gradient norm
`2L - t^2/(e_t^T H^{-1} e_t)`. Dikin containment yields beta <= 1. In the
root-leaf case, the displayed direction has zero second derivative of the root
determinant itself; its Hessian value is therefore exactly
`4(1-sqrt(1-eps))^2/q_r^2`, tending to one. Scaling all internal subtrees by
`eps^2` leaves their axial squares of order `eps^4`, as required.

For an all-internal root, eliminating all coordinates below each child leaves
an axial Schur curvature at least `a_i^{-2}`. Monotonicity of the final Schur
complement under an increased child Hessian is valid. With
`Z=sum a_i^4/(q+2a_i^2)`, the rank-one inverse calculation indeed gives

`S=[2(1+r)-16Z/(q+4Z)]/q^2`.

The scalar bound `Z <= r^2/(1+r)` follows termwise from monotonicity of
`x/(q+2x)`. Substitution into the equivalent condition
`r(3-r)>=4(2-r)Z` leaves exactly `3r(1-r)^2/(1+r)>=0`.
The root-only direction at vanishing subtree scales proves sharpness. Thus the
standard parameter is exactly `2L-2` or `2L-1`, and independent forests add.

### Capped tree combinatorics

For fixed root arity c, feasibility is equivalent to

`L >= c+1` and `L+c-2 <= E <= (c-1)+(L-1)A`.

At `L=L_0`, existence of a c in `[2,d-1]` is exactly the stated indicator
condition. Partitioning the remaining internal nodes into c nonempty chains
realizes every admissible list of increments. The exclusions `L_0=1,2` are
necessary and correct. Adding one internal node cannot improve the standard
parameter, even if it changes the root type. I checked the criterion against
the above direct integer feasibility test for every `N=2,...,100` and
`d=3,...,20` using the designated qipm Python environment; all cases agreed.
This numerical enumeration supplements the proof, not replaces it.

### Intrinsic section and logarithmic correction

Positive leaf values ensure that the two complementary ray vectors at each
node are independent. The linking equations leave exactly L free beta
coordinates on the root slice. The section is bounded, meets the interior,
and has exactly L independent active facets at beta=0. Every section boundary
lies on the original domain boundary, so restriction of an arbitrary barrier
preserves the barrier property. This supports the NN facet-bound application.
The conic lower bound uses logarithmic homogeneity expressly and correctly;
it does not silently apply to arbitrary nonhomogeneous cone barriers.

I independently expanded the proposed two-block corrected logarithm to third
order using rational arithmetic. The results are `53/16` and `-441/32`, and
the self-concordance residual is `11401/256 = 45604/1024 > 0`, as stated.

### Compact base and rotated lift

The compact-base lemma actually needs only the stated nonnegative height,
as its proof says: orthogonal projection removes
`1/(ell^T H^{-1} ell) >= 1` from the homogeneous squared gradient norm.
No extra compactness premise is missing from the argument.

For the rotated construction, summing cone inequalities proves the exact ball
projection. Away from the north pole the boundary fiber is a singleton and
each block is a nonzero rank-one cone point, including groups whose projected
coordinates vanish. At the north pole, the simplex fiber ranges from q to
`2q-1` null eigenvalues. Direct coefficient matching gives the displayed dual
formula, subject to correction 1 above. Its ranks have exactly the asserted
maxima and minima. Homogenization and the compact-base lemma give the upper
parameter `2q-1`, while a north-pole fiber vertex gives the matching lower
bound. Product additivity and the no-transfer argument for strictly positive
source weights are valid.

### Additional scan

The grouped paraboloid derivative identities and inverse-Hessian gradient
calculation are correct. The H-dimensional box section supplies the arbitrary
barrier lower bound even when mixed derivatives are allowed. The packing proof
does not accidentally assume that columns are orthogonal or that b<=p; bounded
completion fibers and partial minimization handle arbitrary b. The latter
lemma proves local uniform boundedness from closed convexity, rather than
assuming it from pointwise bounded fibers. Its implicit-function and Schur
complement identities justify all derivative assertions.

The explicit distinction between a prescribed standard barrier and intrinsic
barrier optimality is maintained throughout. The unresolved interval for
arbitrary intrinsic tree barriers is presented as a limitation, not as an
unproved optimality theorem. Existing norm-tree/grouped/packed constructions
and the root calculation overlap the repository's central-path manuscript;
the author audit correctly reserves this relationship for the final literature
and contribution discussion. Section 7 itself makes no unsupported absolute
novelty claim.
