# Integer core variables with continuous forest residuals

Date: 2026-10-02. This extends the
[continuous-core theorem](fan-exploration.md) to large integer intervals
among the core variables. The residual variables remain continuous and
their interaction graph must be a forest. No external search or novelty
claim is part of this derivation.

## Statement

Let \(F(x)=\tfrac12x^TAx+b^Tx+c\) be rational. Split its coordinates
as \(x=(h,z)\), where the supplied core has \(r\) coordinates and
the interaction graph induced by the residual coordinates \(z\) is a
forest. Each residual coordinate has a rational continuous interval.
Each core coordinate has either a rational continuous interval or a
bounded integer interval, with its bounds encoded in binary. Round
integer bounds inward, reject empty domains, and substitute fixed
coordinates before applying the result.

Write \(\mathcal H\) for the resulting mixed core domain and define

\[
 v(h)=\min_zF(h,z),\qquad v^*=\min_{h\in\mathcal H}v(h).
\]

Assume that the optimal core \(h^*\) is unique and that

\[
 v(h)-v^*\ge g\|h-h^*\|^2\qquad(h\in\mathcal H),\qquad g>0.
 \tag{1}
\]

The residual optimizer may be nonunique. Put
\(L=\max(0,\max_{i\in C}A_{ii})\). For \(L>0\), set
\(\kappa=\max(1,L/g)\). There are deterministic algorithms returning
a feasible rational mixed point with certified objective gap at most
\(2^{-q}\), and returning an exact global optimizer, respectively in

\[
 f(r,\kappa)(I+q+1)^K
 \quad\hbox{and}\quad
 f_1(r,\kappa)(I+1)^{K_1}
 \tag{2}
\]

bit operations. The exponents \(K,K_1\) are absolute. No growth
constant is supplied to either algorithm. The numerical cardinalities of
the integer intervals do not multiply these bounds. They enter through
their binary input length and the number of dyadic levels.

A global Hessian bound \(\|A\|_2\le H\) gives \(L\le H\), so
the algorithms are also FPT in \((r,H/g)\). If \(L=0\), solve the
residual problem at the at most \(2^r\) mixed core endpoints; this
already gives an exact optimum without (1). If there is no core, use
the continuous forest oracle directly.

The exact rational forest oracle and the self-contained disjoint-path
special case are described in the continuous-core note. Fixing a feasible
rational mixed core changes only residual linear coefficients and the
constant. Thus its oracle guarantee applies unchanged. This extension
does not place integer variables in the residual forest: every integer
variable belongs to the supplied core.

## Nested mixed cells

Let \(r_c\) and \(r_i\) be the numbers of continuous and integer
core coordinates, with \(r_c+r_i=r\). Choose a power of two \(s\)
at least one, at least every continuous core side length, and at least
every integer core cardinality \(b_i-a_i+1\). Its bit length is
\(O(I)\). Set \(h_j=s2^{-j}\).

For a continuous coordinate \([a_i,b_i]\), use the intervals of length
\(h_j\) anchored at \(a_i\), clipping the final interval to
\(b_i\). These are the isotropic partitions from the continuous-core
proof.

While \(h_j\ge1\), it is an integer power of two. Partition an
integer coordinate into the disjoint sets

\[
 \{a_i+k h_j,\ldots,
       \min(a_i+(k+1)h_j-1,b_i)\},
 \tag{3}
\]

omitting empty sets. Each set contains at most \(h_j\) consecutive
integers and its convex hull has width at most \(h_j-1\). At the
next level it splits into at most two disjoint such sets. At \(h_j=1\)
these sets are singletons. Keep the singleton partition at all later
levels rather than applying a fractional mesh to integer coordinates.

A mixed cell is a product of these coordinate cells. Level zero has one
cell because \(s\) bounds every integer cardinality, not just its
diameter. Each cell has at most \(2^r\) children. Its continuous
interval widths are at most \(h_j\); its integer hull widths are at
most \(h_j\) when \(h_j\ge1\), and zero when \(h_j<1\).
The real hulls of different integer children have gaps, but these gaps
contain no feasible integers. The children cover the mixed feasible set.

