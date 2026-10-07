# Independent review of the shared-root fallback and common-law budgets

Date: 2026-10-05 (America/New_York). Reviewer: Sol, independent of the
completed revision author. The reviewed source is the immutable
`evidence/snapshots/integrated-mathematical-draft-r1/`, captured at
`2026-10-06T03:49:31.635993+00:00`. Root confirmed that snapshot as the
review target. Locations below refer to its files; **03** means
`sections/03-counting.tex` and **A** means `appendices/A-finite-noise.tex`.

**Decision.** The shared-root lemma and strengthened exact-fallback theorem
pass this mathematical review. The common-grid and Gaussian parts of the
universal-law corollary also pass. Part (c) has one narrow construction-cost
gap in its abstract hypothesis: mere effectiveness of an envelope does not
give the claimed polynomial overhead for evaluating it. Add the precise
premise described below before approving that formulation. The explicit
flow/TU envelopes admit that premise; this finding does not invalidate those
routes or their parameter-dependent precision. No optimizer counterexample,
fatal defect, or reason to abandon these results was found.

This is approval only of the assigned proof chain, subject to that repair
and the pending classical-source audit. It is not approval of the entire
paper, the complete route algorithms, their literature attribution, or
submission readiness. I read the complete current 03 and A proofs, the
model/output context, and scoped route schedules. Author reports and earlier
reviews were used to identify obligations, not as substitutes for checking
the written arguments.

The principal files match the frozen manifest and their live counterparts:

| File | SHA-256 |
| --- | --- |
| `sections/03-counting.tex` | `9818728f37864c878ab2e7d0bb1690bb79e8d53f3a338e2f316e31787692b049` |
| `appendices/A-finite-noise.tex` | `4ff3fe30e76466dcc744389e88deaa9759fc19a2709c1104cba89612379c39cd` |
| `sections/02-model.tex` | `0a9267cd7a893497d212e5ccb0fbb6433b6428c4784793dd9fc79ec4f4e38a63` |
| `macros.tex` | `ac79fc04907f0edc4f964033bbcfa9c1d4d5b07b36428ad0466c72a34d6c8abd` |
| `main.tex` | `e22e0015a0b032eedbd618b75c6be0fb8c120f6789e12acb0b9cafc5420b9000` |

**Required local repair: moderate formal bit-complexity gap.**
`cor:count:universal-law`(c), **03:689–696**, assumes only an effective
nondecreasing function `F`. Its conclusion charges an overhead
`(1+F(K))^c`; the proof at **A:704–709** substitutes the resulting
coefficient lengths into fixed work polynomials but does not bound the work
of computing `F(K)` itself. The algorithm's work model includes computing
the law before sampling (`02-model.tex:255–257`), so this cost cannot be
omitted.

Effectiveness alone supplies no such bound. For computable bits `a_K`, the
integer function `F(K)=2K+a_K` is strictly increasing and has magnitude
`O(K)`, regardless of the work needed to compute those bits. Recovering its
exact value recovers `a_K`. Thus neither monotonicity nor its value bounds
the evaluation cost. This is a defect in the general complexity inference,
not a counterexample to an optimization result or a necessary-precision
lower bound.

A sufficient precise premise is: `F` is a nondecreasing integer-valued
function at least one, computable with a fixed polynomial bound in
`I+F(K)+1`, with `K` encoded in the supplied data; the exponent `c` is
enlarged to cover this evaluation as well as sampling, construction, output,
and refinement. Alternatively choose an enlarged integer envelope that
dominates the work of constructing itself, and state that convention. The
proof should charge this computation before substituting the precision
bound. The elementary effective-envelope construction may count and sum the
work of earlier parameter evaluations; no promise test or enumeration of
all base inputs is needed.

