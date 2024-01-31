const title = chrome.runtime.getManifest().name;
let selectedText = "";  // Variable to store the selected text

chrome.contextMenus.create({
    id: title,
    title: title,
    contexts: ["selection"]
});

chrome.contextMenus.onClicked.addListener((info) => {
    selectedText = info.selectionText;

    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const tab = tabs[0];
        
        // Send the selected text to the Python server
        fetch('https://keyword-search-bk9w.onrender.com/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: selectedText }),
        })
        // Send the processed text back to the chrom extension as an alert
        .then(response => response.json())
        .then(data => {
            if (data && data.processed_text) 
                alert("Processed Text: " + data.processed_text);
            else 
                alert("Error processing text.");
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Error processing text.");
        });

    });
    
    //     const tab = tabs[0];
    //     chrome.tabs.sendMessage(tab.id, { text: selectedText }, (response) => {
    //         console.log("Server Response" + response);
    //         if(response && response.processed_text){
    //             alert("Processed Text: " + response.processed_text);
    //         } else{
    //             alert("Error processing text.")
    //         }
    //     });
    // });

    // //  Send the selected text to the python server. 
    // fetch('http://localhost:8080',{
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({text: selectedText}),
    // });
    // alert("Selected Text: " + selectedText);
});

