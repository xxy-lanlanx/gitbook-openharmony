---
description: OpenHarmony 全球化子系统（多语言、时区、格式化、资源分级）。
---

# 32-全球化与国际化

全球化子系统为应用提供多语言、时区与本地化格式化能力，并通过**资源限定词**实现按区域/设备自动加载正确资源。它让同一份代码与逻辑能面向不同国家、语言、地区的用户，是应用出海与"一套工程多区域发布"的基础。

## 一、资源管理

资源按**目录 + 限定词**组织，系统根据设备当前的语言、地区、屏幕、横竖屏等自动选择最匹配的资源：

```
resources/
 ├─ base/            # 默认（兜底）
 │   └─ element/string.json
 ├─ zh_CN/           # 中文（中国）
 │   └─ element/string.json
 ├─ en_US/           # 英文（美国）
 │   └─ element/string.json
 └─ phone/           # 按设备类型
     └─ media/icon.png
```

限定词可叠加：语言_地区（`zh_CN`）、屏幕密度、设备类型、横竖屏等。缺少对应限定词时回退到 `base`。

## 二、国际化（i18n）

- **格式化**：数字、日期、货币、百分比等按区域规则格式化，避免手写拼接；
- **时区**：统一使用标准时区 API，避免服务器/设备时区不一致导致的显示错误；
- **单复数 / 复数**：不同语言复数规则不同，通过资源中的复数条目处理。

```ts
import { intl } from '@kit.InternationalizationKit';

const nf = new intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY' });
console.info(nf.format(1234.5));   // ¥1,234.50

const df = new intl.DateTimeFormat('en-GB', { dateStyle: 'medium' });
console.info(df.format(new Date())); // 25 Jun 2026
```

## 三、区域与 RTL

- **RTL（从右到左）**：阿拉伯语、希伯来语等布局方向为 RTL；应通过布局方向（layout_direction）与对称边距适配，而非固定左右。
- **区域差异**：日期顺序（日/月/年 vs 月/日/年）、姓名顺序、纸张尺寸等需随区域调整。
- 建议：UI 布局用相对约束（start/end）而非绝对（left/right），自动跟随语言方向。

## 四、常见问题与排查

1. **显示英文而非中文**：资源目录限定词与设备语言不匹配，或 `base` 兜底缺失；检查 `zh_CN` 目录与 `string.json` 键名一致。
2. **时间显示错误**：未使用标准时区 API，或拼接 `new Date()` 字符串而非格式化输出。
3. **RTL 未镜像**：布局写死 left/right，应改用 start/end 与方向感知属性。

## 相关阅读

- [24-元能力Ability框架](24-ying-yong-kuang-jia-ability.md)
- [25-包管理子系统](25-bao-guan-li-zi-xi-tong.md)
- [05-源码结构](05-yuan-ma-jie-gou.md)

## 参考资源

- OpenHarmony 全球化与国际化官方文档（代码仓 `global`、资源管理 `resource_manager`）
- ArkTS 接口：`@kit.InternationalizationKit`、`@kit.LocalizationKit`
