# Stage 5B correction author record

The first five independent reviews accepted the existing mathematics.
`stage5b-assessment.md` accepted reviewer 5's coverage issue and requested
substantive inclusion of the dynamic scale-maintenance source. This record
documents that addition; it does not replace any previous review or author
report. The addition now awaits five fresh independent reviews.

## Exact changes

Only `sections/12c-newton-comparisons.tex`, `audit/source-map.md`, and this
record were authored. The manuscript's prior static results and all other
mathematical sections retain their hypotheses and proofs. Build products
were regenerated. Concurrent changes in `RESEARCH_NOTES.md` and `paper/`
were not edited. No Stage5C work was started.

In 12c's recentering/access subsection:

- Added the explicit compile-and-commit contract immediately before
  `newt:dynamic-scale`: each committed object has fixed encoded values;
  compute/copy/uncompute reads every label without raw queries and restores
  the entire backing workspace, including reference correlations. Joint
  success covers every source and epoch. Rational encodings make the
  `delta=0` endpoint meaningful; positive-error fixed-point encodings must
  have sufficient precision. Arbitrary consumable state output is excluded.
- Added Theorem `newt:dynamic-scale` (printed Theorem 28.7), equations
  `newt:dynamic-commit` and `newt:dynamic-margin`: tight fresh-batch quantum
  and randomized query costs, public interior reset, and the replicated
  block margin version. The stronger simultaneous-oracle lower-bound model
  explicitly allows coherent epoch/source/coordinate queries and retained
  quantum workspace.
- Added Corollary `newt:scale-service` (28.8) and equation
  `newt:scale-service-cost`: the exact universal adaptive invocation versus
  compilation tradeoff, with raw calls charged in both phases and a
  separate statement for the margin promise.
- Expanded `newt:scale-update` into the explicit sparse-list maintenance
  comparison and supplied the repeated fixed-oracle OR caching example.
- Added Proposition `newt:fixed-scale` (28.9) and equation
  `newt:fixed-path-scale`: exact uncoupled central-path scales, points,
  centered labels, and the source Hessian ratio. Norm acquisition is a
  one-time cost for fixed explicit objectives. Clean reversible evaluation
  uses O(1) norm-oracle calls, with inverse calls, arithmetic and precision
  charged; it is not described as one clean call without qualification.

The source map appends a current inclusion disposition that explicitly
supersedes the original dynamic-source exclusion. Earlier dispositions,
assessment and review records remain intact.

## Independent proof checks

Read both complete workbench sources
`2026-09-04-dynamic-psd-fiber-scale-maintenance-lower-bound.md` and
`2026-09-04-implicit-psd-fiber-recentering-access.md`, together with the
assessment, the existing static access proof, and the marginal/centered
system dependency in 12c. The older static note's weaker off-center
comparison was not reintroduced.

1. The public base has slack 1/s; zeroing one additional coordinate gives
   2/s. Both are interior, including s=2. Proposition `newt:center` gives
   the exact labels rho/h_a for any existing packing. Positive public h_a
   cancels in the relative-error test. The intervals are disjoint exactly
   for 0 <= delta < 1/3.
2. A nondestructive read of all commitments recovers Tb presence bits
   without changing the maintainer's subsequent state. The existing star
   adversary on epoch/source tensor factors has norm Tb sqrt(s-1), masked
   norm one, nonnegative entries and zero entries for identical output
   vectors. No new general direct-sum theorem is asserted.
3. For randomized algorithms, under the independent half-empty,
   half-uniform-mark distribution, marginal success 2/3 requires expected
   no-mark coverage at least (s-1)/3. Weighting that branch by 1/2 and
   summing gives the stated bound even with adaptive cross-pair queries.
4. The replicated promise has s/k-1 candidate blocks, between one and
   Theta(s/k). Representative coordinates establish both reductions and
   matching upper bounds. This version has k-sparse updates, not
   one-sparse updates when k>1.
5. A permitted service client reads min(r_t,b) distinct labels per epoch;
   other pairs can be fixed. The same vector-output proof yields the sum.
   Controlled exact promised search with coherent verification and
   uncomputation implements each value invocation; alternatively, compile
   all b bits once. Both strategies have zero error, so joint success
   requires no amplification logarithm. Zero invocation budgets cost zero.
6. Fixed-path stationarity gives rho + tau^2 rho^2/4 = 1. The displayed
   positive root is interior and handles zero objective norm and eta=0.
   Strict convexity gives uniqueness. The Hessian eigenvalues give the
   stated ratio when radial and tangential modes exist (s_a>=2). No
   additional affine coupling or generic inexact iterate is assumed to
   satisfy this formula.

All reductions concern fresh independent information and readable values.
They do not realize these batches as a fixed conic program's Newton
trajectory, multiply a static query bound by an iteration count, or claim
finite-precision gate bounds.

## Primary citations

Verified the finite-output, entrywise nonnegative spectral adversary and
its tensor-sum construction directly in Ambainis, Childs, Le Gall and Tani,
*The Quantum Query Complexity of Certification*, Theorems 3–4, printed
pp. 185–186 ([publisher PDF](https://www.rintonpress.com/xxqic10/qic-10-34/0181-0189.pdf)).
The existing `ACGT2010` entry suffices for the new lower bound.

Verified exact amplification for known positive success probability and
the exact zero-versus-known-cardinality promise in Brassard, Hoyer, Mosca
and Tapp, *Quantum Amplitude Amplification and Estimation*, Theorems 4
and 16 ([primary PDF](https://arxiv.org/pdf/quant-ph/0005055)). The existing
`BHMT2002` entry suffices for the new upper bound. No bibliography changes
were needed; the existing static proof's `LMRSS2011` attribution remains.

## Build and output checks

Ran sequentially in `conic-lift-complexity`:

```
conda run -n qipm --live-stream make clean
conda run -n qipm --live-stream make
```

Both exited successfully. The clean build regenerated `main.pdf` with 167
pages (1,359,843 bytes). The final `main.log` has zero warnings, undefined
references/citations, multiply defined labels, overfull boxes or underfull
boxes. A check using `/workspace/local-home/miniconda3/envs/qipm/bin/python` confirmed
unique 12c labels and balanced theorem/proof environments. PDF text and
rendered pages 125–127 were inspected: the new contract, theorem, proofs,
tradeoff and caching formula are legible and unclipped. Poppler commands
were run through `conda run -n qipm --live-stream`; no packages were installed.

The correction author is frozen pending the second five-review round.
