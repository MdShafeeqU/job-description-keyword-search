// script.js (Background Script)

const title = chrome.runtime.getManifest().name;
const API_ROUTE = "http://127.0.0.1:8080";
let extracted_keywords;

chrome.contextMenus.create({
    id: title,
    title: title,
    contexts: ["selection"]
});

chrome.contextMenus.onClicked.addListener((info) => {
    selectedText = info.selectionText;

    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const tab = tabs[0];
        console.log("Selected Text:", selectedText);

        fetch(API_ROUTE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: selectedText }),
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.processed_text) {
                console.log("Processed Text:", data.processed_text);
                extracted_keywords = data.processed_text;
                chrome.tabs.sendMessage(tab.id, { type: "popup-modal", processedText: data.processed_text });
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
});

// Message listener to handle resume upload
chrome.runtime.onMessage.addListener((request) => {
    if (request.type === "uploadText") {
        // Save entered text to local storage
        chrome.storage.local.set({ 'enteredText': request.enteredText }, () => {
            console.log(request.enteredText);
        });

        // chrome.storage.local.get('enteredText', function(result) {
        //     const enteredText = result.enteredText;
        //     console.log('Entered text retrieved:', enteredText);
        // });
    }
});

chrome.runtime.onMessage.addListener((request) => {
    if (request.type === "matchResume") {
        chrome.storage.local.get('enteredText', function(result) {
            const enteredText = result.enteredText;
            console.log('Entered text retrieved:', enteredText);
            console.log("Extracted keywords: ", extracted_keywords)
            fetch("http://127.0.0.1:8080/match",{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({resumeText: enteredText, extractedKeywords: extracted_keywords}),
            })
            .then(response => response.json())
            .then(data => {
                console.log("Server response: ", data);
            })
            .catch(error =>{
                console.error("Fetch Error: ", error);
            });
        });
    }
});