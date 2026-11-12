# The Samsung ABL / dtbo trap

**Short version:** Samsung's bootloader (ABL) always applies the overlay found in the `dtbo` partition on top of the DTB inside `boot`.
With a normal mainline DTB this fails and the tablet drops into **Download mode** (USB id `04e8:685d`) or appears stuck at the Samsung logo.
The kernel never even starts. The fix is two small things.

## What happens
The stock `dtbo` is a Qualcomm/Samsung overlay (compatible `qcom,atoll-ab-idp` / `qcom,atoll-ab`, `qcom,board-id = <0x22 0>`, no msm-id,
about 120 fragments for display, touch, camera, audio, thermal...). Its fragment targets are resolved by label (161 labels) through `__fixups__`.
A mainline DTB neither has those labels nor `/__symbols__`. The ABL's (old, Android-O-era) libufdt then fails.

The ABL log lives in the `debug` partition (readable read-only from recovery). I saw, in this order:

1. `Bad main_symbols in ufdt_overlay_do_fixups` ... `Dtb overlay failed` ... `Launching Download Mode`
   -> **the base DTB has no `/__symbols__`.** Build the DTB with `DTC_FLAGS=-@`. Check with `fdtget <dtb> /__symbols__`.
2. `Bad overlay_fixups`
   -> the old libufdt also needs **`__fixups__` in the overlay itself**. The stock overlay does not fit a mainline DTB anyway, so flash a minimal overlay
   with a valid `__fixups__` (compile `dtbo/overlay-gta4xlve-fixups.dts` with `dtc -@`; `tools/build-dtbo.sh` wraps it into the dtbo image format).
3. Success: `Apply Overlay total time NN ms` (34 ms on my device), followed by the end of UEFI. The kernel starts.

## Rules that must hold
- `boot.img` must keep `qcom,msm-id = <0x1bb 0>` and `qcom,board-id = <0x22 0>` in the DTB, otherwise the ABL picks no DTB.
- The overlay root has `compatible = "samsung,gta4xlve", "qcom,sm7125"`, the same msm-id and board-id as the DTB.
- My overlay has one fragment that targets the `reserved_memory` label and adds a `ramoops` node (`0xb4600000`, 1 MiB; record/console/ftrace/pmsg 256 KiB each, `no-map`).
  The point is not the node itself but a valid, minimal overlay with `__fixups__`. It also gives pstore logs (`/sys/fs/pstore`) for debugging.
  The DTB therefore needs a `reserved_memory:` label (all my DTBs have it).
- dtbo image format: mkdtboimg v0, header 32 bytes, one entry (id, rev, custom all 0), DTB at offset 64.
  `dtbo-gta4xlve-fixups.img` is 685 bytes; the partition is 24 MiB and keeps old data behind the image, which is harmless.

## Debugging without a UART console
- `loglevel=8 ignore_loglevel` plus pstore/ramoops; after a hang reboot into recovery and read `/sys/fs/pstore/`.
- No initramfs means no USB networking during very early boot; that is normal.
- Do not paste the raw ABL log anywhere: it contains the device S/N.
