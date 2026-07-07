---
description: OpenHarmony 分布式任务调度子系统，实现跨设备 Ability 拉起、流转（Continue）与协同（Collaboration）。
---

# 27-分布式任务调度

分布式任务调度（Distributed Scheduler）建立在[16-分布式软总线](16-fen-bu-shi-ruan-zong-xian.md)、[23-安全子系统](23-an-quan-zi-xi-tong.md) 设备认证、[17-分布式数据管理](17-fen-bu-shi-shu-ju-guan-li.md) 与 [18-分布式硬件](18-fen-bu-shi-ying-jian.md) 之上，提供**跨设备 Ability 拉起、迁移流转与协同调用**能力——这是 OpenHarmony"超级终端"体验的核心支撑。

## 一、分布式调度架构

```
            ┌──────────────── 分布式任务调度 (DMS) ────────────────┐
            │  跨设备启动 / 流转(Continue) / 协同(Collaboration)    │
            └───────────────┬───────────────┬─────────────────────┘
                            │               │
             软总线(传输通道) │      设备认证(信任前提) │
                            │               │
                 分布式数据管理        分布式硬件
```

- **信任前提**：目标设备必须经过设备互信认证，否则不在"可信设备列表"中，调度会被拒绝。
- **通道**：实际数据传输经由软总线加密通道，应用无需自建安全。
- **落地**：跨设备启动最终由对端系统的 Ability 管理服务（AMS）拉起对应 Ability。

## 二、跨设备 Ability 启动

在 [24-元能力Ability框架](24-ying-yong-kuang-jia-ability.md) 的基础上，Want 中填入 `deviceId` 即可拉起对端设备的 Ability：

```ts
import { distributedDeviceManager } from '@kit.DistributedServiceKit';
import { common, Want } from '@kit.AbilityKit';

const dm = distributedDeviceManager.createDeviceManager('com.example.myapp');
const devices = dm.getTrustedDeviceListSync();   // 已互信设备

if (devices.length > 0) {
  const want: Want = {
    deviceId: devices[0].deviceId,
    bundleName: 'com.example.myapp',
    abilityName: 'EntryAbility',
    parameters: { from: 'phone' }
  };
  (getContext(this) as common.UIAbilityContext).startAbility(want);
}
```

## 三、迁移与流转（ContinueAbility）

典型场景：手机上正在看的视频，一键流转到平板继续播放。

- **源端**：Ability 实现 `onContinue`，返回是否允许迁移，并把要延续的状态写入 Want 的 `continueState` / 自定义参数；
- **目标端**：系统拉起同 Ability，`onCreate(want)` / `onWindowStageCreate` 中读取 Want 携带的状态恢复页面与进度。

```ts
// 源端：允许迁移并保存状态
onContinue(wantParam: Record<string, Object>): AbilityConstant.OnContinueResult {
  wantParam['playPosition'] = this.currentTime;   // 保存播放进度
  return AbilityConstant.OnContinueResult.AGREE;
}

// 目标端：恢复
onCreate(want: Want, launchParam: AbilityConstant.LaunchParam) {
  const pos = want.parameters?.['playPosition'];
  if (pos !== undefined) this.restore(pos as number);
}
```

## 四、协同调用

对于需要"在对端执行一段逻辑并拿回结果"的场景（如远端计算、远端设备能力调用）：

- Stage 模型下用 `ServiceExtensionAbility` / 后台扩展能力承载被调用方；
- 调用方通过 `connectServiceExtensionAbility` 获取远端代理，基于 **IDL** 定义的桩/代理调用方法，结果经回调回传。

## 五、设备发现与选择

- **已认证设备**：`getTrustedDeviceListSync()` 直接拿到同帐号/同群组的可信设备；
- **发现新设备**：`startDeviceDiscovery` 发现附近设备，结合[30-通信子系统](30-tong-xin-zi-xi-tong.md) 的 Wi-Fi / 蓝牙完成认证入组；
- **选择策略**：按设备类型、能力、网络质量筛选最合适的目标（如大屏流转优先选 tablet / TV）。

## 六、常见问题与排查

1. **设备不在可信列表**：两台设备未登录同一帐号或群组失效，先完成设备认证。
2. **远程拉起失败**：目标设备未安装该应用，或应用未使用相同签名（分布式要求同签名/同帐号）。
3. **流转后状态丢失**：源端 `onContinue` 未保存、或目标端未在 `onCreate` 读取恢复——务必两端对齐 Want 参数键名。
4. **调用超时**：软总线通道中断或对端负载过高，检查网络与设备在线状态。

## 相关阅读

- [16-分布式软总线](16-fen-bu-shi-ruan-zong-xian.md)
- [17-分布式数据管理](17-fen-bu-shi-shu-ju-guan-li.md)
- [18-分布式硬件](18-fen-bu-shi-ying-jian.md)
- [24-元能力Ability框架](24-ying-yong-kuang-jia-ability.md)

## 参考资源

- OpenHarmony 分布式任务调度官方文档（代码仓 `distributedschedule`）
- ArkTS 接口：`@kit.DistributedServiceKit`（`distributedDeviceManager`）
