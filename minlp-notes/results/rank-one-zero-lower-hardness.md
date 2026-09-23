# Strong hardness with only unit upper bounds on rank-one flows

Status: proof completed and independently checked by a separate agent on
2026-09-04; 2,000 exact rational repair and penalty checks passed. This strengthens the construction in
`rank-one-row-column-hardness.md`. A targeted open-literature search found the
original two-sided-bounds conjecture and later convexifications, but no previous
statement of this restriction. This is a provisional novelty assessment.

## Statement

Let

\[
\mathcal U_{p,q}=\{W\in\mathbb R_+^{p\times q}:\operatorname{rank}W\le1,
 W\mathbf1\le\mathbf1,\ W^\top\mathbf1\le\mathbf1\}.
\]

Linear optimization over this set is strongly NP-hard. All lower bounds are
zero and all upper bounds are one; only the integer cost matrix and dimensions
vary. The feasible zero matrix does not remove the difficulty of deciding
whether the optimal value is below a specified negative threshold.

The proof gives an explicit error bound and objective penalty that remove the
two positive lower bounds used in the earlier reduction.

## Lemma: distance to two saturated margins

Fix distinguished row 0 and column 0, and define

\[
F=\{W\in\mathcal U_{p,q}:r_0=c_0=1\},\qquad
r=W\mathbf1,\quad c=W^\top\mathbf1.
\]

For every \(W\in\mathcal U_{p,q}\), there is \(W'\in F\) such that

\[
\|W-W'\|_{1,\mathrm{entry}}\le2(2-r_0-c_0).
\]

**Proof.** Write \(S=\mathbf1^\top r=\mathbf1^\top c\) and
\(\delta=2-r_0-c_0\). If \(S\ge1\), raise \(r_0\) to 1 and
decrease the other row margins by a total of \(1-r_0\). This is possible
because their sum is \(S-r_0\ge1-r_0\). The resulting vector \(r'\)
remains in the unit box and has total \(S\). Do the same for \(c\).
Then \(W'=r'(c')^\top/S\in F\), and the rank-one parametrization gives

\[
\begin{aligned}
\|W'-W\|_{1,\mathrm{entry}}
&\le \|(r'-r)(c')^\top/S\|_{1,\mathrm{entry}}
  +\|r(c'-c)^\top/S\|_{1,\mathrm{entry}}\\
&=\|r'-r\|_1+\|c'-c\|_1=2\delta.
\end{aligned}
\]

If \(0<S<1\), take \(W'=E_{00}\). Since
\((S-r_0)(S-c_0)\ge0\),
\(W_{00}=r_0c_0/S\ge r_0+c_0-S\). Therefore

\[
\|W-E_{00}\|_{1,\mathrm{entry}}
=1+S-2W_{00}
\le1+3S-2r_0-2c_0\le2\delta.
\]

For \(S=0\), \(W=0\), and \(E_{00}\) satisfies the bound directly. ∎

## Exact penalty theorem

For any cost matrix \(C\), let \(B=\max_{ij}|C_{ij}|\). For every
\(L>2B\),

\[
\min_{W\in\mathcal U_{p,q}}
\{\langle C,W\rangle-L(r_0+c_0)\}
=\min_{W\in F}\langle C,W\rangle-2L.
\]

Every minimizer on the left belongs to \(F\).

**Proof.** For \(W\notin F\), use the lemma to find \(W'\in F\).
The difference between its penalized objective and that of \(W\) is at most

\[
B\|W'-W\|_{1,\mathrm{entry}}-L(2-r_0-c_0)
\le(2B-L)\delta<0.
\]

Thus no point outside \(F\) minimizes. Compactness guarantees attainment. ∎

## Reduction and decision gap

The biclique construction in `rank-one-row-column-hardness.md`, Theorem 1,
has every upper bound equal to one. Its only positive lower bounds are the
distinguished row and column margins, both fixed at one. Thus its feasible
set is exactly \(F\) for its chosen dimensions.

For integer \(C\), set \(L=2B+1\) and replace the cost matrix by

\[
C'_{ij}=C_{ij}-L\,\mathbf1[i=0]-L\,\mathbf1[j=0].
\]

Remove both positive lower bounds. The exact penalty theorem implies

\[
\min_{\mathcal U_{p,q}}\langle C',W\rangle\le-2L
\quad\Longleftrightarrow\quad
\min_F\langle C,W\rangle\le0.
\]

The entries of \(C'\) are integers of magnitude at most \(5B+2\).
In the earlier reduction \(B\le n^2\), where \(n\) is the larger side
of the input bipartite graph, and all dimensions are linear in \(n\).
The reduction is therefore strong. Its separation between yes and no
optimal values remains at least \(1/(2n+1)\), since the optimum is shifted
by exactly \(-2L\).

This also transfers the earlier obstruction to uniformly constructible
polynomial-size, polynomial-time-solvable exact convex formulations to the
zero-lower-bound family. Stronger unconditional lower bounds are developed
separately through a correlation-polytope face.

## Interpretation and literature boundary

The result concerns source-to-terminal dependent linear costs on a rank-one
flow block. Ordinary additive inlet and outlet costs depend only on the
margins and lead to a simpler model; this theorem does not claim hardness
for that special objective.

The initial conjecture appears after Theorem 4 of
[Dey, Kocuk and Santana's open manuscript](https://arxiv.org/abs/1902.00739).
The later
[Jalilian–Kocuk manuscript](https://arxiv.org/abs/2306.10810)
establishes second-order-cone representability with row, column, and total
bounds. Neither fact supplies a polynomial-size formulation. The present
restriction and penalty lemma are separate from those established results;
a failed search for an antecedent is not proof of novelty.

## Verification record

`notes/audit-rank-one.md` records the independent check of the penalty proof.
`code/rank_one_zero_lower/verify_penalty.py` checks the repair construction,
rank, capacities, entrywise distance bound, and strict penalized improvement
using exact rational arithmetic. Its 2,000 seeded cases include 1,184 with
total flow below one, 214 at one, and 602 above one. These finite checks
supplement the proof and do not establish a complexity theorem on their own.
