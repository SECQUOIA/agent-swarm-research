# Independent review of the completed upper-bound manuscript

Reviewed on 2026-10-05. Scope: `sections/03-upper.tex` and
`appendices/A-upper.tex`, against the actual models, point/value, reductions,
and constraints interfaces. This review reconstructs the arguments; it does
not adopt the prewriting audit verdicts. No manuscript file was edited.

The core unconstrained, strongly monotone, and adaptive-sign arguments are
sound on analytic reconstruction. The root repaired the rational constants,
rounded-cut answer-length assumption, and Horner update during this review;
I rechecked all three actual patches. No internal proof blocker remains.
The optional explicit-separation remark has an unresolved bibliography key,
and the rounded-ellipsoid external contract awaits literature-owner
confirmation. Full independent Opus review remains pending. The original
findings and their resolution are recorded below.

## Findings, ordered by severity

1. **P1: irrational constants enter a claimed ordinary rational algorithm.**
   `appendices/A-upper.tex:561`–`567` calls
   `Lambda_f = n^(3/2) D^3 ||f||_1 R_2^D` and
   `Lambda_h = n^(1/2) D ||h||_1 R_2^D` rational numbers of polynomial
   encoding length. For nonsquare `n` they need not be rational. They enter
   `Lambda_varphi`, `rho_varphi`, and the rational value-accuracy request at
   lines 578–590, so the construction as written does not meet its ordinary
   rational bit-model interface. **Repair:** replace `n^(3/2)` by `n^2` and
   `n^(1/2)` by `n`. These are rational upper bounds for `n >= 1`; every
   subsequent inequality, including `zeta rho_varphi <= 1/4`, remains valid.
   No new algorithm or field representation is needed. This was reported to
   the root immediately. **Resolved:** the current formulas at
   `appendices/A-upper.tex:565`–`566` use `n^2` and `n`. The larger bounds
   preserve all derivative and Newton-radius estimates.

2. **P2: the standalone rounded-cut lemma omits the bound on oracle-answer
   length needed for its bit-complexity conclusion.**
   `appendices/A-upper.tex:292`–`300` assumes only a deterministic procedure
   returning a nonzero rational cut vector. Its conclusion bounds all further
   bit operations using only `n`, `R_0`, `rho_0`, and `delta_0`; the proof
   explicitly normalizes the returned vector at lines 307–309. An arbitrarily
   long rational cut answer is allowed by the stated hypotheses. The
   normalization and a rational rounded update cannot be assigned the stated
   bound without controlling that answer length. **Repair:** require cut
   vectors of encoding length polynomial in the query length and the listed
   input parameters, with a fixed polynomial, or require a polynomial-time
   procedure and state the resulting composed polynomial bound. The actual
   polynomial-map application at lines 399–401 already supplies this property
   by exact sparse evaluation, so this is an interface repair to the lemma,
   not a missing monotone warm-start algorithm. **Resolved:** the current
   statement at `appendices/A-upper.tex:298`–`302` assumes polynomial
   returned-vector encoding length in the query length and named parameters.
   The normalization and further-bit-operation conclusion now compose
   correctly with the polynomial-map procedure.

3. **P2: one cited key is absent from the manuscript bibliography.**
   `appendices/A-upper.tex:141` cites
   `JeronimoPerrucciTsigaridas2013`, which was absent from `references.bib`
   during this review. This affects the optional explicit-separation remark
   at lines 134–146. **Repair:** have the literature owner supply its vetted
   entry and confirm the quoted theorem/version, or remove the remark. The
   main separation and Newton proofs use Basu's imported theorem and do not
   depend on this remark. This was reported to the root for literature-owner
   resolution; I did no literature research.

4. **P3: the printed Horner update doubles twice if read sequentially.**
   `appendices/A-upper.tex:152`–`155` says to replace the current `v` by
   `v+v` and then, if the digit is one, by `v+v+1`. Executing those two
   replacements makes the binary string `11` produce `5`. **Repair:** write
   the single update `v_new = 2 v_old + a_digit`, or say to double and then
   add one when the digit is one. The intended standard integer construction
   has the stated linear size, and the denominator-clearing formulas are
   otherwise correct. **Resolved:** the current text at
   `appendices/A-upper.tex:153`–`154` says to double and then add one.

