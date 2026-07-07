---
description: OpenHarmony 编译构建体系（hb 命令行、GN/Ninja、部件/特性/产品配置、编译产物）。
---

# 26-编译构建子系统

OpenHarmony 使用 **hb 命令行**配合 **GN / Ninja** 完成源码编译与镜像生成。理解构建体系是把[05-源码结构](05-yuan-ma-jie-gou.md) 变成可烧录固件的关键一步，也是定位"为什么编不出来""怎么加一个新部件"的基础。

## 一、构建工具链

| 工具 | 角色 |
| --- | --- |
| **hb** | Python 封装的构建入口（`ohos-build` 仓），统一 `set / build / clean` 等命令 |
| **GN** | 元构建工具（源自 Chromium），读取 `BUILD.gn` 生成 Ninja 构建描述（定义"构建什么"） |
| **Ninja** | 真正的执行器，按 `.ninja` 文件执行编译 / 链接，快且支持增量 |
| **clang / llvm** | 编译器与链接器（lld），部分场景用 gcc |

整体链路：`hb build` → 调 `gn gen out/<product>` → 生成 ninja 文件 → `ninja` 执行编译链接。

## 二、配置模型（层级）

OpenHarmony 以"产品 → 单板 → 设备族 → 子系统 → 部件 → 特性"组织配置：

```
product（产品，如 rk3568 / hi3516）
  └─ board（单板）
       └─ device（设备族）
            └─ subsystem（子系统，如 ability、distributedhardware）
                 └─ component（部件，如 ability_runtime）
                      └─ feature（特性开关）
```

关键配置文件：

- 产品配置：`productdefine/common/products/<product>.json` 或通过 `build-profile.json5` 声明包含的 `subsystem` / `parts`；
- 部件声明：各部件根目录 `bundle.json` 写明 `subsystem`、`component`、`parts`、`system_capability`；
- 构建描述：源码目录中的 `BUILD.gn`，声明源文件、头目录、依赖。

核心 GN 变量：`product_name`、`ohos_components`、`device_name` 等，决定哪些部件参与编译。

## 三、编译流程

```bash
# 1) 进入源码根目录，初始化环境（首次）
source build/envsetup.sh

# 2) 选择产品（生成 ohos_config，指向产品配置）
hb set
#   交互选择如 rk3568

# 3) 查看当前环境
hb env

# 4) 全量/增量编译
hb build                 # 全量
hb build -T 目标名        # 指定目标
hb build 部件名           # 只编某部件（增量）
hb build --fast-rebuild  # 快速重编

# 5) 清理
hb clean
```

`gn gen` 与 `ninja` 由 `hb` 内部驱动；Ninja 只对变更文件重编，二次构建明显更快。

## 四、产物与镜像

编译产物位于 `out/<product>/`：

- `packages/phone/`（或对应设备类型）下生成系统镜像：`system.img`、`vendor.img`、`userdata.img`、`boot.img`、`ramdisk.img`；
- 镜像烧录到设备后，由 Bootloader 加载，进入 [10-启动流程](10-qi-dong-liu-cheng.md) 的内核与 init 阶段。

## 五、自定义部件与产品

新增一个部件的典型步骤：

1. 在子系统目录下新建部件目录，编写 `bundle.json` 声明 `subsystem` / `component` / `parts`；
2. 编写 `BUILD.gn` 描述源文件与依赖；
3. 将部件加入目标产品的 `parts` 列表；
4. `hb build 部件名` 验证可编。

```gn
import("//build/ohos.gni")

ohos_shared_library("mylib") {
  sources = [ "mylib.cpp" ]
  include_dirs = [ "." ]
  external_deps = [ "hilog:hilog" ]   # 声明对其它部件的依赖
  part_name = "my_part"
  subsystem_name = "my_subsystem"
}
```

## 六、常见问题与排查

1. **`hb: command not found`**：未 `source build/envsetup.sh` 或未 `pip install` 构建依赖；确认 Python 环境与 `hb` 已安装。
2. **GN 报错 `undefined variable`**：`BUILD.gn` 中变量名拼错或未 `import` 相应的 `.gni`。
3. **链接找不到符号**：依赖部件未在 `external_deps` 声明，或 `part_name` / `subsystem_name` 与 `bundle.json` 不一致。
4. **编译机 OOM**：全量构建内存占用大，调小并行度（`hb build -j N`）或增大交换分区。

## 相关阅读

- [05-源码结构](05-yuan-ma-jie-gou.md)
- [02-开发环境搭建篇](02-kai-fa-huan-jing-da-jian-pian.md)
- [10-启动流程](10-qi-dong-liu-cheng.md)
- [09-HDF驱动框架](09-hdf-qu-dong-kuang-jia.md)

## 参考资源

- OpenHarmony 编译构建官方文档（代码仓 `build`、`ohos-build`、`productdefine`）
- GN / Ninja 官方手册
