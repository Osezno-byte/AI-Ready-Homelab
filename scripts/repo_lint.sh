#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-.}"
cd "$ROOT_DIR"

echo "== AI-Ready-Homelab • Repo Lint =="
echo "Scanning in: $(pwd)"
echo

# Prefer ripgrep if available
if command -v rg >/dev/null 2>&1; then
  G="rg -n --hidden --no-ignore --follow --color never"
else
  G="grep -RIn --binary-files=without-match"
fi

# Common exclusions
EXCL='--glob=!./.git/* --glob=!./docs/images/* --glob=!./**/*.png --glob=!./**/*.jpg --glob=!./**/*.jpeg --glob=!./**/*.svg'

# Buckets
declare -A BUCKETS

# 1) Stray collaborator or AI assistant names (should be gone)
BUCKETS[stray_names]='\b(Solace|Claude)\b'

# 2) Placeholders / WIP
BUCKETS[placeholders]='\b(TODO|FIXME|WIP|DRAFT|coming soon)\b'

# 3) Lowercase repo path (prefer canonical casing)
BUCKETS[repo_casing]='\bai-ready-homelab\b'

# 4) Competitive tone we tried to avoid
BUCKETS[competitive]='\b(competitor|competitors|vs\.|versus)\b'

# 5) Vendor refs (allowed if truly necessary; we just flag for review)
BUCKETS[vendors]='\b(ChatGPT|OpenAI|Claude|Anthropic|Gemini|Google AI|Bard|Copilot)\b'

# 6) Emoji/emoji-like markers (heads-up only)
BUCKETS[emoji]='[✅❌⛔⚠️✨🚀🔥🎯💥⭐👍👎💡📝]'

# 7) Odd phrasing we explicitly replaced earlier
BUCKETS[odd_phrasing]='Plan Cloud AI|safety officer|24-48 hours'

# 8) Empty markdown links or obvious link typos
BUCKETS[md_link_smells]='\[[^]]*\]\(\s*\)|\(\)|\[(\s*)\]'

# 9) Private/DM language in Discussions (since Discussions are public)
BUCKETS[privacy_discussions]='private thread in GitHub Discussions'

# 10) Cloud-required wording (should always be optional)
BUCKETS[cloud_required]='\brequire(s|d)? cloud\b'

# Scan function
scan_bucket () {
  local key="$1" pattern="${BUCKETS[$1]}"
  echo ">> $key"
  # shellcheck disable=SC2086
  if $G $EXCL -H -e "$pattern" . >/tmp/_lint_"$key".out 2>/dev/null; then
    cat /tmp/_lint_"$key".out
  else
    echo "(none)"
  fi
  echo
}

# Run all buckets
for k in "${!BUCKETS[@]}"; do
  scan_bucket "$k"
done

# Unicode emoji sweep via python (more complete)
echo ">> emoji_unicode (broad sweep)"
python3 - <<'PY' || true
import os, re
emoji_pattern = re.compile(r'[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U00002600-\U000026FF]')
hits = []
for root, _, files in os.walk(".", topdown=True):
    if "/.git/" in root or "/docs/images/" in root:
        continue
    for f in files:
        if f.lower().endswith((".png",".jpg",".jpeg",".svg",".gif",".ico")):
            continue
        path = os.path.join(root, f)
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                for i, line in enumerate(fh, 1):
                    if emoji_pattern.search(line):
                        hits.append(f"{path}:{i}:{line.rstrip()}")
        except Exception:
            pass
if hits:
    print("\n".join(hits))
else:
    print("(none)")
PY
echo

echo "== Lint complete =="
