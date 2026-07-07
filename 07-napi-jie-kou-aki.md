---
description: NAPI接口-aki
---

# 07-NAPI接口-aki





## 简介





正常使用NAPI写接口，太过于复杂，体验十分的差，这里提供一个很好的工具，开箱即用，开发者只需关注c++逻辑实现即可。





AKI (Alpha Kernel Interacting) 是一款边界性编程体验友好的ArkTs FFI开发框架，针对OpenHarmony Native开发提供JS与C/C++跨语言访问场景解决方案。支持极简语法糖使用方式，一行代码完成JS与C/C++的无障碍跨语言互调，所键即所得。





链接：





[https://gitcode.com/openharmony-sig/aki](https://gitcode.com/openharmony-sig/aki)





## 优势





1. 极简使用，解耦FFI代码与业务代码，友好的边界性编程体验；


2. 提供完整的数据类型转换、函数绑定、对象绑定、线程安全等特性；


3. 支持JS & C/C++互调；


4. 支持与Node-API嵌套使用；





![](assets/image-3-1-1-1-1.png)





## 使用





非常简易的使用





CMakeLists.txt定义





```cmake


# the minimum version of CMake.


cmake_minimum_required(VERSION 3.4.1)


project(aki_demo)





set(NATIVERENDER_ROOT_PATH ${CMAKE_CURRENT_SOURCE_DIR})





include_directories(${NATIVERENDER_ROOT_PATH}


                    ${NATIVERENDER_ROOT_PATH}/include)





# 本例直接使用根目录源码作为依赖，实际工程使用时，需要`clone`源码到指定路径


set(NATIVERENDER_ROOT_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../../../../aki/)





add_library(entry SHARED hello.cpp)





add_subdirectory(${NATIVERENDER_ROOT_PATH} aki)





target_link_libraries(entry PUBLIC


    aki_jsbind)


```





样例cpp





```cpp


#include <string>


#include <aki/jsbind.h>





std::string SayHello(std::string msg)


{


    return msg + " too.";


}





JSBIND_GLOBAL()


{


    JSBIND_FUNCTION(SayHello);


}





JSBIND_ADDON(hello) // 注册 AKI 插件名为: hello


```





调用





<pre class="language-javascript"><code class="lang-javascript"><strong>import aki from 'libentry.so'


</strong><strong>


</strong>this.message = aki.SayHello("hello world");


</code></pre>





比正常接入多了一个so





![](assets/image-30.png)





开发过程再也不用关心一大堆复杂的定义和类型转换





其他使用参考文档：[https://gitcode.com/openharmony-sig/aki/blob/master/README.md](https://gitcode.com/openharmony-sig/aki/blob/master/README.md)

## 相关阅读

- [NAPI接口](07-napi-jie-kou.md)
- [源码结构](05-yuan-ma-jie-gou.md)