For the actual nonlinear boundary flow/TU application, this is an available
choice of envelope, not a new structural restriction. The elimination
formats are explicit parameter powers, and the statement already permits an
enlarged effective parameter function. Taking a monotone integer bound for
these fixed formulas, including its construction cost, retains a bound of
the form `F_d(K) poly_d(I)` with polynomial exponents independent of `K`.
The original proof at `F-integer.tex:822–832` has the precision dependence
at the chart-value margin, and `F-integer.tex:859–863` already charges the
resulting data length. The TU transfer retains that same contract. The
interior and bilinear precision branches remain polynomial in input length.
Root has accepted this formulation repair for later integration; it is not
present in the frozen text reviewed here.

**Shared-root construction: pass.** `lem:count:shared-root`, **A:439–562**,
constructs a representation of the designated tuple, rather than a list of
unrelated scalar isolators. The following checks were made directly.

- Squarefree preprocessing at **A:456–471** makes the tensor quotient
  reduced. Over the complex numbers it is the product algebra on exactly
  `N=product d_i` distinct Cartesian tuples. The tensor-companion matrices
  therefore have the asserted simultaneous eigenvalues. This covers
  repeated roots in the original factors and avoids a false squarefree test
  on a nonreduced algebra.
- For distinct tuples, the moment-form collision polynomial is nonzero and
  has degree at most `m-1`. The list of
  `1+(m-1) binomial(N,2)` integers at **A:473–490** therefore contains a
  separating form. Its characteristic polynomial is squarefree exactly when
  all complex tuple projections are distinct. The gcd test is both necessary
  and sufficient, including `m=1` and `N=1`.
- At **A:492–511**, each coordinate uses its own coefficient-direction
  derivative. Evaluating `q_i` at a simple projected root gives the
  coordinate times the characteristic-polynomial derivative. Inversion of
  that derivative modulo the characteristic polynomial therefore gives the
  coordinate maps. Differentiation solely with respect to the moment
  parameter would not suffice; the written proof does not make that mistake.
- A real projected root must correspond to an all-real tuple: a nonreal
  tuple and its conjugate would otherwise collide. The target root is the
  weighted sum of the roots specified by the source isolators. The
  root-separation bound and prescribed source precision at **A:513–527**
  give a bounded selection step. The summed interval contains the target
  and no other root. Endpoint tests also cover point isolators. Separating
  all Cartesian tuples alone would not select the canonical tuple; the
  proof explicitly performs the required selection.
- The determinant/interpolation computation at **A:529–550** involves only
  two interpolation variables and polynomially many matrices and forms.
  Clearing denominators adds their bit lengths, rather than raising a
  coefficient-height variable to a power depending on the tuple length.
  Polynomial degree/height bounds for univariate arithmetic then give
  absolute polynomial exponents in `D,m,H`.
- The Cauchy bound and termwise derivative bounds at **A:552–561** give
  polynomial logarithmic map sensitivities. Refining the shared root with
  that allowance yields scalar evaluation, and the additional dimension
  allowance yields Euclidean error. Substitution of an explicitly listed
  fixed-degree polynomial, followed by sign determination at the selected
  root, supplies the stated sign interface.

**Canonical fallback and enlarged budget: pass.**
`thm:count:fallback`, **03:539–601**, and its proof at **A:564–673** meet the
model's common-root coordinate-and-value contract.

The successive minima on compact optimizer sets at **A:565–571** give a
single lexicographically least optimizer, even with a continuum of
minimizers. The coordinate and value formulas at **A:573–593** use the same
witness condition. A feasible witness must have minimum value and must
precede every tied minimizer. Thus every scalar formula selects a coordinate
of the same point, and the value formula selects its objective value.

The two positive quantified blocks and one free scalar variable are within
the stated elimination format. The exponentially large integer
disjunctions have polynomial logarithmic atom count. Denominator clearing
has a fixed polynomial coefficient-height bound in `I+b`; it does not
increase the degree or format. The format-degree estimate at **A:595–609**
is independent of sampled bit length. This distinction is essential.

For the univariate formula, a singleton truth set must meet a nonconstant
atom's zero set. The squarefree product at **A:611–628** contains every such
root. Since all atom roots lie among its roots, their signs at the isolated
candidate are determined correctly by gcd/root counting or an endpoint
sign. Exactly one candidate satisfies the singleton formula. Products,
squarefree extraction, isolation, and refinement preserve a base-only
exponential degree bound and a fixed polynomial dependence on height.

