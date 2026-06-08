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
        
        # 1. DuckDuckGo AI की टोकन सर्विस से वरीफिकेशन पास प्राप्त करना
        status_url = "https://duckduckgo.com"
        headers = {"x-vqd-accept": "1", "User-Agent": "Mozilla/5.0"}
        
        status_res = requests.get(status_url, headers=headers, timeout=10)
        vqd_token = status_res.headers.get("x-vqd-token")
        
        if not vqd_token:
            return jsonify({"reply": "सर्वर गेटवे टोकन नहीं बना सका। कृपया पुनः प्रयास करें।"})

        # 2. एआई चैट सर्विस को डेटा पोस्ट करना (Llama-3 मॉडल का उपयोग)
        chat_url = "https://duckduckgo.com"
        chat_headers = {
            "x-vqd-token": vqd_token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        
        payload = {
            "model": "meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
            "messages": [{"role": "user", "content": user_message}]
        }
        
        # सरलीकृत और सटीक स्ट्रीमिंग रिस्पॉन्स पार्सिंग
        response = requests.post(chat_url, json=payload, headers=chat_headers, timeout=15)
        
        if response.status_code == 200:
            full_reply = ""
            # DuckDuckGo डेटा को Server-Sent Events (SSE) में भेजता है, उसे यहाँ जोड़ रहे हैं
            for line in response.text.splitlines():
                if line.startswith("data:"):
                    data_content = line[5:].strip()
                    if data_content == "[DONE]":
                        break
                    # टेक्स्ट चंक्स को साफ़ करना
                    if '"message":"' in data_content:
                        try:
                            # सिंपल स्ट्रिंग स्लाइसिंग द्वारा टेक्स्ट निकालना ताकि JSON क्रैश न हो
                            part = data_content.split('"message":"')[1].split('"')[0]
                            # एस्केप कैरेक्टर्स को ठीक करना
                            part = part.encode().decode('unicode_escape')
                            full_reply += part
                        except Exception:
                            pass
            
            if full_reply.strip():
                return jsonify({"reply": full_reply.strip()})
                
        # 3. अंतिम बैकअप (अगर DuckDuckGo भी ब्लॉक करे)
        fallback_res = requests.get(f"https://pollinations.ai{user_message}?model=mistral", timeout=10)
        if fallback_res.status_code == 200:
            return jsonify({"reply": fallback_res.text.strip()})

        return jsonify({"reply": "माफ़ कीजिये, सभी फ्री सर्वर अभी व्यस्त हैं। कृपया 1 मिनट बाद पुनः प्रयास करें।"})

    except Exception as e:
        return jsonify({"reply": f"तकनीकी त्रुटि: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
