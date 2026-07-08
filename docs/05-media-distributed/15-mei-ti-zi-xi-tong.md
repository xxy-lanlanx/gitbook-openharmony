---
description: 媒体子系统
---

# 15-媒体子系统

## 简介

媒体子系统为开发者提供一套简单且易于理解的接口，使得开发者能够方便接入系统并使用系统的媒体资源。

媒体子系统包含了音视频、相机相关媒体业务，提供以下常用功能：

* 音频播放和录制。
* 视频播放和录制。
* 相机拍照和录制。

## 架构





![](../../.gitbook/assets/image.png)





* **Media**: 为应用提供播放、录制等接口，通过跨进程调用或直接调用方式，调用媒体引擎Gstreamer、Histreamer或其它引擎。
  * mini设备上，Media部件调用Histreamer支持音频播放等功能。
  * small设备上，Media部件调用recorder_lite支持音视频录制，默认调用player_lite支持音视频播放，通过设置系统属性变量debug.media_service.histreamer为1使用histreamer。详细设置方法参见[syspara系统属性组件使用说明](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/subsystems/subsys-boot-init-sysparam.md)或者参见[syspara模块代码](https://gitcode.com/openharmony/startup_syspara_lite)。
  * standard设备上，Media部件调用Gstreamer支持音视频播放、音视频录制。
* **Audio**: Audio部件支持音频输入输出、策略管理、音频焦点管理等功能。
* **Camera**: Camera部件提供相机操作接口，支持预览、拍照、录像。
* **Image**: Image部件支持常见图片格式的编解码。
* **MediaLibrary**: MediaLibrary支持本地和分布式媒体数据访问管理。
* **Histreamer**: 轻量级媒体引擎，支持文件/网络流媒体输入，支持音视频解码播放，支持音视频编码录制，支持插件扩展。
* **Gstreamer**: 开源GStreamer引擎，支持流媒体、音视频播放、录制等功能。

## 媒体引擎对比：Histreamer vs Gstreamer

| 维度 | Histreamer | Gstreamer |
|------|------------|-----------|
| 目标系统 | 轻量 / 小型系统 | 标准系统 |
| 内存占用 | 极小（KB~MB 级） | 较大（MB 级） |
| 插件体系 | 轻量插件 | 丰富插件生态 |
| 功能覆盖 | 音频为主，基础视频 | 全功能音视频、流媒体、滤镜 |
| 开发依赖 | 无 glib，C 标准库 | 依赖 glib，跨平台 |
| 适用场景 | IoT、穿戴、音箱 | 手机、平板、车机 |

开发者在选择设备平台时，实际上已由系统类型决定了媒体引擎（mini/small 用 Histreamer，standard 用 Gstreamer），但了解两者差异有助于理解媒体子系统的分层设计。

## 音频焦点管理

当多个应用同时请求音频输出时，系统通过**音频焦点（Audio Focus）**机制进行协调：

- 应用播放前需申请焦点（如 `AudioFocusType.FOCUS_GAIN`）；
- 系统根据焦点类型与优先级决定谁获得播放权；
- 焦点被抢占时，应用会收到回调（如 `AUDIO_FOCUS_LOSS`），应暂停或降低音量；
- 常见场景：导航提示音临时抢占音乐播放，提示结束后焦点归还，音乐恢复。

## 相机预览与拍照流程

```
应用调用 Camera API
  │
  ▼
Camera Service（跨进程）
  │
  ▼
相机驱动（HDI / V4L2）
  │
  ▼
硬件（ISP + 传感器）
```

- **预览**：相机持续输出图像帧，通过 Surface 传递到应用或窗口子系统显示；
- **拍照**：应用触发 capture，Camera Service 协调 ISP 输出一帧高分辨率图像，经编码（JPEG/HEIF）后保存到媒体库；
- **录像**：预览流同时送入视频编码器，与音频流复用为 MP4/MPEG-TS 等容器格式。

## 媒体库与分布式媒体

MediaLibrary 统一管理本地媒体数据（照片、视频、音频），并支持分布式访问：

- **本地访问**：应用通过 `photoAccessHelper` 或 `mediaLibrary` 查询、增删媒体文件；
- **分布式访问**：同帐号可信设备间，媒体库可展示远端设备的媒体索引，应用可选择远端图片/视频进行浏览或编辑（实际传输由分布式文件系统或软总线承载）。

## 权限与隐私

媒体操作涉及敏感权限，典型权限需求如下：

| 能力 | 权限 | 授权方式 |
|------|------|----------|
| 相机预览/拍照 | `ohos.permission.CAMERA` | user_grant |
| 麦克风录音 | `ohos.permission.MICROPHONE` | user_grant |
| 读取媒体文件 | `ohos.permission.READ_MEDIA` | user_grant |
| 写入媒体文件 | `ohos.permission.WRITE_MEDIA` | user_grant |
| 媒体焦点控制 | 系统服务内部，无需应用申请 | — |

> 相机与麦克风属于高度敏感权限，应用必须在运行时明确向用户申请，且系统会提示用户当前哪个应用正在使用相机/麦克风（隐私指示器）。

## Gstreamer

### 简介

Gstreamer是一个支持Windows，Linux，Android， iOS的跨平台的多媒体框架，应用程序可以通过管道（Pipeline）的方式，将多媒体处理的各个步骤串联起来，达到预期的效果。每个步骤通过元素（Element）基于GObject对象系统通过插件（plugins）的方式实现，方便了各项功能的扩展。

gstreamer跟ffmpeg一样，也是一个媒体框架，可以实现采集，编码，解码，渲染，滤镜等一条龙的媒体解决方案。

1. 跟ffmpeg一样，也是有命令行工具进行测试验证。同时还可以通过代码框架直接封装命令来做工程开发，这一点ffmpeg是不具备的，ffmpeg需要学习API才能做工程开发，就算你会ffplay.exe或ffmpeg.exe验证某些需求，但要集成到代码，需要学习API来实现。而gstreamer只要知道的命令行实现方式，就可以马上命令行集成到代码中进行使用，当然你想代码优雅一点或者你是熟手也可以使用API来实现。
2. Gstreamer是glib实现的，跨平台的实现，windows,linux,androd,ios，macos官方原生支持，而且官方发布了windows,linux,androd,ios包，如果没有特别需求，可以直接拿发布包集成使用。而ffmpeg想支持android,ios，就需要自己做交叉编译了。
3. Gstreamer采用插件实现方式，根据业务需要可以灵活裁剪插件，可以将发布包做的非常小，特别适合在嵌入式和移动端等应用领域，而ffmpeg比较大，在嵌入领域需要自己做代码级裁剪。
4. Gstreamer 采用glib实现，用C语言来实现面向对象思维，完全不是标准C++那一套逻辑，由于要跨平台，原生的系统API都是适配封装了一套，甚至自己实现队列，MAP，容器，协程，线程，异步操作，不熟悉glib 的API话，代码理解比较困难，用惯了C++，STL，boost，感觉得这是gstream最让人反感的一点，不合主流，搞的我又要学一套API。
5. Gstreamer采用插件管理各个模块，软件框架比较复杂，采用了异步，协程编程模型，进一步增加了理解难度。

参考文档：[https://vinming.github.io/2022/03/12/gstreamer_basic_tutorial/](https://vinming.github.io/2022/03/12/gstreamer_basic_tutorial/)

### 框架





![](../../.gitbook/assets/image-2.png)

## 相关阅读

- [窗口子系统](../../04-ipc-graphics/13-chuang-kou-zi-xi-tong.md)
- [图形子系统-openharmony](../../04-ipc-graphics/12-graphics/12-tu-xing-zi-xi-tong-openharmony.md)
- [33-文件与存储](../../09-build-services/33-wen-jian-cun-chu-zi-xi-tong.md)
- [17-分布式数据管理](../17-fen-bu-shi-shu-ju-guan-li.md)
