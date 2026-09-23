# Sequential Peirce compression makes product-ball hard ranks additive

Status: Proved; independently hostile-audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High on the theorem and constants; novelty pending specialist review

## Result

Sequential compression into the Jordan face orthogonal to previously
selected row slacks makes exposed ranks telescope.  As a consequence, the
one-ball hard-objective rank lower bound adds across an arbitrary product of
balls, even when rows share symmetric-cone factors.

Let

\[
                 C=\prod_{a=1}^bB_2^{s_a},\qquad s_a\geq2,
\]

and suppose its extreme-row slack has a globally labelled bi-\(C^1\)
factorization through finitely many symmetric cones:

\[
  1-x_a^Tz_a=
  \sum_i\langle X_i(x_1,\ldots,x_b),Y_i^a(z_a)\rangle_i.           \tag{1}
\]

Assume each row \(Y^a(z_a)\) is a genuine affine-slice dual certificate,
so every positive weighted sum is an exposing slack for the lifted linear
objective.  Suppose every nonray irreducible factor has real dimension at
most \(d\), where \(d\geq3\).  Define

\[
 h_d(s)=
 \begin{cases}
  1,&d\geq s+1,\\[2mm]
  \left\lceil s/(d-2)\right\rceil,&d<s+1.
 \end{cases}                                                       \tag{2}
\]

Then there is a simultaneous contact \(z_a=x_a\), and hence a positive
weighted support objective, whose aggregate exposing slack has total Jordan
rank

\[
                         \boxed{Q\geq\sum_{a=1}^bh_d(s_a).}        \tag{3}
\]

The branch in (2) is essential.  If \(d\geq s+1\), the direct Lorentz lift
of \(B_2^s\) through \(Q_{s+1}\) has exposed rank one.  If
\(d<s+1\) and \(s-1=t(d-2)\), then \(h_d(s)=t+1\): (3) adds the topological
divisibility premium separately for every such source.  Equivalently, with
\(c=d-2\),

\[
 \sum_a h_d(s_a)
 =\sum_a\left\lceil{s_a-1\over c}\right\rceil
  +\#\{a:s_a-1\in\{2c,3c,\ldots\}\}.                              \tag{3a}
\]

For a source ordering \(1,\ldots,b\), there is a sharper adaptive version.
Let \(d_a\) be the largest real dimension of a nonray face remaining after
compressing away the supports selected in stages \(1,\ldots,a-1\).  The
exact ball row with \(s_a\geq2\) has nonzero contact curvature, so such a
nonray face exists and \(d_a\geq3\).  The construction below gives

\[
             Q\geq\sum_a h_{d_a}(s_a)\geq\sum_a h_d(s_a).          \tag{4}
\]

Thus one may maximize the first sum over row orderings and over the hard
contacts supplied at each stage.  Formula (3) is the uniform statement that
does not depend on those choices.

### Exactness of the uniform bound

The bound (3) is sharp.  Let \({\mathfrak F}_d\) be the class of finite,
globally labelled bi-\(C^1\) full-row factorizations in the theorem,
together with a fixed genuine certificate sheet.  For
\({\cal F}\in{\mathfrak F}_d\), let \(Q_{\cal F}(x)\) be the aggregate
exposed rank at a simultaneous contact; it is independent of the chosen
positive row weights because the support of a positive sum is the join of
the summand supports.  Then

\[
 \boxed{
  \inf_{{\cal F}\in{\mathfrak F}_d}
  \sup_{x\in\prod_aS^{s_a-1}}Q_{\cal F}(x)
      =\sum_a h_d(s_a).}                                          \tag{4a}
\]

For the upper construction, handle each source separately.  If
\(d\geq s_a+1\), use the direct Lorentz lift through \(Q_{s_a+1}\).  In the
strict-cap case, partition the \(s_a\) Euclidean coordinates into
\(h_d(s_a)\) nonempty groups \(G\) of size at most \(d-2\), introduce
lifted scalars \(t_G\) with \(\sum_Gt_G=1\), and impose

\[
 A_G(t_G,x_G)=\left({1+t_G\over2},{1-t_G\over2},x_G\right)
        \in Q_{|G|+2}.                                             \tag{4b}
\]

This is equivalent to \(t_G\geq\|x_G\|^2\), so its projection is exactly
the ball.  For a boundary objective \(z\), define

\[
 B_G(z)=\left({1+\|z_G\|^2\over2},
             -{1-\|z_G\|^2\over2},-z_G\right).                    \tag{4c}
\]

Then \(B_G(z)\) is a nonzero Lorentz-boundary element and, for every
feasible lifted point,

