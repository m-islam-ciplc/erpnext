#!/usr/bin/env bash
set -euo pipefail

SITE="assets.localhost"
BENCH="$HOME/frappe-bench"
DB_ROOT_PASSWORD="admin"

cd "$BENCH"

echo "=== Stopping bench processes (if any) ==="
pkill -f "bench start" 2>/dev/null || true
pkill -f "honcho" 2>/dev/null || true
sleep 2

echo "=== Flushing Redis ==="
redis-cli -p 6380 FLUSHALL 2>/dev/null || true

echo "=== Dropping site $SITE ==="
bench drop-site "$SITE" --force --no-backup \
  --db-root-password "$DB_ROOT_PASSWORD" || true

echo "=== Creating fresh site $SITE ==="
bench new-site "$SITE" \
  --db-host 127.0.0.1 \
  --db-port 3307 \
  --mariadb-root-password "$DB_ROOT_PASSWORD" \
  --admin-password admin \
  --install-app erpnext \
  --set-default

echo "=== Enabling developer mode ==="
bench --site "$SITE" set-config developer_mode 1

echo "=== Disabling public signup ==="
bench --site "$SITE" execute frappe.db.set_single_value --args "['Website Settings', 'disable_signup', 1]"

echo "=== Building assets ==="
bench build --app frappe
bench build --app erpnext

echo "=== Reset complete ==="
bench --site "$SITE" execute frappe.db.get_single_value --args "['System Settings', 'setup_complete']"
