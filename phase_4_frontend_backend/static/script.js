const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const disclaimer = document.querySelector('.disclaimer');

// Fetch last updated time
async function checkLastUpdated() {
    try {
        const response = await fetch('last_updated.txt');
        if (response.ok) {
            const timestamp = await response.text();
            disclaimer.innerText = `Facts-only. No investment advice. Last updated: ${timestamp}`;
        }
    } catch (e) {
        console.log("Could not fetch last updated time");
    }
}
checkLastUpdated();

userInput.addEventListener('input', () => {
    if (userInput.value.trim() !== "") {
        sendBtn.classList.add('active');
    } else {
        sendBtn.classList.remove('active');
    }
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    appendMessage('user', text);
    userInput.value = "";
    sendBtn.classList.remove('active');

    // Show typing indicator or simplistic loading
    const loadingId = appendMessage('bot', '...', true);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: text })
        });
        const data = await response.json();
        updateMessage(loadingId, data.response);
    } catch (error) {
        updateMessage(loadingId, 'Sorry, something went wrong. Please try again.');
    }
}

function sendSuggestion(text) {
    userInput.value = text;
    sendMessage();
}

function appendMessage(sender, text, isLoading = false) {
    const id = Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    msgDiv.id = `msg-${id}`;

    const avatar = document.createElement('div');
    avatar.className = 'avatar-small';
    avatar.innerText = sender === 'bot' ? '🤖' : '👤';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = `<p>${formatResponse(text)}</p>`;

    msgDiv.appendChild(avatar);
    msgDiv.appendChild(contentDiv);
    chatMessages.appendChild(msgDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;
    return id;
}

function updateMessage(id, text) {
    const msgDiv = document.getElementById(`msg-${id}`);
    if (msgDiv) {
        const content = msgDiv.querySelector('.message-content p');
        content.innerHTML = formatResponse(text);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function formatResponse(text) {
    if (!text) return "";
    // Regular expression to match URLs more robustly
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    let formatted = text.replace(urlRegex, (url) => {
        // Remove trailing punctuation from URL that might be part of the sentence
        const cleanUrl = url.replace(/[.,!?;:]+$/, "");
        return `<a href="${cleanUrl}" target="_blank" class="chat-link" rel="noopener noreferrer">${cleanUrl}</a>`;
    });
    // Replace newlines with <br>
    return formatted.replace(/\n/g, '<br>');
}
