# Lower reductions: round 2 review of the R1 repairs

Reviewed 2026-10-05. This is a review of the changed scope, not a new
review of unrelated chapters. I read `reductions-r1.md`, the full Opus
response `repair-heights-reductions-r1.md`, the actual Section 04 and
Appendix B passages, the corresponding diffs against the writer's saved
pre-repair copies, the vetted literature report, and the current relevant
bibliography entries. The prior full analytic proof review remains the
basis for unchanged arguments.

**Mathematical readiness:** all four local correctness/encoding findings
from R1 are resolved. No new mathematical defect was found in their
repairs, and no theorem, hypothesis, compiler, or realization interface
changed. The EY2010 prose now matches the root-relayed Luna-cleared
contract. A short follow-up read after root bibliography checkpoint 31
confirmed that the two vetted commutator/group-circuit citations are now
integrated and the stale literature comments removed. No reductions
finding remains unresolved in this review's scope.

This internal review does not certify the separate heights repairs, the
independent Opus numerical review still in progress, or publication
priority. No manuscript edit, experiment, mathematical script, online
research, CI inspection, or project-wide check was performed.

## Reviewed snapshot

SHA-256 hashes identify the files inspected. A later change requires review
of its own diff; these hashes are not claims about a later manuscript.

| File | SHA-256 |
| --- | --- |
| `sections/04-reductions.tex` | `32648ab439cadd654a90c167614d30502c122b0e706882598b8872244c5ff76f` |
| `appendices/B-reductions.tex` | `1c78b5cd28b75854390eac3d8f48ffa6c623ecb7061f3bc4142375d70a692b94` |
| `evidence/reviews/reductions-r1.md` | `d20ec6014feca4f3ff2aeaf74568e5f2aeed04840f964a1283c0380505fb2157` |
| `evidence/authoring/repair-heights-reductions-r1.md` | `f376093fe156f51f7ccf0c29696608e47ae2fee8240b427bea471368d25e6212` |
| `evidence/literature-review.md` | `452741bfca1ef248858534400cda21096609c78608f39be86521ab4f4a3012aa` |
| `references.bib` | `866c8d1f4860ffbaa4ff54ef872fb82327aa117d1f118eb91addd03c4f23b354` |

The table includes the follow-up bibliography checkpoint. Before that
integration, the reviewed Section 04 hash was
`cfd23bacf72ff5a6f0a29492e7b2ab2abc2fd25e0ba3394f63cd7a7a82f6754f`
and the bibliography hash was
`a86e99828964889d15b5fa39e63abf22d950f763a6598559c05b17f4fd88d05e`.
The follow-up changes add the two citations and remove literature comments;
the mathematical dispositions below remain unchanged.

The diff baselines also have recorded hashes:

- `/tmp/hr-r1-orig/04-reductions.tex`:
  `20f6287ab77ded2ce6a3d516a45ce42804f55a9cbfeb6677dfe08a8ca8af7305`.
- `/tmp/hr-r1-orig/B-reductions.tex`:
  `7dd5237d87067df765287ac37e7c23f0f04c7ab98f4695997164dad64ead7911`.

## Resolved R1 findings

### 1. Block-sum positive definite Hessian Gram obstruction

**Resolved.** `sections/04-reductions.tex:717–726` now distinguishes all
three cases. With `m>=2`, the construction has at least two nonempty
variable blocks and no full positive definite Hessian Gram. With one
block, the singleton-field theorem supplies a positive definite rational
certificate. The empty-list fallback has the displayed Gram
`diag(2,12)` for `z^2+z^4` on `(v,zv)`.

The qualification is exactly the required one. Every summand receives its
own nonempty block even when its affine coefficient `c_i` is zero. Thus
`m>=2` really gives the two blocks required by the cross-monomial
obstruction. For an `x_j` coordinate in one block and direction `v_i` in
another, the coefficient of `x_j^2 v_i^2` in the Hessian biform vanishes;
only the full Gram's diagonal entry for `x_j v_i` contributes to it. A
positive definite full Gram cannot have that zero diagonal entry.

The additional sentence correctly explains the upper-bound interface:
A1 uses the supplied curvature promise `Hessian F >= I`, which holds
for every list size. It does not require a full positive definite Gram
for the combined block sum. The proposition and its proof are unchanged.

### 2. Blanket necessity of a positive definite squared input

**Resolved.** `sections/04-reductions.tex:216–227` now states the actual
negative-curvature calculation for the naive residual, describes the
positive definite exposing square as a feature of this paper's
construction, and explicitly rejects a general necessity claim.

The new example is correct:

`(x^2-y^2)^2+(2xy)^2=(x^2+y^2)^2`.

The two quadratic matrices are `diag(1,-1)` and
`[[0,1],[1,0]]`, both indefinite, while the sum's Hessian is
`4(x^2+y^2) I + 8 (x,y)(x,y)^T`, which is positive semidefinite everywhere.
It therefore demonstrates the intended collective cancellation of
negative curvature. The reference to the realization lemma remains an
application of its sufficient conditions; it no longer claims necessity.
No change to that lemma or to either realization is needed.

### 3. Printed size of the first parameter radicand

**Resolved.** `appendices/B-reductions.tex:315–318` now counts both the
boxes and the first parameter radicand as `O(Q)` bits. It also gives
`Q=12T+7`, obtained from `r_0=2T+5`, `r_1=T+1`, `9T` macro root gates,
and one zero gate.

The denominator of `delta_0^2=1000^{-2(Q+3)}` has `O(Q)` bits, as do
the numerator and denominator of `1+3 delta_0^2`. The other raw radicand
coefficients remain fixed constants. With `O(Q)` gates, the total encoding
is `O(Q^2)=O(T^2)`, including predecessor indices. The original small-signal
and interval proofs, and the output/auxiliary gate promises, are unchanged.

