---
description: OpenHarmony 帐号与用户身份管理（系统帐号、分布式帐号、用户身份 IAM）。
---

# 34-帐号与用户身份

帐号与用户身份子系统管理设备的系统帐号、分布式帐号同步与多用户身份。它和[23-安全子系统](../../07-security/23-an-quan-zi-xi-tong.md) 的设备认证、[23-权限与访问控制](../../07-security/23-quan-xian-guan-li-zi-xi-tong.md) 的权限上下文一起，回答了"谁在使用这台设备、能否互信协同"的问题——分布式能力是否可用，很大程度取决于帐号状态。

## 一、系统帐号（OS Account）

系统帐号是设备上的"身份主体"，通常是登录的厂商帐号：

- **创建 / 切换 / 删除**：设备可存在多个系统帐号（主帐号、子帐号、访客）；
- **分布式前提**：同一帐号登录的多台设备会自动建立互信群组，这正是 [23-安全子系统](../../07-security/23-an-quan-zi-xi-tong.md) 设备认证与 [27-分布式任务调度](../../05-media-distributed/27-fen-bu-shi-ren-wu-diao-du.md) 协同的基础。

```ts
import { osAccount } from '@kit.BasicServicesKit';

const mgr = osAccount.getAccountManager();
// 创建访客帐号
mgr.createOsAccount('guest', osAccount.OsAccountType.GUEST, (err, id) => {
  if (!err) console.info(`已创建访客帐号 id=${id}`);
});
```

## 二、分布式帐号

- 同帐号在跨设备间**同步身份**，使"我在手机上的帐号就是平板上的同一帐号"；
- 设备认证（见安全章）正是基于帐号群组派生的共享凭据，从而让流转、硬件共享只对同帐号设备开放。

## 三、多用户与身份（IAM）

- **多用户隔离**：主用户 / 子用户 / 访客各自拥有独立沙箱、应用数据与权限上下文，互不可见——这是 [33-文件与存储](../33-wen-jian-cun-chu-zi-xi-tong.md) 沙箱隔离在用户维度的延伸。
- **IAM（Identity and Access Management）**：统一管理身份与权限上下文，确保每个操作都在正确的用户/权限边界内执行。

## 四、与设备认证的关系

帐号与设备认证是"可信协同"的两端：

```
帐号回答 "我是谁"（身份）   ─┐
                            ├─→ 同帐号 + 已认证设备 = 可信协同（流转/硬件/数据）
设备认证回答 "这台设备可信" ─┘
```

只有当两台设备**登录同一帐号且完成设备认证**，分布式能力才会对应用开放；任一条件不满足，跨设备调用将被拒绝。

## 五、常见问题与排查

1. **分布式能力不可用**：两台设备未登录同一帐号，或某台未通过设备认证——在"超级终端"中确认。
2. **多用户数据不互通**：属设计预期，不同用户沙箱独立；如需共享应通过公共目录或分布式数据。
3. **切换帐号后需重认证**：切换/登出会使既有设备群组凭据失效，重新登录后需再次确认信任关系。

## 相关阅读

- [23-安全子系统](../../07-security/23-an-quan-zi-xi-tong.md)
- [23-权限与访问控制](../../07-security/23-quan-xian-guan-li-zi-xi-tong.md)
- [27-分布式任务调度](../../05-media-distributed/27-fen-bu-shi-ren-wu-diao-du.md)

## 参考资源

- OpenHarmony OS 帐号官方文档（代码仓 `os_account`）
- ArkTS 接口：`@kit.BasicServicesKit` 中的 `osAccount`
