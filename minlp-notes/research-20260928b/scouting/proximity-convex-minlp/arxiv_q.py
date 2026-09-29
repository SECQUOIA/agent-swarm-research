import sys, xml.etree.ElementTree as ET
ns={'a':'http://www.w3.org/2005/Atom'}
t=ET.parse(sys.argv[1]).getroot()
for e in t.findall('a:entry',ns):
    i=e.find('a:id',ns).text.split('/abs/')[-1]
    ti=' '.join(e.find('a:title',ns).text.split())
    d=e.find('a:published',ns).text[:10]
    au=', '.join(a.find('a:name',ns).text for a in e.findall('a:author',ns))[:70]
    print(d,i,'|',ti[:110],'|',au)
