# Topic 28 frozen claims

Status: all obligations proved; see [coverage](COVERAGE.md) and
verification. These are mathematical obligations fixed
from the source inventory, not a list of already proved
declarations. A stronger internal statement is acceptable when its explicit
specialization proves the source conclusion with its original hypotheses.

Use topic 27's finite real symmetric-matrix system
`f_i(x)=x^T A_i x+2 b_i^T x+c_i`, strict set `S={x : ∀i, f_i(x)<0}`,
closed set `T={x : ∀i, f_i(x)≤0}`, and ordinary convex hull. A nontrivial
convex certificate has nonzero nonnegative weights, PSD `A_lambda`, and
`(A_lambda,b_lambda)≠(0,0)`. AHC and HHC retain their original meanings.

| ID | Required conclusion |
|---|---|
| C01 | Prove that every nontrivial convex certificate puts `T` inside a proper convex closed quadratic sublevel set. Prove the required unboundedness above, including a nonzero PSD quadratic part and a zero quadratic but nonzero linear part. This implication needs neither strict feasibility nor AHC. |
| C02 | Source Corollary 1: if `S` is nonempty and AHC holds, prove `conv(T)≠univ ↔ ∃lambda, Certificate lambda`, and `conv(T)=univ ↔ conv(S)=univ`. Supply the HHC specialization through the existing implication to AHC. |
| C03 | Define the actual Shor projection `P={x : ∃X, [1 x^T; x X] PSD ∧ ∀i, ⟨A_i,X⟩+2 b_i^T x+c_i≤0}`, with the real symmetric matrix inner product. Prove its equivalence to witnesses `Y PSD` with `f_i(x)+⟨A_i,Y⟩≤0`, using `X=xx^T+Y`. Establish the required PSD trace pairing, convexity of `P`, and `S⊆T⊆P`. |
| C04 | For every nonnegative weight vector with PSD aggregate, prove `P⊆{x : f_lambda(x)≤0}`. Deduce that any nontrivial certificate makes `P` proper, without AHC or strict feasibility. |
| C05 | Source Corollary 4: if `S` is nonempty and AHC holds, prove `P=univ ↔ conv(S)=univ ↔ conv(T)=univ`, with the HHC specialization. The headline must concern C03's actual Shor projection. |
| C06 | Source Lemma 4: if `S` is nonempty, prove `P=univ ↔` every convex certificate is trivial, equivalently absence of a nontrivial certificate. No hyperplane-convexity premise, closed-image-cone premise, or supplied duality/separation certificate is permitted. A proof through `C={ (⟨A_i,Y⟩)_i : Y PSD }+R_+^m` must establish the dual description and justify passage from its closure to membership; an alternative exact proof must discharge the same feasibility conclusion. |
| C07 | Source Corollary 3, coefficient formulation: prove that absence of nontrivial certificates is equivalent to vanishing of `(A_lambda,b_lambda)` for every nonnegative weight vector with PSD aggregate, and equivalently for all such vectors normalized by `∑i lambda_i=1`. Derive normalization and handle infeasibility of the normalized set. Under nonempty `S` and HHC, connect these conditions to `conv(S)=univ`; an AHC strengthening is welcome. |
| C08 | Source Corollary 3, SDP formulation: on the normalized spectrahedron prove compactness, and attainment of every signed coordinate objective when feasible. Prove the equivalence between C07's vanishing condition and every signed coordinate SDP having optimum zero or being infeasible. Use coordinates of the symmetric matrix and linear vector, or prove a bridge from redundant matrix coordinates; account for `n(n+1)/2+n` independent coordinates and `n(n+1)+2n` signed programs, each with `m` nonnegative variables and one `n×n` PSD block. No floating-point or solver claim is included. |
| C09 | Define the closed-system example on `R^3`: `f_1=x_1 x_2-1`, `f_2=1-x_1 x_2`, `f_3=x_1^2-x_2^2`. Prove `S=∅`, `T≠∅`, `T={x : x_1 x_2=1 ∧ x_1^2≤x_2^2}`, `conv(T)⊆{x : |x_1|≤1}`, and properness of `conv(T)`. Prove that all nonnegative PSD aggregates have zero quadratic and linear parts. |
| C10 | Prove actual HHC of C09's example. A proved two-form convexity theorem and linear-image reduction suffice; assuming Dines' conclusion or HHC does not. Together with C09, state explicitly the failure of the closed-system equivalence when strict feasibility is removed. |
| C11 | Define the relaxation-strength example on `R^3`: `f_1=x_1^2-4`, `f_2=-x_1^2+2x_1+3`. Prove `S={x : -2<x_1 ∧ x_1< -1}`, nonemptiness, convexity and properness, actual HHC, and that nonnegative weights give a PSD aggregate exactly when `lambda_1≥lambda_2`. Every nonzero such aggregation is strictly negative at zero, although zero is outside `conv(S)`. Thus the intersection of globally convex strict aggregations does not equal the hull. |
| C12 | For C11, exhibit the actual Shor witness `x=0`, `X=diag(7/2,0,0)`, prove block PSD and both residuals equal `-1/2`, and deduce `0∈P` but `0∉conv(S)`. Combine with the proved consequences to show that this Shor projection is proper yet strictly larger than the hull even under HHC. |

The package excludes the full good-aggregation hull theorem behind source
Corollary 2; source Corollary 5's general sufficient convexity criteria; the
closed example's additional assertion about BDS-good aggregations and
Remark 2.24; other examples; numerical SDP solver correctness; algorithms
for testing HHC; complexity and novelty claims; and the separate infinite
aggregation development. These exclusions do not weaken C01–C12.
