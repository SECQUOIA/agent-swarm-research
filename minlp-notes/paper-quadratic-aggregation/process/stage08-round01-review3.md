# Stage 8, round 1: independent whole-manuscript review 3

Disposition: **clean; no major or minor correction requested**.

I read `main.tex`, every main section from `00-introduction.tex` through
`10-discussion.tex`, and both included appendices. My detailed emphasis was
the strict PDLC theorem and the three-dimensional matrix-span appendix. I
assessed those arguments directly, without treating the previous stage
reports as evidence of correctness. I also checked their interfaces with
the definitions, certificate theorem, infinite example, approximation
results, and concluding claims.

## Strict PDLC transfer

The external input is stated with the necessary independence, strict
interior, regularity, and no-points-at-infinity conditions. I inspected
Theorem 1.4 and its proof, Propositions 8.6, 8.7, and 8.10, and the standing
definition of permissible/good aggregations in the primary BD preprint
(`/tmp/quadratic-paper-literature/bd.txt`). Its proof explicitly includes
dimensions one and two, and its PDLC portion does not impose smoothness
of the spectral curve. I independently reopened the official arXiv records
for [BD](https://arxiv.org/abs/2405.18282) and
[BDS](https://arxiv.org/abs/2210.01722), and searched for the strict
four-aggregation and certificate-conjecture developments. This limited
search did not identify a conflicting priority claim; it is not an
exhaustive proof of novelty. The manuscript appropriately acknowledges
Dunbar's stronger regular nonstrict statement and isolates the strict
transfer as its contribution.

I checked the following potentially fragile steps:

- Properness excludes a common strict negative leading direction. Adding
  positive definite leading blocks therefore gives no nonzero common
  nonpositive direction, and the normalized unbounded-sequence argument
  correctly proves compactness of every inward weak set.
- The three proposed perturbation matrices are independent even when
  `n = 1`. A coordinate minor with nonzero cubic leading coefficient
  rules out dependence except at finitely many parameters. PDLC and one
  common strictly feasible point persist for sufficiently small parameters.
- The countable-base sublevel lemma is valid: every exceptional level is
  the infimum on a basic open set containing a point at that level.
  Avoiding these levels gives precisely the regular weak sets needed by
  the external theorem. No unproved Sard-type assertion is used.
- Deleting globally nonpositive quadratics before strictification is
  essential and is done correctly. A quadratic with a zero local maximum
  has its global maximum there; thus each retained weak sublevel has the
  claimed strict interior. The finite-intersection interior identity and
  the interior-of-closure identity apply in this setting.
- Simplex normalization prevents zero limiting weights. Evaluation at the
  common strict point makes each limiting homogeneous matrix have exactly
  one negative eigenvalue. One common subsequence is used for the four
  matrices and their oriented eigenvectors. For each fixed point of the
  original strict set, eventual inward feasibility proves the same
  orientation; strict evaluation then excludes a zero limiting inner
  product. This establishes goodness on the entire hull, not merely
  pointwise nonstrict validity on the original set.
- The reverse inclusion uses strictness of only four limiting inequalities
  and eventual membership in one inward hull. It does not inadvertently
  prove only a closure equality.
- The four-ray sharpness argument includes all nonzero good multipliers,
  and uses the repeated negative leading eigenvalue only for `n >= 3`.
  Its witness argument and the already proved upper bound legitimately
  establish the displayed exact four-cut description. No low-dimensional
  sharpness is claimed.
- The oriented SOC closure argument mixes with a common strict point.
  The half-ball example correctly demonstrates why simply weakening the
  original quadratic signs is insufficient.

## Many rows in a three-dimensional span

I checked BDS Proposition 2.22 and Propositions 9.1 and 9.6 directly in
`/tmp/quadratic-paper-literature/bdsv2.txt`. The appendix uses these results
within their hypotheses. Strict evaluation gives a pointed cone with a
compact polygonal base. HHC follows by restricting a PDLC basis triple to
hyperplanes of dimension at least three, then taking the linear image
corresponding to the original rows.

For a positive definite direction, the minimum ratio over negatively
oriented facet normals keeps all inequalities valid until a selected facet
is reached. The improved matrix cannot be zero: that would make the
original good matrix negative definite. Nonnegative coefficient
representations of the original and improved matrices explicitly verify
the PSD-improvement lemma's hypothesis. The pair-support reduction is
correctly applied to goodness relative to the full set, not to a two-row
subsystem. The conditional `2k - 2` conclusion follows from a PSD direction
with a positive facet evaluation and a small PD perturbation.

The ellipsoid witness identity exposes every original matrix ray. Appending
the two negative square rows leaves the weak set unchanged and removes only
two coordinate subspaces from the strict set; the small symmetric
perturbation proves equality of its ordinary hull with the original open
ellipsoid intersection. The two added rays are extreme in the zero-constant
face. The identity yielding the negative constant basis vector proves the
required complementary cone inclusion. Every original witness is strict
for both added rows, so the indispensable-ray count survives enlargement
of the aggregation cone. The same finite-family neighborhood argument
establishes the weak count. Thus this really refutes a general-cone
constant/two-bound under that complementary condition, including for
regular compact weak sets. It does not refute the actual three-generator
BD result or an unconditional `2k - 2` bound, and the text says so.

## Whole-manuscript assessment

The distinction between globally convex certificates and good
aggregations remains consistent. Strict and weak feasible sets, ordinary
hulls and their closures, and original-variable descriptions versus lifts
are distinguished where the proofs need them. The coefficient-cone
normalization in the certificate proof retains a nonzero limit even when
simplex-normalized certificates could cancel. The Shor section uses an
explicit closure statement and proves its whole-space assertion without
assuming projection closedness.

I checked the Gram-fiber interval argument, singular fidelity
regularization, all-dimensional two-point hull decomposition, and
quartic-arc countability obstruction. The approximation proof tests only
nonnegative directions of its two-by-two matrix, and its lower bound
allows arbitrary interior good multipliers. The single-objective result
does not contradict the uniform approximation lower bound. The formal
overview distinguishes the paper's stronger lower constant and shorter
SDP test from the formally verified formulations, and explicitly lists
unformalized results; it does not claim formal verification of the PDLC
argument reviewed here.

The main narrative is coherent despite the breadth of the material.
The introduction identifies the three conjectures and the exact new
claims, the sections develop them in a logical order, and the appendices
keep the local-certificate application and many-row refinement from
interrupting those proofs. The literature qualifications are sufficiently
precise: classical fidelity, duality, inverse-square approximation, SDP
lifting, and the existing four-bound/sharp example are credited. I found
no mathematical gap, inconsistent hypothesis, unsupported strengthening,
or mandatory readability correction in this review.

## Targeted checks actually run

Both commands exited successfully:

```
python3 paper-quadratic-aggregation/supplement/check_four_aggregation.py
python3 paper-quadratic-aggregation/supplement/check_three_dimensional_span.py
```

The first checked the PDLC identity, strict point, radical/rational witness
slacks, and ray decomposition. The second checked the Vandermonde,
witness-numerator, and negative-cone identities plus 1,235 rational witness
evaluations. These finite checks support the algebra; the universal
regularization, limiting, and cone arguments were reviewed mathematically.
I did not run project-wide verification, inspect CI, or independently rerun
the complete portable Lean project during this review.