\[
\langle A_G(t_G,x_G),B_G(z)\rangle
       ={t_G+\|z_G\|^2\over2}-x_G^Tz_G.                            \tag{4d}
\]

Here the Lorentz factor uses the standard Euclidean self-dual pairing.  If
the ambient convention uses the Jordan trace pairing, rescale \(B_G\) by
the fixed normalization constant; its support and rank are unchanged.

Summing (4d) gives \(1-x^Tz\), so these are genuine affine-slice
certificates.  At every diagonal contact each group contributes one exposed
Jordan-rank unit, even when \(x_G=0\).  Taking separate group factors for
all sources gives \(Q=\sum_ah_d(s_a)\) at every simultaneous contact.  The
construction is polynomial, globally smooth, strictly feasible, and every
factor dimension is at most \(d\), proving the upper half of (4a).  The
sequential theorem proves the lower half.

## 1. A support-join compression identity

Let \(V\) be a Euclidean Jordan algebra with unit \(e\), let \(K\) be its
cone of squares, and let \(c\) be an idempotent.  Put \(f=e-c\).  For
\(y\in K\), write \(s=\operatorname{supp}y\) and

\[
                    t=\operatorname{supp}(P(f)y),                  \tag{5}
\]

where \(P(f)\) is the positive Peirce projection onto the face algebra
\(V(f,1)\).  Then

\[
                       \boxed{c\vee s=c+t},                        \tag{6}
\]

and therefore

\[
 \boxed{
  \operatorname{rank}(P(f)y)
   =\operatorname{rank}(c\vee\operatorname{supp}y)
      -\operatorname{rank}c.}                                     \tag{7}
\]

This holds in every Euclidean Jordan algebra, including spin factors and
the Albert algebra.

To prove it, note first that \(t\leq f\).  Put \(g=f-t\).  Self-adjointness
of \(P(f)\) and the definition of support give

\[
          \langle g,y\rangle=\langle g,P(f)y\rangle=0.
\]

Positive elements with zero inner product are Jordan-orthogonal, so
\(s\perp g\), whence \(s\leq e-g=c+t\).  This proves
\(c\vee s\leq c+t\).  Conversely, let \(h=e-(c\vee s)\).  Since
\(h\perp c\), one has \(h\leq f\), and

\[
          \langle h,P(f)y\rangle=\langle h,y\rangle=0.
\]

Thus \(h\perp t\), so \(t\leq e-h=c\vee s\).  Hence
\(c+t\leq c\vee s\), proving (6).  Since \(c\perp t\), ranks add and
(7) follows.

## 2. Sequential compression preserves the next full row

Choose the row contacts inductively.  After selecting
\(x_1,\ldots,x_{a-1}\), define in each factor

\[
 c_i^{a-1}=\bigvee_{j<a}\operatorname{supp}Y_i^j(x_j),
 \qquad f_i^{a-1}=e_i-c_i^{a-1}.                                  \tag{8}
\]

Fixing a prior row \(j<a\) at contact makes its slack zero for every choice
of all unrelated primal coordinates.  Every summand in (1) is nonnegative,
so termwise Jordan complementarity gives

\[
             X_i(x)\circ Y_i^j(x_j)=0
             \quad\text{for all remaining source coordinates}.   \tag{9}
\]

Consequently \(X_i(x)\) lies in the face algebra
\(V_i(f_i^{a-1},1)\).  Fix arbitrary temporary values of the future primal
coordinates and vary \(x_a,z_a\).  Self-adjointness of the Peirce
projection turns (1) into the exact factorization

\[
  1-x_a^Tz_a
   =\sum_i\left\langle X_i(x),
          P(f_i^{a-1})Y_i^a(z_a)\right\rangle_i.                  \tag{10}
\]

The compressed dual factors remain cone-valued and \(C^1\).  The primal
factors lie in the corresponding face cones.  Faces of symmetric cones are
symmetric cones; in particular, a rank-two face of the Albert cone is the
spin factor \(H_2(\mathbb O)\cong Q_{10}\), and its rank-one faces are
rays.  Every remaining nonray face has dimension at most the original
factor dimension and hence at most \(d\).

The one-ball support-cover theorem can now be applied to (10).  That theorem
uses only the globally labelled \(C^1\) full-row factorization; the
compressed row need not itself be an affine-slice certificate.  If
\(d_a<s_a+1\), it selects \(x_a\) for which

\[
 \sum_i\operatorname{rank}
       \bigl(P(f_i^{a-1})Y_i^a(x_a)\bigr)
       \geq\left\lceil{s_a\over d_a-2}\right\rceil.               \tag{11}
\]

