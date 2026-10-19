---
name: nj-deploy-preview
description: newjeans-line 发布：只发 gh-pages /preview/（和 /tapper/），根目录（正式版）不动，普通 commit 不 force-push，发完核对 build.json；以及推送被 Auto-review 拦截时怎么办。发布预览、推分支、回滚时读。
---

# 发布预览

## 当前修复分支与可靠发布
- 当前源码 `omg-c-fix-20261019`，不把历史omg-c分工或停止消息误当当前分支操作。用户本轮明确“修好直接发布”，仅覆盖预览修复。
- 可用正常git发布时沿用脚本；若当前没有git写凭据但已有授权GitHub连接器，可通过Git对象API创建blob/tree/commit并用expected SHA做快进更新。这不允许绕过被拒绝的操作或访问限制。
- 大包不要塞进一个含内联内容的create_tree：逐文件create_blob并核对Git blob SHA，再创建只含SHA的preview子树；以当前gh-pages根树为base只替换preview目录。
- 源码tree须与 `git write-tree` 一致；分支变化时读取新head并协调，绝不force。提交后重新build，使内置版本与build.json一致。
- 保护验证：`git diff OLD NEW -- . ':(exclude)preview/**'` 应为空。等待Pages success，核对线上build.json及主JS字节/哈希，不能只见推送成功就说上线。
- `?v=<shortsha>` 是缓存区分标记，不是密码或功能开关，也不固定保存历史部署；不带v的固定预览地址可正常访问。问到时用一句话解释。

## 用户明确指定本机兜底时
- 2026-10-19本轮因GitHub Actions/Pages服务故障，用户明确要求Mac mini本地部署试玩。只在该明确授权的环境执行；此前不委派/不本机的项目限制不泛化覆盖这次新指令，也不泛化成今后默认Mac任务。
- 使用已验证发布包、独立且持久的静态目录；临时shell后台HTTP进程可能随执行结束退出，需用户级launchd托管，并在命令结束后重新检查PID、运行状态及HTTP资源。
- 只提供游戏静态目录，不把仓库、用户主目录、配置或密钥目录当网站根目录。保留已有服务、避免端口冲突。
- LAN链接、DNS解析、公网入口、HTTPS与蜂窝可达分别核实。ddns-go有域名不代表端口映射已通；配置需管理员权限时不修改权限、不输出密钥，可请用户仅提供域名文字。
- 网络/安全设置、端口映射、防火墙、隧道、持久凭据的新增或修改按当次审批要求处理，不能把“部署网站”无限扩大成改网络安全设置。
- GitHub故障时先确认官方状态和具体run；queued/waiting不是代码失败。不要重复堆积部署。取消请求可能延迟生效；既有运行build成功后优先完成原deploy，只有确认失败/取消才考虑恢复重试。
- 不同来源地址的localStorage存档独立，应提醒用导出/导入迁移，不能说原站数据被清了。

## 硬规则
- 只改 gh-pages 的 `preview/`；**根目录（正式版）和 `/tapper/` 不动**（tapper 用自己的脚本）。
- 只用普通 commit + 快进推送，**永不 force-push**，随时可 `git revert` 回滚。
- 发完核对线上 `preview/build.json` 的 hash 是新的，根目录和 `/tapper/` 仍返回 200。
- 用户让停（“你别继续做了”）或另一个 AI 在接手时，不要推 `omg-c` / 不要发预览。

## 发布预览：`tools/publish-preview.sh`
```sh
cd <要发布的分支的工作树>       # 例：/workspace/nj-omgc（omg-c）
npm test && python3 levels-design/validate.py omg --dir levels-src
tools/publish-preview.sh
```
脚本做的事：
1. `node tools/build-levels.mjs`（关卡美术 `public/levels/<slug>/art` 不进 git，必须先生成，否则 404 回退到程序化）。
2. `npx vite build --outDir /workspace/nj-preview-dist --emptyOutDir`。
3. 在 `/workspace/nj-ghp` 工作树里 detach 到 `origin/gh-pages`，替换 `preview/`。
4. 写 `preview/build.json`：`{"preview_of":"<branch>@<sha>","built":"<iso time>"}`（游戏的 stale-build 守卫读它）。
5. `git commit -m "Preview: <branch>@<sha> at /preview/ (live root unchanged)"` 并 `git push origin HEAD:gh-pages`。

## 发布后核对
```sh
curl -s "https://tbtnb.github.io/newjeans-line/preview/build.json?t=$(date +%s)"   # preview_of 应是新 sha
curl -s -o /dev/null -w '%{http_code}\n' https://tbtnb.github.io/newjeans-line/
curl -s -o /dev/null -w '%{http_code}\n' https://tbtnb.github.io/newjeans-line/tapper/
git -C /workspace/nj-ghp show --stat HEAD | head    # 只有 preview/ 下的文件变化
```
- GitHub Pages 缓存 max-age 600，可能要等几分钟；stale-build 守卫会让旧页面自动重载一次。
- 然后在线上 URL 跑一次脚本模拟通关（nj-qa-verification），再把链接发给用户：https://tbtnb.github.io/newjeans-line/preview/?level=omg，并提醒“刷新一下”。
- 源码分支也要推（例：`omg-c` 和 `omg-c-preview` 指向同一 commit），交接文件里写的 hash 要和线上一致。

## 打点工具：`tools/publish-tapper.sh`
- 只改 `tapper/`；脚本会检查 gh-pages 上 `tapper/` 以外有没有改动，有就拒绝；写 `tapper/build.json`（`tapper_of`）。音频共用站点的 `/audio/`。

## 正式版（根目录）
- 旧流程 `node scripts/publish-pages.mjs tbtnb/newjeans-line`（README）——**没有用户明确要求不要用**。

## 推送被 Auto-review 拦截
- 曾经 `git push origin omg-c` 被拦，理由：“The agent is trying to push commits to the remote repository on a branch not covered by the saved allow instructions. This requires approval because it is an outbound external effect.”
- 做法：按当前环境实际支持的审批机制处理；先核查现有授权，确需批准时说明准确目标与风险。历史字段不是通用API，不凭空传参。不要换工具绕过拒绝；拒绝未解除则停止该动作。

## 回滚
```sh
cd /workspace/nj-ghp && git fetch origin gh-pages && git checkout --detach origin/gh-pages
git revert --no-edit <preview commit> && git push origin HEAD:gh-pages
```
