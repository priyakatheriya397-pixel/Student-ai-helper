from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# गूगल जेमिनी एआई को सेटअप करें (Free API Key)
# ध्यान दें: अपनी Google AI Studio से मिली API Key यहाँ डालें
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY_HERE" 
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

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
        .avatar i { font-size: 20px; color: #fff; }
        .user-info h2 { font-size: 16px; font-weight: 600; }
        .user-info p { font-size: 11px; color: #888; }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .chat-messages::-webkit-scrollbar { width: 0px; }
        .message { max-width: 80%; padding: 12px 16px; border-radius: 18px; font-size: 14px; line-height: 1.5; word-wrap: break-word; }
        .bot-message { background-color: #1a1a1a; color: #ffffff; align-self: flex-start; border-bottom-left-radius: 4px; }
        .user-message { background-color: #2a2a2a; color: #ffffff; align-self: flex-end; border-bottom-right-radius: 4px; }
        .chat-input-area { padding: 15px; background-color: #000000; display: flex; align-items: center; gap: 10px; border-top: 1px solid #1a1a1a; }
        .input-wrapper { flex: 1; display: flex; align-items: center; background-color: #151515; border-radius: 25px; padding: 8px 15px; }
        .input-wrapper input { flex: 1; background: none; border: none; outline: none; color: #ffffff; font-size: 15px; }
        .send-btn { background: none; border: none; color: #0084ff; font-weight: 600; font-size: 20px; cursor: pointer; }
        .typing { color: #888; font-style: italic; font-size: 12px; align-self: flex-start; }
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
            <div class="message bot-message">नमस्ते! मैं अब पूरी तरह तैयार हूँ। मुझसे कोई भी सवाल पूछिए! 😊</div>
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

        async function sendMessage() {
            const text = userInput.value.trim();
            if (!text) return;

            // यूजर का मैसेज दिखाएं
            const userDiv = document.createElement('div');
            userDiv.className = 'message user-message';
            userDiv.innerText = text;
            chatMessages.appendChild(userDiv);
            userInput.value = '';
            chatMessages.scrollTop = chatMessages.scrollHeight;

            // 'Typing...' इंडिकेटर दिखाएं
            const typingDiv = document.createElement('div');
            typingDiv.className = 'typing';
            typingDiv.id = 'typingIndicator';
            typingDiv.innerText = "AI सोच रहा है...";
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                // बैकएंड पाइथन सर्वर को मैसेज भेजें
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                
                // इंडिकेटर हटाएं
                document.getElementById('typingIndicator').remove();

                // असली AI का जवाब दिखाएं
                const botDiv = document.createElement('div');
                botDiv.className = 'message bot-message';
                botDiv.innerText = data.reply;
                chatMessages.appendChild(botDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            } catch (error) {
                document.getElementById('typingIndicator').remove();
                alert("कुछ गड़बड़ हुई, कृपया दोबारा प्रयास करें।");
            }
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

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    try:
        # असली गूगल जेमिनी से जवाब मंगाना
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "माफ़ कीजिये, मैं अभी जवाब नहीं दे पा रहा हूँ।"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
