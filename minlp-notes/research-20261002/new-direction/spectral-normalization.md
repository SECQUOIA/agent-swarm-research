# Rational normalization of the negative spectral part

Date: 2026-10-02. Status: a constructive lemma with a self-contained bit-complexity proof. The optimization consequence is conditional on the separate convex-slab theorem. No novelty claim is made.

## Statement

Let A be a symmetric rational n by n matrix, let H >= 0 be rational with H >= ||A||_2, and let k be the negative inertia of A, counting multiplicities. There is a deterministic algorithm, polynomial in the binary encoding length of (A,H), producing a rational n by k matrix U such that

    ||U||_2 <= 1,                 A + 2H U U^T >= 0.

The output encoding length is polynomial too. The construction handles a singular A without assuming a lower bound on its nonzero eigenvalues as an additional parameter. It uses Gaussian elimination, rational arithmetic, and scalar bisection. It does not require an irrational spectral decomposition as input or enumerate candidate subspaces.

Consequently, the rational decomposition

    A = P - T^T D T,
    P = A + 2H U U^T >= 0,       T = U^T,       D = 2H I_k

has exactly k rows in T and ||T||_2 <= 1. The case k = 0 uses the empty matrix U and P = A.

## Choosing the norm bound from A

A supplied H is optional. If A = 0, take H = 0. Otherwise start with the rational absolute row-sum bound

    H0 = max_i sum_j |A_ij|,

and set H = H0. While both (H/2)I - A and (H/2)I + A are positive semidefinite, replace H by H/2. Exact rational positive-semidefiniteness testing is polynomial-time by symmetric elimination. The two tests are equivalent to ||A||_2 <= H/2. Consequently the final bound satisfies

    ||A||_2 <= H < 2 ||A||_2.

For a symmetric matrix, H0 <= sqrt(n) ||A||_2, so only O(log n) successful halvings and one failed pair of tests are needed. The rational encoding lengths stay polynomial. Thus a complexity bound parameterized by H/g can be stated instead in terms of ||A||_2/g, up to an absolute constant; H is not essential additional input. This observation does not weaken the separate projected-minimizer hypothesis below.

## A rational lower bound for the nonzero spectral gap

Compute d = rank(A) exactly. If d = 0, return the empty matrix; this also covers H = 0. Otherwise H > 0. Let D0 be a positive common denominator of the entries of A; the product of their denominators suffices. Put

    mu = 1 / (D0^d H^(d-1)).

The coefficient of t^(n-d) in det(tI-A), up to sign, is the product of the d nonzero eigenvalues. Since D0 A is integral, its corresponding nonzero coefficient is a nonzero integer. Thus that product has absolute value at least D0^(-d). The other d-1 eigenvalues have absolute value at most H, so every nonzero eigenvalue has absolute value at least mu. In particular 0 < mu <= H. Computing mu requires polynomial time and its numerator and denominator have polynomial encoding length. A very small mu affects precision and running time only through log(H/mu).

Also compute the exact orthogonal projector R onto range(A). For example, take linearly independent columns C of A and set

    R = C (C^T C)^(-1) C^T.

This is a rational matrix of polynomial encoding length, computable by exact Gaussian elimination. It obeys R = R^T = R^2, ||R||_2 <= 1, and ker(R) = ker(A).

## Relation to the rational Jacobi literature

Rational near-diagonalization is established prior work. Del Pia's *Rational Jacobi Rotations and the Complexity of Approximating Mixed Integer Quadratic Programming* ([primary preprint](https://arxiv.org/abs/2607.29386), [local source record](../../literature/papers/pia2026-rational-jacobi-rotations-and-the/paper.md)) proves polynomial-time rational orthogonal near-diagonalization in Theorem 2. Theorem 3 also preserves inertia after rounding the near-zero diagonal entries; Corollary 1 states the resulting eigenvector residual bound. Those results can supply the approximate negative subspace used below. When invoking Theorem 2 directly, its tolerance restriction to (0,1] is met by requesting min(e,1).

