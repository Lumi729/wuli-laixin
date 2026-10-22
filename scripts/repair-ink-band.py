from pathlib import Path
from PIL import Image
import numpy as np,base64,json
R=Path(__file__).resolve().parents[1];D=R/'assets/ink-seam-v3';D.mkdir(exist_ok=True)
im=Image.open(R/'assets/ink-v1/ink-atlas.webp').convert('RGB')
def save(im,name):
 a=255-np.asarray(im.convert('L'));v=np.zeros((*a.shape,4),dtype=np.uint8);v[:,:,3]=a
 o=Image.fromarray(v);o.save(D/(name+'.webp'),lossless=True);b=base64.b64encode((D/(name+'.webp')).read_bytes()).decode();w,h=o.size
 (D/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><image width="{w}" height="{h}" href="data:image/webp;base64,{b}"/></svg>')
# One continuous strip: the ribbon and its original vines are never split.
band=im.crop((27,696,997,832))
# Exclude tips belonging to the separate controls ornament below the name band.
band.paste('white',(73,124,213,136));band.paste('white',(757,124,897,136))
save(band,'name-band')
# Remove neighbouring pendant fragments before mapping the action frame.
out=Image.new('RGB',(1000,333),'white')
xs=[100,300,724,924];tx=[0,240,760,1000];ys=[820,878,988,1024];ty=[32,86,251,301]
for i in range(3):
 for j in range(3):out.paste(im.crop((xs[i],ys[j],xs[i+1],ys[j+1])).resize((tx[i+1]-tx[i],ty[j+1]-ty[j]),Image.Resampling.LANCZOS),(tx[i],ty[j]))
# Only the feather tips belong in the top strip; other marks are name-band pendants.
out.paste('white',(180,32,820,44))
save(out,'controls')
s=(R/'theme/ink-letter-aligned.css').read_text().replace('../assets/ink-aligned-v2/v9-controls-frame.svg','../assets/ink-seam-v3/controls.svg')
s+='''\n/* Codex: keep the original ink ribbon and ivy in one uninterrupted image. */
#chat .mes > .mes_block::before {
 left:-20px;right:-20px;width:auto;top:-16px;height:auto;aspect-ratio:970/136;
 background-image:url('../assets/ink-seam-v3/name-band.svg');
 background-size:100% 100%;mask-image:none;-webkit-mask-image:none;
}
#chat .mes > .mes_block::after {content:none;}
#chat .mes .ch_name {background-image:none;}
'''
(R/'theme/ink-letter-seam.css').write_text(s)
d=json.loads((R/'theme/Ink-Letter-Aligned.json').read_text());d['name']='墨羽来信·完整拼接版';d['custom_css']=s.replace('../assets/ink-aligned-v2/','https://raw.githubusercontent.com/Lumi729/wuli-laixin/ink-aligned-v2/assets/ink-aligned-v2/').replace('../assets/ink-seam-v3/','https://raw.githubusercontent.com/Lumi729/wuli-laixin/ink-seam-v3/assets/ink-seam-v3/')
(R/'theme/Ink-Letter-Seam.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
