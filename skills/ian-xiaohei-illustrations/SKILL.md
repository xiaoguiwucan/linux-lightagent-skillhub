---
name: ian-xiaohei-illustrations
schema_version: 2
version: 1.1.0
description: 生成 Ian 风格的中文正文配图。用于用户要求为中文文章、帖子、博客、工作流文档、方法论、流程、结构、状态、隐喻或观点生成“怪诞”“小黑”“手绘”“正文配图”“文章插图”“配图建议”“shot list”“去标题/改图”等任务；通过 Linux LightAgent 受控生图工具输出纯白手绘、少量红橙蓝批注的 16:9 图片。
author: Ian
license: MIT
homepage: https://github.com/helloianneo/ian-xiaohei-illustrations
repository: https://github.com/xiaoguiwucan/ian-xiaohei-illustrations
min_lightagent_version: 1.0.0-rc.1
max_lightagent_version: null
platforms: [linux, darwin, windows]
category: image
tags: [illustration, chinese-article, hand-drawn, xiaohei, image-generation]
status: active
publisher: community
release_notes: 新增受技能快照与微信群 ACL 约束的提示词预加载声明，命中小黑风格请求时一次加载核心规则，减少生图前的多轮模型读取。
breaking_changes: []
requirements:
  env: []
  bins: []
  python: []
  npm: []
  downloads: []
  capabilities: []
lightagent:
  network_domains: []
  file_paths: [<workspace>/images]
  tools: [read, image_generate]
  docker_notes: 可在官方 Docker 非 root 用户环境运行；管理员需要先在模型设置中配置可用的生图 Provider。
  wechat_group:
    access: restricted
    authorization_scope: stable-room-or-member
    notes: 安装后由管理员按稳定群或稳定成员显式授权；生图继续受当前群每小时额度限制，一次请求只交付一张图片。
  output_contract:
    mode: agent-managed
  prompt_preload:
    triggers: [小黑, Ian风格, "Ian 风格"]
    files: [SKILL.md, references/style-dna.md, references/xiaohei-ip.md, references/composition-patterns.md, references/prompt-template.md, references/qa-checklist.md]
    max_chars: 30000
  entrypoints: []
---

# Ian 小黑怪诞正文配图

## 核心定位

为中文文章设计和生成 16:9 横版正文配图。目标不是做商业插画、PPT 信息图或可爱卡通，而是把文章里的关键判断、流程、结构、状态或隐喻，变成一张清爽、怪诞、有创意、可读但不说明书的手绘解释图。

默认视觉 IP 是“小黑”：黑色实心、白点眼、细腿、空表情，认真做一件荒诞但成立的事。小黑必须参与画面的核心动作，不能只是站在旁边当装饰。

## 先读这些参考

按任务需要读取，不要一次塞满上下文：

- `references/style-dna.md`：风格 DNA、颜色、文字、禁忌。
- `references/xiaohei-ip.md`：小黑 IP 的形象、性格、动作库和禁忌。
- `references/composition-patterns.md`：结构类型、原创隐喻方法和反复刻规则。
- `references/prompt-template.md`：单张生图提示词模板。
- `references/qa-checklist.md`：生成后检查和迭代规则。
- `assets/examples/`：只作低频视觉校准，不进入默认生成路径。不要照抄这些案例的构图、物件或标注。

## 工作流

### 1. 消化正文

先读用户给的正文、链接、Notion 页面、Markdown 文件或截图内容。提炼：

- 核心观点是什么
- 哪些段落承担认知转折
- 哪些内容适合用图解释
- 哪些地方只适合文字，不需要图

不要平均配图。优先选择“认知锚点”，例如：核心判断、两个断点、输入输出闭环、分流、前后对比、一鱼多吃、承接路径、常见坑、角色状态变化。

### 2. 先出配图策略

如果用户只是说“分析怎么配图 / 思考哪些地方需要配图”，先给 shot list。每张图写清楚：

- 放在哪个段落后
- 图的主题
- 核心意思
- 结构类型
- 小黑在图里做什么
- 建议元素
- 建议中文标注词

默认 4-8 张。文章很短时 1-3 张；长文也不要轻易超过 9 张。够用就好，避免把正文做成画册。

### 3. 单张生成

如果用户明确要求“生成 / 输出 / 做图 / 帮我生成”，不要停下来等确认；整理一张完整提示词后调用一次 `image_generate`。不要调用 `bash`、`write` 或 `send`，也不要自行请求任何生图 API。`image_generate` 成功后会把本地图片加入当前回复附件。

调用参数固定遵循以下结构：

```json
{
  "prompt": "<按 references/prompt-template.md 形成的完整提示词>",
  "quality": "medium",
  "aspect_ratio": "16:9"
}
```

一次请求只调用一次 `image_generate` 并交付一张图。如果用户要求多张：先给完整 shot list，同时生成第 1 张；最终文字说明“已生成第 1/N 张，回复继续生成下一张”。后续每次“继续”只生成下一张，禁止一轮调用多次造成只有第一张实际发送。

每张图只讲一个核心结构。提示词必须包含：

- 16:9 横版中文正文配图
- 纯白背景
- 黑色手绘线稿
- 少量红色/橙色/蓝色中文手写批注
- 大量留白
- 小黑作为核心动作主体
- 禁止 PPT、商业插画、幼稚可爱、复杂架构、左上角类型标题

不要复刻过往案例。案例只提供风格密度和小黑参与方式，不能直接复用“传送带断点 / 小黑拉线 / 素材鱼 / 盖章工具箱 / 常见坑路径”等已有构图，除非用户明确要求复刻某张图。每次都要从当前文章重新发明一个奇怪但成立的隐喻。

### 4. 检查与迭代

生成后检查 `references/qa-checklist.md`。如果出现以下问题，优先重生成或局部编辑：

- 小黑只是装饰
- 画面太满
- 太像流程图/PPT
- 中文太多或错字严重
- 左上角出现“常见坑/流程图/系统架构图”等标题
- 画风太可爱、幼稚、死板
- 背景不是干净白底

改图时只允许把 workspace 内现有图片路径放到 `image_generate.image_path`；禁止传 URL 或 workspace 外路径。没有可用本地路径时，直接说明需要先把原图保存到 workspace，不要猜测路径。

### 5. 保存交付

`image_generate` 默认把最终图写入：

```text
<workspace>/images/
```

文件名由生图 Provider 生成且不会覆盖既有图片。不要为了重命名再调用文件写入工具。

## 输出口径

生成前的策略输出要短而准。生成后的交付要包含：

- 当前生成的是第几张及其用途
- 多图任务还剩几张，可回复“继续”逐张生成
- 图片已作为当前回复附件发送

不要在群聊里暴露本地保存路径，不要长篇解释风格理论；让图自己说话。
