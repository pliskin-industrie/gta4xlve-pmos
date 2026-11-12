#!/bin/sh
# Build the minimal dtbo image (mkdtboimg format v0, one entry, id/rev/custom = 0)
# from dtbo/overlay-gta4xlve-fixups.dts. Needs dtc and python3.
# Usage: tools/build-dtbo.sh dtbo/overlay-gta4xlve-fixups.dts dtbo-gta4xlve-fixups.img
set -e
src="$1"; out="$2"
[ -n "$src" ] && [ -n "$out" ] || { echo "usage: $0 overlay.dts out.img"; exit 1; }
tmp=$(mktemp)
dtc -I dts -O dtb -@ -o "$tmp" "$src" 2>/dev/null
python3 - "$tmp" "$out" <<'PY'
import struct, sys
d = open(sys.argv[1], 'rb').read()
hdr = struct.pack('>8I', 0xd7b7ab1e, 64 + len(d), 32, 32, 1, 32, 4096, 0)
ent = struct.pack('>8I', len(d), 64, 0, 0, 0, 0, 0, 0)
open(sys.argv[2], 'wb').write(hdr + ent + d)
PY
rm -f "$tmp"
sha256sum "$out"
