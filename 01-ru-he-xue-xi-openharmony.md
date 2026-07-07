---
description: openharmony操作系统
---

# 01-如何学习openharmony？

## 综述

官方文档必不可少，辅助学习，但是知晓了架构才能入门。

可能有人问：编程语言需要么？

需要？但不重要，语言的学习是长期精深的过程。学过很多语言的同学，可能会有感觉，其实每种语言体系设计思维都基本类似的，但每种语言又有它们特有的体系、语法糖和适用的领域，这个上面花费的时间才是大头。

精深一门语言即可，其他语言用到了再学习也不迟，语言对于学习OpenHarmony并非是障碍，当然了，OpenHarmony每种涉及的语言都深入学习，效果会更好。

## 文档

### 应用层面

官方文档：以最新发布的版本4.1release为例，

文档地址：[https://docs.openharmony.cn/pages/v4.1/zh-cn/application-dev/application-dev-guide.md](https://docs.openharmony.cn/pages/v4.1/zh-cn/application-dev/application-dev-guide.md)

<figure><img src=".gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

### 设备系统层面

官方文档：

[https://docs.openharmony.cn/pages/v4.1/zh-cn/device-dev/device-dev-guide.md](https://docs.openharmony.cn/pages/v4.1/zh-cn/device-dev/device-dev-guide.md)

<figure><img src=".gitbook/assets/image (2) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

## 如何学习？

通过查阅文档其实已经可以对OpenHarmony有个初步的认知，但是万事开头难，本章不是为了把官方的文档解释一遍，搬运一遍，没有太大意义，对于学习OpenHarmony帮助和官方是重复动作。

那么到底怎么学习呢？没有一个总览全局的认知，学习起来可能知识盲人摸象，找不到重点，浪费大量时间。

言归正传，正式开始。

### 架构层

第一步，还是回到架构，看文档是细则，但是没有对架构清晰的认知还是，还是不知道学哪里，哪里适合自己入手，进一步的入门，进阶，熟练，变成对应体系的专家。

<figure><img src=".gitbook/assets/image (3) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

调度逻辑由上而下，所以学习的路径也是由上而下，一个链路搞懂以后，之后所有的平行模块都是一个设计思想，区别的是不同模块业务并不相同，彻底搞懂一条线，逐步再扩展到整个面。

### 应用层&系统框架层相互调用

架构图

<figure><img src=".gitbook/assets/image (4) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

关键字：NAPI

NAPI的概念源自Nodejs，为了实现javascript脚本与C++库之间的相互调用，Nodejs对V8引擎的api做了一层封装，称为NAPI。

NAPI适合封装IO、CPU密集型、OS底层等能力并对外暴露JS接口，通过NAPI可以实现JS与C/C++代码互相访问。我们可以通过NAPI接口构建例如网络通信、串口访问、多媒体解码、传感器数据收集等模块。

它是应用调用系统服务\&Native层关键技术，当前只需要知道它是勾连js\&c++的重要工具。

详细展开，后续章节会单独描述。

### 框架层服务相互调用

架构图

<figure><img src=".gitbook/assets/image (2) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

samgr组件是OpenHarmony的核心组件，提供OpenHarmony系统服务启动、注册、查询等功能。

每个系统服务都需要使用当前组件，管理每个子系统生命周期，并且配合特有的IPC机制，对外提供接口功能调用。

详细展开，后续章节会单独描述。

### 框架服务&内核相互调用

框架图

<figure><img src=".gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

驱动子系统采用C面向对象编程模型构建，通过平台解耦、内核解耦，兼容不同内核，提供了归一化的驱动平台底座，旨在为开发者提供更精准、更高效的开发环境，力求做到一次开发，多系统部署。

交互流程

<figure><img src=".gitbook/assets/image (2) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

详细展开，后续章节会单独描述。

### 综述

以上链路就是一个完整的一条线，是OpenHarmony基础的基础，优先了解此链路相关，才能完成入门的第一步。

