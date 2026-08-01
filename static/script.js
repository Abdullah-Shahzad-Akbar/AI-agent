// Get the input element
const input = document.getElementById("message");
const sendbutton = document.getElementById("send-btn")

const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");

uploadBtn.addEventListener("click", () => {
    fileInput.click();
});
fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        console.log(fileInput.files[0].name);
    }
});

async function sendMessage() {

    // Get the user's message
    const message = input.value;

    // Don't send empty messages
    if (
        message.trim() === "" &&
        fileInput.files.length === 0
    ) {
        return;
    }
    // Clear the input box
    input.value = "";

    // Display the user's message
    const chat = document.getElementById("chat");
    const userDiv = document.createElement("div");
    userDiv.className = "user-message";
    userDiv.textContent = message;
    chat.appendChild(userDiv);
    chat.scrollTop = chat.scrollHeight;

    // Send the message to FastAPI
    
    const formData = new FormData();

    formData.append("message", message);

    if (fileInput.files.length > 0) {
        formData.append("file", fileInput.files[0]);
    }

    const response = await fetch("/chat", {
        method: "POST",
        body: formData
    });
    if (response.status === 401) {
    window.location.href = "/login";
    return;
    }
    if (!response.ok) {
    console.error("Server Error");
    return;
    }
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullText = "";
    // const response = await fetch("/chat", {
    //     method: "POST",
    //     headers: {
    //         "Content-Type": "application/json"
    //     },
    //     body: JSON.stringify({
    //         message: message,
    //     })
    // });

    // Read the JSON response
    // const data = await response.json();
    // Display the AI's reply
    marked.setOptions({
        breaks: true,
        gfm: true
    });
    // const aiDiv = document.createElement("div");
    // aiDiv.className = "ai-message";
    // const html = marked.parse(data.answer);
    // aiDiv.innerHTML = DOMPurify.sanitize(html);
    // chat.appendChild(aiDiv);
    // input.focus();
    chat.scrollTop = chat.scrollHeight;
    const aiDiv = document.createElement("div");
    aiDiv.className = "ai-message";
    chat.appendChild(aiDiv);
    while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        fullText += decoder.decode(value, { stream: true });

        const html = marked.parse(fullText);
        aiDiv.innerHTML = DOMPurify.sanitize(html);

        chat.scrollTop = chat.scrollHeight;
    }
    fullText += decoder.decode();
    fileInput.value = "";
    input.focus();
}

sendbutton.addEventListener("click", sendMessage);
input.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent any default behavior
        sendMessage();
    }
});