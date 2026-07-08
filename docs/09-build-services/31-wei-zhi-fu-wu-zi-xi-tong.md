---
description: OpenHarmony 位置服务（GNSS/网络定位、地理编码、地理围栏）。
---

# 31-位置服务子系统

位置服务子系统提供设备定位能力，融合 GNSS、基站与 Wi-Fi 定位，并支持地理编码与地理围栏。它是地图、出行、本地生活类应用的基础，同时受到严格隐私约束——强依赖 [23-权限与访问控制](../../07-security/23-quan-xian-guan-li-zi-xi-tong.md) 的位置权限，并借助 [30-通信子系统](../30-tong-xin-zi-xi-tong.md) 的 Wi-Fi / 基站辅助提升精度。

## 一、定位技术

| 技术 | 特点 | 适用 |
| --- | --- | --- |
| **GNSS**（GPS / 北斗 / GLONASS / Galileo） | 室外精度高（米级），耗电较高 | 户外导航 |
| **基站定位** | 利用周边蜂窝基站估算，精度较低 | 无 GNSS 覆盖 |
| **Wi-Fi 定位** | 利用 Wi-Fi 指纹与数据库，室内可用 | 室内/城市峡谷 |
| **融合定位** | 系统按场景在精度/功耗间权衡 | 通用 |

## 二、地理编码

- **正向地理编码**：地址文本 → 经纬度坐标；
- **逆向地理编码**：坐标 → 可读地址；
- 用于"在地图上标出某地点""显示当前所在城市"等。

## 三、地理围栏（Geofence）

设定一个圆形/区域，当设备进入或离开时触发回调，典型场景："到家自动提醒""离开公司关闭空调"。

```ts
import { geoLocationManager } from '@kit.LocationKit';

// 持续定位
geoLocationManager.on('locationChange', (loc) => {
  console.info(`lat=${loc.latitude}, lon=${loc.longitude}, acc=${loc.accuracy}`);
});

// 地理围栏：进入以(39.9,116.4)为圆心、半径100m的区域
const fence: geoLocationManager.GeofenceRequest = {
  transitions: geoLocationManager.GeofenceTransition.ENTER,
  intex: 1,
  latitude: 39.9, longitude: 116.4, radius: 100, dwellDelayTime: 0
};
geoLocationManager.on('geofenceChange', fence, (res) => {
  console.info(`围栏事件: ${JSON.stringify(res)}`);
});

// 不再需要时及时注销
geoLocationManager.off('locationChange');
```

## 四、隐私与权限

- **权限类型**：位置属于 `user_grant` 敏感权限，必须在运行时申请（见 [23-权限与访问控制](../../07-security/23-quan-xian-guan-li-zi-xi-tong.md)）；后台定位还需 `ohos.permission.LOCATION_IN_BACKGROUND`。
- **精确 / 模糊位置**：应用可只申请模糊位置以减少暴露；用户也可在设置中降级。
- **最小使用**：仅在功能需要时用定位，用完及时 `off` 注销监听，避免后台持续耗电与隐私争议。

## 五、常见问题与排查

1. **室内定位偏差大**：GNSS 在室内弱，依赖 Wi-Fi / 基站定位，精度本就较低。
2. **拿不到位置**：权限被拒或 `locationChange` 未注册；确认已申请并授予位置权限。
3. **后台定位失效**：缺少后台位置权限，或系统对后台定位限频。

## 相关阅读

- [23-权限与访问控制](../../07-security/23-quan-xian-guan-li-zi-xi-tong.md)
- [30-通信子系统](../30-tong-xin-zi-xi-tong.md)
- [27-分布式任务调度](../../05-media-distributed/27-fen-bu-shi-ren-wu-diao-du.md)

## 参考资源

- OpenHarmony 位置服务官方文档（代码仓 `location`）
- ArkTS 接口：`@kit.LocationKit`（`geoLocationManager`）
