"""Exact posterior edge intervals, using a separately verified energy certificate."""
import json
from fractions import Fraction as F

from envelope_rational_certificates import Certificate,energy,law,require,verify_certificate


def divergence(y,z,positive,negative):
    return energy([y],[positive],[negative])-energy([z],[positive],[negative])-law(z,positive,negative)*(y-z)


def sharpen(positive,negative,certificate,steps=80):
    result=[]
    for y,cp,cm in zip(certificate.flow,positive,negative):
        if certificate.gap==0:
            result.append((y,y))
            continue
        ends=[]
        for direction in [-1,1]:
            outside=y+direction*certificate.radius
            inside=y
            require(divergence(y,outside,cp,cm)>=certificate.gap,"initial Bregman bracket")
            for _ in range(steps):
                middle=(inside+outside)/2
                if divergence(y,middle,cp,cm)>=certificate.gap:
                    outside=middle
                else:
                    inside=middle
            ends.append(outside)
        result.append(tuple(ends))
    verify_bounds(positive,negative,certificate,result)
    return result


def verify_bounds(positive,negative,certificate,bounds):
    """Requires the base energy certificate to be independently verified first."""
    require(len(bounds)==len(certificate.flow)==len(positive)==len(negative),"Bregman interval dimensions")
    require(isinstance(certificate.gap,F) and certificate.gap>=0,"nonnegative rational base gap")
    require(all(isinstance(c,F) and c>0 for c in positive+negative),"positive rational Bregman coefficients")
    for y,cp,cm,(lower,upper) in zip(certificate.flow,positive,negative,bounds):
        require(isinstance(lower,F) and isinstance(upper,F),"rational Bregman endpoints")
        require(lower<=y<=upper,"Bregman interval order")
        if certificate.gap==0:
            require(lower<=y<=upper,"zero-gap Bregman interval")
        else:
            require(divergence(y,lower,cp,cm)>=certificate.gap,"lower Bregman bound")
            require(divergence(y,upper,cp,cm)>=certificate.gap,"upper Bregman bound")
    return True


def check_file(path):
    with open(path) as stream:
        payload=json.load(stream)
    b,positive,negative=(list(map(F,payload[key])) for key in ['b','positive','negative'])
    cert=Certificate(list(map(F,payload['flow'])),list(map(F,payload['potentials'])),
                     list(map(F,payload['root_upper'])),F(payload['gap']),F(payload['radius']))
    verify_certificate(payload['edges'],b,positive,negative,cert)
    bounds=sharpen(positive,negative,cert)
    zero_free=sum(lower>0 or upper<0 for lower,upper in bounds)
    widths=[upper-lower for lower,upper in bounds]
    require(max(widths)<=2*cert.radius,"interval improvement")
    for e,(lower,upper) in enumerate(bounds):
        print(f'edge{e}: certified interval width {float(upper-lower):.9g}; sign {"positive" if lower>0 else "negative" if upper<0 else "unresolved"}')
    print(f'{len(bounds)} exact Bregman intervals verified; {zero_free} exclude zero.')
    print(f'Max width {float(max(widths)):.9g}, previous uniform width {float(2*cert.radius):.9g}.')
    pressure_widths=[law(upper,cp,cm)-law(lower,cp,cm)
                     for (lower,upper),cp,cm in zip(bounds,positive,negative)]
    print(f'Max certified envelope edge-pressure width {float(max(pressure_widths)):.9g}.')
    bad=list(bounds);bad[0]=(cert.flow[0],bounds[0][1])
    if cert.gap>0:
        try:
            verify_bounds(positive,negative,cert,bad)
        except ValueError:
            pass
        else:
            raise RuntimeError('Invalid Bregman interval accepted')
    return bounds


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('certificate')
    args=parser.parse_args()
    check_file(args.certificate)
