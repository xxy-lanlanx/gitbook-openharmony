# 19-内核子系统-Linux内核架构

架构示意

<figure><img src=".gitbook/assets/image (79).png" alt=""><figcaption></figcaption></figure>

上图说明了Linux内核的整体架构。根据内核的核心功能，Linux内核提出了5个子系统，分别负责如下的功能：

1. Process Scheduler，也称作进程管理、进程调度。负责管理CPU资源，以便让各个进程可以以尽量公平的方式访问CPU。
2. Memory Manager，内存管理。负责管理Memory（内存）资源，以便让各个进程可以安全地共享机器的内存资源。另外，内存管理会提供虚拟内存的机制，该机制可以让进程使用多于系统可用Memory的内存，不用的内存会通过文件系统保存在外部非易失存储器中，需要使用的时候，再取回到内存中。
3. VFS（Virtual File System），虚拟文件系统。Linux内核将不同功能的外部设备，例如Disk设备（硬盘、磁盘、NAND Flash、Nor Flash等）、输入输出设备、显示设备等等，抽象为可以通过统一的文件操作接口（open、close、read、write等）来访问。这就是Linux系统“一切皆是文件”的体现（其实Linux做的并不彻底，因为CPU、内存、网络等还不是文件）。
4. Network，网络子系统。负责管理系统的网络设备，并实现多种多样的网络标准。
5. IPC（Inter-Process Communication），进程间通信。IPC不管理任何的硬件，它主要负责Linux系统中进程之间的通信。

## 内核代码结构

<figure><img src=".gitbook/assets/image (80).png" alt=""><figcaption></figcaption></figure>

Linux 内核源码按功能自上而下组织，与上面 5 个子系统对应的主要目录如下：

- `kernel/`：进程调度核心，包含调度器（sched）、进程/线程管理、fork/exit 等。
- `mm/`：内存管理，包含物理页分配（buddy）、slab 分配器、页表与虚拟内存（VM）子系统。
- `fs/`：虚拟文件系统 VFS 及各具体文件系统（ext4、f2fs、proc、sysfs 等）。
- `net/`：网络协议栈（TCP/IP、socket、网络设备驱动框架）。
- `ipc/`：进程间通信，包含 System V IPC（msg/sem/shm）与 POSIX 消息队列等。
- `drivers/`：各类设备驱动，是内核中规模最大的部分。
- `arch/`：与体系结构相关的代码（如 arm64、x86、riscv），包含平台启动、异常向量、MMU 等。
- `init/`：内核启动与初始化代码（如 `start_kernel`）。
- `include/`：内核头文件。

## Linux 内核在 OpenHarmony 中的定位

在内核子系统中，Linux 内核是**标准系统（富设备）**所采用的内核形态之一。OpenHarmony 在原生 Linux 内核之上主要做了以下适配与增强：

- **HDF 驱动框架对接**：通过 HDF（Hardware Driver Foundation）统一驱动模型，使设备驱动与具体内核版本解耦。
- **轻量/小型系统差异**：对于资源受限的设备，OpenHarmony 提供 LiteOS-A / LiteOS-M 内核，而非 Linux 内核；标准系统才使用 Linux 内核。
- **基础能力增强**：围绕 OpenHarmony 系统需求，补充或修改部分调度、内存、安全（如安全子系统相关钩子）等基础能力。

## 关键机制小结

- **一切皆文件**：VFS 把设备、管道、网络等抽象为统一文件接口（open/close/read/write/ioctl），是 Linux 易扩展性的根基。
- **公平调度**：进程调度器以 CFS（完全公平调度）等算法，让进程尽量公平地共享 CPU。
- **虚拟内存**：通过页表与缺页中断，提供比物理内存更大的地址空间，并以文件作为换出/换入的载体。
- **模块化**：驱动与部分功能以可加载模块（ko）形式存在，便于按需扩展而无需重新编译内核。
