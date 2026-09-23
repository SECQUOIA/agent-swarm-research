"""Small-instance checks of cyclic, tilt, cone-tree, and completion identities.

These deterministic numerical diagnostics supplement the analytic proofs.
They do not establish query lower bounds or asymptotic statements.
"""

import numpy as np


def close(actual, expected, message):
    if not np.allclose(actual, expected, rtol=2e-10, atol=2e-10):
        raise AssertionError(message)


def cyclic_checks():
    rng = np.random.default_rng(101)
    hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    block_gates = [np.kron(hadamard, np.eye(2)), np.kron(np.eye(2), hadamard)]
    public_norms = []
    for _ in range(4):
        signs = [np.diag(rng.choice([-1, 1], size=4)) for _ in range(2)]
        forward = block_gates + [signs[0]] + block_gates + [signs[1]] + block_gates
        duration = len(forward)
        period = 3 * duration
        gates = forward + [np.eye(4)] * duration + [g.T for g in forward[::-1]]
        transition = np.zeros((period * 4, period * 4))
        states = [np.array([1.0, 0, 0, 0])]
        for t, gate in enumerate(gates):
            next_t = (t + 1) % period
            transition[4 * next_t : 4 * (next_t + 1), 4 * t : 4 * (t + 1)] = gate
            states.append(gate @ states[-1])
        close(np.linalg.matrix_power(transition, period), np.eye(period * 4), "cycle")
        phi = states[duration][0]
        for condition in (3.0, 7.0, 20.0):
            gamma = (condition - 1) / (condition + 1)
            matrix = (np.eye(period * 4) - gamma * transition) / (1 + gamma)
            singulars = np.linalg.svd(matrix, compute_uv=False)
            close([singulars[0], singulars[-1]], [1, 1 / condition], "spectrum")
            e = np.eye(period * 4)[0]
            solution = np.linalg.solve(matrix, e)
            history = np.concatenate([gamma**t * states[t] for t in range(period)])
            history *= (1 + gamma) / (1 - gamma**period)
            close(solution, history, "inverse history")
            norm = np.sqrt(condition * (1 + gamma**period) / (1 - gamma**period))
            close(np.linalg.norm(solution), norm, "public solution norm")
            sums = sum(gamma ** (2 * t) for t in range(duration, 2 * duration))
            z = gamma ** (2 * duration)
            plateau = z / (1 + z + z * z)
            a = np.zeros_like(e)
            for t in range(duration, 2 * duration):
                a[4 * t] = gamma**t / (norm * np.sqrt(sums))
            close(a @ solution, np.sqrt(plateau) * phi, "scalar readout")
            g = np.linalg.solve(matrix.T, a)
            shift = np.roll(np.eye(period), 1, axis=0)
            small = (np.eye(period) - gamma * shift) / (1 + gamma)
            bar_a = a.reshape(period, 4)[:, 0]
            small_g = np.linalg.solve(small.T, bar_a)
            close(np.linalg.norm(g), np.linalg.norm(small_g), "public tilt norm")
            close(small_g[:duration], np.sqrt(plateau) * gamma ** -np.arange(duration), "recurrence")
            objective = e + g / (2 * np.linalg.norm(g))
            expected_value_sq = 1.25 + np.sqrt(plateau) / np.linalg.norm(g) * phi
            close(objective @ objective, expected_value_sq, "normalized tilt")
            hessian = 2 * matrix.T @ matrix
            rhs = matrix.T @ e + a / (2 * np.linalg.norm(g))
            close(rhs @ np.linalg.solve(hessian, rhs), expected_value_sq / 2, "decrement")
            close(np.sum(matrix**2, axis=1), (1 + gamma**2) / (1 + gamma) ** 2, "matrix metadata")
            close(np.sum(hessian**2, axis=1), 4 * ((1 + gamma**2)**2 + 2 * gamma**2) / (1 + gamma)**4, "hessian metadata")
            public_norms.append(np.linalg.norm(g))
    close(np.array(public_norms).reshape(4, 3), np.array(public_norms[:3])[None, :], "input-independent norms")


def tree_checks():
    for leaves in (2, 4, 8, 16):
        # Heap indices: root 0, remaining internal nodes, then leaves.
        count = 2 * leaves - 1
        point = np.zeros(count)
        for node in range(leaves - 1):
            depth = (node + 1).bit_length() - 1
            point[node] = np.sqrt((leaves - 2**depth) / (2**depth * (leaves - 1)))
        gradient = np.zeros(count)
        hessian = np.zeros((count, count))
        metric = np.diag([1, -1, -1])
        for node in range(leaves - 1):
            indices = [node, 2 * node + 1, 2 * node + 2]
            value = point[indices]
            transformed = metric @ value
            slack = value @ transformed
            gradient[indices] += -2 * transformed / slack
            hessian[np.ix_(indices, indices)] += 4 * np.outer(transformed, transformed) / slack**2 - 2 * metric / slack
        close(gradient[1:], 0, "tree center stationarity")
        close(hessian[leaves - 1 :, leaves - 1 :], 2 * (leaves - 1) * np.eye(leaves), "leaf hessian")
        close(hessian[1 : leaves - 1, leaves - 1 :], 0, "cross block")
        assert np.linalg.eigvalsh(hessian[1:, 1:]).min() > 0


def completion_checks():
    for condition in (4, 10, 100):
        for alpha in (1, 3):
            for error in (1 / 16, 1 / 1000):
                scalars = [2 * (1 + 4 * error * z) / (alpha * condition) for z in (0, 1)]
                completions = [np.array([[x, np.sqrt(1 - x * x)], [np.sqrt(1 - x * x), -x]]) for x in scalars]
                distance = np.linalg.norm(completions[0] - completions[1], 2)
                assert distance <= 12 * error / (alpha * condition)
                assert (1 - error) * (1 + 4 * error) > 1 + error


if __name__ == "__main__":
    cyclic_checks()
    tree_checks()
    completion_checks()
    print("Cyclic history, public metadata, tilt, decrement, tree, and completion checks passed.")
