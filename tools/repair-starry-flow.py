from pathlib import Path
import json,re,zipfile
R=Path(__file__).resolve().parents[1]
d=json.loads((R.parent/'downloads/Starry-Voyage.json').read_text())
s=d['custom_css'].split('/* Follow the original wave,')[0]
# Remove every forced focal point, including superseded declarations.
s=re.sub(r'object-position\s*:[^;}]+;?', '', s)
# Let user styling override the default fit, rather than locking it with !important.
s=s.replace('object-fit:cover!important','object-fit:cover')
# Remove the obsolete circular-avatar rule, superseded by the original full frame.
s=re.sub(r'#chat \.mes \.avatar img\{position:absolute!important;left:14%[^}]+\}', '', s)
s=re.sub(r'#chat \.mes \.mes_buttons>:nth-child\([^\n]+\n','',s)
s=s.replace('assets/painted-controls/starry/','assets/starry-flow/')
s+='''
/* Follow the original wave, excluding the expanded menu and hidden actions. */
#chat .mes .mes_buttons{margin-bottom:14px!important;}
#chat .mes .mes_buttons>:not(.extraMesButtons){transform:translateY(var(--wave-y,0px))!important;}
'''
visible=':not(.extraMesButtons):not(.displayNone):not(.hidden):not([hidden]):not([style*="display: none"]):not([style*="display:none"])'
for i,y in enumerate([-5,2,6,3,-4,-2,0],1):
 s+=f'\n#chat .mes .mes_buttons>:nth-child({i} of {visible}){{--wave-y:{y}px;}}'
s+='\n@media(min-width:700px){#chat .mes .mes_buttons{margin-bottom:26px!important;}}\n'
d['custom_css']=s
p=R/'theme/starry-flow/星潮夜航.json';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(R/'theme/starry-flow.css').write_text(s)
assert 'object-position' not in s
assert 'base64,' not in s
out=R.parent/'downloads';(out/'Starry-Voyage.json').write_bytes(p.read_bytes())
with zipfile.ZipFile(out/'Starry-Voyage.zip','w',zipfile.ZIP_DEFLATED) as z:z.write(p,'星潮夜航.json')