With scalar degree at most `A_0=2^{poly_d(I)}` and tuple length `N+1`, their
product degree is at most `A_0^{N+1}=2^{poly_d(I)}`. Substituting the scalar
height bound into the shared-root lemma gives an enlarged base-only
`B poly_d(I+b+q)` at **A:632–642**, with an exponent in `b,q` independent of
dimension. The theorem also charges total output length, rather than
claiming that the base multiplier alone bounds it. This is a real
degree-versus-height argument, not an inference from total runtime.

The selected tuple is `(x^lex,f*)`. Accordingly, the value identity at
**A:644–648** holds at the chosen root. It need not hold modulo the defining
polynomial because extraneous Cartesian tuples may pair coordinate roots
with another value root. The text makes this distinction explicitly.
Integer labels are recovered exactly and listed. Coordinate refinement has
the Euclidean dimension allowance. The mixed-box construction at
**A:656–672** preserves those labels, clips continuous approximations, and
uses a derivative bound and value lower endpoint to certify the requested
gap. It makes no rational-feasibility claim for an arbitrary semialgebraic
domain.

Finally, **03:499–506**, **03:597–598**, and **A:640–642** require the enlarged
fallback multiplier before thresholds, depth, or law selection. The
accounting cancels this base multiplier and retains the sampled-input
polynomial. It does not cancel the entire output or refinement cost.
`S>0`, direct singleton evaluation, positive elimination block sizes, and
the corrected sampler intermediate-height bound are all present in the
actual text. The earlier shared-root, size, singleton, and Euclidean-output
findings are therefore resolved in this snapshot.

**Universal-law parts (a) and (b): pass.**
`cor:count:universal-law`, **03:642–754**, and **A:675–822** state and prove
the required schedule assumptions and their domain/cost qualifications.

For grids, a fixed effective polynomial envelope gives a common power of
two at least every instance's required resolution. The monotone schedule
retains its thresholds, support, and cap. Substitution of the larger
sampling precision changes the fixed bit polynomial, while keeping the
structural and numerical count factors. The algorithm evaluates the
envelope, rather than enumerating valid inputs or materializing all atoms.

The Gaussian pair is constructed together. For
`H=A(I)+D(I)+21`, `t=ceil(4 log_2 H)`, and `b=A(I)+D(I)t`, the displayed
inequality at **A:687–702** follows from
`t<=4 log_2 H+1`, `D<=H`, and `H>=3`:

`b+20 <= H+4H log_2 H <= H+4H^2 <= H^4 <= 2^t <= 2H^4`.

The same pair satisfies `b>=b_Pi(t)` for every shorter valid instance. Thus
its actual sampler support fits the trial auxiliary box, whose cap is chosen
before the draw. Integer comparisons compute `t`; no real-logarithm oracle
is assumed. Both `t` and `b` are polynomially bounded by input length.
Increasing accuracy without recomputing the box would have been invalid;
the written proof does recompute it.

The route checks preserve the following distinctions and costs:

- The scalar fallback degrees and finite-tail constants have polynomial
  logarithmic envelopes even with binary native-label ranges. Gaussian
  requirements in `B-quadratic.tex:664–688,878–887` satisfy the asserted
  affine-in-`t` accuracy envelope. The mixed-gap cutoff enforces `h_J<=1`,
  and its constants stay independent of support. Gaussian-weighted counts
  use original projected widths; larger trial support adds bit/depth costs
  without a new numerical width factor.
- Grid schedules in the sparse, constrained, recourse, and integer branches
  use resolution only through decreasing atom/replacement errors and lower
  bounds such as `M>=2^J`. Their coefficients, numerical certificates, and
  oracle cost models remain part of the input/cost contract. I inspected the
  schedules supporting this inference, rather than reapproving their full
  closure or oracle proofs.
