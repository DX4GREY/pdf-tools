// Utility
function updateText(input, textElement, defaultText) {
	if (input.files.length > 0) {
		const fileNames = Array.from(input.files).map(file => file.name).join(', ');
		textElement.textContent = fileNames;
	} else {
		textElement.textContent = defaultText;
	}
}

function handleDropzone(dropzone, input, textElement, defaultText, acceptedTypes = []) {
	dropzone.addEventListener('dragover', (e) => {
		e.preventDefault();
		dropzone.classList.add('dragover'); // Add class for visual feedback
	});
	dropzone.addEventListener('dragleave', () => {
		dropzone.classList.remove('dragover'); // Remove class when dragging ends
	});
	dropzone.addEventListener('drop', (e) => {
		e.preventDefault();
		dropzone.classList.remove('dragover'); // Remove class on drop
		const files = e.dataTransfer.files;
		const dataTransfer = new DataTransfer();
		for (let file of files) {
			if (acceptedTypes.length === 0 || acceptedTypes.includes(file.type)) {
				dataTransfer.items.add(file);
			} else {
				alert(`Invalid file type: ${file.name}`);
			}
		}
		if (dataTransfer.files.length > 0) {
			for (let file of input.files) {
				dataTransfer.items.add(file); // Retain previously added files
			}
			input.files = dataTransfer.files; // Assign files programmatically
			updateText(input, textElement, defaultText);
		} else {
			alert("No valid files were added.");
		}
	});
	input.addEventListener('change', () => {
		const files = input.files;
		const validFiles = Array.from(files).filter(file => 
			acceptedTypes.length === 0 || acceptedTypes.includes(file.type)
		);
		if (validFiles.length === files.length) {
			updateText(input, textElement, defaultText);
		} else {
			alert("Some files are invalid. Please upload valid files.");
			input.value = ""; // Reset input if invalid
		}
	});
}

// Tabs
document.querySelectorAll('.tab-buttons button').forEach(btn => {
	btn.addEventListener('click', () => {
		document.querySelectorAll('.tab-buttons button').forEach(b => b.classList.remove('active'));
		btn.classList.add('active');
	});
});

function showTab(id) {
	document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
	document.getElementById(id).classList.add('active');
}

// Merge
const mergeInput = document.getElementById('merge_input');
const mergeList = document.getElementById('file_list');
const mergeOrder = document.getElementById('file_order');

mergeInput.addEventListener('change', () => {
	mergeList.innerHTML = '';
	[...mergeInput.files].forEach((file, i) => {
		const li = document.createElement('li');
		li.textContent = file.name;
		li.dataset.index = i;
		mergeList.appendChild(li);
	});
	updateMergeOrder();
});

function updateMergeOrder() {
	const indices = Array.from(mergeList.children).map(li => li.dataset.index);
	mergeOrder.value = indices.join(',');
}

Sortable.create(mergeList, {
	animation: 150,
	onEnd: updateMergeOrder
});

// Image to PDF
const imageInput = document.getElementById('image2pdf_input');
const imageList = document.getElementById('image2pdf_list');
const imageOrder = document.getElementById('image2pdf_order');

imageInput.addEventListener('change', () => {
	imageList.innerHTML = '';
	[...imageInput.files].forEach(file => {
		const li = document.createElement('li');
		li.textContent = file.name;
		li.dataset.name = file.name;
		imageList.appendChild(li);
	});
	updateImageOrder();
});

function updateImageOrder() {
	const names = Array.from(imageList.children).map(li => li.dataset.name);
	imageOrder.value = names.join(',');
}

Sortable.create(imageList, {
	animation: 150,
	onEnd: updateImageOrder
});

// Split
handleDropzone(
	document.getElementById('split_dropzone'),
	document.getElementById('split_input'),
	document.getElementById('split_dropzone_text'),
	"Drop or Click to Upload PDF",
	['application/pdf']
);

// Compress
handleDropzone(
	document.getElementById('compress_dropzone'),
	document.getElementById('compress_input'),
	document.getElementById('compress_dropzone_text'),
	"Drop or Click to Upload PDF",
	['application/pdf']
);

// Word To PDF
handleDropzone(
	document.getElementById('word_dropzone'),
	document.getElementById('word_input'),
	document.getElementById('word_dropzone_text'),
	"Drop or Click to Upload Word File",
	[
		'application/msword',
		'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
	]
);

// PPT to PDF
handleDropzone(
	document.getElementById('ppt2pdf_dropzone'),
	document.getElementById('ppt2pdf_input'),
	document.getElementById('ppt2pdf_dropzone_text'),
	"Drop or Click to Upload PPTX File",
	['application/vnd.openxmlformats-officedocument.presentationml.presentation']
);

// HTML to PDF
handleDropzone(
	document.getElementById('html_dropzone'),
	document.getElementById('html_input'),
	document.getElementById('html_dropzone_text'),
	"Drop or Click to Upload HTML File",
	['text/html']
);

// Quality slider
const qualitySlider = document.getElementById("quality");
const qualityValue = document.getElementById("quality_value");
if (qualitySlider && qualityValue) {
	qualitySlider.addEventListener("input", () => {
		qualityValue.textContent = (parseInt(qualitySlider.value) + 1);
	});
}

// Progress
function showProgress(id) {
	document.getElementById(id).style.display = "block";
}
function hideProgress(id) {
	document.getElementById(id).style.display = "none";
}
document.querySelectorAll("form").forEach(form => {
	form.addEventListener("submit", () => {
		showProgress("process_loading");
		setTimeout(() => hideProgress("process_loading"), 2500);
	});
});

document.querySelectorAll('[data-dropzone]').forEach(dropzone => {
	const type = dropzone.dataset.dropzone;
	const input = document.getElementById(`${type}_input`);
	const textElement = document.getElementById(`${type}_dropzone_text`);
	let defaultText = dropzone.textContent.trim();

	let acceptedTypes = [];
	switch (type) {
		case 'merge':
		case 'split':
		case 'compress':
			acceptedTypes = ['application/pdf'];
			break;
		case 'word':
			acceptedTypes = [
				'application/msword',
				'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
			];
			break;
		case 'ppt2pdf':
			acceptedTypes = ['application/vnd.openxmlformats-officedocument.presentationml.presentation'];
			break;
		case 'html':
			acceptedTypes = ['text/html'];
			break;
		case 'image2pdf':
			acceptedTypes = ['image/jpeg', 'image/png', 'image/gif'];
			break;
	}

	handleDropzone(dropzone, input, textElement, defaultText, acceptedTypes);
});