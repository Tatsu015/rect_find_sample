from pathlib import Path
from pdf2image import convert_from_path
import cv2 as cv
import math
import numpy as np


def convert_pdf2jpeg(src_pdf_path: str, export_dir : str) -> None:
    pdf_path = Path(src_pdf_path)
    pages = convert_from_path(pdf_path)
    image_dir = Path(export_dir)
    for i, page in enumerate(pages):
        file_name = pdf_path.stem + "_{:02d}".format(i + 1) + ".jpeg"
        image_path = image_dir / file_name
        # JPEGで保存
        page.save(str(image_path), "JPEG")



convert_pdf2jpeg("./sample.pdf", "./image")


# ファイルを読み込み
image_file = './image/sample_01.jpeg'
src = cv.imread(image_file, cv.IMREAD_COLOR)
# 画像の大きさ取得
height, width, channels = src.shape
image_size = height * width
# グレースケール化
img_gray = cv.cvtColor(src, cv.COLOR_RGB2GRAY)
# しきい値指定によるフィルタリング
retval, dst = cv.threshold(img_gray, 127, 255, cv.THRESH_TOZERO_INV )
# 白黒の反転
dst = cv.bitwise_not(dst)
# 再度フィルタリング
retval, dst = cv.threshold(dst, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
# 輪郭を抽出
contours, hierarchy = cv.findContours(dst, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# この時点での状態をデバッグ出力
dst = cv.imread(image_file, cv.IMREAD_COLOR)
dst = cv.drawContours(dst, contours, -1, (0, 0, 255, 255), 2, cv.LINE_AA)
cv.imwrite('debug_1.png', dst)
dst = cv.imread(image_file, cv.IMREAD_COLOR)
for i, contour in enumerate(contours):
    # 小さな領域の場合は間引く
    area = cv.contourArea(contour)
    if area < 500:
        continue
    # 画像全体を占める領域は除外する
    if image_size * 0.99 < area:
        continue
    
    # 外接矩形を取得
    x,y,w,h = cv.boundingRect(contour)
    dst = cv.rectangle(dst,(x,y),(x+w,y+h),(0,255,0),2)
# 結果を保存
cv.imwrite('result.jpeg', dst)