#!/usr/bin/env bash
# Full pipeline: scrape → resolve links → build → deploy
#
# Run this whenever you want to refresh the site with new posts.
# On first use, log in once with:  python scraper/main.py --browser-login
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

# Activate venv and set Python path so scraper/ imports resolve
source "$SCRIPT_DIR/venv/bin/activate"
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
  python "$SCRIPT_DIR/scraper/main.py" --crawl --profile-url "$LINKEDIN_PROFILE_URL" $LIMIT_FLAG
  echo ""
fi

# ── 2. Resolve shortened URLs ────────────────────────────────────────────────
echo "=== Resolving shortened URLs ==="
python "$SCRIPT_DIR/web/resolve_links.py"
echo ""

# ── 3. Build & deploy ────────────────────────────────────────────────────────
if [ "$DRY_RUN" = false ]; then
  echo "=== Building & deploying site ==="
  bash "$SCRIPT_DIR/web/deploy.sh"
else
  echo "=== Dry run: building site only (no deploy) ==="
  python "$SCRIPT_DIR/web/build.py"
fi

echo ""
echo "Pipeline complete."
