# 性能调优

性能调优是 OpenHarmony 系统开发与应用开发中的关键环节，涵盖启动速度、内存占用、CPU 使用率、图形渲染、功耗等多个维度。本章介绍系统与应用层面常用的性能分析工具和优化手段，帮助开发者定位瓶颈并提升用户体验。

## 性能分析工具

### 1. SmartPerf

SmartPerf 是 OpenHarmony 官方提供的性能分析工具，支持抓取 CPU、内存、GPU、网络、启动耗时等全量性能数据，并生成可视化报告。

- **启动耗时分析**：自动标记应用冷启动各阶段（进程创建、Ability 加载、首帧绘制）。
- **内存剖析**：抓取内存快照，分析 Native Heap、ArkTS Heap、GFX 内存分布。
- **帧率分析**：统计丢帧率、卡顿帧，定位渲染瓶颈。

### 2. HiPerf

HiPerf 是基于 Linux perf 的轻量级采样分析器，适合线下深入分析 CPU 热点：

```bash
# 采集 10 秒 CPU 性能数据
hiperf record -a --duration 10 -o /data/perf.data

# 查看热点函数
hiperf report -i /data/perf.data
```

### 3. hilog 与 HiTrace

- **hilog**：过滤高耗时日志，定位异常耗时操作。
- **HiTrace**：分布式跟踪工具，可追踪跨进程、跨设备的调用链，分析端到端延迟。

```ts
import hiTrace from '@ohos.hiTraceChain';

let traceId = hiTrace.begin('MyOperation');
// 执行业务逻辑
hiTrace.end(traceId);
```

## 常用优化手段

### 1. 启动优化

| 优化方向 | 具体措施 |
|---------|---------|
| 减少 Ability 初始化 | 延迟加载非首屏模块，避免在 `onCreate()` 中执行耗时操作 |
| 资源预加载 | 使用 `prelauncher` 提前加载高频资源 |
| 布局优化 | 减少嵌套层级，避免过度绘制，使用 `LazyForEach` 延迟加载列表 |
| 编译优化 | 开启 ArkCompiler AOT 编译，减少运行时解释开销 |

### 2. 内存优化

- **对象池**：对频繁创建/销毁的对象（如列表项、动画帧）使用对象池复用。
- **及时释放**：在页面 `onDestroy()` 中取消订阅、清除定时器、释放大图缓存。
- **避免内存泄漏**：注意 `setInterval`、`addEventListener` 等未清理的引用。
- **大图压缩**：使用适当的图片分辨率，启用 `Image` 组件的 `decodingSize` 限制解码尺寸。

### 3. 渲染优化

- **减少重排重绘**：避免频繁修改布局属性（`width`、`height`、`position`），优先使用 `transform` 和 `opacity`。
- **异步加载**：图片、字体、网络数据使用异步加载，避免阻塞主线程。
- **GPU 加速**：对复杂动画开启 GPU 合成层，利用硬件加速渲染。
- **脏区域渲染**：仅重绘变化区域，减少每帧 GPU 负载。

### 4. 功耗优化

- **降低刷新率**：非动画场景降低屏幕刷新率至 60Hz 或以下。
- **传感器节制**：不需要时及时取消传感器订阅，使用批处理模式降低采样频率。
- **后台限制**：后台任务使用 `WorkScheduler` 或 `BackgroundTask`，避免常驻 CPU。
- **网络聚合**：合并网络请求，减少射频唤醒次数。

## 系统级调优

### 1. 内核参数调优

```bash
# 调整虚拟内存脏页回写周期
echo 500 > /proc/sys/vm/dirty_expire_centisecs

# 调整 swappiness，降低交换倾向
echo 10 > /proc/sys/vm/swappiness

# 开启 CPU 调频策略（interactive / schedutil）
echo schedutil > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor
```

### 2. 进程优先级与调度

- 对前台应用设置更高的 `nice` 值或 CFS 优先级。
- 使用 `SCHED_FIFO` 对实时音频/视频线程进行调度，降低抖动。

### 3. 文件系统优化

- 使用 `f2fs` 替代 `ext4` 提升闪存读写性能。
- 定期执行 `fs_trim` 释放废弃块，维持 SSD 性能。

## 典型场景优化案例

### 场景一：列表滑动卡顿

**问题**：长列表滑动时丢帧严重。
**分析**：SmartPerf 显示 `List` 组件每项布局复杂，每次滑动触发大量布局计算。
**优化**：
1. 将列表项拆分为更细粒度的自定义组件，减少不必要的状态变量。
2. 使用 `LazyForEach` + `cachedCount` 控制缓存数量。
3. 图片使用 `syncLoad(false)` 异步加载，避免主线程阻塞。

### 场景二：应用后台耗电异常

**问题**：应用切后台后仍持续占用 CPU。
**分析**：hilog 发现后台定时器未清理，持续执行网络轮询。
**优化**：
1. 在 `onBackground()` 生命周期中清理所有定时器和动画。
2. 使用 `WorkScheduler` 替代 `setInterval`，让系统统一调度后台任务。
3. 使用 `Push` 服务替代客户端轮询，减少网络唤醒。

### 场景三：开机启动慢

**问题**：系统开机到桌面显示耗时超过 30 秒。
**分析**：HiTrace 显示 `init` 阶段启动服务过多且串行执行，HDI 驱动加载阻塞。
**优化**：
1. 将非关键服务（如位置、蓝牙）延迟到桌面显示后启动。
2. 并行化 `init` 脚本中的独立服务启动。
3. 对 HDF 驱动进行按需加载，避免一次性加载所有驱动。

## 调试与验证

- **性能基准测试**：在优化前建立性能基线（启动时间、内存峰值、帧率），优化后对比验证。
- **压力测试**：使用 `XTS` 或自定义脚本进行长时间压测，检查内存泄漏和稳定性。
- **用户体验指标**：关注 `Time to First Frame (TTFF)`、`Time to Interactive (TTI)` 等用户可感知指标。

## 相关阅读

- [SmartPerf 使用指南](https://gitee.com/openharmony/docs/blob/master/zh-cn/device-dev/subsystems/subsys-perf-guide.md)
- [HiPerf 工具文档](https://gitee.com/openharmony/docs/blob/master/zh-cn/device-dev/debug/hiperf.md)
- [HiTrace 分布式跟踪](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/dfx/hitrace.md)
- [应用性能优化最佳实践](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/performance/)
