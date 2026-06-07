from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# आपका पसंदीदा ब्लैक स्क्रीन चैट UI सीधे Python के अंदर
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot Helper</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: #0b0c10; color: #ffffff; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .chat-container { width: 100%; max-width: 450px; height: 100vh; background-color: #000000; display: flex; flex-direction: column; position: relative; }
        .chat-header { display: flex; align-items: center; padding: 15px; background-color: #0b0c10; border-bottom: 1px solid #1f2833; }
        .back-btn { font-size: 20px; margin-right: 15px; color: #ffffff; cursor: pointer; }
        .avatar { width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(45deg, #f06, #9f4); display: flex; justify-content: center; align-items: center; margin-right: 12px; }
        .avatar i { font-size: 20px; color: #fff; }
        .user-info h2 { font-size: 16px; font-weight: 600; }
        .user-info p { font-size: 11px; color: #8c8c8c; }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .chat-messages::-webkit-scrollbar { width: 0px; }
        .message { max-width: 80%; padding: 12px 16px; border-radius: 18px; font-size: 14px; line-height: 1.5; word-wrap: break-word; }
        .bot-message { background-color: #1c1c1e; color: #ffffff; align-self: flex-start; border-bottom-left-radius: 4px; }
        .user-message { background-color: #262629; color: #ffffff; align-self: flex-end; border-bottom-right-radius: 4px; }
        .chat-input-area { padding: 15px; background-color: #000000; display: flex; align-items: center; gap: 10px; border-top: 1px solid #1f2833; }
        .input-wrapper { flex: 1; display: flex; align-items: center; background-color: #1c1c1e; border-radius: 25px; padding: 8px 15px; }
        .input-wrapper input { flex: 1; background: none; border: none; outline: none; color: #ffffff; font-size: 15px; padding: 5px 0; }
        .input-wrapper input::placeholder { color: #727477; }
        .icon-btn { background: none; border: none; color: #a4a4a4; font-size: 18px; cursor: pointer; }
        .send-btn { color: #3897f0; font-weight: 600; font-size: 20px; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="back-btn"><i class="fa-solid fa-arrow-left"></i></div>
            <div class="avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="user-info">
                <h2>AI Chatbot</h2>
                <p>Always active! 🔥</p>
            </div>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="message bot-message">नमस्ते! मैं आपका नया एआई असिस्टेंट हूँ। अब पुराना पेज पूरी तरह हट चुका है। बताइए क्या मदद करूँ? 😊</div>
        </div>
        <div class="chat-input-area">
            <button class="icon-btn"><i class="fa-regular fa-image"></i></button>
            <div class="input-wrapper">
                <input type="text" id="userInput" placeholder="Message..." autocomplete="off">
                <button class="icon-btn"><i class="fa-regular fa-face-smile"></i></button>
            </div>
            <button class="icon-btn send-btn" id="sendBtn"><i class="fa-solid fa-paper-plane"></i></button>
        </div>
    </div>
    <script>
        const chatMessages = document.getElementById('chatMessages');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');

        function sendMessage() {
            const text = userInput.value.trim();
            if (text === '') return;

            const userDiv = document.createElement('div');
            userDiv.className = 'message user-message';
            userDiv.innerText = text;
            chatMessages.appendChild(userDiv);
            userInput.value = '';
            chatMessages.scrollTop = chatMessages.scrollHeight;

            setTimeout(() => {
                const botDiv = document.createElement('div');
                botDiv.className = 'message bot-message';
                botDiv.innerText = "आपका नया पाइथन बैकएंड सही से काम कर रहा है! 👍";
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
    # यह सीधे ऊपर दिए गए HTML टेम्पलेट को स्क्रीन पर भेजेगा
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    # Render के पोर्ट एनवायरनमेंट को सेट करने के लिए
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
