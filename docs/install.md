# Installation (SM-P613 / gta4xlve)

**Experimental. Unlocking wipes the tablet and permanently trips Knox. You can brick the device.**
Every step below was done by hand on one device; there is no installer. Read all of it first.

## Requirements
- SM-P613 (or SM-P619) with **OEM unlock** enabled in the developer options.
- Odin (Windows) with the Samsung USB driver, or Heimdall.
- A LineageOS recovery for gta4xlve(u) (root `adb`, used for backups and for reading the ABL log).
- A Linux PC with `pmbootstrap` (postmarketOS edge, `plasma-desktop`), an aarch64 cross toolchain if you build the kernel yourself.
- Optional but recommended for the first boot: a microSD card for the root filesystem.

## 1. Unlock and back up
1. Unlock the bootloader (Download mode, long press Vol-Up). The tablet is wiped.
2. Flash the LineageOS recovery with Odin (AP slot only, *Auto Reboot* off) and boot into it.
3. **Back up** from recovery with root `adb` and keep the files private (never upload them; they are device-specific and contain your IDs):
   `efs sec_efs persist modemst1 modemst2 fsg fsc persistent`, plus stock `boot` and `dtbo`.
   Use `dd` from `/dev/block/by-name/<name>` and verify with `sha256sum` on both sides.

## 2. Root filesystem
Build it with `pmbootstrap init` (edge, `plasma-desktop`) and `pmbootstrap install`. Two options I used:
- microSD (`--sdcard`) for the first boot, later moved to the internal `userdata` partition (ext4).
- directly on `userdata`.

Firmware: **I do not distribute any.** Copy the Qualcomm/Samsung firmware (ADSP, CDSP, venus, Adreno zap shader, Wi-Fi board data,
Bluetooth NVM) from the vendor partitions of **your own** device or your own stock firmware into `/lib/firmware/qcom/sm7125/gta4xlve/` and the usual `ath10k` / `qca` paths.

## 3. Kernel, modules, dtbo, boot image
There is no prebuilt boot image yet. The releases carry the dtbo image, the modules and the kernel config; build the kernel yourself (see README, "How to apply the patches") and then the boot image.
- **Modules** go to `/usr/lib/modules/<version>/` of the root filesystem (`depmod <version>` afterwards). Without them the display, touch, USB and battery work,
  but Wi-Fi, Bluetooth, sound and video do not (they are modules because their firmware is loaded from the root filesystem and there is no initramfs).
- **dtbo**: `dtbo-gta4xlve-fixups.img` to the `dtbo` partition (see `docs/abl-dtbo.md`; this is mandatory).
- **boot.img**: Android boot image header v2, page size 4096, `msm-id 0x1bb`, `board-id 0x22`, kernel `Image.gz`, DTB built with `-@`,
  no initramfs needed. `tools/mkboot.py` repacks a known-good `boot.img` of your own with a new kernel and DTB: `python3 tools/mkboot.py Image.gz dtb out.img template-boot.img`.
  The kernel command line selects the root filesystem. Without an initramfs the kernel can only resolve a `root=` value given as the PARTUUID of your partition
  or as a plain device node (`/dev/sdaNN`; `LABEL=` does not work). Set your own, followed by `rootfstype=ext4 rootwait rw`.
  Useful extras: `systemd.firstboot=no` (a headless first boot otherwise stalls), `console=tty0`, `consoleblank=0`, `clk_ignore_unused pd_ignore_unused`.

## 4. Flash
Flash `dtbo` first, then `boot`, either as an Odin AP tar (`boot.img` inside) or with `dd` from recovery, and **read the partition back and compare the hash**
(`head -c <size> /dev/block/by-name/boot | sha256sum`). Check the partition name first (`readlink -f /dev/block/by-name/boot`), and never touch
`abl`, `xbl`, `tz`, modem, `efs` or `persist`.

## 5. First boot
Reboot from the recovery menu. The first boot can take about a minute. Reach it via Wi-Fi/ssh or USB-NCM (`172.16.42.1`, the postmarketOS default).
If you land in Download mode, read `docs/abl-dtbo.md`.

## 6. After boot
- Speakers: see `docs/hacks.md` (UCM link, TAS2562 workaround).
- Never mount the root filesystem read-write from Android or recovery. Android may re-own `/` (uid 1023) and the ext4 `orphan_file` feature is not supported there.

## Way back
- Flash your backed-up stock `boot` + `dtbo` (Odin or `dd`). Android/LineageOS boots again if `userdata` was not reformatted.
- Complete return: stock firmware via Odin (BL, AP, CP, CSC). The stock AP contains `persist`: restore your own persist/EFS backup if anything is off afterwards.