The following bisection and denominator argument is included to make this normalization note self-contained. It uses the same established rational Jacobi method and claims no novelty for it. The additional step needed for the lemma stated here is exact projection onto range(A), followed by a perturbation bound proving the exact positive-semidefinite correction with ||U||_2 <= 1 and coefficient 2H. The lemma retains the residual in the exact convex term P; it does not discard a small objective perturbation. The broader optimization comparison with Del Pia's approximation theorem belongs to the separate literature audit.

## Rational Jacobi rotations

Set

    e = mu^2 / (16 n H),         tau = e/n.

We construct an exactly orthogonal rational Q for which

    Q^T A Q = diag(a_1,...,a_n) + E,       ||E||_2 <= e,

where E has zero diagonal. Start with Q = I. While an off-diagonal entry of B = Q^T A Q has absolute value greater than tau, choose one of maximum absolute value, say b = B_pq, and apply a rational orthogonal rotation in coordinates p,q that makes its new absolute value at most tau/2.

Here is an explicit bisection implementation of that rotation. Write the principal block as [[a,b],[b,c]]. For a scalar t define

    c_t = (1-t^2)/(1+t^2),       s_t = 2t/(1+t^2),
    G(t) = [[c_t,-s_t],[s_t,c_t]].

The new off-diagonal entry of G(t)^T [[a,b],[b,c]] G(t) is

    f(t)/(1+t^2)^2,
    f(t) = b(1-6t^2+t^4) + 2(c-a)t(1-t^2).

At t = 0 it has the sign of b. If c != a, take t_end = -sign(b(c-a))/2; if c = a, take t_end = 1/2. Then

    f(t_end) = -7b/16 + (3/2)(c-a)t_end

has the opposite sign. Bisection, with exact rational sign comparisons, finds a dyadic t within tau/(8H) of a root in the interval between 0 and t_end. If a midpoint is itself a root, stop there. The derivative in operator norm of G(t)^T B_pq G(t) is at most 4H: the rotation angle is 2 arctan(t), its derivative is at most 2, and ||B_pq||_2 <= H. Hence the selected new off-diagonal entry has absolute value at most tau/2. The dyadic parameter requires O(1 + log(H/tau)) bits. Every resulting G(t) is exactly orthogonal over the rationals.

To bound the number of steps, let F(B) be the squared Frobenius norm of the off-diagonal part. A rotation changes F only by twice the change in the square of its selected off-diagonal entry. If M is the selected maximum, then M > tau, its replacement has magnitude at most tau/2 < M/2, and

    F(B_next) <= F(B) - (3/2) M^2
              <= (1 - 3/[2n(n-1)]) F(B)          (n >= 2).

Initially F(B) <= nH^2. Once F(B) <= tau^2, the loop has certainly stopped. Therefore the number of rotations is

    O(n^2 [1 + log(nH/tau)]).

On termination every off-diagonal entry has absolute value at most tau, and ||E||_2 <= ||E||_F <= n tau = e. For n = 1 no rotation is needed.

For completeness, exact arithmetic does not destroy this polynomial bound. Each rotation has a common rational denominator with O(1 + log(H/tau)) bits. A product of N such rotations has a common denominator whose bit length is at most the sum of those lengths. Its entries have magnitude at most one by exact orthogonality. Thus Q has polynomial encoding length. The same applies to Q^T A Q, or to its sequential updates. There are polynomially many rational operations and bisection comparisons on polynomial-length integers. This is a polynomial-bit algorithm even when mu is exponentially small in the input length.

## Selecting and projecting the negative columns

Let V have orthonormal columns spanning the negative eigenspace of A, and write Pi = V V^T. These are proof devices, not quantities the algorithm must compute. Since e <= mu/16, the eigenvalue perturbation bound for symmetric matrices implies that exactly k diagonal entries a_j are below -mu/2. Moreover, each selected a_j is at most -mu + e. All remaining a_j are at least -e. This follows by comparing the sorted eigenvalues of diag(a_j) with those of A; their differences are at most ||E||_2.

Let Bminus consist of the corresponding k columns of Q. Thus Bminus is rational and Bminus^T Bminus = I. For any selected column q_j,

    ||A q_j - a_j q_j||_2 <= e.