If \(d_a\geq s_a+1\), fix any dual boundary point \(z_a=v\) and evaluate
(10) at \(x_a=-v\).  Its left side is two, so some compressed dual factor
at \(v\) is nonzero.  Choosing the contact \(x_a=z_a=v\) makes the same
rank sum at least one.  These are the two branches of \(h_{d_a}(s_a)\).
Later changes to the temporary future primal coordinates do not affect the
chosen dual value \(Y_i^a(x_a)\), so the induction is consistent.

## 3. Telescoping to the aggregate exposed rank

After choosing \(x_a\), set

\[
 c_i^a=c_i^{a-1}\vee\operatorname{supp}Y_i^a(x_a).                \tag{12}
\]

The compression identity (7) gives the exact increment

\[
 \operatorname{rank}c_i^a-\operatorname{rank}c_i^{a-1}
 =\operatorname{rank}\bigl(P(f_i^{a-1})Y_i^a(x_a)\bigr).          \tag{13}
\]

Sum (13) over factors and stages and use (11).  Since \(c_i^0=0\),

\[
            \sum_i\operatorname{rank}c_i^b
              \geq\sum_a h_{d_a}(s_a).                            \tag{14}
\]

For arbitrary positive weights \(\lambda_a\), positivity implies

\[
 \operatorname{supp}\!\left(\sum_a\lambda_aY_i^a(x_a)\right)
     =\bigvee_a\operatorname{supp}Y_i^a(x_a)=c_i^b.               \tag{15}
\]

Thus the left side of (14) is exactly the aggregate exposed rank \(Q\),
which proves (3)--(4).  The initial genuine-certificate hypothesis makes
the weighted uncompressed sum in (15) a dual exposing slack for the final
lifted objective.

## 4. A factor-aware rank-budget refinement

The sequential argument also adds the sharper finite-factor curvature
budgets.  At stage \(a\), split the remaining nonray faces into irreducible
factors.  Let their Jordan ranks and Peirce constants be \(R_{ia}\) and
\(\alpha_{ia}\), and define

\[
 g_a=\min\left\{\sum_iq_i:
   q_i\in\{0,\ldots,R_{ia}\},\quad
   \sum_i\alpha_{ia}q_i(R_{ia}-q_i)\geq s_a-1\right\}.            \tag{15a}
\]

The actual compressed primal and dual ranks \(p_i,q_i\) at any current-row
contact satisfy \(p_i+q_i\leq R_{ia}\).  Peirce mixed-curvature rank
therefore gives

\[
       s_a-1\leq\sum_i\alpha_{ia}p_iq_i
                \leq\sum_i\alpha_{ia}q_i(R_{ia}-q_i).             \tag{15b}
\]

Thus the nonray compressed rank is at least \(g_a\) at every contact.  The
topological choice in Section 2 makes the total compressed rank, including
rays, at least \(h_{d_a}(s_a)\).  Both statements hold at the selected
contact, so exact telescoping strengthens (4) to

\[
                     \boxed{Q\geq\sum_a
                     \max\{g_a,h_{d_a}(s_a)\}.}                   \tag{15c}
\]

There is a useful closed uniform corollary.  Suppose at most \(L\) factors
come from one simple family of Peirce constant \(\alpha\), each of order at
most \(R_0\).  For \(Q_0=uL+t\), \(0\leq t<L\), put

\[
 {\cal C}_{\alpha,R_0}(L,Q_0)=\alpha\bigl[
 (L-t)u(R_0-u)+t(u+1)(R_0-u-1)\bigr]                              \tag{15d}
\]

and define

\[
 Q_{\min}(v)=\min\{Q_0\in\{0,\ldots,LR_0\}:
                   {\cal C}_{\alpha,R_0}(L,Q_0)\geq v\}.          \tag{15e}
\]

If the set is empty, no such factorization exists.  Otherwise, padding
missing factors with rank zero and using \(R_{ia}\leq R_0\) shows
\(g_a\geq Q_{\min}(s_a-1)\).  Consequently

\[
 Q\geq\sum_a\max\{h_d(s_a),Q_{\min}(s_a-1)\}.                    \tag{15f}
\]

For \(b\) equal source balls, the right side is \(b\) times the common
term.  The actual adaptive \(g_a\) can be larger than the padded balanced
envelope \(Q_{\min}\); equality is not asserted.

The additive topology can make (15f) strictly stronger than applying the
capacity envelope once to the total tangent dimension.  For three
three-dimensional Lorentz factors (\(L=3,R_0=2,\alpha=1,d=3\)) and sources
\(B_2^2\times B_2^3\), the total dimension is three and the global envelope
only gives \(Q\geq Q_{\min}(3)=3\).  Formula (3) gives instead

\[
                   Q\geq h_3(2)+h_3(3)=1+3=4.                    \tag{15g}
\]

## 5. Bounded-metric iteration consequence

