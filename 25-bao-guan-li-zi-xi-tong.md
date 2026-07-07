---
description: OpenHarmony 应用包管理（HAP/App Pack、包结构、安装/卸载、包信息查询）。
---

# 25-包管理子系统

包管理子系统（Bundle Manager）负责应用包的安装、卸载与信息查询，是[24-元能力Ability框架](24-ying-yong-kuang-jia-ability.md) 落地的基础——Ability 的注册、启动、权限授予都依赖它维护的包信息。本章说明 OpenHarmony 的应用包结构、安装流程与包信息管理能力。

## 一、应用包结构

OpenHarmony 的发布与部署采用分层包设计：

| 概念 | 说明 |
| --- | --- |
| **App Pack（.app）** | 应用发布形态，一个应用一个 `.app`，内部含一个或多个 HAP |
| **HAP（HarmonyOS Ability Package）** | 部署形态，分两类：`entry`（主入口，应用唯一）、`feature`（可按设备能力按需分发） |
| **HAR（HarmonyOS Archive）** | 静态共享包（库），编译期打入引用方，类似 aar/jar |
| **HSP（HarmonyOS Shared Package）** | 动态共享包，运行时多模块共享，支持按需加载 |

一个 HAP 内部关键组成：

```
module/
 ├─ module.json5      # Ability、权限、deviceTypes 等声明
 ├─ pack.info         # 包内 HAP 列表与版本信息
 ├─ ets/              # 编译后的 ArkUI/方舟字节码
 ├─ resources/        # 资源与限定词（语言/屏幕/地区）
 └─ libs/             # 原生库（如有）
```

## 二、安装与卸载流程

**安装**（以 [23-安全子系统](23-an-quan-zi-xi-tong.md) 的签名校验为前提）：

```
解析包 → 校验签名 → 校验权限声明与 APL
   → 解压到 /data/app/<bundle>/
   → 创建应用沙箱目录（见 33-文件与存储）
   → 向 AMS/samgr 注册 Ability
   → 写入包信息数据库
```

**卸载**：停止运行 → 删除沙箱与安装目录 → 注销 Ability → 清理包信息数据库记录。

> 覆盖安装要求**签名一致**；签名不同会被拒绝，需先卸载旧版。

## 三、包信息管理（BundleManager）

系统与应用可通过 `bundleManager` 查询已安装包的信息：

```ts
import { bundleManager } from '@kit.AbilityKit';

// 查询自身包信息（携带 Ability 列表）
const info = bundleManager.getBundleInfoForSelf(
  bundleManager.BundleFlag.GET_BUNDLE_INFO_WITH_ABILITIES
);
console.info(`包名: ${info.name}, 版本: ${info.versionName}`);
console.info(`Ability 数量: ${info.abilityInfos.length}`);

// 查询指定包（需权限）
const other = bundleManager.getBundleInfo('com.example.other',
  bundleManager.BundleFlag.GET_BUNDLE_INFO_DEFAULT);
```

常用能力：`getApplicationInfo`、`getAllBundleInfo`、`queryAbilityByWant`（按 Want 反查可处理的 Ability）。

## 四、多设备分发与兼容性

同一 App Pack 可内含适配 phone / tablet / tv / wearable 的不同 HAP，安装时**按设备类型选装**：

- `module.json5` 的 `deviceTypes` 声明该 HAP 支持的设备类型；
- `distributionFilter` 可按 API 版本、屏幕、地区等条件过滤，实现"一台设备只装它需要的 HAP"，减小体积、提升兼容。

## 五、常见问题与排查

1. **覆盖安装失败**：签名不一致，需先卸载旧版本或使用相同签名证书。
2. **安装报权限错误**：申请的权限 APL 高于自身等级（见 [23-权限与访问控制](23-quan-xian-guan-li-zi-xi-tong.md)）。
3. **HAP 未安装到目标设备**：`deviceTypes` 未包含该设备类型，或 `distributionFilter` 把该设备过滤掉了。
4. **查询不到别的包**：跨应用查询包信息可能受权限约束，确认是否已申请并授予相应权限。

## 相关阅读

- [24-元能力Ability框架](24-ying-yong-kuang-jia-ability.md)
- [23-权限与访问控制](23-quan-xian-guan-li-zi-xi-tong.md)
- [33-文件与存储子系统](33-wen-jian-cun-chu-zi-xi-tong.md)
- [05-源码结构](05-yuan-ma-jie-gou.md)

## 参考资源

- OpenHarmony 包管理官方文档（代码仓 `bundlemanager`）
- ArkTS 接口：`@kit.AbilityKit` 中的 `bundleManager`
