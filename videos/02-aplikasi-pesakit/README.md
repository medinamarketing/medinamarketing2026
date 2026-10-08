# Video 02 — Aplikasi Pesakit Klinik Medina

Klinik Medina · 16:9 (1920×1080) · 52 saat · Bahasa Melayu · muzik + kesan bunyi

Video pengenalan untuk cadangan aplikasi pesakit Klinik Medina, dibina daripada
13 skrin prototaip dalam PDF "Aplikasi Pesakit Klinik Medina".

## Babak

| Masa  | Fail                               | Kandungan                                                       |
| ----- | ---------------------------------- | --------------------------------------------------------------- |
| 0–6   | `compositions/s1-hook.html`        | Masalah: beratur lama, rekod berselerak, terlupa temujanji      |
| 6–12  | `compositions/s2-reveal.html`      | Logo + "Aplikasi Pesakit"; log masuk dengan No. IC              |
| 12–18 | `compositions/s3-utama.html`       | Laman utama; 6 jubin ciri terbang keluar                        |
| 18–24 | `compositions/s4-pradaftar.html`   | Pra-daftar, kiraan giliran 5→3, notifikasi                      |
| 24–30 | `compositions/s5-kronik.html`      | Penyakit kronik: graf HbA1c, 9.2 → 7.1 %                        |
| 30–36 | `compositions/s6-berat.html`       | Turun berat 44 % / −6.1 kg, Mata Ganjaran 460                   |
| 36–42 | `compositions/s7-chat.html`        | Chat dengan doktor                                              |
| 42–46 | `compositions/s8-lagi.html`        | Karusel: temujanji, rekod, tanggungan, saringan, minda, profil  |
| 46–52 | `compositions/s9-cta.html`         | Penutup: logo, "Akan datang", percuma untuk semua pesakit       |

`compositions/bg.html` ialah latar navy jenama di bawah semua babak.

## Bunyi

- `assets/audio/music.mp3` — muzik korporat 120 BPM (D major). Setiap babak
  bermula tepat pada bar (2 s); "drop" pada 6 s (logo) dan klimaks pada 46 s
  (penutup).
- `assets/audio/sfx-*.mp3` — whoosh, tap, pop, tick, chime, ding, bloop.
  Diletakkan dalam `index.html` (trek 3 whoosh, 4 klik/pop, 5 loceng).
- Semua bunyi disintesis secara deterministik oleh `audio-src/make_audio.py`
  (`python3 -I audio-src/make_audio.py` untuk jana semula; perlu numpy, scipy,
  soundfile dan ffmpeg).

### Menambah voiceover (pilihan)

Tiada voiceover kerana TTS Bahasa Melayu tidak dapat dicapai dari persekitaran
build. Untuk menambahnya:

1. Simpan rakaman sebagai `assets/audio/voiceover.mp3`.
2. Dalam `index.html`, tambah
   `<audio id="vo" src="assets/audio/voiceover.mp3" data-start="0" data-duration="52" data-track-index="6" data-volume="1"></audio>`
   dan turunkan `data-volume` muzik kepada ~0.35.
3. `npm run check`, kemudian `npm run render`.

## Aset

- `assets/screens/` — 13 skrin app (1170×2532) diekstrak terus daripada PDF.
- `assets/crops/` — potongan skrin sebenar untuk callout (jubin, butang, graf, gelembung chat).
- `assets/img/` — logo Klinik Medina. `assets/fonts/` — Plus Jakarta Sans (SIL OFL).
- `vendor/gsap.min.js` — GSAP disimpan setempat supaya render tidak bergantung pada CDN.

## Arahan

```bash
npm run check    # lint + runtime + layout + motion + contrast
npm run render   # → renders/<nama>.mp4
```
