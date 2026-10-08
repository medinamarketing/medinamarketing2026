"""Deterministic music bed + UI sound effects for the Klinik Medina app video.

Run from the project root:  python3 -I audio-src/make_audio.py
Writes assets/audio/music.mp3 and assets/audio/sfx-*.mp3 (via ffmpeg).

Music: 120 BPM (1 bar = 2 s), D major, 52 s, laid out on the storyboard's
scene grid: sparse hook (0-6 s), drop + groove (6-46 s), lift (42-46 s),
closing hit and tail (46-52 s).
"""

import os
import subprocess
import sys

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
BPM = 120
BEAT = 60 / BPM
BAR = BEAT * 4
LENGTH = 52.0
N = int(LENGTH * SR)
rng = np.random.default_rng(20261008)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "audio")


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc, "low", fs=SR, output="sos"), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def place(buf, start, sig, gain=1.0, pan=0.0):
    """Mix a mono or stereo signal into a stereo buffer at `start` seconds."""
    i = int(round(start * SR))
    if i >= buf.shape[0]:
        return
    if sig.ndim == 1:
        left = np.cos((pan + 1) * np.pi / 4)
        right = np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * left * 1.414, sig * right * 1.414], axis=1)
    j = min(buf.shape[0], i + sig.shape[0])
    buf[i:j] += sig[: j - i] * gain


def saw(f, t, phase=0.0):
    return 2.0 * ((f * t + phase) % 1.0) - 1.0


def env_adsr(n, a, d, s, r, total):
    """Attack/decay/sustain over `total` seconds, then release `r`."""
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-4), 1.0)
    e = np.where((t >= a) & (t < a + d), 1 - (1 - s) * (t - a) / max(d, 1e-4), e)
    e = np.where((t >= a + d) & (t < total), s, e)
    e = np.where(t >= total, s * np.exp(-(t - total) / max(r, 1e-4) * 4), e)
    return e


# ---------------------------------------------------------------- instruments


def pad_chord(notes, dur, bright=1800.0):
    t = t_axis(dur + 1.0)
    out = np.zeros((t.size, 2))
    for k, m in enumerate(notes):
        f = mtof(m)
        for c, cents in enumerate((-11, -4, 4, 11)):
            ph = rng.random()
            v = saw(f * 2 ** (cents / 1200), t, ph)
            ch = c % 2
            out[:, ch] += v
    env = env_adsr(t.size, 0.35, 0.4, 0.8, 0.9, dur)
    out[:, 0] = lp(out[:, 0], bright, 2) * env
    out[:, 1] = lp(out[:, 1], bright, 2) * env
    return out * (0.06 / max(1, len(notes) ** 0.5))


def pluck(m, dur=0.45, bright=1.0):
    t = t_axis(dur)
    f = mtof(m)
    sig = (
        np.sin(2 * np.pi * f * t)
        + 0.45 * bright * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 14)
        + 0.22 * bright * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 22)
        + 0.10 * bright * np.sin(2 * np.pi * 4.01 * f * t) * np.exp(-t * 30)
    )
    env = np.exp(-t * 9) * np.minimum(1, t / 0.003)
    return sig * env


def bass_note(m, dur):
    t = t_axis(dur)
    f = mtof(m)
    sig = np.sin(2 * np.pi * f * t) + 0.35 * lp(saw(f, t), 600, 2)
    env = np.minimum(1, t / 0.006) * np.minimum(1, (dur - t) / 0.03)
    env *= 0.75 + 0.25 * np.exp(-t * 6)
    return sig * env


def kick(gain=1.0):
    t = t_axis(0.45)
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 7.5)
    click = hp(rng.standard_normal(t.size), 2500) * np.exp(-t * 300) * 0.25
    return (body + click) * gain


def clap():
    t = t_axis(0.35)
    n = rng.standard_normal(t.size)
    env = np.zeros_like(t)
    for off in (0.0, 0.011, 0.022):
        env += np.where(t >= off, np.exp(-(t - off) * 140), 0)
    env += np.exp(-t * 18) * 0.35
    return bp(n, 900, 4200) * env * 0.55


