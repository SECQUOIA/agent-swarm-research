# Independent review of the numerical chapter and comparison tools

Review scope: `sections/08-computation.tex`, `appendices/D-comparison-tools.tex`,
and `companion/`. I reconstructed the mathematical arguments and compared
the numerical claims with the archived note, compact tables, selected source
implementations, and full-precision reporting outputs. I did not conduct
literature research, run an optimizer, generate an instance, or inspect CI.

## Conclusion

I found no error in the mathematical results in Appendix D and no material
disagreement between the chapter's tables and the archived outcomes. The
chapter preserves the distinctions that matter: computed versus certified
bounds, local auxiliary variables versus shared higher moments, constructed
versus naturally generated gaps, and selective comparisons versus complete
systems. Its computational conclusions are appropriately limited.

No critical or major finding remains. The findings below concern notation,
clarity, and identification of data formats.

## Findings and author responses

1. **Moderate, corrected: normalized hull notation.** The first version of
   Appendix D used `\widehat{\mathcal Q}_3` for the normalized matrix moment
   hull, while Section 2 uses that symbol for the homogeneous cone. This
   could change the meaning of the hull-depth membership test. The author
   changed the normalized matrix hull to `\mathcal M_3` in both owned files.
   I checked the replacements. The cone and the normalized hull are now
   distinct.

2. **Minor, corrected: representative instance identification.** The
   representative table omitted the random seeds, although several classes
   contain instances with the same displayed dimensions. All eight selected
   rows use seed 1. The caption now states this, which identifies them in
   the companion records.

3. **Minor, corrected:** “The comparisons introduce no moment
   outside this pattern” should specify “no first or second moment,” since
   the `K` implementation does introduce higher monomials. The restriction
   of recorded pairs and triples is correct; the proposed change avoids a
   possible conflict with the following description of `K`. The author
   made the change, which I checked.

4. **Minor, corrected in substance:** The statement that the family closes
   all hard-objective gaps “to solver accuracy” should identify the matching
   primal values. The displayed table uses corrected dual estimates, whose
   minimum closure is 0.9999826604704566 for `F` and 0.999912428316144 for
   `KAF`. Their remaining differences reflect conservative dual correction
   and numerical accuracy, rather than the stated input tolerance alone.
   The table itself is correct and the chapter already discusses this
   numerical distinction elsewhere. The author replaced the sentence with
   the recorded primal shortfall and an explicit explanation of the dual
   correction. A final small wording adjustment should name `F` explicitly:
   its maximum shortfall from `X_safe` is 5.46e-9, while the corresponding
   archived `KAF` figure is 2.71e-8.

5. **Minor, corrected: companion data description.** The README's upper-triangle JSON
   description applies to constructed-instance files. The hard-objective
   pool is JSONL with dense 3-by-3 `H`, linear `g`, and constant `c0` fields.
   The archived hard-objective values include `c0`; it cancels in the gap
   comparisons. The author distinguished the formats and constant offsets;
   I checked the revision. No numerical claim is affected.

All findings were sent directly to the author and coordinating agent where
appropriate. These small wording changes are not objections to any proof
or experimental conclusion.

## Mathematical checks

- **Fifteen-support separation.** The smallest-support global minimizer is
  stationary in the relative interior of its simplex face. A singular
  bordered system supplies a nonzero tangent direction along which the
  quadratic is constant. Moving to the first zero coordinate contradicts
  minimality of the support. Hence a nonsingular face attains the global
  minimum even for indefinite or degenerate matrices. The symmetry argument
  also proves that every feasible stationary solution of a singular face
  has the same objective value. The proof supports the stated exact
  algorithm without an unstated positive-definiteness assumption.

- **Exact tetrahedral lift.** The five listed tetrahedra cover the cube.
  Nonnegative barycentric coordinates and `CP_4 = DNN_4` give both
  containments, with the displayed normalization preserving total mass.
  The five blocks, thirty off-diagonal nonnegativity constraints, and ten
  linking equations agree with the archived implementation.

- **Hull depth and cut correction.** The uniform integral is strictly
  positive on every nonzero cube-nonnegative quadratic. Consequently its
  mean-one slice is compact; normalization does not hide an unbounded
  optimization problem. Separation of the compact normalized moment hull
  proves the sign test. The convex mixing formula tests every nonnegative
  quadratic and therefore gives exact hull membership. The simplex shift
  rule is also correct. The manuscript correctly declines to turn an
  uncertified floating-point simplex minimum into a rigorous shift.

- **Triple-local improvement.** Uniform mixing keeps the global point in
  the convex baseline set and makes every recorded triple realizable. The
  separate auxiliary choices can then be combined. The proof needs only
  baseline containment of the uniform point and feasibility of the audited
  point. It does not need `R` to contain a particular named relaxation.
  Shared monomials such as `x_i^2 x_j` prevent the local choices from being
  combined, so excluding the tested shared-auxiliary `K` implementation is
  necessary and correct. The baseline primal-to-dual margin is explicitly
  retained.

- **Dual residual correction.** The displayed inequality follows with the
  sign convention `Au+s=b`. The finite moment and tetrahedral bounds are
  valid. At a baseline-feasible point, the family block gives
  `S=B-N-bb^T` positive semidefinite with diagonal at most one, so its
  entries have absolute value at most one and `N_ij <= 3` follows. The
  chapter explicitly conditions rigorous certification on rigorous cone,
  residual, and rounding verification; the archive provides floating-point
  estimates instead.

## Numerical and provenance checks

All eight representative constructed rows agree with
`logs/table_chain_compact.md`, `logs/table_cactus_compact.md`, and
`logs/table_ht_compact.md` in the original research archive. The hard-three
table agrees with `logs/r1_fix_numbers.out`, including the corrected means,
medians, and the two family minimum closures.

The strict benchmark paragraph reproduces the recorded computed depth,
triangle upper bound on the exact depth, maximum recorded overestimation,
0.045% diagnostic gain expression, and 0.60% / 1.10% conditional sensitivity.
It does not present the 0.079% lower bound on the gain expression as a lower
bound on achieved improvement. It explicitly retains the unverified
one-sided depth and feasibility assumptions. The separate full-`K` test is
correctly presented as one negative instance.

The archived sampling counts and search outcomes agree with the selected
JSON summaries. Inspection of the sampler confirms that it checks the
diagonal caps as well as McCormick and triangle inequalities, with its
stated floating-point tolerance. The sample is not presented as a proof of
completeness. The chain and cactus timing interpretations retain the
different selection rules, separate chain runs, changing iterates, and
shared-machine load.

The companion includes byte-identical source copies, original outcome
records, reconstructed tables, and a source manifest. Its README states
which large campaigns and moment/depth arrays are omitted, which software
versions were not recorded, and which commands would solve models. It does
not claim complete reproduction of every campaign from the compact
archive.

Targeted command actually run:

```text
python paper-box-quadratic-hulls/companion/inspect_records.py
exit 0
PASS: 371 copied-source SHA256 hashes verified
PASS: 334 archived constructed-method table rows reconstructed
PASS: 109 hard-objective closures and strict gain sensitivities reconstructed
No optimization code imported; no instance generated; no model solved.
```

This command inspects archived files with the Python standard library. It
is not an experiment or a CI check. An earlier run also passed with 386
copies before the author removed machine-specific and private source files.
The recorded final check used the resulting 371-copy manifest.
