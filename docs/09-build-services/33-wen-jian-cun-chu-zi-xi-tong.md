---
description: OpenHarmony 文件与存储管理（分布式文件系统、沙箱目录、媒体库、存储统计）。
---

# 33-文件与存储子系统

文件与存储子系统管理设备的文件系统、应用沙箱目录与媒体库，并支持分布式文件访问。它与[23-权限与访问控制](../../07-security/23-quan-xian-guan-li-zi-xi-tong.md) 的沙箱隔离、[17-分布式数据管理](../../05-media-distributed/17-fen-bu-shi-shu-ju-guan-li.md) 的分布式能力协同，决定了应用"能读到什么、写到哪里"。

## 一、文件系统

- **本地文件系统**：标准目录布局（`/system`、`/vendor`、`/data`、`/storage` 等），由 [19-内核子系统](../../03-driver-boot/19-kernel/19-nei-he-zi-xi-tong-linux-nei-he-jia-gou.md) 的文件系统驱动支撑。
- **分布式文件系统（hmdfs）**：把远端可信设备的目录挂载到本地命名空间，应用访问远端文件如同访问本地——前提是设备已通过 [23-安全子系统](../../07-security/23-an-quan-zi-xi-tong.md) 认证。

## 二、应用沙箱目录

每个应用拥有独立沙箱，按加密级别（EL1 开机即可用 / EL2 首次解锁后可用）分层：

| 目录 | 说明 | 权限 |
| --- | --- | --- |
| `context.filesDir` | 应用私有文件 | 应用自身，无需申请 |
| `context.cacheDir` | 缓存，系统可清理 | 应用自身 |
| 公共目录（下载/文档/媒体） | 跨应用共享 | 需对应权限 |
| 其它应用沙箱 | 不可直接访问 | 禁止（沙箱隔离） |

> 跨应用文件访问必须经系统提供的公共目录或媒体库 API，不能直接用路径读取他人沙箱。

## 三、媒体库

图片、视频、音频等媒体资源由媒体库统一管理，应用通过选择器 / 媒体管理 API 进行增删查改，且受 [23-权限与访问控制](../../07-security/23-quan-xian-guan-li-zi-xi-tong.md) 的媒体权限约束。

```ts
import { fileIo as fs } from '@kit.CoreFileKit';

const context = getContext(this);
const filePath = context.filesDir + '/demo.txt';

// 写入
let file = fs.openSync(filePath, fs.OpenMode.CREATE | fs.OpenMode.READ_WRITE);
fs.writeSync(file.fd, 'hello openharmony');
fs.closeSync(file);

// 读取
file = fs.openSync(filePath, fs.OpenMode.READ_ONLY);
const buf = new ArrayBuffer(1024);
fs.readSync(file.fd, buf);
fs.closeSync(file);
console.info('content:', String.fromCharCode.apply(null, new Uint8Array(buf)));
```

## 四、存储统计与配额

- **查询**：通过 `storageStatistics` 获取总空间、可用空间、各应用占用；
- **配额**：系统对单应用可占用空间设限，防止某个应用占满用户数据分区；
- **清理**：缓存目录可由系统在空间紧张时回收。

## 五、常见问题与排查

1. **读取他人文件失败**：沙箱隔离；改用公共目录 / 媒体库等受控通道。
2. **媒体库访问被拒**：未申请媒体读取/写入权限，确认运行时已授权。
3. **分布式文件打不开**：目标设备未认证或离线，先完成 [27-分布式任务调度](../../05-media-distributed/27-fen-bu-shi-ren-wu-diao-du.md) 的设备信任流程。
4. **EL2 目录读不到**：EL2 文件需设备解锁后访问，开机早期只能访问 EL1。

## 相关阅读

- [17-分布式数据管理](../../05-media-distributed/17-fen-bu-shi-shu-ju-guan-li.md)
- [15-媒体子系统](../../05-media-distributed/15-mei-ti-zi-xi-tong.md)
- [23-权限与访问控制](../../07-security/23-quan-xian-guan-li-zi-xi-tong.md)

## 参考资源

- OpenHarmony 文件管理官方文档（代码仓 `filemanagement`）
- ArkTS 接口：`@kit.CoreFileKit`（`fileIo`）、`storageStatistics`