def hat(open_=False):
    dur = 0.22 if open_ else 0.06
    t = t_axis(dur)
    n = hp(rng.standard_normal(t.size), 7000, 3)
    return n * np.exp(-t * (14 if open_ else 70)) * 0.22


def shaker():
    t = t_axis(0.09)
    n = bp(rng.standard_normal(t.size), 5000, 11000)
    return n * np.sin(np.pi * np.minimum(1, t / 0.09)) * 0.08


def riser(dur):
    t = t_axis(dur)
    n = rng.standard_normal(t.size)
    out = np.zeros_like(t)
    seg = int(0.05 * SR)
    for i in range(0, t.size, seg):
        p = i / t.size
        lo = 300 + 5200 * p**2
        out[i : i + seg] = bp(n[i : i + seg + 0], lo, min(lo * 2.2, 18000))
    sweep_f = 220 * 2 ** (3 * t / dur)
    tone = np.sin(2 * np.pi * np.cumsum(sweep_f) / SR) * 0.15
    env = (t / dur) ** 2.2
    return (out * 0.5 + tone) * env


def impact():
    t = t_axis(2.5)
    f = 30 + 70 * np.exp(-t * 6)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.8)
    noise = lp(rng.standard_normal(t.size), 1800) * np.exp(-t * 5) * 0.5
    crash = hp(rng.standard_normal(t.size), 5000) * np.exp(-t * 2.2) * 0.12
    return boom + noise + crash


def reverb(x, seconds=2.4, mix=0.25):
    t = t_axis(seconds)
    ir_l = rng.standard_normal(t.size) * np.exp(-t * 3.2)
    ir_r = rng.standard_normal(t.size) * np.exp(-t * 3.2)
    ir_l = lp(ir_l, 6000)
    ir_r = lp(ir_r, 6000)
    ir_l /= np.sqrt(np.sum(ir_l**2))
    ir_r /= np.sqrt(np.sum(ir_r**2))
    wet_l = fftconvolve(x[:, 0], ir_l)[: x.shape[0]]
    wet_r = fftconvolve(x[:, 1], ir_r)[: x.shape[0]]
    return np.stack([wet_l, wet_r], axis=1) * mix


def delay(x, time=BEAT * 0.75, fb=0.38, mix=0.32):
    out = np.zeros_like(x)
    d = int(time * SR)
    tap = x.copy()
    for k in range(1, 6):
        tap = np.roll(tap, d, axis=0)
        tap[:d] = 0
        ch = k % 2
        out[:, ch] += tap[:, ch] * (fb ** (k - 1))
        tap = tap * 1.0
    return out * mix


# ---------------------------------------------------------------- arrangement

CHORDS = {
    "D": ([62, 66, 69, 74], 38),
    "A": ([61, 64, 69, 73], 33),
    "Bm": ([62, 66, 71, 74], 35),
    "G": ([62, 67, 71, 74], 31),
    "Dmaj9": ([62, 66, 69, 73, 76], 38),
}

# One chord per bar (26 bars = 52 s).
PROG = ["Bm", "G", "A"] + ["D", "A", "Bm", "G"] * 4 + ["D", "A"] + ["Bm", "G"] + ["D", "G", "Dmaj9"]
assert len(PROG) == 26

pad = np.zeros((N, 2))
plk = np.zeros((N, 2))
bass = np.zeros((N, 2))
drums = np.zeros((N, 2))
fx = np.zeros((N, 2))

ARP = [0, 2, 1, 3, 2, 1, 3, 2]  # 8th-note pattern over chord tones

