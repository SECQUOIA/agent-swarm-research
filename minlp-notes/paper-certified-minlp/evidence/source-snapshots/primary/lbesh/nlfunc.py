"""Fast evaluation and gradients of Pyomo nonlinear expressions.

Each NLFunction wraps one Pyomo expression g(x) over an ordered variable list.
Evaluation and gradients use sympy lambdification when possible and fall back
to Pyomo's numeric reverse-mode differentiation otherwise.
"""
from __future__ import annotations

import math
import numpy as np
import pyomo.environ as pe
from pyomo.core.expr.calculus.derivatives import differentiate, Modes
from pyomo.core.expr.visitor import identify_variables


class NLFunction:
    def __init__(self, expr, variables=None, name="g"):
        self.expr = expr
        self.name = name
        if variables is None:
            variables = list(identify_variables(expr, include_fixed=False))
        self.vars = list(variables)
        self.index = {id(v): i for i, v in enumerate(self.vars)}
        self._f = None
        self._grad = None
        self._compile()

    # ------------------------------------------------------------------
    def _compile(self):
        try:
            import sympy
            from pyomo.core.expr.sympy_tools import sympyify_expression
            objmap, sexpr = sympyify_expression(self.expr)
            symbols = []
            for v in self.vars:
                s = objmap.getSympySymbol(v)
                symbols.append(s)
            # variables not appearing get a dummy symbol
            grads = [sympy.diff(sexpr, s) for s in symbols]
            mods = ["numpy", {"log": np.log, "exp": np.exp, "sqrt": np.sqrt}]
            f = sympy.lambdify(symbols, sexpr, modules=mods)
            g = sympy.lambdify(symbols, grads, modules=mods)
            # smoke test
            x0 = np.array([self._val(v) for v in self.vars], dtype=float)
            fv = float(f(*x0))
            gv = np.array(g(*x0), dtype=float)
            if not np.isfinite(fv) or gv.shape != (len(self.vars),):
                raise ValueError("bad compile")
            pv = self._pyomo_eval(x0)
            if abs(pv - fv) > 1e-6 * (1 + abs(pv)):
                raise ValueError("mismatch")
            self._f, self._grad = f, g
        except Exception:
            self._f, self._grad = None, None

    @staticmethod
    def _val(v):
        val = v.value
        if val is None:
            lb, ub = v.lb, v.ub
            if lb is not None and ub is not None:
                return 0.5 * (lb + ub)
            if lb is not None:
                return float(lb)
            if ub is not None:
                return float(ub)
            return 0.0
        return float(val)

    def _set(self, x):
        for v, xv in zip(self.vars, x):
            v.set_value(float(xv), skip_validation=True)

    def _pyomo_eval(self, x):
        self._set(x)
        return float(pe.value(self.expr))

    def _pyomo_grad(self, x):
        self._set(x)
        return np.array(
            differentiate(self.expr, wrt_list=self.vars, mode=Modes.reverse_numeric),
            dtype=float,
        )

    # ------------------------------------------------------------------
    def value(self, x):
        x = np.asarray(x, dtype=float)
        if self._f is not None:
            try:
                return float(self._f(*x))
            except Exception:
                pass
        return self._pyomo_eval(x)

    def grad(self, x):
        x = np.asarray(x, dtype=float)
        if self._grad is not None:
            try:
                return np.array(self._grad(*x), dtype=float)
            except Exception:
                pass
        return self._pyomo_grad(x)

    def value_grad(self, x):
        return self.value(x), self.grad(x)
