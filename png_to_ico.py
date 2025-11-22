from PIL import Image


def main():
    """Convertit icon.png en icon.ico avec plusieurs tailles pour Windows."""
    src = "icon.png"
    dst = "icon.ico"

    img = Image.open(src).convert("RGBA")
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(dst, sizes=sizes)
    print(f"Icône ICO générée: {dst} avec tailles {sizes}")


if __name__ == "__main__":
    main()
