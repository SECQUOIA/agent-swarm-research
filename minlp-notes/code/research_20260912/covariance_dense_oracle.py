"""Covariance-space evaluation of the existing Liu selection relaxation.

Scalar Kalman innovations and their reverse derivative replace the
ill-conditioned latent-precision solve. These are numerical objective/gradient
values, not validated floating-point upper tangents. No new relaxation or
filtering algorithm is claimed.
"""

from __future__ import annotations

import math

import numpy as np

from noisy_markov_design import NoisyDesign
from structured_dense_oracle import StructuredLiuOracle


class CovarianceLiuOracle:
    """Evaluate the same fixed-split objective in O(n p² + p³) operations.

    Split setup reuses the tridiagonal maximum-eigenvalue calculation, but no
    precision-space value/gradient call is made. The split check is numerical;
    exact tangent certification remains a separate operation.
    """

    def __init__(self, design: NoisyDesign, split_fraction: float = 0.5,
                 *, a: float | None = None):
        setup = StructuredLiuOracle(design, split_fraction, a=a)
        self.design = design
        self.a = setup.a
        self.minimum_covariance_eigenvalue = setup.minimum_covariance_eigenvalue
        self.diagonal_variance = setup.diagonal_variance
        if not math.isfinite(self.minimum_covariance_eigenvalue):
            raise FloatingPointError("Covariance variance is outside finite floating-point range")
        # Factoring 1-rho² avoids subtracting two nearly equal squares.
        self.process_variance = (design.latent_variance
                                 * ((1-design.rho)*(1+design.rho)))

    def value_gradient(self, z: np.ndarray) -> tuple[float, np.ndarray]:
        z = np.asarray(z, dtype=float)
        design, a = self.design, self.a
        if (z.shape != (design.n,) or not np.isfinite(z).all()
                or np.any(z < 0) or np.any(z > 1)):
            raise ValueError("z must be a finite n-vector in [0,1]")
        if not np.any(z):
            J, V = design.prior, design.F
        elif self.diagonal_variance is not None:
            denominator = a*(1-z) + self.diagonal_variance*z
            weighted = np.sqrt(z/denominator)[:, None] * design.F
            J = design.prior + weighted.T @ weighted
            V = (a/denominator)[:, None] * design.F
        else:
            beta = a*(1-z) + design.nugget_variance*z
            innovations = np.empty_like(design.F)
            innovation_weights = np.empty(design.n)
            predicted_variances = np.empty(design.n)
            denominators = np.empty(design.n)
            P, mean = design.latent_variance, np.zeros(design.p)
            rho = design.rho
            for i in range(design.n):
                predicted_variances[i] = P
                residual = design.F[i]-mean
                denominator = P*z[i]+beta[i]
                if not math.isfinite(denominator) or denominator <= 0:
                    raise FloatingPointError("Innovation variance is outside positive finite range")
                weight = z[i]/denominator
                innovations[i] = residual
                innovation_weights[i] = weight
                denominators[i] = denominator
                # At z_i=0 the update is exactly skipped, without constructing
                # an infinite pseudo-observation variance beta_i/z_i.
                if i+1 < design.n:
                    mean = rho*(mean + (P*weight)*residual)
                    P = rho*rho*(P*(beta[i]/denominator)) + self.process_variance
                    if not math.isfinite(P) or P <= 0:
                        raise FloatingPointError("Predicted latent variance left positive finite range")
            weighted = np.sqrt(innovation_weights)[:, None]*innovations
            J = design.prior + weighted.T @ weighted
            # Reverse the innovation quadratic instead of subtracting the
            # smoothed mean from F and magnifying the residual by a/beta.
            # This formula also gives the correct residual at z_i=0.
            V, adjoint = np.empty_like(design.F), np.zeros(design.p)
            for i in range(design.n-1, -1, -1):
                V[i] = (a/denominators[i])*(
                    innovations[i]-rho*predicted_variances[i]*adjoint)
                adjoint = (innovation_weights[i]*innovations[i]
                           + rho*(beta[i]/denominators[i])*adjoint)
        # A small Cholesky factor provides the log determinant and nonnegative
        # quadratic gradient entries without explicitly inverting J.
        J = (J+J.T)/2
        factor = np.linalg.cholesky(J)
        transformed = np.linalg.solve(factor, V.T)
        gradient = np.sum(transformed*transformed, axis=0)/a
        value = float(2*np.log(np.diag(factor)).sum())
        if not math.isfinite(value) or not np.isfinite(gradient).all():
            raise FloatingPointError("Oracle result is outside finite floating-point range")
        return value, gradient
