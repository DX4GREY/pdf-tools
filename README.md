# PDF Tools

PDF Tools is a simple web-based application that provides various tools to manipulate PDF files, such as merging, splitting, compressing, and converting files from other formats to PDF.

## Features

1. **PDF Merger**: Combine multiple PDF files into a single PDF file.
2. **PDF Splitter**: Split a PDF file into individual pages.
3. **PDF Compressor**: Reduce the size of a PDF file by adjusting the compression level.
4. **Image to PDF**: Convert multiple images (JPG, PNG, etc.) into a single PDF file.
5. **HTML to PDF**: Convert HTML files into PDF files.
6. **Word to PDF**: Convert Word files (DOCX) into PDF files.

## Installation

### Prerequisites

- Python 3.7 or later
- Pip (Python package manager)
- Ghostscript (for PDF compression)
- Redis (optional, for rate limiting)

### Installation Steps

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd pdf-tools
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Ghostscript:
   - **Linux**: 
     ```bash
     sudo apt update && sudo apt install -y ghostscript
     ```
   - **MacOS**:
     ```bash
     brew install ghostscript
     ```
   - **Windows**: Download and install Ghostscript from [the official site](https://www.ghostscript.com/download/gsdnld.html).

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application in your browser at `http://localhost:8080`.

## Project Structure

```
pdf-tools/
├── app.py               # Main Flask application file
├── utils.py             # Utility functions for file manipulation
├── w2pdf.py             # Word to PDF conversion
├── templates/           # HTML templates for the user interface
│   ├── index.html       # Main page
│   └── 521.html         # Error 521 page
├── static/              # Static files (CSS, JS, etc.)
│   ├── main.js          # Frontend logic
│   ├── style.css        # Main styles
│   └── style.css.bak    # Backup styles
├── requirements.txt     # Python dependencies list
├── install-dep.sh       # Installation script for Linux/MacOS
├── install-dep.bat      # Installation script for Windows
└── README.md            # Project documentation
```

## Usage Instructions

1. **PDF Merger**:
   - Upload multiple PDF files.
   - Arrange the file order using drag-and-drop.
   - Click the "Merge" button to combine the files.

2. **PDF Splitter**:
   - Upload a PDF file.
   - Click the "Split" button to separate the file into individual pages.

3. **PDF Compressor**:
   - Upload a PDF file.
   - Select the compression level using the slider.
   - Click the "Compress" button to reduce the file size.

4. **Image to PDF**:
   - Upload multiple images.
   - Arrange the image order using drag-and-drop.
   - Click the "Convert to PDF" button to create a PDF file.

5. **HTML to PDF**:
   - Upload an HTML file.
   - Click the "Convert" button to convert the file into a PDF.

6. **Word to PDF**:
   - Upload a Word file (DOCX).
   - Click the "Convert to PDF" button to convert the file into a PDF.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contributors

- **Dx4** - Lead Developer
