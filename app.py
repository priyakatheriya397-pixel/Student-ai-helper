import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# फ्री AI मॉडल URL
HF_API_URL = "https://huggingface.co"

# चैटबॉट का पूरा डिज़ाइन (HTML) सीधे कोड के अंदर
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .chat-container { width: 90%; max-width: 400px; background: white; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; height: 80vh; }
        .chat-header { background: #007bff; color: white; padding: 15px; text-align: center; font-size: 18px; font-weight: bold; }
        .chat-box { padding: 15px; flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .message { padding: 10px; border-radius: 5px; max-width: 75%; word-wrap: break-word; font-size: 14px; }
        .user-msg { background: #007bff; color: white; align-self: flex-end; }
        .bot-msg { background: #e9ecef; color: #333; align-self: flex-start; }
        .input-area { display: flex; border-top: 1px solid #ddd; }
        .input-area input { flex: 1; padding: 15px; border: none; outline: none; font-size: 14px; }
        .input-area button { padding: 15px; background: #007bff; color: white; border: none; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">मेरा AI चैटबॉट</div>
    <div class="chat-box" id="chatBox">
        <div class="message bot-msg">नमस्ते! मैं आपकी क्या मदद कर सकता हूँ?</div>
    </div>
    <div class="input-area">
        <input type="text" id="userInput" placeholder="यहाँ अपना सवाल लिखें...">
        <button onclick="sendMessage()">भेजें</button>
    </div>
</div>

<script>
    function sendMessage() {
        let inputField = document.getElementById("userInput");
        let message = inputField.value.trim();
        if (!message) return;

        let chatBox = document.getElementById("chatBox");
        chatBox.innerHTML += `<div class="message user-msg">${message}</div>`;
        inputField.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;

        fetch('/get', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            chatBox.innerHTML += `<div class="message bot-msg">${data.response}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
</script>
</body>
</html>
"""

@app.route('/')
def home():
    # बिना किसी बाहरी HTML फाइल के सीधे स्क्रीन लोड करना
    return render_template_string(HTML_TEMPLATE)

@app.route('/get', methods=['POST'])
def bot_response():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip() if data else ""
        
        if not user_message:
            user_message = request.form.get('msg', '').strip()

        if not user_message:
            return jsonify({"response": "कृपया कुछ टाइप करें..."})

        # फ्री AI मॉडल को डेटा भेजना
        payload = {"inputs": user_message}
        response = requests.post(HF_API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                ai_response = result[0].get('generated_text', 'मैं समझ नहीं पाया।')
            elif isinstance(result, dict):
                ai_response = result.get('generated_text', 'मैं समझ नहीं पाया।')
            else:
                ai_response = "माफ़ कीजिये, अभी जवाब नहीं मिल पाया।"
        else:
            ai_response = "सर्वर अभी व्यस्त है, कृपया दोबारा प्रयास करें।"

        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"response": "सर्वर में कुछ समस्या आ रही है।"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
