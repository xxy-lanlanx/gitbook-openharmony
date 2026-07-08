import os, re

ROOT = r"E:\doc\gitbook\gitbook-openharmony"
meta = {"OpenHarmony书籍分析报告.md","OpenHarmony书籍深度优化计划.md",
        "GitBook适配性报告.md","Phase0-地基改造完成报告.md","缺失章节骨架清单.md",
        "SUMMARY.md","mu-lu.md","README.md","xu-lun.md","zi-xu.md","cao-zuo-xi-tong.md"}

chaps = sorted(f for f in os.listdir(ROOT) if re.match(r'^\d{2}-.*\.md$', f) and f not in meta)
rows = []
for f in chaps:
    t = open(os.path.join(ROOT,f), encoding="utf-8-sig").read()
    cjk = len(re.findall(r'[一-鿿]', t))
    lat = len(re.findall(r'[A-Za-z0-9_]+', t))
    code = t.count('```')//2
    rows.append((f, cjk, lat, code))
rows.sort(key=lambda x: x[1])
print("chapter                         CJK    latin  code  total")
for f,cjk,lat,code in rows:
    print(f"{f:42s} {cjk:6d} {lat:6d} {code:4d}  {cjk+lat}")
print()
print("THINNEST 12 (by CJK):")
for f,cjk,lat,code in rows[:12]:
    print(f"  {f:42s} CJK={cjk} code={code}")
