---
description: XTS子系统
---

# 21-XTS子系统





## 简介





XTS子系统是OpenHarmony兼容性测评套件的集合，当前包括acts（application compatibility test suite）应用兼容性测试套件，后续会拓展dcts（device compatibility test suite）设备兼容性测试套件等。





XTS子系统当前包括acts与tools软件包：





acts，存放acts相关测试用例源码与配置文件，其目的是帮助终端设备厂商尽早发现软件与OpenHarmony的不兼容性，确保软件在整个开发过程中满足OpenHarmony的兼容性要求。





tools，存放acts相关测试用例开发框架。





## 结构





```


/test/xts


├── acts                # 测试代码存放目录


│   └── subsystem       # 标准系统子系统测试用例源码存放目录


│   └── subsystem_lite  # 轻量系统、小型系统子系统测试用例源码存放目录


│   └── BUILD.gn        # 标准系统测试用例编译配置


│   └── build_lite      # 轻量系统、小型系统测试用例编译配置存放目录


│       └── BUILD.gn    # 轻量系统、小型系统测试用例编译配置


└── tools               # 测试工具代码存放目录


```





参考文档：[https://gitcode.com/openharmony/docs/blob/master/zh-cn/readme/XTS%E5%AD%90%E7%B3%BB%E7%BB%9F.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/readme/XTS%E5%AD%90%E7%B3%BB%E7%BB%9F.md)

## 相关阅读

- [DFX子系统](20-dfx-zi-xi-tong.md)
- [架构篇](04-jia-gou-pian.md)
