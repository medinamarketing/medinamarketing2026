---
workflow: product-launch-video
flow: automation
storyboard: no
message: "Aplikasi Pesakit Klinik Medina — semua urusan kesihatan anda, di tapak tangan."
destination: youtube / pembentangan
aspect: "16:9"
language: ms
audience: pesakit Klinik Medina (dan pihak pengurusan yang menilai cadangan)
length: 52s
angle: pengenalan produk (sell) — cadangan app pesakit yang akan datang
vo_mode: none
---

## Intent

Daripada PDF "Aplikasi Pesakit Klinik Medina" (13 skrin prototaip), buat video
motion/animation yang memperkenalkan app pesakit yang dicadangkan untuk Klinik
Medina. Profesional dan moden, ada bunyi, 16:9, bawah 1 minit. Pengguna minta
"guna kreativiti anda" — dijalankan secara autonomi (tiada soalan brief).

## Assets

- 13 skrin app (1170×2532) diekstrak terus daripada PDF → `assets/screens/`.
- Logo Klinik Medina (mark + penuh) daripada video 01 → `assets/img/`.
- Plus Jakarta Sans (SIL OFL) → `assets/fonts/`.

## Customizations

- Bunyi: muzik latar korporat moden 120 BPM + kesan bunyi UI (whoosh, tap,
  pop, chime) — disintesis secara deterministik (`audio-src/make_audio.py`).
- Tiada voiceover: perkhidmatan TTS Bahasa Melayu disekat oleh rangkaian
  persekitaran, dan enjin offline (Kokoro) tidak menyokong Bahasa Melayu.
  Mesej dibawa oleh teks kinetik. Slot voiceover diterangkan dalam README.

## Notes

- Skrin app ialah sumber kebenaran visual: digunakan sebagaimana ada dalam
  bingkai telefon; callout ialah potongan (crop) skrin sebenar, bukan UI rekaan.
