# 雾里来信

## 冷白银蓝素材修复（2026-10-29）

下载 [Blue-Clean.json](https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/theme/Blue-Clean.json) 导入酒馆主题。先备份旧主题，再替换同名主题；不要把新 CSS 追加到旧 CSS 后。

沿用玫瑰月相的布局与 16:9 头像尺寸，使用冷白银蓝透明素材。清理底框花枝和缎带缝隙中的灰底，修正头像下角绘制位置，花饰按自然比例显示。图片保持外链，不嵌入主题。

[布局预览](docs/blue-clean-preview.webp) · [底框白底/深色底检查](docs/blue-clean-bottom-check.webp) · [修改与验证说明](docs/blue-clean-notes.md)

以下为原版本说明。

淡粉白、细线玫瑰与月相的 SillyTavern 主题。角色和用户使用相同的大头像卡片结构。

## 导入

下载 [Wuli-Laixin.json](https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/theme/Wuli-Laixin.json)，在酒馆的用户设置 → 主题中导入。主题名固定为「雾里来信」。如果提示同名主题已存在，请先导出备份旧主题，再删除旧的同名主题后导入。

请用此文件替换旧主题，不要把新 CSS 追加在旧 CSS 后面。图片通过本仓库外链加载，首次打开需要能访问 raw.githubusercontent.com。

## 文件

- `theme/Wuli-Laixin.json`：可直接导入的主题。
- `theme/wuli-laixin.css`：便于修改的 CSS 源文件，使用相对路径。
- `assets/v1/`：独立按钮与纸面背景。
- `assets/v2/`：独立头像框、玫瑰、月相、姓名缎带、月牙挂坠与底部花饰。
- `docs/modules.html`：各独立装饰的查看页。
- `assets/v2/manifest.json`：本版装饰的尺寸与透明通道记录。
- `docs/preview.webp`、`docs/long-message.webp`：使用原生消息 DOM 和样例文本渲染的预览，非手机实机截图。

## 布局与性能

花饰不随正文拉伸；连续细边框负责延长；月牙珠链只在上方短垂，不沿正文重复。底部装饰定位于整条消息底部，包含正文后插入的插件按钮。三个原生计数保持一行，不伪造缺失的计时。头像不设置 object-fit、object-position 或 transform，保留裁剪插件控制。

本版没有内嵌 Base64 图片、JavaScript、动画或背景模糊。图像可由浏览器缓存，同一装饰重复使用同一个链接。外链及压缩不能保证解决插件或聊天内容导致的所有卡顿。

已在 Chromium 的 360、390、430、800 像素宽度样例页检查横向溢出、姓名居中、计数同行及按钮点击；尚未验证用户手机和全部插件组合。

预览头像为此前生成的示意插画，不包含聊天记录或真实用户照片。

当前主题预览随导入文件单独提供；仓库 docs 中的旧预览不代表本次更新。

## 本次调整

头像与透明框分离，花饰与边框分离。移除重复菱形长链，使用独立的短月牙星坠。顶栏图标设置明确的宽高，避免清空字体图标后元素高度塌陷。主题名仍为「雾里来信」。

## 当前修复

上下栏恢复原始花边，使用不带 fill 的 border-image，仅绘制周边，框内不再铺装饰底图。当前聊天装饰改回 v1 原始参考素材，v2 重绘素材保留作历史文件但主题不引用。设置按钮使用修复后的 v3 镜子图标。v4/bar-frame.webp 为单独的透明栏框。
