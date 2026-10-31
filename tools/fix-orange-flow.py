from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
j=json.loads((R/'theme/Orange-Soda-CSS-Only.json').read_text())
s=j['custom_css']
s+='''
/* Ordinary-message repair: content and controls participate in normal flow. */
#chat>.mes[is_user]{display:block!important;min-height:0!important;height:auto!important;padding:14px 5% 38px!important;margin:0 0 12px!important;background:var(--paper) url('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/assets/editorial-faithful/orange/paper.webp') left top/256px auto repeat!important;border-bottom:1px solid #c3b694!important;box-sizing:border-box!important}
#chat>.mes[is_user]>.mes_block{display:block!important;position:relative!important;width:100%!important;max-width:100%!important;min-width:0!important;padding:0!important;margin:0!important;overflow:visible!important;box-sizing:border-box!important}
#chat>.mes[is_user]>.mes_block>.ch_name{position:relative!important;display:flex!important;flex-wrap:wrap!important;align-items:center!important;gap:8px!important;height:auto!important;min-height:30px!important;width:100%!important;margin:0 0 12px!important;padding:0!important;pointer-events:auto!important}
#chat>.mes[is_user]>.mes_block>.ch_name>.flex1{position:static!important;inset:auto!important;width:auto!important;min-width:0!important;flex:1 1 auto!important}
#chat>.mes[is_user] .timestamp{margin:0 0 0 8px!important}
#chat>.mes[is_user]>.mes_block>.ch_name>.mes_buttons{position:static!important;inset:auto!important;flex:0 1 auto!important;display:flex;flex-direction:row!important;flex-wrap:wrap!important;align-items:center!important;width:auto!important;max-width:100%!important;height:auto!important;gap:8px!important;margin:0!important;padding:0!important}
#chat>.mes[is_user] .extraMesButtons{position:static!important;inset:auto!important;max-width:100%!important;width:auto!important;transform:none!important;flex-wrap:wrap!important}
#chat>.mes[is_user] .mes_button{min-width:26px!important;min-height:26px!important;font-size:16px!important;line-height:26px!important}
#chat>.mes[is_user]>.mes_block>.mes_text{position:relative!important;display:block!important;grid-area:auto!important;width:100%!important;min-width:0!important;max-width:100%!important;min-height:0!important;height:auto!important;margin:0!important;padding:0!important;font-size:clamp(16px,2.6vw,26px)!important;line-height:1.8!important;box-sizing:border-box!important;overflow-wrap:anywhere!important}
#chat>.mes[is_user]>.mes_block>.mes_reasoning_details{position:relative!important;inset:auto!important;grid-area:auto!important;display:block;width:100%!important;max-width:100%!important;max-height:40dvh!important;overflow:auto!important;margin:12px 0!important;padding:12px!important;background:#e0e7cb!important;border:1px solid #a4b18b!important;box-sizing:border-box!important}
#chat>.mes[is_user]:not(.reasoning)>.mes_block>.mes_reasoning_details,#chat>.mes[is_user]>.mes_block>.mes_reasoning_details:not([data-has-content="true"]):not(:has(.reasoning_edit_textarea)){display:none!important}
#chat>.mes[is_user]>.mesAvatarWrapper{position:relative!important;inset:auto!important;display:flex!important;align-items:center!important;flex-wrap:wrap!important;gap:10px!important;width:100%!important;height:auto!important;margin:0 0 10px!important;padding:0!important}
#chat>.mes[is_user]>.mesAvatarWrapper>.avatar{position:relative!important;inset:auto!important;width:44px!important;height:44px!important;flex:0 0 44px!important;border-radius:50%!important}
#chat>.mes[is_user]>.mesAvatarWrapper>:is(.mesIDDisplay,.mes_timer,.tokenCounterDisplay){position:static!important;inset:auto!important;width:auto!important;font-size:12px!important}
#chat>.mes[is_user="true"]{background-color:#f8dfb6!important}
#chat::after{content:none!important}
/* The existing header uses one real avatar, not an empty picture slot. */
#chat>.mes[is_user="false"]:not([is_system="true"]):not(:has(~.mes[is_user="false"]:not([is_system="true"])))>.mesAvatarWrapper{position:fixed!important;top:0!important;left:0!important;right:auto!important;width:100vw!important;height:calc(267 * var(--u))!important;margin:0!important;display:block!important}
#chat>.mes[is_user="false"]:not([is_system="true"]):not(:has(~.mes[is_user="false"]:not([is_system="true"])))>.mesAvatarWrapper>.avatar{position:absolute!important;left:4.4%!important;top:8.6%!important;width:22.9%!important;height:86.5%!important}
'''
j['custom_css']=s;j['name']='橘子汽水·普通消息修复'
(R/'theme/Orange-Message-Fix.json').write_text(json.dumps(j,ensure_ascii=False,indent=2))
(R/'theme/Orange-Message-Fix.css').write_text(s)
