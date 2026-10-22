# 素材说明

透明母版使用内置图像工具从此前确认的空白装饰稿提取；背景纸面单独裁取。随后按原坐标裁成独立图块，保存为带 Alpha 的 WebP。运行时不加载整张母版。

提取提示词：

> Use case: background-extraction. Edit target is this exact UI ornamental artwork. Remove ALL pale pink/white paper backdrop and paper texture throughout the entire image, including inside every frame and empty area. Keep the exact existing black ink fine lines, roses, pink petals and ribbons, moon phases, star chains and borders in their EXACT positions, shapes, colors and scale. Preserve pink fill INSIDE rose petals and the pink name ribbons only. Everything else must become genuine transparent alpha, not white or checkerboard. Do not redesign or rearrange anything. No text, no additional objects. Output same tall aspect ratio, crisp fine dark outlines, no shadows/blur. This transparent master will be sliced into independent ornamental assets.

`rose-top-*` 为上角花饰，`rose-bottom-*` 为下角花饰，`moon-crown` 为顶端月相，`moon-footer` 为底部月亮，`name-ribbon` 为姓名缎带；`pendant-*` 和 `star` 为备用独立挂饰。按钮采用此前生成的清透小图案，每个按钮单独保存。

`star-chain.svg` 是连续重复用的小点与星形链条；`paper.webp` 与 `page-background.webp` 是不透明背景。修改背景不会影响透明花饰，修改头像尺寸也不会拉长花饰。
