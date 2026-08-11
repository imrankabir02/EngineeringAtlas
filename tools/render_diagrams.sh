#!/usr/bin/env bash
#
# Render graph/diagrams/*.mmd to light and dark SVGs.
#
# Stage 2 of the diagram pipeline. Stage 1 (tools/generate_diagrams.py) derives the
# Mermaid sources from the graph and is pure Python; this stage needs node and a
# Chromium, which is why it is kept out of CI. CI instead verifies that each SVG carries
# the checksum of the .mmd it was rendered from, so a stale image fails without anything
# having to render.
#
# Why committed SVGs at all: GitHub renders Mermaid on the web but not in its mobile
# apps, where a ```mermaid block falls back to raw source. Images render everywhere.
#
# Usage:
#     tools/render_diagrams.sh            # render every diagram
#     tools/render_diagrams.sh spine      # render one, by view id
#
set -euo pipefail

cd "$(dirname "$0")/.."
DIAGRAMS="graph/diagrams"

# GitHub's canvas colours, so the images sit flush with the page in both themes.
LIGHT_BG="#ffffff"
DARK_BG="#0d1117"

if ! command -v npx >/dev/null 2>&1; then
  echo "error: node/npx not found. Install Node 18+ and retry." >&2
  exit 1
fi

# Reuse a preinstalled Chromium when one is present rather than downloading another.
if [ -z "${PUPPETEER_EXECUTABLE_PATH:-}" ]; then
  for candidate in \
      /opt/pw-browsers/chromium-*/chrome-linux/chrome \
      "$(command -v chromium || true)" \
      "$(command -v chromium-browser || true)" \
      "$(command -v google-chrome || true)"; do
    if [ -x "$candidate" ]; then
      export PUPPETEER_EXECUTABLE_PATH="$candidate"
      break
    fi
  done
fi
echo "chromium: ${PUPPETEER_EXECUTABLE_PATH:-<puppeteer default>}"

PUPPETEER_CFG="$(mktemp)"
MERMAID_CFG="$(mktemp)"
trap 'rm -f "$PUPPETEER_CFG" "$MERMAID_CFG"' EXIT

cat > "$PUPPETEER_CFG" <<EOF
{
  "executablePath": "${PUPPETEER_EXECUTABLE_PATH:-}",
  "args": ["--no-sandbox", "--disable-dev-shm-usage"]
}
EOF

# securityLevel strict matches how GitHub renders Mermaid. htmlLabels stays on because
# it is Mermaid's default, but the generated sources avoid depending on it - see the
# note in tools/generate_diagrams.py.
cat > "$MERMAID_CFG" <<'EOF'
{ "securityLevel": "strict", "flowchart": { "htmlLabels": true, "useMaxWidth": true } }
EOF

targets=()
if [ "$#" -gt 0 ]; then
  for id in "$@"; do targets+=("$DIAGRAMS/$id.mmd"); done
else
  while IFS= read -r f; do targets+=("$f"); done < <(find "$DIAGRAMS" -name '*.mmd' | sort)
fi

if [ "${#targets[@]}" -eq 0 ]; then
  echo "error: no .mmd sources found. Run: python3 tools/generate_diagrams.py" >&2
  exit 1
fi

for src in "${targets[@]}"; do
  [ -f "$src" ] || { echo "error: $src not found" >&2; exit 1; }
  id="$(basename "$src" .mmd)"
  # Must match digest() in tools/generate_diagrams.py: sha256, first 16 hex chars.
  sha="$(python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()[:16])" "$src")"

  for variant in light dark; do
    case "$variant" in
      light) theme=neutral; bg="$LIGHT_BG" ;;
      dark)  theme=dark;    bg="$DARK_BG" ;;
    esac
    out="$DIAGRAMS/$id-$variant.svg"
    npx --yes @mermaid-js/mermaid-cli \
      -i "$src" -o "$out" \
      -t "$theme" -b "$bg" \
      -c "$MERMAID_CFG" -p "$PUPPETEER_CFG" \
      --quiet >/dev/null

    # Stamp the source checksum so the CI staleness check can close the loop.
    python3 - "$out" "$sha" <<'PY'
import sys, pathlib
out, sha = pathlib.Path(sys.argv[1]), sys.argv[2]
text = out.read_text(encoding="utf-8")
marker = f"<!-- mmd-sha256:{sha} -->\n"
if not text.startswith("<!--"):
    out.write_text(marker + text, encoding="utf-8")
PY
    echo "  $out  ($theme)"
  done
done

echo
echo "Rendered ${#targets[@]} diagram(s). Verify with: python3 tools/generate_diagrams.py --check"
