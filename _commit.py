import subprocess
subprocess.run(['git', 'commit', '-m', 'docs: 扩充16篇薄壳子系统文档（阶段1）\n\n- GPU适配、通信、分布式数据、帐号、软总线、电源\n- 全球化、OTA、Linux内核架构、分布式硬件\n- 位置服务、文件存储、DFX、轻量图形、媒体、DRM\n\n新增内容涵盖：\n- 架构层次、典型流程、代码示例、权限矩阵\n- 常见问题调试表、性能权衡、隐私合规、跨设备协同'])
r = subprocess.run(['git', 'push'], capture_output=True, text=True)
print(r.stdout)
print(r.stderr)
