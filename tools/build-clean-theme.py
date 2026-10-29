"""Build from Rose Moon Phases; leave its layout and behavior intact."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/'
ART = BASE + 'assets/blue-clean-v1/'
css = (ROOT / 'theme/rose-moon-phases.css').read_text()
mapping = {
    'assets/v1/paper.webp': 'assets/thin-mist/v1/paper.webp',
    'assets/v7/portrait-surround.webp': 'assets/blue-clean-v1/portrait-surround.webp',
    'assets/v6/bottom-left.webp': 'assets/blue-clean-v1/bottom.webp',
    'assets/v6/bottom-right.webp': 'assets/blue-clean-v1/bottom.webp',
    'assets/v1/moon-footer.webp': 'assets/blue-clean-v1/bottom.webp',
    'assets/v5/counter-frame.webp': 'assets/thin-mist-cool/flower-left.webp',
    'assets/v10/name-left.webp': 'assets/blue-clean-v1/name-left.webp',
    'assets/v10/name-right.webp': 'assets/blue-clean-v1/name-right.webp',
    'assets/v1/name-ribbon.webp': 'assets/blue-clean-v1/name-ribbon.webp',
    'assets/v4/bar-frame.webp': 'assets/thin-mist-native/bar-frame.webp',
    'assets/v7/reasoning-ribbon.webp': 'assets/blue-clean-v1/name-ribbon.webp',
    'assets/v11/message-divider.webp': 'assets/thin-mist-cool/message-divider.webp',
    'assets/v9/controls-frame.webp': 'assets/blue-clean-v1/controls-frame.webp',
}
for path in re.findall(r'assets/v\d+/icon-[\w-]+\.webp', css):
    mapping[path] = 'assets/thin-mist-cool/' + Path(path).name
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
#chat .mes::after {{
 background-image:url('{ART}bottom.webp')!important;
 background-size:100% auto!important;
 background-position:center bottom!important;
 background-repeat:no-repeat!important;
}}
#chat .mes .ch_name {{background-size:146px auto!important;}}
@media (min-width:600px) and (orientation:portrait) {{
 #chat .mes .ch_name {{background-size:calc(var(--c) * 146) auto!important;}}
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
/* Native canvas slices: equal x/y scale for corners; straight rails repeat. */
#top-bar::after,#send_form::after {{
 border-image-slice:66 135;
 border-image-width:calc(18px * 22 / 45) 18px!important;
 border-image-repeat:repeat;
}}
@media (min-width:600px) {{
 #top-bar::after,#send_form::after {{border-image-width:calc(20px * 22 / 45) 20px!important;}}
}}
#top-settings-holder .drawer-icon,
#send_form :is(#options_button,#extensionsMenuButton,#mes_impersonate,#mes_continue,#send_but) {{
 background-size:contain!important;
}}
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
assert 'data:image' not in css
assert '--wl-avatar-ratio: 16 / 9' in css
print(f'Theme: {len(css.encode()):,} CSS bytes; {len(urls)} distinct external assets')
print(f'Assets: {sum((ROOT / u.removeprefix(BASE)).stat().st_size for u in urls):,} bytes')
