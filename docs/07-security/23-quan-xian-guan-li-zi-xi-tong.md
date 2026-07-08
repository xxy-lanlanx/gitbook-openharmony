---
description: OpenHarmony 的权限模型与访问控制（AccessTokenId、权限等级、动态授权、隐私保护）。
---

# 23-权限与访问控制

OpenHarmony 采用**基于令牌（Token）的访问控制模型**，对应用可访问的系统资源与用户数据做分级、按需授权。本章介绍权限等级、授权流程以及敏感权限的隐私保护机制。理解权限模型是开发任何会访问用户数据或系统能力（相机、位置、麦克风、通讯录等）的应用的前提。

## 一、权限模型与等级

### 1. 两种授权方式

| 类型 | 含义 | 例子 |
| --- | --- | --- |
| `system_grant`（系统授权） | 安装即自动授予，无需用户确认 | 联网 `INTERNET`、查看网络状态 |
| `user_grant`（用户授权） | 安装不授予，运行时弹窗由用户决定 | 位置、相机、麦克风、通讯录 |

`user_grant` 权限必须在应用真正需要使用该功能前，通过 `requestPermissionsFromUser` 向用户申请；在后台或权限未授予时调用相关 API 会被系统拒绝。

### 2. APL 权限等级

每个权限还有一个 **APL（Ability Privilege Level）** 等级，决定谁可以申请它：

- **normal（普通）**：低风险，第三方应用均可申请。
- **system_basic（系统基础）**：需系统签名或预置应用，普通第三方应用申请会安装失败。
- **system_core（系统核心）**：仅系统核心应用，普通应用无法持有。

应用自身的 APL 由签名与预置状态决定，申请的权限等级不能超过自身 APL——这是"权限天花板"机制。

### 3. 权限声明

应用在 `module.json5` 中声明所需权限：

```json
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.LOCATION",
        "reason": "$string:location_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" }
      }
    ]
  }
}
```

`reason` 与 `usedScene` 会让系统在弹窗与权限设置中向用户解释"为什么需要这个权限、何时使用"。

## 二、AccessToken 与授权管理

### 1. AccessTokenID

每个应用安装时由包管理服务分配一个**唯一令牌标识 AccessTokenID**。系统所有"是否允许访问"的判断，最终都落到"该 AccessTokenID 是否持有对应权限"上。

### 2. 授权流程

```
应用声明权限(module.json5)
   │
   ├─ system_grant ──► 安装时自动授予
   │
   └─ user_grant ──► 运行时 requestPermissionsFromUser 弹窗
                        │
                        ├─ 允许 ──► 写入授权记录，后续可静默使用
                        └─ 拒绝 ──► 调用相关 API 返回权限错误
```

### 3. 常用查询与授予 API（ArkTS）

```ts
import { abilityAccessCtrl, Permissions, common } from '@kit.AbilityKit';

const atManager = abilityAccessCtrl.createAtManager();
const context = getContext(this) as common.UIAbilityContext;

// 判断是否已授权
const grantStatus = atManager.checkAccessTokenSync(
  context.tokenId, 'ohos.permission.LOCATION'
);

// 未授权则弹窗申请
if (grantStatus !== abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED) {
  atManager.requestPermissionsFromUser(context, ['ohos.permission.LOCATION'])
    .then((data) => {
      if (data.authResults[0] === 0) {
        console.info('用户已授权位置权限');
      }
    });
}
```

### 4. 撤销

用户在"设置 → 应用 → 权限"中可关闭某项权限；应用卸载后其 AccessTokenID 与授权记录一并失效。

## 三、敏感权限与隐私保护

- **敏感权限清单**：位置、相机、麦克风、通讯录、日历、健身运动、读取已安装应用等属于 `user_grant` 敏感权限，必须弹窗并经用户明确允许。
- **隐私标签（Privacy Label）**：应用在应用市场与系统设置中展示"会收集哪些数据、用于什么目的"，便于用户知情决策。
- **模糊位置**：从 API 9 起位置权限支持"精确 / 模糊"两种精度，应用可只申请模糊位置（`LOCATION_IN_BACKGROUND` 等分级）以减少暴露。
- **最小权限原则**：只申请真正用到的权限，过度申请不仅影响过审，也会降低用户信任。

## 四、沙箱与隔离

- **独立运行环境**：每个应用拥有独立的 UID / GID 与私有沙箱目录（如 `/data/storage/el1-el2/...`），进程间默认无法互相访问文件。
- **跨应用访问**：不能直接用路径读取其它应用的沙箱；需通过系统提供的受控通道（如[33-文件与存储子系统](../../09-build-services/33-wen-jian-cun-chu-zi-xi-tong.md) 的公共目录、媒体库、或分布式文件），且受权限约束。
- **权限即边界**：即使代码试图越界访问，内核与应用沙箱也会拦截——权限与沙箱是"软硬结合"的双重防线。

## 五、常见问题与排查

1. **调用 API 返回 201（权限拒绝）**：既可能忘记在 `module.json5` 声明，也可能是 `user_grant` 未弹窗申请或用户拒绝。先查声明，再查运行时授权结果。
2. **安装失败 `install failed`**：常见于申请的权限 APL 高于自身等级（如第三方应用申请 `system_core` 权限），需改用普通权限或调整签名预置策略。
3. **后台无法弹窗**：`user_grant` 弹窗只能在前台 Ability 中发起，后台 Service 不能请求，应在前台用户交互时提前申请。

## 相关阅读

- [23-安全子系统](../23-an-quan-zi-xi-tong.md)
- [24-元能力Ability框架](../../08-app-framework/24-ying-yong-kuang-jia-ability.md)
- [25-包管理子系统](../../08-app-framework/25-bao-guan-li-zi-xi-tong.md)
- [31-位置服务子系统](../../09-build-services/31-wei-zhi-fu-wu-zi-xi-tong.md)

## 参考资源

- OpenHarmony 权限管理官方文档（代码仓 `security_permission`、权限列表 `permission_definition`）
- ArkTS 接口：`@kit.AbilityKit` 中的 `abilityAccessCtrl`
