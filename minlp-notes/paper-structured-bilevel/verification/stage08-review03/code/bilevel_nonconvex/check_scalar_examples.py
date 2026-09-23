"""Small exact regressions for the stated nonconvex bilevel examples."""
import sympy as sp
from scalar_solver import Instance, Constraint, build_atlas, optimize_tariff, rational_between


def main():
    q = sp.Rational
    instance = Instance((1,1),(-1,'-1/2'),(1,1),(0,0),(1,1),'3/5',1,0,1)
    atlas = build_atlas(instance)
    assert any(p.A < 0 for p in atlas.pieces)
    assert any(p.A > 0 for p in atlas.pieces)
    ties = next(rs for x,rs in atlas.points if x == q(17,20))
    assert {(r.left,r.right) for r in ties} == {(q(3,8),q(3,8)),(q(13,8),q(13,8))}
    constraints = [Constraint(0,(1,1),1)]
    optimistic = optimize_tariff(atlas,constraints)
    pessimistic = optimize_tariff(atlas,constraints,'pessimistic')
    assert optimistic.value == pessimistic.value == q(51,160)
    assert optimistic.attained and optimistic.x == q(17,20) and optimistic.w == q(3,8)
    assert not pessimistic.attained and pessimistic.limit_x == q(17,20)
    assert pessimistic.x is None and pessimistic.w is None

    # The convex envelope has all w in [0,1] as minimizers at x=2;
    # the original strictly concave scalar follower has only {0,1}.
    original = build_atlas(Instance((1,),(-1,),(1,),(0,),(1,),3,1,1,3))
    equality = [Constraint(0,(1,),'1/2'),Constraint(0,(-1,),'-1/2')]
    assert optimize_tariff(original,equality) is None
    responses = next(rs for x,rs in original.points if x==2)
    assert {(r.left,r.right) for r in responses} == {(0,0),(1,1)}

    # The sample must not accidentally inherit two independent square roots.
    sample = rational_between(sp.sqrt(2),sp.sqrt(3))
    assert sample.is_Rational and sp.sqrt(2) < sample < sp.sqrt(3)
    print('Nonconvex phase-transition, nonattainment, false convexified tie, and rational-sample regressions passed.')


if __name__ == '__main__':
    main()
