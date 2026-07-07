# 操作系统

## 什么是操作系统

维基百科上面的定义是：操作系统（英语：Operating System，缩写：OS）是一组主管并控制计算机操作、运用和运行硬件、软件资源和提供公共服务来组织用户交互的相互关联的系统软件程序，同时也是计算机系统的内核与基石。操作系统需要处理如管理与配置内存、决定系统资源供需的优先次序、控制输入与输出设备、操作网络与管理文件系统等基本事务。操作系统也提供一个让用户与系统交互的操作界面。

操作系统的类型非常多样，不同机器安装的操作系统可从简单到复杂，可从移动电话的嵌入式系统到超级计算机的大型操作系统。许多操作系统制造者对它涵盖范畴的定义也不尽一致，例如有些操作系统集成了图形用户界面，而有些仅使用命令行界面，将图形用户界面视为一种非必要的应用程序。

操作系统理论在计算机科学中，为历史悠久而又活跃\[1]的分支；而操作系统的设计与实现则是软件工业的基础与内核。

### Linux架构

<figure><img src=".gitbook/assets/image (74).png" alt=""><figcaption></figcaption></figure>

### Android架构

<figure><img src=".gitbook/assets/image (77).png" alt=""><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/image (78).png" alt=""><figcaption></figcaption></figure>

### window NT架构

<figure><img src=".gitbook/assets/image (75).png" alt=""><figcaption></figcaption></figure>

IOS架构-Darwin 架构

<figure><img src=".gitbook/assets/image (76).png" alt=""><figcaption></figcaption></figure>

Darwin的内核是XNU，XNU is Not Unix。XNU是两种技术的混合体，Mach和BSD。BSD层确保了Darwin系统的UNIX特性，真正的内核是Mach，但是对外部隐藏。BSD以上属于用户态，所有的内容都可以被应用程序访问，而应用程序不能访问内核态。当需要从用户态切换到内核态的时候，需要通过mach trap实现切换。

## 操作系统的演变

借鉴澎湃OS白皮书，新一代的操作系统，按发展路径和阶段可以分为四大类：一是由传 统的嵌入式 RTOS 发展而来；二是基于传统操作系统进行的“剪裁”和定制；三是专门面向 物联网研发的操作系统；四是新一代统一型操作系统，通常称为跨设备分布式操作系统。

<figure><img src=".gitbook/assets/image (68).png" alt=""><figcaption></figcaption></figure>

## 发展趋势（多内核共存）

关键字：跨端、多OS内核、统一可信安全、AI

<figure><img src=".gitbook/assets/image (69).png" alt=""><figcaption></figcaption></figure>

未来的物联网 OS，会是「多内核共存」的形式，每种内核负 责解决不同场景下的问题；这种架构下的 OS，会整合如 Linux、Zephyr 等不同类型 的内核以及和内核密切相关的框架和运行时，内核组件化的趋势逐渐开始形成。内核 组件化的本质还是为了解决物联网应用场景的扩展和不断增加的设备种类所带来的碎 片化问题。

其中华为宣传的鸿蒙内核区别于传统内核原因，其中个人猜测的的架构就是这种“多内核共存”模式，将内核组件化。

## 小米Vela

Xiaomi HyperOS 的技术体系下，Vela 定位为轻载硬件资源下，使用的轻量操作系统。 所以Vela所覆盖的设备是所有 L0 ～ L2 类设备，同时覆盖 L3 ～ L5设备的小核 /小系统。

文档借鉴自《小米澎湃OS技术白皮书》

<figure><img src=".gitbook/assets/image (70).png" alt=""><figcaption></figcaption></figure>

### 技术架构

<figure><img src=".gitbook/assets/image (71).png" alt=""><figcaption></figcaption></figure>

### 异构多核

<figure><img src=".gitbook/assets/image (72).png" alt=""><figcaption></figcaption></figure>

## OpenHarmony

OpenHarmony 是由开放原子开源基金会（OpenAtom）孵化、面向「全场景、全连接、全智能」的开源分布式操作系统。其核心特征可概括为：

- **一套系统，弹性部署**：通过组件化设计，同一套代码可按设备资源（从 L0 轻量设备到 L5 标准富设备）裁剪组合，覆盖从百 KB 内存的微小设备到 GB 级内存的富设备。
- **分布式架构**：以分布式软总线为底座，实现设备间能力互助与资源共享（分布式硬件、分布式数据、分布式任务调度）。
- **开源共建**：代码开源、生态开放，任何组织与个人均可参与共建、开发与使用。

## 技术架构

<figure><img src=".gitbook/assets/image (73).png" alt=""><figcaption></figcaption></figure>

OpenHarmony 整体采用分层架构（自上而下）：

- **内核层**：支持 Linux、LiteOS-A、LiteOS-M 多内核，配合 HDF 驱动框架统一硬件访问。
- **系统服务层**：包含分布式软总线、分布式硬件/数据、图形、多媒体、位置、DFX 等子系统，以系统服务形式由 samgr 管理。
- **框架层**：ArkUI、Ability、NAPI 等，为应用提供统一能力。
- **应用层**：ArkTS/JS/C/C++ 应用与原子化服务。

OpenHarmony的架构思路也是这样，统一型操作系统，跨设备分布式操作系统。从内核、框架、应用做了整体型的设计，更重要的是开源，让更多人都可以来共建、开发、消费这种新一代的操作系统。


