---
format: 1920x1080
duration: 52
fps: 30
bpm: 120
music: host (assets/audio/music.wav — sintesis tempatan, lihat audio-src/)
captions: none
---

# Storyboard — Aplikasi Pesakit Klinik Medina

Grid muzik 120 BPM: 1 bar = 2 s. Setiap babak bermula tepat pada bar.
Latar `compositions/bg.html` (navy jenama + cahaya teal + grid titik) berterusan
sepanjang video; babak masuk/keluar di atasnya supaya tiada "lompatan" latar.

| # | Masa | Babak | Visual | Bunyi |
| - | ---- | ----- | ------ | ----- |
| 1 | 0–6 | Hook | Tiga baris kinetik: "Beratur lama di klinik?" · "Rekod kesihatan berselerak?" · "Terlupa tarikh temujanji?" → "Ada cara yang lebih mudah." | pad lembut, pop setiap baris, riser ke 6 s |
| 2 | 6–12 | Pengenalan | Logo lotus mekar + "Aplikasi Pesakit Klinik Medina"; tajuk ke kiri, telefon (log masuk) naik di kanan; callout medan No. IC + tap Log Masuk | impact + groove penuh, whoosh, tap |
| 3 | 12–18 | Satu aplikasi | Telefon laman utama di tengah; 6 jubin ciri terbang keluar ke kiri/kanan | whoosh, 6 pop |
| 4 | 18–24 | Pra-daftar | "Daftar dari rumah. Datang bila hampir giliran." Tap "Daftar & ambil giliran" → notifikasi giliran turun, kiraan 5→3 | tap, chime notifikasi, tick |
| 5 | 24–30 | Penyakit kronik | Dua telefon (Rekod Kesihatan + Penyakit Kronik); kad graf HbA1c terangkat keluar, kiraan 9.2→7.1 %, cip "Menurun baik" | whoosh, pop, ding |
| 6 | 30–36 | Turun berat + ganjaran | Gelang 0→44 %, −6.1 kg; kad Mata Ganjaran 460 | whoosh, ding |
| 7 | 36–42 | Chat doktor | Telefon chat; tiga gelembung mesej muncul satu-satu di sisi | whoosh, 3 bloop mesej |
| 8 | 42–46 | Dan banyak lagi | Karusel 6 telefon: Temujanji, Tanggungan, Saringan, Minda Sihat, Ganjaran, Profil | whoosh, riser |
| 9 | 46–52 | Penutup | Logo penuh, "Aplikasi Pesakit", lencana "Akan datang", "Percuma untuk semua pesakit", Klinik Medina Kuala Nerus · 09-662 1491 | impact, ding, muzik reda |

## Video direction

- Palet: navy #12455A / #0C3646 (latar), teal #3CB394, mint #8BD1B9, hijau butang app #1F7A5E, putih.
- Taip: Plus Jakarta Sans 800 (tajuk), 700 (callout), 500 (badan).
- Telefon: bingkai peranti CSS dengan skrin sebenar (1170×2532). Callout = crop skrin sebenar, dibesarkan, bayang lembut.
- Gerak: masuk power3/expo.out pantas (0.5–0.8 s), keluar 0.35 s blur+skala; elemen terapung bergoyang perlahan (sine).
