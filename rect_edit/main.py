from ast import Return
from dataclasses import dataclass
from email.mime import image
from email.policy import strict
from pathlib import Path
from tkinter.messagebox import RETRY
from typing import Any
from black import out
from cv2 import contourArea
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


def convert_pdf2jpeg(src_pdf_path: str, export_dir: str) -> None:
    pdf_path = Path(src_pdf_path)
    pages = convert_from_path(pdf_path)
    image_dir = Path(export_dir)
    for i, page in enumerate(pages):
        file_name = pdf_path.stem + "_{:02d}".format(i + 1) + ".jpeg"
        image_path = image_dir / file_name
        page.save(str(image_path), "JPEG")


def find_rectangles(image_path: str) -> list[Rectangle]:
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

    rects = __filter(image_size, contours)
    return rects


def draw_rects(
    src_image_path: str, dst_img_path: str, rects: list[Rectangle], buffer: int=-5
) -> None:
    dst = cv.imread(src_image_path, cv.IMREAD_COLOR)
    rect_color = (0, 255, 0)
    for r in rects:
        dst = cv.rectangle(
            dst,
            (r.x - buffer, r.y - buffer),
            (r.x + r.w + buffer, r.y + r.h + buffer),
            rect_color,
            2,
        )
    cv.imwrite(dst_img_path, dst)


def __filter(image_size: int, contours: Any) -> list[Rectangle]:
    rects: list[Rectangle] = []
    for _, contour in enumerate(contours):
        area = cv.contourArea(contour)
        if area < 1000:
            continue

        if image_size * 0.99 < area:
            continue

        x, y, w, h = cv.boundingRect(contour)

        if h < 100:
            continue

        if w < 100:
            continue

        if w < h:
            continue

        rect = Rectangle(x, y, w, h)
        rects.append(rect)

    rects = __remove_outers(rects)

    return rects


def __remove_outers(rects: list[Rectangle]) -> list[Rectangle]:
    inners = []
    for rect in rects:
        if not __is_any_contain(rect, rects):
            inners.append(rect)

    return inners


def __is_any_contain(outer: Rectangle, inners: list[Rectangle]) -> bool:
    for inner in inners:
        if outer.is_contain(inner):
            return True
    return False


convert_pdf2jpeg("./sample.pdf", "./image")
rects = find_rectangles("./image/sample_01.jpeg")
draw_rects("./image/sample_01.jpeg", "result.jpeg", rects)
