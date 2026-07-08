---
description: OpenHarmony 电源管理（电源状态机、亮灭屏、休眠唤醒、电池与功耗优化）。
---

# 28-电源管理子系统

电源管理子系统负责设备的电源状态管理、亮灭屏与休眠唤醒策略，并对外提供电池与功耗服务。它与[13-窗口子系统](../../04-ipc-graphics/13-chuang-kou-zi-xi-tong.md)、[14-多模输入子系统](../../04-ipc-graphics/14-duo-mo-shu-ru-zi-xi-tong.md)、[10-启动流程](../../03-driver-boot/10-qi-dong-liu-cheng.md) 密切联动——亮灭屏驱动窗口显隐，输入事件触发唤醒。

## 一、整体架构

电源管理从应用到硬件分为三层协作：

```
应用层（ArkTS / C++）
  │  订阅电量、申请后台任务、设置屏幕常亮
  ▼
系统服务层（Power Manager SA）
  │  状态机决策、策略调度、唤醒锁管理
  ▼
内核与驱动层（Kernel / PMIC / 显示驱动）
  │  CPU 调频、休眠挂起、GPIO 唤醒、充电管理
  ▼
硬件层（电池、PMIC、屏幕、传感器）
```

* **Power Manager**：运行在用户态的系统服务，维护电源状态机、处理亮灭屏/休眠请求、向应用暴露电池与功耗接口。
* **内核电源子系统**：Linux 的 `cpufreq`/`cpuidle`/`suspend`/`wakelock` 等机制，执行实际的 CPU 调频、深度休眠与唤醒源管理。
* **PMIC 与充电驱动**：通过 HDI 对接电源管理芯片，获取电池信息、控制充电电流、管理硬件唤醒源。

## 二、电源状态与策略

电源服务维护一个状态机：

| 状态 | 含义 | 典型触发 |
| --- | --- | --- |
| **Running** | 唤醒运行，CPU 全频、屏幕亮 | 用户操作、充电插入 |
| **Sleeping（浅休眠）** | 屏幕熄灭、CPU 降频、部分外设断电 | 息屏超时 |
| **Hibernate（深休眠）** | 挂起到内存/磁盘，几乎零功耗 | 长时间无操作或低电量 |
| **Shutdown** | 关机 | 用户/系统指令 |

状态转换由电源服务根据按键、空闲超时、低电量阈值等事件统一决策，使能合理的功耗/响应权衡。

## 三、亮灭屏与背光

- **亮屏**：电源键、触摸、定时唤醒、来电等事件触发；亮屏后窗口子系统恢复前台 [24-Ability](../../08-app-framework/24-ying-yong-kuang-jia-ability.md)。
- **灭屏**：超时或主动调用；进入浅休眠。
- **背光调节**：亮度值由[12-图形子系统](../../04-ipc-graphics/12-graphics/12-tu-xing-zi-xi-tong-openharmony.md) 的背光服务落到底层，支持自动亮度（环境光传感器）与手动档位。

## 四、休眠与唤醒

- **进入休眠**：系统空闲达到阈值，依次冻结后台任务、关闭屏幕、降频/挂起。
- **唤醒源**：电源键、触摸屏、定时闹钟（Alarm）、网络唤醒、充电插入等。唤醒后由 init 恢复用户态服务并重建显示。
- 注意：休眠后**非必要后台任务会被挂起**，需要保活的逻辑应使用系统后台任务机制（如 WorkScheduler、长时任务）。

## 五、CPU 调频与 DVFS

电源管理通过 **DVFS（Dynamic Voltage and Frequency Scaling）** 动态调整 CPU/GPU 频率与电压，在性能与功耗间取得平衡：

- **Performance**：高负载时提升频率，保证流畅度；
- **PowerSave**：空闲或低电量时降频，延长续航；
- **Thermal**：温度超限时主动降频，防止过热关机。

调频策略由内核 `cpufreq`  governor（如 schedutil、ondemand）配合系统服务的热/电策略共同决定。

## 六、电池与功耗优化

- **Battery Service**：提供电量百分比（SOC）、电压、充放电状态、电池健康度；应用可订阅电量变化。
- **耗电统计**：按 UID / 部件统计功耗，支撑系统级优化与"耗电排行"。
- **优化手段**：后台应用冻结、对齐唤醒（低功耗模式集中处理）、[29-通知与公共事件](../29-tong-zhi-gong-gong-shi-jian.md) 合并、按需降频。

```ts
import { batteryInfo } from '@kit.BasicServicesKit';

const soc = batteryInfo.soc;              // 电量百分比 0~100
const status = batteryInfo.chargeState;  // 充电状态
console.info(`电量: ${soc}%, 状态: ${status}`);
```

## 七、应用功耗控制

应用可通过以下方式配合系统电源策略：

- **后台任务**：使用 `WorkScheduler` 或 `长时任务` 替代常驻线程，让系统统一调度执行窗口。
- **屏幕常亮**：视频/导航类应用可申请 `ohos.permission.KEEP_BACKGROUND_RUNNING` 并设置屏幕常亮。
- **避免频繁唤醒**：减少不必要的定时器、网络轮询，使用推送或事件驱动代替心跳。

## 八、常见问题与排查

1. **息屏后任务不跑**：属正常休眠；需保活请用后台任务/定时任务，而非依赖常驻线程。
2. **亮屏耗电高**：常见原因为高背光亮度、高刷新率、频繁唤醒，可从这几处优化。
3. **无法唤醒**：检查对应唤醒源是否注册（如 Alarm 是否设置、网络唤醒是否开启）。
4. **充电慢或无法充电**：检查充电驱动日志、PMIC 温度保护、电池健康状态。

## 相关阅读

- [13-窗口子系统](../../04-ipc-graphics/13-chuang-kou-zi-xi-tong.md)
- [14-多模输入子系统](../../04-ipc-graphics/14-duo-mo-shu-ru-zi-xi-tong.md)
- [10-启动流程](../../03-driver-boot/10-qi-dong-liu-cheng.md)
- [29-通知与公共事件](../29-tong-zhi-gong-gong-shi-jian.md)
- [12-图形子系统](../../04-ipc-graphics/12-graphics/12-tu-xing-zi-xi-tong-openharmony.md)

## 参考资源

- OpenHarmony 电源管理官方文档（代码仓 `powermgr`）
- ArkTS 接口：`@kit.BasicServicesKit` 中的 `batteryInfo`
