# Stage 5A author record

Status: author integration complete; five independent formal reviews remain mandatory.

## Work units and verification

The stage author developed `11d-tree-distance.tex` and used three bounded
authors for disjoint sections: exposed-minor/affine-PSD movement (`11a`),
primal--dual geometry and effective product-ball activity (`11b`), and
concrete formulations (`11c`). Their source-level records accompany this
file. The stage author personally reads each final section, verifies the
proofs and constants, integrates references, and builds the manuscript.
These author checks are not the user's five independent formal reviews.
All three bounded authors have finished. The stage author and root have each
read all four integrated sections and independently checked their mathematical
arguments. Root's only requested adjustment was removing a root-index/radial
scalar notation collision in the explicit tree curve; it is corrected.

## New weighted tree development

The root's candidate is valid under the displayed fixed weighted barrier.
For a fixed tree and unit objective, define active nodes by nonzero norm of
the objective on their descendant leaves. With weights omega_v >= 1, the
exact leading target-distance coefficient is

    sqrt(K), K = sum_active omega_v + (1/2) sum_inactive omega_v.

The manuscript gives a complete proof and the stronger two-sided remainder:
lower `sqrt(K) log(1/epsilon) - O(1)`, upper
`sqrt(K) log(1/epsilon) + O(log log(1/epsilon))`.

Independent checks of the root derivation:

- For a Lorentz block with q = x^T J x, the inverse Hessian of -log q is
  `xx^T - (q/2)J`. A fixed null dual s therefore gives squared dual norm
  one for `d log(s^T x)`. This uses ordinary Euclidean pairings and avoids
  a possible factor-two Jordan normalization error.
- The genuine support pairings telescope over *every* link to the entire
  objective gap; inactive duals are exactly zero. An inactive child axis
  lies perpendicular to the normalized active parent support direction.
  This proves its square is at most `2 gap / alpha_parent`; monotonicity of
  descendant axes supplies the same bound throughout the inactive subtree.
- The potential weights are omega on active rank-one logarithms and
  omega/2 on inactive determinant logarithms. Their squared ambient dual
  norms add to K; affine restriction decreases the dual norm.
- The upper curve sets active determinants to h and inactive ones to
  h/lambda^2, where h=exp(-lambda). Subtree recursion supplies an exact
  positive-sheet feasible completion with root one. Each active squared
  speed tends to one and each inactive squared speed to one-half.
  Error bounds integrate to the stated logarithmic-logarithmic remainder.
- Weighted central stationarity has q_v/omega_v constant, so the central
  coefficient is sqrt(sum omega). The ratio to the optimal target distance
  is exactly sqrt(W/K) in the limit. Zero-weight independent trees can stay
  fixed; positive objective weights affect fixed constants, not the leading
  coefficient. Constants are not uniform as subtree support vanishes.

This sharpens the existing norm-tree finite-accuracy statement without
discarding its useful uniform constants. It concerns the specified barrier,
not an optimal choice among all barriers or an unrestricted algorithm.

## Literature and overlap

Read the actual companion formulation section and its primal--dual section,
not just the workbench status notes. The bounded authors additionally
compared its distribution section. The companion already contains:
weighted all-EJA exposed-minor distances and sharp full-cone coefficient;
dimension-only primal--dual bounds; speed splitting and the one-active and
unique-optimizer product-ball examples; Q1/Q2 head-tail constants, schedules,
and decay orders; uniform tree distances and exact central paths; grouped
and packed movement. These are explicitly attributed background here, with
self-contained proofs. The new weighted inactive-subtree distance coefficient
is absent from the companion.

Primary online texts opened during this stage:

- Hauser--Guler, arXiv:math/0103196, especially Theorem 5.5; the classification
  uses irreducible-factor coefficients at least one.
- Nesterov--Todd, `https://people.orie.cornell.edu/miketodd/NTRiemann.pdf`;
  its feasible small-gap theorem is classical and is not relabeled as a new
  endpoint-set extension.
- Nesterov--Nemirovski,
  `https://www2.isye.gatech.edu/~nemirovs/FCM_Riem_2008.pdf`;
  general primal central-path/geodesic comparisons are prior work.

A targeted search for norm-tree Riemannian distances and boundary behavior
did not find an earlier explicit weighted active/inactive coefficient. This
negative search is not a proof of priority. Duistermaat (2001), DOI
10.3233/ASY-2001-448, is locally marked unread with no full text, and its
publisher PDF is not accessible as full text in the current search. No claim
about its detailed theorem scope is inferred from its title or unread local
metadata. The paper therefore states precisely the result established here
without claiming an exhaustive priority classification.

## Validation

- Added all four main sections before the manuscript's single appendix.
- Added primary references NT2002, NesterovNemirovski2008,
  HauserGuler2002, and BoydVandenberghe2004. Expanded the companion citation
  note to name its overlapping distribution and primal--dual material.
  Companion numerical section references were checked against its compiled
  labels, rather than inferred from source file prefixes.
- Built with `conda run -n qipm --live-stream make` in the deliverable folder.
  The final integrated PDF has 133 pages. The final LaTeX log has no warnings,
  undefined references/citations, duplicate labels, or overfull/underfull boxes.
- Appended complete Stage5A source dispositions without running the
  destructive one-off source-map generator. Existing workbench, literature,
  companion manuscripts, and the preexisting formal directory were not edited.
- No unresolved author-identified mathematical issue remains. This statement
  is preliminary to the mandatory five independent formal stage reviews;
  the full paper still requires Stage5B, Stage5C, and whole-manuscript review.
