# 项目长期记忆：gitbook-openharmony

## 项目性质
OpenHarmony 中文技术 GitBook（30+ 章节，覆盖学习/环境/架构/源码/各子系统/内核）。
优化目标：从当前约 2.7 万字占位稿扩到 8–10 万字，核心子系统达 L3。计划书见 `OpenHarmony书籍深度优化计划.md`。

## 工具链关键事实（易复犯，务必记牢）
- managed Python 运行时路径：`C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python\python.exe`（内层 `python/` 才是真 home）。外层 `versions\3.13.12\python.exe` 与 `envs/default/Scripts/python.exe` 均已失效（报 "No module named encodings"）。
- Bash 里 `PYTHONPATH` 被指到 WorkBuddy cli shim，会污染导入；运行前 `PYTHONPATH=""` 或直接使用上面内层解释器。
- 优先用 Write 写 .py 再执行，避免 heredoc 触发 env 异常。

## 已完成的重要改造（Phase 0，2026-07-07）
- 文件名统一 NN-topic.md；SUMMARY/mu-lu 对 11/12/19 分组且一致。
- 122 张 `<figure>` 图片语法已迁移为标准 Markdown，0 断图。
- 30 篇 frontmatter 已规范化；30 篇末均有 `## 相关阅读` 互链。
- ~~遗留：14 张孤儿图片资源（.gitbook/assets 未被引用）~~ → 已于 2026-07-07 清理（git rm 删除，assets/ 现余 122 张且全部被引用）。

## GitBook 网页编辑器冲突风险（重要）
- GitBook.com 网页端会自动生成提交（如 `bd96037 GitBook: Update content`），把源图片写回 `.gitbook/assets/`、将章节重组成子文件夹 `xxx/README.md`、并把图片路径换回 `.gitbook/assets/...`，与本地 gitbook-cli 结构冲突。此类提交经核对**仅含表面改动（标题大小写、列表符号、图路径），正文零新增**，可直接 force-push 覆盖。
- 推送策略：普通 push 被拒时，先 `git fetch` + `git merge-tree --write-tree HEAD origin/main` 预览冲突（通常仅 SUMMARY.md 冲突），核对远端提交无独特内容后，用 `git push --force-with-lease` 覆盖。禁止 `--force` 硬推；优先 `--force-with-lease`。
- 结论：本项目以 gitbook-cli 为准（有 book.json + .gitignore 忽略 .gitbook/、源码图在 assets/）。勿在网页端编辑，避免再次产生分歧提交。