## Reconstruction of the main proof obligations

### Input model and separation

The local conventions explicitly require unary exponent vectors and unary
dimension, giving `n,D <= L`; they exclude unrestricted binary-exponent
inputs. Sparse evaluation of original monomials costs polynomially many
ordinary bit operations at the short warm-start queries and polynomially
many circuit gates at Newton iterates. The variable-degree affine chart in
the slack-gap proof is evaluated, not expanded.

The scalar derivative bound follows from at most `L'` terms, coefficient
sum at most `2^(2L')`, degree at most `L'`, and the radius `2^(5L')`.
The displayed exponent `5L'^2 + (13/2)L'` is at most `10L'^2` for `L' >= 2`.
The vector bound uses the sum of component coefficient sums and does not
assume that a gradient's expanded component list still has only `L'` terms.
In the gradient case the scalar bounds on `f` provide the bounds on
`T = grad f` and `J_T = Hess f`.

Subject to the stated imported one-block QE contract, the separation proof
is complete: a nonzero eliminated polynomial must vanish at the singleton
or all signs would remain fixed in a neighborhood. Removing its zero root
factor and using its nonzero integer constant term gives
`|alpha| >= 2^(-2 tau d^(c_0 s))`. This does not require a finite complex
critical locus. In the Newton application `s <= L'`, `d <= L'`, and
`tau = 4L'`; the exponent `e = (c_0+3)L'^2` dominates
`log_2(8L') + c_0 L' log_2 L'`. The same fixed, absolute `c_0` is used
throughout the reduction.

### Newton, observables, and checked certificates

Strong monotonicity supplies a unique zero. The Brouwer/projection argument
also proves existence: the variational inequality excludes a boundary fixed
point when the radius exceeds `||T(0)||/mu`, and an interior fixed point is a
zero. The bound `||p|| <= 2^(3L)` is conservative and valid.

Differentiation gives `v^T J_T(x) v >= mu ||v||^2`; Cauchy--Schwarz then
gives `||J_T(x)^(-1)|| <= 1/mu` without symmetry. The homotopy from each
leading block to the identity stays nonsingular, hence its determinant is
positive. The elimination pivots are ratios of positive leading minors.
The Newton circuit therefore needs no pivot or sign branch, even for a
non-gradient map.

The local recurrence is `e_(t+1) <= Lambda e_t^2/(2mu)`. With
`q_t = Lambda e_t/(2mu)` and `q_0 <= 1/8`, it gives
`q_t <= 2^(-3*2^t)`. After `e(L')+1` steps, the observable error is at most
`2mu * 2^(-6*2^e) <= g/8`. The single point circuit is independent of the
observable and works for every explicit `h` of length at most `L'`.
Evaluation uses the original sparse derivative monomials, and the claimed
polynomial shared size follows without expanding previous rational values.

The six shifted comparisons are correct, including zero and nonzero
equality. The four order expressions have absolute margin at least `3g/8`;
the equality expressions have margin at least `15g^2/64`. Positive-denominator
division elimination is syntactic and preserves sharing; its division pair
`(N_a Q_b N_b, Q_a N_b^2)` is correct whenever the divisor is nonzero. It
does not introduce a hidden sign query.

The Hessian/Jacobian certificate language is distinguished from the
curvature promise. Sparse identity checking and rational positive-definite
matrix checking occur on printed polynomial-size data. The determinant--trace
margin has polynomial bit length; the inclusion of every direction monomial
`v_i` makes it a global modulus. Invalid certificates go to the no-instance
`0`, also for equality languages. The two-minima corollary uses separate
moduli and does not assume a full joint Hessian Gram. Equality hardness is
not claimed. The non-gradient example's biform and all four printed leading
minors reconstruct correctly by hand.

### Monotone warm start and supplied slack gap

For the monotone warm start, accepted residuals imply
`||x-p|| <= ||T(x)||/mu <= rho`. A rejected query satisfies
`||x-p|| > mu rho/Lambda`, and with
`delta_0 = mu^3 rho^2/(2 Lambda^3)` the cut expression is strictly less
than `-Lambda delta_0` throughout the same ball `B(p,delta_0)`. This is a
fixed positive-volume retained set, not merely the point `p`. The external
rounded-ellipsoid contract is the only imported step after these inequalities;
one-dimensional bisection is supplied separately.

With the checked rational-constant repair in finding 1, the supplied-slack-gap
proof is complete. Its feasible-point radius has polynomial bit length. The
active-set approximation has distance at most `delta/(8 sigma)` and hence
each slack is known to absolute error at most `delta/8`; the threshold
`delta/2` separates active and inactive rows. All inactive rows have positive
slack, so both signs of a sufficiently small tangent displacement are
feasible. This proves stationarity on the full active affine space even with
dependent rows and without strict complementarity.

The Hadamard/Cramer bound is chosen before the active set is known. The chart
has an identity block, so `Z^T Z >= I` retains the modulus `mu`; its norm is
bounded by the printed rational `zeta = 2^(2L+1)`. Newton in the chart uses
direct affine evaluation of the sparse original objective. The formula in
`(x,lambda)` at lines 643–655 describes stationary points on the affine space;
its unrestricted multipliers are appropriate for that purpose. It defines
the singleton `h(p_P)` with at most `2L` quantified variables, degrees at most
`L`, and coefficient bit sizes at most `4L`. The larger exponent
`e_2(L) = (2c_0+3)L^2` supplies the required gap. Full-rank, no-active-row,
and empty-polyhedron cases are handled. The gap is a supplied promise;
the text correctly makes no general deterministic constrained claim.

### Deterministic adaptive sign closure

The closure proof is internally complete. The following details were checked
directly in the completed appendix, rather than inferred from earlier audits:

- Every original gate, including control arithmetic and unselected
  interpreter candidates, counts in `S`. Thus the exact integer magnitude
  bound `B = 2^(2^S)` is valid on every Boolean input.
- For a threshold input within `1/4` of the exact integer, the shift
  `4 v_tilde - 2` has magnitude at least one and the correct positivity bit
  even when the exact integer is zero or negative. Its magnitude is at most
  `4B+3 <= B^4 = sigma_(S+2)`.
- The entire decreasing schedule
  `F_(sigma_(S+2)),...,F_(sigma_1)` compresses magnitude to `[1,2]`.
  The first `G` refinement reaches `[4/5,1]`; every subsequent error from
  the correct sign squares. Exactly `2S+5` refinements give the claimed
  threshold-bit error at most `epsilon = 2^(-2^(2S+4))`.
- With `kappa = 3B`, the absolute-error induction includes every decoder
  and control arithmetic gate. Addition/subtraction amplify by at most two;
  multiplication by at most `2B+1`; a threshold resets its own error to
  at most `epsilon`. The bound `epsilon kappa^S < 1/4` justifies each
  replacement as it is reached. Cancellation and repeated operands are
  included, and approximate internal control values need not remain bits.
- All compressor/refinement pair denominators are strictly positive.
  The final numerator `2P-Q` tests a rational approximate Boolean output
  against `1/2`. Shared repeated-square scale constants and `O(S)` work per
  threshold give `O(S^2)` integer-circuit nodes. The huge exact values,
  error budget, and expanded rational denominators are never printed.
- A fixed polynomial clock bounds the oracle machine and query length for
  all answer sequences. A polynomial Boolean parser produces padded slot,
  address, opcode, and validity bits. Operand selection sums run over earlier
  addresses; each instruction computes all arithmetic candidates but selects
  only the valid opcode on exact bits. Malformed strings give answer zero,
  with all arithmetic expressions still defined. There is one module per
  time step, so the resulting size is polynomial in the clock bound.
  No execution tree or answer-transcript enumeration is used.
- Part (b) applies only to deterministic bounded computation. It does not
  remove the nondeterministic active-set guess, Las Vegas randomness, or an
  FPT parameter factor. A vector output remains a list of output-bit
  predicates. The constraints section preserves these distinctions.

## Manuscript interfaces and external contracts

The current `sections/02-points.tex:120`–`146` defines
`lem:convex-value`, and its completed proof at `appendices/C-points.tex:328`–`434`
returns exactly feasible rational points, including on lower-dimensional
polyhedra. Its sparse/composed evaluation interface matches both upper-bound
warm starts. The two labels described as missing in the author report,
`sec:points` and `lem:convex-value`, now exist.

The cube-root upper bound is proved once in `appendices/B-reductions.tex:353`–`430`.
Its norm separation, `14L+6` Newton schedule, propagation bound, and positive
divisions agree with the pointer in Section 3. The old undefined
`lem:models-division` reference is no longer present at that handoff: the
current text cites `def:models-circuits`. The structured single-sign
corollary in `sections/05-constraints.tex:639`–`661` applies the bounded
deterministic machine theorem, while the unambiguous and Las Vegas results
retain their different models.

The source contracts are external obligations owned by the Luna literature
reviewer, not new internal proofs:

- Basu 2014 Theorem 2.27 must supply the displayed one-block degree and
  coefficient-height bounds. The supplied literature report explicitly
  confirms that contract and distinguishes its version from the 2011
  Theorem 2.16.
- GLS Theorem 3.2.1, Remark 3.2.33, and Lemma 3.2.8 must support the
  rounded cut-or-accept procedure retaining a fixed subset and polynomial
  center lengths. The internal retained-ball application is correct. I asked
  the root to obtain explicit confirmation from the literature owner because
  the supplied report does not visibly record this exact combined contract.
- The optional Jeronimo--Perrucci--Tsigaridas theorem and bibliography entry
  require literature-owner resolution as in finding 3.

The section distinguishes ordinary bit algorithms, compressed rational
arithmetic, and integer-circuit sign queries consistently. No ordinary
polynomial-time exact optimizer or PosSLP algorithm is inferred. The prior-work
language is appropriately restrained; this review makes no priority claim.

## Readiness and verification record

**Verdict: accept the repaired internal proof chain, pending full independent
Opus review and the remaining external-source work.** Findings 1, 2, and 4
are resolved in the actual appendix. Resolve or remove the optional citation
and confirm the GLS imported contract through the assigned literature
workflow before final journal-ready acceptance. No unresolved internal
obstacle was found in adaptive many-one closure, the supplied-slack-gap
comparison, or the shared Newton-point theorem.

The repaired snapshots checked before final handoff have SHA-256 hashes:

```text
2a741d3e1ae14ce32bc8b59315a1cb1cec6aa84e955b54672470394b1ce25b23  sections/03-upper.tex
42eec91386c49100c000f9c77ff728772fe5662573fe3b3fd99101b145dfce93  appendices/A-upper.tex
```

Verification was analytic proof reconstruction and targeted source reading
with `rg`, `nl -ba`, `sed -n`, `cat`, and `wc -l`. The following targeted
document check was run; it inspects only labels and citations used by the two
upper-bound files:

```text
python - <<'PY'
from pathlib import Path
import re
root = Path('paper-exact-arithmetic')
upper = [root/'sections/03-upper.tex', root/'appendices/A-upper.tex']
all_tex = list(root.glob('sections/*.tex')) + list(root.glob('appendices/*.tex')) + [root/'main.tex', root/'macros.tex']
labels = {m.group(1) for p in all_tex for m in re.finditer(r'\\label\{([^}]+)\}', p.read_text())}
refs = {m.group(1) for p in upper for m in re.finditer(r'\\(?:ref|eqref|pageref)\{([^}]+)\}', p.read_text())}
print('Upper-bound references:', len(refs))
print('Missing upper-bound labels:', sorted(refs-labels))
bib = (root/'references.bib').read_text()
keys = set(re.findall(r'@\w+\s*\{\s*([^,]+),', bib))
cited = {key.strip() for p in upper for m in re.finditer(r'\\cite\w*(?:\[[^\]]*\])*\{([^}]+)\}', p.read_text()) for key in m.group(1).split(',')}
print('Upper-bound citation keys:', len(cited))
print('Missing upper-bound citation keys:', sorted(cited-keys))
PY
```

It found 39 upper references and no missing labels, and seven citation keys
with the single missing key in finding 3. The scoped `sha256sum` command
produced the hashes above. The report whitespace check was:

```text
git diff --no-index --check /dev/null paper-exact-arithmetic/evidence/reviews/upper-r1.md
```

No computational experiment, mathematical checker, compilation, project-wide
verification, or CI status/log inspection was performed. These checks are
document and whitespace checks, not CI results.