### 4. Derived scale parameters versus arbitrary input generators

**Resolved.** `appendices/B-reductions.tex:1003–1010` now names the
derived scale/rounding parameters and rounded coefficients that have
`O(k+N log N)` bits. It separately permits longer input rational generator
coordinates, keeps them exact in the constant-gate residuals, and states
the correct polynomial bound in total input length for the output.

The bound is supported by the unchanged construction. The weights
`omega_i` and `mu` require `O(k)` bits; `nu=(4N)^{-(N-1)}` requires
`O(N log N)` bits. The specified least exponent in `t=2^{-s}` gives
`log(1/epsilon)=O(k+N log N)`. The definitions of `eta` and the dyadic
mesh then give the same bound for their printed precision. Each rounded
coordinate is a multiple of the mesh with absolute value below two,
because the exact quaternion coordinate is at most one in absolute
value and its Euclidean error is at most `eta/2<=1/2`.

Exact input generator coordinates only enter explicitly supplied
constant-gate residuals. The rational quadratic `G`, its scaled square
factors, and the fixed degree-two canonical Hessian-Gram expressions
therefore retain polynomial bit length in total input length. The repair
does not round the exact residuals or change the unique zero, so rational
coordinate exactness and the promises of `thm:rational-optimizer` remain
intact.

## Source-contract and citation status

### EY2010, Lemma 5

**Resolved at the requested manuscript-contract level.**
`sections/04-reductions.tex:154–157` now states the root-relayed
Luna-cleared contract recorded at
`evidence/authoring/repair-heights-reductions-r1.md:221–228`: a linear-size
circuit over `{+, multiplication, division}`, all gate values in `(0,1)`,
and an order comparison of its output. The manuscript leaves the threshold
unnamed and does not add a stronger threshold or encoding claim.

The current citation `EY2010` resolves to the stated journal version at
`references.bib:252–262`: *SIAM Journal on Computing* 39(6), 2531–2597
(2010). The old EY `LIT-REQUEST` comment has been removed. This restricted
review confirms consistency with the cleared handoff; it does not claim
a fresh primary-source verification. The current general literature report
does not itself contain the exact EY Lemma 5 paragraph, so the repair
record is the local provenance for this particular clearance.

The EY citation is a comparison with prior work. No compiler,
realization, hardness reduction, or upper bound in Section 04 imports
that source as an unproved lemma. The self-contained proof interfaces
remain those reviewed in R1.

### Commutator and matrix-circuit citations

**Resolved after root bibliography checkpoint 31.**
`sections/04-reductions.tex:163–171` accurately distinguishes
approximate SU(2) synthesis from shared linear-group identity testing,
in agreement with `evidence/literature-review.md:54`. The claim about
these inspected works' predicates is confined to those works; it does
not claim absence of all related prior art.

Section 04:165 now cites `DawsonNielsen2006` for approximate SU(2)
synthesis; lines 166–167 cite `KoenigLohrey2015` for shared linear-group
circuit identity testing. Both keys have the intended entries in
`references.bib:343–370`. The earlier `ROOT-CITE` comments have been
removed. This follow-up checks the actual integration against the vetted
report and the root's verified metadata handoff; it does not claim new
source research. Ben-Or–Cleve is correctly not asserted as vetted.

### Hesse version scope and other interfaces

The Hesse comparison at `sections/04-reductions.tex:172–175` remains
explicitly limited to version 1, as required by the vetted report's
version warning. The stale `LIT-REQUEST` comment has been removed. The
vetted report already answers the version-1 question and records the
proceedings-text limitation; the prose does not silently assert that the
proceedings version has the same table.

Both diffs change only the named scope/encoding explanations and
prior-work framing. They add no theorem hypothesis, label, macro, source
operation, coefficient, degree, or output promise. The assembly-lemma
applications, min-sign perturbation, strict/weak sign substitutions,
rational-optimizer proof, and equality upper-bound scope are unchanged.
The repaired division reference remains correct: Appendix B:431 cites
`def:models-circuits`; there is no missing `lem:models-division` reference.

## Targeted verification record

Read-only inspection used `cat`, `nl -ba`, `sed -n`, and `rg` on the
named files, `sha256sum` for the snapshots above, and these two local diffs:

```text
diff -u /tmp/hr-r1-orig/04-reductions.tex paper-exact-arithmetic/sections/04-reductions.tex
diff -u /tmp/hr-r1-orig/B-reductions.tex paper-exact-arithmetic/appendices/B-reductions.tex
```

Both diff commands returned 1, meaning the expected textual differences
were present. Their complete output was inspected. An independent
delegated read-only check of the source-contract and citation passages
agreed with the pre-bibliography statuses. The subsequent short follow-up
read checked the actual changed literature paragraph and the two added
bibliography entries. A targeted `rg` search for `ROOT-CITE|LIT-REQUEST`
in Section 04 returned no matches, and updated `sha256sum` output supplied
the current hashes above. No mathematical proof was rerun for this
citation-only checkpoint.

The review artifact itself was checked with:

```text
git diff --check -- paper-exact-arithmetic/evidence/reviews/reductions-r2.md
git diff --no-index --check /dev/null paper-exact-arithmetic/evidence/reviews/reductions-r2.md
```

Both produced no whitespace diagnostics. The first returned 0; the
second returned 1 because the new file differs from `/dev/null`. These
are documentation checks, not mathematical tests or CI results. The
author's earlier compilation record was read, but no compilation or
experiment was rerun for these prose repairs.
