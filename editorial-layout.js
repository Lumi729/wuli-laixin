/* Opt-in layout adapter for the two illustrated editorial themes.
 * No images in script, no polling, no moving native controls or messages.
 * Header is a read-only projection; live text remains in the native message DOM.
 */
(() => {
 if (window.__wuliEditorialLayout) return;
 window.__wuliEditorialLayout = true;
 let mode='', root=null, timer=0, chat=null, observer=null;
 const txt=(node,value)=>{if(node && node.textContent!==value)node.textContent=value};
 const setimg=(node,src)=>{if(node && node.getAttribute('src')!==src){if(src)node.setAttribute('src',src);else node.removeAttribute('src')}};
 function make(){
  root=document.createElement('div');root.id='ed-chrome';root.setAttribute('aria-label','主题人物栏');
  root.innerHTML=`<aside class="ed-sidebar"><div class="ed-photo-strip"><img alt="角色头像"><img alt=""><img alt=""></div><div class="ed-tabs"><span>档案</span><span>回忆</span><span>关系</span><span>语调</span><span>世界观</span></div><div class="ed-profile"><strong class="ed-name"></strong><p>「海会记得，<br>我说过的话。」</p><div class="ed-stat"><b data-field="id"></b><small>对话条目</small></div><div class="ed-stat"><b data-field="timer"></b><small>回复用时</small></div><div class="ed-stat"><b data-field="tokens"></b><small>TOKENS</small></div></div><details class="ed-reason" open><summary>思绪 <small>REASONING</small></summary><div class="ed-reason-text"></div></details></aside><header class="ed-masthead"><div class="ed-brand">NIGHT LOG<br><span>夜航档案</span></div><p class="ed-motto">漂泊的人<br>也会在某处<br>被记住。</p><div class="ed-orange-profile"><img class="ed-header-avatar" alt="当前角色头像"><strong class="ed-name"></strong><p>和你一起，在不完美的日常里，<br>喝一口橘子汽水。</p><div class="ed-header-stats"><span data-field="id"></span><span data-field="timer"></span><span data-field="tokens"></span></div></div></header>`;
  document.querySelector('#sheld').prepend(root);
  const openAvatar=()=>Array.from(document.querySelectorAll('#chat .mes[is_user="false"]')).filter(m=>m.getAttribute('is_system')!=='true').at(-1)?.querySelector('.avatar img')?.click();
  root.querySelectorAll('img').forEach(img=>{img.tabIndex=0;img.setAttribute('role','button');img.onclick=openAvatar;img.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openAvatar()}}});
 }
 function sync(){
  const next=getComputedStyle(document.documentElement).getPropertyValue('--ed-layout').trim().replace(/["']/g,'');
  const active=['night','orange'].includes(next)?next:'';
  if(active!==mode){mode=active;document.body.removeAttribute('data-ed-layout');if(root){root.remove();root=null}}
  if(!mode){if(observer){observer.disconnect();observer=null;chat=null}return}
  const shell=document.querySelector('#sheld'),c=document.querySelector('#chat');if(!shell||!c)return;
  if(!root||!root.isConnected)make();
  if(document.body.dataset.edLayout!==mode)document.body.dataset.edLayout=mode;
  if(chat!==c){observer?.disconnect();chat=c;observer=new MutationObserver(schedule);observer.observe(c,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['src','is_user','ch_name']})}
  const messages=Array.from(c.querySelectorAll('.mes[is_user="false"]')).filter(m=>m.getAttribute('is_system')!=='true');
  const m=messages.at(-1),name=m?.querySelector('.name_text')?.textContent?.trim()||'等待角色';
  const src=m?.querySelector('.avatar img')?.getAttribute('src')||'';
  root.querySelectorAll('.ed-name').forEach(n=>txt(n,name));root.querySelectorAll('img').forEach(n=>setimg(n,src));
  for(const [field,sel] of [['id','.mesIDDisplay'],['timer','.mes_timer'],['tokens','.tokenCounterDisplay']]){
   const val=m?.querySelector(sel)?.textContent?.trim()||'';
   root.querySelectorAll(`[data-field="${field}"]`).forEach(n=>{txt(n,val);(n.closest('.ed-stat')||n).classList.toggle('ed-empty',!val)});
  }
  const reasoning=m?.querySelector('.mes_reasoning')?.textContent?.trim()||'';
  txt(root.querySelector('.ed-reason-text'),reasoning||'此条消息没有可显示的思考内容。');
 }
 function schedule(){clearTimeout(timer);timer=setTimeout(sync,120)}
 // Watch styles, including installations that place customCSS outside head.
 new MutationObserver(schedule).observe(document.head,{childList:true,subtree:true,characterData:true});
 const customStyle=document.getElementById('customCSS');
 if(customStyle && !document.head.contains(customStyle))new MutationObserver(schedule).observe(customStyle,{childList:true,subtree:true,characterData:true});
 window.addEventListener('load',schedule,{once:true});document.addEventListener('change',schedule);
 sync();
})();
