---
description: OpenHarmony 应用模型核心——Ability（FA/Stage 模型）、Want、生命周期、连接与跨设备调用。
---

# 24-元能力Ability框架

Ability 是 OpenHarmony 应用的**基本组成单元与调度单位**——一个应用由一个或多个 Ability 构成，系统的启动、切换、迁移、回收都是围绕 Ability 进行的。本章介绍 Ability 的两种开发模型（FA 与 Stage）、生命周期、Want 启动机制，以及 Ability 间的连接与跨设备调用基础。

## 一、Ability 模型演进：FA 与 Stage

| 维度 | FA 模型（早期） | Stage 模型（当前主推） |
| --- | --- | --- |
| Ability 分类 | Page / Service / Data | UIAbility / ExtensionAbility |
| UI 与 Ability 关系 | Page 与 Ability 强耦合 | 多 Ability 共享进程，UI 用 ArkUI 独立承载 |
| 进程模型 | 每 Ability 独立进程 | 同一应用多 Ability 可共享进程 |
| 分布式/多窗口 | 支持但较繁琐 | 原生支持流转、跨设备、多窗口 |
| 推荐度 | 维护存量 | **新开发首选** |

> 除非维护老工程，否则一律采用 **Stage 模型**。下文以 Stage 为主。

## 二、Ability 生命周期（Stage）

以最常用的 `UIAbility` 为例，关键回调：

```
onCreate        → 创建（读取 Want 参数、初始化）
  ↓
onWindowStageCreate → 窗口舞台创建，loadContent 加载 ArkUI 页面
  ↓
onForeground    → 进入前台（可恢复动画/刷新）
  ↓ (用户切走)
onBackground    → 进入后台（释放非必要资源、保存状态）
  ↓
onWindowStageDestroy → 窗口销毁
  ↓
onDestroy       → 销毁（释放全部资源）
```

多窗口、分屏、流转都会触发 onForeground / onBackground 在不同窗口间切换。

## 三、Want 与启动机制

**Want** 是 OpenHarmony 中"我要启动谁、带什么数据"的载体对象，也是跨 Ability、跨设备调用的统一信封。

- **显式 Want**：指定 `bundleName` + `abilityName`，精准启动某一 Ability。
- **隐式 Want**：只给 `action` + `type` + `uri` 等特征，由系统匹配符合条件的 Ability（如"分享图片"交给系统选择器）。

```ts
import { common, Want } from '@kit.AbilityKit';

const context = getContext(this) as common.UIAbilityContext;

// 显式启动
const explicitWant: Want = {
  bundleName: 'com.example.myapp',
  abilityName: 'EntryAbility',
  parameters: { info: 'hello from caller' }
};
context.startAbility(explicitWant);

// 隐式启动（系统匹配）
const implicitWant: Want = {
  action: 'ohos.want.action.sendData',
  type: 'text/plain',
  uri: 'dataability://com.example.data/notes/1'
};
context.startAbility(implicitWant);
```

## 四、Ability 连接与通信

- **前台 Ability 之间**：通过 `startAbility` 携带 Want 参数传递数据；返回结果用 `startAbilityForResult` + `onAbilityResult`。
- **前后台 / 跨进程**：Stage 中后台能力用 `ExtensionAbility`（如 ServiceExtensionAbility）；前台通过 `connectServiceExtensionAbility` 拿到远端代理，基于 **IDL（接口描述语言）** 定义的桩/代理进行方法调用。
- **轻量事件**：同进程内可用 `context.eventHub` 或 [29-通知与公共事件](29-tong-zhi-gong-gong-shi-jian.md) 的 `Emitter` 做线程/Ability 间通知。

```ts
// UIAbility 生命周期（节选）与页面加载
export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam) {
    // 从 want.parameters 读取启动参数
  }
  onWindowStageCreate(windowStage: window.WindowStage) {
    windowStage.loadContent('pages/Index', (err) => {
      if (err) console.error('loadContent failed', err);
    });
  }
  onForeground() { /* 切前台 */ }
  onBackground() { /* 切后台，释放资源 */ }
  onDestroy() { /* 清理 */ }
}
```

## 五、跨设备 Ability 调用基础

结合[27-分布式任务调度](27-fen-bu-shi-ren-wu-diao-du.md)，Stage 模型可在 Want 中填入 `deviceId` 实现跨设备启动：

```ts
const remoteWant: Want = {
  deviceId: 'ABCDEF1234567890',        // 目标设备（需已互信认证）
  bundleName: 'com.example.myapp',
  abilityName: 'EntryAbility',
  parameters: { from: 'phone' }
};
context.startAbility(remoteWant);
```

要点：目标设备必须经过[23-安全子系统](23-an-quan-zi-xi-tong.md) 的设备互信认证，且应用在两台设备上均已安装、权限齐备，否则调用会被拒绝。

## 六、常见问题与排查

1. **`abilityName` 写错或包名不匹配**：启动直接报错，确保 want 中的名称与 `module.json5` 中声明的完全一致。
2. **跨设备启动无反应**：先确认两台设备在同一帐号/群组且已认证，再确认目标应用已安装。
3. **FA 与 Stage 混用**：同一应用不要混用两套模型，迁移老工程应整体转为 Stage。
4. **后台资源被回收**：onBackground 后系统可能在内存紧张时回收，关键状态应在 `onBackground` 或 `onContinue`（迁移）中持久化。

## 相关阅读

- [25-包管理子系统](25-bao-guan-li-zi-xi-tong.md)
- [27-分布式任务调度](27-fen-bu-shi-ren-wu-diao-du.md)
- [07-NAPI接口](07-napi-jie-kou.md)
- [23-权限与访问控制](23-quan-xian-guan-li-zi-xi-tong.md)

## 参考资源

- OpenHarmony 应用模型开发指南（Stage 模型、Ability 生命周期）
- ArkTS 接口：`@kit.AbilityKit`（`UIAbility`、`Want`、`abilityAccessCtrl`）
