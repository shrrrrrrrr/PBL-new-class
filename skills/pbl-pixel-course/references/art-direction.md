# 素材与跨模型提示词

先读[视觉标准](visual-standard.md)，实际附上同类锚点；说明哪些图定义内容、哪些只作风格。API和参数按当前工具使用，以下不绑定供应商

## 所需素材

按实际页面生成课程封面、桌面/手机地图场景、侧栏裁切、阅读标题、实验封面、逐课关卡/徽章，必要时课程标识/角色。平台校园图、字体、机器人及账号头像通常复用

逐课明确一个可辨识主体：理论课机翼剖面/气流/测量台，实践课模型/发射轨/记录设备。新课先列母题，再绑定真实课时，不能同一空间站换名

## 共同风格段

    Use the attached approved PBL artwork as STYLE reference. Keep coarse retro
    16-bit pixel clusters, staircase contours, dark navy outlines, ivory structures,
    cyan highlights and restrained warm gold. Simple silhouettes and 2–3 flat
    shading bands per material. Match apparent pixel size and subject scale at the
    final webpage size. Original reusable asset, not a website screenshot.
    No smooth 3D, photorealism, painterly texture, soft gradients, antialiasing,
    blur, grain filter, thin hairlines or microscopic detail.
    No words, letters, numbers, watermark, logo or UI baked into the artwork.

题材可改变局部颜色；不要求所有物体都奶油/青色。不把某模型seed视为跨模型可复现保证

## 关卡精灵

附level-vr/theory/glider参照，同组固定角度/光源/平台大小

    Asset: one transparent level-platform sprite for [LESSON SUBJECT].
    [COMMON STYLE BLOCK]
    Isometric 3/4 view, one floating platform matching the reference scale,
    upper-left light. Put [ONE DISTINCTIVE TEACHING OBJECT] on the rear half
    with [ONE OR TWO SUPPORTING OBJECTS]. Clear empty front-center landing
    area for a separate character. Entire silhouette within square frame
    with transparent padding. No person, astronaut, avatar, route, label,
    number, question mark, lock, badge or background. Real transparent alpha,
    no fake checkerboard. Bold 64–96 logical-pixel feel at 192–220 CSS pixels.

站位、编号、锁/问号、状态留网页层；未知平台复用level-unknown或中性灰轮廓，不伪造课时

## 场景与封面

以voyage-map/campus-selection为风格参考，内容来自新课程brief

    Asset: full-bleed [LANDSCAPE/PORTRAIT] background for [COURSE THEME].
    [COMMON STYLE BLOCK]
    Scene: [PLACE, 2–3 BIG SUBJECTS, TIME OF DAY]. About 192–320 logical
    pixel-wide game environment enlarged with hard pixel edges.
    Quiet low-detail zones at [CONTENT/ROUTE POSITIONS], decoration near
    edges, responsive cropping space. No level platforms, people, headings,
    controls, routes, progress or text. Match approved palette density
    and perspective language.

地图场景不画多个完整关卡再重复叠精灵；桌面/手机分别构图。阅读标题可合理裁切，不把所有横图拉伸成竖图。平台登录继续北航：桌面右侧留表单，手机中心留表单，不生成校徽或学校文字

## 徽章、角色、机器人

徽章参照badge-vr/theory/glider，共同深蓝章面/金边/奶油青色大符号和留边

    Asset: one small transparent achievement badge for [LESSON SUBJECT].
    [COMMON STYLE BLOCK]
    Match reference outline, rim thickness and center-symbol scale.
    One unmistakable [SUBJECT SYMBOL], navy field, ivory/cyan symbol,
    sparse gold rim. Simple at 64–96 CSS pixels. No writing, ribbons,
    date, number, UI, surrounding stars, outer glow or rendered lock.
    Real transparent outside. Earned/locked states are rendered in CSS.

新人物先确认身份特征，再对照avatar-*胸像尺寸、头身比例、面部颗粒和描边；不要生成永久能力标签。六角色是否复用由课程brief确定

机器人优先复用robot-wink；确需重绘保持正面头部、海军蓝屏幕、青色wink表情、奶油壳与少量金色天线。没有另行授权不增加整身/外框/气泡/动作帧

## 发布

保留母版和alpha；建议关卡192/384，头像/徽章96/192（必要时384），背景480/960/1536，保持原比例。最近邻缩放、无损WebP/PNG，不用模糊缩放掩盖不合格像素图

按[清单模板](../assets/templates/asset-manifest.example.json)记录用途、参照、提示词、实际工具/模型、尺寸、透明要求、站位和SHA256；未知模型版本填null。不支持透明的工具不得把白底/棋盘当透明交付

用户认可的新锚点另进下一风格版本，原锚点保留；换模型先校准小样，再批量。只有文字生成功能时交付提示词和待生成清单，不交假图片
