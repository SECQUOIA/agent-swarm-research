# Independent review of the isolated-root replacement proof

Reviewer: Sol. Date: 2026-10-06 UTC.

## Decision

PASS. The new proof of `lem:sp:bezout` rigorously proves the unchanged
bound of `D^k` nonsingular complex common zeros. It handles systems with
singular zeros or positive-dimensional components without assuming that
the full zero set is finite. No mathematical repair is required.

The proof is self-contained apart from the ordinary holomorphic implicit
function theorem and elementary polynomial division and linear algebra.
It does not invoke Fulton's inaccessible Example 8.4.6, refined intersection
degree bounds, projective Bezout, a regular-sequence theorem, or a generic
finiteness assertion. The remaining Fulton citation is background
attribution at `C:62–64`, not a dependency in the argument.

This is a focused mathematical verdict on the replacement and its unchanged
caller interface, not a new full-paper review or bibliography audit. The
earlier sparse/domain mathematical PASS remains applicable to the unchanged
proofs in that block.

## Frozen sources and integrity

The target is `evidence/snapshots/isolated-root-proof-r1/`, captured at
`2026-10-06T04:23:50.845160+00:00`. Its manifest SHA256 is
`82bcd7e3082f297b53a10fcee701d9f94cfa082d1251618e244f5c1db0b50136`.
All 21 listed TeX/Bib files match their manifest SHA256 and line counts.

`C` and `A` below mean the corresponding appendix files in that target.
I read the actual new proof at `C:19–60`, the unchanged statement at
`C:13–17`, its scope explanation at `C:62–69`, and the changed caller at
`A:399–422`. I also read the prior report
`reviews/final-sparse-domain-sol-r1.md` and the round-two disposition, and
compared the assigned block against
`evidence/snapshots/mathematical-revision-r2/`.

| Target file | Lines | SHA256 |
| --- | ---: | --- |
| `appendices/C-sparse.tex` | 313 | `f9c4cf9a9e6b26b88ccc0eb3c24ad6b1c9d629eb7e45cd7dbd58a0636bc63206` |
| `appendices/A-finite-noise.tex` | 828 | `4f0b8f781a1e3ded62d15da52754fe4223d3a472f0b026f7e7f2b37d2a9b253f` |
| `sections/05-sparse.tex` | 1145 | `df3ef7c7f7c08d415044d9d93e3f9daa9b8a5d6c301954b950c3130c6718f047` |
| `sections/06-constraints.tex` | 818 | `9467eb72e20f355b3afb70d844bfedcf0a7fe52ba8f53d2483327162ad9db898` |
| `appendices/D-constraints.tex` | 1080 | `c0b90de5054e469a278c2d09f560ce39a746c5b1025c79ecf4aee75ca0f4e66b` |

Sections 05/06 and Appendix D are byte-identical to the round-two baseline.
Appendix C changes only the lemma proof and its following background
sentence; the lemma statement and all remaining proofs are unchanged.
Appendix A removes the refined-theorem assertion from the caller and adds
a Rademacher citation elsewhere; neither change modifies a mathematical
statement or constant. No broader comparison or approval of unrelated
source changes is implied.

## Complete proof check

### Finite selection and persistence (`C:20–28`)

If there are no nonsingular zeros, the conclusion is immediate. Otherwise
take any positive finite number `N` of distinct nonsingular zeros. At a
selected zero `z`, the derivative with respect to `u` of
`G(t,u)=(1-t)P(u)+t(u_i^D-1)_i` at `(0,z)` is exactly the invertible
Jacobian of `P`. The holomorphic implicit function theorem therefore gives
a branch `z(t)` on a complex neighborhood of zero.

For a finite collection, intersect the finitely many parameter
neighborhoods. Choose disjoint neighborhoods of the original points and
shrink this common parameter neighborhood so that each continued branch
stays in its assigned neighborhood. The continued points remain distinct.
No global control of other roots, their multiplicities, or escape to
infinity is needed.

Proving the bound for every finite selection also proves it for the whole
set. If the set had more than `D^k` elements, including infinitely many,
one could select `D^k+1` distinct elements and obtain a contradiction.
Thus the finite selection does not assume the desired finiteness result.

### Homogenization and the ideal component (`C:30–38`)

Let `R=C[x_0,u_1,...,u_k]`, with its ordinary total-degree grading.
Homogenizing to the fixed degree `D` gives

`H_i(t)=(1-t)P_i^h+t(u_i^D-x_0^D)`.

Here `P_i^h=x_0^D P_i(u/x_0)` denotes homogenization to degree `D`, even
when the original degree is smaller. Every coefficient is polynomial in
`t`, and `H_i(t)(1,u)=G_i(t,u)` for every specialization.

For the homogeneous ideal `J(t)=(H_1(t),...,H_k(t))`, its degree-`r`
component is exactly

`J(t)_r=sum_i H_i(t) R_{r-D}=I_r(t)`.

One inclusion is immediate. For the converse, write a degree-`r` element
as `sum_i H_i(t) a_i` and take its degree-`r` component. Since every
generator has degree `D`, only the homogeneous degree-`r-D` pieces of
the `a_i` contribute. This remains true if a specialized generator is
zero. The chosen `r>=D` ensures that the multiplication spaces have
nonnegative degrees. Therefore the cokernel of the displayed finite
multiplication matrix is the degree-`r` quotient used in the proof.

