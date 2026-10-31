# 档案 / 橘子 · 纯 CSS 修复版

直接导入 Night-Log-CSS-Only.json 或 Orange-Soda-CSS-Only.json。无需更新、安装或启用任何新扩展。旧 Faithful 版本不要继续使用。新主题设定 --ed-layout:none，会停用旧布局适配层；不影响浮窗收纳其他功能。

全部图片保持外链，装饰图片等比缩放；主题没有脚本或内嵌 Base64。人物栏使用最后一条角色消息的原生头像、名字和计数，不复制消息 DOM。夜航的三段照片效果由同一原生头像和分隔线构成，不能呈现预览中同一人物的三张不同照片。

修复：顶栏背景与按钮栏按两个独立元素定位；输入框适配真实 nonQRFormItems/leftSendForm/rightSendForm；保留原生按钮显示条件；思考区域滚动；编辑区域回归正常文档流；原生 swipeRightBlock 放在消息尾部；设置抽屉不会盖住顶栏开关。

检查使用 SillyTavern release 的真实 HTML 模板、style.css 和 mobile-styles.css，在 Chromium 的 390×844 和 1024×1536 视口完成。无新增扩展：顶栏点击、输入、发送点击命中、长消息滚动到底、无横向溢出通过。交互使用测试处理器验证命中位置，没有调用真实 API；未覆盖用户全部第三方插件。实际聊天内容及字体换行会不同，不能称为逐像素相同。
