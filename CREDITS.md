# Credits

## mikroffarad - thank you!

**[mikroffarad](https://github.com/mikroffarad/linux/tree/gta4xlve-dev)** published the Samsung Galaxy Tab S6 Lite 2022 (gta4xlve) mainline port
(branch `gta4xlve-dev`): the device tree, the ISL98608 regulator driver, HX83112B / HX83102E SPI touch,
BOE TV104WUM panel support, the ASoC sm8250 MI2S fixes and the WCN3991 Bluetooth fixes. This project is only possible because of that work.
In the patch series the commit metadata of the gta4xlve commits lists *Viktor Zaritskyi* as author; authorship and `Signed-off-by` lines are preserved untouched.

## Authors preserved in `patches/`

Every patch keeps its original `From:` and `Signed-off-by:` lines (cherry-picked from `mikroffarad/linux`, which in turn collects the sm7125-mainline work):

- **Vitalii Skorkin / N1kroks** - Adreno 618 speedbin 0x9f, ZAP firmware name, hwcg, sc7180 CDSP / GPI-DMA / ADSP non-secure / sound nodes, pd-mapper SM7125 and CDSP, tzmem SM7125.
- **map220v** - Samsung SM7125 (a52q / a72q) device trees, SM5714 fuel gauge / charger driver.
- **Joel Selvaraj** - qcom-wled unbalanced `enable_irq` fix.
- **Viktor Zaritskyi** (as listed in mikroffarad's gta4xlve series) - gta4xlve device tree, ISL98608, HX83112B SPI + HX83102E, HX83102 BOE TV104WUM panel, ASoC sm8250 MI2S, hci_qca fix.

## Others

- **sm7125-mainline contributors** (`github.com/sm7125-mainline/linux`) - SM7125 SoC groundwork.
- **Linux SC7180 / SM7125 upstream maintainers** (Qualcomm, Linaro and community) - `sc7180.dtsi`, `sm7125.dtsi`, drm/msm, ath10k, ASoC.
- **postmarketOS** - pmbootstrap, pmaports and the `linux-postmarketos-qcom-sm7125` config used as the starting point for my kernel config.
- **Mesa / freedreno / Turnip** - GPU userspace.
- **LineageOS** and the unofficial gta4xlve(u) maintainers - the recovery used for backups and flashing.
- **libufdt (AOSP)** - reading its source explained the ABL overlay errors.
- **Samsung** - the open-source vendor kernel (`sm5714_fuelgauge.c`) whose scaling formulas I used for the battery fix (GPL-2.0).

## This repository

Packaging, ABL / dtbo findings, the battery-units patch, USB LPM / QUSB2 tuning and documentation: Pliskin Industrie, 2026.
If I forgot you, please open an issue.
