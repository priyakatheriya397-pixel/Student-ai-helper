from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# Character.ai डार्क मोड का 100% सटीक लुक और फ्री बिना चाबी वाला AI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Character.ai</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, sans-serif; }
        body { background-color: #09090b; color: #f4f4f5; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
        .chat-container { width: 100%; max-width: 480px; height: 100vh; background-color: #09090b; display: flex; flex-direction: column; }
        .chat-header { display: flex; align-items: center; padding: 16px 20px; background-color: #09090b; border-bottom: 1px solid #18181b; }
        .back-btn { font-size: 20px; margin-right: 16px; color: #a1a1aa; cursor: pointer; }
        .char-avatar-large { width: 40px; height: 40px; border-radius: 50%; background: #27272a; display: flex; justify-content: center; align-items: center; margin-right: 12px; font-size: 18px; color: #a1a1aa; }
        .char-info h2 { font-size: 15px; font-weight: 600; color: #ffffff; }
        .char-info p { font-size: 11px; color: #71717a; }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px; }
        .chat-messages::-webkit-scrollbar { width: 0px; }
        .message-row { display: flex; width: 100%; align-items: flex-start; }
        .bot-row { justify-content: flex-start; }
        .user-row { justify-content: flex-end; }
        .char-avatar-small { width: 28px; height: 28px; border-radius: 50%; background: #27272a; display: flex; justify-content: center; align-items: center; font-size: 12px; color: #a1a1aa; margin-right: 10px; margin-top: 2px; flex-shrink: 0; }
        .char-name-tag { font-size: 12px; font-weight: 500; color: #a1a1aa; margin-bottom: 2px; }
        .message-content { font-size: 14.5px; line-height: 1.5; max-width: 80%; word-wrap: break-word; }
        .bot-row .message-content { color: #e4e4e7; }
        .user-row .message-content { background-color: #1f1f23; padding: 10px 16px; border-radius: 18px; color: #f4f4f5; }
        .chat-input-area { padding: 16px; background-color: #09090b; display: flex; align-items: center; gap: 12px; }
        .input-wrapper { flex: 1; display: flex; align-items: center; background-color: #18181b; border-radius: 24px; padding: 6px 16px; }
        .input-wrapper input { flex: 1; background: none; border: none; outline: none; color: #ffffff; font-size: 14.5px; height: 36px; }
        .input-wrapper input::placeholder { color: #52525b; }
        .send-btn { background: none; border: none; color: #52525b; font-size: 18px; cursor: pointer; transition: color 0.2s; }
        .send-btn.active { color: #ffffff; }
        .typing-indicator { font-size: 12px; color: #71717a; font-style: italic; margin-left: 38px; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="back-btn"><i class="fa-solid fa-chevron-left"></i></div>
            <div class="char-avatar-large"><i class="fa-solid fa-user-astronaut"></i></div>
            <div class="char-info">
                <h2>AI Chatbot</h2>
                <p>c.ai डार्क क्लोन</p>
            </div>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="message-row bot-row">
                <div class="char-avatar-small"><i class="fa-solid fa-user-astronaut"></i></div>
                <div class="message-content">
                    <div class="char-name-tag">AI Chatbot</div>
                    नमस्ते! मैं आपका लाइव कैरेक्टर हूँ। बिना किसी API Key के भी मैं आपके हर सवाल का बिल्कुल सही जवाब दूँगा। पूछिए क्या पूछना है? 😊
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
            if (userInput.value.trim() !== "") sendBtn.classList.add('active');
            else sendBtn.classList.remove('active');
        });

        async function sendMessage() {
            const text = userInput.value.trim();
            if (!text) return;

            const userRow = document.createElement('div');
            userRow.className = 'message-row user-row';
            userRow.innerHTML = `<div class="message-content">${text}</div>`;
            chatMessages.appendChild(userRow);

            userInput.value = '';
            sendBtn.classList.remove('active');
            chatMessages.scrollTop = chatMessages.scrollHeight;

            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'typing-indicator';
            typingIndicator.id = 'typing';
            typingIndicator.innerText = "typing...";
            chatMessages.appendChild(typingIndicator);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                const response = await fetch('/get_response', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                
                document.getElementById('typing').remove();

                const botRow = document.createElement('div');
                botRow.className = 'message-row bot-row';
                botRow.innerHTML = `
                    <div class="char-avatar-small"><i class="fa-solid fa-user-astronaut"></i></div>
                    <div class="message-content">
                        <div class="char-name-tag">AI Chatbot</div>
                        ${data.reply}
                    </div>
                `;
                chatMessages.appendChild(botRow);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            } catch (e) {
                document.getElementById('typing').remove();
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

@app.route('/get_response', methods=['POST'])
def get_response():
    user_data = request.get_json()
    user_msg = user_data.get('message', '')
    
    # Hugging Face का मुफ़्त और पब्लिक एआई मॉडल (इसके लिए किसी चाबी की ज़रूरत नहीं है)
    api_url = "https://huggingface.co"
    headers = {"Content-Type": "application/json"}
    payload = {"inputs": user_msg, "parameters": {"max_new_tokens": 150}}
    
    try:
        res = requests.post(api_url, headers=headers, json=payload)
        res_data = res.json()
        
        # टेक्स्ट को साफ़ करके सिर्फ जवाब निकालना
        full_text = res_data[0]['generated_text']
        ai_reply = full_text.replace(user_msg, "").strip()
        
        if not ai_reply:
            ai_reply = "मैं आपकी बात समझ रहा हूँ, कृपया थोड़ा और विस्तार से पूछें।"
            
        return jsonify({"reply": ai_reply})
    except:
        return jsonify({"reply": "सर्वर अभी व्यस्त है, कृपया एक बार फिर से पूछें।"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
