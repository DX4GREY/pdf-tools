import os, time, shutil
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
import logging  # Tambahkan impor logging

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def allowed_file(filename):
	logging.info(f"Checking if file is allowed: {filename}")
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_images_to_pdf(image_paths):
	logging.info("Converting images to PDF")
	image_list = []
	for image_path in image_paths:
		img = Image.open(image_path)
		img = img.convert("RGB")
		image_list.append(img)

	output_pdf = BytesIO()
	image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:], resolution=100.0, quality=95, optimize=True)
	output_pdf.seek(0)

	logging.info("Images successfully converted to PDF")
	return output_pdf

def Compress(input_path, output_path, power=2):
	logging.info(f"Compressing PDF: {input_path} with power {power}")
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
	logging.info(f"Compressed PDF saved to: {output_path}")
	
def cleanup_output_folder():
	logging.info("Starting cleanup thread for output folder")
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
					logging.info(f"[Auto Cleanup] Deleted: {path}")
				except Exception as e:
					print(f"[Auto Cleanup] Error bro {path}: {e}")
		time.sleep(600)

def slide_to_image(slide, width, height):
	logging.info("Converting slide to image")
	"""
	Helper function to render a slide as an image.
	"""
	from PIL import Image, ImageDraw

	try:
			# Dynamically adjust resolution to prevent memory issues
		scale_factor = 1
		while True:
			try:
				adjusted_width = int(width // scale_factor)
				adjusted_height = int(height // scale_factor)
				img = Image.new("RGB", (adjusted_width, adjusted_height), "white")
				draw = ImageDraw.Draw(img)

				for shape in slide.shapes:
					if shape.has_text_frame:
						y_offset = 10  # Start drawing text from the top
						for paragraph in shape.text_frame.paragraphs:
							for run in paragraph.runs:
								text = run.text.strip()
								if text:  # Only draw non-empty text
									draw.text((10, y_offset), text, fill="black")
									y_offset += 15  # Increment y-offset for the next line of text

				logging.info("Slide successfully converted to image")
				return img
			except MemoryError:
				scale_factor *= 2  # Increase scale factor to reduce resolution
				logging.warning(f"MemoryError: Reducing resolution by scale factor {scale_factor}")
				if scale_factor > 8:  # Prevent infinite scaling
					logging.error("Unable to process slide due to memory constraints.")
					return None
	except AttributeError as e:
		logging.error(f"AttributeError while processing slide: {e}")
		logging.debug("Ensure the slide object has the expected attributes.", exc_info=True)
	except Exception as e:
		logging.error(f"Unexpected error converting slide to image: {e.__class__.__name__}: {e}")
		logging.debug("Stack trace:", exc_info=True)
		return None