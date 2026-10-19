"""Draws coast.png from figure.json: every row is about 121 games adjacent in move order, every column one ply.
Blue where the row's games still share their moves with some other game, amber where they are alone; transparent where they have ended."""
import json, struct, zlib

f = json.load(open("figure.json"))
PX = 10  # pixels per ply
A, C = (59, 95, 134), (224, 160, 48)
W, H = f["plies"] * PX, len(f["rows"])
px = [[(0, 0, 0, 0)] * W for _ in range(H)]
for y, row in enumerate(f["rows"]):
    games = sum(row["c"][0])  # at ply 1 every game is present
    for p, (s, o) in enumerate(row["c"]):
        alive = s + o
        if not alive:
            continue
        t = s / alive
        rgb = tuple(round(t * a + (1 - t) * c) for a, c in zip(A, C))
        alpha = round(255 * (0.25 + 0.75 * alive / games))
        for x in range(p * PX, (p + 1) * PX):
            px[y][x] = rgb + (alpha,)
# a plain RGBA PNG, written without an imaging library
raw = b"".join(b"\x00" + bytes(v for p in line for v in p) for line in px)
chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
open("coast.png", "wb").write(png)
print(W, H, len(png))
