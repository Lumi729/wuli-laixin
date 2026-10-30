from pathlib import Path
from playwright.sync_api import sync_playwright
import re,json,http.server,threading,functools
R=Path(__file__).resolve().parents[1]
for key,stem in [('night-log','Night-Log'),('orange-soda','Orange-Soda')]:
 h=(R/'docs'/f'{key}-fixture.html').read_text().replace(f'../theme/{key}.css',f'../theme/{stem}-Faithful.css')
 h=h.replace('</style>',' .mes_buttons img{width:calc(20 * var(--u));height:calc(20 * var(--u));vertical-align:middle}</style>')
 h=h.replace('</main><form','<div id="form_sheld"><form').replace('</form>','</form></div></main>')
 h=h.replace('<script>','<script src="../editorial-layout.js"></script><script>')
 h=h.replace('他将那封信放在你掌心，纸页还带着淡淡的花香。','他将那封信放在你掌心。')
 h=h.replace('<article class="mes"','<article class="mes reasoning"').replace('class="mes_reasoning_details" open','class="mes_reasoning_details" data-has-content="true" open')
 if key=='night-log':
  a=h.index('<article');b=h.index('</article>',a)+10;first=h[a:b];second=first.replace('mesid="12"','mesid="13"').replace('#12','#13')
  second=re.sub(r'<details.*?</details>','',second,flags=re.S)
  second=re.sub(r'<div class="mes_text">.*?</div>', '<div class="mes_text"><p>我知道这样的相遇并不该太过频繁，<br>但总有些话，只在夜里才敢讲。</p><p>那封信里有我尚未说完的答案，<br>也有一些……关于我自己的过去。</p><p>如果你来，我会把一切都告诉你。<br>无论结果如何，<br>至少，在这个夜晚，让我再信任你一次。</p></div>',second,flags=re.S)
  h=h[:b]+second+h[b:]
  # Adapter uses last character message; include its actual reasoning for sidebar.
  secondstart=h.index('mesid="13"');idx=h.index('<div class="mes_text">',secondstart)
  h=h[:idx]+'<details class="mes_reasoning_details" data-has-content="true" open><summary class="mes_reasoning_summary">思绪</summary><div class="mes_reasoning">他并未直接说出心意，而是以留下信件与再次相见的约定，试探你是否愿意继续靠近。语气克制，情感真实，仍在等待你的回应。</div></details>'+h[idx:]
 (R/'docs'/f'{key}-faithful-fixture.html').write_text(h)
http.server.SimpleHTTPRequestHandler.log_message=lambda *args:None
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox'])
 for key in ['night-log','orange-soda']:
  for w,height in [(1024,1536),(390,844),(800,1200)]:
   page=b.new_page(viewport={'width':w,'height':height},device_scale_factor=1)
   def route(r):
    path=R/r.request.url.split('/main/',1)[-1]
    if path.exists():r.fulfill(path=str(path),headers={'Access-Control-Allow-Origin':'*'})
    else:r.abort()
   page.route('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/**',route)
   page.goto(f'http://127.0.0.1:{server.server_port}/docs/{key}-faithful-fixture.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(350)
   page.screenshot(path=str(R/'docs'/f'{key}-faithful-{w}.png'))
   row=page.evaluate('''()=>({mode:document.body.dataset.edLayout,screen:innerWidth,scroll:document.documentElement.scrollWidth,chatWidth:document.querySelector('#chat').clientWidth,chatScroll:document.querySelector('#chat').scrollWidth,name:document.querySelector('#ed-chrome .ed-name').textContent,broken:[...document.images].filter(x=>x.hasAttribute('src')&&(!x.complete||!x.naturalWidth)).length})''')
   page.locator('.extraMesButtonsHint').first.click();row['moreVisible']=page.locator('.extraMesButtons').first.is_visible();page.locator('.extraMesButtonsHint').first.click()
   # Streaming updates must reach the shared profile without remounting it.
   page.locator('.mes[is_user="false"] .name_text').last.evaluate('(e)=>e.textContent="新角色"');page.wait_for_timeout(250);row['liveName']=page.locator('#ed-chrome .ed-name').first.text_content()=='新角色'
   page.locator('.mes_text').first.evaluate('(e)=>e.innerHTML="<p>长消息测试，素材保持自己的原始比例。</p>".repeat(35)');row['longScroll']=page.locator('#chat').evaluate('(e)=>e.scrollWidth<=e.clientWidth+1')
   page.add_style_tag(content=':root{--ed-layout:none!important}');page.wait_for_timeout(250);row['cleanup']=page.locator('#ed-chrome').count()==0
   row['theme']=key;results.append(row);page.close()
 b.close()
(R/'docs/faithful-validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print(json.dumps(results,ensure_ascii=False,indent=2))