Only retained cells are refined. The full partitions in (3) define the
geometry; the algorithm never materializes a large integer interval as
an explicit list of integers or cells.

## Mixed-cell lower bounds

For analysis, define \(\bar v(h)=\min_zF(h,z)\) on the entire real
core box, allowing real values even in integer core coordinates. Its
restriction to \(\mathcal H\) is \(v\). As in the continuous proof,

\[
 \bar v(h)-\tfrac12h^TA_{CC}h
\]

is concave. No optimization over infeasible fractional integer points is
needed by the algorithm.

Let \([\alpha_i,\beta_i]\) be the hull of coordinate \(i\) of a
mixed cell \(B\), and let \(w_i=\beta_i-\alpha_i\). Every hull
corner is feasible for the mixed domain: integer endpoints in (3) are
integers, and a singleton has one endpoint. Define

\[
 m_B=\min_{a\in\operatorname{vert}(B)}v(a),\qquad
 \delta_B=\tfrac18\sum_i\max(A_{ii},0)w_i^2.
 \tag{4}
\]

Independent random rounding of a feasible \(h\in B\) to the two
endpoints in each coordinate, followed by concavity, gives

\[
 v(h)\ge m_B-\delta_B.
 \tag{5}
\]

This is valid for an integer \(h_i\) in its integer hull just as it is
for a real \(h_i\). Its random endpoints are feasible integers. All
off-diagonal terms cancel, and singleton coordinates contribute zero
curvature correction. In particular,

\[
 \delta_B\le\delta_j:=\tfrac18 Lr h_j^2.
 \tag{6}
\]

When \(h_j<1\), the sharper bound
\(\delta_B\le Lr_c h_j^2/8\) holds. If all core coordinates are
integer, every level-\(j\) cell at \(h_j=1\) is a singleton with
zero correction.

## Retained-cell count in both mesh regimes

Evaluate all generated cell corners exactly, maintain the best feasible
objective \(U_j\), discard cells with
\(m_B-\delta_B\ge U_j\), and refine the rest. The proof from the
continuous-core note applies because the mixed children cover the mixed
feasible set. Unless the optimum is already exact, a cell containing
\(h^*\) survives. It gives

\[
 U_j-v^*\le\delta_j.
 \tag{7}
\]

Every retained cell consequently has a corner \(a\) satisfying

\[
 \|a-h^*\|<R_j:=h_j\sqrt{rL/(4g)}.
 \tag{8}
\]

The packing bound must respect the integer cells near and below unit
mesh size:

- For a continuous coordinate, the endpoints form one \(h_j\)-spaced
  lattice and possibly one clipped endpoint. An interval of radius
  \(R_j\) contains at most \(2R_j/h_j+3\) such values.
- If \(h_j\ge1\), integer hull endpoints lie in the two lattices
  \(a_i+h_j\mathbb Z\) and \(a_i-1+h_j\mathbb Z\), together with
  possibly the clipped upper endpoint. There are at most
  \(4R_j/h_j+3\) such values in an interval of radius \(R_j\).
- If \(h_j<1\), integer cells are singletons spaced one unit apart.
  There are at most \(2R_j+1\le2R_j/h_j+1\) eligible integer values
  in the same interval.

A mixed corner belongs to at most \(2^{r_c}\) mixed cells: integer
chunks are disjoint, and only continuous endpoints can belong to two
adjacent cells. Therefore a convenient uniform bound on the number of
retained cells at every level is

\[
 B_{\rm mix}(r,\kappa)
 =2^{r_c}\bigl(2\sqrt{r\kappa}+3\bigr)^r.
 \tag{9}
\]

This bound is independent of integer interval cardinalities, continuous
box aspect ratios, and fractional offsets of continuous lower bounds.
At most \(4^rB_{\rm mix}\) oracle calls per level suffice for child
generation and corner evaluation, apart from level zero.

