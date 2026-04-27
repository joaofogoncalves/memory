#!/usr/bin/env bash
# Full pipeline: scrape → resolve links → build → deploy
#
# Run this whenever you want to refresh the site with new posts.
# Dependencies are managed by uv (see pyproject.toml). On first use:
#   uv sync                                    # install deps
#   uv run playwright install chromium         # install browser
#   uv run python -m scraper.main --browser-login   # log in
#
# Usage:
#   bash pipeline.sh              # scrape + resolve + deploy
#   bash pipeline.sh --skip-scrape  # resolve + deploy only (skip crawl)
#   bash pipeline.sh --dry-run    # scrape + resolve (no deploy)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

# Load .env
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: .env not found. Copy .env.example and fill in your values."
  exit 1
fi
set -a; source "$ENV_FILE"; set +a

# uv run auto-syncs and runs in the project env. Set PYTHONPATH so scraper/
# imports resolve when scripts are invoked by file path.
export PYTHONPATH="$SCRIPT_DIR"

SKIP_SCRAPE=false
DRY_RUN=false
LIMIT=""
for arg in "$@"; do
  case $arg in
    --skip-scrape) SKIP_SCRAPE=true ;;
    --dry-run)     DRY_RUN=true ;;
    --limit=*)     LIMIT="${arg#*=}" ;;
  esac
done

# ── 1. Scrape new posts ──────────────────────────────────────────────────────
if [ "$SKIP_SCRAPE" = false ]; then
  : "${LINKEDIN_PROFILE_URL:?Set LINKEDIN_PROFILE_URL in .env}"
  LIMIT_FLAG=""
  [ -n "$LIMIT" ] && LIMIT_FLAG="--limit $LIMIT"
  echo "=== Scraping LinkedIn posts ==="
  uv run python "$SCRIPT_DIR/scraper/main.py" --crawl --profile-url "$LINKEDIN_PROFILE_URL" $LIMIT_FLAG
  echo ""
fi

# ── 2. Resolve shortened URLs ────────────────────────────────────────────────
echo "=== Resolving shortened URLs ==="
uv run python "$SCRIPT_DIR/web/resolve_links.py"
echo ""

# ── 3. Build & deploy ────────────────────────────────────────────────────────
if [ "$DRY_RUN" = false ]; then
  echo "=== Building & deploying site ==="
  bash "$SCRIPT_DIR/web/deploy.sh"
else
  echo "=== Dry run: building site only (no deploy) ==="
  uv run python "$SCRIPT_DIR/web/build.py"
fi

echo ""
echo "Pipeline complete."
