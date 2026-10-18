"""Convert generated images into level art files (<=1.5 MB, <=2048 px). Usage in code: art.export(src, dst, crop=None, alpha=False, square=False, maxpx=1024)"""
from PIL import Image, ImageDraw
import os
def export(src, dst, crop=None, alpha=False, square=False, maxpx=1024, quality=86):
    im = Image.open(src).convert('RGB')
    if square:
        w, h = im.size; s = min(w, h); im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
    if crop: im = im.crop(crop)
    im.thumbnail((maxpx, maxpx))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if alpha:
        im = im.convert('RGBA'); w, h = im.size
        # flood the near-white background from the border to transparent
        for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]:
            if sum(im.getpixel(seed)[:3]) > 3 * 225:
                ImageDraw.floodfill(im, seed, (255, 255, 255, 0), thresh=40)
        im.save(dst, optimize=True)
    else:
        im.save(dst, quality=quality, optimize=True)
    return os.path.getsize(dst)
