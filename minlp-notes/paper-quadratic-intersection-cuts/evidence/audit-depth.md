# Depth and approximation audit

This audit covers the ratio-bound note, both reviews and their retained exact
certificate records, the relevant bilinear results in the sfree note, and the
October closeout. Existing experiments were not rerun. Literature work was not
performed. The mathematical conclusions below come from direct derivation;
saved computation is used only where identified explicitly.

## Conclusions and repairs

The analytic depth guarantee and the order of its dependence on depth survive
the audit. The fixed SCIP rule has the stated order in the product of depth and
the ray condition number, in its narrowly specified coordinates. The exact
upper constant 1.54 is computer-assisted; the universal lower constant
sqrt(2)-1 is analytic. Large depth permits bad examples, but does not force
every corner to have a small ratio: Proposition S3 has arbitrary depth and an
exact orbit family.

Two proofs can be completed beyond the source package:

1. The open boundary case in Theorem C(3) is resolved by the perturbation lemma
   below. Under the unique-contact and positive-height assumptions, closed
   interval feasibility is equivalent to equality of the orbit supremum and
   the corner bound. Interior feasibility at the LP vertex is equivalent to
   attainment. Singular limits can be handled explicitly, so no dimension
   assumption is needed in this repaired statement.
2. Proposition C3 holds on the explicit range `0 < d < 7/128`, with an entirely
   analytic proof of its corner bound and uniqueness. The saved exact checks at
   three values of `d` are corroborating evidence rather than the proof of the
   continuous parameter statement.

Statement repairs are required even though the two existing reviews approved
the principal proofs:

- Theorem A defines `f(1)` twice with different values. Both estimates are
  valid at one. The manuscript uses the elementary stronger branch
  `2/(sqrt((1+D^2)^2+4D^2)+1+D^2)` for `0<=D<=1`, which agrees with the
  large-depth branch at one, and retains `1/(1+2D^2)` as a simpler lower
  estimate. This continuous improvement follows directly from the proof.
  Treat `D=0` separately, as a supremum statement.
- A constant positive restriction of `q` to a ray has `A=B=0`; its relative
  discriminant is undefined. Say “relative discriminants, when defined.” The
  grazing-margin hypothesis already excludes these rays.
- “Affinely invariant” means invariant under the specified affine symmetries
  preserving the bilinear model. It does not license measuring `D` in an
  arbitrary affine frame. Euclidean angles and the condition number are not
  invariant under those symmetries.
- In Lemma R, say “trace-selected branches,” not “convex components” in the
  topological sense. The scalar quadratic region can be connected and
  nonconvex because its two cone branches meet at an apex. For example,
  `X=[[0,1],[-1,0]]` gives `xy <= -(w-1)^2/4`.
- Lemma S's first-root formula applies to the uncompleted orbit set. It is
  false for the upward completion in general. At `sbar=(1,0,1)` on `p=e_w`,
  the uncompleted step is `10+sqrt(120)`, whereas the completion's step is
  infinite. Theorem S explicitly uses the uncompleted set as a lower bound,
  and Proposition S3 computes both values, so their conclusions are valid.
- Theorem S needs three linearly independent projected rays for a finite
  condition number, or full row rank in its stated `N`-ray extension. Its
  first lower bound does not need rank. If rank is absent, use the first
  bound and omit the condition-number statement.
- The printed necessary compactness direction of Theorem C(3) excludes a
  rank-one limit by using an unstated `dim T*=3` hypothesis. Replace this
  exclusion by the two rank-one constructions below. Unique contact and
  positive heights then suffice without a dimension assumption.
- The general lowered-interval sentence for family B does not include all
  admissible endpoints: `h'=xy>0` can be allowed, and negative lowered heights
  cannot be discarded for a general completion without a tangent-support
  argument. Do not promote that informal sentence to a theorem. Use exact
  membership by lowering and retain the B contact test as an open extension.
