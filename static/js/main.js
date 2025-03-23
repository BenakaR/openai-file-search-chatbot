document.addEventListener("DOMContentLoaded", function() {
    // const uploadForm = document.getElementById("upload-form");
    // const fileInput = document.getElementById("file-input");
    
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatOutput = document.getElementById("chat-box");

    // uploadForm.addEventListener("submit", function(event) {
    //     event.preventDefault();
    //     const formData = new FormData();
    //     formData.append("file", fileInput.files[0]);

    //     fetch("/upload", {
    //         method: "POST",
    //         body: formData
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         if (data.success) {
    //             alert("File uploaded successfully!");
    //         } else {
    //             alert("File upload failed.");
    //         }
    //     })
    //     .catch(error => {
    //         console.error("Error:", error);
    //     });
    // });

    chatForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const userQuery = chatInput.value;
        console.log(userQuery);
        chatOutput.innerHTML += `<div class="message user-message">${userQuery}</div>`;
        chatOutput.innerHTML += `<div class="message bot-message" id="loading"> . . . </div>`;
        chatInput.value = "";
        chatOutput.scrollTop = chatOutput.scrollHeight;
        
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userQuery })
        })
        .then(response => response.json())
        .then(data => {
            loading = document.getElementById("loading")
            chatOutput.removeChild(loading)
            chatOutput.innerHTML += `<div class="message bot-message">${data.response}</div>`;
            chatOutput.scrollTop = chatOutput.scrollHeight;
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});