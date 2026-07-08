---
description: OpenHarmony 通信子系统（WLAN、蓝牙、NFC、蜂窝移动网络的连接管理）。
---

# 30-通信子系统

通信子系统统一管理设备的无线连接能力，包括 WLAN、蓝牙、NFC 与蜂窝网络。它也是[16-分布式软总线](../../05-media-distributed/16-fen-bu-shi-ruan-zong-xian.md) 与 [27-分布式任务调度](../../05-media-distributed/27-fen-bu-shi-ren-wu-diao-du.md) 的连接承载——设备发现、认证、软总线建链都依赖这里的无线能力。

## 一、WLAN 管理

- **扫描 / 连接 / 状态**：通过 `wifiManager` 扫描附近 AP、连接指定网络、查询信号与连接状态；
- **P2P（Wi-Fi Direct）**：设备间直连，无需 AP，适合大文件直传；
- **SoftAP（热点）**：本设备作为热点，供其它设备接入（也见下方网络共享）。

```ts
import { wifiManager } from '@kit.ConnectivityKit';

wifiManager.scan();
const apList = wifiManager.getScanInfoList();   // 附近 AP 列表
console.info(`发现 ${apList.length} 个热点`);
```

## 二、蓝牙

- **使能 / 扫描 / 配对 / 连接**：经典蓝牙（音频/串口类）与 BLE（低功耗，信标/传感）分别管理；
- 通过 `@ohos.bluetooth` 或 `@kit.ConnectivityKit` 访问；
- 设备发现后需配对建立信任，配对信息由[23-安全子系统](../../07-security/23-an-quan-zi-xi-tong.md) 的密钥库保护。

## 三、NFC

- **标签读取**：贴近 NFC 标签读取 NDEF 数据（门禁、标签信息）；
- **卡模拟**：设备模拟成卡（公交卡/门禁卡），由安全单元承载；
- 前台应用可注册 NFC 意图，在标签贴近时优先处理。

## 四、连接与网络共享

- **默认网络选择**：系统按评分（类型/质量）自动选择默认网络（Wi-Fi 优先于蜂窝）；应用通过 `connection` 模块获取网络能力与类型。
- **网络共享**：热点（SoftAP）、USB 网络共享、蓝牙网络共享，把本机网络共享给其它设备。

## 五、常见问题与排查

1. **Wi-Fi 扫描/连接失败**：需要位置权限（`ohos.permission.LOCATION` 或 `NEARBY_WIFI_DEVICES`），否则扫描受限。
2. **蓝牙配对失败**：确认对端可被发现、距离与配对码正确；部分设备需先取消旧配对。
3. **NFC 无反应**：NFC 需在前台、标签贴近天线区域，且应用已注册对应意图。
4. **分布式发现不到设备**：先确认 WLAN / 蓝牙已开启且两设备可达，再回到[27-分布式任务调度](../../05-media-distributed/27-fen-bu-shi-ren-wu-diao-du.md) 的设备认证流程。

## 相关阅读

- [16-分布式软总线](../../05-media-distributed/16-fen-bu-shi-ruan-zong-xian.md)
- [27-分布式任务调度](../../05-media-distributed/27-fen-bu-shi-ren-wu-diao-du.md)
- [31-位置服务子系统](../31-wei-zhi-fu-wu-zi-xi-tong.md)

## 参考资源

- OpenHarmony 通信子系统官方文档（代码仓 `communication_wifi`、`communication_bluetooth`、`communication_nfc`）
- ArkTS 接口：`@kit.ConnectivityKit`
