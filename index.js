import { getContext } from '../../../extensions.js';
const KEY='lumiFloatingDock';
const ctx=getContext();
const defaults={enabled:true,theme:'rose',icon:'',size:64,x:0.85,y:0.65,items:[]};
const cfg=ctx.extensionSettings[KEY]??=structuredClone(defaults);
for(const [k,v] of Object.entries(defaults))if(cfg[k]===undefined)cfg[k]=v;
const asset=n=>new URL(`./assets/floating-dock/${n}.png`,import.meta.url).href;
const save=()=>ctx.saveSettingsDebounced();
const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text)n.textContent=text;return n;};
const safeUrl=s=>{try{const u=new URL(s,location.href);return ['https:','http:'].includes(u.protocol)||/^data:image\/(png|jpeg|webp|gif);base64,/.test(s)?u.href:'';}catch{return '';}};
const find=s=>{try{return document.querySelector(s);}catch{return null;}};
const owned=n=>n?.closest?.('#lfd-root,#lfd-settings,#lfd-editor');
const root=el('div');root.id='lfd-root';
const toggle=el('button','lfd-toggle');toggle.type='button';toggle.title='浮窗收纳（拖动可移动）';toggle.setAttribute('aria-label','展开浮窗收纳');
const icon=el('img');icon.alt='';toggle.append(icon);
const tray=el('div','lfd-tray');tray.hidden=true;
const row=el('div','lfd-row');const edit=el('button','lfd-edit','设置');edit.type='button';edit.onclick=()=>openEditor();tray.append(row,edit);root.append(toggle,tray);document.body.append(root);
let opened=false,drag=null,moved=false,picking=false;
const tracked=new Map();
function show(value){opened=value;tray.hidden=!value;toggle.setAttribute('aria-expanded',String(value));position();}
function position(){const size=Math.max(40,Math.min(110,Number(cfg.size)||64));root.style.setProperty('--lfd-size',size+'px');const vw=window.innerWidth,vh=window.innerHeight;root.style.left=Math.max(4,Math.min(vw-size-4,cfg.x*(vw-size)))+'px';root.style.top=Math.max(4,Math.min(vh-size-4,cfg.y*(vh-size)))+'px';tray.style.width=Math.min(580,vw-16)+'px';root.style.setProperty('--lfd-tray-width',Math.min(580,vw-16)+'px');const x=parseFloat(root.style.left);tray.style.left=Math.max(8-x,Math.min(-Math.min(580,vw-16)/2+size/2,vw-8-x-Math.min(580,vw-16)))+'px';tray.classList.toggle('lfd-above',parseFloat(root.style.top)>vh/2);}
function restore(){for(const n of tracked.keys())n.classList.remove('lfd-stored');tracked.clear();}
function resolve(item){const n=find(item.selector);if(!n||owned(n)||['BODY','HTML'].includes(n.tagName)||n.closest('#chat,#top-bar,#send_form'))return null;return n;}
function sync(){restore();root.hidden=!cfg.enabled;root.dataset.theme=cfg.theme==='lily'?'lily':'rose';icon.src=safeUrl(cfg.icon)||asset(root.dataset.theme+'-launcher');icon.onerror=()=>{icon.onerror=null;icon.src=asset(root.dataset.theme+'-launcher');};row.replaceChildren();if(!cfg.enabled)return;
for(const item of cfg.items){const target=resolve(item);if(target){tracked.set(target,item);target.classList.add('lfd-stored');}
const b=el('button','lfd-item');b.type='button';b.disabled=!target;b.title=target?item.name:item.name+'（当前未找到）';const picture=el('img');picture.alt='';picture.src=safeUrl(item.icon)||safeUrl(target?.querySelector('img')?.src)||asset(root.dataset.theme+'-launcher');picture.onerror=()=>{picture.onerror=null;picture.src=asset(root.dataset.theme+'-launcher');};b.append(picture,el('span','',item.name));b.onclick=()=>{const t=resolve(item);if(!t)return;show(false);t.click();};row.append(b);}
if(!cfg.items.length)row.append(el('span','lfd-empty','点“设置”添加悬浮按钮'));position();}
toggle.onclick=()=>{if(!moved)show(!opened);moved=false;};
toggle.onpointerdown=e=>{if(e.button!==0)return;drag={x:e.clientX,y:e.clientY,left:parseFloat(root.style.left),top:parseFloat(root.style.top)};moved=false;toggle.setPointerCapture(e.pointerId);};
toggle.onpointermove=e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.hypot(dx,dy)>6)moved=true;if(moved){const s=parseFloat(root.style.getPropertyValue('--lfd-size'));cfg.x=Math.max(0,Math.min(1,(drag.left+dx)/Math.max(1,innerWidth-s)));cfg.y=Math.max(0,Math.min(1,(drag.top+dy)/Math.max(1,innerHeight-s)));position();}};
toggle.onpointerup=()=>{if(drag&&moved)save();drag=null;};toggle.onpointercancel=()=>{drag=null;};
window.addEventListener('resize',position);document.addEventListener('pointerdown',e=>{if(!root.contains(e.target))show(false);});
function selector(n){if(n.id)return '#'+CSS.escape(n.id);let p=n;const parts=[];while(p&&p!==document.body){if(p.id){parts.unshift('#'+CSS.escape(p.id));break;}const siblings=[...p.parentElement.children].filter(x=>x.tagName===p.tagName);parts.unshift(p.tagName.toLowerCase()+`:nth-of-type(${siblings.indexOf(p)+1})`);p=p.parentElement;}return parts.join(' > ');}
function label(n){return (n.getAttribute('aria-label')||n.title||n.querySelector('img')?.alt||n.textContent?.trim()||n.id||'悬浮按钮').slice(0,40);}
function add(n){if(!n||owned(n)||n.closest('#chat,#top-bar,#send_form')||['HTML','BODY'].includes(n.tagName))return;const s=selector(n);if(!cfg.items.some(x=>x.selector===s)){cfg.items.push({selector:s,name:label(n),icon:''});save();sync();}}
function candidates(){const all=[...document.querySelectorAll('button,[role="button"],div[id],a[id]')];return all.filter(n=>{if(owned(n)||n.closest('#chat,#top-bar,#send_form,dialog,#extensions_settings,#extensions_settings2')||n.classList.contains('lfd-stored'))return false;const s=getComputedStyle(n),r=n.getBoundingClientRect();return s.position==='fixed'&&s.display!=='none'&&s.visibility!=='hidden'&&r.width>=20&&r.width<=160&&r.height>=20&&r.height<=160;}).filter((n,i,a)=>!a.some(p=>p!==n&&p.contains(n)));}
function startPick(){picking=true;document.body.classList.add('lfd-picking');const tip=el('div','lfd-pick-tip','点击要收纳的悬浮按钮；按 Esc 或点这里取消');tip.id='lfd-pick-tip';document.body.append(tip);const done=()=>{picking=false;tip.remove();document.body.classList.remove('lfd-picking');document.removeEventListener('click',pick,true);document.removeEventListener('keydown',key);};const key=e=>{if(e.key==='Escape')done();};const pick=e=>{e.preventDefault();e.stopImmediatePropagation();if(e.target===tip){done();return;}let n=e.target.closest('button,[role="button"],a')||e.target;let p=n;while(p&&p!==document.body){const r=p.getBoundingClientRect();if(getComputedStyle(p).position==='fixed'&&r.width<=160&&r.height<=160){n=p;break;}p=p.parentElement;}const r=n.getBoundingClientRect();if(r.width>180||r.height>180||owned(n)){done();return;}done();add(n);openEditor();};setTimeout(()=>{document.addEventListener('click',pick,true);document.addEventListener('keydown',key);},0);tip.onclick=done;document.addEventListener('keydown',key);}
function input(label,value,change,type='text'){const wrap=el('label','lfd-field',label);const n=el('input');n.type=type;n.value=value;n.onchange=()=>change(n.value);wrap.append(n);return wrap;}
function button(text,fn){const b=el('button','menu_button',text);b.type='button';b.onclick=fn;return b;}
function openEditor(){document.querySelector('#lfd-editor')?.remove();const d=el('dialog');d.id='lfd-editor';const title=el('h3','','浮窗收纳');d.append(title);const close=button('完成',()=>d.close());d.append(close);d.addEventListener('close',()=>d.remove());
const enabled=el('label','lfd-field','启用收纳');const cb=el('input');cb.type='checkbox';cb.checked=cfg.enabled;cb.onchange=()=>{cfg.enabled=cb.checked;save();sync();};enabled.append(cb);d.append(enabled);
const themes=el('select');for(const [v,t] of [['rose','玫瑰月相'],['lily','百合羽信']]){const o=el('option','',t);o.value=v;themes.append(o);}themes.value=cfg.theme;themes.onchange=()=>{cfg.theme=themes.value;save();sync();};d.append(themes,input('入口图片链接（留空使用内置）',cfg.icon,v=>{cfg.icon=v;save();sync();}),input('入口大小（40–110）',cfg.size,v=>{cfg.size=Math.max(40,Math.min(110,Number(v)||64));save();sync();},'number'));
d.append(button('点选一个悬浮按钮',()=>{d.close();startPick();}),button('扫描界面悬浮按钮',()=>{const list=candidates();const area=el('div','lfd-candidates');area.append(el('p','',list.length?'点击需要收纳的按钮：':'未找到固定定位的小按钮，可使用点选收纳。'));for(const n of list)area.append(button(label(n),()=>{add(n);openEditor();}));d.querySelector('.lfd-candidates')?.remove();d.append(area);}));
for(const [i,item] of cfg.items.entries()){const box=el('div','lfd-entry');box.append(input('名字',item.name,v=>{item.name=v||'悬浮按钮';save();sync();}),input('图案链接（留空沿用原图）',item.icon,v=>{item.icon=v;save();sync();}),input('按钮定位（高级）',item.selector,v=>{item.selector=v;save();sync();}));box.append(button('前移',()=>{if(i){[cfg.items[i-1],cfg.items[i]]=[cfg.items[i],cfg.items[i-1]];save();sync();openEditor();}}),button('移出',()=>{cfg.items.splice(i,1);save();sync();openEditor();}));d.append(box);}
d.append(button('恢复全部原按钮',()=>{cfg.enabled=false;save();sync();openEditor();}));document.body.append(d);d.showModal();}
const settings=el('div');settings.id='lfd-settings';settings.append(button('浮窗收纳 · 设置',openEditor));(document.querySelector('#extensions_settings2')||document.querySelector('#extensions_settings')||document.body).append(settings);
let timer;new MutationObserver(records=>{if(picking||records.every(r=>owned(r.target)))return;clearTimeout(timer);timer=setTimeout(sync,350);}).observe(document.body,{childList:true,subtree:true});
sync();
