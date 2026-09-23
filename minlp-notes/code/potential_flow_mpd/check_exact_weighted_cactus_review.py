"""Independent arithmetic and exact-capacity audit of the block solver."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from random import Random
from exact_weighted_cactus import Quadratic, solve_cycle, solve_cactus
from check_reopened_joint_weighted_review import vertex_optimum


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def decimal_rational(x):
    return Decimal(x.numerator)/Decimal(x.denominator)


def decimal_quadratic(x):
    return decimal_rational(x.a)+decimal_rational(x.b)*decimal_rational(x.d).sqrt()


def arithmetic_checks():
    rng = Random(607601)
    count = 0
    with localcontext() as ctx:
        ctx.prec = 180
        for i in range(1200):
            values = []
            for _ in range(2):
                values.append(Quadratic(F(rng.randrange(-100,101),rng.randrange(1,12)),
                                        F(rng.randrange(-100,101),rng.randrange(1,12)),
                                        F(rng.randrange(0,31),rng.randrange(1,12))))
            x,y = values
            dx,dy = map(decimal_quadratic,values)
            expected = (dx>dy)-(dx<dy)
            # Random small values have a huge separation relative to 180-digit error.
            require(x.compare(y)==expected, 'Cross-field comparison mismatch')
            lo,hi = x.interval(i%100)
            require(hi-lo<=F(1,2**(i%100)), 'Interval width failure')
            require(decimal_rational(lo)<=dx<=decimal_rational(hi), 'Interval containment failure')
            count += 1
        # Algebraically equal values with different, non-square-free radicands.
        for d in (2,3,5,7,11):
            for scale in (2,3,17,123):
                x=Quadratic(F(17,9),F(8,13),F(d))
                y=Quadratic(F(17,9),F(8,13*scale),F(d*scale*scale))
                require(x.compare(y)==0 and y.compare(x)==0, 'Equivalent fields compare unequal')
                tiny=F(1,10**90)
                require(x.compare(y+tiny)<0 and (x+tiny).compare(y)>0, 'Near equality sign failure')
                count += 1
    return count


def fixed_q_checks():
    rng=Random(572019)
    feasible=0
    for case in range(140):
        n=rng.randrange(3,7)
        offsets=[F(rng.randrange(-4,5)) for _ in range(n)]
        q=F(rng.randrange(-5,6),rng.randrange(1,4))
        weights=[F(rng.randrange(-2,3)) for _ in range(n)]
        lower=[F(rng.randrange(1,4),2) for _ in range(n)]
        upper=[v+F(rng.randrange(0,6),2) for v in lower]
        f=[(q+t)*abs(q+t) for t in offsets]
        flow_lower=[q+offsets[0]]+[None]*(n-1)
        flow_upper=list(flow_lower)
        for sense in ('max','min'):
            direction=1 if sense=='max' else -1
            expected=vertex_optimum(f,[direction*w for w in weights],lower,upper)
            result=solve_cycle(offsets,weights,lower,upper,flow_lower,flow_upper,sense)
            require((result is None)==(expected is None),'Capacity feasibility mismatch')
            if result is not None:
                feasible+=1
                require(result['circulation'].b==0 and result['circulation'].a==q,'Pinned q changed')
                require(result['objective'].b==0 and result['objective'].a==direction*expected,'Pinned-q LP value mismatch')
                beta=result['resistances']
                require(sum(b*t for b,t in zip(beta,f))==0,'Rational witness loop failed')
                require(all(lo<=b<=hi for lo,b,hi in zip(lower,beta,upper)),'Rational witness box failed')
    return {'sense_cases':280,'feasible':feasible}


def special_checks():
    args=([0,0,3,0],[2,-1,-3,0],[1]*4,[4,3,4,5])
    result=solve_cycle(*args)
    require(result['objective']==-12,'Interior optimum value')
    require(result['circulation']==-1,'Interior optimum q')
    require(result['resistances']==(F(1),F(2),F(1),F(1)),'Unique interior optimizer')
    # Fixed profile has q=sqrt(10)-3 and tests irrational endpoint recovery.
    fixed=solve_cycle([1,0,-1],[2,-1,0],[1,2,2],[1,2,2])
    require(fixed['circulation']==Quadratic(-3,1,10),'Irrational physical q mismatch')
    require(fixed['resistances']==(F(1),F(2),F(2)),'Irrational endpoint rational recovery')
    # All flows zero, repeated cuts, and flat objective.
    zero=solve_cycle([7]*3,[2,-1,0],[1]*3,[2,3,4])
    require(zero['objective']==0 and zero['circulation']==-7,'All-zero branch')
    flat=solve_cycle([1,0,-1],[3]*3,[1]*3,[2,3,4])
    require(flat['objective']==0,'Flat objective')
    problem={'cycles':[{'offsets':[1,0,-1], 'weights':[2,-1,0], 'lower':[1,2,2], 'upper':[1,2,2]},
                       {'offsets':[2,0,-1], 'weights':[2,1,0], 'lower':[1,3,2], 'upper':[1,3,2]}],
             'bridges':[{'flow':-2,'weight':-3,'lower':1,'upper':4}]}
    combined=solve_cactus(problem,bits=83)
    lo,hi=map(F,combined['objective_interval'])
    require(hi-lo<=F(1,2**83),'Sum interval width')
    require(combined['bridges'][0]['resistance']=='4','Bridge max endpoint')
    problem['sense']='min'
    require(solve_cactus(problem)['bridges'][0]['resistance']=='1','Bridge min endpoint')
    return 7


if __name__=='__main__':
    print({'arithmetic_cases':arithmetic_checks(), 'fixed_q':fixed_q_checks(), 'special_cases':special_checks()})