- Theorem B(4) uses a saved symbolic certificate with exact root counting.
  Label it an exact computer-assisted bound, even though B(1)--(3),(5) are
  analytic. It is superseded quantitatively by B2(1), but its dual-certificate
  argument remains useful.

## Claim inventory by original identifier

| Original claim | Status after audit | Scope and disposition |
| --- | --- | --- |
| Lemma N | Analytic, correct with wording repairs | Bilinear affine symmetries with `alpha beta>0` and the coordinate swap; `D` and defined discriminants invariant; angles, condition number and fixed SCIP rule are not. |
| Lemma R | Analytic | Exact determinant/trace formula; use trace-selected branches. Empty slices are possible for a choice of sign, so interior-containing members are the relevant family. |
| Normalized-frame paragraph | Analytic | Vertex becomes `(0,0,1)`; use translation parameters `a=-alpha xbar`, `b=-beta ybar`. Interior is `sym(X)>0`. |
| Cylinder formula (1) | Analytic | Root formula for all rays, with zero denominator interpreted as infinite. Cylinders are in both A and B. |
| B membership/closedness paragraph | Analytic | For `det X>0`, `s in B_X` iff a lowered point with `0<=tau<=q(s)` is in `C_X`; `q(s)>=0` is necessary. This also proves the sum is closed. |
| Theorem A | Analytic | Finite ray family, strictly positive costs, violated vertex, finite corner bound; no rank assumption. Define `f` unambiguously and prove `D=0` separately. |
| Corollary A' | Analytic | `D>=1`; margin only on missing rays with initially decreasing `q`; improves the constant, not order. |
| Theorem B(1) | Analytic | Exact `zK=z0`, unique support-one transverse contact. |
| Theorem B(2) | Analytic except rounded condition number | Discriminants `-1,-1,+1`, fixed nonsingular ray matrix, exact depth. `cond(P)=12.0136...` is numerical and independence of epsilon is exact. |
| Theorem B(3) | Analytic | Lower bound; fixed-rule value `2 sqrt(epsilon)/z0` only for `epsilon<=4/9`, otherwise its minimum with one. |
| Theorem B(4) | Exact computer-assisted; superseded | Rational dual certificate valid for `epsilon<=1/9765625`; do not call its numerical search an analytic proof. |
| Theorem B(5) | Analytic | B ratio tends to zero at fixed condition number and maximal discriminant margins; proof can be simplified as below. No quantitative rate from this proof alone. |
| Theorem B2(1) | Exact computer-assisted | Upper bound `137 sqrt(epsilon)/z0`, every `0<epsilon<1`, all completed orbit members, including those whose generating orbit set misses the vertex. |
| Theorem B2(2) | Exact rational witness | Lower bound `1367/10`, only for the stated exact epsilon threshold; not the heuristic `136.707`. |
| Theorem B3(1) | Analytic | `eta in (0,1)`, `k>=1`, rational square root for the certificate cases; `L<zK<L+1/L`, depth `sqrt(k) zK`, exact relative discriminants. |
| Theorem B3(2)--(4) | Exact computer-assisted | Four retained rational upper certificates, every `L>0`; minimum reported upper asymptotic constant is `1.54`. |
| Theorem B3(5) | Exact rational witnesses | Four completed-set lower bounds for `L>=3.4`; each has a smaller exact individual threshold. |
| B2/B3 worst-case constant comparison | Derived from analytic and computer-assisted claims | Separate constants for A and B lie between `sqrt(2)-1` and `1.54`; they need not be equal. Factor `1.54(1+sqrt(2))<3.72`. |
| Section 3.1 equality with `sup_H rho_max(H)` | Numerical only | Only lower inclusion and shared exact bracket are proved; equality was repaired after r1 and remains unproved. |
| Section 3.3 `56.7`, finite-height A table, heuristic B table | Numerical only | Preserve as calibration if desired, never as exact bounds or asymptotic limit theorems. |
| Lemma S | Analytic with ray-step repair | Exact Case-4 uncompleted set for the unit bilinear representation; actual set is upward completion. First quadratic root is uncompleted step. |
| Theorem S | Analytic | First bound finite N without rank; condition-number bound for full row rank. Coordinates and constraint representation fixed. |
| Proposition S2 | Analytic | Depth one, exact orbit cylinder, worsening rule by diagonal rescaling; piecewise condition number, not `L^2` at all L. |
| Proposition S3 | Analytic | Exact prescribed positive depth and condition number, exact orbit family, all discriminants +1; completed and uncompleted rule values equal in this construction. |
| Theorem C(1) | Analytic | In coordinates centered at a boundary contact, all invertible orbit sets through it have triangular `X=[[alpha,0],[beta,1]]`, alpha positive. Completions containing contact have generators containing it. |
| Theorem C(2) | Analytic | Positive tangent height and nonnegative q; interval membership includes trace automatically. |
| Theorem C(3), attainment | Analytic | Finite vertices, support-one contact, all other tangent heights positive; strict interval membership at sbar exactly means interior there. |
| Theorem C(3), supremum/strict gap | Completed in this audit | Unique contact and positive heights suffice without dimension assumptions: closed interval intersection iff `zA=zK`; its failure for every alpha iff strict gap. Perturbation and explicit singular-limit constructions close the boundary question. |
| Theorem C(4) | Analytic | Cylinder sufficient condition; equality allowed at other vertices, strict at sbar. `H_cyl>1` suffices. Use supremum over t, and infinite ratio when curvature denominator is zero. |
| Theorem C(5) | Analytic with contact-height qualification | A two-sided tangent edge forces alpha; positive-height vertices use intervals; zero-height edge points require `alpha x+y=0` and the nonnegative remaining PSD entry. |
| Proposition C2 | Analytic | Euclidean edge angles alone do not give exactness; existence of the base counterexample can use the self-contained foundation result or the integer witness below. No B nonexactness is proved by that base witness. |
| Proposition C3 | Strengthened analytic | Entire range `0<d<7/128`; full-dimensional T*, unique support-one minimizer, strict A gap, `H_cyl>=1-4d`. B nonexactness is numerical only. |
| Section 6.1 adversarial bracket | Exact computer-assisted | Use `[763/25000,191/6250]`; exact binary-float instance and exact corner normalization are distinguished in r2's independent witness. |
| Section 6.1 restricted B search | Exact scoped comparison | Restriction to generators containing sbar loses at most `137/136.7-1<0.22%` on B family only in the epsilon lower-witness range. It is not general completeness of that restricted search. |
| OQ1, OQ2 | Open | Exact worst-case constants and margin dependence remain open. |
| OQ3, OQ6 | Open | Changing fixed rule or Case 2 is outside the proved fixed Case-4 model. |
| OQ4 | Partly resolved | A supremum boundary resolved here; complete B interval test and its tangent-edge analogue remain open. |
| OQ5 | Open | General minor analogue of depth is not proved. |

