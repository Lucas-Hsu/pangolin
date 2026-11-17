"""Extract UI assets from the supplied artwork without redrawing it.

Development tool only: python -m pip install Pillow; python tools/extract_art.py
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / 'src/pangolin/assets'
BG = (232, 208, 238)
PINK = (252, 102, 255)
CORAL = (252, 102, 102)


def crop(image, box, name):
    result = image.crop(box).convert('RGBA')
    result.putdata([(0, 0, 0, 0) if pixel[:3] == BG else pixel
                    for pixel in result.get_flattened_data()])
    result.save(ROOT / name, icc_profile=image.info.get('icc_profile'))


def silhouette(image, box, color, name):
    source = image.crop(box).convert('RGB')
    mask = Image.new('L', source.size)
    mask.putdata([255 if pixel == color else 0 for pixel in source.get_flattened_data()])
    # The handwritten placeholder letters are holes inside the shape.
    ImageDraw.floodfill(mask, (0, 0), 128)
    mask = mask.point(lambda value: 0 if value == 128 else 255)
    result = Image.new('RGBA', source.size, color + (255,))
    result.putalpha(mask)
    result.save(ROOT / name, icc_profile=image.info.get('icc_profile'))


def main():
    first = Image.open(ROOT / 'originals/page1.png').convert('RGB')
    form = Image.open(ROOT / 'originals/page2-v2.png').convert('RGB')
    last = Image.open(ROOT / 'originals/page3-v2.png').convert('RGB')
    crop(first, (263, 704, 959, 892), 'setup_button.png')
    ImageDraw.Draw(first).rectangle((260, 700, 962, 895), fill=BG)
    first.save(ROOT / 'welcome.png')
    crop(form, (40, 64, 1254, 255), 'questions_header.png')
    for index, box in enumerate(((77, 299, 846, 498), (57, 517, 838, 723), (21, 738, 813, 961))):
        silhouette(form, box, (252, 111, 207), f'question_{index}.png')
    for index, box in enumerate(((833, 394, 1251, 484), (816, 629, 1236, 719), (799, 867, 1219, 957))):
        crop(form, box, f'answer_{index}.png')
    crop(form, (1256, 299, 1280, 651), 'scroll_thumb.png')
    # Bubble: isolate its connected silhouette, retaining the exact new text.
    box = (170, 9, 1058, 440)
    bubble = last.crop(box).convert('RGBA')
    color = last.getpixel((600, 300))
    mask = Image.new('L', bubble.size)
    mask.putdata([255 if pixel[:3] == color else 0 for pixel in bubble.get_flattened_data()])
    ImageDraw.floodfill(mask, (430, 290), 128)
    mask = mask.point(lambda value: 255 if value == 128 else 0)
    ImageDraw.floodfill(mask, (0, 0), 128)
    mask = mask.point(lambda value: 0 if value == 128 else 255)
    bubble.putalpha(mask)
    bubble.save(ROOT / 'bubble_initial.png', icc_profile=last.info.get('icc_profile'))
    ready = bubble.copy()
    ready.putdata([color + (pixel[3],) if pixel[:3] == (238, 225, 233) else pixel
                   for pixel in ready.get_flattened_data()])
    ready.save(ROOT / 'bubble_ready.png', icc_profile=last.info.get('icc_profile'))
    empty = Image.new('RGBA', bubble.size, color + (255,))
    empty.putalpha(mask)
    empty.save(ROOT / 'bubble_empty.png', icc_profile=last.info.get('icc_profile'))

    def transparent_crop(bounds, name, remove_number=False, allowed=None):
        image = last.crop(bounds).convert('RGBA')
        data = []
        for pixel in image.get_flattened_data():
            if pixel[:3] == BG or (allowed is not None and pixel[:3] not in allowed):
                data.append((0, 0, 0, 0))
            elif remove_number and pixel[:3] == (255, 255, 102):
                data.append(CORAL + (255,))
            else:
                data.append(pixel)
        image.putdata(data)
        image.save(ROOT / name, icc_profile=last.info.get('icc_profile'))

    crop(last, (62, 477, 118, 529), 'checked.png')
    crop(last, (62, 640, 118, 696), 'unchecked.png')
    transparent_crop((770, 414, 1274, 918), 'pangolin.png',
                     allowed={(128, 0, 255), (64, 0, 128), (208, 178, 240)})
    transparent_crop((49, 745, 201, 855), 'length_box.png', remove_number=True)
    transparent_crop((201, 735, 269, 797), 'arrow_up.png')
    transparent_crop((201, 796, 269, 857), 'arrow_down.png')
    transparent_crop((69, 939, 506, 1024), 'clear_data.png')
    for name, bounds, icon_y in (
            ('uppercase', (59, 456, 529, 550), 21),
            ('digits', (59, 550, 409, 632), 8),
            ('symbols', (59, 633, 429, 726), 7)):
        transparent_crop(bounds, f'option_{name}.png')
        image = Image.open(ROOT / f'option_{name}.png')
        ImageDraw.Draw(image).rectangle((0, icon_y - 2, 62, icon_y + 59), fill=(0, 0, 0, 0))
        image.save(ROOT / f'option_{name}.png', icc_profile=last.info.get('icc_profile'))
    scene = last.copy()
    # All interactive artwork is drawn by its own widget so it can animate.
    scene.paste(BG, box, mask)
    body_mask = Image.open(ROOT / 'pangolin.png').getchannel('A')
    scene.paste(BG, (770, 414, 1274, 918), body_mask)
    for bounds in ((59, 456, 529, 550), (59, 550, 409, 632), (59, 633, 429, 726),
                   (49, 735, 269, 857), (69, 939, 506, 1024)):
        ImageDraw.Draw(scene).rectangle(bounds, fill=BG)
    scene.save(ROOT / 'main.png')



if __name__ == '__main__':
    main()
