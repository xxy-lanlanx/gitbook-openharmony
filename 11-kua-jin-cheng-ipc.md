---
description: OpenHarmonyIPC
---

# 11-跨进程IPC

## Linux的IPC

OpenHarmony是基于Linux系统上的，先了解一下Linux中的IPC通信原理。

在Linux中，进程之间是隔离的，内存也是不共享的，进程空间分为用户空间和内核空间，用户空间是用户程序运行的空间，内核空间则是内核运行的空间，为了防止用户空间随便干扰，用户空间是独立的，内核空间是共享的，但为了安全性考虑，内核空间跟用户空间也是隔离的，它们之间的仅可以通过系统调用来通信。至此我们知道IPC的大致方案是A进程的数据通过系统调用把数据传递到内核空间，内核空间再利用系统调用把数据传递到B空间，其中会有两次数据的拷贝如下图：

<figure><img src=".gitbook/assets/image (39).png" alt=""><figcaption></figcaption></figure>

## Binder IPC 原理

<figure><img src=".gitbook/assets/image (40).png" alt=""><figcaption></figcaption></figure>

1.首先 Binder 驱动在内核空间创建一个数据接收缓存区；&#x20;

2.接着在内核空间开辟一块内核缓存区，建立内核缓存区和内核中数据接收缓存区之间的映射关系，以及内核中数据接收缓存区和接收进程用户空间地址的映射关系；

&#x20;3.发送方进程通过系统调用 copy\_from\_user() 将数据 copy 到内核中的内核缓存区，由于内核缓存区和接收进程的用户空间存在内存映射，因此也就相当于把数据发送到了接收进程的用户空间，这样便完成了一次进程间的通信。



OpenHarmony IPC流程

IPC通信包括客户端(client)和服务端(service)。

* 服务端TestService继承自IPCObjectStub。
* 客户端TestServiceClient通过iface\_cast(object)获取到一个TestServiceProxy对象。TestServiceProxy继承自PeerHolder，里面包含指向IPCObjectProxy的指针。
* 客户端的IPCObjectProxy和服务端IPCObjectStub是对应关系。

<figure><img src=".gitbook/assets/image (41).png" alt=""><figcaption></figcaption></figure>

