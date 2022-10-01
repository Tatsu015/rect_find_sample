from dataclasses import dataclass
from email.policy import strict
from pathlib import Path
from pdf2image import convert_from_path
import cv2 as cv


@dataclass(frozen=True)
class Rectangle:
    x: int
    y: int
    w: int
    h: int


def convert_pdf2jpeg(src_pdf_path: str, export_dir: str) -> None:
    pdf_path = Path(src_pdf_path)
    pages = convert_from_path(pdf_path)
    image_dir = Path(export_dir)
    for i, page in enumerate(pages):
        file_name = pdf_path.stem + "_{:02d}".format(i + 1) + ".jpeg"
        image_path = image_dir / file_name
        # JPEGで保存
        page.save(str(image_path), "JPEG")


def find_rectangles(image_path: str) -> list[Rectangle]:
    src = cv.imread(image_path, cv.IMREAD_COLOR)
    height, width, _ = src.shape
    image_size = height * width

    img_gray = cv.cvtColor(src, cv.COLOR_RGB2GRAY)

    _, dst = cv.threshold(img_gray, 127, 255, cv.THRESH_TOZERO_INV)

    dst = cv.bitwise_not(dst)

    _, dst = cv.threshold(dst, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

    contours, _ = cv.findContours(dst, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    dst = cv.imread(image_path, cv.IMREAD_COLOR)
    dst = cv.drawContours(dst, contours, -1, (0, 0, 255, 255), 2, cv.LINE_AA)
    cv.imwrite("debug_1.jpeg", dst)
    dst = cv.imread(image_path, cv.IMREAD_COLOR)

    rects: list[Rectangle] = []
    for i, contour in enumerate(contours):
        # 小さな領域の場合は間引く
        area = cv.contourArea(contour)
        if area < 500:
            continue
        # 画像全体を占める領域は除外する
        if image_size * 0.99 < area:
            continue

        # 外接矩形を取得
        x, y, w, h = cv.boundingRect(contour)
        rect = Rectangle(x, y, w, h)
        rects.append(rect)


convert_pdf2jpeg("./sample.pdf", "./image")
rects = find_rectangles("./image/sample_01.jpeg")
dst = cv.imread("./image/sample_01.jpeg", cv.IMREAD_COLOR)
for r in rects:
    dst = cv.rectangle(dst, (r.x, r.y), (r.x + r.w, r.y + r.h), (0, 255, 0), 2)
cv.imwrite("result.jpeg", dst)
