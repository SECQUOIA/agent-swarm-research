"""Catalog of Pyomo GDP test instances available on this machine.

``INSTANCES`` maps an instance name to a zero-argument builder that returns a
fresh Pyomo model.  ``convex_instances()`` returns the names classified as
convex GDPs (every nonlinear constraint convex in its required direction, and
a convex objective).  Sizes and convexity classifications are stored in
``CATALOG`` (filled from ``gdp_catalog_analyze.py``) and copied into the
docstring of every builder.

Sources
-------
gdplib   : instances/gdplib_src (editable install of GDPlib)
pyomo    : instances/pyomo_examples_src/examples/gdp (sparse checkout of the
           Pyomo 6.10.1 repository; the pip wheel does not ship examples)
pyomo_tests : models defined inside pyomo.contrib.gdpopt.tests

Solvers used by the catalog run: ipopt at
/home/sgusev/miniconda3/envs/solvers/bin (prepend to PATH), gurobipy, and GAMS
(BARON) at /home/sgusev/.local/opt/gams/gams54.3_linux_x64_64_sfx.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")  # circles/farm_layout import matplotlib

from pyomo.common.fileutils import import_file

HERE = Path(__file__).resolve().parent
EXAMPLES = HERE / "instances" / "pyomo_examples_src" / "examples" / "gdp"
CATALOG_JSON = HERE / "gdp_catalog.json"

INSTANCES: dict[str, callable] = {}


def _register(name, source, note=""):
    def deco(fn):
        fn.source = source
        fn.note = note
        INSTANCES[name] = fn
        return fn

    return deco


# --------------------------------------------------------------------------
# (a) GDPlib
# --------------------------------------------------------------------------
_GDPLIB_SIMPLE = [
    "batch_processing",
    "biofuel",
    "cstr",
    "disease_model",
    "ex1_linan_2023",
    "gdp_col",
    "hda",
    "jobshop",
    "kaibel",
    "med_term_purchasing",
    "methanol",
    "positioning",
    "small_batch",
    "spectralog",
    "syngas",
    "pandemic",
    "multiperiod_blending",
    "grid",
]


def _gdplib_builder(module, **kwargs):
    def build():
        import importlib

        return importlib.import_module("gdplib." + module).build_model(**kwargs)

    return build


for _name in _GDPLIB_SIMPLE:
    _register("gdplib." + _name, "gdplib")(_gdplib_builder(_name))

_register("gdplib.cstr.NT10", "gdplib", "NT=10 reactors")(_gdplib_builder("cstr", NT=10))
_register("gdplib.cstr.NT25", "gdplib", "NT=25 reactors")(_gdplib_builder("cstr", NT=25))

for _case in ["conventional", "single_module_integer", "multiple_module_integer",
              "mixed_integer", "single_module_discrete", "multiple_module_discrete",
              "mixed_discrete"]:
    _register("gdplib.mod_hens." + _case, "gdplib", "cafaro_approx=True, num_stages=4")(
        _gdplib_builder("mod_hens", case=_case)
    )
_register("gdplib.mod_hens.conventional_nocafaro", "gdplib",
          "cafaro_approx=False (LMTD via Chen approximation), num_stages=4")(
    _gdplib_builder("mod_hens", case="conventional", cafaro_approx=False)
)

for _case in ["Growth", "Dip", "Decay", "Distributed", "QuarterDistributed"]:
    _register("gdplib.modprodnet." + _case, "gdplib")(_gdplib_builder("modprodnet", case=_case))

for _case in [None, "Gas_100", "Gas_250", "Gas_500", "Gas_small", "Gas_large"]:
    _register("gdplib.stranded_gas." + (_case or "base"), "gdplib")(
        _gdplib_builder("stranded_gas", case=_case)
    )

for _approx in ["none", "quadratic_zero_origin", "quadratic_nonzero_origin", "piecewise"]:
    _register("gdplib.water_network." + _approx, "gdplib", f"approximation={_approx}")(
        _gdplib_builder("water_network", approximation=_approx)
    )

_register("gdplib.reverse_electrodialysis", "gdplib",
          "solve_stack=False (skips the GAMS/IPOPTH stack pre-solve; uses default GP bound)")(
    _gdplib_builder("reverse_electrodialysis", solve_stack=False)
)

for _k in [1, 6, 12]:
    def _blend(k=_k):
        from gdplib.multiperiod_blending import build_model, convert_json_to_data
        import gdplib.multiperiod_blending as mod

        path = Path(mod.__file__).parent / "instances_json" / f"mpbp_{k}.json"
        with open(path) as f:
            return build_model(convert_json_to_data(json.load(f)))

    _register(f"gdplib.multiperiod_blending.mpbp_{_k}", "gdplib", f"instances_json/mpbp_{_k}.json")(_blend)


# --------------------------------------------------------------------------
# (b) Pyomo examples/gdp
# --------------------------------------------------------------------------
def _ex(relpath):
    return import_file(str(EXAMPLES / relpath))


def _abstract(relpath, datfile, fn="build_model"):
    def build():
        mod = _ex(relpath)
        return getattr(mod, fn)().create_instance(str(EXAMPLES / datfile))

    return build


_register("pyomo.batch_processing", "pyomo", "AbstractModel + batchProcessing1.dat")(
    _abstract("batchProcessing.py", "batchProcessing1.dat")
)
_register("pyomo.jobshop.small", "pyomo", "AbstractModel + jobshop-small.dat")(
    _abstract("jobshop.py", "jobshop-small.dat")
)
_register("pyomo.jobshop.large", "pyomo", "AbstractModel + jobshop.dat")(
    _abstract("jobshop.py", "jobshop.dat")
)
_register("pyomo.jobshop_nodisjuncts.small", "pyomo",
          "Disjunction built from expression lists (no explicit Disjunct); jobshop-small.dat")(
    _abstract("jobshop-nodisjuncts.py", "jobshop-small.dat")
)
_register("pyomo.med_term_purchasing", "pyomo", "AbstractModel + medTermPurchasing_Literal_Chull.dat")(
    _abstract("medTermPurchasing_Literal.py", "medTermPurchasing_Literal_Chull.dat")
)


@_register("pyomo.stickies", "pyomo", "stickies1.dat loaded inside build_model")
def _stickies():
    return _ex("stickies.py").build_model()


@_register("pyomo.disease_model", "pyomo")
def _disease():
    return _ex("disease_model.py").build_model()


for _v in ["model", "logical", "verbose_model"]:
    def _eight(v=_v):
        return _ex(f"eight_process/eight_proc_{v}.py").build_eight_process_flowsheet()

    _register("pyomo.eight_process." + _v, "pyomo", f"eight_proc_{_v}.py")(_eight)


@_register("pyomo.nine_process", "pyomo", "small_process.build_model")
def _nine():
    return _ex("nine_process/small_process.py").build_model()


@_register("pyomo.nine_process.nonexclusive", "pyomo", "small_process.build_nonexclusive_model")
def _nine_nonex():
    return _ex("nine_process/small_process.py").build_nonexclusive_model()


for _c in ["Circles2D3", "Circles2D3_modified", "Circles3D4"]:
    def _circ(c=_c):
        mod = _ex("circles/circles.py")
        return mod.build_model(mod.circles_model_examples[c])

    _register("pyomo.circles." + _c, "pyomo")(_circ)

for _c in ["FLay02", "FLay03", "FLay04", "FLay05", "FLay06", "FLay03_alt_1", "FLay03_alt_2"]:
    def _farm(c=_c):
        mod = _ex("farm_layout/farm_layout.py")
        return mod.build_model(mod.farm_layout_model_examples[c])

    _register("pyomo.farm_layout." + _c, "pyomo")(_farm)

for _c in ["CLay0203", "CLay0204", "CLay0205", "CLay0303", "CLay0304", "CLay0305"]:
    for _metric in ["l1", "l2"]:
        def _clay(c=_c, metric=_metric):
            mod = _ex("constrained_layout/cons_layout_model.py")
            return mod.build_constrained_layout_model(
                mod.constrained_layout_model_examples[c], metric=metric
            )

        _register(f"pyomo.constrained_layout.{_c}.{_metric}", "pyomo", f"metric={_metric}")(_clay)

for _i in [1, 2, 3]:
    def _simple(i=_i):
        return _ex(f"simple{i}.py").build_model()

    _register(f"pyomo.simple{_i}", "pyomo", "toy")(_simple)


@_register("pyomo.small_lit.basic_step", "pyomo")
def _basic_step():
    return _ex("small_lit/basic_step.py").build_gdp_model()


@_register("pyomo.small_lit.contracts", "pyomo", "random data with fixed seed 1, T=10")
def _contracts():
    return _ex("small_lit/contracts_problem.py").build_model()


@_register("pyomo.small_lit.ex1_Lee", "pyomo")
def _ex1_lee():
    return _ex("small_lit/ex1_Lee.py").build_model()


@_register("pyomo.small_lit.ex_633_trespalacios", "pyomo")
def _ex633():
    return _ex("small_lit/ex_633_trespalacios.py").build_simple_nonconvex_gdp()


@_register("pyomo.small_lit.nonconvex_HEN", "pyomo")
def _hen():
    return _ex("small_lit/nonconvex_HEN.py").build_gdp_model()


for _d in ["4BigM", "12Chull"]:
    def _sp(d=_d):
        mod = _ex("strip_packing/stripPacking.py")
        return mod.model.create_instance(str(EXAMPLES / f"strip_packing/stripPacking_{d}.dat"))

    _register("pyomo.strip_packing." + _d, "pyomo", f"module-level AbstractModel + stripPacking_{_d}.dat")(_sp)


@_register("pyomo.strip_packing.8rect", "pyomo")
def _sp8():
    return _ex("strip_packing/strip_packing_8rect.py").build_rect_strip_packing_model()


@_register("pyomo.strip_packing.concrete", "pyomo")
def _spc():
    return _ex("strip_packing/strip_packing_concrete.py").build_rect_strip_packing_model()


for _mc in [False, True]:
    def _two_rxn(mc=_mc):
        return _ex("two_rxn_lee/two_rxn_model.py").build_model(use_mccormick=mc)

    _register("pyomo.two_rxn_lee" + (".mccormick" if _mc else ""), "pyomo",
              f"use_mccormick={_mc}")(_two_rxn)


# --------------------------------------------------------------------------
# (c) Pyomo test suite
# --------------------------------------------------------------------------
for _mt in [False, True]:
    def _four_stage(mt=_mt):
        from pyomo.contrib.gdpopt.tests.four_stage_dynamic_model import build_model

        return build_model(mode_transfer=mt)

    _register("pyomo_tests.four_stage_dynamic" + (".mode_transfer" if _mt else ""),
              "pyomo_tests", f"four_stage_dynamic_model.build_model(mode_transfer={_mt})")(_four_stage)


# --------------------------------------------------------------------------
# Catalog metadata (sizes + convexity), produced by gdp_catalog_analyze.py
# --------------------------------------------------------------------------
def _load_catalog():
    if CATALOG_JSON.exists():
        with open(CATALOG_JSON) as f:
            return json.load(f)
    return {}


CATALOG: dict[str, dict] = _load_catalog()


def _docstring(name, fn):
    meta = CATALOG.get(name)
    head = f"{name} [{fn.source}]" + (f" -- {fn.note}" if fn.note else "")
    if meta is None or meta.get("build_error"):
        return head + "\n(no catalog entry" + (
            f": build failed: {meta['build_error']}" if meta else "") + ")"
    return (
        f"{head}\n"
        f"vars={meta['n_vars']} (bin={meta['n_binary']}, int={meta['n_integer']}, "
        f"bool={meta['n_boolean']}), cons={meta['n_cons']} "
        f"(global={meta['n_cons_global']}, in-disjunct={meta['n_cons_disjunct']}), "
        f"disjunctions={meta['n_disjunctions']}, disjuncts={meta['n_disjuncts']}, "
        f"nonlinear cons={meta['n_nl']} (global={meta['n_nl_global']}, "
        f"in-disjunct={meta['n_nl_disjunct']}), nonconvex cons={meta['n_nonconvex']}, "
        f"objective={meta['obj_class']}\n"
        f"classification: {meta['classification']}"
    )


for _name, _fn in INSTANCES.items():
    _fn.__doc__ = _docstring(_name, _fn)


def convex_instances() -> list[str]:
    """Names of instances classified as convex GDPs by the catalog analysis."""
    return [n for n in INSTANCES if CATALOG.get(n, {}).get("classification") == "convex"]


def build(name):
    """Build a fresh model for the named instance."""
    return INSTANCES[name]()


if __name__ == "__main__":
    for n, fn in INSTANCES.items():
        print(n, "->", fn.source, fn.note)
    print(len(INSTANCES), "instances;", len(convex_instances()), "convex")