## Replacement proof: vertex normalization and depth guarantee

Let there be finitely many rays, positive reduced costs, `q(sbar)>0`, and a
nonempty feasible corner. Positive objective sublevels in ray coordinates are
compact, so `0<zK<infinity` is attained. Put
`p~_j=(zK/c_j)p_j`, `T_r=conv{sbar,sbar+r p~_j}`. Every point in `T_r` has
cost at most `r zK`, hence `q>0` on `T_r` for `r<1`; by continuity `q>=0` on
`T_1`. The single-cut ratio of a set is the minimum of its steps on the scaled
rays. This is a consequence of the one-cut ray formula, not a new objective
normalization assumption.

The maps in Lemma N act on matrices by `M'=A M B^T`. If `X=F^T`, the image of
its PSD set is the set for `X'=B X A^{-1}`, by congruence. Transposition uses
`X'=X^{-1}`, again by congruence. Their positive scaling of `e_w` commutes
with upward completion. Depth scales by
`X~ -> |alpha| X~`, `Y~ -> |beta| Y~`, `qbar -> alpha beta qbar`, so it is
unchanged. The quadratic coefficients on a transformed ray have a common
positive multiplier, preserving the relative discriminant when its
denominator is nonzero. A simultaneous positive rescaling of a ray and its
cost preserves its scaled ray. Objective scaling has the same cancellation.

