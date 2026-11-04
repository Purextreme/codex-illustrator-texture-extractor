# Codex Illustrator Texture Extractor

这是一个面向 Codex 的 Adobe Illustrator 自动化 Skill。它通过 Windows COM 连接已打开的 Illustrator，再由 JSX 在 Illustrator 内部检查对象、复制矢量并导出适合 3D 模型使用的透明 PNG 贴图，无需安装 CEP 面板或 Illustrator 插件。

## 使用场景

- 从菲林图、丝印图或 CMF 工艺图中提取产品表面图案。
- 提取 Logo、无线充电环、接口文字、认证标志、法规文字、镭雕和丝印。
- 默认按“一个产品表面一张贴图”导出，保留同一表面上所有图案的比例、间距和定位。
- 排除产品结构线、尺寸线、箭头、中心线、工艺注释、标题栏和参考图。
- 从 Illustrator 矢量直接栅格化到指定分辨率，例如长边 2560 像素，并保留 Alpha。

## 工作方式

1. 导出整页预览，配合视觉判断产品表面和实际贴图内容。
2. 读取 Illustrator 对象清单，用位置、层级、边界和绘制属性对应预览区域。
3. 使用产品结构轮廓确定透明画布范围，但不把轮廓复制到贴图。
4. 将同一产品表面的所有图案复制到临时 RGB 文档，并映射回整面坐标。
5. 通过 PNG24 透明导出，从矢量直接生成目标分辨率。
6. 检查尺寸、Alpha、内容边界、方向、分组和视觉完整性。

## 目录结构

```text
.
|-- SKILL.md
|-- README.md
|-- LICENSE
|-- requirements.txt
|-- agents/openai.yaml
|-- improvements/
|   |-- RULES.md
|   `-- pending/
|-- references/workflow.md
`-- scripts/
    |-- illustrator_com_runner.vbs
    |-- inspect_png_alpha.py
    `-- make_contact_sheet.py
```

## 安装

将仓库直接克隆到本机 Codex Skills 目录。若该位置已有手动安装的副本，先将它移到别处备份。

```powershell
$skillPath = Join-Path $env:USERPROFILE '.codex\skills\illustrator-texture-extractor'
git clone https://github.com/Purextreme/codex-illustrator-texture-extractor.git $skillPath
```

重启 Codex 后即可自动发现，也可以显式调用：

```text
使用 $illustrator-texture-extractor，从当前 Illustrator 文档提取全部产品表面贴图，透明 PNG，长边 2560。
```

## 维护

已安装的 Skill 目录就是 Git 工作区。直接在这里编辑和提交，提交后推送到 GitHub。

```powershell
git -C $skillPath status
git -C $skillPath push origin main
```

## 环境

- Windows
- Adobe Illustrator 2024（默认 COM ProgID 为 `Illustrator.Application.28`，可传入其他 ProgID）
- Windows Script Host `cscript.exe`
- Python 3.10+；PNG 检查和联系表需要 Pillow

安装可选的预览依赖：

```powershell
python -m pip install -r requirements.txt
```

## 安全与限制

- 默认不保存或修改源文档；目标对象复制到临时文档后导出。
- 禁用 Illustrator 外部 JSX 警告是全局偏好更改，只能在用户明确授权后执行。
- COM 429 或 Access denied 通常是 Windows 会话或完整性级别边界，不应据此反复修改 JSX。
- 自动选择依赖语义和视觉判断，不能只靠红色、蓝色或黑色等固定颜色过滤。

## 自改进队列

真实任务中新发现的可复用经验会先写入 `improvements/pending/`，并保留错误、警告或运行产物等证据。候选经验只有经过维护者明确审核后，才能进入正式 Skill 规则或脚本，避免一次性特例污染通用流程。

## License

[MIT](LICENSE)
