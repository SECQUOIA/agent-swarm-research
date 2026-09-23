"""Gauss-Hermite checks of shared physical-bath limits (a Gaussian benchmark).

This is not Potts enumeration and does not verify literature novelty. The bath
weight is the exact power-law weight. Increase --order to check convergence.
"""
import argparse
import json
import numpy as np
from numpy.polynomial.hermite import hermgauss

parser=argparse.ArgumentParser()
parser.add_argument('--order',type=int,default=96)
args=parser.parse_args()
x,w=hermgauss(args.order)
w=w/np.sqrt(np.pi)

def xlogx(x):
    out=np.zeros_like(x)
    nz=x>0
    out[nz]=x[nz]*np.log(x[nz])
    return out

def calculate(N, pminus):
    c=N**1.25
    energies=np.concatenate([-N/2+np.sqrt(2*N)*x,
                              N/2+np.sqrt(2*N)*x])
    weights=np.concatenate([pminus*w,(1-pminus)*w])
    total=energies[:,None]+energies[None,:]
    z=total/c
    logW=np.full_like(z,-np.inf)
    feasible=z<1
    zz=z[feasible]
    # log1p(-z)+z; use a series when cancellation would dominate.
    value=np.log1p(-zz)+zz
    small=np.abs(zz)<1e-3
    zs=zz[small]
    value[small]=sum(-zs**k/k for k in range(2,9))
    logW[feasible]=c*value
    W=np.exp(logW)
    jointweights=weights[:,None]*weights[None,:]
    norm=np.sum(jointweights*W)
    ratio=W/norm
    marginalratio=W@weights/norm
    jointtv=.5*np.sum(jointweights*np.abs(ratio-1))
    marginaltv=.5*np.sum(weights*np.abs(marginalratio-1))
    djoint=np.sum(jointweights*xlogx(ratio))
    dmarg=np.sum(weights*xlogx(marginalratio))
    labels=np.concatenate([np.zeros(args.order),np.ones(args.order)])
    opposite=labels[:,None]!=labels[None,:]
    popp=np.sum(jointweights[opposite]*ratio[opposite])
    target=opposite/(2*pminus*(1-pminus))
    toconditioned=.5*np.sum(jointweights*np.abs(ratio-target))
    return {'N':N,'c':c,'minus_weight':pminus,'opposite_probability':popp,
            'TV_joint':jointtv,'TV_marginal':marginaltv,
            'TV_to_conditioned':toconditioned,
            'mutual_information_nats':djoint-2*dmarg}

results=[calculate(N,p) for p in [.5,.7] for N in [100,1000,10000,100000,1000000]]
print(json.dumps({'quadrature_order':args.order,'results':results},indent=2))
