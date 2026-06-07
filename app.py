from flask import Flask, render_template_string
import os

app = Flask(__name__)

# character.ai जैसा 100% ब्लैक स्क्रीन चैट UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, sans-serif; }
        body { background-color: #000000; color: #ffffff; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .chat-container { width: 100%; max-width: 450px; height: 100vh; background-color: #050505; display: flex; flex-direction: column; }
        .chat-header { display: flex; align-items: center; padding: 15px; background-color: #0a0a0a; border-bottom: 1px solid #1a1a1a; }
        .avatar { width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(45deg, #ff0055, #00ff55); display: flex; justify-content: center; align-items: center; margin-right: 12px; }
        .user-info h2 { font-size: 16px; font-weight: 600; }
        .user-info p { font-size: 11px; color: #888; }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .message { max-width: 80%; padding: 12px 16px; border-radius: 18px; font-size: 14px; }
        .bot-message { background-color: #1a1a1a; color: #ffffff; align-self: flex-start; }
        .user-message { background-color: #2a2a2a; color: #ffffff; align-self: flex-end; }
        .chat-input-area { padding: 15px; background-color: #000000; display: flex; align-items: center; gap: 10px; border-top: 1px solid #1a1a1a; }
        .input-wrapper { flex: 1; display: flex; align-items: center; background-color: #151515; border-radius: 25px; padding: 8px 15px; }
        .input-wrapper input { flex: 1; background: none; border: none; outline: none; color: #ffffff; font-size: 15px; }
        .send-btn { background: none; border: none; color: #0084ff; font-weight: 600; font-size: 20px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="user-info">
                <h2>AI Chatbot</h2>
                <p>Character.ai Style 🔥</p>
            </div>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="message bot-message">नमस्ते! अब आपका पुराना पेज पूरी तरह हट चुका है। यह नया ब्लैक चैट स्क्रीन है। 😊</div>
        </div>
        <div class="chat-input-area">
            <div class="input-wrapper">
                <input type="text" id="userInput" placeholder="Message..." autocomplete="off">
            </div>
            <button class="send-btn" id="sendBtn"><i class="fa-solid fa-paper-plane"></i></button>
        </div>
    </div>
    <script>
        const chatMessages = document.getElementById('chatMessages');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');

        function sendMessage() {
            const text = userInput.value.trim();
            if (!text) return;
            const userDiv = document.createElement('div');
            userDiv.className = 'message user-message';
            userDiv.innerText = text;
            chatMessages.appendChild(userDiv);
            userInput.value = '';
            chatMessages.scrollTop = chatMessages.scrollHeight;

            setTimeout(() => {
                const botDiv = document.createElement('div');
                botDiv.className = 'message bot-message';
                botDiv.innerText = "नया कस्टमाइज्ड सर्वर पूरी तरह एक्टिव है!";
                chatMessages.appendChild(botDiv);
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
    
