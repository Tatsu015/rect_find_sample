import cv2 as cv
from rect_find_sample.testsheet_frame_finder import TestsheetFrameFinder, Rectangle


def draw_rects(
    src_image_path: str, dst_img_path: str, rects: list[Rectangle], buffer: int = -5
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


finder = TestsheetFrameFinder()
finder.convert_pdf2jpeg("./sample.pdf", "./image")
rects = finder.find_rectangles("./image/sample_01.jpeg")
draw_rects("./image/sample_01.jpeg", "result.jpeg", rects)
