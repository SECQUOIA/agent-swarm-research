# Independent review of the positive-update approximation argument

Date: 2026-09-27. Reviewer: the `gram_review` research agent, independently
of the agent developing the candidate theorem. The arithmetic subreview
was delegated to a new `rounding_check` agent.

## Conclusion and priority correction

The reviewed rational-normalization argument is mathematically sound under
its stated assumptions. I found no substantive gap in the matrix estimate,
minimum-cost representative argument, or scalar Schur-complement implication.
This is an independent review, not a formal verification or a guarantee that
all errors have been excluded.

**The spectral approximation construction is not a new repository result.**
The earlier note
[A polynomial-size spectral approximation set of feasible DAG paths](../notes/research-20260912-dag-psd-approximation-set.md)
already constructs a two-sided approximation family for rational PSD sums
in fixed dimension. It uses the same maximum-volume coverage argument,
rational normalization, bounded signed rounding, and dynamic programming.
It also handles singular matrices by enumerating their exact ranges,
which is more general than the full-rank case reviewed here.

The current incremental candidate is to retain a minimum additive-cost
representative at each existing state. That preserves **one exact additive
budget with binary-encoded costs**, without representing the budget as a
pseudopolynomial number of graph vertices. The other contribution being
assessed is the application to the regression benefit
\(g(S)=b_S^T(D_S+U_SU_S^T)^{-1}b_S\), giving a multiplicative approximation
under one budget and an additive approximation for activation cost minus
benefit. These extensions are straightforward once the earlier approximation
family is available. Their external priority and publication significance
remain unresolved; they should not be presented as a new general spectral
approximation theorem.

## Assumptions and proof checks

The reviewed model supplies rational \(D\succ0\), rational
\(U\in\mathbb Q^{n\times r}\), and rational \(b,c\), with fixed \(r\).
Activation costs may have either sign. Take rational
\(0<\varepsilon<1\), and handle \(n=0\) directly. Write \(d=r+1\),
\(W_i=(u_i,b_i)(u_i,b_i)^T/D_{ii}\), and
\(K(S)=\operatorname{diag}(I_r,0)+\sum_{i\in S}W_i\).

1. **Coverage by anchors.** If some selected \(b_i\ne0\), the fixed
   coordinate vectors and selected generators span \(\mathbb R^d\), even
   if \(U\) is rank deficient. A maximum-volume generator basis has every
   target generator coordinate bounded in absolute value by one. Hence
   \(\operatorname{tr}(A_B^{-1}W)\le d\) for every target and fixed atom.
   Enumerating all bases therefore covers each target; the algorithm does
   not need to solve a maximum-volume problem.
2. **Rational normalization.** Exact \(A_B=L\Delta L^T\) and dyadic
   scaling give \(R=SL^{-1}\) with
   \(I\preceq RA_BR^T\prec4I\). Directly,
   \(R^TR=L^{-T}S^2L^{-1}\prec4A_B^{-1}\). Admitted transformed atoms
   have trace at most \(4d\), and hence bounded entries. All arithmetic
   can be rational with polynomial encoding length. No square-root or
   sum-of-radicals oracle is needed.
3. **Equal keys.** Round only selectable atoms using
   \(\delta=\varepsilon/(dn)\). For each entry, every floor remainder
   belongs to \([0,\delta)\), including for negative entries. Two support
   remainder sums differ by at most \(n\delta\), even when their
   cardinalities differ. The fixed matrix cancels exactly.
4. **Matrix error.** The symmetric difference has spectral norm at most
   \(dn\delta=\varepsilon\). Forced anchors give
   \(RK(S)R^T\succeq I\). Thus representatives with the same key satisfy
   \[(1-\varepsilon)K(S)\preceq K(T)
     \preceq(1+\varepsilon)K(S).\]
5. **Cost pruning.** At a fixed stage, equal keys and equal auxiliary
   states have the same permitted future choices. Replacing a prefix by
   the one of least additive cost cannot increase final cost. Negative
   costs cause no difficulty in this finite acyclic recurrence. For a DAG
   extension, the current vertex and anchor-owner state must also be kept,
   as in the earlier note.
6. **Schur complement.** The identity
   \(g(S)=\min_y(y,1)^TK(S)(y,1)\) transfers the lower matrix bound to
   \(g(T)\ge(1-\varepsilon)g(S)\). Congruence is first undone, so the
   affine slice \((y,1)\) is taken in the original coordinates. Also
   \(0\le g(S)\le\sum_i b_i^2/D_{ii}\).

The resulting pair guarantee is
\(c(T)\le c(S)\) and \(g(T)\ge(1-\varepsilon)g(S)\).
It immediately yields a fully polynomial approximation scheme, for fixed
\(r\), for maximizing \(g(S)\) under one exact additive budget.
Recording cardinality permits a simultaneous cardinality restriction.
For minimizing \(c(S)-g(S)\), the resulting error is at most
\(\varepsilon g(S^*)\), and hence at most
\(\varepsilon\sum_i b_i^2/D_{ii}\).

