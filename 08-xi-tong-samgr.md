---
description: OpenHarmony系统服务管理组件
---

# 08-系统samgr

## 简介

所有的业务子系统发起点，提供OpenHarmony系统服务启动、注册、查询等功能。

服务链接：[https://gitcode.com/openharmony/systemabilitymgr\_samgr](https://gitcode.com/openharmony/systemabilitymgr\_samgr)

## 架构

<figure><img src=".gitbook/assets/image (38).png" alt=""><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/image (31).png" alt=""><figcaption></figcaption></figure>

## 作用

操作系统的服务是一个个独立的业务单元，但怎么将每个业务单元能够统一整合，这就是系统服务管理组件解决的问题。

主要提供两大能力：1，启动、注册、查询 2，服务相互通信

## 使用

以其中一个子服务为样例

### 声明注册

<figure><img src=".gitbook/assets/image (34).png" alt=""><figcaption></figcaption></figure>

依赖关键SystemAbility，具备完整的服务生命周期

### 配置

<figure><img src=".gitbook/assets/image (33).png" alt=""><figcaption></figcaption></figure>

### 实现

<figure><img src=".gitbook/assets/image (35).png" alt=""><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/image (36).png" alt=""><figcaption></figcaption></figure>

SystemAbility实现一般采用XXX.cfg + profile.json + libXXX.z.so的方式由init进程执行对应的XXX.cfg文件拉起相关SystemAbility进程。

## 服务管理原理解析




