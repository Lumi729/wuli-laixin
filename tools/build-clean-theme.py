"""Build from Rose Moon Phases; leave its layout and behavior intact."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/'
ART = BASE + 'assets/blue-modular-v2/'
css = (ROOT / 'theme/rose-moon-phases.css').read_text()
mapping = {
    'assets/v1/paper.webp': 'assets/thin-mist/v1/paper.webp',
    'assets/v7/portrait-surround.webp': 'assets/blue-refined-v5/portrait-surround.webp',
    'assets/v6/bottom-left.webp': 'assets/blue-modular-v2/bottom-left.webp',
    'assets/v6/bottom-right.webp': 'assets/blue-modular-v2/bottom-right.webp',
    'assets/v1/moon-footer.webp': 'assets/blue-modular-v2/bottom-center.webp',
    'assets/v5/counter-frame.webp': 'assets/thin-mist-cool/flower-left.webp',
    'assets/v10/name-left.webp': 'assets/blue-refined-v3/name-left.webp',
    'assets/v10/name-right.webp': 'assets/blue-refined-v3/name-right.webp',
    'assets/v1/name-ribbon.webp': 'assets/blue-modular-v2/name-ribbon.webp',
    'assets/v4/bar-frame.webp': 'assets/thin-mist-native/bar-frame.webp',
    'assets/v7/reasoning-ribbon.webp': 'assets/blue-modular-v2/name-ribbon.webp',
    'assets/v11/message-divider.webp': 'assets/blue-redrawn-v4/message-divider.webp',
    'assets/v9/controls-frame.webp': 'assets/blue-modular-v2/controls-frame.webp',
}
for path in re.findall(r'assets/v\d+/icon-[\w-]+\.webp', css):
    mapping[path] = 'assets/blue-redrawn-v4/' + Path(path).name
for old, new in mapping.items():
    css = css.replace(BASE + old, BASE + new)
colors = {
    '#4b3540':'#383f48', '#795560':'#7d91a5', '#fff6f3':'#f3f8ff',
    '#f9e8ed':'#edf5ff', '#b18a94':'#b6c7d9', '#fff1f5':'#f3f8ff',
    '#99717e':'#8b9eb2', '#ad8592':'#8b9eb2', '#fff8fb':'#f8fbff',
    '#956578':'#7898ba', '#fff7f9':'#f4f9ff', '#c28b9e':'#94b1cf',
    '#e5becb':'#d0dfee', '#bb93a3':'#96adc5', '#ffe1ec':'#e4efff',
    'rgba(249,232,237,':'rgba(237,245,255,',
}
for old, new in colors.items():
    css = css.replace(old, new)
css = css.replace('玫瑰月相 · external assets v1.', '薄雾来信 · clean external artwork; Rose Moon Phases layout.')

# These replacements affect artwork painting only, not element geometry.
css += f'''
/* Artwork adaptation only: no avatar, message, button or input resizing. */
/* The replacement has a 20.2/941 top-to-bottom rail offset. Move its paint
   layer only so the lower bends meet the unchanged avatar's lower corners. */
#chat .mes::before {{
 height:calc(100cqw * 594.2 / 941);aspect-ratio:auto;
 background-position:center bottom;
}}
#chat .mes + .mes::before {{
 height:calc(100cqw * 594.2 / 941 + 24px);
 background-position:center bottom,center top;
}}
@media (min-width:600px) and (orientation:portrait) {{
 #chat .mes + .mes::before {{height:calc(100cqw * 594.2 / 941 + var(--c) * 24);}}
}}
#chat .mes .ch_name {{background-size:146px auto!important;}}
#chat .mes .ch_name > .flex1 {{min-height:44px;}}
/* The two sparse vines keep their own natural aspect and connect across the
   existing counter row. Do not collapse or move the counters or avatar. */
#chat .mes > .mes_block::before,#chat .mes > .mes_block::after {{
 top:-27px;aspect-ratio:1091 / 1441;
 mask-image:none;-webkit-mask-image:none;
}}
@media (min-width:600px) and (orientation:portrait) {{
 #chat .mes .ch_name {{background-size:calc(var(--c) * 146) auto!important;}}
 #chat .mes .ch_name > .flex1 {{min-height:calc(var(--c) * 44);}}
 #chat .mes > .mes_block::before,#chat .mes > .mes_block::after {{top:calc(var(--c) * -27);}}
}}
#chat .mes .mes_buttons::before {{
 /* Keep the complete frame proportional, including when more actions open. */
 border:0;border-image:none;
 background:url('{ART}controls-frame.webp') center / contain no-repeat;
}}
/* Counter decorations are separate proportional flowers, not a stretched image. */
#chat .mes > .mesAvatarWrapper::after {{
 background-image:url('{BASE}assets/thin-mist-cool/flower-left.webp'),url('{BASE}assets/thin-mist-cool/flower-right.webp'),linear-gradient(#a4b9cc,#a4b9cc),linear-gradient(#a4b9cc,#a4b9cc);
 background-size:22px auto,22px auto,100% 1px,100% 1px;
 background-position:33.333% center,66.667% center,center top,center bottom;
 background-repeat:no-repeat;
}}
@media (min-width:600px) and (orientation:portrait) {{
 #chat .mes > .mesAvatarWrapper::after {{background-size:calc(var(--c) * 22) auto,calc(var(--c) * 22) auto,100% 1px,100% 1px;}}
}}
/* Four independent square corner modules, with CSS rails between them.
   No full-frame bitmap is squeezed into a toolbar or input rectangle. */
#top-bar::after,#send_form::after {{
 border:0!important;border-image:none!important;
 background-image:url('{ART}corner-tl.webp'),url('{ART}corner-tr.webp'),url('{ART}corner-bl.webp'),url('{ART}corner-br.webp'),linear-gradient(#93a6bb,#93a6bb),linear-gradient(#93a6bb,#93a6bb),linear-gradient(#93a6bb,#93a6bb),linear-gradient(#93a6bb,#93a6bb);
 background-size:18px 18px,18px 18px,18px 18px,18px 18px,calc(100% - 36px) 1px,calc(100% - 36px) 1px,1px calc(100% - 36px),1px calc(100% - 36px);
 background-position:left top,right top,left bottom,right bottom,center 3.6px,center calc(100% - 3.6px),3.4px center,calc(100% - 3.4px) center;
 background-repeat:no-repeat;
}}
#top-settings-holder .drawer-icon {{background-size:24px 24px!important;}}
#send_form :is(#options_button,#extensionsMenuButton,#mes_impersonate,#mes_continue,#send_but) {{
 background-size:26px 26px!important;
}}
@media (min-width:600px) {{
 #top-settings-holder .drawer-icon {{background-size:32px 32px!important;}}
 #send_form :is(#options_button,#extensionsMenuButton,#mes_impersonate,#mes_continue,#send_but) {{background-size:30px 30px!important;}}
}}
'''

# Targeted follow-up corrections from the user's phone screenshot.
css += f'''
/* Continuous visible toolbar outlines, independent of proportional corner art. */
#top-bar::after,#send_form::after {{
 inset:3px!important;border:1px solid #7e92a5!important;border-radius:3px;
 background-image:url('{ART}corner-tl.webp'),url('{ART}corner-tr.webp'),url('{ART}corner-bl.webp'),url('{ART}corner-br.webp');
 background-size:22px 22px;background-position:left top,right top,left bottom,right bottom;
 background-repeat:no-repeat;
}}
/* Muted blue artwork; filter does not change alpha or stretch the icons. */
#top-settings-holder .drawer-icon {{filter:none!important;}}
#send_form :is(#options_button,#extensionsMenuButton,#mes_impersonate,#mes_continue,#send_but) {{filter:none!important;}}
/* Align lettering with the paper face rather than the hanging ribbon tips. */
#chat .mes .ch_name .name_text {{transform:translateY(-4px);}}
/* Larger separator with its own space; preserve both artwork aspect ratios. */
#chat .mes {{margin-bottom:40px!important;}}
#chat .mes + .mes::before {{
 top:-40px;height:calc(100cqw * 594.2 / 941 + 40px);
 background-size:100% auto,auto 36px;
}}
@media (min-width:600px) and (orientation:portrait) {{
 #chat .mes .ch_name .name_text {{transform:translateY(calc(var(--c) * -4));}}
 #chat .mes {{margin-bottom:calc(var(--c) * 40)!important;}}
 #chat .mes + .mes::before {{top:calc(var(--c) * -40);height:calc(100cqw * 594.2 / 941 + var(--c) * 40);background-size:100% auto,auto calc(var(--c) * 36);}}
}}
'''

# Restore the user's floral perimeter, not a replacement plain-line frame.
css += f'''
#top-bar::after,#send_form::after {{
 inset:0!important;border:10px solid transparent!important;border-radius:0;
 background:none!important;
 border-image-source:url('{BASE}assets/thin-mist-native/bar-frame.webp')!important;
 border-image-slice:50 100!important;
 border-image-width:10px 20px!important;
 border-image-outset:0!important;border-image-repeat:stretch!important;
}}
/* Stop counter rails at the avatar bounds; no horizontal protrusions. */
#chat .mes > .mesAvatarWrapper::after {{left:0!important;right:0!important;}}
/* A newly drawn sparse ornament, sized for legibility without distortion. */
#chat .mes + .mes::before {{background-size:100% auto,160px auto;}}
@media (min-width:600px) and (orientation:portrait) {{
 #chat .mes + .mes::before {{background-size:100% auto,calc(var(--c) * 160) auto;}}
}}
'''

# Enlarge only bar ornament/icon paint; keep input and avatar layout intact.
css += '''
#top-bar,#send_form {
 border-color:transparent!important;outline:none!important;box-shadow:none!important;
}
#top-bar::after,#send_form::after {
 inset:-2px 0!important;border-image-width:12px 24px!important;
}
#top-settings-holder .drawer-icon {
 flex-basis:32px!important;width:32px!important;min-width:32px!important;
 background-size:32px 32px!important;
}
#send_form :is(#options_button,#extensionsMenuButton,#mes_impersonate,#mes_continue,#send_but) {
 min-width:32px!important;min-height:32px!important;background-size:32px 32px!important;
}
@media (min-width:600px) {
 #top-settings-holder .drawer-icon {background-size:36px 36px!important;}
 #send_form :is(#options_button,#extensionsMenuButton,#mes_impersonate,#mes_continue,#send_but) {background-size:36px 36px!important;}
}
'''

theme = json.loads((ROOT / 'theme/Rose-Moon-Phases.json').read_text())
cool = json.loads((ROOT / 'theme/Thin-Mist-Cool-Native-Size.json').read_text())
for key in theme:
    if key.endswith('_color'):
        theme[key] = cool[key]
theme['name'] = cool['name']
theme['custom_css'] = css
(ROOT / 'theme/blue-clean.css').write_text(css)
(ROOT / 'theme/Blue-Clean.json').write_text(json.dumps(theme, ensure_ascii=False, indent=2) + '\n')
urls = sorted(set(re.findall(r"url\(['\"]?([^)'\"]+)", css)))
for url in urls:
    assert url.startswith(BASE), url
    assert (ROOT / url.removeprefix(BASE)).is_file(), url
    assert (ROOT / url.removeprefix(BASE)).stat().st_size > 100, url
assert 'data:image' not in css
assert '--wl-avatar-ratio: 16 / 9' in css
print(f'Theme: {len(css.encode()):,} CSS bytes; {len(urls)} distinct external assets')
print(f'Assets: {sum((ROOT / u.removeprefix(BASE)).stat().st_size for u in urls):,} bytes')