- The lattice branch explicitly resets `J=log_2 M`. Its terminal error is
  `O(M^{-2})`, while original values have spacing `1/[D_0(M-1)]`; the
  sufficient inequality improves with `M`. One common `M` across aligned
  rows preserves that denominator. This is expressly identified as an
  exception to the literal unchanged-cap definition.
- Strong-field interval masses need not decrease with `M`. The text gives
  the correct two-point/four-point example, requires recomputing `q_i` and
  `beta`, and preserves only the sufficient physical strong-noise regime
  under a common larger grid. It does not infer arbitrary subcriticality.
- Nonlinear boundary flow/TU retains the supplied `k<=K` qualification.
  Coefficient/query lengths and output evaluation inherit the `K` factor.
  Setting `K=I` can impose that cost on small actual cores; the text does not
  claim preservation of the bound in actual `k` or a precision impossibility
  theorem. Interior and bilinear cases are separately polynomial-bit.
- Fixed degree alone does not bound geometric magnitudes on arbitrary
  compact semialgebraic sets. The iterated-squaring example has the stated
  doubly exponential final width. Fixed graph dependency depth, rational
  polytopes, supplied brackets, and supplied curvature/modulus data are
  needed for the route envelopes; they are retained explicitly.
- Correctness applies on every draw, output format and fallback use the
  same sampled problem, and later `q`-bit evaluation does not select a new
  law. Fallback evaluation retains `B poly_d(I+b+q)`, with fixed exponents.
  The standardized family is rescaled by supplied noise scales and uses
  each theorem's perturbation coordinates. The proof does not interchange
  grid/Gaussian laws or remove numerical factors from expected counts.

**Unresolved dependencies and limits of this verdict.** The only new local
repair from this review is the computation-cost premise for the abstract
parameter envelope. Bibliography identities and exact source locators remain
with the Luna literature owner. In particular, the displayed block-sensitive
elimination theorem and the cited polynomial univariate
degree/height/isolation/refinement/sign bounds are classical dependencies
used in this verdict; I have not certified the manuscript's bibliography
keys or claimed source locators. No source identity or priority claim was
invented. The independent proofs of the other structural routes and full
manuscript coherence remain outside this assignment.

**Targeted verification actually performed.** Read-only investigation used
`cat AGENTS.md`, `pwd`, `git status --short`, scoped `rg --files` and `rg -n`,
`wc -l`, `cat`, and `nl -ba ... | sed -n ...` on the requested reports,
contracts, 03/A, preamble/model context, and supporting schedule passages.
In particular the complete 03 reads covered `1,274p`, `275,540p`, and
`539,754p`; the complete A reads covered `1,165p`, `166,330p`, `331,565p`,
`564,674p`, and `675,822p`. The supporting schedule reads were confined to
quadratic, sparse, constrained, recourse, and integer inputs named above.
The inequalities, tuple identities, quantified selectors, and degree/height
substitutions were rederived analytically from the text.

`sha256sum` was run on the five principal live/frozen files, and
`cmp paper-smoothed-global/sections/02-model.tex
paper-smoothed-global/evidence/snapshots/integrated-mathematical-draft-r1/sections/02-model.tex`
passed. A scoped inline `python3 - <<'PY'` check using `hashlib` and the
manifest verified both the frozen hash and live/frozen identity for these
five files plus `sections/04-quadratic.tex`, `appendices/B-quadratic.tex`,
`sections/05-sparse.tex`, `sections/08-integer.tex`,
`appendices/D-constraints.tex`, `appendices/E-recourse.tex`, and
`appendices/F-integer.tex`: all 12 passed. These checks establish identity,
not correctness of the entire supporting sections.

A report-only inline Python check was run after writing for final newline,
trailing whitespace, absence of control characters, and existence of the
named principal snapshot files. It passed. Only this review report was
written. No TeX, saved experimental artifact, literature record, or other
report was edited; no optimization experiment or saved proof diagnostic was
rerun. No project-wide verification, CI status, or CI log was inspected.
