---
description: OpenHarmony 安全子系统的总体架构，涵盖可信执行环境、数据加密（HUKS）、设备认证与隐私保护基础。
---

# 23-安全子系统

安全是 OpenHarmony 分布式能力的基石。OpenHarmony 设计之初就面向"设备泛在、分布协同"的场景，任何跨设备的数据、硬件、Ability 调用都建立在对端设备与对端应用"可信"的前提之上。本章梳理安全子系统的总体架构，并深入到通用密钥库 HUKS、设备互信认证、数据防护与应用签名等核心机制，为后续权限管理、分布式调度等章节提供信任底座的认知。

## 一、安全架构总览

OpenHarmony 的安全体系遵循"硬件可信根 → 可信启动链 → 系统服务隔离 → 应用沙箱"的纵深防御思路。

### 1. REE 与 TEE 双世界

- **REE（Rich Execution Environment，富执行环境）**：即常规的操作系统世界，运行 Linux 内核与各类普通应用，能力丰富但攻击面大。
- **TEE（Trusted Execution Environment，可信执行环境）**：基于芯片 TrustZone 或独立安全核（如 iSE、安全 MCU 上的 TEE OS）构建的隔离执行环境，拥有独立内存与外围访问控制。即使 REE 被攻破，也无法直接读取 TEE 中的密钥与敏感数据。

安全子系统的密钥管理与核心密码运算优先在 TEE 中完成；当硬件不支持 TEE 时回退到 REE 的软件实现（安全性下降、运算性能也不同）。

### 2. 可信启动链（Chain of Trust）

设备上电后，从固化在芯片中的**信任根（Root of Trust, RoT）**开始，每一级镜像在加载下一级前先验证其签名：

```
芯片 RoT → BootROM/XBL → U-Boot / Little Kernel → Trusted Firmware → Linux 内核 → Init → system 镜像
```

任何一级校验失败则启动终止或进入恢复模式，从而保证从底层固件到上层系统的完整性与来源可信。

### 3. 安全模块组成

安全子系统（基础软件服务层 `security` 子系统）主要包含：

| 模块 | 职责 |
| --- | --- |
| HUKS | 通用密钥库，密钥管理与加解密/签名运算 |
| DeviceAuth | 设备互信认证与群组管理 |
| 应用签名校验 | 安装 / OTA / 运行时的完整性度量 |
| 加密服务 | 文件、数据传输加密支撑 |

> 注：本章聚焦安全子系统自身；应用运行时"能否访问某资源"由 [23-权限与访问控制](../23-quan-xian-guan-li-zi-xi-tong.md) 负责。

## 二、HUKS 通用密钥库

HUKS（HarmonyOS Universal KeyStore）是 OpenHarmony 的**统一密钥管理与密码运算服务**，向上为系统与应用提供密钥生命周期管理与标准密码学能力，向下对接 TEE / REE 的密码实现。

### 1. 核心能力

- **密钥生命周期**：生成、导入、导出（受控）、删除、查询密钥参数。
- **密码运算**：对称加解密（AES / SM4 / 3DES）、非对称加解密（RSA / SM2）、签名验签（RSA / ECDSA / SM2）、摘要（SHA / SM3）、密钥协商（ECDH / X25519）。
- **密钥不出安全区**：私钥等敏感材料默认只在 TEE 内参与运算，应用侧只能拿到"句柄 / 引用"，无法导出明文——这是 HUKS 与普通软件加密库最本质的区别。

### 2. 分层架构

```
应用 / NAPI(@ohos.security.huks)
        │
HUKS Framework (huks_standard)  —— 参数校验、策略、并发
        │
HUKS Engine (hks)               —— 密钥存储与算法调度
        │
TEE 实现  /  REE 软件实现
```

### 3. 典型调用（Native API 示意）

