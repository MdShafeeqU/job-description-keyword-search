// content_script.js

chrome.runtime.onMessage.addListener((request) => {
    if (request.type === 'popup-modal') {
        console.log("Received message to show modal. Processed Text:", request.processedText);
        showModal(request.processedText);
    }
});

const showModal = (processedText) => {
    console.log("Showing modal with processed text:", processedText);

    const modal = document.createElement("div");
    modal.classList.add("modal");

    modal.innerHTML = `
        <div class="modal-content">
            <div style="font-size: 16px; margin-bottom: 20px; line-height: 1.5; color: #333;">${processedText}</div>
            <button class="upload-btn">Upload</button>
            <button class="close-btn">Close</button>
        </div>
    `;

    modal.setAttribute(
        "style",`
        display: block;
        padding: 20px;
        position: fixed;
        z-index: 9999;
        top: 0;
        right: 1px;
        width: 400px; /* Adjust width as needed */
        height: 100vh;
        overflow-y: auto;
        margin: auto;
        box-sizing: border-box;
      `
    );

    modal.querySelector(".modal-content").setAttribute(
        "style",`
        background-color: #fefefe;
        padding: 20px;
        border: 1px solid #888;
        border-radius: 0; /* Square corners */
        width: 100%;
      `
    );

    modal.querySelector(".upload-btn").setAttribute(
        "style",`
        padding: 10px 16px;
        font-size: 16px;
        border: none;
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
        cursor: pointer;
        margin-right: 10px;
        transition: background-color 0.3s;
      `
    );

    modal.querySelector(".close-btn").setAttribute(
        "style",`
        padding: 10px 16px;
        font-size: 16px;
        border: none;
        border-radius: 20px;
        background-color: #f44336;
        color: white;
        cursor: pointer;
        transition: background-color 0.3s;
      `
    );

    document.body.appendChild(modal);

    const closeBtn = modal.querySelector(".close-btn");
    const uploadBtn = modal.querySelector(".upload-btn");

    closeBtn.addEventListener("click", () => {
        console.log("Closing modal");
        modal.style.display = "none";
    });

    uploadBtn.addEventListener("click", () => {
        console.log("Uploading resume");
        triggerFileInput();
    });

    // Prevent modal from closing when clicking outside
    modal.addEventListener("click", (event) => {
        if (event.target === modal) {
            event.stopPropagation();
        }
    });
};

function triggerFileInput() {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.txt, .pdf, .doc, .docx';

    fileInput.addEventListener('change', handleFileUpload);

    fileInput.click();
}

function handleFileUpload(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const resumeContent = e.target.result;
            // Send resume content to background script
            chrome.runtime.sendMessage({ type: "uploadResume", resumeContent: resumeContent });
            alert('Resume uploaded successfully!');
        };
        reader.readAsText(file);
    } else {
        alert('Please select a valid resume file.');
    }
}
