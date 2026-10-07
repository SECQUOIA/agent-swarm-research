# Focused independent review of the parameter-envelope repair

Date: 2026-10-06 (America/New_York). Reviewer: Sol. Review target:
`evidence/snapshots/integration-repairs-r1/`, captured at
`2026-10-06T03:59:42.813203+00:00`. This is a fresh review of the changed
model, universal-law statement, and cost proof. It follows
`shared-root-universal-independent-sol-r1.md`; it does not replace that
report's detailed review of the unchanged shared-root construction.

**Decision: the moderate envelope-computation finding is resolved.** The
new premise bounds the work of computing the parameter envelope, the proof
charges that work before sampling, and the overhead exponent includes its
fixed computation exponent. The flow/TU application explicitly selects an
envelope with this property. No further local mathematical repair is needed
for this finding, and no new parameter or output-contract defect was found
in the changed passages. The assigned mathematical scope passes, subject to
the unchanged pending classical-source audit. This is not complete-paper
submission approval.

The principal files match the new frozen manifest:

| File | SHA-256 |
| --- | --- |
| `sections/02-model.tex` | `9fe94874c591d201af37daeae527ee93298baa53fb061db356eb97ebf91571c4` |
| `sections/03-counting.tex` | `ccbe57f1117ed70fea17f6702b9cadbe1155ae5c719c9139ddad8ee6e00a1c0d` |
| `appendices/A-finite-noise.tex` | `31b257efb6a6ad8106a06fab5e01b1bc0723b3e2b5e2d34efe8d6a412b7e991f` |
| `macros.tex` | `ac79fc04907f0edc4f964033bbcfa9c1d4d5b07b36428ad0466c72a34d6c8abd` |
| `main.tex` | `e22e0015a0b032eedbd618b75c6be0fb8c120f6789e12acb0b9cafc5420b9000` |

**Changed statement and proof.** At
`cor:count:universal-law`(c), `sections/03-counting.tex:689–699`, `F` is now
nondecreasing and positive integer-valued, with evaluation work bounded by
`(1+size(K)+F(K))^{c_F}` for a fixed exponent `c_F`. The supplied `K` is part
of the base data. The claimed overhead exponent `c` expressly depends on
`c_F` as well as the existing fixed polynomial exponents. The old
effectiveness-only inference is therefore no longer used.

The proof in `app:count:universal`,
`appendices/A-finite-noise.tex:704–712`, first evaluates this envelope and
charges its work. Since `size(K)<=I`,

`(1+size(K)+F(K))^{c_F} <= (1+I)^{c_F}(1+F(K))^{c_F}`.

Thus the construction cost has the asserted form with exponents independent
of the supplied parameter. Computing the exponent
`E=ceil(F(K) P_0(I))` and drawing the endpoint-grid index also fit this bound:
arithmetic uses the encoded integers, and the draw uses `E` fair bits.
Positivity gives `E>=1`, so the prescribed grid has at least two points.
Nondecreasing `P_0` and the supplied precision bound give
`2^E>=M_Pi` for each eligible instance.

For any fixed original exponent `e`, substituting the new coefficient
length into a bound in `I+b+q` gives a fixed polynomial in `I+q` times
`(1+F(K))^e`. Enlarging `c` to cover this and `c_F` completes the stated
cost argument. No exponent of `b`, `q`, or `I` depends on `K`. The new
computation premise is necessary for the abstract corollary; its presence
excludes precisely the uncontrolled effective-function examples identified
in the first review.

**Actual route premise and model consistency.** The route paragraph at
`appendices/A-finite-noise.tex:805–818` now chooses a nondecreasing integer
envelope for the explicit nonlinear boundary flow/TU parameter powers,
with evaluation polynomial in `1+size(K)+F_d(K)`. Such a choice is available
for those fixed explicit formulas. Integer powers can be computed by exact
arithmetic; an enlarged monotone envelope can also dominate the parameter
and construction work. Its fixed arithmetic exponent depends on the fixed
route and degree, not on `K`.

The underlying parameter-dependent precision/work block is unchanged in
the new snapshot (`F-integer.tex:824–834,861–865`). The new common grid
therefore changes only the admitted precision and corresponding data costs.
The original numerical count factor and the same-support coefficient cube
remain as before. The proof still admits dependence on supplied `K`; it
does not claim preservation of the work bound in a smaller actual core
size after setting `K=I`. The interior/bilinear polynomial-bit branches
are not changed by this repair.

`prop:model:uniform`, `sections/02-model.tex:192–215`, carries the same
integer-envelope computation convention and charges it before sampling.
Its proof invokes the repaired corollary. The general model already counts
structural data in input length, and the corollary now explicitly counts
the supplied `K` there.

The accompanying cost qualifications at `02-model.tex:278–286,374–385`
correctly retain polynomial dependence on sampled coefficient length
`I+b` and requested precision `I+b+q`. When sampling precision contains a
parameter factor, the expected fallback contribution retains that factor.
The rare-event cancellation removes the base-only multiplier `B`; it does
not erase sampled-height costs. These changes preserve the shared-root
output model, every-draw correctness, same-draw fallback, and evaluation
of the existing descriptor without a new sample.

**Unchanged proofs and remaining scope.** A direct byte comparison between
the two immutable snapshots confirms that the entire exact-fallback
statement/explanation in Section 3, the shared-root lemma and fallback
proof in Appendix A, and the statement and proof of universal-law parts
(a) and (b) are unchanged. Their first-review verdicts therefore carry
forward. The macros and main file are also unchanged.

The other root repairs in front matter, Appendix B, and the integer
resultant construction are outside this focused proof review. The short
flow-boundary precision/work read above checks only the envelope application.
Bibliography identities, exact classical-source locators, and the later
full proof/source audit remain separate. I performed no literature research
and did not invent source identities or locators.

**Checks actually run.** I read the original and independent review briefs,
the first focused review, the final root disposition, the new manifest, and
the relevant root repair diff. The prior integration contract/decisions and
quadratic author report were retained as context; scoped `rg -n` reads
located their common-law and sampling-parameter obligations. Actual source
reads used `nl -ba ... | sed -n ...` on new frozen `02-model.tex` ranges
`143,218p`, `247,291p`, `370,388p`, and `9,17p`; `03-counting.tex` range
`642,757p`; `A-finite-noise.tex` range `675,827p`; and the scoped
`F-integer.tex` precision/work passages listed above. `rg --files` located
the supplied diff at `evidence/reviews/round1-root-repairs.diff`; an initial
read at `evidence/round1-root-repairs.diff` reported that the path did not
exist, after which the actual file was read.

A scoped inline `python3 - <<'PY'` check using `hashlib`, `json`, and
`difflib` verified old/new manifest hashes for the five principal files,
printed their exact diffs, and asserted equality of four unchanged proof
blocks. All assertions passed. A second scoped Python check verified
`appendices/F-integer.tex` against the new manifest
(`4ec4e5fbf8907398384e75c4b98f39888d57b603c6389aa398f78c8d58b6ccfd`)
and verified byte equality of its flow-boundary proof block between the
snapshots. This establishes source identity, not approval of all Appendix F.

A report-only Python check for final newline, trailing whitespace, control
characters, and principal source existence passed after writing. Only this
report was written. No TeX, literature record, or other review was edited;
no experiment or saved proof diagnostic was rerun; no project-wide check,
CI status, or CI log was inspected. Review work stops with this report.
