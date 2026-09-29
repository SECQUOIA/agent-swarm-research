# Independent review of the moment-to-star projection transfer

Date: 2026-09-25.

## Verdict

The transfer theorem in `tree-indicator-moment-gluing.md` is correct for free real continuous variables, interior leaf marginals, and local compatibility order at least one. Every point that passes the stated local compatibility tests but fails full joint compatibility can, after complementing selected indicators, be exposed by the epigraph objective of a positive definite quadratic star. The gap survives projection to the original variables and passage to the closed convex hull.

The proof does not require continuity of the infimum of a linear objective over an unbounded set. The proposed nonnegative perturbation gives a direct lower bound and resolves that concern. Positive definiteness resolves the separate concern about taking the closed hull while the means and marginal probabilities vary along an approximating sequence.

This review independently checks the proof. It does not establish novelty, verify the separate quantum incompatibility constructions, or prove a lower bound for arbitrary extended formulations.

## Precise setup

Fix a center mean \(m\in\mathbb R\), leaf marginals \(z\in(0,1)^n\), and an integer \(k\ge1\). For a tuple \(q=(v,s,r)\), put

\[
 M(q)=\begin{pmatrix}1&m\\m&v\end{pmatrix},\qquad
 M_i(q)=\begin{pmatrix}z_i&s_i\\s_i&r_i\end{pmatrix}.
\]

Let \(C(m,z)\) consist of tuples admitting matrices \(G_S\succeq0\), indexed by \(S\subseteq[n]\), with

\[
 \sum_SG_S=M(q),\qquad
 \sum_{S\ni i}G_S=M_i(q).
 \tag{1}
\]

Let \(C_k(m,z)\) require this property for every subfamily of at most \(k\) leaves, using the same total matrix and singleton matrices. Assume

\[
 q^*\in C_k(m,z)\setminus C(m,z).
 \tag{2}
\]

The assumption implies \(k<n\). Both sets impose \(0\preceq M_i\preceq M\), so

\[
 v\ge m^2\ge0,\quad 0\le r_i\le v,\quad
 |s_i|^2\le z_i r_i.
 \tag{3}
\]

## Closure and strict separation

The full set \(C(m,z)\) is nonempty: take the constant center value \(m\) and independent Bernoulli indicators of means \(z_i\). It is convex because (1) is linear in the PSD matrices.

For closedness, take a convergent sequence of tuples in \(C(m,z)\), and choose one joint decomposition for each tuple. Every summand satisfies

\[
 0\preceq G_S\preceq M.
\]

The total matrices converge and therefore have bounded trace. All finitely many summands are bounded, so a common subsequence converges to PSD matrices satisfying (1) at the limit. Thus \(C(m,z)\) is closed. This bounded-fiber argument is necessary: a linear image of a closed PSD cone is not automatically closed.

Strict separation of a point from a nonempty closed convex set now gives

\[
 L(q)=av+\sum_i(u_i s_i+c_i r_i)\ge\ell
 \quad(q\in C(m,z)),\qquad
 L(q^*)=\ell-\delta,quad\delta>0.
 \tag{4}
\]

No compactness of \(C(m,z)\) is needed. For example, its nearest point to \(q^*\) supplies such a separating functional.

## Recession directions and complementation

For every support \(S\), adding \(\tau\operatorname{diag}(0,1)\) to \(G_S\), with \(\tau\ge0\), preserves feasibility of (1). The resulting increase of the left side of (4) is

\[
 \tau\left(a+\sum_{i\in S}c_i\right).
\]

Consequently,

\[
 a+\sum_{i\in S}c_i\ge0\quad\text{for all }S\subseteq[n].
 \tag{5}
\]

For every index with \(c_i>0\), complement its indicator. This replaces

\[
 (z_i,s_i,r_i)\longmapsto(1-z_i,m-s_i,v-r_i).
 \tag{6}
\]

Relabeling the patterns proves that (6) preserves full and every local compatibility condition. The transformation is affine and invertible on the fixed-mean slice.

