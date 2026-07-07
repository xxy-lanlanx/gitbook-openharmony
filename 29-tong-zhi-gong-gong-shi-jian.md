---
description: OpenHarmony 通知（Notification）与公共事件（CommonEvent/Emitter）子系统。
---

# 29-通知与公共事件

通知服务与公共事件机制是应用间、以及应用与系统间通信的重要手段。本章介绍通知的发布与管理、公共事件的发布订阅模型，以及进程内轻量事件 Emitter。

## 一、通知服务（Notification）

通知用于向用户呈现重要信息，即使应用不在前台也能触达。

- **类型**：普通文本、进度条、横幅（浮动提醒）等。
- **发布**：构造 `NotificationRequest`，通过 `notificationManager.publish` 发出；可携带 `wantAgent` 指定点击后跳转的 Ability。
- **管理**：取消（cancel）、查询当前有效通知、订阅通知开关变化。

```ts
import { notificationManager } from '@kit.NotificationKit';
import { Want } from '@kit.AbilityKit';

const req: notificationManager.NotificationRequest = {
  id: 1,
  content: {
    contentType: notificationManager.ContentType.NOTIFICATION_CONTENT_BASIC_TEXT,
    normal: { title: '新消息', text: '您有一条待办事项' }
  },
  wantAgent: {
    pkgName: 'com.example.myapp',
    abilityName: 'EntryAbility'
  } as Want
};
notificationManager.publish(req);
```

> 发布通知需声明并申请通知相关权限；用户可在设置中关闭某应用通知。

## 二、公共事件（CommonEvent）

公共事件是一种广播式通信，常用于系统状态变化（亮屏/灭屏、网络变化、电量低、时区变更、开机完成等）。

- **发布**：系统或应用通过 `CommonEvent.publish` 发出；
- **订阅**：应用通过 `commonEventManager.subscribe` 注册关心的事件名（如 `usual.event.SCREEN_OFF`）；
- **有序事件**：按订阅者优先级串行投递，可被中断；
- **粘性事件**：后订阅者也能收到"最近一次"的事件，适合获取当前状态。

```ts
import { commonEventManager } from '@kit.BasicServicesKit';

commonEventManager.subscribe({
  events: ['usual.event.SCREEN_OFF']
}, (err, data) => {
  if (!err && data) console.info('屏幕已熄灭');
});
```

> 监听部分系统事件需对应权限（如开机完成 `ohos.permission.RECEIVER_STARTUP_COMPLETED`）。

## 三、Emitter 进程内事件

Emitter 是**同应用内**的轻量事件分发机制，用于 Ability 之间、线程之间的解耦通知，比 CommonEvent 更轻、且仅对本应用可见。

- 通过 `emit` 发送、`on` 订阅、`off` 取消；
- 适合页面与后台逻辑的状态同步，不涉及跨应用广播。

## 四、选型建议

| 场景 | 推荐 |
| --- | --- |
| 触达用户的重要信息 | 通知 Notification |
| 跨应用/系统状态广播 | 公共事件 CommonEvent |
| 同应用内线程/Ability 通信 | Emitter |
| 结构化数据传递 | [24-Ability 的 Want](24-ying-yong-kuang-jia-ability.md) |

## 五、常见问题与排查

1. **通知不显示**：未申请通知权限，或用户在设置中关闭了通知；检查 `NotificationRequest` 字段完整。
2. **CommonEvent 收不到**：事件名拼写错误，或缺少所需权限；确认订阅在事件可能产生之前已注册。
3. **后台频繁通知被限流**：系统对高频通知有限流，合并同类通知、降低频率。

## 相关阅读

- [24-元能力Ability框架](24-ying-yong-kuang-jia-ability.md)
- [13-窗口子系统](13-chuang-kou-zi-xi-tong.md)
- [28-电源管理子系统](28-dian-yuan-guan-li-zi-xi-tong.md)

## 参考资源

- OpenHarmony 通知与公共事件官方文档（代码仓 `notification`、`common_event`）
- ArkTS 接口：`@kit.NotificationKit`、`@kit.BasicServicesKit`
