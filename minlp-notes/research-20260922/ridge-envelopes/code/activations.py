"""Univariate functions sigma used in the verification (vectorized numpy)."""
import math

import numpy as np

_erf = np.frompyfunc(math.erf, 1, 1)


def erf(s):
    return np.asarray(_erf(np.asarray(s, dtype=float)), dtype=float)


def sigmoid(s):
    s = np.asarray(s, dtype=float)
    return np.where(s >= 0, 1.0 / (1.0 + np.exp(-np.abs(s))), np.exp(-np.abs(s)) / (1.0 + np.exp(-np.abs(s))))


def softplus(s):
    s = np.asarray(s, dtype=float)
    return np.maximum(s, 0.0) + np.log1p(np.exp(-np.abs(s)))


SIGMAS = {
    "sigmoid": sigmoid,
    "tanh": np.tanh,
    "silu": lambda s: np.asarray(s, float) * sigmoid(s),
    "gelu": lambda s: 0.5 * np.asarray(s, float) * (1.0 + erf(np.asarray(s, float) / math.sqrt(2.0))),
    "sin": np.sin,
    "cos": np.cos,
    "cube": lambda s: np.asarray(s, float) ** 3,
    "cube_m3x": lambda s: np.asarray(s, float) ** 3 - 3.0 * np.asarray(s, float),
    "exp": np.exp,
    "neg_exp": lambda s: -np.exp(s),
    "log1p_sq": lambda s: np.log1p(np.asarray(s, float) ** 2),
    "softplus": softplus,
    # p''(s) = 10 s (2 s^2 - 3): three inflections at 0 and +-sqrt(1.5)
    "poly5": lambda s: np.asarray(s, float) ** 5 - 5.0 * np.asarray(s, float) ** 3 + 4.0 * np.asarray(s, float),
    "hazen_williams": lambda s: np.sign(s) * np.abs(np.asarray(s, float)) ** 1.852,
    "gauss": lambda s: np.exp(-np.asarray(s, float) ** 2),
}


def negated(sig):
    return lambda s: -sig(s)
