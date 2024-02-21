let modal;
let loadingModal;

chrome.runtime.onMessage.addListener((request) => {
    if (request.type === 'popup-modal') {
        closeLoadingModal();
        console.log("Received message to show modal. Processed Text:", request.processedText);
        showModal(request.processedText);
    }
    else if (request.type === 'match-display') {
        displayMatchText(request.text)
    }
    else if (request.type === 'loading-modal') {
        showLoadingModal();
    }
});

const closeLoadingModal = () => {
    if (loadingModal) {
        loadingModal.remove();
        loadingModal = null;
    }
};

const showLoadingModal = () => {
    closeModal(); // Close any existing modals
    loadingModal = document.createElement("div");
    loadingModal.classList.add("modal");

    loadingModal.innerHTML = `
        <div class="modal-content">
            <p>Loading...</p>
        </div>
    `;

    loadingModal.setAttribute(
        "style", `
        display: block;
        padding: 20px;
        position: fixed;
        z-index: 9999;
        top: 0;
        right: 5px;
        width: 200px;
        height: auto;
        margin: auto;
        box-sizing: border-box;
        word-wrap: break-word;
        background-color: #fefefe;
        border: 1px solid #888;
        border-radius: 0;
      `
    );

    document.body.appendChild(loadingModal);
};

const displayMatchText = (matchText) => {
    const matchTextContainer = modal.querySelector(".match-text-container");
    matchTextContainer.textContent = matchText;

    
};

const showModal = (processedText) => {
    console.log("Showing modal with processed text:", processedText);
    closeModal();
    
    modal = document.createElement("div");
    modal.classList.add("modal");

    modal.innerHTML = `
        <div class="modal-content">
            <div class="processed-text">${processedText.replace('Skills:', '<strong>Skills:</strong>')
                                                    .replace('Experience:', '<strong><br>Experience:</strong>')
                                                    .replace('Education:', '<strong><br>Education:</strong>')}
            </div>
            <div class="match-text-container" style="margin-bottom: 10px;">
            </div> 
            <button id="resumeButton" class="add-resume-btn">
                Add Resume
            </button>
            <div class="text-box-container" style="display: none;">
                <textarea id="resumeText" rows="4" cols="50" style="width: 100%;" placeholder="Enter your resume text here..."></textarea>
            </div>
            <button class="upload-btn">
                    Upload
            </button>
            <button class="close-btn">Close</button>
        </div>
    `;

    modal.querySelector(".processed-text").setAttribute(
        "style", `
        font-size: 16px;
        margin-bottom: 20px;
        line-height: 1.5;
        color: #333;
        `
    )

    modal.setAttribute(
        "style", `
        display: block;
        padding: 20px;
        position: fixed;
        z-index: 9999;
        top: 0;
        right: 5px;
        width: 400px; /* Adjust width as needed */
        height: auto;
        margin: auto;
        box-sizing: border-box;
        word-wrap: break-word;
        border-radius: 10px; 
      `
    );

    modal.querySelector(".modal-content").setAttribute(
        "style", `
        background-color: #fefefe;
        padding: 20px;
        border: 1px solid #888;
        border-radius: 10px; /* Square corners */
        height: auto;
        max-height: none;
        width: 100%;
        word-wrap: break-word;
      `
    );

    modal.querySelector(".add-resume-btn").setAttribute(
        "style", `
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

    modal.querySelector(".upload-btn").setAttribute(
        "style", `
        display: none; 
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
        "style", `
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
    const addResumeBtn = modal.querySelector(".add-resume-btn");
    const uploadBtn = modal.querySelector(".upload-btn");
    const textBoxContainer = modal.querySelector(".text-box-container");

    modal.addEventListener("click", (event) => {
        const target = event.target;
        if (target === modal) {
            event.stopPropagation(); // Prevent modal from closing when clicking outside
        } else if (target.classList.contains("close-btn")) {
            console.log("Closing modal");
            modal.style.display = "none";
        } else if (target.classList.contains("add-resume-btn")) {
            console.log("Adding resume");
            target.style.display = "none";
            textBoxContainer.style.display = "block";
            uploadBtn.style.display = "inline-block";
        } else if (target.classList.contains("upload-btn")) {
            console.log("Uploading resume");
            const resumeText = document.getElementById("resumeText").value;
            chrome.runtime.sendMessage({ type: "uploadText", enteredText: resumeText });
            alert('Resume uploaded successfully!');
            // Revert back to initial state
            resumeButton.style.display = none
            addResumeBtn.style.display = "block";
            textBoxContainer.style.display = "none";
        }
    });
};

const closeModal = () => {
    if (modal) {
        modal.remove();
        modal = null;
    }
};
