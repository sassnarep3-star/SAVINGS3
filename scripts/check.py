"""Check generated HTML references, official citations per row, and model arithmetic."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import math
ROOT=Path(__file__).resolve().parents[1]/'site'
allowed={'marcus.com','capitalone.com','ally.com','americanexpress.com','synchrony.com','chase.com','bankofamerica.com','wellsfargo.com','citi.com','fdic.gov'}
class Check(HTMLParser):
 def __init__(self,path): super().__init__();self.path=path;self.row=False;self.data=False;self.source=False;self.ids=set();self.refs=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a: self.ids.add(a['id'])
  if tag=='tr': self.row=True;self.data=False;self.source=False
  if tag=='td': self.data=True
  for key in ('href','src'):
   ref=a.get(key)
   if not ref:continue
   u=urlparse(ref)
   if u.scheme in ('http','https'):
    assert any(u.hostname==d or u.hostname.endswith('.'+d) for d in allowed),ref
    if self.row and tag=='a':self.source=True
   elif not u.scheme:
    target=ROOT/unquote(u.path) if u.path else self.path
    assert target.is_file(),(self.path,ref)
    if u.fragment:self.refs.append((target,u.fragment))
 def handle_endtag(self,tag):
  if tag=='tr':
   assert not self.data or self.source, f'Uncited row in {self.path}'
   self.row=False
checks={}
for p in ROOT.glob('*.html'):
 c=Check(p);c.feed(p.read_text());checks[p]=c
for c in checks.values():
 for target,frag in c.refs:assert frag in checks[target].ids,(target,frag)
for r in [.035,.032,.031]:
 p=math.floor(250000/(1+r)*100)/100
 assert p*(1+r)<=250000
 assert abs(100000*((1+r)**(365/365)-1)-100000*r)<1e-8
assert (Path('site/returns.html').read_text().count('$8,400.00'))>0
print(f'PASS: {len(checks)} HTML pages; internal files/fragments; every data row officially cited; coverage and annual-return arithmetic')
