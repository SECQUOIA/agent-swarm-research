"""Reproduce all manuscript numerical artifacts from the bundled inputs.

Requires Python >=3.10, NumPy, SciPy and Matplotlib. No network or parent imports.
Run from the paper directory: OPENBLAS_NUM_THREADS=1 python repro/reproduce.py
The computations illustrate proved results; they are not substitutes for proofs.
"""
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal as D, localcontext
import csv, hashlib, json, math, platform, sys
import numpy as np
import scipy
from scipy.linalg import null_space, eigh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from prepare_data import reconstruct, frac, dot
from decimal_linear import reference_errors

ROOT=Path(__file__).resolve().parent
PAPER=ROOT.parent
SEED=20260907
PDF_METADATA={'CreationDate':None,'ModDate':None,'Creator':'conditioning-paper/repro/reproduce.py'}
plt.rcParams.update({'font.size':8.5,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})

def write_rows(name, rows):
    with (ROOT/'results'/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def savefig(name):
    plt.savefig(PAPER/'figures'/name,bbox_inches='tight',metadata=PDF_METADATA);plt.close()

def verify_data():
    records={}
    provenance=json.loads((ROOT/'data'/'provenance.json').read_text())
    for name in ('afiro','sc50b','adlittle'):
        path=ROOT/'data'/(name+'.json')
        assert hashlib.sha256(path.read_bytes()).hexdigest()==provenance['instances'][name]['frozen_json_sha256']
        data=json.loads(path.read_text());cert=data['certificates']
        A=[[frac(v) for v in row] for row in data['A']]
        b,c=list(map(frac,data['b'])),list(map(frac,data['c']))
        x,y=list(map(Q,cert['strict_point'])),list(map(Q,cert['compactness_y']))
        eta=Q(cert['compactness_eta']);m,n=len(A),len(c)
        assert eta>=0 and min(x)>0
        assert all(dot(row,x)==rhs for row,rhs in zip(A,b))
        margins=[sum(A[i][j]*y[i] for i in range(m))+eta*c[j] for j in range(n)]
        assert min(margins)>0
        upper_x,lower_y=list(map(Q,cert['near_optimal_primal'])),list(map(Q,cert['dual_lower_bound_y']))
        assert min(upper_x)>=0 and all(dot(row,upper_x)==rhs for row,rhs in zip(A,b))
        assert min(c[j]-sum(A[i][j]*lower_y[i] for i in range(m)) for j in range(n))>=0
        lo,hi=dot(b,lower_y),dot(c,upper_x)
        assert lo==Q(cert['objective_lower']) and hi==Q(cert['objective_upper']) and lo<=hi
        records[name]={'exact_certificates':'passed','strict_margin':float(min(x)), 'compactness_margin':float(min(margins)),'eta':int(eta),'objective_interval_width':float(hi-lo)}
    (ROOT/'results'/'certificate_checks.json').write_text(json.dumps(records,indent=2)+'\n')
    return records

def fractional():
    rows=[]
    with localcontext() as ctx:
        ctx.prec=80
        for exponent in range(2,25):
            g=D(10)**(-exponent);b=(-g+(3*g-2*g*g).sqrt())/3;a=1-g-b;q=a*g-b*b
            mu=q/(1-b-2*g);qb=-g-2*b;qg=1-b-2*g
            k11=b**-2+qb*qb/(q*q)+2/q;k12=qb*qg/(q*q)+1/q;k22=qg*qg/(q*q)+2/q
            tr=(2*k11-2*k12+4*k22)/7;det=(k11*k22-k12*k12)/7
            high=(tr+(tr*tr-4*det).sqrt())/2;low=det/high
            ah=(a+g+((a-g)**2+4*b*b).sqrt())/2;al=q/ah
            eig=[1/(b*ah),low,1/(b*al),high]
            assert all(eig[j]<eig[j+1] for j in range(3))
            assert abs(q+b*qb)/q<D('1e-60')
            scales=[eig[0]*mu.sqrt(),eig[1]*mu,eig[2]*mu*mu.sqrt(),eig[3]*mu*mu]
            row=dict(gap=float(g),mu=float(mu),**{f'lambda{j+1}':float(v) for j,v in enumerate(eig)},**{f'scaled{j+1}':float(v) for j,v in enumerate(scales)},kappa_full=float(high/eig[0]),kappa_restricted=float(high/low),full_scaled_gap=float(high/eig[0]*g*g.sqrt()),restricted_scaled_gap=float(high/low*g))
            rows.append(row)
            # Separate coordinate-free float64 trace-product calculation at resolved points.
            if exponent in (2,4,6):
                X=np.array([[float(a),float(b),0],[float(b),float(g),0],[0,0,float(b)]])
                U=np.array([[[-1,1,0],[1,0,0],[0,0,1]],[[-1,0,0],[0,1,0],[0,0,0]],[[0,0,1],[0,0,0],[1,0,0]],[[0,0,0],[0,0,1],[0,1,0]]],float)
                Xi=np.linalg.inv(X);G=np.einsum('aij,bij->ab',U,U)
                K=np.array([[np.trace(Xi@u@Xi@v) for v in U] for u in U])
                direct=eigh(K,G,eigvals_only=True)
                assert np.max(abs(direct/np.array(list(map(float,eig)))-1))<1e-7
    write_rows('fractional_sdp.csv',rows)
    fig,axes=plt.subplots(1,2,figsize=(6.4,2.7))
    g=np.array([r['gap'] for r in rows]);limits=[np.sqrt(2),1,np.sqrt(2),4/7]
    for j in range(4):axes[0].semilogx(g,[r[f'scaled{j+1}']/limits[j] for r in rows],label=rf'$\lambda_{j+1}\mu^{{{["1/2","1","3/2","2"][j]}}}/C_{j+1}$')
    axes[0].axhline(1,color='gray',lw=.6);axes[0].set(xlabel='Primal gap $g$',ylabel='Normalized spectral constant',ylim=(.97,1.3));axes[0].legend(fontsize=7)
    axes[1].loglog(g,[r['kappa_full'] for r in rows],label='Four-dimensional tangent')
    axes[1].loglog(g,[r['kappa_restricted'] for r in rows],label='Two-dimensional section')
    axes[1].set(xlabel='Primal gap $g$',ylabel='Reduced Hessian condition number');axes[1].legend()
    fig.tight_layout();savefig('fractional-sdp.pdf')
    return rows

def simplex():
    rows=[]
    W=null_space(np.ones((1,3)))
    for theta in (1.,.1,.01,.001):
        with localcontext() as ctx:
            ctx.prec=70;t=D(str(theta))
            for exponent in np.linspace(-8,1,73):
                mu=D(str(10**exponent));c=[D(0),t,D(1)]
                # x_i=mu/(c_i+z), with sum x=1 and z>0; monotone bisection.
                lo,hi=D(0),3*mu
                for _ in range(250):
                    z=(lo+hi)/2
                    if sum(mu/(ci+z) for ci in c)>1:lo=z
                    else:hi=z
                x=[mu/(ci+(lo+hi)/2) for ci in c];g=sum(ci*xi for ci,xi in zip(c,x))
                # Factor SVD avoids squaring the condition number in a normal matrix.
                s=np.linalg.svd(W/np.array(list(map(float,x)))[:,None],compute_uv=False)
                kappa=(s[0]/s[-1])**2
                rows.append(dict(theta=theta,mu=float(mu),gap=float(g),kappa=kappa,asymptotic_limit=(1+theta**2+math.sqrt(1-theta**2+theta**4))/(1+theta**2-math.sqrt(1-theta**2+theta**4))))
    write_rows('simplex.csv',rows)
    plt.figure(figsize=(3.15,2.7))
    for theta in (1.,.1,.01,.001):
        r=[r for r in rows if r['theta']==theta];plt.loglog([v['gap'] for v in r],[v['kappa'] for v in r],label=rf'$\vartheta={theta:g}$')
    plt.xlabel('Primal gap $g$');plt.ylabel('Reduced Hessian condition number');plt.legend(ncol=2,fontsize=7);savefig('simplex-plateau.pdf')
    return rows

def oscillatory():
    rows=[]
    with localcontext() as ctx:
        ctx.prec=80;pi=D('3.141592653589793238462643383279502884197169399375105820974944592307816406286');eps=D('.01')
        for k in (1,2,3,4,6,8):
            g=(-2*pi*k).exp();a,b,d=D(2),eps/g,g**-2+(1-g)**-2
            hi=(a+d+((a-d)**2+4*b*b).sqrt())/2;lo=(a*d-b*b)/hi
            slope=-b/(d-lo);weak=abs(slope)/(1+slope*slope).sqrt();strong=1/(1+slope*slope).sqrt()
            uw=weak/(4*lo);us=strong/(4*hi);error=uw/(uw*uw+us*us).sqrt()
            rows.append(dict(k=k,gap=float(g),weak_rhs_fraction=float(weak),weak_rhs_over_gap=float(weak/g),relative_solution_error=float(error),weak_solution_over_gap=float(uw/g),strong_solution_over_gap_squared=float(us/(g*g))))
    write_rows('oscillatory.csv',rows)
    with (PAPER/'tables'/'analytic-checks.tex').open('w') as f:
        f.write('\\begin{tabular}{rrrr}\n\\toprule\n$k$ & $g_k$ & $\\|\\Pi c\\|/(g_k\\|c\\|)$ & Relative solution error\\\\\n\\midrule\n')
        for r in rows[:4]:f.write(f"{r['k']} & {r['gap']:.2e} & {r['weak_rhs_over_gap']:.8f} & {r['relative_solution_error']:.8f} \\\\\n")
        f.write('\\bottomrule\n\\end{tabular}\n')
    return rows

def factor_metrics(W,c,x,mu):
    U,s,Vt=np.linalg.svd(W/x[:,None],full_matrices=False)
    grad=W.T@(-1/x+c/mu)
    local=(Vt@grad)/s
    rho=np.linalg.norm(local)
    step=-Vt.T@(local/s)
    return rho,step,s

def center(W,c,x,mu):
    x=x.copy();status='iteration_limit'
    for iteration in range(150):
        rho,dxz,s=factor_metrics(W,c,x,mu)
        if rho<1e-7:return x,iteration,rho,'converged'
        dx=W@dxz;directional=float((-1/x+c/mu)@dx)
        if directional>=0:return x,iteration,rho,'non_descent'
        negative=dx<0;alpha=min(1.,.99*np.min(-x[negative]/dx[negative])) if negative.any() else 1.
        accepted=False
        for _ in range(70):
            relative=alpha*dx/x
            change=-np.log1p(relative).sum()+alpha*(c@dx)/mu
            if change<=.01*alpha*directional:
                x=x+alpha*dx;accepted=True;break
            alpha*=.5
        if not accepted:return x,iteration,rho,'line_search_stall'
        if alpha*np.linalg.norm(dx)<=np.finfo(float).eps*np.linalg.norm(x) and rho<1e-5:
            return x,iteration,rho,'roundoff_stop'
    return x,iteration,rho,status

def netlib():
    rows=[];summary=[]
    for name in ('afiro','sc50b','adlittle'):
        data=json.loads((ROOT/'data'/(name+'.json')).read_text());cert=data['certificates']
        A=np.array(data['A']);b=np.array(data['b']);c=np.array(data['c']);W=null_space(A)
        Aq=[[frac(v) for v in row] for row in A];bq=list(map(frac,b));cq=list(map(frac,c))
        x=np.array([float(Q(v)) for v in cert['strict_point']]);m,n=A.shape
        lo,hi=Q(cert['objective_lower']),Q(cert['objective_upper'])
        scale=max(1.,np.max(abs(c)))
        for j in range(27):
            mu=scale*10**(-.5*j)
            x,iterations,rho,solver_status=center(W,c,x,mu)
            xr=reconstruct(Aq,bq,x,cert['pivots'])
            xf=np.array(list(map(float,xr)));repair=float(np.max(abs(xf-x)/x))
            positive=min(xr)>0
            exact_obj=dot(cq,xr);gaplo,gaphi=float(exact_obj-hi),float(exact_obj-lo)
            status=[]
            if not positive:status.append('rational_repair_not_positive')
            if repair>1e-4:status.append('large_feasibility_repair')
            tested=xf if positive else x
            rho_after,_,singular=factor_metrics(W,c,tested,mu)
            if rho_after>1e-5:status.append('centrality_unresolved')
            # Interval width and exact rational objective avoid cancellation-based gap claims.
            if gaplo<=0 or float(hi-lo)> .01*max(gaplo,0):status.append('gap_unresolved')
            equality=np.linalg.norm(A@tested-b,np.inf)/(1+np.linalg.norm(A,np.inf)*np.linalg.norm(tested,np.inf)+np.linalg.norm(b,np.inf))
            if equality>1e-12:status.append('equality_unresolved')
            spectral_indicator=np.finfo(float).eps*max(W.shape)*singular[0]/singular[-1]
            if spectral_indicator>1e-6:status.append('spectral_resolution_unresolved')
            cond=(singular[0]/singular[-1])**2
            row=dict(instance=name,mu=mu,gap_lower=gaplo,gap_upper=gaphi,gap_midpoint=(gaplo+gaphi)/2,kappa=cond,lambda_min=singular[-1]**2,lambda_max=singular[0]**2,unscaled_decrement=rho_after,scaled_equality_residual=equality,relative_feasibility_repair=repair,spectral_resolution_indicator=spectral_indicator,min_coordinate=float(min(xr)),newton_iterations=iterations,solver_status=solver_status,status='accepted' if not status else '|'.join(status))
            rows.append(row)
            if positive and repair<1e-4:x=xf
        accepted=[r for r in rows if r['instance']==name and r['status']=='accepted']
        assert len(accepted)>=5
        tail=accepted[-1]
        summary.append(dict(instance=name,m=m,n=n,accepted=len(accepted),attempted=27,last_gap=tail['gap_midpoint'],last_kappa=tail['kappa'],last_decrement=tail['unscaled_decrement']))
        print('Netlib',summary[-1],flush=True)
    write_rows('netlib.csv',rows);write_rows('netlib_summary.csv',summary)
    plt.figure(figsize=(3.15,2.7))
    for name in ('afiro','sc50b','adlittle'):
        r=[r for r in rows if r['instance']==name and r['status']=='accepted'];plt.loglog([v['gap_midpoint'] for v in r],[v['kappa'] for v in r],'.-',label=name)
    plt.xlabel('Primal gap interval midpoint');plt.ylabel('Reduced Hessian condition number');plt.legend();savefig('netlib.pdf')
    with (PAPER/'tables'/'netlib.tex').open('w') as f:
        f.write('\\begin{tabular}{lrrrrr}\n\\toprule\nInstance & $(m,n)$ & Accepted/attempted & Last gap & $\\kappa$ & $\\rho$\\\\\n\\midrule\n')
        for r in summary:f.write(f"{r['instance']} & $({r['m']},{r['n']})$ & {r['accepted']}/{r['attempted']} & {r['last_gap']:.2e} & {r['last_kappa']:.2e} & {r['last_decrement']:.1e} \\\\\n")
        f.write('\\bottomrule\n\\end{tabular}\n')
    return rows

def degenerate_lp():
    A=np.array([[1,1,1,1],[0,1,1.5,3.]])
    c=np.array([1.,1,0,1]);W=null_space(A);x=np.array([2,3,3,3.])/11
    t=(-6+4*np.sqrt(3))/9;slack=c-A.T@np.array([-1.5*t,t]);lim=np.linalg.eigvalsh(W.T@np.diag(slack**2)@W)
    rows=[]
    for mu in np.logspace(0,-9,19):
        x,it,rho,status=center(W,c,x,mu);s=np.linalg.svd(W/x[:,None],compute_uv=False)
        rows.append(dict(mu=mu,gap=float(c@x),kappa=(s[0]/s[-1])**2,scaled_lambda_min=mu*mu*s[-1]**2,scaled_lambda_max=mu*mu*s[0]**2,limit_min=lim[0],limit_max=lim[-1],limit_kappa=lim[-1]/lim[0],decrement=rho,status=status))
    assert abs(rows[-1]['kappa']/rows[-1]['limit_kappa']-1)<1e-5
    write_rows('degenerate_lp.csv',rows)
    return rows

def cg():
    rng=np.random.default_rng(SEED);n=60
    Qm,_=np.linalg.qr(rng.normal(size=(n,n)));coeff=rng.normal(size=n);rhs=Qm@coeff
    rows=[];hist=[];systems=[]
    for gap in (1e-1,1e-2,1e-3,1e-4):
        values=np.r_[np.linspace(1,2,n//2),np.linspace(1,3,n//2)*gap**-2]
        # Explicit float64 matrix-vector access; no exact-spectral implementation of CG.
        H=(Qm*values)@Qm.T;H=(H+H.T)/2
        observed=np.linalg.eigvalsh(H)
        assert observed[0]>0 and np.max(abs(observed/np.sort(values)-1))<1e-6
        systems.append(dict(gap=gap,H=H.tolist(),rhs=rhs.tolist(),prescribed_eigenvalues=values.tolist()))
        u=np.zeros(n);r=rhs.copy();p=r.copy();rr=r@r
        exact_coeff=coeff/values;energy0=np.sqrt(np.sum(coeff*coeff/values))
        target=1e-8;stop=None
        for k in range(1,501):
            Hp=H@p;alpha=rr/(p@Hp);u+=alpha*p;r-=alpha*Hp
            newrr=r@r
            true=np.linalg.norm(rhs-H@u)/np.linalg.norm(rhs)
            # Known exact eigenvalues define a stable reference energy norm, without a normal solve.
            error_coeff=Qm.T@u-exact_coeff
            energy=np.sqrt(np.sum(values*error_coeff**2))/energy0
            recursive=np.sqrt(newrr)/np.linalg.norm(rhs)
            hist.append(dict(gap=gap,iteration=k,recursive_residual=recursive,true_residual=true,relative_energy_error=energy))
            if recursive<=target:
                true,energy=reference_errors(H,rhs,u)
                stop=dict(gap=gap,condition=values[-1]/values[0],iterations=k,recursive_residual=recursive,true_residual=true,relative_energy_error=energy,status='true_residual_pass' if true<=target else 'recursive_only_stop');break
            p=r+(newrr/rr)*p;rr=newrr
        if stop is None:stop=dict(gap=gap,condition=values[-1],iterations=k,recursive_residual=recursive,true_residual=true,relative_energy_error=energy,status='iteration_limit')
        rows.append(stop)
    write_rows('cg.csv',rows);write_rows('cg_history.csv',hist)
    (ROOT/'results'/'cg_systems.json').write_text(json.dumps(systems)+'\n')
    with (PAPER/'tables'/'cg.tex').open('w') as f:
        f.write('\\begin{tabular}{rrrrr}\n\\toprule\n$g$ & Iterations & Recursive residual & True residual & Relative energy error\\\\\n\\midrule\n')
        for r in rows:f.write(f"{r['gap']:.0e} & {r['iterations']} & {r['recursive_residual']:.2e} & {r['true_residual']:.2e} & {r['relative_energy_error']:.2e} \\\\\n")
        f.write('\\bottomrule\n\\end{tabular}\n')
    return rows

def manifest():
    files=list((ROOT/'data').glob('*'))+list((ROOT/'results').glob('*'))+list((PAPER/'figures').glob('*.pdf'))+list((PAPER/'tables').glob('*.tex'))+list(ROOT.glob('*.py'))
    files=[p for p in files if p.name!='manifest.json']
    out=dict(command=f'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 {sys.executable} repro/reproduce.py',portable_command='OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python repro/reproduce.py',python=sys.version,numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,platform=platform.platform(),seed=SEED,decimal_precision=dict(fractional_sdp=80,oscillatory=80,cg_reference=80,simplex=70),
       contracts=dict(netlib_decrement_max=1e-5,netlib_gap_interval_relative_width_max=.01,netlib_feasibility_repair_relative_max=1e-4,netlib_scaled_equality_max=1e-12,netlib_spectral_resolution_indicator_max=1e-6,cg_recursive_stop=1e-8,cg_max_iterations=500),
       hashes={str(p.relative_to(PAPER)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)})
    (ROOT/'results'/'manifest.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':
    (ROOT/'results').mkdir(exist_ok=True);(PAPER/'figures').mkdir(exist_ok=True);(PAPER/'tables').mkdir(exist_ok=True)
    verify_data();fractional();simplex();oscillatory();degenerate_lp();netlib();print('CG',cg(),flush=True);manifest()
    print('All reproduction checks passed.')
