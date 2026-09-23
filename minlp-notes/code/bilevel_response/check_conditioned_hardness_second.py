"""Independent exact network, scaling, and gap-constant checks."""
from fractions import Fraction as F
from itertools import product


def require(ok):
    if not ok:
        raise RuntimeError("conditioned hardness arithmetic check failed")


def build(n, clauses):
    N = 3*n+len(clauses)
    A = [[F(0) for _ in range(N)] for _ in range(N)]
    b0, b1 = [F(0)]*N, [F(0)]*N
    for i in range(n):
        for offset in (0, 1):
            row = 2*i+offset
            b0[row], b1[row] = F(-1-offset), F(3**(i+1))
            for j in range(i):
                A[row][2*j], A[row][2*j+1] = F(-2*3**(i-j)), F(2*3**(i-j))
        A[2*n+i][2*i], A[2*n+i][2*i+1] = F(2), F(-2)
        b0[2*n+i] = F(-1)
    for k, clause in enumerate(clauses):
        row = 3*n+k
        b0[row] = F(1)
        for j, positive in clause:
            sign = 1 if positive else -1
            A[row][2*j] -= sign
            A[row][2*j+1] += sign
            b0[row] -= not positive
    return A, b0, b1


def network(A, b0, b1, x):
    h, residual = [], []
    for i in range(len(A)):
        t = b0[i]+x*b1[i]+sum(A[i][j]*h[j] for j in range(i))
        h.append(max(F(0), t))
        residual.append(h[-1]-t)
    return h, residual


def run():
    families = [(1, []), (2, []), (3, []),
                (3, [[(0, True), (1, False), (2, True)]]),
                (3, [[(j, signs[j]) for j in range(3)]
                     for signs in product((False, True), repeat=3)])]
    samples = witnesses = 0
    maxbits = 0
    for n, clauses in families:
        A, b0, b1 = build(n, clauses)
        N, C = len(A), 2*3**n
        require(all(not A[i][j] for i in range(N) for j in range(i, N)))
        require(max(abs(v) for row in A for v in row) <= C)
        require(max(map(abs, b0+b1)) <= C)
        M = (1+N*C)**N
        theta = F(1, 100*N*C*M)
        scales = [F(1, 4*C)*theta**i for i in range(N)]
        B = [[scales[i]*A[i][j]/scales[j] for j in range(N)] for i in range(N)]
        U = [[abs(A[j][i])*scales[j]**2/scales[i]**2 for j in range(N)] for i in range(N)]
        rownorm = max(sum(map(abs, row)) for row in B)
        colnorm = max(sum(abs(B[i][j]) for i in range(N)) for j in range(N))
        require(max(rownorm, colnorm) <= 2*C*theta <= F(1, 50))
        require(max(sum(row) for row in U) <= 2*C*theta**2)
        require(2*M*C*(1+N*C)*theta**2 < F(1, 2))
        require(8*M*C*theta**2 == F(1, 1250*N*N*C*M) <= F(1, 16*N))
        # Direct normalized Q,c,d checks, separately from the norm proof.
        H = [[F(i == j)-B[i][j] for j in range(N)] for i in range(N)]
        Q = [[sum(H[k][i]*H[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
        require(max(abs(v) for row in Q for v in row) <= 2)
        for b in (b0, b1):
            coefficient = [-sum(H[k][i]*scales[k]*b[k] for k in range(N)) for i in range(N)]
            require(max(map(abs, coefficient)) < 1)
        upper = [2*scales[-1]/s for s in scales]
        require(max(upper) <= 2)
        maxbits = max(maxbits, max(max(v.numerator.bit_length(), v.denominator.bit_length())
                                  for row in Q for v in row))
        for k in range(98):
            h, residual = network(A, b0, b1, F(k, 97))
            require(all(0 <= v <= 2 for v in h+residual))
            y = [h[2*i]-h[2*i+1] for i in range(n)]
            require(all(0 <= v <= 1 for v in y))
            score = 2*sum(y)-2*sum(h[2*n:3*n])+2*sum(h[3*n:])
            literal_sums = [sum(y[j] if positive else 1-y[j] for j, positive in clause)
                            for clause in clauses]
            expected = 2*sum(min(v, 1-v) for v in y)+2*sum(max(F(0), 1-v) for v in literal_sums)
            require(score == expected >= 0)
            if len(clauses) == 8:
                require(score >= 2)
            samples += 1
        for bits in product((0, 1), repeat=n):
            x = sum(F(2*b, 3**(i+1)) for i, b in enumerate(bits))+F(1, 2*3**n)
            h, residual = network(A, b0, b1, x)
            require([h[2*i]-h[2*i+1] for i in range(n)] == list(bits))
            witnesses += 1
    print(f"PASS: {len(families)} exact matrix/scaling families, {samples} network-score "
          f"samples, {witnesses} Boolean leaders; maximum checked Q-entry size {maxbits} bits.")


if __name__ == "__main__":
    run()
