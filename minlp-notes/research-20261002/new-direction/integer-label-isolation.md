# A finite-grid isolation bound for mixed-integer labels

Date: 2026-10-02. Elementary ingredient for the mixed-integer extension
under investigation. This is a discrete isolation argument, not a novelty
claim. Its use in an exact global algorithm needs separate verification.

Let \(Z\) be any nonempty finite subset of
\(\prod_{i=1}^p\{L_i,\ldots,U_i\}\), and let \(h:Z\to\mathbb R\)
be arbitrary. Independently sample each \(\gamma_i\) uniformly from the
same \(N\)-point endpoint grid in \([-\sigma,\sigma]\), with
\(N\ge2\) and \(\sigma>0\). Minimize

\[
 h(z)+\gamma^Tz,\qquad z\in Z.
\]

Write \(\Delta\) for the difference between the two lowest values
at distinct labels. Set \(\Delta=+\infty\) if there is only one
label; tied best labels give \(\Delta=0\). Put
\(S=\sum_i(U_i-L_i)\). Then, for every \(\varepsilon\ge0\),

\[
 \Pr\{\Delta\le\varepsilon\}
 \le S\left(\frac{\varepsilon}{\sigma}+\frac1N\right).
                                                               \tag{1}
\]

The bound can of course be capped at one. For independent continuous
uniform coefficients, the same proof omits the \(1/N\) term. Numerical
integer widths enter (1); they are not replaced by their encoding lengths.

## Proof

Fix an index \(i\) and every other coefficient. Group labels by their
\(i\)-th coordinate. For each nonempty group define

\[
 a_t=\min_{z\in Z:\ z_i=t}
       \left[h(z)+\sum_{j\ne i}\gamma_jz_j\right].
\]

As a function of the remaining coefficient \(u=\gamma_i\), the
minimum is the lower envelope of lines \(a_t+tu\). Their slopes are
distinct integers. The envelope has at most \(U_i-L_i\) breakpoints
on the whole real line: active slopes decrease as \(u\) increases,
and no slope can become active on two separated open intervals.

Suppose two distinct groups have values within \(\varepsilon\)
of the group minimum at \(u\), with one attaining the minimum.
If \(u\) is already a breakpoint there is nothing to show. Otherwise,
let the winning line have slope \(t\), and select a different group
with slope \(t'\). The two lines cross within distance
\(\varepsilon/|t-t'|\le\varepsilon\) of \(u\).
Moving toward that crossing must reach a breakpoint of the lower
envelope no later than the crossing. Another line may intervene earlier;
this only decreases the distance to an envelope breakpoint.

Thus this two-group event is contained in the union of
\(\varepsilon\)-neighborhoods of at most \(U_i-L_i\) fixed
breakpoints. Each such interval has length \(2\varepsilon\).
An equally spaced \(N\)-point endpoint grid assigns an interval of
length \(\ell\) probability at most
\(\ell/(2\sigma)+1/N\). The conditional event probability is
therefore at most

\[
 (U_i-L_i)\left(\frac{\varepsilon}{\sigma}+\frac1N\right).
\]

If the original label gap is at most \(\varepsilon\), choose a
best label and a distinct second-best label. They differ in some
coordinate \(i\), and their two groups satisfy the preceding event.
Taking the union over coordinates and then integrating the conditioned
coefficients proves (1). The proof includes singleton groups, redundant
integer bounds, ties, and breakpoints at noise-grid endpoints.

## Application to a bounded mixed feasible set

Suppose \((z,y)\) ranges over a compact mixed feasible set, \(F\)
is continuous there, and the objective is
\(F(z,y)+\gamma_z^Tz+\gamma_y^Ty\). Condition on all
continuous-coordinate noise. The function

\[
 h(z)=\min_{y:\ (z,y)\text{ feasible}}
          [F(z,y)+\gamma_y^Ty]
\]

is a well-defined real cost for every feasible integer label. The bound
(1) applies without any convexity or uniqueness assumption on these
continuous subproblems. No enumeration of labels or envelope breakpoints
is required by this probability proof.

For a bounded rational mixed polytope, valid integer coordinate bounds
have polynomial encoding length. Although \(S\) may be exponentially
large, \(\log(S+1)\) is polynomial in the input length. This matters
when the bound selects a refinement cutoff through logarithmic accuracy
dependence; it does not make (1) numerically dimension-free.

Discrete isolation and adaptive exact certification are established
prior topics. The [MIQP literature audit](../prior-art/smoothed-exact-qp-prior.md)
records Beier--Vöcking's relevant predecessor, while the literature
knowledge base now includes Röglin--Vöcking's smoothed integer-programming
paper. Their conclusions should be compared before attributing any
originality to a solver that uses this elementary lemma.

This note was proved directly by the parent researcher. A fresh reviewer
checked the isolation argument, including zero-gap ties and missing groups,
and requested the explicit continuity assumption in the mixed application.
That assumption is now stated. The general MIQP theorem and its remaining
ingredients have a separate review in progress.

The parent researcher ran

```sh
python research-20261002/new-direction/check_integer_label_isolation.py
```

The exact enumeration passed eight fixtures and 2,112 complete-law noise
draws, including 247 ties. It checked 558 conditional line envelopes,
4,151 breakpoint witnesses, and 40 exact probability comparisons. The
fixtures include skipped integer labels, non-product feasible sets,
singleton labels, and a breakpoint at a noise endpoint. These are finite
diagnostics, not a proof for arbitrary label sets or an implementation of
the proposed MIQP solver.