For each `t>0`, use the cylinder centered at the LP vertex:

`C_t={q(s)>=(t(x-xbar)-(y-ybar)/t)^2/4}`.

It is the epigraph of a convex quadratic, belongs to both families and contains
the vertex in its interior. Along scaled ray j its slack, divided by qbar, is
`1+a_j s-b_j(t)^2 s^2/4`, where

`a_j=grad q(sbar)^T p~_j/qbar`,
`b_j(t)=(t p~_jx+p~_jy/t)/sqrt(qbar)`.

Its step is `2/(sqrt(a_j^2+b_j^2)-a_j)`, with zero denominator meaning
infinity. Write the original restriction as
`g_j(s)=1+a_j s+d_j s^2`, with `d_j=-p~_jx p~_jy/qbar`.

For positive depth, take `t=sqrt(Y~/X~)`. Then `|b_j|<=2D` and
`|d_j|<=D^2`. If `D<1`, positivity at s=1 gives
`a_j>=-1-d_j>=-1-D^2`. If `D>=1`, positivity at s=1/D gives
`a_j>=-D-d_j/D>=-2D`. This avoids the root-by-root case analysis in A(ii).
If a_j is nonnegative the cylinder denominator is at most `|b_j|<=2D`.
For negative a_j, the small-depth denominator is at most
`sqrt((1+D^2)^2+4D^2)+1+D^2<=2+4D^2`; the squared difference in the
intermediate estimate is `8D^4`. The large-depth denominator is at most
`2D(sqrt(2)+1)`. This proves Theorem A with an unambiguous piecewise f.
Keeping the unsimplified small-depth denominator gives the final continuous
formula described above.

At `D=0`, every d_j is zero. Feasibility implies at least one a_j is negative,
and corner optimality implies `min a_j=-1`. Let t tend to zero when Y~=0,
or to infinity when X~=0, so that every b_j tends to zero. For negative a_j
the step tends to `-1/a_j`; for nonnegative a_j it tends to infinity.
The finite-ray minimum tends to one. Thus both best-family ratios equal one
as suprema; no attainment statement is added.

For A', a missing ray with decreasing q must have d_j>0, and its margin implies
`a_j^2<=4d_j(1-mu)/(1+mu)`. A ray meeting S has `-a_j<=2`: if d_j>0,
write g as `(1-s/r1)(1-s/r2)` with both roots at least one; if d_j<=0 the
positive first root gives `-a_j<=1`. Thus
`-a_j<=2D max(sqrt((1-mu)/(1+mu)),1/D)`. Apply the same denominator bound.

The Euclidean observation is only sufficient, in fixed coordinates:
`dist(sbar,S)<=qbar` by vertical projection, and
`X~Y~<=diam(T*)^2`, so `1/D^2>=dist(sbar,S)/diam(T*)^2` when the product
is positive. It is not an affine invariant Euclidean distance identity.

## Replacement proof: analytic vanishing for completed sets

For Theorem B, expansion gives

`q=epsilon+lambda3-lambda3^2+lambda2 lambda3+(lambda1+2lambda2)(lambda1+lambda2)`.

Consequently q<=0 requires lambda3>=z0, with equality in the objective only
on its ray. Depth and the extreme discriminants follow directly. The ray
matrix is independent of epsilon and nonsingular, which is the analytic
conditioning assertion; its rounded spectral condition number is numerical.

To prove B(5), fix z in (0,1) and suppose completed sets contain
`T_n=conv{sbar_n,sbar_n+z p1,sbar_n+z p2,sbar_n+z p3}`, epsilon_n->0.
Normalize their matrices X_n to norm one and pass to X. Lower each of the
four vertices to its generating orbit set. The lowering is bounded by q at
the vertex, so pass to limits of these lowered vertices too.

