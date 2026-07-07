---
description: 工欲善其事必先利其器
---

# 03-开发工具篇

## 应用IDE

下载路径

官方文档配套并不好用，版本会有迟滞



<figure><img src=".gitbook/assets/image (5) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

链接：[https://gitcode.com/openharmony/docs/blob/master/zh-cn/release-notes/OpenHarmony-v4.1.1-release.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/release-notes/OpenHarmony-v4.1.1-release.md)

切换每个版本都有对应版本的IDE，建议使用版本对应的IDE来进行开发。

应用开发工具的具体使用，可以参考此文档：[https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V2/deveco\_overview-0000001053582387-V2](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V2/deveco\_overview-0000001053582387-V2)

## 系统开发

### vscode

推荐使用vscode

下载链接：[https://code.visualstudio.com/](https://code.visualstudio.com/)

远程连接开发：[https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/quick-start/quickstart-ide-env-remote.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/quick-start/quickstart-ide-env-remote.md)

<figure><img src=".gitbook/assets/image (6) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

官方推荐使用DevEco Device Tool，做系统开发的话，这个可以不需要，但可以使用，部分工具还是挺好用的，也是基于vscode的一个插件。

### vscode插件

推荐几个好用插件，让开发过程更加的自如

#### C/C++工具包

C++开发必备

<figure><img src=".gitbook/assets/image (7) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

#### Git Graph

因为repo管理是超大型项目的一个总集管理，此插件便于我们查看不同git仓库的历史

<figure><img src=".gitbook/assets/image (9) (1).png" alt=""><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/image (10) (1).png" alt=""><figcaption></figcaption></figure>

Remote - SSH

远程连接，必要插件

<figure><img src=".gitbook/assets/image (11) (1).png" alt=""><figcaption></figcaption></figure>

#### GN

Edit GN files in Visual Studio Code，高亮GN脚本文件，作用不大，但更直观的看GN脚本

<figure><img src=".gitbook/assets/image (12) (1).png" alt=""><figcaption></figcaption></figure>



### vscode配置

由于超大型项目的文件过多，开发起来查找、索引都比较麻烦，所以需要添加一些配置，来忽略大部分很少关心的文件夹，让工程变得更加易用

```json
{
    "workbench.iconTheme": "vscode-icons",
    "workbench.editor.enablePreview": false,
    "files.autoSave": "afterDelay",
    "files.associations": {
        "iostream": "cpp",
        "*.tcc": "cpp",
        "source_location": "cpp",
        "*.ipp": "cpp",
        "stdlib.h": "c",
        "stdio.h": "c",
        "unistd.h": "c",
        "random": "cpp",
        "ios": "cpp",
        "__config": "cpp",
        "__bit_reference": "cpp",
        "__bits": "cpp",
        "__debug": "cpp",
        "__functional_base": "cpp",
        "__hash_table": "cpp",
        "__locale": "cpp",
        "__node_handle": "cpp",
        "__nullptr": "cpp",
        "__split_buffer": "cpp",
        "__string": "cpp",
        "__threading_support": "cpp",
        "__tuple": "cpp",
        "algorithm": "cpp",
        "array": "cpp",
        "atomic": "cpp",
        "bit": "cpp",
        "bitset": "cpp",
        "cctype": "cpp",
        "chrono": "cpp",
        "clocale": "cpp",
        "cmath": "cpp",
        "cstdarg": "cpp",
        "cstddef": "cpp",
        "cstdint": "cpp",
        "cstdio": "cpp",
        "cstdlib": "cpp",
        "cstring": "cpp",
        "ctime": "cpp",
        "cwchar": "cpp",
        "cwctype": "cpp",
        "exception": "cpp",
        "functional": "cpp",
        "initializer_list": "cpp",
        "iosfwd": "cpp",
        "istream": "cpp",
        "iterator": "cpp",
        "limits": "cpp",
        "locale": "cpp",
        "memory": "cpp",
        "new": "cpp",
        "numeric": "cpp",
        "ostream": "cpp",
        "queue": "cpp",
        "stdexcept": "cpp",
        "streambuf": "cpp",
        "string": "cpp",
        "string_view": "cpp",
        "tuple": "cpp",
        "type_traits": "cpp",
        "typeinfo": "cpp",
        "unordered_map": "cpp",
        "utility": "cpp",
        "vector": "cpp",
        "memory_resource": "cpp",
        "optional": "cpp",
        "codecvt": "cpp",
        "condition_variable": "cpp",
        "list": "cpp",
        "map": "cpp",
        "fstream": "cpp",
        "mutex": "cpp",
        "ratio": "cpp",
        "sstream": "cpp",
        "system_error": "cpp",
        "thread": "cpp",
        "valarray": "cpp",
        "vendor_adapter.h": "c",
        "hril_enum.h": "c",
        "hril.h": "c",
        "csignal": "cpp",
        "userial_vendor.h": "c",
        "bt_vendor_lib.h": "c"
    },
    "search.exclude": {
        "**/node_modules": true,
        "**/bower_components": true,
        "**/*.o": true,
        "**/out": true,
        "**/prebuilts": true,
        "**/kernel": true,
        "**/third_party": true,
        "**/.ccache": true,
        "**/.repo": true,
        "**/developtools": true,
        "**/napi_generator": true,
        "**/commonlibrary": true,
        "**/test": true,
        "**/device/board/chinasoft/common/uboot": true,
    },
    "C_Cpp.codeAnalysis.exclude": {
        "**/out":true,
        "**/kernel":true,
        "**/third_party":true,
        "**/.ccache":true,
        "**/.repo":true,
        "**/ccache.log":true,
        "**/ccache.log.old":true,
        "**/napi_generator":true,
        "**/commonlibrary":true,
        "**/test":true,
        "**/docs":true,
        "**/prebuilts":true,
        "**/device/board/chinasoft/common/uboot": true,
    },
    "C_Cpp.files.exclude": {
        "**/.vscode": true,
        "**/.vs": true,
        "**/out":true,
        "**/kernel":true,
        "**/third_party":true,
        "**/.ccache":true,
        "**/.repo":true,
        "**/ccache.log":true,
        "**/ccache.log.old":true,
        "**/napi_generator":true,
        "**/commonlibrary":true,
        "**/test":true,
        "**/docs":true,
        "**/prebuilts":true,
        "**/device/board/chinasoft/common/uboot": true,
    },
    "vsicons.dontShowNewVersionMessage": true,
    "editor.fontSize": 16,
    "cmake.configureOnOpen": true,
    "diffEditor.ignoreTrimWhitespace": false,
    "git.mergeEditor": true,
    "cmake.showOptionsMovedNotification": false,
    "cmake.pinnedCommands": [
        "workbench.action.tasks.configureTaskRunner",
        "workbench.action.tasks.runTask"
    ]
}
```

