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

### 资源编译与打包

开发阶段资源按目录组织，编译时 DevEco Studio 会将资源编译为二进制索引格式，打包进 HAP。运行时系统根据设备当前配置（语言、地区、屏幕等）解析索引，加载最匹配的限定词资源。这意味着：

- 增加语言只需新增限定词目录，无需修改代码；
- 删除未使用的限定词可减小包体积；
- `base` 必须完整，否则找不到资源会崩溃。

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

## 三、动态语言切换

系统支持在设置中切换语言，切换后：

- 应用进程会被重新加载或通知配置变更；
- 新启动的 Ability 自动使用新语言资源；
- 已缓存的格式化对象需重新创建，避免 stale 数据。

应用无需手动处理大部分资源重载，但自定义的日期/货币格式器应在 `onConfigurationUpdated` 等生命周期中重建。

## 四、区域与 RTL

- **RTL（从右到左）**：阿拉伯语、希伯来语等布局方向为 RTL；应通过布局方向（layout_direction）与对称边距适配，而非固定左右。
- **区域差异**：日期顺序（日/月/年 vs 月/日/年）、姓名顺序、纸张尺寸等需随区域调整。
- 建议：UI 布局用相对约束（start/end）而非绝对（left/right），自动跟随语言方向。

## 五、全球化在系统服务中的使用

不仅应用需要全球化，系统服务本身也依赖全球化子系统：

| 系统服务 | 全球化依赖 |
|----------|------------|
| 设置 | 语言列表、地区列表、时区选择 |
| 通知 | 时间戳格式化、日期显示 |
| 日历/闹钟 | 节假日、周首日、12/24 小时制 |
| 输入法 | 键盘布局、语言模型 |
| 应用商店 | 内容区域过滤、价格货币转换 |

## 六、测试与验证

- **伪本地化（Pseudolocalization）**：在测试阶段用自动生成的伪语言（如扩展字符、长文本）验证 UI 是否截断或布局错乱。
- **RTL 模拟**：在 DevEco Studio 或系统开发者选项中强制 RTL，检查镜像与对齐。
- **多语言遍历**：至少覆盖主要目标语言，确认字符串完整、无硬编码。

## 七、常见问题与排查

1. **显示英文而非中文**：资源目录限定词与设备语言不匹配，或 `base` 兜底缺失；检查 `zh_CN` 目录与 `string.json` 键名一致。
2. **时间显示错误**：未使用标准时区 API，或拼接 `new Date()` 字符串而非格式化输出。
3. **RTL 未镜像**：布局写死 left/right，应改用 start/end 与方向感知属性。
4. **资源包体积过大**：未使用限定词叠加，重复存放相同资源；可通过资源优化工具去重。

## 相关阅读

- [24-元能力Ability框架](../../08-app-framework/24-ying-yong-kuang-jia-ability.md)
- [25-包管理子系统](../../08-app-framework/25-bao-guan-li-zi-xi-tong.md)
- [05-源码结构](../../02-framework/05-yuan-ma-jie-gou.md)

## 参考资源

- OpenHarmony 全球化与国际化官方文档（代码仓 `global`、资源管理 `resource_manager`）
- ArkTS 接口：`@kit.InternationalizationKit`、`@kit.LocalizationKit`