If det X>0, the limiting completed set B_X contains
`T_0=conv{0,z p1,z p2,z p3}`. This tetrahedron is full dimensional and meets
the tangent plane at its two horizontal vertices. Convex S-freeness and contact
at zero imply B_X lies in w>=0. To justify this explicitly, a point with
negative w gives a short segment from zero inside int S; joining a nearby
point of that segment to an interior point of T_0 gives an interior point of
B_X in int S, a contradiction. Hence its generating C_X also lies in w>=0,
and any w=0 point in B_X must be in C_X. Because 0 belongs to C_X, the rank-one
PSD condition puts X, after positive scaling, in the form
`[[alpha,0],[beta,1]]`, alpha>0. At a w=0 point its PSD off-diagonal must
vanish, so `alpha x+y=0`. The two horizontal vertices require alpha=1 and
alpha=2, a contradiction. This replaces the source's longer exposed-face
classification.

If det X=0, X has rank one and its PSD membership equation puts all limiting
lowered points in a nontrivial affine plane. Their xy projections are not
collinear, so the plane has the form `w=a x+b y`. The convex hull of these
lowered points, plus the upward ray, is an S-free limit: a point in its
interior and int S would persist in approximating full-dimensional convex
subsets of the original completed sets. Thus `a x+b y>=xy` on their planar
projection. Near zero, the directions (1,-1) and (1,-2) give
`a-b>=0`, `a-2b>=0`; the lowered horizontal vertices give the reverse
inequalities. Hence a=b=0. The lowered third vertex must then use lowering z,
although its maximum allowed lowering is z-z^2. Contradiction. Since z was
arbitrary, zB tends to zero.

## New proof: approximation of a contact set with the vertex on its boundary

Let det X>0 and let `sym(X M(v))` be PSD at every vertex v of T*, including
sbar. For fixed `0<r<1`, write `v_r=(1-r)sbar+r v` and `A(s)=sym(XM(s))`.
Then `A(v_r)=(1-r)A(sbar)+r A(v)` is PSD. Its kernel is the intersection
of the two endpoint kernels: for any vector in its kernel, the two
nonnegative quadratic forms have sum zero, so both forms vanish; a PSD
matrix whose quadratic form vanishes annihilates the vector.

Put `J=[[0,1],[-1,0]]`. On the entire segment from sbar to v_r, write
`XM(s)=A(s)+k(s)J`. A vector u in that common kernel satisfies
`XM(s)u=k(s)Ju`. Every such s has cost below zK and hence q(s)>0;
M(s) and X are invertible. Therefore k(s) cannot vanish for a nonzero u.
It is continuous, so its sign is constant on the segment. Applying the
endpoint identities gives

`M(sbar)^(-1) M(v_r) u = (k(v_r)/k(sbar)) u`.

In particular `H_v=sym(M(sbar)^(-1)M(v_r))` is strictly positive on
the kernel of A(v_r). If that kernel is zero, A(v_r) is already PD. In
either case `A(v_r)+epsilon H_v` is PD for sufficiently small positive
epsilon: split the space into the positive eigenspace and kernel of A,
then the Schur complement is `epsilon H_ker+O(epsilon^2)` with positive
leading coefficient. In dimension two this also follows directly from the
positive leading term of the determinant and the positive trace. There are
finitely many vertices, so a single epsilon works for all of them.

Set `X_epsilon=X+epsilon M(sbar)^(-1)`. At sbar its symmetric matrix is
`A(sbar)+epsilon I`, which is PD. Its determinant stays positive by
continuity for small epsilon. Its PSD set therefore contains every vertex of
T_r, contains T_r by convexity, and has sbar in its interior. Its cut ratio
is at least r. Let r tend to one. Thus a closed orbit set containing T*
implies `zA=zK` as a supremum, even when the original set has sbar on its
boundary. This sufficient direction has no rank hypothesis.

