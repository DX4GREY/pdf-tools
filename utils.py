import os, time, shutil
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_images_to_pdf(image_paths):
	image_list = []
	for image_path in image_paths:
		img = Image.open(image_path)
		img = img.convert("RGB")
		image_list.append(img)

	output_pdf = BytesIO()
	image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:], resolution=100.0, quality=95, optimize=True)
	output_pdf.seek(0)

	return output_pdf

def Compress(input_path, output_path, power=2):
	# Map power ke kualitas JPEG
	quality_map = {
		1: 30,   # screen
		2: 50,   # ebook
		3: 70,   # printer
		4: 90	# prepress
	}
	quality = quality_map.get(power, 50)

	# Buka PDF asli
	original = fitz.open(input_path)

	# Simpan halaman sebagai gambar (rasterize)
	images = []
	for page in original:
		pix = page.get_pixmap(dpi=150)  # Bisa diubah tergantung kualitas
		img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
		buffer = BytesIO()
		img.save(buffer, format="JPEG", quality=quality)
		images.append(Image.open(BytesIO(buffer.getvalue())).convert("RGB"))

	# Buat PDF baru dari gambar
	if images:
		images[0].save(output_path, save_all=True, append_images=images[1:])

	original.close()
	
def cleanup_output_folder():
	time.sleep(3)
	while True:
		for folder in [OUTPUT_FOLDER, UPLOAD_FOLDER]:
			for filename in os.listdir(folder):
				path = os.path.join(folder, filename)
				try:
					if os.path.isfile(path) or os.path.islink(path):
						os.remove(path)
					elif os.path.isdir(path):
						shutil.rmtree(path)
					print(f"[Auto Cleanup] Deleted: {path}")
				except Exception as e:
					print(f"[Auto Cleanup] Error bro {path}: {e}")
		time.sleep(600)