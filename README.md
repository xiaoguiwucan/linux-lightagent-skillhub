# Linux LightAgent Skill Hub

Linux LightAgent 专属技能中心。它基于原 LightAgent Hub 的签名发布机制，但针对 Linux/Docker、官方 Linux 微信、稳定身份权限和真实媒体发送建立独立兼容规范。技能通过 GitHub Pull Request 投稿，经自动校验和维护者审核后发布为可校验的静态注册表，不收集安装遥测。

- 源码仓库：https://github.com/xiaoguiwucan/linux-lightagent-skillhub
- 技能目录：https://xiaoguiwucan.github.io/linux-lightagent-skillhub/

## 使用

```bash
lightagent skill search hello
lightagent skill install hello-lightagent
lightagent skill outdated
lightagent skill update hello-lightagent
```

LightAgent Web 控制台的“技能 -> 获取在线技能”可直接浏览、搜索、安装、检查更新、更新、回滚和卸载。后台只检查更新，不会自动升级。

网页目录由 GitHub Pages 发布，Linux LightAgent 只安装通过本 Hub 独立公钥验签的技能；目录不可用时仅使用最后一次验证通过的缓存。CowAgent 原技能广场仍在产品中独立展示，但保持只读，不作为本 Hub 的后备安装源。

## 已收录技能

- `social-media-downloader` `2.1.0`：统一下载抖音、TikTok、YouTube 和 Telegram 视频或图集，支持原始画质、缓存复用、临时网络错误重试、断点续传、无损分段、发送后两分钟清理、进度查询及 Telegram 登录会话。
- `douyin-video-share` `1.0.0`：自动识别当前消息中的单个抖音公开视频分享链接，通过 Skill Runner 安全下载并发送回原 Web 或微信群会话。
- `github-project-assistant` `1.0.0`：配合 LightAgent `github_project` 和 `scheduler` 工具，查询多个 GitHub 项目的 Issue、PR、CI、Release 和动态，并在用户明确确认后创建 Issue 或合并已有 PR。
- `av-meta` `1.2.0`：查询用户当前明确提供的单个番号元数据，并按文字后封面的确定性合同输出。
- `hello-lightagent` `1.0.0`：验证 Skill Hub 安装链路和运行环境。

## 投稿

1. 从 `templates/skill/` 复制模板到 `skills/<name>/`。
2. 完成 `SKILL.md` 的全部必填元数据，并将测试放入 `evaluations/<name>/`。
3. 运行 `python scripts/validate.py` 和 `python scripts/build_registry.py --output dist`。
4. 按中文 PR 模板提交；一个 PR 原则上只修改一个技能。

详细要求见 [CONTRIBUTING.md](CONTRIBUTING.md)、[DEVELOPING.md](DEVELOPING.md) 与 [REVIEWING.md](REVIEWING.md)。

## 安全边界

Schema v2 脚本技能必须声明结构化 `lightagent.entrypoints`，并通过 Linux LightAgent `skill_run` 调用；不得要求 Agent 用 Bash、Python 或 Node 命令字符串直接启动技能脚本。系统组件使用 `requirements.capabilities` 声明，不得包含运行时 root、apt、brew 或 sudo 安装步骤。

每个技能必须声明 `lightagent.wechat_group`。可在微信群调用的技能统一使用 `restricted` 和 `stable-room-or-member`，安装后由管理员显式授权稳定群或稳定成员；不支持微信群的技能必须声明 `disabled`。需要确定性文本加媒体回复时，使用 `ordered-text-attachments` 合同，并返回 `reply_text`、`attachments`、`delivery_order`，由 Linux LightAgent 按文字确认成功后再发送附件。

网络域名、文件路径、环境变量和工具权限必须按实际最小范围声明。通配域名只允许用于无法稳定枚举的媒体 CDN，并须在 PR 中解释。Skill Runner 第一阶段提供受控子进程、最小环境、路径、超时、输出和资源限制，但不构成完整文件系统或网络沙箱。

## 许可证

仓库基础设施采用 Apache-2.0。每个技能必须单独声明 SPDX 许可证，技能代码与素材以该技能声明为准。
