---
name: nj-deploy-preview
description: newjeans-line 发布：只发 gh-pages /preview/（和 /tapper/），根目录（正式版）不动，普通 commit 不 force-push，发完核对 build.json；以及推送被 Auto-review 拦截时怎么办。发布预览、推分支、回滚时读。
---

# 发布预览

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
- 做法：**原样**重试同一条命令，带 `request_smart_mode_approval: true` 和 `smart_mode_block_reason`（上面那句原文），让用户在审批卡片上批准。不要改写命令、不要换别的方式绕过。被拒就停下并报告。

## 回滚
```sh
cd /workspace/nj-ghp && git fetch origin gh-pages && git checkout --detach origin/gh-pages
git revert --no-edit <preview commit> && git push origin HEAD:gh-pages
```
