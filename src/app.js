// content_script.js
chrome.runtime.onMessage.addListener((request) => {
    if (request.type === 'popup-modal') {
        console.log("Received message to show modal. Processed Text:", request.processedText);
        showModal(request.processedText);
    }
});

const showModal = (processedText) => {
    console.log("Showing modal with processed text:", processedText);

    const modal = document.createElement("dialog");
    modal.setAttribute(
        "style",`
        height:450px;
        border: none;
        top:150px;
        border-radius:20px;
        background-color:white;
        position: fixed; box-shadow: 0px 12px 48px rgba(29, 5, 64, 0.32);
        `
    );
    
    modal.innerHTML = `
        <div>${processedText}</div>
        <button style="padding: 8px 12px; font-size: 16px; border: none; border-radius: 20px;">Close</button>
    `;
    
    document.body.appendChild(modal);
    
    const dialog = document.querySelector("dialog");
    dialog.showModal();
    
    dialog.querySelector("button").addEventListener("click", () => {
        console.log("Closing modal");
        dialog.close();
    });
};