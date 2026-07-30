# 技能开发规范

技能应聚焦单一工作流，`description` 必须准确说明触发条件。正文写清输入、步骤、失败处理和输出，不能诱导模型泄露密钥、跳过确认、关闭安全机制或无限制读取和上传文件。

脚本必须可重复执行、默认最小权限、错误时返回非零状态。运行数据写入 LightAgent 提供的技能数据目录；密钥只通过环境变量或 LightAgent 配置获取。更新和卸载不得删除用户配置与生成数据。

兼容性由 `min_lightagent_version`、`max_lightagent_version` 和 `platforms` 描述。无法以非 root 用户在 Linux LightAgent 官方 Docker 中完成依赖准备时，必须填写 `docker_notes`。

复杂技能应在 `evaluations/<name>/cases.json` 提供代表性输入与验收条件，测试答案不能写入发布包。

Schema v2 脚本技能必须在 `lightagent.entrypoints` 声明入口名、相对路径、运行时、超时、输出/内存/进程上限和参数约束。技能正文只说明如何调用 `skill_run`，不提供绕过 Runner 的直接命令。

系统组件使用 `requirements.capabilities` 中的稳定能力名。技能安装和运行时不得执行 `sudo`、`apt` 或 `brew`；缺少能力时，在 `docker_notes` 中说明 `skills-full` 镜像或自定义 `SKILL_CAPABILITY_PACKS` 构建参数。

## Linux LightAgent 渠道合同

- 微信群技能默认受限，配置使用 stable room/member scope；不得把昵称、群名或当前网关 runtime ID 当成长期权限标识。
- 输出单段文字后发送一个或多个附件的脚本，应返回 `reply_text`、`attachments` 和固定 `delivery_order`。文本内容由脚本确定，Agent 不得改写关键字段。
- 附件只写入声明的 workspace 路径，并在输出前确认文件存在；通道文本发送未确认时不得继续发送附件。
- CowAgent 技能广场条目不自动获得本 Hub 的兼容或签名状态，需要迁移时必须作为新版本重新审核和打包。