Conversely, if zA=zK, normalize an approximating sequence X_n to norm one.
A convergent subsequence has a nonzero limit X with det X>=0, and its PSD
inequalities contain T*. If det X>0, contact intervals follow directly. If
det X=0, PSD at the contact origin forces `X=[[a,0],[c,d]]`, d>=0, ad=0.
If d>0, a=0 and PSD at positive-height vertices forces y=-(c/d)h. Set beta=c/d
and choose `0<alpha<min_{v!=0,x_v!=0}4q(v)/x_v^2`; the determinant slack is
`4alpha q(v)-alpha^2 x_v^2>0`. If d=0, PSD at the positive-height LP vertex
forces a>0 (a=0 would force c=0 and X=0). Its symmetric determinant is
`-(a x-c h)^2/4`, so x=(c/a)h at all vertices. Set beta=alpha c/a and choose
`alpha>max_{v!=0}y_v^2/(4q(v))`; the slack is `4alpha q(v)-y_v^2>0`.
Unique contact supplies q(v)>0 at every other vertex, and finiteness supplies
one common alpha. Both singular cases yield an attaining orbit set with all
noncontact vertices PD. Thus no dimension assumption is necessary.

For unique support-one transverse contact, Theorem C(1)--(2) now turns this into:

- `zA=zK` iff some alpha>0 makes all closed intervals meet;
- the value is attained iff some such common point is in the interior of
  the LP-vertex interval;
- no closed intersection for every alpha implies a strict gap.

The independent child audit `/root/audit_depth/depth_check` checked the kernel
identity, invertibility/sign argument, perturbation on the PSD kernel and the
finite-vertex choice of epsilon, and confirmed the result. Its independent
child `nr_symmetry` checked both singular-limit constructions. The root's
independent contact reviewer verified the final main and appendix proofs and
recorded a resolved review in `review-contact.md`. These are mathematical
reviews, not journal peer review, and do not prove a B criterion.

## Replacement proof: explicit sharp cylinder threshold

For Proposition C3 define a,b,c as barycentric weights of the three vertices
other than t*=0, at d=0. On their opposite triangular face `a+b+c=1`,

`q0 = 2a^2+(11/2)ac-(5/4)a+(5/4)c^2-(1/2)c+1/4`.

Its Hessian has negative determinant, so an interior stationary point cannot
be a minimum. On c=0 the minimum is `7/128`, at a=5/16; on a=0 the minimum
is `1/5`; on b=0 the minimum is one. Thus the minimum on that face is
exactly `7/128`. Its tangent height is at least 1/4. Every nonzero point in
T* can be written theta v, with theta in (0,1] and v in that face. Therefore

`q0(theta v)/theta=(1-theta)w(v)+theta q0(v)>=7/128`.

The perturbed instance lowers each of the three vertices by d, so
`qd(theta v)=q0(theta v)-d theta >=theta(7/128-d)>0` for
`0<d<7/128`. The only feasible point at cost at most one is t*, proving
zK=1 and unique support one. The projected ray determinant is
`-3(3d+4)/2`, so T* is full dimensional. All three heights remain positive.

The source's interval separation inequalities are valid on the wider range
`0<d<=1/8`, so apply throughout this explicit range. For t>=1 they give

`left_sbar-right_2 >= (t-1)(38t-26)/7+4dt>0`;

for 0<t<=1 they give

`left_3-right_2 >=(1-t)(77-17t)/62+2dt>0`.

Thus no closed interval intersection exists and zA<1. At t=1 the three
height/curvature ratios are `1-4d`, `1-d`, `1-d/4`, proving
`H_cyl>=1-4d`. For every eta>0 choose
`0<d<min(7/128,eta/4)`. A nonexact corner then has
`H_cyl>1-eta`. This proves sharpness of the strict threshold one.

## Exact certificate dependencies and provenance

