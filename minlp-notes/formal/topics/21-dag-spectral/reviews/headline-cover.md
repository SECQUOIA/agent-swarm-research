# Independent review: actual DAG spectral-cover headline

Verdict: **PASS for the complete mathematical cover, feasibility,
infeasibility detection, kernel preservation, and output-cardinality
headlines.** The returned finite set is computed from the original rational
prior and edge matrices. No decomposition, successful trial, target rank,
representative, or cover certificate is supplied as an extra premise.
Global bit complexity C05 and actual criterion selectors remain separate
work and are not certified by this review.

The stable primary files reviewed are `PathInformation.lean`,
`CoverProducer.lean`, `CoverCorrectness.lean`, `CoverCardinality.lean`, and
`Headline.lean` in `formal/Formal/DAGSpectral/`. I also traced the integration
through `NormalizationInput`, `IndexedFactors`, `NormalizationComplete`,
`NormalizationData`, `TrialApproximation`, `PathMatrix`, `Graph`,
`ProfileDP`, and `ProfileSpectralDP`, with the earlier factorization,
normalization, and rounding reviews supplying their detailed foundations.

## Inputs and actual output

`dagSpectralCover` takes an explicitly indexed DAG, endpoints, rational
matrices `Q0` and `Q`, proof-only PSD promises, and rational `eta`. The graph
stores actual source/destination indices and a proof that every edge
advances the vertex order. Thus this interface receives a verified
topological indexing; it does not assume a path or normalization witness.
Parallel edges retain their distinct edge identities.

`producedData` constructs the factors with rational LDL, indexes each actual
owner/factor position by an executable finite equivalence, and derives its
reconstruction and positivity fields. The prior remains owner `none`;
repeated factors of an edge have separate labels. The actual total label
count `M` is bounded by `p*(m+1)` through `original_input_size` and
`indexedPriorAtomCount_le`.

For positive ranks, `spectralPathSet` enumerates the actual rational
independent-label trials, applies exact prior/edge filters, computes signed
rational upper-triangular labels, and runs the state-merging DP. It unions
all complete-owner terminal representatives and removes duplicate paths by
path identity. The zero-information branch uses a separate zero-edge DP
and retains at most its first output. The `s=t` branch directly returns
the singleton empty path.

The noncomputable `feasiblePaths` finite set is a semantic domain used by
the theorem and optimization corollaries. Its bounded-list enumeration is
not called by `dagSpectralCover`. The producer is executable; the raw-input
checks below evaluate it directly.

## Coverage of every target

`pathMatrix_eq_information` connects the list-based path information to the
selected-owner finite-set sum. Its no-duplicate premise is supplied by the
actual DAG path theorem, not assumed for arbitrary edge lists. The prior is
included exactly once. The congruence and cast bridges preserve this sum.

For each target path, `selectedRank_eq_information_rank` identifies the
factor-span rank with the actual information-matrix rank. The completeness
proof splits on that rank only in its proof. The producer does not need a
real-rank oracle: it enumerates all positive ranks and includes the zero
branch independently.

At positive rank, `exists_accepted_trial` constructs a maximum-volume choice
from the target's actual selected factors, connects its sorted labels to
the enumerator, and proves that every target atom and the prior pass the
range and magnitude tests. The per-owner LDL count supplies the magnitude
constant `4p`. It also proves the forced-owner condition and the actual
normalized identity floor. Therefore `trialPathSet_complete` receives its
seemingly conditional helper premises from the target and original inputs.
They are not left as assumptions in `spectralPathSet_complete` or the raw
headline.

The DP completeness theorem replaces each prefix by an actual stored
representative with the same owner mask and signed profile. Its induction
uses the forward edge order to reach an already processed predecessor.
Appending the current edge gives an actual allowed path; DAG path
properties exclude repeated edges. It does not assume that arbitrary
list concatenations are feasible. Only stored representatives are extended.

`TrialApproximation` uses the rational-floor cast bridge to translate the
actual profile equality into equal upper-triangle label sums. `PathMatrix`
then cancels the common unrounded prior, extends the bound to all entries by
symmetry, and proves the exact `r N h=eta` perturbation estimate. Different
path lengths are permitted. The target's normalized floor converts that
estimate to both relative PSD inequalities. `restore_pathMatrix` uses the
same actual reconstruction matrix for target and representative and their
proved range tests, yielding the original-space sandwich.

## Exceptional cases and kernels

