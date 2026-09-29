import sys, re
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.out=[]; self.skip=0; self.mathdepth=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if self.mathdepth:
            if tag=='math': self.mathdepth+=1
            return
        if tag=='math':
            self.out.append(' $'+(a.get('alttext') or '')+'$ '); self.mathdepth=1; return
        if tag in ('script','style'): self.skip+=1
        if tag in ('p','div','h1','h2','h3','h4','h5','h6','li','tr','br','section'): self.out.append('\n')
        if tag in ('h1','h2','h3','h4','h5','h6'): self.out.append('#'*int(tag[1])+' ')
    def handle_endtag(self, tag):
        if self.mathdepth:
            if tag=='math': self.mathdepth-=1
            return
        if tag in ('script','style'): self.skip-=1
        if tag in ('p','div','h1','h2','h3','h4','h5','h6','li','tr'): self.out.append('\n')
    def handle_data(self, d):
        if self.mathdepth or self.skip: return
        self.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8').read())
t=''.join(p.out); t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n\n',t)
open(sys.argv[2],'w').write(t)
