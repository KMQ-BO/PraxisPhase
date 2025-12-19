from pdf2image import convert_from_path
import os

output_dir = "pages_4"
os.makedirs(output_dir, exist_ok=True)

pages = convert_from_path("Freiwilligen/004.pdf", dpi=300)

for i, page in enumerate(pages):
    page.save(f"{output_dir}/page_{i+1:03}.png", "PNG")



print("DONE")