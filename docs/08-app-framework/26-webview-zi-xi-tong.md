# WebView

WebView 是 OpenHarmony 应用框架提供的网页渲染组件，允许开发者在 ArkUI 应用中嵌入 HTML5 内容、运行 JavaScript 并与宿主应用进行双向通信。OpenHarmony 的 WebView 基于自研 **ArkWeb** 引擎（内核源自 Chromium），在兼容主流 Web 标准的同时，针对嵌入式设备的性能和安全性进行了深度优化。

## 整体架构

WebView 的架构分为：

- **应用层**：ArkUI 应用通过 `Web` 组件或 JS 接口加载网页。
- **ArkWeb 框架层**：
  - **Web Component**：ArkUI 声明式组件，提供 `src`、`controller`、`onPageStart`、`onPageFinish` 等属性与事件。
  - **WebController**：控制网页导航（`loadUrl`、`back`、`forward`、`refresh`）、执行 JavaScript、管理 Cookie 和缓存。
  - **JavaScript Bridge**：`javaScriptProxy` 与 `runJavaScript` 实现 ArkTS ↔ JS 的双向通信。
- **渲染引擎层**：基于 Chromium Content Module，负责 HTML/CSS/JS 解析、布局、渲染和合成。
- **GPU 加速层**：利用 Skia + GPU 进行图形渲染，与 OpenHarmony 图形子系统对接。

## 核心能力

| 能力 | 说明 |
|------|------|
| 网页加载 | 支持 HTTP/HTTPS 本地文件（`resource://`、`data://`）加载 |
| JavaScript 执行 | 支持 `evaluateJavaScript` 异步执行 JS 并获取返回值 |
| JS Bridge | 支持 `javaScriptProxy` 注册 ArkTS 对象供 JS 调用 |
| Cookie 管理 | `WebCookieManager` 设置、获取、清除 Cookie |
| 缓存管理 | 支持缓存模式配置（默认、缓存优先、无缓存） |
| 缩放与手势 | 支持 pinch 缩放、文本选择、长按菜单 |
| 地理位置 | 支持网页获取地理位置（需申请 `ohos.permission.LOCATION`） |
| 文件上传 | 支持 `<input type="file">` 调起系统文件选择器 |
| 深色模式 | 支持跟随系统或强制设置网页深色模式 |
| 自定义 UA | 支持设置自定义 User-Agent |

## 基础使用示例

### 在 ArkUI 中嵌入 WebView

```ts
import { WebView } from '@kit.ArkWeb';

@Entry
@Component
struct WebPage {
  controller: WebController = new WebController();

  build() {
    Column() {
      Web({ src: 'https://openharmony.cn', controller: this.controller })
        .javaScriptAccess(true)
        .domStorageAccess(true)
        .zoomAccess(true)
        .onPageStart((event) => {
          console.log('Page start: ' + event?.url);
        })
        .onPageFinish((event) => {
          console.log('Page finish: ' + event?.url);
        })
        .onErrorReceive((event) => {
          console.error('Page error: ' + event?.error.getErrorInfo());
        })
    }
  }
}
```

### ArkTS 与 JavaScript 双向通信

```ts
// 注册 ArkTS 对象供 JS 调用
class JsBridge {
  @javaScriptInterface
  showMessage(msg: string): void {
    console.log('Message from JS: ' + msg);
  }
}

// 在 Web 组件中配置 javaScriptProxy
Web({ src: 'resource://rawfile/index.html', controller: this.controller })
  .javaScriptProxy({
    object: new JsBridge(),
    name: 'arkBridge',
    methodList: ['showMessage']
  })

// JS 侧调用
// window.arkBridge.showMessage('Hello from JS');
```

```ts
// 在 ArkTS 中执行 JS 并获取返回值
this.controller.runJavaScript('document.title', (result) => {
  console.log('Page title: ' + result);
});
```

## 安全模型

WebView 涉及网络与脚本执行，安全至关重要：

- **网络安全配置**：支持 `networkSecurityConfig` 配置证书固定（Pinning）、明文流量允许等。
- **混合内容**：默认禁止 HTTPS 页面加载 HTTP 资源（Mixed Content），可通过配置放宽。
- **JS 执行控制**：`javaScriptAccess(false)` 可完全禁用 JS，防止恶意脚本。
- **文件访问限制**：默认禁止网页访问本地文件，需显式开启。
- **权限隔离**：网页调用系统敏感 API（如地理位置、相机、麦克风）需通过权限弹窗由用户授权。
- **进程隔离**：渲染进程与主进程隔离，网页崩溃不会影响应用主体。

## 性能优化建议

| 优化项 | 建议 |
|--------|------|
| 预连接 | 对高频域名使用 `preconnect` 提前建立 TCP 连接 |
| 缓存策略 | 合理配置 `CacheMode`，避免重复下载静态资源 |
| 离线包 | 将 H5 资源打包至应用 `rawfile`，实现秒开 |
| 懒加载 | 对非首屏内容使用 `loading="lazy"` |
| 减少重排 | 避免频繁修改 DOM 样式，使用 CSS 动画替代 JS 动画 |
| 渲染合成 | 对复杂页面开启 GPU 加速渲染 |

## 调试方法

- **hilog 日志**：`hilog | grep -i arkweb` 查看 WebView 相关日志。
- **DevTools**：部分版本支持通过 PC 端 Chrome DevTools 远程调试 WebView 页面（需开启 USB 调试并配置端口转发）。
- **性能剖析**：使用 `hiperf` 或系统 `SmartPerf` 工具分析 WebView 渲染性能。

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 网页白屏 | 网络不通、URL 错误、SSL 证书错误 | 检查 URL、网络状态、证书配置 |
| JS 不执行 | `javaScriptAccess` 未开启 | 设置 `.javaScriptAccess(true)` |
| JS Bridge 调用失败 | 方法未注册、名称不匹配 | 检查 `methodList` 和 `name` 配置 |
| 视频无法播放 | 格式不支持、解码器缺失 | 确认视频编码格式，使用系统支持的格式 |
| 内存增长 | 缓存未清理、单页应用内存泄漏 | 定期调用 `deleteJavaScriptRegister()`、清理缓存 |

## 相关阅读

- [ArkWeb 开发指南](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/web/web-overview.md)
- [Web 组件 API 参考](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/reference/arkui-ts/ts-basic-components-web.md)
- [Chromium 架构文档](https://www.chromium.org/developers/design-documents/)
