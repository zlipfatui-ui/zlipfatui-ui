"""Build the animated GitHub profile banner.

Run from the repository root with: python scripts/make_banner.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "profile-banner.gif"
FONT_DIR = Path("C:/Windows/Fonts")

WIDTH, HEIGHT = 1200, 340
BACKGROUND = "#111316"
WHITE = "#f3f3ea"
MUTED = "#aeb3aa"
LIME = "#d3f56b"
CORAL = "#ff9b7b"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_DIR / name, size)


def z_cells() -> list[tuple[int, int]]:
    top = [(0, column) for column in range(8)]
    diagonal = [(row, 7 - row) for row in range(1, 7)]
    bottom = [(7, column) for column in range(8)]
    return top + diagonal + bottom


def make_frame(step: int, cells: list[tuple[int, int]]) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((0, 0, WIDTH - 1, HEIGHT - 1), radius=20, outline="#30353a", width=2)
    draw.rounded_rectangle((64, 54, 73, 286), radius=4, fill=CORAL)

    draw.text((96, 48), "Z / ZLIPFATUI-UI", font=font("consola.ttf", 22), fill=LIME)
    draw.text((93, 91), "I make apps,", font=font("segoeuib.ttf", 73), fill=WHITE)
    draw.text((93, 178), "games & tools.", font=font("segoeuib.ttf", 73), fill=WHITE)
    draw.text((97, 282), "Founder at BeforeBedtime", font=font("segoeui.ttf", 24), fill=MUTED)

    draw.line((807, 58, 807, 282), fill="#393d41", width=2)
    cell_size, gap = 23, 7
    origin_x, origin_y = 865, 54
    cell_order = {cell: index for index, cell in enumerate(cells)}
    for row in range(8):
        for column in range(8):
            x = origin_x + column * (cell_size + gap)
            y = origin_y + row * (cell_size + gap)
            cell = (row, column)
            if cell not in cell_order:
                color = "#252a2d"
            else:
                distance = (step - cell_order[cell]) % len(cells)
                if distance == 0:
                    color = LIME
                elif distance == 1:
                    color = "#acd05f"
                elif distance == 2:
                    color = "#88a954"
                else:
                    color = "#586b47"
            draw.rounded_rectangle((x, y, x + cell_size, y + cell_size), radius=3, fill=color)

    return image


def main() -> None:
    cells = z_cells()
    frames = [make_frame(step, cells) for step in range(len(cells))]
    frames[0].save(
        OUTPUT,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=115,
        loop=0,
        disposal=2,
        optimize=True,
    )
    frames[0].save(ROOT.parent / "profile-banner-preview.png")
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size:,} bytes, {len(frames)} frames)")


if __name__ == "__main__":
    main()
