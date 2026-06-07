from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Character.ai का बिल्कुल सटीक मोबाइल ऐप इंटरफ़ेस
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Character.ai Clone</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: #18181c; color: #f3f3f3; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .chat-container { width: 100%; max-width: 550px; height: 100vh; background-color: #121214; display: flex; flex-direction: column; }
        .chat-header { display: flex; align-items: center; padding: 14px 20px; background-color: #18181c; border-bottom: 1px solid #232329; }
        .back-btn { font-size: 18px; margin-right: 18px; color: #939399; cursor: pointer; }
        .char-avatar-large { width: 45px; height: 45px; border-radius: 50%; background: linear-gradient(135deg, #8a2be2, #4a00e0); display: flex; justify-content: center; align-items: center; margin-right: 14px; font-size: 22px; color: #fff; }
        .char-info h2 { font-size: 16px; font-weight: 600; color: #ffffff; }
        .char-info p { font-size: 12px; color: #939399; margin-top: 2px; }
        .chat-messages { flex: 1; padding: 24px 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; }
        .chat-messages::-webkit-scrollbar { width: 0px; }
        .message-row { display: flex; width: 100%; align-items: flex-start; }
        .bot-row { justify-content: flex-start; }
        .user-row { justify-content: flex-end; }
        .char-avatar-small { width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #8a2be2, #4a00e0); display: flex; justify-content: center; align-items: center; font-size: 14px; color: #fff; margin-right: 12px; flex-shrink: 0; }
        .message-content { font-size: 15px; line-height: 1.6; max-width: 82%; word-wrap: break-word; color: #e3e3e6; }
        .char-name-tag { font-size: 13px; font-weight: 600; color: #ffffff; margin-bottom: 4px; }
        .user-row .message-content { background-color: #202024; padding: 10px 16px; border-radius: 16px; border-bottom-right-radius: 4px; }
        .chat-input-area { padding: 20px; background-color: #121214; display: flex; align-items: center; justify-content: center; }
        .input-wrapper { width: 100%; display: flex; align-items: center; background-color: #202024; border: 1px solid #2d2d34; border-radius: 26px; padding: 6px 18px; }
        .input-wrapper input { flex: 1; background: none; border: none; outline: none; color: #ffffff; font-size: 15px; height: 38px; }
        .send-btn { background: none; border: none; color: #939399; font-size: 18px; cursor: pointer; margin-left: 10px; }
        .send-btn.active { color: #ffffff; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="back-btn"><i class="fa-solid fa-chevron-left"></i></div>
            <div class="char-avatar-large"><i class="fa-solid fa-ghost"></i></div>
            <div class="char-info">
                <h2>AI Chatbot</h2>
                <p>@ansh_tutor द्वारा निर्मित</p>
            </div>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="message-row bot-row">
                <div class="char-avatar-small"><i class="fa-solid fa-ghost"></i></div>
                <div class="message-content">
                    <div class="char-name-tag">AI Chatbot</div>
                    नमस्ते! मैं आपका नया कैरेक्टर असिस्टेंट हूँ। मेरा रूप-रंग अब बिल्कुल असली Character.ai जैसा है। 😊
                </div>
            </div>
        </div>
        <div class="chat-input-area">
            <div class="input-wrapper">
                <input type="text" id="userInput" placeholder="Type a message..." autocomplete="off">
                <button class="send-btn" id="sendBtn"><i class="fa-solid fa-paper-plane"></i></button>
            </div>
        </div>
    </div>
    <script>
        const chatMessages = document.getElementById('chatMessages');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');

        userInput.addEventListener('input', () => {
            if(userInput.value.trim() !== "") sendBtn.classList.add('active');
            else sendBtn.classList.remove('active');
        });

        function sendMessage() {
            const text = userInput.value.trim();
            if (!text) return;

            const userRow = document.createElement('div');
            userRow.className = 'message-row user-row';
            userRow.innerHTML = `<div class="message-content">${text}</div>`;
            chatMessages.appendChild(userRow);

            userInput.value = '';
            sendBtn.classList.remove('active');
            chatMessages.scrollTop = chatMessages.scrollHeight;

            setTimeout(() => {
                const botRow = document.createElement('div');
                botRow.className = 'message-row bot-row';
                botRow.innerHTML = `
                    <div class="char-avatar-small"><i class="fa-solid fa-ghost"></i></div>
                    <div class="message-content">
                        <div class="char-name-tag">AI Chatbot</div>
                        नया Character.ai डिज़ाइन पूरी तरह काम कर रहा है! 👍
                    </div>
                `;
                chatMessages.appendChild(botRow);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1000);
        }
        sendBtn.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
