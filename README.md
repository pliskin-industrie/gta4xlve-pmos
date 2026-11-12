<h1 align="center">THANK YOU, mikroffarad</h1>

<p align="center"><b>
Everything in this repository stands on the shoulders of
<a href="https://github.com/mikroffarad/linux/tree/gta4xlve-dev">mikroffarad</a>.<br>
Without the gta4xlve device tree, the ISL98608 display-bias driver, the HX83112B/HX83102E SPI touch support,
the BOE TV104WUM panel support, the audio and Bluetooth fixes and the whole kernel base mikroffarad published,
none of this would exist. Not one pixel of it.<br>
I only built on top of that work. The hard part was already done.
</b></p>

> **mikroffarad - from the bottom of my heart: thank you.**
> Every patch in `patches/` that comes from that series keeps its original author and `Signed-off-by` line.
> Please also see [CREDITS.md](CREDITS.md) for the other people whose work is in here.

---

# postmarketOS on the Samsung Galaxy Tab S6 Lite 2022 (SM-P613, gta4xlve)

Mainline Linux (7.3.3) and postmarketOS with KDE Plasma on the **Snapdragon 720G (SM7125)** variant of the
Galaxy Tab S6 Lite (2022). This repository contains the kernel patch series, kernel configs, the small
`dtbo` that makes Samsung's bootloader accept a mainline device tree, and the documentation of what I learned.

> **Only SM-P613 / SM-P619 (gta4xlve, Qualcomm).** The SM-P610 / SM-P615 (Exynos 9611) are different devices. Nothing here works on them.
>
> **Unlocking the bootloader wipes the tablet and permanently trips Knox** (Samsung Pay, Secure Folder, warranty).
>
> **Experimental. You can brick your device. You are responsible.** Back up EFS / persist / modem partitions first.

## Status

Tested in daily use on one device (kernel 7.3.3, root filesystem on internal userdata):

| Feature | 7.3.3 (mainline) | 6.18.62 LTS | 6.14.7 (mikroffarad base + 3 patches) |
|---|---|---|---|
| Boot through Samsung ABL (with my dtbo) | works | built, not tested on device | worked |
| Display (BOE TV104WUM / HX83102) + backlight | works | built, not tested | worked |
| Touch (HX83102E over SPI) | works | built, not tested | worked |
| GPU (Adreno 618, freedreno / Turnip) | works | built, not tested | worked |
| Wi-Fi (WCN3990, ath10k) | works | built, not tested | worked |
| Bluetooth (WCN3991) | works | built, not tested | worked |
| Speakers (TAS2562) | works, **needs a workaround after each boot** (see `docs/hacks.md`) | built, not tested | worked (workaround for a different race) |
| Battery values (SM5714 fuel gauge) | **fixed** (units patch), percent and time remaining correct | built, not tested | wrong units without my patch |
| Plasma desktop | works | not tested | worked |
| Steam via FEX in an Ubuntu container, native aarch64 games | works (performance limited, 3.4 GiB RAM) | not tested | worked |
| USB gadget networking (NCM / ssh) | LPM/QUSB2 patch included, not specifically re-tested | not tested | unstable on Windows hosts before the LPM/QUSB2 patch |
| Headphones / microphone | untested | | |
| USB host / OTG | not working (no driver for the SM5714 USB part) | | |
| Rotation sensor | not working (ADSP sensors not set up; manual rotate button instead) | | |
| Cameras, modem | not working | | |
| S Pen | untested | | |

"built, not tested" means exactly that: the 6.18 LTS series compiles and the images were built, but it was never booted on the device.
The modem remoteproc crashes at boot on 7.3.3. The Wi-Fi tablet has no modem, so this is harmless.

## What is in this repository