`selectedRank_zero_iff` proves that zero target information is equivalent to
a zero prior and zero matrix on every selected edge. This follows from PSD
and is not an extra input assumption. A zero target therefore supplies a
feasible path for the zero-edge DP. Taking its first terminal output keeps
an actual path with exactly zero information. The branch remains available
when other feasible paths have positive rank. A nonzero prior excludes a
zero-information target.

If `s=t`, acyclicity proves that the only possible path is empty, and the
producer returns exactly that path even for a nonzero prior. If there is no
source-to-sink path, soundness forces the output to be empty; conversely,
any feasible path has a returned representative. This gives the exact
`dagSpectralCover_empty_iff` result, rather than a promise of nonempty input.
Dimension zero is also covered, although the source theorem only needs
positive dimension. An empty vertex set has no endpoints to instantiate.

The main relative-cover theorem requires only `eta>0`; allowing a larger
parameter is a valid extension of its two inequalities. The kernel theorem
additionally requires `eta<1`, exactly where the positive lower factor is
needed. `dagSpectralCover_kernel` supplies a returned feasible path, both
PSD inequalities, and equality of the actual multiplication kernels for
all vectors. Original information may be singular, and no positive-definite
prior or condition-number premise appears.

## Exact source cardinality

The cardinality proof obtains its entry bound from the actual diagonal
filter and PSD congruence. No externally supplied entry bound remains in
`spectralPathSet_card` or `dagSpectralCover_card`. The rational labels are
proved equal to the spectral labels used in the finite-state bound.

With `N=max(1,v-1)`, the result is exactly

```
C_r = ceil(8 p r N^2/eta + N) + 2
|cover| <= 1 + sum_(r=1..p) choose(M,r) * 2^r * C_r^(r(r+1)/2).
```

The zero branch contributes at most one. Each positive-rank trial has at
most `2^r` masks because it forces at most `r` distinct owners, even when
several basis factors have the same owner. The coordinate bound includes
signed floors and differing lengths; the upper-triangle exponent is exact.
The trial count is bounded by `choose(M,r)`. Taking finite unions and
deduplicating actual paths can only decrease cardinality. The direct
`s=t` singleton also satisfies this bound. Every returned path has length
at most `v-1`, hence at most `N`.

This is a bound on the computed set, not on an existential replacement set.
It does not alone bound costs of constructing or storing that set. The
state/extension bounds and global implementation cost require their own
integration, as do the criterion-specific path selectors.

## Targeted verification

Run from `formal`, with `PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1`:

```
lake build --wfail Formal.DAGSpectral.PathInformation Formal.DAGSpectral.CoverProducer Formal.DAGSpectral.CoverCorrectness Formal.DAGSpectral.CoverCardinality Formal.DAGSpectral.Headline
lake env lean -DwarningAsError=true topics/21-dag-spectral/verification/CoverBoundaryReview.lean
```

Both passed. The independent client constructs raw matrices, derives their
PSD proofs with ordinary kernel-checked lemmas, and evaluates the actual
`dagSpectralCover`. Its seven runtime assertions check:

- Two parallel rank-one atoms with different kernels are both retained.
- A zero-information path and a positive-rank path are both represented.
- A single edge with two basis factors sharing its owner returns that edge.
- A graph without a path returns the empty set.
- `s=t` with a nonzero prior returns exactly the empty path.
- One-edge and two-edge paths with a common nonzero prior and zero atoms
  merge to one actual feasible representative.
- Dimension-zero information returns one of the actual parallel paths.

The client printed `Seven raw-input cover boundary checks passed.` Its
runtime assertions create no proof declarations and use no `native_decide`
axioms. Selected production axiom checks for
`dagSpectralCover_isRelativeCover`, `dagSpectralCover_empty_iff`,
`dagSpectralCover_kernel`, and `dagSpectralCover_card` reported only
`propext`, `Classical.choice`, and `Quot.sound`. This is a targeted check,
not the separate final topic audit. No project-wide check or CI inspection
was run, and no proof source was edited.

Reviewed SHA-256 digests:

```
e50a8a29006f212813dfb87fdca8b3be1473255dd74b53351dfa4a21469523fb  PathInformation.lean
032e23ea37cb9b377228738f1466847f7ef5a30e412f625fc0da9f99be711bef  CoverProducer.lean
f18ac8ec7fad9fbd58cbf464836c211766aff3f40d5d60f0d51ae188398eaf61  CoverCorrectness.lean
d902bec8d338b7ec8d9f94be19c46ed96190fee829f7b24d86df86002d597f8a  CoverCardinality.lean
ce2b294e60f5c97c8807dbcc72f9c3141e0468bffb467c6166396880694f112c  Headline.lean
```
