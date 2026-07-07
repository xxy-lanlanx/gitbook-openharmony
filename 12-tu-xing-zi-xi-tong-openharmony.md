---
description: 基于Linux图形显示之上的OpenHarmony架构
---

# 12-图形子系统-openharmony

## 简介

图形子系统主要包括UI组件、布局、动画、字体、输入事件、窗口管理、渲染绘制等模块，构建基于轻量OS的应用框架，满足硬件资源较小的物联网设备的OpenHarmony系统应用开发。

## 架构

<figure><img src=".gitbook/assets/image (45).png" alt=""><figcaption></figcaption></figure>

各模块介绍：

* View：应用组件，包括UIView、UIViewGroup、UIButton、UILabel、UILabelButton、UIList、UISlider等。
* Animator：动画模块，开发者可以自定义动画。
* Layout：布局控件，包括FlexLayout、GridLayout、ListLayout等。
* Transform：图形变换模块，包括旋转、平移、缩放等。
* Event：事件模块，包括click、press、drag、long press等基础事件。
* Rendering engine：渲染绘制模块。
* 2D graphics library：2D绘制模块，包括直线、矩形、圆、弧、图片、文字等绘制。包括软件绘制和硬件加速能力对接。
* Multi-language：多语言模块，用于处理不用不同语言文字的换行、整形等。
* Image library：图片处理模块，用于解析和操作不同类型和格式的图片，例如png、jpeg、ARGB8888、ARGB565等
* WindowManager：窗口管理模块，包括窗口创建、显示隐藏、合成等处理。
* InputManager：输入事件管理模块。

提供了图形接口能力

<figure><img src=".gitbook/assets/image (46).png" alt=""><figcaption></figcaption></figure>