Apply the exposed-support-minor distance theorem to the hard objective in
(15).  With

\[
                       H=\sum_a h_d(s_a),                          \tag{16}
\]

the standard Jordan log-determinant metric has asymptotic distance-to-
accuracy coefficient at least \(\sqrt H\):

\[
                     d_F(x^c,\{\operatorname{gap}\leq\epsilon\})
                     \geq \sqrt H\log(1/\epsilon)-O(1).            \tag{17}
\]

The same coefficient lower bound holds for every classified self-scaled
barrier because its weighted exposed rank is at least \(Q\).  If a counted
round has intrinsic displacement at most \(B_0\), then

\[
                         T\geq {\sqrt H\over B_0}
                                  \log(1/\epsilon)-O(1).            \tag{18}
\]

For at most \(m\) feasible local chords of starting norm at most \(R<1\)
per round, one may take \(B_0=m\log(1/(1-R))\).  The exact finite endpoint
constant remains the support-determinant scale of the selected certificate;
(17)--(18) state the uniform leading coefficient only.

## Scope and novelty boundary

The result requires globally labelled bi-\(C^1\) full-row factors and a
genuine globally fixed dual-certificate sheet.  It does not apply to
unlabelled or merely pointwise factorizations, arbitrary coupled barriers,
unbounded metric moves, or quantum procedures that do not output a sequence
of feasible classical iterates.

The support lattice, Peirce projections, and face structure are classical.
The candidate new step is to apply the exact support-join compression
identity sequentially to full ball rows, preserving each next row
factorization and making the one-ball topological hard ranks additive.  No
claim of literature priority is made pending specialist review.

A targeted primary-source search found no statement of this sequential
rank theorem.  Important neighboring work includes
[Gouveia--Parrilo--Thomas](https://arxiv.org/abs/1111.3164) on the general
lift--slack-factorization equivalence and products of lifts;
[Fawzi--Parrilo](https://arxiv.org/abs/1311.2571) and
[Fawzi--Safey El Din](https://arxiv.org/abs/1705.06996) on lower bounds for
products of fixed-size PSD cones; and
[Fawzi--Gouveia--Parrilo--Robinson--Thomas](https://arxiv.org/abs/1407.4095)
on topology of finite-matrix PSD factorization spaces.  Those results do
not study a globally \(C^1\) factor field over product-ball contact
manifolds, objectivewise aggregate Jordan rank, or sequential Peirce-face
compression.  Accordingly, this is not claimed to be the first lower bound
for products of small cones or the first topological study of factorization
spaces; only the stated synthesis is a plausible novelty candidate.

The one-ball support theorem and the exposed-minor distance theorem are in
[Exposed Jordan rank forces bounded-Dikin iterations on symmetric-cone
lifts](2026-09-04-symmetric-cone-exposed-rank-dikin-lower-bound.md).

## Independent hostile audit

An independent audit rederived the support-join identity (6) in an
arbitrary Euclidean Jordan algebra and checked each order relation used in
the proof.  It then verified that prior-row complementarity holds on the
whole remaining cylinder, that Peirce compression preserves the exact next
row factorization, and that future-coordinate changes do not affect earlier
support choices.  It checked the face classification explicitly, including
the Albert rank-two face \(H_2(\mathbb O)\cong Q_{10}\), and verified that
Jordan rank in a face agrees with rank in the original block.

The audit also checked both branches of (2), exact telescoping in (13), and
the support-of-a-positive-sum identity (15).  It emphasized the certificate
boundary now stated above: the compressed dual row need not be an
affine-slice certificate and is used only in the factorization theorem;
the final uncompressed weighted sum is the genuine certificate needed for
the Dikin-distance consequence.  No mathematical defect or constant change
was found.

A follow-up hostile audit checked the factor-aware refinement
(15a)--(15f).  It rederived (15b) in every remaining face, including Albert
and spin faces, and verified that ray ranks must remain in the topological
and telescoping counts while being omitted from the zero-curvature budget
\(g_a\).  It also caught and repaired an overstatement in the draft: the
actual adaptive \(g_a\) is bounded **below** by the padded balanced-envelope
\(Q_{\min}\), but need not equal it.  With that correction, the adaptive
and uniform formulas passed.

The same audit checked the exact minimax construction (4a)--(4d).  It
identified the necessary affine-lift presentation with explicit variables
\(t_G\), verified the Lorentz-cone normalization and the certificate
identity at every feasible lifted point, and confirmed that each contact
factor is nonzero rank one even when a coordinate group vanishes.  It also
required the minimax class to include a fixed globally labelled certificate
sheet rather than ranging over bare lifts.  With those points stated in
(4a)--(4d), sharpness passed.
