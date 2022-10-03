from dataclasses import dataclass
from pathlib import Path
from typing import Any
from pdf2image import convert_from_path
import cv2 as cv
import numpy as np


@dataclass(frozen=True)
class Rectangle:
    x: int
    y: int
    w: int
    h: int

    def is_contain(self, inner: "Rectangle") -> bool:
        if self is inner:
            return False

        if self.x > inner.x or self.x + self.w < inner.x:
            return False
        if self.y > inner.y or self.y + self.h < inner.y:
            return False
        if self.w < inner.w:
            return False
        if self.h < inner.h:
            return False
        return True


class TestsheetFrameFinder:
    def convert_pdf2png(self, src_pdf_path: str, export_dir: str) -> None:
        pdf_path = Path(src_pdf_path)
        pages = convert_from_path(pdf_path)
        image_dir = Path(export_dir)
        for i, page in enumerate(pages):
            file_name = pdf_path.stem + "_{:02d}".format(i + 1) + ".png"
            image_path = image_dir / file_name
            page.save(str(image_path), "PNG")

    def find_rectangles(self, image_path: str) -> list[Rectangle]:
        src = cv.imread(image_path, cv.IMREAD_COLOR)
        height, width, _ = src.shape
        image_size = height * width

        img_gray = cv.cvtColor(src, cv.COLOR_RGB2GRAY)

        _, dst = cv.threshold(img_gray, 230, 255, cv.THRESH_BINARY)
        dst = cv.bitwise_not(dst)

        kernel = np.ones((3, 3), np.uint8)
        dst = cv.dilate(dst, kernel, iterations=1)

        _, dst = cv.threshold(dst, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

        contours, _ = cv.findContours(dst, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        rects = self.__filter(image_size, contours)
        return rects

    def __filter(self, image_size: int, contours: Any) -> list[Rectangle]:
        rects: list[Rectangle] = []
        for _, contour in enumerate(contours):
            if self.__is_too_small(image_size, contour):
                continue
            x, y, w, h = cv.boundingRect(contour)
            rects.append(Rectangle(x, y, w, h))

        rects = self.__remove_outers(rects)

        return rects

    def __is_too_small(self, image_size: int, contour: Any) -> bool:
        area = cv.contourArea(contour)
        if area < 1000:
            return True

        if image_size * 0.99 < area:
            return True

        x, y, w, h = cv.boundingRect(contour)

        if h < 100:
            return True

        if w < 100:
            return True

        if w < h:
            return True

        return False

    def __remove_outers(self, rects: list[Rectangle]) -> list[Rectangle]:
        inners = []
        for rect in rects:
            if not self.__is_any_contain(rect, rects):
                inners.append(rect)

        return inners

    def __is_any_contain(self, outer: Rectangle, inners: list[Rectangle]) -> bool:
        for inner in inners:
            if outer.is_contain(inner):
                return True
        return False