The exact computer-assisted upper bounds reduce to six point conditions
(vertex, two horizontal vertices and their three midpoints) and a vertical-line
intersection. These conditions are necessary for all B members, not just
generators that contain the vertex. For a matrix X, the point exclusion is a
single rational vector negative at both endpoints of the allowable lowering
interval. The line exclusions are `rho x21+x22<0` or
`Psi=rho x21(x11-x22)+x11 x22-rho^2 x21^2<0`. With det X>0 and x21 nonzero,
the maximum determinant on the line is `(det X/x21^2)Psi`; if x21=0,
Psi=det X>0. The determinant-negative exclusion handles inadmissible boxes.

Positive matrix scaling reduces the search to eight facets of the unit
entrywise cube. Every retained bisection leaf is a dyadic box with a rational
exclusion. Prefix-free bisection paths with Kraft sum one give complete facet
coverage. This hand reduction and the finite exact arithmetic constitute the
proof; floating-point searches only discover witnesses.

| Claim | Saved leaf file under `ratio-bound/logs/zB_cert/` | Leaves |
| --- | --- | ---: |
| B2(1), rho=137 | `leaves_rho137.jsonl.gz` | 28,699 |
| B3(2), eta=1/1000, k=4, rho=197/200 | `leaves_tan_eta1e-3_k4_rho197_200.jsonl.gz` | 11,132 |
| B3(3), eta=1/100, k=4, rho=5/4 | `leaves_tan_eta1e-2_k4_rho5_4.jsonl.gz` | 1,882 |
| B3(4), eta=1/1000, k=9/4, rho=21/20 | `leaves_tan_eta1e-3_k9_4_rho21_20.jsonl.gz` | 10,705 |
| B3(4), eta=1/1000, k=49/25, rho=11/10 | `leaves_tan_eta1e-3_k49_25_rho11_10.jsonl.gz` | 11,943 |

The saved author verifier is `code/verify_zB.py`; its box decoder is shared
with `code/certify_zB.py`. Independent r1 verification is
`reviews/r1-code/indep_verify_boxes.py`, with records in
`reviews/r1-logs/boxes/`. It checks the exact maximum of Psi rather than the
author's interval upper bound, and checks geometric volumes and nonoverlap.
Its corruption controls reject changed rho, a missing leaf and a duplicated
leaf. R2 confirmed the leaf files and their reproduction. Those historical
verification runs were read, not rerun in this audit.

Exact lower witnesses are the five fixed rational matrices and heights printed
in `logs/rev1/certify_lower_found.log`. Their source is
`code/certify_lower_found.py`; its generation of heights uses floating point,
so this audit did not execute it. Instead, the saved heights and matrices were
checked by a new fraction-only calculation. All four PD/PSD checks per set
passed. The epsilon threshold is exactly
`53661932375105209/2934348356061848092900`. The individual tangent-family L
thresholds are respectively
`1088006250/455956853`, `7873212500/2636922477`,
`15354930000/4969441039`, `807162500/241694057`, all below 17/5.

The superseded A bound uses `logs/certify_sharpA.log`: Y1,Y2,n,theta and
sigma_infinity are fixed rational values there, and positivity on
`0<u<=1/500000` was certified by exact polynomial root counting. The producer
`code/certify_sharpA.py` starts a numerical SDP and must not be presented as
an experiment-free verifier. The manuscript can specify the retained rational
certificate and its polynomial conditions directly. The final appendix does
so, and replaces root counting by elementary coefficient bounds. For a
polynomial on `0<=u<=1/500000`, retain its constant coefficient and replace
each negative coefficient term by its value at the upper endpoint, dropping
positive terms. The resulting exact lower bounds exceed 3600 for the reduced
Y3 determinant, 3/10 for Y0's first entry and 3/40 for det Y0. An independent
reviewer supplied these bounds and this author rederived all three exactly.

