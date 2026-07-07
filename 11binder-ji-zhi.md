---
description: 跨进程通信
---

# 11-binder机制

## 简介

服务与服务之间通信的机制。

Binder机制通常采用客户端-服务器（Client-Server）模型，服务请求方（Client）可获取服务提供方（Server）的代理 （Proxy），并通过此代理读写数据来实现进程间的数据通信。

## 框架

<figure><img src=".gitbook/assets/image (37).png" alt=""><figcaption></figcaption></figure>

官方文档：[https://gitcode.com/openharmony/systemabilitymgr\_safwk](https://gitcode.com/openharmony/systemabilitymgr\_safwk)



## 内核详解

OpenHarmony内核层面直接使用Android的binder机制

<figure><img src=".gitbook/assets/image (42).png" alt=""><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/image (43).png" alt=""><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/image (44).png" alt=""><figcaption></figcaption></figure>

Binder的一次拷贝过程，从数据发送方的User Space通过copy\_from\_user()将数据拷贝入进程间公用内核空间的物理内存。数据接收方通过memory\_mapping（内存映射）从这块物理内存直接获取。

在内核空间划分出了一块物理内存，内核空间和接收方的虚拟内存都映射在这块物理内存上，所以不需要第二次拷贝。而共享内存的0次拷贝通信，是通过发送和接收方共享同一块物理内存来实现。


