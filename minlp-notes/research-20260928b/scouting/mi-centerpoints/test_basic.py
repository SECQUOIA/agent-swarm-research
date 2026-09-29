import numpy as np, time
from midepth import *
sq = np.array([[0,0],[1,0],[1,1],[0,1]],float)
A = np.array([[1,0],[0,1],[1,1]/np.sqrt(2),[-1,0]])
T = np.array([0.3,0.5,np.sqrt(2)*0.5,-0.25])
print(clip_area(sq,A,T), "expect", [0.7,0.5,0.5,0.25])
tri = np.array([[0,0],[1,0],[0,1]],float)
S = MISet([tri,tri])
t=time.time(); print("2 fibers simplex", S.best_point(), "target", 2/9, time.time()-t)
S = MISet([tri,tri,tri])
print("3-prism simplex", S.best_point())
S = MISet([tri])
print("1 fiber simplex", S.best_point(), 4/9)
