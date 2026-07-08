# 电话子系统（Telephony）

电话子系统（Telephony）负责管理蜂窝网络相关的核心功能，包括语音通话、短信收发、移动数据连接、SIM 卡状态以及 IMS 多媒体服务。在 OpenHarmony 标准系统中，Telephony 以系统服务的形式运行在用户态，通过 IPC 与 Ability 框架和应用程序交互。

## 整体架构

Telephony 子系统采用分层设计，整体分为：

- **应用层**：电话、短信、联系人、设置等应用通过 JS API 调用 Telephony 能力。
- **框架层**：`@ohos.telephony` 提供 JS 接口；`Telephony Service` 作为系统服务对外暴露能力。
- **核心服务层**：
  - **Call Manager**：语音通话管理（拨号、接听、挂断、会议通话）。
  - **SMS Manager**：短信与彩信收发、短信中心地址管理。
  - **Data Manager**：蜂窝数据连接（APN 配置、数据开关、网络类型回落）。
  - **SIM Manager**：SIM 卡状态检测、PIN/PUK 验证、运营商信息读取。
  - **IMS**：VoLTE/VoWiFi 语音与视频通话、IMS 注册状态管理。
  - **Network Search**：网络搜索与注册、漫游状态管理、信号强度上报。
  - **State Registry**：注册各类状态变化回调（信号、网络类型、SIM 状态等）。
- **RIL 层**：Radio Interface Layer，通过 HDI 与 Modem 通信，将 AT 指令或 QMI/RIL 请求发送到基带芯片。
- **Modem 硬件层**：基带芯片完成空口协议交互。

## 核心模块详解

### 1. 通话管理（Call Manager）

支持单通、多方会议、呼叫等待、呼叫转移等基础电信业务。通话状态机包括：

- `IDLE` → `DIALING` → `ALERTING` → `ACTIVE`
- `ACTIVE` → `HOLDING` → `DISCONNECTED`

通话音频路由由 **Audio Manager** 根据通话状态自动切换至听筒、扬声器或蓝牙耳机。

### 2. 短信管理（SMS Manager）

- 支持 7bit/8bit/UCS2 编码的 SMS 与长短信拼接。
- 支持 SMS-DELIVER 和 SMS-SUBMIT 的 PDU 编解码。
- 短信中心地址（SMSC）可通过 SIM 卡或运营商配置自动获取。
- 在接收短信时，Telephony 会发送公共事件 `usual.event.SMS_RECEIVE`，应用可通过订阅该事件实现短信验证码自动填充等功能。

### 3. 数据连接（Data Manager）

- 管理 APN（Access Point Name）配置，支持 IPv4/IPv6/IPv4v6 双栈。
- 提供数据开关、漫游数据开关、首选网络类型（5G/4G/3G/2G）设置。
- 与 NetManager 协作，在数据连接建立时配置路由和 DNS。

### 4. SIM 卡管理（SIM Manager）

- 检测 SIM 卡插拔、Ready/Locked/Absent 状态。
- 支持 PIN 码验证、PUK 码解锁。
- 读取 IMSI、ICCID、运营商名称（SPN/PLMN）、语音信箱号码。
- 支持多卡（双卡双待）独立管理，每张卡对应独立的 `slotId`。

### 5. IMS 服务

- 负责 VoLTE/VoWiFi 的注册、去注册、语音/视频通话建立。
- 与 SIP 协议栈交互，处理 IMS 注册状态（`REGISTERED`、`UNREGISTERED`）。
- 在 5G NR 网络下，IMS 是语音回落（EPS Fallback）或 VoNR 的关键组件。

## 典型流程：拨号与接听

```
应用层：startCall()  →  Telephony Service  →  Call Manager
   ↓
RIL：dial()  →  Modem  →  空口信令  →  核心网
   ↓
对端振铃  →  接听  →  Modem  →  RIL  →  Call Manager
   ↓
音频通道建立（Audio Manager 路由至听筒）
```

## 关键接口与权限

| 能力 | 接口示例 | 所需权限 |
|------|---------|---------|
| 拨打电话 | `call.makeCall(phoneNumber)` | `ohos.permission.PLACE_CALL` |
| 获取通话状态 | `call.getCallState()` | 系统权限 |
| 发送短信 | `sms.sendMessage()` | `ohos.permission.SEND_MESSAGES` |
| 获取信号信息 | `signal.getSignalInformation()` | `ohos.permission.GET_TELEPHONY_STATE` |
| 获取 SIM 信息 | `sim.getSimState()` | `ohos.permission.GET_TELEPHONY_STATE` |
| 设置数据开关 | `data.enableCellularData()` | 系统权限 |

> **注意**：大多数 Telephony 接口涉及用户隐私或系统安全，需要声明 `user_grant` 或 `system_grant` 权限，并在应用配置中通过 ACL 申请系统权限。

## 调试与常见问题

### 查看 Telephony 日志

```bash
hilog | grep -i telephony
hilog | grep -i ril
hilog | grep -i call
```

### 常见故障排查

| 现象 | 可能原因 | 排查方向 |
|------|---------|---------|
| 无信号 | 天线/射频问题、SIM 卡未识别 | 查看 SIM 状态、RIL 日志、射频校准 |
| 无法拨号 | 网络未注册、飞行模式、权限缺失 | 检查 `getCallState()`、网络注册状态 |
| 数据无法上网 | APN 错误、数据开关关闭、漫游限制 | 检查 APN 配置、`enableCellularData()` 状态 |
| 短信发送失败 | 短信中心地址错误、信号弱 | 检查 SMSC 地址、信号强度 |
| VoLTE 无法注册 | IMS 配置缺失、网络不支持 | 检查 IMS 开关、运营商配置、SIP 注册日志 |

## 相关阅读

- [RIL 与 Modem 适配](https://gitee.com/openharmony/telephony_ril_adapter)
- [Call Manager 源码](https://gitee.com/openharmony/telephony_call_manager)
- [SMS Manager 源码](https://gitee.com/openharmony/telephony_sms_mms)
- [IMS 源码](https://gitee.com/openharmony/telephony_ims)
- [蜂窝网络协议栈 3GPP TS 24.008](https://www.3gpp.org/specifications)
