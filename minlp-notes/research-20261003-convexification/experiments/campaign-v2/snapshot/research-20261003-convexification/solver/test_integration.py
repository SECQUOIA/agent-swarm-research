"""Observable native-preservation, row sign, and actual exported-cut contracts."""
from copy import deepcopy
from fractions import Fraction
import hashlib
import json

import pytest
import sympy as sp

from solver.integration import (Config, Instance, discover, propose_direction,
                                run_instance, signed_sides, split_affine)
from solver.model import build_model
from solver.row_certificate import AffineSide, certify_row_combination, replay_row_certificate
from solver.support import certify_support, replay_support


def row(*, lin=None, quad=(), nl=None, lb=-float('inf'), ub=float('inf')):
    return {'lin':lin or {},'quad':list(quad),'nl':nl,'lb':lb,'ub':ub}


def instance(name,bounds,rows,sense='min',constant=0.):
    return Instance(name,[b[0] for b in bounds],[b[1] for b in bounds],['C']*len(bounds),sense,constant,rows)


def test_signed_lower_upper_objective_constants_and_unrestricted_equality():
    inst = instance('signs',[(-1.,1.),(-3.,3.)],
                    [row(quad=[(0,0,2.)],lin={1:3.}),
                     row(quad=[(0,0,1.)],lin={1:-2.},lb=.25,ub=.25)],sense='max',constant=5.)
    built=build_model(inst)
    try:
        sides=signed_sides(inst,built)
        assert [(s.sign,s.side) for s in sides]==[(-1,'objective'),(1,'upper'),(-1,'lower')]
        assert sides[0].nonlinear == -2*built.source_symbols[0]**2
        assert dict(sides[0].affine)=={'x1':Fraction(-3),'objective_epigraph':Fraction(1)}
        assert sides[0].rhs==5
        assert sides[1].rhs==Fraction(1,4) and sides[2].rhs==Fraction(-1,4)
        assert sides[1].nonlinear == -sides[2].nonlinear
    finally: built.model.freeProb()


def test_generic_split_preserves_exact_source_value():
    x,y=sp.symbols('x0 x1',real=True)
    source=sp.Rational(.1)*x+sp.log(x+2)+3*y+sp.Rational(.2)+(x+1)**2
    h,d,c=split_affine(source,(x,y))
    assert sp.expand(h+sum(sp.Symbol(v,real=True)*sp.Rational(q) for v,q in d)+sp.Rational(c)-source)==0
    assert dict(d)=={'x0':Fraction(.1),'x1':Fraction(3)}
    assert c==Fraction(.2)


def test_row_lp_has_nonnegative_multipliers_and_eliminates_to_original_vars():
    inst=instance('row_projection',[(0.,1.),(-2.,2.)],
                  [row(lin={1:1.}),row(quad=[(0,0,1.)],lin={1:-1.},ub=0.)])
    built=build_model(inst)
    try:
        block=discover(inst,built).blocks[0]
        direction=propose_direction(block,(.5,0.))
        assert direction is not None and all(c>=0 for c in direction[1:])
        support=certify_support(block.features,block.symbols,block.box,direction,rows=block.rows)
        assert support.cut is not None
        exported=certify_row_combination(variables=('x0','x1'),bounds=dict(zip(('x0','x1'),built.bounds)),
                 linear_terms={'x0':direction[0]},multipliers=direction[1:],support_rhs=support.cut.rhs,
                 sides=[AffineSide(s.source_id,s.affine,s.rhs) for s in block.sides])
        assert exported.rhs-sum(c*v for c,v in zip(exported.coefficients,(.5,0.)))>.1
        for x in (Fraction(0),Fraction(1,4),Fraction(1,2),Fraction(1)):
            z=x*x
            assert sum(Fraction(c)*v for c,v in zip(exported.coefficients,(x,z)))>=Fraction(exported.rhs)
    finally: built.model.freeProb()


def test_presolve_solved_native_model_never_runs_discovery(monkeypatch):
    import solver.integration as integration
    def unexpected(*args,**kwargs): raise AssertionError('presolve solve must not discover blocks')
    monkeypatch.setattr(integration,'discover',unexpected)
    inst=instance('easy',[(0.,1.)],[row(lin={0:1.})])
    original=deepcopy(inst)
    baseline=run_instance(inst,'baseline',time_limit=2.)
    strengthened=run_instance(inst,'auto',time_limit=2.)
    assert baseline['primal']==strengthened['primal']==0.
    assert strengthened['separation']['calls']==0
    assert strengthened['discovery_seconds']==0
    assert strengthened['model_metadata']==baseline['model_metadata']
    assert inst==original


def test_actual_scip_rows_replay_with_no_graph_auxiliaries():
    inst=instance('vector',[(0.,1.),(0.,1.)],
                  [row(quad=[(0,0,1.),(1,1,1.),(0,1,-4.)]),row(lin={0:1.,1:1.},ub=1.)])
    result=run_instance(inst,'all',time_limit=3.,config=Config(max_separation_seconds=2.,separation_budget_fraction=.7))
    assert abs(result['primal']+.5)<1e-6
    assert result['cuts']
    built=build_model(inst)
    try:
        assert built.model.getNVars()==3
        detected=discover(inst,built)
        names=tuple(str(s) for s in built.source_symbols)+(built.objective_var.name,)
        bounds=dict(zip(names,(*built.bounds,(-float('inf'),float('inf')))))
        for record in result['cuts']:
            block=detected.blocks[record['block']]
            co=record['coefficients']
            assert replay_support(block.features,block.symbols,block.box,co,block.rows,record['support_witness'])
            digest=hashlib.sha256(json.dumps(record['support_witness'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
            assert replay_row_certificate(record['row_certificate'],variables=names,bounds=bounds,
                linear_terms=dict(zip((str(s) for s in block.symbols),co[:len(block.variables)])),
                multipliers=co[len(block.variables):],support_rhs=float.fromhex(record['support_witness']['rhs']),
                sides=[AffineSide(s.source_id,s.affine,s.rhs) for s in block.sides],support_id=digest)
            assert not record['actual_row']['local']
            assert record['column_names']==['v0','v1','objective_epigraph']
        assert result['solve_wall_seconds']>=result['separation']['callback_seconds']
        assert result['total_seconds']>=result['solve_wall_seconds']
        json.dumps(result,allow_nan=False)
    finally: built.model.freeProb()


def test_fixed_auto_policy_restricts_redundant_convex_and_unrestricted_boxes():
    for quadratic,extra,expected in [([(0,0,1.)],[],False),
                                    ([(0,1,-1.)],[],False),
                                    ([(0,1,-1.)],[row(lin={0:1.,1:1.},ub=1.)],True)]:
        inst=instance('policy',[(0.,1.),(0.,1.)],[row(quad=quadratic),*extra])
        built=build_model(inst)
        try: assert any(b.auto_eligible for b in discover(inst,built).blocks)==expected
        finally: built.model.freeProb()


def test_unsupported_cut_dimension_keeps_original_native_model():
    inst=instance('dimension',[(0.,1.)]*5,[row(quad=[(i,i,1.) for i in range(5)])])
    built=build_model(inst)
    try:
        detected=discover(inst,built)
        assert not detected.blocks and detected.stats['unsupported_sides']==1
        assert built.model.getNVars()==6
    finally: built.model.freeProb()
