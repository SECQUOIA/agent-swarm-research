# Stage 6b, round 1, independent review 2

Verdict: **pass; no major or minor correction requested**.

I independently reviewed the complete appendix, its author and literature
records, snapshot, exact checker, wrapper and supplement changes, and the
stage coverage entries. I also read the underlying research note and the
relevant primary-source statements and proofs. I did not read other current
review reports or coordinate findings. Only this report was written.

## Directional bound

The assumptions at `appendices/three-dimensional-span.tex:11` support the
cone geometry used throughout. Evaluation at a strictly feasible lift is
strictly negative for every nonzero vector of nonnegative coefficients, so
no such combination vanishes. The cone is pointed and spans a space of
dimension three. Its normalized section is a compact two-dimensional
polygon. Consequently it has equally many extreme rays and facets, with
two extreme generators on each facet. Removing non-extreme generators
preserves both the strict feasible set and the cone of aggregation matrices.

The HHC argument at line 52 checks the required dimension: every linear
homogeneous hyperplane has dimension `n >= 3`, the positive definite
combination remains positive definite upon restriction, and the many-form
image is a linear image of the convex three-form image. It does not infer
HHC merely from convexity of the unrestricted image. Thus the cited strict
full-hull theorem applies to the original system.

For the directional exit at line 60, a positive definite matrix cannot
belong to the generated cone, so the set of negatively evaluated facets
is nonempty. The minimum ratio is finite and nonnegative, remains feasible
for all other facets, and attains a selected facet. The endpoint cannot
vanish: that would make the starting nonzero good matrix negative definite,
contradicting its at-most-one-negative-eigenvalue condition in the stated
dimension. The proof correctly excludes globally redundant good cuts before
using the PSD-improvement lemma.

The representation check at lines 77–79 is essential and correct. Two
nonnegative representations of the initial and final matrices provide a
signed coefficient increment with PSD matrix and nonnegative final
coefficients. This meets the source lemma's actual hypothesis even when
the original matrices are dependent. It proves both strict goodness and
domination; PSD monotonicity alone would not establish the former.

Every selected facet is supported on two retained original generators.
The pair-support reduction is applied relative to the full original set,
not a larger two-row feasible set. Its assumptions hold, and its conclusion
supplies at most two cuts per facet. Empty good-cut families contribute
nothing. The domination argument proves equality with the full hull.

Finally, `E` outside the negative matrix cone has strictly positive
evaluation under at least one inward facet functional. Perturbing it by a
small positive definite matrix retains that sign and makes it positive
definite. At least one facet is therefore absent from `J_-`, which proves
the conditional `2k-2` bound. No unproved complementary-case bound or
multiplier-selection algorithm is used.

## Ellipsoid family

The example at line 106 is valid already for its explicitly stated
`n >= 2`. All leading coefficients are strictly positive. The feasible
set is a nonempty bounded open convex intersection, and the signed
Vandermonde identity proves that its homogeneous span is exactly the
displayed three-dimensional space containing a positive definite form.

The witness identity at line 133 is exact. At witness `p_i`, only the
designated original row has zero slack; every other row is strictly
negative. Thus every exact strict aggregation representation, including an
infinite representation, must include the designated coefficient ray.
The original rows give the matching upper bound and have precisely one
negative homogeneous eigenvalue. The same evaluations expose each original
matrix ray, establishing `k=m` rather than merely counting input rows.

The finite weak lower bound uses the necessary additional argument. If a
finite family omits a designated ray, every chosen cut is strict at that
witness and hence on a common neighborhood. A small radial dilation lies
outside the corresponding ellipsoid while still satisfying all chosen
cuts. Conversely radial contraction toward the origin proves that the
original weak intersection is the closure of the strict set. The text
correctly avoids extending finite-neighborhood reasoning to infinite weak
families.

## Augmented complementary-cone example

The two added inequalities at line 175 change the strict feasible set.
The proof does not call them redundant there. The proposed small midpoint
perturbation can avoid the finitely many prohibited scalar and vector
values while staying inside the open set. Both perturbed points satisfy
the two added strict rows. Hence the ordinary hull of the new set is
exactly the old convex open set, including points on the removed subspaces.

All old boundary witnesses remain strictly negative on both new rows.
They still expose the original matrix rays and still require all `m`
original coefficient rays in every strict aggregation description. The
zero constant coefficient distinguishes the two new rays: a nonnegative
representation of either cannot use any original generator. Both are
extreme and distinct, giving exactly `k=m+2`.

The identity at line 208 uses nonnegative coefficients and places the
negative constant basis matrix in the new cone. The PSD cone within this
diagonal three-dimensional span is precisely the nonnegative orthant in
the displayed basis. Its negative is therefore contained in the generated
cone, as claimed. This verifies the complementary geometric condition
without assuming it from the presence of just one negative definite matrix.

The original rows remain good for the new strict set because its hull is
the original convex intersection. They provide exactly `m` cuts. The
added weak rows hold everywhere, so the weak feasible set is unchanged.
It is compact and full-dimensional; a point with an active ellipsoid
inequality cannot be interior, while radial contraction proves regularity.
Positive definite original leading matrices exclude nonzero points at
infinity. The same finite-neighborhood witness proof gives the exact weak
count, even among arbitrary nonnegative aggregation families.

Since `m` is arbitrary, this example genuinely refutes a constant two-bound
for the complementary general-cone case, including the relevant regular
closed-set hypotheses. Its count `m=k-2` does not refute an unconditional
`2k-2` bound. The concluding paragraphs state this distinction precisely.
The final inertia example also supports exactly its stated limitation:
individual inertia bounds do not justify arbitrary addition.

## Sources, coverage, and actual checks

- Read the local primary BDS v2 passages and freshly opened
  [arXiv:2210.01722v2](https://arxiv.org/html/2210.01722v2). Proposition 2.22
  is the appropriate versioned facet-bound locator. Propositions 9.1 and
  9.6 provide the PSD improvement and full-set pair-support conclusions
  used here. The appendix does not import the source's additional
  determinant-root assertions.
- Read BD v1 Propositions 8.6 and 8.10 and their surrounding arguments,
  and freshly opened [the primary version](https://arxiv.org/html/2405.18282v1).
  The former supports the credited three-generator directional antecedent;
  the latter is a three-generator result with closed-set hypotheses.
  The appendix refutes a proposed extension, not the cited theorem.
- The classical facet argument and three-form convexity input receive
  explicit credit. The directional refinement and examples are described
  as supporting observations, with no broad first-result or optimal-count
  assertion. No bibliographic addition is needed for these cited inputs.
- Compared the underlying research note with the appendix and coverage
  record. The proved supporting material is included, and the note's
  speculative general-cone two-bound is resolved negatively rather than
  imported as an assumption. A best possible general count is explicitly
  outside the established claims.
- Read and ran
  `python3 paper-quadratic-aggregation/supplement/check_three_dimensional_span.py`.
  It passed the exact Vandermonde, witness-numerator, and negative-cone
  coefficient identities and 1,235 rational witness evaluations. The
  integer polynomial arithmetic and rational sign checks match their
  stated finite scope. They are not used to certify the universal hull or
  HHC arguments.
- Checked snapshot hashes for the appendix, exact checker, main wrapper,
  supplement README, author report, and literature report: all matched.
  Checked the dedicated stage 6b LaTeX and BibTeX logs for warnings,
  undefined references, and overfull/underfull boxes: no matches.
- No manuscript change, new build, formal rerun, project-wide verification,
  CI inspection, or subagent was used.
