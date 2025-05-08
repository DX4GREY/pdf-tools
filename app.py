from flask import Flask, render_template, request, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
from utils import *
from PIL import Image
import os, uuid, shutil, threading, pdfkit, tempfile
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from werkzeug.utils import secure_filename
from weasyprint import HTML
from flask_redis import FlaskRedis
from docx import Document
from fpdf import FPDF
from w2pdf import docx_to_pdf_better
from pptx import Presentation
from utils import slide_to_image
import logging  # Tambahkan impor logging

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Rate limiter setup
# app.config['REDIS_URL'] = "redis://localhost:6379/0"
redis = FlaskRedis(app)
limiter = Limiter(get_remote_address, app=app, default_limits=["50 per minute"])

# Konfigurasi logging
if app.debug:  # Aktifkan logging hanya jika Flask dalam mode debug
	logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.errorhandler(RateLimitExceeded)
def ratelimit_handler(e):
	if app.debug:
		logging.warning("Rate limit exceeded")
	return render_template('521.html'), 521

@app.route('/')
def index():
	if app.debug:
		logging.info("Accessed index page")
	return render_template('index.html')

@app.route('/merge', methods=['POST'])
@limiter.limit("10 per minute")
def merge():
	if app.debug:
		logging.info("Merge endpoint called")
	files = request.files.getlist('merge_files')
	order = request.form.get('order', '')

	filenames = []
	for file in files:
		logging.info(f"Processing file: {file.filename}")
		filename = f"{uuid.uuid4().hex}.pdf"
		path = os.path.join(UPLOAD_FOLDER, filename)
		file.save(path)
		filenames.append(path)

	file_order = [int(i) for i in order.split(',') if i.isdigit()]
	files_ordered = [filenames[i] for i in file_order if i < len(filenames)]

	merger = PdfMerger()
	for path in files_ordered:
		merger.append(path)

	output_path = os.path.join(OUTPUT_FOLDER, f'merged_{uuid.uuid4().hex}.pdf')
	merger.write(output_path)
	merger.close()

	for f in filenames:
		os.remove(f)

	if app.debug:
		logging.info(f"Merged PDF saved to: {output_path}")
	return send_file(output_path, as_attachment=True)

@app.route('/split', methods=['POST'])
@limiter.limit("10 per minute")
def split():
	if app.debug:
		logging.info("Split endpoint called")
	file = request.files.get('split_file')
	if not file:
		return 'No file uploaded', 400

	reader = PdfReader(file)
	split_dir = os.path.join(OUTPUT_FOLDER, f"split_{uuid.uuid4().hex}")
	os.makedirs(split_dir, exist_ok=True)

	for i, page in enumerate(reader.pages):
		writer = PdfWriter()
		writer.add_page(page)
		with open(os.path.join(split_dir, f'page_{i+1}.pdf'), 'wb') as f:
			writer.write(f)

	zip_path = f"{split_dir}.zip"
	shutil.make_archive(split_dir, 'zip', split_dir)
	shutil.rmtree(split_dir)

	if app.debug:
		logging.info(f"Split PDF saved to: {zip_path}")
	return send_file(zip_path, as_attachment=True)

@app.route('/compress', methods=['POST'])
@limiter.limit("8 per minute")
def compress_pdf_route():
	if app.debug:
		logging.info("Compress endpoint called")
	uploaded_file = request.files.get('file')
	if not uploaded_file or uploaded_file.filename == '':
		return "No file uploaded", 400
	try:
		power = int(request.form.get('power', 2))
	except ValueError:
		power = 2 

	filename = secure_filename(uploaded_file.filename)
	input_path = os.path.join(UPLOAD_FOLDER, filename)
	uploaded_file.save(input_path)

	filename = f"{uuid.uuid4().hex}.pdf"
	output_path = os.path.join(OUTPUT_FOLDER, f"compressed_{filename}")

	try:
		Compress(input_path, output_path, power=power)
		if app.debug:
			logging.info(f"Compressed PDF saved to: {output_path}")
		return send_file(output_path, as_attachment=True, download_name=f"compressed_{filename}")
	except Exception as e:
		return f"Compression failed: {e}", 500
	finally:
		if os.path.exists(input_path):
			os.remove(input_path)
		if os.path.exists(output_path):
			os.remove(output_path)

@app.route('/image_to_pdf', methods=['POST'])
@limiter.limit("8 per minute")
def image_to_pdf():
	if app.debug:
		logging.info("Image to PDF endpoint called")
	files = request.files.getlist('image_files')
	order = request.form.get('order')

	if not files or not order:
		return "No files or order info provided", 400

	try:
		ordered_filenames = order.split(',')
	except Exception as e:
		return f"Invalid order format: {e}", 400

	file_map = {f.filename: f for f in files}

	images = []
	for name in ordered_filenames:
		original_file = file_map.get(name)
		if original_file and allowed_file(original_file.filename):
			img = Image.open(original_file).convert("RGB")
			images.append(img)
		else:
			return f"Invalid or missing file in order: {name}", 400

	if not images:
		return "No valid images after ordering", 400
	fname = f"cimages_{uuid.uuid4().hex}.pdf"
	output_pdf_path = os.path.join(OUTPUT_FOLDER, fname)
	images[0].save(output_pdf_path, save_all=True, append_images=images[1:], resolution=100.0, quality=95)

	if app.debug:
		logging.info(f"Image-based PDF saved to: {output_pdf_path}")
	return send_file(output_pdf_path, as_attachment=True, download_name=fname)