The global lower bound is the minimum of \(U_j\) and the retained
cell bounds. Since every evaluated \(m_B\ge U_j\), the certified
gap is at most \(\delta_j\). Reaching \(\delta_j\le2^{-q}\)
takes \(O(I+q+1)\) levels. The integer endpoints in (3) and all
continuous mesh endpoints have polynomial bit length in \(I+j\).
The oracle and all bound comparisons have uniform polynomial bit cost.
This proves the approximation bound in (2). If all core coordinates are
integer, the algorithm is exact by the level \(h_j=1\), or sooner.

## Exact output and qualitative termination

The [mixed box-QP height lemma](../geometric-dp/exact-box-qp.md) provides
integers \(R,V\) of polynomial bit length such that some global
optimizer has coordinate denominators at most \(R\), and the optimum
value has denominator at most \(V\). It applies after fixing an
optimal integer assignment for its existence proof; the algorithm does
not enumerate those assignments. Its normalization is \(Q=A/2\), so
the common input denominator includes any required factor of two.
Uniqueness of the mixed optimal core
means that its continuous coordinates inherit the same denominator
bound, regardless of residual nonuniqueness.

Continue refining until the certified interval isolates its unique
denominator-\(V\) rational; this gives \(v^*\). At every subsequent
level keep the incumbent's integer core coordinates and attempt to
reconstruct each continuous core coordinate within radius
\(\rho=1/(4R^2)\), with denominator at most \(R\). Check all mixed
bounds and integrality, solve the residual forest at this candidate
core, and accept only when its exact feasible objective equals \(v^*\).

The acceptance test is sound without knowing \(g\). Once
\(\delta_j/g<\rho^2\), (7) and (1) put the incumbent core within
distance \(\rho\) of \(h^*\). Integer incumbent coordinates then
equal their true optimal integer values, since distinct integers are at
least one apart. All continuous core reconstructions also equal their
true values. Hence the test succeeds after
\(\operatorname{poly}(I)+O(\log\kappa)\) levels, proving the exact
bound in (2).

Finally, a unique mixed optimal core automatically has some positive
projected growth constant. There are finitely many feasible integer core
assignments. On the optimal assignment's continuous slice, the
qualitative lemma in the continuous-core note gives positive growth.
Each other integer assignment has a strictly positive objective gap
above \(v^*\), by compactness and uniqueness of the optimal core.
Taking the least of these finitely many gaps and dividing by the maximum
squared core distance supplies a positive growth bound on the other
slices. Empty cases and a singleton core are immediate. Combining the
bounds gives (1).

This last argument establishes existence only. It does not enumerate
integer assignments or claim a useful uniform lower bound on \(g\).
The exact algorithm therefore terminates on every instance with a unique
mixed optimal core; conditioning controls the FPT runtime guarantee.

## Verification

Fresh independent review found no substantive gap in the mixed-cell
lower bound, the packing estimates above and below unit mesh, exact
height and reconstruction, or the qualitative growth argument. A second
independent reviewer confirmed the growth and height arguments.

The targeted command `python - <<'PY'` ran an inline exact-rational
implementation of mixed-cell refinement, using the independent
active-face verification oracle from
[`check_core_box_bb.py`](check_core_box_bb.py), with seed 20261003. It
passed 15 mixed-core instances, 505 generated boxes, and 710 exact
residual oracle calls. At every level it checked the interval containing
the true optimum and the mesh-gap bound. It also checked integer endpoint
integrality, disjoint integer child coverage, and freezing at unit mesh.
The examples included nonconvex residual slices, a flat residual optimum,
and a nonpositive-core-curvature case certified at the root.

For small integer domains the true optimum came from independent
enumeration of integer assignments and continuous active faces. A
separate large-domain case used its analytically known optimum. Its
integer interval had 67,108,857 feasible values; refinement needed 33
levels, generated 134 boxes, and retained at most three boxes at any
level. That run crossed both mesh regimes and did not enumerate the
integer domain.

The command exited with status zero. These finite tests check the stated
algorithm and boundary behavior; the proof supplies the uniform bounds.
No project-wide checks or CI inspection were performed.

A final targeted `python - <<'PY'` check of this note and its
continuous-core companion passed whitespace and paired math-delimiter
checks. A separate targeted invocation also verified this note's local
source links.
