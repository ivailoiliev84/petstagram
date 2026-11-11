
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");
const sendButton = document.getElementById("send-button");
const chatToggle = document.getElementById("chat-toggle");
const chatClose = document.getElementById("chat-close");
const chatWidget = document.getElementById("chat-widget");

const csrfToken = chatForm.querySelector(
    "[name=csrfmiddlewaretoken]"
).value;

let conversationId = null;
let isSending = false;

function appendMessage(role, content) {
    const messageElement = document.createElement("div");

    messageElement.classList.add("chat-message", role);

    // Prevent HTML injection from message content
    messageElement.textContent = content;

    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatToggle.addEventListener("click", () => {
    chatWidget.hidden = !chatWidget.hidden;

    chatToggle.setAttribute(
        "aria-expanded",
        String(!chatWidget.hidden)
    );

    if (!chatWidget.hidden) {
        chatInput.focus();
    }
});

chatClose.addEventListener("click", () => {
    chatWidget.hidden = true;
    chatToggle.setAttribute("aria-expanded", "false");
    chatToggle.focus();
});

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (isSending) return;

    const message = chatInput.value.trim();

    if (!message) return;

    isSending = true;
    sendButton.disabled = true;

    appendMessage("user", message);
    chatInput.value = "";

    try {
        const response = await fetch("/chatbot/api/messages/", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                message: message,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Request failed");
        }

        conversationId = data.conversation_id;

        appendMessage("assistant", data.content);

    } catch (error) {
        appendMessage("error", error.message);
    } finally {
        isSending = false;
        sendButton.disabled = false;
        chatInput.focus();
    }
});
