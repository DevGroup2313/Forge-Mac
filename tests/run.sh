#!/bin/sh
# serve the Forge on a local port and run every test in turn; the exit code is the number of failed tests
cd "$(dirname "$0")/.." || exit 1
. tests/env.sh
mkdir -p tests/out tests/www
cp "$FORGE_HTML" tests/www/the_forge.html
( cd tests/www && npx --yes http-server -p "$FORGE_PORT" -s >/dev/null 2>&1 & echo $! > ../out/server.pid )
sleep 2
fails=0
for t in boot studio library storage_backup compare a11y; do
  echo "=== $t ==="
  if node "tests/$t.test.js"; then echo "--- $t: passed"; else echo "--- $t: FAILED"; fails=$((fails+1)); fi
done
kill "$(cat tests/out/server.pid)" 2>/dev/null
echo "failed: $fails"
exit $fails
