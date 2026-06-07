import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

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
    return render_template_string(HTML_TEMPLATE)

@app.route('/get', methods=['POST'])
def bot_response():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip().lower() if data else ""
        
        if not user_message:
            user_message = request.form.get('msg', '').strip().lower()

        if not user_message:
            return jsonify({"response": "कृपया कुछ टाइप करें..."})

        # यहाँ बोट के खुद के स्मार्ट जवाब सेट हैं (बिना किसी API के)
        if "what is ai" in user_message or "ai kya hai" in user_message:
            ai_response = "AI (Artificial Intelligence) यानी कृत्रिम बुद्धिमत्ता, कंप्यूटर को इंसानों की तरह सोचने और सीखने की शक्ति देती है।"
        elif "hello" in user_message or "hi" in user_message or "नमस्ते" in user_message:
            ai_response = "नमस्ते! मैं आपका पर्सनल चैटबॉट हूँ। आज मैं आपकी क्या सहायता कर सकता हूँ?"
        elif "how are you" in user_message or "kaise ho" in user_message:
            ai_response = "मैं बिल्कुल ठीक हूँ! आप बताइए, आपका दिन कैसा चल रहा है?"
        elif "your name" in user_message or "naam kya hai" in user_message:
            ai_response = "मेरा नाम 'मेरा AI चैटबॉट' है, जिसे पाइथन और फ्लास्क की मदद से बनाया गया है।"
        elif "thank" in user_message or "shukriya" in user_message:
            ai_response = "आपका स्वागत है! अगर कोई और सवाल हो तो ज़रूर पूछें।"
        else:
            ai_response = f"आपने पूछा: '{user_message}'। बिना API Key के मैं अभी सिर्फ मुख्य सवालों के जवाब दे सकता हूँ। आप मुझसे 'What is AI' या 'Hi' पूछकर टेस्ट कर सकते हैं!"

        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"response": "सर्वर के अंदर कुछ गड़बड़ हुई है।"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