On the orthogonal complement of the negative eigenspace, A is positive semidefinite and a_j <= -mu/2. Resolving this residual in an orthonormal eigenbasis therefore gives

    ||(I-Pi)q_j||_2 <= 2e/mu.

Summing over the selected columns and using equal-rank orthogonal projectors yields

    ||Bminus Bminus^T - Pi||_2
      <= ||Bminus Bminus^T - Pi||_F
       = sqrt(2) ||(I-Pi)Bminus||_F
      <= 2 sqrt(2k) e/mu
      <= 3n e/mu.

Now output U = R Bminus. It is rational, has k columns, and ||U||_2 <= 1. Because R Pi R = Pi,

    ||U U^T - Pi||_2 <= 3n e/mu.

On range(A), the matrix A + 2H Pi has all eigenvalues at least mu. Indeed, a negative eigenvalue lambda becomes lambda+2H >= H >= mu, and every positive eigenvalue is at least mu. The perturbation introduced by replacing Pi with U U^T is at most

    2H (3n e/mu) = 3mu/8.

It follows that A + 2H U U^T is positive definite on range(A), with eigenvalues there at least 5mu/8. On ker(A), both A and U U^T vanish exactly. Hence it is positive semidefinite on the full space. In particular U has rank k: otherwise a nonzero negative direction orthogonal to its columns would contradict positive semidefiniteness.

Exact projection by R matters. An arbitrarily small rotation of a negative direction toward the kernel can make A + 2H Bminus Bminus^T indefinite. For A = diag(-1,0) and Bminus = (cos(theta),sin(theta))^T, the determinant is -2 sin(theta)^2. The range projection removes this failure exactly.

## Stronger normalization using only negative curvature

Define the one-sided negative curvature

    nu = max(0, -lambda_min(A)).

If k = 0, A is already positive semidefinite and the empty correction suffices. Suppose k > 0, so nu > 0. For any supplied positive rational beta >= nu, the same construction produces a rational n by k matrix U satisfying

    ||U||_2 <= 1,                 A + 2 beta U U^T >= 0.

The algorithm runs in time polynomial in the encoding length of (A,H,beta), where H >= ||A||_2 is a positive rational bound used only for preprocessing. In particular, a large positive eigenvalue does not force a large correction coefficient.

To prove this, retain the exact range projector R and the nonzero eigenvalue lower bound

    mu = 1 / (D0^d H^(d-1)).

Since a negative eigenvalue exists, mu <= nu <= beta. Change only the target accuracy to

    e = mu^2 / (16 n beta),       tau = e/n.

The Jacobi matrices, rotation derivatives, and scalar bisection tolerances continue to use the full bound H. Thus the root approximation tolerance remains tau/(8H), not tau/(8 beta). Since e <= mu/(16n), the same diagonal threshold and residual argument select exactly k columns, and the projected output still satisfies

    ||U U^T - Pi||_2 <= 3n e/mu,       ||U||_2 <= 1.

On range(A), the ideal correction A + 2 beta Pi has every eigenvalue at least mu. Each negative eigenvalue lambda becomes lambda + 2 beta >= beta >= mu, while each positive eigenvalue remains at least mu. The perturbation caused by replacing Pi with U U^T is at most

    2 beta (3n e/mu) = 3mu/8.

The matrix A + 2 beta U U^T consequently has eigenvalues at least 5mu/8 on range(A), and vanishes exactly on ker(A). This proves positive semidefiniteness. The same negative-direction argument proves that U has rank k. All precisions have polynomial encoding length; the number of Jacobi rotations depends on logarithms of H, beta, and mu through H/tau = 16n^2 H beta/mu^2. Since both H and beta are at least mu, that ratio is at least 16n^2.

The scalar beta also need not be supplied. First test A >= 0 exactly and return the empty correction if that test passes. Otherwise initialize beta = H and repeatedly halve beta while A + (beta/2)I is positive semidefinite. Each successful test is equivalent to beta/2 >= nu, so the final value satisfies

    nu <= beta < 2 nu.

