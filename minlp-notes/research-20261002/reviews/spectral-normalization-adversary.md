# Adversarial review: rational spectral normalization

Date: 2026-10-02. Reviewed [the normalization note](../new-direction/spectral-normalization.md), including its exact range projection, rational Jacobi construction, and bit-complexity argument. Two fresh independent reviews separately checked the spectral argument and the arithmetic argument. No material gap or counterexample was found.

The supported conclusion is precise: given a symmetric rational matrix A and a rational bound H >= ||A||_2, one can construct in polynomial bit complexity a rational matrix U with exactly k independent columns, where k is the negative inertia, such that ||U||_2 <= 1 and A + 2HUU^T is positive semidefinite. The construction handles zero eigenvalues exactly. This conclusion does not independently establish the downstream optimization algorithm or a novelty claim.

## Attempts to break the proof

**An exponentially small nonzero eigenvalue does not introduce a numerical oracle.** For rank d > 0, the nonzero characteristic coefficient of the integral matrix D0 A proves that the product of its d nonzero eigenvalues has magnitude at least one. Therefore the stated bound mu = 1/(D0^d H^(d-1)) is valid. Both its encoding length and log(H/mu) are polynomial in the input length. Taking a product of input denominators is enough; no least common multiple or spectral computation is required. The proof remains valid when 0 < H < 1: mu <= H, so H/tau >= 16n^2 and the precision logarithms are positive. If H = 0, A = 0 and the initial rank-zero return avoids every division by H.

**The rational rotation really makes the chosen entry small.** Direct expansion gives the stated quartic numerator. At the chosen endpoint its two nonzero contributions have sign opposite to b, including when the two diagonal entries agree. Exact bisection therefore has a valid bracket. Since a principal block of an orthogonal conjugate has norm at most H, differentiating its rotation gives the claimed 4H bound. Root accuracy tau/(8H) consequently gives an off-diagonal entry of magnitude at most tau/2. The use of a negative endpoint requires an ordered interval in an implementation; the supplied checker does this.

**Approximate diagonalization still has a polynomial number of rotations.** A plane rotation preserves the sum of squares of all off-diagonal entries involving a third coordinate. Its only net change to the off-diagonal Frobenius energy is twice the change of the selected entry's square. Selecting a maximum entry and reducing its magnitude by at least a factor two gives the stated contraction. The sufficient stopping condition F <= tau^2 yields the claimed bound even though the actual loop may stop sooner. Neither distinct eigenvalues nor a gap between negative eigenvalues is needed.

**Exact arithmetic does not have an unaccounted denominator recurrence.** For t = m/2^b, a rotation has common denominator 2^(2b)+m^2, with O(b) bits. A product of rotations has the product of their denominators as a common denominator. The bit lengths add, and exact orthogonality bounds the numerators by that denominator. Entries of Q^T A Q have a common denominator dividing D0 times the square of that product. Thus repeated updates do not repeatedly square all earlier denominators. Reduced fractions or an explicit common-denominator implementation give the claimed polynomial arithmetic cost. The exact range projector also has polynomial encoding length by rational Gaussian elimination and determinant bounds.

**The diagonal threshold selects exactly the negative inertia.** Sorted-eigenvalue perturbation compares diag(a_j) with Q^T A Q. Because every negative eigenvalue is at most -mu and every other eigenvalue is nonnegative, exactly k entries are below -mu/2. A selected column's residual is at most e, and its component outside the negative eigenspace is at most 2e/mu. The equal-rank projector identity used to sum these errors is exact, including repeated negative eigenvalues.

**Kernel leakage is the main possible failure, and the range projection fixes it.** An approximate negative subspace alone is insufficient: for A = diag(-1,0), a tilted unit vector b gives det(A+2bb^T) < 0 whenever its kernel component is nonzero. The exact projection U = R Bminus is therefore substantive. It makes UU^T vanish on ker(A), while R Pi R = Pi transfers the projector error without enlargement. On range(A), the ideal matrix A+2H Pi has eigenvalues at least mu, and the actual correction changes it by at most 3mu/8. The remaining margin is 5mu/8. Exact kernel annihilation eliminates cross terms between the range and kernel, proving full-space positive semidefiniteness. Finally, rank(U) < k would leave a nonzero vector in the negative eigenspace orthogonal to U, contradicting that conclusion.

The same reasoning covers scalar matrices, the zero matrix, positive semidefinite matrices with k = 0, negative definite matrices with k = n, repeated eigenvalues, and mixed inertia with a nontrivial kernel. None requires a separate limiting argument.

## Scope of the optimization consequence

With the convention f(x) = (1/2)x^T A x + b^T x + c, the decomposition has D = 2H I_k and T = U^T. The factor of two is consistent with that convention. Since T is a contraction, full-space quadratic growth with constant g implies projected quadratic growth with the same constant. This establishes d_max/g_projected <= 2H/g when g > 0.

It does not show that all global minimizers have the same projection. The current convex-slab theorem separately requires that property; uniqueness is sufficient. The revised consequence paragraph states this limitation correctly. The search bound, exact stopping rule, and bit complexity of that algorithm remain separate obligations. A supplied H may be much larger than the spectral norm, in which case the resulting conditioning parameter is correspondingly weaker, without affecting this lemma's correctness.

