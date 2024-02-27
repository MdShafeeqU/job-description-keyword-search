const title = chrome.runtime.getManifest().name;
// const API_ROUTE = "https://skill-search-c5xg7z7jka-uc.a.run.app/?{";
const API_ROUTE = "http://127.0.0.1:8080";

chrome.contextMenus.create({
    id: title,
    title: title,
    contexts: ["selection"]
});

let selectedText; // Declare selectedText globally

// Define a function to process text and display modal
const processAndDisplayModal = (text, resumeText) => {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const tab = tabs[0];
        console.log("Selected Text:", text);

        chrome.tabs.sendMessage(tab.id, { type: "loading-modal", processedText: "" });
        fetch(API_ROUTE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text, resumeText: resumeText }),
        })
        // Send the processed text back to the chrome extension
        .then(response => response.json())
        .then(data => {
            if (data) {
                chrome.tabs.sendMessage(tab.id, { type: "popup-modal", processedText: data.jd_keywords });
                if(resumeText){
                    chrome.tabs.sendMessage(tab.id, { type: "match-display", text: data.resume_match });
                }
            } else {
                console.error("Error processing text. Data:", data);
                alert("Error processing text.");
            }
        })
        .catch(error => {
            console.error("Fetch Error:", error);
            alert("Error processing text.");
        });
    });
};

// Context menu click listener
chrome.contextMenus.onClicked.addListener((info) => {
    selectedText = info.selectionText; // Set selectedText globally

    // Check if data is available in Chrome local storage
    chrome.storage.local.get('enteredText', function(result) {
        const resumeText = result.enteredText !== undefined ? result.enteredText : null;
        console.log("Stored resume:", resumeText);

        // Process and display modal
        processAndDisplayModal(selectedText, resumeText);
    });
});

// Message listener to handle resume upload
chrome.runtime.onMessage.addListener((request) => {
    if (request.type === "uploadText") {
        // Save entered text to local storage
        chrome.storage.local.set({ 'enteredText': request.enteredText }, () => {
            console.log(request.enteredText);
            
            // Process and display modal after resume is uploaded
            processAndDisplayModal(selectedText, request.enteredText);
        });
    }
});