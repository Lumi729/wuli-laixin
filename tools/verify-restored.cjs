const {chromium}=require('playwright'),fs=require('fs'),path=require('path'),assert=require('assert');
const qaFont=process.env.QA_FONT || path.resolve(__dirname,'../../qa-runtime/Chinese.otf');
const root=path.resolve(__dirname,'..'),base='https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/';
(async()=>{const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH || path.resolve(__dirname,'../../qa-runtime/chromium'),args:['--no-sandbox','--disable-gpu']});const report=[];
for(const theme of ['starry','rabbit','rain','postal'])for(const width of [360,390,800]){
 const page=await browser.newPage({viewport:{width,height:1300},deviceScaleFactor:2}),missing=[];
 await page.route(base+'**',async r=>{const f=path.join(root,r.request().url().slice(base.length));if(!fs.existsSync(f)){missing.push(f);return r.abort();}return r.fulfill({path:f});});
 await page.goto('file://'+root+'/docs/'+theme+'-restored-fixture.html');await page.addStyleTag({content:`@font-face{font-family:QA;src:url('file://${qaFont}')}body,#send_textarea{font-family:QA,serif}`});await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(150);
 const bottom=await page.locator('#send_form').evaluate(e=>e.getBoundingClientRect().bottom);if(width===390)await page.screenshot({path:root+'/docs/'+theme+'-restored-390.png',clip:{x:0,y:0,width,height:Math.ceil(bottom)}});
 assert.equal(missing.length,0);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,theme+' overflow');
 const img=await page.locator('.avatar img').evaluate(e=>({fit:getComputedStyle(e).objectFit,loaded:e.complete&&e.naturalWidth>0}));assert.equal(img.fit,'cover');assert(img.loaded);
 await page.locator('.mes_button').first().click();assert(await page.locator('.extraMesButtons').isVisible());const extra=await page.locator('.extraMesButtons').boundingBox();assert(extra.x>=0&&extra.x+extra.width<=width+1,theme+' expanded actions overflow');
 await page.evaluate(()=>{document.querySelector('.name_text').textContent='裴识渊 · 较长的角色名字';document.querySelector('.mes_text').innerHTML='<p>'+('这是一段用于检查换行和长消息的内容。'.repeat(80))+'</p><pre>'+('long_code_'.repeat(100))+'</pre>';const clone=document.querySelector('.mes').cloneNode(true);clone.setAttribute('is_user','true');document.querySelector('#chat').append(clone)});
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,theme+' long overflow');
 const boxes=await page.locator('.mes').evaluateAll(es=>es.map(e=>{const r=e.getBoundingClientRect();return{top:r.top,bottom:r.bottom}}));assert(boxes[1].top>boxes[0].bottom);
 const collision=await page.locator('.mes').first().evaluate(e=>{const a=e.querySelector('.mesAvatarWrapper').getBoundingClientRect(),n=e.querySelector('.ch_name').getBoundingClientRect(),t=e.querySelector('.mes_text').getBoundingClientRect();return t.top<Math.max(a.bottom,n.bottom)-1});assert(!collision,theme+' text overlap');
 report.push({theme,width,missing,avatar:img,expandedButtons:true,longMessages:true,noHorizontalOverflow:true,noTextOverlap:true});await page.close();}
fs.writeFileSync(root+'/docs/restored-validation.json',JSON.stringify(report,null,2));await browser.close()})();
