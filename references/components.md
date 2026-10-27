# 已复刻的界面 & 怎么加新的

## 现成可用
| 界面 | 在哪 | 复用方式 |
|---|---|---|
| Chrome `chrome://extensions` 扩展程序页（含开发者模式开关、加载按钮、扩展卡片、文件选择器） | `templates/chrome-extension.html` | `new.py` 默认模板，换文案即可 |
| macOS「打开」文件对话框（侧栏 + 面包屑 + 文件列表 + 取消/打开） | 同上，`.finder` 段 | 整段拷走，改文件列表 |
| 通用设置页骨架（开关 / 按钮 / 结果区） | `templates/blank.html` | 起手就改它 |

## 复刻一个新界面的通用做法
1. **量**：拿真实截图，记下关键元素的相对位置、圆角、字号、颜色。别凭印象。
2. **搭壳**：窗口外壳（`.win`）先定死尺寸 —— 横版画布里最舒服的是 `1420×486`，居中留 40px。
3. **分层**：外壳 → 侧栏/工具栏 → 内容区 → 弹层。每层一个 class，别写成一坨。
4. **给可点的东西加 id**：`#devSwitch` `#btnLoad` `#card`。标注只认 id。
5. **状态用 `body[data-step="N"]` 控制**：哪一步显示什么，全写在 CSS 里，JS 只管开关状态（`onState`）。

## 常见系统的复刻要点
- **Chrome 系**：正文 13px，圆角 8~14，主色 `#0b57d0`，开关 40×24，卡片边框 `#dadce0`。
- **macOS 系**：对话框圆角 12，阴影重（`0 34px 90px -24px rgba(0,0,0,.55)`），主按钮蓝色实心、次按钮描边。
- **iOS 系**：列表行高 44，右侧开关用 iOS 绿 `#34c759`，左上返回箭头 + 蓝色文字。
- **网页后台**：侧栏 240~300，表格行高 40~48，主按钮实心品牌色。

## 截图打标路线（界面太复杂时用）
```html
<style>
  .shot{position:absolute;left:40px;top:104px;width:1420px;border-radius:12px;
        box-shadow:0 24px 60px -28px rgba(23,32,51,.30)}
  /* 需要标注的位置，用空 div 盖在图上，坐标按截图实际比例写 */
  .hot{position:absolute;z-index:5}
  #hot1{left:1120px;top:150px;width:80px;height:30px}
</style>
<img class="shot" src="assets/shot.png" />
<div class="hot" id="hot1"></div>
```
`STEPS` 里的 `target` 指 `#hot1` 即可。截图放 `assets/`，宽度先缩到 1420 再存，避免标注坐标对不上。
