# Video 01 — Bila perlu bawa anak untuk nebuliser?

Klinik Medina · 9:16 (1080×1920) · 52 saat · Bahasa Melayu

## Skrip voiceover

Masa ialah sasaran untuk rakaman. Kapsyen dalam `compositions/captions.html`
mengikut masa ini; laraskan senarai `groups` di sana selepas voiceover siap.

| Masa        | Babak               | Voiceover                                                             |
| ----------- | ------------------- | --------------------------------------------------------------------- |
| 0.3 – 3.0   | 1 Hook              | Anak batuk, berdehit dan sukar bernafas?                              |
| 3.0 – 5.9   | 1 Hook              | Bila sebenarnya perlu bawa anak untuk nebuliser?                      |
| 6.2 – 9.6   | 2 Apa itu nebuliser | Nebuliser menukar ubat cecair kepada wap halus,                       |
| 9.6 – 12.9  | 2 Apa itu nebuliser | supaya mudah disedut terus ke saluran pernafasan.                     |
| 13.3 – 16.6 | 3 Lima tanda        | Bawa anak jumpa doktor jika dia bernafas laju atau tercungap-cungap,  |
| 16.6 – 20.0 | 3 Lima tanda        | berbunyi berdehit ketika bernafas,                                    |
| 20.0 – 23.6 | 3 Lima tanda        | dada atau perut tertarik ke dalam,                                    |
| 23.6 – 27.2 | 3 Lima tanda        | batuk berterusan hingga sukar tidur atau makan,                       |
| 27.2 – 30.9 | 3 Lima tanda        | atau inhaler di rumah tidak lagi membantu.                            |
| 31.2 – 34.0 | 4 Doktor            | Doktor akan memeriksa anak terlebih dahulu                            |
| 34.0 – 36.9 | 4 Doktor            | dan menentukan sama ada nebuliser diperlukan.                         |
| 37.2 – 40.8 | 5 Kecemasan         | Jika bibir kebiruan, anak terlalu lemah atau sukar menyusu,           |
| 40.8 – 43.9 | 5 Kecemasan         | terus dapatkan rawatan kecemasan.                                     |
| 44.2 – 47.6 | 6 CTA               | Klinik Medina sedia membantu keluarga anda.                           |
| 47.6 – 51.8 | 6 CTA               | Hubungi kami di 09-662 1491.                                          |

## Menambah voiceover

1. Simpan rakaman sebagai `assets/audio/voiceover.mp3`.
2. Dalam `index.html`, ganti komen "Voiceover slot" dengan:
   `<audio id="vo" src="assets/audio/voiceover.mp3" data-start="0" data-duration="52" data-track-index="3"></audio>`
3. Laraskan masa kapsyen, kemudian `npm run check` dan `npm run render`.

## Fail

- `index.html` — susunan babak (track 0 latar, 1 babak, 2 kapsyen)
- `compositions/` — satu fail bagi setiap babak + `captions.html`
- `assets/img/` — logo, lobi, bangunan, potret doktor (dipotong daripada reference sheet)
- `assets/fonts/` — Anton & Plus Jakarta Sans (SIL OFL)
- `vendor/gsap.min.js` — GSAP disimpan setempat supaya render tidak bergantung pada CDN