## Corrections and limitations

- With cardinality constraints, the zero-benefit fallback needs care.
  For exact cardinality \(k\), choose the \(k\) cheapest indices with
  \(b_i=0\). For an upper bound \(k\), choose up to \(k\) cheapest
  negative-cost such indices. For a representative statement at every
  cardinality, retain the cheapest zero-benefit support at each feasible
  cardinality. Selecting every negative-cost zero-benefit item is valid
  only without a binding cardinality restriction.
- The supplied rational-factor assumption is material: a rational PSD
  matrix need not have a rational unweighted Gram factor of the same
  rank. A weighted rational factorization can address this, but that
  extension must be stated and proved. The earlier DAG theorem already
  uses weighted rational factors.
- One minimum-cost representative does not preserve two independent
  exact resource budgets. Arbitrary matroid or other feasibility
  restrictions also do not follow without an appropriate state space.
- If costs may be negative, an intermediate prefix whose cost exceeds
  the budget cannot be rejected solely on that basis: later negative
  costs may restore feasibility. Filtering final representatives by the
  budget is valid. The reviewed recurrence retains intermediate states.
- The additive guarantee for \(c-g\) may be weak when cost nearly cancels
  benefit. It is not a multiplicative guarantee for that objective.
- Fixed dimension is essential to the stated polynomial bound. The
  construction has a large dimension-dependent exponent and establishes
  no practical solver speedup.
- The full-rank proof does not justify a general multivariate-response
  extension with singular target matrices on its own. Exact range
  handling is available in the earlier repository theorem.

## Targeted computational verification

The exact mathematical check was run once as a Python stdin heredoc from
the repository root. Its complete command, including the exact Python
body, is retained verbatim in
[positive_update_gram_review.sh](checks/positive_update_gram_review.sh).
The output copied from that completed tool call is retained in
[positive_update_gram_review.stdout.txt](checks/positive_update_gram_review.stdout.txt).
The retained command has not been rerun: this avoids duplicating the
parent agent's separate verification.

The replay command is:

```sh
bash research-20260927/checks/positive_update_gram_review.sh
```

That replay command is provided for reproducibility; it is not an
additional command claimed to have been run. A preliminary command
actually run was:

```sh
python - <<'PY'
import sympy
print(sympy.__version__)
PY
```

It reported SymPy `1.14.0`. The mathematical check used exact SymPy
rationals, seed `9817`, 12 instances with five items, scalar positive
updates, \(\varepsilon=4/5\), and costs sampled from integers \(-3\)
through \(4\). It enumerated allowed supports in each branch, grouped
them by exact rounded keys, and selected the least-cost member of each
group. It checked the lower PSD bound using all principal minors of a
two-by-two matrix, the scalar benefit bound, and cost nonincrease.

All 602 target–representative comparisons passed across 86 branches,
including 204 additional members of colliding key groups. The count
includes identity comparisons. The script does not implement or verify
the dynamic program, the upper PSD bound, global branch coverage,
cardinality handling, general dimensions, Turing bit complexity, or
novelty. Those claims rest on the proof review. This was a local targeted
check; no project-wide verification or CI inspection was performed.

The nested arithmetic reviewer independently reported 250 exact rational
SPD normalization cases in dimensions one through five. Its retained
review and checker locations are recorded separately in
[positive-update-normalization-review.md](positive-update-normalization-review.md).
That review checks normalization arithmetic, not the entire selection
algorithm or its priority.

## Literature examined

The primary external comparison examined in this review is
[Das and Kempe, *Algorithms for Subset Selection in Linear Regression*,
STOC 2008](https://david-kempe.com/publications/regression.pdf), especially
Section 4 and Theorem 4.1. It gives a multiplicative approximation scheme
for regression error reduction when the covariance graph has constant
bandwidth and the condition number is polynomially bounded. Its running
time depends polynomially on that condition number. The positive-update
application concerns a different, potentially dense covariance class and
does not need a numerical conditioning bound. This comparison does not
establish that the current application is novel.

Searches included `"fully polynomial" "experimental design" "dimension"`,
`"FPTAS" "sensor selection" covariance`,
`"matrix" "knapsack" "FPTAS" positive semidefinite`,
`Das Kempe algorithms subset selection linear regression FPTAS low rank diagonal covariance`,
`"experimental design" "FPTAS"`, and
`"matrix knapsack" "approximation" fixed dimension`.
These limited searches did not settle later work on fixed-factor
covariances, cost-preserving spectral families, or equivalent formulations.
No novelty claim should be inferred from an unsuccessful search.