The support-one integer witness in sfree Proposition 16 is hand-checkable:
its four PD matrices have determinants 263, 791, 224 and 64, their products
with M(v) sum to zero, and the homogeneous PSD equalities force X=0.
The scaled witness follows by `Y'_v=Delta^{-1}Y_v Delta^{-1}` with
`Delta=diag(k,1)`. The threshold C3 proof above does not depend on its
numerical producer `certify_support_one.py`, which starts an SDP and was not
rerun. The three retained d checks are exact finite checks, not a substitute
for the continuous analytic proof.

The near-boundary adversarial bracket has successful exact-check receipts in `logs/recheck_adv3.log`,
`logs/rev1/certify_adv3_upper_191_6250.log`, and the independent
`reviews/r2-logs/r2_adv3_bracket.log`. The last distinguishes the exact corner
bound of the binary-float input from its displayed floating-point value.
The full rational primal and dual matrices are not printed in these records.
The companion preserves generation/checking source and successful receipts,
but no replayable fixed witness for this ancillary historical bracket. The
manuscript states that limitation and uses the bracket in no theorem proof.

## Targeted verification actually performed in this audit

- Read-only `cat`, `sed`, and `rg --files` on the named source, reviews, exact
  producers/verifiers and retained logs. No external search was performed.
- Inline SymPy expansion of C3's q0, opposite-face polynomial, and projected
  ray determinant: obtained the formulas above. This was symbolic arithmetic,
  not a corner search or numerical experiment.
- Inline fraction-only check of the five saved lower witness matrices at the
  four required points, using the saved rational heights: all passed.
- Inline parsing of the five cited compressed upper certificates: leaf counts
  match, all eight facets have completed blocks, paths are prefix-free, and
  each exact Kraft sum is one. Leaf exclusions were inspected against both
  verifier implementations and their historical verification logs; this audit
  did not rerun every leaf's exclusion arithmetic.
- SHA-256 of the five files, in table order:
  `3d6fba089912f29b2abbd50fdc1bb478633857596b52c91c8e0b4d544ebd45c5`,
  `cdbe3aef878d9555c2285b9237ccbb449170d34cffe4ea414fca2cb78762be98`,
  `89728c72be118393c71e2ab4586fd9da3434aeed9acb44161dfb4b5a3e6bc14e`,
  `995ff011e4daf55e7d23404524e9b2585e7f35a02d5ad7250a139acc6b72ca62`,
  `7a4b9979dc81b81efee00e7fbf4cf163ea4f7c4c864e28f2fe9c6a36859cb876`.
- Final manuscript arithmetic: a new inline SymPy check verified the dual
  matrix identity and all three coefficient lower bounds above; all passed.
- Targeted depth-only LaTeX document: three calls to
  `pdflatex -interaction=nonstopmode -halt-on-error depth-check.tex`, with the
  shared macros and only the owned main/appendix files plus reference stubs;
  all passed, with no warnings or overfull boxes in the final log.
- Topic-only inline document checks: 40 unique labels, all local references
  resolved or identified as the two foundation references, no malformed
  macros, and no trailing whitespace in the four owned files.

No project-wide verification, CI inspection, solver runs, heuristic searches,
or reproduction of experiment producers was performed.

## Standalone manuscript organization

Explain depth as the curvature scale of the optimal-cost simplex around the
violated vertex. State its precise symmetry group, the cylinder construction,
and the analytic guarantee first. Follow with the fixed-conditioning family
and analytic completed-set collapse, then clearly identified exact
computer-assisted upper constants and rational lower witnesses. The
fixed-coordinate SCIP rule deserves a separate subsection: state the orbit
matrix and completion separately, prove its lower bound, and give the two
exact bad families. Finish with contact geometry, the new approximation lemma,
the interval criteria separating supremum and attainment, and the sharp
cylinder/angle statements. Put the full rational certificate reduction,
witness tables, saved certificate descriptions and the exact adversarial
bracket in the depth appendix. Numerical calibration belongs in the evidence
or computation section with status labels. None of these proofs should cite
a repository note as an essential argument.
