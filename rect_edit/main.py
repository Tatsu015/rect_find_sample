from pathlib import Path
from pdf2image import convert_from_path

pdf_path = Path('./sample.pdf')
pages = convert_from_path(pdf_path)
image_dir = Path("./image")
for i, page in enumerate(pages):
    file_name = pdf_path.stem + "_{:02d}".format(i + 1) + ".jpeg"
    image_path = image_dir / file_name
    # JPEGで保存
    page.save(str(image_path), "JPEG")