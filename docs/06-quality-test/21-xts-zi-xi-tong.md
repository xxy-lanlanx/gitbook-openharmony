---
description: XTS子系统
---

# 21-XTS子系统





## 简介





XTS子系统是OpenHarmony兼容性测评套件的集合，当前包括acts（application compatibility test suite）应用兼容性测试套件，后续会拓展dcts（device compatibility test suite）设备兼容性测试套件等。





XTS子系统当前包括acts与tools软件包：





acts，存放acts相关测试用例源码与配置文件，其目的是帮助终端设备厂商尽早发现软件与OpenHarmony的不兼容性，确保软件在整个开发过程中满足OpenHarmony的兼容性要求。





tools，存放acts相关测试用例开发框架。





## 结构





```


/test/xts


├── acts                # 测试代码存放目录


│   └── subsystem       # 标准系统子系统测试用例源码存放目录


│   └── subsystem_lite  # 轻量系统、小型系统子系统测试用例源码存放目录


│   └── BUILD.gn        # 标准系统测试用例编译配置


│   └── build_lite      # 轻量系统、小型系统测试用例编译配置存放目录


│       └── BUILD.gn    # 轻量系统、小型系统测试用例编译配置


└── tools               # 测试工具代码存放目录


```





参考文档：[https://gitcode.com/openharmony/docs/blob/master/zh-cn/readme/XTS%E5%AD%90%E7%B3%BB%E7%BB%9F.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/readme/XTS%E5%AD%90%E7%B3%BB%E7%BB%9F.md)

## 组成与定位

XTS 的全称是 X Test Suite，是 OpenHarmony 为"兼容性"量身打造的测评体系。OpenHarmony 是一个开源、可裁剪的操作系统，不同厂商在移植时可能对接口、行为做改动，导致应用或设备之间出现不兼容。XTS 通过一套标准化的测试套件，在设备出厂前验证其软件实现是否满足 OpenHarmony 的兼容性定义，从而保证"一次开发，多端部署"的承诺。

当前 XTS 主要由以下部分组成：

- **acts（Application Compatibility Test Suite）**：应用兼容性测试套件，验证系统对 OpenHarmony 标准 API、系统能力、应用框架等行为是否符合规范。这是目前最成熟、用例量最大的部分。
- **dcts（Device Compatibility Test Suite）**：设备兼容性测试套件，面向整机设备能力（如传感器、外设）的兼容性验证（规划/逐步落地中）。
- **hts（Hardware Test Suite）**：硬件抽象兼容性测试，验证 HDF 驱动框架相关硬件抽象是否达标。
- **tools**：测试用例开发框架与公共能力，供 acts/dcts 复用，包含用例组织、断言、执行与报告能力。

## acts 测试组织方式

acts 的源码按"系统类型 + 子系统"两级组织：

```
/test/xts/acts
├── subsystem        # 标准系统：各子系统的测试用例源码
│   ├── ability      # Ability 子系统用例
│   ├── graphic      # 图形子系统用例
│   └── ...
├── subsystem_lite   # 轻量系统、小型系统用例
│   ├── kernel_lite  # LiteOS 内核用例
│   └── ...
├── build_lite       # 轻量/小型系统编译配置（BUILD.gn）
└── BUILD.gn         # 标准系统编译入口
```

每个子系统目录下，用例通常再按模块拆分，并配套 `test.json` 描述用例元信息（用例名、类型、执行条件等），由测试框架统一调度。

## 测试用例开发框架

XTS 提供两套互补的用例开发框架：

1. **JS/ArkTS 测试框架**：基于 Hypium（`@ohos/hypium`）测试引擎，用 `describe / it / expect` 组织用例，适合验证应用框架、系统 API、UI 行为。
2. **C/C++ 测试框架**：基于 gtest 封装，适合验证内核、驱动、Native 库等底层能力，断言、套件、Mock 能力齐全。

一个典型的 JS acts 用例：

```js
import { describe, it, expect } from '@ohos/hypium';

describe('ActsSampleTest', function () {
  it('should_return_true_when_call_api', 0, function () {
    const result = exampleApi();
    expect(result).assertTrue();
  });
});
```

## 编译与执行

以标准系统为例，使用 hb 构建目标并烧录/推送到设备后执行：

```bash
hb set            # 选择产品
hb build -T //test/xts/acts/ability:acts          # 仅构建某个子系统用例
hb build -T //test/xts/acts                       # 整体构建
```

用例通过测试框架在设备上运行，结果以 XML/报告形式回传，失败项会给出具体的断言位置与期望/实际值。

## 兼容性认证流程

1. 厂商基于 OpenHarmony 完成系统移植；
2. 在目标设备上全量运行对应系统类型的 acts（及逐步落地的 dcts/hts）；
3. 修复所有不兼容项，确保核心用例 100% 通过；
4. 提交兼容性测试报告，进入 OpenHarmony 兼容性认证（基于实测结果评审）；
5. 通过后可获得相应兼容性标识，其设备可被生态应用正常识别与支持。

XTS 的价值在于把"兼容"从口头约定变成可度量、可回归的工程纪律，避免生态碎片化。

## 相关阅读

- [DFX子系统](../20-dfx-zi-xi-tong.md)
- [架构篇](../../01-basic/04-jia-gou-pian.md)
