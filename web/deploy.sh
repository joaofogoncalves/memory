#!/usr/bin/env bash
set -euo pipefail

# Deploy static site to a remote host via rsync over SSH.
#
# This script is configured for Opalstack hosting by default.
# To adapt for other providers:
#   - GitHub Pages: run `uv run python web/build.py`, then push web/dist/ to gh-pages
#   - Netlify / Vercel: point the build command to `uv run python web/build.py`
#     and set the publish directory to web/dist/
#   - Any SSH host: set the OPAL_* variables in .env to match your server
#
# All config lives in .env — copy .env.example and fill in your values.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$SCRIPT_DIR/dist"
ENV_FILE="$ROOT_DIR/.env"

# Load .env
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: .env file not found at $ENV_FILE"
  echo "Copy .env.example and add your Opalstack credentials."
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

# Validate required vars
: "${OPAL_SSH_USER:?Set OPAL_SSH_USER in .env (e.g. myuser)}"
: "${OPAL_SSH_HOST:?Set OPAL_SSH_HOST in .env (e.g. opal1.opalstack.com)}"
: "${OPAL_APP_PATH:?Set OPAL_APP_PATH in .env (e.g. /home/myuser/apps/mysite)}"
OPAL_SSH_PORT="${OPAL_SSH_PORT:-22}"

# Build first via uv (auto-syncs the project env from pyproject.toml).
# Capture build output so draft URLs can be surfaced after deploy, while
# still streaming it to the terminal live.
echo "Building site..."
BUILD_LOG="$(mktemp)"
trap 'rm -f "$BUILD_LOG"' EXIT
(cd "$ROOT_DIR" && uv run python "$SCRIPT_DIR/build.py") | tee "$BUILD_LOG"

# Deploy via rsync
echo ""
echo "Deploying to $OPAL_SSH_HOST:$OPAL_APP_PATH (port $OPAL_SSH_PORT)..."
rsync -avz --delete \
  --exclude='.DS_Store' \
  -e "ssh -p $OPAL_SSH_PORT" \
  "$DIST_DIR/" \
  "${OPAL_SSH_USER}@${OPAL_SSH_HOST}:${OPAL_APP_PATH}/"

# Surface draft article URLs (unlisted — reachable only by direct link).
# Build prints "Draft: /articles/drafts/<token>/  (<slug>)" lines; turn each
# into a full URL using SITE_URL from .env (falls back to the relative path).
DRAFT_LINES="$(grep -E 'Draft: /articles/drafts/' "$BUILD_LOG" 2>/dev/null || true)"
if [ -n "$DRAFT_LINES" ]; then
  BASE="${SITE_URL:-}"; BASE="${BASE%/}"
  echo ""
  echo "Draft articles (unlisted — direct link only):"
  while IFS= read -r line; do
    path="$(printf '%s\n' "$line" | grep -oE '/articles/drafts/[a-f0-9]+/')"
    [ -n "$path" ] || continue
    slug=""
    case "$line" in *\(*\)*) slug="${line##*\(}"; slug="${slug%%\)*}" ;; esac
    if [ -n "$slug" ]; then
      echo "  ${BASE}${path}  (${slug})"
    else
      echo "  ${BASE}${path}"
    fi
  done <<< "$DRAFT_LINES"
fi

echo ""
echo "Deploy complete."
