---
description: 搭建开发环境
---

# 02-开发环境搭建篇

## 获取代码&编译

文档地址：[https://gitcode.com/openharmony/docs/blob/master/zh-cn/release-notes/Readme.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/release-notes/Readme.md)

上面是每一个release的notes，获取对应版本代码。

建议不使用master的代码，代码太新，版本激进，而且容易有编译失败的风险。

以4.1.1 Release版本为例

### 代码拉取

文档地址：[https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/quick-start/quickstart-pkg-sourcecode.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/quick-start/quickstart-pkg-sourcecode.md)



tag版本地址：[https://gitcode.com/openharmony/docs/blob/master/zh-cn/release-notes/OpenHarmony-v4.1.1-release.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/release-notes/OpenHarmony-v4.1.1-release.md)

<figure><img src=".gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

文档有详细的获取代码方式

代码拉取后的结构

<figure><img src=".gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

后续会对源码结构再细化

### 编译工具环境

{% code overflow="wrap" %}
```sh
sudo apt-get update -y 
sudo apt-get install -y 
# 如果是ubuntu20.04系统请直接安装python3.9，如果是ubuntu18.04请改为安装python3.8
sudo apt-get install -y apt-utils binutils bison flex bc build-essential make mtd-utils gcc-arm-linux-gnueabi u-boot-tools python3.9 python3-pip git zip unzip curl wget gcc g++ ruby dosfstools mtools default-jre default-jdk scons python3-distutils perl openssl libssl-dev cpio git-lfs m4 ccache zlib1g-dev tar rsync liblz4-tool genext2fs binutils-dev device-tree-compiler e2fsprogs git-core gnupg gnutls-bin gperf lib32ncurses5-dev libffi-dev zlib* libelf-dev libx11-dev libgl1-mesa-dev lib32z1-dev xsltproc x11proto-core-dev libc6-dev-i386 libxml2-dev lib32z-dev libdwarf-dev
 
sudo apt-get install -y grsync xxd libglib2.0-dev libpixman-1-dev kmod jfsutils reiserfsprogs xfsprogs squashfs-tools  pcmciautils quota ppp libtinfo-dev libtinfo5 libncurses5 libncurses5-dev libncursesw5 libstdc++6  gcc-arm-none-eabi vim ssh locales doxygen

sudo apt-get install -y libxinerama-dev libxcursor-dev libxrandr-dev libxi-dev

sudo apt-get install libc6-dev-i386 lib32ncurses5-dev x11proto-core-dev libx11-dev lib32z1-dev libgl1-mesa-dev libxml2-utils xsltproc unzip fontconfig kpartx python-mako gcc-arm-linux-gnueabihf libssl-dev gcc-arm-linux-gnueabihf

sudo apt install gcc-arm-linux-gnueabi
```
{% endcode %}

官方工具环境在实际使用的时候会有部分问题，提供一版比较全面的工具环境，直接安装即可

另外prebuilts不要忘记拉取，源码下直接执行

```sh
bash build/prebuilts_download.sh
```

最后执行编译

```sh
./build.sh --product-name rk3568
```

<figure><img src=".gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

编译成功

## 使用docker方式编译

文档地址：[https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/get-code/gettools-acquire.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/get-code/gettools-acquire.md)



其他和正常使用一样