There is no saturation step and no implicit replacement by a radical
ideal. Extra projective or embedded components, if present, cannot
invalidate either this identity or the subsequent evaluation argument.

### Exact quotient dimension at `t=1` (`C:38–47`)

At this specialization, the ideal is generated by
`u_i^D-x_0^D`, one monic polynomial in each separate variable `u_i`.
For any coefficient ring `B`, division by a monic polynomial of degree
`D` identifies `B[u]/(u^D-c)` with a free `B`-module with basis
`1,u,...,u^{D-1}`. Applying this fact successively, starting with
`B=C[x_0]`, proves both existence and uniqueness of the stated remainders.
It gives a free `C[x_0]`-basis of the full quotient indexed by
`a=(a_1,...,a_k)` with `0<=a_i<D`.

The relations are homogeneous, so the degree-`r` quotient basis consists
of the monomials

`x_0^(r-sum_i a_i) product_i u_i^a_i`

for precisely the indices with `sum_i a_i<=r`. The condition
`r>=k(D-1)` includes every one of the `D^k` indices. Their coefficients
in `C[x_0]` are uniquely determined, so they are independent as well as
spanning. Hence the dimension is exactly `D^k`. This is an elementary
module calculation, not an unproved complete-intersection formula.

### Rank specialization near zero (`C:48–52`)

Put `q=dim V_r` and `rho=q-D^k`, the rank at `t=1`. A `rho` by `rho`
minor that is nonzero at one is a nonzero polynomial in `t`. It has
finitely many complex zeros. Away from those zeros, the multiplication
matrix has rank at least `rho`; thus its cokernel dimension is at most
`D^k`. The direction of this inequality is correct: ranks can drop at
exceptional parameters, while the quotient dimension can increase there.

Every neighborhood of zero contains a parameter outside this finite
exceptional set. Choose one in the common continuation neighborhood.
This simultaneously supplies the `N` distinct continued points and the
quotient upper bound. The minor may vanish at zero; that does not prevent
choosing arbitrarily small admissible nonzero parameters. No generic
finiteness theorem is required.

### Evaluation is onto (`C:53–59`)

Write the distinct continued affine points as `z_1,...,z_N`. For every
pair `a!=b`, choose a coordinate `j` with `z_{a,j}!=z_{b,j}` and use the
affine linear factor

`L_ab(u)=(u_j-z_{b,j})/(z_{a,j}-z_{b,j})`.

The product `L_a=product_{b!=a} L_ab` has degree at most `N-1`, value one
at `z_a` and value zero at all other selected points. Homogenizing it to
the chosen degree `r>=N-1` gives a member of `V_r` with the same values
at `(1,z_b)`. These `N` evaluation vectors are the standard basis of
`C^N`, proving surjectivity. For `N=1`, the empty product is one and its
degree-`r` homogenization is `x_0^r`.

Every generator `H_i(t)` vanishes at the selected affine representatives,
so every element of `I_r(t)` evaluates to zero. Consequently evaluation
factors as a surjection `V_r/I_r(t) -> C^N`, and

`N <= dim(V_r/I_r(t)) <= D^k`.

This counts distinct points, exactly as the lemma requires. It needs
neither reducedness of the specialized ideal nor simplicity of any other
root. The continued selected points need only exist and remain distinct
at the chosen parameter.

## Endpoints, degeneracies and caller preservation

The proof covers `k=1` and `D=1`. In the latter case the specialization
has relations `u_i=x_0`, its free module basis has one element, and every
degree-`r` quotient has dimension one. With `k,D>=1` and `r>=D`, the
specialized generators are nonzero and the stated multiplication spaces
are well-defined. Lower-degree original polynomials are handled by fixed
degree homogenization. A nonzero constant original equation has no common
zero; a zero or constant equation has a zero Jacobian row and hence no
nonsingular common zero. Those vacuous cases require no separate
perturbation assumption.

The lemma still applies only to square systems in positive dimension.
The unchanged downstream empty-tuple conventions cover zero dimension:
`A:405–407`; `D:238–241`, `D:615–618`, `D:990–993`. The implicit-graph,
simplex and order tail arguments retain exactly their existing degree
powers and constants. Their justification that positive-growth optimizers
give nonsingular stationary roots was already checked in the preceding
full review and is unchanged. Appendix A now invokes the proved lemma
directly, without claiming an externally supplied refined theorem.

No new work bound is asserted for this perturbation proof. The proof's
choice of `r` may depend on the finite selection size `N`; this is valid
for the cardinality argument and does not introduce an algorithmic cost
or a sampling parameter into any downstream theorem.

## Checks performed and limits

I used targeted `cat`, `nl -ba`/`sed`, and scoped `rg` reads. A Python
script computed all 21 target hashes and line counts and compared the
five relevant files against the round-two baseline. The proof above was
checked analytically; no numerical or symbolic experiment was needed.
Only this report was written, and its final format and target integrity
were checked.

No manuscript edit, literature research, KB change, delegation, build,
experiment rerun, project-wide verification, CI inspection, commit or
publication was performed. Bibliographic attribution remains the source
auditor's responsibility. There is no unresolved mathematical issue in
this replacement proof.
