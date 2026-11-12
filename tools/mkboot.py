# mkboot.py <Image.gz> <dtb> <out.img> <template-boot.img>
# Builds a boot.img from a template boot.img: only kernel + DTB are replaced.
# Header v2, offsets, pagesize, os_version, board, ramdisk and cmdline are kept from the template.
import struct, hashlib, sys
W = sys.argv[4]  # template boot.img (your own, known-good)
P = 4096; al = lambda n: (n + P - 1) // P * P
LIMIT = 96 * 1024 * 1024
b = open(W, 'rb').read()
assert b[:8] == b'ANDROID!' and struct.unpack_from('<I', b, 40)[0] == 2 and struct.unpack_from('<I', b, 36)[0] == P
ks, rs = struct.unpack_from('<I', b, 8)[0], struct.unpack_from('<I', b, 16)[0]
ds = struct.unpack_from('<I', b, 1648)[0]
roff = P + al(ks); doff = roff + al(rs)
k_old = b[P:P + ks]; rd = b[roff:roff + rs]; d_old = b[doff:doff + ds]
tail = b[doff + al(ds):]

def hid(k, r, d):
    s = hashlib.sha1()
    for x in (k, r, b''): s.update(x); s.update(struct.pack('<I', len(x)))
    s.update(struct.pack('<I', 0)); s.update(d); s.update(struct.pack('<I', len(d)))
    return s.digest() + b'\0' * 12
assert hid(k_old, rd, d_old) == b[576:608], 'id formula does not match template'

k = open(sys.argv[1], 'rb').read(); d = open(sys.argv[2], 'rb').read()
assert k[:2] == b'\x1f\x8b', 'kernel is not gzip'
assert d[:4] == b'\xd0\x0d\xfe\xed', 'not a DTB'
h = bytearray(b[:P])
struct.pack_into('<I', h, 8, len(k)); struct.pack_into('<I', h, 1648, len(d))
h[576:608] = hid(k, rd, d)
pad = lambda x: x + b'\0' * (al(len(x)) - len(x))
out = bytes(h) + pad(k) + pad(rd) + pad(d) + tail
assert len(out) < LIMIT, len(out)
open(sys.argv[3], 'wb').write(out)
diff = [i for i in range(P) if b[i] != out[i]]
assert all(8 <= i < 12 or 576 <= i < 608 or 1648 <= i < 1652 for i in diff), diff
print('cmdline unchanged:', out[64:576] == b[64:576] and out[608:1632] == b[608:1632], '| ramdisk unchanged:', out[P + al(len(k)):][:rs] == rd)
print('cmdline:', (h[64:576].rstrip(b'\0') + h[608:1632].rstrip(b'\0')).decode())
print(f'Kernel {len(k)} B, DTB {len(d)} B, Image {len(out)} B ({len(out) / LIMIT:.1%} of 96 MiB)')
print('SHA256', hashlib.sha256(out).hexdigest())
