"""Independent algebra checks for reservoir/composition Hessian elimination."""
import json
import numpy as np

rng = np.random.default_rng(20260907)
max_error = 0.
for _ in range(200):
    n, p, r = 3, 5, 2
    R = rng.normal(size=(p,p))
    C = R.T@R + np.eye(p)
    R = rng.normal(size=(r,r))
    K = R.T@R + .5*np.eye(r)
    G = -np.eye(n)
    P = rng.normal(size=(n,p))
    A = rng.normal(size=(r,p))
    B = rng.normal(size=(r,n))
    Hxx = G+B.T@K@B
    Hxy = P+B.T@K@A
    Hyy = C+A.T@K@A
    direct = Hxx-Hxy@np.linalg.solve(Hyy,Hxy.T)
    Cp = np.linalg.solve(C,P.T)
    relaxed = G-P@Cp
    Beff = B-A@Cp
    S = A@np.linalg.solve(C,A.T)
    formula = relaxed+Beff.T@np.linalg.solve(np.linalg.inv(K)+S,Beff)
    max_error = max(max_error,float(np.linalg.norm(direct-formula,ord=2)))
    assert np.allclose(direct,formula,rtol=1e-10,atol=1e-10)

G = np.diag([-1.,1.])
Jbad = np.array([[1.,2.]])
Jgood = np.array([[1.,.5]])
examples = {}
for name,J in [('unstabilizable',Jbad),('stabilizable',Jgood)]:
    examples[name] = {}
    for tau in [.5, 1., 2., 10., 100.]:
        H = G+tau*J.T@J
        examples[name][str(tau)] = np.linalg.eigvalsh(H).tolist()
        if name=='unstabilizable':
            assert np.linalg.det(H)<0
        elif tau>4/3:
            assert np.linalg.eigvalsh(H).min()>0
print(json.dumps({'random_cases':200,'maximum_schur_error':max_error,
                  'example_eigenvalues':examples},indent=2))
