const title = chrome.runtime.getManifest().name;
let selectedText = "";  // Variable to store the selected text

chrome.contextMenus.create({
    id: title,
    title: title,
    contexts: ["selection"]
});

chrome.contextMenus.onClicked.addListener((info) => {
    selectedText = info.selectionText;

    alert("Selected Text: " + selectedText);
});

