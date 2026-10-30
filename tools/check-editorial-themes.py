from playwright.sync_api import sync_playwright
from pathlib import Path
import json
import threading,http.server,functools
R=Path(__file__).resolve().parents[1]
http.server.SimpleHTTPRequestHandler.log_message=lambda *args:None
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(R)))
threading.Thread(target=server.serve_forever,daemon=True).start()
res=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox'])
 for key in ['night-log','orange-soda']:
  for w in [360,390,430,800]:
   page=b.new_page(viewport={'width':w,'height':1000},device_scale_factor=1.5)
   def route(r):
    path=R/r.request.url.split('/main/',1)[-1]
    if path.exists():r.fulfill(path=str(path))
    else:r.abort()
   page.route('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/**',route)
   page.goto(f'http://127.0.0.1:{server.server_port}/docs/{key}-fixture.html');page.evaluate('document.fonts.ready');page.wait_for_timeout(200)
   page.screenshot(path=str(R/'docs'/f'{key}-{w}.png'),full_page=True)
   report=page.evaluate('''()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,images:[...document.images].filter(x=>!x.complete||!x.naturalWidth).length,portrait:[...document.querySelectorAll('.avatar')].map(x=>({width:x.clientWidth,height:x.clientHeight})),buttons:[...document.querySelectorAll('.mes_buttons')].map(x=>({x:x.getBoundingClientRect().x,y:x.getBoundingClientRect().y,width:x.getBoundingClientRect().width,height:x.getBoundingClientRect().height}))})''')
   page.locator('.extraMesButtonsHint').first.click();report['expanded']=page.locator('.extraMesButtons').first.is_visible()
   page.locator('.extraMesButtonsHint').first.click();page.locator('.mes_reasoning_summary').first.click();report['reasoningClosed']=page.locator('.mes_reasoning_details').first.get_attribute('open') is None
   page.locator('.mes_text').first.evaluate('(e)=>e.innerHTML="<p>这是一段用于检查长消息的文字，花饰保持原始比例。</p>".repeat(30)')
   report['longScroll']=page.evaluate('document.documentElement.scrollWidth');report['theme']=key;res.append(report)
   page.close()
 b.close()
(R/'docs/editorial-validation.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
print(json.dumps(res,ensure_ascii=False,indent=2))