| Path | What |
|---|---|
| `patches/7.3.3/` | 25-patch series on top of the stable tag `v7.3.3` (tested) |
| `patches/6.18.62/` | the same series on top of `v6.18.62` (LTS, built, **untested**) |
| `patches/6.14.7-akku/` | 3 patches on top of mikroffarad's `gta4xlve-dev` (6.14.7) |
| `configs/` | kernel `.config` for each version |
| `dtbo/` + `tools/build-dtbo.sh` | the minimal overlay for the `dtbo` partition (see `docs/abl-dtbo.md`) |
| `tools/mkboot.py` | repacks a known-good `boot.img` with a new kernel and DTB |
| `docs/install.md` | installation and way back |
| `docs/abl-dtbo.md` | the Samsung ABL overlay trap (the most useful thing I found) |
| `docs/hacks.md` | workarounds: speaker amplifier after boot, UCM link, USB LPM, games notes |

**Not here (yet):** `pmaports` packages (`device-samsung-gta4xlve`, `linux-samsung-gta4xlve`). I have not written or tested
APKBUILDs, so I do not pretend to ship them. The device-specific setup is done by hand as described in the docs.
**Never included:** firmware blobs, stock Samsung images, root filesystem images, backups.

There is **no prebuilt boot image yet.** Build `boot.img` yourself with `tools/mkboot.py`: it takes a known-good `boot.img` from your own device as a template
and replaces only the kernel (`Image.gz`) and the DTB, keeping header, offsets, ramdisk and command line (usage: `python3 tools/mkboot.py Image.gz dtb out.img template-boot.img`, details in `docs/install.md`).
The releases only carry the dtbo image, the kernel modules and the kernel config.
The complete corresponding kernel source is "tag `vX.Y.Z` of the Linux stable tree plus the patch series in `patches/`" (GPL-2.0, section 3).

## How to apply the patches

```sh
git clone --branch v7.3.3 --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
cd linux
git am ../gta4xlve-pmos/patches/7.3.3/*.patch
cp ../gta4xlve-pmos/configs/config-7.3.3-gta4xlve .config
make ARCH=arm64 olddefconfig
make ARCH=arm64 -j"$(nproc)" Image.gz dtbs modules DTC_FLAGS=-@   # DTC_FLAGS=-@ is essential, see docs/abl-dtbo.md
```

Cross-compile with `CROSS_COMPILE=aarch64-linux-gnu-` on an x86 host. Details for building the boot image: `docs/install.md`.

## Way back

Flash your own backed-up stock `boot` and `dtbo` partitions (Odin or `dd` from recovery) and Android boots again,
provided `userdata` was not reformatted. Full return: stock firmware via Odin. See `docs/install.md`.

## Licenses

Kernel patches: GPL-2.0-only (see `LICENSE`), device tree files keep the SPDX headers of their origin.
Documentation: CC-BY-SA-4.0 (see `LICENSE-DOCS`).

## Credits

See [CREDITS.md](CREDITS.md). If I forgot you, please open an issue and I will fix it right away.

---

## Kurz auf Deutsch

postmarketOS mit Plasma läuft auf dem Galaxy Tab S6 Lite 2022 (**nur SM-P613 / SM-P619**, Snapdragon 720G) mit Mainline-Kernel 7.3.3:
Display, Touch, GPU, WLAN, Bluetooth, Lautsprecher (nach jedem Start ist ein kleiner Workaround nötig), korrekte Akkuanzeige, Plasma,
Steam über FEX und einige native Spiele. 6.18 LTS ist gebaut, aber auf dem Gerät nicht getestet. Ohne die Arbeit von **mikroffarad** gäbe es
nichts davon, herzlichen Dank! Ein fertiges Boot-Image gibt es noch nicht: Ich baue es mit `tools/mkboot.py` aus einem eigenen, funktionierenden `boot.img` als Vorlage selbst, du kannst das ebenso tun. Wichtigste Falle: Samsungs Bootloader legt immer die `dtbo`-Partition über die DTB; die DTB braucht
`__symbols__` (`DTC_FLAGS=-@`) und das dtbo `__fixups__`, sonst landet das Tablet im Download-Modus. Entsperren löscht das Tablet und löst Knox
dauerhaft aus. Experimentell, auf eigene Gefahr.
