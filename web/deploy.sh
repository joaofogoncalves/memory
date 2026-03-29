#!/usr/bin/env bash
set -euo pipefail

# Deploy static site to Opalstack via rsync over SSH.
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

# Build first
echo "Building site..."
source "$ROOT_DIR/venv/bin/activate" 2>/dev/null || true
python "$SCRIPT_DIR/build.py"

# Deploy via rsync
echo ""
echo "Deploying to $OPAL_SSH_HOST:$OPAL_APP_PATH (port $OPAL_SSH_PORT)..."
rsync -avz --delete \
  --exclude='.DS_Store' \
  -e "ssh -p $OPAL_SSH_PORT" \
  "$DIST_DIR/" \
  "${OPAL_SSH_USER}@${OPAL_SSH_HOST}:${OPAL_APP_PATH}/"

echo ""
echo "Deploy complete."
