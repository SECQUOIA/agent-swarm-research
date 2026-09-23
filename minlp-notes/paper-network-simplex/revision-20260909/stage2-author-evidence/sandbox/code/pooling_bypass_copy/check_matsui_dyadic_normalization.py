"""Exact source-generator normalization checks; print bit lengths, not huge data."""
for n in range(5, 9):
    s = n+n*n
    p = n**(n**4)
    p4 = p**(4*n)
    u0 = 2*p4-p
    D = 1 << ((u0//2).bit_length()-1)
    K = 4*p**(8*n)
    generators = [(u0, u0)]
    for i in range(1, n+1):
        term = 2*s*p**(2*n+i)
        generators.append((u0+term, u0-term))
    for i in range(1, n+1):
        for j in range(1, n+1):
            generators.append((u0+s*p**(i+j), u0+s*p**(i+j)))
    assert 2*D <= u0 < 4*D and D > p4//4
    for U, V in generators:
        assert 2*D <= U < 20*D
        assert K-D*V > 0
        assert 0 <= U-2*D < 32*D
        assert (32*D) & (32*D-1) == 0
    print(f'n={n}: {len(generators)} exact generators pass; '
          f'D bits={D.bit_length()}, threshold bits={K.bit_length()}')
print('PASS all Matsui generator normalization and dyadic-weight bounds')