If \(P=\{i:c_i>0\}\), the transformed coefficient of \(v\) is \(a+\sum_{i\in P}c_i\), the transformed coefficients of \(s_i,r_i\) for \(i\in P\) are \(-u_i,-c_i\), and the additive constant is \(m\sum_{i\in P}u_i\). Absorb that constant into \(\ell\). Dropping primes gives

\[
 L(q)=av+\sum_i(u_i s_i-w_i r_i),\qquad
 w_i\ge0,\qquad a\ge\sum_iw_i.
 \tag{7}
\]

The last inequality follows from the full-support case of (5) in the transformed coordinates. The separation gap \(\delta\) is unchanged.

## A perturbation that preserves the gap

Define

\[
 R(q)=(n+1)v-\sum_i r_i=v+\sum_i(v-r_i).
\]

By (3), \(R\ge0\) throughout \(C_k(m,z)\), including \(C(m,z)\) and \(q^*\). Choose, for example,

\[
 \varepsilon=\frac{\delta}{2(1+R(q^*))}>0,
 \qquad L_\varepsilon=L+\varepsilon R.
 \tag{8}
\]

Then

\[
 L_\varepsilon(q)\ge\ell\quad(q\in C(m,z)),\qquad
 L_\varepsilon(q^*)<\ell-\delta/2.
 \tag{9}
\]

The new coefficients are

\[
 a_\varepsilon=a+(n+1)\varepsilon,\qquad
 w_{i,\varepsilon}=w_i+\varepsilon>0,
\]

and hence

\[
 a_\varepsilon-\sum_iw_{i,\varepsilon}
 =a-\sum_iw_i+\varepsilon\ge\varepsilon>0.
 \tag{10}
\]

This argument controls the infimum directly; an argument based only on an unspecified small perturbation would leave a gap on this unbounded set. Again drop the perturbation notation.

## Exact objective identity

Take a star with

\[
 d_i=b_i=w_i>0,\qquad
 Q=\begin{pmatrix}a&w^T\\w&\operatorname{diag}(w)\end{pmatrix},
 \qquad y_i=\frac{z_i u_i}{2w_i}-s_i^*.
 \tag{11}
\]

Its Schur complement is \(\gamma=a-\sum_iw_i>0\), so \(Q\succ0\), and every star edge is nonzero. This choice avoids the square roots in the alternative choice \(d_i=1,b_i=\sqrt{w_i}\).

For the usual conditional leaf minimization, the moment objective is

\[
 F(q)=av+\sum_i\frac{w_i(y_i+s_i)^2}{z_i}-\sum_iw_i r_i.
 \tag{12}
\]

Expansion gives

\[
 F(q)=L_\varepsilon(q)+C+
       \sum_i\frac{w_i}{z_i}(s_i-s_i^*)^2,
 \qquad
 C=\sum_i\left(\frac{z_i u_i^2}{4w_i}-u_i s_i^*\right).
 \tag{13}
\]

The use of the symbol \(L_\varepsilon\) in (13) refers to the perturbed coefficients, denoted simply by \(a,w\) in (11)–(12). Therefore

\[
 F(q^*)<\ell+C-\delta/2,\qquad
 F(q)\ge\ell+C\quad(q\in C(m,z)).
 \tag{14}
\]

This proves a strict separation of objective values without requiring \(q^*\) to optimize the local relaxation.

## Why the original closed epigraph obeys the lower bound

Consider any finite convex combination of original indicator-feasible points. Let \(X\) be the scalar center coordinate, \(Z_i\) the leaf indicators, and \(Y_i\) the leaf coordinates. Its scalar moments give a tuple in the full set. Conditional square completion and Jensen's inequality give

\[
 \mathbb E\left[aX^2+\sum_i(w_iY_i^2+2w_iXY_i)\right]
 \ge F(v,s,r)
\]

when the mean of \(Y_i\) is \(y_i\). Thus (14) bounds every convex combination at the prescribed means and marginals.

