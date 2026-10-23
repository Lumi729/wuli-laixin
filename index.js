import { getContext } from '../../../extensions.js';
const KEY='lumiFloatingDock';
const ctx=getContext();
const defaults={enabled:true,theme:'rose',icon:'',size:64,frameScale:100,itemSize:44,x:0.85,y:0.65,items:[]};
const cfg=ctx.extensionSettings[KEY]??=structuredClone(defaults);
for(const [k,v] of Object.entries(defaults))if(cfg[k]===undefined)cfg[k]=v;
const asset=n=>new URL(`./assets/floating-dock/${n}.png`,import.meta.url).href;
const save=()=>ctx.saveSettingsDebounced();
const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text)n.textContent=text;return n;};
const safeUrl=s=>{if(typeof s!=='string'||!s.trim())return '';try{const u=new URL(s,location.href);return ['https:','http:'].includes(u.protocol)||(u.protocol==='blob:'&&u.origin===location.origin)||/^data:image\/(png|jpeg|webp|gif|avif|svg\+xml)[;,]/i.test(s)?u.href:'';}catch{return '';}};
const find=s=>{try{let scope=document;const parts=s.split(' >>> ');for(let i=0;i<parts.length;i++){const n=scope.querySelector(parts[i]);if(i===parts.length-1)return n;scope=n?.shadowRoot;if(!scope)return null;}}catch{return null;}};
function deepNodes(scope=document){const nodes=[...scope.querySelectorAll('*')];return [...(scope.shadowRoot?deepNodes(scope.shadowRoot):[]),...nodes.flatMap(n=>n.shadowRoot?[n,...deepNodes(n.shadowRoot)]:[n])];}
function floatingAncestor(n){for(let p=n;p&&p!==document.body;p=p.parentElement||p.getRootNode()?.host){const pos=getComputedStyle(p).position;if(pos==='fixed'||(pos==='absolute'&&p.parentElement===document.body))return p;}return null;}
function protectedNode(n){return n.closest('#top-bar,#send_form')||(n.closest('#chat')&&getComputedStyle(n).position!=='fixed');}
const owned=n=>n?.closest?.('#lfd-root,#lfd-settings,#lfd-editor,[data-lfd-entry]');
const root=el('div');root.id='lfd-root';
const toggle=el('button','lfd-toggle');toggle.type='button';toggle.title='浮窗收纳（拖动可移动）';toggle.setAttribute('aria-label','展开浮窗收纳');
const icon=el('img');icon.alt='';toggle.append(icon);
const tray=el('div','lfd-tray');tray.hidden=true;
const frame=el('div','lfd-frame');frame.setAttribute('aria-hidden','true');const frameImages=[];for(const side of ['bridge','left','right']){const half=el('div','lfd-frame-'+side),img=el('img');img.alt='';half.append(img);frame.append(half);frameImages.push(img);}const row=el('div','lfd-row');tray.append(frame,row);root.append(toggle,tray);document.body.append(root);
let opened=false,drag=null,moved=false,picking=false;
const tracked=new Map();
function show(value){if(value)sync();opened=value;tray.hidden=!value;toggle.setAttribute('aria-expanded',String(value));position();}
function position(){
 const size=Math.max(40,Math.min(110,Number(cfg.size)||64)),vw=innerWidth,vh=innerHeight;
 let x=Math.max(4,Math.min(vw-size-4,cfg.x*(vw-size)));const y=Math.max(4,Math.min(vh-size-4,cfg.y*(vh-size)));
 const side=x+size/2<vw/2?'right':'left';
 if(opened){x=side==='right'?4:vw-size-4;}
 const available=Math.max(80,vw-size-16),requested=Math.max(.6,Math.min(1.6,(Number(cfg.frameScale)||100)/100));
 const itemSize=Math.max(20,Math.min(90,Number(cfg.itemSize)||44)),count=Math.max(1,cfg.items.length),itemWidth=itemSize+8,gap=8;
 const scale=Math.min(requested,(vh-8)/184,Math.max(.25,(available-itemWidth)/140));
 const contentWidth=cfg.items.length?count*itemWidth+(count-1)*gap:120;
 const width=Math.min(available,Math.max(260*scale,140*scale+contentWidth+2)),baseWidth=width/scale;
 row.style.overflowX=contentWidth>width-140*scale?'auto':'hidden';
 root.style.setProperty('--lfd-frame-scale',scale);root.style.setProperty('--lfd-frame-base-width',baseWidth+'px');root.style.setProperty('--lfd-item-size',Math.max(20,Math.min(90,Number(cfg.itemSize)||44))+'px');
 root.style.setProperty('--lfd-size',size+'px');root.style.setProperty('--lfd-tray-width',width+'px');root.style.setProperty('--lfd-bridge-scale',String(Math.max(1,(baseWidth-258)/2)));root.dataset.side=side;
 root.style.left=x+'px';root.style.top=Math.max(4,Math.min(vh-size-4,y))+'px';
 tray.style.width=width+'px';tray.style.left=side==='right'?(size+4)+'px':'auto';tray.style.right=side==='left'?(size+4)+'px':'auto';
 const height=184*scale;tray.style.top=Math.max(4-parseFloat(root.style.top),Math.min((size-height)/2,vh-4-parseFloat(root.style.top)-height))+'px';
}
function release(n){const state=tracked.get(n);state?.observer?.disconnect();if(state){if(state.value)n.style.setProperty('display',state.value,state.priority);else n.style.removeProperty('display');}n.classList.remove('lfd-stored');tracked.delete(n);}
function hideOriginal(n){const state={value:n.style.getPropertyValue('display'),priority:n.style.getPropertyPriority('display'),observer:null};const apply=()=>{if(n.style.getPropertyValue('display')!=='none'||n.style.getPropertyPriority('display')!=='important'){state.value=n.style.getPropertyValue('display');state.priority=n.style.getPropertyPriority('display');n.style.setProperty('display','none','important');}};apply();state.observer=new MutationObserver(apply);state.observer.observe(n,{attributes:true,attributeFilter:['style']});n.classList.add('lfd-stored');tracked.set(n,state);}
function restore(){for(const n of [...tracked.keys()])release(n);}
function resolve(item){let n=find(item.selector);if(item.selector.startsWith('#pear-nai-host'))n=document.querySelector('#pear-nai-host')?.shadowRoot?.querySelector('.fab');if(!n||owned(n)||['BODY','HTML'].includes(n.tagName)||protectedNode(n))return null;return n;}
const views=new Map();
function imageUrl(target){
 if(!target)return '';
 const img=target.matches('img')?target:deepNodes(target).find(n=>n.matches('img'));
 for(const image of [img,...deepNodes(target).filter(n=>n.matches('img'))].filter(Boolean)){const direct=safeUrl(image.currentSrc||image.getAttribute('src'));if(direct)return direct;}
 const nodes=[target,...deepNodes(target)].slice(0,80);
 for(const node of nodes)for(const pseudo of [null,'::before','::after']){
  const style=getComputedStyle(node,pseudo);for(const value of [style.backgroundImage,style.content]){const match=value?.match(/url\(["']?(.*?)["']?\)/);if(match&&safeUrl(match[1]))return safeUrl(match[1]);}
 }
 const svg=nodes.find(n=>n.matches('svg'));if(svg){const copy=svg.cloneNode(true);copy.setAttribute('xmlns','http://www.w3.org/2000/svg');for(const n of [copy,...copy.querySelectorAll('*')]){for(const a of [...n.attributes])if(a.name.startsWith('on'))n.removeAttribute(a.name);}copy.querySelectorAll('script,foreignObject').forEach(n=>n.remove());return 'data:image/svg+xml;charset=utf-8,'+encodeURIComponent(new XMLSerializer().serializeToString(copy));}
 return '';
}
function maskVisual(target){if(!target)return null;for(const node of [target,...deepNodes(target)].slice(0,80)){for(const pseudo of [null,'::before','::after']){const cs=getComputedStyle(node,pseudo),mask=cs.maskImage||cs.webkitMaskImage||cs.getPropertyValue('-webkit-mask-image');if(mask&&mask!=='none'&&mask.includes('url('))return {mask,color:cs.backgroundColor&&cs.backgroundColor!=='rgba(0, 0, 0, 0)'?cs.backgroundColor:cs.color};}}return null;}
function updateVisual(view,item,target){
 const custom=safeUrl(item.icon),mask=custom?null:maskVisual(target);const src=custom||imageUrl(target)||safeUrl(item.originalIcon);
 const symbol=target?.querySelector('i[class*="fa-"],span[class*="fa-"]');
 const signature=(mask?'mask:'+mask.mask+':'+mask.color:'')||src||symbol?.className||target?.textContent?.trim().slice(0,3)||item.name?.slice(0,1)||'◇';
 if(view.signature===signature)return;view.signature=signature;view.visual.replaceChildren();
 if(mask){const art=el('span');art.style.cssText='display:block;width:100%;height:100%;flex:none;';art.style.backgroundColor=mask.color;art.style.maskImage=art.style.webkitMaskImage=mask.mask;art.style.maskSize=art.style.webkitMaskSize='contain';art.style.maskRepeat=art.style.webkitMaskRepeat='no-repeat';art.style.maskPosition=art.style.webkitMaskPosition='center';view.visual.append(art);}
 else if(src){const img=el('img');img.alt='';const source=target?.matches('img')?target:target&&deepNodes(target).find(n=>n.matches('img'));img.referrerPolicy=source?.referrerPolicy||'no-referrer';img.src=src;img.onerror=()=>{img.remove();view.visual.textContent=item.name?.slice(0,1)||'◇';};view.visual.append(img);}
 else if(symbol){const i=el('i',symbol.className);view.visual.append(i);}
 else view.visual.textContent=signature;
}
let pearScope=null,pearObserver=null;
function watchPear(){const scope=document.querySelector('#pear-nai-host')?.shadowRoot;if(scope===pearScope)return;pearObserver?.disconnect();pearScope=scope;if(scope){pearObserver=new MutationObserver(()=>{if(!timer)timer=setTimeout(()=>{timer=null;sync();},250);});pearObserver.observe(scope,{childList:true,subtree:true,attributes:true,attributeFilter:['src']});}}
function sync(){
 watchPear();
 root.hidden=!cfg.enabled;root.dataset.theme=cfg.theme==='lily'?'lily':'rose';const frameSrc=asset(root.dataset.theme+'-frame');for(const img of frameImages)if(img.getAttribute('src')!==frameSrc)img.src=frameSrc;
 const src=safeUrl(cfg.icon)||asset(root.dataset.theme+'-launcher');if(icon.getAttribute('src')!==src){icon.src=src;icon.onerror=()=>{icon.onerror=null;const fallback=asset(root.dataset.theme+'-launcher');if(icon.src!==fallback)icon.src=fallback;};}
 const targets=new Set();const keys=new Set();
 for(const item of cfg.items){const target=resolve(item);if(cfg.enabled&&target)targets.add(target);keys.add(item.selector);
 let v=views.get(item.selector);if(!v){const b=el('button','lfd-item');b.type='button';const visual=el('span','lfd-visual'),name=el('span','lfd-name');b.append(visual,name);v={b,visual,name,signature:null};views.set(item.selector,v);}
 v.b.disabled=!target;v.b.title=target?item.name:item.name+'（当前未找到）';if(v.name.textContent!==item.name)v.name.textContent=item.name;
 v.name.hidden=!item.name?.trim();v.b.setAttribute('aria-label',item.name?.trim()||label(target||v.b)||'悬浮按钮');
 updateVisual(v,item,target);v.b.onclick=()=>{const t=resolve(item);if(t){show(false);t.click();}};
 }
 for(const n of tracked.keys())if(!targets.has(n)){release(n);}
 for(const n of targets)if(!tracked.has(n)){const scope=n.getRootNode();if(scope.host&&!scope.querySelector('style[data-lfd-hide]')){const style=el('style');style.dataset.lfdHide='true';style.textContent='.lfd-stored,.lfd-stored *{visibility:hidden!important;pointer-events:none!important}';scope.append(style);}hideOriginal(n);}
 for(const [key,v] of views)if(!keys.has(key)){v.b.remove();views.delete(key);}
 const ordered=cfg.items.map(x=>views.get(x.selector).b);ordered.forEach((node,i)=>{if(row.children[i]!==node)row.insertBefore(node,row.children[i]||null);});
 let empty=row.querySelector('.lfd-empty');if(cfg.items.length){empty?.remove();}else if(!empty){empty=el('span','lfd-empty','请从扩展页或魔法棒打开设置');row.append(empty);}
 position();
}
toggle.onclick=()=>{if(!moved)show(!opened);moved=false;};
toggle.onpointerdown=e=>{if(e.button!==0)return;drag={x:e.clientX,y:e.clientY,left:parseFloat(root.style.left),top:parseFloat(root.style.top)};moved=false;toggle.setPointerCapture(e.pointerId);};
toggle.onpointermove=e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.hypot(dx,dy)>6)moved=true;if(moved){const s=parseFloat(root.style.getPropertyValue('--lfd-size'));cfg.x=Math.max(0,Math.min(1,(drag.left+dx)/Math.max(1,innerWidth-s)));cfg.y=Math.max(0,Math.min(1,(drag.top+dy)/Math.max(1,innerHeight-s)));position();}};
toggle.onpointerup=()=>{if(drag&&moved)save();drag=null;};toggle.onpointercancel=()=>{drag=null;};
window.addEventListener('resize',position);document.addEventListener('pointerdown',e=>{if(!root.contains(e.target))show(false);});
function selector(n){const scope=n.getRootNode();if(scope.host){if(scope.host.id==='pear-nai-host'&&n.matches('.fab'))return '#pear-nai-host >>> .fab';const inner=n.id?'#'+CSS.escape(n.id):localSelector(n,scope);return selector(scope.host)+' >>> '+inner;}if(n.id)return '#'+CSS.escape(n.id);let p=n;const parts=[];while(p&&p!==document.body){if(p.id){parts.unshift('#'+CSS.escape(p.id));break;}const siblings=[...p.parentElement.children].filter(x=>x.tagName===p.tagName);parts.unshift(p.tagName.toLowerCase()+`:nth-of-type(${siblings.indexOf(p)+1})`);p=p.parentElement;}return parts.join(' > ');}
function localSelector(n,scope){const parts=[];for(let p=n;p&&p!==scope;p=p.parentElement){if(p.id){parts.unshift('#'+CSS.escape(p.id));break;}const peers=[...(p.parentNode?.children||[])].filter(x=>x.tagName===p.tagName);parts.unshift(p.tagName.toLowerCase()+`:nth-of-type(${peers.indexOf(p)+1})`);}return parts.join(' > ');}
function label(n){return (n.getAttribute('aria-label')||n.title||n.querySelector('img')?.alt||n.textContent?.trim()||n.id||'悬浮按钮').slice(0,40);}
function add(n){if(n?.id==='pear-nai-host')n=n.shadowRoot?.querySelector('.fab');if(!n||owned(n)||protectedNode(n)||['HTML','BODY'].includes(n.tagName))return;const s=selector(n);if(!cfg.items.some(x=>x.selector===s)){cfg.items.push({selector:s,name:label(n),icon:'',originalIcon:imageUrl(n)});save();sync();}}
function candidates(){
 const all=deepNodes(document.documentElement);
 return all.filter(n=>{if(n.id==='pear-nai-host'||owned(n)||(protectedNode(n)||n.closest('dialog,#extensions_settings,#extensions_settings2,#extensionsMenu,.lfd-stored'))||['STYLE','SCRIPT','LINK','IFRAME'].includes(n.tagName))return false;
 const s=getComputedStyle(n),r=n.getBoundingClientRect();if(s.display==='none'||s.visibility==='hidden'||r.width<16||r.width>240||r.height<16||r.height>240||r.right<0||r.bottom<0)return false;
 const anchor=floatingAncestor(n);if(!anchor)return false;const box=anchor.getBoundingClientRect();return s.position==='fixed'||s.position==='absolute'||(box.width>0&&box.width<=260&&box.height>0&&box.height<=260);
 }).filter((n,i,a)=>!a.some(p=>p!==n&&(p.contains(n)||p.contains(n.getRootNode()?.host))));
}
function collectAll(){const list=candidates();for(const n of list){const key=selector(n);if(!cfg.items.some(x=>x.selector===key))cfg.items.push({selector:key,name:label(n),icon:'',originalIcon:imageUrl(n)});}cfg.enabled=true;save();sync();return list.length;}
function startPick(){picking=true;document.body.classList.add('lfd-picking');const tip=el('div','lfd-pick-tip','点击要收纳的悬浮按钮；按 Esc 或点这里取消');tip.id='lfd-pick-tip';document.body.append(tip);const done=()=>{picking=false;tip.remove();document.body.classList.remove('lfd-picking');document.removeEventListener('click',pick,true);document.removeEventListener('keydown',key);};const key=e=>{if(e.key==='Escape')done();};const pick=e=>{e.preventDefault();e.stopImmediatePropagation();if(e.target===tip){done();return;}const hit=e.composedPath()[0];let n=hit.closest('button,[role="button"],a')||hit;let p=n;while(p&&p!==document.body){const r=p.getBoundingClientRect();if(getComputedStyle(p).position==='fixed'&&r.width<=160&&r.height<=160){n=p;break;}p=p.parentElement;}const r=n.getBoundingClientRect();if(r.width>260||r.height>260||owned(n)){done();return;}done();add(n);openEditor();};setTimeout(()=>{document.addEventListener('click',pick,true);document.addEventListener('keydown',key);},0);tip.onclick=done;document.addEventListener('keydown',key);}
function input(label,value,change,type='text'){const wrap=el('label','lfd-field',label);const n=el('input');n.type=type;n.value=value;n.onchange=()=>change(n.value);wrap.append(n);return wrap;}
function button(text,fn){const b=el('button','menu_button',text);b.type='button';b.onclick=fn;return b;}
function openEditor(){document.querySelector('#lfd-editor')?.remove();const d=el('dialog');d.id='lfd-editor';const title=el('h3','','浮窗收纳');d.append(title);const close=button('完成',()=>d.close());d.append(close);d.addEventListener('close',()=>d.remove());
const enabled=el('label','lfd-field','启用收纳');const cb=el('input');cb.type='checkbox';cb.checked=cfg.enabled;cb.onchange=()=>{cfg.enabled=cb.checked;save();sync();};enabled.append(cb);d.append(enabled);
const themes=el('select');for(const [v,t] of [['rose','玫瑰月相'],['lily','百合羽信']]){const o=el('option','',t);o.value=v;themes.append(o);}themes.value=cfg.theme;themes.onchange=()=>{cfg.theme=themes.value;save();sync();};d.append(themes,input('入口图片链接（留空使用内置）',cfg.icon,v=>{cfg.icon=v;save();sync();}),input('入口大小（40–110）',cfg.size,v=>{cfg.size=Math.max(40,Math.min(110,Number(v)||64));save();sync();},'number'));
d.append(input('装饰框等比大小（60–160%，超出屏幕时自动适配）',cfg.frameScale,v=>{cfg.frameScale=Math.max(60,Math.min(160,Number(v)||100));save();sync();},'number'),input('收纳图标大小（20–90）',cfg.itemSize,v=>{cfg.itemSize=Math.max(20,Math.min(90,Number(v)||44));save();sync();},'number'));
d.append(button('点选一个悬浮按钮',()=>{d.close();startPick();}),button('一键扫描并全部收纳',()=>{collectAll();openEditor();}));
for(const [i,item] of cfg.items.entries()){const box=el('div','lfd-entry');box.append(input('名字',item.name,v=>{item.name=v;save();sync();}),input('图案链接（留空沿用原图）',item.icon,v=>{item.icon=v;save();sync();}),input('按钮定位（高级）',item.selector,v=>{item.selector=v;save();sync();}));box.append(button('前移',()=>{if(i){[cfg.items[i-1],cfg.items[i]]=[cfg.items[i],cfg.items[i-1]];save();sync();openEditor();}}),button('移出',()=>{cfg.items.splice(i,1);save();sync();openEditor();}));d.append(box);}
d.append(button('恢复全部原按钮',()=>{cfg.enabled=false;save();sync();openEditor();}));document.body.append(d);d.showModal();}
function mountEntries(){
 const host=document.querySelector('#extensions_settings2')||document.querySelector('#extensions_settings');
 if(host&&!document.querySelector('#lfd-settings')){const settings=el('div');settings.id='lfd-settings';settings.className='extension-settings';const drawer=el('div','inline-drawer'),header=el('div','inline-drawer-toggle inline-drawer-header'),content=el('div','inline-drawer-content');header.append(el('b','','浮窗收纳'),el('div','inline-drawer-icon fa-solid fa-circle-chevron-down'));content.append(button('打开收纳设置',openEditor));drawer.append(header,content);settings.append(drawer);host.append(settings);}
 const menu=document.querySelector('#extensionsMenu');if(menu&&!menu.querySelector('[data-lfd-entry="wand"]')){const b=el('div','list-group-item flex-container flexGap5 interactable');b.dataset.lfdEntry='wand';b.tabIndex=0;b.setAttribute('role','button');b.append(el('i','fa-solid fa-box-archive'),el('span','','浮窗收纳'));b.onclick=()=>{document.querySelector('#extensionsMenuButton')?.click();openEditor();};b.onkeydown=e=>{if(e.key==='Enter'||e.key===' ')b.click();};menu.append(b);}
 const qrList=document.querySelector('#qr-list-left');
 if(qrList&&!qrList.querySelector('[data-lfd-entry="qr-menu"]')){const b=button('浮窗收纳设置',openEditor);b.className='action-item';b.dataset.lfdEntry='qr-menu';b.replaceChildren(el('span','','浮窗收纳设置'));qrList.append(b);}
 // QR helper canvas variants: attach beside its preset control without moving other UI.
 const preset=[...document.querySelectorAll('button,.menu_button')].find(n=>!owned(n)&&n.textContent.trim()==='画布预设设置');
 if(preset?.parentElement&&!preset.parentElement.querySelector('[data-lfd-entry="qr"]')){const b=button('浮窗收纳',openEditor);b.dataset.lfdEntry='qr';preset.parentElement.append(b);}
}
let qrBusy=false,qrReady=false;
async function installQr(){const api=globalThis.quickReplyApi;if(qrReady||qrBusy||!api||!ctx.SlashCommandParser||!ctx.SlashCommand)return;qrBusy=true;
 try{if(!globalThis.__lumiDockCommand){ctx.SlashCommandParser.addCommandObject(ctx.SlashCommand.fromProps({name:'floating-dock',callback:()=>{openEditor();return '';},helpString:'打开浮窗收纳设置'}));globalThis.__lumiDockCommand=true;}
 const name='浮窗收纳';if(!api.getSetByName(name))await api.createSet(name);
 if(!api.getQrByLabel(name,'浮窗收纳'))api.createQuickReply(name,'浮窗收纳',{message:'/floating-dock',showLabel:true,title:'打开浮窗收纳设置'});
 if(!api.listGlobalSets().includes(name))api.addGlobalSet(name,true);qrReady=true;
 }catch(e){console.warn('[浮窗收纳] QR入口暂未就绪',e);}finally{qrBusy=false;}}
let timer;
new MutationObserver(records=>{
 if(picking||records.every(r=>owned(r.target)))return;
 const needsSync=records.some(r=>r.target.nodeType===1&&r.target.matches('style')||r.target.parentElement?.matches('style'))||records.some(r=>[...r.addedNodes,...r.removedNodes].some(n=>n.nodeType===1&&!owned(n)))||records.some(r=>r.type==='attributes'&&cfg.items.some(i=>{const t=resolve(i);return t&&(t===r.target||t.contains(r.target)||r.target.contains?.(t));}));
 if(!needsSync)return;if(timer)return;timer=setTimeout(()=>{timer=null;mountEntries();installQr();sync();},250);
}).observe(document.documentElement,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['src','style','class','data-art']});
mountEntries();installQr();sync();