Rational near-diagonalization and rational Jacobi rotations are established ingredients. The note now attributes them to the relevant primary source. This review checked the self-contained proof and did not conduct a literature search or establish novelty for the exact correction or its optimization use.

## Targeted verification

The author reports that `python3 -B research-20261002/new-direction/check_spectral_normalization.py` passed 12 normalization cases and 29 rotations. I inspected the checker but did not duplicate that full run. Its principal-minor enumeration is a small-instance diagnostic, not part of the polynomial-time construction.

An independent delegated reviewer ran an inline exact `Fraction` check of 196 integer principal blocks. It checked orthogonality, the quartic identity, the endpoint bracket, and the bisection residual, including equal diagonal entries; all passed.

For distinct coverage of the H < 1 edge case, I ran `python3 -B -` with an inline script loading the checker's `normalize` function through `runpy.run_path`. The three exact inputs and results were:

| Input A | Bound H used by the checker | Negative inertia | Rotations | Largest output-entry bit length |
| --- | --- | --- | --- | --- |
| -[[1,2],[2,4]]/1024 | 3/512 | 1 | 1 | 35 |
| C diag(-1,1) C^T/4096, C = [[1,2],[3,1],[2,-1]] | 1/256 | 1 | 7 | 383 |
| [[1/1024]] | 1/1024 | 0 | 0 | 0 |

All passed the checker's exact orthogonality, kernel-annihilation, rank, norm, and PSD assertions. These finite checks supplement the proof and do not establish its asymptotic complexity. No project-wide checks or CI inspection were performed.

## Addendum: automatic norm bounds and negative curvature only

The later norm-selection paragraph and the section **Stronger normalization using only negative curvature** received a fresh review. Both pass. The new conclusion is stronger than the original lemma: if nu = max(0,-lambda_min(A)) > 0, one can compute rational beta and U from A alone in polynomial bit complexity such that

    nu <= beta < 2 nu,
    ||U||_2 <= 1,                 A + 2 beta U U^T >= 0,

with rank(U) equal to the negative inertia. An independent arithmetic reviewer rechecked the strengthened constants and edge cases.

The two bound-selection procedures have different costs and should remain distinct. The absolute row-sum bound H0 obeys ||A||_2 <= H0 <= sqrt(n)||A||_2. Testing both (H/2)I-A and (H/2)I+A for positive semidefiniteness is equivalent to testing ||A||_2 <= H/2. It therefore yields ||A||_2 <= H < 2||A||_2 in O(log n) successful halvings, with the zero matrix handled first.

For the one-sided bound, first return the empty correction if A is positive semidefinite. This branch is necessary: a halving loop would otherwise never terminate. In the remaining case, initialize beta = H. The test A+(beta/2)I >= 0 is equivalent to beta/2 >= nu. It preserves beta >= nu after every accepted halving, and failure proves beta < 2nu. Exact equality is correctly accepted: when beta/2 = nu, the next value is beta = nu and the following test fails. Since nu >= mu, the number of tests is O(1+log(H/nu)) <= O(1+log(H/mu)), polynomial in the input encoding length. Halving only adds that many bits to the rational denominator. Positive-semidefiniteness tests use polynomial-time exact rational elimination; enumerating principal minors is unnecessary.

The proof must keep the full bound H in the definition of mu and in the rotation derivative bound 4H. The new note does so. Only the target accuracy and correction coefficient change:

    e = mu^2/(16 n beta),         tau = e/n.

Because mu <= nu <= beta, this still gives e <= mu/(16n). The same diagonal selection and residual bounds apply. On the negative eigenspace, lambda+2beta >= 2beta-nu >= beta >= mu; positive eigenvalues remain at least mu. Replacing the ideal negative projector by UU^T changes the correction by at most

    2 beta (3n e/mu) = 3mu/8.

The corrected matrix therefore retains the same 5mu/8 margin on range(A), and the exact range projection still annihilates its kernel. A large positive eigenvalue does not invalidate this argument. It affects the full-matrix Jacobi precision through H/tau = 16n^2 H beta/mu^2, whose logarithm has polynomial encoding length. It does not enter the correction coefficient 2beta. For the automatically selected beta <= H, the new accuracy requirement is even weaker than the original one.

The one-sided halving count cannot be replaced by O(log n). For example, nu = 2^-10 with a positive eigenvalue 2^20 already creates a factor 2^30 between the negative and positive curvature scales. The note correctly charges the resulting halving count to input bit length. The research-scout agent reports eight exact one-sided halving and ideal-PSD-margin checks, including this scale separation and singular matrices; the scale-separated case used 30 halvings. Those checks cover bound selection and the ideal margin, not the entire construction with its modified accuracy. No duplicate construction test was run for this addendum; the correctness conclusion follows from the fresh proof audit.

For projected quadratic growth with constant g, the strengthened decomposition gives d_max/g_projected <= 2beta/g < 4nu/g. In the separately proved Fenchel envelope formula kappa_W = 2+alpha/g_projected, taking alpha = 2beta consequently gives kappa_W <= 2+4nu/g. This is a valid parameter improvement: positive curvature is charged through polynomial input processing rather than the nonconvex conditioning parameter. The projected-minimizer assumption and the rest of the downstream optimization proof remain separate requirements. When nu = 0 the matrix is positive semidefinite and the convex branch applies; a positive-alpha nonconvex argument is not needed.
