# 20-DFX子系统

## 简介

在OpenHarmony中，DFX([Design for X](https://en.wikipedia.org/wiki/Design\_for\_X))是为了提升质量属性的软件设计，目前包含的内容主要有：DFR（Design for Reliability，可靠性）和DFT（Design for Testability，可测试性）特性。

提供以下功能：

* HiLog流水日志，标准系统类设备（参考内存≥128MB）适用、HiLog\_Lite轻量流水日志，轻量系统类设备（参考内存≥128KiB），小型系统类设备（参考内存≥1MiB）适用。
* HiTraceChain分布式跟踪，标准系统类设备（参考内存≥128MiB）适用。
* HiTraceMeter性能跟踪，标准系统类设备（参考内存≥128MiB）适用。
* HiCollie卡死故障检测，标准系统类设备（参考内存≥128MiB）适用。
* HiSysEvent系统事件埋点，标准系统类设备（参考内存≥128MiB）适用。
* HiDumper信息导出，标准系统类设备（参考内存≥128MB）适用。
* Faultlogger崩溃故障检测，标准系统类设备（参考内存≥128MB）适用。
* Hiview插件平台，标准系统类设备（参考内存≥128MB）适用。
* HiAppEvent应用事件及HiChecker缺陷扫描仅供应用开发者使用。

## 结构

<figure><img src=".gitbook/assets/image (63).png" alt=""><figcaption></figcaption></figure>

参考文档：[https://gitcode.com/openharmony/docs/blob/master/zh-cn/readme/DFX%E5%AD%90%E7%B3%BB%E7%BB%9F.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/readme/DFX%E5%AD%90%E7%B3%BB%E7%BB%9F.md)

