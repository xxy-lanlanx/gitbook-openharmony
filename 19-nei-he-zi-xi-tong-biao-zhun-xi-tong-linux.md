---
description: Linux内核
---

# 19-内核子系统-标准系统Linux

## 简介

Linux® 内核是 Linux 操作系统（OS）的主要组件，也是计算机硬件与其进程之间的核心接口。它负责两者之间的通信，还要尽可能高效地管理资源。

之所以称为内核，是因为在操作系统中就像果实硬壳中的种子一样，控制着硬件（无论是电话、笔记本电脑、服务器，还是任何其他类型的计算机）的所有主要功能。

Linux 是一个符合POSIX 标准的内核。它提供了一套应用程序接口（API），通过接口用户程序能与内核及硬件交互。仅仅一个内核并不是一套完整的操作系统。有一套基于 Linux 内核的完整操作系统叫作Linux 操作系统，或是GNU/Linux（在该系统中包含了很多GNU 计划的系统组件）

## 架构

<figure><img src=".gitbook/assets/image (60).png" alt=""><figcaption></figcaption></figure>

Linux是一个单体内核，支持真正的抢占式多任务处理（于用户态，和版本2.6系列之后的内核态）、虚拟内存、共享库、请求分页、共享写时复制可执行体（通过内核同页合并）、内存管理、Internet协议族和线程等功能。

设备驱动程序和内核扩展运行于内核空间（在很多CPU架构中是ring 0），可以完全访问硬件，但也有运行于用户空间的一些例外，例如基于FUSE/CUSE的文件系统，和部分UIO。多数人与Linux一起使用的图形系统不运行在内核中。与标准单体内核不同，Linux的设备驱动程序可以轻易的配置为内核模块，并在系统运行期间可直接装载或卸载。也不同于标准单体内核，设备驱动程序可以在特定条件下被抢占；增加这个特征用于正确处理硬件中断并更好的支持对称多处理。出于自愿选择，Linux内核没有二进制内核接口。

硬件也被集成入文件层级中。用户应用到设备驱动的接口是在/dev或/sys目录下的入口文件。进程信息也通过/proc目录映射到文件系统。

<figure><img src=".gitbook/assets/image (61).png" alt=""><figcaption></figcaption></figure>

文档地址：[https://zh.wikipedia.org/wiki/Linux%E5%86%85%E6%A0%B8](https://zh.wikipedia.org/wiki/Linux%E5%86%85%E6%A0%B8)

## I/O调度器

<figure><img src=".gitbook/assets/image (62).png" alt=""><figcaption></figcaption></figure>

