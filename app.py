import os
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>मेरा असली AI चैटबॉट</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .chat-container { width: 100%; max-width: 500px; background: white; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column; height: 80vh; }
        .header { background: #007bff; color: white; padding: 15px; text-align: center; font-size: 1.2rem; font-weight: bold; }
        .chat-box { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .message { padding: 10px 15px; border-radius: 15px; max-width: 75%; word-wrap: break-word; font-size: 1rem; line-height: 1.4; }
        .user { background: #007bff; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .bot { background: #e9ecef; color: #333; align-self: flex-start; border-bottom-left-radius: 2px; }
        .input-area { display: flex; border-top: 1px solid #ddd; padding: 10px; background: #fff; }
        input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; outline: none; font-size: 1rem; }
        button { background: #007bff; color: white; border: none; padding: 10px 15px; margin-left: 5px; border-radius: 4px; cursor: pointer; font-size: 1rem; }
        button:disabled { background: #cccccc; cursor: not-allowed; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">मेरा असली AI चैटबॉट</div>
        <div class="chat-box" id="chatBox">
            <div class="message bot">नमस्ते! मैं आपका असली AI असिस्टेंट हूँ। आप मुझसे कोई भी सवाल पूछ सकते हैं।</div>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="यहाँ अपना कोई भी सवाल लिखें..." onkeypress="if(event.key === 'Enter') sendMessage()">
            <button id="sendBtn" onclick="sendMessage()">भेजें</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const sendBtn = document.getElementById('sendBtn');
            const text = input.value.trim();
            if (!text) return;

            input.disabled = true;
            sendBtn.disabled = true;

            chatBox.innerHTML += `<div class="message user">${text}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                chatBox.innerHTML += `<div class="message bot">${data.reply}</div>`;
            } catch (error) {
                chatBox.innerHTML += `<div class="message bot" style="color:red;">सर्वर से संपर्क नहीं हो पाया। कृपया पुनः प्रयास करें।</div>`;
            }
            
            input.disabled = false;
            sendBtn.disabled = false;
            input.focus();
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"reply": "कोई सवाल नहीं मिला।"}), 400

        user_message = data['message']
        
        # Pollinations का नया और सही OpenAI-compatible JSON एंडपॉइंट
        api_url = "https://pollinations.ai"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # इसमें बिना किसी चाबी (Key) के मुफ्त में चैट चलती है
        payload = {
            "model": "openai", 
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant who answers in the language chosen by the user."},
                {"role": "user", "content": user_message}
            ]
        }
        
        # रिक्वेस्ट भेज रहे हैं
        response = requests.post(api_url, json=payload, headers=headers, timeout=20)
        
        if response.status_code == 200:
            result_json = response.json()
            ai_reply = result_json['choices'][0]['message']['content']
            return jsonify({"reply": ai_reply.strip()})
        else:
            # बैकअप: अगर मुख्य सर्वर में कोई दिक्कत हो तो सीधे टेक्स्ट बेस मॉडल पर भेजें
            fallback_url = f"https://text.pollinations.ai/{user_message}?private=true"
            res = requests.get(fallback_url, timeout=15)
            if res.status_code == 200:
                return jsonify({"reply": res.text.strip()})
                
            return jsonify({"reply": "माफ़ कीजिये, फ्री एआई सर्वर अभी जवाब नहीं दे पा रहा है। थोड़ी देर में प्रयास करें।"})

    except Exception as e:
        print(f"Error Log: {str(e)}")
        return jsonify({"reply": f"बैकएंड एरर: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