for bar, name in enumerate(PROG):
    t0 = bar * BAR
    notes, root = CHORDS[name]
    hook = bar < 3
    outro_tail = bar == 25
    groove = 3 <= bar <= 23

    # Pad
    bright = 1100 if hook else (1600 if groove else 1300)
    dur = BAR * (3 if outro_tail else 1)
    place(pad, t0, pad_chord(notes, dur, bright), gain=1.0 if not hook else 1.8)

    # Plucked arpeggio, one octave up
    tones = [n + 12 for n in notes[:4]]
    step = BEAT / 2
    if not outro_tail:
        for i in range(8):
            if hook and bar == 0 and i % 2:
                continue
            vel = 0.9 if i % 2 == 0 else 0.6
            place(plk, t0 + i * step, pluck(tones[ARP[i]], bright=1.0), gain=(0.2 if hook else 0.11) * vel, pan=-0.3 if i % 2 else 0.3)
    else:
        for i, n in enumerate(sorted(tones + [notes[-1] + 12])):
            place(plk, t0 + i * 0.06, pluck(n, dur=2.5), gain=0.09, pan=-0.4 + i * 0.2)

    # Counter melody (bars 9-20): sparse high plucks for a lift
    if 9 <= bar <= 20 or bar in (21, 22):
        mel = [notes[-1] + 12, notes[-2] + 12, notes[-1] + 12, notes[1] + 24]
        for i, m in enumerate(mel):
            place(plk, t0 + i * BEAT + BEAT * 0.5 * (i == 3), pluck(m, bright=0.6), gain=0.05, pan=0.15)

    # Bass: 8ths on the root, pumping
    if groove or bar == 24:
        for i in range(8):
            if bar == 22 and i >= 7:
                continue
            m = root + (12 if i in (3, 7) else 0)
            place(bass, t0 + i * step, bass_note(m, step * 0.9), gain=0.16)
    elif bar == 2:
        place(bass, t0 + BAR * 0.5, bass_note(root, BAR * 0.5), gain=0.10)

    # Drums
    if groove:
        for b in range(4):
            last_beat_cut = bar == 22 and b == 3
            if not last_beat_cut:
                place(drums, t0 + b * BEAT, kick(), gain=0.55)
            if b in (1, 3) and not last_beat_cut:
                place(drums, t0 + b * BEAT, clap(), gain=0.6)
            place(drums, t0 + b * BEAT + BEAT / 2, hat(open_=(b == 3 and bar % 2 == 1)), gain=0.9, pan=0.2)
            for s in (0.25, 0.75):
                place(drums, t0 + b * BEAT + BEAT * s, shaker(), gain=1.0, pan=-0.25)
    elif bar == 1 or bar == 2:
        for b in range(4):
            place(drums, t0 + b * BEAT + BEAT / 2, hat(), gain=0.55, pan=0.2)
    elif bar == 24:
        for b in (0, 2):
            place(drums, t0 + b * BEAT, kick(), gain=0.4)

# Sidechain pump driven by the groove kicks
pump = np.ones(N)
for bar, _ in enumerate(PROG):
    if 3 <= bar <= 23 or bar == 24:
        for b in range(4):
            if bar == 24 and b in (1, 3):
                continue
            i = int((bar * BAR + b * BEAT) * SR)
            L = int(0.32 * SR)
            seg = 1 - 0.55 * np.exp(-np.arange(L) / SR * 11)
            j = min(N, i + L)
            pump[i:j] = np.minimum(pump[i:j], seg[: j - i])
pad *= pump[:, None]
bass *= (0.35 + 0.65 * pump)[:, None]

# Risers and impacts on the scene grid
place(fx, 6.0 - 2.0, riser(2.0), gain=0.35)  # into the reveal
place(fx, 46.0 - 2.5, riser(2.5), gain=0.38)  # into the close
place(fx, 6.0, impact(), gain=0.55)
place(fx, 46.0, impact(), gain=0.5)
place(fx, 50.0, impact(), gain=0.22)

mix = pad * 1.0 + plk * 1.0 + bass * 1.0 + drums * 0.9 + fx * 1.0
mix += reverb(pad * 0.6 + plk * 0.9 + drums * 0.15, mix=0.35)
mix += delay(plk, mix=0.28)