```c
#include "huks/huks_type.h"
#include "huks/huks_param.h"

// 1) 构造密钥参数集：AES-256-GCM
struct HksParamSet *paramSet = HksInitParamSet();
struct HksParam params[] = {
    {.tag = HKS_TAG_ALGORITHM, .uint32Param = HKS_ALG_AES},
    {.tag = HKS_TAG_KEY_SIZE,  .uint32Param = HKS_AES_KEY_SIZE_256},
    {.tag = HKS_TAG_PURPOSE,   .uint32Param = HKS_KEY_PURPOSE_ENCRYPT | HKS_KEY_PURPOSE_DECRYPT},
    {.tag = HKS_TAG_BLOCK_MODE,.uint32Param = HKS_MODE_GCM},
    {.tag = HKS_TAG_DIGEST,    .uint32Param = HKS_DIGEST_SHA256},
};
HksAddParams(paramSet, params, sizeof(params) / sizeof(params[0]));

// 2) 生成密钥（密钥材料留在安全区，不返回明文）
struct HksBlob keyAlias = { .size = 8, .data = (uint8_t*)"demoKey" };
HksGenerateKey(&keyAlias, paramSet);

// 3) 加解密
HksEncrypt(&keyAlias, paramSet, &plainBlob, &cipherBlob);
```

> 应用层更常用的是 NAPI 封装 `@ohos.security.huks`，通过 `huks.generateKey`、`huks.encrypt` 等异步接口调用，无需直接写 C。

## 三、设备互信认证（DeviceAuth）

分布式协同的前提是确认"对端设备是谁、是否可信"。设备互信认证模块解决两个设备之间的**双向认证**与**信任关系（群组）**建立。

- **认证类型**：同帐号设备组（登录同一厂商帐号的多个设备自动互信）、点对点群组（扫码 / 碰一碰建立的临时互信）。
- **认证过程**：基于 HUKS 完成**密钥协商**与会话密钥派生，采用挑战-响应机制抵御重放；认证通过后双方持有共享的群组凭据。
- **与软总线的关系**：设备认证通过后，[16-分布式软总线](../../05-media-distributed/16-fen-bu-shi-ruan-zong-xian.md) 才能基于协商出的会话密钥建立加密传输通道，承载分布式硬件、数据、任务调度。

```
设备 A ── 认证会话(挑战/响应) ──► 设备 B
   │                                   │
   └─ HUKS 密钥协商 → 会话密钥 ◄───────┘
            ↓
   软总线安全通道建立（后续所有分布式流量加密）
```

## 四、数据安全防护

- **存储加密**：系统支持文件级加密（FBE），不同密钥保护不同文件，灭屏后敏感文件不可访问；用户数据分区在首次启动时完成加密初始化。
- **传输加密**：跨设备流量经由软总线加密通道（见上），应用无需自己实现传输层安全。
- **隐私数据分级**：数据按敏感度分为公共、内部、敏感、临界等级别，越敏感则访问控制与加密要求越强，越需要明确的用户授权。

## 五、应用签名与完整性校验

- **签名机制**：系统应用与预置应用必须使用平台私钥签名；第三方应用由应用市场或开发者签名。签名私钥不出开发环境，设备内只内置对应公钥用于验签。
- **校验时机**：
  - 安装时：[25-包管理子系统](../../08-app-framework/25-bao-guan-li-zi-xi-tong.md) 校验签名合法性，拒绝未签名或签名不符的包；
  - 升级时：[22-OTA升级子系统](../../06-quality-test/22-ota-sheng-ji-zi-xi-tong.md) 校验整包与差分包签名；
  - 运行时：关键系统组件可被度量比对，防止被替换。

## 六、常见问题与排查

1. **密钥导出失败**：HUKS 默认禁止导出私钥明文，这是安全设计而非异常；如需备份，应使用"密钥封装 / 导入加密密钥"等受控机制。
2. **无 TEE 的设备性能下降**：软件回退实现缺少硬件加速，大量加解密时耗时会显著上升。
3. **设备认证失败**：多为两台设备未登录同一帐号或群组关系已失效，可在"超级终端"中重新确认信任关系。

## 相关阅读

- [23-权限与访问控制](../23-quan-xian-guan-li-zi-xi-tong.md)
- [18-分布式硬件](../../05-media-distributed/18-fen-bu-shi-ying-jian.md)
- [16-分布式软总线](../../05-media-distributed/16-fen-bu-shi-ruan-zong-xian.md)
- [09-HDF驱动框架](../../03-driver-boot/09-hdf-qu-dong-kuang-jia.md)

## 参考资源

- OpenHarmony 安全子系统官方文档（代码仓 `security_*`）
- HUKS Native API 源码：`foundation/security/huks`
- 设备认证源码：`foundation/deviceauth`
