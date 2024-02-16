let modal;

chrome.runtime.onMessage.addListener((request) => {
    if (request.type === 'popup-modal') {
        console.log("Received message to show modal. Processed Text:", request.processedText);
        showModal(request.processedText);
    }
});

chrome.runtime.onMessage.addListener((request) => {
    if (request.type === 'match-display') {
        //display request.Status in the modal as a text display
        displayMatchText(request.text)
    }
});

const displayMatchText = (matchText) => {
    const matchTextContainer = modal.querySelector(".match-text-container");
    matchTextContainer.textContent = matchText;

    // Append the matchTextContainer to the modal content
    // modal.querySelector(".modal-content").appendChild(matchTextContainer);
};

const showModal = (processedText) => {
    console.log("Showing modal with processed text:", processedText);

    if (modal) {
        modal.style.display = "none";
    }
    
    modal = document.createElement("div");
    modal.classList.add("modal");

    modal.innerHTML = `
        <div class="modal-content">
            <div style="font-size: 16px; margin-bottom: 20px; line-height: 1.5; color: #333;">${processedText.replace('Experience:', '<br>Experience:').replace('Education:', '<br>Education:')}</div>
            <div class="match-text-container" style="margin-bottom: 10px;"></div> 
            <button class="add-resume-btn">Add Resume</button>
            <div class="text-box-container" style="display: none;">
                <textarea id="resumeText" rows="4" cols="50" style="width: 100%;" placeholder="Enter your resume text here..."></textarea>
                <button class="upload-btn">Upload</button>
            </div>
            <button class="close-btn">Close</button>
        </div>
    `;

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
      `
    );

    modal.querySelector(".modal-content").setAttribute(
        "style", `
        background-color: #fefefe;
        padding: 20px;
        border: 1px solid #888;
        border-radius: 0; /* Square corners */
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

    closeBtn.addEventListener("click", () => {
        console.log("Closing modal");
        modal.style.display = "none";
    });

    addResumeBtn.addEventListener("click", () => {
        console.log("Adding resume");
        addResumeBtn.style.display = "none";
        textBoxContainer.style.display = "block";
    });

    uploadBtn.addEventListener("click", () => {
        console.log("Uploading resume");
        const resumeText = document.getElementById("resumeText").value;
        chrome.runtime.sendMessage({ type: "uploadText", enteredText: resumeText });
        alert('Resume uploaded successfully!');
        // Revert back to initial state
        addResumeBtn.style.display = "block";
        textBoxContainer.style.display = "none";
    });

    // Prevent modal from closing when clicking outside
    modal.addEventListener("click", (event) => {
        if (event.target === modal) {
            event.stopPropagation();
        }
    });
};