# Gentle master: fade-in on the first notes, fade-out tail, soft clip, normalize
tt = np.arange(N) / SR
mix *= np.minimum(1, tt / 0.25)[:, None]
mix *= np.clip((LENGTH - tt) / 1.6, 0, 1)[:, None] ** 1.5
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
mix /= np.max(np.abs(mix)) / 0.89


# ---------------------------------------------------------------- UI SFX


def whoosh(dur=0.7, up=True):
    t = t_axis(dur)
    n = rng.standard_normal(t.size)
    out = np.zeros_like(t)
    seg = int(0.02 * SR)
    for i in range(0, t.size, seg):
        p = i / t.size
        f = 400 + 3800 * (np.sin(np.pi * p) if up else (1 - p))
        out[i : i + seg] = bp(n[i : i + seg], f * 0.6, min(f * 1.6, 19000), 1)
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.6
    st = np.stack([out * env * (1 - 0.4 * t / dur), out * env * (0.6 + 0.4 * t / dur)], axis=1)
    return st * 0.9


def tap():
    t = t_axis(0.12)
    s = np.sin(2 * np.pi * 1600 * t) * np.exp(-t * 60)
    c = hp(rng.standard_normal(t.size), 3000) * np.exp(-t * 400) * 0.4
    return (s + c) * 0.7


def pop():
    t = t_axis(0.16)
    f = 520 + 900 * (1 - np.exp(-t * 40))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 32) * np.minimum(1, t / 0.002)
    return s * 0.7


def bloop():
    a = t_axis(0.09)
    s1 = np.sin(2 * np.pi * 988 * a) * np.sin(np.pi * a / 0.09)
    b = t_axis(0.22)
    s2 = np.sin(2 * np.pi * 1480 * b) * np.exp(-b * 18) * np.minimum(1, b / 0.004)
    out = np.zeros(int(0.32 * SR))
    out[: s1.size] += s1 * 0.5
    i = int(0.075 * SR)
    out[i : i + s2.size] += s2 * 0.6
    return out


def bell(f, dur=1.4):
    t = t_axis(dur)
    s = (
        np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2)
        + 0.5 * np.sin(2 * np.pi * 2.0 * f * t) * np.exp(-t * 5)
        + 0.25 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 8)
        + 0.12 * np.sin(2 * np.pi * 4.2 * f * t) * np.exp(-t * 12)
    )
    return s * np.minimum(1, t / 0.003)


def chime():
    out = np.zeros(int(1.8 * SR))
    b1 = bell(mtof(88))  # E6
    b2 = bell(mtof(93))  # A6
    out[: b1.size] += b1 * 0.45
    i = int(0.13 * SR)
    out[i : i + b2.size] += b2[: out.size - i] * 0.45
    return out


def ding():
    out = np.zeros(int(1.6 * SR))
    for k, (m, d) in enumerate(((86, 0.0), (90, 0.05), (93, 0.1))):  # D6 F#6 A6
        b = bell(mtof(m), 1.4)
        i = int(d * SR)
        out[i : i + b.size] += b[: out.size - i] * 0.3
    return out


def tick():
    t = t_axis(0.05)
    return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 120) * 0.45


def to_stereo(x):
    return x if x.ndim == 2 else np.stack([x, x], axis=1)


def write(name, data):
    data = to_stereo(np.asarray(data, dtype=np.float64))
    peak = np.max(np.abs(data))
    if peak > 0.98:
        data = data / peak * 0.98
    wav = os.path.join(OUT, name + ".wav")
    mp3 = os.path.join(OUT, name + ".mp3")
    sf.write(wav, data.astype(np.float32), SR, subtype="PCM_16")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-codec:a", "libmp3lame", "-b:a", "192k", mp3],
        check=True,
    )
    os.remove(wav)
    print(f"{name}.mp3  {data.shape[0] / SR:.2f}s")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    write("music", mix)
    write("sfx-whoosh", whoosh())
    write("sfx-tap", tap())
    write("sfx-pop", pop())
    write("sfx-bloop", bloop())
    write("sfx-chime", chime())
    write("sfx-ding", ding())
    write("sfx-tick", tick())
    sys.exit(0)
