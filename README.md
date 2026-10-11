# PBL 新课程 · 像素风格 Skill

让不同 AI 制作新课程、关卡、徽章、角色和页面时，延续当前已验收的画风

**入口：[SKILL.md](skills/pbl-pixel-course/SKILL.md)** · [视觉预览](skills/pbl-pixel-course/assets/preview.html) · [来源与使用范围](ASSET-SOURCES.md)

包含29张最终参照图、真实寒蝉团圆体与许可、配色/交互CSS、分类生图提示词、课程brief和素材检查脚本。基线为前端仓库17099fe；平台保持北航校园像素风，新课更换课程内部题材

## 使用

支持Skills的AI：把完整 skills/pbl-pixel-course 文件夹放入工具的技能目录，例如项目 .agents/skills/，调用 $pbl-pixel-course

其他AI：把整个文件夹交给它，要求先读SKILL.md及引用文档，并实际查看同类参考图。只给一句“像素风”不足以复现

> 请使用 pbl-pixel-course，为「课程名」制作课程素材与前端
> 先读规范、查看参考图，保持字体、颗粒、面板、按钮和地图交互一致
> 课程主题：___；课时主题：___；需要的素材/页面：___

**不强制GPT生图**。历史记录使用内置image_gen，未记录具体模型版本。其他模型需支持参考图输入，并按相同标准验收；不保证换模型后一键复现。无生图能力的AI应输出素材清单和提示词，不把占位图称为完成

## 预览与检查

直接打开 skills/pbl-pixel-course/assets/preview.html；若浏览器限制本地字体，在仓库目录运行：

    python -m http.server 8123 --bind 127.0.0.1

访问 http://127.0.0.1:8123/skills/pbl-pixel-course/assets/preview.html

检查工具（Python 3.10+）：

    python -m pip install Pillow
    python skills/pbl-pixel-course/scripts/audit_assets.py

检查散列、尺寸、透明通道、字体许可及相对链接，画风仍需看图。新素材用 --candidate 新素材清单.json，格式见skill内模板

本仓库是风格规范包，不含教学数据库、用户上传、公众号照片或教学后端

[本次包验证记录](VALIDATION.md)
