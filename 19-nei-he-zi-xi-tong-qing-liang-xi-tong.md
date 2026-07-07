---
description: 内核子系统-轻量系统
---

# 19-内核子系统-轻量系统





## 简介





OpenHarmony LiteOS-M内核是面向IoT领域构建的轻量级物联网操作系统内核，具有小体积、低功耗、高性能的特点。其代码结构简单，主要包括内核最小功能集、内核抽象层、可选组件以及工程目录等。支持驱动框架HDF（Hardware Driver Foundation），统一驱动标准，为设备厂商提供了更统一的接入方式，使驱动更加容易移植，力求做到一次开发，多系统部署。





OpenHarmony LiteOS-M内核架构包含硬件相关层以及硬件无关层，如下图所示，其中硬件相关层按不同编译工具链、芯片架构分类，提供统一的HAL（Hardware Abstraction Layer）接口，提升了硬件易适配性，满足AIoT类型丰富的硬件和编译工具链的拓展；其他模块属于硬件无关层，其中基础内核模块提供基础能力，扩展模块提供网络、文件系统等组件能力，还提供错误处理、调测等能力，KAL（Kernel Abstraction Layer）模块提供统一的标准接口。





## 架构





![](assets/image-58.png)





## 结构





```


/kernel/liteos_m


├── arch                 # 内核指令架构层目录


│   ├── arm              # arm 架构代码


│   │   ├── arm9         # arm9 架构代码


│   │   ├── cortex-m3    # cortex-m3架构代码


│   │   ├── cortex-m33   # cortex-m33架构代码


│   │   ├── cortex-m4    # cortex-m4架构代码


│   │   ├── cortex-m55   # cortex-m55架构代码


│   │   ├── cortex-m7    # cortex-m7架构代码


│   │   └── include      # arm架构公共头文件目录


│   ├── csky             # csky架构代码


│   │   └── v2           # csky v2架构代码


│   ├── include          # 架构层对外接口存放目录


│   ├── risc-v           # risc-v 架构


│   │   ├── nuclei       # 芯来科技risc-v架构代码


│   │   └── riscv32      # risc-v官方通用架构代码


│   └── xtensa           # xtensa 架构代码


│       └── lx6          # xtensa lx6架构代码


├── components           # 可选组件


│   ├── backtrace        # 栈回溯功能


│   ├── cppsupport       # C++支持


│   ├── cpup             # CPUP功能


│   ├── dynlink          # 动态加载与链接


│   ├── exchook          # 异常钩子


│   ├── fs               # 文件系统


│   ├── lmk              # Low memory killer 机制


│   ├── lms              # Lite memory sanitizer 机制


│   ├── net              # Network功能


│   ├── power            # 低功耗管理


│   ├── shell            # shell功能


│   └── trace            # trace 工具


├── drivers              # 驱动框架Kconfig


├── kal                  # 内核抽象层


│   ├── cmsis            # cmsis标准接口支持


│   └── posix            # posix标准接口支持


├── kernel               # 内核最小功能集支持


│   ├── include          # 对外接口存放目录


│   └── src              # 内核最小功能集源码


├── testsuites           # 内核测试用例


├── tools                # 内核工具


├── utils                # 通用公共目录





```

## 相关阅读

- [内核子系统-标准系统Linux](19-nei-he-zi-xi-tong-biao-zhun-xi-tong-linux.md)
- [启动流程](10-qi-dong-liu-cheng.md)
