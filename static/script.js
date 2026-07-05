const file = document.querySelector('input[type="file"]');
const form = document.querySelector('form');
const submitButton = document.querySelector('button[type="submit"]');
const fileLabelText = document.getElementById('file-label-text');
const dropArea = document.getElementById('file-drop-area');
const API = window.location.origin;

function updateFileLabel() {
    if (!fileLabelText) {
        return;
    }

    if (file && file.files && file.files[0]) {
        fileLabelText.textContent = `Selected file: ${file.files[0].name}`;
    } else {
        fileLabelText.textContent = 'Drag & Drop your file here or click to select';
    }
}

if (file) {
    file.addEventListener('change', updateFileLabel);
}

['dragenter', 'dragover'].forEach((eventName) => {
    dropArea?.addEventListener(eventName, (event) => {
        event.preventDefault();
        event.stopPropagation();
        dropArea.classList.add('drag-over');
    });
});

['dragleave', 'dragend', 'drop'].forEach((eventName) => {
    dropArea?.addEventListener(eventName, (event) => {
        event.preventDefault();
        event.stopPropagation();
        dropArea.classList.remove('drag-over');
    });
});

dropArea?.addEventListener('drop', (event) => {
    if (file && event.dataTransfer?.files?.length) {
        file.files = event.dataTransfer.files;
        updateFileLabel();
    }
});

function formatValue(value) {
    if (value === null || value === undefined || value === '') {
        return 'No breakdown available';
    }

    if (Array.isArray(value)) {
        if (value.length === 0) {
            return 'No breakdown available';
        }

        return value.map((entry) => {
            if (entry && typeof entry === 'object') {
                const description = entry.description ?? entry.name ?? entry.label ?? 'Item';
                const detail = entry.value ?? entry.amount ?? entry.price ?? entry.rate ?? entry.total ?? entry.detail ?? '';
                return `${description}: ${detail}`;
            }
            return String(entry);
        }).join(' • ');
    }

    if (typeof value === 'object') {
        return Object.entries(value)
            .map(([key, innerValue]) => `${key}: ${innerValue}`)
            .join(', ');
    }

    return String(value);
}

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    if (!file || !file.files || !file.files[0]) {
        alert('Please choose a file first.');
        return;
    }

    submitButton.disabled = true;
    submitButton.textContent = 'Processing...';

    const formData = new FormData();
    formData.append('file', file.files[0]);

    try {
        const response = await fetch(`${API}/extract`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        if (!result.success) {
            throw new Error(result.msg || 'Extraction failed.');
        }

        displayResult(result.data);
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Upload';
    }
});

function displayResult(result) {
    const loadSection = document.querySelector(".load-info");
    const pickupSection = document.querySelector(".pickup-info");
    const deliverySection = document.querySelector(".delivery-info");
    const rateSection = document.querySelector(".rate-info");

    [loadSection, pickupSection, deliverySection, rateSection].forEach((section) => {
        if (section) {
            section.innerHTML = '';
        }
    });

    if (!result) {
        return;
    }

    const loadData = result.load || {};
    Object.keys(loadData).forEach((key) => {
        const row = document.createElement("div");
        const rowKey = document.createElement("span");
        const rowValue = document.createElement("span");

        row.classList.add("response-item-cont");
        rowKey.classList.add("item-key");
        rowValue.classList.add("item-val");

        rowKey.textContent = key.split('_').join(' ') || '-';
        rowValue.textContent = formatValue(loadData[key]);

        row.appendChild(rowKey);
        row.appendChild(rowValue);
        if (loadSection) {
            loadSection.appendChild(row);
        }
    });

    const pickupData = result.pickup || {};
    Object.keys(pickupData).forEach((key) => {
        const row = document.createElement("div");
        const rowKey = document.createElement("span");
        const rowValue = document.createElement("span");

        row.classList.add("response-item-cont");
        rowKey.classList.add("item-key");
        rowValue.classList.add("item-val");

        rowKey.textContent = key.split('_').join(' ') || '-';
        rowValue.textContent = formatValue(pickupData[key]);

        row.appendChild(rowKey);
        row.appendChild(rowValue);
        if (pickupSection) {
            pickupSection.appendChild(row);
        }
    });

    const deliveryData = result.delivery || {};
    Object.keys(deliveryData).forEach((key) => {
        const row = document.createElement("div");
        const rowKey = document.createElement("span");
        const rowValue = document.createElement("span");

        row.classList.add("response-item-cont");
        rowKey.classList.add("item-key");
        rowValue.classList.add("item-val");

        rowKey.textContent = key.split('_').join(' ') || '-';
        rowValue.textContent = formatValue(deliveryData[key]);

        row.appendChild(rowKey);
        row.appendChild(rowValue);
        if (deliverySection) {
            deliverySection.appendChild(row);
        }
    });

    const rateData = result.rate || {};
    Object.keys(rateData).forEach((key) => {
        const row = document.createElement("div");
        const rowKey = document.createElement("span");
        const rowValue = document.createElement("span");

        row.classList.add("response-item-cont");
        rowKey.classList.add("item-key");
        rowValue.classList.add("item-val");

        rowKey.textContent = key.split('_').join(' ') || '-';
        rowValue.textContent = formatValue(rateData[key]);

        row.appendChild(rowKey);
        row.appendChild(rowValue);
        if (rateSection) {
            rateSection.appendChild(row);
        }
    });
}