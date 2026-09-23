# Stage 4B corrections after the first five reviews

Correction author: `/root/stage4b_fixer`. I read root's assessment and
all five independent reports before editing. All accepted findings are
implemented. The manuscript is frozen for root's second five-reviewer pass;
this correction does not close Stage 4B.

## Strengthened total sharing bound

In 09b and 09e, fix a block with at least one active row and choose its
nonzero dual contact vector b. Nonnegativity of the fixed-dual pairing on
the entire primal source manifold, together with its zero value at the
contact, proves that every primal derivative is in b-perp. The primal
contact vector is also in b-perp. The original cross-contact identities
make the primal ray and the rank-detecting derivative subspaces a direct
sum. Its dimension is 1 plus the sum of local row ranks; its containing
hyperplane has dimension m_i-1. Thus the total local row rank is at most
m_i-2. The no-active-row case is immediate. A zero primal or dual factor
cannot be active because a two-sided derivative into a pointed cone
vanishes at the vertex.

I independently checked that this argument needs only C1 factor maps,
not symmetric mixed matrices, second derivatives, or nondegeneracy of
the full spectral pairing. The spectral source and polar dimensions may
differ. The contact manifolds still permit the two-sided first derivatives
used in the minimum argument, including zero-dimensional real scalar rows.

The complementary-face inequality is retained. Summing it over q_i>=2
active rows gives (q_i-1)T_i<=q_i(f_i-1), so a shared block satisfies
T_i<=min(r_i,2(f_i-1)). The original discussion of a possible one-unit
sharing bonus is removed: it is impossible under the stated hypotheses.
The obsolete face-bonus label has no remaining references.

## Global product-ball resources

The labelled dual sum Bhat_i(z)=sum_a B_i^a(z_a) takes values in K_i^*
by convex-cone closure under addition and is C1 on the product of spheres.
Together with the existing primal maps it factors
k-sum_a<x_a,z_a>. At z=x this kernel vanishes and its independent mixed
pairing is the product spherical metric, of rank kp. Both source
manifolds are compact, connected, C1, boundaryless, and simply connected
because p>=2. Thus every hypothesis of the already proved joint-cover
theorem applies. At R=kp it would force exactly k positive capacities p.
A strict cap c<p excludes that profile, proving R>=kp+1. Additional ray
factors have zero capacity and do not change the application.

The original face-incidence and face-weighted capacity budgets remain
useful and their proofs are retained. The theorem now combines them as

    K = kp + 1_{c<p},
    R_* = max(ceil(k tau/f), K),
    L_* = max(ceil(k h/f), ceil(R_*/c)).

Here f>=1 is explicit. Face budgets and R>=K give R>=R_*; R<=cL and
the incidence budget give L>=L_*. Therefore D=R+2L>=R_*+2L_*.
The existing product-wedge restriction proves the ambient arbitrary-
barrier bound 2L_*. Since tau>=h and c>=1, L_*<=R_*, consistent with
positive integer capacities. At f=1 the formulas reduce to the existing
exact ray-exposed frontier: R_*=k tau and L_*=kh. No exact frontier for
general f>1 is asserted, and a fixed dictionary need not contain the
attaining Lorentz factors.

## Spectral consequences

In 09e, summing the strengthened local bound gives
sum_i q_i>=sum_a kappa_a. This is now the stated capacity inequality.
The redundant face-weighted and divided-by-f capacity consequences have
been removed. The face-specific inequalities and incidence budget remain.
With an integer dimension cap d and f_i<=f, the stated factor-count bound
combines the incidence ceiling with ceil(sum_a kappa_a/(d-2)). It follows
from the same capacity inequality and q_i<=d-2; no spectral global
topological premium or attainment claim is introduced.

## Integer caps, source coverage, and scope

The cap d>=3 is explicitly integer in the 09b setup, both exact-frontier
theorems in 09d, and the spectral cap hypothesis in 09e. The capacity-excess
proposition explicitly inherits the generic norm-ball theorem's hypotheses.

The source map records that the two sharing sources' weaker total bounds
are strengthened and their suggested one-unit bonus is excluded. The
main author audit and spectral author audit record this revision while
preserving the history of the initial author handoff. Original workbench
notes and literature packages were not edited. No unrelated manuscript
section was changed, and no new stage was started.

## Validation

`conda run -n qipm --live-stream make -C conic-lift-complexity` completed
successfully; the integrated PDF is 81 pages. Output is saved in
`stage4b-corrections-build.log`. The first LaTeX pass requested the normal
cross-reference rerun, which latexmk completed. The final `main.log` and
`main.blg` contain no warnings, unresolved citations/references, multiply
defined labels, or overfull/underfull boxes. A separate qipm Python audit
found no duplicate labels or unresolved reference targets. No dependency
or package was installed. The pre-existing untracked `formal/` was not
touched.
