# Workarounds and notes

## Speakers after boot (TAS2562), kernel 7.3.3
On 7.3.3 the ADSP/AFE reports `Unknown cmd 0x100f6` early during boot, the TAS2562 speaker amplifiers come up in an error state,
PulseAudio finds no profile and there is no sound. I run a small systemd service (`ton-fix.service`, runs a script after boot) that unbinds and
re-binds both amplifiers (I2C bus 0, addresses `0x4c` and `0x4d`) and restarts PulseAudio if no real speaker sink appeared.
After that the speaker sink is there and sound works.
**The script itself is not included in this repository yet** (it has to be copied from the device and cleaned first). A real fix would be in the ADSP / audio topology path of the kernel; I did not do that.

On 6.14.7 a different symptom existed: `lpass-lpi-pinctrl` sometimes timed out on its clock (race with the ADSP) and the sound card was missing; re-binding it 15 s after boot helped.

## UCM link
alsa-ucm-conf has no profile for this model. Add a link in the `ucm2` tree:
`conf.d/sm8250/Galaxy Tab S6 Lite.conf` -> `Samsung/gta4xlve` (the target profile `Samsung/gta4xlve` was already present in my installation; I only had to add the link).
The link can be lost on package updates.

## USB gadget / LPM
USB networking was unstable (Windows reported Code 10). Patch `0023` disables gadget USB2 LPM (`snps,usb2-gadget-lpm-disable`, `snps,has-lpm-erratum`)
and applies the vendor QUSB2 PHY tuning values read from the stock device tree. USB host mode is not available (`dr_mode` peripheral, no driver for the SM5714 USB part).

## Battery
Patch `0025` fixes the SM5714 fuel gauge: SRAM values were masked to 11 bits and read as 8.8 fixed point (voltage ~0.5 V, current without sign).
Scaling now follows Samsung's vendor driver; values are reported in uV/uA as the power_supply ABI requires, plus `charge_full(_design)` etc. from a `monitored-battery` DT node (design capacity 7040 mAh).

## Manual screen rotation
There is no rotation sensor support yet (sensors run on the ADSP; the libssc userspace is not set up). I use a small script around `kscreen-doctor` on output `DSI-1`.

## Firewall note (Steam in-home streaming)
With a default-drop `nftables` policy, Steam's LAN streaming ports (UDP 27031-27036, TCP 27036 and 27040) must be allowed from your local subnet.

## Games (experience, nothing here is packaged)
- Steam runs through FEX in an Ubuntu container (about 6 GB), with GL 4.6 via Turnip. The FEX root filesystem needs `/etc/resolv.conf` and `/etc/hosts` or Steam's game container (bwrap) fails.
- The device has 3.4 GiB RAM and a Snapdragon 720G: large 3D titles are slow or unusable; 2D and older games are fun.
- Native aarch64 builds worked well (OpenRA, OpenXcom, CorsixTH, KeeperFX, Starsector with a self-built LWJGL, Zod Engine with a larger thread stack because musl's default is too small). Game data is yours to supply.

## Bluetooth device address (edit before use)
Patch `0022` sets `local-bd-address` in the Bluetooth node because the firmware default address leaves the controller unconfigured (it comes up at the HCI level, never shows in the management index list, and bluetoothd reports "No default controller").
In the original series this was the address of one specific tablet. **In this repository the value is replaced by a placeholder (`00 00 00 00 00 00`).** Before building, put your own address there:
read it from your device's `/efs/bluetooth/bt_addr` (from your EFS backup) and store it little-endian (write the six bytes in reverse order).
