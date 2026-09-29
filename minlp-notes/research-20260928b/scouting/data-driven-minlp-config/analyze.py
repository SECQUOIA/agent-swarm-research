import sys, numpy as np
def load(path):
    d = np.loadtxt(path)
    return d[:,0], d[:,1].astype(int), d[:,2].astype(int)
def pieces(v):
    return 1 + int(np.sum(v[1:] != v[:-1]))
if __name__ == '__main__':
    for p in sys.argv[1:]:
        a, n, md = load(p)
        print(p, 'N', len(a), 'pieces', pieces(n), 'distinct', len(set(n)), 'min', n.min(), 'max', n.max(), 'maxdepth', md.max(), 'tree-pieces(size,depth)', pieces(n*1000+md))
