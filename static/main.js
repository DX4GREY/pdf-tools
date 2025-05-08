// Utility
function updateText(input, textElement, defaultText) {
	textElement.textContent = input.files.length > 0 ? input.files[0].name : defaultText;
}

function handleDropzone(dropzone, input, textElement, defaultText) {
	dropzone.addEventListener('dragover', (e) => {
		e.preventDefault();
		dropzone.style.backgroundColor = '#ddd';
	});
	dropzone.addEventListener('dragleave', () => {
		dropzone.style.backgroundColor = '#fafafa';
	});
	dropzone.addEventListener('drop', (e) => {
		e.preventDefault();
		dropzone.style.backgroundColor = '#fafafa';
		const files = e.dataTransfer.files;
		if (files.length > 0 && files[0].type === 'application/pdf') {
			input.files = files;
			updateText(input, textElement, defaultText);
		}
	});
	input.addEventListener('change', () => updateText(input, textElement, defaultText));
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
	"Drop or Click to Upload PDF"
);

// Compress
handleDropzone(
	document.getElementById('compress_dropzone'),
	document.getElementById('compress_input'),
	document.getElementById('compress_dropzone_text'),
	"Drop or Click to Upload PDF"
);

// Word To PDF
handleDropzone(
	document.getElementById('word_dropzone'),
	document.getElementById('word_input'),
	document.getElementById('word_dropzone_text'),
	"Drop or Click to Upload Word File"
);

// HTML to PDF
const htmlInput = document.getElementById("html_input");
const htmlText = document.getElementById("html_dropzone_text");

htmlInput.addEventListener("change", () => {
	htmlText.textContent = htmlInput.files.length > 0 ? htmlInput.files[0].name : "Drop or Click to Upload PDF";
});

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