@app.route('/html_to_pdf', methods=['POST'])
@limiter.limit("5 per minute")
def html_to_pdf():
	if app.debug:
		logging.info("HTML to PDF endpoint called")
	uploaded_file = request.files.get('html_file')
	if not uploaded_file or not uploaded_file.filename.endswith(('.html', '.htm')):
		return "File tidak valid. Harus .html atau .htm", 400

	try:
		with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_html:
			uploaded_file.save(temp_html.name)
			html_path = temp_html.name

		fname = f"html2p_{uuid.uuid4().hex}.pdf"
		output_pdf = os.path.join(OUTPUT_FOLDER, fname)

		HTML(html_path).write_pdf(output_pdf)

		if app.debug:
			logging.info(f"HTML-based PDF saved to: {output_pdf}")
		return send_file(output_pdf, as_attachment=True, download_name=fname)
	except Exception as e:
		return f"Gagal konversi: {e}", 500
	finally:
		try: os.remove(html_path)
		except: pass


class StyledPDF(FPDF):
	def __init__(self):
		super().__init__()
		self.set_auto_page_break(auto=True, margin=15)
		self.add_page()
		self.set_font("Arial", size=12)

	def write_text(self, run):
		style = ''
		if run.bold: style += 'B'
		if run.italic: style += 'I'
		if style:
			self.set_font("Arial", style=style, size=12)
		else:
			self.set_font("Arial", style='', size=12)
		self.write(5, run.text)

@app.route('/word_to_pdf', methods=['POST'])
@limiter.limit("5 per minute")
def word_to_pdf():
	if app.debug:
		logging.info("Word to PDF endpoint called")
	uploaded_file = request.files.get('file')
	if not uploaded_file or not uploaded_file.filename.endswith('.docx'):
		return "File tidak valid. Harus .docx", 400

	try:
		docx_path = os.path.join(UPLOAD_FOLDER, secure_filename(uploaded_file.filename))
		uploaded_file.save(docx_path)

		output_pdf_name = f"word2pdf_{uuid.uuid4().hex}.pdf"
		output_pdf_path = os.path.join(OUTPUT_FOLDER, output_pdf_name)

		docx_to_pdf_better(docx_path, output_pdf_path)

		if app.debug:
			logging.info(f"Word-based PDF saved to: {output_pdf_path}")
		return send_file(output_pdf_path, as_attachment=True, download_name=output_pdf_name)
	except Exception as e:
		return f"Gagal konversi: {e}", 500
	finally:
		try: os.remove(docx_path)
		except: pass

@app.route('/ppt_to_pdf', methods=['POST'])
@limiter.limit("5 per minute")
def ppt_to_pdf():
	if app.debug:
		logging.info("PPT to PDF endpoint called")
	uploaded_file = request.files.get('file')
	if not uploaded_file or not uploaded_file.filename.endswith('.pptx'):
		return "File tidak valid. Harus .pptx", 400

	try:
		pptx_path = os.path.join(UPLOAD_FOLDER, secure_filename(uploaded_file.filename))
		uploaded_file.save(pptx_path)

		output_pdf_name = f"ppt2pdf_{uuid.uuid4().hex}.pdf"
		output_pdf_path = os.path.join(OUTPUT_FOLDER, output_pdf_name)

		prs = Presentation(pptx_path)
		pdf = FPDF()
		pdf.set_auto_page_break(auto=True, margin=0)

		for i, slide in enumerate(prs.slides):
			# Render slide as an image
			img_path = os.path.join(OUTPUT_FOLDER, f"slide_{i+1}.png")
			slide_width = prs.slide_width
			slide_height = prs.slide_height

			# Save slide as an image using Pillow
			slide_image = slide_to_image(slide, slide_width, slide_height)
			slide_image.save(img_path, "PNG")

			# Add image to PDF
			pdf.add_page()
			pdf.image(img_path, x=0, y=0, w=210, h=297)  # A4 size (210x297 mm)

			# Remove temporary image file
			os.remove(img_path)

		pdf.output(output_pdf_path)

		if app.debug:
			logging.info(f"PPT-based PDF saved to: {output_pdf_path}")
		return send_file(output_pdf_path, as_attachment=True, download_name=output_pdf_name)
	except Exception as e:
		return f"Gagal konversi: {e}", 500
	finally:
		try: os.remove(pptx_path)
		except: pass

if __name__ == '__main__':
	if app.debug:
		logging.info("Starting the application in debug mode")
	threading.Thread(target=cleanup_output_folder, daemon=True).start()
	app.run(debug=True, host="0.0.0.0", port=8080)