There are O(1 + log(H/nu)) tests, bounded by O(1 + log(H/mu)); this is polynomial in the input length. This count can be much larger than the O(log n) count for the two-sided norm-bound procedure above. Every rational number used has polynomial encoding length. Therefore beta, U, and the exact decomposition

    A = P - T^T D T,
    P = A + 2 beta U U^T >= 0,    T = U^T,    D = 2 beta I_k

are computable in deterministic polynomial bit complexity from A alone. The original H-based lemma is the direct choice beta = H. No additional assumption on positive eigenvalues is needed.

## Consequence for projected quadratic growth

Use the Hessian convention of the separate convex-modulator theorem: f(x) = (1/2)x^T A x + b^T x + c. The decomposition A = P - T^T D T then gives the negative objective term -(1/2)(Tx)^T D(Tx), with D = 2H I_k in the original normalization or D = 2 beta I_k in the stronger version.

Let Xstar be the set of global minimizers over the feasible set. If full-space quadratic growth holds in the form

    f(x)-fstar >= g dist(x,Xstar)^2,

then, because ||T||_2 <= 1,

    dist(Tx,T Xstar) <= dist(x,Xstar),
    f(x)-fstar >= g dist(Tx,T Xstar)^2.

Thus the projected growth constant may be taken to be g. The original normalization gives d_max/g_projected <= 2H/g. The stronger normalization gives d_max/g_projected <= 2 beta/g < 4 nu/g when k > 0; when k = 0 the problem is already convex. Subject to the separate convex-slab algorithm's stated hypotheses, its parameter dependence becomes intrinsic in the negative inertia k and max(1,nu/g), with polynomial preprocessing and polynomial output encoding length. The H/g statement is a weaker corollary. The current convex-slab theorem requires all global minimizers to have the same T projection; a unique global minimizer is sufficient. Full-space growth relative to an arbitrary minimizer set does not by itself imply this condition. This normalization alone does not prove that algorithm's search bound or exact stopping rule.

## Targeted validation

The accompanying checker tests the rational rotation formula, exact orthogonality, inertia selection, exact annihilation of the kernel, the operator-norm bound via I-U^T U >= 0, and positive semidefiniteness of A+2HUU^T on small matrices. Its exact positive-semidefiniteness check uses principal minors solely as a small-instance diagnostic; the construction does not enumerate minors or candidate subspaces. Test cases include mixed inertia, singular matrices, repeated negative eigenvalues, a small nonzero eigenvalue, positive semidefinite matrices, and the zero matrix.

The targeted command was:

    python3 -B research-20261002/new-direction/check_spectral_normalization.py

It passed all 12 normalization cases and 29 rational rotations, plus the exact kernel-leakage counterexample. The oblique singular mixed-inertia case needed seven rotations; its ill-conditioned variant needed eight and produced entries of at most 1,218 bits. Every matrix identity and positive-semidefiniteness check in this run used exact rational arithmetic. Earlier nine-case and eleven-case runs also passed. The added oblique cases test several successive rotations and combined singularity with a small positive eigenvalue; the final additional case tests two negative directions in a mixed-inertia matrix.

The [fresh adversarial review](../reviews/spectral-normalization-adversary.md), including two independent subreviews, found no material gap in the normalization proof. Additional exact checks in that review cover 196 rotation blocks and three matrices with H < 1. The parent agent independently checked the final norm-bound selection paragraph, including the two PSD tests, factor-two guarantee, O(log n) halving count, and polynomial encoding lengths. These finite checks supplement the proof; they do not establish its asymptotic complexity. No project-wide verification or CI inspection was run.

The review addendum independently approves the stronger one-sided construction, including the PSD early return, both automatic-bound procedures, equality cases, the revised accuracy, and polynomial bit complexity. It records eight exact halving and ideal-margin checks supplied by the scout, including a small negative eigenvalue alongside a large positive eigenvalue. The 12-case construction checker reported above tests the original choice beta = H; those tests and the eight scalar/margin checks do not constitute a full construction run with the sharper accuracy. The stronger guarantee rests on the reviewed proof.
