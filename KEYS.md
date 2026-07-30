# 注册表签名密钥

当前密钥：

| key_id | Ed25519 公钥（Base64 Raw） | 状态 |
| --- | --- | --- |
| `linux-lightagent-skillhub-2026-01` | `H0OOSF/KbDA0/FtVah5ZXfEhIl2gZMbn5GMtvZ9GZhs=` | active |

私钥只保存在 GitHub Actions Secret `SKILL_HUB_SIGNING_KEY` 中，不进入仓库。该密钥仅签署 Linux LightAgent 专属 Registry，不与旧 LightAgent Hub 共用。轮换时先发布同时信任新旧公钥的 Linux LightAgent 版本，再切换发布密钥，最后在兼容窗口结束后移除旧公钥。
