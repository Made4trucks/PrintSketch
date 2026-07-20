from PIL import Image, ImageStat, ImageFilter
import os


class PreviewQualityEngine:

    def __init__(self, image_path):

        self.image_path = image_path
        self.image = Image.open(image_path).convert("RGB")

    # ---------------------------------------------------

    def resolution_score(self):

        width, height = self.image.size

        megapixels = (width * height) / 1_000_000

        if megapixels >= 12:
            score = 100
        elif megapixels >= 8:
            score = 90
        elif megapixels >= 5:
            score = 75
        elif megapixels >= 3:
            score = 55
        else:
            score = 30

        return {
            "width": width,
            "height": height,
            "megapixels": round(megapixels, 2),
            "score": score
        }