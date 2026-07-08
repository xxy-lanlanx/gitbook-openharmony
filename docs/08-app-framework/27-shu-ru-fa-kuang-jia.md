# 输入法框架

输入法框架（Input Method Framework，IMF）负责管理系统输入法的生命周期、输入法与应用的交互流程，以及文本输入事件的派发。在 OpenHarmony 中，输入法框架支持系统默认键盘和第三方输入法应用，为多模输入（触屏、手写、语音、键盘）提供统一的接入和管理能力。

## 整体架构

输入法框架的核心角色包括：

- **输入法应用（IME Application）**：提供软键盘面板、候选词、语音输入等交互界面，以独立应用形式运行。
- **输入法管理服务（IMMS）**：系统服务，负责输入法启用/禁用/切换、绑定输入法应用、管理输入法列表和默认设置。
- **输入法客户端（Input Method Client）**：嵌入在编辑框（`TextInput`）所在的应用进程中，负责与输入法服务建立连接，传递文本输入请求和事件。
- **输入法核心服务**：处理输入法与客户端之间的 IPC 通信、编辑器状态同步、按键事件分发。
- **窗口子系统**：为输入法面板提供独立的窗口（Input Method Window），支持悬浮、贴底、分屏等显示模式。

```
应用进程（TextInput） → 输入法客户端 → IMMS → 输入法应用（IME）
                                              ↓
                                        输入法核心服务
```

## 核心机制

### 1. 输入法绑定与生命周期

当用户点击文本框时，应用窗口通过 `InputMethodClient` 向 `IMMS` 请求绑定输入法：

1. `IMMS` 检查当前默认输入法，若未启动则拉起输入法应用进程。
2. 输入法应用创建 `InputMethodPanel` 窗口并显示。
3. 输入法客户端与输入法核心服务建立连接，同步编辑器状态（光标位置、选区、文本内容）。
4. 用户输入时，输入法通过 `InputMethodAgent` 将文本提交或删除事件发送到客户端。
5. 文本框失焦或页面退出时，`IMMS` 通知输入法隐藏面板，可选保留进程或销毁。

### 2. 文本输入模型

输入法与编辑框通过 **InputConnection** 接口交互：

| 操作 | 方法 | 说明 |
|------|------|------|
| 提交文本 | `commitText(text)` | 将候选词或输入字符提交到编辑框 |
| 删除文本 | `deleteText(before, after)` | 删除光标前后指定长度文本 |
| 获取文本 | `getTextBeforeCursor(n)` | 获取光标前文本用于智能联想 |
| 设置选区 | `setSelection(start, end)` | 改变光标位置或选中文本 |
| 发送按键 | `sendKeyEvent(key)` | 模拟退格、回车等按键事件 |

### 3. 输入法面板窗口管理

输入法窗口属于系统级悬浮窗口，受窗口子系统管理：

- **显示模式**：支持全屏、分屏、悬浮窗模式下的自适应布局。
- **避让策略**：当输入法弹出时，窗口子系统自动计算可用区域，应用窗口可选择整体上移或缩放。
- **安全限制**：输入法窗口无法覆盖在其他应用之上，防止点击劫持。

## 关键接口

| 能力 | 接口 | 说明 |
|------|------|------|
| 显示输入法 | `inputMethod.getInputMethodController().show()` | 主动唤起输入法面板 |
| 隐藏输入法 | `inputMethod.getInputMethodController().hide()` | 隐藏输入法面板 |
| 切换输入法 | `inputMethod.switchInputMethod()` | 在当前已启用的输入法间切换 |
| 获取输入法列表 | `inputMethod.getInputMethodList()` | 查询已安装的输入法 |
| 设置默认输入法 | `inputMethod.setDefaultInputMethod()` | 系统设置，需系统权限 |

## 安全与隐私

输入法涉及用户敏感输入，安全设计至关重要：

- **密码输入保护**：密码框（`TextInput({type: InputType.Password})`）自动禁用输入法联想、截图和录屏。
- **输入数据隔离**：输入法应用只能访问当前编辑框的文本，无法读取其他应用内容。
- **签名验证**：第三方输入法需经过应用市场签名审核，防止恶意键盘记录。
- **权限控制**：应用无法直接读取输入法内部数据，防止隐私泄露。

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 输入法无法弹出 | 窗口未获取焦点、IME 未启动 | 检查焦点状态、确认默认输入法已启用 |
| 输入法遮挡内容 | 未开启窗口避让 | 在 `window` 配置中设置 `keyboardAvoidMode` |
| 第三方输入法崩溃 | IME 进程异常、内存不足 | 查看 IME 进程日志、检查面板窗口资源泄漏 |
| 输入延迟 | 主线程阻塞、IPC 频繁 | 避免在主线程执行耗时操作，减少不必要的文本同步 |

## 相关阅读

- [输入法框架源码](https://gitee.com/openharmony/inputmethod_imf)
- [窗口避让策略](https://gitee.com/openharmony/window_window_manager)
- [ArkUI TextInput 组件](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/reference/arkui-ts/ts-basic-components-textinput.md)
