---
description: OpenHarmony 通信子系统（WLAN、蓝牙、NFC、蜂窝移动网络的连接管理）。
---

# 30-通信子系统

通信子系统统一管理设备的无线连接能力，包括 WLAN、蓝牙、NFC 与蜂窝网络。它也是[16-分布式软总线](../../05-media-distributed/16-fen-bu-shi-ruan-zong-xian.md) 与 [27-分布式任务调度](../../05-media-distributed/27-fen-bu-shi-ren-wu-diao-du.md) 的连接承载——设备发现、认证、软总线建链都依赖这里的无线能力。

## 一、整体架构

通信子系统对外提供统一连接能力，对内按协议拆分为独立模块：

```
应用层（ArkTS / C++）
  │  @kit.ConnectivityKit
  ▼
系统服务层（Wi-Fi / BT / NFC / 蜂窝 SA）
  │  IPC/RPC
  ▼
协议栈与驱动层（wpa_supplicant / 蓝牙协议栈 / 调制解调器）
  │  HDI / 内核接口
  ▼
硬件层（Wi-Fi 芯片 / 蓝牙芯片 / NFC 控制器 / Modem）
```

各模块通过独立系统服务（SA）运行，应用通过 Kit 接口统一访问。服务内部管理状态机、扫描队列与连接会话，对上层屏蔽芯片差异。

## 二、WLAN 管理

- **扫描 / 连接 / 状态**：通过 `wifiManager` 扫描附近 AP、连接指定网络、查询信号与连接状态；
- **P2P（Wi-Fi Direct）**：设备间直连，无需 AP，适合大文件直传；
- **SoftAP（热点）**：本设备作为热点，供其它设备接入（也见下方网络共享）。

```ts
import { wifiManager } from '@kit.ConnectivityKit';

wifiManager.scan();
const apList = wifiManager.getScanInfoList();   // 附近 AP 列表
console.info(`发现 ${apList.length} 个热点`);
```

### 状态与事件

WLAN 服务维护连接状态机：`IDLE` → `SCANNING` → `CONNECTING` → `CONNECTED` → `DISCONNECTED`。应用可注册状态回调监听网络变化，如 `wifiManager.on('wifiStateChange', ...)`。连接状态变化会触发 `connection` 模块的默认网络重新评估。

## 三、蓝牙

- **使能 / 扫描 / 配对 / 连接**：经典蓝牙（音频/串口类）与 BLE（低功耗，信标/传感）分别管理；
- 通过 `@ohos.bluetooth` 或 `@kit.ConnectivityKit` 访问；
- 设备发现后需配对建立信任，配对信息由[23-安全子系统](../../07-security/23-an-quan-zi-xi-tong.md) 的密钥库保护。

### BLE 特性

BLE 支持广播（Advertising）、扫描（Scanning）、连接（Connection）与 GATT 服务读写。BLE 广播是软总线设备发现的重要补充手段（尤其在 Wi-Fi 未开启时）。

## 四、NFC

- **标签读取**：贴近 NFC 标签读取 NDEF 数据（门禁、标签信息）；
- **卡模拟**：设备模拟成卡（公交卡/门禁卡），由安全单元承载；
- 前台应用可注册 NFC 意图，在标签贴近时优先处理。

## 五、蜂窝网络（Telephony）

蜂窝子系统提供移动数据、通话、短信与 SIM 卡管理。虽然和 WLAN/蓝牙同属连接能力，但蜂窝链路通常承担「默认网络兜底」角色：当 Wi-Fi 不可用时，系统会自动切到蜂窝数据（受流量策略与用户设置约束）。

- **SIM 与运营商**：由 `telephony` 服务管理 SIM 状态、运营商信息与网络注册；
- **数据连接**：通过 `data` 模块开启/关闭移动数据，查询上下行流量；
- **通话与短信**：`call` 与 `sms` 模块提供基础语音与文本通信能力。

## 六、连接与网络共享

- **默认网络选择**：系统按评分（类型/质量）自动选择默认网络（Wi-Fi 优先于蜂窝）；应用通过 `connection` 模块获取网络能力与类型。
- **网络共享**：热点（SoftAP）、USB 网络共享、蓝牙网络共享，把本机网络共享给其它设备。

## 七、权限矩阵

| 能力 | 所需权限 | 授权方式 |
|------|----------|----------|
| Wi-Fi 扫描 | `ohos.permission.LOCATION` 或 `NEARBY_WIFI_DEVICES` | user_grant |
| Wi-Fi 连接 | 无需额外权限（已含于网络能力） | system_grant |
| 蓝牙扫描/配对 | `ohos.permission.ACCESS_BLUETOOTH` | user_grant |
| 蜂窝数据设置 | 系统应用签名 | system_basic |
| NFC 读取 | `ohos.permission.NFC_TAG` | system_grant |

> `NEARBY_WIFI_DEVICES` 是 Android 12+ 与 OpenHarmony 的趋势，用于不暴露精确定位的情况下扫描附近 Wi-Fi。

## 八、常见问题与排查

1. **Wi-Fi 扫描/连接失败**：需要位置权限（`ohos.permission.LOCATION` 或 `NEARBY_WIFI_DEVICES`），否则扫描受限。
2. **蓝牙配对失败**：确认对端可被发现、距离与配对码正确；部分设备需先取消旧配对。
3. **NFC 无反应**：NFC 需在前台、标签贴近天线区域，且应用已注册对应意图。
4. **分布式发现不到设备**：先确认 WLAN / 蓝牙已开启且两设备可达，再回到[27-分布式任务调度](../../05-media-distributed/27-fen-bu-shi-ren-wu-diao-du.md) 的设备认证流程。

## 相关阅读

- [16-分布式软总线](../../05-media-distributed/16-fen-bu-shi-ruan-zong-xian.md)
- [27-分布式任务调度](../../05-media-distributed/27-fen-bu-shi-ren-wu-diao-du.md)
- [31-位置服务子系统](../31-wei-zhi-fu-wu-zi-xi-tong.md)
- [34-帐号与用户身份](../34-zhang-hao-yu-shen-fen.md)

## 参考资源

- OpenHarmony 通信子系统官方文档（代码仓 `communication_wifi`、`communication_bluetooth`、`communication_nfc`）
- ArkTS 接口：`@kit.ConnectivityKit`
