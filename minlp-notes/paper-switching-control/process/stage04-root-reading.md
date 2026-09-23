# Stage 4 primary-agent investigation and audit

## Three-mode chamber representation

Independently derived the floor-state representation from generic nonintegral cumulative prefixes. At prefix j the sum of fractional parts is sigma in {1,2}; the three integral count nodes are f+e_i or f+1-e_i. Each adjacent floor increment has coordinates 0 or 1 and total 1+sigma_old-sigma_new. The four transition families therefore exhaust all possibilities. A node transition is allowed precisely when its count increment is a unit vector. Every local transition graph has no isolated row or column. Thus every node can be extended both to the beginning and the end of a full integer path. Averaging all paths realizes strict floors simultaneously, proving sufficiency without a numerical feasibility oracle.

The count matrix is [[3,1],[3,3]], initially (1,0). Exact min-switch dynamic programming tracks nine values, indexed by count node and final label. Independent enumeration gives 396 histories at N5, 1872 at N6, and 8856 at N7. Generic perturbation for arbitrary N must use a denominator greater than N and nonzero coordinates, rather than reusing the fixed denominator7 at larger N.

## Exact continuous three-mode/two-switch value

Read the repository's five-cell theorem and the published-source transcript. Once the five-cell upper is independently verified, accepted cell-averaging domination implies F_{3,2}(T)<=T/5. Sager–Zeile Proposition4 already supplies the matching continuous lower bound; novelty must be confined to completing equality, not inventing that lower bound.

The alternative pure input01201 on T5 also gives a short direct lower proof. Its terminal masses are (2,2,1) and first unit-mass times (1,2,3). Any error E<1 requires all three modes, each exactly once within three blocks. If i is last and starts at v, positive discrepancy before its activation gives v<d_i, whereas terminal negative discrepancy gives v>=5-m_i-E>5-m_i-1>=d_i. Contradiction. The word012 at times2 and4 attains1.

## A sharp seven-cell development

The natural proposed extension—2s+1 cells always admit unit error with s switches—is false already at s3. Exact enumeration gives minimum-switch chamber counts at N7:

    0:3, 1:414, 2:4542, 3:3891, 4:6.

The six exceptions form exactly the permutation orbit of the floor history

    (0,0,0), (1,0,0), (1,1,0), (1,1,1),
    (2,1,1), (2,1,1), (2,1,2).

This classification leads to a complete new minimax value, F_grid(3,7,s3)=4/3, rather than just a counterexample. For that chamber, the words1200022,0021122,0011220 each have three switches and respect every floor/ceiling count except, respectively, mode0 at prefix2, mode1 at prefix3, and mode2 at prefix4, where the count is0. Their errors are bounded by max(1,A0(2)), max(1,A1(3)), and max(1,A2(4)). Monotonicity and conservation give A0(2)+A1(3)+A2(4)<=4. One of these schedules therefore has error<=4/3. All other chambers admit error<1, and continuity covers all boundary profiles. I checked the complete exceptional orbit and the three words' sole exceptional coordinates exactly.

For sharpness take unit-cell rates

    u,e0,e1,e2,e0,u,e2, with u=(1/3,1/3,1/3).

Its cumulative triples, multiplied by3, are (1,1,1),(4,1,1),(4,4,1),(4,4,4),(7,4,4),(8,5,5),(8,5,8). An integer prefix outside its floor/ceiling box differs by at least4/3. Its chamber requires four switches, so every schedule with at most three switches has error>=4/3. Direct enumeration of all2187 words confirms its exact optimum4/3, attained for example by0011022. This is a rational instance certificate, while the general upper depends on exhaustive chamber classification and the analytic three-word argument. The stage author must reconstruct and verify these facts independently; five independent reviews remain required.

## Six-cell consequence

