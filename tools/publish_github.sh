#!/usr/bin/env bash
# 一条命令把本地书稿仓库推到 GitHub。
# 用法：
#   bash tools/publish_github.sh                 # 只体检：认证状态 + 将公开的内容清单，不推送
#   bash tools/publish_github.sh --yes-public    # 建公开仓库并推送
#   bash tools/publish_github.sh --yes-private   # 建私有仓库并推送
# 仓库名可用 REPO=xxx 覆盖，默认 unitree-humanoid-book
set -uo pipefail
cd "$(dirname "$0")/.."
REPO="${REPO:-unitree-humanoid-book}"

if ! gh auth status >/dev/null 2>&1; then
  echo "✗ 未登录 GitHub。在你自己的终端跑一次（浏览器会打开你已登录的 Edge）："
  echo "      gh auth login        # GitHub.com → HTTPS → Login with a browser"
  echo "  完成后重跑本脚本。"
  exit 1
fi
echo "✓ 已登录：$(gh api user --jq .login 2>/dev/null || echo '?')"

FILES=$(git ls-files | wc -l | tr -d ' ')
SIZE=$(git ls-files -z | xargs -0 du -ch 2>/dev/null | tail -1 | cut -f1)
DRAFTS=$(git ls-files 'drafts/*' | wc -l | tr -d ' ')
echo "将推送：$FILES 个文件、$SIZE，其中正文草稿 $DRAFTS 个文件（17.6 万字全稿）"
echo "另有 verification/（十一轮审阅判定，含对宇树具体参数的对错结论）与 research/（一手证据存档）。"

case "${1:-}" in
  --yes-public)  VIS="--public" ;;
  --yes-private) VIS="--private" ;;
  *)
    echo
    echo "体检完成，未推送。确认要公开全稿就执行："
    echo "      bash tools/publish_github.sh --yes-public"
    echo "想先只公开可复现性证据（README + 门禁 + 图表 + 审阅记录，不含 drafts/）："
    echo "      bash tools/publish_github.sh --yes-private   # 先私有，之后随时可切公开"
    exit 0 ;;
esac

git push 2>/dev/null && { echo "已推送到既有远端。"; exit 0; }
gh repo create "$REPO" $VIS --source=. --remote=origin --push \
  && echo "✓ 完成：https://github.com/$(gh api user --jq .login)/$REPO" \
  || { echo "✗ 建库或推送失败，上面是原始报错。"; exit 1; }
