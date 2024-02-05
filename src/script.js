const title = chrome.runtime.getManifest().name;
// const API_ROUTE = "https://skill-search-c5xg7z7jka-uc.a.run.app/?{";
const API_ROUTE = "http://127.0.0.1:8080";

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

        // Send the selected text to the Python server
        fetch(API_ROUTE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: selectedText }),
        })
        // Send the processed text back to the chrome extension as an alert
        .then(response => response.json())
        .then(data => {
            if (data && data.processed_text) {
                console.log("Processed Text:", data.processed_text);
                // alert("Processed Text: " + data.processed_text); 
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