All1872 six-cell chambers have minimum switch count at most3. The pure alternating input010101 forces error>=1 for three-switch grid schedules: below1 its integral prefix counts must agree exactly and hence require five switches. Thus F_grid(3,6,s3)=1. Cell averaging gives the new continuous upper F_{3,3}(T)<=T/6, improving the heavy-only T/5 bound, while the published lower remains T/7. The seven-cell upper4T/21 is weaker and should not be presented as the best continuous consequence.

## Limits of exploratory work

The root's unbounded normalized-state exploration did not close a finite automaton. Cost truncation changes the optimization and does not establish a general budget theorem. Those exploratory programs are not mathematical proof dependencies. The exact small-N enumeration above and the author's independent replacement checker are the intended finite proof route. No statement here proves the continuous three-switch value or an arbitrary-budget formula.

## Full arbitrary-grid one-switch proof reading

Read the author's Section08 in full against the original result and proof. The largest-final-mass dominance is valid for both the omitted coordinate and final deficit. The two closed LP families cover every extremal obstruction using thresholds strictly below the optimum and a compactness limit; the equality case F=T/3 has an explicit feasible point. The two-large-mass family reduces exactly to H, including cutoff ties at T/3. Its displayed witness satisfies cumulative conservation and terminal ordering.

The one-distinguished-mode symmetrization is needed only for the m2<=E coverage branch; averaging the other terminal masses moves the reverse order's first eligible switch later, where the distinguished deficit cannot decrease. Reconstruction of x and y from the M interval satisfies both distinguished and aggregate-other monotonicity, including coincident a=b and final b=N. Comparing the four lower M bounds with the two upper bounds gives precisely the listed five nontrivial comparisons and one time-only feasibility inequality. I checked these algebraic directions independently. Every rational formula has fixed algebraic depth, so the compressed bit-complexity claim is appropriate.

The three-mode residue proof handles N2 and the isolated N1 exception. The n5N9 witness and its separate universal upper proof are valid. The failed two-bound simplification is accurately presented as missing feasibility/cutoff conditions, not as a defect in the final formula. No issue identified in this reading; the full new chamber section and five independent reviews remain pending.

## Live primary-source audit

Checked the publisher's current HTML article and its indexed final 49-page PDF, DOI10.1007/s10589-020-00244-5, on 2026-09-07. Corollary4's attainment proof is on printed p610 (PDF page35) and explicitly uses N=k(3+2s)+2+s. Corollary5 is on printed p611 (PDF page36), states the lower (N+s+1)/(3+2s) times maximum width for n>2 and 1<=s<=N-2, and does not include that congruence restriction. At N5,s2 its lower8/7 conflicts with the exact grid value1. Proposition4 begins on printed p612 (PDF page37), with proof through p614; its second branch supplies T/(2s+4-n), including the three-mode lower bounds used here. This confirms the final-version locators independently of the local preprint. The publisher's PDF screenshot endpoint failed to render, so this audit used the final PDF's indexed text together with the full HTML equations, not claimed visual inspection of those source pages.

Primary URLs: https://link.springer.com/article/10.1007/s10589-020-00244-5 and https://link.springer.com/content/pdf/10.1007/s10589-020-00244-5.pdf . These observations establish source scope, not a comprehensive priority claim.

## First complete floor-section reading

Read Section09 in full after the new seven-cell result was incorporated. The four local edge graphs are correct; their nonempty rows and columns establish every node's participation in a complete path and hence strict realizability. The nine-entry minimum-switch recursion counts changes after the free initial label. Full history counts, the N6 distribution, the exact N7 exceptional orbit, the printed single-instance matrices, and the three repair-word exceptions agree with my independently written computation. The prime-denominator perturbation handles all prefix coordinates and measurable inputs enter through the accepted endpoint/cell-averaging lemma. The continuous equality and band use the appropriate grid-to-continuous direction. No theorem extends unit-error rounding to arbitrary budgets or claims the exact continuous three-switch value. The author was asked to update the section title to reflect all three grids. Full verification handoff and five independent reviews remain pending.
