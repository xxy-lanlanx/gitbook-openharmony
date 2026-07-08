---
description: ArkCompiler 方舟编译器——OpenHarmony 的统一编译运行时
---

# ArkCompiler 方舟编译器

## 简介

ArkCompiler 是 OpenHarmony 自研的统一编译运行时，承担将 ArkTS/TS/JS 代码转换为机器可执行指令的核心职责。相比传统 JavaScript 引擎（如 V8、JavaScriptCore）的纯解释或 JIT 执行方式，ArkCompiler 在架构上做了两大革新：**AOT（Ahead-of-Time）静态编译** 与 **类型系统增强**，使 OpenHarmony 应用在启动速度、运行性能与内存占用方面获得显著提升。

## 核心特性

| 特性 | 说明 | 收益 |
|------|------|------|
| **AOT 编译** | 应用在安装或编译阶段将 TS/JS 编译为机器码/字节码，运行时直接执行 | 启动快、运行期无编译开销 |
| **类型系统** | 在 ArkTS 中引入静态类型，编译期做类型检查与优化 | 减少运行时类型错误、提升编译优化空间 |
| **统一运行时** | 同一套引擎运行 ArkTS/TS/JS，API 语义一致 | 降低开发者心智负担 |
| **多语言互操作** | 通过 NAPI 与 C/C++ 代码互调，实现高性能计算下沉 | 兼顾开发效率与性能 |

## 编译流水线

ArkCompiler 的编译过程大致分为以下阶段：

```
ArkTS / TS / JS 源码
  │
  ▼
Parser（词法/语法分析）→ AST
  │
  ▼
TypeChecker（类型检查）→ 带类型注解的 AST
  │
  ▼
IR 生成 → ArkCompiler 中间表示（IR）
  │
  ▼
Optimizer（优化器）→ 内联、死代码消除、逃逸分析等
  │
  ▼
CodeGen（代码生成）→ 字节码（.abc）或机器码
  │
  ▼
Runtime 加载 → 执行
```

- **Parser**：将源码解析为抽象语法树（AST），支持 ArkTS 扩展语法（如声明式 UI、装饰器）。
- **TypeChecker**：基于 ArkTS 的类型注解进行静态类型检查，提前暴露类型错误；同时类型信息用于后续优化。
- **IR 生成与优化**：将 AST 转换为 ArkCompiler 专有的中间表示，执行常量折叠、循环优化、内联等经典编译优化。
- **CodeGen**：根据目标架构生成可执行代码。标准设备上可生成机器码；资源受限设备上生成紧凑字节码，由运行时解释器执行。

## 字节码与 .abc 文件

ArkCompiler 将源码编译为 `.abc`（Ark ByteCode）文件，这是 OpenHarmony 应用的标准可执行单元：

- **HAP 打包**：DevEco Studio 编译工程时，将 ArkTS 源码编译为 `.abc`，并打包进 HAP 的 `ets` 目录；
- **运行时加载**：应用启动时，ArkRuntime 从 HAP 中加载 `.abc`，解析为内部对象模型，准备执行环境；
- **版本兼容**：`.abc` 格式与 ArkRuntime 版本绑定，大版本升级时可能需要重新编译应用。

## 运行时架构

ArkRuntime 负责 `.abc` 的加载、执行与内存管理：

```
ArkRuntime
 ├── Memory Manager（GC：分代垃圾回收）
 ├── Execution Engine（解释器 / AOT 机器码执行器）
 ├── Object Model（对象布局、隐藏类、内联缓存）
 ├── NAPI Bridge（与 Native C++ 互调）
 └── Debugger / Profiler（调试与性能分析接口）
```

- **内存管理**：采用分代垃圾回收（Generational GC），新对象在年轻代快速回收，长生命对象晋升到老年代。相比传统 JS 引擎的 GC，ArkRuntime 针对 ArkTS 的静态类型信息做了指针压缩与分配优化，减少 GC 停顿。
- **执行引擎**：根据编译模式选择解释执行或 AOT 机器码直接执行。热路径上的函数会被优先编译为机器码。
- **对象模型**：基于隐藏类（Hidden Class）与内联缓存（Inline Cache）优化属性访问，使动态类型语言的属性读写接近静态语言性能。

## AOT vs JIT 对比

| 维度 | ArkCompiler AOT | 传统 JIT（如 V8） |
|------|-----------------|-------------------|
| 编译时机 | 安装/构建阶段 | 运行时即时编译 |
| 启动速度 | 快（无需运行时编译） | 慢（需预热编译） |
| 运行时性能 | 稳定高（已编译为机器码） | 高但波动（编译开销） |
| 内存占用 | 较小（无运行时编译器常驻） | 较大（JIT编译器+优化缓存） |
| 安装包体积 | 略大（含机器码） | 较小（仅字节码） |
| 适用场景 | 手机、平板、车机 | 浏览器、动态脚本 |

## 与 NAPI 的协同

ArkCompiler 通过 NAPI（Native API）桥接 ArkTS 与 C/C++ 世界：

- 当 ArkTS 调用 `requireNapi` 加载 Native 模块时，ArkRuntime 通过 NAPI 接口查找并调用已注册的 `napi_module`；
- 数据在 ArkTS 类型与 C 类型之间做转换（如 `string` ↔ `char*`、`Array` ↔ `std::vector`）；
- 高频计算场景（如图像处理、编解码、物理引擎）建议用 C++ 实现并通过 NAPI 暴露给 ArkTS，兼顾开发效率与性能。

> 更多 NAPI 细节请参考 [07-NAPI接口](../07-napi-jie-kou.md)。

## 调试与调优

- **日志**：ArkCompiler 编译错误与运行时异常通过 `HiLog` 输出，可用 `hilog` 命令过滤 `ArkCompiler`/`ArkRuntime` 标签；
- **性能分析**：ArkRuntime 内置 Profiler 接口，可采集 CPU 火焰图、内存分配快照、GC 频率，帮助定位性能瓶颈；
- **调试**：DevEco Studio 支持 ArkTS 源码级调试（断点、单步、变量查看），调试器通过 JDWP 协议与 ArkRuntime 通信。

## 相关阅读

- [07-NAPI接口](../07-napi-jie-kou.md)
- [07-NAPI接口-aki](../07-napi-jie-kou-aki.md)
- [06-Native库](../06-native-ku.md)
- [24-元能力Ability框架](../../08-app-framework/24-ying-yong-kuang-jia-ability.md)

## 参考资源

- ArkCompiler 官方文档（代码仓 `arkcompiler`）
- ArkTS 语言规范（OpenHarmony 应用开发文档）
- DevEco Studio 编译与调试指南