For passage to the closed hull, fixed-slice separation alone is insufficient: an approximating sequence can have varying means and marginals. Instead, take such a sequence with bounded epigraph coordinates. Because \(Q\succ0\), there is \(\lambda>0\) with

\[
 \lambda\,\mathbb E\|(X,Y)\|^2
 \le\mathbb E[(X,Y)^TQ(X,Y)]\le t.
\]

This bounds the center second moments. The corresponding joint matrices satisfy \(0\preceq G_S\preceq M\), so all their entries have a convergent subsequence. Passing to the limit in their defining equalities produces a decomposition (1) at the target \(m,z\). Because the target masses \(z_i\) are positive, the expression (12), including its dependence on the leaf means and masses, is continuous along this subsequence. The limiting epigraph coordinate is consequently at least \(\ell+C\).

This argument also permits approximating points with center-indicator mean below one. The scalar moment construction is valid for those points as well; at the target the center indicator is fixed to one. Thus no face-closure assumption is being used.

The locally feasible epigraph point with coordinate \(t=F(q^*)\) violates this bound by more than \(\delta/2\). This establishes a strict gap after projecting out every auxiliary moment.

## Additional consequence: exact full-moment optimization is attained

For the positive definite star in (11), the minimum of (12) over \(C(m,z)\) is the exact ordinary-convex-hull epigraph value at these means and marginals, and it is attained. This slightly stronger fact is not needed for the transfer proof.

Indeed, by (3),

\[
 F(q)\ge\left(a-\sum_iw_i\right)v=\gamma v.
\]

Any nonempty sublevel set therefore has bounded \(v,r,s\). It is closed by the proved closedness of \(C(m,z)\), so a minimum exists.

Choose a joint PSD decomposition of a minimizer. If a summand has zero mass, it must be \(G_S=\operatorname{diag}(0,\rho)\), with \(\rho\ge0\). Deleting it preserves all prescribed first moments and masses and reduces (12) by

\[
 \left(a-\sum_{i\in S}w_i\right)\rho\ge\gamma\rho.
\]

Optimality forces every such \(\rho\) to vanish. Every remaining matrix has positive mass and is the moment matrix of a scalar measure with at most two atoms. These measures, labeled by their supports, define an actual common law. On it, set

\[
 Y_i=Z_i\left(\frac{y_i+s_i}{z_i}-X\right).
\]

Then \(\mathbb EY_i=y_i\), the on/off constraints hold, and every conditional Jensen bound is attained. This gives a finite convex combination attaining \(F\), with at most two atoms per support. It also explains why the zero-mass second moments allowed by the PSD closure do not obstruct exact optimization for a positive definite star.

## Scope and unresolved questions

- The theorem transfers an established local-versus-global incompatibility; it does not itself construct one for every order. Such constructions must be checked independently, including their interior-marginal assumption after conversion to scalar moments.
- Complementation is part of the construction. The theorem does not promise a gap at the initial uncomplemented marginals for a preselected quadratic objective.
- The construction is existential. It does not give a polynomial-time method to find the separating coefficients or control the resulting conditioning, coefficient sizes, or gap as a function of the number of leaves.
- Free continuous variables are essential to the stated realization argument. Finite bounds, nonnegativity restrictions, and fixed sign patterns of the coupling coefficients require separate analysis.
- The result concerns this local scalar-moment hierarchy. It says nothing against exact formulations based on different auxiliary variables or the known algorithms for tree-supported quadratics.
- No literature novelty search was performed in this review. The proof is an original-to-this-session derivation, which is weaker than a verified originality claim.

## Targeted verification

An inline `python` command using SymPy expanded the one-leaf identity (13) with symbolic \(w,z,u,s,s^*\) and checked it exactly. The same command checked that the perturbation changes the star Schur margin by exactly \(\varepsilon\) for four symbolic leaves; the general formula is proved in (10). It printed:

```text
PASS: exact square identity and perturbation Schur margin
```

These checks verify the algebra, not separation, compactness, novelty, or the quantum constructions. Those proof steps were checked directly above. No project-wide verification or CI inspection was performed.
