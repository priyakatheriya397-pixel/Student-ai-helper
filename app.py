import os
import requests
import urllib.parse  # यूआरएल में स्पेस फिक्स करने के लिए
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

            // इनपुट और बटन को डिसेबल करें ताकि डबल क्लिक न हो
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
            
            // दोबारा इनेबल करें
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
        
        # यूआरएल में स्पेस या स्पेशल कैरेक्टर्स को एनकोड करना (ताकि सर्वर क्रैश न हो)
        encoded_message = urllib.parse.quote(user_message)
        
        # 1. पहला फ्री AI इंजन (Pollinations Text)
        api_url = f"https://pollinations.ai{encoded_message}?model=openai"
        
        try:
            response = requests.get(api_url, timeout=15)
            if response.status_code == 200 and response.text.strip():
                return jsonify({"reply": response.text.strip()})
        except Exception:
            pass # अगर पहला डाउन है, तो दूसरे पर जाएगा

        # 2. बैकअप फ्री AI इंजन (अगर पहला काम न करे)
        backup_url = f"https://pollinations.ai{encoded_message}?model=mistral"
        response = requests.get(backup_url, timeout=15)
        
        if response.status_code == 200 and response.text.strip():
            return jsonify({"reply": response.text.strip()})
        else:
            return jsonify({"reply": "माफ़ कीजिये, अभी कोई भी फ्री सर्वर रिस्पॉन्ड नहीं कर रहा है। थोड़ी देर बाद प्रयास करें।"})

    except Exception as e:
        print(f"Error Log: {str(e)}")
        return jsonify({"reply": "बैकएंड में कोई तकनीकी समस्या आई है।"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
