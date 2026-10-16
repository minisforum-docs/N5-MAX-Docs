#!/bin/sh
# Build n5max-sata-lpm-fix_1.0.0_all.deb from the package/ tree.
# Only requires dpkg-deb (part of the dpkg package).
set -eu
cd "$(dirname "$0")"

VERSION="1.0.0"
OUT="dist/n5max-sata-lpm-fix_${VERSION}_all.deb"

# Normalize permissions (dpkg-deb is picky about maintainer script modes).
chmod 755 package/DEBIAN/postinst package/DEBIAN/prerm package/DEBIAN/postrm
chmod 644 package/DEBIAN/control
chmod 644 package/usr/lib/udev/rules.d/99-n5max-sata-lpm.rules
chmod 644 package/usr/lib/systemd/system/n5max-sata-lpm-fix.service

mkdir -p dist
dpkg-deb --build --root-owner-group package "$OUT"

echo
echo "== Package info =="
dpkg-deb -I "$OUT"
echo
echo "== Package contents =="
dpkg-deb -c "$OUT"
echo
echo "Built: $OUT"
